#!/usr/bin/env python3
"""Source-bound review of incremental CRT recovery without a cold replay."""
import argparse,json,sys
from pathlib import Path
# The unchanged historical import chain is hundreds of native source layers.
# Python 3.12 + legacy Unicorn require setuptools' distutils shim at entry.
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),5000))
import build_th03_mainl_after533_work as b
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import library_members,compare_members,object_program_records
from lib.pc98 import parse_mz
from build_th03_mainl_display_work import literal_fields

ROOT=Path(__file__).resolve().parents[1]


def review(mode):
    names=b.MODES[mode]
    raw=(ROOT/(b.PREFIX+mode+'-build.json')).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,carry,parenthash=b.retained()
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         isinstance(r['literal_OMF_FIXUPP_equal'],bool) and
         r['parent_receipt_sha256']==parenthash and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['driver_sha256']==sha((ROOT/b.DRIVER).read_bytes()) and
         r['mode']==mode and tuple(r['names'])==names and
         r['assembler_flags']==b.TASM_FLAGS and
         r['source_paths']=={n:b.SOURCE_PATHS[n] for n in names} and
         r['source_sha256']=={n:sha((ROOT/b.SOURCE_PATHS[n]).read_bytes())
                              for n in names} and len(r['rounds'])==2,
         'source-bound original CRT scoped native build declaration')
    need(r['source_include_sha256']=={p:sha((ROOT/p).read_bytes()) for p in b.INCLUDES},
         'actual maintained include dependency set')
    original_programs,original_library_hash=b.original_member_programs()
    cold_raw=(b.build.OUT/'mainl-build.json').read_bytes()
    need(r['original_compiler_library_sha256']==original_library_hash and
         sha(cold_raw)==base['cold_report_sha256'] and
         json.loads(cold_raw)['vendor_library_sha256']==original_library_hash,
         'original compiler library hash bound through the retained cold receipt')
    original={n:b.scope(n,original_programs[n]) for n in names}
    need(r['original_profiles']==json.loads(json.dumps(original)) and
         [q['round'] for q in r['rounds']]==[1,2],
         'whole original member interface and both native rounds')
    phases=['extract']
    for i in (1,2):
        phases += [f'round{i}-assemble-{n}' for n in names]
        phases += [f'round{i}-library',f'round{i}-link']
    need([q['label'] for q in r['phases']]==phases and
         all(q['returncode']==0 and sha((ROOT/q['log_path']).read_bytes())==
             q['log_sha256'] for q in r['phases']),
         'actual successful native TASM/TLIB/TLINK writer phases')
    vectors=[]
    for i,row in enumerate(r['rounds']):
        outputs={}
        need(set(row['outputs'])==set(names)|{'lib','exe','map'},
             'whole native OBJ/LIB/EXE/MAP vector')
        for kind,meta in row['outputs'].items():
            blob=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                 'retained entire native output '+kind)
            outputs[kind]=blob
        need(all(b.scope(n,outputs[n])==original[n] for n in names),
             'all original CODE/DATA bytes and relocation sites/targets')
        literal_omf={n:literal_fields(outputs[n])==literal_fields(original_programs[n])
            for n in names}
        original_program={n:object_program_records(outputs[n])==
            object_program_records(original_programs[n]) for n in names}
        need(row['original_program_equal_by_member']==original_program,
             'actual original Borland CL.LIB record equality for every member')
        need(literal_omf=={n:not bool(b.NATIVE[n]['near_frame_sites']) for n in names},
             'all twelve DATA/metadata members have literal ordered FIXUPP equality')
        gaps={n:b.frame_differences(original_programs[n],outputs[n]) for n in names}
        need(row['raw_frame_differences_by_member']==gaps and
             sum(len(v) for v in gaps.values())==0,
             'independent original/native enumeration of zero literal field/frame differences')
        need(row['literal_omf_fixupp_equal_by_member']==literal_omf and
             r['literal_OMF_FIXUPP_equal']==all(literal_omf.values()),
             'actual full native ordered FIXUPP/frame status per member')
        source=dict(carry[i][0],**{n:outputs[n] for n in names})
        cmp=compare_members(members,library_members(outputs['lib']),source)
        need(row['library_comparison']==cmp and len(source)==877+len(names) and
             cmp['contextual_members_unchanged']==893-len(source) and
             outputs['exe']==(b.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(b.WORK/'obj/th03/mainl.map').read_bytes(),
             'all native CRT membership and complete original EXE/MAP raw-equal')
        need(all(m.name in source for m in members[696:893]),
             'all 197 original iostream slots 696 through 892 source-linked')
        mz=parse_mz(outputs['exe'])
        need(mz.valid and len(outputs['exe'])==67372 and
             len(mz.relocations)==677,
             'original decoded Japanese DOS MZ and full relocation inventory')
        vectors.append(outputs)
    need(vectors[0]==vectors[1],
         'two byte-identical native producer rounds')
    return dict(complete=True,mode=mode,native_rounds=2,
                original_CRT_members=893,native_source_members=877+len(names),
                retained_context_members=16-len(names),
                added_CODE_bytes=sum(original[n]['CODE_bytes'] for n in names),
                source_CRT_CODE_bytes=209016+sum(original[n]['CODE_bytes'] for n in names),
                added_DATA_initialized_bytes=sum(original[n]['DATA_bytes'] for n in names),
                added_BSS_bytes=sum(original[n]['BSS_bytes'] for n in names),
                added_INITDATA_initialized_bytes=sum(original[n]['INITDATA_initialized_bytes'] for n in names),
                original_compiler_library_sha256=original_library_hash,
                complete_original_CODE_DATA_equal=True,
                complete_original_initialized_and_uninitialized_storage_equal=True,
                inline_CODE_metadata_bytes=0,
                original_ordered_ALIAS_records=sum(len(b.NATIVE[n]['alias_records']) for n in names),
                all_original_ordered_ALIAS_records_equal=True,
                original_iostream_slots_696_892_all_source_linked=True,
                original_iostream_block_members=197,
                complete_native_link_EXE_MAP_equal=True,
                original_MZ_relocations=677,
                original_ordered_logical_FIXUPP_fields=sum(b.NATIVE[n]['fields'] for n in names),
                original_literal_frame_differences=0,
                source_include_sha256=r['source_include_sha256'],
                original_literal_FIXUPP_equal=r['literal_OMF_FIXUPP_equal'],
                original_library_member_program_equal=all(
                    row['original_program_equal_by_member'][n]
                    for row in r['rounds'] for n in names),
                source_acceptance=False,original_cold_rebuilt=False,
                profiles=original)

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('mode',choices=tuple(b.MODES))
    arg=ap.parse_args()
    record=review(arg.mode)
    (ROOT/(b.PREFIX+arg.mode+'-review.json')).write_text(
        json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))
