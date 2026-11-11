#!/usr/bin/env python3
"""Compare TH03 MRS alpha/noalpha/altered/flip blits with original MAIN."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import tomllib


def original(image, raw, left, top, alpha, altered, flip):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INSN
    from unicorn.x86_const import (UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_SS,
                                  UC_X86_REG_IP, UC_X86_INS_OUT)
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    u.mem_write(0x60000, raw)
    u.mem_write(0x2d560 + 0x1d64, struct.pack('<HH', 0, 0x6000))
    planes = [bytearray([value] * 16000) for value in (0xaa, 0x33, 0x55, 0xff)]
    bases = (0xa8000, 0xb0000, 0xb8000, 0xe0000)
    for base, plane in zip(bases, planes):
        u.mem_write(base, bytes(plane))
    rmw = False

    def hardware(uc, address, size, unused):
        nonlocal rmw
        if address != 0x10f5c:
            return
        rmw = True  # The alpha pass sets the GRCG tile to black.
        sp = uc.reg_read(UC_X86_REG_SP)
        ip, cs = struct.unpack('<HH', uc.mem_read(0x80000 + sp, 4))
        uc.reg_write(UC_X86_REG_SP, sp + 8)
        uc.reg_write(UC_X86_REG_CS, cs)
        uc.reg_write(UC_X86_REG_IP, ip)

    def write(uc, access, address, size, value, unused):
        if not rmw:
            return
        for i in range(size):
            at = address + i - bases[0]
            if 0 <= at < 16000:
                mask = (value >> (i * 8)) & 255
                for plane in planes:
                    plane[at] &= ~mask & 255

    def out(uc, port, size, value, unused):
        nonlocal rmw
        if port == 0x7c and not value and rmw:
            rmw = False
            for base, plane in zip(bases, planes):
                uc.mem_write(base, bytes(plane))

    u.hook_add(UC_HOOK_CODE, hardware)
    u.hook_add(UC_HOOK_MEM_WRITE, write, begin=0xa8000, end=0xabfff)
    u.hook_add(UC_HOOK_INSN, out, None, 1, 0, UC_X86_INS_OUT)

    def call(offset, args=()):
        for reg, value in ((UC_X86_REG_CS, 0x1e8f), (UC_X86_REG_DS, 0x2d56),
                           (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
            u.reg_write(reg, value)
        u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, 0x239d) + b''.join(struct.pack('<H', n & 65535) for n in reversed(args)))
        u.emu_start(0x1e8f0 + offset, 0x329d0, count=2000000)
        if u.reg_read(UC_X86_REG_IP) != 0xf000:
            raise ValueError(f'original MRS {offset:04x} did not return')

    if flip:
        call(0x5d4)
        call(0x7b6, (0,))
    call(0x656 if alpha else 0x704, (left, top, 0) if alpha else (left, top, 0, altered))
    planes = [bytes(u.mem_read(base, 16000)) for base in bases]
    pixels = bytearray(128000)
    for at in range(16000):
        for bit in range(8):
            mask = 128 >> bit
            pixels[at * 8 + bit] = sum((1 << p) for p, plane in enumerate(planes) if plane[at] & mask)
    return pixels


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, required=True)
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
    with tempfile.TemporaryDirectory(prefix='th03-mrs-') as temp:
        file = Path(temp) / '00BM.MRS'
        subprocess.run([str(args.native.resolve()), '--hdi', str(root / '.analysis/runtime/images/zun.hdi'),
                        '--main-assets', '--extract', '00BM.MRS', '--output', str(file)], check=True)
        for case in ((16, 16, 0, 0, 0), (337, 17, 0, 1, 1), (24, 16, 1, 0, 0), (336, 16, 1, 0, 1)):
            native = subprocess.check_output([str(args.native_checks.resolve()), '--mrs', str(file), *map(str, case)])
            expected = original(image, file.read_bytes(), *case)
            if native != expected:
                points = [(i % 640, i // 640, a, b) for i, (a, b) in enumerate(zip(native, expected)) if a != b]
                raise ValueError(f'MRS{case}: differing dots={len(points)}, first={points[:8]}')
    print('Original MRS alpha, opaque/altered colors, aligned coordinates and horizontal flip agree in all pixels')


if __name__ == '__main__':
    main()
