from dataclasses import dataclass, field
from typing import Self

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
        result = settings.report.format(
            name=self.name,
            value=self.value,
        )

        return Report(result, failed=(
            self.value > settings.threshold and not settings.inverted
            or self.value < settings.threshold and settings.inverted
        ))


@dataclass(slots=True, frozen=True)
class Report:
    result: str
    failed: bool = field(default=False, kw_only=True)

    @classmethod
    def aggregate(
        cls, *,
        settings: MetricSettings,
        data: list[ReportData],
    ) -> Self:
        reports = [
            data.report(settings)
            for data in data
        ]

        return cls(
            settings.report_outer.format(
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
