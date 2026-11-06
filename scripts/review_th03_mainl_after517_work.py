#!/usr/bin/env python3
"""Source-bound review of incremental CRT recovery without a cold replay."""
import argparse,json,sys
from pathlib import Path
# The unchanged historical import chain is hundreds of native source layers.
# Python 3.12 + legacy Unicorn require setuptools' distutils shim at entry.
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),5000))
import build_th03_mainl_after517_work as b
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import library_members,compare_members,object_program_records
from lib.pc98 import parse_mz
from build_th03_mainl_display_work import literal_fields
from probe_th03_mainl_large_fixups import original_literal_fixups
from lib.decoded_mainl_display_native import externs

ROOT=Path(__file__).resolve().parents[1]


def review(mode):
    names=b.MODES[mode]
    raw=(ROOT/(b.PREFIX+mode+'-build.json')).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,carry,parenthash=b.retained()
    need(r['stdio_layout_sha256']==sha((ROOT/'src/mainl/crt/stdio_layout.inc').read_bytes()),
         'original maintained isatty include dependency bound to source')
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         isinstance(r['literal_OMF_FIXUPP_equal'],bool) and
         r['parent_receipt_sha256']==parenthash and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['driver_sha256']==sha((ROOT/b.DRIVER).read_bytes()) and
         r['mode']==mode and tuple(r['names'])==names and
         r['assembler_flags']==b.TASM_FLAGS and
         r['source_paths']=={n:'src/mainl/crt/'+n+'.asm' for n in names} and
         r['source_sha256']=={n:sha((ROOT/'src/mainl/crt'/(n+'.asm')).read_bytes())
                              for n in names} and len(r['rounds'])==2,
         'source-bound original CRT scoped native build declaration')
    original={n:b.scope(n,b.original_library_member(members[b.NATIVE[n]['index']]))
              for n in names}
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
        literal_omf={}
        for n in names:
            original_blob=b.original_library_member(members[b.NATIVE[n]['index']])
            borland=original_literal_fixups(original_blob)
            tasm=literal_fields(outputs[n])
            need(len(borland)==len(tasm)==18,
                 'all original threaded Borland and TASM fields')
            o_imports=externs(original_blob)
            n_imports=externs(outputs[n])
            frame4=[]
            for f,g in zip(sorted(borland,key=lambda x:x['site']),
                           sorted(tasm,key=lambda x:x['site'])):
                need(all(f[k]==g[k] for k in ('segment','site',
                     'location_type','width','segment_relative',
                     'target_method','addend')),
                     'actual original x87 location/width/addend '+n)
                need(f['target_method']==2 and
                     o_imports[f['target']-1]==n_imports[g['target']-1],
                     'exact original imported symbol identity '+n)
                symbol=o_imports[f['target']-1]
                if symbol in ('FIDRQQ','FIWRQQ','FIERQQ'):
                    need((f['frame_method'],f['frame'],
                          g['frame_method'],g['frame'])==(4,None,5,None),
                         'only original Borland frame4/x87 TASM frame5')
                    frame4.append(f['site'])
                else:
                    need((f['frame_method'],f['frame'])==
                         (g['frame_method'],g['frame']),
                         'non-FPU original OMF frame unchanged')
            need(len(frame4)==14,'exact number of original FPU sites')
            literal_omf[n]=False
        original_program={n:object_program_records(outputs[n])==
            members[b.NATIVE[n]['index']].program_records for n in names}
        need(row['original_program_equal_by_member']==original_program,
             'actual original Borland CL.LIB record equality for every member')
        need(row['literal_omf_fixupp_equal_by_member']==literal_omf and
             r['literal_OMF_FIXUPP_equal']==all(literal_omf.values()),
             'actual full native ordered FIXUPP/frame status per member')
        source=dict(carry[i][0],**{n:outputs[n] for n in names})
        cmp=compare_members(members,library_members(outputs['lib']),source)
        need(row['library_comparison']==cmp and len(source)==724+len(names) and
             cmp['contextual_members_unchanged']==893-len(source) and
             outputs['exe']==(b.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(b.WORK/'obj/th03/mainl.map').read_bytes(),
             'all native CRT membership and complete original EXE/MAP raw-equal')
        mz=parse_mz(outputs['exe'])
        need(mz.valid and len(outputs['exe'])==67372 and
             len(mz.relocations)==677,
             'original decoded Japanese DOS MZ and full relocation inventory')
        vectors.append(outputs)
    need(vectors[0]==vectors[1],
         'two byte-identical native producer rounds')
    return dict(complete=True,mode=mode,native_rounds=2,
                original_CRT_members=893,native_source_members=724+len(names),
                untouched_vendor_members=169-len(names),
                added_CODE_bytes=sum(original[n]['CODE_bytes'] for n in names),
                source_CRT_CODE_bytes=193815+sum(original[n]['CODE_bytes'] for n in names),
                complete_original_CODE_DATA_equal=True,
                complete_native_link_EXE_MAP_equal=True,
                original_MZ_relocations=677,
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
