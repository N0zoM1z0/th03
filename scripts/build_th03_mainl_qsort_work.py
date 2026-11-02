#!/usr/bin/env python3
"""Build the actual 756-byte Borland DOS qsort from maintained 8086 source.

This is the COMPLETE qsort TU, including its original 46-byte swap,
666-byte median/partition/recursive near sorter and 44-byte far entry.
The original 893-member CRT is reconstructed in its original order,
with sixteen independent already-proven source modules retained.
The cold pair and accepted 28-provider publication are not rebuilt.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_strnset_work as parent
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
SOURCES=('src/mainl/crt/qsort.asm','src/mainl/crt/qswap.inl',
         'src/mainl/crt/qcore.inl','src/mainl/crt/qentry.inl')
DRIVER='scripts/build_th03_mainl_qsort_work.py'
REPORT='.analysis/work/mainl-qsort-native-build.json'
SCRATCH=WORK/'probe/qsfusrc'
ORIGINAL=WORK/'vendor/qsort.obj'
TASM_FLAGS=['/m','/mx','/kh32768','/t','qsort.asm','qsort.obj']


def original_scope(obj):
    need(describe_omf(obj)['valid'],'valid real original qsort OMF program')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(obj)]==
         [('_TEXT','CODE',756),('_DATA','DATA',0),('_BSS','BSS',6)],
         'entire 756-byte CODE and six real original BSS bytes')
    need(code_publics(obj,1)==[(712,'_qsort')] and
         externs(obj)==['N_LXMUL@','N_LDIV@'],
         'original public far entry and literal two arithmetic import names')
    need([x.data for x in parse_omf(obj) if x.name=='GRPDEF']==
         [bytes.fromhex('08ff03ff02')],
         'original qsort BSS-before-DATA group record')
    fields=literal_fields(obj)
    need(len(fields)==29 and [q['site'] for q in fields if not 46<=q['site']<712]==
         [9,721,735,738],'all original qsort OMF fields including both outer helpers')
    p=payload(obj)
    code=bytes(p[1,i] for i in range(756))
    return dict(CODE_bytes=756,CODE_sha256=sha(code),
                literal_ordered_fields=fields,imports=externs(obj),
                far_public_offset=712,BSS_bytes=6,
                original_helper_boundaries=(0,46,712,756))


def retained():
    base,files,accepted,members,previous15,oldhash=parent.retained()
    receipt=(ROOT/parent.REPORT).read_bytes()
    r=json.loads(receipt)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_fifteen_source_build_sha256']==oldhash and
         r['source_sha256']==sha((ROOT/parent.SOURCE).read_bytes()) and
         r['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         len(r['rounds'])==2,
         'unchanged original sixteen-source natural CRT carrier')
    variants=[]
    for i,row in enumerate(r['rounds']):
        outputs={}
        for kind,meta in row['outputs'].items():
            raw=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(raw),sha256=sha(raw)),
                 'unchanged complete sixteen-source raw '+kind)
            outputs[kind]=raw
        need(outputs['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'verified 16-source whole Japanese decoded EXE/MAP exact')
        sources=dict(previous15[i],strnset=outputs['obj'])
        comparison=compare_members(members,library_members(outputs['lib']),sources)
        need(comparison['replaced_members']==[m.name for m in members if m.name in sources] and
             comparison['contextual_members_unchanged']==877,
             'sixteen actual original-position source modules plus877 vendor programs')
        variants.append(sources)
    need(variants[0]==variants[1] and len(members)==893 and
         members[275].name=='qsort',
         'same16 genuine source OBJ vectors and original qsort slot275')
    return base,files,accepted,members,variants,sha(receipt)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,preceding,parenthash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[275].program_records,
         'original complete 756-byte qsort object at its library slot')
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
                preceding_sixteen_source_build_sha256=parenthash,
                original_sha256=sha(original),
                source_sha256={n:sha(b) for n,b in inputs.items()},
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/qsort-full-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                     log_path=path,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1800:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated native qsort source worktree')
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
            rsp=build.response(r'probe\qsfusrc\newcrt.lib /E',
                ['+probe\\qsfusrc\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\qsfusrc\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\qsfusrc\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\qsfusrc\\newcrt.lib'),
            ):
                need(link.count(old)==1,'original independent MAINL link target path')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/qsort-full-library.rsp').write_bytes(rsp)
            (ROOT/'.analysis/work/qsort-full-link.lnk').write_bytes(link)
            for i in (1,2):
                for name in ('qsort.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                generated=(SCRATCH/'qsort.obj').read_bytes()
                need(original_scope(generated)==goal,
                     'complete original756 CODE,29 literal OMF fields,interfaces and6 BSS')
                sources=dict(preceding[i-1],qsort=generated)
                for name,obj in preceding[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(obj)
                run(dos+['tlib',r'@probe\qsfusrc\library.rsp'],
                    WORK,f'round{i}-library')
                lib=(SCRATCH/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(lib),sources)
                need(compared['replaced_members']==[m.name for m in members if m.name in sources] and
                     compared['contextual_members_unchanged']==876,
                     'seventeen real original source CRT positions and876 unchanged members')
                run(dos+['tlink',r'@probe\qsfusrc\link.lnk'],WORK,f'round{i}-link')
                outputs={}
                for kind,name in (('obj','qsort.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    raw=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/qsort-full-round{i}-{name}'
                    (ROOT/path).write_bytes(raw)
                    outputs[kind]=dict(path=path,bytes=len(raw),sha256=sha(raw))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'entire real Japanese decoded MAINL EXE and MAP exact with17 sources')
                report['rounds'].append(dict(round=i,outputs=outputs,
                                             library_comparison=compared))
                save()
                print('17 natural source qsort+xx Japanese MAINL exact round',i,flush=True)
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
