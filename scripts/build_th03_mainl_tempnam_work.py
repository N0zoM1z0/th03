#!/usr/bin/env python3
"""Real original 395 CODE/6 DATA DOS tempnam in 53-source Japanese MAINL.

Both links reproduce complete original EXE/MAP. The near __MKNAME call
has one BCC TARGET-frame5 vs TASM CODE-frame0 difference; this is an
explicit native OMF gap, not an accepted-source publication.
"""
import fcntl,json,os
from pathlib import Path
import shutil,subprocess,tomllib

import build_th03_mainl_strftime_work as previous
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
SOURCE='src/mainl/crt/tempnam.asm'
DRIVER='scripts/build_th03_mainl_tempnam_work.py'
REPORT='.analysis/work/mainl-tempnam-native-build.json'
ORIGINAL=WORK/'vendor/tempnam.obj'
SCRATCH=WORK/'probe/temp53'
TASM_FLAGS=['/m','/mx','/kh32768','/t','tempnam.asm','tempnam.obj']
EXTERNS=['__MKNAME','_strlen','__stpcpy','_strchr','_free',
         '_getenv','_malloc','__dos_getfileattr','___path_issbcs']
ORIGINAL_SITES=[367,323,309,265,203,172,158,144,98,90,60,56,40,15]
NEAR_FRAMES={309}


def native_parts(obj):
    p=payload(obj)
    return bytes(p[1,i] for i in range(395)),bytes(p[2,i] for i in range(6))


def original_scope(obj):
    need(describe_omf(obj)['valid'],'genuine original DOS tempnam native object')
    need([(v['name'],v['class'],v['size']) for v in segment_definitions(obj)]==
         [('_TEXT','CODE',395),('_DATA','DATA',6),('_BSS','BSS',0)],
         '395 original CODE bytes and six initialized TMP bytes')
    need(code_publics(obj,1)==[(0,'_tempnam')] and externs(obj)==EXTERNS,
         'original far tempnam public and nine real imported helpers')
    need([q.data.hex() for q in parse_omf(obj) if q.name=='GRPDEF']==
         ['08ff02ff03'],'original DATA/BSS group')
    fs=literal_fields(obj)
    need(len(fs)==14 and [q['site'] for q in fs]==ORIGINAL_SITES,
         '14 exact original native OMF writer site order')
    normalized=[]
    for q in fs:
        if q['site'] in NEAR_FRAMES:
            need(q['target_method']==2 and q['target']==1 and
                 q['frame_method'] in (0,5),
                 'single near MKNAME TARGET/CODE OMF frame difference')
            normalized.append(dict(q,frame_method=5,frame=None))
        else:normalized.append(q)
    CODE,DATA=native_parts(obj)
    need(DATA==bytes.fromhex('544d50000000'),
         'real initialized TMP prefix and two NUL suffix bytes')
    return dict(CODE_bytes=395,CODE_sha256=sha(CODE),
                DATA_bytes=6,DATA_sha256=sha(DATA),
                logical_fields=normalized,
                public=code_publics(obj,1),imports=externs(obj),
                group='08ff02ff03')


