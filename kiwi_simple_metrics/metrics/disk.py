import os

from ..settings import SETTINGS
from ._report import Report


def disk() -> Report | None:
    if not SETTINGS.disk.enabled:
        return None

    def path_to_used_percent(path: os.PathLike) -> float:
        try:
            sv = os.statvfs(path)
            return (1 - sv.f_bavail / sv.f_blocks) * 100
        except ZeroDivisionError:
            return 0

    data = sorted([
        (str(path), path_to_used_percent(path))
        for path in SETTINGS.disk.paths
    ], key=lambda d: d[1], reverse=True)

    reports = [Report.new(
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
            name=SETTINGS.disk.name,
            inner=report_inner,
        ),
        failed=any(
            report.failed
            for report in reports
        ),
    )
