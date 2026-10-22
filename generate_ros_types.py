#!/usr/bin/env python3

from pathlib import Path

from ros_python_types_gen import generate

ROOT = Path(__file__).resolve().parent

OUTPUT = ROOT / 'smartbot_irl' / 'ros_types'

CUSTOM_PATHS = [
    # ROOT / "vendor",
    "/home/n/Repos/smartbot3_ws/"
]


def main() -> None:
    generate(
        output=OUTPUT,
        custom_paths=CUSTOM_PATHS,
        clean=True,
    )


if __name__ == '__main__':
    main()
