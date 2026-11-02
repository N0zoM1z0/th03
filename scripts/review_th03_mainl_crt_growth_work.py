#!/usr/bin/env python3
"""Independently recheck cumulative original DOS native CRT source links."""
import argparse
import json
from pathlib import Path

import build_th03_mainl_crt_growth_work as producer
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
PREFIX='.analysis/work/mainl-crt-growth-'


def review(mode):
    names=producer.source_names(mode)
    receipt=(ROOT/(PREFIX+mode+'-build.json')).read_bytes()
    r=json.loads(receipt)
    base,files,lib,members,_=producer.baseline_provider.baseline(ROOT)
    need(r['complete'] and not r['original_cold_rebuilt'] and
         not r['source_acceptance'] and r['added_accepted_bytes']==0 and
         r['mode']==mode and tuple(r['names'])==names and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(lib) and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['source_sha256']=={n:sha((ROOT/f'src/mainl/crt/{n}.asm').read_bytes())
                              for n in names},
         'unmodified accepted baseline and real current source/driver bindings')
    target=(producer.WORK/'bin/th03/mainl.target.exe').read_bytes()
    original_map=(producer.WORK/'obj/th03/mainl.map').read_bytes()
    original={n:producer.original_scope(n,(producer.WORK/'vendor'/f'{n}.obj').read_bytes())
              for n in names}
    need(json.loads(json.dumps(original))==r['original_native_scope'],
         'complete literal original owner profiles')
    expected=sorted(names,key=lambda n:producer.KNOWN[n][0])
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two complete native source rounds')
    # Preserve actual chronological round order: all assemblies, then TLIB/TLINK.
    phase_names=['extract']
    for i in (1,2):
        phase_names += [f'round{i}-assemble-{n}' for n in names]
        phase_names += [f'round{i}-library',f'round{i}-link']
    need([x['label'] for x in r['phases']]==phase_names and
         all(x['returncode']==0 and sha((ROOT/x['log_path']).read_bytes())==
             x['log_sha256'] for x in r['phases']),
         'actual original tool commands and successful retained phase logs')
    vectors=[]
    for row in r['rounds']:
        need(set(row['outputs'])==set(names)|{'lib','exe','map'},
             'complete original native source OBJ/LIB/EXE/MAP vector')
        output={}
        for key,metadata in row['outputs'].items():
            raw=(ROOT/metadata['path']).read_bytes()
            need(metadata==dict(path=metadata['path'],bytes=len(raw),sha256=sha(raw)),
                 'unchanged complete raw native '+key)
            output[key]=raw
        source_objs={n:output[n] for n in names}
        need(all(producer.original_scope(n,source_objs[n])==original[n]
                 for n in names),'every native CODE byte/field/public/group exactly original')
        compared=compare_members(members,library_members(output['lib']),source_objs)
        need(compared==row['library_comparison'] and
             compared['replaced_members']==expected and
             compared['contextual_members_unchanged']==893-len(names),
             'original source member positions and all other program records')
        need(output['exe']==target and output['map']==original_map,
             'entire Japanese decoded MAINL EXE/MAP raw equality')
        mz=parse_mz(output['exe'])
        need(mz.valid and len(output['exe'])==67372 and len(mz.relocations)==677,
             'complete original relocation-bearing MZ product')
        vectors.append(output)
    need(vectors[0]==vectors[1], 'two identical raw complete native output vectors')
    return dict(complete=True,mode=mode,source_names=names,
                source_acceptance=False,accepted_source_bytes_added=0,
                full_cold_replay=False,replaced_members=expected,
                original_library_members=893,untouched_member_programs=893-len(names),
                original_and_native_CODE_bytes={n:[original[n]['CODE_bytes']]*2
                                                for n in names},
                total_source_CODE_bytes=sum(original[n]['CODE_bytes'] for n in names),
                all_native_literally_equal=True,
                original_and_native_ordered_fields_equal=True,
                Japanese_decoded_EXE_raw_equal=True,Japanese_MAP_raw_equal=True,
                full_EXE_bytes=67372,MZ_relocations=677,
                native_rounds=2,build_report_sha256=sha(receipt),
                driver_sha256=sha((ROOT/producer.DRIVER).read_bytes()),
                published_accepted_CRT_unchanged=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('mode', choices=tuple(producer.MODES))
    args=parser.parse_args()
    result=review(args.mode)
    out=ROOT/(PREFIX+args.mode+'-review.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
