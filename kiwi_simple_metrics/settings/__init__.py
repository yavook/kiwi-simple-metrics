from pydantic_settings import BaseSettings, SettingsConfigDict

from . import metric, misc
from .metric import MetricSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="METRIC__",
        env_nested_delimiter="__",
    )

    # time between gathering reports
    interval: float = 600

    # reporting to stdout
    log: misc.LogSettings = misc.LogSettings()

    # separates metrics and values in reports
    separator: str = ", "

    # metrics settings
    cpu: metric.CpuMS = metric.CpuMS()
    memory: metric.MemoryMS = metric.MemoryMS()
    disk: metric.DiskMS = metric.DiskMS()

    # pinging webhooks
    webhook: misc.WebhookSettings = misc.WebhookSettings()


SETTINGS = Settings()

__all__ = [
    "MetricSettings",
    "SETTINGS",
]
