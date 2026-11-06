#!/usr/bin/env python3
"""Review abort's exact body/ordered fields and two-product native bridge."""
import json

import build_th03_runtime_after539_work as b
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import library_members, compare_members
from lib.pc98 import parse_mz


def review():
    config, attestation = b.inputs()
    parent_review = b.previous.review()
    old, old_hash = b.base.load(b.parent.REPORT)
    startup, startup_hash = b.base.load(b.base.parent.parent.REPORT)
    record, receipt_hash = b.base.load(b.REPORT)
    op_cold, _, packed_target = b.base.op_context()
    original_raw = (b.ROOT / '.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes()
    originals = library_members(original_raw)
    source = (b.ROOT / config['source_paths']['abort']).read_bytes()
    need(record['complete'] and not record['source_acceptance'] and not record['cold_rebuilt'] and
         record['new_source_members'] == record['new_CODE_extent_bytes'] == record['game_objects_recompiled'] == 0 and
         record['refined_existing_CODE_bytes'] == 20 and record['corrected_literal_order_members'] == 1 and
         record['driver_sha256'] == sha((b.ROOT / b.DRIVER).read_bytes()) and
         record['parent_build_sha256'] == old_hash and record['parent_review'] == parent_review and
         record['startup_build_sha256'] == startup_hash and record['op_cold'] == op_cold and
         record['emitter_attestation'] == attestation and record['source_paths'] == config['source_paths'] and
         record['source_sha256'] == sha(source) and
         sha(original_raw) == config['original_compiler_library_sha256'] and
         len(originals) == 893 and originals[2].name == 'abort', 'complete unchanged source/DAG and original library')
    need((b.SCRATCH / 'abort.asm').read_bytes() == source and
         (b.SCRATCH / 'driver.py').read_bytes() == (b.ROOT / b.DRIVER).read_bytes() and
         (b.SCRATCH / 'config.json').read_bytes() == (b.ROOT / b.CONFIG).read_bytes(), 'actual consumed immutable source/recipe')
    labels = ['extract'] + [f'round{i}-{p}' for i in (1, 2) for p in
                            ('abort', 'library', 'mainl-link', 'op-link')]
    need([p['label'] for p in record['phases']] == labels and all(p['returncode'] == 0 and
         p['log_sha256'] == sha((b.ROOT / p['log_path']).read_bytes()) for p in record['phases']),
         'all nine successful native writer phases/logs')
    need(len(record['rounds']) == 2, 'two actual native rounds')
    dos = ['/usr/bin/wine-stable', str(b.ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    tasm = ['/usr/bin/wine-stable', str(b.ROOT / '.analysis/toolchain/wineprefix/drive_c/TASM50/bin/TASM32.EXE')]
    phase = {p['label']: p for p in record['phases']}
    need(phase['extract']['argv'] == dos + ['tlib', '@extract.rsp'], 'actual native extraction command')
    vectors = []
    for number, row in enumerate(record['rounds'], 1):
        need(row['round'] == number and set(row['outputs']) ==
             {'abort', 'lib', 'mainl_exe', 'mainl_map', 'op_exe', 'op_map'}, 'all six complete raw outputs')
        vector = {n: b.base.checked(meta) for n, meta in row['outputs'].items()}
        body_scope = b.scope(b.base.b.original_library_member(originals[2]), vector['abort'], config)
        need(row['scope'] == json.loads(json.dumps(body_scope)), 'raw complete body/storage/PUBLIC/ordered fields')
        old_lib = b.base.checked(old['rounds'][number - 1]['outputs']['lib'])
        members, native_members = library_members(old_lib), library_members(vector['lib'])
        comparison = compare_members(members, native_members, {'abort': vector['abort']})
        rsp = b.base.b.build.response(f'probe\\af539i\\r{number}.lib /E',
                ['+probe\\af539i\\' + m.name + '.obj' for m in members])
        need(row['library_comparison'] == comparison and comparison['contextual_members_unchanged'] == 892 and
             (b.SCRATCH / 'base.lib').read_bytes() == old_lib and
             (b.SCRATCH / f'r{number}.rsp').read_bytes() == rsp and row['library_response_sha256'] == sha(rsp) and
             (b.SCRATCH / 'extract.rsp').read_bytes() ==
             b.base.b.build.response('base.lib', ['*' + m.name for m in members]), '893 ordered slots and actual library responses')
        need(phase[f'round{number}-abort']['argv'] ==
             tasm + config['tasm_flags'] + ['abort.asm,abort.obj'] and
             phase[f'round{number}-library']['argv'] == dos + ['tlib', f'@probe\\af539i\\r{number}.rsp'],
             'actual source assembly and native TLIB commands')
        c0 = b.base.checked(startup['rounds'][number - 1]['outputs']['startup'])
        materials = {}
        for product, work, scratch, size, relocations in (
            ('mainl', b.base.b.WORK, b.SCRATCH, 67372, 677), ('op', b.base.op.WORK, b.OP_SCRATCH, 63866, 607)):
            # Reconstruct the explicit source-C0/runtime paths independently.
            response = (work / f'obj/th03/{product}.@l').read_bytes()
            for a, z in ((b'c0l.obj', rb'probe\af539i\c0l.obj'),
                         (f'bin\\th03\\{product}.exe'.encode(), f'probe\\af539i\\r{number}.exe'.encode()),
                         (f'obj\\th03\\{product}.map'.encode(), f'probe\\af539i\\r{number}.map'.encode()),
                         (b' crt.lib' if product == 'mainl' else b' cl.lib',
                          f' probe\\af539i\\r{number}.lib'.encode())):
                need(response.count(a) == 1, 'unique source C0/CRT/output binding')
                response = response.replace(a, z)
            need((scratch / f'r{number}.lnk').read_bytes() == response and
                 row['response_sha256'][product] == sha(response) and
                 phase[f'round{number}-{product}-link']['argv'] ==
                 dos + ['tlink', f'@probe\\af539i\\r{number}.lnk'] and
                 (scratch / 'c0l.obj').read_bytes() == c0 and
                 (scratch / f'r{number}.lib').read_bytes() == vector['lib'], 'actual consumed native source C0/CRT')
            exe, mapping = vector[product + '_exe'], vector[product + '_map']
            need(exe == b.base.checked(old['rounds'][number - 1]['outputs'][product + '_exe']) ==
                 (work / f'bin/th03/{product}.target.exe').read_bytes() and
                 mapping == b.base.checked(old['rounds'][number - 1]['outputs'][product + '_map']),
                 'whole original EXE and complete unchanged native MAP ' + product)
            mz = parse_mz(exe)
            need(mz.valid and len(exe) == size and len(mz.relocations) == relocations, 'complete original MZ and ordered relocations')
            materials[product] = b.base.material_scope(mapping, originals, native_members)
        audit = b.selected_literal_audit(materials['op']['selected_members'], originals, native_members)
        need(materials == row['material_scopes'] and audit == row['selected_literal_audit'], 'all selected storage/ownership and literal streams')
        need(not record['packing_rebuilt'] and row['reused_packed_op'] == old['rounds'][number - 1]['reused_packed_op'] and
             b.base.checked(row['reused_packed_op']) == packed_target, 'actual retained packing proof; no new DIET run')
        vectors.append(vector)
    need(vectors[0] == vectors[1], 'both complete six-file native vectors repeat')
    return dict(complete=True, selected_build_sha256=receipt_hash,
        review_driver_sha256=sha((b.ROOT / 'scripts/review_th03_runtime_after539_work.py').read_bytes()),
        native_rounds=2, native_output_files_per_round=6, refined_existing_CODE_bytes=20,
        abort_ordered_fields_equal=2, complete_original_EXEs_equal=True, both_complete_prior_MAPs_equal=True,
        selected_OP_literal_equal=58, selected_OP_order_only=18, selected_counts_are_diagnostic_only=True,
        original_packed_OP_proof_reused=True, cold_rebuilt=False, game_objects_recompiled=0,
        new_source_member_credit=0, new_CODE_extent_credit=0, whole_product_source_acceptance=False)


if __name__ == '__main__':
    result = review()
    (b.ROOT / (b.PREFIX + 'review.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
