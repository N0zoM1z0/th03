#!/usr/bin/env python3
"""Read-only review of two native links of four original sound C/C++ modules."""
import json

import build_th03_mainl_sound_after558_work as b
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets


def review():
    cfg,cfg_sha=b.inputs()
    record,report_sha=b.base.load(b.REPORT)
    parent,parent_sha=b.base.load(b.parent.REPORT)
    sources={u['source']:(b.ROOT/u['source']).read_bytes() for u in cfg['units']}
    originals={u['module']:(b.WORK/u['original_object']).read_bytes() for u in cfg['units']}
    need(parent['complete'] and parent_sha==cfg['parent_report_sha256'],
         'actual native after557 vector parent')
    need(record['complete'] and record['source_acceptance'] is False and
         record['whole_product_accepted'] is False and
         record['canonical_credit_changed'] is False and
         record['cold_rebuilt'] is False and record['library_rebuilt'] is False and
         record['game_objects_recompiled']==4 and
         record['sound_function_instruction_bytes']==124 and
         record['historical_contextual_tail_bytes']==4 and
         record['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         record['config_sha256']==cfg_sha and
         record['parent_report_sha256']==parent_sha and
         record['source_sha256']=={k:sha(raw) for k,raw in sources.items()} and
         record['original_sha256']=={k:sha(raw) for k,raw in originals.items()},
         'all source-native producer contracts and current parent')
    need((b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes() and
         (b.SCRATCH/'driver.py').read_bytes()==(b.ROOT/b.DRIVER).read_bytes(),
         'exact native source producer and configuration')
    for u in cfg['units']:
        name=u['source'].rsplit('/',1)[-1]
        need((b.SCRATCH/name).read_bytes()==b.native_src(sources[u['source']]) and
             (b.SCRATCH/u['module']).read_bytes()==b.wrapper(u),
             'real Borland compiled source and GAME/BINARY wrapping '+name)
    phase_names=[
        x for number in (1,2)
        for x in ([f'round{number}-{u["module"].rsplit(".",1)[0]}-compile' for u in cfg['units']] +
                  [f'round{number}-link'])
    ]
    need([p['label'] for p in record['phases']]==phase_names and
         len(record['phases'])==10 and all(p['returncode']==0 and
         sha((b.ROOT/p['log']).read_bytes())==p['log_sha256'] for p in record['phases']),
         'all ten successful native compiler/linker logs retained')
    vectors=[]
    total_fields=0
    for number,row in enumerate(record['rounds'],1):
        old=parent['rounds'][number-1]
        need(row['round']==number and row['response_sha256']==sha(b.response(number)) and
             row['reused']==old['reused'] and row['reused_banks']==old['reused_banks'] and
             row['reused_root']==old['reused_root'] and
             row['reused_vector']==old['outputs']['obj'],
             'original normal link response and root/C0/CRT/vector inputs')
        native={name:b.base.checked(pin) for name,pin in row['outputs'].items()}
        for u in cfg['units']:
            name=u['module'].rsplit('.',1)[0]
            prop=b.obj_equivalent(native[name],originals[u['module']],u['CODE_bytes'])
            need(prop==row['object_properties'][name],
                 'complete original CODE payload, literal fields and PUBLICs '+name)
        need(native['exe']==b.base.checked(old['outputs']['exe']) and
             b.map_normalized(native['map'])==
             b.parent.map_normalized(b.base.checked(old['outputs']['map'])),
             'entire decoded MZ EXE and original normal native link MAP')
        need(native['exe'][:2]==b'MZ' and len(native['exe'])==67372 and
             int.from_bytes(native['exe'][6:8],'little')==677,
             'whole original MZ including 677 relocations')
        total_fields=sum(len(literal_fields(originals[u['module']])) for u in cfg['units'])
        vectors.append(native)
    need(len(vectors)==2 and vectors[0]==vectors[1], 'all six raw OMF/EXE/MAP outputs repeat')
    need(sum(u['CODE_bytes'] for u in cfg['units'])==128 and total_fields==10,
         'four complete C/C++ module code contributions and all ten literal fields')
    return dict(complete=True,native_rounds=2,sound_C_CPP_functions=4,
        original_function_instruction_bytes=124,historical_codestring_tail_bytes=4,
        original_CODE_allocation_bytes=128,literal_native_fixups=10,
        full_original_decoded_EXE_equal=True,original_MZ_bytes=67372,
        original_MZ_ordered_relocations=677,
        whole_product_source_accepted=False,canonical_factory_acceptance=False,
        native_source_report_sha256=report_sha)


if __name__=='__main__':
    value=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(value,indent=2)+'\n')
    print('Four original C/C++ sound functions: 124 instruction bytes, 4 historic tails, two exact native links.')
