#!/usr/bin/env python3
"""Independently verify complete DOS open original OMF and 40-source MAINL."""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_open_work as p
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REVIEW='.analysis/work/mainl-open-native-review.json'


def native_CODE(blob):
    obj=payload(blob)
    return bytes(obj[1,i] for i in range(459))


def review():
    raw=(ROOT/p.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,old,parenthash=p.retained()
    original=p.ORIGINAL.read_bytes()
    goal=p.original_scope(original)
    original_code=native_CODE(original)
    source=(ROOT/p.SOURCE).read_bytes()
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['prior_fopen_OMF_order_open'] and r['prior_fclose_MKNAME_frame_open'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_thirty_nine_source_build_sha256']==parenthash and
         r['original_sha256']==sha(original) and r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         r['native_assembler_flags']==p.TASM_FLAGS,
         'original source, pinned CRT and unchanged39-member native parent')
    need(goal['CODE_bytes']==459 and goal['public_offset']==53 and
         goal['imports']==p.EXTERNS and
         [f['site'] for f in goal['literal_fields']]==p.FIXUP_SITES and
         goal['original_group']=='08ff03ff02',
         'whole 459-byte open original including 20 ordered native OMF fields')
    original_fields=goal['literal_fields']
    need([sum(ins.size for ins in Cs(CS_ARCH_X86,CS_MODE_16).disasm(
        original_code[a:b],a)) for a,b in ((0,31),(31,53),(53,459))]==[31,22,406],
         'actual near DOS Create/truncate and large far _open function boundaries')
    need([(f['site'],f['frame_method'],f['target_method']) for f in
          original_fields[15:19]]==
         [(392,1,2),(394,5,2),(398,1,2),(400,5,2)],
         'original exit-hook paired relocation fields with distinct frames')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two complete independent original native writer runs')
    phases=['extract']+[f'round{i}-{n}' for i in (1,2)
                        for n in ('assemble','library','link')]
    need([q['label'] for q in r['phases']]==phases and
         all(q['returncode']==0 and
             sha((ROOT/q['log_path']).read_bytes())==q['log_sha256']
             for q in r['phases']),
         'actual TASM/TLIB/TLINK commands/logs in original order')
    raw_vectors=[]
    for i,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'full native original OBJ/LIB/EXE/MAP files')
        outputs={}
        for kind,q in row['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'complete original '+kind+' file identity')
            outputs[kind]=data
        need(p.original_scope(outputs['obj'])==goal and
             native_CODE(outputs['obj'])==original_code and
             literal_fields(outputs['obj'])==original_fields,
             'all459 native CODE bytes, original PUB/EXTDEF/GROUP and20 literal FIXUPPs')
        sources=dict(old[i],open=outputs['obj'])
        cmp=compare_members(members,library_members(outputs['lib']),sources)
        need(cmp==row['library_comparison'] and
             cmp['replaced_members']==sorted(sources) and
             cmp['contextual_members_unchanged']==853,
             '40 exact natural native source positions and853 unmodified vendor records')
        need(outputs['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'entire fixed Japanese MAINL decoded EXE/MAP bitwise identity')
        mz=parse_mz(outputs['exe'])
        need(mz.valid and len(outputs['exe'])==67372 and len(mz.relocations)==677,
             'all original MZ relocations and fixed Japanese EXE size')
        raw_vectors.append(outputs)
    need(raw_vectors[0]==raw_vectors[1],
         'two identical whole source object/library/executable/MAP output vectors')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,
                original_open_CODE_bytes=459,source_open_CODE_bytes=459,
                native_CODE_bytes_exact=True,original_private_dos_create_bytes=31,
                original_private_truncate_bytes=22,
                original_far_open_bytes=406,far_public_open_offset=53,
                original_import_order=p.EXTERNS,
                original_ordered_OMF_FIXUPPs=20,
                all_literal_native_fixups_equal=True,
                paired_exit_cleanup_fields_at=[392,394,398,400],
                original_CRT_member_count=893,source_module_count=40,
                original_untouched_member_programs=853,
                simultaneous_exact_original_source_CODE_bytes=22170,
                entire_Japanese_EXE_raw_equal=True,entire_original_MAP_equal=True,
                real_decoded_Japanese_EXE_bytes=67372,
                original_MZ_relocations=677,
                native_repeated_rounds=2,
                prior_fopen_OMF_order_gap=True,prior_fclose_frame_gap=True,
                source_path=p.SOURCE,original_obj_sha256=sha(original),
                build_report_sha256=sha(raw),
                previous_thirty_nine_source_receipt_sha256=parenthash,
                formal_accepted_ledger_unchanged=True)


if __name__=='__main__':
    x=review()
    (ROOT/REVIEW).write_text(json.dumps(x,indent=2)+'\n')
    print(json.dumps(x,indent=2))
