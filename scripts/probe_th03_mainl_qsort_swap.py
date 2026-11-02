#!/usr/bin/env python3
"""Native 8086 source proof of the first helper of Borland's 756-byte qsort.

This is NOT a full qsort implementation or library replacement: the
original 46-byte near swap helper and first literal BSS relocation
are recovered in isolation using real TASM,without padding or a
manufactured qsort core. The original full object remains unchanged.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_work as build
from build_th03_mainl_resources_work import cold_context,need,sha
from build_th03_mainl_display_work import literal_fields,payload
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.omf import describe_omf,parse_omf

ROOT=Path(__file__).resolve().parents[1]
WORK=build.WORK
SOURCE='src/mainl/crt/qswap.inl'
DRIVER='scripts/probe_th03_mainl_qsort_swap.py'
REPORT='.analysis/work/mainl-qsort-swap-build.json'
SCRATCH=WORK/'probe/qsortmini'
ORIGINAL=WORK/'vendor/qsort.obj'
STUB=""".8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
qsort_compare dd ?
qsort_width dw ?
_BSS ends
; In this original TASM partial context DATA-first declaration
; restores the literal original BSS-before-DATA OMF GRPDEF.
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
include qswap.inl
_TEXT ends
end
"""


def original_prefix(raw):
    s=segment_definitions(raw)
    need([(x['name'],x['size']) for x in s][0]==('_TEXT',s[0]['size']) and
         [(x['name'],x['size']) for x in s[1:]]==
         [('_DATA',0),('_BSS',6)],'original qsort 6-byte live BSS')
    p=payload(raw)
    return bytes(p[1,i] for i in range(46))


def field0(raw):
    f=[f for f in literal_fields(raw) if f['segment']==1 and f['site']<46]
    need(len(f)==1,'one original source width field in the swap helper')
    need(f[0]==dict(segment=1,site=9,location_type=1,width=2,
                    segment_relative=True,frame_method=1,frame=1,
                    target_method=0,target=3,addend=4),
         'native compiler BSS element-width OMF field at CODE+9')
    return f


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    cold_context(ROOT)
    original=ORIGINAL.read_bytes()
    need(segment_definitions(original)[0]['size']==756,
         'full original qsort contains more code than this isolated helper')
    first=original_prefix(original);field0(original)
    need([r.data.hex() for r in parse_omf(original) if r.name=='GRPDEF']==
         ['08ff03ff02'],'literal original qsort DATA/BSS GRPDEF')
    source=(ROOT/SOURCE).read_bytes()
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),TZ='UTC',LANG='C',LC_ALL='C')
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    report=dict(complete=False,source_acceptance=False,
                accepted_source_bytes=0,complete_qsort=False,
                original_cold_rebuilt=False,original_object_sha256=sha(original),
                source_sha256=sha(source),driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                native_wrapper_sha256=sha(STUB.encode()),rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh isolated native qsort swap test')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'qswap.inl').write_bytes(source)
            (SCRATCH/'qswprobe.asm').write_bytes(STUB.encode())
            for i in (1,2):
                (SCRATCH/'qswprobe.obj').unlink(missing_ok=True)
                cp=subprocess.run(tasm+['/m','/mx','/kh32768','/t',
                                        'qswprobe.asm','qswprobe.obj'],
                                  cwd=SCRATCH,env=env,stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,timeout=90)
                logpath=f'.analysis/work/qsort-swap-round{i}.log'
                (ROOT/logpath).write_bytes(cp.stdout)
                need(cp.returncode==0,'actual TASM partial swap helper compilation: '+
                     cp.stdout.decode(errors='replace')[-1000:])
                output=(SCRATCH/'qswprobe.obj').read_bytes()
                need(describe_omf(output)['valid'] and
                     segment_definitions(output)[0]['size']==46 and
                     original_prefix(output)==first and
                     field0(output)==field0(original),
                     'all46 raw original qsort swap instructions/ordered BSS fixup')
                need([r.data.hex() for r in parse_omf(output)
                      if r.name=='GRPDEF']==['08ff03ff02'],
                     'literal original group order preserved')
                where=f'.analysis/work/qsort-swap-round{i}.obj'
                (ROOT/where).write_bytes(output)
                report['rounds'].append(dict(round=i,obj_path=where,
                    obj_sha256=sha(output),obj_bytes=len(output),
                    log_path=logpath,log_sha256=sha(cp.stdout),
                    prefix_CODE_sha256=sha(first),single_native_FIXUPP=field0(output)))
                save()
                print('Actual native qsort 46-byte near swap helper exact round',i,flush=True)
            need(report['rounds'][0]['obj_sha256']==report['rounds'][1]['obj_sha256'],
                 'two identical full raw native qsort helper OMF objects')
        finally:
            shutil.rmtree(SCRATCH)
    need((ROOT/SOURCE).read_bytes()==source and ORIGINAL.read_bytes()==original,
         'no original/maintained source changes during bounded test')
    report['complete']=True
    save()


if __name__=='__main__':
    main()
