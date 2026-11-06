#!/usr/bin/env python3
"""Read-only verification of two ten-object combined MAIN native TLINK rounds."""
import json
from lib.omf import normalize_dependency_timestamps
from lib.pc98 import parse_mz
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
import build_th03_main_combined_after567_work as b


def review():
    cfg,hash_cfg,parents=b.inputs()
    rec=json.loads((b.ROOT/b.REPORT).read_text())
    exe,mapping,target=b.reference(cfg)
    target_mz=parse_mz(target)
    orig_program=parse_mz(exe).program_image
    source_driver=(b.ROOT/b.DRIVER).read_bytes()
    need(rec['complete'] and rec['cold_rebuilt'] is False and
         rec['canonical_credit_changed'] is False and
         rec['whole_japanese_EXE_file_accepted'] is False and
         rec['projects_recompiled_now']==0 and
         (rec['source_objects_reused_per_round'],rec['project_objects_unchanged_per_round'],
          rec['source_compilations_in_retained_parents'])==(10,89,20) and
         (rec['code_bosses'],rec['code_boss_functions'],rec['original_boss_CODE_bytes'])==(9,85,17451)
         and (rec['input_scan_instruction_bytes'],rec['native_INPUT_EVEN_bytes'])==(417,1) and
         rec['driver_sha256']==sha(source_driver) and
         rec['config_sha256']==hash_cfg and
         rec['parent_sha256']=={n:v[1] for n,v in cfg['parent_reports'].items()} and
         rec['baseline_native_exe_sha256']==sha(exe) and
         rec['baseline_native_map_sha256']==sha(mapping) and
         rec['original_japanese_target_sha256']==sha(target),
         'entire native source graph, retained parent hashes and scoped credit bounds')
    need((b.SCRATCH/'driver.py').read_bytes()==source_driver and
         (b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes() and
         len(rec['phases'])==2 and len(rec['rounds'])==2 and
         [p['label'] for p in rec['phases']]==['round1-normal-TLINK','round2-normal-TLINK'] and
         all(p['returncode']==0 and sha((b.ROOT/p['log']).read_bytes())==p['log_sha256']
             for p in rec['phases']), 'two actual logged normal TLINK runs')
    vectors=[]
    for number,row in enumerate(rec['rounds'],1):
        need(row['round']==number and
             row['normal_link_response_sha256']==sha(b.link_response(cfg,number)) and
             (b.SCRATCH/f'r{number}.@l').read_bytes()==b.link_response(cfg,number) and
             row['complete_original_program_image_equal'] and
             row['ordered_1553_original_mz_relocations_equal'],
             'actual ten-object replacement, no altered reference linker response')
        inherited=b.sources_for_round(cfg,parents,number)
        need(row['reused_source_objects']==inherited and len(inherited)==10,
             'all source-compiled OMF evidence used by the literal parent')
        for stem,pin in inherited.items():
            obj=b.read_pin(pin)
            need(obj==(b.SCRATCH/f'r{number}-{stem}.obj').read_bytes(),
                 'consumed maintained native original source object '+stem)
            original=(b.WORK/f'obj/th03/{stem}.obj').read_bytes()
            if stem=='input_s':
                o=payload(original); n=payload(obj)
                need(len(o)==417 and len(n)==418 and
                     all(o[1,i]==n[1,i] for i in range(417)) and
                     n[1,417]==0x90 and len(literal_fields(obj))==42,
                     'all 417 held-key instruction bytes, 42 native sites and natural alignment')
            else:
                need(normalize_dependency_timestamps(obj)==normalize_dependency_timestamps(original),
                     'full native C++ boss source object equivalence after dependency timestamp '+stem)
        outputs={k:b.read_pin(pin) for k,pin in row['outputs'].items()}
        parsed=parse_mz(outputs['exe'])
        need(parsed.program_image==target_mz.program_image and
             len(parsed.program_image)==124642 and
             parsed.relocations==target_mz.relocations and len(parsed.relocations)==1553 and
             outputs['map']==b.read_pin(parents['input_scan']['rounds'][number-1]['outputs']['map']),
             'full target program/MZ relocation order and natural input EVEN MAP layout')
        need(len(outputs['exe'])==132322 and outputs['exe']!=target and
             len(target)==130882 and
             [i for i,(x,y) in enumerate(zip(orig_program,parsed.program_image)) if x!=y]==[0xEC2D],
             'only changed LOAD byte is the original naturally generated 90h alignment')
        vectors.append(outputs)
    need(vectors[0]==vectors[1],
         'two actual raw EXE/MAP vectors repeat; separate source-native objects verified')
    return dict(complete=True,original_japanese_target='candidate-local-attested',
        big_bosses=9,boss_functions=85,boss_CODE_bytes=17451,
        complete_input_8086_instruction_bytes=417,source_assembler_even_bytes=1,
        reused_independently_compiled_objects=10,normal_TLINK_rounds=2,
        full_original_japanese_program_image_exact=True,source_program_bytes=124642,
        all_1553_ordered_MZ_relocations_equal=True,
        original_130882_byte_EXE_file_equal=False,
        canonical_factory_acceptance=False,
        stage_report_sha256=sha((b.ROOT/b.REPORT).read_bytes()))


if __name__=='__main__':
    row=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(row,indent=2)+'\n')
    print('Ten source-native MAIN objects / nine bosses + input/EVEN combined: 2 complete target-equal decoded image/relocation links.')
