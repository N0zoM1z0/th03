#!/usr/bin/env python3
"""Build the actual 485-byte Borland DOS getc from maintained 8086 source.

This is the complete 485-byte DOS near/far getc TU, with four
real PUBLIC entries and one-byte genuine original BSS lookahead.
The original 893-member CRT is reconstructed in its original order,
with 29 exact predecessor native source CRT members retained.
The cold pair and accepted 28-provider publication are not rebuilt.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_fwrite_work as parent
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
SOURCES=('src/mainl/crt/getc.asm',)
DRIVER='scripts/build_th03_mainl_getc_work.py'
REPORT='.analysis/work/mainl-getc-native-build.json'
SCRATCH=WORK/'probe/gtcsrc'
ORIGINAL=WORK/'vendor/getc.obj'
TASM_FLAGS=['/m','/mx','/kh32768','/t','getc.asm','getc.obj']


def original_scope(obj):
    need(describe_omf(obj)['valid'],'complete actual Borland DOS getc native OMF')
    need([(q['name'],q['class'],q['size']) for q in segment_definitions(obj)]==
         [('_TEXT','CODE',485),('_DATA','DATA',0),('_BSS','BSS',1)],
         'full485 CODE, zero DATA and original one-byte BSS lookahead')
    need(code_publics(obj,1)==[(192,'__fgetc'),(217,'__Nfgetc'),
                               (220,'_fgetc'),(469,'_fgetchar')] and
         externs(obj)==['__streams','_fflush','_eof','___read'],
         'original four native near/far getc public names and actual imports')
    need([q.data.hex() for q in parse_omf(obj) if q.name=='GRPDEF']==
         ['08ff03ff02'],'literal original BSS-before-DATA DGROUP geometry')
    f=literal_fields(obj)
    need([x['site'] for x in f]==[359,437,461,19,43,119,372,393,473] and
         all(x['segment']==1 and x['frame_method']==1 and
             x['target_method']==0 and x['target']==3
             for x in f[:3]) and
         [(x['site'],x['target_method'],x['target'],x['frame_method'])
          for x in f[3:]]==
         [(19,2,1,1),(43,2,2,5),(119,2,4,5),
          (372,2,4,5),(393,2,3,5),(473,2,1,1)],
         'all nine original unusual BSS-first then far-call OMF fields in writer order')
    p=payload(obj)
    return dict(CODE_bytes=485,CODE_sha256=sha(bytes(p[1,i] for i in range(485))),
                literal_ordered_fields=f,imports=externs(obj),
                native_publics=code_publics(obj,1),original_BSS_bytes=1)


def retained():
    base,files,accepted,members,prior28,oldhash=parent.retained()
    receipt=(ROOT/parent.REPORT).read_bytes()
    r=json.loads(receipt)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_twenty_eight_source_build_sha256']==oldhash and
         r['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         r['source_sha256']=={name:sha((ROOT/name).read_bytes()) for name in parent.SOURCES} and
         len(r['rounds'])==2,'complete unchanged29-source native fwrite original link')
    owners=[]
    for i,row in enumerate(r['rounds']):
        output={}
        for name,m in row['outputs'].items():
            raw=(ROOT/m['path']).read_bytes()
            need(m==dict(path=m['path'],bytes=len(raw),sha256=sha(raw)),
                 'complete retained native fwrite original '+name+' vector')
            output[name]=raw
        need(output['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             output['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'actual fixed original Japanese 29-source MAINL and MAP raw equality')
        source=dict(prior28[i],fwrite=output['obj'])
        cmp=compare_members(members,library_members(output['lib']),source)
        need(cmp['replaced_members']==sorted(source) and
             cmp['contextual_members_unchanged']==864,
             '29 prior native source CRT members and864 original contexts')
        owners.append(source)
    need(owners[0]==owners[1] and len(members)==893 and
         len(owners[0])==29 and members[237].name=='getc',
         'actual original getc library slot237 and two repeated29-source object vectors')
    return base,files,accepted,members,owners,sha(receipt)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,preceding,parenthash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[237].program_records,
         'original complete 485-byte getc object at its library slot')
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
                previous_twenty_nine_source_build_sha256=parenthash,
                original_sha256=sha(original),
                source_sha256={n:sha(b) for n,b in inputs.items()},
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/getc-full-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                     log_path=path,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1800:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated native getc source worktree')
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
            rsp=build.response(r'probe\gtcsrc\newcrt.lib /E',
                ['+probe\\gtcsrc\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\gtcsrc\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\gtcsrc\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\gtcsrc\\newcrt.lib'),
            ):
                need(link.count(old)==1,'original independent MAINL link target path')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/getc-full-library.rsp').write_bytes(rsp)
            (ROOT/'.analysis/work/getc-full-link.lnk').write_bytes(link)
            for i in (1,2):
                for name in ('getc.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                generated=(SCRATCH/'getc.obj').read_bytes()
                need(original_scope(generated)==goal,
                     'complete original485 CODE, 1 BSS and all9 ordered native OMF fields')
                sources=dict(preceding[i-1],getc=generated)
                for name,obj in preceding[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(obj)
                run(dos+['tlib',r'@probe\gtcsrc\library.rsp'],
                    WORK,f'round{i}-library')
                lib=(SCRATCH/'newcrt.lib').read_bytes()
                compared=compare_members(members,library_members(lib),sources)
                need(compared['replaced_members']==sorted(sources) and
                     compared['contextual_members_unchanged']==863,
                     '30 original source CRT positions and863 unchanged members')
                run(dos+['tlink',r'@probe\gtcsrc\link.lnk'],WORK,f'round{i}-link')
                outputs={}
                for kind,name in (('obj','getc.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    raw=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/getc-full-round{i}-{name}'
                    (ROOT/path).write_bytes(raw)
                    outputs[kind]=dict(path=path,bytes=len(raw),sha256=sha(raw))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'entire original decoded Japanese MAINL EXE/MAP exact with30 source modules')
                report['rounds'].append(dict(round=i,outputs=outputs,
                                             library_comparison=compared))
                save()
                print('30 native sources including 4-public getc exact Japanese MAINL round',i,flush=True)
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
