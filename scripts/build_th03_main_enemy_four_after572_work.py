#!/usr/bin/env python3
"""Source-compile large enemy script/formation and update/hittest producers.

Four tiny maintained C++ wrappers share one natural enemy.cpp source rather
than four flattened, copied 1000-line TUs. Real TC4 emits complete original
CODE/OMF relocation sites and two TLINK rounds replace only the four enemy
slots within the after567 ten-object source-native MAIN. A separate native
DOS-MZ format serializer is checked without copying target bytes.
"""
import fcntl
import json
import os
import subprocess
from pathlib import Path

import build_th03_main_combined_after567_work as parent
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.omf import normalize_dependency_timestamps
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.main_mz_compact import compact_mz

ROOT=parent.ROOT
WORK=parent.WORK
DRIVER='scripts/build_th03_main_enemy_four_after572_work.py'
CONFIG='config/main_work/enemy_four_after572.json'
PREFIX='.analysis/work/main-enemy-four-after572-native-'
REPORT=PREFIX+'build.json'
STAGE='af572e'
SCRATCH=WORK/('probe/'+STAGE)
ORDER=('eforna','efornb','eupda','eupdb')

def inputs():
    c=json.loads((ROOT/CONFIG).read_text())
    expected=[('eforna',1,'TH03_ENEMY_FORMATIONS_ONLY',729,8,58),
              ('efornb',2,'TH03_ENEMY_FORMATIONS_ONLY',1064,4,37),
              ('eupda',1,'TH03_ENEMY_UPDATE_ONLY',372,3,24),
              ('eupdb',2,'TH03_ENEMY_UPDATE_ONLY',1160,4,103)]
    need(c['schema']=='th03-main-enemy-four-native-after572-v1' and
         c['parent_report']==parent.REPORT and
         c['original_source']=='src/main/enemy/enemy.cpp' and
         [(u['stem'],u['partition'],u['phase'],u['CODE_bytes'],
           u['publics'],u['fixups']) for u in c['units']]==expected and
         all(u['wrapper']==f'src/main/enemy/producers/{u["stem"]}.cpp' for u in c['units']) and
         (c['total_CODE_allocation_bytes'],c['complete_public_functions'],
          c['total_original_ordered_fixups'],c['original_TARGET_MAIN_file_bytes'],
          c['original_main_relocations'])==(3325,19,222,130882,1553) and
         c['historical_original_OMF_packet_identity_proved'] is False and
         c['whole_product_source_acceptance_changed'] is False and
         c['canonical_factory_credit_changed'] is False,
         'four bounded original real enemy producer code partitions')
    p=json.loads((ROOT/c['parent_report']).read_text())
    need(p['complete'] and len(p['rounds'])==2 and
         sha((ROOT/c['parent_report']).read_bytes())==c['parent_report_sha256'],
         'genuine unchanged ten-source-object original MAIN native links')
    return c,sha((ROOT/CONFIG).read_bytes()),p

def source_inputs(c):
    common=(ROOT/c['original_source']).read_bytes()
    need(common and b'\r' not in common and
         b'bool near enemy_run(void)' in common and
         b'void near enemy_hittest(void)' in common and
         b'uint8_t prev;' in common and
         (WORK/c['original_source']).read_bytes().replace(b'\r\n',b'\n')==common,
         'true original large C++ maintained source and preserved unchecked behavior')
    wrapper={}
    for u in c['units']:
        raw=(ROOT/u['wrapper']).read_bytes()
        want=(f'(#define TH03_ENEMY_PRODUCER_PART {u["partition"]}\n'
              f'#define {u["phase"]} 1\n'
              '#include "src/main/enemy/enemy.cpp"\n').encode()
        need(raw.endswith(want[1:]) and b'codestring' not in raw.lower() and
             raw.count(b'#include "src/main/enemy/enemy.cpp"')==1,
             'one natural C++ shared producer, two correct compile-time partitions')
        wrapper[u['stem']]=raw
    return common,wrapper

def original_object_scope(candidate,reference,u):
    need(payload(candidate)==payload(reference) and len(payload(candidate))==u['CODE_bytes'] and
         literal_fields(candidate)==literal_fields(reference) and
         len(literal_fields(candidate))==u['fixups'] and
         public_offsets(candidate)==public_offsets(reference) and
         len(public_offsets(candidate))==u['publics'] and
         segment_definitions(candidate)==segment_definitions(reference),
         'full original 16-bit TC4 source CODE, all ordered OMF FIXUPP fields, PUBLICs and segments '+u['stem'])
    return dict(original_CODE_allocation=u['CODE_bytes'],
        complete_original_public_functions=u['publics'],
        original_ordered_native_fixups=u['fixups'],
        original_initialized_CODE_equal=True,
        original_native_fixup_order_equal=True,
        original_publics_and_segments_equal=True,
        original_complete_OMF_packet_equal=False)

def response(n):
    rsp=parent.link_response(parent.inputs()[0],n)
    for stem in ORDER:
        old=f'obj\\th03\\{stem}.obj'.encode()
        new=f'probe\\{STAGE}\\r{n}\\{stem}.obj'.encode()
        need(rsp.count(old)==1,'one original native enemy producer linker slot '+stem)
        rsp=rsp.replace(old,new)
    for old,new in [(f'probe\\af567c\\r{n}.exe',f'probe\\{STAGE}\\r{n}.exe'),
                    (f'probe\\af567c\\r{n}.map',f'probe\\{STAGE}\\r{n}.map')]:
        need(rsp.count(old.encode())==1,'normal source-native MAIN output slot')
        rsp=rsp.replace(old.encode(),new.encode())
    return rsp

