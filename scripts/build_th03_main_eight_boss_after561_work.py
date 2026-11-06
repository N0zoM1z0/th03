#!/usr/bin/env python3
"""Two rounds: compile eight full MAIN boss C++ modules, link normal MAIN once per round.

Independent source/archive and compiler input per boss, no full cold replay.
The old Marisa probe is deliberately kept unchanged because OP/MAINL/ZUN
publication hashes bind it; a separate corrected native probe is used here.
"""
import fcntl
import importlib
import json
import os
import sys
import subprocess

import build_th03_main_boss_chiyuri_after559_work as parent
from build_th03_mainl_resources_work import need,sha
from lib.omf import normalize_dependency_timestamps
from lib.pc98 import parse_mz

ROOT=parent.ROOT
WORK=parent.WORK
DRIVER='scripts/build_th03_main_eight_boss_after561_work.py'
CONFIG='config/main_work/eight_boss_after561.json'
PREFIX='.analysis/work/main-eight-boss-after561-native-'
REPORT=PREFIX+'build.json'
STAGE='af561b'
SCRATCH=WORK/('probe/'+STAGE)

def inputs():
    cfg=json.loads((ROOT/CONFIG).read_text())
    required=[
        ('yumemi','ba_yumem',2358,10,80),('kana','ba_kana',1874,9,80),
        ('mima','ba_mima',1922,9,81),('reimu','ba_reimu',2020,9,72),
        ('kotohime','ba_koto',1840,11,80),('ellen','ba_ellen',1675,9,81),
        ('rikako','ba_rikak',1677,8,81),('marisa','ba_maris',1431,9,81)]
    need(cfg['schema']=='th03-main-eight-boss-after561-v1' and
         cfg['parent_report']==parent.REPORT and
         [(x['name'],x['object'],x['CODE_bytes'],x['functions'],x['switch_bytes'])
          for x in cfg['bosses']]==required and
         (cfg['total_CODE_bytes'],cfg['total_functions'],cfg['total_switch_bytes'])==(14797,74,636) and
         cfg['historical_pinned_marisa_probe_preserved'] is True and
         cfg['whole_original_MAIN_exe_accepted'] is False and
         cfg['canonical_credit_changed'] is False,
         'actual eight large native first-use boss producers')
    return cfg,sha((ROOT/CONFIG).read_bytes())

def probe_module(boss):
    name=boss['name']
    script=('probe_th03_main_boss_marisa_native_corrected'
            if name=='marisa' else 'probe_th03_main_boss_'+name+'_cpp')
    return importlib.import_module(script), 'scripts/'+script+'.py'

def response(cfg,round_no):
    rsp=(WORK/'obj/th03/main.@l').read_bytes()
    need(sha(rsp)==cfg['normal_link_response_sha256'],'unchanged MAIN normal link')
    for boss in cfg['bosses']:
        name=boss['object']
        old=('obj\\th03\\'+name+'.obj').encode()
        new=(f'probe\\{STAGE}\\r{round_no}-{name}.obj').encode()
        need(rsp.count(old)==1,'unique actual source-MAIN object slot '+name)
        rsp=rsp.replace(old,new)
    for old,new in [('bin\\th03\\main.exe',f'probe\\{STAGE}\\r{round_no}.exe'),
                    ('obj\\th03\\main.map',f'probe\\{STAGE}\\r{round_no}.map')]:
        need(rsp.count(old.encode())==1,'exactly one original native output '+old)
        rsp=rsp.replace(old.encode(),new.encode())
    return rsp

