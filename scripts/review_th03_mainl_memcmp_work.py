#!/usr/bin/env python3
"""Review two real native CRT source replacements in an exact MAINL link."""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_memcmp_combo_work as producer
from build_th03_mainl_resources_work import need,sha
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.borland_library import compare_members,library_members

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-memcmp-combo-review.json'


def review():
    baseline,files,library,members,prior,prior_obj,prior_hash=producer.inherited_library()
    raw=(ROOT/producer.REPORT).read_bytes()
    report=json.loads(raw)
    source=(ROOT/producer.SOURCE).read_bytes()
    original=producer.ORIGINAL.read_bytes()
    code=producer.native_scope(original)
    need(report['complete'] and not report['source_acceptance'] and
         report['added_accepted_bytes']==0 and not report['original_cold_rebuilt'] and
         report['accepted_baseline']==baseline and
         report['accepted_library_sha256']==sha(library) and
         report['memcpy_producer_sha256']==prior_hash and
         report['source_sha256']==sha(source) and
         report['original_member_sha256']==sha(original) and
         report['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()),
         'complete current native two-member build and immutable accepted baseline')
    instructions=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(code,0))
    need(sum(ins.size for ins in instructions)==40 and
         instructions[0].mnemonic=='push' and
         instructions[-1].mnemonic=='retf',
         'dense native code from far entry to far return,not copied bytes')
    source_group=[q.data for q in parse_omf(original) if q.name=='GRPDEF']
    need(source_group==[bytes.fromhex('08FF03FF02')],
         'original two-segment group ownership order')
    need(len(report['rounds'])==2 and
         [q['round'] for q in report['rounds']]==[1,2],
         'two full native source rounds')
    phases=['extract']+[f'round{round}-{kind}' for round in (1,2)
                        for kind in ('assemble','library','link')]
    need([p['label'] for p in report['phases']]==phases and
         all(p['returncode']==0 and
             sha((ROOT/p['log_path']).read_bytes())==p['log_sha256']
             for p in report['phases']),
         'every complete native execution log and phase order')
    vectors=[]
    for round in report['rounds']:
        need(set(round['outputs'])=={'obj','lib','exe','map'},
             'actual complete OBJ/LIB/EXE/MAP carrier for this round')
        native={}
        for k,meta in round['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'complete original source pair raw output: '+k)
            native[k]=data
        need(producer.native_scope(native['obj'])==code and
             round['native_code_sha256']==sha(code) and
             [q.data for q in parse_omf(native['obj']) if q.name=='GRPDEF']==source_group,
             'complete40-byte comparator code,ordered fields and group records')
        compare=compare_members(members,library_members(native['lib']),
                                {'memcmp':native['obj'],'memcpy':prior_obj})
        need(compare==round['library_comparison'] and
             compare['replaced_members']==['memcmp','memcpy'] and
             compare['contextual_members_unchanged']==891,
             'both real source members in original260/261 positions,891 untouched')
        need(native['exe']==(producer.build.WORK/'bin/th03/mainl.target.exe').read_bytes()
             and native['map']==(producer.build.WORK/'obj/th03/mainl.map').read_bytes(),
             'full source-only decoded Japanese EXE and original MAP raw equal')
        mz=parse_mz(native['exe'])
        need(mz.valid and len(mz.relocations)==677 and len(native['exe'])==67372,
             'actual complete Japanese original MZ and677 relocations')
        vectors.append(native)
    need(vectors[0]==vectors[1],
         'two complete raw output vectors are identical without normalization')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,bounded_native_source_exact=True,
                original_and_candidate_memcmp_CODE_bytes=[40,40],
                native_memcmp_ordered_fixups=[0,0],original_memcmp_OMF_GROUP=source_group[0].hex(),
                replaced_members=['memcmp','memcpy'],source_member_indices=[260,261],
                all_original_library_members=893,unchanged_original_member_programs=891,
                full_decoded_EXE_bytes=67372,full_decoded_MZ_relocations=677,
                whole_decoded_EXE_raw_equal=True,whole_MAP_raw_equal=True,
                deterministic_complete_rounds=2,
                source_path=producer.SOURCE,source_sha256=sha(source),
                current_compiler_driver_sha256=sha((ROOT/producer.DRIVER).read_bytes()),
                inherited_memcpy_receipt_sha256=prior_hash,
                selected_build_report_sha256=sha(raw),
                accepted_publication_unchanged=True)


if __name__=='__main__':
    r=review()
    (ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
