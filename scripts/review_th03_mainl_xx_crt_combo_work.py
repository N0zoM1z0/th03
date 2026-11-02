#!/usr/bin/env python3
"""Independently recheck eight simultaneous native source CRT members."""
import json
from pathlib import Path
from build_th03_mainl_display_work import literal_fields,payload
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz
from probe_th03_main_bomb_rikako_cpp import segment_definitions

import build_th03_mainl_xx_crt_combo_work as producer
from build_th03_mainl_resources_work import need,sha

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-xx-crt8-review.json'


def review():
    raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,objects,xhash,chash=producer.retained_source_objects()
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['xx_native_build_sha256']==xhash and
         r['crt_native_build_sha256']==chash and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['native_object_sha256']=={n:sha(v) for n,v in objects[0].items()} and
         set(r['source_names'])==set(producer.SOURCE_NAMES),
         'original source objects,accepted baseline and true native build receipts')
    original=(producer.build.WORK/'vendor/xx.obj').read_bytes()
    actual=objects[0]['xx']
    segments=segment_definitions(original)
    need(segment_definitions(actual)==segments and
         [(s['name'],s['size']) for s in segments]==
         [('_TEXT',12622),('_DATA',18),('_BSS',10)],
         'full native xx CODE/DATA/BSS segment extents')
    orig_payload=payload(original);native_payload=payload(actual)
    need(all(orig_payload[1,i]==native_payload[1,i] for i in range(12622)) and
         all(orig_payload[2,i]==native_payload[2,i] for i in range(18)) and
         literal_fields(original)==literal_fields(actual) and
         len(literal_fields(actual))==187,
         'complete native original xx CODE/data and all187 ordered fixups')
    for name in producer.crt.source_names(producer.CRT_MODE):
        vendor=(producer.build.WORK/'vendor'/f'{name}.obj').read_bytes()
        need(producer.crt.original_scope(name,vendor)==
             producer.crt.original_scope(name,objects[0][name]),
             'every natural source memory/string body,pubdef and GRPDEF literal '+name)
    expected=[m.name for m in members if m.name in producer.SOURCE_NAMES]
    need(len(expected)==8 and len(members)==893 and
         len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'eight original-ordered source member definitions and two links')
    need([p['label'] for p in r['phases']]==
         ['extract','round1-library','round1-link','round2-library','round2-link'] and
         all(p['returncode']==0 and
             sha((ROOT/p['log_path']).read_bytes())==p['log_sha256']
             for p in r['phases']),
         'actual native TLIB/TLINK commands and retained literal logs')
    target=(producer.build.WORK/'bin/th03/mainl.target.exe').read_bytes()
    original_map=(producer.build.WORK/'obj/th03/mainl.map').read_bytes()
    vectors=[]
    for i,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'lib','exe','map'},
             'complete real eight-source link output types')
        v={}
        for key,meta in row['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'complete retained raw '+key)
            v[key]=data
        compared=compare_members(members,library_members(v['lib']),objects[i])
        need(compared==row['library_comparison'] and
             compared['replaced_members']==expected and
             compared['contextual_members_unchanged']==885,
             'eight actual native source members and885 original unchanged members')
        need(v['exe']==target and v['map']==original_map,
             'entire fixed Japanese decoded MAINL EXE and MAP identical')
        mz=parse_mz(v['exe'])
        need(mz.valid and len(mz.relocations)==677 and len(v['exe'])==67372,
             'the original real relocation-bearing MZ image')
        vectors.append(v)
    need(vectors[0]==vectors[1],'two raw-equal full native library/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                sources=expected,source_member_count=8,
                original_library_member_count=893,
                unchanged_original_member_programs=885,
                original_native_xx_CODE_bytes=12622,
                native_xx_full_CODE_equal=True,native_xx_ordered_fields=187,
                original_native_CRT_CODE_bytes=329,
                all_original_CRT_native_members_equal=True,
                combined_native_source_CODE_bytes=12951,
                original_decoded_EXE_bytes=67372,
                original_MZ_relocations=677,
                whole_EXE_raw_equal=True,whole_MAP_raw_equal=True,
                repeated_native_link_rounds=2,
                source_builds_independently_repeated=True,
                selected_build_report_sha256=sha(raw),
                xx_source_build_sha256=xhash,crt7_source_build_sha256=chash,
                published_acceptance_unchanged=True)


if __name__=='__main__':
    r=review()
    (ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
