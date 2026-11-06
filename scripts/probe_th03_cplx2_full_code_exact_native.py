#!/usr/bin/env python3
"""Scoped original-vs-native proof of cplx2 all 22 original FAR functions plus private INIT CODE+0..5597.

Native TASM emits two 4-byte PUSH CS/NEAR CALL sequences for Borland's
5-byte intra-segment direct FAR CALL. Preserve and report both real gaps.
Never count the full original 5,598-byte cplx2 as source-linked.
"""
from __future__ import annotations
from hashlib import sha256
import fcntl,json,os
from pathlib import Path
import subprocess
from lib.borland_library import library_members
from lib.omf import parse_omf
from lib.decoded_mainl_display_native import externs
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_mainl_large_fixups import original_literal_fixups
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'src/mainl/crt/cplx2_complete_code_native.asm'
WORK=ROOT/'.analysis/work/probe/cplx2-complete-code-native'
REPORT=ROOT/'.analysis/work/probe/cplx2-complete-code-native-review.json'
ORIGINAL_PREFIX_CODE=5598
NATIVE_PREFIX_CODE=5596
PUBLICS=[(0,'@complex@$brdiv$qm7complex'),(166,'@$bdiv$qm7complext1'),
         (405,'@$bdiv$qdm7complex'),(692,'@acos$qm7complex'),(1079,'@arg$qm7complex'),
         (1217,'@asin$qm7complex'),(1608,'@atan$qm7complex'),(1891,'@cos$qm7complex'),(2124,'@cosh$qm7complex'),(2358,'@exp$qm7complex'),(2564,'@log$qm7complex'),(2708,'@log10$qm7complex'),(2868,'@pow$qm7complexd'),(3226,'@pow$qdm7complex'),(3532,'@pow$qm7complext1'),(3741,'@sin$qm7complex'),(3974,'@sinh$qm7complex'),(4208,'@sqrt$qm7complex'),(4429,'@tan$qm7complex'),(4781,'@tanh$qm7complex'),(5091,'@$blsh$qm7ostreamm7complex'),(5269,'@$brsh$qm7istreamm7complex')]
FPU={'FIDRQQ','FIWRQQ','FIERQQ'}
LOCAL_FAR_CALLS={800,985}

def sha(buf):return sha256(buf).hexdigest()

def compare(original,generated):
    A=payload(original);B=payload(generated)
    code=bytes(A[1,i] for i in range(5598))
    made=bytes(B[1,i] for i in range(5598))
    assert code==made and len(code)==len(made)==5598, (
        [(i,a,b) for i,(a,b) in enumerate(zip(code,made)) if a!=b][:12])
    original_publics=code_publics(original,1)
    native_publics=code_publics(generated,1)
    assert original_publics==PUBLICS==native_publics
    assert len(native_publics)==22
    assert [rec.data.hex() for rec in parse_omf(original) if rec.name=='GRPDEF']==["0aff02ff03"]
    assert [rec.data.hex() for rec in parse_omf(generated) if rec.name=='GRPDEF']==["0aff02ff03"]
    assert [(s['name'],s['class'],s['size'])
            for s in segment_definitions(generated)]==[
             ('_TEXT','CODE',5598),('_DATA','DATA',63),
             ('_BSS','BSS',0),('_INIT_','INITDATA',6)]
    assert {i for s,i in B if s==2}==set(range(16,63))
    assert all((2,i) not in A and (2,i) not in B for i in range(16))
    assert all(A[2,i]==B[2,i] for i in range(16,63))
    assert bytes(A[4,i] for i in range(6))==bytes(
           B[4,i] for i in range(6))==bytes.fromhex('0120c7150000')
    originals=original_literal_fixups(original)
    generated_fields=literal_fields(generated)
    assert len(originals)==len(generated_fields)==860
    assert sum(f['segment']==1 for f in originals)==859
    assert sum(f['segment']==1 for f in generated_fields)==859
    original_init=[f for f in originals if f['segment']==4]
    native_init=[f for f in generated_fields if f['segment']==4]
    assert original_init==native_init and len(original_init)==1
    assert (original_init[0]['site'],original_init[0]['location_type'],
            original_init[0]['target_method'],original_init[0]['target'],
            original_init[0]['addend'])==(2,3,0,1,5575)
    original_imports=externs(original)
    native_imports=externs(generated)
    assert len(original_imports)==len(native_imports)==24
    assert set(original_imports)==set(native_imports)
    assert '__turboFloat' in native_imports
    original_code=[f for f in originals if f['segment']==1]
    native_code={f['site']:f for f in generated_fields if f['segment']==1}
    assert len(native_code)==859
    original_frame4=[]
    near_frame=[]
    frame_equal=[]
    for f in original_code:
        site=f['site']
        g=native_code.pop(site)
        for key in ('segment','site','location_type','width',
                    'segment_relative','target_method','addend'):
            assert f[key]==g[key],(site,key,f,g)
        if f['target_method']==2:
            symbol=original_imports[f['target']-1]
            assert symbol==native_imports[g['target']-1],(site,symbol,g)
        else:
            symbol=None
            assert f['target']==g['target'],(site,f,g)
        if f['frame_method']==4:
            assert symbol in FPU,(site,symbol)
            assert (f['frame'],g['frame_method'],g['frame'])==(
                None,5,None),(site,f,g)
            original_frame4.append(site)
        elif site==5561:
            assert (symbol,f['frame_method'],f['frame'],
                    g['frame_method'],g['frame'])==(
                'N_SCOPY@',5,None,0,1),(site,f,g)
            near_frame.append(site)
        else:
            assert (f['frame_method'],f['frame'])==(
                g['frame_method'],g['frame']),(site,f,g)
            frame_equal.append(site)
    assert not native_code
    assert len(original_frame4)==734
    assert near_frame==[5561]
    assert sorted(site for site in (800,985) if any(
        f['site']==site and f['target_method']==0 and
        f['target']==1 and f['addend']==1079
        for f in original_code))==[800,985]
    return dict(
        all_original_22_FAR_bodies_reconstructed=True,
        original_CODE_bytes=5598,
        native_CODE_bytes=5598,
        original_CODE_bytes_equal=True,
        original_publics_count=22,
        original_DATA_bytes=63,
        original_GROUPDEF_equal=True,
        original_DATA_implicit_prefix_bytes=16,
        original_initialized_DATA_bytes_equal=47,
        original_INITDATA_bytes=6,
        original_INITDATA_bytes_equal=True,
        original_init_routine_CODE_offset=5575,
        original_OMF_fixups_total=860,
        native_OMF_fixups_total=860,
        exact_matching_symbolic_fixup_sites_targets_addends=860,
        original_location_frame4_native_target_frame5_count=734,
        original_location_frame4_sites=original_frame4,
        imported_near_target_frame5_vs_code_frame0_sites=near_frame,
        same_CODE_direct_FAR_CALLs_recovered=[800,985],
        original_unused_extdef_retained_in_native=['__turboFloat'],
        original_raw_Borland_OBJ_equal=False,
        complete_original_raw_FIXUPP_frames_equal=False,
        complete_native_MAINL_link_accepted=False,
        source_linked_original_CRT_members_added=0,
        formal_Factory_source_credit=False,
        native_source_sha256=sha(SOURCE.read_bytes()))

