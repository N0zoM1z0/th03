#!/usr/bin/env python3
"""Independently recheck bounded qsort near swap and far public wrapper."""
import json
from pathlib import Path

import probe_th03_mainl_qsort_entry as producer
from build_th03_mainl_resources_work import cold_context,need,sha
from lib.omf import describe_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-qsort-entry-review.json'


def review():
    cold_context(ROOT)
    report_raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(report_raw)
    original=producer.ORIGINAL.read_bytes()
    sources={p:(ROOT/p).read_bytes() for p in producer.SOURCES}
    need(r['complete'] and not r['complete_qsort'] and
         not r['source_acceptance'] and r['accepted_source_bytes']==0 and
         not r['original_cold_rebuilt'] and
         r['original_object_sha256']==sha(original) and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['source_sha256']=={p:sha(data) for p,data in sources.items()} and
         r['isolated_wrapper_sha256']==sha(producer.WRAPPER.encode()),
         'original fixed qsort, real current source and bounded native wrapper')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two actual independent TASM helper/front-end rounds')
    objects=[]
    for row in r['rounds']:
        data=(ROOT/row['output']).read_bytes()
        log=(ROOT/row['log']).read_bytes()
        need(row['output_bytes']==len(data) and
             row['output_sha256']==sha(data) and
             row['log_sha256']==sha(log) and
             describe_omf(data)['valid'],'complete unmodified native partial object and log')
        details=producer.proof(data)
        need(row['scope']==details,'real original BSS/fields and semantic relative CALL target')
        objects.append(data)
    need(objects[0]==objects[1],'two complete partial qsort native objects equal')
    details=producer.proof(objects[0])
    need(details['original_full_CODE']==756 and
         details['original_total_native_fields']==29 and
         details['original_near_swap_BYTES']==46 and
         details['original_far_public_BYTES']==44 and
         details['far_public_literal_bytes_equal']==42 and
         details['unresolved_symbolic_near_CALL_BYTES']==2 and
         details['near_core_remaining_BYTES']==666 and
         details['original_field_recovered_offsets']==[9,721,735,738] and
         details['source_near_call_target_OFFSET']==46,
         'bounded ninety-byte source structure and original undecoded core')
    return dict(complete=True,complete_qsort=False,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                original_qsort_CODE_bytes=756,original_qsort_native_fields=29,
                original_live_BSS_bytes=6,
                helper_literal_CODE_bytes=46,public_wrapper_CODE_bytes=44,
                wrapper_literal_equal_bytes=42,
                symbolic_original_near_CALL_bytes=2,
                original_core_not_reconstructed_bytes=666,
                native_BSS_fixup_count_recovered=4,
                original_fixup_sites=[9,721,735,738],
                original_near_call_target=46,
                two_actual_TASM_rounds_equal=True,
                original_source_names=producer.SOURCES,
                original_full_qsort_object_sha256=sha(original),
                selected_build_report_sha256=sha(report_raw),
                only_bounded_codegen_claimed=True)


if __name__=='__main__':
    r=review()
    (ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
