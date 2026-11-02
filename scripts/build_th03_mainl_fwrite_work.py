#!/usr/bin/env python3
"""Build the actual 153-byte Borland DOS fwrite from maintained 8086 source.

This is the complete 153-byte native far fwrite TU with three
genuine near imported buffering and large-pointer arithmetic helpers.
The original 893-member CRT is reconstructed in its original order,
with 28 preceding exact source CRT members retained.
The cold pair and accepted 28-provider publication are not rebuilt.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_fread_work as parent
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
SOURCES=('src/mainl/crt/fwrite.asm',)
DRIVER='scripts/build_th03_mainl_fwrite_work.py'
REPORT='.analysis/work/mainl-fwrite-native-build.json'
SCRATCH=WORK/'probe/fwtsrc'
ORIGINAL=WORK/'vendor/fwrite.obj'
TASM_FLAGS=['/m','/mx','/kh32768','/t','fwrite.asm','fwrite.obj']


def original_scope(obj):
    need(describe_omf(obj)['valid'],'valid actual original 153-byte fwrite OMF')
    need([(x['name'],x['class'],x['size']) for x in segment_definitions(obj)]==
         [('_TEXT','CODE',153),('_DATA','DATA',0),('_BSS','BSS',0)],
         'full original fwrite CODE and empty DATA/BSS')
    need(code_publics(obj,1)==[(0,'_fwrite')] and
         externs(obj)==['__FPUTN','N_LXMUL@','N_PADD@'],
         'original far write public and three genuine near helpers')
    need([r.data.hex() for r in parse_omf(obj) if r.name=='GRPDEF']==
         ['08ff03ff02'],'original BSS-before-DATA group')
    fields=literal_fields(obj)
    need([(f['site'],f['target_method'],f['target'],f['frame_method']) for f in fields]==
         [(28,2,2,0),(63,2,1,0),(95,2,1,0),(125,2,3,0)],
         'all four original ordered near helper OMF FIXUPPs')
    p=payload(obj)
    return dict(CODE_bytes=153,CODE_sha256=sha(bytes(p[1,i] for i in range(153))),
                literal_ordered_fields=fields,imports=externs(obj),
                public_offset=0,original_helper_boundaries=(0,153))


def retained():
    base,files,accepted,members,prior27,oldhash=parent.retained()
    receipt=(ROOT/parent.REPORT).read_bytes()
    report=json.loads(receipt)
    need(report['complete'] and not report['source_acceptance'] and
         report['added_accepted_bytes']==0 and not report['original_cold_rebuilt'] and
         report['accepted_baseline']==base and
         report['accepted_library_sha256']==sha(accepted) and
         report['preceding_twenty_seven_source_build_sha256']==oldhash and
         report['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         report['source_sha256']=={n:sha((ROOT/n).read_bytes()) for n in parent.SOURCES} and
         len(report['rounds'])==2,
         'complete original 28-source fread native CRT and unchanged provenance')
    pairs=[]
    for idx,row in enumerate(report['rounds']):
        out={}
        for kind,meta in row['outputs'].items():
            blob=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                 'literal previous native fwrite predecessor '+kind+' bytes')
            out[kind]=blob
        need(out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'whole previous Japanese MAINL original EXE and MAP byte exact')
        sources=dict(prior27[idx],fread=out['obj'])
        cmp=compare_members(members,library_members(out['lib']),sources)
        need(cmp['replaced_members']==sorted(sources) and
             cmp['contextual_members_unchanged']==865,
             '28 real original source programs and 865 original member contexts')
        pairs.append(sources)
    need(pairs[0]==pairs[1] and len(pairs[0])==28 and
         len(members)==893 and members[236].name=='fwrite',
         'actual original fwrite library index and identical 28-source pair')
    return base,files,accepted,members,pairs,sha(receipt)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,preceding,parenthash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[236].program_records,
         'original complete 153-byte fwrite object at its library slot')
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
                previous_twenty_eight_source_build_sha256=parenthash,
                original_sha256=sha(original),
                source_sha256={n:sha(b) for n,b in inputs.items()},
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/fwrite-full-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                     log_path=path,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1800:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated native fwrite source worktree')
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
            rsp=build.response(r'probe\fwtsrc\newcrt.lib /E',
                ['+probe\\fwtsrc\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\fwtsrc\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\fwtsrc\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\fwtsrc\\newcrt.lib'),
            ):
                need(link.count(old)==1,'original independent MAINL link target path')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/fwrite-full-library.rsp').write_bytes(rsp)
            (ROOT/'.analysis/work/fwrite-full-link.lnk').write_bytes(link)
            for i in (1,2):
                for name in ('fwrite.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                generated=(SCRATCH/'fwrite.obj').read_bytes()
                need(original_scope(generated)==goal,
                     'complete original153 CODE and all4 literal near-helper OMF fields')
                sources=dict(preceding[i-1],fwrite=generated)
                for name,obj in preceding[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(obj)
                run(dos+['tlib',r'@probe\fwtsrc\library.rsp'],
                    WORK,f'round{i}-library')
                lib=(SCRATCH/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(lib),sources)
                need(compared['replaced_members']==sorted(sources) and
                     compared['contextual_members_unchanged']==864,
                     '29 original source CRT positions and864 unchanged members')
                run(dos+['tlink',r'@probe\fwtsrc\link.lnk'],WORK,f'round{i}-link')
                outputs={}
                for kind,name in (('obj','fwrite.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    raw=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/fwrite-full-round{i}-{name}'
                    (ROOT/path).write_bytes(raw)
                    outputs[kind]=dict(path=path,bytes=len(raw),sha256=sha(raw))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'entire original Japanese decoded MAINL EXE/MAP exact with29 original sources')
                report['rounds'].append(dict(round=i,outputs=outputs,
                                             library_comparison=compared))
                save()
                print('29 real source fwrite+fread Japanese MAINL exact round',i,flush=True)
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
