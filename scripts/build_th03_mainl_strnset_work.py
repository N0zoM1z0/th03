#!/usr/bin/env python3
"""Compile native BCC strnset and combine 16 exact DOS CRT sources in MAINL.

Reuse original fixed cold and the reviewed fifteen-source native library.
Only the new original 58-byte strnset translation unit is recompiled;
run actual TLIB/TLINK twice without recompressing or a full cold replay.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_strncat_work as parent
import build_th03_mainl_strtol_work as signed
import build_th03_mainl_work as build
import build_th03_mainl_xx_work as xx
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members,object_program_records
from lib.decoded_mainl_display_native import externs
from lib.omf import describe_omf,parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

ROOT=Path(__file__).resolve().parents[1]
WORK=build.WORK
DRIVER='scripts/build_th03_mainl_strnset_work.py'
SOURCE='src/mainl/crt/strnset.cpp'
REPORT='.analysis/work/mainl-strnset-native-build.json'
ORIGINAL=WORK/'vendor/strnset.obj'
SCRATCH=WORK/'probe/snscope'
BCC_FLAGS=signed.BCC_FLAGS



def original_scope(obj):
    need(describe_omf(obj)['valid'],'actual complete original native BCC strnset object')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(obj)]==
         [('_TEXT','CODE',58),('_DATA','DATA',0),('_BSS','BSS',0)],
         'original58-byte body and zero initialized/statically allocated bytes')
    need(code_publics(obj,1)==[(0,'_strnset')] and
         externs(obj)==['_strlen','_setmem'],
         'genuine far strnset public and original two library helper interfaces')
    need([q.data for q in parse_omf(obj) if q.name=='GRPDEF']==
         [bytes.fromhex('08ff02ff03')],
         'original DATA/BSS zero-byte group ownership')
    fields=literal_fields(obj)
    need(len(fields)==2,'two literal original far strlen/setmem fields')
    p=payload(obj)
    return dict(CODE_sha256=sha(bytes(p[1,i] for i in range(58))),
                CODE_bytes=58,native_literal_fields=fields,
                externs=externs(obj),pub=code_publics(obj,1))


def retained():
    base,files,accepted,members,old14,source14hash=parent.retained()
    raw=(ROOT/parent.REPORT).read_bytes()
    r=json.loads(raw)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_fourteen_source_build_sha256']==source14hash and
         r['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         r['source_sha256']==sha((ROOT/parent.SOURCE).read_bytes()) and
         len(r['rounds'])==2,
         'current complete original fifteen-source BCC/TLIB/TLINK baseline')
    combined=[]
    for i,row in enumerate(r['rounds']):
        output={}
        for k,q in row['outputs'].items():
            blob=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(blob),sha256=sha(blob)),
                 'actual complete inherited source output '+k)
            output[k]=blob
        need(output['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             output['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'previous 15-source complete original Japanese decoded EXE/MAP')
        objects=dict(old14[i],strncat=output['obj'])
        comparison=compare_members(members,library_members(output['lib']),objects)
        need(comparison['replaced_members']==[m.name for m in members if m.name in objects] and
             comparison['contextual_members_unchanged']==878,
             'fifteen genuine original native source slots plus878 untouched programs')
        combined.append(objects)
    need(combined[0]==combined[1] and members[306].name=='strnset',
         'same source 15 member pair and original strnset member index306')
    return base,files,accepted,members,combined,sha(raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,old_objs,priorhash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[306].program_records,
         'original large model strnset member program identity')
    goal=original_scope(original)
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    r=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
           original_cold_rebuilt=False,accepted_baseline=base,
           accepted_library_sha256=sha(accepted),
           previous_fifteen_source_build_sha256=priorhash,
           original_sha256=sha(original),source_sha256=sha(source),
           driver_sha256=sha((ROOT/DRIVER).read_bytes()),
           compiler_flags=BCC_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/strnset-{label}.log'
        (ROOT/where).write_bytes(cp.stdout)
        r['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                log_path=where,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1500:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh native original strnset local work')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.lower():p for p in SCRATCH.iterdir() if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all893 original native library member programs extracted')
            for m in members:
                f=extracted[m.name.lower()]
                need(object_program_records(f.read_bytes())==m.program_records,
                     'actual original member native records '+m.name)
                dest=SCRATCH/(m.name+'.obj')
                if f!=dest:f.rename(dest)
            (SCRATCH/'strnset.cpp').write_bytes(source)
            os.utime(SCRATCH/'strnset.cpp',(946684800,946684800))
            response=build.response(r'probe\snscope\newcrt.lib /E',
                ['+probe\\snscope\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in [
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\snscope\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\snscope\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\snscope\\newcrt.lib'),
            ]:
                need(link.count(old)==1,'one actual original linker reference')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(response)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/strnset-library.rsp').write_bytes(response)
            (ROOT/'.analysis/work/strnset-link.lnk').write_bytes(link)
            for i in (1,2):
                for name in ('strnset.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(dos+[r'C:\BC45\BCC.EXE',*BCC_FLAGS,'strnset.cpp'],
                    SCRATCH,f'round{i}-compile')
                native=(SCRATCH/'strnset.obj').read_bytes()
                need(original_scope(native)==goal,
                     'entire58 BCC CODE and2 literal ordered strlen/setmem OMF fields exact')
                source_objs=dict(old_objs[i-1],strnset=native)
                for name,obj in source_objs.items():
                    if name!='strnset':(SCRATCH/(name+'.obj')).write_bytes(obj)
                run(dos+['tlib',r'@probe\snscope\library.rsp'],
                    WORK,f'round{i}-library')
                result=(SCRATCH/'newcrt.lib').read_bytes()
                cmp=compare_members(members,library_members(result),source_objs)
                need(cmp['replaced_members']==[m.name for m in members if m.name in source_objs] and
                     cmp['contextual_members_unchanged']==877,
                     '16 genuine source original CRT slots and877 original untouched programs')
                run(dos+['tlink',r'@probe\snscope\link.lnk'],
                    WORK,f'round{i}-link')
                out={}
                for key,name in [('obj','strnset.obj'),('lib','newcrt.lib'),
                                 ('exe','linked.exe'),('map','linked.map')]:
                    raw=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/strnset-round{i}-{name}'
                    (ROOT/path).write_bytes(raw)
                    out[key]=dict(path=path,bytes=len(raw),sha256=sha(raw))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'whole original Japanese decoded MAINL EXE and MAP raw equal with16 source objects')
                r['rounds'].append(dict(round=i,outputs=out,library_comparison=cmp))
                save()
                print('16 original source CRT strnset + xx native MAINL exact round',i,flush=True)
            need({k:q['sha256'] for k,q in r['rounds'][0]['outputs'].items()}==
                 {k:q['sha256'] for k,q in r['rounds'][1]['outputs'].items()},
                 'two identical entire source OMF/library/EXE/MAP vectors')
        finally:shutil.rmtree(SCRATCH)
    final,_,lib,_,_,newhash=retained()
    need(final==base and lib==accepted and newhash==priorhash and
         source==(ROOT/SOURCE).read_bytes(),'same source and fixed accepted pair')
    r['complete']=True
    save()

if __name__=='__main__':
    main()
