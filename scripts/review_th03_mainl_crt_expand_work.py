#!/usr/bin/env python3
"""Independently review original 16-bit CRT strcpy-family source-only extensions."""
import argparse
import json
from pathlib import Path

import build_th03_mainl_crt_expand_work as producer
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import compare_members,library_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
PREFIX='.analysis/work/mainl-crt-expand-'


def review(mode):
    names=producer.MODES[mode]
    raw=(ROOT/(PREFIX+mode+'-build.json')).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,preceding,parenthash=producer.retained()
    current_sources={n:(ROOT/f'src/mainl/crt/{n}.asm').read_bytes() for n in names}
    original={n:producer.scope(n,(producer.WORK/'vendor'/(n+'.obj')).read_bytes())
              for n in names}
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['mode']==mode and r['names']==list(names) and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['parent_twelve_source_sha256']==parenthash and
         r['source_sha256']=={n:sha(b) for n,b in current_sources.items()} and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['original_profiles']==json.loads(json.dumps(original)),
         'pinned original CRT and maintained original native code/fields')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two complete native TASM/TLIB/TLINK rounds')
    phases=['extract']
    for i in (1,2):
        phases += [f'round{i}-assemble-{n}' for n in names]
        phases += [f'round{i}-library',f'round{i}-link']
    need([p['label'] for p in r['phases']]==phases and all(
         p['returncode']==0 and
         sha((ROOT/p['log_path']).read_bytes())==p['log_sha256']
         for p in r['phases']), 'unmodified original native source phase logs')
    target=(producer.WORK/'bin/th03/mainl.target.exe').read_bytes()
    original_map=(producer.WORK/'obj/th03/mainl.map').read_bytes()
    expected=[m.name for m in members if m.name in set(preceding[0])|set(names)]
    vectors=[]
    for round_no,row in enumerate(r['rounds']):
        need(set(row['outputs'])==set(names)|{'lib','exe','map'},
             'complete source OBJ/LIB/EXE/MAP outputs')
        outputs={}
        for name,meta in row['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'actual complete native byte vector '+name)
            outputs[name]=data
        need(all(producer.scope(n,outputs[n])==original[n] for n in names),
             'all native original CODE/PUBDEF/GROUP/FIXUPP fields exact')
        sources=dict(preceding[round_no],**{n:outputs[n] for n in names})
        comparison=compare_members(members,library_members(outputs['lib']),sources)
        need(comparison==row['library_comparison'] and
             comparison['replaced_members']==expected and
             comparison['contextual_members_unchanged']==893-len(sources),
             'original native library member ordering and all other programs unchanged')
        need(outputs['exe']==target and outputs['map']==original_map,
             'complete fixed Japanese decoded MAINL EXE and MAP exact')
        mz=parse_mz(outputs['exe'])
        need(mz.valid and len(outputs['exe'])==67372 and len(mz.relocations)==677,
             'actual complete relocation-bearing DOS MZ original')
        vectors.append(outputs)
    need(vectors[0]==vectors[1],'raw native OBJ/LIB/EXE/MAP full vectors reproduced twice')
    return dict(complete=True,mode=mode,source_acceptance=False,
                added_accepted_bytes=0,full_cold_replay=False,
                original_library_members=893,
                native_source_members=len(expected),
                unchanged_original_member_programs=893-len(expected),
                new_source_names=names,new_source_CODE_bytes=sum(producer.NATIVE[n][1] for n in names),
                cumulative_source_CODE_bytes=13783+sum(producer.NATIVE[n][1] for n in names),
                original_and_native_CODE_equal=True,
                ordered_native_FIXUPPs_equal=True,
                original_publics_and_groups_equal=True,
                original_exe_bytes=67372,original_mz_relocation_count=677,
                whole_exe_equal=True,whole_map_equal=True,
                deterministic_native_rounds=2,
                original_and_source_profiles=json.loads(json.dumps(original)),
                receipt_sha256=sha(raw),accepted_CRT_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('mode',choices=tuple(producer.MODES))
    args=p.parse_args()
    r=review(args.mode)
    (ROOT/(PREFIX+args.mode+'-review.json')).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
