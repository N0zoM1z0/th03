#!/usr/bin/env python3
"""Offline replay of the actual original-root PFOPEN build, not acceptance.

Checks historical receipts and source provenance without invoking native tools,
requiring today's HEAD to equal the historical HEAD, or reading live registries.
"""
from pathlib import Path
import argparse
import hashlib
import json
import stat
import sys
import types

PROPOSAL = '.analysis/op-pfopen-native-deferred-v01'
OUT = '.analysis/op-pfopen-native-output-v01'
AUDIT = '.analysis/op-selection-order-trace-20261022-v01/link_correction'
MANIFEST_SHA = '87eed7d10f27298eb1eb7f6c0cb59c8a4f173cbe5b995c3665deee030ca2d58e'
VERIFIER_SHA = '4b0d1a936079d45fce5e03afde7a8dff10a5c08654632289f89f1a995ab74e0d'
REPORT_SHA = '37db39682275d9e2165e2b697a6e13195197a5ca9f95e4999f442cbb03f44e62'
COMPLETION_SHA = '0326246caf5e8d2e6e3f17bbe455a8cbd19e2e3a98a9a93f5937cd8cb85201b5'
AUDIT_SHA = '227ff0e1c3e814c01aa8d0217feb7718de0a9de310a3b00e82e9429b73548e4e'
AUDIT_CODE_SHA = '021e0f3691741452cfc35cc0c397ba9b85146e54b42f2c44a334aea9f5ab2ba5'
AUDIT_PINS_SHA = 'b92ed823195d0bdcb4541a2063cb6294d450ae740db23eb774d03074abb21405'
HISTORICAL_HEAD = '1feecd5c980be16625a4dbf0ba148a98b6a8f3f3'
EXE_SHA = '0ed2822e8acda85fb321e848a9555829da50cc389505528fbb070377009afe8e'
CONFIG = 'config/th03_op_pfopen_source_candidate.json'
STAGE = 'scripts/stage_th03_op_pfopen_source.py'
SELF = 'scripts/replay_th03_op_pfopen_source.py'
SOURCE = 'src/shared/formats/pfopen.asm'
HEADERS = {'compat/op_pfopen/'+n for n in ('ReC98.inc', 'libs/master.lib/func.inc',
    'libs/master.lib/super.inc', 'libs/master.lib/bgm.inc', 'libs/master.lib/pf.inc',
    'libs/master.lib/clip.inc', 'libs/master.lib/macros.inc', 'libs/kaja/kaja.inc',
    'twobyte.inc', 'pc98.inc', 'th01/hardware/egc.inc', 'th02/formats/pi_slots.inc')}
SOURCE_CLOSURE = {CONFIG, STAGE, SELF, SOURCE} | HEADERS
HELPER_CLOSURE = {'scripts/lib/__init__.py', 'scripts/lib/pc98.py', 'scripts/lib/omf.py'}
PHASES = ['compile_root', 'link']
FLAGS = ('source_acceptance', 'exact_acceptance', 'whole_root_credit',
         'whole_product_ownership', 'cold_build', 'two_cold_builds', 'runtime_rerun', 'packing_run')


