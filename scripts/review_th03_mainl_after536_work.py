#!/usr/bin/env python3
"""Review baseline refinements, retaining the literal native MAP tie change."""
import json

import build_th03_mainl_after536_work as b
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import library_members, compare_members
from lib.pc98 import parse_mz


def review():
    baseline = b.parent_review.review()
    old, old_hash = b.parent.parent.load(b.parent.REPORT)
    record = json.loads((b.ROOT / b.REPORT).read_bytes())
    original, compiler_hash = b.originals()
    config, attestation = b.emitter()
    need(record['complete'] and not record['source_acceptance'] and not record['cold_rebuilt'] and
         record['new_source_members'] == record['new_CODE_bytes'] == 0 and
         record['driver_sha256'] == sha((b.ROOT / b.DRIVER).read_bytes()) and
         record['parent_build_sha256'] == old_hash and record['parent_review'] == baseline and
         record['emitter_attestation'] == attestation and
         record['original_compiler_library_sha256'] == compiler_hash and
         record['source_paths'] == b.SOURCES and
         record['source_sha256'] == {n: sha((b.ROOT / p).read_bytes()) for n, p in b.SOURCES.items()} and
         record['source_include_sha256'] == {p: sha((b.ROOT / p).read_bytes()) for p in b.INCLUDES},
         'current source/include/native-emitter and unchanged parent-source DAG')
    for name, path in b.SOURCES.items():
        need((b.SCRATCH / (name + '.asm')).read_bytes() == (b.ROOT / path).read_bytes(),
             'actual consumed refined source ' + name)
    for path in b.INCLUDES:
        need((b.SCRATCH / b.Path(path).name).read_bytes() == (b.ROOT / path).read_bytes(),
             'actual consumed original error-data include')
    need((b.SCRATCH / 'driver.py').read_bytes() == (b.ROOT / b.DRIVER).read_bytes() and
         (b.SCRATCH / 'profile.toml').read_bytes() == (b.ROOT / b.PROFILE).read_bytes(),
         'retained immutable native recipe')
    phases = ['extract'] + [f'round{i}-{p}' for i in (1, 2)
                           for p in ('h_padd', 'ioerror', 'library', 'link')]
    need([p['label'] for p in record['phases']] == phases and
         all(p['returncode'] == 0 and p['log_sha256'] ==
             sha((b.ROOT / p['log_path']).read_bytes()) for p in record['phases']),
         'actual native extraction, assembly, library and linker writer logs')
    vectors = []
    for number, row in enumerate(record['rounds'], 1):
        prior = {k: b.parent.parent.retained(v) for k, v in old['rounds'][number - 1]['outputs'].items()}
        need(row['round'] == number and set(row['outputs']) == set(b.SOURCES) | {'lib', 'exe', 'map'},
             'complete raw native vector')
        vector = {k: b.parent.parent.retained(v) for k, v in row['outputs'].items()}
        comparisons = {n: b.compare(n, original[n], vector[n]) for n in b.SOURCES}
        need(row['comparison'] == json.loads(json.dumps(comparisons)),
             'complete independently enumerated original/native profiles and literal gaps')
        library = compare_members(library_members(prior['lib']), library_members(vector['lib']),
                                  {n: vector[n] for n in b.SOURCES})
        need(row['library_comparison'] == library and library['contextual_members_unchanged'] == 891 and
             (b.SCRATCH / 'base.lib').read_bytes() == prior['lib'] and
             (b.SCRATCH / 'c0l.obj').read_bytes() == prior['startup'],
             'all 893 source-bound member positions and original source-generated C0')
        need(row['map_review'] == b.map_review(prior['map'], vector['map']) and
             row['link_response_sha256'] == sha((b.SCRATCH / f'r{number}.lnk').read_bytes()) and
             row['library_response_sha256'] == sha((b.SCRATCH / f'r{number}.rsp').read_bytes()),
             'actual MAP/response files; exact alias exchange and zero-extent BSS owner')
        need(vector['exe'] == prior['exe'] == (b.b.WORK / 'bin/th03/mainl.target.exe').read_bytes(),
             'complete original decoded Japanese EXE equality')
        mz = parse_mz(vector['exe'])
        need(mz.valid and len(vector['exe']) == 67372 and len(mz.relocations) == 677,
             'complete original image and ordered MZ relocation table')
        vectors.append(vector)
    need(len(vectors) == 2 and vectors[0] == vectors[1], 'two actual raw native rounds repeat')
    return dict(complete=True, selected_build_sha256=sha((b.ROOT / b.REPORT).read_bytes()),
        review_driver_sha256=sha((b.ROOT / 'scripts/review_th03_mainl_after536_work.py').read_bytes()),
        source_bound_CRT_slots=893, new_source_members=0, new_CODE_bytes=0,
        native_rounds=2, refined_CODE_bytes=178, refined_DATA_bytes=91,
        complete_original_EXE_equal=True, original_ordered_MZ_relocations=677,
        all_original_segment_group_and_public_ownership_equal=True,
        h_padd_original_ordered_PUBLIC_payload_equal=True,
        ioerror_original_literal_GROUP_equal=True,
        ioerror_literal_ordered_FIXUPP_equal=False,
        all_MAP_addresses_sizes_flags_and_other_bytes_equal=True,
        MAP_raw_equal_to_historical_baseline=False,
        MAP_changes=['F_PADD@/PADD@ display order at shared address 0000:3182',
                     'Zero-sized ioerror _BSS owner at existing address 0E3F:286A'],
        cold_rebuilt=False, source_acceptance=False)


if __name__ == '__main__':
    result = review()
    (b.ROOT / (b.PREFIX + 'review.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
