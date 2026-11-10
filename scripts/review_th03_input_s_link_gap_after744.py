"""Read-only negative proof: the original 417-byte input_s and the old 418-byte MAIN slot.

This does NOT certify a complete native MAIN overlay. Its deliberate
failure to match the full link is the relevant source-ownership blocker.
"""
import json
from pathlib import Path

from build_th03_main_yumemi_cpu_after596_work import WORK
from build_th03_mainl_display_work import payload, literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.pc98 import parse_mz
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_exatt_layout import (
    ROOT, SOURCES, check_native_dependencies, need, sha,
)


def review(stage='af1320d'):
    original = (WORK/'obj/th03/input_s.obj').read_bytes()
    previous = (WORK/'probe/af567c/r1-input_s.obj').read_bytes()
    actual = (WORK/f'probe/{stage}/r1/input_s.obj').read_bytes()
    for name, check in (
        ('original CODE', payload(actual) == payload(original)),
        ('original ordered FIXUPPs', literal_fields(actual) == literal_fields(original)),
        ('original PUBLICs', public_offsets(actual) == public_offsets(original)),
        ('original segments', segment_definitions(actual) == segment_definitions(original)),
    ):
        need(check, 'input_s source-native object does not match '+name)

    current = (ROOT/SOURCES['input_s']).read_bytes()
    saved = (WORK/f'probe/{stage}/r1/{SOURCES["input_s"]}').read_bytes()
    need(saved == current.replace(b'\n', b'\r\n'),
         'input_s original compiler source is not the current maintained input')
    check_native_dependencies(actual, 'input_s', stage, 1, False)

    original_code = payload(original)
    previous_code = payload(previous)
    extras = [(key, value) for key, value in previous_code.items()
              if key not in original_code]
    need(len(original_code) == 417 and len(payload(actual)) == 417 and
         len(previous_code) == 418 and
         all(previous_code[k] == v for k, v in original_code.items()) and
         extras == [((1, 417), 0x90)],
         'input_s historical parent trailing NOP explanation no longer holds')

    parent_exe = (WORK/'probe/af596y/r1.exe').read_bytes()
    candidate_exe = (WORK/f'probe/{stage}/r1.exe').read_bytes()
    differences = [i for i, (a, b) in enumerate(zip(parent_exe, candidate_exe))
                   if a != b]
    need(len(parent_exe) == len(candidate_exe) and differences == [68141] and
         parent_exe[68141] == 0x90 and candidate_exe[68141] == 0 and
         parse_mz(parent_exe).relocations == parse_mz(candidate_exe).relocations,
         'input_s one-byte original normal MAIN link gap changed')

    return {
        'stage': stage,
        'input_s_original_CODE_bytes': 417,
        'native_current_source_object_CODE_exact': True,
        'native_ordered_FIXUPPs': len(literal_fields(original)),
        'native_original_PUBLICs': len(public_offsets(original)),
        'parent_link_object_CODE_bytes': 418,
        'historical_extra_CODE_offset': 417,
        'historical_extra_byte': '90',
        'normal_MAIN_exact': False,
        'normal_MAIN_difference_file_offset': differences[0],
        'normal_MAIN_original_byte': '90',
        'normal_MAIN_candidate_byte': '00',
        'source_sha256': sha(current),
        'canonical_Factory_credit': False,
        'status': 'blocked-by-historical-single-NOP-parent-link-gap',
    }


if __name__ == '__main__':
    print(json.dumps(review(), sort_keys=True))
