#!/usr/bin/env python3
"""Compare defensive/offensive CPU movement and real Bomb activation with MAIN."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def original(image, fixture):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_SS, UC_X86_REG_IP
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    ds, pid = 0x2d560, fixture & 1
    for at, size in ((0x65a6, 256), (0x4ba0, 6624), (0x3ed6, 3072), (0x1dc6, 8),
                     (0x38e4, 8), (0x3ece, 4), (0x6580, 2), (0x6586, 2), (0x658b, 2)):
        u.mem_write(ds + at, bytes(size))
    put = lambda at, value, size=1: u.mem_write(ds + at, int(value).to_bytes(size, 'little'))
    player = 0x65a6 + pid * 128
    u.mem_write(ds + player, struct.pack('<hh', 2304, 5376))
    put(player + 8, 1)
    put(player + 0x16, int(fixture == 7))
    put(player + 0x18, 2048 if fixture in (3, 5) else 0, 2)
    put(player + 0x1d, 2)
    put(player + 0x6e, 0 if fixture in (0, 4, 5) else 1000, 2)
    put(player + 0x74, 1, 2)
    put(0x6588, player, 2)
    put(0x6590, pid)
    put(0x6596, 4, 2)
    u.mem_write(ds + 0x6582, bytes((64, 64, 48, 48)))
    u.mem_write(ds + 0x1e52, bytes((i * 13 + 7) & 255 for i in range(256)))
    put(0x1f52, 0)
    u.mem_write(ds + 0x1d90, struct.pack('<HH', 0, 0x6000))
    u.mem_write(0x60038, bytes([70]))
    if fixture in (1, 7):
        put(0x4ba0 + pid * 3312 + 9 * 184 + 144, 0x80)
    if 2 <= fixture <= 5:
        u.mem_write(ds + 0x4ba0 + pid * 3312, bytes([255] * 3312))
    if fixture == 6:
        put(0x1dca + pid * 2, 1, 2)
        u.mem_write(ds + 0x1dc6, struct.pack('<hh', 3000, 2000))

    def hook(uc, address, size, unused):
        if address != 0x196e0 + 0x22cb:
            return
        sp = uc.reg_read(UC_X86_REG_SP)
        ip, cs = struct.unpack('<HH', uc.mem_read(0x80000 + sp, 4))
        uc.reg_write(UC_X86_REG_SP, sp + 6)  # PUSH CS/CALL-near retains the far Pascal ABI
        uc.reg_write(UC_X86_REG_CS, cs)
        uc.reg_write(UC_X86_REG_IP, ip)

    u.hook_add(UC_HOOK_CODE, hook)
    for reg, value in ((UC_X86_REG_CS, 0x196e), (UC_X86_REG_DS, 0x2d56),
                       (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
        u.reg_write(reg, value)
    u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, player))
    u.emu_start(0x196e0 + 0x2e6a, 0x286e0, count=500000)
    if u.reg_read(UC_X86_REG_IP) != 0xf000:
        raise ValueError(f'original CPU {fixture} did not return: CS={u.reg_read(UC_X86_REG_CS):04x} IP={u.reg_read(UC_X86_REG_IP):04x} SP={u.reg_read(UC_X86_REG_SP):04x}')
    b = bytes(u.mem_read(ds, 65536))
    word = lambda at: struct.unpack_from('<h', b, at)[0]
    out = [word(player), word(player + 2), b[player + 4], *struct.unpack_from('<bb', b, 0x6586),
           b[player + 0x16], word(0x38e4), word(0x38e6), word(0x38ea), word(0x3ece), word(0x3ed0),
           b[0x38e8], b[0x1f52], b[0x6580 + pid], b[player + 0x1d], b[player + 6], b[player + 0x1e],
           b[0x658b + pid], u.mem_read(0x60038, 1)[0]]
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
    for fixture in range(8):
        native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--cpu', str(fixture)], text=True).split()))
        expected = original(image, fixture)
        if native != expected:
            raise ValueError(f'CPU {fixture}: native={native}, original={expected}')
    print('CPU aim, wide/close scans, dodge/retry grids, RNG, stuck Bomb and charge-preserving hit state match original MAIN')


if __name__ == '__main__':
    main()
