#!/usr/bin/env python3
"""Check the complete natural Music Room carrier against the fixed TH03 target."""
import argparse
import hashlib
import json
from pathlib import Path

from review_th03_op_cfg_work import images
import review_th03_op_music_state_work as state_review
from lib.op_startup_cold import verify as cold_graph
from lib.op_music_state_layout import verify as state_layout, CS, START, OBJECT
from lib.op_music_polygon import layout as polygon_layout
from lib.op_music_comment import layout as comment_layout
from lib.op_music_menu import layout as menu_layout
from lib.omf import parse_omf

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'config/op_music_menu_work/observation.json'
INPUTS = tuple(sorted(set((*state_review.INPUTS,
    'scripts/lib/op_music_polygon.py', 'scripts/lib/op_music_comment.py',
    'scripts/lib/op_music_menu.py', 'scripts/review_th03_op_music_menu_work.py'))))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(value, message):
    if not value:
        raise ValueError('OP Music native check: ' + str(message))


def native_relocations(raw):
    """Read the whole carrier's far fields in emitted OMF record order."""
    result, block = [], None
    for record in parse_omf(raw):
        if record.name == 'LEDATA':
            block = record.data[0], int.from_bytes(record.data[1:3], 'little')
        elif record.name == 'FIXUPP' and block[0] == 1:
            at = 0
            while at < len(record.data):
                loc, low, method = record.data[at:at + 3]
                at += 3
                need(method in (20, 22, 86), 'native field form')
                at += 2 if method in (20, 22) else 1
                if loc >> 2 & 15 == 3:
                    need(method == 86, 'ordinary far field')
                    site = block[1] + (loc & 3) * 256 + low
                    need(site + 4 <= 2244, 'complete carrier field')
                    result.append([CS, 0xC1E + site + 2])
    return result


def examine(root=ROOT):
    bindings = {name: sha((root / name).read_bytes()) for name in INPUTS}
    work, target, candidate, cold, cold_raw = images(root)
    validation = cold_graph(root, work, target, candidate, cold)
    dependencies = state_review.dependencies(root, work, cold)
    layouts = {name: check(root, work, target, candidate) for name, check in (
        ('state', state_layout), ('polygon', polygon_layout),
        ('comments', comment_layout), ('menu', menu_layout))}
    need(sum(row['code_bytes'] for row in layouts.values()) == 2244, 'complete CODE partition')
    need(layouts['state']['functions'] + sum(layouts[n]['procedures'] for n in ('polygon', 'comments', 'menu')) == 14,
         'all fourteen complete procedures')
    relocations = native_relocations((work / OBJECT).read_bytes())
    for image in (target, candidate):
        actual = [[r.segment, r.offset] for r in image.relocations if START <= r.linear < START + 2244]
        need(actual == relocations, 'whole literal ordered MZ vector')
    need(bindings == {name: sha((root / name).read_bytes()) for name in INPUTS}, 'inputs unchanged during check')
    return dict(schema='th03-op-music-native-v1', complete=True,
        provenance='candidate-local-attested', native_pair_rebuilt=False,
        implementation_sha256=bindings, cold_report_sha256=sha(cold_raw),
        cold_validation=validation, dependencies=dependencies, layouts=layouts,
        procedures=14, code_bytes=2244, ordered_relocations=relocations,
        raw_sha256=sha(target.program_image[START:START + 2244]),
        containing_DATA_bytes=1008, containing_BSS_bytes=1060,
        source_ownership_promoted=False, whole_product_accepted=False,
        runtime_matrix_required=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare the current native check with its saved receipt')
    options = parser.parse_args()
    current = examine()
    if options.check:
        need(current == json.loads(REPORT.read_bytes()), 'saved native receipt matches current inputs and outputs')
    else:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(current, indent=2) + '\n')
    print(f"Music Room native: 14 procedures / 2244 CODE bytes / {len(current['ordered_relocations'])} ordered relocations PASS; no runtime matrix")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
