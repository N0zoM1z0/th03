#!/usr/bin/env python3
"""Read-only verification of natural TASM word-aligned registration DATA after569."""
import json

import build_th03_mainl_registration_even_after569_work as b
from build_th03_mainl_resources_work import need,sha
from lib.pc98 import parse_mz


def review():
    cfg,cfg_sha=b.inputs()
    previous,previous_sha=b.base.load(b.parent.REPORT)
    report,report_sha=b.base.load(b.REPORT)
    old,aligned,codes=b.sources(cfg)
    original=(b.WORK/cfg['original_context_object']).read_bytes()
    need(previous['complete'] and previous_sha==cfg['parent_report_sha256'],
         'actual after566 original-exact MAINL source link remains bound')
    need(report['complete'] and report['cold_rebuilt'] is False and
         report['CRT_rebuilt'] is False and
         report['whole_product_source_accepted'] is False and
         report['canonical_credit_changed'] is False and
         report['game_objects_recompiled_per_round']==1 and
         report['remaining_project_objects_reused']==35 and
         (report['source_TASM_semantic_DATA_bytes'],report['source_NATIVE_even_DATA_bytes'])==(303,1) and
         report['original_context_object_sha256']==sha(original) and
         report['original_unaligned_source_sha256']==sha(old) and
         report['aligned_source_sha256']==sha(aligned) and
         report['code_definitions_sha256']==sha(codes) and
         report['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         report['config_sha256']==cfg_sha and
         report['parent_report_sha256']==previous_sha,
         'maintained original source and source variant pinned to real native parent')
    for name,raw in [
        ('regpre.asm',b.transport(aligned)),
        ('src/mainl/hiscore/regi_codes.inc',b.transport(codes)),
        ('driver.py',(b.ROOT/b.DRIVER).read_bytes()),
        ('config.json',(b.ROOT/b.CONFIG).read_bytes())]:
        need((b.SCRATCH/name).read_bytes()==raw,
             'complete actual source consumed by original TASM5 '+name)
    labels=[f'round{n}-{phase}' for n in (1,2) for phase in ('assemble','link')]
    need(len(report['phases'])==4 and
         [x['label'] for x in report['phases']]==labels and
         all(x['returncode']==0 and
             x['log_sha256']==sha((b.ROOT/x['log']).read_bytes()) for x in report['phases']),
         'all four complete original compiler and normal linker writer logs')
    vectors=[]
    for n,row in enumerate(report['rounds'],1):
        prior=previous['rounds'][n-1]
        need(row['round']==n and row['response_sha256']==sha(b.response(n)) and
             (b.SCRATCH/f'r{n}.lnk').read_bytes()==b.response(n),
             'original first-use link response, single DATA module replacement')
        v={key:b.base.checked(pin) for key,pin in row['outputs'].items()}
        need(set(v)=={'obj','exe','map'} and
             (b.SCRATCH/'regpre.obj').read_bytes()==v['obj'],
             'retained raw source OBJ and complete binary EXE/MAP')
        scope=b.scope(v['obj'],original)
        need(scope==row['complete_original_DATA_scope'] and
             scope['native_DATA_allocation_bytes']==304 and
             scope['initialized_semantic_DATA_bytes']==303 and
             scope['original_TASM_even_byte']==1 and
             scope['complete_original_context_payload'] and
             scope['original_ordered_fixups_equal'] and
             scope['original_PUBLIC_definitions_equal'] and
             scope['nonvariable_other_OMF_equal'],
             'complete 304-byte original initialized DATA and both OMF fixups/35 public definitions')
        need(v['exe']==b.base.checked(prior['outputs']['exe']) and
             len(v['exe'])==67372 and
             len(parse_mz(v['exe']).relocations)==677 and
             b.canonical_map(v['map'])==b.base.checked(prior['outputs']['map']) and
             row['actual_japanese_decoded_exe_equal'] and
             row['unchanged_original_MAP_outside_REGPRE_row'],
             'entire original Japanese decoded EXE, ordered 677 relocations and MAP outside 1 real DATA row')
        vectors.append(v)
    need(len(vectors)==2 and vectors[0]==vectors[1],
         'both complete original TASM/TLINK OBJ+EXE+MAP vectors repeat')
    return dict(complete=True,
        native_source_rounds=2,maintained_source=cfg['aligned_source'],
        original_registration_DATA_bytes=304,registration_semantic_DATA_bytes=303,
        native_TASM_WORD_even_initialized_bytes=1,
        original_literal_native_FIXUPP_count=2,original_PUBLIC_definitions=35,
        complete_original_object_initializer_equal=True,
        entire_original_decoded_japanese_MAINL_EXE_equal=True,
        entire_original_decoded_EXE_bytes=67372,original_ordered_MZ_relocations=677,
        non_registration_MAP_contributions_unchanged=True,
        new_authored_function_count=0,
        additional_source_game_credit=0,
        canonical_factory_acceptance=False,whole_product_source_accepted=False,
        source_native_report_sha256=report_sha)


if __name__=='__main__':
    result=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('Original 304-byte registration DATA, natural TASM EVEN, original 67372-byte EXE/677 MZ relocations: 2 native rounds exact.')
