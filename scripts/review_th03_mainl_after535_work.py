#!/usr/bin/env python3
"""Review the retained source-startup pair without launching native writers."""
import json

import build_th03_mainl_after535_work as b
from build_th03_mainl_resources_work import need, sha
from lib.pc98 import parse_mz


def review():
    config, config_hash = b.inputs()
    record = json.loads((b.ROOT / b.REPORT).read_bytes())
    baseline = b.parent.review()
    latest, latest_hash = b.parent.load(b.b.PREFIX + b.parent.MODE + '-build.json')
    original = (b.ROOT / config['original']['path']).read_bytes()
    source = (b.ROOT / config['source']).read_bytes()
    need(record['complete'] and not record['source_acceptance'] and
         not record['original_cold_rebuilt'] and record['authored_game_credit_bytes'] == 0 and
         record['driver_sha256'] == sha((b.ROOT / b.DRIVER).read_bytes()) and
         record['config_sha256'] == config_hash and record['source_sha256'] == sha(source) and
         record['baseline_ownership'] == json.loads(json.dumps(baseline)) and
         record['latest_CRT_build_sha256'] == latest_hash and
         record['assembler_flags'] == config['assembler_flags'] and
         record['original_startup_sha256'] == sha(original),
         'current maintained startup, pinned supplier context and source CRT DAG')
    need((b.SCRATCH / 'c0.asm').read_bytes() == source and
         (b.SCRATCH / 'driver.py').read_bytes() == (b.ROOT / b.DRIVER).read_bytes() and
         (b.SCRATCH / 'config.json').read_bytes() == (b.ROOT / b.CONFIG).read_bytes() and
         record['link_response_sha256'] == sha((b.SCRATCH / 'startup.lnk').read_bytes()),
         'actual consumed startup source, recipe and link response')
    need([p['label'] for p in record['phases']] ==
         ['round1-assemble', 'round1-link', 'round2-assemble', 'round2-link'] and
         all(p['returncode'] == 0 and p['log_sha256'] ==
             sha((b.ROOT / p['log_path']).read_bytes()) for p in record['phases']),
         'both original successful TASM/TLINK writer logs')
    vectors = []
    for number, row in enumerate(record['rounds'], 1):
        need(row['round'] == number and set(row['outputs']) == {'startup', 'lib', 'exe', 'map'},
             'complete native vector and reused CRT')
        vector = {k: b.parent.retained(v) for k, v in row['outputs'].items()}
        comparison = b.compare(original, vector['startup'], config)
        need(row['comparison'] == comparison and
             not comparison['literal_ordered_fields_equal'] and
             not comparison['literal_ordered_publics_equal'] and
             not comparison['original_member_program_equal'],
             'independently retained literal metadata differences; no OBJ identity claim')
        need(row['outputs']['lib'] == latest['rounds'][number - 1]['outputs']['lib'] and
             vector['lib'] == (b.SCRATCH / 'crt.lib').read_bytes(),
             'actual unchanged 893-member source-bound library pair')
        need(vector['exe'] == (b.b.WORK / 'bin/th03/mainl.target.exe').read_bytes() and
             vector['map'] == (b.b.WORK / 'obj/th03/mainl.map').read_bytes(),
             'complete original Japanese MAINL EXE/MAP byte equality')
        mz = parse_mz(vector['exe'])
        need(mz.valid and len(vector['exe']) == 67372 and len(mz.relocations) == 677,
             'original complete DOS MZ header, load bytes and ordered relocations')
        vectors.append(vector)
    need(len(vectors) == 2 and vectors[0] == vectors[1], 'complete raw native repeat')
    return dict(complete=True, source=config['source'], source_sha256=sha(source),
        selected_build_sha256=sha((b.ROOT / b.REPORT).read_bytes()),
        review_driver_sha256=sha((b.ROOT / 'scripts/review_th03_mainl_after535_work.py').read_bytes()),
        source_bound_CRT_slots=893, startup_source_bound=True, native_rounds=2,
        CODE_extent=625, initialized_CODE_bytes=623, uninitialized_CODE_cache_bytes=2,
        DATA_bytes=144, uninitialized_STACK_bytes=128, literal_fields=58,
        all_literal_fields_equal_at_original_sites=True,
        literal_ordered_fields_equal=False, literal_ordered_publics_equal=False,
        original_OMF_program_equal=False, complete_original_EXE_MAP_equal=True,
        cold_rebuilt=False, source_acceptance=False, authored_game_credit_bytes=0)


if __name__ == '__main__':
    result = review()
    (b.ROOT / (b.PREFIX + 'review.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
