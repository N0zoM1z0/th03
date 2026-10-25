#!/usr/bin/env python3
"""Review all five complete MAINL CDG procedures against the live cold pair."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import review_th03_mainl_pi_work as pi
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_cdg_layout import SOURCE, verify as layout
from lib.decoded_mainl_cdg_runtime import Machine, verify as runtime, negative_controls

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'.analysis/work/mainl-cdg-build.json'
INPUTS = (*pi.INPUTS,'scripts/review_th03_mainl_cdg_work.py','scripts/lib/decoded_mainl_cdg_layout.py',
          'scripts/lib/decoded_mainl_cdg_runtime.py',SOURCE)
COUNTS = dict(single=1167,single_noalpha=1164,all=607,all_noalpha=134,free=592)


def need(value,message):
    if not value:
        raise ValueError('MAINL CDG review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name:sha((root/name).read_bytes()) for name in INPUTS}


def witness(scope):
    r = scope['runtime']
    need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'],r['ignored_stack_bytes'])
         ==(2,5,593,593,7328,0),'complete five-function and full-memory dimensions')
    maxima = dict(alloc=510,free=510,open=1,read=511,seek=255,close=1)
    need([(o['load_segment'],o['cases'],o['cases_by_function'],o['executed_owner_bytes'],o['maximum_stack_depth'],
           o['maximum_native_free_entries'],o['maximum_interface_calls']) for o in r['observations']]
         ==[(0x1000,3664,COUNTS,593,38,255,maxima),(0x3000,3664,COUNTS,593,38,255,maxima)]
         and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) and o['checked_far_frames']>100000 for o in r['observations']),
         'all native nested helpers / complete BYTE domains / literal physical frames')
    need((r['exhaustive_image_count_BYTE'],r['exhaustive_flag_BYTE'],r['exhaustive_size_and_signed_index_BYTE_lanes'])==(256,256,256)
         and r['far_return_words_checked_at_entry'] and r['actual_owned_nested_helpers']
         and not r['physical_DOS_or_heap_executed'],'bounded file and heap interfaces; no native helper stub')
    l = scope['layout']
    need((l['functions'],l['code_bytes'],len(l['ordered_native_fields']),l['mz_relocation_count'],l['normal_tlink_relaxed_calls'],l['compiler_backward_bridge_calls'])
         ==(5,593,35,24,4,1) and not l['enclosing_DATA_or_interfaces_accepted'] and not l['whole_product_accepted'],
         'whole TU, literal ordered fields and natural compiler/linker bridges')
    c = scope['negative_controls']
    need(c['count']==len(set(c['rejected']))==66 and c['actual_guest_instruction_mutations'] and not c['alignment_mutations_counted'],
         'sixty-six actual instruction mutations')


def smoke(target,candidate):
    rows = []
    for image in (target,candidate):
        machine = Machine(image,0x3000)
        try:
            rows.append([machine.run(k,**p) for k,p in (
                ('single',dict(size=0x3334,n=0xFFFF,allocations=(0,0x5000))),
                ('single_noalpha',dict(size=0xFFFF,n=0x8000,read_limits=(16,0,3),flags=0xED7)),
                ('free',dict(slot=0xFFFF,old_segments=(0,0x8000),ss=0x8000,stack=0x80)),
                ('all',dict(count=3,noalpha=0x80)),('all_noalpha',dict(slot=0xEB8,bottom=0,count=2,noalpha=0xFF)))])
        finally:
            machine.close()
    need(rows[0]==rows[1],'current independent CDG arithmetic / alias / zero-allocation smoke')
    return dict(images=2,cases_per_image=5,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw = (root/'.analysis/work/mainl-cdg-build.json').read_bytes()
    report = json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-cdg-current-review-v1','complete CDG report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),'current implementation / source / cold binding')
    need(report['pi_review_sha256']==sha(pi.REPORT.read_bytes()),'current prerequisite PI proof')
    scope = report['scope']
    need(scope['layout']==layout(work,target,candidate,graph,files),'complete current native CDG ownership')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate the complete unchanged cold pair; rerun all new CDG gates')
    options = parser.parse_args()
    report = dict(schema='th03-mainl-cdg-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
                  provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
                  whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    def save():
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_pi_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files = sound.images(ROOT)
    pi.current_scope(ROOT,work,target,candidate,raw,graph,files)
    report.update(cold_report_sha256=sha(raw),pi_review_sha256=sha(pi.REPORT.read_bytes()),
                  source_inventory_sha256=sound.digest(cold['source_sha256']))
    report['scope'] = dict(layout=layout(work,target,candidate,graph,files),runtime=runtime(target,candidate),
                           negative_controls=negative_controls(target))
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'CDG inputs changed during execution')
    report['complete'] = True
    save()
    print('MAINL CDG: five complete functions / 593 CODE bytes; native ownership, nested instructions and full-state contracts pass')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
