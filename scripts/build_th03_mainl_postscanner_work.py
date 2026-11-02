#!/usr/bin/env python3
"""Build new complete original DOS CRT source modules against 18-source MAINL.

Each mode starts from the retained byte-exact hqsort+qsort+xx 18-source
carrier and replaces ONLY its named original CRT library slots with
fresh TASM source modules. Both native TLIB/TLINK rounds are complete.
No cold replay, accepted publication or parent source relink is performed.
"""
import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_scanner_work as parent
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
DRIVER='scripts/build_th03_mainl_postscanner_work.py'
PREFIX='.analysis/work/mainl-postscanner-'
MODES={
    'strrchr':('strrchr',),
    'strrchr-srchstr':('strrchr','srchstr'),
    'strrchr-srchstr-strrev':('strrchr','srchstr','strrev'),
    'strrchr-srchstr-strrev-strset':('strrchr','srchstr','strrev','strset'),
}
NATIVE={
    'strrchr':dict(member_index=308,CODE_bytes=77,DATA_bytes=0,
                   publics=[(0,'_strrchr')],imports=['_strlen'],
                   group='08ff03ff02',fields=1),
    'srchstr':dict(member_index=282,CODE_bytes=322,DATA_bytes=2,
                   publics=[(0,'__searchstr')],
                   imports=['__getdcwd','_strcat','_strcpy','_strlen',
                            '_free','__fullpath','__access','___path_issbcs'],
                   group='08ff02ff03',fields=10),
    'strrev':dict(member_index=309,CODE_bytes=52,DATA_bytes=0,
                   publics=[(0,'_strrev')],imports=[],
                   group='08ff03ff02',fields=0),
    'strset':dict(member_index=310,CODE_bytes=46,DATA_bytes=0,
                   publics=[(0,'_strset')],imports=['_strlen','_setmem'],
                   group='08ff02ff03',fields=2),
}

TASM=['/m','/mx','/kh32768','/t']


def original_scope(name,data):
    profile=NATIVE[name]
    need(describe_omf(data)['valid'],'valid original DOS owner '+name)
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(data)]==
         [('_TEXT','CODE',profile['CODE_bytes']),
          ('_DATA','DATA',profile['DATA_bytes']),('_BSS','BSS',0)],
         'original full CODE/DATA/BSS object owner for '+name)
    need(code_publics(data,1)==profile['publics'] and externs(data)==profile['imports'],
         'exact original far cdecl/public and imported names/indices '+name)
    need([r.data.hex() for r in parse_omf(data) if r.name=='GRPDEF']==[profile['group']],
         'literal original DGROUP segment order '+name)
    fields=literal_fields(data)
    need(len(fields)==profile['fields'],'all actual original ordered fixups '+name)
    if name=='strrchr':
        need(len(fields)==1 and fields[0]['site']==15 and
             fields[0]['target_method']==2 and fields[0]['target']==1 and
             fields[0]['frame_method']==5,
             'original strrchr literal far strlen TARGET-frame site15')
    p=payload(data)
    code=bytes(p[1,i] for i in range(profile['CODE_bytes']))
    initialized=bytes(p[2,i] for i in range(profile['DATA_bytes']))
    return dict(CODE_bytes=len(code),CODE_sha256=sha(code),
                DATA_bytes=len(initialized),DATA_sha256=sha(initialized),
                publics=code_publics(data,1),externs=externs(data),
                literal_fields=fields,group=profile['group'])


