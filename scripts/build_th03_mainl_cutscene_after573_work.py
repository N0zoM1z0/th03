#!/usr/bin/env python3
"""Compile the 3195-byte natural MAINL cutscene C++ from maintained source twice.

One original first-use GAME=3/BINARY=L original object is replaced in the
after570 link which already sources the natural input scanner, registration
data, original root/picture/text, and four native sound TASM EVEN functions.
Never rebuild the 36-object cold chain.
"""
import fcntl
import json
import os
import subprocess

import build_th03_mainl_sound_natural_after570_work as prior
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.pc98 import parse_mz
from stage_th03_mainl_cutscene import read_inputs as read_cutscene_inputs

ROOT=prior.ROOT
WORK=prior.WORK
base=prior.base
DRIVER='scripts/build_th03_mainl_cutscene_after573_work.py'
CONFIG='config/mainl_work/cutscene_after573.json'
PREFIX='.analysis/work/mainl-cutscene-after573-native-'
REPORT=PREFIX+'build.json'
STAGE='af573c'
SCRATCH=WORK/('probe/'+STAGE)

def inputs():
    c,h=base.load(CONFIG)
    need(c['schema']=='th03-mainl-cutscene-after573-v1' and
         c['parent_report']==prior.REPORT and
         c['source_wrapper']=='src/mainl/cutscene/producer.cpp' and
         c['large_natural_CPP_source']=='src/mainl/cutscene.cpp' and
         c['original_object']=='obj/th03/cutscene.obj' and
         (c['CUTSCENE_CODE_bytes'],c['original_near_PUBLIC_procedures'],
          c['original_ordered_OMF_fixups'],
          c['original_ordered_MZ_relocations_within_scope'],
          c['original_decoded_MAINL_EXE_bytes'])==(3195,13,236,56,67372) and
         c['whole_product_source_accepted'] is False and
         c['canonical_credit_changed'] is False,
         'bounded existing complete 13-procedure cutscene C++ producer')
    return c,h

def sources(c):
    wrapper=(ROOT/c['source_wrapper']).read_bytes()
    original=(ROOT/c['large_natural_CPP_source']).read_bytes()
    need(wrapper.endswith(b'#include "src/mainl/cutscene.cpp"\n') and
         wrapper.count(b'#include "src/mainl/cutscene.cpp"')==1 and
         b'-a2' not in wrapper and
         b'void near cutscene_animate(void)' in original and
         b'bool16 pascal near cutscene_script_load' in original,
         'same complete natural C++ script/UI implementation, no manual codec or command injection')
    dependencies=read_cutscene_inputs(ROOT)
    need(dependencies[c['large_natural_CPP_source']]==original and
         all((WORK/name).read_bytes().replace(b'\r\n',b'\n')==raw
             for name,raw in dependencies.items()),
         'live maintained source/headers identical to original scoped frozen compiler inputs')
    return wrapper,dependencies

def response(number):
    rsp=prior.response(number)
    for before,after in [(rb'obj\th03\cutscene.obj',f'probe\\{STAGE}\\r{number}\\cutscene.obj'.encode()),
                         (f'probe\\af570n\\r{number}.exe'.encode(),f'probe\\{STAGE}\\r{number}.exe'.encode()),
                         (f'probe\\af570n\\r{number}.map'.encode(),f'probe\\{STAGE}\\r{number}.map'.encode())]:
        need(rsp.count(before)==1,'single original cutscene object/normal first-use MAINL output')
        rsp=rsp.replace(before,after)
    return rsp

def normalize_map(raw,number):
    before=f'M=probe/{STAGE}/r{number}/cutscene.cpp'.encode()
    need(raw.count(before)==3,'all original CODE, DATA, BSS contributions')
    return raw.replace(before,b'M=th03/cutscene.cpp')

def scope(new,original,c):
    need(payload(new)==payload(original) and len(payload(new))==c['CUTSCENE_CODE_bytes'] and
         literal_fields(new)==literal_fields(original) and
         len(literal_fields(new))==c['original_ordered_OMF_fixups'] and
         public_offsets(new)==public_offsets(original) and
         len(public_offsets(new))==c['original_near_PUBLIC_procedures'] and
         segment_definitions(new)==segment_definitions(original),
         'entire 3195 original initialized cutscene CODE, 236 ordered fields/13 PUBLICs/segments')
    return dict(complete_original_CUTSCENE_CODE_bytes=c['CUTSCENE_CODE_bytes'])

