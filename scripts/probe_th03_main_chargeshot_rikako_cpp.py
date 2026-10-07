#!/usr/bin/env python3
"""Compile the maintained Rikako charge/gauge C++ producer and compare its code shape."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib

import capstone

from lib.omf import describe_omf, parse_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from replay_th03_main_exact_units import execute
from probe_th03_main_bomb_rikako_cpp import code_bytes, segment_definitions

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "_reference/ReC98"
SOURCE = ROOT / "src/main/player/chargeshot_rikako.cpp"
HEADER = "src/main/player/chargeshot_rikako.hpp"
OVERLAY = Path("th03/cs_rika.cpp")
OBJECT = Path("obj/th03/cs_rika.obj")
TARGET_SEGMENT = 0x1C40
TARGET_OFFSET = 0x000A
TARGET_SIZE = 0x0500

SUPPORT = (
    HEADER,
    "compat/rec98/th03/main/player/ch_shot.hpp",
    "compat/rec98/th03/main/player/cur.hpp",
    "compat/rec98/th03/main/player/stuff.hpp",
    "compat/rec98/th03/main/player/gba.hpp",
    "compat/rec98/th03/main/hitbox.hpp",
    "compat/rec98/th03/main/hitcirc.hpp",
    "compat/rec98/th03/main/bullet/bullet.hpp",
    "compat/rec98/th03/main/sprite16.hpp",
    "compat/rec98/th03/main/playfld.hpp",
    "compat/rec98/th03/math/polar.hpp",
    "compat/rec98/libs/master.lib/master.hpp",
)

# (semantic name, target start, size, return mnemonic, return operand)
FUNCTIONS = (
    ("rikako_charge_setup", 0x0000, 15, "retf", ""),
    ("chargeshot_add_rikako", 0x000F, 126, "retf", "4"),
    ("rikako_charge_add_private", 0x008D, 29, "retf", "4"),
    ("rikako_hyper", 0x00AA, 17, "retf", ""),
    ("chargeshot_update_rikako", 0x00BB, 357, "retf", ""),
    ("rikako_chargeshot_private", 0x0220, 65, "ret", ""),
    ("chargeshot_hittest_rikako", 0x0261, 125, "retf", ""),
    ("chargeshot_render_rikako", 0x02DE, 97, "retf", ""),
    ("gauge_pattern_rikako", 0x033F, 401, "ret", "2"),
    ("gba_gauge_pattern_pellet_rikako", 0x04D0, 24, "retf", ""),
    ("gba_gauge_pattern_bullet_rikako", 0x04E8, 24, "retf", ""),
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode(blob: bytes) -> list:
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    insns = list(cs.disasm(blob, 0))
    if sum(insn.size for insn in insns) != len(blob):
        raise ValueError("Capstone did not cover complete Rikako charge/gauge code image")
    return insns


def shape(insns: list) -> list[tuple[int, int, str]]:
    return [(insn.address, insn.size, insn.mnemonic) for insn in insns]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", args.run_id):
        raise ValueError("invalid run id")

    out = ROOT / ".analysis/th03-main-chargeshot-rikako-cpp" / args.run_id
    out.mkdir(parents=True, exist_ok=False)

    exact_cfg = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    revision = exact_cfg["reference_revision"]
    inputs = {}
    for path in (
        "src/main/player/chargeshot_rikako.cpp",
        *SUPPORT,
        "scripts/probe_th03_main_chargeshot_rikako_cpp.py",
        "config/toolchain.toml",
        "config/targets.toml",
        "scripts/lib/omf.py",
        "scripts/lib/pc98.py",
        "scripts/lib/targets.py",
    ):
        inputs[path] = sha((ROOT / path).read_bytes())

    archive = out / "reference.tar"
    subprocess.run(
        ["git", "archive", "--format=tar", f"--output={archive}", revision],
        cwd=REFERENCE,
        check=True,
    )
    work = out / "source"
    work.mkdir()
    subprocess.run(["tar", "-xf", str(archive), "-C", str(work)], check=True)
    (work / OVERLAY).write_bytes(SOURCE.read_bytes())
    for name in SUPPORT:
        destination = work / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((ROOT / name).read_bytes())
    (work / "obj/th03").mkdir(parents=True, exist_ok=True)

    tool = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    env = os.environ.copy()
    env.update(
        DISPLAY="",
        WAYLAND_DISPLAY="",
        WINEDEBUG="-all",
        WINEPREFIX=str(ROOT / tool["paths"]["wine_prefix"]),
        MSDOS_PATH=r"C:\TC4\BIN",
    )
    command = [
        "wine", "cmd", "/d", "/c",
        r"set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%"
        r"&&bin\msdos -e -x tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -ml "
        r"-nobj/th03/ th03/cs_rika.cpp",
    ]
    build = execute(command, work, env, out / "compiler.log")

    raw = (work / OBJECT).read_bytes()
    omf = describe_omf(raw)
    if "TC86 Borland C++ 4.02" not in omf["translator_comments"]:
        raise ValueError("Rikako charge/gauge probe used the wrong compiler producer")
    segments = segment_definitions(raw)
    nonempty_code = [
        segment for segment in segments
        if segment["class"] == "CODE" and segment["size"]
    ]
    if (
        len(nonempty_code) != 1
        or nonempty_code[0]["name"] != "MAIN_11_TEXT"
        or nonempty_code[0]["overlay"] != ""
    ):
        raise ValueError(f"unexpected Rikako charge/gauge CODE segments: {nonempty_code}")

    code_segment = nonempty_code[0]
    candidate, ledata = code_bytes(raw, int(code_segment["index"]))

    target_raw = read_verified_artifact(
        ROOT,
        find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-main"),
    )
    target_image = parse_mz(target_raw).program_image
    target_start = (TARGET_SEGMENT * 16) + TARGET_OFFSET
    target = target_image[target_start:target_start + TARGET_SIZE]
    if len(target) != TARGET_SIZE:
        raise ValueError("target Rikako charge/gauge extent is truncated")

    candidate_insns = decode(candidate)
    target_insns = decode(target)
    candidate_shape = shape(candidate_insns)
    target_shape = shape(target_insns)

    if candidate_shape != target_shape:
        first = None
        for index, (left, right) in enumerate(zip(candidate_shape, target_shape)):
            if left != right:
                first = {
                    "instruction_index": index,
                    "candidate": left,
                    "target": right,
                }
                break
        report = {
            "kind": "th03-main-rikako-charge-gauge-cpp-producer-shape",
            "observed_utc": datetime.now(timezone.utc).isoformat(),
            "reference_revision": revision,
            "target_sha256": sha(target_raw),
            "inputs": inputs,
            "build": build,
            "object": {
                "path": str(OBJECT),
                "sha256": sha(raw),
                "module_name": omf["module_name"],
                "translator_comments": omf["translator_comments"],
                "segments": segments,
                "code_size": len(candidate),
                "ledata": ledata,
            },
            "comparison": {
                "target_segment": TARGET_SEGMENT,
                "target_offset": TARGET_OFFSET,
                "target_size": TARGET_SIZE,
                "candidate_size": len(candidate),
                "candidate_instruction_count": len(candidate_insns),
                "target_instruction_count": len(target_insns),
                "first_shape_difference": first,
                "instruction_shape_equal": False,
            },
            "source_acceptance": False,
            "exact_acceptance": False,
        }
        (out / "receipt.json").write_text(json.dumps(report, indent=2) + "\n")
        if first:
            raise ValueError(
                "Rikako charge/gauge instruction shape differs at "
                f"instruction {first['instruction_index']}: "
                f"candidate={tuple(first['candidate'])} target={tuple(first['target'])}; "
                f"candidate={len(candidate)} bytes/{len(candidate_insns)} instructions, "
                f"target={len(target)} bytes/{len(target_insns)} instructions"
            )
        raise ValueError(
            "Rikako charge/gauge instruction count/size differs: "
            f"candidate={len(candidate)} bytes/{len(candidate_insns)} instructions, "
            f"target={len(target)} bytes/{len(target_insns)} instructions"
        )

    candidate_returns = [
        (insn.address, insn.mnemonic, insn.op_str)
        for insn in candidate_insns
        if insn.mnemonic in {"ret", "retf"}
    ]
    target_returns = [
        (insn.address, insn.mnemonic, insn.op_str)
        for insn in target_insns
        if insn.mnemonic in {"ret", "retf"}
    ]
    expected_returns = []
    for name, offset, size, mnemonic, operand in FUNCTIONS:
        function = [
            insn for insn in target_insns
            if offset <= insn.address < offset + size
        ]
        if not function or function[-1].address + function[-1].size != offset + size:
            raise ValueError(f"target function boundary drifted: {name}")
        last = function[-1]
        if last.mnemonic != mnemonic or last.op_str != operand:
            raise ValueError(f"target return contract drifted: {name}")
        expected_returns.append((last.address, mnemonic, operand))
    if candidate_returns != target_returns:
        raise ValueError(
            f"Rikako charge/gauge complete return sequence differs: "
            f"candidate={candidate_returns} target={target_returns}"
        )
    for final_return in expected_returns:
        if final_return not in target_returns:
            raise ValueError(
                f"Rikako charge/gauge final ABI boundary missing from target returns: "
                f"{final_return}"
            )

    bss = [
        segment for segment in segments
        if segment["class"] == "BSS" and segment["size"]
    ]
    fixupp = [
        {
            "record_index": index,
            "size": len(record.data),
            "sha256": sha(record.data),
        }
        for index, record in enumerate(parse_omf(raw))
        if record.name == "FIXUPP"
    ]
    report = {
        "kind": "th03-main-rikako-charge-gauge-cpp-producer-shape",
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "reference_revision": revision,
        "target_sha256": sha(target_raw),
        "inputs": inputs,
        "build": build,
        "object": {
            "path": str(OBJECT),
            "sha256": sha(raw),
            "module_name": omf["module_name"],
            "translator_comments": omf["translator_comments"],
            "record_counts": omf["record_counts"],
            "segments": segments,
            "code_size": len(candidate),
            "bss_size": sum(segment["size"] for segment in bss),
            "ledata": ledata,
            "fixupp": fixupp,
        },
        "comparison": {
            "target_segment": TARGET_SEGMENT,
            "target_offset": TARGET_OFFSET,
            "size": TARGET_SIZE,
            "candidate_sha256": sha(candidate),
            "target_sha256": sha(target),
            "raw_differing_bytes_before_link": sum(
                left != right for left, right in zip(candidate, target)
            ),
            "instruction_count": len(candidate_insns),
            "instruction_shape_equal": True,
            "return_boundaries": [
                {
                    "name": name,
                    "offset": offset,
                    "size": size,
                    "return_offset": return_offset,
                    "return_mnemonic": mnemonic,
                    "return_operand": operand,
                }
                for (name, offset, size, mnemonic, operand),
                    (return_offset, _, _) in zip(FUNCTIONS, expected_returns)
            ],
        },
        "source_acceptance": True,
        "exact_acceptance": False,
        "notes": (
            "Object-level TC4J producer proof only. Full-link MAP placement, "
            "historical DATA/BSS ownership and ordered MZ relocations remain separate gates."
        ),
    }
    (out / "receipt.json").write_text(json.dumps(report, indent=2) + "\n")

    for path, before in inputs.items():
        if sha((ROOT / path).read_bytes()) != before:
            raise ValueError("probe input changed during run: " + path)

    print(
        "Rikako charge/gauge TC4J producer shape: PASS; "
        f"{TARGET_SIZE} bytes; {len(candidate_insns)} instructions; "
        f"{len(FUNCTIONS)} function boundaries"
    )
    print("Receipt:", (out / "receipt.json").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
