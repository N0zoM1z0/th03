#!/usr/bin/env python3
"""Generate TH03 progress from current ledgers without guessed denominators."""

import argparse
import csv
from pathlib import Path
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


MAINL_HEAP_UNIT = "th03-mainl-decoded-heap-manager"
MAINL_HEAP_RETAINED = {
    "ev-th03-mainl-heap-retained-structural": (
        "binary", "cb3379b976fd189e5e419c1d0aa6cec8d8e5821f49268b411f28050645680eb3"),
    "ev-th03-mainl-heap-retained-runtime": (
        "runtime", "c9d3ead4db8db4b311e658350c0c33ad28e027de07802508f94048ce0c89c003"),
}


def mainl_unit_progress(units: list[dict[str, str]]) -> dict[str, int]:
    """MAINL has mixed function/module extents, not an authored-function inventory."""
    rows = [u for u in units if u["artifact"] == "th03-mainl"
            and u["state"] != "excluded"]
    if len({u["id"] for u in rows}) != len(rows):
        raise ValueError("duplicate MAINL unit would inflate the tracked denominator")
    present = [u for u in rows if u["state"] in {"source-present", "structural", "exact"}
               and u["source"]]
    return {
        "total": len(rows),
        "reviewed": sum(u["boundary_state"] in {"reviewed", "shared"} for u in rows),
        "source": len(present),
        "source_bytes": sum(int(u["size"], 0) for u in present),
        "exact": sum(u["state"] == "exact" for u in rows),
    }


def mainl_heap_retained(units: list[dict[str, str]],
                        evidence: list[dict[str, str]]) -> bool:
    """A separate diagnostic annotation; never feeds source or exact counts."""
    heaps = [u for u in units if u["id"] == MAINL_HEAP_UNIT]
    if len(heaps) != 1:
        return False
    heap = heaps[0]
    if (heap["artifact"], heap["segment"], heap["offset"], heap["size"],
            heap["boundary_state"], heap["state"], heap["source"]) != (
            "th03-mainl", "decoded:0000", "0x210a", "628", "reviewed",
            "source-present", "src/mainl/memory/heap.inl"):
        return False
    linked = heap["evidence_ids"].split(";")
    for evidence_id, (kind, digest) in MAINL_HEAP_RETAINED.items():
        matches = [e for e in evidence if e["id"] == evidence_id]
        if evidence_id not in linked or len(matches) != 1:
            return False
        row = matches[0]
        if (row["oracle"], row["artifact"], row["unit_id"], row["extent_start"],
                row["extent_size"], row["evidence_class"], row["result"],
                row["output_sha256"]) != (
                "analysis-bundle", "th03-mainl", MAINL_HEAP_UNIT, "0x210a",
                "628", kind, "pass", digest):
            return False
    return True


def zun_init_standalone_retained(units: list[dict[str, str]]) -> bool:
    """Historical standalone diagnostic only; never feeds any progress count."""
    # Reviewed checkpoint: docs/reconstruction/ZUN_INIT_STANDALONE_FEASIBILITY.md.
    # Completion: .analysis/zun-init-cold-continuation-output-20261021-v01/completion.json
    # SHA256: 4fb3cf03ef57da9ae3da738f0f650da385b546abb3fff35975760d75449f70c8.
    # src/zun/init.asm: 078525c35dfa4b499feb661980733964e16fa5654e8403ee55b0de221e828dc2.
    # Two distinct assembler invocations/materializations; first OBJ retained
    # after date-only registry rejection and linked by reviewed continuation.
    # Raw OMF/COM/MAP equal, no normalization. Original transport exit unknown.
    rows = [u for u in units if u["id"] == "th03-zun-decoded-init"]
    return len(rows) == 1 and all(rows[0].get(key) == value for key, value in {
        "artifact": "th03-zun", "segment": "decoded-COM", "offset": "0x6c4",
        "size": "1390", "boundary_state": "reviewed", "state": "boundary-reviewed",
    }.items())


