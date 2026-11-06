#!/usr/bin/env python3
"""Read-only two-round source-native MAINL root/C++ orchestration review."""
import json

import build_th03_mainl_root_controller_after580_work as b
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz


def review():
    cfg,cfg_sha=b.inputs()
    row,report_sha=b.base.load(b.REPORT)
    parent,parent_sha=b.base.load(b.parent.REPORT)
    code,wrapper=b.sources(cfg)
    original=(b.WORK/cfg["original_object"]).read_bytes()
    japanese=(b.WORK/"bin/th03/mainl.target.exe").read_bytes()
    need(parent["complete"] and parent_sha==cfg["parent_report_sha256"] and
         row["complete"] and row["cold_rebuilt"] is False and
         row["library_rebuilt"] is False and
         row["recompiled_game_objects_per_round"]==1 and
         row["other_game_objects_reused"]==35 and
         (row["original_CODE_bytes"],row["original_initialized_DATA_bytes"],
          row["original_BSS_allocation_bytes"])==(2458,112,186) and
         row["canonical_factory_credit_changed"] is False and
         row["whole_product_source_accepted"] is False and
         row["source_SHA256"]==sha(code) and
         row["wrapper_SHA256"]==sha(wrapper) and
         row["original_object_SHA256"]==sha(original) and
         row["parent_report_SHA256"]==parent_sha and
         row["config_SHA256"]==cfg_sha and
         row["driver_SHA256"]==sha((b.ROOT/b.DRIVER).read_bytes()),
         "all original real 11-function source, original object and native parent pins")
    need((b.SCRATCH/"driver.py").read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/"config.json").read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         "compiler actually consumed retained recipe and config")
    labels=[f"round{n}-{step}" for n in (1,2) for step in
            ("root-TC4-compile","normal-TLINK")]
    need([r["label"] for r in row["phases"]]==labels and
         len(row["phases"])==4 and
         all(r["returncode"]==0 and sha((b.ROOT/r["log"]).read_bytes())==r["log_sha256"]
             for r in row["phases"]),"four complete native TCC/TLINK writer logs retained")
    vectors=[]
    for n,round_data in enumerate(row["rounds"],1):
        old=parent["rounds"][n-1]["outputs"]
        raw={k:b.base.checked(pin) for k,pin in round_data["outputs"].items()}
        need(round_data["round"]==n and
             round_data["response_SHA256"]==sha(b.response(n)) and
             (b.SCRATCH/f"r{n}.lnk").read_bytes()==b.response(n) and
             (b.SCRATCH/f"r{n}/rootdata.obj").read_bytes()==raw["obj"] and
             (b.SCRATCH/f"r{n}/root_body.cpp").read_bytes()==code.replace(b"\n",b"\r\n") and
             (b.SCRATCH/f"r{n}/rootdata.cpp").read_bytes()==b.native_wrapper(n),
             "exact object and actual 16-bit compiler source in normal link")
        scope=b.scope(raw["obj"],original,cfg)
        need(scope==round_data["scope"] and
             scope["CODE_bytes"]==2458 and scope["DATA_bytes"]==112 and
             scope["BSS_bytes"]==186 and
             scope["original_code_publics"]==11 and
             scope["original_data_publics"]==3 and
             scope["original_bss_publics"]==3 and
             scope["original_ordered_fixups"]==278 and
             scope["all_original_initialized_BYTES_and_ABI_equal"],
             "original exact 11 root function CODE, literal ordered OMF, initialized DATA/BSS/publics")
        need(raw["exe"]==japanese==b.base.checked(old["exe"]) and
             len(raw["exe"])==67372 and
             parse_mz(raw["exe"]).relocations==parse_mz(japanese).relocations and
             len(parse_mz(raw["exe"]).relocations)==677 and
             b.normalize_map(raw["map"],n)==b.base.checked(old["map"]) and
             round_data["complete_Japanese_MAINL_EXE_equal"],
             "whole original decoded Japanese EXE/ordered relocations and exact MAP geometry")
        vectors.append(raw)
    need(len(vectors)==2 and vectors[0]["exe"]==vectors[1]["exe"] and
         b.stable_map(vectors[0]["map"],1)==b.stable_map(vectors[1]["map"],2) and
         payload(vectors[0]["obj"])==payload(vectors[1]["obj"]) and
         literal_fields(vectors[0]["obj"])==literal_fields(vectors[1]["obj"]) and
         public_offsets(vectors[0]["obj"])==public_offsets(vectors[1]["obj"]),
         "two source-generated independent whole object and original native link vectors repeat")
    return dict(complete=True,native_Turbo_CPP_rounds=2,
        major_original_root_functions=11,original_CODE_bytes=2458,
        initialized_DATA_bytes=112,original_BSS_bytes=186,
        original_ordered_OMF_FIXUPP_fields=278,
        all_original_public_symbols=17,
        original_vendor_OMF_packet_identical=False,
        original_complete_67372_byte_japanese_MAINL_EXE_equal=True,
        original_ordered_MZ_relocations=677,
        whole_product_source_accepted=False,canonical_factory_acceptance=False,
        native_source_build_report_sha256=report_sha)


if __name__=="__main__":
    r=review()
    (b.ROOT/(b.PREFIX+"review.json")).write_text(json.dumps(r,indent=2)+"\n")
    print("Natural root CFG/win/story/stage C++: 2458 CODE/112 DATA/186 BSS, 11 procedures/278 fields, two whole 67372 MAINL EXEs exact.")
