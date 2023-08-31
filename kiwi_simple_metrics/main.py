from .metrics import cpu_metric, disk_metric
from .settings import SETTINGS


def main() -> None:
    # env parameters
    print(SETTINGS.model_dump())

    # CPU metric
    print(cpu_metric())

    # MEM metric

    # DISK metric
    print(disk_metric())


if __name__ == "__main__":
    main()