def zun_driver_hybrid_retained(units: list[dict[str, str]]) -> bool:
    """Historical mixed-source wrapper composition; never feeds progress counts."""
    # Reviewed checkpoint: docs/reconstruction/ZUN_SPRITE16_DRIVER_REVIEW.md.
    # Completion: .analysis/zun-driver-wrapper-composition/zun-init-driver-wrapper-20261021-v01/completion.json
    # SHA256: 07719382277e33709bc9b7c5f15992060a8b4b910ae621e9fc8e98277e452d93.
    # Composition receipt SHA256: 3830777630d3c719765a7ab522a068203e10e452e4e7f6072f140995ed31469b.
    # src/zun/driver_services.inl: d57a52b5dc27a4d548259d7174141b86267734b231a2a0cd55203f1a751507af.
    # src/zun/driver_resident.inl: 258a133463e406dcc7fdf936fc417dc8a502a03d0fb1fe3d605b597af77c7cfa.
    # src/zun/driver_command.inl: 9a49039df84a1c4bde277687b1a35dfd5a9f558a4cd20ff4c46a870b1fa593fc.
    # src/zun/driver_strings.inl: 06effd580a81e6989a7f63fea4bda3cfea6e49940561d149963f3cc157dec01a.
    # src/zun/driver_numbers.inl: de3f42440813c414028dde3130deab8f0e00cdc29efcfa8a69839dfc711683e0.
    # src/zun/driver_graphics.inl: 173dbbb12f3d8e2eb25f417acf5ef194551eff4296592878e5cb15104e271ebc.
    # src/zun/driver_format.inl: 1ee883086ae9045f451e57d9da5ff74ccf6f25980d8228bed2885087cfb94d5e.
    # src/zun/driver.asm: 895751c4e7398a581f10c03ced0462fc1cc404b7fdda4a459cdc4eafc2e56c85.
    # src/zun/driver_data.inl: 656aafabb96b2cab664735bc0dd194a74f01433792704f2e87b94d4370799a2c.
    # src/zun/driver_hardware.inc: 50353aac8704d0c9e53d373f9a9524011b2b7c2798063d90c8152503f2e14ab6.
    # Two independent driver materializations have equal raw OBJ/COM/MAP,
    # no normalization/object reuse. First was not a predeclared pair; second
    # source mtimes were declared from observed first inputs. Not target-exact.
    # Ten maintained sources own the complete 4,224-byte standalone driver:
    # 55 procedures / 2,844 B plus 1,380 B data/layout; candidate only.
    # All ten target differences are inside maintained bodies, not target-exact.
    # Two equal 22,812-byte -2/-4 compositions retain three other payloads
    # and wrapper scaffold. Fourteen wrapper-only observations and wrong-transfer
    # negative pass; no payload execution/native build. Packaging/default stay open.
    if not zun_init_standalone_retained(units):
        return False
    rows = [u for u in units if u["id"] == "th03-zun-decoded-sprite16-driver"]
    return len(rows) == 1 and all(rows[0].get(key) == value for key, value in {
        "artifact": "th03-zun", "segment": "decoded-COM", "offset": "0x33a2",
        "size": "4224", "boundary_state": "reviewed", "state": "boundary-reviewed",
    }.items())


def mainl_cutscene_source_pending(units: list[dict[str, str]]) -> bool:
    """Annotation only: a maintained owner does not promote source/exact counts."""
    rows = [u for u in units if u["id"] == "th03-mainl-decoded-cutscene"]
    return (len(rows) == 1 and all(rows[0].get(k) == v for k, v in {
        "artifact": "th03-mainl", "segment": "decoded:095F", "offset": "0xb3e",
        "size": "3195", "boundary_state": "reviewed", "state": "boundary-reviewed",
        "source": "",
    }.items()) and all((ROOT / p).is_file() for p in (
        "src/mainl/cutscene.cpp", "src/mainl/cutscene/cutscene.hpp",
        "src/mainl/cutscene/script.inl", "src/mainl/cutscene/egc_start_copy.inl",
    )))


