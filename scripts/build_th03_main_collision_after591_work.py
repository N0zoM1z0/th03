#!/usr/bin/env python3
"""Reassemble/compile three original TH03 collision objects in two native rounds.

Preserve the actual original 16-bit hitbox explosion-call encoding. Three
compilable natural C++ variants were tried, but their direct 9A far calls
did not match original 90 0E E8 near-call provenance. These remain negative
controls, not the source of the accepted product. The true maintained
TASM 386 bitstripe source, hit-circle and hitbox are all source recompiled.
"""
import fcntl,json,os,subprocess
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz
import build_th03_main_fireball_after589_work as parent

ROOT=parent.ROOT
WORK=parent.WORK
DRIVER="scripts/build_th03_main_collision_after591_work.py"
CONFIG="config/main_work/collision_after591.json"
PREFIX=".analysis/work/main-collision-after591-native-"
REPORT=PREFIX+"build.json"
STAGE="af591c"
SCRATCH=WORK/("probe/"+STAGE)
TASM=ROOT/".analysis/toolchain/wineprefix/drive_c/TASM50/bin/TASM32.EXE"
ORDER=("hitbox","hitcirc","collmap")

def inputs():
    cfg=json.loads((ROOT/CONFIG).read_text())
    expected=[
        ("hitbox","src/main/collision/hitbox.cpp",
         "src/main/collision/producers/hitbox_native.cpp","TC4",266,1,33),
        ("hitcirc","src/main/collision/hitcircle.cpp",
         "src/main/collision/producers/hitcircle_native.cpp","TC4",445,4,30),
        ("collmap","src/main/collision/map.asm",
         "src/main/collision/producers/collmap_native.asm","TASM",432,3,27)]
    need(cfg["schema"]=="th03-main-collision-after591-v1" and
         cfg["parent_report"]==parent.REPORT and
         [(u["stem"],u["source"],u["wrapper"],u["emitter"],u["CODE_bytes"],
           u["PUBLICs"],u["FIXUPPs"]) for u in cfg["units"]]==expected and
         (cfg["total_original_CODE_bytes"],cfg["total_original_PUBLIC_functions"],
          cfg["total_ordered_literal_FIXUPP_fields"],cfg["original_main_relocations"],
          cfg["original_japanese_MZ_bytes"])==(1143,8,90,1553,130882) and
         cfg["preserved_original_hitbox_nop_push_cs_near_call"] is True and
         cfg["original_VENDOR_OMF_packet_identity_proved"] is False and
         cfg["canonical_factory_credit_changed"] is False and
         cfg["whole_project_source_accepted"] is False,
         "three complete original hitbox/circle/collision map game producer extents")
    parent_record=json.loads((ROOT/cfg["parent_report"]).read_text())
    need(parent_record["complete"] and len(parent_record["rounds"])==2 and
         sha((ROOT/cfg["parent_report"]).read_bytes())==cfg["parent_report_sha256"],
         "real source-built native FIREBALL+BULLET+BOSS+ENEMY program parent")
    return cfg,sha((ROOT/CONFIG).read_bytes()),parent_record

def sources(cfg):
    values={}
    for u in cfg["units"]:
        source=(ROOT/u["source"]).read_bytes()
        wrapper=(ROOT/u["wrapper"]).read_bytes()
        need(source and b"\r" not in source and b"\r" not in wrapper and
             (WORK/u["source"]).read_bytes().replace(b"\r\n",b"\n")==source,
             "unmodified natural compiled collision source "+u["stem"])
        snippet=(f'#include "{u["source"]}"\n' if u["emitter"]=="TC4"
                 else f"include {u['source']}\n").encode()
        need(wrapper.endswith(snippet) and wrapper.count(snippet.strip())==1,
             "single genuinely maintained natural source forwarding TU "+u["stem"])
        values[u["stem"]]=dict(source=source,wrapper=wrapper)
    hitbox=values["hitbox"]["source"]
    need(hitbox.count(b"asm { nop; push cs; call near ptr explosions_hittest; }")==1,
         "source-retained original 16-bit same-segment explosion call semantics")
    return values

