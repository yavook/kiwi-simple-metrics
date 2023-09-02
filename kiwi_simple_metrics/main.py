#!/usr/bin/python3

import asyncio
import concurrent.futures

from . import metrics
from .settings import SETTINGS


def run_metrics(
    executor: concurrent.futures.Executor,
    *_metrics: metrics.Metric,
) -> None:
    # === conc experiment ===

    futures = concurrent.futures.wait(
        executor.submit(metric) for metric in _metrics
    ).done

    print(list(future.result() for future in futures))

    # === end conc ===

    reports = (metric() for metric in _metrics)

    # create single report from metrics
    report = metrics.Report.summary(*reports)

    # maybe print this to stdout
    if SETTINGS.log.enabled:
        print(report)

    # maybe push this to the configured webhook
    report.push_webhook()


async def async_main_loop() -> None:
    loop = asyncio.get_running_loop()

    while True:
        with concurrent.futures.ThreadPoolExecutor() as pool:
            await asyncio.gather(
                asyncio.sleep(SETTINGS.interval),
                loop.run_in_executor(
                    None, run_metrics,
                    pool,
                    metrics.cpu,
                    metrics.memory,
                    metrics.disk,
                    metrics.external,
                ),
            )


def main() -> None:
    asyncio.run(async_main_loop())


if __name__ == "__main__":
    main()
