#!/usr/bin/env python3
"""Native TASM source-link of CDG normal, hflip and no-alpha routines.

These are real symbolic 386 CDG/PC-98 blitters and native assembler EVEN,
not byte arrays or object patches. Only 2 sound/display objects recompile,
using unchanged previous Staff/Cutscene/C0/CRT source-native MAINL link.
"""
import fcntl
import json
import os
import subprocess

import build_th03_mainl_staff_after575_work as parent
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.pc98 import parse_mz

ROOT=parent.ROOT
WORK=parent.WORK
base=parent.base
DRIVER="scripts/build_th03_mainl_cdg_after577_work.py"
CONFIG="config/mainl_work/cdg_after577.json"
PREFIX=".analysis/work/mainl-cdg-after577-native-"
REPORT=PREFIX+"build.json"
STAGE="af577c"
SCRATCH=WORK/("probe/"+STAGE)
TASM=ROOT/".analysis/toolchain/wineprefix/drive_c/TASM50/bin/TASM32.EXE"

def inputs():
    c,h=base.load(CONFIG)
    need(c["schema"]=="th03-mainl-cdg-after577-native-v1" and
         c["parent_report"]==parent.REPORT and
         [(u["stem"],u["source"],u["wrapper"],u["original_CODE_bytes"],
           u["original_FIXUPP_fields"],u["original_PUBLICs"],u["even_at"])
          for u in c["units"]]==[
             ("cdg_put","src/shared/formats/cdg_put.asm",
              "src/mainl/formats/cdg_put_native.asm",382,17,2,[179,381]),
             ("cdg_p_na","src/shared/formats/cdg_noalpha.asm",
              "src/mainl/formats/cdg_noalpha_native.asm",114,2,1,[113])] and
         (c["total_source_CODE_bytes"],c["complete_original_procedures"],
          c["all_original_FIXUPP_fields"],c["documented_TASM_EVEN_boundary_bytes"],
          c["original_decoded_MAINL_EXE_bytes"],c["original_ordered_MZ_relocations"])==
         (496,3,19,3,67372,677) and
         c["original_OMF_packet_identity_claimed"] is False and
         c["canonical_factory_acceptance_changed"] is False and
         c["whole_product_source_accepted"] is False,
         "two complete 386 CDG source modules, no extra source/Factory claim")
    return c,h

def sources(c):
    parts={}
    for u in c["units"]:
        body=(ROOT/u["source"]).read_bytes()
        wrapper=(ROOT/u["wrapper"]).read_bytes()
        need(body and b"\r" not in body and
             wrapper.isascii() and b"\r" not in wrapper and
             wrapper.count(f"include {u['source']}".encode())==1 and
             body.count(b"\teven\n")>=1 and
             b"codestring" not in body.lower() and
             (WORK/u["source"]).read_bytes().replace(b"\r\n",b"\n")==body,
             "original native 386 CDG macros/hardware/assembler source and maintained forwarding TU")
        parts[u["stem"]]=dict(body=body,wrapper=wrapper)
    return parts

def response(n):
    rsp=parent.response(n)
    for stem in ("cdg_put","cdg_p_na"):
        old=f"obj\\th03\\{stem}.obj".encode()
        new=f"probe\\{STAGE}\\{stem}.obj".encode()
        need(rsp.count(old)==1,"single original fixed CDG object in link "+stem)
        rsp=rsp.replace(old,new)
    for old,new in [(f"probe\\af575s\\r{n}.exe",f"probe\\{STAGE}\\r{n}.exe"),
                    (f"probe\\af575s\\r{n}.map",f"probe\\{STAGE}\\r{n}.map")]:
        need(rsp.count(old.encode())==1,"single original MAINL native output")
        rsp=rsp.replace(old.encode(),new.encode())
    return rsp

def map_normalized(raw):
    for stem,count in [("cdg_put",3),("cdg_p_na",1)]:
        before=f"M=probe\\{STAGE}\\{stem}.asm".encode()
        after=f"M=th03\\{stem}.asm".encode()
        need(raw.count(before)==count,"whole CDG CODE/DATA original contributions "+stem)
        raw=raw.replace(before,after)
    return raw

def original_object_scope(native,reference,u):
    x=payload(native);y=payload(reference)
    code=[s["index"] for s in segment_definitions(reference) if s["size"]==u["original_CODE_bytes"]]
    need(len(code)==1,"one exact original real CDG CODE segment")
    seg=code[0]
    need(x==y and len(x)==u["original_CODE_bytes"] and
         len(literal_fields(native))==len(literal_fields(reference))==u["original_FIXUPP_fields"] and
         literal_fields(native)==literal_fields(reference) and
         len(public_offsets(native))==u["original_PUBLICs"] and
         public_offsets(native)==public_offsets(reference) and
         segment_definitions(native)==segment_definitions(reference) and
         all(x[seg,offset]==0x90 for offset in u["even_at"]),
         "all exact CDG original instruction+EVEN bytes, ordered fixups, PUBLICs and segment extents")
    return dict(native_CODE_bytes=len(x),natural_TASM_EVEN_sites=u["even_at"],
                total_original_fixups=len(literal_fields(native)),
                original_PUBLICs=len(public_offsets(native)),
                complete_original_CODE_and_native_fields_equal=True)

