#!/usr/bin/env python3
"""Read-only independent review of two real MAINL far-vector native rounds."""
import json

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
import build_th03_mainl_vector_work as b
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets


def review():
    cfg,cfg_sha=b.inputs()
    record,report_sha=b.base.load(b.REPORT)
    prior,parent_sha=b.base.load(b.parent.REPORT)
    original=(b.WORK/cfg['cold_object']).read_bytes()
    source=(b.ROOT/cfg['source']).read_bytes()
    transport=b.source_snapshot()
    expected=payload(original)
    need(prior['complete'] and parent_sha==cfg['parent_report_sha256'],
         'native source DATA after556 parent actually complete')
    need(record['complete'] and record['cold_rebuilt'] is False and
         record['game_objects_recompiled']==1 and record['library_rebuilt'] is False and
         record['source_acceptance'] is False and record['whole_product_accepted'] is False and
         record['canonical_credit_changed'] is False and
         (record['function_CODE_bytes'],record['emitter_alignment_bytes'])==(159,1) and
         record['config_sha256']==cfg_sha and record['parent_report_sha256']==parent_sha and
         record['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         record['source_sha256']==sha(source) and
         record['transported_source_sha256']==sha(transport) and
         record['wrapper_sha256']==sha(b.wrapper()) and
         record['original_object_sha256']==sha(original),
         'no new product/canonical claims; all maintained source and native parent pins')
    need((b.SCRATCH/'vector_body.asm').read_bytes()==transport and
         (b.SCRATCH/'vector_far.asm').read_bytes()==b.wrapper() and
         (b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes() and
         (b.SCRATCH/'driver.py').read_bytes()==(b.ROOT/b.DRIVER).read_bytes(),
         'actual native compiler consumed identical maintained source')
    need(len(record['phases'])==4 and all(x['returncode']==0 and
         sha((b.ROOT/x['log']).read_bytes())==x['log_sha256'] for x in record['phases']),
         'both original compiler/linker logs retained and successful')
    need(len(expected)==160 and expected[1,69]==0x90,
         'one real alignment opcode between complete far functions')
    publics=public_offsets(original)
    need(publics=={'VECTOR2': {'offset':0,'segment_index':1,'group_index':0},
                   'VECTOR2_BETWEEN_PLUS': {'offset':70,'segment_index':1,'group_index':0}},
         'original Far vector two-entry ABI')
    function_counts={}
    dec=Cs(CS_ARCH_X86,CS_MODE_16)
    for u in cfg['function_extent']:
        start,size=u['offset'],u['size']
        native=bytes(expected[1,start+i] for i in range(size))
        insns=list(dec.disasm(native,0))
        need(sum(i.size for i in insns)==size and
             insns[0].mnemonic=='push' and insns[-1].mnemonic=='retf',
             'entire code instruction span, no data/code overlap '+u['name'])
        function_counts[u['name']]=len(insns)
    vectors=[]
    for number,row in enumerate(record['rounds'],1):
        before=prior['rounds'][number-1]
        need(row['round']==number and row['response_sha256']==sha(b.response(number)) and
             row['reused']==before['reused'] and row['reused_banks']==before['reused_banks'] and
             row['reused_root']==before['outputs']['obj'],
             'real parent link, same C0/CRT/root/text/picture order')
        v={key:b.base.checked(pin) for key,pin in row['outputs'].items()}
        need(payload(v['obj'])==expected and
             literal_fields(v['obj'])==literal_fields(original) and
             len(literal_fields(v['obj']))==5 and
             public_offsets(v['obj'])==publics and
             b.module_metadata(v['obj'])==b.module_metadata(original),
             'whole 160-byte function and native even alignment, literal fixups and other OMF')
        need(v['exe']==b.base.checked(before['outputs']['exe']) and
             b.map_normalized(v['map'])==b.parent.map_normalize(b.base.checked(before['outputs']['map'])),
             'full original decoded image and normal MAP layout')
        need(v['exe'][:2]==b'MZ' and len(v['exe'])==67372 and
             int.from_bytes(v['exe'][6:8],'little')==677,
             'MZ image and original relocation count unchanged')
        vectors.append(v)
    need(len(vectors)==2 and vectors[0]==vectors[1], 'two raw OBJ/EXE/MAP vectors exactly repeat')
    return dict(complete=True,native_rounds=2,complete_functions=2,
        original_far_CODE_function_bytes=159,compiler_alignment_bytes=1,
        assembly_statements_source_bound=True,instruction_counts=function_counts,
        ordered_native_FIXUPP_fields=5,original_OMF_PUBLICs=publics,
        complete_original_MZ_EXE_equal=True,decoded_EXE_bytes=67372,original_MZ_relocation_count=677,
        whole_game_source_closure=False,canonical_factory_acceptance=False,
        native_build_report_sha256=report_sha)

if __name__=='__main__':
    result=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('Both far vector procedures 69+90 code and native EVEN alignment rebuilt in two rounds; full MAINL EXE original-exact.')
