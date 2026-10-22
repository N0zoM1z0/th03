#!/usr/bin/env python3
"""Guarded offline replay of five historical OP helper producers, not acceptance."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import types

PROPOSAL = '.analysis/op-remaining-helpers-native-proposal-v01'
OUTS = ('.analysis/op-remaining-helpers-native-g1-output-v01',
        '.analysis/op-remaining-helpers-native-g2-output-v01')
MANIFEST_SHAS = ('e63fd8c5ea5af70e46b627f90cc19c1a111727a6c99d1560dc77372039b70617',
                '046dd63f4b4a2857167c56607cd2c805befd3c074ba581b053a194f587e35236')
VERIFIER_SHA = '263b16e445919778250bfe964a9580e4bf43b2c25b93af7f243d155368c521b2'
HISTORICAL_HEAD = '6e895a923632a94323b6ecba6fd0237ac78cebc5'
EXE_SHA = '9f2e2af591645963d802489b45f9355a1e9f9b4da4b49ab0767f5be069ec204d'
PHASES = (['compile_snd_mode', 'compile_snd_pmdr', 'compile_polar',
           'compile_snd_kaja', 'compile_initop'], ['link'])
FLAGS = ('source_acceptance', 'exact_acceptance', 'whole_product_ownership',
         'cold_build', 'two_cold_builds', 'runtime_rerun', 'packing_run')
SOURCE_CLOSURE = {
    'src/op/snd/determine_mode.c', 'src/op/snd/pmd_resident.c',
    'src/op/math/polar.cpp', 'src/op/snd/kaja_interrupt.cpp', 'src/op/core/initop.cpp',
    'compat/rec98/x86real.h', 'compat/rec98/th02/snd/snd.h',
    'compat/rec98/th03/math/polar.hpp', 'compat/rec98/th04/snd/snd.h',
    'compat/rec98/th02/snd/impl.hpp', 'compat/rec98/libs/master.lib/master.hpp',
    'compat/rec98/libs/master.lib/pc98_gfx.hpp', 'compat/rec98/th01/hardware/vplanset.h',
    'compat/rec98/th03/core/initexit.h',
    'config/th03_op_remaining_helpers_candidate.json',
    'scripts/stage_th03_op_remaining_helpers.py',
    'scripts/replay_th03_op_remaining_helpers.py',
}
HELPER_CLOSURE = {
    'scripts/lib/__init__.py', 'scripts/lib/pc98.py', 'scripts/lib/omf.py',
    'scripts/lib/targets.py', 'scripts/review_th03_decoded_code.py',
    'scripts/inventory_rec98_th03.py', 'config/targets.toml',
}
EXTENTS = [('snd_determine_mode', 0x4a, 29), ('snd_pmd_resident', 0x68, 57),
           ('polar', 0x155, 26), ('snd_kaja_interrupt', 0x553, 30),
           ('game_init_op', 0x571, 105)]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(ok, message):
    if not ok:
        raise ValueError(message)


def regular(root, name):
    p = Path(name)
    need(not p.is_absolute() and '..' not in p.parts and str(p) == name,
         'unsafe input path')
    p = Path(root) / p
    need(not any(x.is_symlink() for x in (p, *p.parents)) and p.is_file(),
         'regular input ' + name)
    return p


def values(raw):
    return dict(sha256=sha(raw), bytes=len(raw))


def validate_proof(p):
    need(p['schema'] == 'th03-op-remaining-helpers-proof-v1', 'schema')
    need(all(p[n] is False for n in FLAGS), 'credit inflation')
    need(tuple(p[n] for n in ('native_groups', 'native_phases', 'fresh_owner_objects',
         'new_owner_bytes', 'retained_context_objects', 'preserved_prior_owners',
         'preserved_prior_bytes', 'original_producer_context_bytes',
         'excluded_alignment_bytes')) == (2, 6, 5, 247, 22, 37, 12569, 2, 1),
         'bounded scope')
    need(p['manifest_sha256'] == list(MANIFEST_SHAS) and
         p['verifier_sha256'] == VERIFIER_SHA and p['historical_head'] == HISTORICAL_HEAD,
         'recipe identity')
    need(set(p['maintained_closure']) == SOURCE_CLOSURE and
         set(p['helper_closure']) == HELPER_CLOSURE, 'current source/helper closure')


def validate_phase(phase, start, finish, m, env):
    need(start['argv'] == m['native_argv'][phase], 'actual phase argv')
    need(Path(start['cwd']).parts[-len(Path(m['work']).parts):] == Path(m['work']).parts,
         'actual phase cwd')
    need(start['environment'] == env['environment'], 'phase environment')
    need(start['wait_seconds'] == 90 and start['cleanup_seconds'] == 15, 'phase bounds')
    need(len(env['cpu']) == 1 and env['nice'] >= 10, 'resource bounds')
    need(start['environment']['DISPLAY'] == start['environment']['WAYLAND_DISPLAY'] == ''
         and start['environment']['TZ'] == 'UTC', 'headless UTC')
    need(type(finish['exit_code']) is int and finish['exit_code'] == 0, 'phase exit')
    need(all(finish[n] is False for n in ('timeout', 'cleanup_uncertain', 'poison')),
         'unsafe cleanup')
    need(finish['initial_inventory_complete'] is True and finish['inventory_complete'] is True
         and finish['survivors'] == [] and finish['errors'] == [] and finish['ok'] is True,
         'owned cleanup inventory')
    need(len(finish['owned_leader']) == 5 and
         type(finish['owned_leader'][0]) is int and finish['owned_leader'][0] > 0,
         'exact owned process identity')


def validate_report(r):
    need(r['diagnostic_checks_pass'] is True and r['source_integrity_checked'] is True,
         'native diagnostics')
    need(all(r[n] is False for n in ('source_acceptance', 'exact_acceptance',
         'whole_product_ownership', 'cold_build', 'runtime_run')), 'diagnostic scope')
    need(r['native_invocations_now'] == 0 and r['new_helper_bytes'] == 247 and
         r['new_helper_all_raw_ordered_pass'] is True, 'new owner bytes')
    need([(x['name'], x['offset'], x['size']) for x in r['new_helpers']] == EXTENTS,
         'new owner extents')
    for x in r['new_helpers']:
        need(all(x[n] is True and x['full_producer'][n] is True for n in
             ('target_raw_equal', 'baseline_raw_equal', 'target_ordered_equal',
              'baseline_ordered_equal')), 'new owner comparisons')
        need(x['instructions']['full_decode'] is True and
             x['instructions']['return_abi_preserved'] is True, 'original return ABI')
    need(len(r['objects']) == 5 and len(r['retained_project_context']) ==
         r['retained_project_context_count'] == 22, 'fresh/retained object partition')
    need(all(x['maintained_lineage_checked'] is True and x['literal_non_comment_omf_equal']
         is True and x['stable_compiler_comments_equal'] is True for x in r['objects']),
         'fresh maintained OMF lineage')
    need((r['prior_owner_count'], r['prior_owner_bytes'], len(r['prior_owners'])) ==
         (37, 12569, 37) and r['prior_owners_preserved'] is True, 'prior owned scope')
    need(all(all(x[n] is True for n in ('baseline_raw_equal', 'baseline_ordered_equal',
         'map_preserved')) for x in r['prior_owners']), 'prior owner preservation')
    need(r['all_map_publics_preserved'] is True and r['all_map_code_contributions_preserved']
         is True and r['baseline_whole_program_and_order_preserved'] is True and
         r['whole_file_equal_baseline'] is True and r['candidate_sha256'] ==
         r['baseline_sha256'] == EXE_SHA, 'baseline identity')
    need(r['whole_program']['target_different_bytes'] == 6 and
         r['whole_ordered_relocations']['target_different_positions'] == 313 and
         r['whole_ordered_relocations']['target_equal'] is False and
         r['whole_file_equal_target'] is False and r['global_target_negatives_unchanged']
         is True, 'global target negatives')
    need(r['original_producer_context_bytes'] == 2 and r['excluded_alignment_bytes'] == 1
         and [(x['offset'], x['size'], x['raw_hex']) for x in r['unowned_context']] ==
         [(0x67, 1, '90'), (0xa1, 1, '90'), (0x16f, 1, '00')]
         and all(x['function_code_credit'] is False and
                 x['target_baseline_candidate_equal'] is True for x in r['unowned_context']),
         'unowned NOP/alignment context')


def guard_current(root, p, source_root, m):
    # Exhaustive guards run before executing ANY repository Python.
    for n, q in p['helper_closure'].items():
        need(q == {k: m['sources'][n][k] for k in ('sha256', 'bytes')} and
             values(regular(root, n).read_bytes()) == q, 'current helper before import ' + n)
    for n, q in p['maintained_closure'].items():
        need(values(regular(source_root, n).read_bytes()) == q,
             'current maintained source/helper ' + n)
    expected = {n for n in m['repeat_inputs'] if n.startswith(('src/', 'compat/'))
                and n in m['sources']} - SOURCE_CLOSURE
    need(set(p['context_source_closure']) == expected, 'current retained source closure')
    for n, q in p['context_source_closure'].items():
        need(q == {k: m['sources'][n][k] for k in ('sha256', 'bytes')} ==
             {k: m['repeat_inputs'][n][k] for k in ('sha256', 'bytes')} and
             values(regular(root, n).read_bytes()) == q, 'current retained source ' + n)


def guard_pin_closure(pins, manifests, read):
    """Prove required retained paths are present, not merely hash a supplied subset."""
    required = set(HELPER_CLOSURE)
    def collect(value):
        if isinstance(value, dict):
            if {'path', 'sha256', 'bytes'} <= set(value):
                required.add(value['path'])
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)
    for i, m in enumerate(manifests):
        # The native sources map is a historical whole-tree audit snapshot, not
        # a requirement that unrelated installed docs/ledger/HEAD remain frozen.
        collect({k: v for k, v in m.items() if k != 'sources'})
        required |= {m['work'] + '/' + n for n in m['repeat_inputs']}
        required |= {m['work'] + '/' + n for n in m['all_native_outputs']}
        required.add(m['work'] + '/obj/th03/op.map')
        out = OUTS[i]
        required |= {out + '/' + n for n in ('manifest.json', 'environment.json',
            'completion.json', 'materialized-inputs.json', 'source-mtimes.json',
            'accumulated-objects.json', 'next-registry-baseline.json')}
        for phase in PHASES[i]:
            required |= {out + '/' + phase + suffix for suffix in
                ('-started.json', '-finished.json', '-registry-transition.json',
                 '-before-registry.json', '-after-registry.json', '-output.json',
                 '-before-user.reg', '-before-system.reg', '-after-user.reg',
                 '-after-system.reg', '.log')}
    required |= {OUTS[1] + '/linked-verification.json', OUTS[1] + '/link-map-output.json'}
    required |= {'.analysis/op-remaining-helpers-source-proposal-v01/payload/' + n
                 for n in SOURCE_CLOSURE if n != 'scripts/replay_th03_op_remaining_helpers.py'}
    m = manifests[1]
    cfg = json.loads(read(m['helper_config']['path']))
    baseline = Path(m['baseline_exe']['path']).parents[2]
    required |= {str(baseline / u[k]) for u in cfg['units'] for k in ('wrapper', 'original_body')}
    required |= set(json.loads(read(m['target_boundary_report']['path']))['inputs'])
    required.add('.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar')
    need(required <= set(pins), 'missing required retained pin')
    for name in required:
        read(name)

def replay(root, p, source_root=None):
    root = Path(root).resolve()
    source_root = Path(source_root or root).resolve()
    validate_proof(p)
    q = p['inventory']
    raw = regular(root, q['path']).read_bytes()
    need(values(raw) == {k: q[k] for k in ('sha256', 'bytes')}, 'inventory identity')
    inv = json.loads(raw)
    need(inv['metadata'] == {k: v for k, v in p.items() if k != 'inventory'},
         'inventory metadata')
    rows = inv['pins']
    need(len(rows) == len({x['path'] for x in rows}), 'duplicate inventory pins')
    pins = {x['path']: x for x in rows}
    need(inv['inputs'] == {n: {k: q[k] for k in ('sha256', 'bytes')}
                          for n, q in pins.items()}, 'cleanup retention mirror')

    def read(n):
        need(n in pins, 'unbound ' + n)
        b = regular(root, n).read_bytes()
        need(values(b) == {k: pins[n][k] for k in ('sha256', 'bytes')}, 'input drift ' + n)
        return b

    def js(n):
        return json.loads(read(n))

    for n in pins:
        read(n)
    manifests = []
    for i, out in enumerate(OUTS):
        name = PROPOSAL + '/group%d/manifest.json' % (i + 1)
        raw = read(name)
        need(sha(raw) == MANIFEST_SHAS[i] and raw == read(out + '/manifest.json'),
             'consumed native recipe')
        m = json.loads(raw)
        # Historical execution identity only; installed HEAD may legitimately advance.
        need(m['head'] == HISTORICAL_HEAD and m['group'] == i + 1 and m['round'] == 1
             and m['phases'] == PHASES[i], 'historical receipt identity')
        for row in m['inputs']:
            need(values(read(row['path'])) == {k: row[k] for k in ('sha256', 'bytes')},
                 'manifest consumed input')
        for row in m['toolchain_inputs']:
            need(values(read(row['path'])) == {k: row[k] for k in ('sha256', 'bytes')},
                 'toolchain identity')
        for n, stamp in m['fixed_mtimes'].items():
            read(n)
            need(regular(root, n).stat().st_mtime_ns == stamp, 'toolchain mtime')
        manifests.append(m)
    first, m = manifests
    need(first['work'] == m['work'] and Path(m['work']).name == 'OPRH101',
         'actual consumed carrier')
    for key in ('repeat_inputs', 'retained_objects', 'new_owner_objects', 'all_native_argv',
                'all_native_outputs', 'helper_config', 'verifier'):
        need(first[key] == m[key], 'cross-group recipe continuity ' + key)
    need(not first['compose_sources'] and not m['compose_sources'] and first['predecessor']
         is None and first['accumulated_objects'] == {} and not first['verify_after_group']
         and m['verify_after_group'] is True, 'fresh owner groups')
    need(len(m['retained_objects']) == 22 and len(m['new_owner_objects']) == 5 and
         not set(m['retained_objects']) & set(m['new_owner_objects']), 'producer partition')
    need(set(m['retained_objects']) == {n for n in m['repeat_inputs'] if
         Path(n).suffix.lower() in ('.obj', '.exe', '.map', '.lib', '.com')},
         'only declared retained binaries')
    guard_pin_closure(pins, manifests, read)
    guard_current(root, p, source_root, m)

    def load(name, path, body=None, base=root):
        raw = read(path) if body is None else body
        mod = types.ModuleType(name)
        mod.__file__ = str(base / path)
        sys.modules[name] = mod
        exec(compile(raw, mod.__file__, 'exec'), mod.__dict__)
        return mod

    sys.dont_write_bytecode = True
    stagepath = 'scripts/stage_th03_op_remaining_helpers.py'
    stage = load('op_remaining_maintained_stage', stagepath,
                 regular(source_root, stagepath).read_bytes(), source_root)
    cfg, data = stage.read_inputs(source_root)
    need(set(data) == SOURCE_CLOSURE - {'config/th03_op_remaining_helpers_candidate.json',
         stagepath, 'scripts/replay_th03_op_remaining_helpers.py'}, 'maintained body/compat closure')
    for n in SOURCE_CLOSURE - {'scripts/replay_th03_op_remaining_helpers.py'}:
        need(regular(source_root, n).read_bytes() ==
             read('.analysis/op-remaining-helpers-source-proposal-v01/payload/' + n),
             'historical-to-current maintained source ' + n)
    baseline_root = Path(m['baseline_exe']['path']).parents[2]
    for u in cfg['units']:
        for n, key in ((u['wrapper'], 'original_wrapper_sha256'),
                       (u['original_body'], 'original_body_sha256')):
            need(sha(read(str(baseline_root / n))) == u[key], 'original producer source ' + n)
    archive = '.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar'
    need(sha(read(archive)) == cfg['reference_archive_sha256'], 'original frozen reference archive')
    for n, digest in js(m['target_boundary_report']['path'])['inputs'].items():
        need(sha(read(n)) == digest, 'target boundary input ' + n)
    overlay = stage.payload(source_root)
    need(len(overlay) == 24, 'physical TU overlay size')
    for n, b in overlay.items():
        need(b == read(m['work'] + '/' + n), 'maintained-to-consumed source ' + n)
    previous_registry = None
    policy = load('op_remaining_registry_policy', m['registry_policy']['path'])
    for i, (out, manifest) in enumerate(zip(OUTS, manifests)):
        material = js(out + '/materialized-inputs.json')
        times = js(out + '/source-mtimes.json')
        need(set(material) == set(times) == set(manifest['repeat_inputs']), 'materialized closure')
        for n, q in manifest['repeat_inputs'].items():
            a, b = regular(root, q['path']), regular(root, m['work'] + '/' + n)
            need(read(q['path']) == read(m['work'] + '/' + n), 'snapshot to consumed ' + n)
            need((a.stat().st_dev, a.stat().st_ino) != (b.stat().st_dev, b.stat().st_ino)
                 and a.stat().st_mtime_ns == b.stat().st_mtime_ns == q['mtime_ns'] == times[n],
                 'source copy/mtime identity')
            need(material[n] == {k: q[k] for k in ('sha256', 'bytes', 'mode')},
                 'materialized metadata')
        if i == 1:
            need(manifest['materialized_inputs'] == material and
                 manifest['source_mtimes'] == times, 'cross-group materialized metadata')
            need(manifest['predecessor']['path'] == OUTS[0] + '/completion.json' and
                 values(read(manifest['predecessor']['path'])) ==
                 {k: manifest['predecessor'][k] for k in ('sha256', 'bytes')},
                 'group predecessor completion')
            need(manifest['accumulated_objects'] == js(OUTS[0] + '/accumulated-objects.json'),
                 'group accumulated owner lineage')
        environment = js(out + '/environment.json')
        registry = {n: q['sha256'] for n, q in manifest['registry_baseline'].items()}
        if previous_registry is not None:
            need(registry == previous_registry, 'cross-group registry continuity')
        for phase in PHASES[i]:
            a, z = js(out + '/' + phase + '-started.json'), js(out + '/' + phase + '-finished.json')
            tr = js(out + '/' + phase + '-registry-transition.json')
            validate_phase(phase, a, z, manifest, environment)
            need(Path(a['cwd']) == root / m['work'], 'absolute consumed cwd')
            before = {n: read(out + '/' + phase + '-before-' + n) for n in ('user.reg', 'system.reg')}
            after = {n: read(out + '/' + phase + '-after-' + n) for n in before}
            need({n: sha(b) for n, b in before.items()} == registry ==
                 js(out + '/' + phase + '-before-registry.json'), 'registry continuity')
            registry = {n: sha(b) for n, b in after.items()}
            need(registry == js(out + '/' + phase + '-after-registry.json'), 'registry after')
            actual = policy.validate_transition(before, after, phase_start_utc=a['started_utc'],
                        phase_end_utc=tr['phase_end_utc'], child_tz='UTC')
            need(json.loads(json.dumps(actual)) == tr and tr['ok'], 'registry policy')
            output = read(m['work'] + '/' + manifest['native_outputs'][phase])
            receipt = js(out + '/' + phase + '-output.json')
            need(values(output) == {k: receipt[k] for k in ('sha256', 'bytes')},
                 'actual phase output')
        previous_registry = registry
        need(registry == {n: q['sha256'] for n, q in
             js(out + '/next-registry-baseline.json').items()}, 'terminal registry')
        done = js(out + '/completion.json')
        need(done['complete'] is True and done['errors'] == [] and done['owned_lock_released']
             is True and done['native_invocations'] == len(PHASES[i]) and
             done['phases'] == PHASES[i] and done['group'] == i + 1 and done['round'] == 1
             and all(done[n] is False for n in ('runtime_run', 'source_acceptance',
                                              'exact_acceptance', 'full_historical_replay')),
             'completion')
        accumulated = js(out + '/accumulated-objects.json')
        need(set(accumulated) == set(m['new_owner_objects']) |
             ({'bin/th03/op.exe', 'obj/th03/op.map'} if i else set()), 'accumulated object scope')
        for n, q in accumulated.items():
            need(values(read(m['work'] + '/' + n)) == {k: q[k] for k in ('sha256', 'bytes')},
                 'accumulated fresh output')
    receipt = js(OUTS[1] + '/link-map-output.json')
    need(values(read(m['work'] + '/obj/th03/op.map')) ==
         {k: receipt[k] for k in ('sha256', 'bytes')}, 'actual linked MAP')
    need(sha(read(m['verifier']['path'])) == VERIFIER_SHA, 'native verifier identity')
    # Do not trust cached repository modules from a caller's earlier imports.
    for name in ('lib', 'lib.pc98', 'lib.omf', 'lib.targets',
                 'review_th03_decoded_code', 'inventory_rec98_th03'):
        sys.modules.pop(name, None)
    verifier = load('op_remaining_native_verifier', m['verifier']['path'])
    verifier.ROOT = root
    fresh = json.loads(json.dumps(verifier.verify(root / m['work'], m)))
    need(fresh == js(OUTS[1] + '/linked-verification.json'), 'fresh structural replay')
    validate_report(fresh)
    for obj in fresh['objects']:
        need(set(obj['required_dependencies']) <= set(obj['dependency_paths']),
             'actual maintained OMF source lineage')
        for dependency in obj['bound_source_dependencies']:
            n = dependency.get('physical_path', m['work'] + '/' + dependency['path'])
            need(sha(read(n)) == dependency['sha256'], 'actual OMF source dependency')
    return dict(schema=p['schema'], pass_checks=True, pinned_files=len(pins),
        current_helper_closure=len(HELPER_CLOSURE), maintained_closure=len(SOURCE_CLOSURE),
        current_retained_source_closure=len(p['context_source_closure']), source_binding=True,
        native_groups_replayed=2, native_phases_replayed=6, native_invocations_now=0,
        fresh_owner_objects=5, new_owner_bytes=247, retained_context_objects=22,
        preserved_prior_owners=37, preserved_prior_bytes=12569,
        original_producer_context_bytes=2, excluded_alignment_bytes=1,
        candidate_sha256=fresh['candidate_sha256'], whole_program_different_bytes=6,
        whole_ordered_relocations_equal=False, whole_file_equal_target=False,
        historical_head=HISTORICAL_HEAD, installed_head_requirement=False,
        **{n: False for n in FLAGS})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument('--source-root', type=Path)
    ap.add_argument('--proof', type=Path)
    ap.add_argument('--output', type=Path)
    a = ap.parse_args()
    p = json.loads((a.proof or a.repo_root / 'config/op_remaining_helpers/proof.json').read_text())
    r = replay(a.repo_root, p, a.source_root)
    raw = json.dumps(r, indent=2) + '\n'
    if a.output:
        with a.output.open('x') as f:
            f.write(raw)
    print(raw)


if __name__ == '__main__':
    main()

