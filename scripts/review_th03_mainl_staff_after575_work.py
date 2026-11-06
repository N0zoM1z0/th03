#!/usr/bin/env python3
"""Verify two complete source-native MAINL staff CODE+DATA compiler/linker rounds."""
import json

import build_th03_mainl_staff_after575_work as b
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz


def review():
    cfg,cfg_sha=b.inputs()
    row,report_sha=b.base.load(b.REPORT)
    previous,parent_sha=b.base.load(b.parent.REPORT)
    source,wrapper=b.sources(cfg)
    original=(b.WORK/cfg["original_object"]).read_bytes()
    original_target=(b.WORK/"bin/th03/mainl.target.exe").read_bytes()
    need(previous["complete"] and parent_sha==cfg["parent_report_sha256"],
         "actual independent natural cutscene and after570 sound source parent")
    need(row["complete"] and row["cold_rebuilt"] is False and
         row["library_rebuilt"] is False and
         row["game_objects_recompiled_per_round"]==1 and
         row["other_project_objects_reused"]==35 and
         row["canonical_factory_acceptance"] is False and
         row["whole_game_source_accepted"] is False and
         (row["original_CODE_bytes"],row["original_initialized_DATA_bytes"],
          row["original_PUBLIC_functions"],row["original_PUBLIC_DATA_names"])==(3695,224,19,6) and
         row["parent_report_sha256"]==parent_sha and row["config_sha256"]==cfg_sha and
         row["driver_sha256"]==sha((b.ROOT/b.DRIVER).read_bytes()) and
         row["maintained_source_sha256"]==sha(source) and
         row["source_wrapper_sha256"]==sha(wrapper) and
         row["original_object_sha256"]==sha(original),
         "all original source/OBJ/parent/recipe/acceptance bounds intact")
    need((b.SCRATCH/"driver.py").read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/"config.json").read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         "actual consumed compiler recipe source")
    phases=[f"round{n}-{step}" for n in (1,2)
            for step in ("staff-TC4-compile","normal-TLINK")]
    need(len(row["phases"])==4 and [x["label"] for x in row["phases"]]==phases and
         all(x["returncode"]==0 and
             sha((b.ROOT/x["log"]).read_bytes())==x["log_sha256"]
             for x in row["phases"]),
         "both original TCC/TLINK writer phase logs retained")
    vectors=[]
    for n,round_row in enumerate(row["rounds"],1):
        old=previous["rounds"][n-1]
        need(round_row["round"]==n and
             round_row["native_response_sha256"]==sha(b.response(n)) and
             (b.SCRATCH/f"r{n}.lnk").read_bytes()==b.response(n),
             "literal unchanged original MAINL normal response apart from staff slot")
        native={k:b.base.checked(v) for k,v in round_row["outputs"].items()}
        need(set(native)=={"obj","exe","map"} and
             (b.SCRATCH/f"r{n}/staffdat.obj").read_bytes()==native["obj"] and
             (b.SCRATCH/f"r{n}/staff_body.cpp").read_bytes()==source.replace(b"\n",b"\r\n") and
             (b.SCRATCH/f"r{n}/staffdat.cpp").read_bytes()==b.staged_wrapper(n),
             "actual compiler consumed complete maintained natural C++ body and wrapper")
        scope=b.obj_scope(native["obj"],original,cfg)
        need(round_row["scope"]==scope and
             scope["initialized_CODE_bytes"]==3695 and
             scope["initialized_DATA_bytes"]==224 and
             scope["original_CODE_PUBLIC_functions"]==19 and
             scope["original_DATA_PUBLIC_names"]==6 and
             scope["native_ordered_fixups"]==342 and
             scope["original_module_COMENT_LNAMES_packet_identity"] is False,
             "entire original CODE/DATA, 342 literal OMF field order, public names/positions and segment identity")
        need(native["exe"]==original_target==b.base.checked(old["outputs"]["exe"]) and
             len(native["exe"])==67372 and
             len(parse_mz(native["exe"]).relocations)==677 and
             b.map_normalized(native["map"],n)==b.base.checked(old["outputs"]["map"]) and
             round_row["entire_original_japanese_decoded_EXE_equal"] and
             round_row["complete_MAP_addresses_equal"],
             "all original MAINL decoded EXE bytes/MZ relocations and original native MAP geometry")
        vectors.append(native)
    def stable_map(raw,n):
        diagnostic=f"M=probe/af573c/r{n}/cutscene.cpp".encode()
        need(raw.count(diagnostic)==3,"only an upstream diagnostic name changes across source rounds")
        return b.map_normalized(raw,n).replace(diagnostic,b"M=source/cutscene.cpp")
    need(len(vectors)==2 and vectors[0]["exe"]==vectors[1]["exe"] and
         payload(vectors[0]["obj"])==payload(vectors[1]["obj"]) and
         literal_fields(vectors[0]["obj"])==literal_fields(vectors[1]["obj"]) and
         public_offsets(vectors[0]["obj"])==public_offsets(vectors[1]["obj"]) and
         stable_map(vectors[0]["map"],1)==stable_map(vectors[1]["map"],2),
         "full actual source-native two-round vectors repeat (diagnostic names aside)")
    return dict(complete=True,native_Turbo_CPP_rounds=2,source_native_module="staffdat",
        complete_original_CODE_bytes=3695,original_initialized_DATA_bytes=224,
        original_exported_code_procedures=19,original_exported_DATA_names=6,
        original_literal_OMF_fixups=342,
        complete_original_native_CODE_and_DATA_equal=True,
        original_full_OMF_packet_identity=False,
        original_67372_byte_japanese_decoded_MAINL_EXE_equal=True,
        original_ordered_677_MZ_relocations_equal=True,
        whole_product_source_accepted=False,canonical_factory_acceptance=False,
        independent_source_build_report_sha256=report_sha)

if __name__=="__main__":
    result=review()
    (b.ROOT/(b.PREFIX+"review.json")).write_text(json.dumps(result,indent=2)+"\n")
    print("Large MAINL STAFF: 3695 original CODE +224 DATA/19 complete procedures/342 OMF fixups, 2 original-equal native links.")
