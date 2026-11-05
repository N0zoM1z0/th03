#!/usr/bin/env python3
"""Rebuild and strictly compare the first three real FAR functions of cplx2.

SCOPED PARTIAL ONLY: do not count the 692-byte source as a fully owned
5,598-byte CRT member. Original frame method 4 is preserved in metadata,
not rewritten or silently accepted as an original-equivalent TASM OMF record.
"""
from __future__ import annotations
from collections import Counter
import fcntl
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

from lib.borland_library import library_members
from lib.omf import parse_omf
from lib.decoded_mainl_display_native import externs
from build_th03_mainl_display_work import payload, literal_fields
from probe_th03_mainl_large_fixups import original_literal_fixups
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'src/mainl/crt/cplx2_divisions_partial.asm'
WORK=ROOT/'.analysis/work/probe/cplx2-divisions-partial'
REPORT=ROOT/'.analysis/work/probe/cplx2-divisions-partial-review.json'
PUBLICS=[(0,'@complex@$brdiv$qm7complex'),
         (166,'@$bdiv$qm7complext1'),
         (405,'@$bdiv$qdm7complex')]
CODE_BYTES=692
ORIGINAL_CODE_BYTES=5598
FPU={'FIDRQQ','FIWRQQ','FIERQQ'}


def sha(raw):
    return sha256(raw).hexdigest()


def check_raw_original_and_tasm(original, assembled):
    orig=payload(original)
    made=payload(assembled)
    assert len({i for s,i in orig if s==1})==ORIGINAL_CODE_BYTES
    assert len({i for s,i in made if s==1})==CODE_BYTES
    assert all(made[1,i]==orig[1,i] for i in range(CODE_BYTES)), 'CODE prefix mismatch'
    assert code_publics(assembled,1)==PUBLICS
    assert code_publics(original,1)[:3]==PUBLICS
    assert code_publics(original,1)[3][0]==CODE_BYTES
    native_segments=segment_definitions(assembled)
    assert [(x['name'],x['class'],x['size']) for x in native_segments]==[
        ('_TEXT','CODE',692),('_DATA','DATA',0),('_BSS','BSS',0)]
    original_fixups=[f for f in original_literal_fixups(original)
                     if f['segment']==1 and f['site']<CODE_BYTES]
    compiled_fixups=literal_fields(assembled)
    assert len(original_fixups)==len(compiled_fixups)==97
    a={f['site']:f for f in original_fixups}
    b={f['site']:f for f in compiled_fixups}
    assert len(a)==len(original_fixups) and len(b)==len(compiled_fixups)
    assert set(a)==set(b)
    original_imports=externs(original)
    native_imports=externs(assembled)
    gaps=[]
    for site,old in a.items():
        now=b[site]
        for key in ('segment','site','location_type','width','segment_relative',
                    'target_method','addend'):
            assert old[key]==now[key],(site,key,old[key],now[key])
        if old['target_method']==2:
            left=original_imports[old['target']-1]
            right=native_imports[now['target']-1]
            assert left==right,(site,left,right)
        else:
            assert old['target']==now['target'],(site,old,now)
            left='local'
        if old['frame_method']==4:
            assert left in FPU,(site,left)
            assert (old['frame'],now['frame_method'],now['frame'])==(
                None,5,None),(site,old,now)
            gaps.append(site)
        else:
            assert (old['frame_method'],old['frame']) == (
                now['frame_method'],now['frame']),(site,old,now)
    assert len(gaps)==90
    return dict(
        verified_original_prefix_CODE_bytes=CODE_BYTES,
        total_original_member_CODE_bytes=ORIGINAL_CODE_BYTES,
        original_publics_total=len(code_publics(original,1)),
        complete_division_publics=PUBLICS,
        original_FIXUPP_count=97,
        exact_FIXUPP_sites_widths_targets_addends=97,
        original_frame4_vs_TASM_frame5_sites=gaps,
        original_frame4_vs_TASM_frame5_count=len(gaps),
        exact_original_raw_FIXUPP_frame_metadata=False,
        complete_original_member_source=False,
        source_linked_CRT_members_added=0,
        factory_accepted_source_credit=False,
        partial_source_sha256=sha(SOURCE.read_bytes()))


