#!/usr/bin/env python3
"""Review real BCC/TASM memory/string CRT source additions atop whole qsort/xx.

Independent full object, all ordered OMF fields, genuine 893-member TLIB,
native MAP/decoded Japanese MAINL EXE and two deterministic raw rounds.
"""
import argparse
import json
from pathlib import Path

import build_th03_mainl_native_extension_work as producer
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
PREFIX=producer.PREFIX


def review(mode):
    need(mode in producer.MODES,'supported source-only CRT extension')
    names=producer.MODES[mode]
    receipt=(ROOT/(PREFIX+mode+'-build.json')).read_bytes()
    r=json.loads(receipt)
    base,files,accepted,members,old,prevhash=producer.retained()
    vendor={name:producer.original_scope(name,
        (producer.WORK/'vendor'/f'{name}.obj').read_bytes()) for name in names}
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['mode']==mode and tuple(r['names'])==names and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_eighteen_source_receipt_sha256']==prevhash and
         r['source_sha256']=={n:sha((ROOT/f'src/mainl/crt/{n}.asm').read_bytes())
                              for n in names} and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['original_profiles']==json.loads(json.dumps(vendor)),
         'original immutable source candidates and current accepted baseline')
    need(len(r['rounds'])==2 and [x['round'] for x in r['rounds']]==[1,2],
         'two complete native original programmer-verified source rounds')
    phases=['extract']
    for round_no in (1,2):
        phases.extend(f'round{round_no}-assemble-{n}' for n in names)
        phases.extend([f'round{round_no}-library',f'round{round_no}-link'])
    need([x['label'] for x in r['phases']]==phases and
         all(x['returncode']==0 and sha((ROOT/x['log_path']).read_bytes())==
             x['log_sha256'] for x in r['phases']),
         'actual complete TASM/TLIB/TLINK writer phase logs in original order')
    expected=sorted(set(old[0])|set(names))
    vectors=[]
    for idx,row in enumerate(r['rounds']):
        need(set(row['outputs'])==set(names)|{'lib','exe','map'},
             'complete native program OBJ/LIB/EXE/MAP output vectors')
        out={}
        for kind,info in row['outputs'].items():
            blob=(ROOT/info['path']).read_bytes()
            need(info==dict(path=info['path'],bytes=len(blob),sha256=sha(blob)),
                 'complete original native raw '+kind+' file identity')
            out[kind]=blob
        need(all(producer.original_scope(n,out[n])==vendor[n] for n in names),
             'all source CODE/PUBDEF/EXTDEF/GRPDEF/literal FIXUPP records equal original')
        originals=dict(old[idx],**{n:out[n] for n in names})
        compared=compare_members(members,library_members(out['lib']),originals)
        need(compared==row['library_comparison'] and
             compared['replaced_members']==expected and
             compared['contextual_members_unchanged']==893-len(expected),
             'all exact source replacements at original CRT slots and unchanged native context')
        need(out['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete Japanese decoded MAINL and original native MAP bitwise equal')
        mz=parse_mz(out['exe'])
        need(mz.valid and len(out['exe'])==67372 and len(mz.relocations)==677,
             'full Japanese original relocation-bearing DOS MZ executable')
        vectors.append(out)
    need(vectors[0]==vectors[1],
         'two complete deterministic original native source OBJ/LIB/EXE/MAP vectors')
    total=15786+sum(vendor[n]['CODE_bytes'] for n in names)
    return dict(complete=True,mode=mode,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                original_CRT_member_count=893,
                native_source_member_count=len(expected),
                unchanged_original_member_programs=893-len(expected),
                original_and_source_profiles=json.loads(json.dumps(vendor)),
                newly_recovered_CODE_bytes=sum(vendor[n]['CODE_bytes'] for n in names),
                joint_native_source_CODE_bytes=total,
                complete_native_CODE_equal=True,ordered_literal_FIXUPPs_equal=True,
                native_group_and_publics_equal=True,
                entire_Japanese_EXE_raw_equal=True,original_MAP_raw_equal=True,
                original_MZ_relocations=677,whole_EXE_bytes=67372,
                reproducible_native_rounds=2,
                current_build_sha256=sha(receipt),parent_18_source_sha256=prevhash,
                original_accepted_publication_unchanged=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('mode',choices=tuple(producer.MODES))
    args=ap.parse_args()
    result=review(args.mode)
    (ROOT/(PREFIX+args.mode+'-review.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
