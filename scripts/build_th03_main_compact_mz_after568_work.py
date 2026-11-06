#!/usr/bin/env python3
"""Re-encode two complete after567 MAIN source-native TLINK images to minimal MZ.

This is a pure format-level source-derived *alternate container*, not a
Turbo Link original-identity or whole-game Factory acceptance claim.
No original target bytes are inputs to the compact MZ serialization function.
"""
import json

import build_th03_main_combined_after567_work as parent
from build_th03_mainl_resources_work import need,sha
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz,MZ_FIXED_HEADER_BYTES,MZ_RELOCATION_BYTES

ROOT=parent.ROOT
DRIVER='scripts/build_th03_main_compact_mz_after568_work.py'
CONFIG='config/main_work/compact_mz_after568.json'
PREFIX='.analysis/work/main-compact-after568-native-'
REPORT=PREFIX+'build.json'

def inputs():
    cfg=json.loads((ROOT/CONFIG).read_text())
    need(cfg['schema']=='th03-main-native-compact-mz-after568-v1' and
         cfg['parent_report']==parent.REPORT and
         (cfg['native_TLINK_file_bytes'],cfg['native_header_paragraphs'],
          cfg['native_relocation_table_offset'],cfg['japanese_target_file_bytes'],
          cfg['DOS_MZ_fixed_header_bytes'],cfg['source_relocation_entries'],
          cfg['source_load_image_bytes'])==(132322,480,62,130882,28,1553,124642) and
         cfg['whole_original_file_output_equal'] is True and
         cfg['original_linker_producer_identity_proved'] is False and
         cfg['native_TLINK_direct_file_exact'] is False and
         cfg['source_game_whole_accepted'] is False and
         cfg['canonical_factory_credit_changed'] is False,
         'bounded alternate DOS MZ file serialization and original provenance limits')
    prev=json.loads((ROOT/cfg['parent_report']).read_text())
    need(prev['complete'] and sha((ROOT/cfg['parent_report']).read_bytes())==
         cfg['parent_report_sha256'] and len(prev['rounds'])==2,
         'original source-bound 10-OBJ two-round native TLINK parent')
    return cfg,sha((ROOT/CONFIG).read_bytes()),prev

def main():
    cfg,cfg_sha,prev=inputs()
    _,_,japanese=parent.reference(parent.inputs()[0])
    need(sha(japanese)==cfg['target_SHA256'] and len(japanese)==cfg['japanese_target_file_bytes'],
         'pinned original Japanese target integrity')
    native_baseline=(parent.WORK/'bin/th03/main.exe').read_bytes()
    wrong_compact=compact_mz(native_baseline)
    # Negative control: compacting an uncorrected program NEVER fixes its
    # missing CODE alignment. This rejects any covert target patch behavior.
    original_mz=parse_mz(japanese)
    wrong=parse_mz(wrong_compact)
    diffs=[i for i,(x,y) in enumerate(zip(original_mz.program_image,wrong.program_image)) if x!=y]
    need(diffs==[0xEC2D] and wrong_compact!=japanese,
         'recontainerization alone must not fix old CODE/instruction bytes')
    report=dict(complete=False,cold_rebuilt=False,game_objects_recompiled=0,
         native_link_reexecuted=False,postlink_source_derived_container=True,
         original_linker_identity_established=False,whole_product_source_accepted=False,
         canonical_factory_accepted=False,
         driver_sha256=sha((ROOT/DRIVER).read_bytes()),
         library_serializer_sha256=sha((ROOT/'scripts/lib/main_mz_compact.py').read_bytes()),
         config_sha256=cfg_sha,parent_report_sha256=cfg['parent_report_sha256'],
         original_target_sha256=sha(japanese),
         negative_control=dict(baseline_native_SHA256=sha(native_baseline),
                               old_load_image_difference_offsets=diffs,
                               incorrectly_claimed_original_equality=False),
         rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    vectors=[]
    for number,row in enumerate(prev['rounds'],1):
        source_exe=parent.read_pin(row['outputs']['exe'])
        original_native=parse_mz(source_exe)
        need(len(source_exe)==cfg['native_TLINK_file_bytes'] and
             original_native.header.header_paragraphs==cfg['native_header_paragraphs'] and
             original_native.header.relocation_table_offset==cfg['native_relocation_table_offset'] and
             len(original_native.relocations)==cfg['source_relocation_entries'] and
             len(original_native.program_image)==cfg['source_load_image_bytes'] and
             original_native.program_image==original_mz.program_image and
             original_native.relocations==original_mz.relocations,
             'both original source-native complete image/relo MZ parents')
        output=compact_mz(source_exe)
        result=parse_mz(output)
        need(output==japanese and len(output)==cfg['japanese_target_file_bytes'] and
             result.header.header_paragraphs==390 and
             result.header.relocation_table_offset==MZ_FIXED_HEADER_BYTES and
             MZ_FIXED_HEADER_BYTES+MZ_RELOCATION_BYTES*len(result.relocations)==390*16,
             'complete target file byte-equal by DOS MZ-minimal layout, without target file as serializer input')
        dest=PREFIX+f'round{number}-compact-mz.bin'
        (ROOT/dest).write_bytes(output)
        raw=dict(path=dest,bytes=len(output),sha256=sha(output))
        report['rounds'].append(dict(round=number,native_source_parent=row['outputs']['exe'],
                original_complete_reconstruction=raw,semantically_identical_native_image=True,
                exact_original_FILE_bytes=True,original_linker_identity_proved=False))
        save()
        vectors.append(output)
        print('Compact DOS MZ round',number,'complete original 130882-byte file SHA-equal; native code/1553 relocation entries unchanged',flush=True)
    need(vectors[0]==vectors[1],'two source-native file containers fully repeat')
    report['complete']=True
    save()

if __name__=='__main__':
    main()
