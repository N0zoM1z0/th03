#!/usr/bin/env python3
"""Full original MAIN aggregate root physical source, scoped TASM/TLINK.

Only the original root OBJ is rebuilt in each of two rounds. Bounded game
includes are tied to their maintained source; other ReC98 dependencies to
the retained reference checkout. This does not replay the 99-object graph.
"""
import argparse
import json
from pathlib import Path
import re
import probe_th03_main_sound_asm as native
from probe_th03_main_exatt_layout import segment_definitions
from build_th03_mainl_display_work import payload

native.SOURCES={'main':'main'}
native.SOURCE_FILES={'main':'config/main_work/root_carriers/th03_main.asm'}
native.SOURCE_INCLUDES=()
native.ORIGINAL_OBJECT_FILES={'main':'obj/th03/main.obj'}
native.ORIGINAL_LINK_SLOTS={'main':r'obj\th03\main.obj'}
native.MAP_ORIGINAL={'main':'th03_main.asm'}
native.MAP_ROWS={'main':32}
native.ORDER=('main',)
native.REPORT_SCHEMA='th03-main-original-aggregate-root-v1'
native.REPORT_FOLDER='main-root-carrier-'

# Build-local source overrides were already reconstructed and tracked as
# proper bounded include TUs, not taken from the old vendor release.
OVERRIDES={
    'th03/math/randring.inc':'src/main/math/randring_getters.inl',
    'th03/hardware/sprite16_copy.asm':'src/main/graphics/sprite16_copy.inl',
    'th03/formats/pfopen.asm':'src/main/formats/pfopen.inl',
}


def checked_root_includes():
    checks={}
    vendor=native.ROOT/'_reference/ReC98'
    def verify(name):
        if name in checks:
            return
        p=Path(name)
        native.need(not p.is_absolute() and '..' not in p.parts,
                    'bounded MAIN root include '+name)
        exp=(native.ROOT/OVERRIDES[name] if name in OVERRIDES
             else native.ROOT/name if name.startswith('src/')
             else vendor/name)
        source=exp.read_bytes()
        consumed=(native.WORK/name).read_bytes()
        native.need(source==consumed,
                    'actual original TASM consumed pinned MAIN root source '+name)
        checks[name]=native.sha(source)
        for child in re.findall(rb'(?im)^\s*include\s+([^;\s]+)',source):
            verify(child.decode('ascii'))
    for source in native.expected_sources().values():
        for child in re.findall(rb'(?im)^\s*include\s+([^;\s]+)',source):
            verify(child.decode('ascii'))
    return checks

native.checked_includes=checked_root_includes


def checked_summary(stage, read_only):
    result=native.check(stage) if read_only else native.build(stage)
    original=(native.WORK/'obj/th03/main.obj').read_bytes()
    segments=segment_definitions(original)
    counts={s['index']:s['size'] for s in segments}
    initialized=payload(original)
    code=sum(1 for (idx,_),v in initialized.items()
             if segments[idx-1]['class']=='CODE')
    data=sum(1 for (idx,_),v in initialized.items()
             if segments[idx-1]['class']=='DATA')
    native.need(len(segments)==32 and code==896 and data==1289 and
                result['complete_original_units']==1 and
                result['original_scope']['CODE_bytes']==896 and
                result['original_scope']['PUBLICs']==127 and
                result['original_scope']['ordered_native_fields']==64 and
                counts[1]==748 and counts[2]==1294 and
                counts[12]==148 and counts[32]==104,
                'full root carrier CODE/DATA and 32-segment physical owner')
    result.update(executable_CODE_bytes=code,initialized_DATA_bytes=data,
                  CODE_SEGDEF_bytes=748+148,DATA_SEGDEF_bytes=1294,
                  BSS_SEGDEF_bytes=104)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',required=True)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    native.need(re.fullmatch(r'af[0-9]+[a-z][0-9]*',args.stage) is not None,
                'DOS-safe unique stage')
    print(json.dumps(checked_summary(args.stage,args.check),sort_keys=True))
