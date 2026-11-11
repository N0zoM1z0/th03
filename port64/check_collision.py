#!/usr/bin/env python3
"""Compare collision bitmap primitives and ordinary player hit scans with MAIN."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def original(image, kind, pid, x, y, width, height, right, hit):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16
    from unicorn.x86_const import (UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS,
                                  UC_X86_REG_SS, UC_X86_REG_IP)
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    ds = 0x2d560
    u.mem_write(ds + 0x4ba0, bytes(6624))
    u.mem_write(ds + 0x4b8e, struct.pack('<hhhhhhB', x, y, width, height, right, 0, pid))
    for register, value in ((UC_X86_REG_CS, 0x239d), (UC_X86_REG_DS, 0x2d56),
                            (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
        u.reg_write(register, value)
    u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, 0x239d))
    entry = dict(rectangle=0x9e, vertical=0x172, slope=0x1ca)[kind]
    u.emu_start(0x239d0 + entry, 0x239d0 + 0xf000, count=10000)
    if u.reg_read(UC_X86_REG_IP) != 0xf000:
        raise ValueError('original collision writer did not return')
    bitmap = bytes(u.mem_read(ds + 0x4ba0, 6624))
    if not hit:
        return bitmap
    player = bytearray(128)
    struct.pack_into('<hh', player, 0, x, y)
    offset = 0x65a6 + pid * 128
    u.mem_write(ds + offset, bytes(player))
    u.mem_write(ds + 0x6588, struct.pack('<H', offset))
    u.mem_write(ds + 0x6590, bytes([pid]))
    u.mem_write(ds + 0x38e4, bytes(4))
    u.reg_write(UC_X86_REG_CS, 0x196e)
    u.reg_write(UC_X86_REG_SP, 0xff00)
    u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, 4))
    u.emu_start(0x196e0 + 0x4a17, 0x196e0 + 0xf000, count=10000)
    if u.reg_read(UC_X86_REG_IP) != 0xf000:
        raise ValueError('original player hit scan did not return')
    flag = bytes(u.mem_read(ds + offset + 4, 1))[0]
    point = struct.unpack('<hh', u.mem_read(ds + 0x38e4, 4))
    return [flag, *point]


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
    cases = [('rectangle', 0, 2304, 512, 24, 24, 0), ('rectangle', 1, 64, 64, 12, 12, 0),
             ('vertical', 1, 4496, 5856, 1, 8, 0), ('vertical', 0, 2304, 512, 1, 0, 0),
             ('slope', 0, 64, 0, 3, 0, 4000), ('slope', 1, 4000, 0, 7, 0, 64)]
    for case in cases:
        command = [str(args.native_checks.resolve()), '--collmap', *map(str, case)]
        native = subprocess.check_output(command + ['bitmap'])
        if native != original(image, *case, False):
            raise ValueError(f'complete collision bitmap differs: {case}')
        native = list(map(int, subprocess.check_output(command + ['hit'], text=True).split()))
        if native != original(image, *case, True):
            raise ValueError(f'player scan differs: {case}, native={native}, original={original(image, *case, True)}')
    print('Six complete collision bitmaps and player hit scans agree with original MAIN instructions.')


if __name__ == '__main__':
    main()
