#!/usr/bin/env python3
"""Two source-native 16-bit Turbo C++ MAINL root-controller builds and links.

Recover the entire original 2,458-byte CFG/win/story/stage root producer and
112 initialized DATA bytes from natural C++ without copying any target bytes.
Only this one source OBJ recompiled; reuse the latest after578 highscore,
Staff, Cutscene, CDG, natural sound and source C0/CRT original link inputs.
"""
import fcntl
import json
import os
import subprocess

import build_th03_mainl_hiscore_after578_work as parent
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.pc98 import parse_mz

ROOT=parent.ROOT
WORK=parent.WORK
base=parent.base
DRIVER="scripts/build_th03_mainl_root_controller_after580_work.py"
CONFIG="config/mainl_work/root_controller_after580.json"
PREFIX=".analysis/work/mainl-root-controller-after580-native-"
REPORT=PREFIX+"build.json"
STAGE="af580r"
SCRATCH=WORK/("probe/"+STAGE)

def inputs():
    cfg,h=base.load(CONFIG)
    need(cfg["schema"]=="th03-mainl-root-controller-after580-v1" and
         cfg["parent_report"]==parent.REPORT and
         cfg["source"]=="src/mainl/root/complete_data.cpp" and
         cfg["wrapper"]=="src/mainl/root/producer.cpp" and
         cfg["original_object"]=="obj/th03/rootdata.obj" and
         (cfg["original_CODE_bytes"],cfg["original_initialized_DATA_bytes"],
          cfg["original_BSS_allocation_bytes"],cfg["original_CODE_PUBLICs"],
          cfg["original_DATA_PUBLICs"],cfg["original_BSS_PUBLICs"],
          cfg["original_ordered_FIXUPP_fields"],
          cfg["original_decoded_MAINL_EXE_bytes"],cfg["original_ordered_MZ_relocations"])==
         (2458,112,186,11,3,3,278,67372,677) and
         cfg["historic_raw_OMF_packet_identity_proved"] is False and
         cfg["canonical_factory_credit_changed"] is False and
         cfg["whole_product_source_accepted"] is False,
         "complete bounded 11-function ROOTPRE source and original ABI/DATA/BSS")
    return cfg,h

def sources(cfg):
    code=(ROOT/cfg["source"]).read_bytes()
    wrapper=(ROOT/cfg["wrapper"]).read_bytes()
    need(code and b"\r" not in code and wrapper and b"\r" not in wrapper and
         wrapper.endswith(b'#include "src/mainl/root/complete_data.cpp"\n') and
         wrapper.count(b'#include "src/mainl/root/complete_data.cpp"')==1 and
         b"void near mainl_win_animate" in code and
         b"mainl_story_dispatch" in code and
         b"mainl_stage_intro" in code and
         (WORK/"rootdata.cpp").read_bytes().replace(b"\r\n",b"\n")==code,
         "actual original stage/orchestration and shot sprite maintained C++ TU")
    return code,wrapper

def native_wrapper(n):
    return f'#include "probe/{STAGE}/r{n}/root_body.cpp"\r\n'.encode()

def response(n):
    rsp=parent.response(n)
    for old,new in [
        (rb"probe\af558s\rootdata.obj",f"probe\\{STAGE}\\r{n}\\rootdata.obj".encode()),
        (f"probe\\af578r\\r{n}.exe".encode(),f"probe\\{STAGE}\\r{n}.exe".encode()),
        (f"probe\\af578r\\r{n}.map".encode(),f"probe\\{STAGE}\\r{n}.map".encode())]:
        need(rsp.count(old)==1,"one genuine source-root object or normal link output")
        rsp=rsp.replace(old,new)
    return rsp

def normalize_map(raw,n):
    diagnostic=f"M=probe/{STAGE}/r{n}/rootdata.cpp".encode()
    need(raw.count(diagnostic)==3,"all three original root CODE/DATA/BSS MAP rows")
    return raw.replace(diagnostic,b"M=rootdata.cpp")

def stable_map(raw,n):
    raw=normalize_map(raw,n)
    for old_name,stem in (("af573c","cutscene"),("af575s","staffdat"),("af578r","regdata")):
        value=f"M=probe/{old_name}/r{n}/{stem}.cpp".encode()
        need(raw.count(value)==3,"three recorded upstream C++ source-path rows "+stem)
        raw=raw.replace(value,f"M=source/{stem}.cpp".encode())
    return raw

def scope(raw,original,cfg):
    a=payload(raw);b=payload(original)
    pubs=public_offsets(raw)
    need(a==b and len(a)==2570 and
         len([k for k in a if k[0]==1])==cfg["original_CODE_bytes"] and
         len([k for k in a if k[0]==2])==cfg["original_initialized_DATA_bytes"] and
         literal_fields(raw)==literal_fields(original) and
         len(literal_fields(raw))==cfg["original_ordered_FIXUPP_fields"] and
         pubs==public_offsets(original) and
         sum(x["segment_index"]==1 for x in pubs.values())==cfg["original_CODE_PUBLICs"] and
         sum(x["segment_index"]==2 for x in pubs.values())==cfg["original_DATA_PUBLICs"] and
         sum(x["segment_index"]==3 for x in pubs.values())==cfg["original_BSS_PUBLICs"] and
         segment_definitions(raw)==segment_definitions(original) and
         segment_definitions(raw)[2]["size"]==cfg["original_BSS_allocation_bytes"],
         "all original 2458+112 initializer bytes, 186 BSS and 278 literal ordered OMF fields")
    return dict(CODE_bytes=2458,DATA_bytes=112,BSS_bytes=186,
                original_code_publics=11,original_data_publics=3,original_bss_publics=3,
                original_ordered_fixups=278,
                all_original_initialized_BYTES_and_ABI_equal=True,
                original_vendor_full_OMF_packet_identity=False)

