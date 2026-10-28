#!/usr/bin/env python3
"""Bind and execute every remaining Music Room dependency before the menu."""
import argparse
import hashlib
import json
from pathlib import Path

from review_th03_op_cfg_work import images
import review_th03_op_music_state_work as state_review
import review_th03_op_music_polygon_work as polygon_review
from lib.op_startup_cold import verify as cold_graph
from lib.op_music_comment import Machine, ENTRIES, layout, verify as runtime, negative_controls

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'config/op_music_comment_work/observation.json'
INPUTS = tuple(sorted(set((*polygon_review.INPUTS, 'scripts/lib/op_music_comment.py',
    'scripts/review_th03_op_music_comment_work.py', 'tests/test_op_music_comment_current.py'))))


def need(value, message):
    if not value:
        raise ValueError('OP Music comment review: ' + str(message))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name: sha((root / name).read_bytes()) for name in INPUTS}


def prior_binding(root, cold_raw):
    raw = (root / polygon_review.REPORT.relative_to(ROOT)).read_bytes()
    report = json.loads(raw)
    polygon_review.witness(report)
    need(report['implementation_sha256'] == polygon_review.inputs(root), 'complete current prior polygon implementation')
    need(report['cold_report_sha256'] == sha(cold_raw), 'same complete cold graph as polygon witness')
    return sha(raw)


def witness(report):
    need(report['schema'] == 'th03-op-music-comment-diagnostic-v1' and report['complete'], 'complete diagnostic')
    need(report['provenance'] == 'candidate-local-attested' and not report['native_pair_rebuilt'], 'unchanged Japanese/native identities')
    need(not report['source_ownership_promoted'] and not report['whole_product_accepted'], 'no widened acceptance')
    l, r, c = report['layout'], report['runtime'], report['negative_controls']
    need((l['procedures'], l['code_bytes'], l['instruction_count'], len(l['native_fields']), len(l['ordered_relocations'])) ==
         (7, 907, 315, 63, 14), 'whole seven-procedure native partition')
    need(r['images'] == 2 and r['procedures'] == 7 and r['code_bytes'] == 907 and r['ignored_stack_bytes'] == 0, 'two actual images/full stack')
    need(len(r['observations']) == 2, 'two loads')
    for row, load in zip(r['observations'], (0x1000, 0x3000), strict=True):
        need((row['load_segment'], row['cases'], row['helper_bytes'], row['maximum_stack_depth'],
              row['consecutive_dependency_calls']) == (load, 421, 907, 44, 5), 'full native/load/caller chain')
        need(row['complete_returns'] == dict(put=18, flip=27, bg_snap=18, load=299, bg_free=9, unput=17, comment=33), 'all full returns')
        need(len(row['trace_sha256']) == 64, 'complete observation digest')
    need(r['actual_nested_helpers_and_delay'] and not r['synthetic_owned_returns'], 'execute actual helpers/owned delay')
    need((r['explicit_copy_DWORDs_per_plane'], r['explicit_recapture_DWORDs'], r['REP_copy_WORDs']) == (3200, 8000, 16000), 'complete native copies')
    need(r['unchecked_allocation_failure'] and r['live_aliasing'] and r['WORD_pointer_wrap'], 'unsanitized native behavior')
    need(not r['physical_pixels_files_heap_or_frame_time_proved'] and not r['source_ownership_promoted'] and not r['whole_product_accepted'], 'bounded interfaces only')
    need(c['actual_instruction_mutations'] == len(set(c['rejected'])) == 65 and
         c['prediction_constructor_and_unexpected_hook_exceptions_are_fatal'], 'all real controls/fatal verifier errors')


def smoke(target, candidate):
    observations = []
    for image in (target, candidate):
        rows = []
        for load in (0x1000, 0x3000):
            m = Machine(image, load)
            try:
                rows.append(m.run('bg_snap', allocated=(0, 0x5400, 0x5800, 0x5C00), source_offset=65535))
                rows.append(m.run('comment', reenter=True, track=40, read_bytes=39, flags=0xED7))
                rows.append(m.run('flip', reenter=True, ticks=(0, 0x8000), flags=0xED7))
                rows.append(m.run('bg_free', reenter=True, free_reload=True))
            finally:
                m.close()
        observations.append(rows)
    need(observations[0] == observations[1], 'complete current two-load target/candidate dependency chain')
    return dict(images=2, cases_per_image=8, trace_sha256=sha(json.dumps(observations[0], sort_keys=True).encode()))


def check(root=ROOT):
    report = json.loads((root / REPORT.relative_to(ROOT)).read_bytes())
    witness(report)
    work, target, candidate, cold, cold_raw = images(root)
    need(report['implementation_sha256'] == inputs(root), 'all current implementation bindings')
    need(report['cold_report_sha256'] == sha(cold_raw), 'current cold report')
    need(report['polygon_observation_sha256'] == prior_binding(root, cold_raw), 'complete prior context witness binding')
    need(report['cold_validation'] == cold_graph(root, work, target, candidate, cold), 'entire current native graph')
    need(report['dependencies'] == state_review.dependencies(root, work, cold), 'complete producer/SDK/source dependencies')
    need(report['sdk_before'] == report['sdk_after'] == state_review.sdk_inventory(root), 'before/after/current SDK')
    need(report['layout'] == layout(root, work, target, candidate), 'current native helper bytes and ordered relocations')
    need(report['accepted_scope_sha256'] == sha((root / 'config/op_work/scoped_acceptance.json').read_bytes()), 'unchanged accepted publication')
    return smoke(target, candidate)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='revalidate full graph/evidence and execute a current dependency chain')
    options = parser.parse_args()
    if options.check:
        print(json.dumps(check(), indent=2))
        return 0
    work, target, candidate, cold, cold_raw = images(ROOT)
    report = dict(schema='th03-op-music-comment-diagnostic-v1', complete=False,
                  provenance='candidate-local-attested', native_pair_rebuilt=False,
                  source_ownership_promoted=False, whole_product_accepted=False,
                  implementation_sha256=inputs(ROOT), cold_report_sha256=sha(cold_raw),
                  polygon_observation_sha256=prior_binding(ROOT, cold_raw),
                  accepted_scope_sha256=sha((ROOT / 'config/op_work/scoped_acceptance.json').read_bytes()),
                  cold_validation=cold_graph(ROOT, work, target, candidate, cold),
                  dependencies=state_review.dependencies(ROOT, work, cold), sdk_before=state_review.sdk_inventory(ROOT))
    report['layout'] = layout(ROOT, work, target, candidate)
    report['runtime'] = runtime(target, candidate)
    report['negative_controls'] = negative_controls(target)
    report['sdk_after'] = state_review.sdk_inventory(ROOT)
    need(report['implementation_sha256'] == inputs(ROOT) and report['sdk_before'] == report['sdk_after'], 'unchanged implementation/SDK during review')
    need(report['accepted_scope_sha256'] == sha((ROOT / 'config/op_work/scoped_acceptance.json').read_bytes()), 'unchanged acceptance during review')
    report['complete'] = True
    witness(report)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print('OP Music dependencies: 907 CODE / 7 full procedures; 1684 executions; 65 native instruction controls PASS; diagnostic only', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
