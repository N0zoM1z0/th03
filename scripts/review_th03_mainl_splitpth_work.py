#!/usr/bin/env python3
"""Original 850-byte splitpth CODE (including 44-byte lookup tables) and 47-source link."""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_splitpth_work as p
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REVIEW='.analysis/work/mainl-splitpth-native-review.json'


def CODE(blob):
    obj=payload(blob)
    return bytes(obj[1,i] for i in range(850))


def review():
    raw=(ROOT/p.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,parents,parentsha=p.retained()
    original=p.ORIGINAL.read_bytes()
    goal=p.original_scope(original)
    old=CODE(original)
    src=(ROOT/p.SOURCE).read_bytes()
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['prior_fopen_OMF_order_open'] and r['prior_fclose_MKNAME_frame_open'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_forty_six_source_build_sha256']==parentsha and
         r['original_sha256']==sha(original) and
         r['source_sha256']==sha(src) and
         r['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         r['native_assembler_flags']==p.TASM_FLAGS,
         'current 850-byte real path splitter source and unchanged46-source CRT')
    need(goal['CODE_bytes']==850 and
         goal['pubs']==p.PUBLICS and goal['imports']==p.EXTERNS and
         goal['group']=='08ff02ff03' and
         len(goal['ordered_fixups'])==20 and
         [f['site'] for f in goal['ordered_fixups']]==p.FIXUP_SITES and
         goal['true_CODE_data_tables_bytes']==44,
         'genuine two public path functions,4 imports and20 ordered OMF fields')
    sections=[(0,92),(92,214),(230,776),(804,850)]
    decoder=Cs(CS_ARCH_X86,CS_MODE_16)
    need([sum(ins.size for ins in decoder.disasm(old[a:b],a)) for a,b in sections]==
         [92,122,546,46],
         'all real executable instructions in four original semantic CODE regions')
    table1=[int.from_bytes(old[i:i+2],'little') for i in range(214,230,2)]
    table2=[int.from_bytes(old[i:i+2],'little') for i in range(776,804,2)]
    need(table1==[0,47,58,92,199,199,189,199] and
         table2==[0,42,46,47,58,63,92,529,714,439,583,514,714,583],
         'real original immutable path punctuation and 4+7 symbolic jump table words')
    native_offsets=goal['ordered_fixups']
    need(all(f['target_method']==0 and f['target']==1 and
             f['frame_method']==5 for f in native_offsets[:7]+native_offsets[11:15]) and
         src.count(b'dw offset')==11,
         'eleven actual relative CODE segment switch-table relocations, not opcode bytes')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two actual complete source-native build rounds')
    phases=['extract']+[f'round{i}-{stage}' for i in (1,2) for stage in
                        ('assemble','library','link')]
    need([x['label'] for x in r['phases']]==phases and
         all(x['returncode']==0 and sha((ROOT/x['log_path']).read_bytes())==
             x['log_sha256'] for x in r['phases']),
         'complete original TASM/TLIB/TLINK writer command logs')
    vectors=[]
    for i,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'all complete original source OMF/library/EXE/MAP files')
        output={}
        for kind,meta in row['outputs'].items():
            blob=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                 'complete original source '+kind+' byte identity')
            output[kind]=blob
        need(p.original_scope(output['obj'])==goal and
             CODE(output['obj'])==old and
             literal_fields(output['obj'])==literal_fields(original),
             'all850 CODE bytes including real tables and all20 ordered original OMF fields exact')
        owners=dict(parents[i],splitpth=output['obj'])
        cmp=compare_members(members,library_members(output['lib']),owners)
        need(cmp==row['library_comparison'] and
             cmp['replaced_members']==sorted(owners) and
             cmp['contextual_members_unchanged']==846,
             '47 original source CRT slots, all846 other vendor program records byte-identical')
        need(output['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             output['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'entire fixed Japanese decoded MAINL image and MAP byte-for-byte')
        mz=parse_mz(output['exe'])
        need(mz.valid and len(output['exe'])==67372 and len(mz.relocations)==677,
             'complete original Japanese MZ and677 native relocations')
        vectors.append(output)
    need(vectors[0]==vectors[1],
         'two entire deterministic native original OBJ/LIB/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                original_splitpth_CODE_bytes=850,native_CODE_bytes=850,
                entire_native_CODE_raw_equal=True,
                original_executable_instruction_region_sizes=[92,122,546,46],
                original_source_CODE_tables_bytes=44,
                original_table_switch_relocation_words=11,
                real_first_token_table=table1,real_second_token_table=table2,
                original_far_public_offsets=[230,804],
                original_import_names=p.EXTERNS,
                original_literal_OMF_fields=20,all_native_ordered_fixups_equal=True,
                original_library_members=893,simultaneous_source_modules=47,
                unchanged_vendor_program_records=846,
                joint_exact_original_source_CODE_bytes=24627,
                complete_Japanese_EXE_raw_equal=True,complete_original_MAP_equal=True,
                original_EXE_bytes=67372,original_MZ_relocations=677,
                native_repeated_rounds=2,
                inherited_fopen_OMF_gap_open=True,inherited_fclose_frame_gap_open=True,
                source_path=p.SOURCE,source_sha256=sha(src),
                original_build_receipt_sha256=sha(raw),
                parent_46_source_receipt_sha256=parentsha,
                published_ledger_unchanged=True)


if __name__=='__main__':
    r=review()
    (ROOT/REVIEW).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
