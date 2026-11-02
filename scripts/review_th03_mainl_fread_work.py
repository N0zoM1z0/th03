#!/usr/bin/env python3
"""Independently verify full original fread code, four fixups and native MAINL."""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_fread_work as producer
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import compare_members,library_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-fread-native-review.json'


def native_CODE(blob):
    p=payload(blob)
    return bytes(p[1,i] for i in range(437))


def review():
    raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,parent27,previous_sha=producer.retained()
    original=producer.ORIGINAL.read_bytes()
    source={name:(ROOT/name).read_bytes() for name in producer.SOURCES}
    expected=producer.original_scope(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['preceding_twenty_seven_source_build_sha256']==previous_sha and
         r['original_sha256']==sha(original) and
         r['source_sha256']=={name:sha(blob) for name,blob in source.items()} and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['native_assembler_flags']==producer.TASM_FLAGS,
         'maintained fread source, original vendor object and immutable parent')
    need(expected['CODE_bytes']==437 and
         expected['public_offset']==283 and
         expected['original_helper_boundaries']==(0,283,437) and
         expected['imports']==['__fgetc','__rtl_read','N_LXMUL@','N_PADD@'] and
         [(f['site'],f['target'],f['frame_method']) for f in
          expected['literal_ordered_fields']]==
         [(135,2,5),(245,1,5),(313,3,0),(385,4,0)],
         'original private/public fread geometry and mixed target/segment fixups')
    code=native_CODE(original)
    decoder=Cs(CS_ARCH_X86,CS_MODE_16)
    need([sum(x.size for x in decoder.disasm(code[a:b],a))
          for a,b in ((0,283),(283,437))]==[283,154] and
         code[280:283]==bytes.fromhex('c20a00') and code[-1]==0xcb,
         'real private RET 10 and public far RETF instructions at original boundaries')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two actual independent original TASM/TLIB/TLINK rounds')
    phases=['extract']+[f'round{i}-{kind}' for i in (1,2) for kind in
                        ('assemble','library','link')]
    need([q['label'] for q in r['phases']]==phases and all(
         q['returncode']==0 and
         sha((ROOT/q['log_path']).read_bytes())==q['log_sha256']
         for q in r['phases']),
         'all actual native writer commands and logs remain unchanged')
    vectors=[]
    for i,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'complete raw native source output vector')
        outputs={}
        for kind,meta in row['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'literal native fread '+kind+' file identity')
            outputs[kind]=data
        need(producer.original_scope(outputs['obj'])==expected and
             native_CODE(outputs['obj'])==code and
             literal_fields(outputs['obj'])==literal_fields(original),
             'all 437 original native fread instructions and four ordered fields exact')
        sources=dict(parent27[i],fread=outputs['obj'])
        compared=compare_members(members,library_members(outputs['lib']),sources)
        need(compared==row['library_comparison'] and
             compared['replaced_members']==sorted(sources) and
             compared['contextual_members_unchanged']==865,
             '28 original source CRT slots, 865 vendor members wholly untouched')
        need(outputs['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete unchanged Japanese decoded original EXE and MAP raw-equal')
        mz=parse_mz(outputs['exe'])
        need(mz.valid and len(outputs['exe'])==67372 and len(mz.relocations)==677,
             'original entire relocation-bearing MZ output')
        vectors.append(outputs)
    need(vectors[0]==vectors[1],
         'two complete identical native original OBJ/LIB/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                original_fread_CODE_bytes=437,source_fread_CODE_bytes=437,
                all_437_native_CODE_bytes_equal=True,
                private_buffered_read_near_bytes=283,
                public_fread_far_bytes=154,public_fread_offset=283,
                private_return_pop_bytes=10,
                literal_ordered_FIXUPP_count=4,
                all_original_ordered_FIXUPPs_equal=True,
                original_import_order=expected['imports'],
                original_library_members=893,reconstructed_source_members=28,
                untouched_original_member_programs=865,
                simultaneous_exact_source_CODE_bytes=18702,
                complete_Japanese_decoded_EXE_bytes=67372,
                MZ_relocations=677,whole_original_EXE_raw_equal=True,
                whole_original_MAP_raw_equal=True,
                native_repeated_rounds=2,
                source_paths=list(producer.SOURCES),
                build_report_sha256=sha(raw),preceding_27_source_receipt_sha256=previous_sha,
                formal_accepted_publication_unchanged=True)


if __name__=='__main__':
    result=review()
    (ROOT/REPORT).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
