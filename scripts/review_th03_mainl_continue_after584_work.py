#!/usr/bin/env python3
"""Read-only original 417-byte continue-menu C++ segment regression review."""
import json
import build_th03_mainl_continue_after584_work as b
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz


def review():
    cfg,cfg_sha=b.inputs()
    row,report_sha=b.base.load(b.REPORT)
    previous,parent_sha=b.base.load(b.parent.REPORT)
    historical,corrected,wrapper=b.sources(cfg)
    original=(b.WORK/cfg["original_object"]).read_bytes()
    japanese=(b.WORK/"bin/th03/mainl.target.exe").read_bytes()
    negative=b.wrong_segment_control(cfg,original)
    need(previous["complete"] and parent_sha==cfg["parent_report_sha256"] and
         row["complete"] and row["cold_rebuilt"] is False and
         row["library_rebuilt"] is False and
         row["compiled_project_objects_per_round"]==1 and
         row["other_project_objects_reused"]==35 and
         row["natural_CPP_CODE_bytes"]==417 and
         row["original_public_function_count"]==1 and
         row["original_native_fixups"]==35 and
         row["historic_wrong_pragma_unchanged"] and
         row["canonical_factory_credit_changed"] is False and
         row["whole_product_source_accepted"] is False and
         row["original_wrong_source_sha256"]==sha(historical) and
         row["corrected_source_sha256"]==sha(corrected) and
         row["wrapper_sha256"]==sha(wrapper) and
         row["original_object_sha256"]==sha(original) and
         row["driver_sha256"]==sha((b.ROOT/b.DRIVER).read_bytes()) and
         row["config_sha256"]==cfg_sha and
         row["parent_report_sha256"]==parent_sha and
         row["real_negative_segment_control"]==negative,
         "actual original natural source and one-pragma correction, preserved real negative control")
    need(negative["original_untouched_historical_source_segment"]=="CONTINUE_TEXT" and
         negative["corrected_natural_Turbo_CPP_segment"]=="CUTSCENE_TEXT" and
         negative["both_assembled_CODE_and_FIXUPPs_identical"] and
         negative["bad_normal_LINK_relocations"]==696 and
         negative["original_NORMAL_LINK_relocations"]==677 and
         negative["bad_EXE_not_equal"] and negative["good_EXE_byte_equal"],
         "documented original 696-relocation failure and true 677-relocation source repair")
    need((b.SCRATCH/"driver.py").read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/"config.json").read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         "native compiler recipe retained verbatim")
    labels=[f"round{n}-{label}" for n in (1,2)
            for label in ("original-segment-TC4","normal-TLINK")]
    need(len(row["phases"])==4 and
         [x["label"] for x in row["phases"]]==labels and
         all(x["returncode"]==0 and sha((b.ROOT/x["log"]).read_bytes())==x["log_sha256"]
             for x in row["phases"]), "all four genuine native first-use C++ compiler/linker logs")
    results=[]
    for n,item in enumerate(row["rounds"],1):
        prior=previous["rounds"][n-1]["outputs"]
        need(item["round"]==n and
             item["original_link_response_sha256"]==sha(b.response(n)) and
             (b.SCRATCH/f"r{n}.lnk").read_bytes()==b.response(n),
             "single original project source slot/unchanged source/CRT normal link")
        files={k:b.base.checked(pin) for k,pin in item["outputs"].items()}
        need(set(files)=={"obj","exe","map"} and
             (b.SCRATCH/f"r{n}/contmenu.obj").read_bytes()==files["obj"] and
             (b.SCRATCH/f"r{n}/continue_body.cpp").read_bytes()==corrected.replace(b"\n",b"\r\n") and
             (b.SCRATCH/f"r{n}/contmenu.cpp").read_bytes()==b.staged_wrapper(n),
             "real compiled source and 417-byte object staged independently")
        scope=b.original_scope(files["obj"],original,cfg)
        need(scope==item["scope"] and
             scope["original_initialized_CODE_bytes"]==417 and
             scope["original_FIXUPP_sites"]==35 and
             scope["original_PUBLICs"]==1 and
             scope["original_segment"]=="CUTSCENE_TEXT" and
             scope["full_native_original_OBJECT_payload_and_sites_equal"],
             "entire original 417-byte CODE payload, 35 ordered native fields and correct original segment")
        need(files["exe"]==japanese==b.base.checked(prior["exe"]) and
             len(files["exe"])==67372 and
             parse_mz(files["exe"]).relocations==parse_mz(japanese).relocations and
             len(parse_mz(files["exe"]).relocations)==677 and
             b.normalized_map(files["map"],n)==b.base.checked(prior["map"]) and
             item["complete_original_MZ_and_MAP_equal"],
             "entire original Japanese decoded MAINL EXE and exact native linker section layout")
        results.append(files)
    need(len(results)==2 and results[0]["exe"]==results[1]["exe"] and
         payload(results[0]["obj"])==payload(results[1]["obj"]) and
         literal_fields(results[0]["obj"])==literal_fields(results[1]["obj"]) and
         public_offsets(results[0]["obj"])==public_offsets(results[1]["obj"]) and
         b.stable_map(results[0]["map"],1)==b.stable_map(results[1]["map"],2),
         "two complete source-native TC4/normal-link outputs, only upstream diagnostics normalized")
    return dict(complete=True,original_menu_function_BYTES=417,
        original_code_segment="CUTSCENE_TEXT",
        historical_wrong_segment="CONTINUE_TEXT",
        negative_control_MZ_relocations=696,
        repaired_native_original_MZ_relocations=677,
        natural_C_CPP_compilations=2,
        original_OMF_fixup_sites=35,
        complete_original_function_CODE_equal=True,
        native_67372_byte_original_MAINL_EXE_equal=True,
        historical_source_unchanged=True,
        source_corrected_one_pragma_only=True,
        other_game_objects_reused=35,
        whole_product_source_accepted=False,
        canonical_factory_acceptance=False,
        native_build_report_sha256=report_sha)


if __name__=="__main__":
    result=review()
    (b.ROOT/(b.PREFIX+"review.json")).write_text(json.dumps(result,indent=2)+"\n")
    print("Continue-menu source pragma repaired: 417 original CODE +35 fields; bad section produces 696 MZ, fixed section 677 and original entire MAINL EXE exact.")
