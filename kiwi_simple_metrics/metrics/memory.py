import psutil

from ..settings import SETTINGS
from ._report import Report, ReportData


def _hwdata() -> list[ReportData]:
    vmem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    if SETTINGS.memory.swap == "exclude":
        return [ReportData(
            name=SETTINGS.memory.name_ram,
            value=vmem.percent,
        )]

    elif SETTINGS.memory.swap == "combine":
        return [ReportData.from_free_total(
            name=SETTINGS.memory.name,
            free=vmem.available + swap.free,
            total=vmem.total + swap.total,
        )]

    else:  # SETTINGS.memory.swap == "include"
        return [ReportData(
            name=SETTINGS.memory.name_ram,
            value=vmem.percent,
        ), ReportData(
            name=SETTINGS.memory.name_swap,
            value=swap.percent,
        )]


def memory() -> Report | None:
    if not SETTINGS.memory.enabled:
        return None

    data = _hwdata()

    return Report.aggregate(
        settings=SETTINGS.memory,
        data=data,
    )
