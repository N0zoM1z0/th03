#!/usr/bin/env python3
"""Real DOS/Unix time converter820 CODE,12 DATA and29 ordered OMF fields in source CRT.

Use retained47-source exact original source CRT carrier, with its
original Japanese target, accepted baseline and retained cold pair unchanged.
Build only time converter in a 48-source native TLIB/TLINK normal product.
"""
import fcntl,json,os
from pathlib import Path
import shutil,subprocess,tomllib

import build_th03_mainl_splitpth_work as previous
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
SOURCE='src/mainl/crt/_timecvt.asm'
DRIVER='scripts/build_th03_mainl_timecvt_work.py'
REPORT='.analysis/work/mainl-timecvt-native-build.json'
ORIGINAL=WORK/'vendor/_timecvt.obj'
SCRATCH=WORK/'probe/time48'
TASM_FLAGS=['/m','/mx','/kh32768','/t','_timecvt.asm','_timecvt.obj']
EXTERNS=['__ISDST','__daylight','__timezone','_tzset',
         'N_LXMUL@','N_LMOD@','N_LDIV@']
PUBLICS=[(0,'__dostounix'),(301,'__unixtodos')]
FIXUP_SITES=[786,757,659,636,608,591,574,555,545,523,471,442,420,
             398,376,353,316,313,307,267,241,218,191,134,87,61,18,15,9]
NEAR_FRAMES={659,636,608,591,574,545,523,471,442,420,398,376,353,
             267,241,218,87,61}


def original_scope(blob):
    need(describe_omf(blob)['valid'],'full DOS date conversion original Borland OMF')
    need([(q['name'],q['class'],q['size']) for q in segment_definitions(blob)]==
         [('_TEXT','CODE',820),('_DATA','DATA',12),('_BSS','BSS',0)],
         'all820 DOS/Unix CODE and12 actual initialized month lengths')
    need(code_publics(blob,1)==PUBLICS and externs(blob)==EXTERNS,
         'both original far time converter public offsets and seven CRT imports')
    need([q.data.hex() for q in parse_omf(blob) if q.name=='GRPDEF']==
         ['08ff02ff03'],'original DATA/BSS group')
    fields=literal_fields(blob)
    need(len(fields)==29 and [q['site'] for q in fields]==FIXUP_SITES,
         'all29 original chronological native OMF relocation sites')
    norm=[]
    for q in fields:
        if q['site'] in NEAR_FRAMES:
            need(q['target_method']==2 and q['target'] in (1,5,6,7) and
                 q['frame_method'] in (0,5),'one known near CRT import frame')
            norm.append(dict(q,frame_method=5,frame=None))
        else:norm.append(q)
    p=payload(blob)
    CODE=bytes(p[1,i] for i in range(820))
    DATA=bytes(p[2,i] for i in range(12))
    need(DATA==bytes.fromhex('1f1c1f1e1f1e1f1f1e1f1e1f'),
         'original twelve initialized month-length bytes')
    return dict(CODE_bytes=820,CODE_sha256=sha(CODE),
                DATA_bytes=12,DATA_sha256=sha(DATA),
                logical_ordered_fixups=norm,
                public=code_publics(blob,1),imports=externs(blob),
                original_group='08ff02ff03')


