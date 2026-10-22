#!/usr/bin/env python3
"""Stage an opt-in P_SHOT link candidate; never invoke native tools or grant credit."""
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ROOT_SHA = '32e572ba4e136dc1ff96e75ad657759f52a64f6f93ebff54f5f7868910bfcf57'
SCORE_SHA = 'ec13b2fb32376e0b068ab6fbb49183bbfcad4487bdc0e06a7e7b9bc8356ae62e'
RESPONSE_SHA = '645495db8a9699a01641bd425917c529382c30762800465b30c613b215aebe20'
ENTRIES = (
    ('sub_E266', '@stage_prepare_shot_sprites$qv'),
    ('sub_E313', '@round_objects_and_counters_reset$qv'),
    ('sub_E35B', '@ROUND_RESULT_NUMBER_PUT$QIII'),
    ('sub_E3F2', '@round_match_result_render$qv'),
    ('sub_E737', '@player_shots_add$qv'),
)
DATA_ALIASES = (
    ('byte_23AF9', '_round_reset_flag', 'byte'),
    ('byte_23B00', '_round_reset_clear_flag', 'byte'),
    ('byte_20E3D', '_round_defeated_player', 'byte'),
    ('score_23DEA', '_result_bonus_step', 'word'),
    ('word_23DEC', '_result_bonus_low', 'word'),
    ('word_23DEE', '_result_bonus_high', 'word'),
    ('score_23DF0', '_result_bonus_remaining', 'dword'),
    ('byte_23DF9', '_result_lives_remaining', 'byte'),
    ('aMAX_COMBO', '_result_label_combo', 'byte'),
    ('aGAUGE_ATTACK_TIMES', '_result_label_gauge', 'byte'),
    ('aBOSS_ATTACK_TIMES', '_result_label_boss', 'byte'),
    ('aBOSS_REVERSAL_TIMES', '_result_label_reversal', 'byte'),
    ('aBOSS_PANIC_TIMES', '_result_label_panic', 'byte'),
    ('aTOTAL', '_result_label_total', 'byte'),
    ('aWINNER_BONUS', '_result_label_winner', 'byte'),
    ('aALL_CLEAR', '_result_label_clear', 'byte'),
    ('aPLAYER_REM', '_result_label_lives', 'byte'),
)
SCORE_ALIAS = '@ROUND_RESULT_HIGH_DIGITS_PUT$QIIUIUC'
EXPECTED_REFS = dict(zip((n for n, _ in ENTRIES), (1, 1, 0, 1, 1)))


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def allocation_lines(text):
    return re.findall(r'^[^;\r\n]*\b(?:db|dw|dd)\b[^;\r\n]*', text, re.M | re.I)


def transform_root(raw):
    need(sha(raw) == ROOT_SHA, 'baseline root identity')
    text = raw.decode('latin1')
    first, last = 'sub_E266\tproc near', 'sub_E737\tendp'
    need(text.count(first) == text.count(last) == 1, 'complete P_SHOT interval anchors')
    start, end = text.index(first), text.index(last) + len(last)
    removed = text[start:end]
    need(re.findall(r'^(\S+)\s+proc\s+(near|far)', removed, re.M)
         == [(name, 'near') for name, _ in ENTRIES], 'five complete original procedures')
    changed = text[:start] + '; Five P_SHOT procedures supplied by maintained C++ source.\r\n' + text[end:]
    refs = {}
    for old, new in ENTRIES:
        pattern = r'\b' + re.escape(old) + r'\b'
        refs[old] = len(re.findall(pattern, changed))
        changed = re.sub(pattern, lambda m, new=new: new, changed)
    need(refs == EXPECTED_REFS, 'outside caller membership')
    segment = "P_SHOT_TEXT segment byte public 'CODE' use16\r\n"
    need(changed.count(segment) == 1, 'original segment declaration')
    imports = ''.join('\textern ' + new + ':near\r\n' for old, new in ENTRIES if refs[old])
    changed = changed.replace(segment, segment + imports)
    for old, new, kind in DATA_ALIASES:
        matches = list(re.finditer(r'^' + re.escape(old) + r'[\t ]+(?:db|dw|dd)\b', changed, re.M))
        need(len(matches) == 1 and new not in text, 'existing storage alias ' + old)
        at = matches[0].start()
        changed = changed[:at] + 'public ' + new + '\r\n' + new + ' label ' + kind + '\r\n' + changed[at:]
    need(all(not re.search(r'\b' + re.escape(old) + r'\b', changed) for old, _ in ENTRIES), 'old entry remains')
    need(allocation_lines(text) == allocation_lines(changed), 'all DATA/BSS allocations preserved')
    return changed.encode('latin1'), refs


def transform_score(raw):
    need(sha(raw) == SCORE_SHA, 'score source identity')
    anchor = b'score_bonus_digits_put proc far\n'
    need(raw.count(anchor) == 1 and SCORE_ALIAS.encode() not in raw, 'existing far score entry')
    alias = ('public ' + SCORE_ALIAS + '\n' + SCORE_ALIAS + ' label far\n').encode()
    return raw.replace(anchor, alias + anchor)


def transform_response(raw):
    need(sha(raw) == RESPONSE_SHA, 'baseline response identity')
    anchor, new = b'obj\\th03\\p_shot.obj', b'obj\\th03\\shotroot.obj'
    need(raw.count(anchor) == 1 and new not in raw, 'sole ordered shot object insertion')
    return raw.replace(anchor, new + b' ' + anchor)


def stage(baseline, output):
    baseline, output = Path(baseline).resolve(), Path(output).resolve()
    need(output.is_relative_to((ROOT/'.analysis').resolve()), 'ignored output required')
    need(not output.exists(), 'fresh output required')
    names = ('th03_main.asm', 'src/main/hud/score.asm', 'obj/th03/main.@l')
    inputs = {}
    for name in names:
        path = baseline/name
        need(not any(p.is_symlink() for p in (path, *path.parents)), 'source symlink')
        inputs[name] = path.read_bytes()
    changed, refs = transform_root(inputs[names[0]])
    products = {names[0]: changed, names[1]: transform_score(inputs[names[1]]),
                names[2]: transform_response(inputs[names[2]])}
    output.mkdir()
    for name, raw in products.items():
        path = output/name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(raw)
    report = dict(schema='th03-shotroot-source-link-stage-v1', native_invocations=0,
                  source_acceptance=False, exact_acceptance=False, transferred_code_bytes=1497,
                  existing_update_render_bytes=185, outside_caller_references=refs,
                  zero_storage_data_aliases=len(DATA_ALIASES), zero_code_score_alias=SCORE_ALIAS,
                  proposed_object='obj/th03/shotroot.obj',
                  inputs={str(baseline/n): dict(sha256=sha(raw), bytes=len(raw)) for n, raw in inputs.items()},
                  outputs={n: dict(sha256=sha(raw), bytes=len(raw)) for n, raw in products.items()})
    (output/'stage-report.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(stage(args.baseline, args.output), indent=2))


if __name__ == '__main__':
    main()
