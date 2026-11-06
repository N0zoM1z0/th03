#!/usr/bin/env python3
"""Read-only two-round score file, input wait and PI file loading source/link review."""
import json

import build_th03_mainl_score_input_pi_after587_work as b
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz


def review():
    cfg,cfg_sha,parent=b.inputs()
    report,report_sha=b.base.load(b.REPORT)
    sources=b.source_inputs(cfg)
    originals={u["stem"]:(b.WORK/u["original_object"]).read_bytes() for u in cfg["units"]}
    original_japanese=(b.WORK/"bin/th03/mainl.target.exe").read_bytes()
    need(report["complete"] and report["cold_rebuilt"] is False and
         report["library_rebuilt"] is False and
         report["project_objects_recompiled_per_round"]==3 and
         report["other_project_objects_reused"]==33 and
         (report["complete_score_input_pi_CODE_bytes"],report["original_PUBLIC_functions"],
          report["original_native_ordered_FIXUPP_sites"])==(425,6,32) and
         report["canonical_factory_credit_changed"] is False and
         report["whole_project_source_accepted"] is False and
         report["config_sha256"]==cfg_sha and
         report["parent_report_sha256"]==cfg["parent_report_sha256"] and
         report["driver_sha256"]==sha((b.ROOT/b.DRIVER).read_bytes()) and
         report["source_sha256"]==
           {s:{k:sha(v) for k,v in data.items()} for s,data in sources.items()} and
         report["original_object_sha256"]=={s:sha(raw) for s,raw in originals.items()} and
         report["original_japanese_decoded_EXE_SHA256"]==sha(original_japanese),
         "genuine complete bounded Turbo C++ natural source inputs and unchanged older source/target")
    need((b.SCRATCH/"driver.py").read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/"config.json").read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         "actual native compiler source recipe pinned")
    phases=[label for n in (1,2) for label in (
        [f"round{n}-{s}-TC4-compile" for s in b.ORDER]+[f"round{n}-normal-TLINK"])]
    need(len(report["phases"])==8 and
         [p["label"] for p in report["phases"]]==phases and
         all(p["returncode"]==0 and
             sha((b.ROOT/p["log"]).read_bytes())==p["log_sha256"] for p in report["phases"]),
         "two real three-object Turbo C++/TLINK rounds with eight logs")
    vectors=[]
    for n,row in enumerate(report["rounds"],1):
        previous=parent["rounds"][n-1]["outputs"]
        need(row["round"]==n and
             row["original_link_response_SHA256"]==sha(b.response(n)) and
             (b.SCRATCH/f"r{n}.lnk").read_bytes()==b.response(n) and
             row["full_japanese_MAINL_EXE_equal"],
             "literal normal C0/CRT/mainl first-use link response and source-root")
        outputs={key:b.base.checked(pin) for key,pin in row["outputs"].items()}
        need(set(outputs)=={s+"_obj" for s in b.ORDER}|{"exe","map"},
             "complete three raw OBJ files, EXE and MAP from retained native stage")
        for unit in cfg["units"]:
            s=unit["stem"]
            obj=outputs[s+"_obj"]
            scope=b.object_scope(obj,originals[s],unit)
            need(scope==row["source_objects"][s] and
                 (b.SCRATCH/f"r{n}/{s}.cpp").read_bytes()==
                   sources[s]["wrapper"].replace(b"\n",b"\r\n") and
                 (b.SCRATCH/f"r{n}/{s}.obj").read_bytes()==obj and
                 payload(obj)==payload(originals[s]) and
                 literal_fields(obj)==literal_fields(originals[s]) and
                 public_offsets(obj)==public_offsets(originals[s]),
                 "original whole source CODE, native ordered references, ABI and actual emitted object "+s)
        need(outputs["exe"]==original_japanese==b.base.checked(previous["exe"]) and
             len(outputs["exe"])==67372 and
             parse_mz(outputs["exe"]).relocations==parse_mz(original_japanese).relocations and
             len(parse_mz(outputs["exe"]).relocations)==677 and
             b.normalize_map(outputs["map"],n)==b.base.checked(previous["map"]),
             "original complete decoded MAINL program and all ordered relocation entries/MAP geometry")
        vectors.append(outputs)
    need(len(vectors)==2 and vectors[0]["exe"]==vectors[1]["exe"] and
         all(payload(vectors[0][s+"_obj"])==payload(vectors[1][s+"_obj"])
             and literal_fields(vectors[0][s+"_obj"])==literal_fields(vectors[1][s+"_obj"])
             for s in b.ORDER) and
         b.stable_map(vectors[0]["map"],1)==b.stable_map(vectors[1]["map"],2),
         "two independent native source/link output sets repeat, except known previous diagnostic paths")
    return dict(complete=True,source_C_CPP_rounds=2,
        complete_original_CODE_bytes=425,complete_original_public_procedures=6,
        original_native_FIXUPP_fields=32,
        original_score_CODE_bytes=229,original_input_wait_CODE_bytes=126,original_PI_load_CODE_bytes=70,
        complete_original_japanese_decoded_EXE_equal=True,
        original_MAINL_decoded_EXE_bytes=67372,ordered_original_MZ_relocations=677,
        whole_project_source_accepted=False,canonical_factory_acceptance=False,
        original_vendor_OMF_packet_identity_unproven=True,
        native_build_report_SHA256=report_sha)


if __name__=="__main__":
    result=review()
    (b.ROOT/(b.PREFIX+"review.json")).write_text(json.dumps(result,indent=2)+"\n")
    print("Three native Turbo C++ score/input/PI modules: 425 CODE bytes, 6 funcs and 32 ordered fixups; two exact original MAINL EXEs.")
