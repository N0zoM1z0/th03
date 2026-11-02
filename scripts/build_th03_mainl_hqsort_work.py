#!/usr/bin/env python3
"""Build the actual 916-byte Borland DOS hqsort from maintained 8086 source.

This is the COMPLETE hqsort TU, including its original 46-byte swap,
666-byte median/partition/recursive near sorter and 44-byte far entry.
The original 893-member CRT is reconstructed in its original order,
with seventeen previously proven genuine source modules retained.
The cold pair and accepted 28-provider publication are not rebuilt.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_qsort_work as parent
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
SOURCES=('src/mainl/crt/hqsort.asm','src/mainl/crt/qswap.inl',
         'src/mainl/crt/hqcore.inl','src/mainl/crt/hqentry.inl')
DRIVER='scripts/build_th03_mainl_hqsort_work.py'
REPORT='.analysis/work/mainl-hqsort-native-build.json'
SCRATCH=WORK/'probe/hqfusrc'
ORIGINAL=WORK/'vendor/hqsort.obj'
TASM_FLAGS=['/m','/mx','/kh32768','/t','hqsort.asm','hqsort.obj']


def original_scope(obj):
    need(describe_omf(obj)['valid'],'valid real original hqsort OMF program')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(obj)]==
         [('_TEXT','CODE',916),('_DATA','DATA',0),('_BSS','BSS',6)],
         'entire 916-byte CODE and six original BSS bytes')
    need(code_publics(obj,1)==[(872,'__hqsort')] and
         externs(obj)==['N_PADD@','N_LXMUL@','N_PADA@','N_PCMP@',
                        'N_PSBA@','N_PSUB@','N_PSBP@','N_LDIV@'],
         'original public far entry and literal two arithmetic import names')
    need([x.data for x in parse_omf(obj) if x.name=='GRPDEF']==
         [bytes.fromhex('08ff03ff02')],
         'original hqsort BSS-before-DATA group record')
    fields=literal_fields(obj)
    need(len(fields)==52 and [q['site'] for q in fields if not 46<=q['site']<872]==
         [9,881,895,898],'all original hqsort OMF fields including both outer helpers')
    p=payload(obj)
    code=bytes(p[1,i] for i in range(916))
    return dict(CODE_bytes=916,CODE_sha256=sha(code),
                literal_ordered_fields=fields,imports=externs(obj),
                far_public_offset=872,BSS_bytes=6,
                original_helper_boundaries=(0,46,872,916))


def retained():
    base,files,accepted,members,preceding16,parentsha=parent.retained()
    receipt=(ROOT/parent.REPORT).read_bytes()
    r=json.loads(receipt)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['preceding_sixteen_source_build_sha256']==parentsha and
         r['source_sha256']=={name:sha((ROOT/name).read_bytes()) for name in parent.SOURCES} and
         r['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         len(r['rounds'])==2,
         'verified unchanged full qsort native source and seventeen-source original CRT')
    objects=[]
    for i,row in enumerate(r['rounds']):
        outputs={}
        for kind,meta in row['outputs'].items():
            raw=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(raw),sha256=sha(raw)),
                 'complete original qsort source output '+kind)
            outputs[kind]=raw
        need(outputs['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'prior seventeen-source complete original Japanese MAINL and MAP')
        src=dict(preceding16[i],qsort=outputs['obj'])
        compared=compare_members(members,library_members(outputs['lib']),src)
        need(compared['replaced_members']==[m.name for m in members if m.name in src] and
             compared['contextual_members_unchanged']==876,
             'original seventeen source programs and876 untouched vendor members')
        objects.append(src)
    need(objects[0]==objects[1] and len(members)==893 and
         members[464].name=='hqsort',
         'two identical complete source pairs and original high sort member index464')
    return base,files,accepted,members,objects,sha(receipt)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,preceding,parenthash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[464].program_records,
         'original complete 916-byte hqsort object at its library slot')
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
                preceding_seventeen_source_build_sha256=parenthash,
                original_sha256=sha(original),
                source_sha256={n:sha(b) for n,b in inputs.items()},
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/hqsort-full-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                     log_path=path,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1800:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated native hqsort source worktree')
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
            rsp=build.response(r'probe\hqfusrc\newcrt.lib /E',
                ['+probe\\hqfusrc\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\hqfusrc\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\hqfusrc\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\hqfusrc\\newcrt.lib'),
            ):
                need(link.count(old)==1,'original independent MAINL link target path')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/hqsort-full-library.rsp').write_bytes(rsp)
            (ROOT/'.analysis/work/hqsort-full-link.lnk').write_bytes(link)
            for i in (1,2):
                for name in ('hqsort.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                generated=(SCRATCH/'hqsort.obj').read_bytes()
                need(original_scope(generated)==goal,
                     'complete original916 CODE,52 literal OMF fields,interfaces and6 BSS')
                sources=dict(preceding[i-1],hqsort=generated)
                for name,obj in preceding[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(obj)
                run(dos+['tlib',r'@probe\hqfusrc\library.rsp'],
                    WORK,f'round{i}-library')
                lib=(SCRATCH/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(lib),sources)
                need(compared['replaced_members']==sorted(sources) and
                     compared['contextual_members_unchanged']==875,
                     'eighteen real original source CRT positions and875 unchanged members')
                run(dos+['tlink',r'@probe\hqfusrc\link.lnk'],WORK,f'round{i}-link')
                outputs={}
                for kind,name in (('obj','hqsort.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    raw=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/hqsort-full-round{i}-{name}'
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
                print('18 genuine source high-sort+xx Japanese MAINL exact round',i,flush=True)
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
