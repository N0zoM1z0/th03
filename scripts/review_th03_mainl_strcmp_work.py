#!/usr/bin/env python3
"""Review exact original DOS strcmp and cumulative three-source CRT link."""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_strcmp_combo_work as producer
from build_th03_mainl_resources_work import need,sha
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from lib.borland_library import compare_members,library_members

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-strcmp-combo-review.json'


def review():
    base,files,accepted,members,prior,memcpy_obj,memcmp_obj,prior_hash=producer.existing_memory_sources()
    existing={'memcpy':memcpy_obj,'memcmp':memcmp_obj}
    raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(raw)
    original=producer.VENDOR_OBJ.read_bytes()
    source=(ROOT/producer.SOURCE).read_bytes()
    code=producer.native_scope(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['preceding_memcmp_producer_sha256']==prior_hash and
         r['source_sha256']==sha(source) and
         r['original_member_sha256']==sha(original) and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()),
         'original vendor,source,driver and inherited two-source library')
    instructions=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(code,0))
    need(sum(i.size for i in instructions)==48 and
         instructions[0].mnemonic=='push' and
         instructions[-1].mnemonic=='retf',
         'complete natural far cdecl 48-byte function')
    need(len(r['rounds'])==2 and [x['round'] for x in r['rounds']]==[1,2],
         'two complete real native source rounds')
    expected=['extract']+[f'round{n}-{kind}' for n in (1,2)
                          for kind in ('assemble','library','link')]
    need([x['label'] for x in r['phases']]==expected and
         all(x['returncode']==0 and
             sha((ROOT/x['log_path']).read_bytes())==x['log_sha256']
             for x in r['phases']),
         'complete original writer phase order and actual logs')
    grp=[x.data for x in parse_omf(original) if x.name=='GRPDEF']
    need(grp==[bytes.fromhex('08ff03ff02')],'original BSS-before-DATA record')
    vectors=[]
    for entry in r['rounds']:
        need(set(entry['outputs'])=={'obj','lib','exe','map'},
             'four complete raw native output kinds')
        v={}
        for kind,meta in entry['outputs'].items():
            b=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(b),sha256=sha(b)),
                 'unchanged complete raw '+kind+' output')
            v[kind]=b
        need(producer.native_scope(v['obj'])==code and
             entry['native_CODE_sha256']==sha(code) and
             [q.data for q in parse_omf(v['obj']) if q.name=='GRPDEF']==grp,
             'all48 source CODE bytes,no ordered fixups,original group records')
        compared=compare_members(members,library_members(v['lib']),
                                 dict(existing,strcmp=v['obj']))
        need(compared==entry['library_comparison'] and
             compared['replaced_members']==['memcmp','memcpy','strcmp'] and
             compared['contextual_members_unchanged']==890,
             'three original-position source members,890 preserved vendor records')
        need(v['exe']==(producer.build.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             v['map']==(producer.build.WORK/'obj/th03/mainl.map').read_bytes(),
             'exact complete original Japanese decoded MAINL EXE and MAP')
        mz=parse_mz(v['exe'])
        need(mz.valid and len(mz.relocations)==677 and len(v['exe'])==67372,
             'complete valid original MZ header and ordered relocations')
        vectors.append(v)
    need(vectors[0]==vectors[1],'two reproducible complete raw native vectors')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,bounded_native_source_exact=True,
                original_and_candidate_strcmp_CODE_bytes=[48,48],
                native_strcmp_ordered_fixups=[0,0],original_strcmp_OMF_GROUP=grp[0].hex(),
                source_member_indices=[260,261,292],
                replaced_members=['memcmp','memcpy','strcmp'],
                original_library_members=893,unchanged_original_member_programs=890,
                decoded_EXE_bytes=67372,MZ_relocations=677,
                whole_decoded_EXE_raw_equal=True,whole_MAP_raw_equal=True,
                deterministic_complete_rounds=2,source=producer.SOURCE,
                source_sha256=sha(source),driver_sha256=sha((ROOT/producer.DRIVER).read_bytes()),
                inherited_two_source_receipt_sha256=prior_hash,
                selected_build_report_sha256=sha(raw),
                published_acceptance_unchanged=True)


if __name__=='__main__':
    result=review()
    (ROOT/REPORT).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
