#!/usr/bin/env python3
"""Offline replay of raster producers and separate aggregation correction, not acceptance."""
from pathlib import Path
import argparse
import hashlib
import json
import stat
import sys
import types

PROPOSAL = '.analysis/op-raster-native-proposal-v01'
SOURCE = '.analysis/op-raster-source-proposal-v01/payload'
OUT = '.analysis/op-raster-native-output-v01'
AUDIT = '.analysis/op-raster-offline-correction-v01'
MANIFEST_SHA = '62a464caafe5b468736982a187457c1c2d35951495813c1126a517d24b96d092'
VERIFIER_SHA = '36723c93537c07d4373773d8f7532c43e564fa24a8b17755e1c3d84db939f64c'
AUDIT_SHA = 'c13d4c4c4009a6da64d057dc720ad18b515ab4098986a43a6a09a4dccd1572cd'
AUDIT_CODE_SHA = '7f4fe4c4e03829da8f06cfb678b53587591d89f864608bdd542286844d1c9fd3'
AUDIT_PINS_SHA = '33c501c3dada4f9edb35ea163bc56458fd7a2e7954f077431060031d673cb858'
HISTORICAL_HEAD = '6e895a923632a94323b6ecba6fd0237ac78cebc5'
EXE_SHA = 'ca6786f03b28415da3601f8e49fe5dac6ec908dae0d0f420dd701ac58b4e2275'
PHASES = ['compile_op_music', 'compile_op_main', 'link']
FLAGS = ('source_acceptance', 'exact_acceptance', 'whole_product_ownership',
         'cold_build', 'two_cold_builds', 'runtime_rerun', 'packing_run')
BODIES = {'src/op/music/nopoly_blit.inl', 'src/op/menu/column_restore.inl'}
SOURCE_CLOSURE = BODIES | {'config/th03_op_raster_candidate.json',
    'scripts/stage_th03_op_raster.py', 'scripts/replay_th03_op_raster.py'}
HELPER_CLOSURE = {'scripts/lib/__init__.py', 'scripts/lib/pc98.py',
    'scripts/lib/omf.py', 'scripts/lib/targets.py', 'scripts/review_th03_decoded_code.py',
    'scripts/inventory_rec98_th03.py', 'config/targets.toml'}
MODULES = ('lib', 'lib.pc98', 'lib.omf', 'lib.targets',
           'review_th03_decoded_code', 'inventory_rec98_th03')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def values(raw):
    return dict(sha256=sha(raw), bytes=len(raw))


def regular(root, name):
    p = Path(name)
    need(not p.is_absolute() and '..' not in p.parts and str(p) == name,
         'unsafe input path')
    p = Path(root) / p
    need(not any(x.is_symlink() for x in (p, *p.parents)) and p.is_file(),
         'regular input ' + name)
    return p


def stable_read(root, name):
    p = regular(root, name)
    a = p.stat()
    raw = p.read_bytes()
    b = p.stat()
    need((a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns, a.st_ctime_ns) ==
         (b.st_dev, b.st_ino, b.st_size, b.st_mtime_ns, b.st_ctime_ns),
         'unstable input ' + name)
    return raw


def validate_proof(p):
    need(p['schema'] == 'th03-op-raster-proof-v1', 'schema')
    need(all(p[n] is False for n in FLAGS), 'credit inflation')
    need(tuple(p[n] for n in ('native_phases', 'fresh_owner_objects',
        'new_owner_bytes', 'retained_context_objects', 'preserved_prior_owners',
        'preserved_prior_bytes', 'excluded_alignment_bytes')) == (3, 2, 124, 25, 42, 12816, 1),
        'bounded scope')
    need(p['manifest_sha256'] == MANIFEST_SHA and p['verifier_sha256'] == VERIFIER_SHA
         and p['audit_sha256'] == AUDIT_SHA and p['historical_head'] == HISTORICAL_HEAD,
         'recipe identity')
    need(p['original_runner_complete'] is False and
         p['separate_offline_correction'] is True, 'original failure preserved')
    need(set(p['maintained_closure']) == SOURCE_CLOSURE and
         set(p['helper_closure']) == HELPER_CLOSURE, 'current source/helper closure')