MAINL_CUTSCENE_SOURCE_EVIDENCE = {
    "ev-th03-mainl-cutscene-source-compiler": "compiler",
    "ev-th03-mainl-cutscene-source-runtime": "runtime",
    "ev-th03-mainl-cutscene-source-reproducible": "reproducibility",
}
MAINL_CUTSCENE_SOURCE_RECEIPT = "7f68b341f72bff5814593ca4291043ab9c22b3e3ef58f27517d4af0b0a94c82b"

def mainl_cutscene_hybrid_source(units, evidence):
    rows = [u for u in units if u["id"] == "th03-mainl-decoded-cutscene"]
    if len(rows) != 1 or any(rows[0].get(k) != v for k, v in {
        "artifact": "th03-mainl", "segment": "decoded:095F", "offset": "0xb3e",
        "size": "3195", "boundary_state": "reviewed", "state": "source-present",
        "source": "src/mainl/cutscene.cpp",
    }.items()):
        return False
    linked = rows[0].get("evidence_ids", "").split(";")
    for name, kind in MAINL_CUTSCENE_SOURCE_EVIDENCE.items():
        records = [e for e in evidence if e["id"] == name]
        if name not in linked or len(records) != 1 or any(records[0].get(k) != v for k, v in {
            "artifact": "th03-mainl", "unit_id": rows[0]["id"], "oracle": "analysis-bundle",
            "extent_start": "0xb3e", "extent_size": "3195", "evidence_class": kind,
            "result": "pass", "output_sha256": MAINL_CUTSCENE_SOURCE_RECEIPT,
        }.items()):
            return False
    return True


