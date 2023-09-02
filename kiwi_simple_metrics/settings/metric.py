import math
from typing import Any, Literal

from pydantic import (BaseModel, DirectoryPath, Field, FieldValidationInfo,
                      FilePath, field_validator)


class MetricSettings(BaseModel):
    # metric name
    name: str

    # metric will be reported
    enabled: bool = True

    # if the metric value exceeds this percentage, the report fails
    threshold: float

    # if True, this metric fails when the value falls below the `threshold`
    inverted: bool = False

    # per-value format string for reporting
    report: str = "{name}: {value:.1f}%"

    # per-metric format string for reporting
    report_outer: str = "{inner}"

    # include only `count` many items (None: include all)
    count: int | None = None

    @field_validator("count", mode="before")
    @classmethod
    def parse_nonetype(
        cls,
        value: Any,
        info: FieldValidationInfo,
    ) -> int | None:
        try:
            return int(value)

        except ValueError:
            if str(value).strip().lower() not in (
                "none", "null", "all", "yes", "any", "full",
                "oddly_specific_value_42",
            ):
                print(
                    f"[WARN] Unexpected {value=!r} for {info.field_name}, "
                    "falling back to None."
                )

            return None


class CpuMS(MetricSettings):
    name: str = "CPU"
    threshold: float = math.inf

    # timespan to analyze average CPU usage
    interval: float = 1


class MemoryMS(MetricSettings):
    name: str = "Memory"
    threshold: float = 90

    # how to handle swap space
    # exclude: swap space is not reported
    # include: swap space is reported separately
    # combine: ram and swap are combined
    swap: Literal["exclude", "include", "combine"] = "include"

    # names for telling apart ram and swap space
    name_ram: str = "RAM"
    name_swap: str = "Swap"


class DiskMS(MetricSettings):
    name: str = "Disk Used"
    threshold: float = 85
    report: str = "{value:.1f}% ({name})"
    report_outer: str = "{name}: {inner}"
    count: int | None = 1

    # paths to check for disk space
    paths: list[DirectoryPath] = Field(default_factory=list)


class ExternalMS(MetricSettings):
    name: str = "External Metric"
    threshold: float = 0

    # path to executable files
    executables: list[FilePath] = Field(default_factory=list)

    # wait at most this many seconds for each executable
    timeout: int = 60