# This is a current replay-code revision, not an amended native receipt. The
# predecessor proof and replay remain byte-identical retained data. Only the two
# enumerated, nonconsumed housekeeping inputs use historical snapshots; current
# maintained sources and imported helpers never use a fallback. Snapshot storage
# mode is deliberately 0644; historical input modes remain in historical_pin.
REPLAY_BINDING = 'config/op_pfopen_source/replay_binding_v2.json'
EXPECTED_BINDING = {'schema': 'th03-op-pfopen-replay-binding-v2',
 'original_proof': {'path': 'config/op_pfopen_source/proof.json',
                    'sha256': 'b7b70fbb7a9da705f93fc7533528311007b56f441105830116bb6ff99b6adf35',
                    'bytes': 16287},
 'predecessor_replay': {'historical_pin': {'path': 'scripts/replay_th03_op_pfopen_source.py',
                                           'sha256': 'ac8372f0ad8e9899035ef694ff2d9959aa42007bb353a5f531e6af0724ca43d1',
                                           'bytes': 24142},
                        'snapshot': {'path': 'config/recovery/op_pfopen_replay_0b07a287.py.txt',
                                     'sha256': 'ac8372f0ad8e9899035ef694ff2d9959aa42007bb353a5f531e6af0724ca43d1',
                                     'bytes': 24142,
                                     'mode': 420},
                        'origin_commit': '0b07a287ddeef8904046ef5f8ebdfaa352f332ea',
                        'origin_blob': 'd6f0b5a637fdfba70b1e8974b172056f0bfd6b94'},
 'historical_inputs': {'scripts/clean_generated.py': {'historical_pin': {'path': 'scripts/clean_generated.py',
                                                                         'sha256': '25c0760614c7ef6996dea6659f63208c03f4d2a28a11776141294ac730e7a0ea',
                                                                         'bytes': 17828,
                                                                         'mode': 493},
                                                      'snapshot': {'path': 'config/recovery/clean_generated_095e54bc.py.txt',
                                                                   'sha256': '25c0760614c7ef6996dea6659f63208c03f4d2a28a11776141294ac730e7a0ea',
                                                                   'bytes': 17828,
                                                                   'mode': 420},
                                                      'origin_commit': '095e54bc3d437ca12ea499aeb242d1c6b1e79253',
                                                      'origin_blob': '9d658a86ac7f5c4fe9140c59e04ac5cff0bd9c5c'},
                       'scripts/progress.py': {'historical_pin': {'path': 'scripts/progress.py',
                                                                  'sha256': '958818dcd3cb8a3229b6810e129cbb7901009d28a8d2357e4f89abbefac90469',
                                                                  'bytes': 111209,
                                                                  'mode': 384},
                                               'snapshot': {'path': 'config/recovery/progress_1feecd5c.py.txt',
                                                            'sha256': '958818dcd3cb8a3229b6810e129cbb7901009d28a8d2357e4f89abbefac90469',
                                                            'bytes': 111209,
                                                            'mode': 420},
                                               'origin_commit': '1feecd5c980be16625a4dbf0ba148a98b6a8f3f3',
                                               'origin_blob': 'e7ec8096111a2da54de429fc4120bf5430dd8d9e'}}}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def values(raw):
    return dict(sha256=sha(raw), bytes=len(raw))


def regular(root, name):
    p = Path(name)
    need(not p.is_absolute() and '..' not in p.parts and str(p) == name, 'unsafe input path')
    p = Path(root)/p
    need(not any(x.is_symlink() for x in (p, *p.parents)) and p.is_file(), 'regular input '+name)
    return p


def stable_read(root, name):
    p = regular(root, name)
    a = p.stat(); raw = p.read_bytes(); b = p.stat()
    need((a.st_dev, a.st_ino, a.st_size, a.st_mode, a.st_mtime_ns, a.st_ctime_ns) ==
         (b.st_dev, b.st_ino, b.st_size, b.st_mode, b.st_mtime_ns, b.st_ctime_ns), 'unstable input '+name)
    return raw


def checked_file(root, pin, label):
    raw = stable_read(root, pin['path'])
    need(values(raw) == {k: pin[k] for k in ('sha256', 'bytes')}, label+' identity')
    if 'mode' in pin:
        need(stat.S_IMODE(regular(root, pin['path']).stat().st_mode) == pin['mode'], label+' mode')
    return raw


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate replay binding key '+key)
        result[key] = value
    return result


def read_replay_binding(source_root, p):
    binding = json.loads(stable_read(source_root, REPLAY_BINDING), object_pairs_hook=unique_object)
    need(isinstance(binding, dict) and set(binding) == set(EXPECTED_BINDING) | {'current_replay'},
         'current replay binding schema')
    need({k: binding[k] for k in EXPECTED_BINDING} == EXPECTED_BINDING,
         'current replay binding provenance')
    checked_file(source_root, binding['original_proof'], 'original proof')
    predecessor = binding['predecessor_replay']
    need(p['maintained_closure'][SELF] == {k: predecessor['historical_pin'][k]
         for k in ('sha256', 'bytes')}, 'original predecessor replay pin')
    checked_file(source_root, predecessor['snapshot'], 'predecessor replay snapshot')
    current = binding['current_replay']
    need(isinstance(current, dict) and set(current) == {'path', 'sha256', 'bytes', 'mode'}
         and current['path'] == SELF and current['mode'] == 0o755
         and type(current['bytes']) is int and current['bytes'] > 0
         and isinstance(current['sha256'], str) and len(current['sha256']) == 64
         and all(c in '0123456789abcdef' for c in current['sha256']), 'current replay pin schema')
    checked_file(source_root, current, 'current replay')
    for entry in binding['historical_inputs'].values():
        checked_file(source_root, entry['snapshot'], 'historical housekeeping snapshot')
    return binding


