#!/usr/bin/env python3
"""Complete original DOS buffered putc 974 CODE/1 DATA/1 BSS/29 FIXUPPs in source CRT.

Use retained45-source original CRT carrier, with its
original Japanese target, accepted baseline and retained cold pair unchanged.
Build only original putc in a 46-source actual TASM/TLIB/TLINK normal product.
"""
import fcntl,json,os
from pathlib import Path
import shutil,subprocess,tomllib

import build_th03_mainl_direct_work as previous
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
SOURCE='src/mainl/crt/putc.asm'
DRIVER='scripts/build_th03_mainl_putc_work.py'
REPORT='.analysis/work/mainl-putc-native-build.json'
ORIGINAL=WORK/'vendor/putc.obj'
SCRATCH=WORK/'probe/putc46'
TASM_FLAGS=['/m','/mx','/kh32768','/t','putc.asm','putc.obj']
EXTERNS=['__streams','_fflush','___write','__openfd',
         '_lseek','__rtl_write','_memcpy']
FIXUP_SITES=[947,821,795,772,729,695,641,615,592,565,434,419,386,373,
             355,345,324,315,292,262,247,240,218,180,109,94,87,41,21]
PUBLICS=[(0,'__fputc'),(32,'_fputc'),(427,'_fputchar'),(451,'__FPUTN')]


def original_scope(blob):
    need(describe_omf(blob)['valid'],'full actual original buffered putc OMF')
    need([(v['name'],v['class'],v['size']) for v in segment_definitions(blob)]==
         [('_TEXT','CODE',974),('_DATA','DATA',1),('_BSS','BSS',1)],
         'all974 native CODE, one initialized CR DATA and one real BSS byte')
    need(code_publics(blob,1)==PUBLICS and externs(blob)==EXTERNS,
         'original four mixed far/near output publics and seven imported CRT providers')
    need([v.data.hex() for v in parse_omf(blob) if v.name=='GRPDEF']==
         ['08ff02ff03'],'original literal DATA/BSS group')
    fs=literal_fields(blob)
    need(len(fs)==29 and [f['site'] for f in fs]==FIXUP_SITES and
         fs[-1]['site']==21 and fs[-1]['target_method']==0 and
         fs[-1]['target']==1 and fs[-1]['frame_method']==5 and
         fs[-1]['addend']==32,
         'all29 ordered native fixups including original internal far CALL TARGET frame')
    p=payload(blob)
    code=bytes(p[1,i] for i in range(974))
    data=bytes(p[2,i] for i in range(1))
    need(data==bytes([13]),'real initialized carriage-return DATA')
    return dict(CODE_bytes=974,CODE_sha256=sha(code),
                DATA_bytes=1,DATA_sha256=sha(data),BSS_bytes=1,
                ordered_fields=fs,publics=code_publics(blob,1),
                externs=externs(blob),original_group='08ff02ff03')


def retained():
    base,files,accepted,members,prior44,parenthash=previous.retained()
    raw=(ROOT/previous.REPORT).read_bytes()
    r=json.loads(raw)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['prior_fopen_OMF_order_open'] and
         r['prior_fclose_MKNAME_frame_open'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_forty_four_source_build_sha256']==parenthash and
         r['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         r['source_sha256']==sha((ROOT/previous.SOURCE).read_bytes()) and
         len(r['rounds'])==2,
         'current native45-source original directory subsystem and linked Japanese MAINL')
    objects=[]
    for i,row in enumerate(r['rounds']):
        out={}
        for kind,q in row['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'entire unchanged previous45-source '+kind+' file')
            out[kind]=data
        need(out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'complete prior45 source original Japanese EXE/MAP')
        source=dict(prior44[i],direct=out['obj'])
        c=compare_members(members,library_members(out['lib']),source)
        need(c['replaced_members']==sorted(source) and
             c['contextual_members_unchanged']==848,
             'actual45 original source CRT members and848 untouched programs')
        objects.append(source)
    need(len(objects)==2 and objects[0]==objects[1] and
         len(objects[0])==45 and len(members)==893 and
         members[271].name=='putc',
         'two complete native original source pairs and putc at CRT index271')
    return base,files,accepted,members,objects,sha(raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,parents,parentsha=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[271].program_records,
         'original DOS putc member program identity in selected CRT')
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
           previous_forty_five_source_build_sha256=parentsha,
           original_sha256=sha(original),source_sha256=sha(source),
           driver_sha256=sha((ROOT/DRIVER).read_bytes()),
           native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/putc-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        r['phases'].append(dict(label=label,command=cmd,
                                returncode=cp.returncode,log_path=path,
                                log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1600:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated native putc CRT scratch')
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
            (SCRATCH/'putc.asm').write_bytes(source)
            os.utime(SCRATCH/'putc.asm',(946684800,946684800))
            lib_rsp=build.response(r'probe\putc46\newcrt.lib /E',
                ['+probe\\putc46\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\putc46\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\putc46\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\putc46\\newcrt.lib'),
            ):
                need(link.count(old)==1,'one genuine original MAINL normal linker slot')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(lib_rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/putc-library.rsp').write_bytes(lib_rsp)
            (ROOT/'.analysis/work/putc-link.lnk').write_bytes(link)
            for i in (1,2):
                for f in ('putc.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/f).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                native=(SCRATCH/'putc.obj').read_bytes()
                need(original_scope(native)==goal and
                     literal_fields(native)==literal_fields(original),
                     'all974 original CODE,1 DATA/1 BSS and29 ordered native OMF fields')
                sources=dict(parents[i-1],putc=native)
                for name,blob in parents[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(blob)
                run(dos+['tlib',r'@probe\putc46\library.rsp'],
                    WORK,f'round{i}-library')
                comparison=compare_members(members,
                    library_members((SCRATCH/'newcrt.lib').read_bytes()),sources)
                need(comparison['replaced_members']==sorted(sources) and
                     comparison['contextual_members_unchanged']==847,
                     '46 original native source positions and847 vendor programs unchanged')
                run(dos+['tlink',r'@probe\putc46\link.lnk'],
                    WORK,f'round{i}-link')
                output={}
                for kind,f in (('obj','putc.obj'),('lib','newcrt.lib'),
                               ('exe','linked.exe'),('map','linked.map')):
                    blob=(SCRATCH/f).read_bytes()
                    path=f'.analysis/work/putc-round{i}-{f}'
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
                print('46-source original buffered putc Japanese MAINL exact round',i,flush=True)
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