def retained():
    base,files,accepted,members,prior51,parenthash=previous.retained()
    raw=(ROOT/previous.REPORT).read_bytes()
    r=json.loads(raw)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['native_strftime_near_UTOA_TARGET_frame_open'] is True and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_fifty_one_source_build_sha256']==parenthash and
         r['source_sha256']==sha((ROOT/previous.SOURCE).read_bytes()) and
         r['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         len(r['rounds'])==2,
         'full source-bound52-source original strftime CRT carrier')
    pairs=[]
    for i,row in enumerate(r['rounds']):
        outputs={}
        for kind,q in row['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'whole original52-source '+kind+' raw output')
            outputs[kind]=data
        need(outputs['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'full original Japanese 52-source EXE/MAP raw-equal')
        sources=dict(prior51[i],strftime=outputs['obj'])
        comp=compare_members(members,library_members(outputs['lib']),sources)
        need(comp['replaced_members']==sorted(sources) and
             comp['contextual_members_unchanged']==841,
             '52 original source owners,841 untouched vendor programs')
        pairs.append(sources)
    need(len(pairs)==2 and pairs[0]==pairs[1] and
         len(pairs[0])==52 and len(members)==893 and
         members[320].name=='tempnam',
         'two whole original source pairs and actual tempnam member320')
    return base,files,accepted,members,pairs,sha(raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,prior,parenthash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[320].program_records,
         'the actual original 893-member CRT tempnam object identity')
    goal=original_scope(original)
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    report=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,
                native_tempnam_near_MKNAME_TARGET_frame_open=True,
                prior_strftime_near_UTOA_TARGET_frame_open=True,
                prior_timecvt_near_frame_open=True,
                prior_fopen_OMF_order_open=True,prior_fclose_near_frame_open=True,
                accepted_baseline=base,accepted_library_sha256=sha(accepted),
                previous_fifty_two_source_build_sha256=parenthash,
                original_sha256=sha(original),source_sha256=sha(source),
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/tempnam-{label}.log'
        (ROOT/where).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                     log_path=where,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1600:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh original native tempnam isolated build')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            objfiles={p.stem.lower():p for p in SCRATCH.iterdir() if p.suffix.lower()=='.obj'}
            need(set(objfiles)=={m.name.lower() for m in members},
                 'all893 original CRT objects extracted unchanged')
            for m in members:
                f=objfiles[m.name.lower()]
                need(object_program_records(f.read_bytes())==m.program_records,
                     'original whole CRT member raw program '+m.name)
                dest=SCRATCH/(m.name+'.obj')
                if f!=dest:f.rename(dest)
            (SCRATCH/'tempnam.asm').write_bytes(source)
            os.utime(SCRATCH/'tempnam.asm',(946684800,946684800))
            rsp=build.response(r'probe\temp53\newcrt.lib /E',
                ['+probe\\temp53\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for originaldest,targetdest in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\temp53\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\temp53\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\temp53\\newcrt.lib'),
            ):
                need(link.count(originaldest)==1,
                     'one true original Japanese MAINL link target destination')
                link=link.replace(originaldest,targetdest)
            (SCRATCH/'library.rsp').write_bytes(rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/tempnam-library.rsp').write_bytes(rsp)
            (ROOT/'.analysis/work/tempnam-link.lnk').write_bytes(link)
            for i in (1,2):
                for name in ('tempnam.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                obj=(SCRATCH/'tempnam.obj').read_bytes()
                old_fields=literal_fields(original)
                new_fields=literal_fields(obj)
                need(original_scope(obj)==goal and
                     len(old_fields)==len(new_fields)==14 and
                     sum(x!=y for x,y in zip(old_fields,new_fields))==1 and
                     all(x==y for x,y in zip(old_fields,new_fields)
                         if x['site'] not in NEAR_FRAMES) and
                     old_fields[2]['site']==new_fields[2]['site']==309 and
                     old_fields[2]['frame_method']==5 and
                     new_fields[2]['frame_method']==0 and
                     old_fields[2]['target']==new_fields[2]['target']==1,
                     '395 CODE/6 DATA and14 ordered relocations; one near MKNAME frame gap')
                owners=dict(prior[i-1],tempnam=obj)
                for name,old in prior[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(old)
                run(dos+['tlib',r'@probe\temp53\library.rsp'],WORK,f'round{i}-library')
                compared=compare_members(members,
                    library_members((SCRATCH/'newcrt.lib').read_bytes()),owners)
                need(compared['replaced_members']==sorted(owners) and
                     compared['contextual_members_unchanged']==840,
                     '53 original source CRT programs and840 original vendor members unchanged')
                run(dos+['tlink',r'@probe\temp53\link.lnk'],WORK,f'round{i}-link')
                output={}
                for kind,name in (('obj','tempnam.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    data=(SCRATCH/name).read_bytes()
                    where=f'.analysis/work/tempnam-round{i}-{name}'
                    (ROOT/where).write_bytes(data)
                    output[kind]=dict(path=where,bytes=len(data),sha256=sha(data))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'entire Japanese original 67372-byte EXE and MAP bitwise exact')
                report['rounds'].append(dict(round=i,outputs=output,
                                             library_comparison=compared))
                save()
                print('53-source original tempnam Japanese MAINL exact round',i,flush=True)
            need({k:q['sha256'] for k,q in report['rounds'][0]['outputs'].items()}==
                 {k:q['sha256'] for k,q in report['rounds'][1]['outputs'].items()},
                 'two complete reproducible TASM/TLIB/TLINK raw output vectors')
        finally:shutil.rmtree(SCRATCH)
    current,_,originalCRT,_,_,afterhash=retained()
    need(current==base and originalCRT==accepted and afterhash==parenthash and
         source==(ROOT/SOURCE).read_bytes(),
         'original Japanese target and accepted provider CRT/source frozen')
    report['complete']=True
    save()


if __name__=='__main__':
    main()
