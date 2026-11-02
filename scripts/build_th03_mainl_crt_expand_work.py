#!/usr/bin/env python3
"""Append independently native-exact 8086 CRT sources to the proven 12-source library.

Reuses the pinned cold pair, preserved original 893-member CRT and current
12-source BCC objects; compiles only the chosen 8086 TASM member(s), then
links actual MAINL twice. The two modes form a cumulative working carrier.
"""
import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_strtol_work as parent
import build_th03_mainl_xx_work as xx
import build_th03_mainl_work as build
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.omf import describe_omf,parse_omf
from lib.borland_library import library_members,compare_members,object_program_records
from lib.decoded_mainl_display_native import externs
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

ROOT=Path(__file__).resolve().parents[1]
WORK=build.WORK
DRIVER='scripts/build_th03_mainl_crt_expand_work.py'
MODES={'strncpy':('strncpy',),
       'strncpy-movmem':('strncpy','movmem')}
NATIVE={'strncpy':(304,49,[(0,'_strncpy')],[]),
        'movmem':(266,119,[(0,'_movmem'),(82,'_memmove')],['N_PCMP@'])}
PREFIX='.analysis/work/mainl-crt-expand-'


def scope(name,raw):
    index,size,publics,imports=NATIVE[name]
    need(describe_omf(raw)['valid'],'valid native Borland CRT OMF '+name)
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(raw)]==
         [('_TEXT','CODE',size),('_DATA','DATA',0),('_BSS','BSS',0)],
         'original complete CODE/DATA/BSS geometry '+name)
    need(code_publics(raw,1)==publics and externs(raw)==imports,
         'original public and helper import order '+name)
    need([x.data for x in parse_omf(raw) if x.name=='GRPDEF']==
         [bytes.fromhex('08ff03ff02')],'original BSS-before-DATA group '+name)
    p=payload(raw)
    return dict(original_index=index,CODE_bytes=size,
                CODE_sha256=sha(bytes(p[1,i] for i in range(size))),
                publics=publics,imports=imports,
                literal_fields=literal_fields(raw))


