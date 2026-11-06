#!/usr/bin/env python3
"""Two natural C++4.02 staff/endings native builds replacing only staffdat.obj.

Preserves original unmodified maintained source with a new small wrapper.
Uses the exact after573 native root including source cutscene, TASM sounds,
keyboard, registration DATA, math and original CRT; never full cold replay.
"""
import fcntl
import json
import os
from pathlib import Path
import subprocess

import build_th03_mainl_cutscene_after573_work as parent
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.pc98 import parse_mz

ROOT=parent.ROOT
WORK=parent.WORK
base=parent.base
DRIVER="scripts/build_th03_mainl_staff_after575_work.py"
CONFIG="config/mainl_work/staff_after575.json"
PREFIX=".analysis/work/mainl-staff-after575-native-"
REPORT=PREFIX+"build.json"
STAGE="af575s"
SCRATCH=WORK/("probe/"+STAGE)

def inputs():
    cfg,digest=base.load(CONFIG)
    need(cfg["schema"]=="th03-mainl-staff-native-after575-v1" and
         cfg["parent_report"]==parent.REPORT and
         cfg["maintained_source"]=="src/mainl/staff/data.cpp" and
         cfg["source_wrapper"]=="src/mainl/staff/producer.cpp" and
         cfg["original_object"]=="obj/th03/staffdat.obj" and
         (cfg["original_CODE_bytes"],cfg["original_initialized_DATA_bytes"],
          cfg["original_PUBLIC_CODE_functions"],cfg["original_PUBLIC_DATA_names"],
          cfg["ordered_OMF_fixups"],cfg["original_decoded_MAINL_EXE_bytes"],
          cfg["original_ordered_MZ_relocations"])==(3695,224,19,6,342,67372,677) and
         cfg["complete_original_OMF_packet_identity_claimed"] is False and
         cfg["canonical_factory_credit_changed"] is False and
         cfg["whole_game_source_accepted"] is False,
         "complete 19-function/6 DATA symbol staff natural C++ scope")
    return cfg,digest

def sources(cfg):
    main=(ROOT/cfg["maintained_source"]).read_bytes()
    wrapper=(ROOT/cfg["source_wrapper"]).read_bytes()
    need(main and b"\r" not in main and
         b"mainl_staff_roll" in main and b"mainl_ending" in main and
         b"mainl_snow_update" in main and
         b"mainl_staff_verdict" in main and
         wrapper.count(b'#include "src/mainl/staff/data.cpp"')==1 and
         wrapper.endswith(b'#include "src/mainl/staff/data.cpp"\n') and
         b"codestring" not in wrapper.lower(),
         "actual complete endgame, snow, verdict and staff C++ source")
    return main,wrapper

def staged_wrapper(number):
    return f'#include "probe/{STAGE}/r{number}/staff_body.cpp"\r\n'.encode()

def response(number):
    rsp=parent.response(number)
    for before,after in [
        (rb"obj\th03\staffdat.obj",f"probe\\{STAGE}\\r{number}\\staffdat.obj".encode()),
        (f"probe\\af573c\\r{number}.exe".encode(),f"probe\\{STAGE}\\r{number}.exe".encode()),
        (f"probe\\af573c\\r{number}.map".encode(),f"probe\\{STAGE}\\r{number}.map".encode())]:
        need(rsp.count(before)==1,"one unchanged original staff compiler object/normal output")
        rsp=rsp.replace(before,after)
    return rsp

def map_normalized(raw,number):
    value=f"M=probe/{STAGE}/r{number}/staffdat.cpp".encode()
    need(raw.count(value)==3,"original STAFFP CODE/DATA/BSS native contributions")
    return raw.replace(value,b"M=staffdat.cpp")

def obj_scope(obj,original,cfg):
    x=payload(obj);y=payload(original)
    pubs=public_offsets(obj);before=public_offsets(original)
    need(x==y and
         sum(s==1 for s,i in x)==cfg["original_CODE_bytes"] and
         sum(s==2 for s,i in x)==cfg["original_initialized_DATA_bytes"] and
         literal_fields(obj)==literal_fields(original) and
         len(literal_fields(obj))==cfg["ordered_OMF_fixups"] and
         pubs==before and
         sum(row["segment_index"]==1 for row in pubs.values())==cfg["original_PUBLIC_CODE_functions"] and
         sum(row["segment_index"]==2 for row in pubs.values())==cfg["original_PUBLIC_DATA_names"] and
         segment_definitions(obj)==segment_definitions(original),
         "all original code and mutable sprite/credits DATA, ordered OMF native fixups and ABI")
    return dict(initialized_CODE_bytes=cfg["original_CODE_bytes"],
                initialized_DATA_bytes=cfg["original_initialized_DATA_bytes"],
                original_CODE_PUBLIC_functions=cfg["original_PUBLIC_CODE_functions"],
                original_DATA_PUBLIC_names=cfg["original_PUBLIC_DATA_names"],
                native_ordered_fixups=cfg["ordered_OMF_fixups"],
                original_module_COMENT_LNAMES_packet_identity=False)