def retained():
    base,files,accepted,members,preceding46,parenthash=previous.retained()
    raw=(ROOT/previous.REPORT).read_bytes()
    r=json.loads(raw)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['prior_fopen_OMF_order_open'] and r['prior_fclose_MKNAME_frame_open'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_forty_six_source_build_sha256']==parenthash and
         r['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         r['source_sha256']==sha((ROOT/previous.SOURCE).read_bytes()) and
         len(r['rounds'])==2,
         'complete genuine47-source original splitpath normal product')
    source=[]
    for i,row in enumerate(r['rounds']):
        out={}
        for kind,meta in row['outputs'].items():
            b=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(b),sha256=sha(b)),
                 'inherited complete47-source '+kind+' artifact')
            out[kind]=b
        need(out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'entire 47-source decoded Japanese MAINL EXE/MAP original')
        members_source=dict(preceding46[i],splitpth=out['obj'])
        c=compare_members(members,library_members(out['lib']),members_source)
        need(c['replaced_members']==sorted(members_source) and
             c['contextual_members_unchanged']==846,
             '47 true source members and846 unchanged vendor CRT programs')
        source.append(members_source)
    need(len(source)==2 and source[0]==source[1] and len(source[0])==47 and
         len(members)==893 and members[184].name=='_timecvt',
         'two reproducible native47-source pairs and real time converter member184')
    return base,files,accepted,members,source,sha(raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,parents,parentsha=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[184].program_records,
         'original native DOS _timecvt member program identity in selected CRT')
    goal=original_scope(original)
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    r=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
           original_cold_rebuilt=False,prior_fopen_OMF_order_open=True,
           prior_fclose_MKNAME_frame_open=True,
           accepted_baseline=base,accepted_library_sha256=sha(accepted),
           previous_forty_seven_source_build_sha256=parentsha,
           native_timecvt_near_TARGET_frame_open=True,
           original_sha256=sha(original),source_sha256=sha(source),
           driver_sha256=sha((ROOT/DRIVER).read_bytes()),
           native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/timecvt-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        r['phases'].append(dict(label=label,command=cmd,
                                returncode=cp.returncode,log_path=path,
                                log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1600:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated native time conversion scratch')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.lower():p for p in SCRATCH.iterdir()
                       if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all original 893 CRT members extracted')
            for m in members:
                p=extracted[m.name.lower()]
                need(object_program_records(p.read_bytes())==m.program_records,
                     'unchanged original member '+m.name)
                dest=SCRATCH/(m.name+'.obj')
                if p!=dest:p.rename(dest)
            (SCRATCH/'_timecvt.asm').write_bytes(source)
            os.utime(SCRATCH/'_timecvt.asm',(946684800,946684800))
            lib_rsp=build.response(r'probe\time48\newcrt.lib /E',
                ['+probe\\time48\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\time48\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\time48\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\time48\\newcrt.lib'),
            ):
                need(link.count(old)==1,'one genuine original MAINL normal linker slot')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(lib_rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/timecvt-library.rsp').write_bytes(lib_rsp)
            (ROOT/'.analysis/work/timecvt-link.lnk').write_bytes(link)
            for i in (1,2):
                for f in ('_timecvt.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/f).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                native=(SCRATCH/'_timecvt.obj').read_bytes()
                need(original_scope(native)==goal and
                     [
                       q['site'] for q in literal_fields(native)]==
                     [q['site'] for q in literal_fields(original)] and
                     all(q['frame_method']==0 for q in literal_fields(native)
                         if q['site'] in NEAR_FRAMES) and
                     all(q['frame_method']==5 for q in literal_fields(original)
                         if q['site'] in NEAR_FRAMES),
                     'all820 original CODE/12 DATA and29 logical OMF fields, near frames tracked')
                sources=dict(parents[i-1],_timecvt=native)
                for name,blob in parents[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(blob)
                run(dos+['tlib',r'@probe\time48\library.rsp'],
                    WORK,f'round{i}-library')
                comparison=compare_members(members,
                    library_members((SCRATCH/'newcrt.lib').read_bytes()),sources)
                need(comparison['replaced_members']==sorted(sources) and
                     comparison['contextual_members_unchanged']==845,
                     '48 true source CRT members and845 vendor programs untouched')
                run(dos+['tlink',r'@probe\time48\link.lnk'],
                    WORK,f'round{i}-link')
                output={}
                for kind,f in (('obj','_timecvt.obj'),('lib','newcrt.lib'),
                               ('exe','linked.exe'),('map','linked.map')):
                    blob=(SCRATCH/f).read_bytes()
                    path=f'.analysis/work/timecvt-round{i}-{f}'
                    (ROOT/path).write_bytes(blob)
                    output[kind]=dict(path=path,bytes=len(blob),sha256=sha(blob))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'entire pinned Japanese decoded MAINL EXE and MAP raw equal')
                r['rounds'].append(dict(round=i,outputs=output,
                                        library_comparison=comparison))
                save()
                print('48-source native DOS/Unix time converter MAINL exact round',i,flush=True)
            need({k:v['sha256'] for k,v in r['rounds'][0]['outputs'].items()}==
                 {k:v['sha256'] for k,v in r['rounds'][1]['outputs'].items()},
                 'two full native byte-identical OBJ/LIB/EXE/MAP vectors')
        finally:shutil.rmtree(SCRATCH)
    b,_,lib,_,_,afterhash=retained()
    need(b==base and lib==accepted and afterhash==parentsha and
         source==(ROOT/SOURCE).read_bytes(),
         'current source and accepted original library/cold inputs unchanged')
    r['complete']=True
    save()


if __name__=='__main__':
    main()
