#!/usr/bin/python3

import asyncio
import concurrent.futures

from . import metrics
from .settings import SETTINGS


def run_metrics(
    executor: concurrent.futures.Executor,
    *_metrics: metrics.Metric,
) -> None:
    # run metrics in executor
    tasks = [executor.submit(metric) for metric in _metrics]

    # wait for finish
    # pair up each result with its task index
    results = (
        (tasks.index(future), future.result())
        for future in concurrent.futures.wait(tasks).done
    )

    # extract reports in task index order
    reports = (report for _, report in sorted(results, key=lambda x: x[0]))

    # create summary report
    report = metrics.Report.summary(*reports)

    # maybe print this to stdout
    if SETTINGS.log.enabled:
        print(report)

    # maybe push this to the configured webhook
    report.push_webhook()


async def async_main_loop() -> None:
    loop = asyncio.get_running_loop()

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=SETTINGS.threads,
    ) as pool:
        while True:
            # start interval and metrics at the same time
            await asyncio.gather(
                asyncio.sleep(SETTINGS.interval),
                loop.run_in_executor(
                    None,
                    run_metrics,
                    pool,
                    # metrics are reported in this order
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