def retained():
    base,files,accepted,members,eleven,parenthash=parent.retained()
    report_raw=(ROOT/parent.REPORT).read_bytes()
    report=json.loads(report_raw)
    need(report['complete'] and not report['source_acceptance'] and
         report['added_accepted_bytes']==0 and not report['original_cold_rebuilt'] and
         report['accepted_baseline']==base and report['accepted_library_sha256']==sha(accepted) and
         report['preceding_eleven_source_build_sha256']==parenthash and
         report['source_sha256']==sha((ROOT/parent.SOURCE).read_bytes()) and
         report['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         len(report['rounds'])==2,
         'current exact natural 12-source native baseline receipt')
    existing=[]
    for i,row in enumerate(report['rounds']):
        data={}
        for key,entry in row['outputs'].items():
            raw=(ROOT/entry['path']).read_bytes()
            need(entry==dict(path=entry['path'],bytes=len(raw),sha256=sha(raw)),
                 'complete original raw signed scanner '+key)
            data[key]=raw
        need(data['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             data['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'full real Japanese target from twelve native source members')
        sources=dict(eleven[i],strtol=data['obj'])
        comparison=compare_members(members,library_members(data['lib']),sources)
        need(comparison['replaced_members']==[m.name for m in members if m.name in sources] and
             comparison['contextual_members_unchanged']==881,
             'twelve original-position source programs and881 native members')
        existing.append(sources)
    need(existing[0]==existing[1],'two exact preceding native source object vectors')
    return base,files,accepted,members,existing,sha(report_raw)


def main(mode):
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    names=MODES[mode]
    base,files,accepted,members,preceding,parenthash=retained()
    need(len(members)==893 and all(members[NATIVE[n][0]].name==n for n in names),
         'original 893 member slots for all new CRT source units')
    original={n:(WORK/'vendor'/f'{n}.obj').read_bytes() for n in names}
    profiles={n:scope(n,raw) for n,raw in original.items()}
    need(all(object_program_records(original[n])==members[NATIVE[n][0]].program_records
             for n in names), 'all original CRT source member identities')
    source={n:(ROOT/f'src/mainl/crt/{n}.asm').read_bytes() for n in names}
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    scratch=WORK/'probe/crtnext'
    report_path=ROOT/(PREFIX+mode+'-build.json')
    report=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,mode=mode,names=names,
                accepted_baseline=base,accepted_library_sha256=sha(accepted),
                parent_twelve_source_sha256=parenthash,
                original_profiles=profiles,source_sha256={n:sha(b) for n,b in source.items()},
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),phases=[],rounds=[])
    save=lambda:report_path.write_text(json.dumps(report,indent=2)+'\n')
    def run(args,cwd,label):
        cp=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/crt-next-{mode}-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=args,returncode=cp.returncode,
                                     log_path=path,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1200:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not scratch.exists(),'fresh scoped native CRT linker scratch')
        scratch.mkdir()
        try:
            (scratch/'base.lib').write_bytes(accepted)
            (scratch/'extract.rsp').write_bytes(build.response('base.lib',
                                      ['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],scratch,'extract')
            extracted={p.stem.casefold():p for p in scratch.iterdir()
                       if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.casefold() for m in members},
                 'all893 original native member program objects')
            for m in members:
                f=extracted[m.name.casefold()]
                need(object_program_records(f.read_bytes())==m.program_records,
                     'original library member '+m.name)
                target=scratch/(m.name+'.obj')
                if f!=target:f.rename(target)
            for n,raw in source.items():
                f=scratch/(n+'.asm')
                f.write_bytes(raw)
                os.utime(f,(946684800,946684800))
            library_response=build.response(r'probe\crtnext\newcrt.lib /E',
                ['+probe\\crtnext\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\crtnext\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\crtnext\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\crtnext\\newcrt.lib'),
            ):
                need(link.count(old)==1,'one original normal linker input/output')
                link=link.replace(old,new)
            (scratch/'library.rsp').write_bytes(library_response)
            (scratch/'link.lnk').write_bytes(link)
            (ROOT/f'.analysis/work/crt-next-{mode}-library.rsp').write_bytes(library_response)
            (ROOT/f'.analysis/work/crt-next-{mode}-link.lnk').write_bytes(link)
            for i in (1,2):
                for filename in [*(n+'.obj' for n in names),'newcrt.lib',
                                 'newcrt.bak','linked.exe','linked.map']:
                    (scratch/filename).unlink(missing_ok=True)
                rebuilt={}
                for n in names:
                    run(tasm+['/m','/mx','/kh32768','/t',n+'.asm',n+'.obj'],
                        scratch,f'round{i}-assemble-{n}')
                    data=(scratch/(n+'.obj')).read_bytes()
                    need(scope(n,data)==profiles[n],
                         'whole natural native TASM source exact for '+n)
                    rebuilt[n]=data
                sources=dict(preceding[i-1],**rebuilt)
                for n,data in preceding[i-1].items():
                    (scratch/(n+'.obj')).write_bytes(data)
                run(dos+['tlib',r'@probe\crtnext\library.rsp'],WORK,
                    f'round{i}-library')
                lib=(scratch/'newcrt.lib').read_bytes()
                comparison=compare_members(members,library_members(lib),sources)
                need(comparison['replaced_members']==[m.name for m in members if m.name in sources] and
                     comparison['contextual_members_unchanged']==893-len(sources),
                     'every real source member position,all other original member programs')
                run(dos+['tlink',r'@probe\crtnext\link.lnk'],WORK,
                    f'round{i}-link')
                output={}
                for name,filename in ([(n,n+'.obj') for n in names]+[
                    ('lib','newcrt.lib'),('exe','linked.exe'),('map','linked.map')]):
                    raw=(scratch/filename).read_bytes()
                    path=f'.analysis/work/crt-next-{mode}-round{i}-{filename}'
                    (ROOT/path).write_bytes(raw)
                    output[name]=dict(path=path,bytes=len(raw),sha256=sha(raw))
                need((scratch/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (scratch/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'complete decoded Japanese MAINL EXE/MAP original raw equality')
                report['rounds'].append(dict(round=i,outputs=output,
                                             library_comparison=comparison))
                save()
                print('Original MAINL native CRT extended',mode,'round',i,
                      'EXE/MAP exact',flush=True)
            need(len(report['rounds'])==2 and
                 {k:q['sha256'] for k,q in report['rounds'][0]['outputs'].items()}==
                 {k:q['sha256'] for k,q in report['rounds'][1]['outputs'].items()},
                 'two complete identical raw TASM/TLIB/TLINK vectors')
        finally:shutil.rmtree(scratch)
    b,_,lib,_,_,afterhash=retained()
    need(b==base and lib==accepted and afterhash==parenthash and
         {n:sha((ROOT/f'src/mainl/crt/{n}.asm').read_bytes()) for n in names}==
         report['source_sha256'],
         'accepted 28-provider source library and original inputs unchanged')
    report['complete']=True
    save()


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('mode',choices=tuple(MODES))
    main(p.parse_args().mode)
