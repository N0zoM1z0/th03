#!/usr/bin/env python3
"""Native 16-bit source build of sound-effect mode, music, delay and sound loader producers.

Two rounds recompile only four real Turbo C++ TUs, reusing the previous
natural original MAINL linkage with fixed CUTSCENE_TEXT continue menu.
All code/fixup site and complete original EXE/MAP comparisons are literal.
"""
import fcntl
import json
import os
import subprocess

import build_th03_mainl_sound_control_after586_work as parent
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz
from probe_th03_main_bomb_rikako_cpp import segment_definitions

ROOT=parent.ROOT
WORK=parent.WORK
base=parent.base
DRIVER="scripts/build_th03_mainl_score_input_pi_after587_work.py"
CONFIG="config/mainl_work/score_input_pi_after587.json"
PREFIX=".analysis/work/mainl-score-input-pi-after587-native-"
REPORT=PREFIX+"build.json"
STAGE="af587p"
SCRATCH=WORK/("probe/"+STAGE)
ORDER=("scoredat","inp_wait","pi_load")

def inputs():
    c,digest=base.load(CONFIG)
    expected=[
       ("scoredat","src/mainl/scoredat.cpp","src/mainl/scoredat_producer.cpp","O","obj/th03/scoredat.obj",229,15,3),
       ("inp_wait","src/mainl/hardware/input_wait.cpp","src/mainl/hardware/input_wait_producer.cpp","L","obj/th03/inp_wait.obj",126,11,2),
       ("pi_load","src/shared/formats/pi_load.cpp","src/mainl/formats/pi_load_producer.cpp","O","obj/th03/pi_load.obj",70,6,1)]
    need(c["schema"]=="th03-mainl-score-input-pi-source-after587-v1" and
         c["parent_report"]==parent.REPORT and
         [(u["stem"],u["source"],u["wrapper"],u["binary"],u["original_object"],u["CODE_bytes"],
           u["original_fixups"],u["original_PUBLICs"]) for u in c["units"]]==expected and
         (c["total_CODE_bytes"],c["public_code_functions"],c["original_OMF_fixups"],
          c["whole_original_MAINL_bytes"],c["whole_original_MZ_relocations"])==
             (425,6,32,67372,677) and
         c["full_original_vendor_OMF_packets_identical"] is False and
         c["canonical_factory_credit_changed"] is False and
         c["whole_project_source_accepted"] is False,
         "three complete score, input-wait and PI-load C++ producers")
    previous,old_sha=base.load(parent.REPORT)
    need(previous["complete"] and old_sha==c["parent_report_sha256"],
         "real unchanged original source native parent after586")
    return c,digest,previous

def source_inputs(c):
    kept={}
    for u in c["units"]:
        raw=(ROOT/u["source"]).read_bytes()
        wrap=(ROOT/u["wrapper"]).read_bytes()
        need(raw and b"\r" not in raw and b"\r" not in wrap and
             wrap.count(f'#include "{u["source"]}"'.encode())==1 and
             wrap.endswith(f'#include "{u["source"]}"\n'.encode()) and
             b"codestring" not in wrap.lower() and
             (WORK/u["source"]).read_bytes().replace(b"\r\n",b"\n")==raw,
             "complete original maintained and first-use natural C++ source "+u["stem"])
        kept[u["stem"]]=dict(body=raw,wrapper=wrap)
    return kept

def response(n):
    rsp=parent.response(n)
    for stem in ORDER:
        before=f"obj\\th03\\{stem}.obj".encode()
        after=f"probe\\{STAGE}\\r{n}\\{stem}.obj".encode()
        need(rsp.count(before)==1,"one unchanged original source module slot "+stem)
        rsp=rsp.replace(before,after)
    for before,after in [(f"probe\\{parent.STAGE}\\r{n}.exe",
                          f"probe\\{STAGE}\\r{n}.exe"),
                         (f"probe\\{parent.STAGE}\\r{n}.map",
                          f"probe\\{STAGE}\\r{n}.map")]:
        need(rsp.count(before.encode())==1,"one original native output")
        rsp=rsp.replace(before.encode(),after.encode())
    return rsp

def normalize_map(raw,n):
    for stem in ORDER:
        name=f"M=probe/{STAGE}/r{n}/{stem}.cpp".encode()
        need(raw.count(name)==3,"original CODE/DATA/BSS placement for "+stem)
        raw=raw.replace(name,f"M=th03/{stem}.cpp".encode())
    return raw

def stable_map(raw,n):
    rsp=normalize_map(raw,n)
    return parent.stable_map(rsp,n)

def object_scope(blob,original,u):
    source=payload(blob);target=payload(original)
    pubs=public_offsets(blob)
    need(source==target and len(source)==u["CODE_bytes"] and
         len(literal_fields(blob))==u["original_fixups"] and
         literal_fields(blob)==literal_fields(original) and
         pubs==public_offsets(original) and len(pubs)==u["original_PUBLICs"] and
         segment_definitions(blob)==segment_definitions(original),
         "entire source-native OMF literal initializer, ordered fixups/ABI and segments "+u["stem"])
    return dict(complete_original_CODE_bytes=u["CODE_bytes"],
        original_publics=u["original_PUBLICs"],
        ordered_native_FIXUPP_sites=u["original_fixups"],
        complete_original_CODE_and_ABI_equal=True,
        original_Borland_OMF_metadata_packets_identical=False)

