from dataclasses import dataclass
from typing import Any, Callable, Iterator, Self

from ..settings import MetricSettings


@dataclass(slots=True, kw_only=True)
class ReportData:
    name: str
    value: float

    @classmethod
    def from_free_total(cls, *, name: str, free: float, total: float) -> Self:
        return cls(
            name=name,
            value=(total - free) / total * 100,
        )

    def report(self, settings: MetricSettings) -> "Report":
        return Report(
            result=settings.report.format(
                name=self.name,
                value=self.value,
            ),
            failed=(
                self.value > settings.threshold and not settings.inverted
                or self.value < settings.threshold and settings.inverted
            ),
        )


@dataclass(slots=True, kw_only=True, frozen=True)
class Report:
    result: str
    failed: bool = False

    @classmethod
    def concat(cls, *_reports: Any) -> Self:
        reports = [
            report
            for report in _reports
            if isinstance(report, Report)
        ]

        return cls(
            result=", ".join(
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

        reports = [
            data.report(settings)
            for data in get_data()
        ]

        return cls(
            result=settings.report_outer.format(
                name=settings.name,
                inner=", ".join(
                    report.result
                    for report in reports[:settings.count]
                ),
            ),
            failed=any(
                report.failed
                for report in reports
            ),
        )
