#!/usr/bin/env python3
"""Review ordered C0 startup fields, entry, true holes and both products."""
import json

import build_th03_runtime_after548_work as b
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import library_members
from lib.pc98 import parse_mz


def review():
    config, attestation = b.inputs()
    parent_review = b.previous.review()
    old, old_hash = b.base.load(b.parent.REPORT)
    _, baseline_hash = b.base.load(b.startup_baseline.REPORT)
    record, digest = b.base.load(b.REPORT)
    op_cold, _, packed_target = b.base.op_context()
    source = (b.ROOT / config['source']).read_bytes()
    original = (b.ROOT / config['original']['path']).read_bytes()
    original_library = (b.ROOT / '.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes()
    need(sha(original_library) == config['original_compiler_library_sha256'], 'real original compiler library')
    originals = library_members(original_library)
    need(record['complete'] and not record['source_acceptance'] and not record['cold_rebuilt'] and
         not record['library_rebuilt'] and not record['packing_rebuilt'] and
         record['authored_game_credit_bytes'] == record['new_source_members'] ==
         record['new_CODE_extent_bytes'] == record['game_objects_recompiled'] == 0 and
         record['fresh_native_outputs_per_round'] == 5 and record['reused_library_outputs_per_round'] == 1 and
         record['CODE_extent'] == 625 and record['initialized_CODE_bytes'] == 623 and
         record['DATA_bytes'] == 144 and record['uninitialized_CODE_bytes'] == 2 and
         record['uninitialized_STACK_bytes'] == 128 and record['ordered_fields_equal'] == 58 and
         record['ordered_PUBLIC_entries_equal'] is False and
         record['driver_sha256'] == sha((b.ROOT / b.DRIVER).read_bytes()) and
         record['parent_build_sha256'] == old_hash and record['parent_review'] == parent_review and
         record['startup_baseline_build_sha256'] == baseline_hash and record['op_cold'] == op_cold and
         record['emitter_attestation'] == attestation and record['source'] == config['source'] and
         record['source_sha256'] == sha(source), 'current source and complete preserved receipt DAG')
    need((b.SCRATCH / 'c0.asm').read_bytes() == source and
         (b.SCRATCH / 'driver.py').read_bytes() == (b.ROOT / b.DRIVER).read_bytes() and
         (b.SCRATCH / 'config.json').read_bytes() == (b.ROOT / b.CONFIG).read_bytes(), 'actual immutable consumed inputs')
    labels = [f'round{i}-{name}' for i in (1, 2) for name in ('assemble', 'mainl-link', 'op-link')]
    need([p['label'] for p in record['phases']] == labels and all(p['returncode'] == 0 and
         p['log_sha256'] == sha((b.ROOT / p['log_path']).read_bytes()) for p in record['phases']),
         'all six successful native writer logs')
    need(len(record['rounds']) == 2, 'two actual native rounds')
    phases = {p['label']: p for p in record['phases']}
    tasm = ['/usr/bin/wine-stable', str(b.ROOT / config['native_tools']['tasm']['path'])]
    dos = ['/usr/bin/wine-stable', str(b.ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    vectors = []
    for number, row in enumerate(record['rounds'], 1):
        need(row['round'] == number and set(row['outputs']) ==
             {'startup', 'lib', 'mainl_exe', 'mainl_map', 'op_exe', 'op_map'}, 'five fresh files and one reused library')
        vector = {n: b.base.checked(meta) for n, meta in row['outputs'].items()}
        comparison = b.scope(original, vector['startup'], config)
        need(row['comparison'] == comparison and not comparison['original_OMF_program_equal'] and
             phases[f'round{number}-assemble']['argv'] == tasm + config['native_flags'] + ['c0.ASM,c0l.obj'],
             'complete raw startup fields/storage, retained PUBLIC difference and actual native assembly')
        need(row['outputs']['lib'] == old['rounds'][number - 1]['outputs']['lib'] and
             vector['lib'] == b.base.checked(old['rounds'][number - 1]['outputs']['lib']), 'actual unchanged library pair')
        materials, responses = {}, {}
        for product, work, scratch, size, relocations in (
            ('mainl', b.base.b.WORK, b.SCRATCH, 67372, 677), ('op', b.base.op.WORK, b.OP_SCRATCH, 63866, 607)):
            # Independently reconstruct actual startup/library/output bindings.
            response = (work / f'obj/th03/{product}.@l').read_bytes()
            for a, z in ((b'c0l.obj', rb'probe\af548h\c0l.obj'),
                         (f'bin\\th03\\{product}.exe'.encode(), f'probe\\af548h\\r{number}.exe'.encode()),
                         (f'obj\\th03\\{product}.map'.encode(), f'probe\\af548h\\r{number}.map'.encode()),
                         (b' crt.lib' if product == 'mainl' else b' cl.lib', f' probe\\af548h\\r{number}.lib'.encode())):
                need(response.count(a) == 1, 'unique native binding')
                response = response.replace(a, z)
            responses[product] = sha(response)
            need((scratch / f'r{number}.lnk').read_bytes() == response and
                 (scratch / f'r{number}.lib').read_bytes() == vector['lib'] and
                 (scratch / 'c0l.obj').read_bytes() == vector['startup'] and
                 phases[f'round{number}-{product}-link']['argv'] == dos + ['tlink', f'@probe\\af548h\\r{number}.lnk'],
                 'actual consumed new C0 and unchanged source library')
            exe, mapping = vector[product + '_exe'], vector[product + '_map']
            need(exe == b.base.checked(old['rounds'][number - 1]['outputs'][product + '_exe']) ==
                 (work / f'bin/th03/{product}.target.exe').read_bytes() and
                 mapping == b.base.checked(old['rounds'][number - 1]['outputs'][product + '_map']), 'full original EXE / prior MAP ' + product)
            mz = parse_mz(exe)
            need(mz.valid and len(exe) == size and len(mz.relocations) == relocations, 'whole original MZ and ordered entries')
            materials[product] = b.base.material_scope(mapping, originals, library_members(vector['lib']))
        need(row['response_sha256'] == responses and row['material_scopes'] == materials and
             row['reused_packed_op'] == old['rounds'][number - 1]['reused_packed_op'] and
             b.base.checked(row['reused_packed_op']) == packed_target, 'selected ownership and actual retained packed proof')
        vectors.append(vector)
    need(vectors[0] == vectors[1], 'both five-file fresh vectors and unchanged library repeat')
    return dict(complete=True, selected_build_sha256=digest,
        review_driver_sha256=sha((b.ROOT / 'scripts/review_th03_runtime_after548_work.py').read_bytes()),
        source=config['source'], native_rounds=2, fresh_native_outputs_per_round=5,
        reused_library_outputs_per_round=1, native_writer_phases=6, source_bound_library_slots=893,
        initialized_CODE_bytes=623, DATA_bytes=144, uninitialized_CODE_sites=[621, 622], uninitialized_STACK_bytes=128,
        literal_ordered_fields_equal=58, literal_entry_segment_import_records_equal=True,
        PUBLIC_packet_multiset_equal=True, literal_ordered_PUBLIC_entries_equal=False,
        original_OMF_program_equal=False, every_initialized_byte_written_once=True,
        complete_original_EXEs_equal=True, both_complete_prior_MAPs_equal=True,
        original_packed_OP_proof_reused=True, library_rebuilt=False, cold_rebuilt=False,
        game_objects_recompiled=0, new_source_member_credit=0, authored_game_credit_bytes=0,
        whole_product_source_acceptance=False)


if __name__ == '__main__':
    result = review()
    (b.ROOT / (b.PREFIX + 'review.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
