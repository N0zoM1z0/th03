#!/usr/bin/env python3
"""Original four-segment DOS tzset/DST plus genuine 58-source MAINL carrier.

Original native CODE, DATA, BSS, INITDATA, all 48 ordered OMF fields are
source-authored, not copied binary objects. Only affected native source,
whole retained CRT library and relevant normal linker product are built.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_posttempnam_work as previous
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
SOURCE='src/mainl/crt/tzset.asm'
DRIVER='scripts/build_th03_mainl_tzset_work.py'
REPORT='.analysis/work/mainl-tzset-native-build.json'
ORIGINAL=WORK/'vendor/tzset.obj'
SCRATCH=WORK/'probe/tzset58'
MODE='dirs-tmpnam-ftime'
TASM_FLAGS=['/m','/mx','/kh32768','/t','tzset.asm','tzset.obj']
EXTERNS=['__ctype','_atol','_getenv','_memset','_strcpy',
         '_strlen','_strncpy','N_LXMUL@']
CODE_PUB=[(0,'_tzset'),(508,'__ISDST')]
DATA_PUB=[(0,'__monthDay'),(26,'__tzname'),(34,'__timezone'),
          (38,'__daylight')]
SIZES={1:744,2:48,3:8,4:6}


def native_scope(blob):
    need(describe_omf(blob)['valid'],'complete real original tzset Borland OMF')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(blob)]==
         [('_TEXT','CODE',744),('_DATA','DATA',48),
          ('_BSS','BSS',8),('_INIT_','INITDATA',6)],
         'all four genuine CODE, DATA, BSS, and INITDATA segment definitions')
    need(code_publics(blob,1)==CODE_PUB and code_publics(blob,2)==DATA_PUB and
         code_publics(blob,3)==[] and code_publics(blob,4)==[] and
         externs(blob)==EXTERNS,
         'all original far/near code, DATA exports and eight real runtime imports')
    need([r.data.hex() for r in parse_omf(blob) if r.name=='GRPDEF']==
         ['0aff03ff02'],'original DATA/BSS GRPDEF sequence')
    p=payload(blob)
    code=bytes(p[1,i] for i in range(SIZES[1]))
    data=bytes(p[2,i] for i in range(SIZES[2]))
    init=bytes(p[4,i] for i in range(SIZES[4]))
    need(init==bytes.fromhex('011e00000000'),
         'real original six-byte Borland far initialization record')
    need(data==bytes.fromhex(
         '00001f003b005a0078009700b500d400f300110130014e016d01'
         '00000000040000007081ffff0000545a004a53540000'),
         'whole original Julian day table, far names and JST default configuration')
    fields=literal_fields(blob)
    need(len(fields)==48 and
         [f['segment'] for f in fields]==[1]*45+[2]*2+[4] and
         [(f['segment'],f['site']) for f in fields[-3:]]==
         [(2,26),(2,30),(4,2)],
         '45 CODE/2 DATA/1 INIT native original ordered relocation fields')
    return dict(CODE_bytes=744,CODE_sha256=sha(code),
                DATA_bytes=48,DATA_sha256=sha(data),
                BSS_bytes=8,INITDATA_bytes=6,INITDATA_sha256=sha(init),
                original_literal_ordered_fixups=fields,
                original_code_publics=code_publics(blob,1),
                original_data_publics=code_publics(blob,2),
                original_imports=externs(blob),
                original_group='0aff03ff02')


def retained():
    base,files,accepted,members,parents53,parenthash=previous.retained()
    path=ROOT/(previous.PREFIX+MODE+'-build.json')
    raw=path.read_bytes()
    r=json.loads(raw)
    names=previous.MODES[MODE]
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['parent_tempnam_near_frame_open'] and
         r['parent_strftime_near_frame_open'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_fifty_three_source_build_sha256']==parenthash and
         r['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         r['original_source_paths']=={n:previous.source_path(n) for n in names} and
         r['source_sha256']=={n:sha((ROOT/previous.source_path(n)).read_bytes())
                              for n in names} and len(r['rounds'])==2,
         'complete immutable 57-member original CRT source pair')
    pairs=[]
    for i,row in enumerate(r['rounds']):
        out={}
        for kind,q in row['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'whole actual original 57-source '+kind+' byte vector')
            out[kind]=data
        need(out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'complete decoded Japanese 57-source MAINL EXE and MAP byte equal')
        sources=dict(parents53[i],**{n:out[n] for n in names})
        compared=compare_members(members,library_members(out['lib']),sources)
        need(compared['replaced_members']==sorted(sources) and
             compared['contextual_members_unchanged']==836,
             '57 distinct original source CRT slots and836 untouched vendor programs')
        pairs.append(sources)
    need(len(pairs)==2 and pairs[0]==pairs[1] and len(pairs[0])==57 and
         len(members)==893 and members[324].name=='tzset' and
         'tzset' not in pairs[0],
         'two complete identical 57-source CRT vectors with genuine tzset index324')
    return base,files,accepted,members,pairs,sha(raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,parents,parenthash=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[324].program_records,
         'all original tzset CRT member program records true')
    goal=native_scope(original)
    src=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    report=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,
                original_tzset_literal_OMF_exact=True,
                prior_fopen_OMF_order_open=True,
                prior_fclose_MKNAME_frame_open=True,
                prior_timecvt_near_frame_open=True,
                prior_strftime_near_frame_open=True,
                prior_tempnam_near_frame_open=True,
                accepted_baseline=base,accepted_library_sha256=sha(accepted),
                previous_fifty_seven_source_build_sha256=parenthash,
                original_sha256=sha(original),source_sha256=sha(src),
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/tzset-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                     log_path=path,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1600:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated original tzset native scratch')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            (SCRATCH/'extract.rsp').write_bytes(build.response(
                'base.lib',['*'+m.name for m in members]))
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.lower():p for p in SCRATCH.iterdir()
                       if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.lower() for m in members},
                 'all 893 original Borland CRT members extracted')
            for m in members:
                f=extracted[m.name.lower()]
                need(object_program_records(f.read_bytes())==m.program_records,
                     'all original CRT vendor program records '+m.name)
                target=SCRATCH/(m.name+'.obj')
                if f!=target:f.rename(target)
            (SCRATCH/'tzset.asm').write_bytes(src)
            os.utime(SCRATCH/'tzset.asm',(946684800,946684800))
            rsp=build.response(r'probe\tzset58\newcrt.lib /E',
                ['+probe\\tzset58\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\tzset58\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\tzset58\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\tzset58\\newcrt.lib'),
            ):
                need(link.count(old)==1,'normal linker original MAINL output present')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/tzset-library.rsp').write_bytes(rsp)
            (ROOT/'.analysis/work/tzset-link.lnk').write_bytes(link)
            for i in (1,2):
                for filename in ('tzset.obj','newcrt.lib','newcrt.bak',
                                 'linked.exe','linked.map'):
                    (SCRATCH/filename).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                obj=(SCRATCH/'tzset.obj').read_bytes()
                need(native_scope(obj)==goal and
                     literal_fields(obj)==literal_fields(original),
                     'all 744 CODE,48 DATA,8 BSS,6 INITDATA and 48 literal ordered fixups')
                sources=dict(parents[i-1],tzset=obj)
                for name,blob in parents[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(blob)
                run(dos+['tlib',r'@probe\tzset58\library.rsp'],WORK,
                    f'round{i}-library')
                compared=compare_members(members,
                    library_members((SCRATCH/'newcrt.lib').read_bytes()),sources)
                need(compared['replaced_members']==sorted(sources) and
                     compared['contextual_members_unchanged']==835,
                     '58 original source CRT positions,835 other vendor programs unchanged')
                run(dos+['tlink',r'@probe\tzset58\link.lnk'],WORK,
                    f'round{i}-link')
                output={}
                for kind,name in (('obj','tzset.obj'),('lib','newcrt.lib'),
                                  ('exe','linked.exe'),('map','linked.map')):
                    data=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/tzset-round{i}-{name}'
                    (ROOT/path).write_bytes(data)
                    output[kind]=dict(path=path,bytes=len(data),sha256=sha(data))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (WORK/'obj/th03/mainl.map').read_bytes(),
                     'entire Japanese original 67372-byte MAINL EXE and MAP bitwise equal')
                report['rounds'].append(dict(round=i,outputs=output,
                                             library_comparison=compared))
                save()
                print('58-source full tzset DOS time initialization Japanese MAINL exact round',
                      i,flush=True)
            need({k:q['sha256'] for k,q in report['rounds'][0]['outputs'].items()}==
                 {k:q['sha256'] for k,q in report['rounds'][1]['outputs'].items()},
                 'two byte-identical complete native OBJ/CRT/EXE/MAP vectors')
        finally:
            shutil.rmtree(SCRATCH)
    now,_,CRT,_,_,afterhash=retained()
    need(now==base and CRT==accepted and afterhash==parenthash and
         src==(ROOT/SOURCE).read_bytes(),
         'accepted native original and source unchanged during scoped build')
    report['complete']=True
    save()


if __name__=='__main__':
    main()
