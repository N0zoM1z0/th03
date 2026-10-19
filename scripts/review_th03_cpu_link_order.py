#!/usr/bin/env python3
"""Reproduce the pinned TH03 CPU retained-link ordering obstruction.

Read-only historical diagnostic, not an acceptance comparator or native runner.
Private inputs are required. Path overrides relocate those same hash-pinned files;
they cannot substitute a new candidate. Reports go to stdout only.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import struct
import sys
from lib.omf import parse_omf
REPOSITORY = Path(__file__).resolve().parents[1]
DEFAULT_ROOTS = {'baseline': '.analysis/th03-main-exact/gpt-dots-gameplay-promoted-default-cold-v01/round1/source', 'combined': '.analysis/gpt-dots-player-cpu-placement-v02/relink-proposal-v01/run-first-v01/source'}
DEFAULT_TARGET = '.analysis/targets/th03/main.exe'
PINNED = {
    "baseline": {
        "obj/th03/main.obj": "9e29417f344767664c43f2573f470937c8384cb0c326b295b979c098677bc4c0",
        "obj/th03/main.map": "7c1a6e9dcfb9af5ef4cbddd5548fc1b36848ac8c26006cc97ebfb499b2919dfc",
        "bin/th03/main.exe": "6f8ea28e2dd78f20adb0dddec570355522a52222d481bceda6a64653f76d319d",
        "obj/th03/main.@l": "0f1cafec615ce74e8be1eac7ff0ff2bf23f6be2b89b67461f4a581384d76ac4d"
    },
    "combined": {
        "obj/th03/p_cpre.obj": "4fb2e6572da2534632d3489fc889f4441d506120e1b52629fe1d1eb41a5aba78",
        "obj/th03/p_cpu.obj": "26bcae741b3d4579cd10e14209e46f6de10e214e15f474f5e182d2c59fa1a7d6",
        "obj/th03/bm_yume.obj": "70a3bb942afe8e1e962030764b680f1bc7f9c8fefbbf0ef4720cc22cd682e7a1",
        "obj/th03/cs_yume.obj": "8a58065415ae229bd38a0d602eccb5f940955cfed62e2b0b9c425508b2ff0994",
        "obj/th03/main.obj": "8af04e8684b0c24f15115166947909f239e2857c6d4f02600f111cabdaf2f1f6",
        "obj/th03/main.map": "a6f4227210bc2b104c524c8d9bfb4fa702b716abd4735646313fd5e3e1d23a6b",
        "bin/th03/main.exe": "9477aae080a2334ede97d43cf52a102780703018adf454b51c4bf43065082a77",
        "obj/th03/main.@l": "928bb4e29e6d78f29320e53da402dcc2ac3be1f9b905df544478b3ec04873cad"
    },
    "target": {
        ".": "f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b"
    }
}
NEW = [(0xc370, 0xc7a5), (0x159ff, 0x15cb9), (0x16983, 0x16ff0)]

def require(condition, message):
    if not condition:
        raise ValueError(message)

def check_digest(path, expected):
    if not path.is_file():
        raise ValueError(f'required private input is missing: {path}')
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    require(actual == expected, f'historical input hash mismatch: {path}')

def guard_inputs(roots, target):
    for label, files in PINNED.items():
        for relative, digest in files.items():
            path = target if label == 'target' else roots[label] / relative
            check_digest(path, digest)

def module_runs(relocations):
    runs = []
    for row in relocations:
        if not runs or runs[-1]['module'] != row['module']:
            runs.append(dict(module=row['module'], start=row['index'], count=1))
        else:
            runs[-1]['count'] += 1
    require(len({r['module'] for r in runs}) == len(runs), 'module appears in multiple literal MZ runs')
    return runs

def same_order(actual, expected, label):
    require(actual == expected, f'literal order mismatch: {label}')

def index(d, i):
    n = d[i]
    i += 1
    if n & 128:
        n = (n & 127) << 8 | d[i]
        i += 1
    return (n, i)

def rows(p):
    out = []
    for line in p.read_text().splitlines():
        m = re.fullmatch(' ([0-9A-F]{4}):([0-9A-F]{4}) ([0-9A-F]+) C=(\\S+)\\s+S=(\\S+)\\s+G=(\\S+)\\s+M=(\\S+)\\s+ACBP=(\\S+)', line)
        if m:
            s, o, n, cl, seg, g, mod, ac = m.groups()
            start = int(s, 16) * 16 + int(o, 16)
            out.append(dict(start=start, size=int(n, 16), segment=seg, module=mod, group=g, acbp=ac))
    return out

def mz(p, rs):
    b = p.read_bytes()
    n = struct.unpack_from('<H', b, 6)[0]
    off = struct.unpack_from('<H', b, 24)[0]
    out = []
    for i in range(n):
        o, s = struct.unpack_from('<HH', b, off + 4 * i)
        a = 16 * s + o
        rr = [r for r in rs if r['start'] <= a and a + 2 <= r['start'] + r['size']]
        require(len(rr) == 1, 'complete MZ relocation word must have exactly one MAP owner')
        out.append(dict(index=i, site=a, pair=[s, o], module=rr[0]['module'], segment=rr[0]['segment']))
    return out

def omf(p, rs):
    """Decode only the observed non-threaded 16-bit FIXUPP dialect; fail otherwise."""
    records = parse_omf(p.read_bytes())
    names = ['']
    segs = [None]
    exts = [None]
    mod = records[0].data[1:].decode('ascii')
    segments = {r['segment']: r for r in rs if r['module'] == mod}
    blocks = []
    for r in records:
        d = r.data
        if r.record_type == 0x96:
            i = 0
            while i < len(d):
                n = d[i]
                i += 1
                names.append(d[i:i + n].decode('ascii'))
                i += n
        elif r.record_type == 0x98:
            require(d[0] >> 5 != 0, 'unexpected pinned evidence')
            ni, i = index(d, 3)
            segs.append(names[ni])
        elif r.record_type == 0x8c:
            i = 0
            while i < len(d):
                n = d[i]
                i += 1
                exts.append(d[i:i + n].decode('ascii'))
                i += n
                _, i = index(d, i)
    for ri, r in enumerate(records):
        d = r.data
        if r.record_type == 0xa0:
            si, i = index(d, 0)
            offset = struct.unpack_from('<H', d, i)[0]
            i += 2
            block = dict(record=ri, segment=segs[si], offset=offset, size=len(d) - i, fixups=[])
            blocks.append(block)
        elif r.record_type == 0x9c:
            i = 0
            while i < len(d):
                begin = i
                loc = d[i]
                require(loc & 128, 'thread record')
                position = (loc & 3) << 8 | d[i + 1]
                kind = loc >> 2 & 15
                fd = d[i + 2]
                i += 3
                require(not fd & 128 and (not fd & 8), 'threaded fixup')
                fm = fd >> 4 & 7
                tm = fd & 3
                frame = None
                if fm <= 2:
                    frame, i = index(d, i)
                elif fm == 3:
                    frame = struct.unpack_from('<H', d, i)[0]
                    i += 2
                target, i = index(d, i)
                disp = 0
                if not fd & 4:
                    disp = struct.unpack_from('<H', d, i)[0]
                    i += 2
                require(tm in (0, 1, 2), 'unexpected pinned evidence')
                name = exts[target] if tm == 2 else segs[target] if tm == 0 else 'group#' + str(target)
                site = segments[block['segment']]['start'] + block['offset'] + position
                f = dict(site=site, kind=kind, target_method=tm, target=name, frame_method=fm, frame=frame, raw=d[begin:i].hex())
                if kind in (2, 3):
                    f['mz_site'] = site + (2 if kind == 3 else 0)
                block['fixups'].append(f)
    return (mod, blocks)

def analyze(roots, target):
    """Check historical files before parsing and again before reporting."""
    guard_inputs(roots, target)
    report = {'inputs': {}, 'images': {}}
    for label, root in roots.items():
        mp = root / 'obj/th03/main.map'
        ep = root / 'bin/th03/main.exe'
        rs = rows(mp)
        rels = mz(ep, rs)
        mods = module_runs(rels)
        image = {'player_map': [r for r in rs if r['segment'] == 'PLAYER_M_TEXT'], 'module_runs': mods, 'outside': [r for r in rels if not any((a <= r['site'] < b for a, b in NEW))], 'objects': {}}
        for obj in ['main'] if label == 'baseline' else ['p_cpre', 'p_cpu', 'bm_yume', 'cs_yume', 'main']:
            op = root / f'obj/th03/{obj}.obj'
            mod, blocks = omf(op, rs)
            far = [f for b in blocks for f in b['fixups'] if 'mz_site' in f]
            exe = ep.read_bytes()
            header = struct.unpack_from('<H', exe, 8)[0] * 16
            optimized = []
            predicted = []
            for f in far:
                # Observed native same-CS far-call lowering: NOP / PUSH CS / CALL near.
                if f['kind'] == 3 and exe[header + f['site'] - 1:header + f['site'] + 2] == bytes.fromhex('900ee8'):
                    require((f['target_method'], f['target']) in [(0, '_TEXT'), (2, '@bullets_add$qv')], (label, obj, f))
                    optimized.append(f)
                else:
                    predicted.append(f['mz_site'])
            actual = [r['site'] for r in rels if r['module'] == mod]
            same_order(predicted, actual, (label, obj))
            image['objects'][obj] = {'module': mod, 'surviving_far_subrecords_match_literal_mz': True, 'far_count': len(predicted), 'same_cs_far_calls_lowered': optimized, 'player_blocks': [b for b in blocks if b['segment'] == 'PLAYER_M_TEXT']}
            report['inputs'][str(op)] = hashlib.sha256(op.read_bytes()).hexdigest()
        for p in [mp, ep, root / 'obj/th03/main.@l']:
            report['inputs'][str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
        report['images'][label] = image
    A = report['images']['baseline']['outside']
    B = report['images']['combined']['outside']
    require(len(A) == len(B) == 1519, 'unexpected pinned evidence')
    report['outside_positional_differences'] = sum((x['pair'] != y['pair'] for x, y in zip(A, B)))
    for name, lo, hi in [('prefix', 0xc0d8, 0xc370), ('suffix', 0xc7a5, 0xd6d4)]:
        aa = [r['site'] for r in A if lo <= r['site'] < hi]
        bb = [r['site'] for r in B if lo <= r['site'] < hi]
        report[name] = {'baseline': [hex(x) for x in aa], 'combined': [hex(x) for x in bb], 'internal_differences': sum((x != y for x, y in zip(aa, bb)))}
    report['precedence_cycle'] = [{'before': 'main', 'after': 'p_cpre', 'reason': 'outside literal 0xB735 precedes 0xC10E'}, {'before': 'p_cpre', 'after': 'p_cpu', 'reason': 'same-name BYTE PUBLIC contributions C0D8,C370'}, {'before': 'p_cpu', 'after': 'main', 'reason': 'same-name BYTE PUBLIC contributions C370,C7A5'}]
    require(next((i for i, r in enumerate(A) if r['site'] == 0xb735)) < next((i for i, r in enumerate(A) if r['site'] == 0xc10e)), 'unexpected pinned evidence')
    report['scope'] = 'Read-only historical diagnostic; current object partition and observed TLINK traversal only. No acceptance gate is changed.'
    report['outside_count'] = len(A)
    report['prefix_filtered_indices'] = {tag: [i for i, r in enumerate(im['outside']) if 0xc0d8 <= r['site'] < 0xc370] for tag, im in report['images'].items()}
    report['outside_common_without_prefix_suffix_equal'] = [r['pair'] for r in A if not (0xc0d8 <= r['site'] < 0xc370 or 0xc7a5 <= r['site'] < 0xd6d4)] == [r['pair'] for r in B if not (0xc0d8 <= r['site'] < 0xc370 or 0xc7a5 <= r['site'] < 0xd6d4)]
    for image in report['images'].values():
        image['mapped_mz_sites'] = sum((r['count'] for r in image['module_runs']))
        image['all_modules_single_contiguous_run'] = True
        image['module_count'] = len(image['module_runs'])
        image['module_runs'] = [r for r in image['module_runs'] if r['module'] in {o['module'] for o in image['objects'].values()}]
        del image['outside']
        for obj in image['objects'].values():
            for block in obj['player_blocks']:
                block['all_fixup_count'] = len(block['fixups'])
                block['far_fixups'] = [f for f in block.pop('fixups') if 'mz_site' in f]
    t = target.read_bytes()
    require(hashlib.sha256(t).hexdigest() == 'f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b', 'unexpected pinned evidence')
    report['inputs'][str(target)] = hashlib.sha256(t).hexdigest()
    regions = [('prefix', 0xc0d8, 0xc370), ('cpu', 0xc370, 0xc7a5), ('bomb', 0x159ff, 0x15cb9), ('tail', 0xc7a5, 0xd6d4), ('charge', 0x16983, 0x16ff0)]
    selected = []
    for i in range(struct.unpack_from('<H', t, 6)[0]):
        o, seg = struct.unpack_from('<HH', t, struct.unpack_from('<H', t, 24)[0] + 4 * i)
        site = seg * 16 + o
        for name, lo, hi in regions:
            if lo <= site < hi:
                selected.append((name, i, site))
    runs = []
    for name, i, site in selected:
        if not runs or name != runs[-1]['owner']:
            runs.append(dict(owner=name, count=1, first_original_index=i, last_original_index=i))
        else:
            runs[-1]['count'] += 1
            runs[-1]['last_original_index'] = i
    report['target_selected_union_runs'] = runs
    cpu_records = [[b['record'], hex(f['mz_site'])] for b in report['images']['baseline']['objects']['main']['player_blocks'] for f in b['far_fixups'] if 0xc370 <= f['mz_site'] < 0xc7a5]
    require(cpu_records == [[930, '0xc452'], [932, '0xc5bb']], 'unexpected pinned evidence')
    report['same_framing_cpu_obstruction'] = {'required_target_sites': ['0xC5BB', '0xC452'], 'baseline_record_sites': cpu_records, 'reason': 'Literal record traversal forces C452 before C5BB while those two record boundaries remain.'}
    guard_inputs(roots, target)
    return report

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-root', type=Path, default=REPOSITORY / DEFAULT_ROOTS['baseline'])
    parser.add_argument('--candidate-root', type=Path, default=REPOSITORY / DEFAULT_ROOTS['combined'])
    parser.add_argument('--target', type=Path, default=REPOSITORY / DEFAULT_TARGET)
    args = parser.parse_args(argv)
    try:
        report = analyze({'baseline': args.baseline_root, 'combined': args.candidate_root}, args.target)
    except (OSError, ValueError, IndexError, KeyError, struct.error) as error:
        print(f'CPU link-order review failed: {error}', file=sys.stderr)
        return 1
    print(json.dumps(report, separators=(',', ':')))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
