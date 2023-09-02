#!/usr/bin/python3

import asyncio

from . import metrics
from .settings import SETTINGS


def run_metrics(*_metrics: metrics.Metric) -> None:
    reports = (metric() for metric in _metrics)

    # create single report from metrics
    report = metrics.Report.summary(*reports)

    # maybe print this to stdout
    if SETTINGS.log.enabled:
        print(report)

    # maybe push this to the configured webhook
    report.push_webhook()


async def async_main() -> None:
    loop = asyncio.get_running_loop()

    while True:
        await asyncio.gather(
            asyncio.sleep(SETTINGS.interval),
            loop.run_in_executor(
                None, run_metrics,
                metrics.cpu,
                metrics.memory,
                metrics.disk,
                metrics.external,
            ),
        )


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
