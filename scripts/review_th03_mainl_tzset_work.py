#!/usr/bin/env python3
"""Independent review original four-segment tzset and 58-source Japanese MAINL.

Unlike prior timecvt/strftime/fclose gaps, tzset's 48 native ordered
OMF FIXUPPs including DATA and INITDATA fields are literal-original.
"""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_tzset_work as p
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-tzset-native-review.json'


def part(obj,section,size):
    d=payload(obj)
    return bytes(d[section,i] for i in range(size))


def review():
    raw=(ROOT/p.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,parents,parenthash=p.retained()
    original=p.ORIGINAL.read_bytes()
    goal=p.native_scope(original)
    source=(ROOT/p.SOURCE).read_bytes()
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['original_tzset_literal_OMF_exact'] and
         r['prior_fopen_OMF_order_open'] and
         r['prior_fclose_MKNAME_frame_open'] and
         r['prior_timecvt_near_frame_open'] and
         r['prior_strftime_near_frame_open'] and
         r['prior_tempnam_near_frame_open'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_fifty_seven_source_build_sha256']==parenthash and
         r['original_sha256']==sha(original) and
         r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         r['native_assembler_flags']==p.TASM_FLAGS,
         'source-bound tzset native code and accepted original CRT/57-parent')
    need(goal['CODE_bytes']==744 and goal['DATA_bytes']==48 and
         goal['BSS_bytes']==8 and goal['INITDATA_bytes']==6 and
         goal['original_code_publics']==p.CODE_PUB and
         goal['original_data_publics']==p.DATA_PUB and
         goal['original_imports']==p.EXTERNS and
         goal['original_group']=='0aff03ff02' and
         len(goal['original_literal_ordered_fixups'])==48,
         'all four original physical segments, data exports and CODE/INIT fields')
    CODE=part(original,1,744)
    DATA=part(original,2,48)
    INIT=part(original,4,6)
    decoder=Cs(CS_ARCH_X86,CS_MODE_16)
    sizes=[sum(x.size for x in decoder.disasm(CODE[a:b],a))
           for a,b in ((0,508),(508,744))]
    need(sizes==[508,236],
         'all 744 original instructions in native tzset and ISDST function bodies')
    need(DATA[40:]==bytes.fromhex('545a004a53540000') and
         DATA[34:38]==bytes.fromhex('7081ffff') and
         INIT==bytes.fromhex('011e00000000'),
         'real TZ/JST source strings, -32400 JST and initializer signature')
    fields=literal_fields(original)
    need([sum(f['segment']==segment for f in fields) for segment in (1,2,3,4)]==
         [45,2,0,1] and
         [(f['segment'],f['site']) for f in fields[-3:]]==
         [(2,26),(2,30),(4,2)],
         'original 45 CODE, two far DATA name pointers and one INITDATA fixup')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two independent complete original TASM/TLIB/TLINK rounds')
    labels=['extract']+[f'round{i}-{stage}' for i in (1,2)
                        for stage in ('assemble','library','link')]
    need([q['label'] for q in r['phases']]==labels and
         all(q['returncode']==0 and
             sha((ROOT/q['log_path']).read_bytes())==q['log_sha256']
             for q in r['phases']),
         'real Borland commands and preserved writer logs')
    vectors=[]
    for index,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'complete original native OBJ/LIB/EXE/MAP artifacts')
        output={}
        for kind,meta in row['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'complete actual source '+kind+' raw artifact')
            output[kind]=data
        obj=output['obj']
        need(p.native_scope(obj)==goal and
             part(obj,1,744)==CODE and part(obj,2,48)==DATA and
             part(obj,4,6)==INIT and
             literal_fields(obj)==fields,
             'all CODE/DATA/INITDATA and 48 literal ordered original OMF fields')
        sources=dict(parents[index],tzset=obj)
        cmp=compare_members(members,library_members(output['lib']),sources)
        need(cmp==row['library_comparison'] and
             cmp['replaced_members']==sorted(sources) and
             cmp['contextual_members_unchanged']==835,
             '58 genuine source CRT owner programs,835 original members unchanged')
        need(output['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             output['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'whole original Japanese decoded MAINL EXE/MAP raw equal')
        mz=parse_mz(output['exe'])
        need(mz.valid and len(output['exe'])==67372 and len(mz.relocations)==677,
             'full original DOS MZ including exact 677 relocation entries')
        vectors.append(output)
    need(vectors[0]==vectors[1],
         'two complete reproducible source native original outputs')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,
                new_tzset_CODE_bytes=744,new_tzset_DATA_bytes=48,
                new_tzset_BSS_bytes=8,new_tzset_INITDATA_bytes=6,
                full_original_CODE_raw_equal=True,full_original_DATA_raw_equal=True,
                full_original_INITDATA_raw_equal=True,
                original_function_sizes=[508,236],
                original_CODE_publics=p.CODE_PUB,original_DATA_publics=p.DATA_PUB,
                original_imports=p.EXTERNS,
                original_OMF_fixups=48,complete_literal_ordered_FIXUPPs_equal=True,
                CODE_fixup_count=45,DATA_fixup_count=2,INITDATA_fixup_count=1,
                original_893_CRT_members=893,simultaneous_source_CRT_members=58,
                unchanged_original_vendor_programs=835,
                cumulative_exact_source_CODE_bytes=28211,
                whole_original_Japanese_EXE_raw_equal=True,whole_original_MAP_raw_equal=True,
                original_Japanese_EXE_bytes=67372,original_MZ_relocations=677,
                independent_native_rounds=2,
                predecessor_fopen_OMF_gap_open=True,
                predecessor_fclose_OMF_gap_open=True,
                predecessor_timecvt_OMF_gap_open=True,
                predecessor_strftime_OMF_gap_open=True,
                predecessor_tempnam_OMF_gap_open=True,
                native_source_path=p.SOURCE,build_report_sha256=sha(raw),
                parent_57_source_report_sha256=parenthash,
                formal_accepted_ledger_unchanged=True)


if __name__=='__main__':
    r=review()
    (ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
