#!/usr/bin/env python3
"""Full DOS strftime CODE/real DATA/switch words and 52-source Japanese MAINL.

The exact CODE/segment/data/whole linked EXE and logical original ordered
OMF fields do not imply complete original OMF metadata. Four near __UTOA
external calls have historical TARGET frame5 vs TASM CODE frame0.
"""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_strftime_work as p
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-strftime-native-review.json'


def review():
    raw=(ROOT/p.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,parents,parenthash=p.retained()
    original=p.ORIGINAL.read_bytes()
    expected=p.original_scope(original)
    source=(ROOT/p.SOURCE).read_bytes()
    origcode,origdata=p.native_parts(original)
    originals=literal_fields(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['native_strftime_near_UTOA_TARGET_frame_open'] and
         r['prior_timecvt_near_frame_open'] and
         r['prior_fopen_OMF_order_open'] and r['prior_fclose_near_frame_open'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_fifty_one_source_build_sha256']==parenthash and
         r['original_sha256']==sha(original) and
         r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         r['native_assembler_flags']==p.TASM_FLAGS,
         'current strftime source, BCC original and unchanged51-source native CRT')
    need(expected['CODE_bytes']==1256 and expected['DATA_bytes']==18 and
         expected['public']==[(0,'_strftime')] and
         expected['imports']==p.EXTERNS and len(originals)==66 and
         [f['site'] for f in originals]==p.FIXUP_SITES and
         origdata==p.DATA,'literal original CODE/DATA/EXTDEF and BCC66 OMF fields')
    ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(origcode[:1168],0))
    need(len(ins)==448 and sum(x.size for x in ins)==1168,
         'all original 448 8086 instructions end at actual format/switch WORD tables')
    format_chars=[int.from_bytes(origcode[i:i+2],'little')
                  for i in range(1168,1212,2)]
    switches=[int.from_bytes(origcode[i:i+2],'little')
              for i in range(1212,1256,2)]
    all_addr={x.address for x in ins}
    need(format_chars==p.FORMAT_CHARS and switches==p.SWITCH_TO and
         len(format_chars)==len(switches)==22 and
         all(site in all_addr for site in switches) and
         source.count(b'dw offset ')==22,
         'all22 real original CODE character classes and symbolic 22-branch switch words')
    need(originals==originals[:40]+originals[40:62]+originals[62:] and
         [f['site'] for f in originals[40:62]]==p.TABLE_SITES and
         [f['site'] for f in originals[62:]]==p.TAIL_SITES and
         [f['site'] for f in originals[:40]]==p.BODY_SITES and
         all(f['frame_method']==5 for f in originals
             if f['site'] in p.NEAR_FRAMES) and len(p.NEAR_FRAMES)==4,
         'original BCC body/table/tail FIXUPP order and four near TARGET-frame imports')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two complete native source writer rounds')
    stages=['extract']+[f'round{i}-{v}' for i in (1,2)
                        for v in ('assemble','library','link')]
    need([q['label'] for q in r['phases']]==stages and
         all(q['returncode']==0 and
             sha((ROOT/q['log_path']).read_bytes())==q['log_sha256']
             for q in r['phases']),
         'original Borland TASM/TLIB/TLINK actual commands/log file hashes')
    vectors=[]
    for idx,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'whole native original source OBJ/LIB/EXE/MAP vectors')
        output={}
        for kind,q in row['outputs'].items():
            blob=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(blob),sha256=sha(blob)),
                 'complete real native '+kind+' output')
            output[kind]=blob
        generated=p.native_parts(output['obj'])
        fix=literal_fields(output['obj'])
        need(p.original_scope(output['obj'])==expected and
             generated==(origcode,origdata) and
             len(fix)==66 and
             [f['site'] for f in fix]==p.FIXUP_SITES and
             sum(a!=b for a,b in zip(originals,fix))==4 and
             all(a==b for a,b in zip(originals,fix)
                 if a['site'] not in p.NEAR_FRAMES) and
             all(a['frame_method']==5 and b['frame_method']==0 and
                 a['target_method']==b['target_method']==2 and
                 a['target']==b['target']==1 and a['site']==b['site']
                 for a,b in zip(originals,fix) if a['site'] in p.NEAR_FRAMES),
             'all1256 CODE,18 DATA and66 ordered original OMF fields, only four known frames')
        owners=dict(parents[idx],strftime=output['obj'])
        compared=compare_members(members,library_members(output['lib']),owners)
        need(compared==row['library_comparison'] and
             compared['replaced_members']==sorted(owners) and
             compared['contextual_members_unchanged']==841,
             '52 real CRT source owner positions and841 entirely untouched member programs')
        need(output['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             output['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete original Japanese decoded EXE/MAP byte-for-byte')
        mz=parse_mz(output['exe'])
        need(mz.valid and len(output['exe'])==67372 and len(mz.relocations)==677,
             'entire original DOS Japanese MZ relocation-bearing linked image')
        vectors.append(output)
    need(vectors[0]==vectors[1],
         'two complete identical original native OBJ/LIB/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                original_strftime_CODE_bytes=1256,source_CODE_bytes=1256,
                original_initialized_DATA_bytes=18,source_DATA_bytes=18,
                complete_native_CODE_equal=True,complete_initialized_DATA_equal=True,
                real_executable_instruction_bytes=1168,original_instruction_count=448,
                original_CODE_data_table_bytes=88,original_format_class_words=22,
                original_switch_offset_words=22,
                literal_ordered_original_OMF_fields=66,
                literal_ordered_sites_equal=True,
                logical_native_fixups_equal=True,
                native_original_OMF_equal=False,
                original_UTOA_TARGET_frame_sites=[879,811,774,723],
                original_near_call_frame_method=5,source_near_call_frame_method=0,
                literal_other_62_fields_equal=True,
                original_CRT_program_count=893,simultaneous_source_modules=52,
                unchanged_original_member_programs=841,
                cumulative_source_CODE_bytes=26971,
                entire_original_Japanese_EXE_equal=True,entire_original_MAP_equal=True,
                original_MZ_relocations=677,original_EXE_bytes=67372,
                repeated_native_rounds=2,
                previous_timecvt_OMF_near_gap_open=True,
                previous_fopen_OMF_order_gap_open=True,
                previous_fclose_near_frame_gap_open=True,
                source_path=p.SOURCE,source_sha256=sha(source),
                bound_native_build_receipt_sha256=sha(raw),
                parent_51_source_receipt_sha256=parenthash,
                original_formal_accepted_publication_unchanged=True)


if __name__=='__main__':
    q=review()
    (ROOT/REPORT).write_text(json.dumps(q,indent=2)+'\n')
    print(json.dumps(q,indent=2))
