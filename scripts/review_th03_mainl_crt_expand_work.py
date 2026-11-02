#!/usr/bin/env python3
"""Independent real TASM/TLIB/TLINK review of 13/14 cumulative CRT sources."""
import argparse
import json
from pathlib import Path

import build_th03_mainl_crt_expand_work as producer
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]


def review(mode):
    need(mode in producer.MODES,'supported new real CRT member scope')
    names=producer.MODES[mode]
    raw=(ROOT/(producer.PREFIX+mode+'-build.json')).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,parents,priorhash=producer.retained()
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['mode']==mode and tuple(r['names'])==names and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['parent_twelve_source_sha256']==priorhash and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['source_sha256']=={n:sha((ROOT/f'src/mainl/crt/{n}.asm').read_bytes()) for n in names},
         'original immutable source,caller provenance and current producer')
    expected_profiles={}
    for name in names:
        original=(producer.WORK/'vendor'/f'{name}.obj').read_bytes()
        expected_profiles[name]=producer.scope(name,original)
    need(json.loads(json.dumps(expected_profiles))==r['original_profiles'],
         'actual original full CODE/PUBDEF/GRPDEF/fixup fields')
    need(len(r['rounds'])==2 and [x['round'] for x in r['rounds']]==[1,2],
         'two actual native source assembler/library/link rounds')
    expected_phases=['extract']
    for i in (1,2):
        expected_phases.extend(f'round{i}-assemble-{n}' for n in names)
        expected_phases.extend([f'round{i}-library',f'round{i}-link'])
    need([p['label'] for p in r['phases']]==expected_phases and
         all(p['returncode']==0 and sha((ROOT/p['log_path']).read_bytes())==
             p['log_sha256'] for p in r['phases']),
         'real original writer phase log contents and phase order')
    vectors=[]
    for i,row in enumerate(r['rounds']):
        need(set(row['outputs'])==set(names)|{'lib','exe','map'},
             'full original native new OMF/CRT/exe/map output vector')
        output={}
        for kind,q in row['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'complete retained raw output '+kind)
            output[kind]=data
        for name in names:
            need(producer.scope(name,output[name])==expected_profiles[name],
                 'original entire native source module bytes/relocations '+name)
        src=dict(parents[i],**{n:output[n] for n in names})
        compared=compare_members(members,library_members(output['lib']),src)
        need(row['library_comparison']==compared and
             compared['replaced_members']==[m.name for m in members if m.name in src] and
             compared['contextual_members_unchanged']==893-len(src),
             'complete original library order and all unchanged member programs')
        need(output['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             output['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'entire complete Japanese decoded MAINL exe and original MAP exact')
        mz=parse_mz(output['exe'])
        need(mz.valid and len(output['exe'])==67372 and len(mz.relocations)==677,
             'all original MZ relocation entries and original size')
        vectors.append(output)
    need(vectors[0]==vectors[1],'two equal full raw native OMF/LIB/EXE/MAP vectors')
    total=13783+sum(expected_profiles[n]['CODE_bytes'] for n in names)
    return dict(complete=True,mode=mode,original_cold_rebuilt=False,
                source_acceptance=False,added_accepted_bytes=0,
                source_members=12+len(names),original_CRT_members=893,
                unchanged_original_program_records=881-len(names),
                new_module_names=names,new_module_CODE_bytes={
                    n:expected_profiles[n]['CODE_bytes'] for n in names},
                native_CODE_and_ordered_fields_equal=True,
                source_built_total_CODE_bytes=total,
                original_decoded_Japanese_EXE_raw_equal=True,
                original_complete_MAP_raw_equal=True,
                original_EXE_file_bytes=67372,original_MZ_relocations=677,
                complete_native_rounds=2,parent_source_build_sha256=priorhash,
                retained_build_receipt_sha256=sha(raw),
                accepted_publication_unchanged=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('mode',choices=tuple(producer.MODES))
    args=ap.parse_args()
    result=review(args.mode)
    (ROOT/(producer.PREFIX+args.mode+'-review.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
