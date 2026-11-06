#!/usr/bin/env python3
"""Recompile the four maintained MAINL sound C/C++ producers with original TC4.

This is a source-bound native proof. The historic sources have one explicit
codestring tail each, kept contextual and uncredited. Do not conflate exact
whole EXE with proof of naturally compiler-produced source trailing bytes.
"""
import fcntl
import json
import os
import subprocess

import build_th03_mainl_vector_work as parent
from build_th03_mainl_resources_work import need, sha
from build_th03_mainl_display_work import payload, literal_fields
from lib.mainl_owner_migrations import public_offsets

ROOT=parent.ROOT
WORK=parent.WORK
base=parent.base
DRIVER="scripts/build_th03_mainl_sound_after558_work.py"
CONFIG="config/mainl_work/sound_after558.json"
PREFIX=".analysis/work/sound-after558-native-"
REPORT=PREFIX+"build.json"
STAGE="af558s"
SCRATCH=WORK/("probe/"+STAGE)

def inputs():
    cfg, digest=base.load(CONFIG)
    want=[
      ("snd_mode.c","src/mainl/linked_game/sound_mode.c","O",30,"obj/th02/snd_mode.obj"),
      ("snd_pmdr.c","src/mainl/linked_game/sound_pmd.c","O",58,"obj/th02/snd_pmdr.obj"),
      ("snd_dlyv.c","src/mainl/linked_game/sound_volume.c","M",28,"obj/th02/snd_dlyv.obj"),
      ("snd_se_r.cpp","src/mainl/linked_game/sound_reset.cpp","O",12,"obj/th02/snd_se_r.obj")]
    need(cfg["schema"]=="th03-mainl-sound-after558-v1" and
         cfg["parent_report"]==parent.REPORT and
         [(u["module"],u["source"],u["first_binary"],u["CODE_bytes"],u["original_object"]) for u in cfg["units"]]==want
         and (cfg["function_instruction_bytes"],cfg["contextual_codestring_tail_bytes"])==(124,4)
         and cfg["whole_product_accepted"] is False and cfg["canonical_credit_changed"] is False,
         "four complete original first-use GAME/BINARY producers and bounded tail contract")
    return cfg,digest

def native_src(raw):
    return raw.decode("utf-8").encode("cp932").replace(b"\n",b"\r\n")

def wrapper(u):
    name=u["source"].rsplit("/",1)[-1]
    return f'#include "probe/{STAGE}/{name}"\r\n'.encode()

def response(number):
    raw=parent.response(number)
    need(raw.count(b"af557v")==10, "retained after557 parent response")
    raw=raw.replace(b"af557v",STAGE.encode())
    cfg,_=inputs()
    for u in cfg["units"]:
        name=u["module"].rsplit(".",1)[0]
        old=u["original_object"].replace("/", "\\").encode()
        new=f"probe\\{STAGE}\\{name}.obj".encode()
        need(raw.count(old)==1,"one original sound object occurrence "+name)
        raw=raw.replace(old,new)
    return raw

def map_normalized(raw):
    cfg,_=inputs()
    for u in cfg["units"]:
        old=f"M=probe/{STAGE}/{u['module']}".encode()
        new=f"M=th02/{u['module']}".encode()
        need(raw.count(old)==3, "complete original CODE/DATA/BSS contribution rows "+u["module"])
        raw=raw.replace(old,new)
    return parent.map_normalized(raw)

def obj_equivalent(new, original,code_len):
    x=payload(new); y=payload(original)
    need(x==y and len(x)==code_len and set(x)=={(1,i) for i in range(code_len)}
         and y[1,code_len-1]==0x90 and literal_fields(new)==literal_fields(original)
         and public_offsets(new)==public_offsets(original),
         "all native source object code, literal fixups, complete PUBLIC and contextual tail")
    return dict(CODE_bytes=code_len,
                instruction_bytes=code_len-1,
                contextual_codestring_tail_bytes=1,
                fixups=len(literal_fields(new)),
                public_definitions=len(public_offsets(new)))

