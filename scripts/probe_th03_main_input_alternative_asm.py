#!/usr/bin/env python3
"""Alternative 418-byte input scanner TASM linker-carrier proof.

This intentionally compares the historical source-linked 418-byte parent,
NOT the original physical 417-byte TC4 input_s.obj. It contributes no
new original-OBJ or Factory credit.
"""
import argparse
import json
import re
import probe_th03_main_sound_asm as native

native.SOURCES={'input_s':'input_s'}
native.SOURCE_FILES={'input_s':'src/main/hardware/input_scan.asm'}
native.SOURCE_INCLUDES=()
native.ORIGINAL_OBJECT_FILES={'input_s':'probe/af567c/r1-input_s.obj'}
native.ORIGINAL_LINK_SLOTS={'input_s':r'probe\af567c\r{n}-input_s.obj'}
native.MAP_ORIGINAL={'input_s':r'probe\af565s\input_s.asm'}
native.MAP_ROWS={'input_s':3}
native.ORDER=('input_s',)
native.REPORT_SCHEMA='th03-main-input-alternative-tasm-v1'
native.REPORT_FOLDER='main-input-alternative-asm-'

if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage',required=True)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    native.need(re.fullmatch(r'af[0-9]+[a-z][0-9]*',args.stage) is not None,
                'DOS-safe unique stage')
    summary=native.check(args.stage) if args.check else native.build(args.stage)
    summary['original_TC4_object_equivalent']=False
    summary['historical_418_byte_linker_carrier']=True
    summary['included_in_current_source_native_selection']=False
    print(json.dumps(summary,sort_keys=True))
