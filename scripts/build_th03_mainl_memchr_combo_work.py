#!/usr/bin/env python3
"""Four-source original DOS CRT link: memchr plus memcpy/memcmp/strcmp.

One newly assembled memchr member; three previously proved source members
and 889 original native library members are reused. No cold/DIET replay.
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
import build_th03_mainl_strcmp_combo_work as strcmp
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.omf import describe_omf,parse_omf
from lib.borland_library import library_members,compare_members,object_program_records
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs

ROOT=Path(__file__).resolve().parents[1]
SOURCE='src/mainl/crt/memchr.asm'
DRIVER='scripts/build_th03_mainl_memchr_combo_work.py'
REPORT='.analysis/work/mainl-memchr-combo-build.json'
SCRATCH=build.WORK/'probe/mchcombo'
ORIGINAL=build.WORK/'vendor/memchr.obj'
REPLACED=['memchr','memcmp','memcpy','strcmp']


def native_scope(raw):
    segs=segment_definitions(raw)
    need([(s['name'],s['class'],s['size']) for s in segs] ==
         [('_TEXT','CODE',37),('_DATA','DATA',0),('_BSS','BSS',0)],
         'complete37-byte original CODE, zero DATA/BSS')
    need(code_publics(raw,1)==[(0,'_memchr')] and not externs(raw) and
         not literal_fields(raw) and describe_omf(raw)['valid'],
         'single public far memchr, zero imported and literal OMF fields')
    need([r.data for r in parse_omf(raw) if r.name=='GRPDEF']==
         [bytes.fromhex('08ff03ff02')], 'original BSS/DATA group order')
    q=payload(raw)
    return bytes(q[1,i] for i in range(37))


def inherited_library():
    base,files,accepted,members,_,memcpy_obj,memcmp_obj,_=strcmp.existing_memory_sources()
    report_raw=(ROOT/strcmp.REPORT).read_bytes();report=json.loads(report_raw)
    need(report['complete'] and not report['source_acceptance'] and
         report['added_accepted_bytes']==0 and not report['original_cold_rebuilt'] and
         report['accepted_baseline']==base and
         report['accepted_library_sha256']==sha(accepted) and
         report['source_sha256']==sha((ROOT/strcmp.SOURCE).read_bytes()) and
         report['driver_sha256']==sha((ROOT/strcmp.DRIVER).read_bytes()) and
         len(report['rounds'])==2,
         'current complete inherited three-source native carrier')
    vectors=[]
    for row in report['rounds']:
        v={}
        for key,meta in row['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'literal inherited raw '+key+' output')
            v[key]=data
        vectors.append(v)
    need(vectors[0]==vectors[1] and
         vectors[0]['exe']==(build.WORK/'bin/th03/mainl.target.exe').read_bytes() and
         vectors[0]['map']==(build.WORK/'obj/th03/mainl.map').read_bytes(),
         'original real source triple whole decoded EXE/MAP exactness')
    source_objs={'memcpy':memcpy_obj,'memcmp':memcmp_obj,'strcmp':vectors[0]['obj']}
    need(strcmp.native_scope(source_objs['strcmp'])==
         strcmp.native_scope(strcmp.VENDOR_OBJ.read_bytes()),
         'inherited full strcmp source code exact')
    compared=compare_members(members,library_members(vectors[0]['lib']),source_objs)
    need(compared['replaced_members']==REPLACED[1:] and
         compared['contextual_members_unchanged']==890,
         'original three natural-source slots,890 original members')
    return base,files,accepted,members,vectors[0]['lib'],source_objs,sha(report_raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,prior,existing,prior_hash=inherited_library()
    need(len(members)==893 and [(i,m.name) for i,m in enumerate(members)
         if m.name in REPLACED]==[(259,'memchr'),(260,'memcmp'),
                                  (261,'memcpy'),(292,'strcmp')],
         'original four CRT member positions')
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[259].program_records,
         'original memcpy family member provenance')
    original_code=native_scope(original)
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    report=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,accepted_baseline=base,
                accepted_library_sha256=sha(accepted),inherited_three_source_sha256=prior_hash,
                original_member_sha256=sha(original),source_sha256=sha(source),
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')

    def run(cmd,cwd,label):
        p=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=120)
        logfile=f'.analysis/work/memchr-combo-{label}.log'
        (ROOT/logfile).write_bytes(p.stdout)
        report['phases'].append(dict(label=label,returncode=p.returncode,
                                     command=cmd,log_path=logfile,
                                     log_sha256=sha(p.stdout)))
        save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1300:])

    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated TASM/TLIB/TLINK source work')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(prior)
            extract=build.response('base.lib',['*'+m.name for m in members])
            (SCRATCH/'extract.rsp').write_bytes(extract)
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            after=library_members(prior)
            objects={p.stem.casefold():p for p in SCRATCH.iterdir()
                     if p.suffix.casefold()=='.obj'}
            need(set(objects)=={m.name.casefold() for m in members},
                 'all893 inherited library positions extracted')
            for member in after:
                found=objects[member.name.casefold()]
                need(object_program_records(found.read_bytes())==member.program_records,
                     'every original/source inherited CRT member '+member.name)
                target=SCRATCH/(member.name+'.obj')
                if found!=target:found.rename(target)
            (SCRATCH/'memchr.asm').write_bytes(source)
            os.utime(SCRATCH/'memchr.asm',(946684800,946684800))
            rsp=build.response(r'probe\mchcombo\newcrt.lib /E',
                ['+probe\\mchcombo\\'+m.name+'.obj' for m in members])
            link=memcpy.link_response(files)
            for old,new in ((b'probe\\mcpctx\\linked.exe',b'probe\\mchcombo\\linked.exe'),
                            (b'probe\\mcpctx\\linked.map',b'probe\\mchcombo\\linked.map'),
                            (b'probe\\mcpctx\\newcrt.lib',b'probe\\mchcombo\\newcrt.lib')):
                need(link.count(old)==1,'exact one normal MAINL link destination')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/memchr-combo-library.rsp').write_bytes(rsp)
            (ROOT/'.analysis/work/memchr-combo-link.lnk').write_bytes(link)
            for number in (1,2):
                for name in ('memchr.obj','newcrt.lib','newcrt.bak',
                             'linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(tasm+['/m','/mx','/kh32768','/t','memchr.asm','memchr.obj'],
                    SCRATCH,f'round{number}-assemble')
                obj=(SCRATCH/'memchr.obj').read_bytes()
                need(native_scope(obj)==original_code,
                     'entire37-byte native original memchr instructions and fields')
                run(dos+['tlib',r'@probe\mchcombo\library.rsp'],build.WORK,
                    f'round{number}-library')
                new_lib=(SCRATCH/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(new_lib),
                                         dict(existing,memchr=obj))
                need(compared['replaced_members']==REPLACED and
                     compared['contextual_members_unchanged']==889,
                     'four source members at original indices,889 original members')
                run(dos+['tlink',r'@probe\mchcombo\link.lnk'],build.WORK,
                    f'round{number}-link')
                outputs={}
                for kind,name in [('obj','memchr.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')]:
                    raw=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/memchr-combo-round{number}-{name}'
                    (ROOT/path).write_bytes(raw)
                    outputs[kind]=dict(path=path,bytes=len(raw),sha256=sha(raw))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (build.WORK/'bin/th03/mainl.target.exe').read_bytes(),
                     'entire real original Japanese decoded MAINL executable')
                need((SCRATCH/'linked.map').read_bytes()==
                     (build.WORK/'obj/th03/mainl.map').read_bytes(),
                     'entire real original Japanese MAINL MAP')
                report['rounds'].append(dict(round=number,outputs=outputs,
                                             library_comparison=compared,
                                             native_code_sha256=sha(original_code)))
                save()
                print('MAINL four CRT sources exact linked round',number,flush=True)
            need(len(report['rounds'])==2 and
                 {k:v['sha256'] for k,v in report['rounds'][0]['outputs'].items()}==
                 {k:v['sha256'] for k,v in report['rounds'][1]['outputs'].items()},
                 'two repeatable complete native OBJ/LIB/EXE/MAP vectors')
        finally:shutil.rmtree(SCRATCH)
    after=inherited_library()
    need(after[0]==base and after[2]==accepted and after[4]==prior and
         after[5]==existing and after[6]==prior_hash and
         (ROOT/SOURCE).read_bytes()==source,
         'unchanged accepted library and inherited three-source inputs')
    report['complete']=True
    save()


if __name__=='__main__':
    main()
