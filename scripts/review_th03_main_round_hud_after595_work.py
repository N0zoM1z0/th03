#!/usr/bin/env python3
"""Read-only 3-object original MAIN result/shot/HUD C++ native proof."""
import json
import build_th03_main_round_hud_after595_work as b
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz

def review():
    c,h,prior=b.inputs()
    report=json.loads((b.ROOT/b.REPORT).read_text())
    report_sha=sha((b.ROOT/b.REPORT).read_bytes())
    src=b.sources(c)
    original={s:(b.WORK/f'obj/th03/{s}.obj').read_bytes() for s in b.ORDER}
    jap=b.read_verified_artifact(b.ROOT,b.find_artifact(
       b.load_target_manifest(b.ROOT/'config/targets.toml'),'th03-main'))
    need(report['complete'] and report['cold_rebuilt'] is False and
         report['library_rebuilt'] is False and
         report['native_project_objects_recompiled_per_round']==3 and
         report['original_other_project_objects_reused']==96 and
         (report['native_source_CODE_bytes'],report['original_PUBLIC_functions'],
          report['original_native_FIXUPP_fields'])==(2987,10,251) and
         report['canonical_factory_credit_changed'] is False and
         report['whole_project_source_accepted'] is False and
         report['parent_report_sha256']==c['parent_report_sha256'] and
         report['config_sha256']==h and
         report['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         report['sources_sha256']=={
           s:{k:sha(v) for k,v in val.items()} for s,val in src.items()} and
         report['original_object_sha256']=={s:sha(v) for s,v in original.items()} and
         report['original_japanese_MAIN_sha256']==sha(jap),
         'original 3 complete C++ source/OMF and Japanese target plus two-round parent pins')
    need((b.SCRATCH/'driver.py').read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         'actual native 16-bit compiler recipe retained')
    expected=[f'round{n}-{step}' for n in (1,2) for step in (
      'results-TC4-compile','shots-TC4-compile','intro-TC4-compile','normal-TLINK')]
    need(len(report['phases'])==8 and
         [x['label'] for x in report['phases']]==expected and
         all(x['returncode']==0 and sha((b.ROOT/x['log']).read_bytes())==x['log_sha256']
             for x in report['phases']),
         'eight genuine original 16-bit C++ compiler/linker phases and logs')
    target_mz=parse_mz(jap)
    pair=[]
    for n,row in enumerate(report['rounds'],1):
        old=prior['rounds'][n-1]['outputs']
        need(row['round']==n and row['actual_link_response_sha256']==sha(b.response(n)) and
             (b.SCRATCH/f'r{n}.@l').read_bytes()==b.response(n) and
             row['whole_original_source_derived_MZ_equal'],
             'exact normal 99-source-object original linker response')
        vals={name:b.read_pin(pin) for name,pin in row['outputs'].items()}
        need(set(vals)=={stem+'_obj' for stem in b.ORDER}|{'exe','map','compact_mz'},
             'complete original new project OBJ, EXE, MAP and full Japanese MZ products')
        for u in c['units']:
            stem=u['stem']
            o=vals[stem+'_obj']
            scope=b.object_scope(o,original[stem],u)
            need(scope==row['scopes'][stem] and
                 scope['CODE_bytes']==u['CODE_bytes'] and
                 scope['original_publics']==u['PUBLICs'] and
                 scope['ordered_native_FIXUPPs']==u['ordered_fixups'] and
                 scope['original_CODE_segment']==u['CODE_segment'] and
                 scope['complete_original_CODE_and_native_fields_equal'] and
                 scope['raw_vendor_OMF_packets_identical'] is False and
                 (b.SCRATCH/f'r{n}/{stem}.cpp').read_bytes()==
                   src[stem]['wrapper'].replace(b'\n',b'\r\n') and
                 (b.SCRATCH/f'r{n}/{stem}.obj').read_bytes()==o and
                 payload(o)==payload(original[stem]) and
                 literal_fields(o)==literal_fields(original[stem]) and
                 public_offsets(o)==public_offsets(original[stem]),
                 'real original natural source/entire CODE/FIXUPP/PUBLIC/'+stem)
        m=parse_mz(vals['exe'])
        need(vals['exe']==b.read_pin(old['exe']) and
             len(vals['exe'])==132322 and
             b.map_normalize(vals['map'],n)==b.read_pin(old['map']) and
             m.program_image==target_mz.program_image and
             m.relocations==target_mz.relocations and
             len(m.relocations)==1553 and
             vals['compact_mz']==compact_mz(vals['exe'])==jap and
             len(jap)==130882,
             'whole original Japanese MAIN program/1553 ordered relocations, exact MZ after separate format')
        pair.append(vals)
    need(len(pair)==2 and pair[0]['exe']==pair[1]['exe'] and
         pair[0]['compact_mz']==pair[1]['compact_mz'] and
         all(payload(pair[0][s+'_obj'])==payload(pair[1][s+'_obj']) and
             literal_fields(pair[0][s+'_obj'])==literal_fields(pair[1][s+'_obj'])
             for s in b.ORDER),
         'two whole independent original-source game binary vectors repeat')
    return dict(complete=True,native_Turbo_CPP_rounds=2,
        original_results_CODE_bytes=1060,
        original_shots_CODE_bytes=449,
        original_HUD_intro_CODE_bytes=1478,
        total_original_CODE_bytes=2987,
        original_functions=10,original_ordered_OMF_fields=251,
        full_original_Japanese_program_equal=True,
        original_1553_ordered_MZ_relocations_equal=True,
        entire_original_130882_byte_file_equal_after_distinct_MZ_format=True,
        vendor_original_OMF_packet_identity=False,
        authored_function_ledger_credit_added=0,
        canonical_factory_acceptance=False,
        native_source_report_sha256=report_sha)

if __name__=='__main__':
    result=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('Round results, player shots and HUD: 2987 original CODE, 10 PUBLICs, 251 native OMF fields; both Japanese MAIN files exact.')
