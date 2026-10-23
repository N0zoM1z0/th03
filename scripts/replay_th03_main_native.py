#!/usr/bin/env python3
"""Recreate the mixed MAIN tree twice, then review the regrouped native owners."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    for _ in range(2):
        subprocess.run(
            [
                sys.executable,
                "-B",
                "scripts/build_th03_main_work.py",
                "--build",
                "--cold",
                "--runtime",
            ],
            cwd=ROOT,
            check=True,
        )
    subprocess.run(
        [sys.executable, "-B", "scripts/review_th03_main_native_units.py"],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
