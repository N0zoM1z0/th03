#!/usr/bin/env python3
"""Stage the maintained MAINL cutscene into a fresh, source-only build overlay.

Merge this overlay into a fresh frozen ReC98 archive before compiling the existing
th03/cutscene.cpp slot. No executable, object, linker input order, or target byte
is edited here. The archived dependencies remain explicit compat inputs.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SLOT = "th03/cutscene.cpp"
OWNER = "src/mainl/cutscene.cpp"
WRAPPER = b'#include "src/mainl/cutscene.cpp"\n'
OWNED = (
    OWNER,
    "src/mainl/cutscene/cutscene.hpp",
    "src/mainl/cutscene/script.inl",
    "src/mainl/cutscene/egc_start_copy.inl",
)
COMPAT = (
    "compat/rec98/game/cutscene.hpp",
    "compat/rec98/libs/master.lib/master.hpp",
    "compat/rec98/th02/v_colors.hpp",
    "compat/rec98/th02/hardware/frmdelay.h",
    "compat/rec98/th03/hardware/input.h",
    "compat/rec98/th03/formats/pi.hpp",
    "compat/rec98/th01/hardware/grppsafx.h",
    "compat/rec98/th03/snd/snd.h",
    "compat/rec98/platform.h",
    "compat/rec98/th01/hardware/egc_impl.hpp",
)
INPUTS = OWNED + COMPAT

def read_inputs(root: Path) -> dict[str, bytes]:
    result = {}
    for name in INPUTS:
        path = root / name
        if path.is_symlink() or any(p.is_symlink() for p in path.parents):
            raise ValueError("source input cannot traverse a symlink: " + name)
        body = path.read_bytes()
        if not body or b"\r" in body or not body.endswith(b"\n"):
            raise ValueError("source input must be nonempty LF text: " + name)
        body.decode("utf-8")
        result[name] = body
    for name in OWNED:
        for include in re.findall(rb'^\s*#include "([^"\n]+)"', result[name], re.M):
            if include.decode() not in result:
                raise ValueError("undeclared maintained dependency: " + include.decode())
    if b"#pragma option -zPgroup_01" not in result[OWNER]:
        raise ValueError("MAINL cutscene group pragma is missing")
    return result

def stage(root: Path, output: Path) -> dict:
    payload = read_inputs(root)
    payload[SLOT] = WRAPPER
    # Validate every input before creating the exclusive output directory.
    output.mkdir(parents=False, exist_ok=False)
    rows = []
    for name, body in payload.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(body)
        rows.append({"path": name, "size": len(body), "sha256": hashlib.sha256(body).hexdigest()})
    report = {
        "kind": "th03-mainl-cutscene-source-overlay",
        "compile_slot": SLOT,
        "owner": OWNER,
        "reference_revision": "b6ba5b0a529edbb31efdf8c0e939263804f8ee47",
        "files": rows,
        "native_runs": 0,
        "cold_reproducible": False,
        "exact": False,
        "open_raw_pi_operand_offsets": ["095F:140A", "095F:1414", "095F:144B"],
    }
    (output / "stage.json").write_text(json.dumps(report, indent=2) + "\n")
    return report

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="new .analysis/NAME source overlay")
    args = parser.parse_args()
    path = Path(args.output)
    if len(path.parts) != 2 or path.parts[0] != ".analysis" or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", path.name):
        parser.error("output must be a new .analysis/NAME directory")
    report = stage(ROOT, ROOT / path)
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
