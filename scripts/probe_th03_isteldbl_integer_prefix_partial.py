#!/usr/bin/env python3
"""Native two-round original integer-prefix proof for the huge 1947-byte parser.

One unresolved near jump uses a symbolic external, not target displacement
bytes: its two original operand bytes are explicitly excluded. No full
istream long-double member or linked EXE credit is asserted.
"""
from __future__ import annotations
import fcntl,json,os,subprocess
from hashlib import sha256
from pathlib import Path
from lib.borland_library import library_members
from lib.omf import parse_omf
from lib.decoded_mainl_display_native import externs
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_mainl_large_fixups import original_literal_fixups
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'src/mainl/crt/isteldbl_integer_prefix_partial.asm'
WORK=ROOT/'.analysis/work/probe/isteldbl-integer-prefix-proof'
REPORT=ROOT/'.analysis/work/probe/isteldbl-integer-prefix-review.json'
FPU={'FIDRQQ','FIWRQQ','FIERQQ'}
PREFIX=460
UNRESOLVED_OPERAND={30,31}
def sha(b):return sha256(b).hexdigest()
def check(original,native):
    A=payload(original);B=payload(native)
    assert next(x['size'] for x in segment_definitions(original) if x['class']=='CODE')==1947
    assert [(x['name'],x['class'],x['size'])
            for x in segment_definitions(native)]==[
              ('_TEXTA','CODE',460),('_DATA','DATA',4),('_BSS','BSS',0)]
    assert code_publics(original,1)==code_publics(native,1)==[(0,'@istream@$brsh$qmg')]
    assert [r.data.hex() for r in parse_omf(native) if r.name=='GRPDEF']==['08ff02ff03']
    assert set(i for seg,i in B if seg==1)==set(range(PREFIX))
    assert set(i for seg,i in B if seg==2)==set(range(4))
    assert all(A[2,i]==B[2,i] for i in range(4))
    different={i for i in range(PREFIX) if A[1,i]!=B[1,i]}
    assert different==UNRESOLVED_OPERAND,sorted(different)[:20]
    assert A[1,29]==B[1,29]==0xe9
    assert bytes(A[1,i] for i in (30,31))==bytes.fromhex('6f07')
    assert bytes(B[1,i] for i in (30,31))==bytes.fromhex('0000')
    originals=[x for x in original_literal_fixups(original)
               if x['segment']==1 and x['site']<PREFIX]
    compiled=literal_fields(native)
    assert len(originals)==16 and len(compiled)==17
    oi=externs(original);ni=externs(native)
    origsites={f['site'] for f in originals}
    extra=[g for g in compiled if g['site'] not in origsites]
    assert len(extra)==1 and extra[0]['site']==30
    assert ni[extra[0]['target']-1]=='parser_eof'
    assert extra[0]['location_type']==1 and extra[0]['width']==2
    frame4=[]
    for f in originals:
        matches=[g for g in compiled if g['site']==f['site']]
        assert len(matches)==1
        g=matches[0]
        for key in ('segment','site','location_type','width',
                    'segment_relative','target_method','addend'):
            assert f[key]==g[key],(f['site'],key)
        if f['target_method']==2:
            symbol=oi[f['target']-1]
            assert symbol==ni[g['target']-1]
        else:
            symbol=None
            assert f['target']==g['target']
        if f['frame_method']==4:
            assert symbol in FPU
            assert (f['frame'],g['frame_method'],g['frame'])==(None,5,None)
            frame4.append(f['site'])
        else:
            assert (f['frame_method'],f['frame'])==(g['frame_method'],g['frame'])
    assert len(frame4)==9
    return dict(original_member_CODE_bytes=1947,
                original_prefix_CODE_bytes=460,
                original_equal_prefix_CODE_bytes=458,
                original_unresolved_jump_operand_sites=[30,31],
                original_unresolved_jump_destination=0x78f,
                original_prefix_fixups=16,
                native_total_fixups_including_unresolved_jump=17,
                original_x87_frame4_vs_tasm_frame5_count=9,
                original_x87_frame4_sites=frame4,
                original_initialized_DATA_prefix_bytes_equal=4,
                original_publics_equal=True,
                complete_original_member_source=False,
                complete_native_MAINL_link=False,
                source_linked_original_CRT_members_added=0,
                formal_Factory_source_credit=False,
                native_source_sha256=sha(SOURCE.read_bytes()))
def verify():
    members=library_members((ROOT/'.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes())
    original=b'\x80\x02\x00\x00\x7e'+next(m.program_records for m in members if m.name=='isteldbl')
    work=WORK
    work.mkdir(parents=True,exist_ok=True)
    exe=ROOT/'.analysis/toolchain/wineprefix/drive_c/TASM50/bin/TASM32.EXE'
    env=dict(os.environ,WINEPREFIX=str(ROOT/'.analysis/toolchain/wineprefix'),
             WINEDEBUG='-all',DISPLAY='',WAYLAND_DISPLAY='',TZ='UTC',
             LANG='C',LC_ALL='C')
    rounds=[];results=[];objs=[]
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for n in (1,2):
            dest=WORK/f'round{n}'
            dest.mkdir(exist_ok=True)
            (dest/SOURCE.name).write_bytes(SOURCE.read_bytes())
            proc=subprocess.run(['/usr/bin/wine-stable',str(exe),'/m','/mx',
                 '/kh32768','/t',SOURCE.name,'prefix.obj'],cwd=dest,env=env,
                 stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT,timeout=90)
            (dest/'tasm.log').write_bytes(proc.stdout)
            assert proc.returncode==0,proc.stdout.decode(errors='replace')[-2000:]
            blob=(dest/'prefix.obj').read_bytes()
            result=check(original,blob)
            results.append(result);objs.append(blob)
            rounds.append(dict(round=n,object_path=str((dest/'prefix.obj').relative_to(ROOT)),
                               object_sha256=sha(blob),
                               log_path=str((dest/'tasm.log').relative_to(ROOT)),
                               log_sha256=sha(proc.stdout)))
    # A time-dependent compiler COMENT does not change semantic OMF bytes.
    aa=list(parse_omf(objs[0]));bb=list(parse_omf(objs[1]))
    assert len(aa)==len(bb)
    volatile=[]
    for i,(a,b) in enumerate(zip(aa,bb)):
        assert a.name==b.name
        if a.data!=b.data:
            assert a.name=='COMENT' and a.data[:2]==b.data[:2]==bytes.fromhex('40e9')
            assert a.data[3:]==b.data[3:] and len(a.data)==len(b.data)
            volatile.append(i)
    assert results[0]==results[1]
    result=dict(**results[0],native_TASM_rounds=2,
                native_nonvolatile_OMF_rounds_equal=True,
                native_COMENT_clock_record_indices=volatile,rounds=rounds)
    REPORT.write_text(json.dumps(result,indent=2)+'\n')
    return result
if __name__=='__main__':
    p=verify()
    print('isteldbl scoped 460-byte original prefix:',p['original_equal_prefix_CODE_bytes'],
          'exact, unresolved near target operand',p['original_unresolved_jump_operand_sites'],
          'original fixups',p['original_prefix_fixups'])
