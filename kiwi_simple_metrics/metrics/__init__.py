from typing import Callable, TypeAlias

from ._report import Report
from .cpu import cpu
from .disk import disk
from .external import external
from .memory import memory

Metric: TypeAlias = Callable[[], Report | None]

__all__ = [
    "Report",
    "Metric",
    #
    "cpu",
    "disk",
    "external",
    "memory",
]
