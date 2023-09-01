from typing import Iterator

from ..settings import SETTINGS
from ._report import Report, ReportData


def _hwdata() -> Iterator[ReportData]:
    yield ReportData(
        name="Foo",
        value=69.42,
        threshold=80,
        inverted=False,
        format=SETTINGS.cpu.report,
    )


def external() -> Report | None:
    return Report.aggregate(
        settings=SETTINGS.external,
        get_data=_hwdata,
    )
