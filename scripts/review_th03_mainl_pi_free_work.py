#!/usr/bin/env python3
"""Review the complete MAINL PI release against the current native cold pair."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import review_th03_mainl_root_helpers_work as helpers
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_pi_free_layout import SOURCE, verify as layout
from lib.decoded_mainl_pi_free_runtime import Machine, verify as runtime, negative_controls

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / '.analysis/work/mainl-pi-free-build.json'
INPUTS = (*helpers.INPUTS, 'scripts/review_th03_mainl_pi_free_work.py',
          'scripts/lib/decoded_mainl_pi_free_layout.py', 'scripts/lib/decoded_mainl_pi_free_runtime.py',
          'scripts/lib/decoded_mainl_root_helpers_runtime.py', SOURCE, 'src/mainl/memory/heap.inl')


def need(value, message):
    if not value:
        raise ValueError('MAINL PI free review: ' + message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name: sha((root / name).read_bytes()) for name in INPUTS}


def witness(scope):
    r = scope['runtime']
    need((r['images'], r['functions'], r['code_bytes'], r['executed_owner_bytes'],
          r['cases_per_image'], r['exhaustive_segment_byte_lanes'], r['ignored_stack_bytes'])
         == (2, 1, 76, 76, 5558, 256, 0), 'complete release / WORD lane / physical memory dimensions')
    need([(o['load_segment'], o['cases'], o['executed_owner_bytes'], o['heap_call_counts'], o['maximum_owner_stack_depth'])
          for o in r['observations']] == [(0x1000, 2779, 76, [0, 1, 2, 3], 8), (0x3000, 2779, 76, [0, 1, 2, 3], 8)]
         and all(re.fullmatch(r'[0-9a-f]{64}', o['trace_sha256']) for o in r['observations']),
         'both loads, all native paths and exact caller/callee frames')
    need(not r['heap_body_executed'] and not r['physical_allocator_proved'], 'bounded unowned allocator interface')
    c = scope['negative_controls']
    need(c['count'] == len(set(c['rejected'])) == 20 and c['actual_guest_instruction_mutations']
         and not c['nop_mutations_counted'], 'twenty real instruction mutations')
    l = scope['layout']
    need(l['functions'] == 1 and l['code_bytes'] == 76 and l['ordered_native_fields'] == l['ordered_relocations'] == []
         and l['native_nopcall_sites'] == [0xFFD, 0x1016, 0x102F]
         and not l['containing_producer_accepted'] and not l['heap_body_accepted'] and not l['whole_product_accepted'],
         'complete root owner, native macro calls and excluded context')


def smoke(target, candidate):
    rows = []
    for image in (target, candidate):
        machine = Machine(image, 0x3000)
        try:
            rows.append([machine.run(**p) for p in (
                {}, dict(segments=(0, 0, 0)), dict(segments=(0x100, 0x8000, 0xFFFF), flags=0xED7),
                dict(header_offset=0xFFFF, foreign_ds=True, ss=0x8000, stack=0x80),
                dict(alias_frame=True), dict(replies=((0xFFFF, 0x895),) * 3))])
        finally:
            machine.close()
    need(rows[0] == rows[1], 'current independent release / alias / stack smoke')
    return dict(images=2, cases_per_image=6, trace_sha256=sha(json.dumps(rows[0], sort_keys=True).encode()),
                full_runtime_reexecuted_now=False, full_runtime_witness_bound=True)


def current_scope(root, work, target, candidate, cold_raw, graph, files):
    raw = (root / '.analysis/work/mainl-pi-free-build.json').read_bytes()
    report = json.loads(raw)
    need(report['complete'] and report['schema'] == 'th03-mainl-pi-free-current-review-v1', 'complete release review')
    need(report['implementation_sha256'] == inputs(root) and report['cold_report_sha256'] == sha(cold_raw),
         'current source / implementation / cold binding')
    need(report['root_helpers_review_sha256'] == sha(helpers.REPORT.read_bytes()), 'current prerequisite review')
    scope = report['scope']
    need(scope['layout'] == layout(work, target, candidate, graph, files), 'current complete native release ownership')
    witness(scope)
    return dict(**scope, review_sha256=sha(raw), current_smoke=smoke(target, candidate))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold', action='store_true', help='revalidate the entire unchanged cold pair; rerun release gates')
    options = parser.parse_args()
    report = dict(schema='th03-mainl-pi-free-current-review-v1', complete=False, implementation_sha256=inputs(ROOT),
                  provenance='candidate-local-attested', native_pair_built_now=not options.current_cold,
                  whole_product_accepted=False, canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    def save():
        REPORT.write_text(json.dumps(report, indent=2) + '\n')

    save()
    if not options.current_cold:
        subprocess.run([sys.executable, str(ROOT / 'scripts/review_th03_mainl_root_helpers_work.py')], cwd=ROOT, check=True)
    work, target, candidate, cold, raw, graph, files = sound.images(ROOT)
    sound.current_scope(ROOT, work, target, candidate, raw, graph, files)
    helpers.current_scope(ROOT, work, target, candidate, raw, graph, files)
    report.update(cold_report_sha256=sha(raw), root_helpers_review_sha256=sha(helpers.REPORT.read_bytes()),
                  source_inventory_sha256=sound.digest(cold['source_sha256']))
    report['scope'] = dict(layout=layout(work, target, candidate, graph, files), runtime=runtime(target, candidate),
                           negative_controls=negative_controls(target))
    witness(report['scope'])
    need(report['implementation_sha256'] == inputs(ROOT), 'release inputs changed during execution')
    report['complete'] = True
    save()
    print('MAINL PI release: one complete function / 76 CODE bytes; native ownership, frames and bounded heap contracts pass')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
