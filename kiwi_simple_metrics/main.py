from . import metrics
from .settings import SETTINGS


def main() -> None:
    # env parameters
    print(SETTINGS.model_dump())

    # CPU metric
    print(metrics.cpu())

    # MEM metric
    print(metrics.memory())

    # DISK metric
    print(metrics.disk())


if __name__ == "__main__":
    main()
