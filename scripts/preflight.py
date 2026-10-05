#!/usr/bin/env python3
"""Check TH03 identity and ledgers before target-dependent work."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    for script, arguments in [("check_environment.py", []), ("validate_tracking.py", []),
                              ("verify_targets.py", ["--game", "th03"]), ("status.py", [])]:
        print(f"[{script}]", flush=True)
        result = subprocess.run([sys.executable, f"scripts/{script}", *arguments], cwd=ROOT)
        if result.returncode:
            return result.returncode
    print("preflight: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
