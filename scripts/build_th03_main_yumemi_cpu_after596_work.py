#!/usr/bin/env python3
"""Compile full original round-results/shot/HUD animation C++ concurrently in MAIN.

Only the 3 affected original source TUs are rebuilt in two independent
original TC4.02 rounds; remaining native source-backed 96 project objects
and C0/CRT library are SHA-pinned and reused. TLINK/MZ comparison is
whole-product, and natural wrappers do not patch code or targets.
"""
import fcntl
import json
import os
import subprocess

import build_th03_main_round_hud_after595_work as parent
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact

ROOT=parent.ROOT
WORK=parent.WORK
DRIVER='scripts/build_th03_main_yumemi_cpu_after596_work.py'
CONFIG='config/main_work/yumemi_cpu_after596.json'
PREFIX='.analysis/work/main-yumemi-cpu-after596-native-'
REPORT=PREFIX+'build.json'
STAGE='af596y'
SCRATCH=WORK/('probe/'+STAGE)
ORDER=('ex_yume','cs_yume','p_cpu')

def inputs():
    cfg=json.loads((ROOT/CONFIG).read_text())
    expected=[
       ('ex_yume','src/main/player/exatt_yumemi.cpp',
        'src/main/player/producers/yumemi_exatt_native.cpp',1696,5,87,'MAIN_06_TEXT','th03/ex_yume.cpp'),
       ('cs_yume','src/main/player/chargeshot_yumemi.cpp',
        'src/main/player/producers/yumemi_chargeshot_native.cpp',1645,10,133,'PELLET_PUT','th03/cs_yume.cpp'),
       ('p_cpu','src/main/player/cpu.cpp',
        'src/main/player/producers/cpu_native.cpp',1077,4,64,'PLAYER_M_TEXT','th03/p_cpu.cpp')]
    need(cfg['schema']=='th03-main-yumemi-cpu-after596-native-v1' and
         cfg['parent_report']==parent.REPORT and
         [(u['stem'],u['source'],u['wrapper'],u['CODE_bytes'],
           u['PUBLICs'],u['ordered_fixups'],u['CODE_segment'],u['original_MAP_module'])
          for u in cfg['units']]==expected and
         (cfg['first_use_GAME'],cfg['first_use_BINARY'])==(3,'M') and
         (cfg['original_total_CODE_bytes'],cfg['original_total_public_functions'],
          cfg['original_ordered_fixups'],cfg['original_main_relocations'],
          cfg['original_full_japanese_file_bytes'])==(4418,19,284,1553,130882) and
         cfg['historic_raw_vendor_OMF_packet_identity'] is False and
         cfg['canonical_factory_credit_changed'] is False and
         cfg['whole_project_source_accepted'] is False,
         'all three original Yumemi/CPU complete source compiler units')
    prior=json.loads((ROOT/cfg['parent_report']).read_text())
    need(prior['complete'] and len(prior['rounds'])==2 and
         cfg['parent_report_sha256']==sha((ROOT/cfg['parent_report']).read_bytes()),
         'two actual original after595 results/HUD/shot and nine BOSS parent links')
    return cfg,sha((ROOT/CONFIG).read_bytes()),prior

def sources(c):
    items={}
    for u in c['units']:
        raw=(ROOT/u['source']).read_bytes()
        wrapper=(ROOT/u['wrapper']).read_bytes()
        needle=f'#include "{u["source"]}"\n'.encode()
        need(raw and b'\r' not in raw and b'\r' not in wrapper and
             wrapper.count(needle.strip())==1 and wrapper.endswith(needle) and
             (WORK/u['source']).read_bytes().replace(b'\r\n',b'\n')==raw and
             b'codestring' not in wrapper.lower(),
             'real unchanged original GAME3 natural C++ producer '+u['stem'])
        items[u['stem']]=dict(body=raw,wrapper=wrapper)
    return items

def object_scope(obj,orig,u):
    native=payload(obj)
    reference=payload(orig)
    pubs=public_offsets(obj)
    segs=segment_definitions(obj)
    need(native==reference and len(native)==u['CODE_bytes'] and
         all(s==4 for s,o in native) and
         len(literal_fields(obj))==u['ordered_fixups'] and
         literal_fields(obj)==literal_fields(orig) and
         pubs==public_offsets(orig) and len(pubs)==u['PUBLICs'] and
         all(info['segment_index']==4 for info in pubs.values()) and
         segs==segment_definitions(orig) and
         segs[3]['name']==u['CODE_segment'] and
         segs[3]['size']==u['CODE_bytes'],
         'whole exact original C++ CODE, all ordered 16-bit fixups and segment/PUBLIC '+u['stem'])
    return dict(CODE_bytes=u['CODE_bytes'],original_publics=u['PUBLICs'],
        ordered_native_FIXUPPs=u['ordered_fixups'],original_CODE_segment=u['CODE_segment'],
        complete_original_CODE_and_native_fields_equal=True,
        raw_vendor_OMF_packets_identical=False)

def response(n):
    raw=parent.response(n)
    for stem in ORDER:
        old=f'obj\\th03\\{stem}.obj'.encode()
        new=f'probe\\{STAGE}\\r{n}\\{stem}.obj'.encode()
        need(raw.count(old)==1,'single original native source slot '+stem)
        raw=raw.replace(old,new)
    for before,after in [(f'probe\\{parent.STAGE}\\r{n}.exe',
                          f'probe\\{STAGE}\\r{n}.exe'),
                         (f'probe\\{parent.STAGE}\\r{n}.map',
                          f'probe\\{STAGE}\\r{n}.map')]:
        need(raw.count(before.encode())==1,'single original native full output slot')
        raw=raw.replace(before.encode(),after.encode())
    return raw

