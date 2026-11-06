#!/usr/bin/env python3
"""Recompile original complete bullet main+PELLET_PUT source in two local rounds.

Target linked MAIN: after572 source-backed 9 bosses, 4 enemy controllers,
natural keyboard; reuse remaining 98 source objects, original linker and
CRT. Preserve original BSS/Turbo C++ memory/ABI. No cold replay or opcode
patch. The DOS MZ compact serializer is a distinct, already verified step.
"""
import fcntl,json,os,subprocess
from pathlib import Path
import build_th03_main_enemy_four_after572_work as previous
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz
from build_th03_mainl_resources_work import sha,need
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact

ROOT=previous.ROOT
WORK=previous.WORK
DRIVER='scripts/build_th03_main_bullet_after588_work.py'
CONFIG='config/main_work/bullet_after588.json'
PREFIX='.analysis/work/main-bullet-after588-native-'
REPORT=PREFIX+'build.json'
STAGE='af588b'
SCRATCH=WORK/('probe/'+STAGE)

def inputs():
    c=json.loads((ROOT/CONFIG).read_text())
    need(c['schema']=='th03-main-bullet-after588-native-v1' and
         c['parent_report']==previous.REPORT and
         c['source']=='src/main/bullet/bullet.cpp' and
         c['wrapper']=='src/main/bullet/producers/bullet_native.cpp' and
         c['original_object']=='obj/th03/bullet.obj' and
         (c['GAME'],c['BINARY'])==(3,'M') and
         (c['original_main_CODE_bytes'],c['original_pellet_render_CODE_bytes'],
          c['original_BSS_bytes'],c['original_ordered_fixups'],
          c['original_public_symbols'],c['original_bullet_MAIN_MZ_relocations'],
          c['original_target_file_bytes'])==(2602,83,9500,196,20,1553,130882) and
         c['canonical_factory_credit_changed'] is False and
         c['whole_project_source_accepted'] is False,
         'all complete real bullet/trail GRCG BSS and ABI bounds')
    parent=json.loads((ROOT/c['parent_report']).read_text())
    need(parent['complete'] and len(parent['rounds'])==2 and
         sha((ROOT/c['parent_report']).read_bytes())==c['parent_report_sha256'],
         'actual source-native original 4 enemy/9 boss parent, no full replay')
    return c,sha((ROOT/CONFIG).read_bytes()),parent

def sources(c):
    body=(ROOT/c['source']).read_bytes()
    wrapper=(ROOT/c['wrapper']).read_bytes()
    need(body and b'\r' not in body and
         b'#pragma option -a2' in body and
         b'void bullets_update' in body and
         b'grcg_pellet_put' in body and
         wrapper.endswith(f'#include "{c["source"]}"\n'.encode()) and
         wrapper.count(f'#include "{c["source"]}"'.encode())==1 and
         (WORK/c['source']).read_bytes().replace(b'\r\n',b'\n')==body,
         'actual original natural C++ bullet/trail and fast GRCG renderer source')
    return body,wrapper

def object_scope(obj,original,c):
    code=payload(obj)
    ref=payload(original)
    public=public_offsets(obj)
    segs=segment_definitions(obj)
    need(code==ref and
         sum(idx==1 for idx,offset in code)==2602 and
         sum(idx==4 for idx,offset in code)==83 and
         len(literal_fields(obj))==196 and
         literal_fields(obj)==literal_fields(original) and
         public==public_offsets(original) and len(public)==20 and
         segs==segment_definitions(original) and
         (segs[0]['name'],segs[0]['size'],segs[2]['size'],
          segs[3]['name'],segs[3]['size'])==
          ('BULLET_TEXT',2602,9500,'PELLET_PUT',83),
         'entire bullet simulation and pellet fast renderer original native CODE, 196 ordered fixups, 9500 BSS')
    return dict(complete_initialized_CODE_bytes=2685,
                main_bullet_CODE_bytes=2602,PELLET_PUT_CODE_bytes=83,
                BSS_bytes=9500,original_PUBLIC_count=20,
                original_FIXUPP_count=196,entire_original_linker_semantics_equal=True,
                original_vendor_OMF_packet_identity=False)

def response(n):
    original=previous.response(n)
    for old,new in [(b'obj\\th03\\bullet.obj',f'probe\\{STAGE}\\r{n}\\bullet.obj'.encode()),
                    (f'probe\\af572e\\r{n}.exe'.encode(),f'probe\\{STAGE}\\r{n}.exe'.encode()),
                    (f'probe\\af572e\\r{n}.map'.encode(),f'probe\\{STAGE}\\r{n}.map'.encode())]:
        need(original.count(old)==1,'one native original bullet slot and one original link output')
        original=original.replace(old,new)
    return original

