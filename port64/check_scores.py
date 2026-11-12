#!/usr/bin/env python3
"""Compare score encryption, insertion, name entry and continue with MAINL."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import tomllib


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-checks', type=Path, required=True)
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--dos-root', type=Path, required=True)
    args = parser.parse_args()
    root = args.dos_root.resolve()
    sys.path.insert(0, str(root / 'scripts'))
    from lib.pc98 import parse_mz
    from review_th03_mainl_regist import RegistrationProbe, section, number_digits, encrypted
    from review_th03_mainl_root import RootProbe
    raw = (root / '.analysis/toolchain/wineprefix/drive_c/TH03PKG/af1409l/r1/mainl.exe').read_bytes()
    manifest = tomllib.loads((root / 'config/th03_diet.toml').read_text())
    expected = next(row['decoded_sha256'] for row in manifest['artifacts'] if row['id'] == 'th03-mainl')
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('original MAINL identity changed')
    image = parse_mz(raw)
    executable = str(args.native_checks.resolve())

    def native_path(path):
        return subprocess.check_output(['wslpath', '-w', str(path)], text=True).strip() if args.native_checks.suffix == '.exe' else str(path)

    def run(*command):
        return subprocess.check_output([executable, *map(str, command)], text=True)

    with tempfile.TemporaryDirectory(prefix='th03-scores-') as work:
        plain = section()
        file = Path(work) / 'section.bin'
        file.write_bytes(plain)
        for seed, stage, credits in ((0, 1, 3), (0x12345678, 99, 3), (0xffffffff, 99, 2)):
            random_words = []
            state = seed
            for _ in range(3):
                state = (state * 0x015a4e35 + 1) & 0xffffffff
                random_words.append((state >> 16) & 65535)
            probe = RegistrationProbe(image, random_words=random_words)
            probe.resident(stage=stage, credits=credits)
            probe.set_hi(plain)
            probe.run(0x1900, (0,))
            actual = list(map(int, run('--score-codec', native_path(file), seed, stage, credits).split()))
            if actual != [state, *probe.hi()]:
                raise ValueError(f'score encryption/checksum/clear flag differs: {(seed, stage, credits)}')
            probe.run(0x17b9)
            probe.run(0x1874)
            if probe.get('AX') & 255:
                raise ValueError('original decoder rejected the native-equivalent encrypted section')
        print('Complete encrypted sections, key RNG consumption, checksum and clear flag agree with MAINL.', flush=True)
        for missing, corrupt, stage in ((False, False, 1), (False, True, 99), (True, False, 1)):
            seed = 0x12345678
            state, random_words = seed, []
            for _ in range(12 if missing or corrupt else 0):
                state = (state * 0x015a4e35 + 1) & 0xffffffff
                random_words.append((state >> 16) & 65535)
            data = bytearray(encrypted(plain) * 4)
            if corrupt:
                data[206] ^= 1
            score_file = Path(work) / 'YUME.NEM'
            score_file.write_bytes(data)
            probe = RegistrationProbe(image, random_words=random_words or [0], file_exists=not missing, read_bytes=bytes(data[206:412]))
            probe.resident(stage=stage, credits=3)
            probe.run(0x189e, (1,))
            actual = list(map(int, run('--score-file', '-' if missing else native_path(score_file), 1, seed, stage, 3).split()))
            expected_file = b''.join(probe.files) if probe.files else data
            if actual != [state, *probe.hi(), *expected_file]:
                raise ValueError(f'load/recreate/full-file/RNG differs: {missing, corrupt, stage}')
        print('Valid load and missing/corrupt recreation agree in all four encrypted sections, including the original all-rank clear flag quirk.', flush=True)
        for value, credits, stage, character in ((1001, 3, 5, 1), (1000, 0, 5, 6), (901, 2, 7, 15), (1, 3, 9, 18), (0, 0, 1, 1), (1001, 3, 99, 17)):
            probe = RegistrationProbe(image)
            probe.resident(digits=number_digits(value), credits=credits, stage=stage, packed=character)
            probe.set_hi(plain)
            probe.run(0x1a4d)
            place = probe.get('AX')
            if place == 65535:
                place = -1
            actual = list(map(int, run('--score-insert', native_path(file), value, credits, stage, character).split()))
            if actual != [place, *probe.hi()]:
                raise ValueError(f'score insertion/shift/continue digit differs: {(value, credits, stage, character)}')
        print('Score insertion, equal-score order, complete row shifts, character/stage and continue digits agree.', flush=True)
        presses = [value for _ in range(7) for value in (32, 0)] + [32]
        sequences = [presses, [32] * 40 + [0] + [value for _ in range(6) for value in (32, 0)] + [32],
                     [8] * 40 + [0] + presses, [32, 0, 16, 0] + presses, [4, 0, 2, 0, 2, 0, 32],
                     [1, 0, 4, 0, 8, 0, 2, 0] + presses,
                     [4, 0, 2, 0, 2, 0, 4, 0, 1, 0, 2, 0, 8, 0, 32]]
        blank = bytearray(plain)
        blank[2:10] = bytes([14] * 8)
        file.write_bytes(blank)
        for keys in sequences:
            probe = RegistrationProbe(image, keys=keys)
            probe.set_hi(blank)
            probe.run(0x1e7b)
            actual = [list(map(int, line.split())) for line in run('--name-entry', native_path(file), ','.join(map(str, keys))).splitlines()]
            expected = [[frame['regi'], frame['cursor'], frame['done'], *frame['holds'], 45 if frame['cursor'] == 255 else -1] for frame in probe.frames]
            if actual[:-1] != expected or actual[-1] != list(probe.hi()):
                mismatch = next((pair for pair in zip(actual[:-1], expected) if pair[0] != pair[1]), 'final section')
                raise ValueError(f'name input/repeat/underflow differs: {mismatch}')
        print('Every name-entry frame agrees: release locks, repeat, backspace, END, eighth-character underflow and complete name data.', flush=True)
        disk = root / '.analysis/runtime/images/zun.hdi'
        font = root / '.analysis/runtime/fonts/FREECG98.BMP'
        native_frame, dos_frame = Path(work) / 'scores.ppm', Path(work) / 'dos.ppm'
        subprocess.run([str(args.native.resolve()), '--hdi', str(disk), '--font-bmp', str(font), '--headless', '--scene', 'scores', '--frames', '40', '--screenshot', str(native_frame)], check=True)
        subprocess.run(['convert', str(root / '.analysis/runtime/candidates/dos-play-replay/high-scores.png'), '-depth', '8', str(dos_frame)], check=True)
        if native_frame.read_bytes() != dos_frame.read_bytes():
            raise ValueError('complete original DOS high-score frame differs')
        print('Complete original DOS high-score frame agrees in every RGB byte.', flush=True)
        for credits, keys in ((3, [32]), (3, [4, 4, 0, 8, 32]), (3, [4096]), (3, [4, 0, 32]), (0, [32])):
            probe = RootProbe(image, keys=keys)
            probe.resident(stage=5, credits=credits)
            probe.uc.mem_write(0x50034, b'\0')
            probe.uc.mem_write(0x50018, bytes([9] * 16))
            probe.run(0x99d)
            native_keys = [0] * 18 + keys + [0] * 18
            file = Path(work) / 'continue.ppm'
            actual = list(map(int, run('--continue-ui', native_path(disk), native_path(font), credits, ','.join(map(str, native_keys)), native_path(file)).split()))
            resident = probe.uc.mem_read(0x50000, 256)
            expected = [probe.get('AX'), 1, resident[0x36], resident[0x33], resident[0x34], *resident[0x18:0x28]]
            if actual != expected:
                raise ValueError(f'continue choice/latch/lives/stage/scores differs: {credits, keys}: {actual} != {expected}')
        print('Continue yes/no/cancel/exhaustion agrees with original MAINL, including score clearing and resident changes.', flush=True)
        subprocess.run([executable, '--scores-flow', native_path(disk), native_path(font), native_path(Path(work) / 'save')], check=True)


if __name__ == '__main__':
    main()
