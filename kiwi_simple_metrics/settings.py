import math
from typing import Any, Literal

from pydantic import (AnyUrl, BaseModel, DirectoryPath, Field,
                      FieldValidationInfo, field_validator)
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
            if str(value).lower().strip() not in (
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


class LogSettings(BaseModel):
    # if True, prints reports to stdout
    enabled: bool = False

    # how to format reports to stdout
    format: str = "[{state}] {result}"


class WebhookSettings(BaseModel):
    # webhooks to ping on success/on failure
    url: AnyUrl | None = None
    fail: AnyUrl | None = None

    # allow insecure/self-signed webhook targets
    insecure: bool = False

    def get_url(self, failed: bool) -> AnyUrl | None:
        if failed:
            return self.fail

        return self.url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="METRIC__",
        env_nested_delimiter="__",
    )

    # time between gathering reports
    interval: float = 600

    # reporting to stdout
    log: LogSettings = LogSettings()

    # separates metrics and values in reports
    separator: str = ", "

    # metrics settings
    cpu: CpuMS = CpuMS()
    memory: MemoryMS = MemoryMS()
    disk: DiskMS = DiskMS()

    # pinging webhooks
    webhook: WebhookSettings = WebhookSettings()


SETTINGS = Settings()
