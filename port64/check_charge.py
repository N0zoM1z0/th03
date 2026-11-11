#!/usr/bin/env python3
"""Compare all nine character charge lifecycles with original MAIN.

The original vector, clipping, RNG and hit-circle callees execute together.
Only sound output is captured at its far service boundary.
"""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def original(image, character, pid, ticks, hyper):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE
    from unicorn.x86_const import (UC_X86_REG_AX, UC_X86_REG_SP, UC_X86_REG_CS,
                                  UC_X86_REG_DS, UC_X86_REG_SS, UC_X86_REG_IP)
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    ds = 0x2d560
    for at, size in ((0x2d6a, 768), (0x306c, 1), (0x3796, 300), (0x38c4, 4),
                     (0x288a, 100), (0x65a6, 256), (0x2832, 80), (0x2881, 1), (0x8df6, 1),
                     (0x2008, 768), (0x28fa, 16), (0x267c, 438), (0x38f6, 66),
                     (0x1f5a, 96), (0x4b80, 12), (0x1dca, 4), (0x3ed6, 3072)):
        u.mem_write(ds + at, bytes(size))
    put = lambda at, value, size=1: u.mem_write(ds + at, int(value).to_bytes(size, 'little'))
    player = 0x65a6 + pid * 128
    put(player + 0x22, 1)  # shot_active
    put(player + 0x18, 1234, 2)
    u.mem_write(ds + player, struct.pack('<hh', 1200, 5000))
    put(0x6590, pid)
    put(0x2928, pid)
    u.mem_write(ds + 0x659c, struct.pack('<hh', 6, -6))
    u.mem_write(ds + 0x1e52, bytes((i * 13 + 7) & 255 for i in range(256)))
    put(0x1f52, 254)
    sounds = []

    def hook(uc, address, size, unused):
        if address != 0x1e8f0 + 0x34a:
            return
        sp = uc.reg_read(UC_X86_REG_SP)
        ip, cs, sound = struct.unpack('<HHH', uc.mem_read(0x80000 + sp, 6))
        sounds.append(sound & 255)
        uc.reg_write(UC_X86_REG_SP, sp + 6)
        uc.reg_write(UC_X86_REG_CS, cs)
        uc.reg_write(UC_X86_REG_IP, ip)

    u.hook_add(UC_HOOK_CODE, hook)

    code = (0x139d, 0x139d, 0x139d, 0x1b65, 0x1c15, 0x1bc4, 0x1c40, 0x1b26, 0x139d)[character] + 0x1000

    def call(offset, center=None):
        for reg, value in ((UC_X86_REG_CS, code), (UC_X86_REG_DS, 0x2d56),
                           (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
            u.reg_write(reg, value)
        stack = struct.pack('<HH', 0xf000, 0x239d)
        if center is not None:
            stack += struct.pack('<hh', center[1], center[0])
        u.mem_write(0x8ff00, stack)
        u.emu_start(code * 16 + offset, 0x329d0, count=200000)
        if u.reg_read(UC_X86_REG_IP) != 0xf000:
            raise ValueError(f'original charge call {offset:04x} did not return')
        return u.reg_read(UC_X86_REG_AX) & 255

    add = (0x10c7, 0x1a0c, 0x90f, 0x24, 0x17, 0x1c, 0x19, 0x17, 0x3094)[character]
    update = (0x11ac, 0x1af4, 0x9ee, 0xd3, 0x4f, 0x95, 0xc5, 0x62, 0x30bd)[character]
    hit = (0x1313, 0x1bc7, 0xab7, 0x2b3, 0xde, 0x212, 0x26b, 0x150, 0x313c)[character]
    call(0x113a if hyper and character == 0 else 0x970 if hyper and character == 2 else
         0x7a if hyper and character == 3 else 0x97 if hyper and character == 6 else add,
         None if hyper and character == 2 else (1200, 5000))
    for tick in range(ticks):
        center = (1200 + (tick % 32) * 28, 5000 - (tick % 17) * 16)
        u.mem_write(ds + player, struct.pack('<hh', *center))
        put(0x6596, tick & 65535, 2)
        if hyper and character == 2 and tick < 40:
            call(0x970)
        if hyper and character == 1 and tick == 25:
            call(add, center)
        call(update)
    u.mem_write(ds + 0x38ce, struct.pack('<hhhhhhB', 900, 3000, 700, 1050, 2300, 5100, pid))
    damage = call(hit)
    b = bytes(u.mem_read(ds, 65536))
    word = lambda at: struct.unpack_from('<H', b, at)[0]
    out = [word(player + 0x18), b[player + 0x22], b[0x306c], b[0x38c4 + pid],
           b[0x38c6 + pid], b[0x1f52], b[0x2880], damage, b[0x8df6]]
    for i in range(12):
        at = 0x2d6a + pid * 384 + i * 32
        out.extend((b[at], b[at + 1], b[at + 30], b[at + 31]))
        for sample in range(7):
            out.extend((struct.unpack_from('<h', b, at + 2 + sample * 2)[0],
                        struct.unpack_from('<h', b, at + 16 + sample * 2)[0]))
    for i in range(15):
        at = 0x3796 + pid * 150 + i * 10
        out.extend(struct.unpack_from('<BBhhhh', b, at))
    at = 0x288a + pid * 50
    out.extend((b[at], b[at + 1]))
    for sample in range(12):
        out.extend((struct.unpack_from('<h', b, at + 2 + sample * 2)[0],
                    struct.unpack_from('<h', b, at + 26 + sample * 2)[0]))
    for i in range(32):
        out.extend(struct.unpack_from('<BBBBhhhh', b, 0x2008 + pid * 384 + i * 12))
    out.extend(struct.unpack_from('<BBhhh', b, 0x28fa + pid * 8))
    out.extend((b[0x282e + pid], b[0x2830 + pid]))
    for i in range(4):
        at = 0x267c + pid * 216 + i * 54
        out.extend((b[at + 52], b[at + 53]))
        for sample in range(13):
            out.extend((struct.unpack_from('<h', b, at + sample * 2)[0],
                        struct.unpack_from('<h', b, at + 26 + sample * 2)[0]))
    signed = lambda at: struct.unpack_from('<h', b, at)[0]
    out.extend((b[0x3928 + pid], b[0x392a + pid], signed(0x392c + pid * 2),
                signed(0x3930 + pid * 2), signed(0x3934 + pid * 2)))
    for i in range(4):
        out.extend(struct.unpack_from('<hhBB', b, 0x38f6 + pid * 24 + i * 6))
    for i in range(8):
        out.extend(struct.unpack_from('<BBhh', b, 0x1f5a + pid * 48 + i * 6))
    out.extend(struct.unpack_from('<BBhh', b, 0x4b80 + pid * 6))
    for i in range(13):
        out.extend(struct.unpack_from('<BBhh', b, 0x2832 + i * 6))
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
    cases = ((0, 0, 0, 0), (0, 0, 24, 0), (0, 0, 65, 0), (0, 0, 115, 0),
             (0, 1, 0, 1), (0, 1, 30, 1), (1, 1, 4, 0), (1, 1, 56, 0),
             (1, 1, 120, 0), (1, 1, 32, 1), (2, 0, 1, 0), (2, 0, 24, 0),
             (2, 0, 37, 0), (2, 1, 45, 1), (2, 1, 80, 1),
             (3, 0, 0, 0), (3, 0, 45, 0), (3, 1, 110, 0), (3, 1, 45, 1),
             (4, 1, 8, 0), (4, 1, 100, 0), (5, 0, 42, 0), (5, 0, 120, 0),
             (6, 1, 32, 0), (6, 1, 146, 0), (6, 0, 80, 1),
             (7, 0, 10, 0), (7, 0, 80, 0), (8, 1, 0, 0), (8, 1, 64, 0), (8, 1, 128, 0))
    for case in cases:
        native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--charge-run',
                                                        *map(str, case)], text=True).split()))
        expected = original(image, *case)
        if native != expected:
            index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
            raise ValueError(f'charge case={case}, index={index}: native={native[index:index + 5]}, original={expected[index:index + 5]}')
    print('All nine charge families, projectile Hyper helpers, full histories, clipping, hit-circle RNG and sound events match original MAIN')


if __name__ == '__main__':
    main()
