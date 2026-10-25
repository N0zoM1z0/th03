#!/usr/bin/env python3
"""Review MAINL's complete natural ending entry and actual accepted callees."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import review_th03_mainl_cdg_draw_work as draw
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_ending_layout import SOURCE, verify as layout
from lib.decoded_mainl_ending_runtime import Machine, verify as runtime, negative_controls

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'.analysis/work/mainl-ending-build.json'
INPUTS = (*draw.INPUTS,'scripts/review_th03_mainl_ending_work.py','scripts/lib/decoded_mainl_ending_layout.py',
          'scripts/lib/decoded_mainl_ending_runtime.py',SOURCE)


def need(value,message):
    if not value:
        raise ValueError('MAINL ending review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name:sha((root/name).read_bytes()) for name in INPUTS}


def witness(scope):
    r,l,c = scope['runtime'],scope['layout'],scope['negative_controls']
    need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'],r['ignored_stack_bytes'])
         ==(2,1,280,280,9528,0),'complete ending and physical-memory dimensions')
    need([(o['load_segment'],o['cases'],o['executed_owner_bytes'],o['actual_helper_bytes'],o['maximum_stack_depth'])
          for o in r['observations']]==[(0x1000,4764,280,227,24),(0x3000,4764,280,227,24)]
         and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) and 0<o['bonus_entries']<o['cases']
                 and o['byte_port_requests']>o['cases']*6 and o['counter_polls']>o['cases'] for o in r['observations']),
         'all native helper bytes, full branch matrix and progressing counters')
    need(r['actual_owned_nested_helpers'] and r['actual_helper_bytes']==227 and r['complete_near_return']
         and r['flat_memory_operand_contract'] and not r['interface_bodies_or_assets_owned']
         and not r['physical_IRQ_graphics_exec_proved'],'explicit interface and hardware boundary')
    need((l['functions'],l['code_bytes'],len(l['ordered_native_fields']),l['mz_relocation_count'],l['near_external_fields'],l['own_DATA_fields'])
         ==(1,280,34,14,7,4),'complete raw / ordered native and MZ owner fields')
    need((l['enclosing_CODE_bytes'],l['enclosing_initialized_DATA_bytes'],l['enclosing_BSS_bytes'],l['enclosing_procedures'])
         ==(3695,224,0,19) and not l['enclosing_DATA_or_other_functions_accepted']
         and not l['physical_runtime_or_assets_accepted'] and not l['whole_product_accepted'],'separate enclosing TU ownership')
    need(c['count']==len(set(c['rejected']))==39 and (c['owner_instruction_mutations'],c['actual_helper_instruction_mutations'])==(35,4)
         and c['actual_guest_mutations'],'actual ending and nested helper instruction controls')


def smoke(target,candidate):
    rows = []
    for image in (target,candidate):
        m = Machine(image,0x3000)
        try:
            rows.append([m.run(**p) for p in (dict(character=0,credits=255,segments=(0,0,0),cdg_segments=(0,0)),
                dict(character=255,script=(0xFFFF,0x6000),digits=(255,255),flags=0xED7,ss=0x8000,stack=0x80),
                dict(character=255,credits=0,writes=(('regist',1,0x5008C,b'\x0E'),('regist',1,0x500B6,b'\x03'))))])
        finally:
            m.close()
    need(rows[0]==rows[1],'current independent full-state nested smoke')
    return dict(images=2,cases_per_image=3,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw = (root/'.analysis/work/mainl-ending-build.json').read_bytes()
    report = json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-ending-current-review-v1','complete ending report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),
         'current maintained source / implementation / cold binding')
    need(report['draw_review_sha256']==sha(draw.REPORT.read_bytes()),'current prerequisite drawing proof')
    scope = report['scope']
    need(scope['layout']==layout(work,target,candidate,graph,files),'current full owner bytes / native producer ownership')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate the unchanged complete cold pair; rerun ending gates')
    options = parser.parse_args()
    report = dict(schema='th03-mainl-ending-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
                  provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
                  whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    def save():
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_cdg_draw_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files = sound.images(ROOT)
    draw.current_scope(ROOT,work,target,candidate,raw,graph,files)
    report.update(cold_report_sha256=sha(raw),draw_review_sha256=sha(draw.REPORT.read_bytes()),
                  source_inventory_sha256=sound.digest(cold['source_sha256']))
    report['scope'] = dict(layout=layout(work,target,candidate,graph,files),runtime=runtime(target,candidate),
                           negative_controls=negative_controls(target))
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'ending inputs changed during execution')
    report['complete'] = True
    save()
    print('MAINL ending: complete280 CODE bytes,34 native fields/14 MZ relocations; actual227 helper bytes and full-state contracts pass')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
