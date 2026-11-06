#!/usr/bin/env python3
"""Read-only evidence review of minimal DOS MZ re-serialization of MAIN."""
import json
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz,MZ_FIXED_HEADER_BYTES,MZ_RELOCATION_BYTES
from build_th03_mainl_resources_work import need,sha
import build_th03_main_compact_mz_after568_work as b


def review():
    cfg,cfg_sha,previous=b.inputs()
    record=json.loads((b.ROOT/b.REPORT).read_text())
    target_exe=b.parent.reference(b.parent.inputs()[0])[2]
    wrong_native=(b.parent.WORK/'bin/th03/main.exe').read_bytes()
    target=parse_mz(target_exe)
    wrong_normalized=compact_mz(wrong_native)
    dif=[i for i,(a,v) in enumerate(zip(target.program_image,
                                      parse_mz(wrong_normalized).program_image)) if a!=v]
    need(record['complete'] and record['cold_rebuilt'] is False and
         record['game_objects_recompiled']==0 and
         record['native_link_reexecuted'] is False and
         record['postlink_source_derived_container'] and
         record['original_linker_identity_established'] is False and
         record['whole_product_source_accepted'] is False and
         record['canonical_factory_accepted'] is False and
         record['driver_sha256']==sha((b.ROOT/b.DRIVER).read_bytes()) and
         record['library_serializer_sha256']==
           sha((b.ROOT/'scripts/lib/main_mz_compact.py').read_bytes()) and
         record['config_sha256']==cfg_sha and
         record['parent_report_sha256']==cfg['parent_report_sha256'] and
         record['original_target_sha256']==sha(target_exe) and
         record['negative_control']==dict(
           baseline_native_SHA256=sha(wrong_native),
           old_load_image_difference_offsets=[0xEC2D],
           incorrectly_claimed_original_equality=False),
         'genuine parent-derived byte claim and identity/whole-project credit limits')
    need(dif==[0xEC2D] and wrong_normalized!=target_exe and
         target.program_image[0xEC2D]==0x90,
         'negative control: serializer does not modify or repair CODE')
    x=[]
    for n,pr in enumerate(record['rounds'],1):
        parent_row=previous['rounds'][n-1]
        source=b.parent.read_pin(parent_row['outputs']['exe'])
        retained=b.parent.read_pin(pr['original_complete_reconstruction'])
        parsed_source=parse_mz(source)
        parsed=parse_mz(retained)
        need(pr['round']==n and
             pr['native_source_parent']==parent_row['outputs']['exe'] and
             pr['semantically_identical_native_image'] and
             pr['exact_original_FILE_bytes'] and
             pr['original_linker_identity_proved'] is False and
             retained==compact_mz(source)==target_exe and
             len(retained)==130882 and sha(retained)==cfg['target_SHA256'] and
             parsed.program_image==parsed_source.program_image and
             parsed.relocations==parsed_source.relocations==target.relocations and
             len(parsed.relocations)==1553 and
             len(parsed.program_image)==124642 and
             len(source)==132322 and
             parsed.header.relocation_table_offset==MZ_FIXED_HEADER_BYTES and
             parsed.header.header_paragraphs==390 and
             parsed_source.header.relocation_table_offset==62 and
             parsed_source.header.header_paragraphs==480 and
             MZ_FIXED_HEADER_BYTES+MZ_RELOCATION_BYTES*1553==390*16,
             'two independent complete native inputs, minimal-MZ semantic roundtrips and literal target file equivalence')
        x.append(retained)
    need(len(x)==2 and x[0]==x[1] and len(record['rounds'])==2,
         'complete 2-round raw output reproducibility')
    return dict(complete=True,native_source_combined_rounds=2,
        bytes_generated_per_compact_MZ=130882,original_file_SHA256=sha(target_exe),
        complete_original_japanese_file_byte_equal=True,
        complete_code_image_bytes=124642,original_ordered_relocations=1553,
        native_linker_header_offset=62,compact_relocation_table_offset=28,
        native_linker_header_paragraphs=480,compact_header_paragraphs=390,
        all_code_and_relocations_source_derived=True,
        negative_control_unfixed_CODE_still_wrong=True,
        full_original_linker_identity_proved=False,
        native_TLINK_direct_output_original_equal=False,
        canonical_factory_accepted=False,
        entire_project_source_accepted=False,
        native_container_report_sha256=sha((b.ROOT/b.REPORT).read_bytes()))


if __name__=='__main__':
    result=review()
    (b.ROOT/(b.PREFIX+'review.json')).write_text(json.dumps(result,indent=2)+'\n')
    print('Two source-derived compact DOS MZ EXEs: entire 130882-byte Japanese original file exact; code/image and 1553 relocations unchanged.')
