#!/usr/bin/python3

import asyncio

from . import metrics
from .settings import SETTINGS


def handle_report() -> None:
    # create single report from metrics
    report = metrics.Report.summary(
        metrics.cpu(),
        metrics.memory(),
        metrics.disk(),
        metrics.external(),
    )

    # maybe print this to stdout
    if SETTINGS.log.enabled:
        print(report)

    # maybe push this to the configured webhook
    report.push_webhook()


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
