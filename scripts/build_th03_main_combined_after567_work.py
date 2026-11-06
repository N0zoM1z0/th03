#!/usr/bin/env python3
"""Link original-source nine bosses and natural input scanner together, twice.

Consumes two *independent* native source-produced OBJ rounds from after559,
after561 and after565; never repeats the 99-object cold build. Does not
modify any original OBJ, target binary, source TUs or reusable parent receipt.
"""
import fcntl
import json
import os
import subprocess
from pathlib import Path

from lib.omf import normalize_dependency_timestamps
from lib.pc98 import parse_mz
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
import build_th03_main_work as main

ROOT=main.ROOT
WORK=main.WORK
DRIVER='scripts/build_th03_main_combined_after567_work.py'
CONFIG='config/main_work/combined_after567.json'
PREFIX='.analysis/work/main-combined-after567-native-'
REPORT=PREFIX+'build.json'
STAGE='af567c'
SCRATCH=WORK/('probe/'+STAGE)

def inputs():
    c=json.loads((ROOT/CONFIG).read_text())
    need(c['schema']=='th03-main-combined-after567-v1' and
         set(c['parent_reports'])=={'chiyuri','eight_bosses','input_scan'} and
         c['boss_stems']==['ba_chiyu','ba_yumem','ba_kana','ba_mima','ba_reimu','ba_koto',
                           'ba_ellen','ba_rikak','ba_maris'] and c['input_stem']=='input_s' and
         (c['normal_link_project_objects'],c['replacement_objects'],c['reused_project_objects'],
          c['original_target_program_bytes'],c['original_target_relocations'])==(99,10,89,124642,1553) and
         c['whole_original_EXE_file_accepted'] is False and
         c['canonical_factory_credit_changed'] is False,'bounded ten-source-object MAIN link')
    roots={}
    for name,(path,digest) in c['parent_reports'].items():
        raw=(ROOT/path).read_bytes()
        proof=json.loads(raw)
        need(sha(raw)==digest and proof['complete'] and len(proof['rounds'])==2,
             'actual native complete source parent '+name)
        roots[name]=proof
    return c,sha((ROOT/CONFIG).read_bytes()),roots

def sources_for_round(cfg,parents,round_no):
    sources={}
    record=parents['chiyuri']['rounds'][round_no-1]
    sources['ba_chiyu']=record['output']['obj']
    record=parents['eight_bosses']['rounds'][round_no-1]
    for stem in cfg['boss_stems'][1:]:
        sources[stem]=record['outputs'][stem+'_obj']
    sources['input_s']=parents['input_scan']['rounds'][round_no-1]['outputs']['obj']
    need(set(sources)==set(cfg['boss_stems']+['input_s']),'ten actual replaced OBJ evidence inputs')
    return sources

def link_response(cfg,round_no):
    rsp=(WORK/'obj/th03/main.@l').read_bytes()
    need(sha(rsp)==cfg['normal_link_response_sha256'] and
         rsp.count(b'obj\\th03\\')>=90,'fixed actual initial original main 99-object source response')
    for stem in cfg['boss_stems']+[cfg['input_stem']]:
        old=f'obj\\th03\\{stem}.obj'.encode()
        new=f'probe\\{STAGE}\\r{round_no}-{stem}.obj'.encode()
        need(rsp.count(old)==1,'one original slot exactly '+stem)
        rsp=rsp.replace(old,new)
    for old,new in [(b'bin\\th03\\main.exe',f'probe\\{STAGE}\\r{round_no}.exe'.encode()),
                    (b'obj\\th03\\main.map',f'probe\\{STAGE}\\r{round_no}.map'.encode())]:
        need(rsp.count(old)==1,'exactly one native MAIN output')
        rsp=rsp.replace(old,new)
    return rsp

def read_pin(pin):
    path=Path(pin['path'])
    need(not path.is_absolute() and '..' not in path.parts,'bounded retained evidence path')
    raw=(ROOT/path).read_bytes()
    need(len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],'raw original source-native OBJ pin '+str(path))
    return raw

