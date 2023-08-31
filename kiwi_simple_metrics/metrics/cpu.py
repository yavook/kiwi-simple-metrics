import psutil

from ..settings import SETTINGS
from ._report import Report, ReportData


def _hwdata() -> ReportData:
    return ReportData(
        name=SETTINGS.cpu.name,
        value=psutil.cpu_percent(interval=1),
    )


def cpu() -> Report | None:
    if not SETTINGS.cpu.enabled:
        return None

    data = _hwdata()

    return data.report(SETTINGS.cpu)
