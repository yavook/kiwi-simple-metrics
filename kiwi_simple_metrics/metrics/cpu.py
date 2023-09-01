from typing import Iterator

import psutil

from ..settings import SETTINGS
from ._report import Report, ReportData


def _hwdata() -> Iterator[ReportData]:
    yield ReportData.from_settings(
        name=SETTINGS.cpu.name,
        value=psutil.cpu_percent(interval=1),
        settings=SETTINGS.cpu,
    )


def cpu() -> Report | None:
    return Report.aggregate(
        settings=SETTINGS.cpu,
        get_data=_hwdata,
    )
