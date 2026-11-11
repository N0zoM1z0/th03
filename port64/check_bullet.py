#!/usr/bin/env python3
"""Compare portable bullet group velocities with original MAIN instructions."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def original(image, group, count, speed, angle, index, cursor, spawn=None, run=None):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE
    from unicorn.x86_const import (UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS,
                                  UC_X86_REG_SS, UC_X86_REG_IP, UC_X86_REG_AX)
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    ds = 0x2d560
    kind, pid, base_speed, trail, trail_cursor, fg0, fg1 = spawn or (0, 0, 0, 0, 0, 0, 0)
    t = struct.pack('<hhBBBBBBhhHBBBB', 1200, 1600, speed, angle, pid, group, 128, count,
                    0, 0, 0x1234, kind, 1, 1, trail)
    u.mem_write(ds + 0x68de, t)
    u.mem_write(ds + 0x65a6, struct.pack('<hh', 3600, 4800))
    u.mem_write(ds + 0x6626, struct.pack('<hh', 800, 5200))
    u.mem_write(ds + 0x6590, bytes([40 if pid else 0]))
    u.mem_write(ds + 0x68dc, bytes([base_speed]))
    u.mem_write(ds + 0x6598, bytes([0]))
    u.mem_write(ds + 0x659c, struct.pack('<hh', fg0, fg1))
    u.mem_write(ds + 0x68f2, bytes(320 * 26))
    u.mem_write(ds + 0x68f2, b'\x05')
    u.mem_write(ds + 0x8972, bytes(48 * 24))
    u.mem_write(ds + 0x8df3, bytes([trail_cursor]))
    u.mem_write(ds + 0x1e52, bytes((i * 13 + 7) & 255 for i in range(256)))
    u.mem_write(ds + 0x1f52, bytes([cursor]))
    for register, value in ((UC_X86_REG_CS, 0x239d), (UC_X86_REG_DS, 0x2d56),
                            (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
        u.reg_write(register, value)
    u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, 0x239d) if spawn else struct.pack('<Hh', 0xf000, index))
    u.emu_start(0x239d0 + (0x3d60 if spawn else 0x39d2), 0x239d0 + 0xf000, count=100000)
    if u.reg_read(UC_X86_REG_IP) != 0xf000:
        raise ValueError('original bullet group did not return')
    if run:
        ticks, policy = run
        tick = 0

        def hook(uc, address, size, unused):
            if address == 0x239d0 + 0x2d3d:
                sp = uc.reg_read(UC_X86_REG_SP)
                ip, cs = struct.unpack('<HH', uc.mem_read(0x80000 + sp, 4))
                uc.reg_write(UC_X86_REG_AX, int(policy in (1, 4) and tick == 2))
                uc.reg_write(UC_X86_REG_SP, sp + 4)
                uc.reg_write(UC_X86_REG_CS, cs)
                uc.reg_write(UC_X86_REG_IP, ip)

        u.hook_add(UC_HOOK_CODE, hook)
        for tick in range(ticks):
            u.mem_write(ds + 0x4ba0, bytes(6624))
            u.mem_write(ds + 0x6580, bytes([int(policy == 2 and tick >= 2), 0]))
            u.mem_write(ds + 0x658b, bytes([0, int(policy == 3 and tick >= 1)]))
            u.mem_write(ds + 0x2d54, bytes([int(policy == 4)] * 2))
            u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, 0x239d))
            u.reg_write(UC_X86_REG_SP, 0xff00)
            u.reg_write(UC_X86_REG_IP, 0x404b)
            u.emu_start(0x239d0 + 0x404b, 0x239d0 + 0xf000, count=100000)
            if u.reg_read(UC_X86_REG_IP) != 0xf000:
                raise ValueError('original bullet update did not return')
    if spawn:
        b = bytes(u.mem_read(ds, 65536))
        word = lambda at: struct.unpack_from('<H', b, at)[0]
        signed = lambda at: struct.unpack_from('<h', b, at)[0]
        out = [signed(0x68de), signed(0x68e0), *b[0x68e2:0x68e8], signed(0x68e8), signed(0x68ea),
               word(0x68ec), *b[0x68ee:0x68f2], b[0x8df2], b[0x1f52], b[0x8df3]]
        for i in range(320):
            at = 0x68f2 + i * 26
            out.extend([b[at], b[at + 1], *struct.unpack_from('<hhhhhh', b, at + 2),
                        *b[at + 14:at + 18], word(at + 18), *b[at + 20:at + 24],
                        (word(at + 24) - 0x8972) // 24 if b[at + 23] else 0])
        out.extend(struct.unpack_from('<576h', b, 0x8972))
        if run:
            out.extend(b[0x4ba0:0x6580])
        return out
    velocity = struct.unpack('<hh', u.mem_read(ds + 0x68de + 10, 4))
    return [u.reg_read(UC_X86_REG_AX), *velocity,
            bytes(u.mem_read(ds + 0x8df2, 1))[0], bytes(u.mem_read(ds + 0x1f52, 1))[0]]


def original_pellet(image, left, top, cel):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16
    from unicorn.x86_const import (UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES,
                                  UC_X86_REG_SS, UC_X86_REG_IP, UC_X86_REG_AX, UC_X86_REG_BX, UC_X86_REG_DX)
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    # The 83-byte pellet writer has no segment relocations or callees.
    u.mem_write(0x10000, image.program_image)
    for register, value in ((UC_X86_REG_CS, 0x239d), (UC_X86_REG_DS, 0x2d56), (UC_X86_REG_ES, 0xa800),
                            (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00),
                            (UC_X86_REG_AX, left & 65535), (UC_X86_REG_BX, top & 65535), (UC_X86_REG_DX, cel * 256)):
        u.reg_write(register, value)
    u.mem_write(0x8ff00, struct.pack('<H', 0xf000))
    u.emu_start(0x239d0 + 0x3620, 0x239d0 + 0xf000, count=1000)
    if u.reg_read(UC_X86_REG_IP) != 0xf000:
        raise ValueError('original pellet writer did not return')
    plane = bytes(u.mem_read(0xa8000, 16000))
    return bytes(15 if byte & (0x80 >> bit) else 0 for byte in plane for bit in range(8))


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
    # Fixed, aimed, spread, ring and randomized families, including the byte
    # cursor seam. These are group inputs, not a whole-frame combat model.
    cases = [(0, 0, 32, 64, 0, 0), (1, 0, 32, 0, 0, 0), (2, 0, 32, 64, 1, 0),
             (11, 0, 48, 240, 2, 0), (15, 0, 64, 64, 2, 0), (25, 0, 80, 0, 4, 0),
             (32, 0, 48, 0, 3, 0), (37, 0, 32, 0, 31, 0), (41, 0, 32, 0, 7, 0),
             (38, 7, 32, 240, 6, 0), (44, 48, 64, 8, 20, 0), (34, 0, 32, 48, 1, 0),
             (28, 8, 128, 7, 8, 255), (29, 0, 24, 0, 0, 255),
             (13, 0, 48, 241, 0, 0), (25, 0, 80, 0, 0, 0)]
    for case in cases:
        reply = subprocess.check_output([str(args.native_checks.resolve()), '--bullet-group', *map(str, case)], text=True)
        native = list(map(int, reply.split()))
        expected = original(image, *case)
        if native != expected:
            raise ValueError(f'bullet group={case}: native={native}, original={expected}')
    spawns = [(2, 11, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0),
              (7, 38, 7, 120, 64, 1, 24, 1, 47, 255, 0, 0),
              (3, 29, 0, 24, 0, 0, 8, 0, 0, 255, 3, -4),
              (3, 0, 0, 32, 8, 1, 0, 0, 0, 9, -4, 3),
              (4, 29, 0, 16, 0, 1, 24, 0, 0, 255, 0, 0),
              (8, 34, 0, 250, 48, 0, 24, 0, 0, 0, 0, 0)]
    for case in spawns:
        kind, group, count, speed, angle, pid, base_speed, trail, trail_cursor, cursor, fg0, fg1 = case
        native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--bullet-spawn', *map(str, case)], text=True).split()))
        expected = original(image, group, count, speed, angle, 0, cursor,
                            (kind, pid, base_speed, trail, trail_cursor, fg0, fg1))
        if native != expected:
            index = next(i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1])
            raise ValueError(f'bullet spawn={case}, index={index}: native={native[index]}, original={expected[index]}')
    updates = [(spawns[0], 80, 0), (spawns[1], 160, 0), (spawns[2], 200, 0),
               (spawns[3], 200, 0), (spawns[4], 20, 0),
               ((1, 0, 0, 24, 64, 0, 0, 0, 0, 0, 0, 0), 80, 1),
               ((1, 0, 0, 24, 64, 0, 0, 0, 0, 0, 0, 0), 8, 4),
               (spawns[0], 4, 2), (spawns[1], 4, 3)]
    for case, ticks, policy in updates:
        kind, group, count, speed, angle, pid, base_speed, trail, trail_cursor, cursor, fg0, fg1 = case
        native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--bullet-run',
                                                       *map(str, case), str(ticks), str(policy)], text=True).split()))
        expected = original(image, group, count, speed, angle, 0, cursor,
                            (kind, pid, base_speed, trail, trail_cursor, fg0, fg1), (ticks, policy))
        if native != expected:
            index = next(i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1])
            raise ValueError(f'bullet update={case}, ticks={ticks}, policy={policy}, index={index}: native={native[index]}, original={expected[index]}')
    pellets = [(22, 20, 1), (30, 20, 1), (7, 0, 0), (15, 0, 0), (-9, 0, 1)]
    for case in pellets:
        native = subprocess.check_output([str(args.native_checks.resolve()), '--pellet', *map(str, case)])
        if native != original_pellet(image, *case):
            raise ValueError(f'complete pellet raster differs from original: {case}')
    print(f'{len(pellets)} complete pellet rasters agree, including authored preshift dots and the narrow-write path.')
    print(f'{len(updates)} bullet update cases agree, including cloud/transfer, trails, acceleration, clearing and complete collision maps.')
    print(f'{len(spawns)} complete bullet pools/trail rings agree, including transfer coordinates and speed restoration.')
    print(f'{len(cases)} bullet group velocities, completion flags and ring cursor states agree with original MAIN.')


if __name__ == '__main__':
    main()