def main():
    c,cfg_sha=inputs()
    before,previous_sha=base.load(prior.REPORT)
    need(before['complete'] and previous_sha==c['parent_report_sha256'],
         'real independent after570 natural sound/root/input original MAINL link')
    wrapper,dep=sources(c)
    original=(WORK/c['original_object']).read_bytes()
    report=dict(complete=False,cold_rebuilt=False,library_rebuilt=False,
        game_objects_recompiled_per_round=1,other_game_objects_reused=35,
        canonical_credit_changed=False,whole_product_source_accepted=False,
        CUTSCENE_CODE_bytes=3195,source_near_procedures=13,original_literal_fixups=236,
        parent_report_sha256=previous_sha,
        wrapper_sha256=sha(wrapper),dependencies_sha256={k:sha(v) for k,v in dep.items()},
        original_object_sha256=sha(original),driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        config_sha256=cfg_sha,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
        WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'),MSDOS_PATH=r'C:\TC4\BIN',
        TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']
    def run(argv,label):
        result=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,timeout=105)
        log=PREFIX+label+'.log'
        (ROOT/log).write_bytes(result.stdout)
        report['phases'].append(dict(label=label,argv=argv,returncode=result.returncode,
            log=log,log_sha256=sha(result.stdout)))
        save()
        need(result.returncode==0,label+': '+result.stdout.decode(errors='replace')[-1200:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh complete C++ cutscene source-native stage')
        SCRATCH.mkdir()
        (SCRATCH/'driver.py').write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/'config.json').write_bytes((ROOT/CONFIG).read_bytes())
        pair=[]
        for n in (1,2):
            folder=SCRATCH/f'r{n}'
            folder.mkdir()
            (folder/'cutscene.cpp').write_bytes(wrapper.replace(b'\n',b'\r\n'))
            os.utime(folder/'cutscene.cpp',(946684800,946684800))
            command=dos+['tcc','-c','-I.','-O','-b-','-3','-Z','-d','-DGAME=3','-ml',
                         "-DBINARY='L'",f'-nprobe/{STAGE}/r{n}/',
                         f'probe/{STAGE}/r{n}/cutscene.cpp']
            run(command,f'round{n}-cutscene-TC4-compile')
            obj=(folder/'cutscene.obj').read_bytes()
            scope(obj,original,c)
            rsp=response(n)
            (SCRATCH/f'r{n}.lnk').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{n}.lnk'],f'round{n}-normal-TLINK')
            v=dict(obj=obj,exe=(SCRATCH/f'r{n}.exe').read_bytes(),
                   map=(SCRATCH/f'r{n}.map').read_bytes())
            old=before['rounds'][n-1]['outputs']
            image=parse_mz(v['exe'])
            need(v['exe']==base.checked(old['exe']) and
                 normalize_map(v['map'],n)==base.checked(old['map']) and
                 len(v['exe'])==67372 and len(image.relocations)==677,
                 'complete original Japanese MAINL EXE/ordered MZ relocations and all MAP coordinates')
            outputs={}
            for k,raw in v.items():
                path=PREFIX+f'round{n}-{k}.bin'
                (ROOT/path).write_bytes(raw)
                outputs[k]=dict(path=path,bytes=len(raw),sha256=sha(raw))
            report['rounds'].append(dict(round=n,outputs=outputs,
                response_sha256=sha(rsp),
                complete_original_cutscene_native_object_equal=True,
                full_Japanese_MAINL_EXE_equal=True,original_677_relocations_equal=True))
            save()
            pair.append(v)
            print('Cutscene C++ round',n,'complete 3195 CODE /13 functions/236 native fixups; full original MAINL EXE exact',flush=True)
        need(pair[0]['exe']==pair[1]['exe'] and
             normalize_map(pair[0]['map'],1)==normalize_map(pair[1]['map'],2) and
             payload(pair[0]['obj'])==payload(pair[1]['obj']) and
             sources(c)==(wrapper,dep),
             'two complete native compiler/linker source and binary vectors repeat')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
