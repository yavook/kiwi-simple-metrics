from dataclasses import dataclass, field
from typing import Self

from ..settings import MetricSettings


@dataclass(slots=True, frozen=True)
class Report:
    result: str
    failed: bool = field(default=False, kw_only=True)

    @classmethod
    def new(
        cls, *,
        settings: MetricSettings,
        name: str,
        value: float,
    ) -> Self:
        result = settings.report.format(name=name, value=value)

        if (
            value > settings.threshold and not settings.inverted
            or value < settings.threshold and settings.inverted
        ):
            return cls(result, failed=True)

        else:
            return cls(result)
