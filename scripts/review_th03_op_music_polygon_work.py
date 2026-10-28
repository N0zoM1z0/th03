#!/usr/bin/env python3
"""Revalidate the unchanged OP cold graph and execute the whole polygon pair.

This is a diagnostic observation, separate from the source-acceptance ledger.
It deliberately never launches an ancestor or whole-product cold replay.
"""
import argparse
import hashlib
import json
from pathlib import Path

from review_th03_op_cfg_work import images
import review_th03_op_music_state_work as previous
from lib.op_startup_cold import verify as cold_graph
from lib.op_music_polygon import Machine, layout, verify as runtime, negative_controls

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'config/op_music_polygon_work/observation.json'
INPUTS = tuple(sorted(set((*previous.INPUTS, 'scripts/lib/op_music_polygon.py',
    'scripts/review_th03_op_music_polygon_work.py', 'scripts/lib/op_startup_state.py',
    'scripts/lib/op_cfg_runtime.py', 'tests/test_op_music_polygon_current.py'))))


def need(value, message):
    if not value:
        raise ValueError('OP Music polygon review: ' + str(message))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name: sha((root / name).read_bytes()) for name in INPUTS}


def witness(report):
    need(report['schema'] == 'th03-op-music-polygon-diagnostic-v1' and report['complete'], 'complete observation')
    need(report['provenance'] == 'candidate-local-attested' and not report['native_pair_rebuilt'], 'unchanged pinned cold graph')
    need(not report['source_ownership_promoted'] and not report['whole_product_accepted'], 'diagnostic scope only')
    l, r, c = report['layout'], report['runtime'], report['negative_controls']
    need((l['code_bytes'], l['procedures'], l['instruction_count'], len(l['native_fields']), len(l['ordered_relocations'])) ==
         (645, 2, 219, 54, 14), 'complete two-procedure native geometry')
    need(r['images'] == 2 and len(r['observations']) == 2 and r['ignored_stack_bytes'] == 0, 'both images/two loads/full stack')
    for row, load in zip(r['observations'], (0x1000, 0x3000), strict=True):
        need((row['load_segment'], row['cases'], row['executed_code_bytes'], row['executed_context_bytes'],
              row['consecutive_frames'], row['maximum_stack_depth']) == (load, 571, 645, 68, 3, 40), 'complete load/context/frame witness')
        need(row['complete_returns'] == dict(build=304, update=267), 'all full procedure returns')
        need(len(row['trace_sha256']) == 64, 'complete trace digest')
    need(r['actual_random_and_polar'] and not r['synthetic_owned_returns'] and r['renderer_is_bounded_reply'], 'actual context and explicit renderer')
    need(not r['physical_pixels_or_timing_proved'] and not r['source_ownership_promoted'] and not r['whole_product_accepted'], 'bounded claims')
    need(c['actual_instruction_mutations'] == len(set(c['rejected'])) == 46 and
         c['verifier_implementation_exceptions_are_not_rejections'], 'all real-instruction controls reject')


def smoke(target, candidate):
    observations = []
    for image in (target, candidate):
        rows = []
        for load in (0x1000, 0x3000):
            m = Machine(image, load)
            try:
                rows.append(m.run('build', count=129, angle=0xFFFF, radius=-32768, center_y=0x7FFF))
                rows.append(m.run('update', initialized=0, seed=1, flags=0xED7))
                rows.append(m.run('update', reenter=True, seed=1, flags=0xED7))
            finally:
                m.close()
        observations.append(rows)
    need(observations[0] == observations[1], 'current two-load reentry smoke')
    return dict(images=2, cases_per_image=6, trace_sha256=sha(json.dumps(observations[0], sort_keys=True).encode()))


def check(root=ROOT):
    report = json.loads((root / REPORT.relative_to(ROOT)).read_bytes())
    witness(report)
    work, target, candidate, cold, cold_raw = images(root)
    need(report['implementation_sha256'] == inputs(root), 'all current implementation bindings')
    need(report['cold_report_sha256'] == sha(cold_raw), 'current cold report')
    need(report['cold_validation'] == cold_graph(root, work, target, candidate, cold), 'entire current native graph')
    need(report['dependencies'] == previous.dependencies(root, work, cold), 'complete producer/SDK dependencies')
    need(report['sdk_before'] == report['sdk_after'] == previous.sdk_inventory(root), 'before/after/current SDK')
    need(report['layout'] == layout(root, work, target, candidate), 'current native layout')
    need(report['accepted_scope_sha256'] == sha((root / 'config/op_work/scoped_acceptance.json').read_bytes()), 'unchanged acceptance publication')
    return smoke(target, candidate)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='revalidate bound complete evidence and execute a current smoke')
    options = parser.parse_args()
    if options.check:
        print(json.dumps(check(), indent=2))
        return 0
    work, target, candidate, cold, cold_raw = images(ROOT)
    report = dict(schema='th03-op-music-polygon-diagnostic-v1', complete=False,
                  provenance='candidate-local-attested', native_pair_rebuilt=False,
                  source_ownership_promoted=False, whole_product_accepted=False,
                  implementation_sha256=inputs(ROOT), cold_report_sha256=sha(cold_raw),
                  accepted_scope_sha256=sha((ROOT / 'config/op_work/scoped_acceptance.json').read_bytes()),
                  cold_validation=cold_graph(ROOT, work, target, candidate, cold),
                  dependencies=previous.dependencies(ROOT, work, cold), sdk_before=previous.sdk_inventory(ROOT))
    report['layout'] = layout(ROOT, work, target, candidate)
    report['runtime'] = runtime(target, candidate)
    report['negative_controls'] = negative_controls(target)
    report['sdk_after'] = previous.sdk_inventory(ROOT)
    need(report['implementation_sha256'] == inputs(ROOT) and report['sdk_before'] == report['sdk_after'], 'unchanged inputs during review')
    need(report['accepted_scope_sha256'] == sha((ROOT / 'config/op_work/scoped_acceptance.json').read_bytes()), 'acceptance unchanged during review')
    report['complete'] = True
    witness(report)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print('OP polygon pair: 645 CODE bytes / 2 full procedures; 2284 executions; 46 instruction controls PASS; diagnostic only', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
