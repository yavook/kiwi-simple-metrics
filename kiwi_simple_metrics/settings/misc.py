from pydantic import AnyUrl, BaseModel


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