def validate_phase(phase, start, finish, m, env):
    need(start['argv'] == m['native_argv'][phase], 'actual phase argv')
    need(Path(start['cwd']).parts[-len(Path(m['work']).parts):] ==
         Path(m['work']).parts, 'actual phase cwd')
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
    # Historical failure is retained verbatim, not silently converted into success.
    need(r['diagnostic_checks_pass'] is False and r['prior_owners_preserved'] is False,
         'original failed aggregate')
    need(all(r[n] is False for n in ('source_acceptance', 'exact_acceptance',
         'source_progress_changed', 'whole_product_ownership', 'cold_build', 'runtime_run')),
         'diagnostic scope')
    need(r['native_invocations_now'] == 0 and r['new_raster_bytes'] == 124,
         'new owner bytes')
    need([(x['name'], x['size']) for x in r['new_raster_bodies']] ==
         [('nopoly_B_put', 30), ('box_column16_unput', 94)], 'new owner extents')
    need(all(x['target_raw_equal'] is True and x['target_ordered_equal'] is True
         and x['candidate_sha256'] == x['target_sha256'] for x in r['new_raster_bodies']),
         'new raster comparison')
    need((r['prior_owner_count'], r['prior_owner_bytes'], len(r['prior_owners'])) ==
         (42, 12816, 42), 'prior scoped denominator')
    need(all(all(x[n] is True for n in ('baseline_raw_equal', 'baseline_ordered_equal',
         'map_preserved')) for x in r['prior_owners']), 'prior baseline preservation')
    need(len(r['objects']) == 2 and len(r['retained_project_context']) ==
         r['retained_project_context_count'] == 25, 'object partition')
    need(all(x['literal_non_data_omf_preserved'] is True and
         x['maintained_lineage_checked'] is True for x in r['objects']), 'OMF lineage')
    need(r['all_map_publics_preserved'] is True and
         r['all_map_code_contributions_preserved'] is True and
         r['candidate_sha256'] == EXE_SHA, 'native output identity')
    need(r['whole_program'] == dict(target_different_bytes=1, baseline_different_bytes=5)
         and r['whole_ordered_relocations'] == dict(target_equal=False,
             baseline_equal=True, target_different_positions=313)
         and r['whole_file_equal_target'] is False, 'global negatives')
    need(r['excluded_vendor_alignment'] == dict(program_offset=0xdd95, target=0x90,
         candidate=0, authored_credit=0, unchanged=True,
         kind='vendor EVEN alignment, not authored variable/CODE'), 'vendor alignment')


def guard_current(root, p, source_root, m):
    """Guard the entire repository import and source closure before any such imports."""
    for n, q in p['helper_closure'].items():
        need(q == {k: m['sources'][n][k] for k in ('sha256', 'bytes')} and
             values(stable_read(root, n)) == q, 'current helper before import ' + n)
    for n, q in p['maintained_closure'].items():
        need(values(stable_read(source_root, n)) == q, 'current maintained source/helper ' + n)
    expected = {n for n in m['repeat_inputs'] if n.startswith(('src/', 'compat/'))} - BODIES
    need(set(p['context_source_closure']) == expected, 'current retained source closure')
    for n, q in p['context_source_closure'].items():
        need(q == {k: m['repeat_inputs'][n][k] for k in ('sha256', 'bytes')} and
             values(stable_read(root, n)) == q, 'current retained source ' + n)


def receipt_names():
    names = {'manifest.json', 'environment.json', 'completion.json',
             'linked-verification.json', 'materialized-inputs.json', 'source-mtimes.json',
             'link-map-output.json'}
    for phase in PHASES:
        names |= {phase + s for s in ('-started.json', '-finished.json', '-output.json',
                                     '-registry-transition.json', '.log')}
        names |= {phase + '-' + side + '-' + n for side in ('before', 'after')
                  for n in ('registry.json', 'user.reg', 'system.reg')}
    return names


