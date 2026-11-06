#!/usr/bin/env python3
"""Read-only verification of four source-shared large enemy C++ objects."""
import json
from pathlib import Path
import csv

from build_th03_mainl_resources_work import need,sha
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz
import build_th03_main_enemy_four_after572_work as b


def review():
    cfg,cfg_sha,parent=b.inputs()
    report=json.loads((b.ROOT/b.REPORT).read_text())
    report_sha=sha((b.ROOT/b.REPORT).read_bytes())
    common,wrappers=b.source_inputs(cfg)
    reference={u['stem']:(b.WORK/f'obj/th03/{u["stem"]}.obj').read_bytes() for u in cfg['units']}
    _,_,target=b.parent.reference(cfg)
    native_baseline=(b.WORK/'bin/th03/main.exe').read_bytes()
    need(report['complete'] and report['cold_rebuilt'] is False and
         report['source_game_objects_recompiled_per_round']==4 and
         report['original_unmodified_other_objects']==95 and
         report['compiler_runtime_rebuilt'] is False and
         report['canonical_credit_changed'] is False and
         report['whole_product_source_accepted'] is False and
         (report['complete_CODE_allocation_bytes'],report['public_functions'],
          report['ordered_native_fixups'])==(3325,19,222) and
         report['common_source_sha256']==sha(common) and
         report['source_wrapper_sha256']=={k:sha(v) for k,v in wrappers.items()} and
         report['original_object_sha256']=={k:sha(v) for k,v in reference.items()} and
         report['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         report['config_sha256']==cfg_sha and
         report['parent_report_sha256']==cfg['parent_report_sha256'] and
         report['original_japanese_target_sha256']==sha(target) and
         report['original_native_baseline_SHA256']==sha(native_baseline),
         'actual source/OBJs/parent/code quota without promoting unproved credit')
    need((b.SCRATCH/'driver.py').read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         'exact source-input script and fixed whole native compiler recipe')
    labels=[label for n in (1,2) for label in
            ([f'round{n}-{stem}-TC4-compile' for stem in b.ORDER] +
             [f'round{n}-normal-TLINK'])]
    need(len(report['phases'])==10 and
         [row['label'] for row in report['phases']]==labels and
         all(row['returncode']==0 and
             sha((b.ROOT/row['log']).read_bytes())==row['log_sha256'] for row in report['phases']),
         'all ten actual TC4/TLINK writer logs retained')
    # Independent ledger sampling confirms two large, non-leaf original
    # functions in addition to entire producer object/payload checks.
    with (b.ROOT/'config/th03_main_authored_functions.csv').open(newline='') as stream:
        functions={row['name']:row for row in csv.DictReader(stream)}
    scopes=(('enemy_run',0x1578C,867),('enemy_hittest',0x179BD,848))
    for name,offset,size in scopes:
        need(name in functions and
             int(functions[name]['size'],0)==size,
             'original independently published large enemy function scope '+name)
    original_mz=parse_mz(target)
    need(len(original_mz.program_image)==124642 and len(original_mz.relocations)==1553,
         'full original Japanese MAIN target image and relocation inventory')
    vectors=[]
    total_fixups=0
    for n,row in enumerate(report['rounds'],1):
        prev=parent['rounds'][n-1]
        need(row['round']==n and row['response_sha256']==sha(b.response(n)) and
             (b.SCRATCH/f'r{n}.@l').read_bytes()==b.response(n),
             'real preserved source-native 99-object MAIN linker order')
        v={key:(b.ROOT/pin['path']).read_bytes() for key,pin in row['outputs'].items()}
        need(set(v)=={s+'_obj' for s in b.ORDER}|{'exe','map','compact_mz'} and
             all(len(v[key])==pin['bytes'] and sha(v[key])==pin['sha256']
                 for key,pin in row['outputs'].items()),
             'complete seven native source OBJ/EXE/MAP/compact MZ products pinned')
        for u in cfg['units']:
            stem=u['stem']
            source_path=b.SCRATCH/f'r{n}/{stem}.cpp'
            need(source_path.read_bytes()==wrappers[stem].replace(b'\n',b'\r\n'),
                 'fresh original compiler actual shared source wrapper '+stem)
            obj=v[stem+'_obj']
            need((b.SCRATCH/f'r{n}/{stem}.obj').read_bytes()==obj,
                 'real native compiled source object '+stem)
            scope=b.original_object_scope(obj,reference[stem],u)
            need(row['objects_scope'][stem]==scope and
                 scope['original_initialized_CODE_equal'] and
                 scope['original_native_fixup_order_equal'] and
                 scope['original_publics_and_segments_equal'] and
                 scope['original_complete_OMF_packet_equal'] is False,
                 'whole linker-facing OMF evidence and declared original packet boundary '+stem)
            total_fixups+=scope['original_ordered_native_fixups']
        native=b.parent.read_pin(prev['outputs']['exe'])
        native_map=b.parent.read_pin(prev['outputs']['map'])
        need(v['exe']==native and
             b.normalize_map(v['map'],n)==native_map and
             row['whole_native_MAIN_EXE_equal'],
             'all original source-linked MAIN EXE and MAP byte geometry unchanged')
        current_mz=parse_mz(v['exe'])
        need(current_mz.program_image==original_mz.program_image and
             current_mz.relocations==original_mz.relocations and
             all(current_mz.program_image[offset:offset+size]==
                 original_mz.program_image[offset:offset+size]
                 for _,offset,size in scopes),
             'whole image/1553 relocations and independently reviewed 867+848-byte major functions')
        need(v['compact_mz']==target==compact_mz(v['exe']) and
             len(target)==130882 and
             row['complete_original_japanese_file_equal_after_MZ_format_conversion'],
             'whole exact original Japanese MZ file from native source, with explicit formatting step')
        vectors.append(v)
    need(len(vectors)==2 and
         vectors[0]['exe']==vectors[1]['exe'] and
         vectors[0]['compact_mz']==vectors[1]['compact_mz'] and
         b.normalize_map(vectors[0]['map'],1)==b.normalize_map(vectors[1]['map'],2) and
         total_fixups==444,
         'both independent source-compiled four-object groups and full original files repeat')
    return dict(complete=True,native_source_rounds=2,
        original_major_functions=['enemy_run','enemy_hittest'],
        original_major_function_bytes=[867,848],
        original_enemy_C_CODE_allocation_bytes=3325,
        natural_CPP_producer_modules=4,complete_public_functions=19,
        ordered_OMF_fixups_per_native_round=222,
        initialized_original_OBJECT_code_equal=True,
        linker_literally_ordered_FIXUPP_fields_equal=True,
        complete_original_vendor_OMF_packet_identity=False,
        source_link_MAIN_full_program_equal=True,
        ordered_original_MAIN_MZ_relocations=1553,
        original_file_exact_after_independent_MZ_format=True,
        original_file_bytes=130882,
        native_TLINK_direct_original_file_exact=False,
        existing_function_ledger_credit_unchanged=True,
        whole_game_source_closure_unproven=True,canonical_factory_acceptance=False,
        original_target_provenance='candidate-local-attested',
        native_source_report_sha256=report_sha)

if __name__=='__main__':
    r=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(r,indent=2)+'\n')
    print('Four shared C++ enemy producers / 3325 original CODE / 19 functions including 867+848 B control; two exact original MAIN files.')