def normalize_map(raw,n):
    for stem in ORDER:
        before=f'M=probe/{STAGE}/r{n}/{stem}.cpp'.encode()
        after=f'M=th03/{stem}.cpp'.encode()
        need(raw.count(before)>=3,'all native CODE/DATA/BSS contributions retained for '+stem)
        raw=raw.replace(before,after)
    return raw

def main():
    cfg,cfg_sha,parent_report=inputs()
    common,wrappers=source_inputs(cfg)
    originals={u['stem']:(WORK/f'obj/th03/{u["stem"]}.obj').read_bytes() for u in cfg['units']}
    _,_,target=parent.reference(cfg)  # actual original MAIN source graph/target
    target_mz=parse_mz(target)
    baseline=(WORK/'bin/th03/main.exe').read_bytes()
    need(len(target)==130882 and len(target_mz.relocations)==1553 and
         compact_mz(parent.read_pin(parent_report['rounds'][0]['outputs']['exe']))==target,
         'original encoded target already source-backed by previous complete MAIN link and MZ stage')
    report=dict(complete=False,cold_rebuilt=False,source_game_objects_recompiled_per_round=4,
        original_unmodified_other_objects=95,compiler_runtime_rebuilt=False,
        canonical_credit_changed=False,whole_product_source_accepted=False,
        complete_CODE_allocation_bytes=3325,public_functions=19,ordered_native_fixups=222,
        common_source_sha256=sha(common),
        source_wrapper_sha256={k:sha(v) for k,v in wrappers.items()},
        original_object_sha256={k:sha(v) for k,v in originals.items()},
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        config_sha256=cfg_sha,parent_report_sha256=cfg['parent_report_sha256'],
        original_japanese_target_sha256=sha(target),
        original_native_baseline_SHA256=sha(baseline),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
        WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'),
        MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']
    def run(argv,label):
        done=subprocess.run(argv,cwd=WORK,env=env,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,timeout=105)
        log=PREFIX+label+'.log'
        (ROOT/log).write_bytes(done.stdout)
        report['phases'].append(dict(label=label,argv=argv,returncode=done.returncode,
            log=log,log_sha256=sha(done.stdout)))
        save()
        need(done.returncode==0,label+': '+done.stdout.decode(errors='replace')[-1200:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh entire retained shared-C++ enemy native stage')
        SCRATCH.mkdir()
        (SCRATCH/'driver.py').write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/'config.json').write_bytes((ROOT/CONFIG).read_bytes())
        vectors=[]
        for n in (1,2):
            loc=SCRATCH/f'r{n}'
            loc.mkdir()
            for s,raw in wrappers.items():
                path=loc/f'{s}.cpp'
                path.write_bytes(raw.replace(b'\n',b'\r\n'))
                os.utime(path,(946684800,946684800))
            scopes={}
            products={}
            for u in cfg['units']:
                stem=u['stem']
                cmd=dos+['tcc','-c','-I.','-O','-b-','-3','-Z','-d','-DGAME=3',
                     '-ml',"-DBINARY='M'",f'-nprobe/{STAGE}/r{n}/',
                     f'probe/{STAGE}/r{n}/{stem}.cpp']
                run(cmd,f'round{n}-{stem}-TC4-compile')
                obj=(loc/f'{stem}.obj').read_bytes()
                scopes[stem]=original_object_scope(obj,originals[stem],u)
                products[stem+'_obj']=obj
            rsp=response(n)
            (SCRATCH/f'r{n}.@l').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{n}.@l'],
                f'round{n}-normal-TLINK')
            native=(SCRATCH/f'r{n}.exe').read_bytes()
            map_raw=(SCRATCH/f'r{n}.map').read_bytes()
            old=parent.read_pin(parent_report['rounds'][n-1]['outputs']['exe'])
            oldmap=parent.read_pin(parent_report['rounds'][n-1]['outputs']['map'])
            need(native==old and normalize_map(map_raw,n)==oldmap and
                 parse_mz(native).program_image==target_mz.program_image and
                 parse_mz(native).relocations==target_mz.relocations,
                 'whole native MAIN source EXE unchanged and all 1553 original ordered MZ relocations')
            compacted=compact_mz(native)
            need(compacted==target and len(compacted)==130882,
                 'complete exact original Japanese MAIN file from unchanged independently source-generated CODE')
            products.update(exe=native,map=map_raw,compact_mz=compacted)
            outputs={}
            for key,raw in products.items():
                path=PREFIX+f'round{n}-{key}.bin'
                (ROOT/path).write_bytes(raw)
                outputs[key]=dict(path=path,bytes=len(raw),sha256=sha(raw))
            report['rounds'].append(dict(round=n,outputs=outputs,objects_scope=scopes,
                response_sha256=sha(rsp),whole_native_MAIN_EXE_equal=True,
                complete_original_japanese_file_equal_after_MZ_format_conversion=True))
            save()
            vectors.append(products)
            print('Enemy shared C++ round',n,'4 objects /3325 original CODE /19 functions, whole MAIN and compact original exact',flush=True)
        need(vectors[0]['exe']==vectors[1]['exe'] and
             normalize_map(vectors[0]['map'],1)==normalize_map(vectors[1]['map'],2) and
             vectors[0]['compact_mz']==vectors[1]['compact_mz'] and
             all(payload(vectors[0][s+'_obj'])==payload(vectors[1][s+'_obj']) for s in ORDER) and
             source_inputs(cfg)==(common,wrappers),
             'two real source-produced group/whole output vectors repeat without product code drift')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
