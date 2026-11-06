#!/usr/bin/env python3
"""Read-only two-round check of natural formula-generated MAINL trig DATA."""
import json

import build_th03_mainl_root_trig_work as b
from build_th03_mainl_resources_work import need, sha
from build_th03_mainl_display_work import payload, literal_fields
from lib.mainl_owner_migrations import public_offsets


def review():
    config, config_sha = b.inputs()
    record, report_sha = b.base.load(b.REPORT)
    prior, prior_sha = b.base.load(b.parent.REPORT)
    source = (b.ROOT / config['source']).read_bytes()
    parts = b.generated(config)
    wrapper = b.context(config, parts)
    original = (b.WORK / 'obj/th03/mainl.obj').read_bytes()
    need(prior['complete'] and prior_sha == config['parent_report_sha256'], 'real after554 parent')
    need(record['complete'] and record['source_acceptance'] is False and
         record['whole_product_accepted'] is False and record['canonical_credit_changed'] is False and
         record['cold_rebuilt'] is False and record['game_objects_recompiled'] == 1 and
         record['library_rebuilt'] is False and record['library_source_DATA_bytes'] == 896 and
         record['source_sha256'] == sha(source) and record['context_sha256'] == sha(wrapper) and
         record['generated_sha256'] == {n:sha(v) for n,v in parts.items()} and
         record['config_sha256'] == config_sha and
         record['driver_sha256'] == sha((b.ROOT / b.DRIVER).read_bytes()) and
         record['parent_report_sha256'] == prior_sha and
         record['original_object_sha256'] == sha(original), 'bound stage inputs and claim limits')
    need((b.SCRATCH / 'th03_mainl.asm').read_bytes() == wrapper and
         all((b.SCRATCH / name).read_bytes() == raw.replace(b'\n',b'\r\n')
             for name,raw in parts.items()), 'retained actual source used by TASM')
    need(len(record['phases']) == 4 and all(row['returncode'] == 0 and
        sha((b.ROOT / row['log']).read_bytes()) == row['log_sha256'] for row in record['phases']),
        'all four retained native writer logs')
    old_data = payload(original)
    table = b.table_bytes(config)
    for extent in config['table_extents']:
        at, size, name = extent['data_offset'], extent['size'], extent['name']
        need(len(table[name]) == size and
             bytes(old_data[2,at+i] for i in range(size)) == table[name],
             'all native table bytes from formula ' + name)
    vectors = []
    for number,row in enumerate(record['rounds'],1):
        need(row['round'] == number and row['response_sha256'] == sha(b.link_response(number)),
             'exact normal link response')
        native = {k:b.base.checked(v) for k,v in row['outputs'].items()}
        before = prior['rounds'][number-1]
        need(row['reused'] == before['reused'] and
             row['reused_banks'] == {k:before['outputs'][k] for k in ('registration','ending')},
             'real source root/C0/CRT/text-bank parents')
        obj = native['obj']
        need(payload(obj) == old_data and literal_fields(obj) == literal_fields(original) and
             len(literal_fields(obj)) == 392 and public_offsets(obj) == public_offsets(original) and
             b.structure_without_publics(obj) == b.structure_without_publics(original),
             'all root initializer bytes, public sites, ordered fields and other OMF metadata')
        need(native['exe'] == b.base.checked(before['outputs']['exe']) and
             b.map_canonical(native['map']) == b.base.checked(before['outputs']['map']),
             'complete original EXE/relocation/MAP coordinates')
        # Actual DOS MZ relocation count (unaltered complete raw file).
        need(native['exe'][:2] == b'MZ' and
             int.from_bytes(native['exe'][6:8], 'little') == 677, 'MZ literal relocation count')
        vectors.append(native)
    need(len(vectors) == 2 and vectors[0] == vectors[1], 'whole native pair repeats')
    return dict(complete=True, source_pinned=True, native_rounds=2, library_table_bytes=896,
                game_code_bytes_claimed=0, root_original_DATA_bytes=2036,
                root_literal_fixups=392, public_symbols=len(public_offsets(original)),
                decoded_original_EXE_bytes=len(vectors[0]['exe']), original_MZ_relocations=677,
                complete_original_EXE_equal=True, whole_product_source_accepted=False,
                canonical_factory_acceptance=False, stage_report_sha256=report_sha)


if __name__ == '__main__':
    result=review()
    (b.ROOT / (b.PREFIX+'review.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('Formula DATA896 native confirmed; complete two-round OBJ/EXE/MAP vectors;392 literal fields;677 MZ relocations.')
