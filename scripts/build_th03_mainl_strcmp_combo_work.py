#!/usr/bin/env python3
"""Three-source native DOS CRT memory bank: memcpy, memcmp, strcmp.

Rebuild only strcmp and verify the entire original Japanese decoded MAINL
EXE/MAP, reusing the two previously reviewed source-only working library pairs.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_work as build
import build_th03_mainl_memcpy_work as memcpy
import build_th03_mainl_memcmp_combo_work as memcmp
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.omf import describe_omf,parse_omf
from lib.borland_library import library_members,compare_members,object_program_records
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs

ROOT=Path(__file__).resolve().parents[1]
SOURCE='src/mainl/crt/strcmp.asm'
DRIVER='scripts/build_th03_mainl_strcmp_combo_work.py'
REPORT='.analysis/work/mainl-strcmp-combo-build.json'
SCRATCH=build.WORK/'probe/scmcombo'
VENDOR_OBJ=build.WORK/'vendor/strcmp.obj'


def native_scope(obj):
    segs=segment_definitions(obj)
    need([(s['name'],s['class'],s['size']) for s in segs] ==
         [('_TEXT','CODE',48),('_DATA','DATA',0),('_BSS','BSS',0)],
         'original native48-byte CODE and zero DATA/BSS extents')
    need(code_publics(obj,1)==[(0,'_strcmp')] and
         not externs(obj) and not literal_fields(obj) and describe_omf(obj)['valid'],
         'one far strcmp native public and no OMF relocations/imports')
    need([r.data for r in parse_omf(obj) if r.name=='GRPDEF'] ==
         [bytes.fromhex('08FF03FF02')],
         'original empty BSS/DATA GRPDEF member order')
    p=payload(obj)
    return bytes(p[1,i] for i in range(48))


def existing_memory_sources():
    base,files,accepted,members,mcp_lib,mcp_obj,mcp_hash=memcmp.inherited_library()
    raw=(ROOT/memcmp.REPORT).read_bytes()
    receipt=json.loads(raw)
    need(receipt['complete'] and not receipt['source_acceptance'] and
         receipt['added_accepted_bytes']==0 and
         receipt['source_sha256']==sha((ROOT/memcmp.SOURCE).read_bytes()) and
         receipt['driver_sha256']==sha((ROOT/memcmp.DRIVER).read_bytes()) and
         receipt['memcpy_producer_sha256']==mcp_hash and
         receipt['accepted_baseline']==base and
         receipt['accepted_library_sha256']==sha(accepted) and
         len(receipt['rounds'])==2,
         'unchanged current two-source native memcmp source pair')
    rawlib=(ROOT/receipt['rounds'][0]['outputs']['lib']['path']).read_bytes()
    obj=(ROOT/receipt['rounds'][0]['outputs']['obj']['path']).read_bytes()
    need(memcmp.native_scope(obj)==memcmp.native_scope(memcmp.ORIGINAL.read_bytes()),
         'native40-byte memcmp member remains exact')
    for round in receipt['rounds']:
        for kind in ('obj','lib','exe','map'):
            out=round['outputs'][kind]
            data=(ROOT/out['path']).read_bytes()
            need(out==dict(path=out['path'],bytes=len(data),sha256=sha(data)),
                 'complete reused two-source native '+kind)
        need({k:v['sha256'] for k,v in round['outputs'].items()}==
             {k:v['sha256'] for k,v in receipt['rounds'][0]['outputs'].items()},
             'same complete native two-source raw pair')
    cmp=compare_members(members,library_members(rawlib),
                        {'memcmp':obj,'memcpy':mcp_obj})
    need(cmp['replaced_members']==['memcmp','memcpy'] and
         cmp['contextual_members_unchanged']==891,
         'two original native source providers retain original member order')
    return base,files,accepted,members,rawlib,mcp_obj,obj,sha(raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,library,memcpy_obj,memcmp_obj,prev_hash=existing_memory_sources()
    need(len(members)==893 and
         [(i,m.name) for i,m in enumerate(members)
          if m.name in ('memcpy','memcmp','strcmp')]==
         [(260,'memcmp'),(261,'memcpy'),(292,'strcmp')],
         'three distinct original CRT member positions')
    original=VENDOR_OBJ.read_bytes()
    need(object_program_records(original)==members[292].program_records,
         'original source ownership and library identity')
    target_code=native_scope(original)
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    report=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,accepted_baseline=base,
                accepted_library_sha256=sha(accepted),
                preceding_memcmp_producer_sha256=prev_hash,
                original_member_sha256=sha(original),
                source_sha256=sha(source),driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(argv,cwd,label):
        result=subprocess.run(argv,cwd=cwd,env=env,
                              stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/strcmp-combo-{label}.log'
        (ROOT/where).write_bytes(result.stdout)
        report['phases'].append(dict(label=label,returncode=result.returncode,
                                     command=argv,log_path=where,log_sha256=sha(result.stdout)))
        save()
        need(result.returncode==0,label+':'+result.stdout.decode(errors='replace')[-1600:])

    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated native strcmp scratch')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(library)
            extract=build.response('base.lib',['*'+m.name for m in members])
            (SCRATCH/'extract.rsp').write_bytes(extract)
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            current_members=library_members(library)
            extracted={p.stem.casefold():p for p in SCRATCH.iterdir()
                       if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.casefold() for m in members},
                 'all893 current native source members extracted')
            for m in current_members:
                existing=extracted[m.name.casefold()]
                need(object_program_records(existing.read_bytes())==m.program_records,
                     'exact current native member: '+m.name)
                dest=SCRATCH/(m.name+'.obj')
                if existing!=dest:existing.rename(dest)
            (SCRATCH/'strcmp.asm').write_bytes(source)
            os.utime(SCRATCH/'strcmp.asm',(946684800,946684800))
            rsp=build.response(r'probe\scmcombo\newcrt.lib /E',
                ['+probe\\scmcombo\\'+m.name+'.obj' for m in members])
            link=memcpy.link_response(files)
            for old,new in ((b'probe\\mcpctx\\linked.exe',b'probe\\scmcombo\\linked.exe'),
                            (b'probe\\mcpctx\\linked.map',b'probe\\scmcombo\\linked.map'),
                            (b'probe\\mcpctx\\newcrt.lib',b'probe\\scmcombo\\newcrt.lib')):
                need(link.count(old)==1,'one real source-link output path')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/strcmp-combo-library.rsp').write_bytes(rsp)
            (ROOT/'.analysis/work/strcmp-combo-link.lnk').write_bytes(link)
            for number in (1,2):
                for name in ('strcmp.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(tasm+['/m','/mx','/kh32768','/t','strcmp.asm','strcmp.obj'],
                    SCRATCH,f'round{number}-assemble')
                obj=(SCRATCH/'strcmp.obj').read_bytes()
                need(native_scope(obj)==target_code,'complete48-byte original comparator')
                run(dos+['tlib',r'@probe\scmcombo\library.rsp'],
                    build.WORK,f'round{number}-library')
                newlib=(SCRATCH/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(newlib),
                    {'memcmp':memcmp_obj,'memcpy':memcpy_obj,'strcmp':obj})
                need(compared['replaced_members']==['memcmp','memcpy','strcmp'] and
                     compared['contextual_members_unchanged']==890,
                     'three authentic natural source owners,890 unchanged originals')
                run(dos+['tlink',r'@probe\scmcombo\link.lnk'],
                    build.WORK,f'round{number}-link')
                outputs={}
                for kind,name in [('obj','strcmp.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')]:
                    raw=(SCRATCH/name).read_bytes()
                    where=f'.analysis/work/strcmp-combo-round{number}-{name}'
                    (ROOT/where).write_bytes(raw)
                    outputs[kind]=dict(path=where,bytes=len(raw),sha256=sha(raw))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (build.WORK/'bin/th03/mainl.target.exe').read_bytes(),
                     'full original Japanese MAINL EXE raw equal with three native sources')
                need((SCRATCH/'linked.map').read_bytes()==
                     (build.WORK/'obj/th03/mainl.map').read_bytes(),
                     'full original Japanese MAINL MAP raw equal with three native sources')
                report['rounds'].append(dict(round=number,outputs=outputs,
                    library_comparison=compared,native_CODE_sha256=sha(target_code)))
                save()
                print('MAINL memcpy+memcmp+strcmp exact native link round',number,flush=True)
            need({k:v['sha256'] for k,v in report['rounds'][0]['outputs'].items()}==
                 {k:v['sha256'] for k,v in report['rounds'][1]['outputs'].items()},
                 'two complete repeatable raw OBJ/LIB/EXE/MAP vectors')
        finally:shutil.rmtree(SCRATCH)
    again=existing_memory_sources()
    need(again[0]==base and again[2]==accepted and again[4]==library and
         again[7]==prev_hash and (ROOT/SOURCE).read_bytes()==source,
         'accepted library and all previous source-only producers unchanged')
    report['complete']=True
    save()


if __name__=='__main__':main()
