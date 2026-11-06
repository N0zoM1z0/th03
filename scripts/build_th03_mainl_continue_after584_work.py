#!/usr/bin/env python3
"""Restore the original near continue menu into CUTSCENE_TEXT, no code rewrite.

The historical maintained alternate had the wrong CONTINUE_TEXT segment.
Compilation proves its 417 code bytes/35 OMF fields were correct but the
wrong section made the linked MZ relocation inventory 696 rather than 677.
Two source-native TC4/TLINK rounds verify the single natural pragma fix
against the already source-backed 35 other original MAINL objects.
"""
import fcntl
import json
import os
import subprocess

import build_th03_mainl_grppsafx_after583_work as parent
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.pc98 import parse_mz

ROOT=parent.ROOT
WORK=parent.WORK
base=parent.base
DRIVER="scripts/build_th03_mainl_continue_after584_work.py"
CONFIG="config/mainl_work/continue_after584.json"
PREFIX=".analysis/work/mainl-continue-after584-native-"
REPORT=PREFIX+"build.json"
STAGE="af584m"
SCRATCH=WORK/("probe/"+STAGE)
NEGATIVE=WORK/"probe/af584cont-try"

def inputs():
    cfg,h=base.load(CONFIG)
    need(cfg["schema"]=="th03-mainl-continue-fixed-segment-after584-v1" and
         cfg["parent_report"]==parent.REPORT and
         cfg["historical_unmodified_source"]=="src/mainl/root/continue.cpp" and
         cfg["corrected_natural_source"]=="src/mainl/root/continue_cutscene_text.cpp" and
         cfg["forward_source"]=="src/mainl/root/continue_producer.cpp" and
         cfg["original_object"]=="obj/th03/contmenu.obj" and
         cfg["original_CODE_segment"]=="CUTSCENE_TEXT" and
         cfg["historical_hypothesis_CODE_segment"]=="CONTINUE_TEXT" and
         (cfg["original_CODE_bytes"],cfg["original_PUBLIC_functions"],
          cfg["original_native_ordered_FIXUPP_fields"],
          cfg["original_MZ_relocations"],cfg["misaligned_segment_MZ_relocations"],
          cfg["original_decoded_MAINL_EXE_bytes"])==(417,1,35,677,696,67372) and
         cfg["canonical_factory_credit_changed"] is False and
         cfg["whole_game_source_accepted"] is False and
         cfg["historical_compiler_OMF_packet_identity_proved"] is False,
         "one natural C++ section pragma correction, no manual CODE patch")
    return cfg,h

def sources(cfg):
    old=(ROOT/cfg["historical_unmodified_source"]).read_bytes()
    new=(ROOT/cfg["corrected_natural_source"]).read_bytes()
    wrapper=(ROOT/cfg["forward_source"]).read_bytes()
    needle=b"#pragma option -zCCONTINUE_TEXT"
    need(old.count(needle)==1 and
         new==old.replace(needle,b"#pragma option -zCCUTSCENE_TEXT") and
         len(old)==len(new)==2111 and
         b"\r" not in old and b"\r" not in new and
         wrapper.endswith(b'#include "src/mainl/root/continue_cutscene_text.cpp"\n') and
         wrapper.count(b'#include "src/mainl/root/continue_cutscene_text.cpp"')==1 and
         (WORK/"contmenu.cpp").read_bytes().replace(b"\r\n",b"\n")==new,
         "independently checked exact one-pragma change from historical source to original frozen CODE segment")
    return old,new,wrapper

def original_scope(raw,original,cfg):
    orig=payload(original);new=payload(raw)
    need(new==orig and len(new)==cfg["original_CODE_bytes"] and
         literal_fields(raw)==literal_fields(original) and
         len(literal_fields(raw))==cfg["original_native_ordered_FIXUPP_fields"] and
         public_offsets(raw)==public_offsets(original) and
         len(public_offsets(raw))==1 and
         segment_definitions(raw)==segment_definitions(original) and
         segment_definitions(raw)[0]["name"]==cfg["original_CODE_segment"],
         "all original 417 complete instructions, 35 ordered OMF fixups, far/near ABI and restored segment")
    return dict(original_initialized_CODE_bytes=417,
                original_FIXUPP_sites=35,original_PUBLICs=1,
                original_segment="CUTSCENE_TEXT",
                full_native_original_OBJECT_payload_and_sites_equal=True)