def retained():
    base,files,accepted,members,earlier22,source22hash=parent.retained()
    raw=(ROOT/parent.REPORT).read_bytes()
    report=json.loads(raw)
    need(report['complete'] and not report['source_acceptance'] and
         report['added_accepted_bytes']==0 and not report['original_cold_rebuilt'] and
         report['accepted_baseline']==base and
         report['accepted_library_sha256']==sha(accepted) and
         report['prior_twenty_two_source_build_sha256']==source22hash and
         report['source_sha256']==sha((ROOT/parent.SOURCE).read_bytes()) and
         report['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         len(report['rounds'])==2,
         'current complete original 23-source MAINL scanner native build')
    combined=[]
    for i,row in enumerate(report['rounds']):
        output={}
        for kind,meta in row['outputs'].items():
            blob=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                 'actual 23-source source-bound original native '+kind)
            output[kind]=blob
        need(output['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             output['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'original 23-source Japanese decoded EXE and MAP byte-equal')
        objects=dict(earlier22[i],scanner=output['obj'])
        compared=compare_members(members,library_members(output['lib']),objects)
        need(compared['replaced_members']==sorted(objects) and
             compared['contextual_members_unchanged']==870,
             '23 original source members plus 870 untouched native vendor programs')
        combined.append(objects)
    need(combined[0]==combined[1] and len(members)==893 and len(combined[0])==23,
         'two identical complete 23 native source OBJ vectors')
    return base,files,accepted,members,combined,sha(raw)


def main(mode):
    names=MODES[mode]
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,prior,parenthash=retained()
    need(all(members[NATIVE[n]['member_index']].name==n for n in names),
         'original member positions independently determined')
    originals={n:(WORK/'vendor'/f'{n}.obj').read_bytes() for n in names}
    goal={n:original_scope(n,b) for n,b in originals.items()}
    need(all(object_program_records(originals[n])==
             members[NATIVE[n]['member_index']].program_records for n in names),
         'literal original library member program identity')
    source={n:(ROOT/f'src/mainl/crt/{n}.asm').read_bytes() for n in names}
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    scratch=WORK/'probe/postscan'
    path=ROOT/(PREFIX+mode+'-build.json')
    report=dict(complete=False,mode=mode,names=names,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                accepted_baseline=base,accepted_library_sha256=sha(accepted),
                previous_twenty_three_source_receipt_sha256=parenthash,
                original_profiles=goal,
                source_sha256={n:sha(b) for n,b in source.items()},
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),phases=[],rounds=[])
    save=lambda:path.write_text(json.dumps(report,indent=2)+'\n')
    def run(command,cwd,label):
        cp=subprocess.run(command,cwd=cwd,env=env,
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=130)
        where=f'.analysis/work/postscanner-{mode}-{label}.log'
        (ROOT/where).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=command,
                                     returncode=cp.returncode,log_path=where,
                                     log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1400:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as writer:
        fcntl.flock(writer,fcntl.LOCK_EX)
        need(not scratch.exists(),'fresh local original native extension working tree')
        scratch.mkdir()
        try:
            (scratch/'base.lib').write_bytes(accepted)
            (scratch/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],scratch,'extract')
            extracted={p.stem.lower():p for p in scratch.iterdir()
                       if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all original893 CRT program records extracted')
            for member in members:
                found=extracted[member.name.lower()]
                need(object_program_records(found.read_bytes())==member.program_records,
                     'untouched original member '+member.name)
                destination=scratch/(member.name+'.obj')
                if found!=destination:found.rename(destination)
            for n,b in source.items():
                f=scratch/(n+'.asm');f.write_bytes(b);os.utime(f,(946684800,946684800))
            response=build.response(r'probe\postscan\newcrt.lib /E',
                ['+probe\\postscan\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\postscan\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\postscan\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\postscan\\newcrt.lib'),
            ):
                need(link.count(old)==1,'original independent MAINL full target link')
                link=link.replace(old,new)
            (scratch/'library.rsp').write_bytes(response)
            (scratch/'link.lnk').write_bytes(link)
            (ROOT/f'.analysis/work/postscanner-{mode}-library.rsp').write_bytes(response)
            (ROOT/f'.analysis/work/postscanner-{mode}-link.lnk').write_bytes(link)
            for round_no in (1,2):
                for filename in [*(n+'.obj' for n in names),'newcrt.lib',
                                 'newcrt.bak','linked.exe','linked.map']:
                    (scratch/filename).unlink(missing_ok=True)
                rebuilt={}
                for n in names:
                    run(tasm+TASM+[n+'.asm',n+'.obj'],scratch,
                        f'round{round_no}-assemble-{n}')
                    blob=(scratch/(n+'.obj')).read_bytes()
                    need(original_scope(n,blob)==goal[n],
                         'full original SOURCE+ordered OMF native code '+n)
                    rebuilt[n]=blob
                owners=dict(prior[round_no-1],**rebuilt)
                for n,blob in prior[round_no-1].items():
                    (scratch/(n+'.obj')).write_bytes(blob)
                run(dos+['tlib',r'@probe\postscan\library.rsp'],
                    WORK,f'round{round_no}-library')
                lib=(scratch/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(lib),owners)
                need(compared['replaced_members']==sorted(owners) and
                     compared['contextual_members_unchanged']==893-len(owners),
                     'all native source member slots and original remaining programs unchanged')
                run(dos+['tlink',r'@probe\postscan\link.lnk'],
                    WORK,f'round{round_no}-link')
                out={}
                for kind,filename in ([(n,n+'.obj') for n in names]+[
                    ('lib','newcrt.lib'),('exe','linked.exe'),('map','linked.map')]):
                    raw=(scratch/filename).read_bytes()
                    where=f'.analysis/work/postscanner-{mode}-round{round_no}-{filename}'
                    (ROOT/where).write_bytes(raw)
                    out[kind]=dict(path=where,bytes=len(raw),sha256=sha(raw))
                need((scratch/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (scratch/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'real Japanese 67,372-byte MAINL full original EXE/MAP raw equality')
                report['rounds'].append(dict(round=round_no,outputs=out,
                                             library_comparison=compared))
                save()
                print('Source CRT after scanner',mode,'source modules',len(owners),
                      'Japanese EXE/MAP exact round',round_no,flush=True)
            need({k:v['sha256'] for k,v in report['rounds'][0]['outputs'].items()}==
                 {k:v['sha256'] for k,v in report['rounds'][1]['outputs'].items()},
                 'two whole deterministic raw OBJ/LIB/EXE/MAP output vectors')
        finally:shutil.rmtree(scratch)
    after,_,otherlib,_,_,otherhash=retained()
    need(after==base and otherlib==accepted and otherhash==parenthash and
         {n:sha((ROOT/f'src/mainl/crt/{n}.asm').read_bytes()) for n in names}==
         report['source_sha256'],'retained original fixed baseline and sources unchanged')
    report['complete']=True
    save()


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=tuple(MODES))
    main(parser.parse_args().mode)
