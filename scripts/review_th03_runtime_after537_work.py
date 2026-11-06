#!/usr/bin/env python3
"""Read-only review of actual shared exec/CRT adoption in MAINL and OP."""
import json

import build_th03_runtime_after537_work as b
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import library_members, compare_members
from lib.pc98 import parse_mz


def review():
    parent = b.parent_review.review()
    old, old_hash = b.load(b.parent.REPORT)
    startup, startup_hash = b.load(b.parent.parent.REPORT)
    config, config_hash = b.load(b.CONFIG)
    r, receipt_hash = b.load(b.REPORT)
    op_cold, op_files, packed_target = b.op_context()
    original_raw = (b.ROOT / '.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes()
    original_members = library_members(original_raw)
    original = b.b.original_library_member(original_members[config['exec_slot']])
    source = (b.ROOT / config['source']).read_bytes()
    need(r['complete'] and not r['source_acceptance'] and not r['cold_rebuilt'] and
         r['new_source_members'] == r['new_CODE_extent_bytes'] == r['game_objects_recompiled'] == 0 and
         r['corrected_initialized_CODE_bytes'] == 255 and r['corrected_literal_frames'] == 4 and
         r['driver_sha256'] == sha((b.ROOT / b.DRIVER).read_bytes()) and
         r['config_sha256'] == config_hash and r['source_sha256'] == sha(source) and
         r['parent_build_sha256'] == old_hash and r['parent_review'] == parent and
         r['startup_build_sha256'] == startup_hash and r['op_cold'] == op_cold and
         sha(original_raw) == config['original_compiler_library_sha256'] and
         original_members[config['exec_slot']].name == 'exec',
         'current real-library provenance and complete shared/live-source binding')
    need((b.SCRATCH / 'exec.asm').read_bytes() == source and
         (b.SCRATCH / 'driver.py').read_bytes() == (b.ROOT / b.DRIVER).read_bytes() and
         (b.SCRATCH / 'config.json').read_bytes() == (b.ROOT / b.CONFIG).read_bytes(),
         'immutable native consumed source and recipe')
    labels = ['extract'] + [f'round{i}-{p}' for i in (1, 2) for p in
        ('exec', 'library', 'mainl-link', 'op-link', 'op-pack', 'op-restore')]
    need([p['label'] for p in r['phases']] == labels and all(
        p['returncode'] == (1 if p['label'].endswith(('op-pack', 'op-restore')) else 0) and
        p['log_sha256'] == sha((b.ROOT / p['log_path']).read_bytes()) for p in r['phases']),
        'actual complete successful TASM/TLIB/TLINK/DIET native phases')
    vectors, scopes = [], None
    need(len(r['rounds']) == 2, 'two complete native rounds')
    for number, row in enumerate(r['rounds'], 1):
        need(row['round'] == number and set(row['outputs']) ==
             {'exec', 'lib', 'mainl_exe', 'mainl_map', 'op_exe', 'op_map', 'op_packed'},
             'complete unmodified original native output vector')
        v = {k: b.checked(q) for k, q in row['outputs'].items()}
        need(row['exec_scope'] == b.exec_scope(original, v['exec'], config),
             'full original 931-byte initialization and literal ordered 21-field scope')
        old_lib = b.checked(old['rounds'][number - 1]['outputs']['lib'])
        need(row['library_comparison'] == compare_members(library_members(old_lib),
             library_members(v['lib']), {'exec': v['exec']}) and
             row['library_comparison']['contextual_members_unchanged'] == 892,
             'one genuine refinement and all 892 other source programs unchanged')
        c0 = b.checked(startup['rounds'][number - 1]['outputs']['startup'])
        need((b.SCRATCH / 'c0l.obj').read_bytes() == (b.OP_SCRATCH / 'c0l.obj').read_bytes() == c0,
             'same retained source-generated large-model startup in both products')
        materials = {}
        for product, work, scratch, size, relocs in (
            ('mainl', b.b.WORK, b.SCRATCH, 67372, 677), ('op', b.op.WORK, b.OP_SCRATCH, 63866, 607)):
            response = (work / f'obj/th03/{product}.@l').read_bytes()
            for a, z in ((b'c0l.obj', rb'probe\af537d\c0l.obj'),
                         (f'bin\\th03\\{product}.exe'.encode(), f'probe\\af537d\\r{number}.exe'.encode()),
                         (f'obj\\th03\\{product}.map'.encode(), f'probe\\af537d\\r{number}.map'.encode()),
                         (b' crt.lib' if product == 'mainl' else b' cl.lib',
                          f' probe\\af537d\\r{number}.lib'.encode())):
                need(response.count(a) == 1, 'unique independently reviewed link substitution')
                response = response.replace(a, z)
            phase, = [p for p in r['phases'] if p['label'] == f'round{number}-{product}-link']
            need((scratch / f'r{number}.lnk').read_bytes() == response and
                 phase['argv'][-2:] == ['tlink', f'@probe\\af537d\\r{number}.lnk'],
                 'actual linker consumes the explicit source-generated C0 and CRT paths')
            exe, mapping = v[product + '_exe'], v[product + '_map']
            need(exe == (work / f'bin/th03/{product}.target.exe').read_bytes() and
                 (scratch / f'r{number}.exe').read_bytes() == exe and
                 (scratch / f'r{number}.map').read_bytes() == mapping and
                 (scratch / f'r{number}.lib').read_bytes() == v['lib'],
                 'actual consumed source library and complete original ' + product + ' EXE')
            mz = parse_mz(exe)
            need(mz.valid and len(exe) == size and len(mz.relocations) == relocs,
                 'complete original ' + product + ' MZ and literal ordered relocations')
            materials[product] = b.material_scope(mapping, original_members, library_members(v['lib']))
        need(materials == row['material_scopes'] and
             materials['op']['selected_members'] == config['OP_selected_members'] and
             materials['op']['totals'] == config['OP_material_totals'],
             'all actual selected material extents equal real compiler-library initialization/flags')
        mainl_map = b.checked(old['rounds'][number - 1]['outputs']['map'])
        need(v['mainl_map'] == mainl_map and row['map_reviews']['mainl'] ==
             dict(raw_equal_to_after536=True, sha256=sha(mainl_map), bytes=len(mainl_map)) and
             row['map_reviews']['op'] == b.op_map_review((b.op.WORK / 'obj/th03/op.map').read_bytes(), v['op_map']),
             'entire native MAPs and explicitly bounded zero-BSS differences')
        need(v['op_packed'] == packed_target and
             (b.OP_SCRATCH / f'p{number}/OP.EXE').read_bytes() == v['op_exe'],
             'complete original packed OP and actual DIET roundtrip')
        vectors.append(v)
        scopes = materials
    need(vectors[0] == vectors[1], 'all seven whole native outputs repeat byte-for-byte')
    return dict(complete=True, selected_build_sha256=receipt_hash,
        review_driver_sha256=sha((b.ROOT / 'scripts/review_th03_runtime_after537_work.py').read_bytes()),
        shared_source=config['source'], native_rounds=2, cold_rebuilt=False,
        restored_exec_initialized_work_bytes=255, original_exec_literal_ordered_fields=21,
        original_exec_all_initialized_bytes_equal=True, original_exec_all_literal_fields_equal=True,
        native_CRT_slots=893, new_source_member_credit=0, new_CODE_extent_credit=0,
        MAINL_selected_CRT_members=len(scopes['mainl']['selected_members']),
        MAINL_material_totals=scopes['mainl']['totals'], OP_selected_CRT_members=76,
        OP_material_totals=scopes['op']['totals'], MAINL_EXE_and_after536_MAP_raw_equal=True,
        OP_decoded_and_canonical_packed_raw_equal=True, OP_MAP_reviewed_zero_BSS_rows=2,
        game_objects_recompiled=0, all_original_OMF_records_equal=False,
        whole_product_source_acceptance=False)


if __name__ == '__main__':
    result = review()
    (b.ROOT / (b.PREFIX + 'review.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