def map_normalize(raw,n):
    cfg,_,_=inputs()
    for u in cfg['units']:
        stem=u['stem']
        old=f'M=probe/{STAGE}/r{n}/{stem}.cpp'.encode()
        replacement=f"M={u['original_MAP_module']}".encode()
        need(raw.count(old)==4,'original CODE/DATA/BSS/empty segment native MAP rows '+stem)
        raw=raw.replace(old,replacement)
    return raw

def read_pin(pin):
    return parent.read_pin(pin)

def main():
    cfg,cfg_sha,prior=inputs()
    maintained=sources(cfg)
    original={s:(WORK/f'obj/th03/{s}.obj').read_bytes() for s in ORDER}
    target=read_verified_artifact(ROOT,find_artifact(load_target_manifest(
        ROOT/'config/targets.toml'),'th03-main'))
    ref=parse_mz(target)
    need(len(target)==130882 and len(ref.program_image)==124642 and
         len(ref.relocations)==1553,
         'original candidate-local-attested Japanese MAIN exact file')
    report=dict(complete=False,cold_rebuilt=False,library_rebuilt=False,
        native_project_objects_recompiled_per_round=3,
        original_other_project_objects_reused=96,
        native_source_CODE_bytes=4418,original_PUBLIC_functions=19,
        original_native_FIXUPP_fields=284,
        canonical_factory_credit_changed=False,whole_project_source_accepted=False,
        parent_report_sha256=cfg['parent_report_sha256'],
        config_sha256=cfg_sha,driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        sources_sha256={stem:{k:sha(v) for k,v in entry.items()}
                        for stem,entry in maintained.items()},
        original_object_sha256={stem:sha(raw) for stem,raw in original.items()},
        original_japanese_MAIN_sha256=sha(target),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
        WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'),
        MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']
    def run(args,label):
        p=subprocess.run(args,cwd=WORK,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=110)
        log=PREFIX+label+'.log'
        (ROOT/log).write_bytes(p.stdout)
        report['phases'].append(dict(label=label,argv=args,returncode=p.returncode,
                                    log=log,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1200:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh real three Yumemi/CPU C++ native source stage')
        SCRATCH.mkdir()
        (SCRATCH/'driver.py').write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/'config.json').write_bytes((ROOT/CONFIG).read_bytes())
        pair=[]
        for n in (1,2):
            folder=SCRATCH/f'r{n}'
            folder.mkdir()
            objs={}
            scopes={}
            for u in cfg['units']:
                stem=u['stem']
                file=folder/f'{stem}.cpp'
                file.write_bytes(maintained[stem]['wrapper'].replace(b'\n',b'\r\n'))
                os.utime(file,(946684800,946684800))
                run(dos+['tcc','-c','-I.','-O','-b-','-3','-Z','-d',
                         '-DGAME=3','-ml',"-DBINARY='M'",
                         f'-nprobe/{STAGE}/r{n}/',
                         f'probe/{STAGE}/r{n}/{stem}.cpp'],
                    f'round{n}-{stem}-TC4-compile')
                obj=(folder/f'{stem}.obj').read_bytes()
                scopes[stem]=object_scope(obj,original[stem],u)
                objs[stem+'_obj']=obj
            rsp=response(n)
            (SCRATCH/f'r{n}.@l').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{n}.@l'],
                f'round{n}-normal-TLINK')
            exe=(SCRATCH/f'r{n}.exe').read_bytes()
            map_data=(SCRATCH/f'r{n}.map').read_bytes()
            prev=prior['rounds'][n-1]['outputs']
            need(exe==read_pin(prev['exe']) and
                 map_normalize(map_data,n)==read_pin(prev['map']) and
                 parse_mz(exe).program_image==ref.program_image and
                 parse_mz(exe).relocations==ref.relocations,
                 'entire source-native original MAIN EXE/MAP/image/1553 ordered relocations')
            packed=compact_mz(exe)
            need(packed==target,'entire original Japanese MAIN.EXE after independent standard MZ serialization')
            vector={**objs,'exe':exe,'map':map_data,'compact_mz':packed}
            outputs={}
            for key,data in vector.items():
                file=PREFIX+f'round{n}-{key}.bin'
                (ROOT/file).write_bytes(data)
                outputs[key]=dict(path=file,bytes=len(data),sha256=sha(data))
            report['rounds'].append(dict(round=n,outputs=outputs,scopes=scopes,
                 actual_link_response_sha256=sha(rsp),
                 whole_original_source_derived_MZ_equal=True))
            save()
            pair.append(vector)
            print('Yumemi Extra Attack / Charged Shot / CPU native',n,'4418 original CODE /19 PUBLIC /284 fixups, full Japanese original MAIN exact',flush=True)
        need(pair[0]['exe']==pair[1]['exe'] and
             pair[0]['compact_mz']==pair[1]['compact_mz'] and
             all(payload(pair[0][s+'_obj'])==payload(pair[1][s+'_obj']) and
                 literal_fields(pair[0][s+'_obj'])==literal_fields(pair[1][s+'_obj'])
                 for s in ORDER) and
             sources(cfg)==maintained,
             'two independent complete C++/original native MAIN output vectors repeat')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
