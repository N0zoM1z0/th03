#!/usr/bin/env python3
"""Two source-native Turbo C++ high-score editor/score loader MAINL links.

Source is genuine maintained nested regdata.cpp -> regist.cpp, no copied
machine-code text, and no rewritten frozen historic original source.
Only one project object is recompiled per round. Preserves the native
after577 sound, 386 CDG, Staff, Cutscene, input, root and C0/CRT chain.
"""
import fcntl
import json
import os
import subprocess

import build_th03_mainl_cdg_after577_work as parent
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.pc98 import parse_mz

ROOT=parent.ROOT
WORK=parent.WORK
base=parent.base
DRIVER="scripts/build_th03_mainl_hiscore_after578_work.py"
CONFIG="config/mainl_work/hiscore_after578.json"
PREFIX=".analysis/work/mainl-hiscore-after578-native-"
REPORT=PREFIX+"build.json"
STAGE="af578r"
SCRATCH=WORK/("probe/"+STAGE)

def inputs():
    cfg,cfg_sha=base.load(CONFIG)
    need(cfg["schema"]=="th03-mainl-hiscore-after578-v1" and
         cfg["parent_report"]==parent.REPORT and
         cfg["source_wrapper"]=="src/mainl/hiscore/producer.cpp" and
         cfg["nested_source"]=="src/mainl/hiscore/regdata.cpp" and
         cfg["registration_natural_CPP"]=="src/mainl/regist.cpp" and
         cfg["original_object"]=="obj/th03/regdata.obj" and
         (cfg["original_CODE_bytes"],cfg["original_initialized_DATA_bytes"],
          cfg["original_CODE_PUBLICs"],cfg["original_DATA_PUBLICs"],
          cfg["original_ordered_FIXUPP"],cfg["original_decoded_MAINL_EXE_bytes"],
          cfg["original_MZ_relocations"])==(2788,40,15,1,188,67372,677) and
         cfg["historical_complete_raw_OMF_packets_proved"] is False and
         cfg["canonical_factory_credit_changed"] is False and
         cfg["whole_product_source_accepted"] is False,
         "complete source-backed high-score/registration/PI/sound producer")
    return cfg,cfg_sha

def sources(cfg):
    results={k:(ROOT/cfg[k]).read_bytes() for k in
             ("source_wrapper","nested_source","registration_natural_CPP")}
    wrapper,nested,natural=(results[k] for k in
             ("source_wrapper","nested_source","registration_natural_CPP"))
    need(wrapper.endswith(b'#include "src/mainl/hiscore/regdata.cpp"\n') and
         wrapper.count(b'#include "src/mainl/hiscore/regdata.cpp"')==1 and
         nested.count(b'#include "src/mainl/regist.cpp"')==1 and
         b'#pragma option -zCREGIST_TEXT' in nested and
         b'void near mainl_reg_music(void)' in nested and
         b'void near regist_load_and_put_initial_both(void)' in natural and
         b'void near regist_name_enter_menu(void)' in natural and
         all(b'\r' not in x for x in results.values()) and
         (WORK/"regdata.cpp").read_bytes().replace(b'\r\n',b'\n')==nested and
         (WORK/"src/mainl/regist.cpp").read_bytes().replace(b'\r\n',b'\n')==natural,
         "real maintained original nested C++ registration/score menu producer")
    return results

def native_wrapper(n):
    return f'#include "probe/{STAGE}/r{n}/regdata_body.cpp"\r\n'.encode()

def response(n):
    raw=parent.response(n)
    for before,after in [
        (rb'obj\th03\regdata.obj',f'probe\\{STAGE}\\r{n}\\regdata.obj'.encode()),
        (f'probe\\af577c\\r{n}.exe'.encode(),f'probe\\{STAGE}\\r{n}.exe'.encode()),
        (f'probe\\af577c\\r{n}.map'.encode(),f'probe\\{STAGE}\\r{n}.map'.encode())]:
        need(raw.count(before)==1,"unique genuine high-score producer slot in normal source link")
        raw=raw.replace(before,after)
    return raw

def map_normalized(blob,n):
    name=f'M=probe/{STAGE}/r{n}/regdata.cpp'.encode()
    need(blob.count(name)==3,"whole original high-score CODE/DATA/BSS contribution rows")
    return blob.replace(name,b'M=regdata.cpp')

def object_scope(raw,original,cfg):
    x,y=payload(raw),payload(original)
    pubs=public_offsets(raw)
    need(x==y and
         sum(seg==1 for seg,off in x)==cfg["original_CODE_bytes"] and
         sum(seg==2 for seg,off in x)==cfg["original_initialized_DATA_bytes"] and
         len(literal_fields(raw))==cfg["original_ordered_FIXUPP"] and
         literal_fields(raw)==literal_fields(original) and
         pubs==public_offsets(original) and
         sum(row["segment_index"]==1 for row in pubs.values())==cfg["original_CODE_PUBLICs"] and
         sum(row["segment_index"]==2 for row in pubs.values())==cfg["original_DATA_PUBLICs"] and
         segment_definitions(raw)==segment_definitions(original),
         "all 2788+40 original bytes, all 188 ordered fields and 16 original near ABI entries")
    return dict(original_CODE_bytes=2788,initialized_DATA_bytes=40,
                original_CODE_FUNCTIONS=15,original_DATA_PUBLICs=1,
                ordered_native_FIXUPP_count=188,
                full_original_CODE_and_DATA_equal=True,
                original_historical_OMF_COMENT_packet_identity=False)

