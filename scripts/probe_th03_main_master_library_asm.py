#!/usr/bin/env python3
"""Two original large master.lib CODE owners, TASM/TLINK without cold replay.

The tracked sources are symbolic carrier assemblers; included vendor routines
are independently checked against the retained ReC98 reference and the exact
TASM worktree. This is library provenance, not authored game-function credit.
"""
import argparse
import json
from pathlib import Path
import re
import probe_th03_main_sound_asm as native

native.SOURCES={'mst_pref':'mst_pref','mst_body':'mst_body'}
native.SOURCE_FILES={name:'config/main_work/library_carriers/'+name+'.asm' for name in native.SOURCES}
native.SOURCE_INCLUDES=()
native.ORIGINAL_OBJECT_FILES={name:'obj/th03/'+name+'.obj' for name in native.SOURCES}
native.ORIGINAL_LINK_SLOTS={name:'obj\\th03\\'+name+'.obj' for name in native.SOURCES}
native.MAP_ORIGINAL={name:'th03\\'+name+'.asm' for name in native.SOURCES}
native.MAP_ROWS={name:3 for name in native.SOURCES}
native.ORDER=tuple(native.SOURCES)
native.REPORT_SCHEMA='th03-main-two-master-library-asm-v1'
native.REPORT_FOLDER='main-master-library-asm-'


def checked_library_includes():
    """Bind actual dependency content to the retained reference, recursively."""
    hashes={}
    vendor=native.ROOT/'_reference/ReC98'
    work=native.WORK
    def verify(path):
        if path in hashes:
            return
        native.need('..' not in Path(path).parts and not Path(path).is_absolute(),
                    'bounded vendor include path '+path)
        expected=(vendor/path).read_bytes()
        actual=(work/path).read_bytes()
        native.need(expected==actual,
                    'TASM consumed exact retained ReC98 vendor source '+path)
        hashes[path]=native.sha(expected)
        for match in re.findall(rb'(?im)^include\s+([^;\s]+)',expected):
            verify(match.decode('ascii'))
    for source in native.expected_sources().values():
        for name in re.findall(rb'(?im)^include\s+([^;\s]+)',source):
            verify(name.decode('ascii'))
    return hashes

native.checked_includes=checked_library_includes

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',required=True)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    native.need(re.fullmatch(r'af[0-9]+[a-z][0-9]*',args.stage) is not None,
                'DOS-safe unique stage')
    print(json.dumps(native.check(args.stage) if args.check
                     else native.build(args.stage),sort_keys=True))