def read_retained(root, source_root, name, pins, binding):
    need(name in pins, 'unbound input '+name)
    pin = pins[name]
    if name in binding['historical_inputs']:
        entry = binding['historical_inputs'][name]
        need(pin == entry['historical_pin'], 'historical housekeeping pin '+name)
        return checked_file(source_root, entry['snapshot'], 'historical housekeeping snapshot '+name)
    raw = stable_read(root, name)
    need(values(raw) == {k: pin[k] for k in ('sha256', 'bytes')}, 'input drift '+name)
    need(stat.S_IMODE(regular(root, name).stat().st_mode) == pin['mode'], 'input mode drift '+name)
    return raw


def load_retained_module(name, root, path, read, binding):
    # These records are evidence-only. Never turn a historical path remap into
    # an alternate code loader, even if a later caller accidentally requests it.
    evidence_only = set(binding['historical_inputs']) | {
        q['snapshot']['path'] for q in binding['historical_inputs'].values()}
    evidence_only.add(binding['predecessor_replay']['snapshot']['path'])
    need(path not in evidence_only, 'historical snapshot is data only '+path)
    return load_checked_module(name, root/path, read(path))


def bind_verifier_inputs(verifier, read, binding):
    # Keep the original verifier bytes and every comparison intact. Its pin()
    # independently rechecks m.inputs, so apply the same two-path data binding
    # at that I/O boundary. All other requests use its original path/mode checks.
    original_pin = verifier.pin
    def bound_pin(pin, base=None):
        name = pin['path']
        if name in binding['historical_inputs']:
            need(base is None, 'historical housekeeping alternate base '+name)
            need(pin == binding['historical_inputs'][name]['historical_pin'],
                 'historical verifier housekeeping pin '+name)
            return read(name)
        return original_pin(pin, base)
    verifier.pin = bound_pin


def validate_proof(p):
    need(p['schema'] == 'th03-op-pfopen-source-proof-v1', 'proof schema')
    need(all(p[n] is False for n in FLAGS), 'credit inflation')
    need(tuple(p[n] for n in ('native_phases', 'fresh_owner_objects', 'new_owner_bytes',
        'preserved_prior_owners', 'preserved_prior_bytes', 'total_scoped_bodies',
        'total_scoped_bytes')) == (2, 1, 281, 44, 12940, 45, 13221), 'PFOPEN-only scope')
    need(p['retained_context_objects']+p['fresh_owner_objects'] == p['project_objects'] == 28,
         'actual project object graph')
    need(p['manifest_sha256'] == MANIFEST_SHA and p['verifier_sha256'] == VERIFIER_SHA
         and p['report_sha256'] == REPORT_SHA and p['completion_sha256'] == COMPLETION_SHA
         and p['selection_audit_sha256'] == AUDIT_SHA and p['historical_head'] == HISTORICAL_HEAD,
         'historical recipe identity')
    need(p['original_runner_complete'] is True and p['corrected_selection_prerequisite'] is True,
         'native completion/prerequisite')
    need(set(p['maintained_closure']) == SOURCE_CLOSURE and set(p['helper_closure']) == HELPER_CLOSURE,
         'maintained/helper closure')


def receipt_names():
    names = {'manifest.json', 'environment.json', 'completion.json', 'linked-verification.json',
             'materialized-inputs.json', 'source-mtimes.json', 'link-map-output.json',
             'accumulated-objects.json', 'next-registry-baseline.json'}
    for phase in PHASES:
        names |= {phase+s for s in ('-started.json', '-finished.json', '-output.json',
                                   '-registry-transition.json', '.log')}
        names |= {phase+'-'+side+'-'+n for side in ('before', 'after')
                  for n in ('registry.json', 'user.reg', 'system.reg')}
    return names


