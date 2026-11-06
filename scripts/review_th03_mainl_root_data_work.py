#!/usr/bin/env python3
"""Verify the retained two native rounds for MAINL root DATA after556."""
import json

import build_th03_mainl_root_data_work as b
from build_th03_mainl_resources_work import need, sha
from build_th03_mainl_display_work import payload, literal_fields
from lib.mainl_owner_migrations import public_offsets


def review():
    cfg, cfg_sha = b.inputs()
    record, report_hash = b.base.load(b.REPORT)
    prior, parent_hash = b.base.load(b.parent.REPORT)
    inputs = b.input_sources(cfg)
    rebuilt_source = b.context()
    source_inls = {name: b.transported(inputs[path]) for name,path in b.BANKS.items()}
    original = (b.WORK/'obj/th03/mainl.obj').read_bytes()
    original_data = payload(original)
    need(prior['complete'] and parent_hash==cfg['parent_report_sha256'], 'actual after555 parent')
    need(record['complete'] and record['source_acceptance'] is False and
         record['whole_product_accepted'] is False and record['canonical_credit_changed'] is False and
         record['cold_rebuilt'] is False and record['game_objects_recompiled']==1 and
         record['library_rebuilt'] is False and
         (record['initialized_source_DATA_bytes'],record['reserved_source_DATA_bytes'],
          record['game_authored_DATA_bytes'],record['library_DATA_bytes']) == (1825,34,900,959) and
         record['source_sha256']=={k:sha(v) for k,v in inputs.items()} and
         record['native_source_sha256']==sha(rebuilt_source) and
         record['config_sha256']==cfg_sha and record['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         record['parent_report_sha256']==parent_hash and
         record['original_object_sha256']==sha(original), 'all actual maintained input bindings')
    need((b.SCRATCH/'th03_mainl.asm').read_bytes()==rebuilt_source and
         all((b.SCRATCH/'banks'/name).read_bytes()==raw for name,raw in source_inls.items()) and
         (b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes() and
         (b.SCRATCH/'driver.py').read_bytes()==(b.ROOT/b.DRIVER).read_bytes(),
         'retained CP932 assembler input and all 13 source banks')
    need(len(record['phases'])==4 and all(x['returncode']==0 and
         sha((b.ROOT/x['log']).read_bytes())==x['log_sha256'] for x in record['phases']),
         'original native assembler and linker logs retained')
    reserved=set(range(0x748,0x768))|set(range(0x782,0x784))
    need(len(reserved)==34 and all((2,n) not in original_data for n in reserved),
         'two genuine initialized-DATA holes, not fake zero initializers')
    covered=set()
    for u in cfg['units']:
        covered |= set(range(u['offset'],u['offset']+u['size']))
    need(len(covered)==1859 and all(x not in covered for x in cfg['uncredited_padding_offsets']),
         'all 16 disjoint source extents, five excluded gap locations')
    raw_vectors=[]
    for number,row in enumerate(record['rounds'],1):
        before=prior['rounds'][number-1]
        need(row['round']==number and row['response_sha256']==sha(b.response(number)) and
             row['reused']==before['reused'] and row['reused_banks']==before['reused_banks'],
             'original normal link order and true source parent inputs')
        native={name:b.base.checked(pin) for name,pin in row['outputs'].items()}
        obj=native['obj']
        need(payload(obj)==original_data and literal_fields(obj)==literal_fields(original) and
             len(literal_fields(obj))==392 and public_offsets(obj)==public_offsets(original) and
             b.parent.structure_without_publics(obj)==b.parent.structure_without_publics(original),
             'complete actual root native OBJ data/fixups/definitions/metadata')
        need(native['exe']==b.base.checked(before['outputs']['exe']) and
             b.map_normalize(native['map'])==b.parent.map_canonical(b.base.checked(before['outputs']['map'])),
             'every byte of original MZ image and full original MAP addresses')
        need(native['exe'][:2]==b'MZ' and len(native['exe'])==67372 and
             int.from_bytes(native['exe'][6:8],'little')==677,
             'actual decoded MZ product and ordered relocation field count')
        raw_vectors.append(native)
    need(len(raw_vectors)==2 and raw_vectors[0]==raw_vectors[1],
         'two full raw OBJ/EXE/MAP native vectors repeat')
    return dict(complete=True, native_rounds=2, source_units=16,
        source_DATA_bytes=1859, source_initialized_DATA_bytes=1825,
        source_reserved_DATA_bytes=34, newly_source_bound_DATA_bytes=963,
        authored_DATA_bytes=900, supplier_DATA_bytes=959, excluded_alignments=5,
        original_root_DATA_allocation_bytes=2036, original_root_BSS_allocation_bytes=5108,
        all392_literal_fields_equal=True, all363_public_definitions_equal=True,
        complete_original_EXE_equal=True, decoded_EXE_bytes=67372, ordered_MZ_relocations=677,
        whole_product_source_accepted=False, canonical_factory_acceptance=False,
        source_native_report_sha256=report_hash)

if __name__=='__main__':
    result=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('Root DATA 1859 bytes/16 extents verified;34 real reserved,5 excluded alignments;two full native rounds EXE original-exact.')
