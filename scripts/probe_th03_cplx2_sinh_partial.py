#!/usr/bin/env python3
"""Scoped original-vs-native proof of cplx2 division + acos + arg + asin + atan + cos + cosh + exp + log + log10 + three pow overloads + sin + sinh CODE+0..4207.

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
SOURCE=ROOT/'src/mainl/crt/cplx2_seventeen_functions_partial.asm'
WORK=ROOT/'.analysis/work/probe/cplx2-sinh-partial'
REPORT=ROOT/'.analysis/work/probe/cplx2-sinh-partial-review.json'
ORIGINAL_PREFIX_CODE=4208
NATIVE_PREFIX_CODE=4206
PUBLICS=[(0,'@complex@$brdiv$qm7complex'),(166,'@$bdiv$qm7complext1'),
         (405,'@$bdiv$qdm7complex'),(692,'@acos$qm7complex'),(1079,'@arg$qm7complex'),
         (1217,'@asin$qm7complex'),(1608,'@atan$qm7complex'),(1891,'@cos$qm7complex'),(2124,'@cosh$qm7complex'),(2358,'@exp$qm7complex'),(2564,'@log$qm7complex'),(2708,'@log10$qm7complex'),(2868,'@pow$qm7complexd'),(3226,'@pow$qdm7complex'),(3532,'@pow$qm7complext1'),(3741,'@sin$qm7complex'),(3974,'@sinh$qm7complex')]
FPU={'FIDRQQ','FIWRQQ','FIERQQ'}
LOCAL_FAR_CALLS={800,985}

def sha(buf):return sha256(buf).hexdigest()

def compare(original,generated):
    A=payload(original);B=payload(generated)
    code=bytes(A[1,i] for i in range(ORIGINAL_PREFIX_CODE))
    made=bytes(B[1,i] for i in range(NATIVE_PREFIX_CODE))
    assert len(code)==4208 and len(made)==4206
    # This is instruction-aware alignment, NOT byte patching or padding.
    assert code[:799]==made[:799]
    assert code[804:984]==made[803:983]
    assert code[989:4208]==made[987:4206]
    assert code[799]==code[984]==0x9a  # Borland direct FAR CALL
    assert made[799]==made[983]==0x0e  # TASM PUSH CS
    assert made[800]==made[984]==0xe8  # followed by NEAR CALL
    public=code_publics(generated,1)
    assert public[:4]==PUBLICS[:4]
    assert public[4]==(1077,'@arg$qm7complex')
    assert public[5]==(1215,'@asin$qm7complex'),public
    assert public[6]==(1606,'@atan$qm7complex'),public
    assert public[7]==(1889,'@cos$qm7complex'),public
    assert public[8]==(2122,'@cosh$qm7complex'),public
    assert public[9]==(2356,'@exp$qm7complex'),public
    assert public[10]==(2562,'@log$qm7complex'),public
    assert public[11]==(2706,'@log10$qm7complex'),public
    assert public[12]==(2866,'@pow$qm7complexd'),public
    assert public[13]==(3224,'@pow$qdm7complex'),public
    assert public[14]==(3530,'@pow$qm7complext1'),public
    assert public[15]==(3739,'@sin$qm7complex'),public
    assert public[16]==(3972,'@sinh$qm7complex'),public
    assert len(public)==17, public
    assert code_publics(original,1)[:17]==PUBLICS
    assert code_publics(original,1)[17][0]==ORIGINAL_PREFIX_CODE
    segs=segment_definitions(generated)
    assert [(s['name'],s['class'],s['size']) for s in segs]==[
        ('_TEXT','CODE',4206),('_DATA','DATA',52),('_BSS','BSS',0)]
    assert {i for s,i in B if s==2}==set(range(16,52))
    for i in range(16,52):
        assert A[2,i]==B[2,i],i
    ff=[f for f in original_literal_fixups(original)
        if f['segment']==1 and f['site']<ORIGINAL_PREFIX_CODE]
    gg=literal_fields(generated)
    assert len(ff)==654 and len(gg)==652
    native={f['site']:f for f in gg}
    assert len(native)==652
    original_imports=externs(original)
    generated_imports=externs(generated)
    omitted=[]
    frame4=[]
    imported=[]
    local_data=[]
    for f in ff:
        site=f['site']
        if site in LOCAL_FAR_CALLS:
            assert (f['target_method'],f['target'],f['addend'],
                    f['frame_method'])==(0,1,1079,5),f
            omitted.append(site)
            continue
        shifted=site if site<799 else site-1 if site<984 else site-2
        g=native.pop(shifted)
        for k in ('segment','location_type','width','segment_relative',
                  'target_method','addend'):
            assert f[k]==g[k],(site,k,f[k],g[k])
        if f['target_method']==2:
            left=original_imports[f['target']-1]
            right=generated_imports[g['target']-1]
            assert left==right,(site,left,right)
            imported.append(left)
        else:
            assert f['target']==g['target'],(site,f,g)
            local_data.append(site)
        if f['frame_method']==4:
            assert left in FPU,(site,left)
            assert (f['frame'],g['frame_method'],g['frame'])==(
                None,5,None),(site,f,g)
            frame4.append(site)
        else:
            assert (f['frame_method'],f['frame'])==(
                g['frame_method'],g['frame']),(site,f,g)
    assert len(omitted)==2 and not native
    assert len(frame4)==564 and len(local_data)==30
    return dict(
        complete_original_member_source=False,
        full_member_original_CODE_bytes=5598,
        recovered_original_prefix_CODE_bytes=4208,
        native_source_CODE_bytes=4206,
        equal_CODE_bytes_outside_two_local_FAR_calls=4198,
        original_complete_FAR_function_bodies=17,
        original_member_publics_total=22,
        exact_matching_original_fixups_site_target_addend=652,
        original_fixup_count_in_prefix=654,
        omitted_symbolic_local_FAR_calls=sorted(omitted),
        original_location_frame4_native_target_frame5_count=len(frame4),
        original_location_frame4_sites=frame4,
        original_genuine_DATA_bytes_equal=36,
        original_DATA_implicit_unmaterialized_prefix_bytes=16,
        original_Borland_complete_FIXUPP_equality=False,
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
                   SOURCE.name,'cplx2_seventeen_functions_partial.obj'],
                  cwd=dest,env=env,stdin=subprocess.DEVNULL,
                  stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
            (dest/'tasm.log').write_bytes(result.stdout)
            assert result.returncode==0,result.stdout.decode(errors='replace')[-1200:]
            blob=(dest/'cplx2_seventeen_functions_partial.obj').read_bytes()
            attested=compare(original,blob)
            rounds.append(dict(round=round_n,raw_obj_sha256=sha(blob),
                  raw_obj_bytes=len(blob),
                  relative_obj=str((dest/'cplx2_seventeen_functions_partial.obj').relative_to(ROOT)),
                  relative_log=str((dest/'tasm.log').relative_to(ROOT)),
                  log_sha256=sha(result.stdout)))
    a=(WORK/'round1/cplx2_seventeen_functions_partial.obj').read_bytes()
    b=(WORK/'round2/cplx2_seventeen_functions_partial.obj').read_bytes()
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
    print('cplx2 partial: original span',r['recovered_original_prefix_CODE_bytes'],
          'TASM',r['native_source_CODE_bytes'],
          'exact original FIXUPP site/targets',r['exact_matching_original_fixups_site_target_addend'],
          'original LOCAL FAR missing',r['omitted_symbolic_local_FAR_calls'],
          'source-linked member credit',r['source_linked_original_CRT_members_added'])
