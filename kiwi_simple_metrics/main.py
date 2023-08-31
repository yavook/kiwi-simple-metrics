#!/usr/bin/python3

import asyncio
import urllib.parse

import requests

from . import metrics
from .settings import SETTINGS


async def run_metrics() -> None:
    while True:
        interval = asyncio.sleep(SETTINGS.interval)

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

        await interval


def main() -> None:
    loop = asyncio.get_event_loop()
    loop.create_task(run_metrics())
    loop.run_forever()


if __name__ == "__main__":
    main()
