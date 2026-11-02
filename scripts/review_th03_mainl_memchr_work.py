#!/usr/bin/env python3
"""Review exact original memchr code and four-member source CRT MAINL link."""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_memchr_combo_work as producer
from build_th03_mainl_resources_work import need,sha
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.borland_library import compare_members,library_members

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-memchr-combo-review.json'


def review():
    base,files,accepted,members,prior,existing,prior_hash=producer.inherited_library()
    raw=(ROOT/producer.REPORT).read_bytes()
    report=json.loads(raw)
    source=(ROOT/producer.SOURCE).read_bytes()
    original=producer.ORIGINAL.read_bytes()
    code=producer.native_scope(original)
    need(report['complete'] and not report['source_acceptance'] and
         report['added_accepted_bytes']==0 and not report['original_cold_rebuilt'] and
         report['accepted_baseline']==base and
         report['accepted_library_sha256']==sha(accepted) and
         report['inherited_three_source_sha256']==prior_hash and
         report['original_member_sha256']==sha(original) and
         report['source_sha256']==sha(source) and
         report['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()),
         'current original source, three-source parent and native build recipe')
    decoded=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(code,0))
    need(sum(i.size for i in decoded)==37 and
         decoded[0].mnemonic=='push' and decoded[-1].mnemonic=='retf',
         'complete natural 8086 far C function body, without patches')
    original_group=[r.data for r in parse_omf(original) if r.name=='GRPDEF']
    need(original_group==[bytes.fromhex('08ff03ff02')],
         'original zero-size BSS before DATA native group')
    need(len(report['rounds'])==2 and
         [r['round'] for r in report['rounds']]==[1,2],
         'two real native rounds')
    phases=['extract']+[f'round{n}-{kind}' for n in (1,2)
                        for kind in ('assemble','library','link')]
    need([q['label'] for q in report['phases']]==phases and
         all(q['returncode']==0 and
             sha((ROOT/q['log_path']).read_bytes())==q['log_sha256']
             for q in report['phases']),
         'complete native builder commands and real phase log bytes')
    vectors=[]
    for row in report['rounds']:
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'all four complete native raw output types')
        v={}
        for key,meta in row['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'actual complete retained source output '+key)
            v[key]=data
        need(producer.native_scope(v['obj'])==code and
             row['native_code_sha256']==sha(code) and
             [f.data for f in parse_omf(v['obj']) if f.name=='GRPDEF']==original_group,
             'all37 original CODE bytes, no fixups and exact group layout')
        compared=compare_members(members,library_members(v['lib']),
                                 dict(existing,memchr=v['obj']))
        need(compared==row['library_comparison'] and
             compared['replaced_members']==producer.REPLACED and
             compared['contextual_members_unchanged']==889,
             'original four-source member positions, all889 vendor members intact')
        need(v['exe']==(producer.build.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             v['map']==(producer.build.WORK/'obj/th03/mainl.map').read_bytes(),
             'entire Japanese decoded MAINL EXE and MAP raw-equal')
        mz=parse_mz(v['exe'])
        need(mz.valid and len(mz.relocations)==677 and len(v['exe'])==67372,
             'complete source MZ original header and677 relocations')
        vectors.append(v)
    need(vectors[0]==vectors[1],'two repeated complete native raw vectors')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,bounded_native_source_exact=True,
                original_and_candidate_memchr_CODE_bytes=[37,37],
                native_memchr_ordered_fixups=[0,0],
                original_memchr_OMF_GROUP=original_group[0].hex(),
                source_member_indices=[259,260,261,292],
                replaced_members=producer.REPLACED,
                original_library_members=893,unchanged_original_member_programs=889,
                decoded_EXE_bytes=67372,MZ_relocations=677,
                whole_decoded_EXE_raw_equal=True,whole_MAP_raw_equal=True,
                deterministic_complete_rounds=2,
                source_path=producer.SOURCE,source_sha256=sha(source),
                driver_sha256=sha((ROOT/producer.DRIVER).read_bytes()),
                preceding_three_source_receipt_sha256=prior_hash,
                selected_build_report_sha256=sha(raw),
                published_acceptance_unchanged=True)


if __name__=='__main__':
    result=review()
    (ROOT/REPORT).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
