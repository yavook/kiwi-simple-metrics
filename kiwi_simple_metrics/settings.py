import math

from pydantic import BaseModel, DirectoryPath, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MetricSettings(BaseModel):
    # metric will be reported
    enabled: bool = True

    # format string to report the metric
    report: str = "{name}: {value:.2f}%"

    # if the metric value exceeds this percentage, the report fails
    threshold: float

    # if True, this metric fails when the value falls below the `threshold`
    inverted: bool = False


class DiskMS(MetricSettings):
    # outer format string for reporting
    report_outer: str = "{name}: [{inner}]"

    # paths to check for disk space
    paths: list[DirectoryPath] = Field(default_factory=list)

    # include only `count` many of the paths with the least free space
    count: int = 1


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="METRIC_",
        env_nested_delimiter="__",
    )

    cpu: MetricSettings = MetricSettings(threshold=math.inf)
    memory: MetricSettings = MetricSettings(threshold=90)
    disk: DiskMS = DiskMS(threshold=15, inverted=True)


SETTINGS = Settings()
