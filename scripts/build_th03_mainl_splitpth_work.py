#!/usr/bin/env python3
"""Complete original DOS path splitter850 CODE and20 literal ordered OMF fields in source CRT.

Use retained46-source original CRT carrier, with its
original Japanese target, accepted baseline and retained cold pair unchanged.
Build only original splitpth in a 47-source native TLIB/TLINK normal product.
"""
import fcntl,json,os
from pathlib import Path
import shutil,subprocess,tomllib

import build_th03_mainl_putc_work as previous
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
SOURCE='src/mainl/crt/splitpth.asm'
DRIVER='scripts/build_th03_mainl_splitpth_work.py'
REPORT='.analysis/work/mainl-splitpth-native-build.json'
ORIGINAL=WORK/'vendor/splitpth.obj'
SCRATCH=WORK/'probe/splt47'
TASM_FLAGS=['/m','/mx','/kh32768','/t','splitpth.asm','splitpth.obj']
EXTERNS=['_strcpy','_strlen','_strncpy','___path_issbcs']
FIXUP_SITES=[802,800,798,796,794,792,790,611,418,376,331,228,226,224,222,
             168,138,79,47,20]
PUBLICS=[(230,'___fnsplit'),(804,'__splitpath')]


def original_scope(blob):
    need(describe_omf(blob)['valid'],'valid original Borland path parser OMF')
    need([(v['name'],v['class'],v['size']) for v in segment_definitions(blob)]==
         [('_TEXT','CODE',850),('_DATA','DATA',0),('_BSS','BSS',0)],
         'complete 850-byte original CODE and genuine zero DATA/BSS')
    need(code_publics(blob,1)==PUBLICS and externs(blob)==EXTERNS,
         'two original far path splitting entries and four CRT imported helpers')
    need([r.data.hex() for r in parse_omf(blob) if r.name=='GRPDEF']==
         ['08ff02ff03'],'original DATA-before-BSS DGROUP')
    fields=literal_fields(blob)
    need(len(fields)==20 and [f['site'] for f in fields]==FIXUP_SITES and
         all(f['target_method']==0 and f['target']==1 and
             f['frame_method']==5 for f in fields[:7]+fields[11:15]),
         'all original20 ordered fields, original11 true CODE-table relocs')
    p=payload(blob)
    CODE=bytes(p[1,i] for i in range(850))
    need(CODE[214:222]==bytes.fromhex('00002f003a005c00') and
         CODE[776:790]==bytes.fromhex('00002a002e002f003a003f005c00'),
         'real original path token classification WORD tables in CODE')
    return dict(CODE_bytes=850,CODE_sha256=sha(CODE),
                true_CODE_data_tables_bytes=44,
                ordered_fixups=fields,pubs=code_publics(blob,1),
                imports=externs(blob),group='08ff02ff03')


def retained():
    base,files,accepted,members,preceding45,parenthash=previous.retained()
    raw=(ROOT/previous.REPORT).read_bytes()
    r=json.loads(raw)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['prior_fopen_OMF_order_open'] and r['prior_fclose_MKNAME_frame_open'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_forty_five_source_build_sha256']==parenthash and
         r['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         r['source_sha256']==sha((ROOT/previous.SOURCE).read_bytes()) and
         len(r['rounds'])==2,
         'current source-bound46-member original putc CRT carrier')
    objects=[]
    for i,row in enumerate(r['rounds']):
        out={}
        for kind,meta in row['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'complete inherited original46-source '+kind+' raw byte vector')
            out[kind]=data
        need(out['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'original46-source complete decoded Japanese MAINL EXE/MAP')
        sources=dict(preceding45[i],putc=out['obj'])
        comparison=compare_members(members,library_members(out['lib']),sources)
        need(comparison['replaced_members']==sorted(sources) and
             comparison['contextual_members_unchanged']==847,
             '46 original source positions and847 unchanged vendor programs')
        objects.append(sources)
    need(len(objects)==2 and objects[0]==objects[1] and
         len(objects[0])==46 and len(members)==893 and
         members[286].name=='splitpth',
         'two identical real original source vectors and path module index286')
    return base,files,accepted,members,objects,sha(raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,parents,parentsha=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[286].program_records,
         'original DOS splitpth member program identity in selected CRT')
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
           previous_forty_six_source_build_sha256=parentsha,
           original_sha256=sha(original),source_sha256=sha(source),
           driver_sha256=sha((ROOT/DRIVER).read_bytes()),
           native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/splitpth-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        r['phases'].append(dict(label=label,command=cmd,
                                returncode=cp.returncode,log_path=path,
                                log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1600:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated native splitpth CRT scratch')
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
            (SCRATCH/'splitpth.asm').write_bytes(source)
            os.utime(SCRATCH/'splitpth.asm',(946684800,946684800))
            lib_rsp=build.response(r'probe\splt47\newcrt.lib /E',
                ['+probe\\splt47\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\splt47\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\splt47\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\splt47\\newcrt.lib'),
            ):
                need(link.count(old)==1,'one genuine original MAINL normal linker slot')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(lib_rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/splitpth-library.rsp').write_bytes(lib_rsp)
            (ROOT/'.analysis/work/splitpth-link.lnk').write_bytes(link)
            for i in (1,2):
                for f in ('splitpth.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/f).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                native=(SCRATCH/'splitpth.obj').read_bytes()
                need(original_scope(native)==goal and
                     literal_fields(native)==literal_fields(original),
                     'all850 original CODE bytes including real switch tables and20 ordered OMF fields')
                sources=dict(parents[i-1],splitpth=native)
                for name,blob in parents[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(blob)
                run(dos+['tlib',r'@probe\splt47\library.rsp'],
                    WORK,f'round{i}-library')
                comparison=compare_members(members,
                    library_members((SCRATCH/'newcrt.lib').read_bytes()),sources)
                need(comparison['replaced_members']==sorted(sources) and
                     comparison['contextual_members_unchanged']==846,
                     '47 original source CRT positions and846 vendor programs unchanged')
                run(dos+['tlink',r'@probe\splt47\link.lnk'],
                    WORK,f'round{i}-link')
                output={}
                for kind,f in (('obj','splitpth.obj'),('lib','newcrt.lib'),
                               ('exe','linked.exe'),('map','linked.map')):
                    blob=(SCRATCH/f).read_bytes()
                    path=f'.analysis/work/splitpth-round{i}-{f}'
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
                print('47-source original splitpth Japanese MAINL exact round',i,flush=True)
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
