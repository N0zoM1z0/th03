#!/usr/bin/env python3
"""Complete native-original DOS open 459 CODE/20 ordered FIXUPPs in source CRT.

Use the preserved 39-source native stat/fgets/gets/fstat carrier, with its
original Japanese target, accepted baseline and retained cold pair unchanged.
Build only open and its 40-source TLIB/TLINK normal product twice.
"""
import fcntl,json,os
from pathlib import Path
import shutil,subprocess,tomllib

import build_th03_mainl_poststat_work as previous
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
SOURCE='src/mainl/crt/open.asm'
DRIVER='scripts/build_th03_mainl_open_work.py'
REPORT='.analysis/work/mainl-open-native-build.json'
ORIGINAL=WORK/'vendor/open.obj'
SCRATCH=WORK/'probe/open40'
PARENT_MODE='fgets-gets-fstat'
TASM_FLAGS=['/m','/mx','/kh32768','/t','open.asm','open.obj']
EXTERNS=['_errno','__doserrno','__rtl_chmod','__rtl_close','_ioctl','__rtl_open',
         '__IOERROR','__openfd','__fmode','__notUmask','__exitopen','__xclose']
FIXUP_SITES=[23,68,77,92,106,118,136,146,153,212,221,263,284,
             326,377,392,394,398,400,448]


def original_scope(blob):
    need(describe_omf(blob)['valid'],'valid complete native DOS open OMF program')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(blob)]==
         [('_TEXT','CODE',459),('_DATA','DATA',0),('_BSS','BSS',0)],
         'native full 459 CODE and zero original DATA/BSS')
    need(code_publics(blob,1)==[(53,'_open')] and externs(blob)==EXTERNS,
         'two private near DOS helpers, public far _open and12 genuine imports')
    need([r.data.hex() for r in parse_omf(blob) if r.name=='GRPDEF']==
         ['08ff03ff02'],'original BSS/DATA group record')
    fields=literal_fields(blob)
    need(len(fields)==20 and [f['site'] for f in fields]==FIXUP_SITES and
         [(fields[i]['site'],fields[i]['frame_method'],fields[i]['target_method'])
          for i in (15,16,17,18)]==
         [(392,1,2),(394,5,2),(398,1,2),(400,5,2)],
         'all20 original chronological FIXUPPs including paired exit hook fields')
    code=bytes(payload(blob)[1,i] for i in range(459))
    return dict(CODE_bytes=459,CODE_sha256=sha(code),
                literal_fields=fields,imports=externs(blob),
                public_offset=53,original_group='08ff03ff02')


