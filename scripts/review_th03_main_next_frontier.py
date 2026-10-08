#!/usr/bin/env python3
"""Target-first, non-exact MAIN next-owner interval intake.

All starts/stops below are hypotheses for COMPLETE contiguous CODE intervals,
not newly accepted logical or physical producer owners. They are checked
against the immutable Japanese MAIN.EXE by 16-bit decode, relocation edges,
original target bytes and every previously accepted exact extent.

Known frozen ASM/Ghidra names are corroboration only, never acceptance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import tomllib

import capstone

from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from replay_th03_main_exact_units import normalized_code_extents

ROOT = Path(__file__).resolve().parents[1]

# The exact-review priority is set by game-state dependencies and subsystem
# boundaries, not byte count. Every range is a target LOAD-image offset.
CANDIDATES = (
    dict(id="main-marisa-charge-hitbox-prefix", start=0x142D0, end=0x14A76,
         terminal="retf", subsystem="Marisa charge-shot, hyper and hitbox prefix",
         caution="many far/near functions, sprite/shot/gauge deps; no trusted owner partition yet"),
    dict(id="main-ordinary-shot-producer-prefix", start=0xE266, end=0xE313,
         terminal="ret", subsystem="ordinary-shot low-level producer",
         caution="includes PC-98 graphics IO; verify device ABI and callers"),
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def observe_candidate(image, candidate: dict) -> dict:
    """Read exactly one bounded interval, refusing decode or relocation drift."""
    start, end = candidate["start"], candidate["end"]
    if not image.valid or not (0 <= start < end <= len(image.program_image)):
        raise ValueError(f"invalid next-owner interval {candidate['id']}")
    for relocated in image.relocations:
        if relocated.linear < end and relocated.linear + 2 > start:
            if not start <= relocated.linear <= end - 2:
                raise ValueError(f"relocation crosses boundary of {candidate['id']}")
    raw = image.program_image[start:end]
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    decoded = list(decoder.disasm(raw, start))
    if not decoded or sum(i.size for i in decoded) != len(raw):
        raise ValueError(f"not fully 16-bit linearly decodable: {candidate['id']}")
    final = decoded[-1]
    if final.mnemonic != candidate["terminal"] or final.address + final.size != end:
        raise ValueError(f"terminal return boundary not supported: {candidate['id']}")
    sites = [r.linear - start for r in image.relocations if start <= r.linear < end]
    return {
        "id": candidate["id"],
        "subsystem_hypothesis": candidate["subsystem"],
        "abi_dependency_risks": candidate["caution"],
        "start": f"0x{start:05X}", "end_exclusive": f"0x{end:05X}",
        "load_image_offset": start, "size": len(raw), "raw_sha256": sha(raw),
        "linear_decoded_bytes": len(raw),
        "instruction_count": len(decoded),
        "terminal_mnemonic": final.mnemonic,
        "terminal_instruction_bytes": raw[-final.size:].hex(),
        "far_direct_calls": sum(i.mnemonic == "lcall" for i in decoded),
        "near_direct_calls": sum(i.mnemonic == "call" for i in decoded),
        "relocation_count": len(sites),
        "ordered_relocation_sites": sites,
        "source_present": False,
        "code_exact": False,
        "owner_partition_accepted": False,
        "evidence_limit": "Target interval bytes/linear decode and relocation containment only; functions, DATA/BSS, producer, ABI and full-link exact remain unreviewed.",
    }


def existing_exact_spans(manifest: dict) -> list[tuple[int, int, str]]:
    accepted = []
    for unit in manifest["units"]:
        for extent in normalized_code_extents(unit, manifest["segment"]):
            absolute_start = extent["segment"] * 16 + extent["start"]
            accepted.append((absolute_start, absolute_start + extent["size"], unit["id"]))
    return accepted


def review() -> dict:
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-main")
    target = read_verified_artifact(ROOT, artifact)
    image = parse_mz(target)
    if not image.valid:
        raise ValueError("target MZ failed integrity checks")
    manifest = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    if sha(target) != manifest["target_sha256"]:
        raise ValueError("immutable target digest differs from scoped Oracle binding")
    accepted = existing_exact_spans(manifest)
    spans = []
    for candidate in CANDIDATES:
        lo,hi = candidate["start"],candidate["end"]
        if any(a < hi and b > lo for a,b,_ in accepted):
            raise ValueError(f"next-owner interval overlaps existing exact CODE: {candidate['id']}")
        if any(a["load_image_offset"] < hi and int(a["end_exclusive"],16) > lo for a in spans):
            raise ValueError("candidate ranges overlap")
        spans.append(observe_candidate(image,candidate))
    return {
        "kind":"th03-main-next-frontier-target-interval-review",
        "artifact":"th03-main",
        "target_sha256":sha(target),
        "scope":"two remaining provisional unowned CODE intervals; Hyper and complete HUD owners exact in default manifest",
        "existing_exact_function_count":len(manifest["functions"]),
        "existing_exact_extent_count":len(accepted),
        "candidates":spans,
        "total_provisional_interval_bytes":sum(x["size"] for x in spans),
        "all_intervals_nonoverlapping_existing_exact_code":True,
        "compiler_object_acceptance":False,
        "full_link_exact":False,
        "historical_data_ownership_resolved":False,
    }


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",default=".analysis/th03-main-next-frontier/target-review-v3.json")
    args=parser.parse_args()
    p=(ROOT / args.output).resolve()
    if not p.is_relative_to((ROOT / ".analysis").resolve()):
        raise ValueError("review output must be in .analysis/")
    result=review()
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,indent=2)+"\n")
    print(f"MAIN target-first frontier: {len(result['candidates'])} NON-EXACT intervals; {result['total_provisional_interval_bytes']} fully decoded bytes")
    for entry in result["candidates"]:
        print(f"{entry['id']}: {entry['size']} B, {entry['relocation_count']} ordered relocation sites, decode complete, {entry['terminal_mnemonic']}")
    print(f"review: {p.relative_to(ROOT)}")
    return 0


if __name__=="__main__":
    sys.exit(main())
