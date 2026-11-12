#!/usr/bin/env python3
"""Compare the Bomb/effect GRCG rasters with original master.lib instructions."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def original(image, kind, values):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_MEM_WRITE
    from unicorn.x86_const import UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_SS, UC_X86_REG_IP
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    ds = 0x2d560
    u.mem_write(ds + 0x2c0, struct.pack('<H', 0xa800))
    u.mem_write(ds + 0x2c8, b'\0')
    u.mem_write(ds + 0x5e8, b'\xff\xff')
    pixels = bytearray(640 * 200)

    def write(uc, access, address, size, value, unused):
        for i in range(size):
            at = address + i - 0xa8000
            if not 0 <= at < 16000:
                continue
            mask = (value >> (i * 8)) & 255
            for bit in range(8):
                if mask & (128 >> bit):
                    pixels[at * 8 + bit] = 13

    u.hook_add(UC_HOOK_MEM_WRITE, write, begin=0xa8000, end=0xabfff)

    def call(offset, args):
        for reg, value in ((UC_X86_REG_CS, 0x1000), (UC_X86_REG_DS, 0x2d56),
                           (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
            u.reg_write(reg, value)
        u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, 0x239d) + b''.join(struct.pack('<H', n & 65535) for n in reversed(args)))
        u.emu_start(0x10000 + offset, 0x329d0, count=1000000)
        if u.reg_read(UC_X86_REG_IP) != 0xf000:
            raise ValueError(f'original raster {offset:04x} did not return')

    call(0xc40, (16, 8, 303, 191))
    call({'circle': 0x9e2, 'line': 0xdbe, 'triangle': 0xfac, 'trapezoid': 0x1120}[kind], values)
    return pixels


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-checks', type=Path, required=True)
    parser.add_argument('--dos-root', type=Path, required=True)
    args = parser.parse_args()
    root = args.dos_root.resolve()
    config = tomllib.loads((root / 'config/targets.toml').read_text())
    target = next(row for row in config['artifacts'] if row['id'] == 'th03-main')
    raw = (root / target['private_path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != target['sha256']:
        raise ValueError('original MAIN identity changed')
    sys.path.insert(0, str(root / 'scripts'))
    from lib.pc98 import parse_mz
    image = parse_mz(raw)
    cases = [('circle', v) for v in ((160, 100, 80), (8, 90, 40), (160, 184, 32), (160, -4, 32), (160, 100, 0))]
    cases += [('line', v) for v in ((20, 10, 290, 180), (0, 100, 320, 120), (-100, -10, 400, 200),
                                    (160, -30, 120, 250), (50, 8, 50, 191), (303, 191, 16, 8))]
    cases += [('triangle', v) for v in ((160, -12, 353, 155, -33, 155), (-2, 170, 300, 0, 100, 80),
                                        (20, 20, 250, 20, 100, 150), (20, 20, 250, 150, 100, 150))]
    cases += [('trapezoid', v) for v in ((8, 150, 162, 192, 100, 112), (8, 50, 52, 192, 250, 252),
        (8, 10, 14, 192, 90, 94), (8, 303, 315, 192, 200, 212), (100, 50, 50, 8, 100, 100))]
    for kind, values in cases:
        native = subprocess.check_output([str(args.native_checks.resolve()), '--raster', kind, *map(str, values)])
        expected = original(image, kind, values)
        if native != expected:
            points = [(i % 640, i // 640, a, b) for i, (a, b) in enumerate(zip(native, expected)) if a != b]
            raise ValueError(f'{kind}{values}: differing dots={len(points)}, first={points[:8]}')
    print('Original GRCG circle, clipped DDA line and filled triangle/trapezoid rasters agree in all pixels')


if __name__ == '__main__':
    main()
