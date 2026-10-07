#!/usr/bin/env python3
"""Generate TH03 progress from current ledgers without guessed denominators."""

import argparse
import csv
from pathlib import Path
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def render_svg(units: list[dict[str, str]], functions: list[dict[str, str]]) -> str:
    rows = []
    for index, (artifact, label) in enumerate((
        ("th03-op", "OP.EXE"), ("th03-main", "MAIN.EXE"),
        ("th03-mainl", "MAINL.EXE"), ("th03-zun", "ZUN.COM"),
    )):
        candidates = [f for f in functions if f["artifact"] == artifact]
        reviewed = sum(f["boundary_state"] in {"reviewed", "shared"} for f in candidates)
        exact = sum(f["state"] == "exact" for f in candidates)
        total = len(candidates)
        y = 128 + index * 62
        inventory = f"{total} tracked functions" if total else "Inventory pending"
        rows.append(f'''  <text x="24" y="{y}" fill="#f4f4f5" font-family="sans-serif" font-size="14" font-weight="600">{label}</text>
  <text x="24" y="{y+20}" fill="#c8cad2" font-family="monospace" font-size="11">{inventory}</text>
  <rect x="200" y="{y-7}" width="250" height="12" rx="4" fill="#353b52"/>
  <rect x="488" y="{y-7}" width="270" height="12" rx="4" fill="#353b52"/>
  <rect x="200" y="{y-7}" width="{250*reviewed/total if total else 0:.2f}" height="12" fill="#9b6de3"/>
  <rect x="488" y="{y-7}" width="{270*exact/total if total else 0:.2f}" height="12" fill="#55c7a6"/>
  <text x="200" y="{y+22}" fill="#c8cad2" font-family="monospace" font-size="11">Reviewed {reviewed} · Pending {total-reviewed}</text>
  <text x="488" y="{y+22}" fill="#c8cad2" font-family="monospace" font-size="11">Exact {exact} · Pending {total-exact}</text>''')
    exact_units = [u for u in units if u["artifact"] == "th03-main" and u["state"] == "exact"]
    exact_bytes = sum(int(u["size"], 0) for u in exact_units)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="788" height="440" viewBox="0 0 788 440" role="img" aria-label="TH03 reviewed subset reconstruction progress">
  <title>TH03 reconstruction progress by artifact</title>
  <desc>Boundary review and exact function acceptance for the tracked subset. Whole-game function and authored-byte totals remain unknown.</desc>
  <rect width="788" height="440" rx="8" fill="#1f2335"/>
  <text x="24" y="31" fill="#f4f4f5" font-family="sans-serif" font-size="18" font-weight="600">TH03 reconstruction progress</text>
  <text x="24" y="52" fill="#c8cad2" font-family="sans-serif" font-size="12">Reviewed ledger subset · whole-game totals remain unknown</text>
  <text x="200" y="83" fill="#f4f4f5" font-family="sans-serif" font-size="13" font-weight="600">Boundary confidence</text>
  <text x="488" y="83" fill="#f4f4f5" font-family="sans-serif" font-size="13" font-weight="600">Function acceptance</text>
  <text x="200" y="100" fill="#c8cad2" font-family="sans-serif" font-size="11">Reviewed contiguous bodies</text>
  <text x="488" y="100" fill="#c8cad2" font-family="sans-serif" font-size="11">Complete raw bytes and relocations</text>
{chr(10).join(rows)}
  <path d="M24 366 H764" stroke="#4b526d"/>
  <text x="24" y="391" fill="#f4f4f5" font-family="sans-serif" font-size="13" font-weight="600">MAIN verified exact extents: {exact_bytes:,} bytes · {len(exact_units)} owners</text>
  <text x="24" y="414" fill="#c8cad2" font-family="sans-serif" font-size="12">Whole-game source/link/product graph: OPEN · no whole-game completion percentage</text>
</svg>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    with (ROOT / "config/units.csv").open(newline="") as stream:
        units = list(csv.DictReader(stream))
    with (ROOT / "config/th03_main_authored_functions.csv").open(newline="") as stream:
        functions = list(csv.DictReader(stream))
    targets = tomllib.loads((ROOT / "config/targets.toml").read_text())["artifacts"]
    lines = ["# TH03 reconstruction progress", "",
             "| Artifact | Target bytes | Source-present units | Exact units | Exact functions | Exact owned bytes |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for target in (a for a in targets if a["game"] == "th03"):
        rows = [u for u in units if u["artifact"] == target["id"] and u["state"] != "excluded"]
        present = sum(bool(u["source"]) and (ROOT / u["source"]).is_file() for u in rows)
        exact = sum(u["state"] == "exact" for u in rows)
        exact_functions = sum(f["state"] == "exact" for f in functions if f["artifact"] == target["id"])
        exact_bytes = sum(int(u["size"], 0) for u in rows if u["state"] == "exact")
        lines.append(f"| {target['id']} | {target['size']} | {present} | {exact} | {exact_functions} | {exact_bytes} |")
    lines.extend([
        "",
        "Reviewed authored-byte coverage is scoped to currently reviewed file-backed unit extents; "
        "the whole-product authored denominator remains unknown.",
        "Infrastructure and reference builds do not count as game reconstruction.",
        "",
    ])
    content = "\n".join(lines)
    destination = ROOT / "docs/PROGRESS.md"
    svg = render_svg(units, functions)
    svg_path = ROOT / "resources/progress.svg"
    if args.check:
        return 0 if (destination.is_file() and destination.read_text() == content
                     and svg_path.is_file() and svg_path.read_text() == svg) else 1
    destination.write_text(content)
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(svg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
