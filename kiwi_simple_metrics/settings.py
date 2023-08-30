from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MetricS(BaseModel):
    # metric will be reported
    enabled: bool = True

    # if the metric value exceeds this percentage, the report fails
    threshold: float

    # if True, this metric fails when the value falls below the `threshold`
    inverted: bool = False


class ParamMS(MetricS):
    # arbitrary parameters
    params: list[str] = Field(default_factory=list)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="METRIC_",
        env_nested_delimiter="__",
    )

    cpu: MetricS = MetricS(
        threshold=100,
    )

    memory: MetricS = MetricS(
        threshold=90,
    )

    disk: ParamMS = ParamMS(
        threshold=85,
    )


SETTINGS = Settings()
