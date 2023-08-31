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
) -> Report:
    result = settings.report.format(name=name, value=value)

    if (
        value > settings.threshold and not settings.inverted
        or value < settings.threshold and settings.inverted
    ):
        return Report(result, failed=True)

    else:
        return Report(result)


def cpu_metric() -> Report | None:
    if not SETTINGS.cpu.enabled:
        return None

    value = psutil.cpu_percent(interval=1)
    return _report(
        settings=SETTINGS.cpu,
        name="CPU",
        value=value,
    )


def disk_metric() -> Report | None:
    if not SETTINGS.disk.enabled:
        return None

    def path_to_free_percent(path: os.PathLike) -> float:
        try:
            sv = os.statvfs(path)
            return sv.f_bavail / sv.f_blocks * 100
        except ZeroDivisionError:
            return 0

    data = sorted([
        (str(path), path_to_free_percent(path))
        for path in SETTINGS.disk.paths
    ], key=lambda d: d[1])

    reports = [_report(
        settings=SETTINGS.disk,
        name=path,
        value=percent,
    ) for path, percent in data]

    report_inner = ", ".join(
        report.result
        for report in reports[:SETTINGS.disk.count]
    )

    return Report(
        SETTINGS.disk.report_outer.format(
            name="DISK FREE",
            inner=report_inner,
        ),
        failed=any(
            report.failed
            for report in reports
        ),
    )
