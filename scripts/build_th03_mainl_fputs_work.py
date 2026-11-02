#!/usr/bin/env python3
"""Compile exact natural Borland C++ fputs in a51-source original CRT.

Reuse original 50-source perror carrier and the 893-member fixed CRT.
Compile only the affected 85-byte fputs TU twice. Keep the fixed Japanese
target, original accepted publication and cold pair untouched.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_posttimecvt_work as previous
import build_th03_mainl_strset_work as bcc
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
SOURCE='src/mainl/crt/fputs.cpp'
DRIVER='scripts/build_th03_mainl_fputs_work.py'
REPORT='.analysis/work/mainl-fputs-native-build.json'
ORIGINAL=WORK/'vendor/fputs.obj'
SCRATCH=WORK/'probe/fputs51'
BCC_FLAGS=bcc.BCC_FLAGS


def original_scope(obj):
    need(describe_omf(obj)['valid'],'complete original Borland far fputs OMF')
    need([(q['name'],q['class'],q['size']) for q in segment_definitions(obj)]==
         [('_TEXT','CODE',85),('_DATA','DATA',0),('_BSS','BSS',0)],
         '85 original CODE bytes, empty true DATA/BSS segments')
    need(code_publics(obj,1)==[(0,'_fputs')] and
         externs(obj)==['__FPUTN','_strlen'],
         'actual Pascal near FPUTN first then far strlen original import order')
    need([q.data.hex() for q in parse_omf(obj) if q.name=='GRPDEF']==
         ['08ff02ff03'],'original DATA-before-BSS group')
    fields=literal_fields(obj)
    need([(f['site'],f['width'],f['frame_method'],
           f['target_method'],f['target']) for f in fields]==
         [(56,2,5,2,1),(23,4,5,2,2)],
         'two literal descending TARGET-frame near FPUTN and far strlen calls')
    p=payload(obj)
    return dict(CODE_bytes=85,CODE_sha256=sha(bytes(p[1,i] for i in range(85))),
                native_literal_fields=fields,
                externs=externs(obj),public=code_publics(obj,1))


def retained():
    base,files,accepted,members,prior48,parenthash=previous.retained()
    mode='strlwr-perror'
    raw=(ROOT/(previous.PREFIX+mode+'-build.json')).read_bytes()
    receipt=json.loads(raw)
    names=previous.MODES[mode]
    need(receipt['complete'] and not receipt['source_acceptance'] and
         receipt['added_accepted_bytes']==0 and not receipt['original_cold_rebuilt'] and
         receipt['parent_timecvt_near_frame_open'] and
         receipt['parent_fopen_OMF_order_open'] and
         receipt['parent_fclose_near_frame_open'] and
         receipt['accepted_baseline']==base and
         receipt['accepted_library_sha256']==sha(accepted) and
         receipt['previous_forty_eight_source_build_sha256']==parenthash and
         receipt['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         receipt['source_sha256']=={name:sha((ROOT/('src/mainl/crt/'+name+'.asm')).read_bytes())
                                    for name in names} and
         len(receipt['rounds'])==2,
         'current complete 50-source original perror+strlwr CRT and fixed target')
    pairs=[]
    for i,row in enumerate(receipt['rounds']):
        outputs={}
        for kind,q in row['outputs'].items():
            blob=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(blob),sha256=sha(blob)),
                 'complete unchanged original50-source '+kind+' byte vector')
            outputs[kind]=blob
        need(outputs['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'original50-source entire decoded Japanese EXE/MAP raw-equal')
        source=dict(prior48[i],**{n:outputs[n] for n in names})
        cmp=compare_members(members,library_members(outputs['lib']),source)
        need(cmp['replaced_members']==sorted(source) and
             cmp['contextual_members_unchanged']==843,
             '50 real original source member slots and843 unchanged CRT vendors')
        pairs.append(source)
    need(pairs[0]==pairs[1] and len(pairs[0])==50 and
         len(members)==893 and members[228].name=='fputs',
         'two actual native source pairs and original fputs CRT index228')
    return base,files,accepted,members,pairs,sha(raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,objects,priorhash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[228].program_records,
         'original real DOS far fputs CRT member program identity')
    expected=original_scope(original)
    src=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    r=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
           original_cold_rebuilt=False,accepted_baseline=base,
           accepted_library_sha256=sha(accepted),
           previous_fifty_source_build_sha256=priorhash,
           original_sha256=sha(original),source_sha256=sha(src),
           driver_sha256=sha((ROOT/DRIVER).read_bytes()),
           compiler_flags=BCC_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    def run(cmd,cwd,label):
        c=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/fputs-{label}.log'
        (ROOT/where).write_bytes(c.stdout)
        r['phases'].append(dict(label=label,command=cmd,returncode=c.returncode,
                                log_path=where,log_sha256=sha(c.stdout)))
        save()
        need(c.returncode==0,label+': '+c.stdout.decode(errors='replace')[-1400:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh fputs original source scratch')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.lower():p for p in SCRATCH.iterdir() if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},'all 893 original CRT objects')
            for m in members:
                p=extracted[m.name.lower()]
                need(object_program_records(p.read_bytes())==m.program_records,
                     'unchanged original module program '+m.name)
                d=SCRATCH/(m.name+'.obj')
                if p!=d:p.rename(d)
            (SCRATCH/'fputs.cpp').write_bytes(src)
            os.utime(SCRATCH/'fputs.cpp',(946684800,946684800))
            library=build.response(r'probe\fputs51\newcrt.lib /E',
                ['+probe\\fputs51\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\fputs51\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\fputs51\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\fputs51\\newcrt.lib'),
            ):
                need(link.count(old)==1,'one genuine normal-link MAINL destination')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(library)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/fputs-library.rsp').write_bytes(library)
            (ROOT/'.analysis/work/fputs-link.lnk').write_bytes(link)
            for i in (1,2):
                for f in ('fputs.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/f).unlink(missing_ok=True)
                run(dos+[r'C:\BC45\BCC.EXE',*BCC_FLAGS,'fputs.cpp'],
                    SCRATCH,f'round{i}-compile')
                native=(SCRATCH/'fputs.obj').read_bytes()
                need(original_scope(native)==expected,
                     'all85 original BCC CODE and two literal native far/near fixups')
                sources=dict(objects[i-1],fputs=native)
                for n,b in objects[i-1].items():(SCRATCH/(n+'.obj')).write_bytes(b)
                run(dos+['tlib',r'@probe\fputs51\library.rsp'],WORK,f'round{i}-library')
                comparison=compare_members(members,library_members((SCRATCH/'newcrt.lib').read_bytes()),sources)
                need(comparison['replaced_members']==sorted(sources) and
                     comparison['contextual_members_unchanged']==842,
                     '51 original compiled source members and842 unchanged vendor programs')
                run(dos+['tlink',r'@probe\fputs51\link.lnk'],WORK,f'round{i}-link')
                outputs={}
                for kind,name in (('obj','fputs.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    data=(SCRATCH/name).read_bytes()
                    where=f'.analysis/work/fputs-round{i}-{name}'
                    (ROOT/where).write_bytes(data)
                    outputs[kind]=dict(path=where,bytes=len(data),sha256=sha(data))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'entire original Japanese MAINL EXE/MAP exact with51 source members')
                r['rounds'].append(dict(round=i,outputs=outputs,library_comparison=comparison))
                save()
                print('51-source natural BCC fputs original Japanese MAINL exact round',i,flush=True)
            need({k:x['sha256'] for k,x in r['rounds'][0]['outputs'].items()}==
                 {k:x['sha256'] for k,x in r['rounds'][1]['outputs'].items()},
                 'two identical complete real native compiler/link vectors')
        finally:shutil.rmtree(SCRATCH)
    again,_,original_library,_,_,afterhash=retained()
    need(again==base and original_library==accepted and afterhash==priorhash and
         src==(ROOT/SOURCE).read_bytes(),'current native source and prior original inputs unchanged')
    r['complete']=True
    save()


if __name__=='__main__':
    main()
