#!/usr/bin/env python3
"""Compare the shared BOSS controller and all nine BOSS families with original MAIN instructions.

Real templates, launch/reversal, pattern selection, bullets, Extra entities,
collision, shot hits, palette restore, explosion rewards and RNG run together.
Only final sprite output and sound playback are captured at service boundaries.
"""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
import tomllib

from check_gauge import original


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-checks', type=Path, required=True)
    parser.add_argument('--dos-root', type=Path, required=True)
    parser.add_argument('--character', type=int, choices=range(9))
    args = parser.parse_args()
    root = args.dos_root.resolve()
    target = next(row for row in tomllib.loads((root / 'config/targets.toml').read_text())['artifacts'] if row['id'] == 'th03-main')
    raw = (root / target['private_path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != target['sha256']:
        raise ValueError('original MAIN identity changed')
    sys.path.insert(0, str(root / 'scripts'))
    from lib.pc98 import parse_mz
    image = parse_mz(raw)
    for character, name, modes in ((0, 'reimu', (2, 7, 8, 15)), (1, 'mima', (2, 6, 11, 14)), (2, 'marisa', (2, 6, 8, 11)), (3, 'ellen', (2, 6, 11)), (4, 'kotohime', (2, 7, 10, 12)), (5, 'kana', (2, 5, 7, 13)), (6, 'rikako', (2, 6, 7)), (7, 'chiyuri', (2, 6, 10, 14)), (8, 'yumemi', (2, 5, 7, 11, 15))):
        if args.character is not None and args.character != character:
            continue
        cases = [(0, 0, 0, 0), (1, 0, 100, 8), (0, 0, 1024, 16)]
        cases += [(mode & 1, mode, 160, 8) for mode in (*modes, 128)]
        if character in (2, 7):
            cases.append((1, 11 if character==2 else 6, 100, 3))  # Sparse clouds before the level8 ring branch.
        if character == 8:
            cases += [(1, 2, 20, 16), (0, 7, 40, 8), (1, 15, 96, 8), (0, 15, 320, 16)]
        cases += [(1, 255, 28, 16), (0, 256, 40, 8), (1, 257, 28, 8)]
        for pid, mode, ticks, level in cases:
            case = pid, mode, ticks, level
            native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--boss', str(character), *map(str, case)], text=True).split()))
            expected = original(image, character, pid, 0, level, ticks, True, True, boss_case=mode)
            if native != expected:
                index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
                raise ValueError(f'{name} {case}, index={index}: native={native[index:index + 10]}, original={expected[index:index + 10]}')
            print(f'{name} BOSS {case}: complete state/pools/collision agree', flush=True)
    print('Selected BOSS templates, patterns, pools and collision match original MAIN')


if __name__ == '__main__':
    main()
