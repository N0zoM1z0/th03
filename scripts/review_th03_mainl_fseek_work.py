#!/usr/bin/env python3
"""Review true selected CRT fseek member, standalone variant and 31-source MAINL."""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_fseek_work as producer
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.omf import parse_omf
from lib.borland_library import compare_members,library_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-fseek-native-review.json'


def review():
    raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,previous,parenthash=producer.retained()
    vendor=producer.ORIGINAL.read_bytes()
    h=next(iter(parse_omf(vendor)))
    member=vendor[h.offset:h.offset+h.length+3]+members[232].program_records
    goal=producer.original_scope(member)
    standfields=literal_fields(vendor)
    memberfields=literal_fields(member)
    sources={name:(ROOT/name).read_bytes() for name in producer.SOURCES}
    layout=(ROOT/producer.LAYOUT).read_bytes()
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_thirty_source_build_sha256']==parenthash and
         r['original_sha256']==sha(vendor) and
         r['selected_original_member_sha256']==sha(members[232].program_records) and
         r['source_sha256']=={name:sha(blob) for name,blob in sources.items()} and
         r['layout_sha256']==sha(layout) and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['native_assembler_flags']==producer.TASM_FLAGS,
         'current native semantic FILE layout, real library and writer recipe')
    need([q['site'] for q in memberfields]==[342,149,239,293,365,409] and
         [q['site'] for q in standfields]==[409,365,342,293,239,149] and
         r['original_selected_member_fixup_sites']==[q['site'] for q in memberfields] and
         r['original_standalone_fixup_sites']==[q['site'] for q in standfields] and
         sorted(memberfields,key=lambda f:f['site'])==
         sorted(standfields,key=lambda f:f['site']),
         'original source/standalone variants agree logically but differ in OMF order')
    a=payload(vendor)
    b=payload(member)
    need(all(a[1,i]==b[1,i] for i in range(492)),
         'real original vendor library and standalone original CODE raw equal')
    need(goal['CODE_bytes']==492 and goal['original_public_offsets']==[137,267] and
         goal['original_function_boundaries']==(0,137,267,492) and
         goal['imports']==['_fflush','_lseek','__openfd'],
         'two public fseek/ftell, private near LF correction, actual import order')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16)
    code=bytes(b[1,i] for i in range(492))
    need([sum(ins.size for ins in decoder.disasm(code[i:j],i))
          for i,j in [(0,137),(137,267),(267,492)]]==[137,130,225],
         'three original near/private and two far public function bodies')
    need(len(r['rounds'])==2 and [v['round'] for v in r['rounds']]==[1,2],
         'two independent source compiler and original library links')
    logs=['extract']+[f'round{i}-{kind}' for i in (1,2)
                      for kind in ('assemble','library','link')]
    need([x['label'] for x in r['phases']]==logs and all(
         x['returncode']==0 and sha((ROOT/x['log_path']).read_bytes())==
         x['log_sha256'] for x in r['phases']),
         'actual real TASM/TLIB/TLINK native phase logs')
    vectors=[]
    for i,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'complete native OBJ/LIB/EXE/MAP source outputs')
        out={}
        for name,meta in row['outputs'].items():
            content=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(content),sha256=sha(content)),
                 'full real output byte identity '+name)
            out[name]=content
        need(producer.original_scope(out['obj'])==goal and
             bytes(payload(out['obj'])[1,k] for k in range(492))==code and
             literal_fields(out['obj'])==memberfields,
             'source CODE, actual selected CRT six ordered relocations and public ABI exact')
        compiled=dict(previous[i],fseek=out['obj'])
        comparison=compare_members(members,library_members(out['lib']),compiled)
        need(comparison==row['library_comparison'] and
             comparison['replaced_members']==sorted(compiled) and
             comparison['contextual_members_unchanged']==862,
             '31 genuine native source modules and862 entire unchanged library programs')
        need(out['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'entire original fixed Japanese decoded MAINL EXE/MAP raw identical')
        mz=parse_mz(out['exe'])
        need(mz.valid and len(out['exe'])==67372 and len(mz.relocations)==677,
             'true original relocation-bearing Japanese executable file')
        vectors.append(out)
    need(vectors[0]==vectors[1],'two complete byte-identical native source rounds')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,
                original_selected_CRT_CODE_bytes=492,source_CODE_bytes=492,
                all_native_CODE_bytes_equal=True,
                private_near_buffer_calculator_bytes=137,
                far_fseek_bytes=130,far_ftell_bytes=225,
                original_far_public_offsets=[137,267],
                literal_selected_CRT_FIXUPPs=6,selected_fields_raw_equal=True,
                standalone_original_FIXUPPs=6,
                selected_member_fixup_sites=[342,149,239,293,365,409],
                standalone_original_fixup_sites=[409,365,342,293,239,149],
                logical_field_sets_equal_but_order_distinct=True,
                original_library_members=893,simultaneous_source_members=31,
                unchanged_original_member_programs=862,
                cumulative_source_CODE_bytes=19832,
                real_Japanese_EXE_bytes=67372,original_MZ_relocations=677,
                entire_Japanese_EXE_raw_equal=True,whole_MAP_raw_equal=True,
                native_repeated_rounds=2,
                code_source=producer.SOURCES[0],file_layout_source=producer.LAYOUT,
                parent_receipt_sha256=parenthash,build_report_sha256=sha(raw),
                accepted_publication_unchanged=True)


if __name__=='__main__':
    receipt=review()
    (ROOT/REPORT).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