def reference(cfg):
    exe=(WORK/'bin/th03/main.exe').read_bytes()
    mapped=(WORK/'obj/th03/main.map').read_bytes()
    target=read_verified_artifact(ROOT,find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-main'))
    x=parse_mz(exe);t=parse_mz(target)
    dif=[i for i,(a,b) in enumerate(zip(x.program_image,t.program_image)) if a!=b]
    need(dif==[0xEC2D] and len(x.program_image)==len(t.program_image)==124642 and
         x.relocations==t.relocations and len(x.relocations)==1553,
         'original cold MAIN source build baseline still has only old input alignment gap')
    return exe,mapped,target

def main_run():
    cfg,cfg_sha,parents=inputs()
    baseline,mapping,target=reference(cfg)
    for n in (1,2):
        sources=sources_for_round(cfg,parents,n)
        for name,pin in sources.items():
            raw=read_pin(pin)
            original=(WORK/f'obj/th03/{name}.obj').read_bytes()
            if name!='input_s':
                need(normalize_dependency_timestamps(raw)==normalize_dependency_timestamps(original),
                     'actual original entire normalized C++ boss object '+name)
            else:
                before=payload(original)
                after=payload(raw)
                need(len(before)==417 and len(after)==418 and
                     all(before[1,i]==after[1,i] for i in range(417)) and
                     after[1,417]==0x90 and len(literal_fields(raw))==42,
                     'original 417 scan instructions, 42 native fields and real EVEN')
    result=dict(complete=False,cold_rebuilt=False,canonical_credit_changed=False,
        whole_japanese_EXE_file_accepted=False,projects_recompiled_now=0,
        source_objects_reused_per_round=10,project_objects_unchanged_per_round=89,
        source_compilations_in_retained_parents=20,code_bosses=9,code_boss_functions=85,
        original_boss_CODE_bytes=17451,input_scan_instruction_bytes=417,native_INPUT_EVEN_bytes=1,
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),config_sha256=cfg_sha,
        parent_sha256={n:v[1] for n,v in cfg['parent_reports'].items()},
        baseline_native_exe_sha256=sha(baseline),baseline_native_map_sha256=sha(mapping),
        original_japanese_target_sha256=sha(target),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(result,indent=2)+'\n')
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
        WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'),
        MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']
    target_mz=parse_mz(target)
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh retained combined MAIN native stage')
        SCRATCH.mkdir()
        (SCRATCH/'driver.py').write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/'config.json').write_bytes((ROOT/CONFIG).read_bytes())
        all_vectors=[]
        for n in (1,2):
            staged_source_objects=sources_for_round(cfg,parents,n)
            retained={}
            for name,pin in staged_source_objects.items():
                raw=read_pin(pin)
                (SCRATCH/f'r{n}-{name}.obj').write_bytes(raw)
                retained[name]=pin
            rsp=link_response(cfg,n)
            (SCRATCH/f'r{n}.@l').write_bytes(rsp)
            p=subprocess.run(dos+['tlink',f'@probe\\{STAGE}\\r{n}.@l'],cwd=WORK,env=env,
                             stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=105)
            log=PREFIX+f'round{n}-normal-TLINK.log'
            (ROOT/log).write_bytes(p.stdout)
            result['phases'].append(dict(round=n,argv=dos+['tlink',f'@probe\\{STAGE}\\r{n}.@l'],
                label=f'round{n}-normal-TLINK',returncode=p.returncode,log=log,
                log_sha256=sha(p.stdout)))
            save()
            need(p.returncode==0,'normal unchanged MAIN TLINK '+str(n)+': '+p.stdout.decode(errors='replace')[-1200:])
            exe=(SCRATCH/f'r{n}.exe').read_bytes()
            mapped=(SCRATCH/f'r{n}.map').read_bytes()
            m=parse_mz(exe)
            need(m.program_image==target_mz.program_image and
                 m.relocations==target_mz.relocations and len(m.relocations)==1553,
                 'whole exact Japanese program and all ordered MZ fixups in combined 10 object native link')
            input_map=read_pin(parents['input_scan']['rounds'][n-1]['outputs']['map'])
            need(mapped==input_map,'same original MAP geometry and natural EVEN allocation')
            outputs={}
            for k,v in [('exe',exe),('map',mapped)]:
                path=PREFIX+f'round{n}-{k}.bin'
                (ROOT/path).write_bytes(v)
                outputs[k]=dict(path=path,bytes=len(v),sha256=sha(v))
            result['rounds'].append(dict(round=n,reused_source_objects=retained,
                normal_link_response_sha256=sha(rsp),outputs=outputs,
                complete_original_program_image_equal=True,
                ordered_1553_original_mz_relocations_equal=True))
            save()
            all_vectors.append((exe,mapped))
            print(f'Combined MAIN round {n}: 9 bosses/85 functions and natural input/EVEN, original 124642 program bytes, 1553 relocations',flush=True)
        need(all_vectors[0]==all_vectors[1],'both whole MAIN exe/map outputs repeat')
    result['complete']=True
    save()

if __name__=='__main__':
    main_run()
