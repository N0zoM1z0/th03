#!/usr/bin/env python3
"""Read-only original bullet engine and GRCG PELLET_PUT source/native review."""
import json
from build_th03_mainl_resources_work import sha,need
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz
import build_th03_main_bullet_after588_work as b

def review():
    cfg,cfg_sha,prior=b.inputs()
    report=json.loads((b.ROOT/b.REPORT).read_text())
    report_sha=sha((b.ROOT/b.REPORT).read_bytes())
    source,wrapper=b.sources(cfg)
    orig=(b.WORK/cfg['original_object']).read_bytes()
    target=b.read_verified_artifact(b.ROOT,b.find_artifact(
        b.load_target_manifest(b.ROOT/'config/targets.toml'),'th03-main'))
    need(report['complete'] and report['cold_rebuilt'] is False and
         report['library_rebuilt'] is False and
         report['source_game_objects_recompiled_per_round']==1 and
         report['other_project_objects_reused']==98 and
         (report['source_CODE_bytes'],report['source_BSS_bytes'])==(2685,9500) and
         report['canonical_factory_credit_changed'] is False and
         report['whole_game_source_accepted'] is False and
         report['parent_report_sha256']==cfg['parent_report_sha256'] and
         report['config_sha256']==cfg_sha and
         report['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         report['maintained_source_sha256']==sha(source) and
         report['wrapper_sha256']==sha(wrapper) and
         report['original_object_sha256']==sha(orig) and
         report['original_target_sha256']==sha(target),
         'actual complete bullet and BSS/target plus native source bindings')
    need((b.SCRATCH/'driver.py').read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         'staged recipe and code remain maintained byte-for-byte')
    names=[f'round{n}-{kind}' for n in (1,2)
           for kind in ('bullet-TC4-compile','normal-TLINK')]
    need([x['label'] for x in report['phases']]==names and len(report['phases'])==4 and
         all(x['exit_code']==0 and sha((b.ROOT/x['log']).read_bytes())==x['log_sha256']
             for x in report['phases']),
         'two native compiler/linker rounds with all four writer logs')
    original_mz=parse_mz(target)
    outputs=[]
    for n,scope in enumerate(report['rounds'],1):
        ref=prior['rounds'][n-1]['outputs']
        need(scope['round']==n and
             scope['actual_link_response_sha256']==sha(b.response(n)) and
             (b.SCRATCH/f'r{n}.@l').read_bytes()==b.response(n),
             'one bullet slot replaced in genuine unchanged original MAIN link')
        values={k:b.previous.parent.read_pin(p) for k,p in scope['outputs'].items()}
        need(set(values)=={'obj','exe','map','compact_mz'} and
             (b.SCRATCH/f'r{n}/bullet.cpp').read_bytes()==wrapper.replace(b'\n',b'\r\n') and
             (b.SCRATCH/f'r{n}/bullet.obj').read_bytes()==values['obj'],
             'each actual Turbo C++ source and complete emitted OBJ retained')
        observed=b.object_scope(values['obj'],orig,cfg)
        need(observed==scope['scope'] and
             observed['complete_initialized_CODE_bytes']==2685 and
             observed['main_bullet_CODE_bytes']==2602 and
             observed['PELLET_PUT_CODE_bytes']==83 and
             observed['BSS_bytes']==9500 and
             observed['original_PUBLIC_count']==20 and
             observed['original_FIXUPP_count']==196 and
             observed['entire_original_linker_semantics_equal'] and
             observed['original_vendor_OMF_packet_identity'] is False,
             'real full bullet source CODE/9.5KB BSS/196 fields/20 PUBLIC')
        src=b.previous.parent.read_pin(ref['exe'])
        parent_map=b.previous.parent.read_pin(ref['map'])
        native_mz=parse_mz(values['exe'])
        need(values['exe']==src and b.map_normalize(values['map'],n)==parent_map and
             native_mz.program_image==original_mz.program_image and
             native_mz.relocations==original_mz.relocations and
             len(native_mz.relocations)==1553 and
             values['compact_mz']==target==compact_mz(values['exe']) and
             len(target)==130882 and
             scope['whole_original_program_and_MZ_equal'],
             'entire original MAIN and separate standard compact DOS MZ file')
        outputs.append(values)
    need(len(outputs)==2 and outputs[0]['exe']==outputs[1]['exe'] and
         payload(outputs[0]['obj'])==payload(outputs[1]['obj']) and
         literal_fields(outputs[0]['obj'])==literal_fields(outputs[1]['obj']) and
         public_offsets(outputs[0]['obj'])==public_offsets(outputs[1]['obj']) and
         outputs[0]['compact_mz']==outputs[1]['compact_mz'],
         'both full bullet source OMF/EXE/MAP/MZ vectors repeat')
    return dict(complete=True,independent_Turbo_CPP_rounds=2,
         original_bullet_main_CODE_bytes=2602,
         original_386_PELLET_PUT_CODE_bytes=83,complete_original_BSS_bytes=9500,
         original_bullet_PUBLIC_entries=20,ordered_native_OMF_FIXUPPs=196,
         original_2_segment_CODE_exact=True,original_linker_MZ_relocations=1553,
         complete_original_japanese_130882_byte_FILE_equal_after_standard_MZ_format=True,
         direct_original_vendor_OMF_packet_identity=False,
         additional_canonical_factory_credit=0,whole_product_source_accepted=False,
         original_source_native_report_sha256=report_sha)

if __name__=='__main__':
    r=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(r,indent=2)+'\n')
    print('Bullet and GRCG: 2685 CODE / 9500 BSS, 20 PUBLIC/196 fixes, two exact original source-derived Japanese MAIN files.')
