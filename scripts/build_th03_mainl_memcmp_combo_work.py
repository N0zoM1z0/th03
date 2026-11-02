#!/usr/bin/env python3
"""Recover DOS memcmp alongside the retained native memcpy source library.

Only the original memcmp object is assembled; all 893 member slots are relinked
in native TLIB order. Neither the accepted cold build nor its vendor inputs change.
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
from build_th03_mainl_resources_work import need, sha
from build_th03_mainl_display_work import payload, literal_fields
from lib.omf import describe_omf, parse_omf
from lib.borland_library import library_members, compare_members, object_program_records
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs

ROOT=Path(__file__).resolve().parents[1]
SOURCE='src/mainl/crt/memcmp.asm'
DRIVER='scripts/build_th03_mainl_memcmp_combo_work.py'
REPORT='.analysis/work/mainl-memcmp-combo-build.json'
SCRATCH=build.WORK/'probe/mmcombo'
ORIGINAL=build.WORK/'vendor/memcmp.obj'


def native_scope(obj):
    segments=segment_definitions(obj)
    need([(s['name'],s['class'],s['size']) for s in segments] ==
         [('_TEXT','CODE',40),('_DATA','DATA',0),('_BSS','BSS',0)],
         'one native40-byte CODE scope and two empty CRT segments')
    need(code_publics(obj,1)==[(0,'_memcmp')] and not externs(obj) and
         not literal_fields(obj) and describe_omf(obj)['valid'],
         'complete native far comparator interface,zero ordered fixups')
    need([r.data for r in parse_omf(obj) if r.name=='GRPDEF'] ==
         [bytes.fromhex('08FF03FF02')],
         'original BSS-before-DATA group ownership')
    p=payload(obj)
    return bytes(p[1,i] for i in range(40))


def inherited_library():
    baseline,files,lib,members,_=memcpy.baseline_provider.baseline(ROOT)
    meta=json.loads((ROOT/memcpy.REPORT).read_bytes())
    need(meta['complete'] and not meta['source_acceptance'] and
         meta['source_sha256']==sha((ROOT/memcpy.SOURCE).read_bytes()) and
         meta['driver_sha256']==sha((ROOT/memcpy.DRIVER).read_bytes()) and
         meta['current_library_sha256']==sha(lib) and
         meta['reused_accepted_library']==baseline and len(meta['rounds'])==2,
         'current reviewed36-byte memcpy source producer')
    raw=(ROOT/meta['rounds'][0]['outputs']['lib']['path']).read_bytes()
    source_obj=(ROOT/meta['rounds'][0]['outputs']['obj']['path']).read_bytes()
    for row in meta['rounds']:
        for kind in ('obj','lib','exe','map'):
            info=row['outputs'][kind]
            need(info['sha256']==sha((ROOT/info['path']).read_bytes()),
                 'retained complete native memcpy source raw pair')
        need({k:v['sha256'] for k,v in row['outputs'].items()}==
             {k:v['sha256'] for k,v in meta['rounds'][0]['outputs'].items()},
             'identical original36-byte memcpy OBJ/LIB/EXE/MAP pair')
    need(memcpy.native_scope(source_obj)==memcpy.native_scope(memcpy.TARGET_OBJ.read_bytes()),
         'entire original memcpy instructions preserved')
    compare=compare_members(members,library_members(raw),{'memcpy':source_obj})
    need(compare['replaced_members']==['memcpy'] and
         compare['contextual_members_unchanged']==892,
         'current source memcpy library is one-member native replacement')
    return baseline,files,lib,members,raw,source_obj,sha((ROOT/memcpy.REPORT).read_bytes())


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    baseline,files,lib,members,prior,prior_obj,prior_hash=inherited_library()
    need(len(members)==893 and
         [(i,m.name) for i,m in enumerate(members) if m.name in ('memcmp','memcpy')]==
         [(260,'memcmp'),(261,'memcpy')], 'two adjacent original CRT members')
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[260].program_records,
         'original40-byte comparator object identity')
    target_code=native_scope(original)
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    report=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,
                accepted_baseline=baseline,accepted_library_sha256=sha(lib),
                memcpy_producer_sha256=prior_hash,source_sha256=sha(source),
                original_member_sha256=sha(original),
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')

    def execute(command,cwd,label):
        out=subprocess.run(command,cwd=cwd,env=env,stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/memcmp-combo-{label}.log'
        (ROOT/path).write_bytes(out.stdout)
        report['phases'].append(dict(label=label,returncode=out.returncode,
                                     command=command,log_path=path,log_sha256=sha(out.stdout)))
        save()
        need(out.returncode==0,label+':'+out.stdout.decode(errors='replace')[-1200:])

    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated memcmp source-work directory')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(prior)
            extract=build.response('base.lib',['*'+m.name for m in members])
            (SCRATCH/'extract.rsp').write_bytes(extract)
            execute(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            items={p.stem.lower():p for p in SCRATCH.iterdir() if p.suffix.lower()=='.obj'}
            expected=library_members(prior)
            need(len(items)==len(expected)==893,'all893 extracted source-library members')
            for m in expected:
                found=items[m.name.lower()]
                need(object_program_records(found.read_bytes())==m.program_records,
                     'exact inherited native member '+m.name)
                dest=SCRATCH/(m.name+'.obj')
                if found!=dest:found.rename(dest)
            (SCRATCH/'memcmp.asm').write_bytes(source)
            os.utime(SCRATCH/'memcmp.asm',(946684800,946684800))
            rsp=build.response(r'probe\mmcombo\newcrt.lib /E',
                ['+probe\\mmcombo\\'+m.name+'.obj' for m in members])
            link=memcpy.link_response(files)
            for old,new in ((b'probe\\mcpctx\\linked.exe',b'probe\\mmcombo\\linked.exe'),
                            (b'probe\\mcpctx\\linked.map',b'probe\\mmcombo\\linked.map'),
                            (b'probe\\mcpctx\\newcrt.lib',b'probe\\mmcombo\\newcrt.lib')):
                need(link.count(old)==1,'one scoped original link target')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/memcmp-combo-library.rsp').write_bytes(rsp)
            (ROOT/'.analysis/work/memcmp-combo-link.lnk').write_bytes(link)
            for number in (1,2):
                for name in ('memcmp.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                execute(tasm+['/m','/mx','/kh32768','/t','memcmp.asm','memcmp.obj'],
                        SCRATCH,f'round{number}-assemble')
                obj=(SCRATCH/'memcmp.obj').read_bytes()
                need(native_scope(obj)==target_code,'entire40-byte original native comparator')
                execute(dos+['tlib',r'@probe\mmcombo\library.rsp'],
                        build.WORK,f'round{number}-library')
                linked_lib=(SCRATCH/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(linked_lib),
                                         {'memcpy':prior_obj,'memcmp':obj})
                need(compared['replaced_members']==['memcmp','memcpy'] and
                     compared['contextual_members_unchanged']==891,
                     'two source replacements and891 unchanged original members')
                execute(dos+['tlink',r'@probe\mmcombo\link.lnk'],
                        build.WORK,f'round{number}-link')
                outputs={}
                for key,name in [('obj','memcmp.obj'),('lib','newcrt.lib'),
                                 ('exe','linked.exe'),('map','linked.map')]:
                    data=(SCRATCH/name).read_bytes()
                    where=f'.analysis/work/memcmp-combo-round{number}-{name}'
                    (ROOT/where).write_bytes(data)
                    outputs[key]=dict(path=where,bytes=len(data),sha256=sha(data))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (build.WORK/'bin/th03/mainl.target.exe').read_bytes(),
                     'full Japanese decoded MAINL EXE raw equality with two CRT sources')
                need((SCRATCH/'linked.map').read_bytes()==
                     (build.WORK/'obj/th03/mainl.map').read_bytes(),
                     'full original MAINL MAP equality with two CRT sources')
                report['rounds'].append(dict(round=number,outputs=outputs,
                                             library_comparison=compared,
                                             native_code_sha256=sha(target_code)))
                save()
                print('MAINL memcpy+memcmp exact native link round',number,flush=True)
            need({k:v['sha256'] for k,v in report['rounds'][0]['outputs'].items()}==
                 {k:v['sha256'] for k,v in report['rounds'][1]['outputs'].items()},
                 'two fully reproducible OBJ/LIB/EXE/MAP vectors')
        finally:
            shutil.rmtree(SCRATCH)
    new_base,_,new_lib,_,new_prior,new_obj,new_hash=inherited_library()
    need(new_base==baseline and new_lib==lib and new_prior==prior and
         new_obj==prior_obj and new_hash==prior_hash and
         source==(ROOT/SOURCE).read_bytes(),'unchanged accepted/inherited source inputs')
    report['complete']=True
    save()


if __name__=='__main__':main()
