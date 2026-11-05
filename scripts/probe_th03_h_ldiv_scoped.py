#!/usr/bin/env python3
"""Source-only original proof for the twelve-API 16-bit long-divide core.

Full TASM-produced CODE/public ABI equals Japanese CL.LIB. A targeted
linked comparison found an EXE-exact output but two MAP alias-order
swaps; no complete source member or Factory accepted credit is claimed.
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
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'src/mainl/crt/h_ldiv.asm'
WORK=ROOT/'.analysis/work/probe/h_ldiv-scoped'
REPORT=ROOT/'.analysis/work/probe/h_ldiv-scoped-review.json'
PUBLICS=[(0,'N_LDIV@'),(3,'F_LDIV@'),(3,'LDIV@'),
         (7,'N_LUDIV@'),(10,'F_LUDIV@'),(10,'LUDIV@'),
         (15,'N_LMOD@'),(18,'F_LMOD@'),(18,'LMOD@'),
         (23,'N_LUMOD@'),(26,'F_LUMOD@'),(26,'LUMOD@')]
def sha(blob):return sha256(blob).hexdigest()
def proof(original,native):
    old=payload(original);new=payload(native)
    assert {i for s,i in old if s==1}==set(range(174))
    assert {i for s,i in new if s==1}==set(range(174))
    assert all(old[1,i]==new[1,i] for i in range(174))
    for raw in (original,native):
        assert code_publics(raw,1)==PUBLICS
        assert externs(raw)==[]
        assert literal_fields(raw)==[]
        assert [(s['name'],s['class'],s['size']) for s in segment_definitions(raw)]==[
            ('_TEXT','CODE',174),('_DATA','DATA',0)]
        assert [r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF']==['06ff02']
        assert all(s==1 for s,i in payload(raw))
    return dict(
       original_MEMBER_CODE_bytes=174,exact_original_CODE_bytes=174,
       original_publics=PUBLICS,original_OMF_FIXUPP_count=0,
       complete_segment_and_logical_OMF_match=True,
       original_raw_OBJ_identity=False,
       complete_original_native_MAP_equal=False,
       complete_original_source_link_acceptance=False,
       source_linked_CRT_members_added=0,
       formal_Factory_source_credit=False,
       native_source_sha256=sha(SOURCE.read_bytes()))

def check_link_diagnostic():
    # Optional retained local diagnostic; do not run a full native link here.
    from build_th03_mainl_after502_work import WORK as w
    obj=w/'probe/h_ldiv-link-debug.exe'
    mp=w/'probe/h_ldiv-link-debug.map'
    if not obj.exists() or not mp.exists():
        return dict(retained_target_link_diagnostic=False)
    original_exe=(w/'bin/th03/mainl.target.exe').read_bytes()
    linked=obj.read_bytes()
    assert linked==original_exe
    assert len(parse_mz(linked).relocations)==677
    original_map=(w/'obj/th03/mainl.map').read_bytes().splitlines()
    linked_map=mp.read_bytes().splitlines()
    assert len(original_map)==len(linked_map)
    diffs=[i for i,(a,b) in enumerate(zip(original_map,linked_map)) if a!=b]
    assert diffs==[1321,1322,1330,1331],diffs
    assert (original_map[1321],original_map[1322])==(
        linked_map[1322],linked_map[1321])
    assert (original_map[1330],original_map[1331])==(
        linked_map[1331],linked_map[1330])
    return dict(retained_target_link_diagnostic=True,
        actual_linked_EXE_original_equal=True,
        actual_linked_MZ_relocations=677,
        actual_linked_MAP_original_equal=False,
        different_MAP_line_indices=diffs,
        alias_tie_groups=[
            ['LDIV@','F_LDIV@'],['F_LUMOD@','LUMOD@']])

def verify():
    lib=library_members((ROOT/'.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes())
    original=b'\x80\x02\x00\x00\x7e'+next(m.program_records for m in lib if m.name=='h_ldiv')
    source=SOURCE.read_bytes()
    prefix=ROOT/'.analysis/toolchain/wineprefix'
    exe=prefix/'drive_c/TASM50/bin/TASM32.EXE'
    env=dict(os.environ,WINEPREFIX=str(prefix),WINEDEBUG='-all',
             DISPLAY='',WAYLAND_DISPLAY='',TZ='UTC',LANG='C',LC_ALL='C')
    WORK.mkdir(parents=True,exist_ok=True)
    outputs=[]
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for n in (1,2):
            directory=WORK/f'round{n}'
            directory.mkdir(exist_ok=True)
            (directory/SOURCE.name).write_bytes(source)
            proc=subprocess.run(['/usr/bin/wine-stable',str(exe),'/m','/mx',
                  '/kh32768','/t',SOURCE.name,'h_ldiv.obj'],
                  cwd=directory,env=env,stdin=subprocess.DEVNULL,
                  stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
            (directory/'tasm.log').write_bytes(proc.stdout)
            assert proc.returncode==0,proc.stdout.decode(errors='replace')[-1500:]
            raw=(directory/'h_ldiv.obj').read_bytes()
            result=proof(original,raw)
            outputs.append(dict(round=n,obj_sha256=sha(raw),
                        log_sha256=sha(proc.stdout),obj_bytes=len(raw),
                        relative_obj=str((directory/'h_ldiv.obj').relative_to(ROOT)),
                        relative_log=str((directory/'tasm.log').relative_to(ROOT))))
    first=(WORK/'round1/h_ldiv.obj').read_bytes()
    second=(WORK/'round2/h_ldiv.obj').read_bytes()
    fa=list(parse_omf(first));fb=list(parse_omf(second))
    assert len(fa)==len(fb)
    variable=[]
    for i,(a,b) in enumerate(zip(fa,fb)):
        assert a.name==b.name
        if a.data==b.data:continue
        assert a.name=='COMENT' and a.data[:2]==b.data[:2]==bytes.fromhex('40e9')
        assert len(a.data)==len(b.data) and a.data[3:]==b.data[3:]
        variable.append(i)
    assert len(variable)<=1
    out=dict(**result,**check_link_diagnostic(),
             native_TASM_rounds=2,
             nonvolatile_native_OMF_rounds_equal=True,
             changed_TASM_COMENT_record_indices=variable,
             original_raw_round_sha_equal=sha(first)==sha(second),
             rounds=outputs)
    REPORT.write_text(json.dumps(out,indent=2)+'\n')
    return out

if __name__=='__main__':
    r=verify()
    print('h_ldiv scoped: twelve APIs, CODE original-exact',
          r['exact_original_CODE_bytes'],'MAP original-equal?',
          r['complete_original_native_MAP_equal'],
          'source-linked member credit',r['source_linked_CRT_members_added'])