def wrong_segment_control(cfg,original):
    before=(NEGATIVE/"old/contmenu.obj").read_bytes()
    fixed=(NEGATIVE/"fixed/contmenu.obj").read_bytes()
    target=(WORK/"bin/th03/mainl.target.exe").read_bytes()
    bad=(NEGATIVE/"old/r1.exe").read_bytes()
    good=(NEGATIVE/"fixed/r1.exe").read_bytes()
    original_code=payload(original)
    need(payload(before)==original_code==payload(fixed) and
         literal_fields(before)==literal_fields(original)==literal_fields(fixed) and
         public_offsets(before)==public_offsets(original)==public_offsets(fixed) and
         segment_definitions(before)[0]["name"]==cfg["historical_hypothesis_CODE_segment"] and
         segment_definitions(fixed)==segment_definitions(original) and
         bad!=target and good==target and
         len(parse_mz(bad).relocations)==cfg["misaligned_segment_MZ_relocations"] and
         len(parse_mz(good).relocations)==cfg["original_MZ_relocations"],
         "real negative old-pragma native object has exact CODE but wrong segment/link image")
    return dict(original_untouched_historical_source_segment="CONTINUE_TEXT",
        corrected_natural_Turbo_CPP_segment="CUTSCENE_TEXT",
        both_assembled_CODE_and_FIXUPPs_identical=True,
        bad_normal_LINK_relocations=696,original_NORMAL_LINK_relocations=677,
        bad_EXE_not_equal=True,good_EXE_byte_equal=True,
        original_negative_object_SHA256=sha(before),
        negative_EXE_SHA256=sha(bad))

def staged_wrapper(n):
    return f'#include "probe/{STAGE}/r{n}/continue_body.cpp"\r\n'.encode()

def response(n):
    rsp=parent.response(n)
    for before,after in [
        (rb"obj\th03\contmenu.obj",f"probe\\{STAGE}\\r{n}\\contmenu.obj".encode()),
        (f"probe\\{parent.STAGE}\\r{n}.exe".encode(),f"probe\\{STAGE}\\r{n}.exe".encode()),
        (f"probe\\{parent.STAGE}\\r{n}.map".encode(),f"probe\\{STAGE}\\r{n}.map".encode())]:
        need(rsp.count(before)==1,"single original GAME3 BINARY L continue object/output")
        rsp=rsp.replace(before,after)
    return rsp

def normalized_map(raw,n):
    name=f"M=probe/{STAGE}/r{n}/contmenu.cpp".encode()
    need(raw.count(name)==3,"all original CUTSCENE_TEXT/DATA/BSS contribution rows")
    return raw.replace(name,b"M=contmenu.cpp")

def stable_map(raw,n):
    raw=normalized_map(raw,n)
    for stage,stem in [
        ("af573c","cutscene"),("af575s","staffdat"),("af578r","regdata"),
        ("af580r","rootdata"),("af582l","cdg_load"),("af583g","grppsafx")]:
        old=f"M=probe/{stage}/r{n}/{stem}.cpp".encode()
        need(raw.count(old)==3,"only previous source diagnostic path changes "+stem)
        raw=raw.replace(old,f"M=source/{stem}.cpp".encode())
    return raw