def negative_control(reference):
    folder=WORK/"probe/af590h"
    variants={}
    original=payload(reference)
    assert (original[1,207],original[1,208],original[1,209])==(0x90,0x0e,0xe8)
    for variant in ("v1","v2","v3"):
        p=folder/variant/"hitbox.obj"
        raw=p.read_bytes()
        f=payload(raw)
        need(len(f)==266 and f!=original and f[1,207]==0x9a and
             f[1,208]==0 and f[1,209]==0 and
             literal_fields(raw)!=literal_fields(reference) and
             (folder/variant/"compiler.log").exists(),
             "three truly compiled but source-incorrect ordinary C++ far-call controls")
        variants[variant]=dict(object_sha256=sha(raw),
             original_function_bytes_equal=False,
             actual_far_call_opcode=f[1,207],
             real_original_nop_opcode=original[1,207],
             original_literal_FIXUPP_equal=False)
    return variants

def object_scope(data,original,u):
    actual=payload(data)
    reference=payload(original)
    publics=public_offsets(data)
    need(actual==reference and len(actual)==u["CODE_bytes"] and
         literal_fields(data)==literal_fields(original) and
         len(literal_fields(data))==u["FIXUPPs"] and
         publics==public_offsets(original) and len(publics)==u["PUBLICs"] and
         segment_definitions(data)==segment_definitions(original),
         "all original source-native 386/16bit CODE, ordered relocation sites, PUBLIC and segment geometry")
    return dict(CODE_bytes=u["CODE_bytes"],original_PUBLICs=u["PUBLICs"],
        ordered_OMF_fixups=u["FIXUPPs"],complete_original_CODE_and_symbols_equal=True,
        original_vendor_packet_identity=False)

def response(n):
    raw=parent.response(n)
    for stem in ORDER:
        before=f"obj\\th03\\{stem}.obj".encode()
        after=f"probe\\{STAGE}\\r{n}\\{stem}.obj".encode()
        need(raw.count(before)==1,"one actual original native collision object slot "+stem)
        raw=raw.replace(before,after)
    for old,new in [(f"probe\\{parent.STAGE}\\r{n}.exe",
                     f"probe\\{STAGE}\\r{n}.exe"),
                    (f"probe\\{parent.STAGE}\\r{n}.map",
                     f"probe\\{STAGE}\\r{n}.map")]:
        need(raw.count(old.encode())==1,"one retained normal MAIN source linker output")
        raw=raw.replace(old.encode(),new.encode())
    return raw

def normalize_map(raw,n):
    for stem in ORDER:
        old=(f"M=probe\\{STAGE}\\r{n}\\{stem}.asm" if stem=="collmap"
             else f"M=probe/{STAGE}/r{n}/{stem}.cpp").encode()
        new=(f"M=th03\\{stem}.asm" if stem=="collmap"
             else f"M=th03/{stem}.cpp").encode()
        count=(2 if stem=="collmap" else 3)
        need(raw.count(old)==count,"all original CODE/DATA/BSS native MAP contribution rows "+stem)
        raw=raw.replace(old,new)
    return raw

def read_pin(pin):
    return parent.read_pin(pin)

