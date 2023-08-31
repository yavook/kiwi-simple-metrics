from dataclasses import dataclass, field

import psutil

from .settings import SETTINGS, MetricSettings


@dataclass(slots=True, frozen=True)
class Report:
    result: str
    failed: bool = field(default=False, kw_only=True)


def _report(
    settings: MetricSettings,
    name: str,
    value: float,
) -> Report | None:
    if not settings.enabled:
        return None

    result = settings.report.format(name=name, value=value)

    if (
        value > settings.threshold and not settings.inverted
        or value < settings.threshold and settings.inverted
    ):
        return Report(result, failed=True)

    else:
        return Report(result)


def cpu_metric() -> Report | None:
    value = psutil.cpu_percent(interval=1)
    return _report(SETTINGS.cpu, "CPU", value)
