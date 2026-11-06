#!/usr/bin/env python3
"""Read-only verification of native source CDG PICTURE blitters and alignment."""
import json

import build_th03_mainl_cdg_after577_work as b
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz


def review():
    cfg,cfg_sha=b.inputs()
    report,report_sha=b.base.load(b.REPORT)
    prev,prev_sha=b.base.load(b.parent.REPORT)
    source=b.sources(cfg)
    original={u["stem"]:(b.WORK/f'obj/th03/{u["stem"]}.obj').read_bytes()
              for u in cfg["units"]}
    reference_target=(b.WORK/"bin/th03/mainl.target.exe").read_bytes()
    need(prev["complete"] and prev_sha==cfg["parent_report_sha256"] and
         report["complete"] and report["cold_rebuilt"] is False and
         report["library_rebuilt"] is False and
         report["compiled_project_objects_per_round"]==2 and
         report["other_project_objects_reused"]==34 and
         (report["complete_source_CODE_bytes"],report["original_PUBLIC_code_functions"],
          report["natural_assembler_EVEN_bytes"],report["original_OMF_FIXUPP_fields"])==
          (496,3,3,19) and
         report["canonical_factory_credit_changed"] is False and
         report["whole_product_source_accepted"] is False and
         report["driver_sha256"]==sha((b.ROOT/b.DRIVER).read_bytes()) and
         report["config_sha256"]==cfg_sha and
         report["parent_report_sha256"]==prev_sha and
         report["sources_sha256"]==
           {name:{k:sha(raw) for k,raw in val.items()} for name,val in source.items()} and
         report["original_OMF_sha256"]==
           {name:sha(raw) for name,raw in original.items()},
         "all existing source/CDG TASM/parent and original OMF evidence locked")
    need((b.SCRATCH/"driver.py").read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/"config.json").read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         "actual assembler driver/config kept")
    for stem,val in source.items():
        need((b.SCRATCH/f"{stem}.asm").read_bytes()==val["wrapper"].replace(b"\n",b"\r\n"),
             "complete source-native forwarded TASM source "+stem)
    labels=[label for n in (1,2) for label in
        ([f"round{n}-{name}-TASM-assemble" for name in ("cdg_put","cdg_p_na")] +
         [f"round{n}-normal-TLINK"])]
    need(len(report["phases"])==6 and
         [x["label"] for x in report["phases"]]==labels and
         all(x["returncode"]==0 and sha((b.ROOT/x["log"]).read_bytes())==x["log_sha256"]
             for x in report["phases"]), "all six actual original TASM/TLINK writer logs retained")
    vectors=[]
    for n,row in enumerate(report["rounds"],1):
        old=prev["rounds"][n-1]
        need(row["round"]==n and row["normal_response_sha256"]==sha(b.response(n)) and
             (b.SCRATCH/f"r{n}.lnk").read_bytes()==b.response(n) and
             row["entire_original_MAINL_EXE_equal"],
             "only two original source CODE objects replaced in genuine native link")
        native={name:b.base.checked(pin) for name,pin in row["outputs"].items()}
        need(set(native)=={"cdg_put_obj","cdg_p_na_obj","exe","map"},
             "all four original source-native OMF/EXE/MAP outputs SHA-pinned")
        for u in cfg["units"]:
            stem=u["stem"]
            blob=native[stem+"_obj"]
            scope=b.original_object_scope(blob,original[stem],u)
            need(row["scope"][stem]==scope and
                 (b.SCRATCH/f"{stem}.obj").read_bytes()==blob and
                 scope["native_CODE_bytes"]==u["original_CODE_bytes"] and
                 scope["natural_TASM_EVEN_sites"]==u["even_at"] and
                 scope["total_original_fixups"]==u["original_FIXUPP_fields"] and
                 scope["original_PUBLICs"]==u["original_PUBLICs"] and
                 scope["complete_original_CODE_and_native_fields_equal"] and
                 payload(blob)==payload(original[stem]) and
                 literal_fields(blob)==literal_fields(original[stem]) and
                 public_offsets(blob)==public_offsets(original[stem]),
                 "all native original 386 blitter instruction/EVEN, literal fixup order and PUBLICs "+stem)
        need(native["exe"]==reference_target==
             b.base.checked(old["outputs"]["exe"]) and
             len(native["exe"])==67372 and
             parse_mz(native["exe"]).relocations==
               parse_mz(reference_target).relocations and
             len(parse_mz(native["exe"]).relocations)==677 and
             b.map_normalized(native["map"])==b.base.checked(old["outputs"]["map"]),
             "all original Japanese decoded MAINL EXE bytes/ordered MZ fields and MAP geometry")
        vectors.append(native)
    def stable_map(raw,n):
        txt=b.map_normalized(raw)
        for name,stem in (("af573c","cutscene"),("af575s","staffdat")):
            p=f"M=probe/{name}/r{n}/{stem}.cpp".encode()
            need(txt.count(p)==3,"real independent previous CODE/DATA/BSS diagnostic path "+stem)
            txt=txt.replace(p,f"M=source/{stem}.cpp".encode())
        return txt
    need(len(vectors)==2 and
         vectors[0]["exe"]==vectors[1]["exe"] and
         vectors[0]["cdg_put_obj"]==vectors[1]["cdg_put_obj"] and
         vectors[0]["cdg_p_na_obj"]==vectors[1]["cdg_p_na_obj"] and
         stable_map(vectors[0]["map"],1)==stable_map(vectors[1]["map"],2),
         "two independent original TASM object/EXE/MAP vectors and bounded name normalization")
    return dict(complete=True,native_assembler_rounds=2,original_CDG_functions=3,
        original_CDG_CODE_bytes=496,original_ordered_native_FIXUPP=19,
        original_EVEN_bytes=[179,381,113],
        full_source_native_Omf_OMF_initialized_CODE_equal=True,
        original_CDG_public_names_positions_equal=True,
        original_vendor_OMF_packet_identity=False,
        original_entire_67372_byte_MAINL_EXE_equal=True,
        original_ordered_MZ_relocations=677,
        whole_product_source_accepted=False,canonical_factory_acceptance=False,
        native_source_report_sha256=report_sha)

if __name__=="__main__":
    result=review()
    (b.ROOT/(b.PREFIX+"review.json")).write_text(json.dumps(result,indent=2)+"\n")
    print("Native CDG 3 complete 386 blitters /496 original CODE /19 ordered OMF fields; both whole 67372 MAINL EXEs exact.")
