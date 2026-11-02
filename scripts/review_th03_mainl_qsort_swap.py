#!/usr/bin/env python3
"""Review only the first 46 bytes of the original qsort boss TU."""
import json
from pathlib import Path

import probe_th03_mainl_qsort_swap as producer
from build_th03_mainl_resources_work import need,sha,cold_context
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.omf import parse_omf

ROOT=Path(__file__).resolve().parents[1]
REVIEW='.analysis/work/mainl-qsort-swap-review.json'


def review():
    cold_context(ROOT)
    raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(raw)
    original=producer.ORIGINAL.read_bytes()
    source=(ROOT/producer.SOURCE).read_bytes()
    first=producer.original_prefix(original)
    expected=producer.field0(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['accepted_source_bytes']==0 and not r['complete_qsort'] and
         not r['original_cold_rebuilt'] and
         r['original_object_sha256']==sha(original) and
         r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['native_wrapper_sha256']==sha(producer.STUB.encode()),
         'true unchanged original 756-byte qsort and 46-byte native recipe')
    need(len(r['rounds'])==2 and [x['round'] for x in r['rounds']]==[1,2],
         'two complete original writer runs')
    vectors=[]
    for row in r['rounds']:
        obj=(ROOT/row['obj_path']).read_bytes()
        log=(ROOT/row['log_path']).read_bytes()
        need(row['obj_sha256']==sha(obj) and row['obj_bytes']==len(obj) and
             row['log_sha256']==sha(log) and
             producer.original_prefix(obj)==first and
             producer.field0(obj)==expected and
             row['single_native_FIXUPP']==expected and
             row['prefix_CODE_sha256']==sha(first),
             '46 native bytes and original unaltered ordered BSS relocation')
        need(segment_definitions(obj)[0]['size']==46 and
             [x.data.hex() for x in parse_omf(obj) if x.name=='GRPDEF']==
             ['08ff03ff02'],'one natural near helper and original segment group')
        vectors.append(obj)
    need(vectors[0]==vectors[1],'all actual raw native OMF records repeat twice')
    return dict(complete=True,source_acceptance=False,
                complete_qsort=False,original_cold_rebuilt=False,
                original_boss_CODE_bytes=756,native_recovered_helper_CODE_bytes=46,
                native_helper_raw_equal=True,original_helper_near_return_pop_bytes=8,
                original_qsort_BSS_bytes=6,ordered_prefix_fixups=1,
                prefix_FIXUPP_raw_equal=True,whole_qsort_source_exact=False,
                whole_qsort_linked=False,verified_native_rounds=2,
                source_path=producer.SOURCE,
                driver_sha256=sha((ROOT/producer.DRIVER).read_bytes()),
                bound_build_report_sha256=sha(raw),
                published_accepted_source_bytes_added=0)


if __name__=='__main__':
    result=review()
    (ROOT/REVIEW).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
