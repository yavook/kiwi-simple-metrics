import psutil

from ..settings import SETTINGS
from ._report import Report


def cpu() -> Report | None:
    if not SETTINGS.cpu.enabled:
        return None

    value = psutil.cpu_percent(interval=1)
    return Report.new(
        settings=SETTINGS.cpu,
        name=SETTINGS.cpu.name,
        value=value,
    )
