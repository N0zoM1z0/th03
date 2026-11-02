#!/usr/bin/env python3
"""Verify the original qsort far public wrapper and near swap,not its core.

An isolated short RET 6 core placeholder exposes the original qsort_core
near-call ABI but is not a reconstruction of the real 666-byte core.
No original qsort library member is replaced or accepted here.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_work as build
from build_th03_mainl_resources_work import need,sha,cold_context
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.omf import describe_omf,parse_omf
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

ROOT=Path(__file__).resolve().parents[1]
WORK=build.WORK
SOURCES=('src/mainl/crt/qswap.inl','src/mainl/crt/qentry.inl')
DRIVER='scripts/probe_th03_mainl_qsort_entry.py'
REPORT='.analysis/work/mainl-qsort-entry-build.json'
ORIGINAL=WORK/'vendor/qsort.obj'
SCRATCH=WORK/'probe/qentrmini'
WRAPPER=""".8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
qsort_compare dd ?
qsort_width dw ?
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
include qswap.inl
; Genuine original recursive core is 666 bytes but not reconstructed.
; This three-byte ABI-only stub has the same entry coordinate 0x2E
; without manufacturing 666 fake bytes or publishing an exact object.
qsort_core proc near
    ret 6
qsort_core endp
include qentry.inl
_TEXT ends
end
"""


def proof(obj):
    raw=ORIGINAL.read_bytes()
    a,b=payload(raw),payload(obj)
    need(bytes(a[1,i] for i in range(46))==
         bytes(b[1,i] for i in range(46)),
         'all46 original swap helper opcode bytes remain literally equal')
    original_entry=bytes(a[1,i] for i in range(712,756))
    candidate_start=code_publics(obj,1)[0][0]
    need(candidate_start==49,'real complete46-byte swap and3-byte ABI stub')
    current_entry=bytes(b[1,i] for i in range(candidate_start,candidate_start+44))
    needed={(38,39)}
    different=[i for i,(x,y) in enumerate(zip(original_entry,current_entry)) if x!=y]
    need(different==[38,39] and
         original_entry[:38]==current_entry[:38] and
         original_entry[40:]==current_entry[40:] and
         original_entry[37]==current_entry[37]==0xE8,
         'all42 non-call operand qsort wrapper bytes exact')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16)
    for data,start in ((original_entry,712),(current_entry,candidate_start)):
        instructions=list(decoder.disasm(data,start))
        need(sum(inst.size for inst in instructions)==44 and
             instructions[-1].mnemonic=='retf','whole original far qsort body')
        x=next(ins for ins in instructions if ins.address==start+37)
        disp=int.from_bytes(x.bytes[1:3],'little',signed=True)
        need(x.mnemonic=='call' and
             (x.address+x.size+disp)&65535==46,
             'genuine near CALL from public qsort to the core start0x2E')
    orig_fields=literal_fields(raw)
    cand_fields=literal_fields(obj)
    def relevant(fields,start,span):
        return [dict(f,site=f['site']-start) for f in fields
                if f['segment']==1 and start<=f['site']<start+span]
    old_swap=relevant(orig_fields,0,46)
    new_swap=relevant(cand_fields,0,46)
    old_entry=relevant(orig_fields,712,44)
    new_entry=relevant(cand_fields,candidate_start,44)
    need(old_swap==new_swap and old_entry==new_entry and
         [f['site'] for f in old_swap]==[9] and
         [f['site'] for f in old_entry]==[9,23,26],
         'original qsort BSS first and final three literal field offsets/order')
    need([r.data.hex() for r in parse_omf(obj) if r.name=='GRPDEF']==
         ['08ff03ff02'] and
         [(s['name'],s['size']) for s in segment_definitions(obj)]==
         [('_TEXT',93),('_DATA',0),('_BSS',6)],
         'only real swap,three-byte ABI marker,far entry and6-byte BSS')
    return dict(original_full_CODE=756,original_total_native_fields=29,
                original_near_swap_BYTES=46,original_far_public_BYTES=44,
                far_public_literal_bytes_equal=42,
                unresolved_symbolic_near_CALL_BYTES=2,
                near_core_remaining_BYTES=666,
                original_field_recovered_offsets=[9,721,735,738],
                original_relative_field_offsets=[9,9,23,26],
                actual_source_public_OFFSET=candidate_start,
                source_near_call_target_OFFSET=46,
                complete_qsort=False)


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    cold_context(ROOT)
    original=ORIGINAL.read_bytes()
    need(segment_definitions(original)[0]['size']==756 and
         len(literal_fields(original))==29,
         'unchanged full original qsort original bytes and fields')
    sources={p:(ROOT/p).read_bytes() for p in SOURCES}
    cfg=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/cfg['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),TZ='UTC',LANG='C',LC_ALL='C')
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    report=dict(complete=False,complete_qsort=False,source_acceptance=False,
                accepted_source_bytes=0,original_cold_rebuilt=False,
                original_object_sha256=sha(original),
                source_sha256={p:sha(raw) for p,raw in sources.items()},
                driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                isolated_wrapper_sha256=sha(WRAPPER.encode()),
                rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        need(not SCRATCH.exists(),'fresh bounded original qsort partial TU')
        SCRATCH.mkdir()
        try:
            for p,raw in sources.items():
                (SCRATCH/Path(p).name).write_bytes(raw)
            (SCRATCH/'qentr.asm').write_bytes(WRAPPER.encode())
            for n in (1,2):
                (SCRATCH/'qentr.obj').unlink(missing_ok=True)
                cp=subprocess.run(tasm+['/m','/mx','/kh32768','/t',
                                        'qentr.asm','qentr.obj'],
                                  cwd=SCRATCH,env=env,stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,timeout=90)
                where=f'.analysis/work/qsort-entry-round{n}.log'
                (ROOT/where).write_bytes(cp.stdout)
                need(cp.returncode==0,'bounded original qsort native TASM: '+
                     cp.stdout.decode(errors='replace')[-1000:])
                output=(SCRATCH/'qentr.obj').read_bytes()
                need(describe_omf(output)['valid'],'valid actual native qsort partial OMF')
                details=proof(output)
                outfile=f'.analysis/work/qsort-entry-round{n}.obj'
                (ROOT/outfile).write_bytes(output)
                report['rounds'].append(dict(round=n,output=outfile,
                    output_bytes=len(output),output_sha256=sha(output),
                    log=where,log_sha256=sha(cp.stdout),scope=details))
                save()
                print('qsort original swap+far public wrapper semantic native round',n,flush=True)
            need(report['rounds'][0]['output_sha256']==report['rounds'][1]['output_sha256'],
                 'two identical complete native partial OMF objects')
        finally:shutil.rmtree(SCRATCH)
    need(original==ORIGINAL.read_bytes() and
         {p:sha((ROOT/p).read_bytes()) for p in sources}==report['source_sha256'],
         'original game/source unchanged during bounded proof')
    report['complete']=True
    save()


if __name__=='__main__':
    main()
