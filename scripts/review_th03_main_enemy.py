#!/usr/bin/env python3
"""Replay the raw target boundary observations for the complete enemy owner.

Semantic names and selection extents are reviewed hypotheses in the candidate
manifest. Raw terminators, instructions, dispatch tables and relocations are
observed from the pinned Japanese target, independently of its decompiler.
"""

import argparse
import hashlib
import json
from pathlib import Path
import struct
import tomllib

import capstone

from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / ".analysis"):
        raise ValueError("target review exports belong under .analysis/")
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-main")
    target = read_verified_artifact(ROOT, artifact)
    image = parse_mz(target)
    if not image.valid:
        raise ValueError("invalid target MZ")
    manifest_path = ROOT / "config/th03_main_exact_units.toml"
    manifest = tomllib.loads(manifest_path.read_text())
    units = [u for u in manifest["units"] if u["id"] == "th03-main-enemies"]
    if len(units) != 1:
        raise ValueError("accepted enemy owner missing or duplicated")
    config = {"units": units, "functions": [
        f for f in manifest["functions"]
        if f.get("object") == "e_enemy"
    ]}
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    functions = []
    disassembly = []
    for function in config["functions"]:
        base = function["segment"] * 16
        start, size = function["offset"], function["size"]
        code = image.program_image[base + start:base + start + size]
        instructions = list(decoder.disasm(code, start))
        if sum(i.size for i in instructions) != size:
            raise ValueError(f"undecoded function bytes: {function['name']}")
        last = instructions[-1]
        if last.mnemonic not in {"ret", "retf"}:
            raise ValueError(f"reviewed function does not end in RET: {function['name']}")
        functions.append({
            "semantic_name_candidate": function["name"], "segment": function["segment"],
            "offset": start, "size": size,
            "file_offset": image.header.header_size + base + start,
            "sha256": hashlib.sha256(code).hexdigest(),
            "return": {"offset": last.address, "instruction": f"{last.mnemonic} {last.op_str}"},
            "calls": [{"offset": i.address, "instruction": f"{i.mnemonic} {i.op_str}"}
                      for i in instructions if i.mnemonic in {"call", "lcall"}],
        })
        disassembly.append(f"\n{function['name']} {function['segment']:04X}:{start:04X} size={size}\n")
        disassembly.extend(f"{i.address:04X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}\n"
                           for i in instructions)
    base = 0x139d * 16
    # The original sparse-switch dispatch explicitly loads BX=08C0,
    # CX=16 and uses JMP CS:[BX+20]. The RET at 08BE precedes one alignment
    # byte and the 32-byte key / 32-byte destination arrays.
    dispatch = image.program_image[base + 0x0592:base + 0x05ac]
    if dispatch[:6] != bytes.fromhex("b91000bbc008") or dispatch[-4:] != bytes.fromhex("2eff6720"):
        raise ValueError("enemy_run sparse dispatch changed")
    keys = struct.unpack_from("<16H", image.program_image, base + 0x08c0)
    destinations = struct.unpack_from("<16H", image.program_image, base + 0x08e0)
    if keys != (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 128, 129, 130, 131):
        raise ValueError("enemy_run sparse keys changed")
    if any(not 0x055c <= d < 0x08bf for d in destinations):
        raise ValueError("enemy_run table escapes reviewed body")
    extents = []
    for extent in config["units"][0]["code_extents"]:
        start = extent["segment"] * 16 + extent["start"]
        end = start + extent["size"]
        extents.append({"name": extent["name"], "payload_offset": start,
                        "file_offset": start + image.header.header_size, "size": extent["size"],
                        "sha256": hashlib.sha256(image.program_image[start:end]).hexdigest(),
                        "ordered_relocation_sites": [r.linear - start for r in image.relocations
                                                     if start <= r.linear < end]})
    report = {
        "kind": "th03-main-enemy-raw-target-boundary-review",
        "target_sha256": hashlib.sha256(target).hexdigest(),
        "selection_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "decoder": f"capstone {capstone.__version__} x86 16-bit; diagnostic only",
        "functions": functions, "code_extents": extents,
        "enemy_run_switch": {"alignment_offset": 0x08bf, "table_offset": 0x08c0,
                             "table_size": 64, "keys": keys, "destinations": destinations},
        "acceptance": "boundary observations only; no compiler, runtime or exact credit",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    output.with_suffix(".txt").write_text("".join(disassembly))
    print(f"enemy target review: {len(functions)} functions, 3 extents, sparse table verified")


if __name__ == "__main__":
    main()
