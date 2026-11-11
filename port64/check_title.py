#!/usr/bin/env python3
"""Compare the portable title with original TH03 decoding and a DOS frame.

Run with the DOS checkout's Python environment, which supplies Unicorn and
Capstone. ImageMagick converts the supplied original DOS screenshot to PPM.
"""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--native', type=Path, required=True)
    p.add_argument('--dos-root', type=Path, required=True)
    p.add_argument('--dos-frame', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    root, output = args.dos_root.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    disk = root / '.analysis/runtime/images/zun.hdi'
    targets = tomllib.loads((root / 'config/targets.toml').read_text())
    if sha(disk.read_bytes()) != targets['source']['hdi_sha256']:
        raise ValueError('original Japanese HDI identity changed')
    decoded = root / '.analysis/toolchain/wineprefix/drive_c/TH03PKG/af1409l/r1/mainl.exe'
    diet = tomllib.loads((root / 'config/th03_diet.toml').read_text())
    expected = next(row for row in diet['artifacts'] if row['id'] == 'th03-mainl')
    raw = decoded.read_bytes()
    if sha(raw) != expected['decoded_sha256']:
        raise ValueError('original MAINL decoded identity changed')
    command = [str(args.native.resolve()), '--hdi', str(disk)]
    subprocess.run(command + ['--extract', 'TL02.PI', '--output', str(output / 'TL02.PI')], check=True)
    subprocess.run(command + ['--pi', 'TL02.PI', '--packed', str(output / 'portable.pixels')], check=True)
    sys.path.insert(0, str(root / 'scripts'))
    from lib.pc98 import parse_mz
    from review_th03_mainl_pi_decoder import DecoderProbe, LOAD_ARGS
    probe = DecoderProbe(parse_mz(raw), {})
    probe.file = (output / 'TL02.PI').read_bytes()
    probe.run('load', LOAD_ARGS, budget=30000000)
    if probe.get('AX') != 0:
        raise ValueError('original PI decoder returned failure')
    offset, segment = struct.unpack('<HH', probe.uc.mem_read(0x50300, 4))
    original = bytes(probe.uc.mem_read(segment * 16 + offset, 128000))
    if original != (output / 'portable.pixels').read_bytes():
        raise ValueError('portable PI pixels differ from original instructions')
    (output / 'original.pixels').write_bytes(original)
    subprocess.run(command + ['--headless', '--scene', 'menu', '--screenshot', str(output / 'portable.ppm')], check=True)
    subprocess.run(['convert', str(args.dos_frame.resolve()), '-depth', '8', str(output / 'dos.ppm')], check=True)
    if (output / 'dos.ppm').read_bytes() != (output / 'portable.ppm').read_bytes():
        raise ValueError('complete title/menu differs from supplied original DOS frame')
    print('Original instructions: all 128000 PI bytes agree; full 640x400 DOS/menu RGB agrees.')
    if sha(disk.read_bytes()) != targets['source']['hdi_sha256']:
        raise ValueError('original media changed')


if __name__ == '__main__':
    main()
