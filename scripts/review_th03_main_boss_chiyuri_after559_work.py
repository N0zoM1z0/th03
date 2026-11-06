#!/usr/bin/env python3
"""Read-only two-round reviewer: full natural C++ Chiyuri producer and MAIN link."""
import json
from lib.omf import normalize_dependency_timestamps
from lib.pc98 import parse_mz
from build_th03_mainl_resources_work import need,sha
import build_th03_main_boss_chiyuri_after559_work as b


def review():
    cfg,cfg_sha=b.inputs()
    rec,rec_sha=b.sha_and_load() if hasattr(b,'sha_and_load') else (
        json.loads((b.ROOT/b.REPORT).read_text()),sha((b.ROOT/b.REPORT).read_bytes()))
    source=(b.ROOT/cfg['source']).read_bytes()
    probe=(b.ROOT/b.PROBE).read_bytes()
    reference_obj,selected,map_raw,target=b.verify_reference(cfg)
    need(rec['complete'] and rec['cold_rebuilt'] is False and
         rec['original_MAIN_source_accepted'] is False and
         rec['canonical_credit_changed'] is False and
         rec['game_objects_recompiled']==1 and rec['per_round_recompiles']==1 and
         rec['untouched_game_objects_reused']==98 and
         rec['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         rec['config_sha256']==cfg_sha and
         rec['source_sha256']==sha(source) and rec['probe_sha256']==sha(probe) and
         rec['original_object_sha256']==sha(reference_obj) and
         rec['baseline_native_EXE_sha256']==sha(selected) and
         rec['baseline_native_MAP_sha256']==sha(map_raw) and
         rec['original_target_sha256']==sha(target) and
         rec['base_report_sha256']==cfg['main_native_report_sha256'],
         'source-bound native receipt and no full-product acceptance overclaim')
    need((b.SCRATCH/'driver.py').read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         'complete original staged source driver and configuration')
    need(len(rec['phases'])==4 and
         [p['label'] for p in rec['phases']]==[
             'round1-boss-TCC-compile','round1-boss-TLINK-link',
             'round2-boss-TCC-compile','round2-boss-TLINK-link'] and
         all(p['returncode']==0 and sha((b.ROOT/p['log']).read_bytes())==p['log_sha256']
             for p in rec['phases']), 'actual complete compiler/linker logs')
    target_mz=parse_mz(target)
    selected_mz=parse_mz(selected)
    begin,size=cfg['decoded_main_owner_start'],cfg['decoded_main_owner_bytes']
    need(target_mz.program_image[begin:begin+size]==selected_mz.program_image[begin:begin+size],
         'complete 2654 original boss/C++-generated table CODE bound to target')
    vectors=[]
    for i,row in enumerate(rec['rounds'],1):
        probe_id=cfg['probe_run_ids'][i-1]
        work=b.ROOT/('.analysis/th03-main-boss-chiyuri-cpp/'+probe_id)
        receipt_path=work/'receipt.json'
        source_obj=(work/'source/obj/th03/ba_chiyu.obj').read_bytes()
        receipt=json.loads(receipt_path.read_text())
        need(row['round']==i and row['probe_run_id']==probe_id and
             row['probe_receipt_sha256']==sha(receipt_path.read_bytes()) and
             row['native_response_sha256']==sha(b.link_response(cfg,i)) and
             row['normalized_original_OMF_equal'] and
             row['all_11_function_shapes_exact'] and
             row['whole_native_MAIN_EXE_reproduced'] and
             row['all_1553_target_relocations_equal'],
             'actual independent TC4 compile and original link response')
        need(receipt['source_acceptance'] and
             receipt['exact_acceptance'] is False and
             receipt['comparison']['candidate_size']==size and
             receipt['comparison']['target_size']==size and
             len(receipt['comparison']['function_differences'])==0 and
             receipt['comparison']['table_semantics_equal'] and
             receipt['comparison']['candidate_table_span']==[1904,1985] and
             len(receipt['object']['code_publics'])==11 and
             receipt['object']['sha256']==sha(source_obj) and
             len(receipt['inputs'])==24 and
             receipt['inputs'][cfg['source']]==sha(source) and
             receipt['inputs'][b.PROBE]==sha(probe) and
             all(sha((b.ROOT/p).read_bytes())==v for p,v in receipt['inputs'].items()),
             'all 11 target function boundaries and true C++ dependency tree')
        cli=receipt['build']['argv']
        need(receipt['build']['exit_code']==0 and all('-a2' not in arg for arg in cli) and
             'tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -ml' in cli[-1],
             'original, unmodified TCC compiler flags (global -a2 is an invalid control)')
        native={k:b.load_pin(pin) if hasattr(b,'load_pin') else (b.ROOT/pin['path']).read_bytes()
                for k,pin in row['output'].items()}
        need(all(sha(native[k])==row['output'][k]['sha256'] and
                 len(native[k])==row['output'][k]['bytes'] for k in native),
             'all raw OBJ/EXE/MAP native stage outputs pinned')
        need((b.SCRATCH/f'r{i}.obj').read_bytes()==source_obj==native['obj'] and
             (b.SCRATCH/f'r{i}.@l').read_bytes()==b.link_response(cfg,i),
             'actual object and unchanged source-cold link')
        need(normalize_dependency_timestamps(native['obj'])==
             normalize_dependency_timestamps(reference_obj),
             'complete original link-relevant OMF, not merely function shape')
        need(native['exe']==selected and native['map']==map_raw and
             parse_mz(native['exe']).relocations==target_mz.relocations and
             len(target_mz.relocations)==1553,
             'whole selected MAIN native output/MAP, all 1553 original ordered relocations')
        vectors.append(native)
    need(len(vectors)==2 and vectors[0]['exe']==vectors[1]['exe'] and
         vectors[0]['map']==vectors[1]['map'] and
         normalize_dependency_timestamps(vectors[0]['obj'])==
         normalize_dependency_timestamps(vectors[1]['obj']),
         'independent repeat of complete compiler object plus full-link outputs')
    differences=[i for i,(x,y) in enumerate(zip(target_mz.program_image,selected_mz.program_image)) if x!=y]
    need(differences==[0xEC2D] and
         target_mz.program_image[0xEC2D]==0x90 and selected_mz.program_image[0xEC2D]==0,
         'one unrelated source MAIN target image byte remains open')
    return dict(complete=True,compiler_rounds=2,native_link_rounds=2,
        boss='Chiyuri',complete_C_CPP_bodies=11,boss_CODE_bytes=2654,
        inline_switch_table_bytes=81,source_generated_normalized_OMF_equal=True,
        original_target_boss_load_bytes_exact=True,full_selected_MAIN_native_EXE_equal=True,
        full_selected_MAP_equal=True,all_1553_ordered_MZ_relocations_exact=True,
        full_original_MAIN_EXE_equal=False,
        original_MAIN_remaining_load_mismatch_offset=0xEC2D,
        whole_MAIN_source_accepted=False,canonical_factory_acceptance=False,
        retained_native_stage_sha256=rec_sha)


if __name__=='__main__':
    result=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('Chiyuri boss 2654 CODE / 11 complete C++ functions + 81-byte switch: both native rounds fully exact; MAIN header/EC2D still open.')
