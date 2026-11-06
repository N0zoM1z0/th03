#!/usr/bin/env python3
"""Verify the complete input candidate while retaining the whole-product failure."""
import json
import re

import build_th03_mainl_input_scan_work as b
from build_th03_mainl_resources_work import need, sha


def review():
    config, attestation = b.inputs()
    previous = b.prior_review.review()
    parent, parent_hash = b.base.load(b.runtime.REPORT)
    _, _, _, _, cold_raw, graph, _ = b.images(b.ROOT)
    record, digest = b.base.load(b.REPORT)
    source = (b.ROOT / config['source']).read_bytes()
    original = (b.base.b.WORK / config['cold_object']).read_bytes()
    producer = next(g for g in graph if g['output'] == config['cold_object'])
    need(record['complete'] and record['whole_product_accepted'] is False and
         record['canonical_unit_credit_changed'] is False and record['source_acceptance_publication_changed'] is False and
         record['cold_rebuilt'] is False and record['game_objects_recompiled'] == 0 and
         record['driver_sha256'] == sha((b.ROOT / b.DRIVER).read_bytes()) and
         record['source_sha256'] == sha(source) and record['config_sha256'] == attestation['config_sha256'] and
         record['attestation'] == attestation and record['previous'] == previous and
         record['parent_build_sha256'] == parent_hash and record['cold_report_sha256'] == sha(cold_raw) and
         record['cold_object_sha256'] == sha(original) and record['cold_producer'] == producer,
         'current candidate, actual source-only cold pair and unchanged active runtime DAG')
    need((b.SCRATCH / 'input_s.asm').read_bytes() == source and
         (b.SCRATCH / 'driver.py').read_bytes() == (b.ROOT / b.DRIVER).read_bytes() and
         (b.SCRATCH / 'config.json').read_bytes() == (b.ROOT / b.CONFIG).read_bytes(), 'actual consumed input snapshots')
    labels = [f'round{i}-{p}' for i in (1, 2) for p in ('assemble', 'link')]
    need([p['label'] for p in record['phases']] == labels and all(p['returncode'] == 0 and
         p['log_sha256'] == sha((b.ROOT / p['log_path']).read_bytes()) for p in record['phases']), 'four successful native phases')
    phases = {p['label']: p for p in record['phases']}
    jwasm = str(b.ROOT / attestation['compatible_attestation']['native_tools']['jwasm']['path'])
    dos = ['/usr/bin/wine-stable', str(b.ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    need(len(record['rounds']) == 2, 'two native candidate rounds')
    vectors = []
    allocations = []
    for number, row in enumerate(record['rounds'], 1):
        need(row['round'] == number and set(row['outputs']) == {'obj', 'exe', 'map'}, 'three complete raw candidate outputs')
        vector = {k: b.base.checked(v) for k, v in row['outputs'].items()}
        old = parent['rounds'][number - 1]['outputs']
        need(row['reused_startup'] == old['startup'] and row['reused_library'] == old['lib'] and
             (b.SCRATCH / 'c0l.obj').read_bytes() == b.base.checked(old['startup']) and
             (b.SCRATCH / f'r{number}.lib').read_bytes() == b.base.checked(old['lib']), 'actual after548 C0 and library pair')
        response = (b.base.b.WORK / 'obj/th03/mainl.@l').read_bytes()
        for a, z in ((b'c0l.obj', rb'probe\af549h\c0l.obj'),
                     (rb'bin\th03\mainl.exe', f'probe\\af549h\\r{number}.exe'.encode()),
                     (rb'obj\th03\mainl.map', f'probe\\af549h\\r{number}.map'.encode()),
                     (b' crt.lib', f' probe\\af549h\\r{number}.lib'.encode()),
                     (rb'obj\th03\input_s.obj', rb'probe\af549h\input_s.obj')):
            need(response.count(a) == 1, 'one explicit candidate substitution')
            response = response.replace(a, z)
        need((b.SCRATCH / f'r{number}.lnk').read_bytes() == response and row['response_sha256'] == sha(response) and
             phases[f'round{number}-assemble']['argv'] == [jwasm, *config['compatible_flags'], '-Foinput_s.obj', 'input_s.asm'] and
             phases[f'round{number}-link']['argv'] == dos + ['tlink', f'@probe\\af549h\\r{number}.lnk'], 'actual source and linker argv/bindings')
        target = b.base.checked(old['mainl_exe'])
        scope = b.scope(original, vector['obj'], target, vector['exe'], config)
        need(row['scope'] == scope and scope['instruction_scope_exact'] and not scope['whole_product_exact'],
             'complete raw function and explicit whole-product difference')
        rows = re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=CODE\s+S=SHARED\s+G=\(none\)\s+M=input_s\.asm\s+ACBP=48\s*$',
                          vector['map'].decode(), re.M | re.I)
        need(len(rows) == 1 and int(rows[0][0], 16) * 16 + int(rows[0][1], 16) == config['decoded_start'] and
             int(rows[0][2], 16) == 417, 'actual 417-byte CODE contribution at original function address')
        allocations.append(rows[0])
        vectors.append(vector)
    need(vectors[0] == vectors[1], 'both complete OBJ/EXE/MAP candidate vectors repeat')
    return dict(complete=True, selected_build_sha256=digest,
        review_driver_sha256=sha((b.ROOT / 'scripts/review_th03_mainl_input_scan_work.py').read_bytes()),
        source=config['source'], instruction_scope_exact=True, instruction_bytes=417,
        literal_ordered_fields=42, native_rounds=2, raw_outputs_per_round=3, native_writer_phases=4,
        body_sha256=record['rounds'][0]['scope']['body_sha256'], native_allocations=allocations,
        unowned_following_byte=0x90, whole_product_exact=False, whole_product_accepted=False,
        cold_rebuilt=False, runtime_replayed=False, source_acceptance_publication_changed=False,
        canonical_unit_credit_changed=False, active_runtime_root_unchanged=b.runtime.REPORT)


if __name__ == '__main__':
    result = review()
    (b.ROOT / (b.PREFIX + 'review.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
