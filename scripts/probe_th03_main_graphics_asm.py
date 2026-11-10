#!/usr/bin/env python3
"""Six complete original graphics/asset ASM owners, scoped native TASM/TLINK.

Use only the six selected MAIN objects. The original 99-object parent,
assembler, target, EXE and MAP comparisons are shared with sound leaves.
"""
import argparse
import json
import re
import probe_th03_main_sound_asm as native

native.SOURCES = {name:name for name in (
    'hfliplut','sprite16','stg_pal','mrs','score_hud','gf_ctx'
)}
native.SOURCE_FILES = {
    'hfliplut':'src/main/formats/hfliplut.asm',
    'sprite16':'src/main/graphics/sprite16.asm',
    'stg_pal':'src/main/graphics/stage_palette.asm',
    'mrs':'src/main/formats/mrs.asm',
    'score_hud':'src/main/hud/score.asm',
    'gf_ctx':'src/main/graphics/round_fill_context.asm',
}
native.MAP_ORIGINAL = {owner:'th03\\'+owner+'.asm' for owner in native.SOURCES}
native.MAP_ORIGINAL['score_hud'] = 'src\\main\\hud\\score.asm'
native.MAP_ROWS = dict(hfliplut=1,sprite16=3,stg_pal=6,mrs=3,
                       score_hud=5,gf_ctx=10)
native.ORDER = tuple(native.SOURCES)
native.REPORT_SCHEMA = 'th03-main-six-graphics-asm-v1'
native.REPORT_FOLDER = 'main-graphics-asm-'

if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage',required=True)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    native.need(re.fullmatch(r'af[0-9]+[a-z][0-9]*',args.stage) is not None,
                'DOS-safe unique stage')
    print(json.dumps(native.check(args.stage) if args.check
                     else native.build(args.stage),sort_keys=True))