def main():
    cfg,cfg_sha,previous=inputs()
    data=sources(cfg)
    original={u["stem"]:(WORK/f"obj/th03/{u['stem']}.obj").read_bytes()
              for u in cfg["units"]}
    negatives=negative_control(original["hitbox"])
    target=parent.parent.read_verified_artifact(ROOT,parent.parent.find_artifact(
        parent.parent.load_target_manifest(ROOT/"config/targets.toml"),"th03-main"))
    orig_mz=parse_mz(target)
    need(len(target)==130882 and len(orig_mz.relocations)==1553,
         "unchanged Japanese original target and relocation inventory")
    report=dict(complete=False,cold_rebuilt=False,library_rebuilt=False,
        project_objects_recompiled_per_round=3,other_project_objects_reused=96,
        total_CODE_bytes=1143,original_PUBLIC_functions=8,original_OMF_fields=90,
        canonical_factory_credit_changed=False,whole_project_source_accepted=False,
        first_use_profile="GAME=3 BINARY=M original TC4/TASM",
        preserved_original_hitbox_call=True,negative_cpp_far_call_controls=negatives,
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        config_sha256=cfg_sha,parent_report_sha256=cfg["parent_report_sha256"],
        original_target_sha256=sha(target),
        source_sha256={k:{x:sha(y) for x,y in row.items()} for k,row in data.items()},
        original_object_sha256={k:sha(v) for k,v in original.items()},
        phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+"\n")
    env=dict(os.environ,DISPLAY="",WAYLAND_DISPLAY="",WINEDEBUG="-all",
        WINEPREFIX=str(ROOT/".analysis/toolchain/wineprefix"),
        MSDOS_PATH=r"C:\TC4\BIN",TZ="UTC",LANG="C",LC_ALL="C")
    dos=["/usr/bin/wine-stable",str(ROOT/"_reference/ReC98/bin/msdos.exe"),"-e","-x"]
    tasm=["/usr/bin/wine-stable",str(TASM)]
    def run(argv,label):
        p=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=115)
        log=PREFIX+label+".log"
        (ROOT/log).write_bytes(p.stdout)
        report["phases"].append(dict(label=label,argv=argv,
          exit_code=p.returncode,log=log,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+": "+p.stdout.decode(errors="replace")[-1500:])
    with (ROOT/".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),"fresh source-native collision/TASM stage")
        SCRATCH.mkdir()
        (SCRATCH/"driver.py").write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/"config.json").write_bytes((ROOT/CONFIG).read_bytes())
        all_outputs=[]
        for n in (1,2):
            folder=SCRATCH/f"r{n}"
            folder.mkdir()
            blobs={}
            scopes={}
            for u in cfg["units"]:
                stem=u["stem"]
                suffix="cpp" if u["emitter"]=="TC4" else "asm"
                file=folder/f"{stem}.{suffix}"
                file.write_bytes(data[stem]["wrapper"].replace(b"\n",b"\r\n"))
                os.utime(file,(946684800,946684800))
                if u["emitter"]=="TC4":
                    argv=dos+["tcc","-c","-I.","-O","-b-","-3","-Z","-d",
                      "-DGAME=3","-ml","-DBINARY='M'",
                      f"-nprobe/{STAGE}/r{n}/",f"probe/{STAGE}/r{n}/{stem}.cpp"]
                else:
                    argv=tasm+["/m","/mx","/kh32768","/t","/dGAME=3",
                      f"probe\\{STAGE}\\r{n}\\{stem}.asm,probe\\{STAGE}\\r{n}\\{stem}.obj"]
                run(argv,f"round{n}-{stem}-{u['emitter']}")
                obj=(folder/f"{stem}.obj").read_bytes()
                scopes[stem]=object_scope(obj,original[stem],u)
                blobs[stem+"_obj"]=obj
            rsp=response(n)
            (SCRATCH/f"r{n}.@l").write_bytes(rsp)
            run(dos+["tlink",f"@probe\\{STAGE}\\r{n}.@l"],
                f"round{n}-normal-TLINK")
            exe=(SCRATCH/f"r{n}.exe").read_bytes()
            mapped=(SCRATCH/f"r{n}.map").read_bytes()
            before=previous["rounds"][n-1]["outputs"]
            need(exe==read_pin(before["exe"]) and
                 normalize_map(mapped,n)==read_pin(before["map"]) and
                 parse_mz(exe).program_image==orig_mz.program_image and
                 parse_mz(exe).relocations==orig_mz.relocations,
                 "complete original source-native linked MAIN and all 1553 MZ relocations/MAP")
            compact=compact_mz(exe)
            need(compact==target,"independently standardized DOS MZ file original byte-exact")
            vector={**blobs,"exe":exe,"map":mapped,"compact_mz":compact}
            outputs={}
            for key,raw in vector.items():
                dest=PREFIX+f"round{n}-{key}.bin"
                (ROOT/dest).write_bytes(raw)
                outputs[key]=dict(path=dest,bytes=len(raw),sha256=sha(raw))
            report["rounds"].append(dict(round=n,outputs=outputs,
              source_object_scope=scopes,
              actual_normal_link_response_sha256=sha(rsp),
              whole_japanese_MZ_file_exact_after_explicit_format=True))
            save()
            all_outputs.append(vector)
            print("Collision round",n,"1143 original CODE/8 funcs/90 native fields; full 130882-byte Japanese file exact",flush=True)
        need(all_outputs[0]["exe"]==all_outputs[1]["exe"] and
             all_outputs[0]["compact_mz"]==all_outputs[1]["compact_mz"] and
             all(payload(all_outputs[0][s+"_obj"])==payload(all_outputs[1][s+"_obj"]) and
                 literal_fields(all_outputs[0][s+"_obj"])==
                 literal_fields(all_outputs[1][s+"_obj"]) for s in ORDER) and
             sources(cfg)==data,
             "two independent genuine TC4/TASM/LINK input/object vectors repeat")
    report["complete"]=True
    save()

if __name__=="__main__":
    main()
