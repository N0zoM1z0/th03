#!/usr/bin/env python3
"""Native complete 1256 CODE/18 DATA strftime in 52-source Japanese MAINL.

Real TASM writes the original 66 ordered OMF relocation sites and all CODE/
DATA bytes. Four BCC near __UTOA TARGET frames remain TASM CODE frames;
the normal linker still must reproduce the complete original EXE/MAP.
No binary postprocessing, synthesized acceptance or full cold replay.
"""
import fcntl,json,os
from pathlib import Path
import shutil,subprocess,tomllib

import build_th03_mainl_fputs_work as previous
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
SOURCE='src/mainl/crt/strftime.asm'
DRIVER='scripts/build_th03_mainl_strftime_work.py'
REPORT='.analysis/work/mainl-strftime-native-build.json'
ORIGINAL=WORK/'vendor/strftime.obj'
SCRATCH=WORK/'probe/stft52'
TASM_FLAGS=['/m','/mx','/kh32768','/t','strftime.asm','strftime.obj']
EXTERNS=['__UTOA','__tzname','_strcat','_strcpy','_strlen','_strncpy',
         '_SWeekday','_LWeekday','_SMonth','_LMonth','_AmPm','_atime']
NEAR_FRAMES={879,811,774,723}
BODY_SITES=[1016,1012,911,892,883,879,844,824,815,811,774,760,736,727,
            723,709,689,680,674,666,662,645,636,630,622,618,435,431,
            213,189,185,168,164,147,143,126,122,87,63,54]
TABLE_SITES=list(range(1254,1211,-2))
TAIL_SITES=[1090,1059,1036,1027]
FIXUP_SITES=BODY_SITES+TABLE_SITES+TAIL_SITES
DATA=bytes.fromhex('303000200020002c20003a30003a30002500')
FORMAT_CHARS=[37,65,66,72,73,77,83,85,87,88,89,90,97,98,99,100,106,109,112,119,120,121]
SWITCH_TO=[1021,130,172,246,269,387,440,462,538,779,981,999,109,
           151,200,223,311,363,410,528,605,945]


def native_parts(obj):
    p=payload(obj)
    return bytes(p[1,i] for i in range(1256)),bytes(p[2,i] for i in range(18))


def original_scope(obj):
    need(describe_omf(obj)['valid'],'valid full Borland strftime original OMF owner')
    need([(q['name'],q['class'],q['size']) for q in segment_definitions(obj)]==
         [('_TEXT','CODE',1256),('_DATA','DATA',18),('_BSS','BSS',0)],
         'complete original 1256 CODE and18 initialized DATA with zero BSS')
    need(code_publics(obj,1)==[(0,'_strftime')] and externs(obj)==EXTERNS,
         'original far strftime entry and12 exact CRT symbol import indices')
    need([q.data.hex() for q in parse_omf(obj) if q.name=='GRPDEF']==
         ['08ff02ff03'],'original DATA-before-BSS group')
    fields=literal_fields(obj)
    need(len(fields)==66 and [q['site'] for q in fields]==FIXUP_SITES,
         'all66 original literal CODE/switch/late relocation sites and order')
    canonical=[]
    for f in fields:
        if f['site'] in NEAR_FRAMES:
            need(f['target_method']==2 and f['target']==1 and f['frame_method'] in (0,5),
                 'precisely one genuine near __UTOA target and frame variation')
            canonical.append(dict(f,frame_method=5,frame=None))
        else:canonical.append(f)
    CODE,data=native_parts(obj)
    need(data==DATA,'seven original initialized source C string fragments')
    need([int.from_bytes(CODE[i:i+2],'little') for i in range(1168,1212,2)]==
         FORMAT_CHARS,'22 immutable real ASCII format character WORDs')
    need([int.from_bytes(CODE[i:i+2],'little') for i in range(1212,1256,2)]==
         SWITCH_TO,'22 actual original symbolic CODE dispatch destinations')
    need(all(f['target_method']==0 and f['frame_method']==5 and f['target']==1
             for f in fields[40:62]),'original 22 TARGET-frame CODE switch relocations')
    return dict(CODE_bytes=1256,CODE_sha256=sha(CODE),
                DATA_bytes=18,DATA_sha256=sha(data),
                logical_ordered_fields=canonical,
                public=code_publics(obj,1),imports=externs(obj),
                switch_table_offset=1212,format_class_offset=1168,
                group='08ff02ff03')