def collect_pins(value):
    found = []
    if isinstance(value, dict):
        if {'path', 'sha256', 'bytes'} <= set(value):
            found.append(value)
        for child in value.values():
            found.extend(collect_pins(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(collect_pins(child))
    return found


def required_paths(m, packet, baseline, audit_pins):
    # The full historical sources manifest is evidence, NOT a current whole-tree guard.
    paths = {q['path'] for q in collect_pins({k: val for k, val in m.items() if k != 'sources'})}
    paths |= HELPER_CLOSURE | set(m['fixed_mtimes'])
    paths |= {m['work']+'/'+n for n in set(m['repeat_inputs']) | set(m['all_native_outputs'])}
    paths |= {OUT+'/'+n for n in receipt_names()} | {PROPOSAL+'/manifest.json'}
    paths |= {AUDIT+'/'+n for n in ('audit.py', 'replay-pins.json', 'audit-result.json')}
    paths |= {q['path'] for q in collect_pins(audit_pins)}
    paths |= {baseline['baseline_map']['path'], baseline['baseline_exe']['path'], baseline['verifier']['path']}
    packet_root = Path(m['source_packet_manifest']['path']).parent
    paths |= {str(packet_root/q['path']) for q in [packet['source'], *packet['compatibility_closure']]}
    original_root = Path(m['baseline_exe']['path']).parents[2]
    paths |= {str(original_root/q['path']) for q in [packet['original_source'], *packet['physical_context']]}
    paths |= {n for n in m['repeat_inputs'] if n.startswith(('src/', 'compat/'))}
    return paths


def guard_current(root, p, source_root, m, binding=None):
    current_binding = read_replay_binding(source_root, p)
    need(binding is None or current_binding == binding, 'current replay binding changed during replay')
    binding = current_binding
    for name, q in p['helper_closure'].items():
        need(q == {k: m['sources'][name][k] for k in ('sha256', 'bytes')}, 'historical import helper '+name)
        need(values(stable_read(root, name)) == q, 'current helper before import '+name)
    for name, q in p['maintained_closure'].items():
        if name == SELF:
            q = {k: binding['current_replay'][k] for k in ('sha256', 'bytes')}
        need(values(stable_read(source_root, name)) == q, 'maintained closure drift '+name)
    expected = {n for n in m['repeat_inputs'] if n.startswith(('src/', 'compat/'))}
    need(set(p['context_source_closure']) == expected, 'retained maintained context membership')
    for name, q in p['context_source_closure'].items():
        need(q == {k: m['repeat_inputs'][name][k] for k in ('sha256', 'bytes')}
             and values(stable_read(root, name)) == q, 'current consumed maintained context '+name)


def validate_phase(phase, start, finish, m, env):
    need(start['argv'] == m['native_argv'][phase], 'native argv')
    need(Path(start['cwd']).parts[-len(Path(m['work']).parts):] == Path(m['work']).parts, 'native cwd')
    need(start['environment'] == env['environment'], 'phase environment')
    need(start['wait_seconds'] == 90 and start['cleanup_seconds'] == 15, 'phase bounds')
    need(len(env['cpu']) == 1 and env['nice'] >= 10, 'resource bounds')
    need(start['environment']['DISPLAY'] == start['environment']['WAYLAND_DISPLAY'] == ''
         and start['environment']['TZ'] == 'UTC', 'headless UTC')
    need(type(finish['exit_code']) is int and finish['exit_code'] == 0, 'native exit')
    need(all(finish[n] is False for n in ('timeout', 'cleanup_uncertain', 'poison')), 'unsafe cleanup')
    need(finish['initial_inventory_complete'] is True and finish['inventory_complete'] is True
         and finish['survivors'] == [] and finish['errors'] == [] and finish['ok'] is True,
         'owned cleanup inventories')
    need(len(finish['owned_leader']) == 5 and type(finish['owned_leader'][0]) is int
         and finish['owned_leader'][0] > 0, 'exact owned process identity')


def validate_completion(done):
    need(done['complete'] is True and done['errors'] == [] and done['owned_lock_released'] is True,
         'actual native completion')
    need(done['native_invocations'] == 2 and done['phases'] == PHASES and done['group'] == done['round'] == 1,
         'native phase count/graph')
    need(all(done[n] is False for n in ('source_acceptance', 'exact_acceptance',
         'full_historical_replay', 'runtime_run')), 'native receipt credit scope')


def validate_report(r):
    need(r['diagnostic_checks_pass'] is True and r['linked_scope_checks_pass'] is True
         and r['checks'] and all(v is True for v in r['checks'].values()), 'actual linked checks')
    need(all(r[n] is False for n in ('source_acceptance', 'exact_acceptance', 'whole_root_credit',
         'whole_product_ownership', 'source_progress_changed', 'runtime_run', 'packing_run')), 'report credit scope')
    need((r['prior_owner_count'], r['prior_owner_bytes'], len(r['prior_owners']),
          r['candidate_scope_count'], r['candidate_scope_bytes'], r['new_candidate_count'],
          r['new_candidate_bytes']) == (44, 12940, 44, 45, 13221, 1, 281), 'report scoped denominator')
    need(len({u['id'] for u in r['prior_owners']}) == 44 and sum(u['size'] for u in r['prior_owners']) == 12940,
         'prior IDs/sizes')
    need(all(u['baseline_raw_equal'] is True and u['baseline_ordered_equal'] is True and u['target_raw_equal'] is True
         and u['target_ordered_equal'] is True for u in r['prior_owners']), 'prior scoped preservation')
    u = r['new_pfopen_body']
    need((u['id'], u['segment'], u['offset'], u['size']) == ('PFOPEN', 0, 0x2EF2, 281)
         and u['target_raw_equal'] is True and u['target_ordered_equal'] is True
         and u['candidate_sha256'] == u['target_sha256'], 'sole new PFOPEN extent')
    g = r['graph']
    need(g['project_object_count'] == len(g['project_object_order']) == 28
         and g['retained_project_object_count'] == r['retained_project_context_count'] ==
         len(r['retained_project_context']) == 27 and g['fresh_project_object_count'] == 1,
         'report object partition')
    need(all(r['root_object'][n] is True for n in ('valid', 'raw_equal',
         'complete_structural_equal', 'normalized_file_equal')), 'complete actual root OMF identity')
    need(r['source_proof']['comment_only_statement_identity'] is True
         and r['source_proof']['physical_context_files'] == 142
         and r['source_proof']['compatibility_headers'] == 12, 'complete source/context closure')
    abi = r['source_proof']['abi']
    need((abi['model'], abi['retsize_words'], abi['datasize_words'], abi['far_return'],
          abi['callee_pop_bytes'], abi['file_bp_offset'], abi['parfile_bp_offset'], abi['preserved_registers'])
         == ('use16 large _TEXT', 2, 2, True, 8, 6, 10, ['SI', 'DI']), 'actual source ABI')
    publics = r['map_public_counts']
    need(publics['candidate'] == publics['baseline'] and publics['candidate']['Name']
         == publics['candidate']['Value'] > 0, 'both complete public sections')
    need(r['native_proof']['phase_count'] == 2 and r['native_proof']['materialized_root_seed_absent'] is True
         and r['verifier_native_invocations'] == 0, 'native provenance scope')
    need(r['candidate_sha256'] == r['baseline_sha256'] == EXE_SHA
         and r['whole_program']['baseline_different_bytes'] == 0, 'baseline complete image preservation')
    rel = r['whole_ordered_relocations']
    diff = lambda a, b: sum(x != y for x, y in zip(a, b))+abs(len(a)-len(b))
    need(rel['baseline_equal'] is True and rel['candidate'] == rel['baseline']
         and rel['baseline_different_positions'] == 0, 'literal baseline relocation preservation')
    need(rel['target_equal'] == (rel['candidate'] == rel['target']) and
         rel['target_different_positions'] == diff(rel['candidate'], rel['target']), 'measured target relocation diagnostics')
    need(r['excluded_context'] == dict(following_alignment_and_str_ieq=[0x300B, 0x3044],
         dd95=[0xDD95, 0xDD96], all_other_root_bodies_data_and_alignment=True), 'vendor context exclusion')


def validate_selection_audit(a, m, baseline, read):
    need(a['post_diagnostic_audit_pass'] is True and a['original_runner_complete'] is True
         and a['original_linked_scope_checks_pass'] is False
         and a['original_report_reproduced_verbatim'] is True
         and a['immutable_original_receipts_unchanged'] is True, 'dated selection audit outcome')
    need(a['native_invocations_now'] == 0 and a['source_acceptance'] is False and a['exact_acceptance'] is False,
         'selection audit credit scope')
    for key, q in [('original_manifest_sha256', m['baseline_manifest']),
                   ('original_completion_sha256', m['baseline_completion']),
                   ('original_report_sha256', m['baseline_report'])]:
        need(a[key] == q['sha256'] == sha(read(q['path'])), 'selection historical receipt binding')
    need(a['original_verifier_sha256'] == baseline['verifier']['sha256'], 'selection original verifier binding')
    need(a['corrected_diagnostic']['diagnostic_checks_pass'] is True
         and a['corrected_diagnostic']['linked_scope_checks_pass'] is True, 'selection corrected prerequisite')
    for name, key in [('bin/th03/op.exe', 'baseline_exe'), ('obj/th03/op.map', 'baseline_map')]:
        need(a['actual_native_outputs'][name] == {k: m[key][k] for k in ('sha256', 'bytes', 'mode')},
             'selection-to-PFOPEN actual output identity')


def load_checked_module(name, path, raw):
    mod = types.ModuleType(name)
    mod.__file__ = str(path)
    if name == 'lib':
        mod.__path__ = [str(path.parent)]
    sys.modules[name] = mod
    exec(compile(raw, str(path), 'exec'), mod.__dict__)
    return mod


def replay(root, p, source_root=None):
    root, source_root = Path(root).resolve(), Path(source_root or root).resolve()
    validate_proof(p)
    binding = read_replay_binding(source_root, p)
    q = p['inventory']; raw = stable_read(root, q['path'])
    need(values(raw) == {k: q[k] for k in ('sha256', 'bytes')}, 'inventory identity')
    inv = json.loads(raw)
    need(inv['metadata'] == {k: val for k, val in p.items() if k != 'inventory'}, 'inventory metadata')
    pins = {q['path']: q for q in inv['pins']}
    need(len(pins) == len(inv['pins']), 'duplicate inventory pin')
    need(inv['inputs'] == {n: {k: q[k] for k in ('sha256', 'bytes')} for n, q in pins.items()},
         'cleanup retention mirror')
    def read(name):
        return read_retained(root, source_root, name, pins, binding)
    js = lambda name: json.loads(read(name))
    # No repository code is imported until every retained input and current import/source guard passes.
    for name in pins:
        read(name)
    raw = read(PROPOSAL+'/manifest.json')
    need(sha(raw) == MANIFEST_SHA and raw == read(OUT+'/manifest.json'), 'actual consumed manifest')
    m = json.loads(raw)
    need(m['schema'] == 'th03-op-pfopen-root-context-native-v1' and m['head'] == HISTORICAL_HEAD
         and m['phases'] == PHASES and m['output'] == OUT and Path(m['work']).name == 'OPPF101',
         'historical native identity')
    baseline, packet = js(m['baseline_manifest']['path']), js(m['source_packet_manifest']['path'])
    audit_pins = js(AUDIT+'/replay-pins.json')
    need(required_paths(m, packet, baseline, audit_pins) == set(pins), 'exact retained closure membership')
    for row in m['inputs'] + m['toolchain_inputs'] + collect_pins(audit_pins):
        need(values(read(row['path'])) == {k: row[k] for k in ('sha256', 'bytes')}, 'consumed input binding')
        if 'mode' in row:
            need(pins[row['path']]['mode'] == row['mode'], 'consumed input mode binding')
    for name, stamp in m['fixed_mtimes'].items():
        need(regular(root, name).stat().st_mtime_ns == stamp, 'fixed tool mtime')
    guarded_code = SOURCE_CLOSURE | HELPER_CLOSURE | set(p['context_source_closure'])
    consumed_paths = set(m['repeat_inputs']) | {q['path'] for q in m['repeat_inputs'].values()}
    need(not (set(binding['historical_inputs']) & (guarded_code | consumed_paths | set(m['fixed_mtimes']))),
         'historical housekeeping is not consumed code')
    guard_current(root, p, source_root, m, binding)
    need({x.name for x in (root/OUT).iterdir()} == receipt_names(), 'native receipt membership')
    for x in (root/OUT).iterdir(): regular(root, str(x.relative_to(root)))
    need({x.relative_to(root/m['work']).as_posix() for x in (root/m['work']).rglob('*') if x.is_file()}
         == set(m['repeat_inputs']) | set(m['all_native_outputs']), 'native carrier membership')
    need(m['new_owner_objects'] == ['obj/th03/op.obj'] and 'obj/th03/op.obj' not in m['repeat_inputs']
         and set(m['retained_objects']) | set(m['new_owner_objects']) == set(m['project_objects']),
         'unseeded original root producer graph')
    need(p['project_objects'] == m['project_object_count'] == len(m['project_objects'])
         and p['retained_context_objects'] == len(m['retained_objects'])
         and p['fresh_owner_objects'] == len(m['new_owner_objects']), 'proof derives actual object graph')
    done = js(OUT+'/completion.json'); validate_completion(done)
    need(sha(read(OUT+'/completion.json')) == COMPLETION_SHA and sha(read(OUT+'/linked-verification.json')) == REPORT_SHA,
         'actual output receipt identities')
    audit = js(AUDIT+'/audit-result.json')
    need(sha(read(AUDIT+'/audit-result.json')) == AUDIT_SHA == m['baseline_corrected_audit']['sha256']
         and sha(read(AUDIT+'/audit.py')) == AUDIT_CODE_SHA
         and sha(read(AUDIT+'/replay-pins.json')) == AUDIT_PINS_SHA, 'dated selection audit identity')
    validate_selection_audit(audit, m, baseline, read)
    material, times = js(OUT+'/materialized-inputs.json'), js(OUT+'/source-mtimes.json')
    need(set(material) == set(times) == set(m['repeat_inputs']), 'materialized closure')
    for name, q in m['repeat_inputs'].items():
        a, b = regular(root, q['path']), regular(root, m['work']+'/'+name)
        need(read(q['path']) == read(m['work']+'/'+name), 'snapshot-to-consumed bytes')
        need((a.stat().st_dev, a.stat().st_ino) != (b.stat().st_dev, b.stat().st_ino)
             and a.stat().st_mtime_ns == b.stat().st_mtime_ns == q['mtime_ns'] == times[name], 'source copy/mtime')
        need(material[name] == {k: q[k] for k in ('sha256', 'bytes', 'mode')}, 'materialized metadata')
    sys.dont_write_bytecode = True
    load = lambda name, path: load_retained_module(name, root, path, read, binding)
    for name in ('lib', 'lib.pc98', 'lib.omf'):
        sys.modules.pop(name, None)
    load('lib', 'scripts/lib/__init__.py')
    load('lib.pc98', 'scripts/lib/pc98.py')
    load('lib.omf', 'scripts/lib/omf.py')
    stage = load_checked_module('pfopen_maintained_stage', source_root/STAGE, stable_read(source_root, STAGE))
    cfg, overlay = stage.read_inputs(source_root)
    need(set(overlay) == {'th03/formats/pfopen.asm'} | {q['stage_destination'] for q in packet['compatibility_closure']},
         'maintained thirteen-input overlay')
    reference = Path(m['baseline_exe']['path']).parents[2]
    payload = stage.payload(source_root, root/reference)
    need(len(payload) == 143, 'complete physical source closure')
    for name, data in payload.items(): need(data == read(m['work']+'/'+name), 'maintained-to-consumed source '+name)
    correction = load('pfopen_selection_prerequisite', AUDIT+'/audit.py')
    public_report = correction.compare_publics(read(baseline['baseline_map']['path']).decode(), read(m['baseline_map']['path']).decode())
    corrected = correction.corrected(js(m['baseline_report']['path']), public_report)
    need(json.loads(json.dumps(corrected)) == audit['corrected_diagnostic'], 'dated selection correction reproduction')
    policy = load('pfopen_snapshot_registry_policy', m['registry_policy']['path'])
    registry = {n: q['sha256'] for n, q in m['registry_baseline'].items()}
    env = js(OUT+'/environment.json')
    for phase in PHASES:
        start, finish = js(OUT+'/'+phase+'-started.json'), js(OUT+'/'+phase+'-finished.json')
        validate_phase(phase, start, finish, m, env)
        need(Path(start['cwd']) == root/m['work'], 'actual absolute phase cwd')
        before = {n: read(OUT+'/'+phase+'-before-'+n) for n in registry}
        after = {n: read(OUT+'/'+phase+'-after-'+n) for n in registry}
        need({n: sha(data) for n, data in before.items()} == registry == js(OUT+'/'+phase+'-before-registry.json'),
             'historical registry continuity')
        registry = {n: sha(data) for n, data in after.items()}
        need(registry == js(OUT+'/'+phase+'-after-registry.json'), 'historical registry after')
        tr = js(OUT+'/'+phase+'-registry-transition.json')
        actual = policy.validate_transition(before, after, phase_start_utc=start['started_utc'],
                                           phase_end_utc=tr['phase_end_utc'], child_tz='UTC')
        need(json.loads(json.dumps(actual)) == tr and tr['ok'], 'historical registry policy replay')
    need(registry == {n: q['sha256'] for n, q in js(OUT+'/next-registry-baseline.json').items()}, 'historical final registry receipt')
    need(sha(read(m['verifier']['path'])) == VERIFIER_SHA, 'native verifier identity')
    verifier = load('pfopen_actual_native_verifier', m['verifier']['path'])
    verifier.ROOT = root
    bind_verifier_inputs(verifier, read, binding)
    fresh = json.loads(json.dumps(verifier.verify(root/m['work'], m)))
    need(fresh == js(OUT+'/linked-verification.json'), 'native report verbatim replay')
    validate_report(fresh)
    accumulated = js(OUT+'/accumulated-objects.json')
    need(set(accumulated) == set(m['all_native_outputs']), 'accumulated output membership')
    for name, q in accumulated.items():
        need(values(read(m['work']+'/'+name)) == {k: q[k] for k in ('sha256', 'bytes')}, 'accumulated output hash')
    for name in pins: read(name)
    guard_current(root, p, source_root, m, binding)
    return dict(schema=p['schema'], pass_checks=True, pinned_files=len(pins), native_invocations_now=0,
        original_runner_complete=True, original_report_reproduced_verbatim=True,
        native_phases_replayed=len(PHASES), fresh_owner_objects=1, new_owner_bytes=281,
        retained_context_objects=fresh['graph']['retained_project_object_count'],
        project_objects=fresh['graph']['project_object_count'], preserved_prior_owners=44,
        preserved_prior_bytes=12940, total_scoped_bodies=45, total_scoped_bytes=13221,
        complete_root_omf_preserved=True, source_binding=True,
        dated_selection_prerequisite_sha256=AUDIT_SHA, selection_correction_reproduced=True,
        candidate_sha256=fresh['candidate_sha256'], whole_program=fresh['whole_program'],
        whole_ordered_relocations={k: val for k, val in fresh['whole_ordered_relocations'].items()
                                   if k not in ('candidate', 'baseline', 'target')},
        whole_file_equal_target=fresh['whole_file_equal_target'], excluded_context=fresh['excluded_context'],
        historical_head=HISTORICAL_HEAD, installed_head_requirement=False,
        replay_binding_schema=binding['schema'],
        historical_input_snapshots={n: q['snapshot']['path'] for n, q in binding['historical_inputs'].items()},
        current_replay_sha256=binding['current_replay']['sha256'],
        historical_audit_claims_not_rerun=['current_HEAD_and_membership', 'live_registry_equality',
            'no_poison_or_active_claim', 'shared_read_lock'], **{n: False for n in FLAGS})


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument('--source-root', type=Path)
    ap.add_argument('--proof', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    proof = json.loads((args.proof or args.repo_root/'config/op_pfopen_source/proof.json').read_bytes())
    result = replay(args.repo_root, proof, args.source_root)
    raw = json.dumps(result, indent=2)+'\n'
    if args.output:
        with args.output.open('x') as stream: stream.write(raw)
    print(raw)


if __name__ == '__main__':
    main()
