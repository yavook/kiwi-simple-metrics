import os
from pathlib import PurePath
from typing import Iterator

from ..settings import SETTINGS
from ._report import Report, ReportData


def _hwdata() -> Iterator[ReportData]:
    def get_path_statvfs(path: os.PathLike) -> dict[str, int]:
        sv = os.statvfs(path)
        return {
            "free": sv.f_bavail,
            "total": sv.f_blocks,
        }

    def get_path_name(path: os.PathLike) -> str:
        # get path and its parents
        path = PurePath(path)

        # if path or above is the vroot, make it a "virtual absolute" path
        if SETTINGS.disk.vroot in [path, *path.parents]:
            path = "/" / path.relative_to(SETTINGS.disk.vroot)

        return str(path)

    yield from sorted(
        [
            ReportData.from_free_total(
                name=get_path_name(path),
                **get_path_statvfs(path),
                settings=SETTINGS.disk,
            )
            for path in SETTINGS.disk.paths
        ],
        key=lambda d: d.value,
        reverse=True,
    )


def disk() -> Report | None:
    return Report.aggregate(
        settings=SETTINGS.disk,
        get_data=_hwdata,
    )
