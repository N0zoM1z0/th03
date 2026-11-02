#!/usr/bin/env python3
"""Scoped genuine TASM source and 33-module original Japanese MAINL link.

Important distinction: complete fopen machine CODE and logical OMF fixups
are recovered, but TASM fixup RECORD ORDER differs from original BCC.
This source-only native link is product-exact, not full native OBJ equality.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_fscanf_work as previous
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
SOURCE='src/mainl/crt/fopen.asm'
DRIVER='scripts/build_th03_mainl_fopen_work.py'
REPORT='.analysis/work/mainl-fopen-native-build.json'
ORIGINAL=WORK/'vendor/fopen.obj'
SCRATCH=WORK/'probe/fopsrc'
TASM_FLAGS=['/m','/mx','/kh32768','/t','fopen.asm','fopen.obj']
EXTERNS=['__streams','__nfile','_fclose','_setvbuf','__fmode',
         '_isatty','_open','__exitfopen','__xfclose']
ORIGINAL_SITES=[464,461,436,387,369,318,274,184,182,178,176,156]


def original_scope(obj):
    need(describe_omf(obj)['valid'],'valid complete original/native fopen OMF')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(obj)]==
         [('_TEXT','CODE',556),('_DATA','DATA',0),('_BSS','BSS',0)],
         '556 complete CODE bytes and two empty DATA/BSS owners')
    need(code_publics(obj,1)==[(212,'__OPENFP'),(422,'__GETFP'),(499,'_fopen')] and
         externs(obj)==EXTERNS,
         'native near parser, near OPENFP/GETFP and far fopen interface')
    need([q.data.hex() for q in parse_omf(obj) if q.name=='GRPDEF']==
         ['08ff02ff03'],'native original DATA/BSS group')
    fields=literal_fields(obj)
    need(len(fields)==12 and sorted(f['site'] for f in fields)==sorted(ORIGINAL_SITES),
         'all twelve original CODE-site OMF fields')
    code=bytes(payload(obj)[1,i] for i in range(556))
    return dict(CODE_bytes=556,CODE_sha256=sha(code),
                logical_fields=sorted(fields,key=lambda x:(x['site'],x['location_type'])),
                public=code_publics(obj,1),externs=externs(obj),
                group='08ff02ff03')


def retained():
    base,files,accepted,members,prior31,parenthash=previous.retained()
    raw=(ROOT/previous.REPORT).read_bytes()
    r=json.loads(raw)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_thirty_one_source_build_sha256']==parenthash and
         r['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         r['source_sha256']==sha((ROOT/previous.SOURCE).read_bytes()) and
         len(r['rounds'])==2,'exact unmodified 32-source natural BCC fscanf CRT parent')
    source=[]
    for i,row in enumerate(r['rounds']):
        out={}
        for name,meta in row['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'entire native fscanf '+name+' raw vector')
            out[name]=data
        need(out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'complete original Japanese 32-source EXE and MAP')
        objs=dict(prior31[i],fscanf=out['obj'])
        cmp=compare_members(members,library_members(out['lib']),objs)
        need(cmp['replaced_members']==sorted(objs) and
             cmp['contextual_members_unchanged']==861,
             '32 original source slots and all 861 original context programs')
        source.append(objs)
    need(source[0]==source[1] and len(source[0])==32 and
         len(members)==893 and members[226].name=='fopen',
         'identical 32-source OBJ pair and actual fopen member226')
    return base,files,accepted,members,source,sha(raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,objects,parenthash=retained()
    orig=ORIGINAL.read_bytes()
    need(object_program_records(orig)==members[226].program_records,
         'exact original fopen program records in original accepted library')
    goal=original_scope(orig)
    source=(ROOT/SOURCE).read_bytes()
    original_fields=literal_fields(orig)
    need([f['site'] for f in original_fields]==ORIGINAL_SITES,
         'literal original descending BCC OMF field sites')
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    report=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,complete_native_OMF_equal=False,
                accepted_baseline=base,accepted_library_sha256=sha(accepted),
                previous_thirty_two_source_build_sha256=parenthash,
                original_sha256=sha(orig),source_sha256=sha(source),
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(args,cwd,label):
        p=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/fopen-{label}.log'
        (ROOT/where).write_bytes(p.stdout)
        report['phases'].append(dict(label=label,command=args,returncode=p.returncode,
                                     log_path=where,log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1600:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'new isolated fopen native linker scratch')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            ex={p.stem.lower():p for p in SCRATCH.iterdir() if p.suffix.lower()=='.obj'}
            need(set(ex)=={m.name.lower() for m in members},
                 'all original 893 CRT object members extracted')
            for m in members:
                f=ex[m.name.lower()]
                need(object_program_records(f.read_bytes())==m.program_records,
                     'original untouched CRT member '+m.name)
                dest=SCRATCH/(m.name+'.obj')
                if f!=dest:f.rename(dest)
            (SCRATCH/'fopen.asm').write_bytes(source)
            os.utime(SCRATCH/'fopen.asm',(946684800,946684800))
            response=build.response(r'probe\fopsrc\newcrt.lib /E',
                ['+probe\\fopsrc\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\fopsrc\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\fopsrc\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\fopsrc\\newcrt.lib'),
            ):
                need(link.count(old)==1,'actual normal MAINL linker input/output')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(response)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/fopen-library.rsp').write_bytes(response)
            (ROOT/'.analysis/work/fopen-link.lnk').write_bytes(link)
            for i in (1,2):
                for filename in ('fopen.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/filename).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                obj=(SCRATCH/'fopen.obj').read_bytes()
                need(original_scope(obj)==goal,
                     'all fopen CODE, 12 logical OMF fields, original symbols/group')
                f=literal_fields(obj)
                need(f!=original_fields and
                     [x['site'] for x in f]==sorted(ORIGINAL_SITES),
                     'literal native fixup writer order still OPEN and explicitly distinct')
                repl=dict(objects[i-1],fopen=obj)
                for name,data in objects[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(data)
                run(dos+['tlib',r'@probe\fopsrc\library.rsp'],WORK,
                    f'round{i}-library')
                compared=compare_members(members,library_members((SCRATCH/'newcrt.lib').read_bytes()),repl)
                need(compared['replaced_members']==sorted(repl) and
                     compared['contextual_members_unchanged']==860,
                     '33 original source modules and860 unmodified CRT programs')
                run(dos+['tlink',r'@probe\fopsrc\link.lnk'],WORK,
                    f'round{i}-link')
                out={}
                for kind,filename in (('obj','fopen.obj'),('lib','newcrt.lib'),
                                      ('exe','linked.exe'),('map','linked.map')):
                    blob=(SCRATCH/filename).read_bytes()
                    path=f'.analysis/work/fopen-round{i}-{filename}'
                    (ROOT/path).write_bytes(blob)
                    out[kind]=dict(path=path,bytes=len(blob),sha256=sha(blob))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'whole original Japanese MAINL decoded EXE and MAP raw-equal')
                report['rounds'].append(dict(round=i,outputs=out,
                                             library_comparison=compared))
                save()
                print('33-source fopen product-only EXE/MAP exact round',i,flush=True)
            need({k:q['sha256'] for k,q in report['rounds'][0]['outputs'].items()}==
                 {k:q['sha256'] for k,q in report['rounds'][1]['outputs'].items()},
                 'two byte-identical real TASM/TLIB/TLINK output vectors')
        finally:shutil.rmtree(SCRATCH)
    again,_,accepted2,_,_,afterhash=retained()
    need(again==base and accepted2==accepted and afterhash==parenthash and
         source==(ROOT/SOURCE).read_bytes(),'fixed parent original CRT and source unchanged')
    report['complete']=True
    save()


if __name__=='__main__':
    main()