def retained():
    base,files,accepted,members,old36,parenthash=previous.retained()
    path=ROOT/(previous.PREFIX+PARENT_MODE+'-build.json')
    raw=path.read_bytes()
    r=json.loads(raw)
    names=previous.MODES[PARENT_MODE]
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['parent_fopen_OMF_order_open'] and r['parent_fclose_near_frame_open'] and
         r['mode']==PARENT_MODE and tuple(r['names'])==names and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_thirty_six_source_build_sha256']==parenthash and
         r['driver_sha256']==sha((ROOT/previous.DRIVER).read_bytes()) and
         r['source_sha256']=={n:sha((ROOT/('src/mainl/crt/'+n+'.asm')).read_bytes()) for n in names} and
         len(r['rounds'])==2,
         'complete native 39-source original CRT with preceding metadata gaps explicit')
    output=[]
    for idx,row in enumerate(r['rounds']):
        raw_outputs={}
        for kind,q in row['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'current source-bound previous39 '+kind+' raw vector')
            raw_outputs[kind]=data
        need(raw_outputs['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes() and
             raw_outputs['map']==(WORK/'obj/th03/mainl.map').read_bytes(),
             'preceding 39-source entire Japanese original EXE/MAP byte equal')
        sources=dict(old36[idx],**{n:raw_outputs[n] for n in names})
        c=compare_members(members,library_members(raw_outputs['lib']),sources)
        need(c['replaced_members']==sorted(sources) and
             c['contextual_members_unchanged']==854,
             '39 original sources and854 unchanged original member program records')
        output.append(sources)
    need(len(output)==2 and output[0]==output[1] and len(output[0])==39 and
         len(members)==893 and members[267].name=='open',
         'identical 39 native source vectors and real open library member267')
    return base,files,accepted,members,output,sha(raw)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    base,files,accepted,members,parents,parentsha=retained()
    original=ORIGINAL.read_bytes()
    need(object_program_records(original)==members[267].program_records,
         'original DOS open member program identity in selected CRT')
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
           previous_thirty_nine_source_build_sha256=parentsha,
           original_sha256=sha(original),source_sha256=sha(source),
           driver_sha256=sha((ROOT/DRIVER).read_bytes()),
           native_assembler_flags=TASM_FLAGS,phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    def run(cmd,cwd,label):
        cp=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,timeout=120)
        path=f'.analysis/work/open-{label}.log'
        (ROOT/path).write_bytes(cp.stdout)
        r['phases'].append(dict(label=label,command=cmd,
                                returncode=cp.returncode,log_path=path,
                                log_sha256=sha(cp.stdout)))
        save()
        need(cp.returncode==0,label+': '+cp.stdout.decode(errors='replace')[-1600:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'new original open isolated native scratch')
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
            (SCRATCH/'open.asm').write_bytes(source)
            os.utime(SCRATCH/'open.asm',(946684800,946684800))
            lib_rsp=build.response(r'probe\open40\newcrt.lib /E',
                ['+probe\\open40\\'+m.name+'.obj' for m in members])
            link=xx.link_response(files)
            for old,new in (
                (b'probe\\xxwhole\\xxfull.exe',b'probe\\open40\\linked.exe'),
                (b'probe\\xxwhole\\xxfull.map',b'probe\\open40\\linked.map'),
                (b'probe\\xxwhole\\xxcrt.lib',b'probe\\open40\\newcrt.lib'),
            ):
                need(link.count(old)==1,'one genuine original MAINL normal linker slot')
                link=link.replace(old,new)
            (SCRATCH/'library.rsp').write_bytes(lib_rsp)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/open-library.rsp').write_bytes(lib_rsp)
            (ROOT/'.analysis/work/open-link.lnk').write_bytes(link)
            for i in (1,2):
                for f in ('open.obj','newcrt.lib','newcrt.bak','linked.exe','linked.map'):
                    (SCRATCH/f).unlink(missing_ok=True)
                run(tasm+TASM_FLAGS,SCRATCH,f'round{i}-assemble')
                native=(SCRATCH/'open.obj').read_bytes()
                need(original_scope(native)==goal and
                     literal_fields(native)==literal_fields(original),
                     'all459 original CODE bytes and literal 20 ordered OMF fixups')
                sources=dict(parents[i-1],open=native)
                for name,blob in parents[i-1].items():
                    (SCRATCH/(name+'.obj')).write_bytes(blob)
                run(dos+['tlib',r'@probe\open40\library.rsp'],
                    WORK,f'round{i}-library')
                comparison=compare_members(members,
                    library_members((SCRATCH/'newcrt.lib').read_bytes()),sources)
                need(comparison['replaced_members']==sorted(sources) and
                     comparison['contextual_members_unchanged']==853,
                     '40 original native source slots with853 other vendor program records')
                run(dos+['tlink',r'@probe\open40\link.lnk'],
                    WORK,f'round{i}-link')
                output={}
                for kind,f in (('obj','open.obj'),('lib','newcrt.lib'),
                               ('exe','linked.exe'),('map','linked.map')):
                    blob=(SCRATCH/f).read_bytes()
                    path=f'.analysis/work/open-round{i}-{f}'
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
                print('Original 40-source DOS open Japanese MAINL EXE/MAP exact round',i,flush=True)
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