def render_svg(units: list[dict[str, str]], functions: list[dict[str, str]],
               evidence: list[dict[str, str]] | None = None) -> str:
    rows = []
    for index, (artifact, label) in enumerate((
        ("th03-op", "OP.EXE"), ("th03-main", "MAIN.EXE"),
        ("th03-mainl", "MAINL.EXE"), ("th03-zun", "ZUN.COM"),
    )):
        if artifact == "th03-mainl":
            counts = mainl_unit_progress(units)
            total = counts["total"]
            reviewed = counts["reviewed"]
            source = counts["source"]
            exact = counts["exact"]
            y = 128 + index * 62
            retained = (" · Heap: 8 procedures / 628 B retained-only"
                        if mainl_heap_retained(units, evidence or []) else "")
            rows.append(f"""  <g aria-label="MAINL bars count tracked unit extents, not functions; source-present is not exact">
  <text x="24" y="{y}" fill="#f4f4f5" font-family="sans-serif" font-size="14" font-weight="600">{label}</text>
  <text x="24" y="{y+20}" fill="#c8cad2" font-family="monospace" font-size="11">{total} tracked unit extents</text>
  <rect x="200" y="{y-7}" width="250" height="12" rx="4" fill="#353b52"/>
  <rect x="488" y="{y-7}" width="270" height="12" rx="4" fill="#353b52"/>
  <rect x="200" y="{y-7}" width="{250*reviewed/total if total else 0:.2f}" height="5" fill="#9b6de3"/>
  <rect x="200" y="{y}" width="{250*source/total if total else 0:.2f}" height="5" fill="#e0af68"/>
  <rect x="488" y="{y-7}" width="{270*exact/total if total else 0:.2f}" height="12" fill="#55c7a6"/>
  <text x="200" y="{y+22}" fill="#c8cad2" font-family="monospace" font-size="11">Reviewed {reviewed} · Source {source}/{total}</text>
  <text x="488" y="{y+22}" fill="#c8cad2" font-family="monospace" font-size="11">Unit acceptance: exact {exact}/{total}</text>
  <text x="200" y="{y+40}" fill="#e0af68" font-family="sans-serif" font-size="10">Source-present: {counts['source_bytes']:,} B{retained}</text>
  </g>""")
            if mainl_cutscene_source_pending(units):
                rows.append(f'<text x="200" y="{y+52}" fill="#e0af68" font-family="sans-serif" font-size="10">Cutscene owner: 13 bodies / 3,195 B · native proof pending · not counted</text>')
            elif mainl_cutscene_hybrid_source(units, evidence or []):
                rows.append(f'<text x="200" y="{y+52}" fill="#e0af68" font-family="sans-serif" font-size="10">Cutscene: 3,195 B source · repeat OBJ/EXE/MAP · 3 PI bytes still differ</text>')
            continue
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
        if artifact == "th03-zun" and zun_init_standalone_retained(units):
            rows.append(f'<text x="200" y="{y+40}" fill="#e0af68" font-family="sans-serif" font-size="10">Retained standalone init: 2 materializations · 9 procedures / 1,390 B · no exact credit</text>')
        if artifact == "th03-zun" and zun_driver_hybrid_retained(units):
            rows.append(f'<text x="200" y="{y+56}" fill="#e0af68" font-family="sans-serif" font-size="10" aria-label="Two equal 22,812-byte mixed-source outputs: maintained init (-2) and driver (-4), three retained other payloads and retained wrapper scaffold. Two independent driver materializations have raw OBJ/COM/MAP equality, no normalization or object reuse; first was not a predeclared pair, and second source mtimes were declared from observed first inputs. Fourteen wrapper-only observations and wrong-transfer negative pass; no payload execution or native composition build. Ten target differences remain; no exact acceptance or DIET closure">Maintained -2/-4 composition: 22,812 B · mixed retained inputs · 10 target differences · no exact credit</text>')
    exact_units = [u for u in units if u["artifact"] == "th03-main" and u["state"] == "exact"]
    exact_bytes = sum(int(u["size"], 0) for u in exact_units)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="788" height="458" viewBox="0 0 788 458" role="img" aria-label="TH03 reviewed subset reconstruction progress">
  <title>TH03 reconstruction progress by artifact</title>
  <desc>Boundary review and exact function acceptance for the tracked subset. Whole-game function and authored-byte totals remain unknown.</desc>
  <rect width="788" height="458" rx="8" fill="#1f2335"/>
  <text x="24" y="31" fill="#f4f4f5" font-family="sans-serif" font-size="18" font-weight="600">TH03 reconstruction progress</text>
  <text x="24" y="52" fill="#c8cad2" font-family="sans-serif" font-size="12">Reviewed ledger subset · whole-game totals remain unknown</text>
  <text x="200" y="83" fill="#f4f4f5" font-family="sans-serif" font-size="13" font-weight="600">Boundary confidence</text>
  <text x="488" y="83" fill="#f4f4f5" font-family="sans-serif" font-size="13" font-weight="600">Function acceptance</text>
  <text x="200" y="100" fill="#c8cad2" font-family="sans-serif" font-size="11">Reviewed contiguous bodies</text>
  <text x="488" y="100" fill="#c8cad2" font-family="sans-serif" font-size="11">Complete raw bytes and relocations</text>
{chr(10).join(rows)}
  <path d="M24 384 H764" stroke="#4b526d"/>
  <text x="24" y="409" fill="#f4f4f5" font-family="sans-serif" font-size="13" font-weight="600">MAIN verified exact extents: {exact_bytes:,} bytes · {len(exact_units)} owners</text>
  <text x="24" y="432" fill="#c8cad2" font-family="sans-serif" font-size="12">Whole-game source/link/product graph: OPEN · no whole-game completion percentage</text>
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
    with (ROOT / "config/evidence.csv").open(newline="") as stream:
        evidence = list(csv.DictReader(stream))
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
    svg = render_svg(units, functions, evidence)
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
