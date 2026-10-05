#!/usr/bin/env python3
"""Generate TH03 progress from current ledgers without guessed denominators."""

import argparse
import csv
from pathlib import Path
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    with (ROOT / "config/units.csv").open(newline="") as stream:
        units = list(csv.DictReader(stream))
    targets = tomllib.loads((ROOT / "config/targets.toml").read_text())["artifacts"]
    lines = ["# TH03 reconstruction progress", "",
             "| Artifact | Target bytes | Source-present units | Exact units |",
             "| --- | ---: | ---: | ---: |"]
    for target in (a for a in targets if a["game"] == "th03"):
        rows = [u for u in units if u["artifact"] == target["id"] and u["state"] != "excluded"]
        present = sum(bool(u["source"]) and (ROOT / u["source"]).is_file() for u in rows)
        exact = sum(u["state"] == "exact" for u in rows)
        lines.append(f"| {target['id']} | {target['size']} | {present} | {exact} |")
    lines.extend(["", "Reviewed authored-byte denominator: unknown until ownership is reviewed.",
                  "Infrastructure and reference builds do not count as game reconstruction.", ""])
    content = "\n".join(lines)
    destination = ROOT / "docs/PROGRESS.md"
    if args.check:
        return 0 if destination.is_file() and destination.read_text() == content else 1
    destination.write_text(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
