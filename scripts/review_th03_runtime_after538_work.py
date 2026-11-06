#!/usr/bin/env python3
"""Review five shared runtime refinements without native or runtime replay."""
import json

import build_th03_runtime_after538_work as b
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import library_members, compare_members
from lib.pc98 import parse_mz


def review():
    config, attestation = b.inputs()
    parent_review = b.previous.review()
    parent, parent_hash = b.base.load(b.base.REPORT)
    startup, startup_hash = b.base.load(b.base.parent.parent.REPORT)
    record, receipt_hash = b.base.load(b.REPORT)
    op_cold, _, packed_target = b.base.op_context()
    original_raw = (b.ROOT / '.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes()
    originals = library_members(original_raw)
    need(record['complete'] and not record['source_acceptance'] and not record['cold_rebuilt'] and
         record['new_source_members'] == record['new_CODE_extent_bytes'] == record['game_objects_recompiled'] == 0 and
         record['corrected_near_frames'] == 10 and record['corrected_group_memberships'] == 1 and
         record['driver_sha256'] == sha((b.ROOT / b.DRIVER).read_bytes()) and
         record['parent_build_sha256'] == parent_hash and record['parent_review'] == parent_review and
         record['startup_build_sha256'] == startup_hash and record['op_cold'] == op_cold and
         record['emitter_attestation'] == attestation and record['source_paths'] == config['source_paths'] and
         record['source_sha256'] == {n: sha((b.ROOT / p).read_bytes()) for n, p in config['source_paths'].items()} and
         record['include_sha256'] == {p: sha((b.ROOT / p).read_bytes()) for p in config['includes']} and
         sha(original_raw) == config['original_compiler_library_sha256'],
         'complete unchanged source/DAG and real compiler-library identity')
    for n, p in config['source_paths'].items():
        need((b.SCRATCH / (n + '.asm')).read_bytes() == (b.ROOT / p).read_bytes(), 'actual consumed source ' + n)
    for p in config['includes']:
        need((b.SCRATCH / b.Path(p).name).read_bytes() == (b.ROOT / p).read_bytes(), 'actual consumed include')
    need((b.SCRATCH / 'driver.py').read_bytes() == (b.ROOT / b.DRIVER).read_bytes() and
         (b.SCRATCH / 'config.json').read_bytes() == (b.ROOT / b.CONFIG).read_bytes(), 'immutable native recipe')
    labels = ['extract'] + [f'round{i}-{p}' for i in (1, 2) for p in
        (*config['compatible_members'], 'setblock', 'library', 'mainl-link', 'op-link')]
    need([p['label'] for p in record['phases']] == labels and all(p['returncode'] == 0 and
         p['log_sha256'] == sha((b.ROOT / p['log_path']).read_bytes()) for p in record['phases']),
         'all seventeen successful native assembly/library/linker phases')
    vectors = []
    need(len(record['rounds']) == 2, 'two original native rounds')
    for number, row in enumerate(record['rounds'], 1):
        need(row['round'] == number and set(row['outputs']) == set(config['source_paths']) |
             {'lib', 'mainl_exe', 'mainl_map', 'op_exe', 'op_map'}, 'all ten whole raw outputs per round')
        vector = {n: b.base.checked(meta) for n, meta in row['outputs'].items()}
        scopes = {n: b.scope(b.base.b.original_library_member(originals[config['slots'][n]]),
                            vector[n], n, config) for n in config['source_paths']}
        need(row['scopes'] == json.loads(json.dumps(scopes)), 'complete literal original/native scopes and order gaps')
        old_lib = b.base.checked(parent['rounds'][number - 1]['outputs']['lib'])
        comparison = compare_members(library_members(old_lib), library_members(vector['lib']),
                                     {n: vector[n] for n in config['source_paths']})
        need(row['library_comparison'] == comparison and comparison['contextual_members_unchanged'] == 888 and
             (b.SCRATCH / 'base.lib').read_bytes() == old_lib and
             row['library_response_sha256'] == sha((b.SCRATCH / f'r{number}.rsp').read_bytes()),
             'all 893 ordered source slots and other 888 native programs unchanged')
        c0 = b.base.checked(startup['rounds'][number - 1]['outputs']['startup'])
        materials = {}
        for product, work, scratch, size, relocs in (
            ('mainl', b.base.b.WORK, b.SCRATCH, 67372, 677), ('op', b.base.op.WORK, b.OP_SCRATCH, 63866, 607)):
            response = (work / f'obj/th03/{product}.@l').read_bytes()
            for a, z in ((b'c0l.obj', rb'probe\af538l\c0l.obj'),
                         (f'bin\\th03\\{product}.exe'.encode(), f'probe\\af538l\\r{number}.exe'.encode()),
                         (f'obj\\th03\\{product}.map'.encode(), f'probe\\af538l\\r{number}.map'.encode()),
                         (b' crt.lib' if product == 'mainl' else b' cl.lib', f' probe\\af538l\\r{number}.lib'.encode())):
                need(response.count(a) == 1, 'unique reviewed source startup/runtime link path')
                response = response.replace(a, z)
            phase, = [p for p in record['phases'] if p['label'] == f'round{number}-{product}-link']
            need((scratch / f'r{number}.lnk').read_bytes() == response and
                 row['response_sha256'][product] == sha(response) and
                 phase['argv'][-2:] == ['tlink', f'@probe\\af538l\\r{number}.lnk'] and
                 (scratch / 'c0l.obj').read_bytes() == c0 and
                 (scratch / f'r{number}.lib').read_bytes() == vector['lib'], 'actual consumed source C0/CRT and native command')
            exe, mapping = vector[product + '_exe'], vector[product + '_map']
            need(exe == b.base.checked(parent['rounds'][number - 1]['outputs'][product + '_exe']) ==
                 (work / f'bin/th03/{product}.target.exe').read_bytes(), 'complete original ' + product + ' EXE')
            mz = parse_mz(exe)
            need(mz.valid and len(exe) == size and len(mz.relocations) == relocs, 'whole original MZ/ordered relocations')
            materials[product] = b.base.material_scope(mapping, originals, library_members(vector['lib']))
        need(materials == row['material_scopes'], 'all selected initialized/uninitialized storage and MAP ownership')
        old_map = b.base.checked(parent['rounds'][number - 1]['outputs']['mainl_map'])
        need(row['map_reviews']['mainl'] == b.mainl_map_review(old_map, vector['mainl_map']) and
             vector['op_map'] == (b.base.op.WORK / 'obj/th03/op.map').read_bytes() and
             row['map_reviews']['op'] == dict(raw_equal_to_cold=True, sha256=sha(vector['op_map']), bytes=len(vector['op_map'])),
             'complete OP MAP equality and exactly reviewed MAINL zero-BSS changes')
        need(not record['packing_rebuilt'] and row['reused_packed_op'] ==
             parent['rounds'][number - 1]['outputs']['op_packed'] and
             b.base.checked(row['reused_packed_op']) == packed_target,
             'retained actual packed proof, explicitly not represented as new DIET output')
        vectors.append(vector)
    need(vectors[0] == vectors[1], 'both ten-file raw native vectors repeat')
    return dict(complete=True, selected_build_sha256=receipt_hash,
        review_driver_sha256=sha((b.ROOT / 'scripts/review_th03_runtime_after538_work.py').read_bytes()),
        native_rounds=2, native_output_files_per_round=10, refined_existing_CODE_bytes=1648,
        refined_existing_DATA_bytes=42, literal_fields_at_original_sites=77,
        corrected_near_frames=10, corrected_GROUP_memberships=1,
        all_five_original_import_orders_and_public_ownership_equal=True,
        fully_equal_ordered_members=['execl', 'setblock'],
        remaining_order_gaps=['fbrk', 'write', 'loadprog'],
        both_complete_original_EXEs_equal=True, complete_OP_cold_MAP_equal=True,
        MAINL_MAP_only_reviewed_zero_BSS_rows_changed=True,
        original_packed_OP_proof_reused=True, cold_rebuilt=False, game_objects_recompiled=0,
        new_source_member_credit=0, new_CODE_extent_credit=0, whole_product_source_acceptance=False)


if __name__ == '__main__':
    result = review()
    (b.ROOT / (b.PREFIX + 'review.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
