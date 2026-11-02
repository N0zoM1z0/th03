#!/usr/bin/env python3
"""Full DOS 820 CODE/12 DATA time converter and 48-source normal MAINL.

Native TASM emits all original bytes and original ordered logical relocations,
but 18 near-call original BCC TARGET frames are CODE-framed in TASM. This
real original OMF metadata difference must not be reported as exact OMF.
"""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
import build_th03_mainl_timecvt_work as p
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-timecvt-native-review.json'


def native_parts(blob):
    b=payload(blob)
    return bytes(b[1,i] for i in range(820)),bytes(b[2,i] for i in range(12))


def review():
    raw=(ROOT/p.REPORT).read_bytes()
    receipt=json.loads(raw)
    base,files,accepted,members,prior,parenthash=p.retained()
    orig=p.ORIGINAL.read_bytes()
    expected=p.original_scope(orig)
    code,DATA=native_parts(orig)
    src=(ROOT/p.SOURCE).read_bytes()
    original_fields=literal_fields(orig)
    need(receipt['complete'] and not receipt['source_acceptance'] and
         receipt['added_accepted_bytes']==0 and not receipt['original_cold_rebuilt'] and
         receipt['native_timecvt_near_TARGET_frame_open'] is True and
         receipt['prior_fopen_OMF_order_open'] is True and
         receipt['prior_fclose_MKNAME_frame_open'] is True and
         receipt['accepted_baseline']==base and
         receipt['accepted_library_sha256']==sha(accepted) and
         receipt['previous_forty_seven_source_build_sha256']==parenthash and
         receipt['original_sha256']==sha(orig) and
         receipt['source_sha256']==sha(src) and
         receipt['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         receipt['native_assembler_flags']==p.TASM_FLAGS,
         'current semantic month/time convert source, 47-original-source parent and OMF gap')
    need(expected['CODE_bytes']==820 and expected['DATA_bytes']==12 and
         expected['public']==p.PUBLICS and expected['imports']==p.EXTERNS and
         [f['site'] for f in original_fields]==p.FIXUP_SITES and
         expected['original_group']=='08ff02ff03' and len(original_fields)==29,
         'original two public time converters and actual 29 descending fields')
    dec=Cs(CS_ARCH_X86,CS_MODE_16)
    need([sum(i.size for i in dec.disasm(code[a:b],a))
          for a,b in ((0,301),(301,820))]==[301,519],
         'complete original DOS time and Unix time routine instruction coverage')
    need(DATA==bytes.fromhex('1f1c1f1e1f1e1f1f1e1f1e1f'),
         '12 real initialized non-leap-year month-length bytes')
    need(len(p.NEAR_FRAMES)==18 and
         all(f['frame_method']==5 for f in original_fields
             if f['site'] in p.NEAR_FRAMES) and
         len(receipt['rounds'])==2 and
         [r['round'] for r in receipt['rounds']]==[1,2],
         'precisely18 true original near import TARGET-framed original fields')
    expected_phases=['extract']+[f'round{i}-{kind}' for i in (1,2)
                                 for kind in ('assemble','library','link')]
    need([q['label'] for q in receipt['phases']]==expected_phases and
         all(q['returncode']==0 and sha((ROOT/q['log_path']).read_bytes())==
             q['log_sha256'] for q in receipt['phases']),
         'complete native TASM/TLIB/TLINK original writer command receipts')
    vectors=[]
    for index,row in enumerate(receipt['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'all four complete raw source outputs')
        out={}
        for kind,q in row['outputs'].items():
            blob=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(blob),sha256=sha(blob)),
                 'whole literal native '+kind+' output identity')
            out[kind]=blob
        need(p.original_scope(out['obj'])==expected and
             native_parts(out['obj'])==(code,DATA),
             'literal native all820 CODE bytes and12 original DATA bytes')
        native_fields=literal_fields(out['obj'])
        need(len(native_fields)==29 and
             [f['site'] for f in native_fields]==p.FIXUP_SITES and
             sum(a!=b for a,b in zip(original_fields,native_fields))==18 and
             all(a==b for a,b in zip(original_fields,native_fields)
                 if a['site'] not in p.NEAR_FRAMES) and
             all(a['frame_method']==5 and b['frame_method']==0 and
                 a['site']==b['site'] and a['target']==b['target'] and
                 a['target_method']==b['target_method']
                 for a,b in zip(original_fields,native_fields)
                 if a['site'] in p.NEAR_FRAMES),
             'all29 OMF fields original order,18 near TARGET/CODE frame discrepancies only')
        objs=dict(prior[index],_timecvt=out['obj'])
        cmp=compare_members(members,library_members(out['lib']),objs)
        need(cmp==row['library_comparison'] and
             cmp['replaced_members']==sorted(objs) and
             cmp['contextual_members_unchanged']==845,
             '48 source CRT members and all845 original vendor program records unchanged')
        need(out['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'full decoded Japanese MAINL and entire original MAP bit-for-bit')
        mz=parse_mz(out['exe'])
        need(mz.valid and len(out['exe'])==67372 and len(mz.relocations)==677,
             'all677 original DOS MZ relocation entries in entire Japanese executable')
        vectors.append(out)
    need(vectors[0]==vectors[1],'two complete identical source OBJ/LIB/EXE/MAP native pairs')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,
                original_CODE_bytes=820,source_CODE_bytes=820,
                original_initialized_DATA_bytes=12,source_DATA_bytes=12,
                complete_native_CODE_raw_equal=True,complete_native_DATA_raw_equal=True,
                original_function_sizes=[301,519],
                original_far_public_offsets=[0,301],
                original_import_names=p.EXTERNS,
                literal_native_ordered_FIXUPP_count=29,
                logical_ordered_FIXUPPs_equal=True,
                complete_original_OMF_equal=False,
                original_near_TARGET_to_source_CODE_frame_count=18,
                original_near_frame=5,source_near_frame=0,
                original_893_library_members=893,
                source_members_in_working_CRT=48,unchanged_original_member_programs=845,
                combined_exact_source_CODE_bytes=25447,
                whole_original_Japanese_EXE_raw_equal=True,
                whole_original_MAP_raw_equal=True,
                original_exe_bytes=67372,original_mz_relocations=677,
                repeated_native_rounds=2,
                prior_fopen_OMF_order_open=True,prior_fclose_near_frame_open=True,
                source_path=p.SOURCE,bound_build_receipt_sha256=sha(raw),
                parent_47_source_receipt_sha256=parenthash,
                formal_accepted_ledger_unchanged=True)


if __name__=='__main__':
    q=review()
    (ROOT/REPORT).write_text(json.dumps(q,indent=2)+'\n')
    print(json.dumps(q,indent=2))
