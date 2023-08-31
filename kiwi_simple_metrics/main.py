#!/usr/bin/python3

import asyncio

from . import metrics
from .settings import SETTINGS


async def run_metrics() -> None:
    while True:
        interval = asyncio.sleep(SETTINGS.interval)

        print(metrics.Report.concat(
            metrics.cpu(),
            metrics.memory(),
            metrics.disk(),
        ))

        await interval


def main() -> None:
    loop = asyncio.get_event_loop()
    loop.create_task(run_metrics())
    loop.run_forever()


if __name__ == "__main__":
    main()
