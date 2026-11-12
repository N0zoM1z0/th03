#!/usr/bin/env python3
"""Compare rendered-frame combo expiry and deferred scoring with original MAIN."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def original(image, ticks):
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
    u.mem_write(ds + 0x393e, struct.pack('<BBHBBH', 80, 42, 65535, 80, 7, 1234))
    u.mem_write(ds + 0x4b64, bytes(16))
    graphics = {0x1128c: 8, 0x112d0: 10, 0x12024: 8, 0x196e0 + 0x3f28: 8}

    def hook(uc, address, size, unused):
        if address not in graphics:
            return
        sp = uc.reg_read(UC_X86_REG_SP)
        ip, cs = struct.unpack('<HH', uc.mem_read(0x80000 + sp, 4))
        uc.reg_write(UC_X86_REG_SP, sp + 4 + graphics[address])
        uc.reg_write(UC_X86_REG_CS, cs)
        uc.reg_write(UC_X86_REG_IP, ip)

    u.hook_add(UC_HOOK_CODE, hook)
    out = []
    for tick in range(ticks):
        u.mem_write(ds + 0x6596, struct.pack('<H', tick & 65535))
        for reg, value in ((UC_X86_REG_CS, 0x239d), (UC_X86_REG_DS, 0x2d56),
                           (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
            u.reg_write(reg, value)
        u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, 0x239d))
        u.emu_start(0x239d0 + 0x2383, 0x329d0, count=100000)
        if u.reg_read(UC_X86_REG_IP) != 0xf000:
            raise ValueError('original combo owner did not return')
        for pid in range(2):
            out.extend(struct.unpack('<BBH', u.mem_read(ds + 0x393e + pid * 4, 4)))
            out.extend(u.mem_read(ds + 0x4b64 + pid * 8, 8))
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
    native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--combo', '90'], text=True).split()))
    expected = original(parse_mz(raw), 90)
    if native != expected:
        index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
        raise ValueError(f'combo index={index}: native={native[index:index + 10]}, original={expected[index:index + 10]}')
    print('Both complete 80-frame combos, expiry, reset and deferred BCD score awards agree with original MAIN.')


if __name__ == '__main__':
    main()
