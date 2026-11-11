#!/usr/bin/env python3
"""Compare original round-introduction updates and render-side state changes."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def original(image, seed, mode, ticks, cursor):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE
    from unicorn.x86_const import (UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS,
                                  UC_X86_REG_ES, UC_X86_REG_SS, UC_X86_REG_IP)
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    ds = 0x2d560
    u.mem_write(ds + 0x1d90, struct.pack('<HH', 0, 0x6000))
    u.mem_write(0x60028, bytes([mode]))
    u.mem_write(ds + 0x3282, b'\x01')
    u.mem_write(ds + 0x3284, bytes(1280))
    u.mem_write(ds + 0x3786, bytes(8))
    u.mem_write(ds + 0x312, struct.pack('<I', seed))
    u.mem_write(ds + 0x1e52, bytes((i * 13 + 7) & 255 for i in range(256)))
    u.mem_write(ds + 0x1f52, bytes([cursor]))
    for register, value in ((UC_X86_REG_CS, 0x196e), (UC_X86_REG_DS, 0x2d56),
                            (UC_X86_REG_ES, 0x2d56), (UC_X86_REG_SS, 0x8000)):
        u.reg_write(register, value)
    stopped = False

    def hook(uc, address, size, unused):
        nonlocal stopped
        if address == 0x196e0 + 0x100:
            stopped = True
            uc.emu_stop()
        elif address == 0x10000 + 0x26ca:  # SUPER_PUT far Pascal, three WORDs
            sp = uc.reg_read(UC_X86_REG_SP)
            ip, cs = struct.unpack('<HH', uc.mem_read(0x80000 + sp, 4))
            uc.reg_write(UC_X86_REG_SP, sp + 10)
            uc.reg_write(UC_X86_REG_CS, cs)
            uc.reg_write(UC_X86_REG_IP, ip)

    u.hook_add(UC_HOOK_CODE, hook)
    rows = []
    for _ in range(ticks):
        for entry in (0x2432, 0x277d):
            u.mem_write(0x8ff00, struct.pack('<H', 0x100))
            u.reg_write(UC_X86_REG_SP, 0xff00)
            u.reg_write(UC_X86_REG_IP, entry)
            stopped = False
            u.emu_start(0x196e0 + entry, 0, count=100000)
            if not stopped:
                raise ValueError('original HUD update/render did not return')
        b = bytes(u.mem_read(ds, 65536))
        row = [b[0x3282], b[0x3786], *struct.unpack_from('<hhh', b, 0x3788),
               struct.unpack_from('<I', b, 0x312)[0], b[0x1f52]]
        for i in range(128):
            row.extend(struct.unpack_from('<hhhBBBB', b, 0x3284 + i * 10))
        rows.append(row)
    return rows


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
    for seed, mode, cursor in ((0, 1, 0), (0xffffffff, 0x81, 255)):
        ticks = 260
        reply = subprocess.check_output([str(args.native_checks.resolve()), '--hud-intro',
                                         *map(str, (seed, mode, ticks, cursor))], text=True)
        native = [list(map(int, line.split())) for line in reply.splitlines()]
        expected = original(image, seed, mode, ticks, cursor)
        for frame, (actual, want) in enumerate(zip(native, expected)):
            if actual != want:
                index = next(i for i, pair in enumerate(zip(actual, want)) if pair[0] != pair[1])
                raise ValueError(f'mode={mode}, frame={frame}, index={index}: native={actual[index]}, original={want[index]}')
    print('Story/versus introductions agree for 520 frames: slide/banner state, all128 particles, seed and ring cursor.')


if __name__ == '__main__':
    main()