def native_parents(cfg):
    prior=json.loads((ROOT/cfg['parent_report']).read_text())
    need(prior['complete'] and sha((ROOT/cfg['parent_report']).read_bytes())==
         cfg['parent_report_sha256'],'after559 large Chiyuri native source checkpoint')
    ccfg,_=parent.inputs()
    original_chiyuri,exe,map_raw,target=parent.verify_reference(ccfg)
    need(sha(exe)==cfg['existing_native_MAIN_exe_sha256'] and
         sha(map_raw)==cfg['existing_native_MAIN_map_sha256'],
         'actual unchanged selected MAIN source-native link')
    original_link=parse_mz(exe)
    target_image=parse_mz(target)
    need(original_link.relocations==target_image.relocations and
         len(original_link.relocations)==1553 and
         [i for i,(a,b) in enumerate(zip(original_link.program_image,target_image.program_image))
          if a!=b]==[0xEC2D],'original unchanged MAIN target-relative 1-byte difference')
    orig_objs={u['object']:(WORK/'obj/th03'/(u['object']+'.obj')).read_bytes()
               for u in cfg['bosses']}
    return exe,map_raw,target,orig_objs

def main():
    cfg,cfg_sha=inputs()
    exe,map_raw,target,orig_objs=native_parents(cfg)
    source_bindings={}
    for boss in cfg['bosses']:
        module,script=probe_module(boss)
        need(module.OBJECT.name==boss['object']+'.obj' and
             module.TARGET_SIZE==boss['CODE_bytes'] and
             len(module.FUNCTIONS)==boss['functions'] and
             module.TARGET_TABLE_END-module.TARGET_TABLE_START==boss['switch_bytes'],
             'original finite complete boss source/target bounds '+boss['name'])
        text=(ROOT/script).read_bytes()
        need(b'-a2 -nobj/th03/' not in text and
             b'-nobj/th03/' in text,'original first-use native compiler flags '+boss['name'])
        source_bindings[script]=sha(text)
        source_bindings[str(module.SOURCE.relative_to(ROOT))]=sha(module.SOURCE.read_bytes())
    need('scripts/probe_th03_main_boss_marisa_cpp.py' not in source_bindings,
         'old acceptance-bound Marisa probe remains entirely untouched')
    record=dict(complete=False,source_ownership_closure=False,canonical_credit_changed=False,
        full_original_MAIN_accepted=False,cold_rebuilt=False,CRT_rebuilt=False,
        source_game_objects_recompiled_per_round=8,other_game_objects_reused=91,
        complete_functions=74,complete_CODE_bytes=14797,compiler_switch_bytes=636,
        parent_sha256=cfg['parent_report_sha256'],config_sha256=cfg_sha,
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),source_sha256=source_bindings,
        initial_original_object_sha256={name:sha(raw) for name,raw in orig_objs.items()},
        native_exe_sha256=sha(exe),native_map_sha256=sha(map_raw),
        original_japanese_target_sha256=sha(target),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(record,indent=2)+'\n')
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
        WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'),
        MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']
    def run(argv,cwd,label,limit):
        p=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=limit)
        log=PREFIX+label+'.log'
        (ROOT/log).write_bytes(p.stdout)
        record['phases'].append(dict(label=label,argv=argv,log=log,
            log_sha256=sha(p.stdout),returncode=p.returncode))
        save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1500:])

    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh source-native eight-boss stage')
        SCRATCH.mkdir()
        (SCRATCH/'driver.py').write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/'config.json').write_bytes((ROOT/CONFIG).read_bytes())
        all_vectors=[]
        for number in (1,2):
            outputs={}
            receipts={}
            for boss in cfg['bosses']:
                name=boss['name'];stem=boss['object']
                module,script=probe_module(boss)
                proof_id=f'gptweb-561-{name}-r{number}'
                proof_root=ROOT/('.analysis/th03-main-boss-'+name+'-cpp/'+proof_id)
                need(not proof_root.exists(),'new independent boss source materialization '+proof_id)
                run([sys.executable,str(ROOT/script),'--run-id',proof_id],ROOT,
                    f'round{number}-{name}-TC4-compile',130)
                receipt_path=proof_root/'receipt.json'
                receipt=json.loads(receipt_path.read_text())
                candidate=(proof_root/'source/obj/th03'/(stem+'.obj')).read_bytes()
                need(receipt['source_acceptance'] and receipt['exact_acceptance'] is False and
                     receipt['object']['sha256']==sha(candidate) and
                     receipt['object']['code_size']==boss['CODE_bytes'] and
                     receipt['comparison']['candidate_size']==boss['CODE_bytes'] and
                     len(receipt['object']['code_publics'])==boss['functions'] and
                     receipt['comparison']['candidate_table_span']==[
                         module.TARGET_TABLE_START,module.TARGET_TABLE_END] and
                     not receipt['comparison']['function_differences'] and
                     receipt['comparison']['table_semantics_equal'] and
                     normalize_dependency_timestamps(candidate)==
                     normalize_dependency_timestamps(orig_objs[stem]),
                     'entire original 16-bit C++ OMF/11+ function boundaries/table '+name)
                need(receipt['inputs'][script]==source_bindings[script] and
                     receipt['inputs'][str(module.SOURCE.relative_to(ROOT))]==
                     source_bindings[str(module.SOURCE.relative_to(ROOT))] and
                     all(sha((ROOT/p).read_bytes())==h for p,h in receipt['inputs'].items()),
                     'all actual source/probe/header provenance inputs '+name)
                need(receipt['build']['exit_code']==0 and
                     'tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -ml' in receipt['build']['argv'][-1]
                     and '-a2' not in receipt['build']['argv'][-1],
                     'true original native Borland compiler command '+name)
                old_img=parse_mz(target).program_image
                start=module.TARGET_SEGMENT*16+module.TARGET_OFFSET
                need(old_img[start:start+boss['CODE_bytes']]==
                     parse_mz(exe).program_image[start:start+boss['CODE_bytes']],
                     'entire original Japanese-target boss CODE extent '+name)
                path=SCRATCH/f'r{number}-{stem}.obj'
                path.write_bytes(candidate)
                key=stem+'_obj'
                fname=PREFIX+f'round{number}-{key}.bin'
                (ROOT/fname).write_bytes(candidate)
                outputs[key]=dict(path=fname,bytes=len(candidate),sha256=sha(candidate))
                receipts[name]=dict(probe_run_id=proof_id, receipt_sha256=sha(receipt_path.read_bytes()),
                    source_object_sha256=sha(candidate), normalized_complete_OMF_equal=True,
                    original_target_CODE_equal=True)
            rsp=response(cfg,number)
            (SCRATCH/f'r{number}.@l').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{number}.@l'],
                WORK,f'round{number}-normal-TLINK',105)
            vec={'exe':(SCRATCH/f'r{number}.exe').read_bytes(),
                 'map':(SCRATCH/f'r{number}.map').read_bytes()}
            need(vec['exe']==exe and vec['map']==map_raw and
                 parse_mz(vec['exe']).relocations==parse_mz(target).relocations,
                 'complete original-source native MAIN EXE/MAP and all1553 target relocations')
            for key,raw in vec.items():
                fname=PREFIX+f'round{number}-{key}.bin'
                (ROOT/fname).write_bytes(raw)
                outputs[key]=dict(path=fname,bytes=len(raw),sha256=sha(raw))
            record['rounds'].append(dict(round=number,outputs=outputs,original_OMF=receipts,
                link_response_sha256=sha(rsp),original_selected_native_exe_equal=True,
                original_selected_native_map_equal=True,all_1553_target_relocations_equal=True))
            save()
            all_vectors.append((vec,receipts))
            print(f'Eight-boss round {number}: 74 C++ functions/14797 CODE, 8 original OMF objects, full MAIN link exact',flush=True)
        need(all_vectors[0][0]==all_vectors[1][0], 'two whole native MAIN EXE/MAP builds identical')
        for boss in cfg['bosses']:
            stem=boss['object']
            x=(SCRATCH/f'r1-{stem}.obj').read_bytes()
            y=(SCRATCH/f'r2-{stem}.obj').read_bytes()
            need(normalize_dependency_timestamps(x)==normalize_dependency_timestamps(y),
                 'two native OMF sources repeat after observed-only timestamp normalization '+stem)
        need(source_bindings == {
            p:sha((ROOT/p).read_bytes()) for p in source_bindings},
            'maintained sources/probes did not change during real builds')
    record['complete']=True
    save()

if __name__=='__main__':
    main()