def verify():
    source=SOURCE.read_bytes()
    original_lib=ROOT/'.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB'
    m=next(m for m in library_members(original_lib.read_bytes()) if m.name=='cplx2')
    original=b'\x80\x02\x00\x00\x7e'+m.program_records
    prefix=ROOT/'.analysis/toolchain/wineprefix'
    tasm=prefix/'drive_c/TASM50/bin/TASM32.EXE'
    env=dict(os.environ,WINEPREFIX=str(prefix),WINEDEBUG='-all',
             DISPLAY='',WAYLAND_DISPLAY='',TZ='UTC',LANG='C',LC_ALL='C')
    WORK.mkdir(parents=True,exist_ok=True)
    outputs=[]
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        for round_n in (1,2):
            scratch=WORK/f'round{round_n}'
            scratch.mkdir(exist_ok=True)
            (scratch/'cplx2_divisions_partial.asm').write_bytes(source)
            cmd=['/usr/bin/wine-stable',str(tasm),
                 '/m','/mx','/kh32768','/t',
                 'cplx2_divisions_partial.asm','cplx2_divisions_partial.obj']
            result=subprocess.run(cmd,cwd=scratch,env=env,
                    stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,timeout=90)
            (scratch/'tasm.log').write_bytes(result.stdout)
            assert result.returncode==0, result.stdout.decode(errors='replace')[-1400:]
            obj=(scratch/'cplx2_divisions_partial.obj').read_bytes()
            checks=check_raw_original_and_tasm(original,obj)
            outputs.append(dict(round=round_n,
                                obj_sha256=sha(obj),
                                log_sha256=sha(result.stdout),
                                obj_bytes=len(obj),
                                relative_obj=str((scratch/'cplx2_divisions_partial.obj').relative_to(ROOT)),
                                relative_log=str((scratch/'tasm.log').relative_to(ROOT))))
    # Borland TASM emits a COMENT 40E9 native build stamp. Separate native
    # rounds may differ by its clock byte while CODE/FIXUPP remain exact.
    first=(WORK/'round1/cplx2_divisions_partial.obj').read_bytes()
    second=(WORK/'round2/cplx2_divisions_partial.obj').read_bytes()
    first_records=list(parse_omf(first))
    second_records=list(parse_omf(second))
    assert len(first_records)==len(second_records)
    mutable=[]
    for i,(a,b) in enumerate(zip(first_records,second_records)):
        assert a.name==b.name
        if a.data==b.data:continue
        assert a.name=='COMENT' and a.data[:2]==b.data[:2]==bytes.fromhex('40e9')
        assert len(a.data)==len(b.data) and a.data[3:]==b.data[3:],(i,a,b)
        mutable.append(i)
    assert len(mutable)<=1
    result=dict(**checks,native_assembly_rounds=2,
                raw_TASM_obj_sha256_equal=outputs[0]['obj_sha256']==outputs[1]['obj_sha256'],
                native_build_stamp_COMENT_record_indices=mutable,
                nonvolatile_native_OMF_records_equal=True,
                both_native_partial_obj_original_prefix_exact=True,
                rounds=outputs)
    REPORT.write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    v=verify()
    print('SCOPED cplx2 first three division functions CODE',v['verified_original_prefix_CODE_bytes'],
          'original FIXUPP sites/targets/addends',v['exact_FIXUPP_sites_widths_targets_addends'],
          'original frame4 differing from TASM frame5',v['original_frame4_vs_TASM_frame5_count'],
          'native TASM rounds',v['native_assembly_rounds'],
          'full member acceptance',v['complete_original_member_source'])
