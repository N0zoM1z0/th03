#!/usr/bin/env python3
"""Original MAIN master tail's initialized DATA and global BSS carrier.

Only this 0-CODE project data object is assembled/relinked in the 99-object
MAIN response. Input data includes are pinned to maintained/referenced bytes.
"""
import argparse
import json
from pathlib import Path
import re
import probe_th03_main_sound_asm as native
from probe_th03_main_exatt_layout import segment_definitions
from build_th03_mainl_display_work import payload

native.SOURCES={'mst_tail':'mst_tail'}
native.SOURCE_FILES={'mst_tail':'config/main_work/data_carriers/mst_tail.asm'}
native.SOURCE_INCLUDES=()
native.ORIGINAL_OBJECT_FILES={'mst_tail':'obj/th03/mst_tail.obj'}
native.ORIGINAL_LINK_SLOTS={'mst_tail':r'obj\th03\mst_tail.obj'}
native.MAP_ORIGINAL={'mst_tail':r'th03\mst_tail.asm'}
native.MAP_ROWS={'mst_tail':3}
native.ORDER=('mst_tail',)
native.REPORT_SCHEMA='th03-main-master-tail-data-v1'
native.REPORT_FOLDER='main-master-tail-data-'


def checked_tail_includes():
    """Pin the full actual include graph, including two generated sprites."""
    hashes={}
    vendor=native.ROOT/'_reference/ReC98'
    work=native.WORK
    original_sprite_stems=('score','pellet')
    def verify(name):
        if name in hashes:
            return
        path=Path(name)
        native.need(not path.is_absolute() and '..' not in path.parts,
                    'bounded relative tail source dependency '+name)
        if name == 'th03/math/randring.inc':
            # The native WORK include is exactly the current repaired
            # symbol-case / EVEN macro implementation, not an old
            # vendor checkout file. Preserve this real dependency.
            actual_repo=native.ROOT/'src/main/math/randring_getters.inl'
        elif name.startswith('src/'):
            actual_repo=native.ROOT/name
        elif name in (f'th03/sprites/{stem}.asp'
                     for stem in original_sprite_stems):
            actual_repo=native.ROOT/'config/main_work/generated_sprites'/path.name
        else:
            actual_repo=vendor/name
        expected=actual_repo.read_bytes()
        consumed=(work/name).read_bytes()
        native.need(expected==consumed,
                    'original TASM consumed exact tracked/reference tail dependency '+name)
        hashes[name]=native.sha(expected)
        for child in re.findall(rb'(?im)^\s*include\s+([^;\s]+)',expected):
            verify(child.decode('ascii'))
    for raw in native.expected_sources().values():
        for entry in re.findall(rb'(?im)^\s*include\s+([^;\s]+)',raw):
            verify(entry.decode('ascii'))
    # Bind the historical source images used to generate the two .asp sheets.
    for stem in original_sprite_stems:
        name=f'th03/sprites/{stem}.bmp'
        expected=(vendor/name).read_bytes()
        native.need(expected==(work/name).read_bytes(),
                    'original source BMP matches retained vendor image '+name)
        hashes[name]=native.sha(expected)
    return hashes

native.checked_includes=checked_tail_includes


def summary_checked(stage, check):
    result=native.check(stage) if check else native.build(stage)
    expected=(native.WORK/'obj/th03/mst_tail.obj').read_bytes()
    layout=segment_definitions(expected)
    native.need(result['complete_original_units']==1 and
                result['original_scope']['CODE_bytes']==0 and
                result['original_scope']['ordered_native_fields']==0 and
                result['original_scope']['PUBLICs']==414 and
                [s['size'] for s in layout]==[0,1606,22250] and
                len(payload(expected))==1566,
                'original master tail has 0 CODE, 1566 initialized DATA, 22250 BSS')
    result.update(initialized_DATA_bytes=1566, DATA_SEGDEF_bytes=1606,
                  BSS_SEGDEF_bytes=22250, executable_CODE_bytes=0)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',required=True)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    native.need(re.fullmatch(r'af[0-9]+[a-z][0-9]*',args.stage) is not None,
                'DOS-safe unique stage')
    print(json.dumps(summary_checked(args.stage,args.check),sort_keys=True))
