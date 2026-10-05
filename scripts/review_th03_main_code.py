#!/usr/bin/env python3
"""Export raw target observations for complete manifest-selected MAIN owners.

Manifest selection and semantic names are review hypotheses. This diagnostic
checks their complete byte partition and decodes target instructions; it does
not grant compiler, runtime, whole-product or exact acceptance.
"""

import argparse
import hashlib
import json
from pathlib import Path
import tomllib

import capstone

from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from replay_th03_main_exact_units import normalized_code_extents

ROOT = Path(__file__).resolve().parents[1]


def observe(config, target, owner_ids):
    image = parse_mz(target)
    if not image.valid or hashlib.sha256(target).hexdigest() != config["target_sha256"]:
        raise ValueError("target identity or format differs")
    owners = [u for u in config["units"] if u["id"] in owner_ids]
    if len(owners) != len(owner_ids) or len(set(owner_ids)) != len(owner_ids) or not owners:
        raise ValueError("unknown or empty owner selection")
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    observations = []
    disassembly = []
    for owner in owners:
        extents = normalized_code_extents(owner, config["segment"])
        owner_functions = [f for f in config["functions"] if f["object"] == owner["object"]]
        matched_functions = []
        for extent in extents:
            segment, start, size = extent["segment"], extent["start"], extent["size"]
            base = segment * 16
            coverage = [None] * size
            functions = []
            for function in owner_functions:
                offset, length = function["offset"], function["size"]
                if function.get("segment", config["segment"]) != segment or not start <= offset < start + size:
                    continue
                if offset + length > start + size:
                    raise ValueError("function crosses ownership edge")
                matched_functions.append(function["name"])
                for i in range(offset - start, offset - start + length):
                    if coverage[i] is not None:
                        raise ValueError("overlapping function ownership")
                    coverage[i] = function["name"]
                code = image.program_image[base + offset:base + offset + length]
                instructions = list(decoder.disasm(code, offset))
                if sum(i.size for i in instructions) != length:
                    raise ValueError("undecoded function bytes")
                last = instructions[-1]
                if last.mnemonic not in {"ret", "retf"}:
                    raise ValueError("reviewed body does not end in RET")
                functions.append({
                    "semantic_name_candidate": function["name"], "offset": offset,
                    "size": length, "sha256": hashlib.sha256(code).hexdigest(),
                    "return": f"{last.mnemonic} {last.op_str}".strip(),
                    "calls": [{"offset": i.address, "instruction": f"{i.mnemonic} {i.op_str}"}
                              for i in instructions if i.mnemonic in {"call", "lcall"}],
                    "jumps": [{"offset": i.address, "instruction": f"{i.mnemonic} {i.op_str}"}
                              for i in instructions if i.mnemonic.startswith("j")],
                })
                disassembly.append(f"\n{function['name']} {segment:04X}:{offset:04X} size={length}\n")
                disassembly.extend(f"{i.address:04X} {i.bytes.hex():24} {i.mnemonic} {i.op_str}\n"
                                   for i in instructions)
            for producer in extent["producer_ranges"]:
                for i in range(producer["relative"], producer["relative"] + producer["size"]):
                    if i < 0 or i >= size or coverage[i] is not None:
                        raise ValueError("invalid producer ownership")
                    coverage[i] = producer["kind"]
            if None in coverage:
                raise ValueError("unclassified owner bytes")
            payload_start = base + start
            payload_end = payload_start + size
            if payload_end > len(image.program_image):
                raise ValueError("owner exceeds target image")
            if any(r.linear < payload_end and r.linear + 2 > payload_start and
                   not payload_start <= r.linear <= payload_end - 2 for r in image.relocations):
                raise ValueError("relocation crosses ownership edge")
            observations.append({
                "owner": owner["id"], "ledger_id": extent["ledger_id"],
                "segment": segment, "offset": start, "size": size,
                "file_offset": payload_start + image.header.header_size,
                "sha256": hashlib.sha256(image.program_image[payload_start:payload_end]).hexdigest(),
                "ordered_relocation_sites": [r.linear - payload_start for r in image.relocations
                                             if payload_start <= r.linear < payload_end],
                "producer_ranges": extent["producer_ranges"], "functions": functions,
            })
        if sorted(matched_functions) != sorted(f["name"] for f in owner_functions):
            raise ValueError("function does not map exactly once to selected owner extents")
    return observations, "".join(disassembly)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=ROOT / "config/th03_main_exact_units.toml")
    parser.add_argument("--owner", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / ".analysis"):
        raise ValueError("target exports belong under .analysis/")
    config = tomllib.loads(args.manifest.read_text())
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), config["artifact"])
    target = read_verified_artifact(ROOT, artifact)
    observations, disassembly = observe(config, target, args.owner)
    report = {
        "kind": "th03-main-raw-owner-boundary-observations",
        "target_sha256": hashlib.sha256(target).hexdigest(),
        "manifest_sha256": hashlib.sha256(args.manifest.read_bytes()).hexdigest(),
        "decoder": f"capstone {capstone.__version__} x86 16-bit; diagnostic only",
        "extents": observations, "acceptance": "review observations only; no exact credit",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    output.with_suffix(".txt").write_text(disassembly)
    print(f"raw MAIN review: {len(args.owner)} owners, {len(observations)} complete extents")


if __name__ == "__main__":
    main()
