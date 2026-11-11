#!/usr/bin/env python3
"""Compare nine Bomb controllers and coupled effect pools with original MAIN.

Sound events and hardware drawing calls are captured at their far services.
Palette, RNG, motion, clipping, effect allocation/update/rotation execute together.
Kotohime's fade receives an explicit incoming stack byte in both implementations.
"""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def original(image, character, pid, ticks, stack_color):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_SS, UC_X86_REG_IP
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    ds = 0x2d560
    for at, size in ((0x6580, 2), (0x307e, 514), (0x689a, 64), (0x25dc, 130),
                     (0x2674, 1), (0x28f2, 6), (0x4b8c, 2), (0x3946, 121),
                     (0x659c, 4), (0x65a6, 256)):
        u.mem_write(ds + at, bytes(size))
    put = lambda at, value, size=1: u.mem_write(ds + at, int(value).to_bytes(size, 'little'))
    put(0x6580 + pid, 1)
    put(0x65a6 + pid * 128 + 8, character * 2 + 1)
    put(0x2928, pid)
    put(0x6590, pid * 40)
    palette = bytes((i * 5 + 7) & 255 for i in range(48))
    u.mem_write(ds + 0x11ba, palette)
    u.mem_write(ds + 0x1d94, palette)
    put(0x2d4, 100, 2)
    u.mem_write(ds + 0x1e52, bytes((i * 13 + 7) & 255 for i in range(256)))
    put(0x1f52, 254)
    sounds = []
    hardware = {0x10704: 0, 0x1071a: 0, 0x10f5c: 4, 0x10f86: 0, 0x10c40: 8,
                0x1e8f0 + 0x704: 8, 0x1e8f0 + 0x810: 6, 0x1e8f0 + 0x872: 8,
                0x109e2: 6, 0x10dbe: 8, 0x10fac: 12, 0x1109a: 6,
                0x11c7e: 0, 0x196e0 + 0x1cbe: 0}

    def hook(uc, address, size, unused):
        if address not in hardware and address != 0x1e8f0 + 0x34a:
            return
        sp = uc.reg_read(UC_X86_REG_SP)
        ip, cs = struct.unpack('<HH', uc.mem_read(0x80000 + sp, 4))
        count = hardware.get(address, 2)
        if address == 0x1e8f0 + 0x34a:
            sounds.append(struct.unpack('<H', uc.mem_read(0x80000 + sp + 4, 2))[0])
        uc.reg_write(UC_X86_REG_SP, sp + 4 + count)
        uc.reg_write(UC_X86_REG_CS, cs)
        uc.reg_write(UC_X86_REG_IP, ip)

    u.hook_add(UC_HOOK_CODE, hook)

    def call(segment, offset):
        for reg, value in ((UC_X86_REG_CS, segment + 0x1000), (UC_X86_REG_DS, 0x2d56),
                           (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
            u.reg_write(reg, value)
        u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, 0x239d))
        u.mem_write(0x8fefc, bytes([stack_color]))
        u.emu_start((segment + 0x1000) * 16 + offset, 0x329d0, count=200000)
        if u.reg_read(UC_X86_REG_IP) != 0xf000:
            raise ValueError(f'original Bomb {segment:04x}:{offset:04x} did not return')

    update = (0x139d, (0x16bc, 0x3673)[character]) if character < 2 else (0x183c, 0x1eb) if character == 3 else (0x139d, 0x164e)
    render = ((0x139d, 0x1811), (0x139d, 0x37ea), (0x139d, 0xee5), (0x183c, 0x3a6),
              (0x183c, 0x7f8), (0x183c, 0x5ea), (0x183c, 0xa08), (0x183c, 1), (0x139d, 0x202f))[character]
    for tick in range(ticks):
        call(*update)
        call(0x96e, 0x37d2)
        call(*render)
        call(0x96e, 0x3800)
    b = bytes(u.mem_read(ds, 65536))
    word = lambda at: struct.unpack_from('<h', b, at)[0]
    out = [b[0x6580 + pid], b[0x307e + pid], word(0x659c + pid * 2), word(0x2d4), b[0x1f52], b[0x39be]]
    out.extend(b[0x11ba:0x11ea])
    for i in range(32):
        at = 0x3080 + pid * 256 + i * 8
        out.extend((b[at], *struct.unpack_from('<hhh', b, at + 2)))
    for i in range(8):
        out.extend(struct.unpack_from('<hH', b, 0x689a + pid * 32 + i * 4))
    for i in range(8):
        out.extend(struct.unpack_from('<hhhh', b, 0x25de + pid * 64 + i * 8))
    out.extend((word(0x25dc), word(0x28f6), b[0x2674], word(0x4b8c), word(0x28f2), word(0x28f4)))
    for i in range(12):
        out.extend(struct.unpack_from('<BBhhBbB', b, 0x3946 + i * 10))
    out.extend((len(sounds), *sounds))
    return out


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
    for character in range(9):
        for ticks in (80, 170, 180):
            case = character, character & 1, ticks, 90
            native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--bomb-run', *map(str, case)], text=True).split()))
            expected = original(image, *case)
            if native != expected:
                index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
                raise ValueError(f'Bomb case={case}, index={index}: native={native[index:index + 6]}, original={expected[index:index + 6]}')
    print('Nine Bomb controllers and coupled effect pools, palettes, motion, RNG and sound events match original MAIN')


if __name__ == '__main__':
    main()
