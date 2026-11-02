#!/usr/bin/env python3
"""Rebuild original DOS strtoul with its two private scanner callbacks.

Keep the original accepted CRT/cold pair fixed. Reuse ten genuinely
compiled source objects,compile only strtoul with BCC 4.5,then link
all eleven source objects at their native positions for two rounds.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_strtok_work as parent
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
SOURCE='src/mainl/crt/strtoul.cpp'
DRIVER='scripts/build_th03_mainl_strtoul_work.py'
REPORT='.analysis/work/mainl-strtoul-native-build.json'
SCRATCH=WORK/'probe/stulscope'
ORIGINAL=WORK/'vendor/strtoul.obj'
BCC_FLAGS=parent.BCC_FLAGS


def original_scope(raw):
    need(describe_omf(raw)['valid'],'actual complete original BCC OMF')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(raw)]==
         [('_TEXT','CODE',231),('_DATA','DATA',0),('_BSS','BSS',0)],
         '231 CODE instructions, empty native DATA/BSS')
    need(code_publics(raw,1)==[(56,'_strtoul')] and
         externs(raw)==['_errno','__ctype','__scantol'],
         'two private near callbacks plus original far public and three imports')
    need([r.data for r in parse_omf(raw) if r.name=='GRPDEF']==
         [bytes.fromhex('08ff02ff03')],
         'original DATA/BSS native group ownership')
    fields=literal_fields(raw)
    need(len(fields)==6,'six original ordered BCC arithmetic/ctype/callback fields')
    p=payload(raw)
    return dict(CODE_sha256=sha(bytes(p[1,i] for i in range(231))),
                CODE_bytes=231,native_literal_fields=fields,
                public_offset=56,imports=externs(raw))


def retained():
    base,files,accepted,members,nine,prevhash=parent.retained()
    raw=(ROOT/parent.REPORT).read_bytes()
    r=json.loads(raw)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['preceding_nine_source_build_sha256']==prevhash and
         r['source_sha256']==sha((ROOT/parent.SOURCE).read_bytes()) and
         r['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         len(r['rounds'])==2,'unchanged exact ten-source original carrier')
    ten=[]
    for i,entry in enumerate(r['rounds']):
        out={}
        for k,q in entry['outputs'].items():
            b=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(b),sha256=sha(b)),
                 'complete actual preceding original tokenizer output '+k)
            out[k]=b
        need(out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'preceding original Japanese source linker exactness')
        row=dict(nine[i],strtok=out['obj'])
        compared=compare_members(members,library_members(out['lib']),row)
        need(compared['replaced_members']==[m.name for m in members if m.name in row] and
             compared['contextual_members_unchanged']==883,
             'original ten source programs and other883 members')
        ten.append(row)
    need(ten[0]==ten[1] and members[315].name=='strtoul',
         'genuine repeated ten-source objects and original strtoul member315')
    return base,files,accepted,members,ten,sha(raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,ten,priorhash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[315].program_records,
         'original strtoul object program records and exact member slot')
    goal=original_scope(original)
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    report=dict(complete=False,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                accepted_baseline=base,accepted_library_sha256=sha(accepted),
                preceding_ten_source_build_sha256=priorhash,
                source_sha256=sha(source),original_sha256=sha(original),
                compiler_flags=BCC_FLAGS,driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(command,cwd,label):
        cp=subprocess.run(command,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/strtoul-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=command,returncode=cp.returncode,
                                     log_path=path,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1250:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh original strtoul source linker scratch')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.lower():p for p in SCRATCH.iterdir() if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all893 original member programs extracted')
            for m in members:
                f=extracted[m.name.lower()]
                need(object_program_records(f.read_bytes())==m.program_records,
                     'original extracted CRT member '+m.name)
                target=SCRATCH/(m.name+'.obj')
                if f!=target:f.rename(target)
            (SCRATCH/'strtoul.cpp').write_bytes(source)
            os.utime(SCRATCH/'strtoul.cpp',(946684800,946684800))
            library_rsp=build.response(r'probe\stulscope\newcrt.lib /E',
                ['+probe\\stulscope\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in [
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\stulscope\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\stulscope\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\stulscope\\newcrt.lib'),
            ]:
                need(link.count(old)==1,'original regular MAINL link slot')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(library_rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/strtoul-library.rsp').write_bytes(library_rsp)
            (ROOT/'.analysis/work/strtoul-link.lnk').write_bytes(link)
            for n in (1,2):
                for name in ('strtoul.obj','newcrt.lib','newcrt.bak',
                             'linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(dos+[r'C:\BC45\BCC.EXE',*BCC_FLAGS,'strtoul.cpp'],
                    SCRATCH,f'round{n}-compile')
                generated=(SCRATCH/'strtoul.obj').read_bytes()
                need(original_scope(generated)==goal,
                     'complete231-byte native strtoul and six ordered OMF fields equal')
                sources=dict(ten[n-1],strtoul=generated)
                for name,raw in sources.items():
                    if name!='strtoul':(SCRATCH/(name+'.obj')).write_bytes(raw)
                run(dos+['tlib',r'@probe\stulscope\library.rsp'],
                    WORK,f'round{n}-library')
                result_lib=(SCRATCH/'newcrt.lib').read_bytes()
                comparison=compare_members(members,library_members(result_lib),sources)
                need(comparison['replaced_members']==[m.name for m in members if m.name in sources] and
                     comparison['contextual_members_unchanged']==882,
                     'original11 source members and882 other complete native programs')
                run(dos+['tlink',r'@probe\stulscope\link.lnk'],
                    WORK,f'round{n}-link')
                outputs={}
                for kind,name in [('obj','strtoul.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')]:
                    b=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/strtoul-round{n}-{name}'
                    (ROOT/path).write_bytes(b)
                    outputs[kind]=dict(path=path,bytes=len(b),sha256=sha(b))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'complete decoded Japanese MAINL EXE/MAP exact with11 natural source members')
                report['rounds'].append(dict(round=n,outputs=outputs,
                                             library_comparison=comparison))
                save()
                print('11 source strtoul + xx Japanese MAINL exact round',n,flush=True)
            need({k:x['sha256'] for k,x in report['rounds'][0]['outputs'].items()}==
                 {k:x['sha256'] for k,x in report['rounds'][1]['outputs'].items()},
                 'two full identical BCC/TLIB/TLINK output vectors')
        finally:shutil.rmtree(SCRATCH)
    again,_,lib,_,_,newhash=retained()
    need(again==base and lib==accepted and newhash==priorhash and
         source==(ROOT/SOURCE).read_bytes(),'all original and upstream source receipts unchanged')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
