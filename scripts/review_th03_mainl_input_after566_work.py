#!/usr/bin/env python3
"""Read-only review of MAINL's complete natural input scan and TASM EVEN source."""
import json
import tomllib

import build_th03_mainl_input_after566_work as b
from build_th03_mainl_resources_work import need,sha
from lib.pc98 import parse_mz
from lib.targets import read_verified_artifact,find_artifact,load_target_manifest
from build_th03_mainl_display_work import literal_fields


def review():
    cfg,cfg_sha=b.inputs()
    prev,prior_sha=b.base.load(b.parent.REPORT)
    report,report_sha=b.base.load(b.REPORT)
    wrapper,scanner,native_wrapper,native_body=b.source_snapshot(cfg)
    original=(b.WORK/cfg['original_project_object']).read_bytes()
    stored=read_verified_artifact(b.ROOT,find_artifact(
        load_target_manifest(b.ROOT/'config/targets.toml'),'th03-mainl'))
    original_decoded=(b.WORK/'bin/th03/mainl.target.exe').read_bytes()
    target_info,=[x for x in tomllib.loads((b.ROOT/'config/th03_diet.toml').read_text())['artifacts']
                 if x['id']=='th03-mainl']
    need(target_info['decoded_size']==len(original_decoded)==67372 and
         target_info['decoded_sha256']==sha(original_decoded) and
         len(stored)==37975 and prev['complete'] and
         prior_sha==cfg['parent_report_sha256'],
         'unchanged source-native after558 and pinned Japanese decoded/DIET identities')
    need(report['complete'] and
         report['original_obj_source_accepted'] is False and
         report['whole_product_source_accepted'] is False and
         report['canonical_credit_changed'] is False and
         report['cold_rebuilt'] is False and report['library_rebuilt'] is False and
         report['game_objects_recompiled_per_round']==1 and
         report['other_project_objects_reused']==35 and
         (report['native_CODE_bytes'],report['natural_8086_instruction_bytes'],
          report['native_even_bytes'])==(418,417,1) and
         report['input_TU_sha256']==sha(wrapper) and
         report['shared_scanner_sha256']==sha(scanner) and
         report['staged_TU_sha256']==sha(native_wrapper) and
         report['staged_scanner_sha256']==sha(native_body) and
         report['original_input_obj_sha256']==sha(original) and
         report['japanese_decoded_target_sha256']==sha(original_decoded) and
         report['japanese_DIET_stored_target_sha256']==sha(stored) and
         report['config_sha256']==cfg_sha and
         report['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         report['parent_report_sha256']==prior_sha,
         'all two-part maintained source, actual original contexts and limited acceptance claims')
    for local,content in [('input_s.asm',native_wrapper),('scan_body.asm',native_body),
                          ('maintained_TU.asm',wrapper),
                          ('driver.py',(b.ROOT/b.DRIVER).read_bytes()),
                          ('config.json',(b.ROOT/b.CONFIG).read_bytes())]:
        need((b.SCRATCH/local).read_bytes()==content,
             'actual complete retained original native input '+local)
    labels=[f'round{n}-{task}' for n in (1,2) for task in ('assemble','link')]
    need(len(report['phases'])==4 and
         [p['label'] for p in report['phases']]==labels and
         all(p['returncode']==0 and
             sha((b.ROOT/p['log']).read_bytes())==p['log_sha256']
             for p in report['phases']), 'all actual TASM/TLINK phases and pinned writer logs')
    target=parse_mz(original_decoded)
    vectors=[]
    for n,row in enumerate(report['rounds'],1):
        prior=prev['rounds'][n-1]
        need(row['round']==n and
             row['response_sha256']==sha(b.response(n)) and
             (b.SCRATCH/f'r{n}.lnk').read_bytes()==b.response(n),
             'only original input object changes in normal native MAINL link')
        v={k:b.base.checked(pin) for k,pin in row['outputs'].items()}
        need(set(v)=={'obj','exe','map'} and
             (b.SCRATCH/f'r{n}.obj').read_bytes()==v['obj'],
             'complete three native raw outputs and original TASM object')
        scope=b.verify_object(v['obj'],original)
        need(row['original_418_CODE_scope']==scope and
             scope['complete_original_CODE_bytes']==418 and
             scope['complete_instruction_bytes']==417 and
             scope['true_even_alignment_bytes']==1 and
             scope['instructions']==115 and
             scope['original_literal_fixup_sites']==42 and
             scope['original_OMF_FIXUPP_order_equal'] is False,
             'full original initializer, all FIXUPP site tuples and real EVEN not codestring')
        exe=parse_mz(v['exe'])
        need(v['exe']==original_decoded==
             b.base.checked(prior['outputs']['exe']) and
             len(exe.relocations)==677 and exe.relocations==target.relocations and
             b.normalize_map(v['map'])==b.base.checked(prior['outputs']['map']) and
             row['raw_japanese_MAINL_EXE_exact'] and
             row['ordered_677_relocations_equal'] and
             row['parent_unchanged_source_round']==n,
             'entire original Japanese decoded EXE, ordered MZ fields and every MAP coordinate')
        vectors.append(v)
    need(len(vectors)==2 and vectors[0]==vectors[1], 'both complete native OBJ/EXE/MAP vectors repeat')
    return dict(complete=True,target_provenance='candidate-local-attested',
         maintained_input_TU=cfg['maintained_TU'],proved_shared_BODY=cfg['proved_common_scanner'],
         original_complete_FUNCTION_bytes=417,original_instructions=115,
         TASM_even_alignment_bytes=1,full_CODE_allocation_bytes=418,
         original_OMF_fixup_sites=42,original_OMF_fixup_order_equal=False,
         original_PUBLIC_definitions_equal=True,
         native_build_rounds=2,
         complete_original_japanese_decoded_MAINL_EXE_equal=True,
         decoded_original_bytes=67372,original_ordered_MZ_relocations=677,
         normal_MAP_all_unchanged_addresses_equal=True,
         original_DIET_stored_file_repacked_now=False,
         whole_game_source_accepted=False,canonical_factory_acceptance=False,
         native_source_report_sha256=report_sha)


if __name__=='__main__':
    result=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('MAINL shared PC-98 scanner: 417 instructions plus native CODE EVEN; both entire 67372-byte original EXEs and all 677 ordered relocations exact.')
