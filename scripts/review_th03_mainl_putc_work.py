#!/usr/bin/env python3
"""Whole original 974-byte DOS putc CODE/1 DATA/1 BSS and 46-source MAINL."""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_putc_work as p
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-putc-native-review.json'


def parts(raw):
    obj=payload(raw)
    return bytes(obj[1,i] for i in range(974)),bytes([obj[2,0]])


def review():
    receipt_raw=(ROOT/p.REPORT).read_bytes()
    r=json.loads(receipt_raw)
    base,files,accepted,members,prior,parentsha=p.retained()
    original=p.ORIGINAL.read_bytes()
    goal=p.original_scope(original)
    code,data=parts(original)
    source=(ROOT/p.SOURCE).read_bytes()
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['prior_fopen_OMF_order_open'] and
         r['prior_fclose_MKNAME_frame_open'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_forty_five_source_build_sha256']==parentsha and
         r['original_sha256']==sha(original) and
         r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         r['native_assembler_flags']==p.TASM_FLAGS,
         'genuine original putc object and complete retained45-source CRT')
    need(goal['CODE_bytes']==974 and goal['DATA_bytes']==1 and
         goal['BSS_bytes']==1 and data==bytes([13]) and
         goal['publics']==p.PUBLICS and goal['externs']==p.EXTERNS and
         [f['site'] for f in goal['ordered_fields']]==p.FIXUP_SITES and
         len(goal['ordered_fields'])==29 and
         goal['original_group']=='08ff02ff03',
         'all original public, import, storage, geometry and29 ordered fixups')
    fixup=goal['ordered_fields'][-1]
    need(fixup['site']==21 and fixup['frame_method']==5 and
         fixup['target_method']==0 and fixup['target']==1 and
         fixup['addend']==32 and
         b'assume cs:NOTHING' in source.lower().replace(b'nothing',b'NOTHING') and
         b'call far ptr _fputc' in source,
         'true original internal far CALL and TASM no-same-CS optimization state')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16)
    sections=((0,32),(32,427),(427,451),(451,974))
    need([sum(x.size for x in decoder.disasm(code[a:b],a)) for a,b in sections]==
         [32,395,24,523],
         'complete four real original DOS character and many-byte output routines')
    need(len(r['rounds'])==2 and [row['round'] for row in r['rounds']]==[1,2],
         'two independent real source writer rounds')
    phase_labels=['extract']+[f'round{i}-{stage}' for i in (1,2)
                              for stage in ('assemble','library','link')]
    need([q['label'] for q in r['phases']]==phase_labels and
         all(q['returncode']==0 and sha((ROOT/q['log_path']).read_bytes())==
             q['log_sha256'] for q in r['phases']),
         'real TASM/TLIB/TLINK writer logs and current command sequences')
    vectors=[]
    for i,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'complete native OBJ/LIB/EXE/MAP output vector')
        outputs={}
        for kind,q in row['outputs'].items():
            raw=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(raw),sha256=sha(raw)),
                 'original complete source '+kind+' raw output identity')
            outputs[kind]=raw
        need(p.original_scope(outputs['obj'])==goal and
             parts(outputs['obj'])==(code,data) and
             literal_fields(outputs['obj'])==literal_fields(original),
             'complete original putc source CODE+DATA+BSS and29 literal ordered OMF fields')
        source_owners=dict(prior[i],putc=outputs['obj'])
        comp=compare_members(members,library_members(outputs['lib']),source_owners)
        need(comp==row['library_comparison'] and
             comp['replaced_members']==sorted(source_owners) and
             comp['contextual_members_unchanged']==847,
             '46 original CRT source members with 847 entire vendor member records untouched')
        need(outputs['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'entire original Japanese decoded MAINL and native MAP byte-for-byte')
        mz=parse_mz(outputs['exe'])
        need(mz.valid and len(outputs['exe'])==67372 and len(mz.relocations)==677,
             'whole 67372-byte DOS image and original677 MZ relocations')
        vectors.append(outputs)
    need(vectors[0]==vectors[1],
         'two deterministic real native source OBJ/LIB/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,
                original_putc_CODE_bytes=974,native_CODE_bytes=974,
                exact_literal_CODE_equal=True,
                original_DATA_bytes=1,native_DATA_bytes=1,
                original_BSS_bytes=1,native_BSS_bytes=1,
                initialized_DATA_raw_equal=True,
                original_public_function_sizes=[32,395,24,523],
                original_pubdefs=p.PUBLICS,original_extdefs=p.EXTERNS,
                original_literal_FIXUPPs=29,all29_ordered_fields_equal=True,
                original_internal_far_call_frame_method=5,
                restored_TARGET_frame_at_CODE_21=True,
                original_library_members=893,source_modules=46,
                unchanged_vendor_member_programs=847,
                cumulative_exact_source_CODE_bytes=23777,
                whole_original_EXE_raw_equal=True,whole_original_MAP_equal=True,
                original_Japanese_EXE_bytes=67372,original_MZ_relocations=677,
                repeated_native_rounds=2,
                previous_fopen_OMF_gap_open=True,previous_fclose_near_frame_gap_open=True,
                original_source=p.SOURCE,source_sha256=sha(source),
                bound_build_receipt_sha256=sha(receipt_raw),
                prior_45_source_receipt_sha256=parentsha,
                formal_accepted_ledger_unchanged=True)


if __name__=='__main__':
    rec=review()
    (ROOT/REPORT).write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec,indent=2))