def main():
    cfg,cfg_sha=inputs()
    p,p_sha=base.load(parent.REPORT)
    need(p["complete"] and p_sha==cfg["parent_report_sha256"],
         "actual complete after573 source-backed native cutscene/sound parent")
    main_src,wrapper=sources(cfg)
    original=(WORK/cfg["original_object"]).read_bytes()
    report=dict(complete=False,cold_rebuilt=False,library_rebuilt=False,
        game_objects_recompiled_per_round=1,other_project_objects_reused=35,
        canonical_factory_acceptance=False,whole_game_source_accepted=False,
        original_CODE_bytes=3695,original_initialized_DATA_bytes=224,
        original_PUBLIC_functions=19,original_PUBLIC_DATA_names=6,
        parent_report_sha256=p_sha,config_sha256=cfg_sha,
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        maintained_source_sha256=sha(main_src),source_wrapper_sha256=sha(wrapper),
        original_object_sha256=sha(original),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+"\n")
    env=dict(os.environ,DISPLAY="",WAYLAND_DISPLAY="",WINEDEBUG="-all",
        WINEPREFIX=str(ROOT/".analysis/toolchain/wineprefix"),
        MSDOS_PATH=r"C:\TC4\BIN",TZ="UTC",LANG="C",LC_ALL="C")
    dos=["/usr/bin/wine-stable",str(ROOT/"_reference/ReC98/bin/msdos.exe"),"-e","-x"]
    def run(command,label):
        process=subprocess.run(command,cwd=WORK,env=env,stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,timeout=115)
        log=PREFIX+label+".log"
        (ROOT/log).write_bytes(process.stdout)
        report["phases"].append(dict(label=label,argv=command,returncode=process.returncode,
                 log=log,log_sha256=sha(process.stdout)))
        save()
        need(process.returncode==0,label+": "+process.stdout.decode(errors="replace")[-1450:])
    with (ROOT/".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),"fresh source-backed staff C++ native stage")
        SCRATCH.mkdir()
        (SCRATCH/"driver.py").write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/"config.json").write_bytes((ROOT/CONFIG).read_bytes())
        vectors=[]
        for n in (1,2):
            folder=SCRATCH/f"r{n}"
            folder.mkdir()
            (folder/"staff_body.cpp").write_bytes(main_src.replace(b"\n",b"\r\n"))
            (folder/"staffdat.cpp").write_bytes(staged_wrapper(n))
            for name in ("staff_body.cpp","staffdat.cpp"):
                os.utime(folder/name,(946684800,946684800))
            run(dos+["tcc","-c","-I.","-O","-b-","-3","-Z","-d","-DGAME=3",
                     "-ml","-DBINARY='L'",f"-nprobe/{STAGE}/r{n}/",
                     f"probe/{STAGE}/r{n}/staffdat.cpp"],f"round{n}-staff-TC4-compile")
            obj=(folder/"staffdat.obj").read_bytes()
            scope=obj_scope(obj,original,cfg)
            rsp=response(n)
            (SCRATCH/f"r{n}.lnk").write_bytes(rsp)
            run(dos+["tlink",f"@probe\\{STAGE}\\r{n}.lnk"],f"round{n}-normal-TLINK")
            exe=(SCRATCH/f"r{n}.exe").read_bytes()
            mapped=(SCRATCH/f"r{n}.map").read_bytes()
            prev=p["rounds"][n-1]["outputs"]
            need(exe==base.checked(prev["exe"]) and
                 map_normalized(mapped,n)==base.checked(prev["map"]) and
                 len(exe)==67372 and len(parse_mz(exe).relocations)==677,
                 "entire exact original MAINL EXE, all 677 literal MZ relocations and every MAP position")
            native=dict(obj=obj,exe=exe,map=mapped)
            outputs={}
            for name,raw in native.items():
                path=PREFIX+f"round{n}-{name}.bin"
                (ROOT/path).write_bytes(raw)
                outputs[name]=dict(path=path,bytes=len(raw),sha256=sha(raw))
            report["rounds"].append(dict(round=n,outputs=outputs,scope=scope,
                    native_response_sha256=sha(rsp),
                    entire_original_japanese_decoded_EXE_equal=True,
                    complete_MAP_addresses_equal=True))
            save()
            vectors.append(native)
            print("Staff original C++ round",n,"3695 CODE/224 DATA/19 code functions/342 OMF fields; full 67372-byte EXE exact",flush=True)
        # The upstream cutscene C++ is independently source-compiled in
        # r1/r2; only that earlier diagnostic module path is round-specific.
        def stable_map(blob,n):
            label=f"M=probe/af573c/r{n}/cutscene.cpp".encode()
            need(blob.count(label)==3,"all upstream cutscene CODE/DATA/BSS diagnostic rows")
            return map_normalized(blob,n).replace(label,b"M=source/cutscene.cpp")
        need(vectors[0]["exe"]==vectors[1]["exe"] and
             stable_map(vectors[0]["map"],1)==stable_map(vectors[1]["map"],2) and
             payload(vectors[0]["obj"])==payload(vectors[1]["obj"]) and
             sources(cfg)==(main_src,wrapper),
             "both complete native STAFF/EXE/MAP source vectors repeat")
    report["complete"]=True
    save()

if __name__=="__main__":
    main()
