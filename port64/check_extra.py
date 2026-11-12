#!/usr/bin/env python3
"""Compare all Extra Attack motion/collision and special spawns with MAIN.

The original shared flight, vector/angle, RNG, bullet/effect allocation and
charge/shot collision run together. Reimu's real render loop advances its clock;
only the near sprite helper is captured. Other rendering is checked separately.
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
    args = parser.parse_args()
    root = args.dos_root.resolve()
    target = next(row for row in tomllib.loads((root / 'config/targets.toml').read_text())['artifacts'] if row['id'] == 'th03-main')
    raw = (root / target['private_path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != target['sha256']:
        raise ValueError('original MAIN identity changed')
    sys.path.insert(0, str(root / 'scripts'))
    from lib.pc98 import parse_mz
    image = parse_mz(raw)
    count = 0
    for character in range(9):
        for special in (0, 1) if character not in (1, 7) else (0,):
            for pid, ticks, spawns in ((0, 0, 1), (1, 110, 1), (0, 240, 1), (1, 520, 1), (0, 180, 20)):
                case = character, pid, ticks, special, spawns
                command = [str(args.native_checks.resolve()), '--extra', *map(str, case)]
                native = list(map(int, subprocess.check_output(command, text=True).split()))
                expected = original(image, character, pid, special, 0, ticks, True, True, spawns)
                if native != expected:
                    index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
                    raise ValueError(f'{case}, index={index}: native={native[index:index + 8]}, original={expected[index:index + 8]}')
                count += 1
        print(f'Extra character {character}: complete state/pools/collision agree', flush=True)
    print(f'{count} ordinary/special Extra snapshots match original MAIN')


if __name__ == '__main__':
    main()
