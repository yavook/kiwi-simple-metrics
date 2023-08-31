import os
from dataclasses import dataclass, field

import psutil

from .settings import SETTINGS, MetricSettings


@dataclass(slots=True, frozen=True)
class Report:
    result: str
    failed: bool = field(default=False, kw_only=True)


def _report(
    *,
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
    return _report(
        settings=SETTINGS.cpu,
        name="CPU",
        value=value,
    )


def disk_metric() -> Report | None:
    if not SETTINGS.disk.enabled:
        return None

    def vfs_to_percent(sv: os.statvfs_result) -> float:
        try:
            return sv.f_bavail / sv.f_blocks * 100
        except ZeroDivisionError:
            return 0

    data = sorted([
        (str(path), vfs_to_percent(os.statvfs(path)))
        for path in SETTINGS.disk.paths
    ], key=lambda d: d[1])

    reports = [
        report
        for path, percent in data
        if (report := _report(
            settings=SETTINGS.disk,
            name=path,
            value=percent,
        )) is not None
    ]

    return Report(
        ", ".join(report.result for report in reports),
        failed=any(report.failed for report in reports),
    )
