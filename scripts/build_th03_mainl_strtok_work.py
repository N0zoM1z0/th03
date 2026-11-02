#!/usr/bin/env python3
"""Compile original DOS strtok in BCC and relink it with xx + eight CRT sources.

Ten source TUs share the actual original CRT 893-member ordering. Only the
one new BCC unit is compiled; all unchanged original native objects and
the fixed Japanese decoded MAINL source-only cold baseline are reused.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_strstr_work as prior
import build_th03_mainl_work as build
import probe_th03_mainl_xx_dispatch as profile
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members,object_program_records
from lib.decoded_mainl_display_native import externs
from lib.omf import describe_omf,parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

ROOT=Path(__file__).resolve().parents[1]
WORK=build.WORK
DRIVER='scripts/build_th03_mainl_strtok_work.py'
SOURCE='src/mainl/crt/strtok.cpp'
REPORT='.analysis/work/mainl-strtok-native-build.json'
SCRATCH=WORK/'probe/stokscope'
ORIGINAL=WORK/'vendor/strtok.obj'
BCC_FLAGS=[x for x in profile.FLAGS if x!='-S']+['-y','-c']


def original_scope(obj):
    need(describe_omf(obj)['valid'],'valid complete native stateful tokenizer OMF')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(obj)]==
         [('_TEXT','CODE',203),('_DATA','DATA',0),('_BSS','BSS',4)],
         'original203 CODE,zero DATA and real4-byte BSS storage')
    need(code_publics(obj,1)==[(0,'_strtok')] and not externs(obj),
         'one far C strtok public and zero runtime imports')
    need([r.data for r in parse_omf(obj) if r.name=='GRPDEF']==
         [bytes.fromhex('08ff02ff03')],
         'literal DATA then BSS original segment group')
    p=payload(obj)
    code=bytes(p[1,i] for i in range(203))
    return dict(code_sha256=sha(code),code_bytes=len(code),
                native_fields=literal_fields(obj))


def retained():
    base,files,accepted,members,eight_objects,parenthash=prior.retained()
    parent_report=(ROOT/prior.REPORT).read_bytes()
    p=json.loads(parent_report)
    need(p['complete'] and not p['source_acceptance'] and
         p['added_accepted_bytes']==0 and not p['original_cold_rebuilt'] and
         p['accepted_baseline']==base and p['accepted_library_sha256']==sha(accepted) and
         p['preceding_eight_source_receipt_sha256']==parenthash and
         p['source_sha256']==sha((ROOT/prior.SOURCE).read_bytes()) and
         p['driver_sha256']==sha((ROOT/prior.DRIVER).read_bytes()) and
         len(p['rounds'])==2,
         'complete unchanged preceding natural substring source/link rounds')
    nine=[]
    for i,entry in enumerate(p['rounds']):
        outputs={}
        for key,m in entry['outputs'].items():
            raw=(ROOT/m['path']).read_bytes()
            need(m==dict(path=m['path'],bytes=len(raw),sha256=sha(raw)),
                 'complete preceding raw native strstr source pair')
            outputs[key]=raw
        need(outputs['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'preceding nine-source full Japanese original link')
        nine.append(dict(eight_objects[i],strstr=outputs['obj']))
        compared=compare_members(members,library_members(outputs['lib']),nine[-1])
        need(compared['replaced_members']==[m.name for m in members if m.name in nine[-1]] and
             compared['contextual_members_unchanged']==884,
             'nine genuine native-source member positions and884 original members')
    need(nine[0]==nine[1] and members[313].name=='strtok',
         'repeated 9 source object pair and original tokenizer member index')
    return base,files,accepted,members,nine,sha(parent_report)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,objects,parenthash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[313].program_records,
         'original tokenizer native member at index313')
    profile0=original_scope(original)
    need(len(profile0['native_fields'])==12,'all12 original ordered relocation records')
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    report=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,accepted_baseline=base,
                accepted_library_sha256=sha(accepted),
                preceding_nine_source_build_sha256=parenthash,
                source_sha256=sha(source),original_sha256=sha(original),
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                compiler_flags=BCC_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(args,cwd,label):
        cp=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/strtok-{label}.log'
        (ROOT/where).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=args,returncode=cp.returncode,
                                     log_path=where,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1300:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated tokenizer original native scratch')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.lower():p for p in SCRATCH.iterdir() if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all893 original library members extracted')
            for m in members:
                found=extracted[m.name.lower()]
                need(object_program_records(found.read_bytes())==m.program_records,
                     'original native member '+m.name+' program records')
                dest=SCRATCH/(m.name+'.obj')
                if found!=dest:found.rename(dest)
            (SCRATCH/'strtok.cpp').write_bytes(source)
            os.utime(SCRATCH/'strtok.cpp',(946684800,946684800))
            library_rsp=build.response(r'probe\stokscope\newcrt.lib /E',
                 ['+probe\\stokscope\\'+m.name+'.obj' for m in members])
            link=prior.parent.xx.link_response(files)
            for old,new in [
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\stokscope\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\stokscope\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\stokscope\\newcrt.lib'),
            ]:
                need(link.count(old)==1,'one original normal linker output slot')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(library_rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/strtok-library.rsp').write_bytes(library_rsp)
            (ROOT/'.analysis/work/strtok-link.lnk').write_bytes(link)
            for n in (1,2):
                for fname in ('strtok.obj','newcrt.lib','newcrt.bak',
                              'linked.exe','linked.map'):
                    (SCRATCH/fname).unlink(missing_ok=True)
                run(dos+[r'C:\BC45\BCC.EXE',*BCC_FLAGS,'strtok.cpp'],
                    SCRATCH,f'round{n}-compile')
                obj=(SCRATCH/'strtok.obj').read_bytes()
                need(original_scope(obj)==profile0,
                     'complete203 native CODE bytes,12 fields,static BSS and group equality')
                sources=dict(objects[n-1],strtok=obj)
                for key,data in sources.items():
                    if key!='strtok':(SCRATCH/(key+'.obj')).write_bytes(data)
                run(dos+['tlib',r'@probe\stokscope\library.rsp'],WORK,
                    f'round{n}-library')
                lib=(SCRATCH/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(lib),sources)
                need(compared['replaced_members']==[m.name for m in members if m.name in sources] and
                     compared['contextual_members_unchanged']==883,
                     'all10 actual natural source members and883 original intact')
                run(dos+['tlink',r'@probe\stokscope\link.lnk'],WORK,
                    f'round{n}-link')
                out={}
                for kind,name in [('obj','strtok.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')]:
                    data=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/strtok-round{n}-{name}'
                    (ROOT/path).write_bytes(data)
                    out[kind]=dict(path=path,bytes=len(data),sha256=sha(data))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'full original Japanese decoded MAINL and MAP exact with10 source modules')
                report['rounds'].append(dict(round=n,outputs=out,library_comparison=compared))
                save()
                print('10 source tokenizer+xx MAINL native link exact round',n,flush=True)
            need({k:x['sha256'] for k,x in report['rounds'][0]['outputs'].items()}==
                 {k:x['sha256'] for k,x in report['rounds'][1]['outputs'].items()},
                 'two identical complete original source native vectors')
        finally:shutil.rmtree(SCRATCH)
    after,_,newlib,_,_,newhash=retained()
    need(after==base and newlib==accepted and newhash==parenthash and
         source==(ROOT/SOURCE).read_bytes(), 'unchanged existing original source evidence')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
