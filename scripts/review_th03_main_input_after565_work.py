#!/usr/bin/env python3
"""Read-only review of the two native MAIN input-scan/EVEN source links."""
import json
import build_th03_main_input_after565_work as b
from build_th03_mainl_resources_work import need,sha
from lib.pc98 import parse_mz
from build_th03_mainl_display_work import literal_fields


def review():
    cfg,cfg_hash=b.inputs()
    report=json.loads((b.ROOT/b.REPORT).read_text())
    report_sha=sha((b.ROOT/b.REPORT).read_bytes())
    parent_report=json.loads((b.ROOT/b.parent.REPORT).read_text())
    parent_hash=sha((b.ROOT/b.parent.REPORT).read_bytes())
    original=(b.WORK/cfg['original_cold_object']).read_bytes()
    source=(b.ROOT/cfg['source']).read_bytes()
    native_source=b.transported(source)
    parent_cfg,_=b.parent.inputs()
    native_exe,native_map,target,_=b.parent.native_parents(parent_cfg)
    original_mz=parse_mz(target)
    old_mz=parse_mz(native_exe)
    need(parent_report['complete'] and parent_hash==cfg['parent_report_sha256'],
         'complete after561 original-normal MAIN source-native parent without cold replay')
    need(report['complete'] and report['canonical_credit_changed'] is False and
         report['cold_rebuilt'] is False and
         report['existing_GAME_objects_reused']==98 and
         report['game_objects_recompiled_per_round']==1 and
         report['original_99_object_link_order'] and
         report['original_MZ_header_exact'] is False and
         report['original_FULL_japanese_FILE_accepted'] is False and
         report['correct_main_instruction_bytes']==417 and
         report['natural_assembler_even_bytes']==1 and
         report['source_sha256']==sha(source) and
         report['transported_source_sha256']==sha(native_source) and
         report['config_sha256']==cfg_hash and
         report['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         report['parent_report_sha256']==parent_hash and
         report['original_input_OBJ_sha256']==sha(original) and
         report['original_native_main_EXE_sha256']==sha(native_exe) and
         report['original_native_main_MAP_sha256']==sha(native_map) and
         report['pinned_japanese_MAIN_sha256']==sha(target),
         'source-bound actual first-use MAIN native objects and no false original file credit')
    need((b.SCRATCH/'input_s.asm').read_bytes()==native_source and
         (b.SCRATCH/'driver.py').read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         'all original consumed source/recipe copies preserved')
    expected_phases=[
       'round1-natural-TASM','round1-normal-TLINK',
       'round2-natural-TASM','round2-normal-TLINK']
    need(len(report['phases'])==4 and
         [p['label'] for p in report['phases']]==expected_phases and
         all(p['returncode']==0 and
             sha((b.ROOT/p['log']).read_bytes())==p['log_sha256'] for p in report['phases']),
         'two real native TASM and TLINK rounds and all writer logs')
    need(original_mz.header.header_paragraphs==390 and
         old_mz.header.header_paragraphs==480 and
         original_mz.header.relocation_table_offset==28 and
         old_mz.header.relocation_table_offset==62 and
         len(original_mz.relocations)==1553,
         'original known independent Borland MZ header differences, no fabricated file identity')
    vectors=[]
    for number,row in enumerate(report['rounds'],1):
        native={kind:(b.ROOT/p['path']).read_bytes() for kind,p in row['outputs'].items()}
        need(row['round']==number and
             len(native)==3 and
             all(len(native[k])==v['bytes'] and sha(native[k])==v['sha256']
                 for k,v in row['outputs'].items()) and
             row['native_response_sha256']==sha(b.response(number)) and
             (b.SCRATCH/f'r{number}.@l').read_bytes()==b.response(number) and
             (b.SCRATCH/f'r{number}.obj').read_bytes()==native['obj'],
             'actual raw original assembler/linker input and all three retained outputs')
        scope=b.verify_object(native['obj'],original,cfg)
        need(row['object_scope']==scope and
             scope['complete_function_instructions']==115 and
             scope['complete_instruction_bytes']==417 and
             scope['native_CODE_alignment_bytes']==1 and
             scope['object_CODE_bytes']==418 and
             scope['original_literal_field_sites']==42 and
             scope['native_FIXUPP_order_matches_original'] is False,
             'real 115 symbolic 8086 instructions, native TASM EVEN and 42 fields')
        result=parse_mz(native['exe'])
        need(result.program_image==original_mz.program_image and
             len(result.program_image)==124642 and
             result.relocations==original_mz.relocations and
             len(result.relocations)==1553 and
             result.header.header_paragraphs==480 and
             result.header.relocation_table_offset==62,
             'complete original Japanese program image and ordered MZ relocations, not header')
        need(row['full_original_japanese_program_image_equal'] and
             row['all_original_1553_ordered_MZ_fields_equal'] and
             row['full_original_japanese_EXE_file_equal'] is False and
             native['exe']!=target and len(native['exe'])==132322 and len(target)==130882 and
             b.map_normalized(native['map'])==native_map and
             [i for i,(a,z) in enumerate(zip(old_mz.program_image,result.program_image)) if a!=z]==[0xEC2D],
             'single genuine input scan layout fix, no other map/address/target drift')
        vectors.append(native)
    need(len(vectors)==2 and vectors[0]==vectors[1],
         'two whole native OBJ/EXE/MAP vectors repeat')
    return dict(complete=True,source='src/main/hardware/input_scan.asm',
        full_input_function_bytes=417,complete_8086_instructions=115,
        semantic_unowned_linker_alignment_fixed=True,
        native_TASM_even_CODE_bytes=1,
        native_CODE_allocation_bytes=418,original_OMF_fixup_sites=42,
        original_OMF_FIXUPP_order_identical=False,
        original_entire_japanese_load_image_exact=True,
        exact_japanese_load_image_bytes=124642,
        all_1553_ordered_japanese_MZ_relocations_exact=True,
        native_source_LINK_rounds=2,
        original_japanese_MZ_header_identical=False,
        japanese_file_size_bytes=130882,native_file_size_bytes=132322,
        japanese_header_paragraphs=390,native_header_paragraphs=480,
        japanese_relocation_table_offset=28,native_relocation_table_offset=62,
        whole_product_source_accepted=False,canonical_factory_accepted=False,
        native_source_report_sha256=report_sha)


if __name__=='__main__':
    result=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('MAIN input: 417 original instructions + natural TASM EVEN; 124642 Japanese program bytes /1553 relocations exact in both rounds; only MZ header remains.')
