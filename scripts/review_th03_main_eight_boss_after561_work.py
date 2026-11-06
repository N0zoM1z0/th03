#!/usr/bin/env python3
"""Independently review after561 eight-boss dual native builds and MAIN links.

Read retained TCC source trees, OMF records, full EXE/MAP and target MZ
relocations. Do not run the compiler, TLINK, cold replay or emulator.
"""
import json

import build_th03_main_eight_boss_after561_work as b
from build_th03_mainl_resources_work import need,sha
from lib.omf import normalize_dependency_timestamps
from lib.pc98 import parse_mz


def review():
    cfg,config_sha=b.inputs()
    record=json.loads((b.ROOT/b.REPORT).read_text())
    report_sha=sha((b.ROOT/b.REPORT).read_bytes())
    native_exe,native_map,target,reference=b.native_parents(cfg)
    target_image=parse_mz(target)
    current_image=parse_mz(native_exe)
    stage_source=(b.ROOT/b.DRIVER).read_bytes()
    cfg_source=(b.ROOT/b.CONFIG).read_bytes()
    need(record['complete'] and record['source_ownership_closure'] is False and
         record['canonical_credit_changed'] is False and
         record['full_original_MAIN_accepted'] is False and
         record['cold_rebuilt'] is False and record['CRT_rebuilt'] is False and
         record['source_game_objects_recompiled_per_round']==8 and
         record['other_game_objects_reused']==91 and
         (record['complete_functions'],record['complete_CODE_bytes'],
          record['compiler_switch_bytes'])==(74,14797,636) and
         record['parent_sha256']==cfg['parent_report_sha256'] and
         record['config_sha256']==config_sha and
         record['driver_sha256']==sha(stage_source) and
         record['native_exe_sha256']==sha(native_exe) and
         record['native_map_sha256']==sha(native_map) and
         record['original_japanese_target_sha256']==sha(target) and
         record['initial_original_object_sha256']==
            {name:sha(raw) for name,raw in reference.items()} and
         record['source_sha256']==
            {name:sha((b.ROOT/name).read_bytes()) for name in record['source_sha256']},
         'complete original retained native/source evidence and no false acceptance')
    need((b.SCRATCH/'driver.py').read_bytes()==stage_source and
         (b.SCRATCH/'config.json').read_bytes()==cfg_source and
         len(record['rounds'])==2 and len(record['phases'])==18,
         'real preserved two-round script, config and eighteen writer logs')
    expected_phases=[
        label for number in (1,2) for label in
            ([f'round{number}-{boss["name"]}-TC4-compile' for boss in cfg['bosses']]
             +[f'round{number}-normal-TLINK'])]
    need([p['label'] for p in record['phases']]==expected_phases and
         all(p['returncode']==0 and
             sha((b.ROOT/p['log']).read_bytes())==p['log_sha256']
             for p in record['phases']),
         'all independent compiler/linker commands and intact writer logs')

    vectors=[]
    compiler_sources=0
    for number,round_row in enumerate(record['rounds'],1):
        need(round_row['round']==number and
             round_row['link_response_sha256']==sha(b.response(cfg,number)) and
             round_row['original_selected_native_exe_equal'] and
             round_row['original_selected_native_map_equal'] and
             round_row['all_1553_target_relocations_equal'],
             'normal original TLINK response, actual selected complete image and fields')
        need((b.SCRATCH/f'r{number}.@l').read_bytes()==b.response(cfg,number),
             'exact retained normal replacement TLINK response, not a rewritten object')
        outputs={key:(b.ROOT/entry['path']).read_bytes()
                 for key,entry in round_row['outputs'].items()}
        need(all(len(outputs[key])==row['bytes'] and sha(outputs[key])==row['sha256']
                 for key,row in round_row['outputs'].items()) and
             len(outputs)==10,'all eight real OMF/EXE/MAP outputs integrity-pinned')
        for boss in cfg['bosses']:
            name=boss['name'];stem=boss['object']; key=stem+'_obj'
            row=round_row['original_OMF'][name]
            proof_id=f'gptweb-561-{name}-r{number}'
            archive=b.ROOT/('.analysis/th03-main-boss-'+name+'-cpp/'+proof_id)
            receipt_path=archive/'receipt.json'
            receipt=json.loads(receipt_path.read_text())
            obj=(archive/'source/obj/th03'/(stem+'.obj')).read_bytes()
            imported,script=b.probe_module(boss)
            need(row['probe_run_id']==proof_id and
                 row['receipt_sha256']==sha(receipt_path.read_bytes()) and
                 row['source_object_sha256']==sha(obj) and
                 row['normalized_complete_OMF_equal'] and
                 row['original_target_CODE_equal'] and
                 obj==outputs[key]==(b.SCRATCH/f'r{number}-{stem}.obj').read_bytes() and
                 normalize_dependency_timestamps(obj)==
                    normalize_dependency_timestamps(reference[stem]),
                 'complete actual native 16-bit TC4 OMF source (not only shape) '+name)
            need(receipt['source_acceptance'] and
                 receipt['exact_acceptance'] is False and
                 receipt['object']['sha256']==sha(obj) and
                 receipt['object']['code_size']==boss['CODE_bytes'] and
                 receipt['comparison']['target_size']==boss['CODE_bytes'] and
                 receipt['comparison']['candidate_size']==boss['CODE_bytes'] and
                 receipt['comparison']['candidate_table_span']==[
                    imported.TARGET_TABLE_START,imported.TARGET_TABLE_END] and
                 receipt['comparison']['table_semantics_equal'] and
                 not receipt['comparison']['function_differences'] and
                 len(receipt['object']['code_publics'])==boss['functions'] and
                 all(sha((b.ROOT/path).read_bytes())==digest
                     for path,digest in receipt['inputs'].items()),
                 'complete original-CODE function boundaries / switch table / dependencies '+name)
            need('tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -ml' in
                    receipt['build']['argv'][-1] and
                 '-a2' not in receipt['build']['argv'][-1] and
                 receipt['build']['exit_code']==0 and
                 receipt['inputs'][script]==sha((b.ROOT/script).read_bytes()),
                 'original compiler command, native source and proof script '+name)
            start=imported.TARGET_SEGMENT*16+imported.TARGET_OFFSET
            stop=start+boss['CODE_bytes']
            need(target_image.program_image[start:stop]==
                 current_image.program_image[start:stop],
                 'entire original Japanese-target CODE owner already equal '+name)
            compiler_sources+=1
        need(outputs['exe']==native_exe and outputs['map']==native_map and
             parse_mz(outputs['exe']).relocations==target_image.relocations and
             len(target_image.relocations)==1553,
             'actual unchanged MAIN native EXE, MAP, literal ordered MZ relocations')
        vectors.append(outputs)
    need(compiler_sources==16 and vectors[0]['exe']==vectors[1]['exe'] and
         vectors[0]['map']==vectors[1]['map'] and
         all(normalize_dependency_timestamps(vectors[0][u['object']+'_obj'])==
             normalize_dependency_timestamps(vectors[1][u['object']+'_obj'])
             for u in cfg['bosses']),
         'two independent, normalized reproducible full OMF groups and whole native MAIN')
    need([i for i,(x,y) in enumerate(zip(target_image.program_image,
                                          current_image.program_image)) if x!=y]==[0xEC2D],
         'the independent MAIN load-image/EXE-header differences are still explicit')
    return dict(complete=True,original_japanese_target='candidate-local-attested',
        bosses=8,full_C_CPP_functions=74,complete_boss_CODE_bytes=14797,
        compiler_switch_table_bytes=636,independent_TCC_source_rounds=2,
        total_new_original_Omf_compilations=16,
        simultaneous_replacement_TLINK_rounds=2,
        normalized_all_16_original_OMF_objects_equal=True,
        full_selected_NATIVE_MAIN_EXE_equal=True,
        full_selected_NATIVE_MAP_equal=True,
        all_1553_original_MZ_relocations_equal=True,
        japanese_original_MAIN_EXE_equal=False,
        remaining_load_image_mismatch=0xEC2D,
        original_header_identity_unresolved=True,
        whole_product_source_accepted=False,canonical_factory_acceptance=False,
        retained_report_sha256=report_sha)

if __name__=='__main__':
    outcome=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(outcome,indent=2)+'\n')
    print('Eight large bosses: 74 complete C++ functions /14797 original CODE, 16 TC4 source objects, 2 whole MAIN links exact.')
