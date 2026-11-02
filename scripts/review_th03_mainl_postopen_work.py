#!/usr/bin/env python3
"""Review complete native stream input CRT sources and original MAINL link."""
import argparse,json
from pathlib import Path
import build_th03_mainl_postopen_work as p
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REVIEW_PREFIX=p.PREFIX


def review(mode):
    names=p.MODES[mode]
    raw=(ROOT/(p.PREFIX+mode+'-build.json')).read_bytes()
    rec=json.loads(raw)
    base,files,accepted,members,prior,parenthash=p.retained()
    original={n:p.scope(n,(p.WORK/'vendor'/(n+'.obj')).read_bytes()) for n in names}
    source_hashes={n:sha((ROOT/('src/mainl/crt/'+n+'.asm')).read_bytes()) for n in names}
    need(rec['complete'] and not rec['source_acceptance'] and
         rec['added_accepted_bytes']==0 and not rec['original_cold_rebuilt'] and
         rec['parent_fopen_OMF_order_open'] is True and
         rec['parent_fclose_near_frame_open'] is True and
         rec['mode']==mode and tuple(rec['names'])==names and
         rec['accepted_baseline']==base and rec['accepted_library_sha256']==sha(accepted) and
         rec['previous_forty_source_build_sha256']==parenthash and
         rec['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         rec['source_sha256']==source_hashes and
         rec['original_profiles']==json.loads(json.dumps(original)) and
         rec['native_assembler_flags']==p.TASM_FLAGS,
         'original unchanged native 36-source parent and affected sources')
    need(len(rec['rounds'])==2 and [r['round'] for r in rec['rounds']]==[1,2],
         'two independent native source rounds')
    steps=['extract']
    for i in (1,2):
        steps.extend(f'round{i}-assemble-{n}' for n in names)
        steps.extend([f'round{i}-library',f'round{i}-link'])
    need([q['label'] for q in rec['phases']]==steps and
         all(q['returncode']==0 and sha((ROOT/q['log_path']).read_bytes())==
             q['log_sha256'] for q in rec['phases']),
         'actual original TASM/TLIB/TLINK output command/phase logs')
    output_vectors=[]
    expected=sorted(set(prior[0])|set(names))
    for idx,row in enumerate(rec['rounds']):
        need(set(row['outputs'])==set(names)|{'lib','exe','map'},
             'complete source OMF objects and native library/product pair')
        out={}
        for name,meta in row['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'whole literal raw native '+name+' file identity')
            out[name]=data
        need(all(p.scope(n,out[n])==original[n] for n in names),
             'all source original CODE/PUBDEF/EXTDEF/GRPDEF/ordered FIXUPPs exact')
        source_objs=dict(prior[idx],**{n:out[n] for n in names})
        compared=compare_members(members,library_members(out['lib']),source_objs)
        need(compared==row['library_comparison'] and
             compared['replaced_members']==expected and
             compared['contextual_members_unchanged']==893-len(expected),
             'all original source member indices and other native programs unchanged')
        need(out['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete pinned Japanese decoded MAINL executable and MAP raw equal')
        mz=parse_mz(out['exe'])
        need(mz.valid and len(out['exe'])==67372 and len(mz.relocations)==677,
             'original DOS MZ size and whole original relocation vector')
        output_vectors.append(out)
    need(output_vectors[0]==output_vectors[1],
         'two byte-identical full native OBJ/LIB/EXE/MAP source vectors')
    return dict(complete=True,mode=mode,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                original_CRT_members=893,native_source_modules=len(expected),
                untouched_original_member_programs=893-len(expected),
                current_source_members=list(names),
                exact_original_native_CODE_bytes=sum(original[n]['CODE_bytes'] for n in names),
                cumulative_source_CODE_bytes=22170+
                    sum(original[n]['CODE_bytes'] for n in names),
                actual_original_source_profiles=json.loads(json.dumps(original)),
                complete_native_CODE_equal=True,all_ordered_native_FIXUPPs_equal=True,
                original_extdefs_publics_groups_equal=True,
                entire_Japanese_EXE_raw_equal=True,entire_MAP_raw_equal=True,
                original_MZ_relocations=677,original_EXE_file_bytes=67372,
                native_repeated_rounds=2,
                prior_fopen_FIXUPP_order_open=True,prior_fclose_near_frame_open=True,
                retained_build_report_sha256=sha(raw),
                parent_40_source_receipt_sha256=parenthash,
                accepted_publication_unchanged=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('mode',choices=tuple(p.MODES))
    args=ap.parse_args()
    x=review(args.mode)
    (ROOT/(REVIEW_PREFIX+args.mode+'-review.json')).write_text(json.dumps(x,indent=2)+'\n')
    print(json.dumps(x,indent=2))
