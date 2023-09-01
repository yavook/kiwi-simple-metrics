from typing import Iterator

import psutil

from ..settings import SETTINGS
from ._report import Report, ReportData


def _hwdata() -> Iterator[ReportData]:
    vmem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    if SETTINGS.memory.swap == "exclude":
        yield ReportData.from_settings(
            name=SETTINGS.memory.name_ram,
            value=vmem.percent,
            settings=SETTINGS.memory,
        )

    elif SETTINGS.memory.swap == "combine":
        yield ReportData.from_free_total(
            name=SETTINGS.memory.name,
            free=vmem.available + swap.free,
            total=vmem.total + swap.total,
            settings=SETTINGS.memory,
        )

    else:  # SETTINGS.memory.swap == "include"
        yield ReportData.from_settings(
            name=SETTINGS.memory.name_ram,
            value=vmem.percent,
            settings=SETTINGS.memory,
        )
        yield ReportData.from_settings(
            name=SETTINGS.memory.name_swap,
            value=swap.percent,
            settings=SETTINGS.memory,
        )


def memory() -> Report | None:
    return Report.aggregate(
        settings=SETTINGS.memory,
        get_data=_hwdata,
    )