def verify():
    originals=library_members((ROOT/'.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes())
    ms=[m for m in originals if m.name=='cplx2']
    assert len(ms)==1
    original=b'\x80\x02\x00\x00\x7e'+ms[0].program_records
    source=SOURCE.read_bytes()
    prefix=ROOT/'.analysis/toolchain/wineprefix'
    tasm=prefix/'drive_c/TASM50/bin/TASM32.EXE'
    env=dict(os.environ,WINEPREFIX=str(prefix),WINEDEBUG='-all',
             DISPLAY='',WAYLAND_DISPLAY='',TZ='UTC',LANG='C',LC_ALL='C')
    WORK.mkdir(parents=True,exist_ok=True)
    rounds=[]
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for round_n in (1,2):
            dest=WORK/f'round{round_n}'
            dest.mkdir(exist_ok=True)
            (dest/SOURCE.name).write_bytes(source)
            result=subprocess.run(['/usr/bin/wine-stable',str(tasm),
                   '/m','/mx','/kh32768','/t',
                   SOURCE.name,'cplx2_complete_code_native.obj'],
                  cwd=dest,env=env,stdin=subprocess.DEVNULL,
                  stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
            (dest/'tasm.log').write_bytes(result.stdout)
            assert result.returncode==0,result.stdout.decode(errors='replace')[-1200:]
            blob=(dest/'cplx2_complete_code_native.obj').read_bytes()
            attested=compare(original,blob)
            rounds.append(dict(round=round_n,raw_obj_sha256=sha(blob),
                  raw_obj_bytes=len(blob),
                  relative_obj=str((dest/'cplx2_complete_code_native.obj').relative_to(ROOT)),
                  relative_log=str((dest/'tasm.log').relative_to(ROOT)),
                  log_sha256=sha(result.stdout)))
    a=(WORK/'round1/cplx2_complete_code_native.obj').read_bytes()
    b=(WORK/'round2/cplx2_complete_code_native.obj').read_bytes()
    aa=list(parse_omf(a));bb=list(parse_omf(b))
    assert len(aa)==len(bb)
    variable=[]
    for i,(x,y) in enumerate(zip(aa,bb)):
        assert x.name==y.name
        if x.data==y.data:continue
        assert x.name=='COMENT' and x.data[:2]==y.data[:2]==bytes.fromhex('40e9')
        assert x.data[3:]==y.data[3:] and len(x.data)==len(y.data)
        variable.append(i)
    assert len(variable)<=1
    report=dict(**attested,native_TASM_rounds=2,
        native_nonvolatile_OMF_rounds_equal=True,
        native_COMENT_clock_record_indices=variable,
        raw_native_obj_sha_equal=sha(a)==sha(b),rounds=rounds)
    REPORT.write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    r=verify()
    print('cplx2 complete CODE',r['original_CODE_bytes'],
          '22 original functions, symbolic OMF fields',r['original_OMF_fixups_total'],
          'FPU frame gaps',r['original_location_frame4_native_target_frame5_count'],
          'full-link source credit',r['source_linked_original_CRT_members_added'])
