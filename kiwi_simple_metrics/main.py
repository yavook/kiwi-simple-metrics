#!/usr/bin/python3

import asyncio
import urllib.parse

import requests

from . import metrics
from .settings import SETTINGS


def handle_report() -> None:
    # create single report from metrics
    report = metrics.Report.summary(
        metrics.cpu(),
        metrics.memory(),
        metrics.disk(),
    )

    # maybe print this to stdout
    if SETTINGS.log.enabled:
        print(report)

    # maybe push this to a webhook
    if (url := SETTINGS.webhook.get_url(failed=report.failed)) is not None:
        requests.get(
            url=str(url).format(
                urllib.parse.quote_plus(report.result)
            ),
            verify=not SETTINGS.webhook.insecure,
        )


async def run_metrics() -> None:
    loop = asyncio.get_running_loop()

    while True:
        await asyncio.gather(
            asyncio.sleep(SETTINGS.interval),
            loop.run_in_executor(None, handle_report),
        )


def main() -> None:
    asyncio.run(run_metrics())


if __name__ == "__main__":
    main()
