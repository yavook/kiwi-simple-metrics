from typing import Iterator

import psutil

from ..settings import SETTINGS
from ._report import Report, ReportData


def _hwdata() -> Iterator[ReportData]:
    vmem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    if SETTINGS.memory.swap == "exclude":
        yield ReportData(
            name=SETTINGS.memory.name_ram,
            value=vmem.percent,
        )

    elif SETTINGS.memory.swap == "combine":
        yield ReportData.from_free_total(
            name=SETTINGS.memory.name,
            free=vmem.available + swap.free,
            total=vmem.total + swap.total,
        )

    else:  # SETTINGS.memory.swap == "include"
        yield ReportData(
            name=SETTINGS.memory.name_ram,
            value=vmem.percent,
        )
        yield ReportData(
            name=SETTINGS.memory.name_swap,
            value=swap.percent,
        )


def memory() -> Report | None:
    return Report.aggregate(
        settings=SETTINGS.memory,
        get_data=_hwdata,
    )