def retained():
    base,files,accepted,members,old50,parenthash=previous.retained()
    receipt=(ROOT/previous.REPORT).read_bytes()
    r=json.loads(receipt)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_fifty_source_build_sha256']==parenthash and
         r['source_sha256']==sha((ROOT/previous.SOURCE).read_bytes()) and
         r['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         len(r['rounds'])==2,
         'complete source-bound 51-member original far fputs CRT parent')
    old=[]
    for i,row in enumerate(r['rounds']):
        out={}
        for kind,meta in row['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'complete original source parent '+kind+' output')
            out[kind]=data
        need(out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'full original decoded Japanese EXE/MAP from previous 51 modules')
        owners=dict(old50[i],fputs=out['obj'])
        comp=compare_members(members,library_members(out['lib']),owners)
        need(comp['replaced_members']==sorted(owners) and
             comp['contextual_members_unchanged']==842,
             '51 source CRT modules and 842 unchanged vendor program records')
        old.append(owners)
    need(old[0]==old[1] and len(old[0])==51 and
         len(members)==893 and members[298].name=='strftime',
         'two equal 51 source objects and real original strftime index298')
    return base,files,accepted,members,old,sha(receipt)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,prior,parenthash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[298].program_records,
         'the actual original 893-member CRT strftime object identity')
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
                native_strftime_near_UTOA_TARGET_frame_open=True,
                prior_timecvt_near_frame_open=True,
                prior_fopen_OMF_order_open=True,prior_fclose_near_frame_open=True,
                accepted_baseline=base,accepted_library_sha256=sha(accepted),
                previous_fifty_one_source_build_sha256=parenthash,
                original_sha256=sha(original),source_sha256=sha(source),
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/strftime-{label}.log'
        (ROOT/where).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                     log_path=where,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1600:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh original native strftime isolated build')
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
            (SCRATCH/'strftime.asm').write_bytes(source)
            os.utime(SCRATCH/'strftime.asm',(946684800,946684800))
            rsp=build.response(r'probe\stft52\newcrt.lib /E',
                ['+probe\\stft52\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for originaldest,targetdest in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\stft52\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\stft52\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\stft52\\newcrt.lib'),
            ):
                need(link.count(originaldest)==1,
                     'one true original Japanese MAINL link target destination')
                link=link.replace(originaldest,targetdest)
            (SCRATCH/'library.rsp').write_bytes(rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/strftime-library.rsp').write_bytes(rsp)
            (ROOT/'.analysis/work/strftime-link.lnk').write_bytes(link)
            for i in (1,2):
                for name in ('strftime.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                obj=(SCRATCH/'strftime.obj').read_bytes()
                need(original_scope(obj)==goal and
                     [f['site'] for f in literal_fields(obj)]==
                     [f['site'] for f in literal_fields(original)] and
                     all(f['frame_method']==0 for f in literal_fields(obj)
                         if f['site'] in NEAR_FRAMES) and
                     all(f['frame_method']==5 for f in literal_fields(original)
                         if f['site'] in NEAR_FRAMES),
                     'complete1256 original CODE,18 DATA, all66 OMF fields and four known frames')
                owners=dict(prior[i-1],strftime=obj)
                for name,old in prior[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(old)
                run(dos+['tlib',r'@probe\stft52\library.rsp'],WORK,f'round{i}-library')
                compared=compare_members(members,
                    library_members((SCRATCH/'newcrt.lib').read_bytes()),owners)
                need(compared['replaced_members']==sorted(owners) and
                     compared['contextual_members_unchanged']==841,
                     '52 original source CRT programs and841 untouched original vendor programs')
                run(dos+['tlink',r'@probe\stft52\link.lnk'],WORK,f'round{i}-link')
                output={}
                for kind,name in (('obj','strftime.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    data=(SCRATCH/name).read_bytes()
                    where=f'.analysis/work/strftime-round{i}-{name}'
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
                print('52-source original strftime Japanese MAINL exact round',i,flush=True)
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
