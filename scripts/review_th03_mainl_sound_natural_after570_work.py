#!/usr/bin/env python3
"""Read-only review of four complete natural sound ASM objects and two links."""
import json
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
import build_th03_mainl_sound_natural_after570_work as b
from build_th03_mainl_resources_work import need,sha
from lib.pc98 import parse_mz
from build_th03_mainl_display_work import payload,literal_fields


def review():
    cfg,cfg_sha=b.inputs()
    prev,prev_sha=b.base.load(b.prior.REPORT)
    out,out_sha=b.base.load(b.REPORT)
    source=b.sources(cfg)
    original={s:(b.WORK/f'obj/th02/{s}.obj').read_bytes() for s in b.ORDER}
    need(prev['complete'] and prev_sha==cfg['parent_report_sha256'],
         'real natural registration + root/input/VECTOR/C0/CRT parent')
    need(out['complete'] and out['canonical_credit_changed'] is False and
         out['whole_game_source_accepted'] is False and out['cold_rebuilt'] is False and
         out['library_rebuilt'] is False and out['four_game_objects_recompiled_per_round']==4 and
         out['other_game_objects_reused']==32 and
         (out['native_source_instruction_bytes'],out['native_code_alignment_bytes'])==(124,4) and
         out['parent_report_sha256']==prev_sha and out['config_sha256']==cfg_sha and
         out['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         out['sources_sha256']=={s:sha(raw) for s,raw in source.items()} and
         out['original_objects_sha256']=={s:sha(raw) for s,raw in original.items()},
         'bounded original sound statements and all source/parent/producer hashes')
    for stem,raw in source.items():
        need((b.SCRATCH/f'{stem}.asm').read_bytes()==raw.replace(b'\n',b'\r\n'),
             'actual complete original TASM input from maintained source '+stem)
    need((b.SCRATCH/'driver.py').read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         'native build driver/config staged inputs immutable')
    order=[x for n in (1,2) for x in
           ([f'round{n}-{stem}-assemble' for stem in b.ORDER]+[f'round{n}-link'])]
    need(len(out['phases'])==10 and [x['label'] for x in out['phases']]==order and
         all(x['returncode']==0 and sha((b.ROOT/x['log']).read_bytes())==x['log_sha256']
             for x in out['phases']), 'ten real successful independent native writer phases')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16)
    raw_vectors=[]
    function_counts={}
    for n,row in enumerate(out['rounds'],1):
        before=prev['rounds'][n-1]
        need(row['round']==n and row['link_response_sha256']==sha(b.response(n)) and
             (b.SCRATCH/f'r{n}.lnk').read_bytes()==b.response(n),
             'real original 36-object MAINL link response replaces only four sound modules')
        v={k:b.base.checked(pin) for k,pin in row['outputs'].items()}
        need(set(v)=={stem+'_obj' for stem in b.ORDER}|{'exe','map'},
             'complete six original raw OMF/EXE/MAP native products')
        for u in cfg['sources']:
            stem=u['stem']; raw=v[stem+'_obj']
            scope=b.object_scope(raw,original[stem],u)
            need(row['input_objects_exact'][stem]==scope and
                 (b.SCRATCH/f'{stem}.obj').read_bytes()==raw,
                 'complete TASM original CODE, frame-symbols, field sites and LIVE source evidence '+stem)
            old=payload(original[stem])
            instructions=bytes(old[1,i] for i in range(u['instructions_bytes']))
            decoded=list(decoder.disasm(instructions,0))
            need(sum(x.size for x in decoded)==u['instructions_bytes'] and
                 decoded[-1].mnemonic=='retf' and
                 old[1,u['instructions_bytes']]==0x90 and
                 scope['natural_TASM_CODE_even_bytes']==1 and
                 scope['full_source_CODE_exact'],
                 'complete true instructions, natural alignment not hidden C++ codestring '+stem)
            function_counts[stem]=len(decoded)
        need(v['exe']==b.base.checked(before['outputs']['exe']) and
             v['exe'][:2]==b'MZ' and len(v['exe'])==67372 and
             len(parse_mz(v['exe']).relocations)==677 and
             b.normalize_map(v['map'])==b.base.checked(before['outputs']['map']) and
             row['whole_original_MAINL_exe_equal'] and row['all_677_ordered_MZ_relocations_equal'],
             'every original Japanese decoded EXE byte, literal 677 MZ relocations and MAP allocation sites')
        raw_vectors.append(v)
    need(len(raw_vectors)==2 and raw_vectors[0]==raw_vectors[1],
         'both native complete four-object + EXE + MAP vectors repeat exactly')
    return dict(complete=True, native_rounds=2, native_sound_sources=4,
        full_original_CODE_allocation_bytes=128, complete_function_instruction_bytes=124,
        natural_assembler_even_bytes=4, instruction_counts=function_counts,
        original_OMF_FIXUPP_fields=10,
        four_complete_original_OMF_CODE_PAYLOADS_equal=True,
        original_OMF_FIXUPP_packet_order_identical=False,
        original_compiler_emitter_identity_proved=False,
        complete_original_decoded_MAINL_EXE_equal=True,
        decoded_EXE_bytes=67372,original_ordered_MZ_relocations=677,
        whole_product_source_accepted=False,canonical_factory_acceptance=False,
        native_source_report_sha256=out_sha)

if __name__=='__main__':
    result=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('Four natural sound routines 124 CODE instruction bytes + 4 TASM EVEN: two real native MAINL EXE/677-MZ links byte-exact.')
