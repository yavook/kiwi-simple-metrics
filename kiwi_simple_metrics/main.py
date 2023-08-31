import os
import shutil

import psutil

from .settings import SETTINGS


def main() -> None:
    # env parameters
    print(SETTINGS.model_dump())

    # CPU metric
    print(psutil.cpu_percent(interval=1))

    # MEM metric

    # DISK metric
    # TODO test this using timeit
    for path in SETTINGS.disk.paths:
        try:
            sv = os.statvfs(path)
            percent = sv.f_bavail / sv.f_blocks * 100
        except ZeroDivisionError:
            percent = 0

        print(f"{path} Free (sv): {percent:.2f} %")

        try:
            total, _, free = shutil.disk_usage(path)
            percent = free / total * 100
        except ZeroDivisionError:
            percent = 0

        print(f"{path} Free (du): {percent:.2f} %")


if __name__ == "__main__":
    main()
