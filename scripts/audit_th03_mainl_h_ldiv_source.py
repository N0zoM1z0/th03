#!/usr/bin/env python3
"""Scoped ORIGINAL Japanese CL.LIB long-div source audit; no cold replay.

This is a separate, *not counted as full source* experiment. The source
assembles to all original division/modulo CODE and PUBDEF aliases, while a
prior native carrier experiment found two same-address MAP alias order gaps.
Do not promote this member to the accepted or 408-source working carrier.
"""
import fcntl
import json
import os
import subprocess
import tomllib
from pathlib import Path

import build_th03_mainl_after356_work as parent
from build_th03_mainl_display_work import payload, literal_fields
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import object_program_records
from review_th03_mainl_after356_work import review as review_parent
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

ROOT=Path(__file__).resolve().parents[1]
WORK=parent.WORK
SOURCE=ROOT/'src/mainl/crt/h_ldiv.asm'
OUTPUT=ROOT/'.analysis/work/h_ldiv-original-source-scope.json'
PUBLICS=[(0,'N_LDIV@'),(3,'F_LDIV@'),(3,'LDIV@'),
         (7,'N_LUDIV@'),(10,'F_LUDIV@'),(10,'LUDIV@'),
         (15,'N_LMOD@'),(18,'F_LMOD@'),(18,'LMOD@'),
         (23,'N_LUMOD@'),(26,'F_LUMOD@'),(26,'LUMOD@')]


def audit():
    base,files,accepted,members,carry,_=parent.retained()
    current=review_parent('string-hash-static-boss')
    # retained() is deliberately the *inherited* 407-member carrier; the
    # scoped reviewer adds and verifies the real 408th source from raw rounds.
    need(len(carry[0][0])==407 and len(carry[1][0])==407 and
         current['native_source_members']==408 and
         current['complete_native_link_EXE_MAP_equal'] and
         'h_ldiv' not in carry[0][0] and members[67].name=='h_ldiv',
         'unchanged full reviewed 408-member parent and original CRT member 67')
    parent_sha=sha((ROOT/(parent.PREFIX+'string-hash-static-boss-build.json')).read_bytes())
    original=parent.original_library_member(members[67])
    need(object_program_records(original)==members[67].program_records,
         'original pinned Japanese CL.LIB OMF program')
    config=tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix=ROOT/config['paths']['wine_prefix']
    scratch=WORK/'probe/h_ldiv-scoped-code-audit'
    scratch.mkdir(parents=True,exist_ok=True)
    source=SOURCE.read_bytes()
    (scratch/'h_ldiv.asm').write_bytes(source)
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',
             WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',
             TZ='UTC',LANG='C',LC_ALL='C')
    flags=['/m','/mx','/kh32768','/t']
    command=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),
             *flags,'h_ldiv.asm','h_ldiv.obj']
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lk:
        fcntl.flock(lk,fcntl.LOCK_EX)
        result=subprocess.run(command,cwd=scratch,env=env,stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,timeout=120,check=False)
    need(result.returncode==0,'actual TASM 5.0 original 16-bit source assembly')
    created=(scratch/'h_ldiv.obj').read_bytes()
    need(SOURCE.read_bytes()==source,'source stable during assembler run')
    need(segment_definitions(original)==segment_definitions(created) and
         [(q['name'],q['class'],q['size']) for q in segment_definitions(created)]==
         [('_TEXT','CODE',174),('_DATA','DATA',0)] and
         code_publics(created,1)==PUBLICS==code_publics(original,1) and
         code_publics(created,2)==[] and
         externs(created)==externs(original)==[] and
         literal_fields(created)==literal_fields(original)==[] and
         [r.data.hex() for r in parse_omf(created) if r.name=='GRPDEF']==
         [r.data.hex() for r in parse_omf(original) if r.name=='GRPDEF']==
         ['06ff02'] and payload(created)==payload(original),
         'all original CODE bytes, aliases, segments, group and zero FIXUPPs')
    need(object_program_records(created)!=members[67].program_records,
         'no claim of original Borland PUBDEF or whole OMF serialization')
    # Full MAP alias order remains unaccepted; source must not be inserted
    # into the 408-member carrier until exact Japanese EXE *and MAP* agree.
    return dict(status='original-code-only-not-native-MAP-accepted',
        source_counted=False,original_CRT_index=67,
        original_CODE_bytes=174,original_public_aliases=len(PUBLICS),
        original_FIXUPP_count=0,original_source_CODE_equal=True,
        original_publics_equal=True,original_segment_group_equal=True,
        original_library_member_program_equal=False,
        native_full_MAP_equality_not_claimed=True,
        known_MAP_alias_order_gaps=[['LDIV@','F_LDIV@'],
                                    ['F_LUMOD@','LUMOD@']],
        original_member_program_sha256=sha(members[67].program_records),
        original_CODE_sha256=sha(bytes(payload(original)[1,i] for i in range(174))),
        source_path='src/mainl/crt/h_ldiv.asm',source_sha256=sha(source),
        source_OBJ_sha256=sha(created),toolchain_sha256=sha(
            (ROOT/'config/toolchain.toml').read_bytes()),
        parent_receipt_sha256=parent_sha,assembler_flags=flags,
        original_fully_linked_source_members_remain=408,
        original_cold_rebuilt=False,source_acceptance=False)


if __name__=='__main__':
    result=audit()
    OUTPUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
