#!/usr/bin/env python3
"""Rebuild original Borland signed strtol with all preceding native CRT sources.

Only the new 290-byte parser is compiled. Eleven other independent source
objects and 881 unchanged original native member programs are relinked.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_strtoul_work as parent
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
SOURCE='src/mainl/crt/strtol.cpp'
DRIVER='scripts/build_th03_mainl_strtol_work.py'
REPORT='.analysis/work/mainl-strtol-native-build.json'
SCRATCH=WORK/'probe/stlscope'
ORIGINAL=WORK/'vendor/strtol.obj'
BCC_FLAGS=parent.BCC_FLAGS


def original_scope(obj):
    need(describe_omf(obj)['valid'],'real complete Borland signed scanner OMF')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(obj)]==
         [('_TEXT','CODE',290),('_DATA','DATA',0),('_BSS','BSS',0)],
         'complete290-byte CODE with empty original DATA/BSS')
    need(code_publics(obj,1)==[(56,'_strtol')] and
         externs(obj)==['_errno','__ctype','__scantol'],
         'two near helpers,far public at56,and original extern ordering')
    need([q.data for q in parse_omf(obj) if q.name=='GRPDEF']==
         [bytes.fromhex('08ff02ff03')],'original DATA-before-BSS group')
    fields=literal_fields(obj)
    need(len(fields)==7,'all seven ordered original FIXUPPs')
    p=payload(obj)
    return dict(CODE_sha256=sha(bytes(p[1,i] for i in range(290))),
                CODE_bytes=290,native_literal_fields=fields,
                public_offset=56,imports=externs(obj))


def retained():
    base,files,accepted,members,ten,previoushash=parent.retained()
    report_raw=(ROOT/parent.REPORT).read_bytes()
    report=json.loads(report_raw)
    need(report['complete'] and not report['source_acceptance'] and
         report['added_accepted_bytes']==0 and not report['original_cold_rebuilt'] and
         report['accepted_baseline']==base and
         report['accepted_library_sha256']==sha(accepted) and
         report['preceding_ten_source_build_sha256']==previoushash and
         report['source_sha256']==sha((ROOT/parent.SOURCE).read_bytes()) and
         report['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         len(report['rounds'])==2,
         'reused genuine eleven-source native build and fixed accepted baseline')
    eleven=[]
    for index,entry in enumerate(report['rounds']):
        out={}
        for name,q in entry['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'unchanged complete preceding source output '+name)
            out[name]=data
        need(out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'preceding actual eleven-source whole Japanese decoded EXE and MAP')
        objects=dict(ten[index],strtoul=out['obj'])
        cmp=compare_members(members,library_members(out['lib']),objects)
        need(cmp['replaced_members']==[m.name for m in members if m.name in objects] and
             cmp['contextual_members_unchanged']==882,
             'all eleven source TUs and other882 native member programs')
        eleven.append(objects)
    need(eleven[0]==eleven[1] and members[314].name=='strtol',
         'repeated11 source vectors and original signed parser at index314')
    return base,files,accepted,members,eleven,sha(report_raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,objects,priorhash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[314].program_records,
         'original signed parser member program identity')
    target=original_scope(original)
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    report=dict(complete=False,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                accepted_baseline=base,accepted_library_sha256=sha(accepted),
                preceding_eleven_source_build_sha256=priorhash,
                original_sha256=sha(original),source_sha256=sha(source),
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                compiler_flags=BCC_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(command,cwd,label):
        cp=subprocess.run(command,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/strtol-{label}.log'
        (ROOT/where).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=command,returncode=cp.returncode,
                                     log_path=where,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1350:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'new isolated original native signed scanner scratch')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.lower():p for p in SCRATCH.iterdir() if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all893 original native library members extracted')
            for m in members:
                found=extracted[m.name.lower()]
                need(object_program_records(found.read_bytes())==m.program_records,
                     'entire original member program '+m.name)
                dest=SCRATCH/(m.name+'.obj')
                if found!=dest:found.rename(dest)
            (SCRATCH/'strtol.cpp').write_bytes(source)
            os.utime(SCRATCH/'strtol.cpp',(946684800,946684800))
            library_rsp=build.response(r'probe\stlscope\newcrt.lib /E',
                ['+probe\\stlscope\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in [
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\stlscope\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\stlscope\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\stlscope\\newcrt.lib'),
            ]:
                need(link.count(old)==1,'real original MAINL source output slot')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(library_rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/strtol-library.rsp').write_bytes(library_rsp)
            (ROOT/'.analysis/work/strtol-link.lnk').write_bytes(link)
            for n in (1,2):
                for name in ('strtol.obj','newcrt.lib','newcrt.bak',
                             'linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(dos+[r'C:\BC45\BCC.EXE',*BCC_FLAGS,'strtol.cpp'],
                    SCRATCH,f'round{n}-compile')
                result_obj=(SCRATCH/'strtol.obj').read_bytes()
                need(original_scope(result_obj)==target,
                     'complete original290-byte native CODE and seven literal fields')
                sources=dict(objects[n-1],strtol=result_obj)
                for name,obj in sources.items():
                    if name!='strtol':(SCRATCH/(name+'.obj')).write_bytes(obj)
                run(dos+['tlib',r'@probe\stlscope\library.rsp'],
                    WORK,f'round{n}-library')
                library=(SCRATCH/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(library),sources)
                need(compared['replaced_members']==[m.name for m in members if m.name in sources] and
                     compared['contextual_members_unchanged']==881,
                     'twelve authentic source objects at original slots and881 other programs')
                run(dos+['tlink',r'@probe\stlscope\link.lnk'],WORK,
                    f'round{n}-link')
                outs={}
                for kind,name in [('obj','strtol.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')]:
                    data=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/strtol-round{n}-{name}'
                    (ROOT/path).write_bytes(data)
                    outs[kind]=dict(path=path,bytes=len(data),sha256=sha(data))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'complete original Japanese decoded MAINL EXE/MAP with 12 native source members')
                report['rounds'].append(dict(round=n,outputs=outs,library_comparison=compared))
                save()
                print('12 source signed parser and xx exact Japanese MAINL round',n,flush=True)
            need({k:q['sha256'] for k,q in report['rounds'][0]['outputs'].items()}==
                 {k:q['sha256'] for k,q in report['rounds'][1]['outputs'].items()},
                 'two actual identical complete native output vectors')
        finally:shutil.rmtree(SCRATCH)
    b,_,lib,_,_,afterhash=retained()
    need(b==base and lib==accepted and afterhash==priorhash and
         source==(ROOT/SOURCE).read_bytes(), 'same source and unchanged original inputs')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
