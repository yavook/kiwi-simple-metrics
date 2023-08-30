import psutil


def main() -> None:
    print(psutil.cpu_percent(interval=1))


if __name__ == "__main__":
    main()
