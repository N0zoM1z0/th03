#!/usr/bin/env python3
"""Review original hitbox, hitcircle and 386 collision-map native sources.

Also verify the three compiled negative C++ call-control objects. These
are real code-generation comparisons, not claims about untested C++.
"""
import json
import build_th03_main_collision_after591_work as b
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz

def review():
    cfg,cfg_sha,parent=b.inputs()
    record=json.loads((b.ROOT/b.REPORT).read_text())
    report_sha=sha((b.ROOT/b.REPORT).read_bytes())
    sources=b.sources(cfg)
    originals={stem:(b.WORK/f'obj/th03/{stem}.obj').read_bytes() for stem in b.ORDER}
    target=b.parent.parent.read_verified_artifact(
        b.ROOT,b.parent.parent.find_artifact(
            b.parent.parent.load_target_manifest(b.ROOT/'config/targets.toml'),
            'th03-main'))
    negative=b.negative_control(originals['hitbox'])
    need(record['complete'] and record['cold_rebuilt'] is False and
         record['library_rebuilt'] is False and
         record['project_objects_recompiled_per_round']==3 and
         record['other_project_objects_reused']==96 and
         (record['total_CODE_bytes'],record['original_PUBLIC_functions'],
          record['original_OMF_fields'])==(1143,8,90) and
         record['canonical_factory_credit_changed'] is False and
         record['whole_project_source_accepted'] is False and
         record['preserved_original_hitbox_call'] and
         record['negative_cpp_far_call_controls']==negative and
         record['first_use_profile']=='GAME=3 BINARY=M original TC4/TASM' and
         record['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         record['config_sha256']==cfg_sha and
         record['parent_report_sha256']==cfg['parent_report_sha256'] and
         record['original_target_sha256']==sha(target) and
         record['source_sha256']==
           {name:{key:sha(data) for key,data in val.items()} for name,val in sources.items()} and
         record['original_object_sha256']=={name:sha(blob) for name,blob in originals.items()},
         'all original C++ and TASM source provenance, real negative control and parent pinned')
    need((b.SCRATCH/'driver.py').read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         'original native recipe and config stage preserved')
    expected=[f'round{n}-{label}' for n in (1,2)
             for label in ('hitbox-TC4','hitcirc-TC4','collmap-TASM','normal-TLINK')]
    need(len(record['phases'])==8 and
         [p['label'] for p in record['phases']]==expected and
         all(p['exit_code']==0 and
             sha((b.ROOT/p['log']).read_bytes())==p['log_sha256']
             for p in record['phases']),
         'eight native compiler/TASM/linker phases with complete writer logs')
    control=payload(originals['hitbox'])
    need((control[1,207],control[1,208],control[1,209])==(0x90,0x0e,0xe8),
         'actual original NOP/PUSH CS/near CALL retained, no unproved far call')
    assert all(row['actual_far_call_opcode']==0x9a and
               row['real_original_nop_opcode']==0x90 and
               not row['original_function_bytes_equal'] for row in negative.values())
    target_mz=parse_mz(target)
    vectors=[]
    for n,row in enumerate(record['rounds'],1):
        original_parent=parent['rounds'][n-1]['outputs']
        need(row['round']==n and
             row['actual_normal_link_response_sha256']==sha(b.response(n)) and
             (b.SCRATCH/f'r{n}.@l').read_bytes()==b.response(n) and
             row['whole_japanese_MZ_file_exact_after_explicit_format'],
             'actual original normal linker response with only three source modules replaced')
        output={key:b.read_pin(pin) for key,pin in row['outputs'].items()}
        need(set(output)=={s+'_obj' for s in b.ORDER}|{'exe','map','compact_mz'},
             'all original three source objects, full native executable/MAP and compact file')
        for u in cfg['units']:
            stem=u['stem']
            obj=output[stem+'_obj']
            bound=b.object_scope(obj,originals[stem],u)
            ext='asm' if u['emitter']=='TASM' else 'cpp'
            need(row['source_object_scope'][stem]==bound and
                 bound['CODE_bytes']==u['CODE_bytes'] and
                 bound['original_PUBLICs']==u['PUBLICs'] and
                 bound['ordered_OMF_fixups']==u['FIXUPPs'] and
                 bound['complete_original_CODE_and_symbols_equal'] and
                 bound['original_vendor_packet_identity'] is False and
                 (b.SCRATCH/f'r{n}/{stem}.obj').read_bytes()==obj and
                 (b.SCRATCH/f'r{n}/{stem}.{ext}').read_bytes()==
                     sources[stem]['wrapper'].replace(b'\n',b'\r\n') and
                 payload(obj)==payload(originals[stem]) and
                 literal_fields(obj)==literal_fields(originals[stem]) and
                 public_offsets(obj)==public_offsets(originals[stem]),
                 'actual original compiler source, whole CODE/OMF fixups and public ABI '+stem)
        mz=parse_mz(output['exe'])
        need(output['exe']==b.read_pin(original_parent['exe']) and
             b.normalize_map(output['map'],n)==b.read_pin(original_parent['map']) and
             len(output['exe'])==132322 and
             mz.program_image==target_mz.program_image and
             mz.relocations==target_mz.relocations and
             len(mz.relocations)==1553 and
             output['compact_mz']==target==compact_mz(output['exe']) and
             len(target)==130882,
             'all original MAIN byte image, ordered relocation fields and separate compact MZ file exact')
        vectors.append(output)
    need(len(vectors)==2 and
         vectors[0]['exe']==vectors[1]['exe'] and
         vectors[0]['compact_mz']==vectors[1]['compact_mz'] and
         all(payload(vectors[0][s+'_obj'])==payload(vectors[1][s+'_obj']) and
             literal_fields(vectors[0][s+'_obj'])==literal_fields(vectors[1][s+'_obj'])
             for s in b.ORDER),
         'two independent native full source object/EXE/MAP/MZ vector repeats')
    return dict(complete=True,source_game_functions=8,
         original_code_BYTES=1143,ordered_OMF_fixup_FIELDS=90,
         original_hitbox_source_bytes=266,original_hitcircles_source_bytes=445,
         original_386_collision_map_bytes=432,
         independent_native_TC4_TASM_rounds=2,
         compiled_direct_C_CPP_call_controls_rejected=3,
         correctly_preserved_same_CS_near_call=True,
         whole_original_japanese_program_equal=True,
         all_1553_ordered_MZ_relocations_equal=True,
         complete_original_130882_byte_japanese_FILE_equal_after_explicit_MZ_format=True,
         original_vendor_OMF_packet_identity_unproven=True,
         additional_canonical_factory_credit=0,whole_project_source_accepted=False,
         native_source_report_sha256=report_sha)

if __name__=='__main__':
    r=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(r,indent=2)+'\n')
    print('Three collision original sources: hitbox 266, hitcircle 445, 386 collmap 432, 90 fields; two original Japanese MAIN complete files exact.')
