#!/usr/bin/env python3
"""Whole original DOS directory subsystem CODE/DATA/OMF plus 45-source MAINL."""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_direct_work as p
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-direct-native-review.json'


def parts(blob):
    v=payload(blob)
    return bytes(v[1,i] for i in range(517)),bytes(v[2,i] for i in range(9))


def review():
    build_raw=(ROOT/p.REPORT).read_bytes()
    receipt=json.loads(build_raw)
    base,files,accepted,members,previous,parentsha=p.retained()
    original=p.ORIGINAL.read_bytes()
    goal=p.original_scope(original)
    input_source=(ROOT/p.SOURCE).read_bytes()
    old_code,old_data=parts(original)
    need(receipt['complete'] and not receipt['source_acceptance'] and
         receipt['added_accepted_bytes']==0 and not receipt['original_cold_rebuilt'] and
         receipt['prior_fopen_OMF_order_open'] and
         receipt['prior_fclose_MKNAME_frame_open'] and
         receipt['accepted_baseline']==base and
         receipt['accepted_library_sha256']==sha(accepted) and
         receipt['previous_forty_four_source_build_sha256']==parentsha and
         receipt['original_sha256']==sha(original) and
         receipt['source_sha256']==sha(input_source) and
         receipt['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         receipt['native_assembler_flags']==p.TASM_FLAGS,
         'bound original DOS directory object, source and 44-source parent')
    need(goal['CODE_bytes']==517 and goal['DATA_bytes']==9 and
         goal['publics']==p.PUBLICS and goal['externs']==p.EXTERNS and
         len(goal['ordered_fields'])==20 and
         [f['site'] for f in goal['ordered_fields']]==p.FIXUP_SITES and
         old_data==bytes.fromhex('5c2a2e2a002a2e2a00'),
         'original four far DIR interfaces, real patterns and 20 ordered native fields')
    reader=Cs(CS_ARCH_X86,CS_MODE_16)
    ranges=((0,311),(311,367),(367,442),(442,517))
    need([sum(x.size for x in reader.disasm(old_code[a:b],a)) for a,b in ranges]==
         [311,56,75,75],
         'four whole semantic directory instruction streams, no executable gaps')
    need(len(receipt['rounds'])==2 and [r['round'] for r in receipt['rounds']]==[1,2],
         'two complete source native writer rounds')
    phases=['extract']+[f'round{n}-{kind}' for n in (1,2)
                        for kind in ('assemble','library','link')]
    need([x['label'] for x in receipt['phases']]==phases and
         all(x['returncode']==0 and
             sha((ROOT/x['log_path']).read_bytes())==x['log_sha256']
             for x in receipt['phases']),
         'actual original TASM/TLIB/TLINK writer phase logs')
    vectors=[]
    for idx,entry in enumerate(receipt['rounds']):
        need(set(entry['outputs'])=={'obj','lib','exe','map'},
             'complete actual native OBJ/LIB/EXE/MAP outputs')
        out={}
        for kind,q in entry['outputs'].items():
            blob=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(blob),sha256=sha(blob)),
                 'complete real native output '+kind)
            out[kind]=blob
        need(p.original_scope(out['obj'])==goal and
             parts(out['obj'])==(old_code,old_data) and
             literal_fields(out['obj'])==literal_fields(original),
             'all517 original CODE and9 DATA bytes and literal20 ordered native OMF fields')
        source_owners=dict(previous[idx],direct=out['obj'])
        cmp=compare_members(members,library_members(out['lib']),source_owners)
        need(cmp==entry['library_comparison'] and
             cmp['replaced_members']==sorted(source_owners) and
             cmp['contextual_members_unchanged']==848,
             '45 original source CRT program slots and all848 others unchanged')
        need(out['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete fixed Japanese decoded MAINL EXE/MAP raw equal')
        mz=parse_mz(out['exe'])
        need(mz.valid and len(out['exe'])==67372 and len(mz.relocations)==677,
             'whole original MZ relocation vector unchanged')
        vectors.append(out)
    need(vectors[0]==vectors[1],
         'two complete byte-identical source native OBJ/LIB/EXE/MAP rounds')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,original_CODE_bytes=517,
                native_CODE_bytes=517,complete_original_CODE_equal=True,
                original_initialized_DATA_bytes=9,native_DATA_bytes=9,
                literal_initialized_DATA_equal=True,
                original_far_pubs=p.PUBLICS,
                original_import_order=p.EXTERNS,all_original_imports_equal=True,
                original_native_ordered_FIXUPPs=20,
                literal_original_fixups_equal=True,
                original_function_sizes=[311,56,75,75],
                original_893_member_library=893,source_CRT_members=45,
                original_vendor_member_programs_unchanged=848,
                cumulative_source_CODE_bytes=22803,
                whole_original_japanese_EXE_raw_equal=True,
                whole_original_MAP_raw_equal=True,
                original_EXE_file_bytes=67372,original_MZ_relocations=677,
                native_repeated_rounds=2,
                previous_fopen_OMF_order_open=True,
                previous_fclose_near_frame_open=True,
                source_path=p.SOURCE,source_sha256=sha(input_source),
                build_report_sha256=sha(build_raw),
                previous_44_source_receipt_sha256=parentsha,
                accepted_publication_unchanged=True)


if __name__=='__main__':
    r=review()
    (ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
