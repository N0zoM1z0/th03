#!/usr/bin/env python3
"""Stage both opt-in MAIN candidates and existing-storage aliases; no native run."""
from pathlib import Path
import argparse
import hashlib
import json
import re

import stage_th03_main_shotroot as shot

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = (
    ('sub_DA43', '@PLAYER_STATE_UPDATE$QUIP14PLAYER_STUFF_T'),
    ('_player_render', '@PLAYER_RENDER$QP14PLAYER_STUFF_T'),
    ('sub_DF18', '@PLAYER_OVERLAY_RENDER$QP14PLAYER_STUFF_T'),
    ('sub_DFE9', '@PLAYER_KNOCKBACK_UPDATE$QP14PLAYER_STUFF_T'),
    ('player_bomb', 'PLAYER_BOMB'),
)
CODE_ALIASES = (
    ('sub_C0D8', '@PLAYER_LOSE_ANIM_UPDATE$QP14PLAYER_STUFF_T'),
    ('sub_C248', '@PLAYER_LOSE_ANIM_RENDER$QP14PLAYER_STUFF_T'),
)
EXPECTED_REFS = dict(zip((old for old, _ in ENTRIES), (2, 2, 2, 0, 0)))
RESERVE = '_collmap_pid\tdb ?\r\n\t\tdb 5 dup(?)\r\n_collmap'
VIEW = ('_collmap_pid\tdb ?\r\n\t\tdb ?\r\npublic _shot_release_frames\r\n'
        '_shot_release_frames db 2 dup(?)\r\n\t\tdb 2 dup(?)\r\n_collmap')


def transform_root(raw):
    """Extend the hash-guarded shot staging, preserving every other allocation."""
    staged, shot_refs = shot.transform_root(raw)
    text = staged.decode('latin1')
    first, last = 'sub_DA43\tproc near', 'player_bomb\tendp'
    shot.need(text.count(first) == text.count(last) == 1, 'complete state anchors')
    a, b = text.index(first), text.index(last) + len(last)
    removed = text[a:b]
    shot.need(re.findall(r'^(\S+)\s+proc\s+(near|far)', removed, re.M)
              == [(name, 'near') for name, _ in ENTRIES], 'five complete state procedures')
    changed = text[:a] + '; Five state procedures supplied by maintained C++ source.\r\n' + text[b:]
    refs = {}
    for old, new in ENTRIES:
        pattern = r'\b' + re.escape(old) + r'\b'
        refs[old] = len(re.findall(pattern, changed))
        changed = re.sub(pattern, lambda m, new=new: new, changed)
    shot.need(refs == EXPECTED_REFS, 'outside state caller membership')
    segment = "main_010_TEXT\tsegment\tbyte public 'CODE' use16\r\n"
    shot.need(changed.count(segment) == 1, 'state segment declaration')
    imports = ''.join('\textern ' + new + ':near\r\n' for old, new in ENTRIES if refs[old])
    changed = changed.replace(segment, segment + imports)
    for old, new in CODE_ALIASES:
        anchor = old + '\tproc near'
        shot.need(changed.count(anchor) == 1 and new not in text, 'existing code alias ' + old)
        changed = changed.replace(anchor, 'public ' + new + '\r\n' + new + ' label near\r\n' + anchor)
    shot.need(changed.count(RESERVE) == 1 and '_shot_release_frames' not in text, 'original five-byte reserve')
    changed = changed.replace(RESERVE, VIEW)
    # Reverse only the reviewed 1+2+2 split when comparing allocation syntax.
    shot.need(shot.allocation_lines(text) == shot.allocation_lines(changed.replace(VIEW, RESERVE)),
              'all other DATA/BSS allocations preserved')
    return changed.encode('latin1'), dict(shot=shot_refs, state=refs)


def transform_response(raw):
    staged = shot.transform_response(raw)
    anchor, new = b'obj\\th03\\main_010.obj', b'obj\\th03\\state.obj'
    shot.need(staged.count(anchor) == 1 and new not in staged, 'sole ordered state insertion')
    return staged.replace(anchor, new + b' ' + anchor)


def stage(baseline, output):
    baseline, output = Path(baseline).resolve(), Path(output).resolve()
    shot.need(output.is_relative_to((ROOT / '.analysis').resolve()) and not output.exists(),
              'fresh ignored output required')
    names = ('th03_main.asm', 'src/main/hud/score.asm', 'obj/th03/main.@l')
    inputs = {}
    for name in names:
        path = baseline / name
        shot.need(not any(p.is_symlink() for p in (path, *path.parents)), 'source symlink')
        inputs[name] = path.read_bytes()
    root, refs = transform_root(inputs[names[0]])
    products = {names[0]: root, names[1]: shot.transform_score(inputs[names[1]]),
                names[2]: transform_response(inputs[names[2]])}
    output.mkdir()
    for name, raw in products.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(raw)
    digest = lambda raw: dict(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
    report = dict(schema='th03-state-shot-source-link-stage-v1', native_invocations=0,
                  source_acceptance=False, exact_acceptance=False, transferred_code_bytes=3213,
                  state_bytes=1716, shot_bytes=1497, outside_caller_references=refs,
                  release_counter_reserve_partition=[1, 2, 2], code_aliases=CODE_ALIASES,
                  inputs={str(baseline / n): digest(raw) for n, raw in inputs.items()},
                  outputs={n: digest(raw) for n, raw in products.items()})
    (output / 'stage-report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(stage(args.baseline, args.output), indent=2))


if __name__ == '__main__':
    main()
