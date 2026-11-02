#!/usr/bin/env python3
"""Verify full original DOS scanner CODE/DATA, switch table and linked MAINL.

Re-read the actual native qsort+hqsort+xx/scantol 22-source evidence,
pinned original scanner.obj, literal ordered 33 OMF fields, semantic
format-class DATA and both real TASM/TLIB/TLINK output vectors.
"""
import json
from pathlib import Path

from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_scanner_work as producer
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REVIEW='.analysis/work/mainl-scanner-native-review.json'


def native_parts(blob):
    p=payload(blob)
    return (bytes(p[1,i] for i in range(1282)),
            bytes(p[2,i] for i in range(128)))


def review():
    build_raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(build_raw)
    base,files,accepted,members,previous,prevhash=producer.retained()
    original=producer.ORIGINAL.read_bytes()
    src=(ROOT/producer.SOURCE).read_bytes()
    goal=producer.original_scope(original)
    actual_CODE,actual_DATA=native_parts(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['prior_twenty_two_source_build_sha256']==prevhash and
         r['original_sha256']==sha(original) and
         r['source_sha256']==sha(src) and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['native_assembler_flags']==producer.TASM_FLAGS,
         'unchanged fixed Japanese scanner, actual current source/driver and preceding22')
    need(goal['CODE_bytes']==1282 and goal['initialized_DATA_bytes']==128 and
         goal['public']==[(0,'__scanner')] and goal['externals']==
         ['__scantod','__scantol','__scanpop','__scanrslt'] and
         goal['jump_table_start']==1238 and goal['jump_table_entries']==22 and
         len(goal['literal_fields'])==33,
         'entire original 1282 CODE, 128 static ASCII data, 33 literal FIXUPPs')
    ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(actual_CODE[:1238],0))
    need(len(ins)==523 and sum(x.size for x in ins)==1238 and
         all(x.address+ x.size<=1238 for x in ins),
         '523 real 8086 format scanner instructions before actual 22-word table')
    dispatch=[int.from_bytes(actual_CODE[i:i+2],'little') for i in range(1238,1282,2)]
    addr={x.address for x in ins}
    need(len(dispatch)==22 and all(to in addr for to in dispatch),
         'all22 true original switch branch offsets at actual instruction boundaries')
    # These are *source data classes*, not native executable opcodes.
    assert_values={'%':3,'*':4,'0':5,'9':5,'D':7,'d':7,'F':21,
                   'f':10,'[':16,']':16,'s':15,'n':17,'x':18,'X':18,
                   ' ':1,'\t':1}
    need(len(actual_DATA)==128 and
         all(actual_DATA[ord(c)]==value for c,value in assert_values.items()) and
         sum(c==1 for c in actual_DATA)==6,
         'real original format token/ASCII width/whitespace DATA classifications')
    fixups=goal['literal_fields']
    need([q['site'] for q in fixups[:4]]==[96,108,204,221] and
         fixups[3]['frame_method']==5 and fixups[3]['addend']==1238 and
         len([q for q in fixups if 1238<=q['site']<1282])==22,
         'literal original BCC ordered DATA references then TARGET-frame switch')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two actual complete TASM/TLIB/TLINK native original rounds')
    phases=['extract']+[f'round{i}-{x}' for i in (1,2)
                        for x in ('assemble','library','link')]
    need([p['label'] for p in r['phases']]==phases and all(
         p['returncode']==0 and sha((ROOT/p['log_path']).read_bytes())==
         p['log_sha256'] for p in r['phases']),
         'actual original Borland writer phase return codes and logs')
    expected=sorted(set(previous[0])|{'scanner'})
    output_vectors=[]
    for index,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'complete raw scanner object and source CRT/executable/map outputs')
        out={}
        for name,meta in row['outputs'].items():
            blob=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                 'complete original native '+name+' file identity')
            out[name]=blob
        need(producer.original_scope(out['obj'])==goal and
             native_parts(out['obj'])==(actual_CODE,actual_DATA) and
             literal_fields(out['obj'])==fixups,
             'all scanner CODE bytes, semantic DATA and literal ordered OMF fields exact')
        native=dict(previous[index],scanner=out['obj'])
        compared=compare_members(members,library_members(out['lib']),native)
        need(compared==row['library_comparison'] and
             compared['replaced_members']==expected and
             compared['contextual_members_unchanged']==870,
             'real23 source library members in original slots with870 others unchanged')
        need(out['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete original Japanese decoded MAINL EXE and actual native MAP bitwise equal')
        mz=parse_mz(out['exe'])
        need(mz.valid and len(out['exe'])==67372 and len(mz.relocations)==677,
             'complete native DOS Japanese MZ and all677 original relocations')
        output_vectors.append(out)
    need(output_vectors[0]==output_vectors[1],
         'two identical raw native source OBJ/LIB/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                original_scanner_CODE_bytes=1282,native_scanner_CODE_bytes=1282,
                original_scanner_initialized_DATA_bytes=128,
                native_initialized_DATA_bytes=128,
                literal_native_CODE_equal=True,literal_native_DATA_equal=True,
                ordered_original_OMF_FIXUPPs=33,literal_FIXUPPs_equal=True,
                semantic_ASCII_classifications_exact=True,
                original_8086_instruction_count=523,
                symbolic_switch_table_words=22,
                original_switch_table_offset=1238,
                original_CRT_members=893,native_source_modules=23,
                untouched_original_CRT_programs=870,
                cumulative_source_CODE_bytes=17768,
                newly_recovered_initialized_DATA_bytes=128,
                entire_original_Japanese_EXE_raw_equal=True,
                entire_original_MAP_raw_equal=True,
                original_MZ_relocations=677,whole_EXE_file_bytes=67372,
                native_repeated_rounds=2,
                source_path=producer.SOURCE,
                source_sha256=sha(src),original_obj_sha256=sha(original),
                native_build_report_sha256=sha(build_raw),
                previous_twenty_two_source_receipt_sha256=prevhash,
                formal_accepted_publication_unchanged=True)


if __name__=='__main__':
    report=review()
    (ROOT/REVIEW).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
