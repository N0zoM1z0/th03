#!/usr/bin/env python3
"""Recompile eight large natural C++ boss TUs; relink only their original slots.

Reuses MAIN's unchanged source-cold pair and after559 Chiyuri proof.
Round1 already has separately stored fresh compiler receipts. Round2 compiles
all eight in independent source trees. Both rounds run real TLINK on the normal
99-object response; no complete game cold replay or patched objects.
"""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys

import build_th03_main_boss_chiyuri_after559_work as prior
from lib.omf import normalize_dependency_timestamps
from lib.pc98 import parse_mz
from build_th03_mainl_resources_work import need,sha

ROOT=prior.ROOT
WORK=prior.WORK
DRIVER="scripts/build_th03_main_eight_bosses_after560_work.py"
CONFIG="config/main_work/eight_bosses_after560.json"
PREFIX=".analysis/work/main-eight-bosses-after560-native-"
REPORT=PREFIX+"build.json"
STAGE="af560b"
SCRATCH=WORK/("probe/"+STAGE)

def inputs():
    cfg=json.loads((ROOT/CONFIG).read_text())
    need(cfg['schema']=="th03-main-eight-bosses-after560-v1" and
         cfg['parent_report']==prior.REPORT and
         cfg['original_CODE_bytes']==14797 and
         cfg['complete_procedures']==74 and
         cfg['inline_switch_bytes']==636 and
         cfg['native_cold_replay'] is False and
         cfg['canonical_credit_changed'] is False and
         cfg['whole_original_MAIN_file_accepted'] is False and
         len(cfg['bosses'])==8 and
         [x['name'] for x in cfg['bosses']]==[
             'yumemi','kana','mima','reimu','kotohime','ellen','rikako','marisa'] and
         sum(x['size'] for x in cfg['bosses'])==14797 and
         sum(x['functions'] for x in cfg['bosses'])==74 and
         sum(x['switch_bytes'] for x in cfg['bosses'])==636,
         'eight complete first-use natural C++ boss producers')
    for x in cfg['bosses']:
        need(x['size']>300 and
             x['source']==f"src/main/boss/{x['name']}.cpp" and
             x['probe']==(
                 'scripts/probe_th03_main_boss_marisa_native_corrected.py'
                 if x['name']=='marisa' else
                 f"scripts/probe_th03_main_boss_{x['name']}_cpp.py") and
             x['object'] in ('ba_yumem','ba_kana','ba_mima','ba_reimu',
                             'ba_koto','ba_ellen','ba_rikak','ba_maris') and
             x['first_probe']!=x['second_probe'] and
             x['offset']+x['size']<=0x47EA,
             'original boss function size, source/first-use compiler path')
    return cfg,sha((ROOT/CONFIG).read_bytes())

def response(cfg,n):
    raw=(WORK/'obj/th03/main.@l').read_bytes()
    need(sha(raw)==cfg['main_link_response_sha256'], 'unchanged original source-only MAIN response')
    for x in cfg['bosses']:
        old=f"obj\\th03\\{x['object']}.obj".encode()
        new=f"probe\\{STAGE}\\r{n}\\{x['object']}.obj".encode()
        need(raw.count(old)==1,'original one-object contribution '+x['name'])
        raw=raw.replace(old,new)
    for original,new in [
         (rb'bin\th03\main.exe',f'probe\\{STAGE}\\r{n}.exe'.encode()),
         (rb'obj\th03\main.map',f'probe\\{STAGE}\\r{n}.map'.encode())]:
        need(raw.count(original)==1,'exact one link output')
        raw=raw.replace(original,new)
    return raw

def probe_folder(x,n):
    probe_id=x['first_probe'] if n==1 else x['second_probe']
    return ROOT/f".analysis/th03-main-boss-{x['name']}-cpp/{probe_id}"

def original():
    cfg,_=inputs()
    pre,_=prior.inputs()
    parent,hash_parent=prior.load(cfg['parent_report']) if hasattr(prior,'load') else (
      json.loads((ROOT/cfg['parent_report']).read_text()),sha((ROOT/cfg['parent_report']).read_bytes()))
    need(parent['complete'] and hash_parent==cfg['parent_report_sha256'],
         'complete source-born Chiyuri prior without cold replay')
    original_obj,selected,map_raw,target=prior.verify_reference(pre)
    need(sha(selected)==cfg['native_selected_main_exe_sha256'] and
         sha(map_raw)==cfg['native_selected_main_map_sha256'],
         'entire pinned native MAIN source-selected EXE/MAP')
    t=parse_mz(target);s=parse_mz(selected)
    start=0xF1F*16
    for x in cfg['bosses']:
        a=start+x['offset'];z=a+x['size']
        need(s.program_image[a:z]==t.program_image[a:z] and len(s.program_image[a:z])==x['size'],
             'complete current actual original target CODE '+x['name'])
    need(t.relocations==s.relocations and len(t.relocations)==1553,
         'all original MAIN ordered MZ relocations retained')
    return selected,map_raw,target

