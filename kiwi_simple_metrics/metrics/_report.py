import urllib.parse
from dataclasses import dataclass
from typing import Any, Callable, Iterator, Self

import requests

from ..settings import SETTINGS, MetricSettings


@dataclass(slots=True, kw_only=True)
class ReportData:
    name: str
    value: float
    threshold: float
    inverted: bool
    format: str

    @classmethod
    def from_settings(
        cls, *,
        name: str,
        value: float,
        settings: MetricSettings,
    ) -> Self:
        return cls(
            name=name,
            value=value,
            threshold=settings.threshold,
            inverted=settings.inverted,
            format=settings.report,
        )

    @classmethod
    def from_free_total(
        cls, *,
        name: str,
        free: float,
        total: float,
        settings: MetricSettings,

    ) -> Self:
        return cls.from_settings(
            name=name,
            value=(total - free) / total * 100,
            settings=settings,
        )

    @property
    def report(self) -> "Report":
        return Report(
            result=self.format.format(
                name=self.name,
                value=self.value,
            ),
            failed=(
                self.value > self.threshold and not self.inverted
                or self.value < self.threshold and self.inverted
            ),
        )


@dataclass(slots=True, kw_only=True, frozen=True)
class Report:
    result: str
    failed: bool = False

    def __str__(self) -> str:
        state = "OK" if not self.failed else "FAIL"

        return SETTINGS.log.format.format(
            state=state,
            result=self.result,
        )

    @classmethod
    def summary(cls, *_reports: Any) -> Self:
        reports = [
            report
            for report in _reports
            if isinstance(report, Report)
        ]

        return cls(
            result=SETTINGS.separator.join(
                report.result
                for report in reports
            ),
            failed=any(
                report.failed
                for report in reports
            ),
        )

    @classmethod
    def aggregate(
        cls, *,
        settings: MetricSettings,
        get_data: Callable[[], Iterator[ReportData]],
    ) -> Self | None:
        if not settings.enabled:
            return None

        reports = [data.report for data in get_data()]

        return cls(
            result=settings.report_outer.format(
                name=settings.name,
                inner=SETTINGS.separator.join(
                    report.result
                    for report in reports[:settings.count]
                ),
            ),
            failed=any(
                report.failed
                for report in reports
            ),
        )

    def push_webhook(self) -> None:
        if (url := SETTINGS.webhook.url if not self.failed
                else SETTINGS.webhook.fail) is None:
            return

        requests.get(
            url=str(url).format(
                urllib.parse.quote_plus(self.result)
            ),
            verify=not SETTINGS.webhook.insecure,
        )
