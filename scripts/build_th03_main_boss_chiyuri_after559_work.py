#!/usr/bin/env python3
"""Two independent actual TC4 builds of Chiyuri boss, relink only its OBJ.

The original MAIN cold build is reused, never replayed. Verify full normalized
OMF identity, full selected MAIN native EXE/MAP, target boss bytes and all
ordered MZ relocations. Earlier global -a2 control is deliberately rejected.
"""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys

import build_th03_main_work as main
from lib.omf import normalize_dependency_timestamps
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from build_th03_mainl_resources_work import need, sha

ROOT=main.ROOT
WORK=main.WORK
DRIVER="scripts/build_th03_main_boss_chiyuri_after559_work.py"
PROBE="scripts/probe_th03_main_boss_chiyuri_cpp.py"
CONFIG="config/main_work/chiyuri_boss_after559.json"
PREFIX=".analysis/work/main-chiyuri-after559-native-"
REPORT=PREFIX+"build.json"
STAGE="af559ch"
SCRATCH=WORK/("probe/"+STAGE)

def inputs():
    cfg=json.loads((ROOT/CONFIG).read_text())
    need(cfg['schema']=="th03-main-boss-chiyuri-after559-v1" and
         cfg['main_native_report']==".analysis/work/main-build.json" and
         cfg['source']=="src/main/boss/chiyuri.cpp" and
         cfg['original_object']=="obj/th03/ba_chiyu.obj" and
         cfg['original_code_size']==2654 and cfg['complete_functions']==11 and
         (cfg['switch_table_offset'],cfg['switch_table_bytes'])==(1904,81) and
         (cfg['decoded_main_owner_start'],cfg['decoded_main_owner_bytes'])==(74141,2654) and
         cfg['target_load_image_mismatch_outside_owner']==0xEC2D and
         cfg['probe_run_ids']==["gptweb-chiyuri-559-proof-r1","gptweb-chiyuri-559-proof-r2"] and
         cfg['whole_main_original_exe_accepted'] is False and
         cfg['canonical_credit_changed'] is False,
         'complete boss natural source and known original MAIN limits')
    return cfg,sha((ROOT/CONFIG).read_bytes())

def link_response(cfg, number):
    raw=(WORK/'obj/th03/main.@l').read_bytes()
    need(sha(raw)==cfg['native_link_response_sha256'],
         'original unchanged MAIN link response')
    for x,y in [(rb'obj\th03\ba_chiyu.obj', f'probe\\{STAGE}\\r{number}.obj'.encode()),
                (rb'bin\th03\main.exe',f'probe\\{STAGE}\\r{number}.exe'.encode()),
                (rb'obj\th03\main.map',f'probe\\{STAGE}\\r{number}.map'.encode())]:
        need(raw.count(x)==1,'single original object/target root link placeholder '+str(x))
        raw=raw.replace(x,y)
    return raw

def verify_reference(cfg):
    record=json.loads((ROOT/cfg['main_native_report']).read_text())
    need(record['complete'] and record['native_outputs_unchanged'] and
         record['staged_sources_unchanged'] and
         sha((ROOT/cfg['main_native_report']).read_bytes())==cfg['main_native_report_sha256'],
         'real complete unchanged cold pair, without calling any cold builder')
    original_obj=(WORK/cfg['original_object']).read_bytes()
    selected=(WORK/'bin/th03/main.exe').read_bytes()
    map_raw=(WORK/'obj/th03/main.map').read_bytes()
    need(sha(selected)==cfg['native_link_exe_sha256'] and
         sha(map_raw)==cfg['native_link_map_sha256'] and len(original_obj)>2654,
         'genuine retained original source build outputs')
    target=read_verified_artifact(ROOT,find_artifact(
        load_target_manifest(ROOT/'config/targets.toml'),'th03-main'))
    t=parse_mz(target); s=parse_mz(selected)
    need(len(t.relocations)==len(s.relocations)==1553 and t.relocations==s.relocations,
         'original all 1553 ordered MAIN MZ fixups')
    differences=[i for i,(a,b) in enumerate(zip(t.program_image,s.program_image)) if a!=b]
    mismatch=cfg['target_load_image_mismatch_outside_owner']
    need(len(s.program_image)==len(t.program_image) and differences==[mismatch] and
         t.program_image[mismatch]==0x90 and s.program_image[mismatch]==0x00,
         'separate, previously diagnosed one-byte original MAIN load-image difference')
    start,size=cfg['decoded_main_owner_start'],cfg['decoded_main_owner_bytes']
    need(s.program_image[start:start+size]==t.program_image[start:start+size],
         'all 2654 original boss/inline switch bytes already exact in retained image')
    return original_obj,selected,map_raw,target

