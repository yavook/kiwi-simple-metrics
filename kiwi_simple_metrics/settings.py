import math
from typing import Literal

from pydantic import BaseModel, DirectoryPath, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    report: str = "{name}: {value:.2f}%"

    # per-metric format string for reporting
    report_outer: str = "{inner}"

    # include only `count` many items (None: include all)
    count: int | None = None


class CpuMS(MetricSettings):
    name: str = "CPU"
    threshold: float = math.inf


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
    report_outer: str = "{name}: [{inner}]"
    count: int = 1

    # paths to check for disk space
    paths: list[DirectoryPath] = Field(default_factory=list)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="METRIC_",
        env_nested_delimiter="__",
    )

    cpu: CpuMS = CpuMS()
    memory: MemoryMS = MemoryMS()
    disk: DiskMS = DiskMS()


SETTINGS = Settings()
