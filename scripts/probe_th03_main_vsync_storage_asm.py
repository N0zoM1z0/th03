#!/usr/bin/env python3
"""Native TASM/TLINK proof for TH03 MAIN's storage-only VS.ASM owner.

The original VS module has zero executable CODE, eight initialized DATA
bytes, eight uninitialized BSS bytes and twelve PUBLIC aliases.
"""
import argparse
import json
import re
import probe_th03_main_sound_asm as native

native.SOURCES={'vs':'vs'}
native.SOURCE_FILES={'vs':'src/main/hardware/vsync_storage.asm'}
native.SOURCE_INCLUDES=()
native.ORIGINAL_OBJECT_FILES={'vs':'obj/th03/vs.obj'}
native.ORIGINAL_LINK_SLOTS={'vs':r'obj\th03\vs.obj'}
native.MAP_ORIGINAL={'vs':'VS.ASM    '}
native.MAP_ROWS={'vs':3}
# The historical TASM emitted VSYNC aliases in one grouped PUBDEF; current
# TASM serializes them separately and swaps the two same-offset OldMask
# lines in the by-value MAP. Validate the exact two lines and normalize
# their ordering only, after verifying the full original PUBLIC map.
native.MAP_TIED_PUBLIC_ORDER_PAIRS = ((
    b' 1D56:05A4 idle  _vsync_OldMask\r\n 1D56:05A4       vsync_OldMask\r\n',
    b' 1D56:05A4       vsync_OldMask\r\n 1D56:05A4 idle  _vsync_OldMask\r\n',
),)
native.ORDER=('vs',)
native.REPORT_SCHEMA='th03-main-vsync-storage-asm-v1'
native.REPORT_FOLDER='main-vsync-storage-asm-'

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage',required=True)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    native.need(re.fullmatch(r'af[0-9]+[a-z][0-9]*',args.stage) is not None,
                'DOS-safe unique stage')
    summary=native.check(args.stage) if args.check else native.build(args.stage)
    native.need(summary['complete_original_units']==1 and
                summary['original_scope']['CODE_bytes']==0 and
                summary['original_scope']['PUBLICs']==12 and
                summary['original_scope']['ordered_native_fields']==0,
                'one physical VSYNC storage-only original owner')
    summary['initialized_DATA_bytes']=8
    summary['uninitialized_BSS_bytes']=8
    summary['executable_CODE_bytes']=0
    print(json.dumps(summary,sort_keys=True))
