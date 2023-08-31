import os
from typing import Iterator

from ..settings import SETTINGS
from ._report import Report, ReportData


def _hwdata() -> Iterator[ReportData]:
    def get_path_statvfs(path: os.PathLike) -> dict[str, float]:
        sv = os.statvfs(path)
        return {
            "free": sv.f_bavail,
            "total": sv.f_blocks,
        }

    yield from sorted([
        ReportData.from_free_total(
            name=str(path),
            **get_path_statvfs(path),
        ) for path in SETTINGS.disk.paths
    ], key=lambda d: d.value, reverse=True)


def disk() -> Report | None:
    return Report.aggregate(
        settings=SETTINGS.disk,
        get_data=_hwdata,
    )