def map_normalize(raw,n):
    name=f'M=probe/{STAGE}/r{n}/bullet.cpp'.encode()
    need(raw.count(name)==4,'real BULLET_TEXT/PELLET_PUT/DATA/BSS native rows')
    return raw.replace(name,b'M=th03/bullet.cpp')

def main():
    cfg,cfg_sha,prev=inputs()
    source,wrapper=sources(cfg)
    original=(WORK/cfg['original_object']).read_bytes()
    target=read_verified_artifact(ROOT,find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-main'))
    tmz=parse_mz(target)
    need(len(target)==130882 and len(tmz.relocations)==1553,
         'pinned original Japanese MAIN file')
    result=dict(complete=False,cold_rebuilt=False,library_rebuilt=False,
        source_game_objects_recompiled_per_round=1,other_project_objects_reused=98,
        source_CODE_bytes=2685,source_BSS_bytes=9500,
        canonical_factory_credit_changed=False,whole_game_source_accepted=False,
        parent_report_sha256=cfg['parent_report_sha256'],
        config_sha256=cfg_sha,driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        maintained_source_sha256=sha(source),wrapper_sha256=sha(wrapper),
        original_object_sha256=sha(original),original_target_sha256=sha(target),
        phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(result,indent=2)+'\n')
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
       WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'),MSDOS_PATH=r'C:\TC4\BIN',
       TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/'_reference/ReC98/bin/msdos.exe'),'-e','-x']

    def run(cmd,label):
        p=subprocess.run(cmd,cwd=WORK,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=105)
        path=PREFIX+label+'.log'
        (ROOT/path).write_bytes(p.stdout)
        result['phases'].append(dict(label=label,command=cmd,exit_code=p.returncode,
                                     log=path,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1000:])

    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        need(not SCRATCH.exists(),'fresh original bullet source compiler/link stage')
        SCRATCH.mkdir()
        (SCRATCH/'driver.py').write_bytes((ROOT/DRIVER).read_bytes())
        (SCRATCH/'config.json').write_bytes((ROOT/CONFIG).read_bytes())
        vectors=[]
        for n in (1,2):
            stage=SCRATCH/f'r{n}'
            stage.mkdir()
            (stage/'bullet.cpp').write_bytes(wrapper.replace(b'\n',b'\r\n'))
            os.utime(stage/'bullet.cpp',(946684800,946684800))
            run(dos+['tcc','-c','-I.','-O','-b-','-3','-Z','-d',
                     '-DGAME=3','-ml',"-DBINARY='M'",
                     f'-nprobe/{STAGE}/r{n}/',f'probe/{STAGE}/r{n}/bullet.cpp'],
                f'round{n}-bullet-TC4-compile')
            obj=(stage/'bullet.obj').read_bytes()
            scoped=object_scope(obj,original,cfg)
            rsp=response(n)
            (SCRATCH/f'r{n}.@l').write_bytes(rsp)
            run(dos+['tlink',f'@probe\\{STAGE}\\r{n}.@l'],
                f'round{n}-normal-TLINK')
            exe=(SCRATCH/f'r{n}.exe').read_bytes()
            mapped=(SCRATCH/f'r{n}.map').read_bytes()
            old_output=prev['rounds'][n-1]['outputs']
            old_exe=previous.parent.read_pin(old_output['exe'])
            old_map=previous.parent.read_pin(old_output['map'])
            need(exe==old_exe and map_normalize(mapped,n)==old_map and
                 len(exe)==132322 and parse_mz(exe).program_image==tmz.program_image and
                 parse_mz(exe).relocations==tmz.relocations,
                 'full original native MAIN source EXE/MAP, complete target program and 1553 ordered relocations')
            compact=compact_mz(exe)
            need(compact==target,'separate actual native DOS MZ standard container fully original-equal')
            raw=dict(obj=obj,exe=exe,map=mapped,compact_mz=compact)
            outputs={}
            for name,blob in raw.items():
                path=PREFIX+f'round{n}-{name}.bin'
                (ROOT/path).write_bytes(blob)
                outputs[name]=dict(path=path,bytes=len(blob),sha256=sha(blob))
            result['rounds'].append(dict(round=n,outputs=outputs,scope=scoped,
                  actual_link_response_sha256=sha(rsp),
                  whole_original_program_and_MZ_equal=True))
            save()
            vectors.append(raw)
            print('Bullet C++ round',n,'2602 main CODE +83 pellet 386 CODE/9500 BSS, 196 fixups, entire Japanese MAIN file exact',flush=True)
        need(vectors[0]['exe']==vectors[1]['exe'] and
             payload(vectors[0]['obj'])==payload(vectors[1]['obj']) and
             literal_fields(vectors[0]['obj'])==literal_fields(vectors[1]['obj']) and
             vectors[0]['compact_mz']==vectors[1]['compact_mz'] and
             sources(cfg)==(source,wrapper),
             'two independent original source-bound bullet object/link vectors repeat')
    result['complete']=True
    save()

if __name__=='__main__':
    main()
