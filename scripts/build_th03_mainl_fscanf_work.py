#!/usr/bin/env python3
"""Compile true Borland C++ fscanf and link 32 original MAINL source owners.

Reuse the exact 31-source fseek carrier and original 893-member library.
Compile only the affected 40-byte fscanf TU twice. Keep the fixed Japanese
target, original accepted publication and cold pair untouched.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_fseek_work as previous
import build_th03_mainl_strset_work as bcc
import build_th03_mainl_xx_work as xx
import build_th03_mainl_work as build
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members,object_program_records
from lib.decoded_mainl_display_native import externs
from lib.omf import describe_omf,parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

ROOT=Path(__file__).resolve().parents[1]
WORK=build.WORK
SOURCE='src/mainl/crt/fscanf.cpp'
DRIVER='scripts/build_th03_mainl_fscanf_work.py'
REPORT='.analysis/work/mainl-fscanf-native-build.json'
ORIGINAL=WORK/'vendor/fscanf.obj'
SCRATCH=WORK/'probe/fsscan'
BCC_FLAGS=bcc.BCC_FLAGS


def original_scope(obj):
    need(describe_omf(obj)['valid'],'complete Borland original scanf wrapper OMF')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(obj)]==
         [('_TEXT','CODE',40),('_DATA','DATA',0),('_BSS','BSS',0)],
         '40 complete original fscanf CODE and empty DATA/BSS')
    need(code_publics(obj,1)==[(0,'_fscanf')] and
         externs(obj)==['__Nfgetc','__Nungetc','__scanner'],
         'original far public and near scanner callbacks/import order')
    need([q.data.hex() for q in parse_omf(obj) if q.name=='GRPDEF']==
         ['08ff02ff03'],'original DATA/BSS segment group')
    fields=literal_fields(obj)
    need([(f['site'],f['location_type'],f['segment_relative'],
           f['frame_method'],f['target_method'],f['target']) for f in fields]==
         [(31,1,False,5,2,3),(27,1,True,5,2,1),(23,1,True,5,2,2)],
         'all three original descending TARGET-framed callback/call FIXUPPs')
    p=payload(obj)
    return dict(CODE_bytes=40,CODE_sha256=sha(bytes(p[1,i] for i in range(40))),
                native_literal_fields=fields,
                externs=externs(obj),public=code_publics(obj,1))


def retained():
    base,files,accepted,members,prior30,parenthash=previous.retained()
    raw=(ROOT/previous.REPORT).read_bytes()
    r=json.loads(raw)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_thirty_source_build_sha256']==parenthash and
         r['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         r['source_sha256']=={name:sha((ROOT/name).read_bytes()) for name in previous.SOURCES} and
         r['layout_sha256']==sha((ROOT/previous.LAYOUT).read_bytes()) and
         len(r['rounds'])==2,'bound 31-source real fseek native LINK/OMF parent')
    objects=[]
    for i,row in enumerate(r['rounds']):
        outputs={}
        for kind,q in row['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'full unchanged preceding fseek '+kind)
            outputs[kind]=data
        need(outputs['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             '31 native sources produced entire original Japanese EXE/MAP')
        source=dict(prior30[i],fseek=outputs['obj'])
        cmp=compare_members(members,library_members(outputs['lib']),source)
        need(cmp['replaced_members']==sorted(source) and
             cmp['contextual_members_unchanged']==862,
             'original 31 native source owners and other 862 unchanged programs')
        objects.append(source)
    need(objects[0]==objects[1] and len(objects[0])==31 and
         len(members)==893 and members[231].name=='fscanf',
         'two whole native parent source vectors and original fscanf slot231')
    return base,files,accepted,members,objects,sha(raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,objects,priorhash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[231].program_records,
         'original whole fscanf member native program identity')
    expected=original_scope(original)
    src=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    r=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
           original_cold_rebuilt=False,accepted_baseline=base,
           accepted_library_sha256=sha(accepted),
           previous_thirty_one_source_build_sha256=priorhash,
           original_sha256=sha(original),source_sha256=sha(src),
           driver_sha256=sha((ROOT/DRIVER).read_bytes()),
           compiler_flags=BCC_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    def run(cmd,cwd,label):
        c=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/fscanf-{label}.log'
        (ROOT/where).write_bytes(c.stdout)
        r['phases'].append(dict(label=label,command=cmd,returncode=c.returncode,
                                log_path=where,log_sha256=sha(c.stdout)))
        save()
        need(c.returncode==0,label+': '+c.stdout.decode(errors='replace')[-1400:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh fscanf original source scratch')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.lower():p for p in SCRATCH.iterdir() if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},'all 893 original CRT objects')
            for m in members:
                p=extracted[m.name.lower()]
                need(object_program_records(p.read_bytes())==m.program_records,
                     'unchanged original module program '+m.name)
                d=SCRATCH/(m.name+'.obj')
                if p!=d:p.rename(d)
            (SCRATCH/'fscanf.cpp').write_bytes(src)
            os.utime(SCRATCH/'fscanf.cpp',(946684800,946684800))
            library=build.response(r'probe\fsscan\newcrt.lib /E',
                ['+probe\\fsscan\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\fsscan\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\fsscan\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\fsscan\\newcrt.lib'),
            ):
                need(link.count(old)==1,'one genuine normal-link MAINL destination')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(library)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/fscanf-library.rsp').write_bytes(library)
            (ROOT/'.analysis/work/fscanf-link.lnk').write_bytes(link)
            for i in (1,2):
                for f in ('fscanf.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/f).unlink(missing_ok=True)
                run(dos+[r'C:\BC45\BCC.EXE',*BCC_FLAGS,'fscanf.cpp'],
                    SCRATCH,f'round{i}-compile')
                native=(SCRATCH/'fscanf.obj').read_bytes()
                need(original_scope(native)==expected,
                     'all40 real BCC CODE and three literal native fixups equal')
                sources=dict(objects[i-1],fscanf=native)
                for n,b in objects[i-1].items():(SCRATCH/(n+'.obj')).write_bytes(b)
                run(dos+['tlib',r'@probe\fsscan\library.rsp'],WORK,f'round{i}-library')
                comparison=compare_members(members,library_members((SCRATCH/'newcrt.lib').read_bytes()),sources)
                need(comparison['replaced_members']==sorted(sources) and
                     comparison['contextual_members_unchanged']==861,
                     '32 original native source members and 861 untouched programs')
                run(dos+['tlink',r'@probe\fsscan\link.lnk'],WORK,f'round{i}-link')
                outputs={}
                for kind,name in (('obj','fscanf.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    data=(SCRATCH/name).read_bytes()
                    where=f'.analysis/work/fscanf-round{i}-{name}'
                    (ROOT/where).write_bytes(data)
                    outputs[kind]=dict(path=where,bytes=len(data),sha256=sha(data))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'complete original Japanese MAINL EXE/MAP exact with32 source members')
                r['rounds'].append(dict(round=i,outputs=outputs,library_comparison=comparison))
                save()
                print('32 native source original fscanf Japanese MAINL exact round',i,flush=True)
            need({k:x['sha256'] for k,x in r['rounds'][0]['outputs'].items()}==
                 {k:x['sha256'] for k,x in r['rounds'][1]['outputs'].items()},
                 'two identical complete real native compiler/link vectors')
        finally:shutil.rmtree(SCRATCH)
    again,_,original_library,_,_,afterhash=retained()
    need(again==base and original_library==accepted and afterhash==priorhash and
         src==(ROOT/SOURCE).read_bytes(),'current native source and prior original inputs unchanged')
    r['complete']=True
    save()


if __name__=='__main__':
    main()
