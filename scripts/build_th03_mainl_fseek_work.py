#!/usr/bin/env python3
"""Build the actual 492-byte Borland DOS fseek from maintained 8086 source.

This is the complete 492-byte DOS seek/tell translation unit: one near
text-mode buffer offset calculator plus two public far functions.
The original 893-member CRT is reconstructed in its original order,
with 30 preceding exact source CRT members retained.
The cold pair and accepted 28-provider publication are not rebuilt.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_getc_work as parent
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
SOURCES=('src/mainl/crt/fseek.asm',)
DRIVER='scripts/build_th03_mainl_fseek_work.py'
REPORT='.analysis/work/mainl-fseek-native-build.json'
SCRATCH=WORK/'probe/fsksrc'
ORIGINAL=WORK/'vendor/fseek.obj'
TASM_FLAGS=['/m','/mx','/kh32768','/t','fseek.asm','fseek.obj']
LAYOUT='src/mainl/crt/stdio_layout.inc'


def original_scope(obj):
    need(describe_omf(obj)['valid'],'valid complete original DOS fseek/ftell OMF')
    need([(x['name'],x['class'],x['size']) for x in segment_definitions(obj)]==
         [('_TEXT','CODE',492),('_DATA','DATA',0),('_BSS','BSS',0)],
         '492 original native CODE bytes, zero DATA/BSS')
    need(code_publics(obj,1)==[(137,'_fseek'),(267,'_ftell')] and
         externs(obj)==['_fflush','_lseek','__openfd'],
         'original private near buffered helper and two public far cdecl entries')
    need([r.data.hex() for r in parse_omf(obj) if r.name=='GRPDEF']==
         ['08ff02ff03'],'original DATA-before-BSS GRPDEF')
    fields=literal_fields(obj)
    need([(f['site'],f['target_method'],f['target'],f['frame_method'],f['addend'])
          for f in fields]==
         [(342,2,3,1,1),(149,2,1,5,0),(239,2,2,5,0),
          (293,2,2,5,0),(365,2,2,5,0),(409,2,2,5,0)],
         'literal ordered six original fseek/ftell import and DATA references')
    p=payload(obj)
    return dict(CODE_bytes=492,
                CODE_sha256=sha(bytes(p[1,i] for i in range(492))),
                native_ordered_fields=fields,imports=externs(obj),
                original_public_offsets=[137,267],
                original_function_boundaries=(0,137,267,492))


def retained():
    base,files,accepted,members,preceding29,parenthash=parent.retained()
    receipt=(ROOT/parent.REPORT).read_bytes()
    report=json.loads(receipt)
    need(report['complete'] and not report['source_acceptance'] and
         report['added_accepted_bytes']==0 and not report['original_cold_rebuilt'] and
         report['accepted_baseline']==base and
         report['accepted_library_sha256']==sha(accepted) and
         report['previous_twenty_nine_source_build_sha256']==parenthash and
         report['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         report['source_sha256']=={n:sha((ROOT/n).read_bytes()) for n in parent.SOURCES} and
         len(report['rounds'])==2,
         'complete original30-source native getc/fwrite CRT provenance')
    original=[]
    for i,row in enumerate(report['rounds']):
        outs={}
        for kind,meta in row['outputs'].items():
            blob=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                 'complete preceding 30-source native '+kind+' byte vector')
            outs[kind]=blob
        need(outs['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outs['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'original full Japanese EXE/MAP from thirty source members')
        sources=dict(preceding29[i],getc=outs['obj'])
        cmp=compare_members(members,library_members(outs['lib']),sources)
        need(cmp['replaced_members']==sorted(sources) and
             cmp['contextual_members_unchanged']==863,
             '30 original source members and863 wholly unchanged vendor programs')
        original.append(sources)
    need(original[0]==original[1] and len(original[0])==30 and
         len(members)==893 and members[232].name=='fseek',
         'two identical source object vectors and actual fseek member index232')
    return base,files,accepted,members,original,sha(receipt)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,preceding,parenthash=retained()
    original=ORIGINAL.read_bytes()
    theadr=next(iter(parse_omf(original)))
    header=original[theadr.offset:theadr.offset+theadr.length+3]
    selected_original=header+members[232].program_records
    goal=original_scope(selected_original)
    standalone_fields=literal_fields(original)
    selected_fields=literal_fields(selected_original)
    need(sha(bytes(payload(original)[1,i] for i in range(492)))==
         goal['CODE_sha256'] and
         sorted(standalone_fields,key=lambda f:f['site'])==
         sorted(selected_fields,key=lambda f:f['site']) and
         standalone_fields!=selected_fields,
         'two original CRT/standalone fseek variants: equal CODE and fields, different order')
    inputs={name:(ROOT/name).read_bytes() for name in SOURCES}
    layout=(ROOT/LAYOUT).read_bytes()
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
                previous_thirty_source_build_sha256=parenthash,
                original_sha256=sha(original),
                selected_original_member_sha256=sha(members[232].program_records),
                original_standalone_fixup_sites=[f['site'] for f in standalone_fields],
                original_selected_member_fixup_sites=[f['site'] for f in selected_fields],
                layout_sha256=sha(layout),
                source_sha256={n:sha(b) for n,b in inputs.items()},
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/fseek-full-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                     log_path=path,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1800:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated native fseek source worktree')
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
            (SCRATCH/'stdio_layout.inc').write_bytes(layout)
            rsp=build.response(r'probe\fsksrc\newcrt.lib /E',
                ['+probe\\fsksrc\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\fsksrc\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\fsksrc\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\fsksrc\\newcrt.lib'),
            ):
                need(link.count(old)==1,'original independent MAINL link target path')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/fseek-full-library.rsp').write_bytes(rsp)
            (ROOT/'.analysis/work/fseek-full-link.lnk').write_bytes(link)
            for i in (1,2):
                for name in ('fseek.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                generated=(SCRATCH/'fseek.obj').read_bytes()
                need(original_scope(generated)==goal,
                     'complete original492 CODE, six ordered literal native OMF fields and two far entries')
                sources=dict(preceding[i-1],fseek=generated)
                for name,obj in preceding[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(obj)
                run(dos+['tlib',r'@probe\fsksrc\library.rsp'],
                    WORK,f'round{i}-library')
                lib=(SCRATCH/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(lib),sources)
                need(compared['replaced_members']==sorted(sources) and
                     compared['contextual_members_unchanged']==862,
                     '31 original native source members and862 unchanged CRT programs')
                run(dos+['tlink',r'@probe\fsksrc\link.lnk'],WORK,f'round{i}-link')
                outputs={}
                for kind,name in (('obj','fseek.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    raw=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/fseek-full-round{i}-{name}'
                    (ROOT/path).write_bytes(raw)
                    outputs[kind]=dict(path=path,bytes=len(raw),sha256=sha(raw))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'whole original Japanese MAINL EXE/MAP exact with31 source modules')
                report['rounds'].append(dict(round=i,outputs=outputs,
                                             library_comparison=compared))
                save()
                print('31 real native fseek/ftell source Japanese MAINL exact round',i,flush=True)
            need(len(report['rounds'])==2 and
                 {k:q['sha256'] for k,q in report['rounds'][0]['outputs'].items()}==
                 {k:q['sha256'] for k,q in report['rounds'][1]['outputs'].items()},
                 'two equal whole native raw OBJ/LIB/EXE/MAP vectors')
        finally:shutil.rmtree(SCRATCH)
    after,_,otherlib,_,_,afterhash=retained()
    need(after==base and otherlib==accepted and afterhash==parenthash and
         inputs=={name:(ROOT/name).read_bytes() for name in SOURCES} and
         layout==(ROOT/LAYOUT).read_bytes(),
         'all native input sources,original CRT library and cold pair unchanged')
    report['complete']=True
    save()


if __name__=='__main__':
    main()
