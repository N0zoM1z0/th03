#!/usr/bin/env python3
"""Read-only proof of two complete source-native MAINL cutscene C++ links."""
import json

import build_th03_mainl_cutscene_after573_work as b
from build_th03_mainl_resources_work import need,sha
from lib.pc98 import parse_mz
from build_th03_mainl_display_work import payload,literal_fields
from lib.mainl_owner_migrations import public_offsets


def review():
    c,cfg_sha=b.inputs()
    previous,previous_sha=b.base.load(b.prior.REPORT)
    report,report_sha=b.base.load(b.REPORT)
    wrapper,dependencies=b.sources(c)
    original=(b.WORK/c['original_object']).read_bytes()
    need(previous['complete'] and previous_sha==c['parent_report_sha256'],
         'real latest natural four-sound and original registration/input source-native parent')
    need(report['complete'] and report['cold_rebuilt'] is False and
         report['library_rebuilt'] is False and
         report['game_objects_recompiled_per_round']==1 and
         report['other_game_objects_reused']==35 and
         report['canonical_credit_changed'] is False and
         report['whole_product_source_accepted'] is False and
         (report['CUTSCENE_CODE_bytes'],report['source_near_procedures'],
          report['original_literal_fixups'])==(3195,13,236) and
         report['parent_report_sha256']==previous_sha and
         report['wrapper_sha256']==sha(wrapper) and
         report['dependencies_sha256']=={k:sha(v) for k,v in dependencies.items()} and
         report['original_object_sha256']==sha(original) and
         report['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         report['config_sha256']==cfg_sha,
         'all existing source-proof inputs and scoped native product boundaries')
    need((b.SCRATCH/'driver.py').read_bytes()==(b.ROOT/b.DRIVER).read_bytes() and
         (b.SCRATCH/'config.json').read_bytes()==(b.ROOT/b.CONFIG).read_bytes(),
         'actual original native compiler source recipe/cfg')
    expected=['round1-cutscene-TC4-compile','round1-normal-TLINK',
              'round2-cutscene-TC4-compile','round2-normal-TLINK']
    need(len(report['phases'])==4 and
         [x['label'] for x in report['phases']]==expected and
         all(x['returncode']==0 and sha((b.ROOT/x['log']).read_bytes())==x['log_sha256']
             for x in report['phases']),
         'actual two complete TC4/TLINK native writer phase logs')
    from lib.targets import read_verified_artifact,find_artifact,load_target_manifest
    target=(b.WORK/'bin/th03/mainl.target.exe').read_bytes()
    loaded=parse_mz(target)
    load_start=0x95F*16+0xB3E
    scope_rows=[x for x in loaded.relocations
                if load_start<=x.segment*16+x.offset<load_start+3195]
    need(len(scope_rows)==56,'all 56 original scoped literal MZ relocations')
    vectors=[]
    for n,row in enumerate(report['rounds'],1):
        prior=previous['rounds'][n-1]
        need(row['round']==n and row['response_sha256']==sha(b.response(n)) and
             (b.SCRATCH/f'r{n}.lnk').read_bytes()==b.response(n),
             'one original cutscene object and unchanged first-use order')
        output={key:b.base.checked(pin) for key,pin in row['outputs'].items()}
        obj=output['obj']
        need(set(output)=={'obj','exe','map'} and
             (b.SCRATCH/f'r{n}/cutscene.obj').read_bytes()==obj and
             (b.SCRATCH/f'r{n}/cutscene.cpp').read_bytes()==
               wrapper.replace(b'\n',b'\r\n'),
             'complete preserved C++ source and object for independent compiler round')
        b.scope(obj,original,c)
        need(len(payload(obj))==3195 and len(literal_fields(obj))==236 and
             len(public_offsets(obj))==13 and
             output['exe']==b.base.checked(prior['outputs']['exe'])==target and
             len(output['exe'])==67372 and
             parse_mz(output['exe']).relocations==loaded.relocations and
             len(loaded.relocations)==677 and
             b.normalize_map(output['map'],n)==b.base.checked(prior['outputs']['map']) and
             row['complete_original_cutscene_native_object_equal'] and
             row['full_Japanese_MAINL_EXE_equal'] and row['original_677_relocations_equal'],
             'entire 3195 CODE/236 OMF fields/13 funcs/56 local MZ fixes/whole 67372-byte EXE exact')
        vectors.append(output)
    need(len(vectors)==2 and vectors[0]['exe']==vectors[1]['exe'] and
         payload(vectors[0]['obj'])==payload(vectors[1]['obj']) and
         b.normalize_map(vectors[0]['map'],1)==b.normalize_map(vectors[1]['map'],2),
         'two native C++ compiler/linker source vectors repeat and preserve original MAP')
    return dict(complete=True,original_target_provenance='candidate-local-attested',
        complete_natural_CPP_cutscene_CODE_bytes=3195,
        existing_complete_procedures=13,
        original_CUTSCENE_OMF_FIXUPP_fields=236,
        original_scoped_MZ_relocations=56,
        fresh_Turbo_CPP_compiler_rounds=2,full_original_MAINL_EXE_equal=True,
        full_decoded_EXE_bytes=67372,full_original_MZ_relocations=677,
        historical_compiler_OMF_packet_identity_proved=False,
        new_authored_function_credit=0,new_canonical_factory_acceptance=False,
        new_whole_product_source_accepted=False,
        source_native_build_report_sha256=report_sha)


if __name__=='__main__':
    r=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(r,indent=2)+'\n')
    print('MAINL large cutscene natural C++ 3195 CODE/13 procedures/236 native fields/56 MZ sites: two whole 67372-byte EXEs exact.')
