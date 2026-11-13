#!/usr/bin/env python3
"""Package the Windows x64 preview without external game data or user saves."""
import argparse
import hashlib
from pathlib import Path
import re
import struct
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', type=Path, required=True)
    parser.add_argument('--version', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', args.version):
        parser.error('version must be a filename-safe identifier')
    if args.output.exists():
        parser.error('output already exists; choose a fresh ZIP path')
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT):
        parser.error('commit source and packaging changes before packaging')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    exe = args.exe.read_bytes()
    if len(exe) < 256 or exe[:2] != b'MZ':
        parser.error('expected a Windows x64 executable')
    pe = struct.unpack_from('<I', exe, 60)[0]
    if (pe + 26 > len(exe) or exe[pe:pe + 4] != b'PE\0\0'
            or struct.unpack_from('<H', exe, pe + 4)[0] != 0x8664
            or struct.unpack_from('<H', exe, pe + 24)[0] != 0x20b):
        parser.error('expected AMD64 PE32+')
    digest = hashlib.sha256(exe).hexdigest()
    readme = f'''# TH03 Portable 64-bit — Windows x64 preview {args.version}

Add your original Japanese TH03 game disk as `th03.hdi` and your
2048x2048 Anex86-format font as `FREECG98.BMP` beside `th03-port64.exe`.
For sound, also add the 8192-byte `ym2608_adpcm_rom.bin`, then run `Play.bat`.
`Play-silent.bat` runs without sound and does not require that ROM.

The title initially hides its menu: press a direction to reveal it.
Arrows move/navigate, Z fires/confirms, X bombs, Enter confirms, Esc pauses
or returns, and Q leaves a paused battle. Release keys between menu choices.
Two-player P1 uses T/F/H/B and Z/X; P2 uses the numeric keypad and Left/Right.

Scores and options are written to `save-normal`, outside the game disk.
Keep this directory and your external data files when updating the executable.

Source/build instructions, controls and current verification limits:
https://github.com/N0zoM1z0/th03/blob/{commit}/docs/PORTABLE.md
Source revision: `{commit}`
Executable SHA-256: `{digest}`

This is a native x64 preview. No DOS emulator is required.
The package includes no game image, original executable, font, chip ROM or saves.
Repository-authored code: MIT (`LICENSE.txt`). Vendored ymfm: BSD-3-Clause
(`licenses/ymfm-LICENSE.txt`). MinGW runtimes are linked statically.
'''
    files = {
        'th03-port64.exe': exe,
        'Play.bat': (ROOT / 'port64/Play.bat').read_bytes(),
        'Play-silent.bat': (ROOT / 'port64/Play-silent.bat').read_bytes(),
        'README.md': readme.encode('utf-8'),
        'LICENSE.txt': (ROOT / 'LICENSE').read_bytes(),
        'licenses/ymfm-LICENSE.txt': (ROOT / 'port64/pmd/vendor/ymfm/LICENSE').read_bytes(),
    }
    files['SHA256SUMS.txt'] = ''.join(
        f'{hashlib.sha256(data).hexdigest()}  {name}\n'
        for name, data in sorted(files.items())).encode()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, 'x', zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            archive.writestr(name, data)
    print(f'{args.output}: {len(files)} files; executable SHA-256 {digest}')


if __name__ == '__main__':
    main()
