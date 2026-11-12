#!/usr/bin/env python3
"""Compare all nine Gauge patterns and Kotohime Extra Attack with original MAIN.

Real bullet allocation/group vectors, flight, charge/shot collision, effects,
palette restore and RNG run together. Only sound output and GRCG drawing are
captured at their service boundaries. Bullet motion is outside these fixtures.
"""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def original(image, character, pid, kind, level, ticks, extra=False, extended=False, spawns=1):
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
    frames = (0x2d68, 0x3794, 0x2888, 0x2006, 0x28f8, 0x267a, 0x38f4, 0x1f58, 0x4b7e)
    centers = (None, None, (None, 0x2884), (0x1ffe, 0x2002), None, (0x2676, None), None, (0x1f54, None), None)
    for at, size in ((0x65a6, 256), (0x292a, 1024), (0x2d54, 12), (0x3790, 6), (0x2884, 6),
                     (0x1ffe, 10), (0x28f8, 18), (0x2676, 6), (0x38f4, 2), (0x1f54, 6),
                     (0x4b7e, 2), (0x2d68, 2), (0x3946, 121), (0x68de, 0x8df4 - 0x68de),
                     (0x38cc, 2), (0x38dc, 1), (0x6580, 2), (0x66a6, 448), (0x2832, 80), (0x8df6, 1)):
        u.mem_write(ds + at, bytes(size))
    put = lambda at, value, size=1: u.mem_write(ds + at, int(value).to_bytes(size, 'little'))
    u.mem_write(ds + 0x65a6, struct.pack('<hh', 3600, 4800))
    u.mem_write(ds + 0x6626, struct.pack('<hh', 800, 5200))
    put(0x65a6 + 8, character * 2 + 1)
    put(0x6626 + 8, character * 2 + 1)
    put(0x2928, pid)
    put(0x6590, pid * 40)
    put(0x6598, 64)
    put(0x68dc, 8)
    u.mem_write(ds + 0x659c, struct.pack('<hh', 3, -4))
    put(0x68e6, 128)
    u.mem_write(ds + 0x1e52, bytes((i * 13 + 7) & 255 for i in range(256)))
    put(0x1f52, 254)
    palette = bytes((i * 5 + 7) & 255 for i in range(48))
    u.mem_write(ds + 0x11ba, palette)
    u.mem_write(ds + 0x1d94, palette)
    put(0x2d4, 100, 2)
    sounds = []
    hardware = {0x10f5c: 4, 0x10c40: 8, 0x109e2: 6, 0x10dbe: 8}

    def hook(uc, address, size, unused):
        sp = uc.reg_read(UC_X86_REG_SP)
        if address == 0x1e8f0 + 0x34a:
            sounds.append(struct.unpack('<H', uc.mem_read(0x80000 + sp + 4, 2))[0])
        ip, cs = struct.unpack('<HH', uc.mem_read(0x80000 + sp, 4))
        uc.reg_write(UC_X86_REG_SP, sp + 4 + hardware.get(address, 2))
        uc.reg_write(UC_X86_REG_CS, cs)
        uc.reg_write(UC_X86_REG_IP, ip)

    for address in (*hardware, 0x1e8f0 + 0x34a):
        u.hook_add(UC_HOOK_CODE, hook, begin=address, end=address)

    def call(segment, offset, args=()):
        for reg, value in ((UC_X86_REG_CS, segment + 0x1000), (UC_X86_REG_DS, 0x2d56),
                           (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
            u.reg_write(reg, value)
        u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, 0x239d) + b''.join(struct.pack('<H', v & 65535) for v in reversed(args)))
        u.emu_start((segment + 0x1000) * 16 + offset, 0x329d0, count=1000000)
        if u.reg_read(UC_X86_REG_IP) != 0xf000:
            raise ValueError(f'original Gauge/Extra {segment:04x}:{offset:04x} did not return')

    if extended:
        u.mem_write(ds + 0x230a, bytes(720))
        call(0x18fe, 0x3dc)
        # Reimu's frame byte advances in the renderer, which calls a near
        # sprite helper. Capture only that helper; execute the real loop.
        def skip_near(uc, address, size, unused):
            sp = uc.reg_read(UC_X86_REG_SP)
            ip = struct.unpack('<H', uc.mem_read(0x80000 + sp, 2))[0]
            uc.reg_write(UC_X86_REG_SP, sp + 2)
            uc.reg_write(UC_X86_REG_IP, ip)
        u.hook_add(UC_HOOK_CODE, skip_near, begin=0x28fe0 + 0x13e4, end=0x28fe0 + 0x13e4)
    if extra:
        u.mem_write(ds + 0x2d58 + pid * 4, bytes((6, 1, 2, 0)))
        for p in range(2):
            u.mem_write(ds + 0x2d3c + p * 4, struct.pack('<HH', 0xde, 0x2c15))
        if extended:
            add = (0x129e, 0x164b, 0xadc, 0x40f, 0xd80, 0x845, 0x1fc2, 0xa, 0x1922)
            special = {0: (0x12ee, (2048, 1920, 72)), 2: (0xb26, (2048, 1920, pid ^ 1)),
                       3: (0x4c9, (2048, 1920, 72, 255)), 4: (0xdf3, (2048, 1920)),
                       5: (0x8b6, (2048, 1920, 72)), 6: (0x2026, (2048, 1920, 72)), 8: (0x197f, (2048, 1920))}
            offset, arguments = special[character] if kind else (add[character], (*((3600, 4800) if pid == 0 else (800, 5200)), pid))
            for _ in range(spawns):
                call(0x18fe, offset, arguments)
        elif kind:
            call(0x18fe, 0xdf3, (2048, 0))
        else:
            call(0x18fe, 0xd80, (*((3600, 4800) if pid == 0 else (800, 5200)), pid))
        index = pid * 16 + (8 if kind and character in (4, 8) else 0)
        target_x = struct.unpack('<h', u.mem_read(ds + 0x292a + index * 32 + (2 if extended and kind else 10), 2))[0]
        put(0x66a6, 1)
        u.mem_write(ds + 0x66a8, struct.pack('<hh', target_x - 256, 1920))
        put(0x66a6 + 12, pid ^ 1)
    else:
        put(0x2d54 + pid, 1 if kind == 1 else 3)
        put(0x2d56 + pid, level)
    entry = ((0x139d, 0x161e), (0x139d, 0x1ef5), (0x139d, 0xeb5), (0x1b65, 0x5cd),
             (0x1c15, 0x28a), (0x1bc4, 0x4e8), (0x1c40, 0x4da), (0x1b26, 0x3c3), (0x139d, 0x35f0))[character]
    u.mem_write(ds + 0x4ba0, bytes(6624))
    for tick in range(ticks):
        put(0x6596, tick & 65535, 2)
        u.mem_write(ds + 0x4ba0, bytes(6624))
        call(0x139d, 0x3faf)
        if extra:
            update = (0x1500, 0x1765, 0xc56, 0x63d, 0x100f, 0x9b9, 0x2125, 0x280, 0x1e4e)
            call(0x18fe, update[character] if extended else 0x100f)
            if extended and character == 0:
                call(0x18fe, 0x1619)
        else:
            call(*entry)
            call(entry[0], entry[1] + 24)
        call(0x96e, 0x37d2)
        call(0x96e, 0x3800)
    b = bytes(u.mem_read(ds, 65536))
    signed = lambda at: struct.unpack_from('<h', b, at)[0]
    word = lambda at: struct.unpack_from('<H', b, at)[0]
    out = [*b[0x2d54:0x2d56], b[0x1f52], b[0x8df3], b[0x39be]]
    for base in frames:
        out.extend(b[base:base + 2])
    for pair in centers:
        for p in range(2):
            out.extend(signed(at + p * 2) if at is not None else 0 for at in pair or (None, None))
    out.extend((*b[0x3790:0x3794], *b[0x2d58:0x2d60], *b[0x11ba:0x11ea]))
    out.extend((signed(0x68de), signed(0x68e0), *b[0x68e2:0x68e8], signed(0x68e8), signed(0x68ea), word(0x68ec), *b[0x68ee:0x68f2], b[0x8df2]))
    for i in range(320):
        out.extend(struct.unpack_from('<BBhhhhhhBBBBHBBBBH', b, 0x68f2 + i * 26))
    for i in range(32):
        out.extend(struct.unpack_from('<BBhhhhhhhBBBBh', b, 0x292a + i * 32))
    for i in range(12):
        out.extend(struct.unpack_from('<BBhhBbB', b, 0x3946 + i * 10))
    out.extend((b[0x8df6], b[0x2880]))
    for i in range(13):
        out.extend(struct.unpack_from('<BBhh', b, 0x2832 + i * 6))
    out.extend(b[0x66a6 + i * 14] for i in range(32))
    out.extend(b[0x4ba0:0x6580])
    if extended:
        out.extend(b[0x292a + i * 32 + 23] for i in range(32))
        for i in range(24):
            at = 0x230a + i * 30
            for j in range(7):
                out.extend((signed(at + 2 + j * 2), signed(at + 16 + j * 2)))
    out.extend((len(sounds), *sounds))
    return out


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

    def compare(command, expected):
        native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), *map(str, command)], text=True).split()))
        if native != expected:
            index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
            raise ValueError(f'{command}, index={index}: native={native[index:index + 5]}, original={expected[index:index + 5]}')

    for character in range(9):
        for kind, level, ticks in ((1, 3, 24), (2, 15, 180)):
            case = character, character & 1, kind, level, ticks
            compare(('--gauge', *case), original(image, *case))
    for pid, ticks, kind in ((0, 0, 0), (1, 520, 0), (0, 110, 1), (1, 190, 1)):
        compare(('--koto-extra', pid, ticks, kind), original(image, 4, pid, kind, 0, ticks, True))
    print('Nine Gauge patterns and Kotohime ordinary/Gauge Extra match original MAIN, coupled to full bullet/effect/entity pools and collision')


if __name__ == '__main__':
    main()
