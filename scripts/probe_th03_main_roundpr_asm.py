#!/usr/bin/env python3
"""Exact native TASM/TLINK scope for MAIN's round RNG and collision reset carrier."""
import argparse
import json
import re
import probe_th03_main_sound_asm as native

native.SOURCES = {'roundpr': 'roundpr'}
native.SOURCE_FILES = {'roundpr': 'src/main/round/roundpr.asm'}
native.SOURCE_INCLUDES = (
    'src/main/math/randring_getters.inl',
    'src/main/math/randring_fill.inl',
    'src/main/collision/reset.inl',
)
native.ORIGINAL_OBJECT_FILES = {'roundpr':'obj/th03/roundpr.obj'}
native.ORIGINAL_LINK_SLOTS = {'roundpr': r'obj\th03\roundpr.obj'}
native.MAP_ORIGINAL = {'roundpr': r'th03\roundpr.asm'}
native.MAP_ROWS = {'roundpr':6}
native.ORDER = ('roundpr',)
native.REPORT_SCHEMA = 'th03-main-roundpr-asm-v1'
native.REPORT_FOLDER = 'main-roundpr-asm-'

if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage',required=True)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    native.need(re.fullmatch(r'af[0-9]+[a-z][0-9]*',args.stage) is not None,
                'DOS-safe unique stage')
    print(json.dumps(native.check(args.stage) if args.check
                     else native.build(args.stage),sort_keys=True))
