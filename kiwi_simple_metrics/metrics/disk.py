import os

from ..settings import SETTINGS
from ._report import Report, ReportData


def _hwdata() -> list[ReportData]:
    def get_path_statvfs(path: os.PathLike) -> dict[str, float]:
        sv = os.statvfs(path)
        return {
            "free": sv.f_bavail,
            "total": sv.f_blocks,
        }

    return sorted([
        ReportData.from_free_total(
            name=str(path),
            **get_path_statvfs(path),
        ) for path in SETTINGS.disk.paths
    ], key=lambda d: d.value, reverse=True)


def disk() -> Report | None:
    if not SETTINGS.disk.enabled:
        return None

    data = _hwdata()

    return Report.aggregate(
        settings=SETTINGS.disk,
        data=data,
    )
