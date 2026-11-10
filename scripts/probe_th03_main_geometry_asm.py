#!/usr/bin/env python3
"""Three complete MAIN vector/playfield/collision ASM objects, native TASM/TLINK.

Keep the original historical collmap input and both normal MAIN link rounds;
only these three source owners are reassembled.
"""
import argparse
import json
import re
import probe_th03_main_sound_asm as native

native.SOURCES = {name:name for name in ('vectorfar','playfld','collmap')}
native.SOURCE_FILES = {
    'vectorfar':'src/main/math/vector_far.asm',
    'playfld':'src/main/playfield/playfld.asm',
    'collmap':'src/main/collision/producers/collmap_native.asm',
}
native.SOURCE_INCLUDES = ('src/main/collision/map.asm',)
native.ORIGINAL_OBJECT_FILES = {
    'vectorfar':'obj/th03/vectorfar.obj',
    'playfld':'obj/th03/playfld.obj',
    'collmap':'probe/af591c/r1/collmap.obj',
}
native.ORIGINAL_LINK_SLOTS = {
    'vectorfar':r'obj\th03\vectorfar.obj',
    'playfld':r'obj\th03\playfld.obj',
    'collmap':r'probe\af591c\r{n}\collmap.obj',
}
native.MAP_ORIGINAL = {
    'vectorfar':r'th03\vectorfar.asm',
    'playfld':r'th03\playfld.asm',
    'collmap':r'probe\af591c\r{n}\collmap.asm',
}
native.MAP_ROWS = dict(vectorfar=1,playfld=3,collmap=2)
native.ORDER = tuple(native.SOURCES)
native.REPORT_SCHEMA = 'th03-main-three-geometry-asm-v1'
native.REPORT_FOLDER = 'main-geometry-asm-'

if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage',required=True)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    native.need(re.fullmatch(r'af[0-9]+[a-z][0-9]*',args.stage) is not None,
                'DOS-safe unique stage')
    print(json.dumps(native.check(args.stage) if args.check
                     else native.build(args.stage),sort_keys=True))
