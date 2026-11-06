#!/usr/bin/env python3
"""Review complete score/load, 739-byte name editor and 348-byte rank menu."""
import json

import build_th03_mainl_hiscore_after578_work as b
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz


def review():
    cfg,cfg_sha=b.inputs()
    record,report_sha=b.base.load(b.REPORT)
    prev,prev_sha=b.base.load(b.parent.REPORT)
    contents=b.sources(cfg)
    original=(b.WORK/cfg["original_object"]).read_bytes()
    target=(b.WORK/"bin/th03/mainl.target.exe").read_bytes()
    need(prev["complete"] and prev_sha==cfg["parent_report_sha256"] and
         record["complete"] and record["cold_rebuilt"] is False and
         record["library_rebuilt"] is False and
         record["recompiled_project_objects_per_round"]==1 and
         record["other_project_objects_reused"]==35 and
         (record["source_CODE_bytes"],record["source_DATA_bytes"],
          record["source_CODE_functions"])==(2788,40,15) and
         record["canonical_factory_credit_changed"] is False and
         record["whole_product_source_accepted"] is False and
         record["driver_sha256"]==sha((b.ROOT/b.DRIVER).read_bytes()) and
         record["config_sha256"]==cfg_sha and
         record["parent_report_sha256"]==prev_sha and
         record["maintained_sources_sha256"]=={key:sha(content) for key,content in contents.items()} and
         record["original_object_sha256"]==sha(original),
         "full current natural C++/parent/authoritative source object provenance")
    need((b.SCRATCH/"driver.py").read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/"config.json").read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         "the actual native source builder and compilation profile were retained")
    expected=[f"round{n}-{label}" for n in (1,2)
              for label in ("highscore-TC4-compile","normal-TLINK")]
    need(len(record["phases"])==4 and
         [x["label"] for x in record["phases"]]==expected and
         all(x["returncode"]==0 and
             sha((b.ROOT/x["log"]).read_bytes())==x["log_sha256"]
             for x in record["phases"]),
         "all four real native compiler/linker writer phases and logs")
    names=public_offsets(original)
    assert names["@regist_name_enter_menu$qv"]["segment_index"]==1
    need(names["@regist_name_enter_menu$qv"]["offset"]==1501 and
         names["@regist_replace_same_letter_name_$qv"]["offset"]==2240 and
         names["@regist_menu$qv"]["offset"]==2372 and
         names["_mainl_reg_music"]["offset"]==2720,
         "independently original public name editor 739 B and near menu 348 B code bounds")
    pairs=[]
    for n,row in enumerate(record["rounds"],1):
        old=prev["rounds"][n-1]["outputs"]
        need(row["round"]==n and
             row["original_link_response_sha256"]==sha(b.response(n)) and
             (b.SCRATCH/f"r{n}.lnk").read_bytes()==b.response(n),
             "single original large score source slot in the first-use TLINK response")
        raw={k:b.base.checked(v) for k,v in row["outputs"].items()}
        need(set(raw)=={"obj","exe","map"} and
             (b.SCRATCH/f"r{n}/regdata.obj").read_bytes()==raw["obj"] and
             (b.SCRATCH/f"r{n}/regdata_body.cpp").read_bytes()==
               contents["nested_source"].replace(b"\n",b"\r\n") and
             (b.SCRATCH/f"r{n}/regdata.cpp").read_bytes()==b.native_wrapper(n),
             "actual compiler input and full native source object")
        scope=b.object_scope(raw["obj"],original,cfg)
        need(scope==row["scope"] and
             scope["original_CODE_bytes"]==2788 and
             scope["initialized_DATA_bytes"]==40 and
             scope["original_CODE_FUNCTIONS"]==15 and
             scope["original_DATA_PUBLICs"]==1 and
             scope["ordered_native_FIXUPP_count"]==188 and
             scope["full_original_CODE_and_DATA_equal"] and
             scope["original_historical_OMF_COMENT_packet_identity"] is False,
             "complete original high-score GAME3 near-Pascal CODE, original typed DATA and all 188 ordered fixups")
        need(raw["exe"]==target==b.base.checked(old["exe"]) and
             len(raw["exe"])==67372 and
             len(parse_mz(raw["exe"]).relocations)==677 and
             b.map_normalized(raw["map"],n)==b.base.checked(old["map"]) and
             row["complete_original_japanese_EXE_equal"] and row["MAP_coordinates_identical"],
             "full source-native MAINL EXE and all original 677 ordered relocations/MAP rows")
        pairs.append(raw)
    def stable_map(raw,n):
        value=b.map_normalized(raw,n)
        for stage,stem in (("af573c","cutscene"),("af575s","staffdat")):
            old=f"M=probe/{stage}/r{n}/{stem}.cpp".encode()
            need(value.count(old)==3,"all previous CODE/DATA/BSS module diagnostic rows")
            value=value.replace(old,f"M=source/{stem}.cpp".encode())
        return value
    need(len(pairs)==2 and
         pairs[0]["exe"]==pairs[1]["exe"] and
         payload(pairs[0]["obj"])==payload(pairs[1]["obj"]) and
         literal_fields(pairs[0]["obj"])==literal_fields(pairs[1]["obj"]) and
         public_offsets(pairs[0]["obj"])==public_offsets(pairs[1]["obj"]) and
         stable_map(pairs[0]["map"],1)==stable_map(pairs[1]["map"],2),
         "both independent original C++ produced native OBJ/EXE/MAP vectors repeat")
    return dict(complete=True,native_C_CPP_rounds=2,maintained_cpp_nested_source=True,
                code_bytes=2788,initialized_DATA_bytes=40,
                original_near_code_functions=15,
                name_input_menu_original_bytes=739,registration_menu_original_bytes=348,
                original_ordered_OMF_fixups=188,original_publics=16,
                original_full_raw_OMF_packet_identity=False,
                complete_original_japanese_67372_decoded_EXE_equal=True,
                full_ordered_original_MZ_relocations=677,
                whole_product_source_accepted=False,canonical_factory_acceptance=False,
                source_native_report_sha256=report_sha)

if __name__=="__main__":
    result=review()
    (b.ROOT/(b.PREFIX+"review.json")).write_text(json.dumps(result,indent=2)+"\n")
    print("MAINL natural score editor: 2788 CODE/40 DATA, 739-byte name editor +348-byte menu, 2 whole original 67372 EXEs exact.")
