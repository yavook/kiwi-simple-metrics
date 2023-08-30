import psutil

from .settings import SETTINGS


def main() -> None:
    print(psutil.cpu_percent(interval=1))
    print(SETTINGS.model_dump())


if __name__ == "__main__":
    main()