def main():
    cfg,cfg_sha=inputs()
    prior,prior_sha=base.load(parent.REPORT)
    need(prior["complete"] and prior_sha==cfg["parent_report_sha256"],
         "actual original source-bound after578 complete root/cutscene/staff/sound parent")
    code,wrapper=sources(cfg)
    original=(WORK/cfg["original_object"]).read_bytes()
    report=dict(complete=False,cold_rebuilt=False,library_rebuilt=False,
        recompiled_game_objects_per_round=1,other_game_objects_reused=35,
        original_CODE_bytes=2458,original_initialized_DATA_bytes=112,
        original_BSS_allocation_bytes=186,
        canonical_factory_credit_changed=False,whole_product_source_accepted=False,
        source_SHA256=sha(code),wrapper_SHA256=sha(wrapper),
        original_object_SHA256=sha(original),
        parent_report_SHA256=prior_sha,config_SHA256=cfg_sha,
        driver_SHA256=sha((ROOT/DRIVER).read_bytes()),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+"\n")
    env=dict(os.environ,DISPLAY="",WAYLAND_DISPLAY="",WINEDEBUG="-all",
             WINEPREFIX=str(ROOT/".analysis/toolchain/wineprefix"),
             MSDOS_PATH=r"C:\TC4\BIN",TZ="UTC",LANG="C",LC_ALL="C")
    dos=["/usr/bin/wine-stable",str(ROOT/"_reference/ReC98/bin/msdos.exe"),"-e","-x"]
    def run(argv,label):
        p=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=110)
        path=PREFIX+label+".log"
        (ROOT/path).write_bytes(p.stdout)
        report["phases"].append(dict(label=label,argv=argv,returncode=p.returncode,
                log=path,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+": "+p.stdout.decode(errors="replace")[-1200:])

    with (ROOT/".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),"fresh independent original MAINL root C++ stage")
        SCRATCH.mkdir()
        (SCRATCH/"driver.py").write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/"config.json").write_bytes((ROOT/CONFIG).read_bytes())
        whole=[]
        for n in (1,2):
            folder=SCRATCH/f"r{n}"
            folder.mkdir()
            (folder/"root_body.cpp").write_bytes(code.replace(b"\n",b"\r\n"))
            (folder/"rootdata.cpp").write_bytes(native_wrapper(n))
            for name in ("root_body.cpp","rootdata.cpp"):
                os.utime(folder/name,(946684800,946684800))
            run(dos+["tcc","-c","-I.","-O","-b-","-3","-Z","-d","-DGAME=3",
                  "-ml","-DBINARY='L'",f"-nprobe/{STAGE}/r{n}/",
                  f"probe/{STAGE}/r{n}/rootdata.cpp"],f"round{n}-root-TC4-compile")
            obj=(folder/"rootdata.obj").read_bytes()
            bound=scope(obj,original,cfg)
            rsp=response(n)
            (SCRATCH/f"r{n}.lnk").write_bytes(rsp)
            run(dos+["tlink",f"@probe\\{STAGE}\\r{n}.lnk"],
                f"round{n}-normal-TLINK")
            exe=(SCRATCH/f"r{n}.exe").read_bytes()
            mapped=(SCRATCH/f"r{n}.map").read_bytes()
            before=prior["rounds"][n-1]["outputs"]
            need(exe==base.checked(before["exe"]) and
                 normalize_map(mapped,n)==base.checked(before["map"]) and
                 len(exe)==67372 and len(parse_mz(exe).relocations)==677,
                 "complete original decoded MAINL EXE, 677 ordered relocations and original MAP coordinates")
            native=dict(obj=obj,exe=exe,map=mapped)
            outputs={}
            for key,value in native.items():
                path=PREFIX+f"round{n}-{key}.bin"
                (ROOT/path).write_bytes(value)
                outputs[key]=dict(path=path,bytes=len(value),sha256=sha(value))
            report["rounds"].append(dict(round=n,outputs=outputs,scope=bound,
                response_SHA256=sha(rsp),complete_Japanese_MAINL_EXE_equal=True))
            save()
            whole.append(native)
            print("MAINL root C++ round",n,"2458 CODE +112 DATA +186 BSS/11 functions; original full 67372 EXE exact",flush=True)
        need(whole[0]["exe"]==whole[1]["exe"] and
             stable_map(whole[0]["map"],1)==stable_map(whole[1]["map"],2) and
             payload(whole[0]["obj"])==payload(whole[1]["obj"]) and
             literal_fields(whole[0]["obj"])==literal_fields(whole[1]["obj"]) and
             sources(cfg)==(code,wrapper),
             "two independent complete root source/whole EXE native vectors repeat")
    report["complete"]=True
    save()

if __name__=="__main__":
    main()
