#!/usr/bin/python3

from . import metrics


def main() -> None:
    print(metrics.Report.concat(
        metrics.cpu(),
        metrics.memory(),
        metrics.disk(),
    ))


if __name__ == "__main__":
    main()
