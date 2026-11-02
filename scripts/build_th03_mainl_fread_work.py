#!/usr/bin/env python3
"""Build the actual 437-byte Borland DOS fread from maintained 8086 source.

This is the COMPLETE fread TU: 283-byte near buffered read core and
154-byte public far fread entry with two genuine far and two near imports.
The original 893-member CRT is reconstructed in its original order,
with 27 independent original native source CRT modules retained.
The cold pair and accepted 28-provider publication are not rebuilt.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_strset_work as parent
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
SOURCES=('src/mainl/crt/fread.asm',)
DRIVER='scripts/build_th03_mainl_fread_work.py'
REPORT='.analysis/work/mainl-fread-native-build.json'
SCRATCH=WORK/'probe/frdsrc'
ORIGINAL=WORK/'vendor/fread.obj'
TASM_FLAGS=['/m','/mx','/kh32768','/t','fread.asm','fread.obj']


def original_scope(obj):
    need(describe_omf(obj)['valid'],'genuine original 437-byte fread OMF module')
    need([(x['name'],x['class'],x['size']) for x in segment_definitions(obj)]==
         [('_TEXT','CODE',437),('_DATA','DATA',0),('_BSS','BSS',0)],
         'complete original fread CODE and zero DATA/BSS segments')
    need(code_publics(obj,1)==[(283,'_fread')] and
         externs(obj)==['__fgetc','__rtl_read','N_LXMUL@','N_PADD@'],
         'original two near/far entries and four genuine imported CRT helpers')
    need([r.data.hex() for r in parse_omf(obj) if r.name=='GRPDEF']==
         ['08ff03ff02'],'original BSS-before-DATA group for fread')
    fields=literal_fields(obj)
    need([(f['site'],f['target_method'],f['target'],f['frame_method']) for f in fields]==
         [(135,2,2,5),(245,2,1,5),(313,2,3,0),(385,2,4,0)],
         'all four literal mixed far-call and near-helper native FIXUPPs')
    p=payload(obj)
    return dict(CODE_bytes=437,
                CODE_sha256=sha(bytes(p[1,i] for i in range(437))),
                literal_ordered_fields=fields,imports=externs(obj),
                public_offset=283,original_helper_boundaries=(0,283,437))


def retained():
    base,files,accepted,members,prior26,priorhash=parent.retained()
    receipt=(ROOT/parent.REPORT).read_bytes()
    r=json.loads(receipt)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_twenty_six_source_build_sha256']==priorhash and
         r['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         r['source_sha256']==sha((ROOT/parent.SOURCE).read_bytes()) and
         len(r['rounds'])==2,
         'unmodified real27-source Borland CRT/EXE/MAP input evidence')
    objects=[]
    for i,row in enumerate(r['rounds']):
        output={}
        for kind,meta in row['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'complete raw original source 27-module output '+kind)
            output[kind]=data
        need(output['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             output['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'actual whole original Japanese decoded MAINL EXE and MAP')
        owners=dict(prior26[i],strset=output['obj'])
        compared=compare_members(members,library_members(output['lib']),owners)
        need(compared['replaced_members']==sorted(owners) and
             compared['contextual_members_unchanged']==866,
             'genuine27 original source owners and866 untouched CRT programs')
        objects.append(owners)
    need(objects[0]==objects[1] and len(members)==893 and
         len(objects[0])==27 and members[229].name=='fread',
         'real original fread index229 and identical27 source object pairs')
    return base,files,accepted,members,objects,sha(receipt)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,preceding,parenthash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[229].program_records,
         'original complete 437-byte fread object at its library slot')
    goal=original_scope(original)
    inputs={name:(ROOT/name).read_bytes() for name in SOURCES}
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    report=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,accepted_baseline=base,
                accepted_library_sha256=sha(accepted),
                preceding_twenty_seven_source_build_sha256=parenthash,
                original_sha256=sha(original),
                source_sha256={n:sha(b) for n,b in inputs.items()},
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/fread-full-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                     log_path=path,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1800:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated native fread source worktree')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.lower():p for p in SCRATCH.iterdir() if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all893 actual original CRT library member objects extracted')
            for m in members:
                f=extracted[m.name.lower()]
                need(object_program_records(f.read_bytes())==m.program_records,
                     'untouched original native member program '+m.name)
                destination=SCRATCH/(m.name+'.obj')
                if f!=destination:f.rename(destination)
            for name,raw in inputs.items():
                file=SCRATCH/Path(name).name
                file.write_bytes(raw)
                os.utime(file,(946684800,946684800))
            rsp=build.response(r'probe\frdsrc\newcrt.lib /E',
                ['+probe\\frdsrc\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\frdsrc\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\frdsrc\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\frdsrc\\newcrt.lib'),
            ):
                need(link.count(old)==1,'original independent MAINL link target path')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/fread-full-library.rsp').write_bytes(rsp)
            (ROOT/'.analysis/work/fread-full-link.lnk').write_bytes(link)
            for i in (1,2):
                for name in ('fread.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                generated=(SCRATCH/'fread.obj').read_bytes()
                need(original_scope(generated)==goal,
                     'complete original437 CODE,4 literal fields,2 real functions and native imports')
                sources=dict(preceding[i-1],fread=generated)
                for name,obj in preceding[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(obj)
                run(dos+['tlib',r'@probe\frdsrc\library.rsp'],
                    WORK,f'round{i}-library')
                lib=(SCRATCH/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(lib),sources)
                need(compared['replaced_members']==sorted(sources) and
                     compared['contextual_members_unchanged']==865,
                     '28 original source CRT positions and865 unchanged members')
                run(dos+['tlink',r'@probe\frdsrc\link.lnk'],WORK,f'round{i}-link')
                outputs={}
                for kind,name in (('obj','fread.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    raw=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/fread-full-round{i}-{name}'
                    (ROOT/path).write_bytes(raw)
                    outputs[kind]=dict(path=path,bytes=len(raw),sha256=sha(raw))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'entire original Japanese decoded MAINL EXE and MAP exact with28 source modules')
                report['rounds'].append(dict(round=i,outputs=outputs,
                                             library_comparison=compared))
                save()
                print('28 real source fread+xx Japanese MAINL exact round',i,flush=True)
            need(len(report['rounds'])==2 and
                 {k:q['sha256'] for k,q in report['rounds'][0]['outputs'].items()}==
                 {k:q['sha256'] for k,q in report['rounds'][1]['outputs'].items()},
                 'two equal whole native raw OBJ/LIB/EXE/MAP vectors')
        finally:shutil.rmtree(SCRATCH)
    after,_,otherlib,_,_,afterhash=retained()
    need(after==base and otherlib==accepted and afterhash==parenthash and
         inputs=={name:(ROOT/name).read_bytes() for name in SOURCES},
         'all native input sources,original CRT library and cold pair unchanged')
    report['complete']=True
    save()


if __name__=='__main__':
    main()