def main():
    cfg,cfg_sha,prev=inputs()
    maintained=source_inputs(cfg)
    originals={u["stem"]:(WORK/u["original_object"]).read_bytes() for u in cfg["units"]}
    japanese=(WORK/"bin/th03/mainl.target.exe").read_bytes()
    need(len(japanese)==67372 and len(parse_mz(japanese).relocations)==677,
         "unchanged original Japanese decoded product")
    row=dict(complete=False,cold_rebuilt=False,library_rebuilt=False,
        project_objects_recompiled_per_round=3,other_project_objects_reused=33,
        complete_score_input_pi_CODE_bytes=425,original_PUBLIC_functions=6,
        original_native_ordered_FIXUPP_sites=32,
        canonical_factory_credit_changed=False,whole_project_source_accepted=False,
        config_sha256=cfg_sha,parent_report_sha256=cfg["parent_report_sha256"],
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        source_sha256={s:{k:sha(v) for k,v in m.items()} for s,m in maintained.items()},
        original_object_sha256={s:sha(v) for s,v in originals.items()},
        original_japanese_decoded_EXE_SHA256=sha(japanese),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(row,indent=2)+"\n")
    env=dict(os.environ,DISPLAY="",WAYLAND_DISPLAY="",WINEDEBUG="-all",
         WINEPREFIX=str(ROOT/".analysis/toolchain/wineprefix"),
         MSDOS_PATH=r"C:\TC4\BIN",TZ="UTC",LANG="C",LC_ALL="C")
    dos=["/usr/bin/wine-stable",str(ROOT/"_reference/ReC98/bin/msdos.exe"),"-e","-x"]
    def run(args,label):
        p=subprocess.run(args,cwd=WORK,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=105)
        log=PREFIX+label+".log"
        (ROOT/log).write_bytes(p.stdout)
        row["phases"].append(dict(label=label,argv=args,returncode=p.returncode,
            log=log,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+": "+p.stdout.decode(errors="replace")[-1300:])
    with (ROOT/".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),"fresh source-native score/PI/input original producer stage")
        SCRATCH.mkdir()
        (SCRATCH/"driver.py").write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/"config.json").write_bytes((ROOT/CONFIG).read_bytes())
        vectors=[]
        for n in (1,2):
            folder=SCRATCH/f"r{n}"
            folder.mkdir()
            objects={}
            scopes={}
            for u in cfg["units"]:
                stem=u["stem"]
                file=folder/f"{stem}.cpp"
                file.write_bytes(maintained[stem]["wrapper"].replace(b"\n",b"\r\n"))
                os.utime(file,(946684800,946684800))
                cmd=dos+["tcc","-c","-I.","-O","-b-","-3","-Z","-d",
                     "-DGAME=3","-ml","-DBINARY='"+u["binary"]+"'",
                     f"-nprobe/{STAGE}/r{n}/",f"probe/{STAGE}/r{n}/{stem}.cpp"]
                run(cmd,f"round{n}-{stem}-TC4-compile")
                obj=(folder/f"{stem}.obj").read_bytes()
                scopes[stem]=object_scope(obj,originals[stem],u)
                objects[stem+"_obj"]=obj
            response_bytes=response(n)
            (SCRATCH/f"r{n}.lnk").write_bytes(response_bytes)
            run(dos+["tlink",f"@probe\\{STAGE}\\r{n}.lnk"],f"round{n}-normal-TLINK")
            exe=(SCRATCH/f"r{n}.exe").read_bytes()
            mapped=(SCRATCH/f"r{n}.map").read_bytes()
            parent_output=prev["rounds"][n-1]["outputs"]
            need(exe==japanese==base.checked(parent_output["exe"]) and
                 normalize_map(mapped,n)==base.checked(parent_output["map"]) and
                 parse_mz(exe).relocations==parse_mz(japanese).relocations,
                 "complete 67372 Japanese MAINL decoded EXE with all 677 literal ordered relocs and MAP")
            v={**objects,"exe":exe,"map":mapped}
            outputs={}
            for key,content in v.items():
                path=PREFIX+f"round{n}-{key}.bin"
                (ROOT/path).write_bytes(content)
                outputs[key]=dict(path=path,bytes=len(content),sha256=sha(content))
            row["rounds"].append(dict(round=n,source_objects=scopes,
                original_link_response_SHA256=sha(response_bytes),
                outputs=outputs,full_japanese_MAINL_EXE_equal=True))
            save()
            vectors.append(v)
            print(f"Score/input/PI round {n}: 425 original CODE / 6 functions / 32 FIXUPPs, full MAINL EXE exact",flush=True)
        need(vectors[0]["exe"]==vectors[1]["exe"] and
             all(payload(vectors[0][s+"_obj"])==payload(vectors[1][s+"_obj"])
                 and literal_fields(vectors[0][s+"_obj"])==literal_fields(vectors[1][s+"_obj"])
                 for s in ORDER) and
             stable_map(vectors[0]["map"],1)==stable_map(vectors[1]["map"],2) and
             source_inputs(cfg)==maintained,
             "complete repeat of two source-native original code/link groups")
    row["complete"]=True
    save()

if __name__=="__main__":
    main()
