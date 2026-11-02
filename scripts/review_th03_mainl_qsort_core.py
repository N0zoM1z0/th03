#!/usr/bin/env python3
"""Bounded verified structural blueprint for the still-open DOS qsort core.

Read the immutable original qsort CODE/OMF, classify every near helper
and imported arithmetic call, far comparator callback, and branch
destination. Does NOT pass off disassembly as recovered source or
introduce binary patches.
"""
import json
from pathlib import Path

from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM

import probe_th03_mainl_qsort_entry as entry
from build_th03_mainl_resources_work import cold_context,need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.decoded_mainl_display_native import externs
from lib.omf import describe_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-qsort-core-map-review.json'


def review():
    cold_context(ROOT)
    original=entry.ORIGINAL.read_bytes()
    need(describe_omf(original)['valid'] and
         [(s['name'],s['size']) for s in segment_definitions(original)]==
         [('_TEXT',756),('_DATA',0),('_BSS',6)],
         'entire original native qsort BSS/CODE ownership')
    p=payload(original)
    code=bytes(p[1,i] for i in range(756))
    core=code[46:712]
    decoder=Cs(CS_ARCH_X86,CS_MODE_16)
    decoder.detail=True
    instructions=list(decoder.disasm(core,46))
    need(len(core)==666 and len(instructions)==242 and
         sum(q.size for q in instructions)==666 and
         instructions[0].address==46 and
         instructions[0].mnemonic=='push' and
         instructions[-1].address==0x2C5 and
         instructions[-1].mnemonic=='ret' and
         instructions[-1].op_str=='6',
         'complete original 666-byte/242-instruction near pascal recursive core')
    fields=literal_fields(original)
    need(len(fields)==29 and externs(original)==['N_LXMUL@','N_LDIV@'],
         '29 real fixups and two original 16-bit far arithmetic imports')
    core_fields=[q for q in fields if 46<=q['site']<712]
    need(len(core_fields)==25 and
         [q['site'] for q in fields if not 46<=q['site']<712]==
         [9,721,735,738],
         '25 native core field sites plus known four near/far source fields')
    math_sites={134:'N_LXMUL@',161:'N_LXMUL@',
                613:'N_LDIV@',648:'N_LDIV@'}
    bysite={f['site']:f for f in fields}
    for site,name in math_sites.items():
        f=bysite[site]
        need(f['target_method']==2 and f['target']==externs(original).index(name)+1 and
             f['location_type']==1 and f['width']==2 and not f['segment_relative'],
             'literal source arithmetic near call displacement: '+name)
    swapped=[];recurse=[];math=[];comparator=[];branches=[]
    bounds={i.address for i in instructions}
    for ins in instructions:
        if ins.mnemonic=='call':
            need(ins.size==3 and ins.bytes[0]==0xe8,
                 'original near helper and imported arithmetic 16-bit call')
            if ins.address+1 in math_sites:
                math.append(dict(site=ins.address,name=math_sites[ins.address+1]))
                continue
            disp=int.from_bytes(ins.bytes[1:],'little',signed=True)
            target=(ins.address+3+disp)&65535
            need(target in (0,46),'real near call is swap helper or recursive core')
            (swapped if target==0 else recurse).append(ins.address)
        elif ins.mnemonic=='lcall':
            need(ins.bytes==bytes.fromhex('ff1e0000') and
                 any(f['site']==ins.address+2 and
                     f['target_method']==0 and f['target']==3 and
                     f['addend']==0 for f in core_fields),
                 'one far comparator callback through four-byte BSS slot')
            comparator.append(ins.address)
        if ins.mnemonic.startswith('j'):
            need(ins.operands and ins.operands[0].type==X86_OP_IMM,
                 'original local 16-bit branch,not an indirect import')
            target=ins.operands[0].imm &65535
            need(target in bounds,
                 'all original qsort branches stay within the real core')
            branches.append(dict(at=ins.address,target=target,mnemonic=ins.mnemonic))
    need(swapped==[0xCE,0x119,0x12E,0x15E,0x1BF,0x234] and
         recurse==[0x299,0x2AE] and
         [m['site'] for m in math]==[0x85,0xA0,0x264,0x287] and
         comparator==[0x5D,0xB7,0xDD,0x102,0x181,0x19D,0x1EF] and
         len(branches)==30,
         'full actual recursive/helper/compare/math/branch control-flow inventories')
    return dict(complete=True,complete_qsort=False,source_acceptance=False,
                accepted_source_bytes=0,original_cold_rebuilt=False,
                original_qsort_CODE_bytes=756,private_swap_CODE_bytes=46,
                recursive_core_CODE_bytes=666,far_public_CODE_bytes=44,
                recursive_core_instruction_count=242,
                original_Omf_fixup_count=29,recursive_core_fixup_count=25,
                recovered_prefix_and_entry_fixups=[9,721,735,738],
                comparator_BSS_offset=0,element_width_BSS_offset=4,
                near_swap_call_sites=swapped,recursive_call_sites=recurse,
                math_call_sites=math,far_comparator_call_sites=comparator,
                branch_count=len(branches),original_core_branch_targets=branches,
                original_unmodified_qsort_object_sha256=sha(original),
                original_source_core_recovered=False,
                next_work_reconstruct_near_recursive_partition=True)


if __name__=='__main__':
    r=review()
    (ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='original_core_branch_targets'},indent=2))
