#!/usr/bin/env python3
"""Review bounded natural original qsort near swap helper and one BSS fixup."""
import json
from pathlib import Path

import probe_th03_mainl_qsort_swap as producer
from build_th03_mainl_resources_work import cold_context,need,sha
from lib.omf import describe_omf,parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from build_th03_mainl_display_work import literal_fields

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-qsort-swap-review.json'


def review():
    cold_context(ROOT)
    raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(raw)
    source=(ROOT/producer.SOURCE).read_bytes()
    original=producer.ORIGINAL.read_bytes()
    target=producer.original_prefix(original)
    native_field=producer.field0(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['accepted_source_bytes']==0 and not r['complete_qsort'] and
         not r['original_cold_rebuilt'] and
         r['original_object_sha256']==sha(original) and
         r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['native_wrapper_sha256']==sha(producer.STUB.encode()),
         'unchanged full original qsort and maintained native semantic swap source')
    need(segment_definitions(original)[0]['size']==756 and
         len(literal_fields(original))==29 and
         len(r['rounds'])==2 and [n['round'] for n in r['rounds']]==[1,2],
         '756-byte original TU/29 fields and two native helper-only rounds')
    objects=[]
    for q in r['rounds']:
        data=(ROOT/q['obj_path']).read_bytes()
        log=(ROOT/q['log_path']).read_bytes()
        need(q['obj_sha256']==sha(data) and q['obj_bytes']==len(data) and
             q['log_sha256']==sha(log) and q['prefix_CODE_sha256']==sha(target) and
             q['single_native_FIXUPP']==native_field,
             'retained complete TASM output and original native BSS fixup')
        need(describe_omf(data)['valid'] and
             [(s['name'],s['size']) for s in segment_definitions(data)]==
             [('_TEXT',46),('_DATA',0),('_BSS',6)] and
             producer.original_prefix(data)==target and
             producer.field0(data)==native_field and
             [x.data.hex() for x in parse_omf(data) if x.name=='GRPDEF']==
             ['08ff03ff02'],
             'all46 actual original qsort helper instructions and native group/field')
        objects.append(data)
    need(objects[0]==objects[1],
         'two full native partial qsort object files reproducible raw')
    return dict(complete=True,source_acceptance=False,accepted_source_bytes=0,
                complete_qsort=False,original_cold_rebuilt=False,
                original_qsort_CODE_bytes=756,original_qsort_FIXUPPs=29,
                exactly_recovered_swap_CODE_bytes=46,
                exact_swap_BSS_fixup_site=9,original_BSS_bytes=6,
                native_source_swap_exact=True,native_swap_FIXUPP_equal=True,
                separate_native_rounds=2,
                actual_pinned_original_object_sha256=sha(original),
                selected_build_receipt_sha256=sha(raw),
                source_sha256=sha(source),
                only_bounded_swap_claimed=True)


if __name__=='__main__':
    result=review()
    (ROOT/REPORT).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