def main_run():
    cfg,cfg_sha=inputs()
    source=(ROOT/cfg['source']).read_bytes()
    probe=(ROOT/PROBE).read_bytes()
    need(b'-a2 -nobj' not in probe and
         b'-nobj/th03/ th03/ba_chiyu.cpp' in probe and
         b'#pragma option -a2' in source,
         'correct original compiler command with source-local packing preserved')
    original,selected,original_map,target=verify_reference(cfg)
    source_hash=sha(source); probe_hash=sha(probe)
    result=dict(complete=False,cold_rebuilt=False,original_MAIN_source_accepted=False,
        canonical_credit_changed=False,game_objects_recompiled=1,per_round_recompiles=1,
        untouched_game_objects_reused=98,source_sha256=source_hash,probe_sha256=probe_hash,
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),config_sha256=cfg_sha,
        base_report_sha256=cfg['main_native_report_sha256'],
        original_object_sha256=sha(original),baseline_native_EXE_sha256=sha(selected),
        baseline_native_MAP_sha256=sha(original_map),
        original_target_sha256=sha(target),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(result,indent=2)+'\n')
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
        WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'),
        MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']

    def run(argv,cwd,label,limit):
        p=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,timeout=limit)
        log=PREFIX+label+'.log'
        (ROOT/log).write_bytes(p.stdout)
        result['phases'].append(dict(label=label,argv=argv,returncode=p.returncode,
            log=log,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1500:])

    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh retained Chiyuri single-object stage')
        SCRATCH.mkdir(parents=True)
        (SCRATCH/'driver.py').write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/'config.json').write_bytes((ROOT/CONFIG).read_bytes())
        vectors=[]
        for n,probe_id in enumerate(cfg['probe_run_ids'],1):
            probe_root=ROOT/('.analysis/th03-main-boss-chiyuri-cpp/'+probe_id)
            need(not probe_root.exists(),'fresh independent source materialization '+probe_id)
            run([sys.executable,str(ROOT/PROBE),'--run-id',probe_id],ROOT,
                f'round{n}-boss-TCC-compile',120)
            receipt_path=probe_root/'receipt.json'
            receipt=json.loads(receipt_path.read_text())
            candidate=(probe_root/'source/obj/th03/ba_chiyu.obj').read_bytes()
            need(receipt['source_acceptance'] and
                 receipt['exact_acceptance'] is False and
                 receipt['object']['sha256']==sha(candidate) and
                 receipt['comparison']['candidate_size']==cfg['original_code_size'] and
                 len(receipt['comparison']['function_differences'])==0 and
                 receipt['comparison']['table_semantics_equal'] and
                 len(receipt['object']['code_publics'])==11 and
                 receipt['comparison']['candidate_table_span']==[1904,1985] and
                 normalize_dependency_timestamps(candidate)==normalize_dependency_timestamps(original),
                 'all 2654 bytes/11 C++ functions/81-byte switch and complete normalized original OMF')
            need(receipt['inputs'][cfg['source']]==source_hash and
                 receipt['inputs'][PROBE]==probe_hash and
                 all(sha((ROOT/path).read_bytes())==digest for path,digest in receipt['inputs'].items()),
                 'complete source/header/compiler probe dependency graph')
            (SCRATCH/f'r{n}.obj').write_bytes(candidate)
            rsp=link_response(cfg,n)
            (SCRATCH/f'r{n}.@l').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{n}.@l'],WORK,f'round{n}-boss-TLINK-link',100)
            v=dict(obj=candidate,exe=(SCRATCH/f'r{n}.exe').read_bytes(),
                   map=(SCRATCH/f'r{n}.map').read_bytes())
            need(v['exe']==selected and v['map']==original_map and
                 parse_mz(v['exe']).relocations==parse_mz(target).relocations,
                 'entire actual MAIN source-selected native EXE/MAP and all1553 target MZ fields')
            files={}
            for k,raw in v.items():
                path=PREFIX+f'round{n}-{k}.bin'
                (ROOT/path).write_bytes(raw)
                files[k]=dict(path=path,bytes=len(raw),sha256=sha(raw))
            result['rounds'].append(dict(round=n,output=files,
                native_response_sha256=sha(rsp),probe_run_id=probe_id,
                probe_receipt_sha256=sha(receipt_path.read_bytes()),
                normalized_original_OMF_equal=True,all_11_function_shapes_exact=True,
                whole_native_MAIN_EXE_reproduced=True,all_1553_target_relocations_equal=True))
            save()
            vectors.append(v)
            print('Chiyuri round',n,'11 complete natural C++ procedures/2654 CODE, full selected MAIN EXE+MAP exact',flush=True)
        need(len(vectors)==2 and vectors[0]['exe']==vectors[1]['exe'] and
             vectors[0]['map']==vectors[1]['map'] and
             normalize_dependency_timestamps(vectors[0]['obj'])==normalize_dependency_timestamps(vectors[1]['obj']),
             'both independent source-produced native OBJ/EXE/MAP vectors agree')
        need(source==(ROOT/cfg['source']).read_bytes() and probe==(ROOT/PROBE).read_bytes(),
             'maintained compiler script and product source unchanged during two rounds')
    result['complete']=True
    save()

if __name__=='__main__':
    main_run()
