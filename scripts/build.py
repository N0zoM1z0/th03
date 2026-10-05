#!/usr/bin/env python3
"""Report open product closure or cold-build the explicit ReC98 reference."""

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--reference", action="store_true")
    parser.add_argument("--run-id")
    args = parser.parse_args()
    if args.reference:
        if not args.run_id:
            parser.error("--reference requires a fresh --run-id")
        return subprocess.run([sys.executable, "scripts/cold_build_rec98.py",
                               "--run-id", args.run_id], cwd=ROOT).returncode
    config = tomllib.loads((ROOT / "config/build.toml").read_text())
    print(json.dumps(config, indent=2))
    if args.status:
        return 0
    print("TH03 maintained product graph is open; use --reference for calibration only.",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
