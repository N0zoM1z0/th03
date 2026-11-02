#!/usr/bin/env python3
"""Complete native-original DOS direct 517 CODE/9 DATA/20 ordered FIXUPPs in source CRT.

Use retained44-source original CRT carrier, with its
original Japanese target, accepted baseline and retained cold pair unchanged.
Build only the original directory subsystem in a 45-source TLIB/TLINK normal product.
"""
import fcntl,json,os
from pathlib import Path
import shutil,subprocess,tomllib

import build_th03_mainl_postopen_work as previous
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
SOURCE='src/mainl/crt/direct.asm'
DRIVER='scripts/build_th03_mainl_direct_work.py'
REPORT='.analysis/work/mainl-direct-native-build.json'
ORIGINAL=WORK/'vendor/direct.obj'
SCRATCH=WORK/'probe/dir45'
PARENT_MODE='clearerr-rewind-remove-rename'
TASM_FLAGS=['/m','/mx','/kh32768','/t','direct.asm','direct.obj']
EXTERNS=['__dos_findfirst','__dos_findnext','_errno','_free','_malloc',
         '_strcat','_strcpy','_strlen','___path_issbcs']
FIXUP_SITES=[504,493,467,405,384,348,259,248,230,205,194,177,165,
             155,149,136,66,46,29,15]
PUBLICS=[(0,'_opendir'),(311,'_rewinddir'),(367,'_readdir'),(442,'_closedir')]


def original_scope(blob):
    need(describe_omf(blob)['valid'],'valid complete 517-byte DOS directory owner')
    need([(v['name'],v['class'],v['size']) for v in segment_definitions(blob)]==
         [('_TEXT','CODE',517),('_DATA','DATA',9),('_BSS','BSS',0)],
         'entire original517 CODE and real9 initialized DATA bytes')
    need(code_publics(blob,1)==PUBLICS and externs(blob)==EXTERNS,
         'actual four far directory publics and original nine runtime import names')
    need([v.data.hex() for v in parse_omf(blob) if v.name=='GRPDEF']==['08ff02ff03'],
         'original DATA/BSS group record')
    fields=literal_fields(blob)
    need(len(fields)==20 and [f['site'] for f in fields]==FIXUP_SITES,
         'all20 literal original descending native OMF field sites')
    p=payload(blob)
    code=bytes(p[1,i] for i in range(517))
    data=bytes(p[2,i] for i in range(9))
    need(data==bytes.fromhex('5c2a2e2a002a2e2a00'),
         'two complete source-owned original DOS wildcard search strings')
    return dict(CODE_bytes=517,CODE_sha256=sha(code),
                DATA_bytes=9,DATA_sha256=sha(data),
                ordered_fields=fields,publics=code_publics(blob,1),
                externs=externs(blob),original_group='08ff02ff03')


def retained():
    base,files,accepted,members,prior40,parenthash=previous.retained()
    report_path=ROOT/(previous.PREFIX+PARENT_MODE+'-build.json')
    raw=report_path.read_bytes()
    r=json.loads(raw)
    names=previous.MODES[PARENT_MODE]
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['parent_fopen_OMF_order_open'] and r['parent_fclose_near_frame_open'] and
         r['mode']==PARENT_MODE and tuple(r['names'])==names and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_forty_source_build_sha256']==parenthash and
         r['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         r['source_sha256']=={n:sha((ROOT/('src/mainl/crt/'+n+'.asm')).read_bytes())
                              for n in names} and len(r['rounds'])==2,
         'verified original44-source complete native CRT and original-target link')
    result=[]
    for i,row in enumerate(r['rounds']):
        outputs={}
        for kind,meta in row['outputs'].items():
            raw_bytes=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(raw_bytes),sha256=sha(raw_bytes)),
                 'complete previously attested44-source '+kind+' bytes')
            outputs[kind]=raw_bytes
        need(outputs['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'entire original decoded Japanese source-linked EXE/MAP unchanged')
        sources=dict(prior40[i],**{n:outputs[n] for n in names})
        c=compare_members(members,library_members(outputs['lib']),sources)
        need(c['replaced_members']==sorted(sources) and
             c['contextual_members_unchanged']==849,
             '44 source CRT members at genuine original indices plus849 contexts')
        result.append(sources)
    need(result[0]==result[1] and len(result[0])==44 and
         len(members)==893 and members[214].name=='direct',
         'two entire matching native source pairs and original directory member214')
    return base,files,accepted,members,result,sha(report_path.read_bytes())


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,parents,parentsha=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[214].program_records,
         'original DOS direct member program identity in selected CRT')
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
           previous_forty_four_source_build_sha256=parentsha,
           original_sha256=sha(original),source_sha256=sha(source),
           driver_sha256=sha((ROOT/DRIVER).read_bytes()),
           native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/direct-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        r['phases'].append(dict(label=label,command=cmd,
                                returncode=cp.returncode,log_path=path,
                                log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1600:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'new original direct isolated native scratch')
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
            (SCRATCH/'direct.asm').write_bytes(source)
            os.utime(SCRATCH/'direct.asm',(946684800,946684800))
            lib_rsp=build.response(r'probe\dir45\newcrt.lib /E',
                ['+probe\\dir45\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\dir45\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\dir45\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\dir45\\newcrt.lib'),
            ):
                need(link.count(old)==1,'one genuine original MAINL normal linker slot')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(lib_rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/direct-library.rsp').write_bytes(lib_rsp)
            (ROOT/'.analysis/work/direct-link.lnk').write_bytes(link)
            for i in (1,2):
                for f in ('direct.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/f).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                native=(SCRATCH/'direct.obj').read_bytes()
                need(original_scope(native)==goal and
                     literal_fields(native)==literal_fields(original),
                     'all517 original CODE bytes,9 DATA bytes and20 ordered native OMF fields')
                sources=dict(parents[i-1],direct=native)
                for name,blob in parents[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(blob)
                run(dos+['tlib',r'@probe\dir45\library.rsp'],
                    WORK,f'round{i}-library')
                comparison=compare_members(members,
                    library_members((SCRATCH/'newcrt.lib').read_bytes()),sources)
                need(comparison['replaced_members']==sorted(sources) and
                     comparison['contextual_members_unchanged']==848,
                     '45 native source library slots and848 untouched CRT member programs')
                run(dos+['tlink',r'@probe\dir45\link.lnk'],
                    WORK,f'round{i}-link')
                output={}
                for kind,f in (('obj','direct.obj'),('lib','newcrt.lib'),
                               ('exe','linked.exe'),('map','linked.map')):
                    blob=(SCRATCH/f).read_bytes()
                    path=f'.analysis/work/direct-round{i}-{f}'
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
                print('45-source original directory subsystem Japanese MAINL exact round',i,flush=True)
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