def main():
    cfg,cfg_hash=inputs()
    prior,prior_hash=base.load(parent.REPORT)
    need(prior["complete"] and prior_hash==cfg["parent_report_sha256"],
         "actual after557 2-round vector/source-root parent")
    original={u["module"]:(WORK/u["original_object"]).read_bytes() for u in cfg["units"]}
    source={u["source"]:(ROOT/u["source"]).read_bytes() for u in cfg["units"]}
    need(all(raw.count(b'#pragma codestring "\\x90"')==1 for raw in source.values()),
         "historical unproven per-TU padding retained, not newly attributed as natural compiler code")
    outputs=dict(complete=False,source_acceptance=False,whole_product_accepted=False,
        canonical_credit_changed=False,cold_rebuilt=False,library_rebuilt=False,
        game_objects_recompiled=4,sound_function_instruction_bytes=124,
        historical_contextual_tail_bytes=4,config_sha256=cfg_hash,
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),parent_report_sha256=prior_hash,
        source_sha256={k:sha(v) for k,v in source.items()},
        original_sha256={k:sha(v) for k,v in original.items()},phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(outputs,indent=2)+"\n")
    env=dict(os.environ,DISPLAY="",WAYLAND_DISPLAY="",WINEDEBUG="-all",
        WINEPREFIX=str(ROOT/".analysis/toolchain/wineprefix"),
        MSDOS_PATH=r"C:\TC4\BIN",TZ="UTC",LANG="C",LC_ALL="C")
    dos=["/usr/bin/wine-stable",str(ROOT/"_reference/ReC98/bin/msdos.exe"),"-e","-x"]
    def run(cmd,label):
        p=subprocess.run(cmd,cwd=WORK,env=env,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,timeout=100)
        log=PREFIX+label+".log"
        (ROOT/log).write_bytes(p.stdout)
        outputs["phases"].append(dict(label=label,argv=cmd,log=log,log_sha256=sha(p.stdout),returncode=p.returncode))
        save()
        need(p.returncode==0,label+": "+p.stdout.decode(errors="replace")[-1300:])

    with (ROOT/".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock,fcntl.LOCK_EX | fcntl.LOCK_NB)
        need(not SCRATCH.exists(), "fresh preserved sound native build stage")
        SCRATCH.mkdir()
        for u in cfg["units"]:
            filename=u["source"].rsplit("/",1)[-1]
            for path,raw in [(filename,native_src(source[u["source"]])),(u["module"],wrapper(u))]:
                (SCRATCH/path).write_bytes(raw)
                os.utime(SCRATCH/path,(946684800,946684800))
        for n,raw in [("driver.py",(ROOT/DRIVER).read_bytes()),("config.json",(ROOT/CONFIG).read_bytes())]:
            (SCRATCH/n).write_bytes(raw)
        pair=[]
        for number in (1,2):
            ancestor=prior["rounds"][number-1]
            for key,path in [("startup","c0l.obj"),("library",f"r{number}.lib"),
                             ("root","rootdata.obj"),("pictures","rootpre.obj")]:
                (SCRATCH/path).write_bytes(base.checked(ancestor["reused"][key]))
            for key,path in [("registration","regpre.obj"),("ending","regtail.obj")]:
                (SCRATCH/path).write_bytes(base.checked(ancestor["reused_banks"][key]))
            (SCRATCH/"mainl.obj").write_bytes(base.checked(ancestor["reused_root"]))
            (SCRATCH/"vector_far.obj").write_bytes(base.checked(ancestor["outputs"]["obj"]))
            objects={}
            properties={}
            for u in cfg["units"]:
                name=u["module"].rsplit(".",1)[0]
                command=dos+["tcc","-c","-I.","-O","-b-","-3","-Z","-d","-DGAME=2","-ml",
                             "-DBINARY='"+u["first_binary"]+"'",
                             f"-nprobe/{STAGE}/",f"probe/{STAGE}/{u['module']}"]
                run(command,f"round{number}-{name}-compile")
                compiled=(SCRATCH/(name+".obj")).read_bytes()
                properties[name]=obj_equivalent(compiled,original[u["module"]],u["CODE_bytes"])
                objects[name]=compiled
            rsp=response(number)
            (SCRATCH/f"r{number}.lnk").write_bytes(rsp)
            run(dos+["tlink",f"@probe\\{STAGE}\\r{number}.lnk"],f"round{number}-link")
            v={**objects,"exe":(SCRATCH/f"r{number}.exe").read_bytes(),
               "map":(SCRATCH/f"r{number}.map").read_bytes()}
            need(v["exe"]==base.checked(ancestor["outputs"]["exe"]) and
                 map_normalized(v["map"])==parent.map_normalized(base.checked(ancestor["outputs"]["map"])),
                 "entire original MZ EXE with all677 ordered relocations and actual MAP layout")
            native={}
            for key,raw in v.items():
                fn=PREFIX+f"round{number}-{key}.bin"
                (ROOT/fn).write_bytes(raw)
                native[key]=dict(path=fn,bytes=len(raw),sha256=sha(raw))
            outputs["rounds"].append(dict(round=number,outputs=native,
                object_properties=properties,response_sha256=sha(rsp),
                reused=ancestor["reused"],reused_banks=ancestor["reused_banks"],
                reused_root=ancestor["reused_root"],reused_vector=ancestor["outputs"]["obj"]))
            save()
            pair.append(v)
            print(f"Sound round {number}: 4 natural C/C++ bodies, total 124 instruction bytes, 4 contextual tails; original EXE exact",flush=True)
        need(pair[0]==pair[1] and all((ROOT/n).read_bytes()==raw for n,raw in source.items()),
             "whole OBJ/EXE/MAP native pair and unchanged sources repeat")
    outputs["complete"]=True
    save()

if __name__=="__main__":
    main()
