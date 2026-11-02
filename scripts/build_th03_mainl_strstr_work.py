#!/usr/bin/env python3
"""Link recovered DOS strstr together with native xx and seven proven CRT sources."""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_work as build
import build_th03_mainl_xx_crt_combo_work as parent
from build_th03_mainl_resources_work import need, sha
from build_th03_mainl_display_work import payload, literal_fields
from lib.borland_library import library_members, compare_members, object_program_records
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs

ROOT=Path(__file__).resolve().parents[1]
WORK=build.WORK
DRIVER='scripts/build_th03_mainl_strstr_work.py'
SOURCE='src/mainl/crt/strstr.asm'
REPORT='.analysis/work/mainl-strstr-native-build.json'
SCRATCH=WORK/'probe/stccombo'
ORIGINAL=WORK/'vendor/strstr.obj'


def original_scope(raw):
    need(describe_omf(raw)['valid'],'valid original/source substring OMF')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(raw)]==
         [('_TEXT','CODE',108),('_DATA','DATA',0),('_BSS','BSS',0)],
         'whole original108-byte code and empty DATA/BSS')
    need(code_publics(raw,1)==[(0,'_strstr')] and not externs(raw) and
         literal_fields(raw)==[], 'original one far public/no imports/no fields')
    need([r.data for r in parse_omf(raw) if r.name=='GRPDEF']==
         [bytes.fromhex('08ff03ff02')],
         'original BSS-before-DATA ownership')
    p=payload(raw)
    return bytes(p[1,i] for i in range(108))


def retained():
    base,files,accepted,members,objects,xhash,chash=parent.retained_source_objects()
    receipt=(ROOT/parent.REPORT).read_bytes()
    r=json.loads(receipt)
    need(r['complete'] and not r['source_acceptance'] and
         not r['original_cold_rebuilt'] and r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['xx_native_build_sha256']==xhash and r['crt_native_build_sha256']==chash and
         r['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         len(r['rounds'])==2,
         'unchanged eight-source exact native parent')
    for row in r['rounds']:
        for kind,meta in row['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'complete unchanged eight-source library/EXE/MAP vector')
        need(row['outputs']['exe']['sha256']==sha((WORK/'bin/th03/mainl.target.exe').read_bytes()) and
             row['outputs']['map']['sha256']==sha((WORK/'obj/th03/mainl.map').read_bytes()),
             'actual parent whole original EXE and MAP')
    need(len(members)==893 and members[312].name=='strstr' and len(objects)==2 and
         objects[0]==objects[1], 'original substring slot and source eight OBJ pair')
    return base,files,accepted,members,objects,sha(receipt)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,objects,priorhash=retained()
    orig=ORIGINAL.read_bytes()
    original_code=original_scope(orig)
    need(members[312].program_records==object_program_records(orig),
         'real vendor substring library member program records')
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    report=dict(complete=False, source_acceptance=False, added_accepted_bytes=0,
                original_cold_rebuilt=False, accepted_baseline=base,
                accepted_library_sha256=sha(accepted),
                preceding_eight_source_receipt_sha256=priorhash,
                source_sha256=sha(source),original_sha256=sha(orig),
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/strstr-{label}.log'
        (ROOT/where).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                     log_path=where,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1300:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated substring source native scratch')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response('base.lib',
                                      ['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.lower():p for p in SCRATCH.iterdir() if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},'all893 original member objects extracted')
            for m in members:
                found=extracted[m.name.lower()]
                need(object_program_records(found.read_bytes())==m.program_records,
                     'unmodified original native member '+m.name)
                dest=SCRATCH/(m.name+'.obj')
                if found!=dest:found.rename(dest)
            (SCRATCH/'strstr.asm').write_bytes(source)
            os.utime(SCRATCH/'strstr.asm',(946684800,946684800))
            lib_rsp=build.response(r'probe\stccombo\newcrt.lib /E',
                         ['+probe\\stccombo\\'+m.name+'.obj' for m in members])
            link=parent.xx.link_response(files)
            for old,new in [
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\stccombo\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\stccombo\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\stccombo\\newcrt.lib'),
            ]:
                need(link.count(old)==1,'one real linked product path')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(lib_rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/strstr-library.rsp').write_bytes(lib_rsp)
            (ROOT/'.analysis/work/strstr-link.lnk').write_bytes(link)
            for n in (1,2):
                for fname in ('strstr.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/fname).unlink(missing_ok=True)
                run(tasm+['/m','/mx','/kh32768','/t','strstr.asm','strstr.obj'],
                    SCRATCH,f'round{n}-assemble')
                obj=(SCRATCH/'strstr.obj').read_bytes()
                need(original_scope(obj)==original_code,
                     'entire native substring CODE, group and OMF interface raw equal')
                replacements=dict(objects[n-1],strstr=obj)
                for key,data in replacements.items():
                    if key!='strstr':(SCRATCH/(key+'.obj')).write_bytes(data)
                run(dos+['tlib',r'@probe\stccombo\library.rsp'],
                    WORK,f'round{n}-library')
                lib=(SCRATCH/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(lib),replacements)
                need(compared['replaced_members']==[m.name for m in members if m.name in replacements] and
                     compared['contextual_members_unchanged']==884,
                     'original9 source slots and884 native members unchanged')
                run(dos+['tlink',r'@probe\stccombo\link.lnk'],WORK,f'round{n}-link')
                outs={}
                for kind,name in [('obj','strstr.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')]:
                    raw=(SCRATCH/name).read_bytes()
                    where=f'.analysis/work/strstr-round{n}-{name}'
                    (ROOT/where).write_bytes(raw)
                    outs[kind]=dict(path=where,bytes=len(raw),sha256=sha(raw))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'exact whole Japanese decoded MAINL EXE and MAP with9 real CRT sources')
                report['rounds'].append(dict(round=n,outputs=outs,library_comparison=compared))
                save()
                print('9 source xx/CRT + strstr exact MAINL round',n,flush=True)
            need({k:x['sha256'] for k,x in report['rounds'][0]['outputs'].items()}==
                 {k:x['sha256'] for k,x in report['rounds'][1]['outputs'].items()},
                 'repeated complete raw source OBJECT/LIB/EXE/MAP vectors')
        finally:shutil.rmtree(SCRATCH)
    nextbase,_,nextlib,_,_,nexthash=retained()
    need(nextbase==base and nextlib==accepted and nexthash==priorhash and
         source==(ROOT/SOURCE).read_bytes(),'accepted and upstream native source artifacts unchanged')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
