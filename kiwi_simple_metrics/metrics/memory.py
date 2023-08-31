import psutil

from ..settings import SETTINGS
from ._report import Report


def memory() -> Report | None:
    if not SETTINGS.memory.enabled:
        return None

    def get_used_percent(free: float, total: float) -> float:
        return (total - free) / total * 100

    vmem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    if SETTINGS.memory.swap == "exclude":
        data = {
            SETTINGS.memory.name_ram: vmem.percent,
        }

    elif SETTINGS.memory.swap == "combine":
        data = {
            SETTINGS.memory.name: get_used_percent(
                vmem.available + swap.free,
                vmem.total + swap.total,
            )
        }

    else:  # SETTINGS.memory.swap == "include"
        data = {
            SETTINGS.memory.name_ram: vmem.percent,
            SETTINGS.memory.name_swap: swap.percent,
        }

    reports = [Report.new(
        settings=SETTINGS.memory,
        name=name,
        value=value,
    ) for name, value in data.items()]

    report_inner = ", ".join(
        report.result
        for report in reports
    )

    return Report(
        SETTINGS.memory.report_outer.format(
            name=SETTINGS.memory.name,
            inner=report_inner,
        ),
        failed=any(
            report.failed
            for report in reports
        ),
    )
