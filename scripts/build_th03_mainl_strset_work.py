#!/usr/bin/env python3
"""Compile natural BCC strset and combine 27 exact DOS CRT sources in MAINL.

Reuse fixed original cold and the verified 26-source native library.
Only the new original 46-byte strset translation unit is compiled;
run actual TLIB/TLINK twice without recompressing or a full cold replay.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_postscanner_work as parent
import build_th03_mainl_strtol_work as signed
import build_th03_mainl_work as build
import build_th03_mainl_xx_work as xx
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members,object_program_records
from lib.decoded_mainl_display_native import externs
from lib.omf import describe_omf,parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

ROOT=Path(__file__).resolve().parents[1]
WORK=build.WORK
DRIVER='scripts/build_th03_mainl_strset_work.py'
SOURCE='src/mainl/crt/strset.cpp'
REPORT='.analysis/work/mainl-strset-native-build.json'
ORIGINAL=WORK/'vendor/strset.obj'
SCRATCH=WORK/'probe/sscope'
BCC_FLAGS=signed.BCC_FLAGS



def original_scope(obj):
    need(describe_omf(obj)['valid'],'actual complete original native BCC strset object')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(obj)]==
         [('_TEXT','CODE',46),('_DATA','DATA',0),('_BSS','BSS',0)],
         'original46-byte body and zero initialized/statically allocated bytes')
    need(code_publics(obj,1)==[(0,'_strset')] and
         externs(obj)==['_strlen','_setmem'],
         'genuine far strset public and original two library helper interfaces')
    need([q.data for q in parse_omf(obj) if q.name=='GRPDEF']==
         [bytes.fromhex('08ff02ff03')],
         'original DATA/BSS zero-byte group ownership')
    fields=literal_fields(obj)
    need(len(fields)==2,'two literal original far strlen/setmem fields')
    p=payload(obj)
    return dict(CODE_sha256=sha(bytes(p[1,i] for i in range(46))),
                CODE_bytes=46,native_literal_fields=fields,
                externs=externs(obj),pub=code_publics(obj,1))


def retained():
    base,files,accepted,members,prior23,priorhash=parent.retained()
    mode='strrchr-srchstr-strrev'
    receipt=(ROOT/(parent.PREFIX+mode+'-build.json')).read_bytes()
    r=json.loads(receipt)
    names=parent.MODES[mode]
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_twenty_three_source_receipt_sha256']==priorhash and
         r['driver_sha256']==sha((ROOT/parent.DRIVER).read_bytes()) and
         r['source_sha256']=={n:sha((ROOT/f'src/mainl/crt/{n}.asm').read_bytes())
                              for n in names} and
         len(r['rounds'])==2,
         'actual exact 26-source TASM original CRT build and bound input hashes')
    combined=[]
    for i,row in enumerate(r['rounds']):
        output={}
        for name,q in row['outputs'].items():
            blob=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(blob),sha256=sha(blob)),
                 'complete original native 26-source output '+name)
            output[name]=blob
        need(output['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             output['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'inherited original 26-source Japanese EXE/MAP raw identical')
        objects=dict(prior23[i],**{n:output[n] for n in names})
        cmp=compare_members(members,library_members(output['lib']),objects)
        need(cmp['replaced_members']==sorted(objects) and
             cmp['contextual_members_unchanged']==867,
             'inherited26 exact source modules and867 untouched native records')
        combined.append(objects)
    need(combined[0]==combined[1] and len(members)==893 and
         len(combined[0])==26 and members[310].name=='strset',
         'identical previous original source vectors and CRT strset slot310')
    return base,files,accepted,members,combined,sha(receipt)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,old_objs,priorhash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[310].program_records,
         'original large model strset member program identity')
    goal=original_scope(original)
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    r=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
           original_cold_rebuilt=False,accepted_baseline=base,
           accepted_library_sha256=sha(accepted),
           previous_twenty_six_source_build_sha256=priorhash,
           original_sha256=sha(original),source_sha256=sha(source),
           driver_sha256=sha((ROOT/DRIVER).read_bytes()),
           compiler_flags=BCC_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/strset-{label}.log'
        (ROOT/where).write_bytes(cp.stdout)
        r['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                log_path=where,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1500:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh native original strset local work')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.lower():p for p in SCRATCH.iterdir() if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all893 original native library member programs extracted')
            for m in members:
                f=extracted[m.name.lower()]
                need(object_program_records(f.read_bytes())==m.program_records,
                     'actual original member native records '+m.name)
                dest=SCRATCH/(m.name+'.obj')
                if f!=dest:f.rename(dest)
            (SCRATCH/'strset.cpp').write_bytes(source)
            os.utime(SCRATCH/'strset.cpp',(946684800,946684800))
            response=build.response(r'probe\sscope\newcrt.lib /E',
                ['+probe\\sscope\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in [
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\sscope\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\sscope\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\sscope\\newcrt.lib'),
            ]:
                need(link.count(old)==1,'one actual original linker reference')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(response)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/strset-library.rsp').write_bytes(response)
            (ROOT/'.analysis/work/strset-link.lnk').write_bytes(link)
            for i in (1,2):
                for name in ('strset.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(dos+[r'C:\BC45\BCC.EXE',*BCC_FLAGS,'strset.cpp'],
                    SCRATCH,f'round{i}-compile')
                native=(SCRATCH/'strset.obj').read_bytes()
                need(original_scope(native)==goal,
                     'entire46 BCC CODE and2 literal ordered strlen/setmem OMF fields exact')
                source_objs=dict(old_objs[i-1],strset=native)
                for name,obj in source_objs.items():
                    if name!='strset':(SCRATCH/(name+'.obj')).write_bytes(obj)
                run(dos+['tlib',r'@probe\sscope\library.rsp'],
                    WORK,f'round{i}-library')
                result=(SCRATCH/'newcrt.lib').read_bytes()
                cmp=compare_members(members,library_members(result),source_objs)
                need(cmp['replaced_members']==sorted(source_objs) and
                     cmp['contextual_members_unchanged']==866,
                     '27 real source slots and866 original untouched programs')
                run(dos+['tlink',r'@probe\sscope\link.lnk'],
                    WORK,f'round{i}-link')
                out={}
                for key,name in [('obj','strset.obj'),('lib','newcrt.lib'),
                                 ('exe','linked.exe'),('map','linked.map')]:
                    raw=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/strset-round{i}-{name}'
                    (ROOT/path).write_bytes(raw)
                    out[key]=dict(path=path,bytes=len(raw),sha256=sha(raw))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'whole original Japanese MAINL EXE/MAP raw equal with27 source modules')
                r['rounds'].append(dict(round=i,outputs=out,library_comparison=cmp))
                save()
                print('27 original source CRT strset + xx native MAINL exact round',i,flush=True)
            need({k:q['sha256'] for k,q in r['rounds'][0]['outputs'].items()}==
                 {k:q['sha256'] for k,q in r['rounds'][1]['outputs'].items()},
                 'two identical entire source OMF/library/EXE/MAP vectors')
        finally:shutil.rmtree(SCRATCH)
    final,_,lib,_,_,newhash=retained()
    need(final==base and lib==accepted and newhash==priorhash and
         source==(ROOT/SOURCE).read_bytes(),'same source and fixed accepted pair')
    r['complete']=True
    save()

if __name__=='__main__':
    main()