def main():
    cfg,cfg_sha=inputs()
    old,parent_sha=base.load(parent.REPORT)
    need(old["complete"] and parent_sha==cfg["parent_report_sha256"],
         "real original source-native Staff/CDG/sound/cutscene/registration parent")
    current=sources(cfg)
    original=(WORK/cfg["original_object"]).read_bytes()
    report=dict(complete=False,cold_rebuilt=False,library_rebuilt=False,
         recompiled_project_objects_per_round=1,other_project_objects_reused=35,
         source_CODE_bytes=2788,source_DATA_bytes=40,source_CODE_functions=15,
         canonical_factory_credit_changed=False,whole_product_source_accepted=False,
         driver_sha256=sha((ROOT/DRIVER).read_bytes()),config_sha256=cfg_sha,
         parent_report_sha256=parent_sha,
         maintained_sources_sha256={k:sha(v) for k,v in current.items()},
         original_object_sha256=sha(original),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+"\n")
    env=dict(os.environ,DISPLAY="",WAYLAND_DISPLAY="",WINEDEBUG="-all",
             WINEPREFIX=str(ROOT/".analysis/toolchain/wineprefix"),
             MSDOS_PATH=r"C:\TC4\BIN",TZ="UTC",LANG="C",LC_ALL="C")
    dos=["/usr/bin/wine-stable",str(ROOT/"_reference/ReC98/bin/msdos.exe"),"-e","-x"]

    def run(argv,label):
        done=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,timeout=105)
        log=PREFIX+label+".log"
        (ROOT/log).write_bytes(done.stdout)
        report["phases"].append(dict(label=label,argv=argv,log=log,
                   log_sha256=sha(done.stdout),returncode=done.returncode))
        save()
        need(done.returncode==0,label+": "+done.stdout.decode(errors="replace")[-1600:])

    with (ROOT/".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),"fresh independent original high-score C++ producer stage")
        SCRATCH.mkdir()
        (SCRATCH/"driver.py").write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/"config.json").write_bytes((ROOT/CONFIG).read_bytes())
        pair=[]
        for n in (1,2):
            folder=SCRATCH/f"r{n}"
            folder.mkdir()
            (folder/"regdata_body.cpp").write_bytes(
                  current["nested_source"].replace(b"\n",b"\r\n"))
            (folder/"regdata.cpp").write_bytes(native_wrapper(n))
            for name in ("regdata_body.cpp","regdata.cpp"):
                os.utime(folder/name,(946684800,946684800))
            run(dos+["tcc","-c","-I.","-O","-b-","-3","-Z","-d","-DGAME=3",
                "-ml","-DBINARY='L'",f"-nprobe/{STAGE}/r{n}/",
                f"probe/{STAGE}/r{n}/regdata.cpp"],
                f"round{n}-highscore-TC4-compile")
            obj=(folder/"regdata.obj").read_bytes()
            scope=object_scope(obj,original,cfg)
            rsp=response(n)
            (SCRATCH/f"r{n}.lnk").write_bytes(rsp)
            run(dos+["tlink",f"@probe\\{STAGE}\\r{n}.lnk"],
                f"round{n}-normal-TLINK")
            exe=(SCRATCH/f"r{n}.exe").read_bytes()
            mapped=(SCRATCH/f"r{n}.map").read_bytes()
            ref=old["rounds"][n-1]["outputs"]
            need(exe==base.checked(ref["exe"]) and
                 map_normalized(mapped,n)==base.checked(ref["map"]) and
                 len(exe)==67372 and len(parse_mz(exe).relocations)==677,
                 "whole source-native original Japanese MAINL EXE and all 677 relocations/MAP")
            raw=dict(obj=obj,exe=exe,map=mapped)
            outputs={}
            for key,body in raw.items():
                file=PREFIX+f"round{n}-{key}.bin"
                (ROOT/file).write_bytes(body)
                outputs[key]=dict(path=file,bytes=len(body),sha256=sha(body))
            report["rounds"].append(dict(round=n,outputs=outputs,scope=scope,
                original_link_response_sha256=sha(rsp),
                complete_original_japanese_EXE_equal=True,
                MAP_coordinates_identical=True))
            save()
            pair.append(raw)
            print("Score menu native round",n,"2788 CODE/40 DATA, 15 functions/188 original OMF sites; whole 67372-byte EXE exact",flush=True)
        def stable_map(raw,n):
            norm=map_normalized(raw,n)
            for stage,stem in (("af573c","cutscene"),("af575s","staffdat")):
                before=f"M=probe/{stage}/r{n}/{stem}.cpp".encode()
                need(norm.count(before)==3,"only upstream source-native round diagnostic path")
                norm=norm.replace(before,f"M=source/{stem}.cpp".encode())
            return norm
        need(pair[0]["exe"]==pair[1]["exe"] and
             stable_map(pair[0]["map"],1)==stable_map(pair[1]["map"],2) and
             payload(pair[0]["obj"])==payload(pair[1]["obj"]) and
             literal_fields(pair[0]["obj"])==literal_fields(pair[1]["obj"]) and
             sources(cfg)==current,
             "both entire source-C++ object/EXE/MAP vectors repeat")
    report["complete"]=True
    save()

if __name__=="__main__":
    main()