def validate_probe(x,n,source_sha,probe_sha):
    folder=probe_folder(x,n)
    receipt_path=folder/'receipt.json'
    need(receipt_path.is_file(),'actual complete original TCC receipt '+x['name'])
    row=json.loads(receipt_path.read_text())
    obj=(folder/f"source/obj/th03/{x['object']}.obj").read_bytes()
    ref=(WORK/f"obj/th03/{x['object']}.obj").read_bytes()
    need(row['source_acceptance'] and row['exact_acceptance'] is False and
         row['object']['sha256']==sha(obj) and
         row['object']['code_size']==x['size'] and
         len(row['object']['code_publics'])==x['functions'] and
         len(row['comparison']['function_differences'])==0 and
         row['comparison']['table_semantics_equal'] and
         row['comparison']['candidate_table_span'][1]-
         row['comparison']['candidate_table_span'][0]==x['switch_bytes'] and
         normalize_dependency_timestamps(obj)==normalize_dependency_timestamps(ref),
         'all original CODE/FIXUP/PUBLIC/OMF normal compiler bytes '+x['name'])
    need(row['build']['exit_code']==0 and
         '-a2' not in row['build']['argv'][-1] and
         row['inputs'][x['source']]==source_sha and
         row['inputs'][x['probe']]==probe_sha and
         all(sha((ROOT/path).read_bytes())==digest for path,digest in row['inputs'].items()),
         'full current natural C++ source/header compiler proof '+x['name'])
    return obj,dict(receipt_path=str(receipt_path.relative_to(ROOT)),
        receipt_sha256=sha(receipt_path.read_bytes()),source_object_sha256=sha(obj),
        normalized_original_OMF_equal=True,
        functions=x['functions'],CODE_bytes=x['size'],switch_bytes=x['switch_bytes'])

def main():
    cfg,cfg_sha=inputs()
    selected,map_raw,target=original()
    sources={x['source']:sha((ROOT/x['source']).read_bytes()) for x in cfg['bosses']}
    scripts={x['probe']:sha((ROOT/x['probe']).read_bytes()) for x in cfg['bosses']}
    need(all(b'-a2 -nobj' not in (ROOT/path).read_bytes() for path in scripts) and
         sha((ROOT/'scripts/probe_th03_main_boss_marisa_cpp.py').read_bytes())==
         '271ca45e64db11e6575c8160659126d234b566ce21f42110af9e51a8b06ff9f3',
         'corrected separate Marisa producer, immutable OP/MAINL/ZUN recipe dependency')
    report=dict(complete=False,cold_rebuilt=False,
        number_of_game_objects_recompiled_per_full_round=8,
        original_OTHER_GAME_objects_reused=91,
        accepted_ever_firstuse_source_objects=8,
        original_large_boss_CODE_bytes=14797,complete_boss_procedures=74,
        original_inline_switch_bytes=636,canonical_credit_changed=False,
        whole_original_MAIN_file_accepted=False,
        source_sha256=sources,probe_sha256=scripts,driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        config_sha256=cfg_sha,parent_report_sha256=cfg['parent_report_sha256'],
        original_target_sha256=sha(target),baseline_source_MAIN_sha256=sha(selected),
        baseline_MAP_sha256=sha(map_raw),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
        WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'),
        MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']
    def run(argv,cwd,label,timeout=105):
        p=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=timeout)
        log=PREFIX+label+'.log'
        (ROOT/log).write_bytes(p.stdout)
        report['phases'].append(dict(label=label,argv=argv,returncode=p.returncode,
            log=log,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1300:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh eight-boss retained source proof stage')
        SCRATCH.mkdir()
        (SCRATCH/'driver.py').write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/'config.json').write_bytes((ROOT/CONFIG).read_bytes())
        vectors=[]
        for n in (1,2):
            (SCRATCH/f'r{n}').mkdir()
            objs={}
            witnesses={}
            for x in cfg['bosses']:
                if n==2:
                    folder=probe_folder(x,n)
                    need(not folder.exists(),'fresh independent compiled source round2 '+x['name'])
                    run([sys.executable,str(ROOT/x['probe']),'--run-id',x['second_probe']],
                        ROOT,f'round2-{x["name"]}-TC4-compile',120)
                obj,witness=validate_probe(x,n,sources[x['source']],scripts[x['probe']])
                (SCRATCH/f'r{n}'/(x['object']+'.obj')).write_bytes(obj)
                objs[x['object']]=obj
                witnesses[x['name']]=witness
            rsp=response(cfg,n)
            (SCRATCH/f'r{n}.@l').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{n}.@l'],WORK,
                f'round{n}-eight-boss-native-TLINK',105)
            raw_exe=(SCRATCH/f'r{n}.exe').read_bytes()
            raw_map=(SCRATCH/f'r{n}.map').read_bytes()
            need(raw_exe==selected and raw_map==map_raw and
                 parse_mz(raw_exe).relocations==parse_mz(target).relocations,
                 'entire normal MAIN 99-object selected output and all target MZ fields')
            vector={**objs,'exe':raw_exe,'map':raw_map}
            outputs={}
            for key,raw in vector.items():
                path=PREFIX+f'round{n}-{key}.bin'
                (ROOT/path).write_bytes(raw)
                outputs[key]=dict(path=path,bytes=len(raw),sha256=sha(raw))
            report['rounds'].append(dict(round=n,outputs=outputs,
                probe_receipts=witnesses,normal_link_response_sha256=sha(rsp),
                full_selected_native_MAIN_EXE_equal=True,full_MAP_equal=True,
                original_1553_ordered_MZ_relocations_equal=True))
            save()
            vectors.append(vector)
            print('Eight bosses native round',n,
                  '14797 CODE,74 complete C++ procedures, 8 OMF producers, full MAIN native EXE+MAP exact',flush=True)
        need(vectors[0]['exe']==vectors[1]['exe'] and
             vectors[0]['map']==vectors[1]['map'] and
             all(normalize_dependency_timestamps(vectors[0][x['object']])==
                 normalize_dependency_timestamps(vectors[1][x['object']])
                 for x in cfg['bosses']),
             'whole selected native EXE/MAP vectors and eight normalized OMF producers repeat')
        need(sources=={x['source']:sha((ROOT/x['source']).read_bytes()) for x in cfg['bosses']} and
             scripts=={x['probe']:sha((ROOT/x['probe']).read_bytes()) for x in cfg['bosses']},
             'no source or compiler script drift during rounds')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