def required_paths(m):
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
    # sources is the historical whole-tree audit, not an obsolete installed HEAD guard.
    collect({k: v for k, v in m.items() if k != 'sources'})
    required |= set(m['fixed_mtimes'])
    required |= {m['work'] + '/' + n for n in m['repeat_inputs']}
    required |= {m['work'] + '/' + n for n in m['all_native_outputs']}
    required |= {OUT + '/' + n for n in receipt_names()}
    required |= {SOURCE + '/' + n for n in BODIES}
    required |= {AUDIT + '/' + n for n in ('audit.py', 'replay-pins.json', 'audit-result.json')}
    required.add(PROPOSAL + '/manifest.json')
    baseline = Path(m['baseline_exe']['path']).parents[2]
    required |= {str(baseline / n) for n in ('th03/op_music.cpp', 'th03/op/m_main.cpp')}
    return required


def replay(root, p, source_root=None):
    root = Path(root).resolve()
    source_root = Path(source_root or root).resolve()
    validate_proof(p)
    q = p['inventory']
    raw = stable_read(root, q['path'])
    need(values(raw) == {k: q[k] for k in ('sha256', 'bytes')}, 'inventory identity')
    inv = json.loads(raw)
    need(inv['metadata'] == {k: v for k, v in p.items() if k != 'inventory'},
         'inventory metadata')
    rows = inv['pins']
    need(len(rows) == len({x['path'] for x in rows}), 'duplicate inventory pins')
    pins = {x['path']: x for x in rows}
    need(inv['inputs'] == {n: {k: q[k] for k in ('sha256', 'bytes')} for n, q in pins.items()},
         'cleanup retention mirror')

    def read(n):
        need(n in pins, 'unbound ' + n)
        b = stable_read(root, n)
        need(values(b) == {k: pins[n][k] for k in ('sha256', 'bytes')},
             'input drift ' + n)
        need(stat.S_IMODE(regular(root, n).stat().st_mode) == pins[n]['mode'],
             'input mode drift ' + n)
        return b

    def js(n):
        return json.loads(read(n))

    # All pins and current helper/source guards precede execution of repository Python.
    for n in pins:
        read(n)
    raw = read(PROPOSAL + '/manifest.json')
    need(sha(raw) == MANIFEST_SHA and raw == read(OUT + '/manifest.json'),
         'consumed native recipe')
    m = json.loads(raw)
    need(m['schema'] == 'th03-op-raster-bounded-native-v1' and m['head'] == HISTORICAL_HEAD
         and m['phases'] == PHASES and Path(m['work']).name == 'OPRA101'
         and m['output'] == OUT and m['round'] == 1, 'historical identity')
    need(required_paths(m) <= set(pins), 'missing required retained pin')
    for row in m['inputs'] + m['toolchain_inputs']:
        need(values(read(row['path'])) == {k: row[k] for k in ('sha256', 'bytes')},
             'manifest consumed input')
    for n, stamp in m['fixed_mtimes'].items():
        read(n)
        need(regular(root, n).stat().st_mtime_ns == stamp, 'toolchain mtime')
    guard_current(root, p, source_root, m)
    baseline = Path(m['baseline_exe']['path']).parents[2]
    config = json.loads(stable_read(source_root, 'config/th03_op_raster_candidate.json'))
    need({u['carrier'] for u in config['units']} ==
         {'th03/op_music.cpp', 'th03/op/m_main.cpp'}, 'original carrier source closure')
    for u in config['units']:
        need(sha(read(str(baseline / u['carrier']))) == u['original_carrier_sha256'],
             'pinned original carrier before import')
    need(len(m['new_owner_objects']) == 2 and len(m['retained_objects']) == 25 and
         not set(m['new_owner_objects']) & set(m['retained_objects']), 'producer partition')
    need({x.name for x in (root / OUT).iterdir()} == receipt_names(), 'receipt membership')
    for x in (root / OUT).iterdir():
        regular(root, str(x.relative_to(root)))
    need({x.relative_to(root / m['work']).as_posix() for x in
         (root / m['work']).rglob('*') if x.is_file()} ==
         set(m['repeat_inputs']) | set(m['all_native_outputs']), 'carrier file membership')
    done = js(OUT + '/completion.json')
    need(done['complete'] is False and done['errors'] ==
         ["ValueError('fresh cold validation failed')"] and done['native_invocations'] == 3
         and done['owned_lock_released'] is True, 'exact original failed completion')
    audit_raw = read(AUDIT + '/audit-result.json')
    need(sha(audit_raw) == AUDIT_SHA and sha(read(AUDIT + '/audit.py')) == AUDIT_CODE_SHA
         and sha(read(AUDIT + '/replay-pins.json')) == AUDIT_PINS_SHA, 'dated audit identity')
    audit_result = json.loads(audit_raw)
    need(audit_result['post_diagnostic_audit_pass'] is True and
         audit_result['original_runner_complete'] is False and
         audit_result['original_report_reproduced_verbatim'] is True and
         audit_result['immutable_original_receipts_unchanged'] is True and
         audit_result['native_invocations_now'] == 0 and
         audit_result['source_acceptance'] is False and audit_result['exact_acceptance'] is False
         and all(v is True for v in audit_result['post_checks'].values()), 'dated audit outcome')
    for key, path in [('original_completion_sha256', OUT + '/completion.json'),
                      ('original_report_sha256', OUT + '/linked-verification.json'),
                      ('original_manifest_sha256', PROPOSAL + '/manifest.json')]:
        need(audit_result[key] == sha(read(path)), 'dated audit original binding')
    need(audit_result['original_verifier_sha256'] == VERIFIER_SHA, 'dated verifier binding')

    def load(name, path, body=None, base=root):
        raw = read(path) if body is None else body
        mod = types.ModuleType(name)
        mod.__file__ = str(base / path)
        sys.modules[name] = mod
        exec(compile(raw, mod.__file__, 'exec'), mod.__dict__)
        return mod

    sys.dont_write_bytecode = True
    for name in MODULES:
        sys.modules.pop(name, None)
    stagepath = 'scripts/stage_th03_op_raster.py'
    stage = load('op_raster_maintained_stage', stagepath,
                 stable_read(source_root, stagepath), source_root)
    cfg, data = stage.read_inputs(source_root)
    need(set(data) == BODIES, 'maintained body closure')
    for n in BODIES:
        need(data[n] == read(SOURCE + '/' + n), 'immutable original source ' + n)
    baseline = Path(m['baseline_exe']['path']).parents[2]
    overlay = stage.payload(source_root, root / baseline)
    need(len(overlay) == 4, 'two body/two carrier overlay')
    for n, b in overlay.items():
        need(b == read(m['work'] + '/' + n), 'maintained-to-consumed source ' + n)
    material = js(OUT + '/materialized-inputs.json')
    times = js(OUT + '/source-mtimes.json')
    need(set(material) == set(times) == set(m['repeat_inputs']), 'materialized closure')
    for n, q in m['repeat_inputs'].items():
        a, b = regular(root, q['path']), regular(root, m['work'] + '/' + n)
        need(read(q['path']) == read(m['work'] + '/' + n), 'snapshot to consumed ' + n)
        need((a.stat().st_dev, a.stat().st_ino) != (b.stat().st_dev, b.stat().st_ino)
             and a.stat().st_mtime_ns == b.stat().st_mtime_ns == q['mtime_ns'] == times[n],
             'source copy/mtime identity')
        need(material[n] == {k: q[k] for k in ('sha256', 'bytes', 'mode')},
             'materialized metadata')
    policy = load('op_raster_registry_policy', m['registry_policy']['path'])
    registry = {n: q['sha256'] for n, q in m['registry_baseline'].items()}
    env = js(OUT + '/environment.json')
    phases = []
    for phase in PHASES:
        a, z = js(OUT + '/' + phase + '-started.json'), js(OUT + '/' + phase + '-finished.json')
        tr = js(OUT + '/' + phase + '-registry-transition.json')
        validate_phase(phase, a, z, m, env)
        need(Path(a['cwd']) == root / m['work'], 'absolute consumed cwd')
        before = {n: read(OUT + '/' + phase + '-before-' + n) for n in registry}
        after = {n: read(OUT + '/' + phase + '-after-' + n) for n in registry}
        need({n: sha(b) for n, b in before.items()} == registry ==
             js(OUT + '/' + phase + '-before-registry.json'), 'registry continuity')
        registry = {n: sha(b) for n, b in after.items()}
        need(registry == js(OUT + '/' + phase + '-after-registry.json'), 'registry after')
        actual = policy.validate_transition(before, after, phase_start_utc=a['started_utc'],
                    phase_end_utc=tr['phase_end_utc'], child_tz='UTC')
        need(json.loads(json.dumps(actual)) == tr and tr['ok'], 'registry policy replay')
        name = m['native_outputs'][phase]
        receipt = js(OUT + '/' + phase + '-output.json')
        need(values(read(m['work'] + '/' + name)) ==
             {k: receipt[k] for k in ('sha256', 'bytes')}, 'actual phase output')
        phases.append(dict(phase=phase, native_exit_code=0, cleanup_certain=True,
            registry_policy_replayed=True, output=name, sha256=receipt['sha256']))
    need(phases == audit_result['actual_clean_native_phases'], 'dated native phases')
    receipt = js(OUT + '/link-map-output.json')
    need(values(read(m['work'] + '/obj/th03/op.map')) ==
         {k: receipt[k] for k in ('sha256', 'bytes')}, 'actual linked MAP')
    need(sha(read(m['verifier']['path'])) == VERIFIER_SHA, 'original verifier identity')
    verifier = load('op_raster_original_verifier', m['verifier']['path'])
    verifier.ROOT = root
    fresh = json.loads(json.dumps(verifier.verify(root / m['work'], m)))
    need(fresh == js(OUT + '/linked-verification.json'), 'original report verbatim replay')
    validate_report(fresh)
    # Import only definitions. Never execute audit.main or obsolete historical runner.guard.
    correction = load('op_raster_independent_correction', AUDIT + '/audit.py')
    correction.ROOT = root
    expected = correction.baseline_expectations(verifier, m, fresh)
    corrected = json.loads(json.dumps(correction.aggregate(fresh, expected)))
    need(corrected == audit_result['corrected_diagnostic'] and
         corrected['diagnostic_checks_pass'] is True, 'separate corrected aggregation')
    need(len(corrected['known_prior_target_negatives']) == 1 and
         corrected['known_prior_target_negatives'][0]['baseline_target_ordered_equal'] is False
         and corrected['known_prior_target_negatives'][0]['candidate_target_ordered_equal'] is False,
         'selection target-order negative retained')
    for obj in fresh['objects']:
        for dependency in obj['bound_dependencies']:
            n = dependency.get('physical_path', m['work'] + '/' + dependency['path'])
            need(sha(read(n)) == dependency['sha256'], 'actual OMF source dependency')
    # Recheck files after the replay without asserting current registry/HEAD historical equality.
    for n in pins:
        read(n)
    guard_current(root, p, source_root, m)
    return dict(schema=p['schema'], pass_checks=True, pinned_files=len(pins),
        current_helper_closure=len(HELPER_CLOSURE), maintained_closure=len(SOURCE_CLOSURE),
        current_retained_source_closure=len(p['context_source_closure']), source_binding=True,
        native_phases_replayed=3, native_invocations_now=0, fresh_owner_objects=2,
        new_owner_bytes=124, retained_context_objects=25, preserved_prior_owners=42,
        preserved_prior_bytes=12816, total_source_bodies=44, total_source_bytes=12940,
        original_runner_complete=False, original_diagnostic_checks_pass=False,
        original_report_reproduced_verbatim=True, separate_offline_correction_pass=True,
        dated_post_diagnostic_audit_sha256=AUDIT_SHA,
        historical_audit_claims_not_rerun=['tracked_HEAD_and_membership',
            'current_registry_equals_actual_last_phase', 'no_poison_or_active_claim', 'shared_read_lock'],
        known_prior_target_negatives=corrected['known_prior_target_negatives'],
        candidate_sha256=fresh['candidate_sha256'], whole_program_different_bytes=1,
        whole_ordered_relocations_equal=False, whole_ordered_relocation_differences=313,
        whole_file_equal_target=False, excluded_vendor_alignment_bytes=1,
        historical_head=HISTORICAL_HEAD, installed_head_requirement=False,
        **{n: False for n in FLAGS})


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument('--source-root', type=Path)
    ap.add_argument('--proof', type=Path)
    ap.add_argument('--output', type=Path)
    a = ap.parse_args()
    p = json.loads((a.proof or a.repo_root / 'config/op_raster/proof.json').read_text())
    r = replay(a.repo_root, p, a.source_root)
    raw = json.dumps(r, indent=2) + '\n'
    if a.output:
        with a.output.open('x') as f:
            f.write(raw)
    print(raw)


if __name__ == '__main__':
    main()
