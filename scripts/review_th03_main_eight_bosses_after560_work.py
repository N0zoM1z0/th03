#!/usr/bin/env python3
"""Read-only audit of two independent TC4 builds of eight complete MAIN bosses."""
import json
from lib.omf import normalize_dependency_timestamps
from lib.pc98 import parse_mz
from build_th03_mainl_resources_work import need, sha
import build_th03_main_eight_bosses_after560_work as b


def review():
    cfg, cfg_sha=b.inputs()
    record_path=b.ROOT/b.REPORT
    report=json.loads(record_path.read_text())
    parent=json.loads((b.ROOT/cfg['parent_report']).read_text())
    selected,map_raw,target=b.original()
    source={x['source']:sha((b.ROOT/x['source']).read_bytes()) for x in cfg['bosses']}
    scripts={x['probe']:sha((b.ROOT/x['probe']).read_bytes()) for x in cfg['bosses']}
    need(parent['complete'] and sha((b.ROOT/cfg['parent_report']).read_bytes())==
         cfg['parent_report_sha256'], 'actual native after559 parent')
    need(report['complete'] and report['cold_rebuilt'] is False and
         report['number_of_game_objects_recompiled_per_full_round']==8 and
         report['original_OTHER_GAME_objects_reused']==91 and
         report['accepted_ever_firstuse_source_objects']==8 and
         report['canonical_credit_changed'] is False and
         report['whole_original_MAIN_file_accepted'] is False and
         (report['original_large_boss_CODE_bytes'],report['complete_boss_procedures'],
          report['original_inline_switch_bytes'])==(14797,74,636) and
         report['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         report['config_sha256']==cfg_sha and
         report['parent_report_sha256']==cfg['parent_report_sha256'] and
         report['source_sha256']==source and report['probe_sha256']==scripts and
         report['baseline_source_MAIN_sha256']==sha(selected) and
         report['baseline_MAP_sha256']==sha(map_raw) and
         report['original_target_sha256']==sha(target),
         'real source/header/TCC references and conservative acceptance limits')
    need((b.SCRATCH/'driver.py').read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         'staged and maintained source-native scripts identical')
    frozen_marisa=sha((b.ROOT/'scripts/probe_th03_main_boss_marisa_cpp.py').read_bytes())
    need(frozen_marisa=='271ca45e64db11e6575c8160659126d234b566ce21f42110af9e51a8b06ff9f3' and
         cfg['bosses'][-1]['probe']=='scripts/probe_th03_main_boss_marisa_native_corrected.py',
         'historic acceptance-bound Marisa recipe untouched')
    expected_phases=['round1-eight-boss-native-TLINK']+[
        f'round2-{x["name"]}-TC4-compile' for x in cfg['bosses']]+[
        'round2-eight-boss-native-TLINK']
    need(len(report['phases'])==10 and
         [p['label'] for p in report['phases']]==expected_phases and
         all(p['returncode']==0 and sha((b.ROOT/p['log']).read_bytes())==
             p['log_sha256'] for p in report['phases']),
         'all actual scoped compilation and TLINK writer logs')
    original_mz=parse_mz(target)
    native_mz=parse_mz(selected)
    need(len(original_mz.relocations)==1553 and
         original_mz.relocations==native_mz.relocations,
         'all original Japanese 1553 ordered MZ relocation entries')
    vectors=[]
    for number,row in enumerate(report['rounds'],1):
        need(row['round']==number and
             row['normal_link_response_sha256']==sha(b.response(cfg,number)) and
             row['full_selected_native_MAIN_EXE_equal'] and
             row['full_MAP_equal'] and row['original_1553_ordered_MZ_relocations_equal'],
             'normal 99-object response and entire source-selected native link')
        saved={name:(b.ROOT/data['path']).read_bytes() for name,data in row['outputs'].items()}
        need(set(saved)=={'exe','map'} | {x['object'] for x in cfg['bosses']} and
             all(sha(saved[k])==row['outputs'][k]['sha256'] and
                 len(saved[k])==row['outputs'][k]['bytes'] for k in saved),
             'both complete eight-OBJ/native-EXE/MAP raw vectors retained')
        need((b.SCRATCH/f'r{number}.@l').read_bytes()==b.response(cfg,number) and
             saved['exe']==(b.SCRATCH/f'r{number}.exe').read_bytes()==selected and
             saved['map']==(b.SCRATCH/f'r{number}.map').read_bytes()==map_raw,
             'normal original native MAIN MZ/MAP layout and actual staged binaries')
        need(parse_mz(saved['exe']).relocations==original_mz.relocations and
             len(saved['exe'])==132322 and len(saved['map'])==157164,
             'whole native source build, all target ordered fixups')
        for x in cfg['bosses']:
            obj=saved[x['object']]
            need((b.SCRATCH/f'r{number}'/(x['object']+'.obj')).read_bytes()==obj,
                 'actual selected object passed to TLINK '+x['name'])
            original_obj=(b.WORK/f"obj/th03/{x['object']}.obj").read_bytes()
            need(normalize_dependency_timestamps(obj)==normalize_dependency_timestamps(original_obj),
                 'complete original compiler OMF, not only shape '+x['name'])
            p=b.probe_folder(x,number)/'receipt.json'
            witness=row['probe_receipts'][x['name']]
            need(witness['receipt_path']==str(p.relative_to(b.ROOT)) and
                 witness['receipt_sha256']==sha(p.read_bytes()) and
                 witness['source_object_sha256']==sha(obj) and
                 witness['functions']==x['functions'] and
                 witness['CODE_bytes']==x['size'] and
                 witness['switch_bytes']==x['switch_bytes'] and
                 witness['normalized_original_OMF_equal'] and
                 b.validate_probe(x,number,source[x['source']],scripts[x['probe']])[0]==obj,
                 'source headers, all function boundaries and native first-use OMF '+x['name'])
            a=0xF1F*16+x['offset'];z=a+x['size']
            need(native_mz.program_image[a:z]==original_mz.program_image[a:z],
                 'every byte of original Japanese target 8 large BOSS code bodies '+x['name'])
        vectors.append(saved)
    need(len(vectors)==2 and vectors[0]['exe']==vectors[1]['exe'] and
         vectors[0]['map']==vectors[1]['map'] and
         all(normalize_dependency_timestamps(vectors[0][x['object']])==
             normalize_dependency_timestamps(vectors[1][x['object']])
             for x in cfg['bosses']),
         'second independent source-compiled OBJ pair and full normal EXE/MAP pair')
    differences=[i for i,(a,c) in enumerate(zip(original_mz.program_image,
                                                native_mz.program_image)) if a!=c]
    need(differences==[0xEC2D] and
         original_mz.program_image[0xEC2D]==0x90 and
         native_mz.program_image[0xEC2D]==0x00,
         'known independent mismatch of original MAIN source build preserved')
    return dict(complete=True,independent_native_compile_rounds=2,
        source_OMF_objects=8,complete_natural_C_CPP_procedures=74,
        full_original_boss_CODE_bytes=14797,compiler_switch_bytes=636,
        complete_native_OMF_equivalent=True,whole_selected_MAIN_EXE_equal=True,
        whole_selected_MAP_equal=True,original_ordered_MZ_relocations=1553,
        original_target_boss_CODE_byte_exact=True,
        original_MAIN_target_EXE_byte_exact=False,
        unrelated_original_load_mismatch=0xEC2D,
        full_cold_replay_performed=False,whole_game_source_accepted=False,
        canonical_factory_acceptance=False,retained_native_report_sha256=sha(record_path.read_bytes()))


if __name__=='__main__':
    result=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('Eight original boss source TUs: 74 procedures/14797 CODE, all OMF exact and twice jointly native-linked exact.')