def main():
    cfg,cfg_sha=inputs()
    prev,prev_sha=base.load(parent.REPORT)
    need(prev["complete"] and prev_sha==cfg["parent_report_sha256"],
         "actual real after583 36-project-object and source-backed CRT parent")
    old,code,wrapper=sources(cfg)
    original=(WORK/cfg["original_object"]).read_bytes()
    negative=wrong_segment_control(cfg,original)
    reference=(WORK/"bin/th03/mainl.target.exe").read_bytes()
    report=dict(complete=False,cold_rebuilt=False,library_rebuilt=False,
        compiled_project_objects_per_round=1,other_project_objects_reused=35,
        natural_CPP_CODE_bytes=417,original_public_function_count=1,
        original_native_fixups=35,
        historic_wrong_pragma_unchanged=True,
        canonical_factory_credit_changed=False,whole_product_source_accepted=False,
        original_wrong_source_sha256=sha(old),corrected_source_sha256=sha(code),
        wrapper_sha256=sha(wrapper),original_object_sha256=sha(original),
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        config_sha256=cfg_sha,parent_report_sha256=prev_sha,
        real_negative_segment_control=negative,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+"\n")
    env=dict(os.environ,DISPLAY="",WAYLAND_DISPLAY="",WINEDEBUG="-all",
             WINEPREFIX=str(ROOT/".analysis/toolchain/wineprefix"),
             MSDOS_PATH=r"C:\TC4\BIN",TZ="UTC",LANG="C",LC_ALL="C")
    dos=["/usr/bin/wine-stable",str(ROOT/"_reference/ReC98/bin/msdos.exe"),"-e","-x"]
    def run(argv,label):
        p=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=105)
        path=PREFIX+label+".log"
        (ROOT/path).write_bytes(p.stdout)
        report["phases"].append(dict(label=label,argv=argv,returncode=p.returncode,
                log=path,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+": "+p.stdout.decode(errors="replace")[-1200:])
    with (ROOT/".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),"new real original menu section-native stage")
        SCRATCH.mkdir()
        (SCRATCH/"driver.py").write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/"config.json").write_bytes((ROOT/CONFIG).read_bytes())
        vectors=[]
        for n in (1,2):
            folder=SCRATCH/f"r{n}"
            folder.mkdir()
            (folder/"continue_body.cpp").write_bytes(code.replace(b"\n",b"\r\n"))
            (folder/"contmenu.cpp").write_bytes(staged_wrapper(n))
            for file in ("continue_body.cpp","contmenu.cpp"):
                os.utime(folder/file,(946684800,946684800))
            run(dos+["tcc","-c","-I.","-O","-b-","-3","-Z","-d",
                "-DGAME=3","-ml","-DBINARY='L'",f"-nprobe/{STAGE}/r{n}/",
                f"probe/{STAGE}/r{n}/contmenu.cpp"],
                f"round{n}-original-segment-TC4")
            obj=(folder/"contmenu.obj").read_bytes()
            scope=original_scope(obj,original,cfg)
            rsp=response(n)
            (SCRATCH/f"r{n}.lnk").write_bytes(rsp)
            run(dos+["tlink",f"@probe\\{STAGE}\\r{n}.lnk"],
                f"round{n}-normal-TLINK")
            exe=(SCRATCH/f"r{n}.exe").read_bytes()
            mapped=(SCRATCH/f"r{n}.map").read_bytes()
            older=prev["rounds"][n-1]["outputs"]
            need(exe==reference==base.checked(older["exe"]) and
                 len(exe)==67372 and
                 parse_mz(exe).relocations==parse_mz(reference).relocations and
                 len(parse_mz(exe).relocations)==677 and
                 normalized_map(mapped,n)==base.checked(older["map"]),
                 "original entire decoded Japanese MAINL EXE and MZ relocations, normal MAP coordinates")
            native=dict(obj=obj,exe=exe,map=mapped)
            outputs={}
            for key,data in native.items():
                file=PREFIX+f"round{n}-{key}.bin"
                (ROOT/file).write_bytes(data)
                outputs[key]=dict(path=file,bytes=len(data),sha256=sha(data))
            report["rounds"].append(dict(round=n,outputs=outputs,scope=scope,
                original_link_response_sha256=sha(rsp),
                complete_original_MZ_and_MAP_equal=True))
            save()
            vectors.append(native)
            print("Continue original-section C++ round",n,
                  "417 CODE/35 original OMF fields, full 67372 EXE/677 MZ relocations exact",flush=True)
        need(vectors[0]["exe"]==vectors[1]["exe"] and
             payload(vectors[0]["obj"])==payload(vectors[1]["obj"]) and
             literal_fields(vectors[0]["obj"])==literal_fields(vectors[1]["obj"]) and
             stable_map(vectors[0]["map"],1)==stable_map(vectors[1]["map"],2) and
             sources(cfg)==(old,code,wrapper),
             "two complete native source/compiled object/normal-link vectors repeat")
    report["complete"]=True
    save()

if __name__=="__main__":
    main()