def main():
    cfg,cfg_sha=inputs()
    prev,prev_sha=base.load(parent.REPORT)
    need(prev["complete"] and prev_sha==cfg["parent_report_sha256"],
         "actual source-native previous STAFF/large cutscene, TASM sound, root and C0/CRT")
    parts=sources(cfg)
    originals={stem:(WORK/f"obj/th03/{stem}.obj").read_bytes() for stem in parts}
    need(sha(TASM.read_bytes())=="ba50fe547863b96242d98cff54cdf95ab268a8682395afad172eedbfc46c5b26",
         "same exact pinned native TASM5 emitter")
    report=dict(complete=False,cold_rebuilt=False,library_rebuilt=False,
        compiled_project_objects_per_round=2,other_project_objects_reused=34,
        complete_source_CODE_bytes=496,original_PUBLIC_code_functions=3,
        natural_assembler_EVEN_bytes=3,original_OMF_FIXUPP_fields=19,
        canonical_factory_credit_changed=False,whole_product_source_accepted=False,
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),config_sha256=cfg_sha,
        parent_report_sha256=prev_sha,
        sources_sha256={name:{k:sha(raw) for k,raw in value.items()}
                       for name,value in parts.items()},
        original_OMF_sha256={name:sha(blob) for name,blob in originals.items()},
        phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+"\n")
    env=dict(os.environ,DISPLAY="",WAYLAND_DISPLAY="",WINEDEBUG="-all",
             WINEPREFIX=str(ROOT/".analysis/toolchain/wineprefix"),
             MSDOS_PATH=r"C:\TC4\BIN",TZ="UTC",LANG="C",LC_ALL="C")
    tasm=["/usr/bin/wine-stable",str(TASM)]
    dos=["/usr/bin/wine-stable",str(ROOT/"_reference/ReC98/bin/msdos.exe"),"-e","-x"]

    def run(argv,label):
        p=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=105)
        file=PREFIX+label+".log"
        (ROOT/file).write_bytes(p.stdout)
        report["phases"].append(dict(label=label,argv=argv,returncode=p.returncode,
                                     log=file,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+": "+p.stdout.decode(errors="replace")[-1400:])

    with (ROOT/".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),"fresh source-native two-CDG TASM stage")
        SCRATCH.mkdir()
        (SCRATCH/"driver.py").write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/"config.json").write_bytes((ROOT/CONFIG).read_bytes())
        for stem,part in parts.items():
            (SCRATCH/f"{stem}.asm").write_bytes(
                part["wrapper"].replace(b"\n",b"\r\n"))
            os.utime(SCRATCH/f"{stem}.asm",(946684800,946684800))
        vectors=[]
        for n in (1,2):
            objs={}
            scopes={}
            for u in cfg["units"]:
                stem=u["stem"]
                run(tasm+["/m","/mx","/kh32768","/t","/dGAME=3",
                    f"probe\\{STAGE}\\{stem}.asm,probe\\{STAGE}\\{stem}.obj"],
                    f"round{n}-{stem}-TASM-assemble")
                obj=(SCRATCH/f"{stem}.obj").read_bytes()
                scopes[stem]=original_object_scope(obj,originals[stem],u)
                objs[stem+"_obj"]=obj
            rsp=response(n)
            (SCRATCH/f"r{n}.lnk").write_bytes(rsp)
            run(dos+["tlink",f"@probe\\{STAGE}\\r{n}.lnk"],
                f"round{n}-normal-TLINK")
            exe=(SCRATCH/f"r{n}.exe").read_bytes()
            mapped=(SCRATCH/f"r{n}.map").read_bytes()
            old=prev["rounds"][n-1]["outputs"]
            need(exe==base.checked(old["exe"]) and
                 map_normalized(mapped)==base.checked(old["map"]) and
                 len(exe)==67372 and len(parse_mz(exe).relocations)==677,
                 "whole original Japanese decoded MAINL EXE, ordered 677 MZ fixups, MAP geometry")
            native=dict(**objs,exe=exe,map=mapped)
            outputs={}
            for key,raw in native.items():
                file=PREFIX+f"round{n}-{key}.bin"
                (ROOT/file).write_bytes(raw)
                outputs[key]=dict(path=file,bytes=len(raw),sha256=sha(raw))
            report["rounds"].append(dict(round=n,scope=scopes,
                    normal_response_sha256=sha(rsp),outputs=outputs,
                    entire_original_MAINL_EXE_equal=True))
            save()
            vectors.append(native)
            print("CDG original native round",n,"496 CODE, three original functions/3 EVEN, exact 67372-byte EXE",flush=True)
        def stable_map(raw,n):
            mapped=map_normalized(raw)
            for name,stem in (("af573c","cutscene"),("af575s","staffdat")):
                original=f"M=probe/{name}/r{n}/{stem}.cpp".encode()
                need(mapped.count(original)==3,
                     "three original CODE/DATA/BSS round-local diagnostic rows "+stem)
                mapped=mapped.replace(original,f"M=source/{stem}.cpp".encode())
            return mapped
        need(vectors[0]["exe"]==vectors[1]["exe"] and
             vectors[0]["cdg_put_obj"]==vectors[1]["cdg_put_obj"] and
             vectors[0]["cdg_p_na_obj"]==vectors[1]["cdg_p_na_obj"] and
             stable_map(vectors[0]["map"],1)==stable_map(vectors[1]["map"],2) and
             sources(cfg)==parts,
             "two complete independent original CODE/EXE/normalized MAP native vectors repeat")
    report["complete"]=True
    save()

if __name__=="__main__":
    main()
