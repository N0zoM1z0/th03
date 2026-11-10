#!/usr/bin/env python3
"""Source-bound zero-byte segment-order providers in TH03 MAIN.

They own no CODE/DATA/PUBLIC, but the order/align of their 30 original
SEGDEFs determines TLINK placements and relocations across large BOSS and
engine owners. Reassemble only these two physical scaffold objects.
"""
import argparse
import json
import re
import probe_th03_main_sound_asm as native
from probe_th03_main_exatt_layout import segment_definitions
from build_th03_mainl_display_work import payload, literal_fields
from lib.mainl_owner_migrations import public_offsets

native.SOURCES={'bo_shim':'bo_shim','ex_ord':'ex_ord'}
native.SOURCE_FILES={
    'bo_shim':'src/main/boss/order.asm',
    'ex_ord':'src/main/player/exatt_order.asm',
}
native.ORIGINAL_OBJECT_FILES={o:f'obj/th03/{o}.obj' for o in native.SOURCES}
native.ORIGINAL_LINK_SLOTS={o:'obj\\th03\\'+o+'.obj' for o in native.SOURCES}
native.SOURCE_INCLUDES=()
native.MAP_ORIGINAL={o:'th03\\'+o+'.asm' for o in native.SOURCES}
native.MAP_ROWS={'bo_shim':19,'ex_ord':11}
native.STRICT_OMF_SEGMENT_LAYOUT = True
native.ORDER=tuple(native.SOURCES)
native.REPORT_SCHEMA='th03-main-zero-segment-order-v1'
native.REPORT_FOLDER='main-zero-order-'


def run(stage,check):
    result=native.check(stage) if check else native.build(stage)
    expected={'bo_shim':19,'ex_ord':11}
    for owner,n in expected.items():
        data=(native.WORK/native.ORIGINAL_OBJECT_FILES[owner]).read_bytes()
        native.need(len(segment_definitions(data))==n and not payload(data) and
                    not literal_fields(data) and not public_offsets(data),
                    'original zero-byte segment-order carrier '+owner)
    native.need(result['complete_original_units']==2 and
                result['original_scope']=={'CODE_bytes':0,
                                           'ordered_native_fields':0,'PUBLICs':0},
                'zero new game CODE bytes and PUBLICs')
    result['zero_length_SEGDEFs']=30
    result['game_CODE_bytes']=0
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage',required=True)
    p.add_argument('--check',action='store_true')
    a=p.parse_args()
    native.need(re.fullmatch(r'af[0-9]+[a-z][0-9]*',a.stage) is not None,
                'unique DOS-safe native stage')
    print(json.dumps(run(a.stage,a.check),sort_keys=True))
