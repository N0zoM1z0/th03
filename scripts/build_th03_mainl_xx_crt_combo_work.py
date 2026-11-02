#!/usr/bin/env python3
"""Link native source xx plus seven natural DOS CRT source modules together.

Reuse validated repeated native BCC/TASM objects; reassemble only the
affected library and normal MAINL link,never the unchanged cold/DIET pair.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_work as build
import build_th03_mainl_xx_work as xx
import build_th03_mainl_crt_growth_work as crt
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import library_members,compare_members,object_program_records

ROOT=Path(__file__).resolve().parents[1]
DRIVER='scripts/build_th03_mainl_xx_crt_combo_work.py'
REPORT='.analysis/work/mainl-xx-crt8-build.json'
SCRATCH=build.WORK/'probe/xx8combo'
CRT_MODE='memchr-memset-strlen-strchr'
SOURCE_NAMES=crt.source_names(CRT_MODE)+('xx',)
ORIGINAL_MEMBER_INDICES={'memchr':259,'memcmp':260,'memcpy':261,
                         'memset':263,'strchr':291,'strcmp':292,'strlen':300}


def retained_source_objects():
    baseline,files,accepted,members,_=xx.baseline(ROOT)
    xr=json.loads((ROOT/xx.REPORT).read_bytes())
    cr=json.loads((ROOT/(crt.PREFIX+CRT_MODE+'-build.json')).read_bytes())
    need(xr['complete'] and xr['whole_product_linked'] and
         xr['baseline']==baseline and xr['native_object_compiler'] and
         not xr['source_acceptance'] and not xr['whole_product_cold_rebuilt'] and
         xr['source_sha256']=={p:sha((ROOT/p).read_bytes())
                               for p in xr['source_sha256']} and
         xr['driver_sha256']==sha((ROOT/xx.DRIVER).read_bytes()) and
         len(xr['rounds'])==2,
         'current double-built genuine BCC source xx member')
    need(cr['complete'] and not cr['source_acceptance'] and
         cr['added_accepted_bytes']==0 and not cr['original_cold_rebuilt'] and
         cr['accepted_baseline']==baseline and
         cr['accepted_library_sha256']==sha(accepted) and
         cr['source_sha256']=={n:sha((ROOT/f'src/mainl/crt/{n}.asm').read_bytes())
                               for n in crt.source_names(CRT_MODE)} and
         cr['driver_sha256']==sha((ROOT/crt.DRIVER).read_bytes()) and
         tuple(cr['names'])==crt.source_names(CRT_MODE) and
         len(cr['rounds'])==2,
         'current seven natural CRT source objects and intact accepted baseline')
    objects=[]
    for round_no in (0,1):
        combined={}
        xout=xr['rounds'][round_no]['outputs']
        for key,meta in xout.items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'complete native BCC source xx '+key)
            if key=='obj': combined['xx']=data
        cout=cr['rounds'][round_no]['outputs']
        for key,meta in cout.items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'complete native TASM source '+key)
            if key in crt.source_names(CRT_MODE):combined[key]=data
        need(set(combined)==set(SOURCE_NAMES),
             'eight completely source-produced members')
        need(xout['exe']['sha256']==sha((build.WORK/'bin/th03/mainl.target.exe').read_bytes()) and
             cout['exe']['sha256']==sha((build.WORK/'bin/th03/mainl.target.exe').read_bytes()),
             'both independent native library contexts matched the original EXE')
        objects.append(combined)
    need(objects[0]==objects[1],
         'all8 complete source native OBJ bytes repeat across two real builds')
    need(len(members)==893 and all(members[i].name==n
        for n,i in ORIGINAL_MEMBER_INDICES.items()) and
        sum(m.name=='xx' for m in members)==1,
        'exact original positions of all8 source CRT members')
    return baseline,files,accepted,members,objects,sha((ROOT/xx.REPORT).read_bytes()),sha((ROOT/(crt.PREFIX+CRT_MODE+'-build.json')).read_bytes())


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    baseline,files,accepted,members,objects,xhash,chash=retained_source_objects()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/cfg['paths']['msdos_player']),'-e','-x']
    report=dict(complete=False,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,accepted_baseline=baseline,
                accepted_library_sha256=sha(accepted),
                xx_native_build_sha256=xhash,crt_native_build_sha256=chash,
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                source_names=SOURCE_NAMES,
                native_object_sha256={n:sha(obj) for n,obj in objects[0].items()},
                phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')

    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        where=f'.analysis/work/xx-crt8-{label}.log'
        (ROOT/where).write_bytes(cp.stdout)
        report['phases'].append(dict(label=label,command=cmd,returncode=cp.returncode,
                                     log_path=where,log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1500:])

    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated eight-source native linker')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(accepted)
            extract=build.response('base.lib',['*'+m.name for m in members])
            (SCRATCH/'extract.rsp').write_bytes(extract)
            run(dos+['tlib','@extract.rsp'],SCRATCH,'extract')
            extracted={p.stem.casefold():p for p in SCRATCH.iterdir()
                       if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.casefold() for m in members},
                 'all893 original CRT members extracted')
            for member in members:
                found=extracted[member.name.casefold()]
                need(object_program_records(found.read_bytes())==member.program_records,
                     'entire original library member program records '+member.name)
                dest=SCRATCH/(member.name+'.obj')
                if found!=dest:found.rename(dest)
            library_rsp=build.response(r'probe\xx8combo\combined.lib /E',
                ['+probe\\xx8combo\\'+m.name+'.obj' for m in members])
            link_rsp=xx.link_response(files)
            for old,new in [
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\xx8combo\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\xx8combo\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\xx8combo\\combined.lib'),
            ]:
                need(link_rsp.count(old)==1,'exact original normal MAINL link slot')
                link_rsp=link_rsp.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(library_rsp)
            (SCRATCH/'link.lnk').write_bytes(link_rsp)
            (ROOT/'.analysis/work/xx-crt8-library.rsp').write_bytes(library_rsp)
            (ROOT/'.analysis/work/xx-crt8-link.lnk').write_bytes(link_rsp)
            for round_no in (1,2):
                for key,raw in objects[round_no-1].items():
                    (SCRATCH/(key+'.obj')).write_bytes(raw)
                for name in ('combined.lib','combined.bak','linked.exe','linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                run(dos+['tlib',r'@probe\xx8combo\library.rsp'],
                    build.WORK,f'round{round_no}-library')
                library=(SCRATCH/'combined.lib').read_bytes()
                cmp=compare_members(members,library_members(library),objects[round_no-1])
                expected=[m.name for m in members if m.name in SOURCE_NAMES]
                need(cmp['replaced_members']==expected and
                     cmp['contextual_members_unchanged']==893-len(SOURCE_NAMES),
                     'eight actual source members at original CRT slots and885 others unchanged')
                run(dos+['tlink',r'@probe\xx8combo\link.lnk'],
                    build.WORK,f'round{round_no}-link')
                output={}
                for kind,name in [('lib','combined.lib'),('exe','linked.exe'),
                                  ('map','linked.map')]:
                    data=(SCRATCH/name).read_bytes()
                    path=f'.analysis/work/xx-crt8-round{round_no}-{name}'
                    (ROOT/path).write_bytes(data)
                    output[kind]=dict(path=path,bytes=len(data),sha256=sha(data))
                need((SCRATCH/'linked.exe').read_bytes()==
                     (build.WORK/'bin/th03/mainl.target.exe').read_bytes() and
                     (SCRATCH/'linked.map').read_bytes()==
                     (build.WORK/'obj/th03/mainl.map').read_bytes(),
                     'eight-source complete original Japanese MAINL EXE/MAP raw equal')
                report['rounds'].append(dict(round=round_no,outputs=output,
                                             library_comparison=cmp))
                save()
                print('Combined exact xx and seven CRT original EXE/MAP round',
                      round_no,flush=True)
            need(len(report['rounds'])==2 and
                 {k:v['sha256'] for k,v in report['rounds'][0]['outputs'].items()}==
                 {k:v['sha256'] for k,v in report['rounds'][1]['outputs'].items()},
                 'two reproducible complete raw eight-source CRT/EXE/MAP vectors')
        finally:shutil.rmtree(SCRATCH)
    after=retained_source_objects()
    need(after[0]==baseline and after[2]==accepted and
         after[5]==xhash and after[6]==chash,
         'accepted and two native independent producer receipts unchanged')
    report['complete']=True
    save()


if __name__=='__main__':
    main()
