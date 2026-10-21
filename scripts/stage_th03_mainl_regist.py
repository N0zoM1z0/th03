#!/usr/bin/env python3
"""Stage the maintained MAINL registration and score data into a fresh, source-only build overlay.

Merge this overlay into a fresh frozen ReC98 archive before compiling the existing
th03/regist.cpp and th03/scoredat.cpp slot. No executable, object, linker input order, or target byte
is edited here. The archived dependencies remain explicit compat inputs.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SLOTS = {'th03/regist.cpp': 'src/mainl/regist.cpp', 'th03/scoredat.cpp': 'src/mainl/scoredat.cpp'}
OWNED = ('src/mainl/regist.cpp', 'src/mainl/scoredat.cpp', 'src/mainl/hiscore/regist.hpp', 'src/mainl/hiscore/scoredat.hpp', 'src/mainl/hiscore/score_load.inl', 'src/mainl/hiscore/score_save.inl', 'src/mainl/hiscore/scorecry.hpp', 'src/mainl/hiscore/regi.h', 'src/mainl/hiscore/regist_text.hpp')
COMPAT = ('compat/rec98/game/input.hpp', 'compat/rec98/libs/master.lib/master.hpp', 'compat/rec98/pc98.h', 'compat/rec98/shiftjis.hpp', 'compat/rec98/th01/hardware/grppsafx.h', 'compat/rec98/th01/rank.h', 'compat/rec98/th02/hardware/frmdelay.h', 'compat/rec98/th03/common.h', 'compat/rec98/th03/formats/cdg.h', 'compat/rec98/th03/formats/pi.hpp', 'compat/rec98/th03/hardware/input.h', 'compat/rec98/th03/playchar.hpp', 'compat/rec98/th03/resident.hpp', 'compat/rec98/th03/score.hpp', 'compat/rec98/th03/snd/snd.h')
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
    if any(b"#pragma option -zPgroup_01" not in result[owner] for owner in SLOTS.values()):
        raise ValueError("MAINL registration and score data group pragma is missing")
    return result

def stage(root: Path, output: Path) -> dict:
    payload = read_inputs(root)
    for slot, owner in SLOTS.items():
        payload[slot] = ('#include "' + owner + '"\n').encode()
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
        "kind": "th03-mainl-regist-source-overlay",
        "compile_slots": SLOTS,
        "reference_revision": "b6ba5b0a529edbb31efdf8c0e939263804f8ee47",
        "files": rows,
        "native_runs": 0,
        "cold_reproducible": False,
        "exact": False,
        "open_raw_pi_operand_offsets": ["095F:19E2", "095F:19EC", "095F:22D8", "095F:22E2", "095F:230F", "095F:2319"],
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
