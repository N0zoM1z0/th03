#!/usr/bin/env python3
"""Target-first exact-boundary intake for Marisa's complete HITBOX prefix.

This does NOT grant exactness: no maintained natural compiler producer,
physical DATA/BSS owner or full-link MAP/ordered MZ acceptance is implied.
The original Japanese target bytes, function return boundaries and
contained ordered MZ sites independently constrain future source work.
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
from lib.targets import read_verified_artifact,load_target_manifest,find_artifact
from replay_th03_main_exact_units import normalized_code_extents

ROOT=Path(__file__).resolve().parents[1]
START=0x142D0
END=0x14A76
# Original proc boundaries cross-checked against instruction terminal returns.
# Explicit early 0x14465 RETF remains within chargeshot_update_marisa.
FUNCTIONS=(
    ("marisa_chargeshot_state_reset",0x142D0,0x142DF,"retf",None),
    ("chargeshot_add_marisa",0x142DF,0x14340,"retf",4),
    ("marisa_hyper_14340",0x14340,0x143BE,"retf",None),
    ("chargeshot_update_marisa",0x143BE,0x14487,"retf",None),
    ("chargeshot_hittest_marisa",0x14487,0x14511,"retf",None),
    ("chargeshot_render_marisa",0x14511,0x146AF,"retf",None),
    ("gauge_pattern_marisa",0x146AF,0x14885,"ret",2),
    ("gba_gauge_pattern_pellet_marisa",0x14885,0x1489D,"retf",None),
    ("gba_gauge_pattern_bullet_marisa",0x1489D,0x148B5,"retf",None),
    ("marisa_bomb",0x148B5,0x14A76,"retf",None),
)


def digest(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()


def inspect_body(image, spec) -> dict:
    name,lo,hi,return_type,ret_immediate=spec
    if not image.valid or not(0<=lo<hi<=len(image.program_image)):
        raise ValueError("invalid immutable target body "+name)
    for fix in image.relocations:
        if fix.linear < hi and fix.linear+2 > lo:
            if not(lo<=fix.linear<=hi-2):
                raise ValueError("relocation straddles body edge "+name)
    raw=image.program_image[lo:hi]
    decoded=list(capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_16).disasm(raw,lo))
    if not decoded or sum(x.size for x in decoded)!=len(raw):
        raise ValueError("uninterpreted bytes in original function "+name)
    last=decoded[-1]
    if last.address+last.size != hi or last.mnemonic != return_type:
        raise ValueError("original function return edge moved "+name)
    if (ret_immediate is None and last.op_str
        or ret_immediate is not None and last.op_str!=str(ret_immediate)):
        raise ValueError("original function stack cleanup changed "+name)
    inside_rets=[x.address for x in decoded[:-1] if x.mnemonic in ("ret","retf")]
    if (name=="chargeshot_update_marisa") != bool(inside_rets):
        raise ValueError("unexpected internal early return "+name)
    if name=="chargeshot_update_marisa" and inside_rets != [0x14464]:
        raise ValueError("the original update early RETF site changed")
    sites=[fix.linear-lo for fix in image.relocations if lo<=fix.linear<hi]
    return dict(
        name=name,load_start=f"0x{lo:05X}",load_end_exclusive=f"0x{hi:05X}",
        physical_segment="HITBOX_TEXT",map_group="MAIN_04",
        map_start=f"139D:{lo-(0x139d*16):04X}",
        program_image_start=lo,size=len(raw),sha256=digest(raw),
        instruction_count=len(decoded),linear_decoded_bytes=len(raw),
        return_instruction=last.mnemonic+(" "+last.op_str if last.op_str else ""),
        intermediate_return_addresses=[f"0x{x:05X}" for x in inside_rets],
        ordered_mz_fixupp_sites=sites,mz_fixupp_count=len(sites),
        exact=False,maintained_source=False,
        semantic_source_hypothesis_only=True,
    )


def review() ->dict:
    m=tomllib.loads((ROOT/"config/th03_main_exact_units.toml").read_text())
    original=read_verified_artifact(ROOT,find_artifact(load_target_manifest(ROOT/"config/targets.toml"),"th03-main"))
    img=parse_mz(original)
    if not img.valid or digest(original)!=m["target_sha256"]:
        raise ValueError("original target identity or structure mismatch")
    accepted=[(e["segment"]*16+e["start"],e["segment"]*16+e["start"]+e["size"],u["id"])
              for u in m["units"] for e in normalized_code_extents(u,m["segment"])]
    if any(a<END and b>START for a,b,_ in accepted):
        raise ValueError("Marisa candidate overlaps previously accepted exact CODE")
    cursor=START
    bodies=[]
    for spec in FUNCTIONS:
        if spec[1]!=cursor:
            raise ValueError("original function body gap or overlap")
        bodies.append(inspect_body(img,spec))
        cursor=spec[2]
    if cursor!=END or sum(x["size"] for x in bodies)!=1958:
        raise ValueError("Marisa complete target prefix was not partitioned")
    reloc=[x.linear-START for x in img.relocations if START<=x.linear<END]
    if sum(x["mz_fixupp_count"] for x in bodies)!=len(reloc) or len(reloc)!=30:
        raise ValueError("Marisa original relocation partition mismatch")
    if len(bodies)!=10 or [x["size"] for x in bodies]!=[15,97,126,201,138,414,470,24,24,449]:
        raise ValueError("large Marisa function boundaries changed")
    return {
        "kind":"th03-main-marisa-gameplay-logical-coverage-provisional",
        "exact_acceptance":False,
        "whole_physical_owner_accepted":False,
        "original_target_sha256":digest(original),
        "original_payload_span":[f"0x{START:05X}",f"0x{END:05X}"],
        "bytes":1958,"function_count":len(bodies),
        "original_ordered_mz_relocations":reloc,
        "segment":"HITBOX_TEXT","group":"MAIN_04",
        "original_frozen_carrier_map_extent":"139D:0900..1F25",
        "functions":bodies,
        "reviewed_exact_scope_unchanged":len(m["functions"]),
        "notes":"Target-only complete logical function intervals; near/far calling arguments, physical producer partitions and DATA/BSS still need compiler/source/Oracle verification. Preserve original update internal early RETF.",
    }


def main()->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-id",default="marisa-gameplay-target-review-v1")
    args=ap.parse_args()
    if not args.run_id or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for ch in args.run_id):
        raise ValueError("invalid review run-id")
    out=ROOT/".analysis/th03-main-marisa-gameplay"/(args.run_id+".json")
    if out.exists():
        raise ValueError("target-first Marisa receipt already exists; choose a new run-id")
    r=review()
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(r,indent=2)+"\n")
    print(f"Marisa HITBOX target-first: {r['function_count']} COMPLETE logical bodies, {r['bytes']} B, 30 original ordered MZ sites; 0 newly exact")
    for f in r["functions"]:
        print(f" {f['name']} {f['size']} B, {f['return_instruction']}, {f['mz_fixupp_count']} relocations")
    print(f"Receipt: {out.relative_to(ROOT)}")
    return 0


if __name__=="__main__":
    sys.exit(main())
