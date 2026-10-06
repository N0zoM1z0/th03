#!/usr/bin/env python3
"""Classify the six decoded OP inequalities without normalizing acceptance."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from inventory_rec98_th03 import frozen_files
from lib.pc98 import parse_mz
from review_th03_mainl_cutscene import REVISION,sha

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/th03-op-title/sol-op-title-source-20261006-b/receipt.json'
PROOF_SHA='626257123d424e373e7e1c051b168f305e57e1f3e9fc35a0894e63ca0ef2eea5'
PROVIDERS=['th03/op_music.cpp','th02/op/m_music.cpp','th03/op/m_main.cpp',
           'th03_op.asm','libs/master.lib/vs[data].asm','libs/master.lib/wordmask[data].asm']


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('OP inequality compiler prerequisite differs')
    proof=json.loads(raw);inputs=dict(proof['inputs']);inputs[PROOF]=sha(raw)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP inequality prerequisite input differs: '+p)
    for p in ('scripts/review_th03_op_inequalities.py','scripts/lib/pc98.py','scripts/inventory_rec98_th03.py','scripts/review_th03_mainl_cutscene.py'):
        inputs[p]=sha((ROOT/p).read_bytes())
    parent=json.loads((ROOT/'.analysis/sol-op-title-review-20261006.json').read_bytes())
    target_path=parent['observations'][0]['path'];target=parse_mz((ROOT/target_path).read_bytes())
    if not target.valid:raise ValueError('invalid decoded OP')
    frozen=frozen_files(REVISION);observations=[];decoder=Cs(CS_ARCH_X86,CS_MODE_16)
    for round in proof['rounds']:
        tree=Path(PROOF).parent/f'round{round["number"]}'/'source';p=str(tree/'bin/th03/op.exe');raw=(ROOT/p).read_bytes()
        inputs[p]=sha(raw)
        if inputs[p]!=round['products']['bin/th03/op.exe']:raise ValueError('OP inequality fresh product differs')
        candidate=parse_mz(raw)
        if not candidate.valid or len(candidate.program_image)!=len(target.program_image):raise ValueError('OP inequality decoded size differs')
        mp=str(tree/'obj/th03/op.map');raw=(ROOT/mp).read_bytes();inputs[mp]=sha(raw);text=raw.decode()
        if inputs[mp]!=round['map_sha256']:raise ValueError('OP inequality original cold MAP differs')
        lineage={}
        for name in PROVIDERS:
            cp=str(tree/name);data=(ROOT/cp).read_bytes();inputs[cp]=sha(data);expected=frozen[name]
            # The title prefix is intentionally maintained in this carrier;
            # its original frozen body is bound by the prerequisite receipt.
            if name=='th03/op/m_main.cpp':
                cfg=tomllib.loads((ROOT/'config/th03_op_title_candidate.toml').read_text())
                text_source=frozen[name].decode();split=text_source.index(cfg['anchor'])
                expected=(f'#include "{cfg["source"]}"\n\n'+text_source[split:]).encode()
                if data!=expected:raise ValueError('OP inequality declared maintained carrier differs')
            else:
                if name.endswith('.asm'):data=data.replace(b'\r\n',b'\n');expected=expected.replace(b'\r\n',b'\n')
                if data!=expected:raise ValueError('OP inequality frozen provider differs: '+name)
            lineage[name]=dict(frozen_sha256=sha(frozen[name]),cached_sha256=inputs[cp])
        changes=[i for i,(x,y) in enumerate(zip(target.program_image,candidate.program_image)) if x!=y]
        if changes!=[0xa606,0xa608,0xb118,0xb119,0xb13e,0xdd95]:raise ValueError('OP known six-byte inequality differs')
        instruction_pairs=[]
        for a,z,name in [(0xcf6,30,'Music Room nopoly_B_put'),(0x180a,94,'box_column16_unput')]:
            original=list(decoder.disasm(target.program_image[0x9900+a:0x9900+a+z],a))
            generated=list(decoder.disasm(candidate.program_image[0x9900+a:0x9900+a+z],a))
            if sum(i.size for i in original)!=z or sum(i.size for i in generated)!=z or original[-1].mnemonic!='ret':raise ValueError('OP inequality instruction boundary differs')
            if [(i.address,i.size,i.mnemonic,i.op_str) for i in original]!=[(i.address,i.size,i.mnemonic,i.op_str) for i in generated]:raise ValueError('OP inequality decoded operation differs')
            for x,y in zip(original,generated):
                if x.bytes!=y.bytes:
                    instruction_pairs.append(dict(candidate_function=name,decoded_segment=0x990,offset=x.address,
                                                  mnemonic=x.mnemonic,operands=x.op_str,target_hex=x.bytes.hex(),candidate_hex=y.bytes.hex()))
        if len(instruction_pairs)!=4:raise ValueError('OP unequal instruction count differs')
        labels={}
        for name,expected in [('vsync_OldMask',0x5a4),('BYTE_MASK',0x5a6)]:
            matches={int(a,16) for a in re.findall(r'^\s*0D7F:([0-9A-F]{4})\s+(?:idle\s+)?'+name+r'\s*$',text,re.M)}
            if matches!={expected}:raise ValueError('OP candidate data label differs')
            labels[name]=expected
        if b'\tEVEN' not in frozen['libs/master.lib/vs[data].asm']:raise ValueError('OP data alignment provider differs')
        target_sites=[(r.segment,r.offset) for r in target.relocations];candidate_sites=[(r.segment,r.offset) for r in candidate.relocations]
        observations.append(dict(round=round['number'],path=p,source_lineage=lineage,instruction_pairs=instruction_pairs,
                                 raw_changed_bytes=len(changes),raw_equal=False,
                                 data=dict(decoded_segment=0xd7f,offset=0x5a5,target=target.program_image[0xdd95],candidate=candidate.program_image[0xdd95],
                                           candidate_labels=labels,source_alignment='EVEN after vsync_OldMask',
                                           ownership='candidate compiler alignment association; original producer remains unknown'),
                                 relocation_count=len(target_sites),candidate_relocation_count=len(candidate_sites),
                                 ordered_relocations_equal=target_sites==candidate_sites,
                                 mismatching_ordered_rows=sum(a!=b for a,b in zip(target_sites,candidate_sites)),
                                 same_site_multiset=Counter(target_sites)==Counter(candidate_sites)))
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP inequality input changed: '+p)
    final=frozen_files(REVISION)
    if any(final[p]!=frozen[p] for p in PROVIDERS):raise ValueError('OP inequality frozen provider changed')
    report=dict(kind='th03-op-six-byte-and-relocation-order-classification',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,
                observations=observations,source_acceptance=False,exact_acceptance=False,
                notes='Five raw bytes belong to four unequal register-operation encodings in two functions; one data byte is associated with candidate EVEN alignment between old-mask and byte-mask labels. Raw inequality retained. Same relocation-site multiset is corroboration only: original ordered vector stays unequal. Title column native attempt fixture is separately reviewed; Music Room callers/DF-dependent copy/runtime and complete root DATA ownership remain open. No extra units or authored/exact bytes credited.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('Classified six raw unequal bytes; original relocation order remains unequal')


if __name__=='__main__':main()
