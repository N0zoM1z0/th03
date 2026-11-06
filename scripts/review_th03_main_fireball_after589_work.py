#!/usr/bin/env python3
"""Read-only two-round original native fireball/explosion TC4/source MAIN link."""
import json
import build_th03_main_fireball_after589_work as b
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz

def review():
    cfg,cfg_sha,parent=b.inputs()
    record=json.loads((b.ROOT/b.REPORT).read_text())
    report_sha=sha((b.ROOT/b.REPORT).read_bytes())
    src=b.source_inputs(cfg)
    original={stem:(b.WORK/f'obj/th03/{stem}.obj').read_bytes() for stem in b.ORDER}
    target=b.parent.read_verified_artifact(b.ROOT,b.parent.find_artifact(
      b.parent.load_target_manifest(b.ROOT/'config/targets.toml'),'th03-main'))
    need(record['complete'] and record['cold_rebuilt'] is False and
         record['library_rebuilt'] is False and
         record['project_objects_recompiled_per_round']==2 and
         record['other_project_objects_reused']==97 and
         (record['total_CODE_bytes'],record['total_DATA_bytes'],record['total_BSS_bytes'])==(2185,1,1) and
         record['canonical_factory_credit_changed'] is False and
         record['whole_project_source_accepted'] is False and
         record['config_sha256']==cfg_sha and
         record['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         record['parent_report_sha256']==cfg['parent_report_sha256'] and
         record['source_sha256']==
            {k:{x:sha(y) for x,y in row.items()} for k,row in src.items()} and
         record['original_object_sha256']=={k:sha(v) for k,v in original.items()} and
         record['original_japanese_file_sha256']==sha(target),
         'all real fixed 16-bit game source bindings, old original and target integrity')
    need((b.SCRATCH/'driver.py').read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         'actual native compiler recipe and fixed parent')
    phases=[f'round{n}-{x}' for n in (1,2)
           for x in ('e_fireb-TC4','e_expl-TC4','normal-TLINK')]
    need(len(record['phases'])==6 and
         [x['label'] for x in record['phases']]==phases and
         all(x['exit_code']==0 and sha((b.ROOT/x['log']).read_bytes())==x['log_sha256']
             for x in record['phases']),
         'both real TCC/TLINK rounds with all six successful writer logs')
    target_mz=parse_mz(target)
    output_pair=[]
    for n,row in enumerate(record['rounds'],1):
        old=parent['rounds'][n-1]['outputs']
        need(row['round']==n and
             row['original_source_response_sha256']==sha(b.response(n)) and
             (b.SCRATCH/f'r{n}.@l').read_bytes()==b.response(n) and
             row['full_original_japanese_file_equal_after_explicit_MZ_format'],
             'genuine two-object source replacement normal MAIN link response')
        out={k:b.read_pin(p) for k,p in row['outputs'].items()}
        need(set(out)=={'e_fireb_obj','e_expl_obj','exe','map','compact_mz'},
             'entire original two-object native EXE/MAP/standard MZ vectors SHA-pinned')
        for u in cfg['units']:
            stem=u['stem']
            obj=out[stem+'_obj']
            scope=b.original_scope(obj,original[stem],u)
            need(scope==row['original_object_scope'][stem] and
                 scope['CODE_bytes']==u['CODE_bytes'] and
                 scope['DATA_bytes']==u['DATA_bytes'] and
                 scope['BSS_bytes']==u['BSS_bytes'] and
                 scope['PUBLICs']==u['publics'] and
                 scope['ordered_FIXUPP']==u['fixups'] and
                 scope['complete_original_linker_semantics'] and
                 scope['original_vendor_packet_identity'] is False and
                 (b.SCRATCH/f'r{n}/{stem}.obj').read_bytes()==obj and
                 (b.SCRATCH/f'r{n}/{stem}.cpp').read_bytes()==
                     src[stem]['wrapper'].replace(b'\n',b'\r\n'),
                 'complete actual source/OMF CODE, DATA, BSS and ordered fixup provenance '+stem)
        m=parse_mz(out['exe'])
        need(out['exe']==b.read_pin(old['exe']) and
             b.map_normalized(out['map'],n)==b.read_pin(old['map']) and
             len(out['exe'])==132322 and
             m.program_image==target_mz.program_image and
             m.relocations==target_mz.relocations and len(m.relocations)==1553 and
             out['compact_mz']==compact_mz(out['exe'])==target,
             'all source program bytes, original ordered relocations and full standalone Japanese MZ')
        output_pair.append(out)
    need(len(output_pair)==2 and output_pair[0]['exe']==output_pair[1]['exe'] and
         output_pair[0]['compact_mz']==output_pair[1]['compact_mz'] and
         all(payload(output_pair[0][stem+'_obj'])==payload(output_pair[1][stem+'_obj'])
             and literal_fields(output_pair[0][stem+'_obj'])==
                 literal_fields(output_pair[1][stem+'_obj']) for stem in b.ORDER),
         'two independent source compiler and full original executable vectors repeat')
    return dict(complete=True,original_fireball_CODE_bytes=1555,
        original_explosion_hittest_CODE_bytes=630,
        original_initialized_DATA_bytes=1,original_BSS_bytes=1,
        original_PUBLIC_symbols=11,original_ordered_OMF_FIXUPPs=164,
        independent_native_Turbo_CPP_rounds=2,
        whole_original_japanese_program_and_1553_MZ_relocations_equal=True,
        full_original_130882_byte_japanese_MZ_file_equal_after_independent_format=True,
        direct_original_vendors_raw_OMF_packets_identical=False,
        canonical_factory_credit=0,whole_project_source_accepted=False,
        native_source_report_sha256=report_sha)

if __name__=='__main__':
    r=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(r,indent=2)+'\n')
    print('Fireball/explosion original C++: 2185 CODE, 164 OMF fields, 2 original MAIN full-file exact native rounds.')
