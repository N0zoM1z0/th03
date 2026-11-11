#!/usr/bin/env python3
"""Compare both background chains and indeterminate-phase equivalence with MAIN."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def original(image, chain, acceleration, first, count, reset, changed):
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
    u.mem_write(ds + 0x39cc, bytes(1280))
    u.mem_write(ds + 0x312, struct.pack('<I', 0x12345678))
    init, accel, periodic = (0x39b2, 0x3a55, 0x3b07) if chain == 1 else (0x3c08, 0x3c60, 0x3d19)
    u.mem_write(ds + 0x39c4, struct.pack('<HH', accel, 0x196e))
    hardware = {0x10f5c: 4, 0x10f86: 0, 0x10704: 0, 0x1071a: 0, 0x1e8f0 + 0x810: 6, 0x1e8f0 + 0x8e2: 6}

    def hook(uc, address, size, unused):
        sp = uc.reg_read(UC_X86_REG_SP)
        if address in (0x196e0 + 0x3b07, 0x196e0 + 0x3d19):
            uc.mem_write(0x80000 + sp - 5, bytes([changed]))
        if address == 0x196e0 + 0x3951:
            ip = struct.unpack('<H', uc.mem_read(0x80000 + sp, 2))[0]
            uc.reg_write(UC_X86_REG_SP, sp + 2)
            uc.reg_write(UC_X86_REG_IP, ip)
        elif address in hardware:
            ip, cs = struct.unpack('<HH', uc.mem_read(0x80000 + sp, 4))
            uc.reg_write(UC_X86_REG_SP, sp + 4 + hardware[address])
            uc.reg_write(UC_X86_REG_CS, cs)
            uc.reg_write(UC_X86_REG_IP, ip)

    u.hook_add(UC_HOOK_CODE, hook)

    def call(offset):
        for reg, value in ((UC_X86_REG_CS, 0x196e), (UC_X86_REG_DS, 0x2d56),
                           (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
            u.reg_write(reg, value)
        u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, 0x196e))
        u.emu_start(0x196e0 + offset, 0x286e0, count=100000)
        if u.reg_read(UC_X86_REG_IP) != 0xf000:
            raise ValueError(f'original background {offset:04x} did not return')

    call(init)
    last_periodic, phase = False, 0

    def update(frame):
        nonlocal last_periodic, phase
        u.mem_write(ds + 0x6592, struct.pack('<I', frame))
        u.mem_write(ds + 0x6596, struct.pack('<H', frame & 65535))
        offset = struct.unpack('<H', u.mem_read(ds + 0x39c4, 2))[0]
        last_periodic, phase = offset == periodic, frame % 4096
        call(offset)

    for frame in range(acceleration):
        update(frame)
    if reset:
        call(0x397d)
    for frame in range(first, first + count):
        update(frame)
    b = bytes(u.mem_read(ds, 65536))
    out = [struct.unpack_from('<I', b, 0x312)[0], b[0x3ecc], struct.unpack_from('<H', b, 0x39c4)[0] == periodic, last_periodic, phase]
    for i in range(80):
        at = 0x39cc + i * 16
        out.extend((*struct.unpack_from('<hhhh', b, at), b[at + 8], *struct.unpack_from('<Hh', b, at + 10)))
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
    for chain in (1, 2):
        accel = 130 if chain == 1 else 146
        cases = ((0, 0, 0, 0), (accel, 0, 0, 0), (accel, 1016, 24, 0),
                 (accel, 2040, 24, 0), (accel, 3068, 16, 0), (accel, 4056, 48, 0), (accel, 1024, 16, 1))
        for acceleration, first, count, reset in cases:
            case = chain, acceleration, first, count, reset
            native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--background', *map(str, case)], text=True).split()))
            for changed in (0, 127):
                expected = original(image, *case, changed)
                if native != expected:
                    index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
                    raise ValueError(f'background {case}, changed={changed}, index={index}: native={native[index:index + 5]}, original={expected[index:index + 5]}')
    print('Both background chains match original MAIN: all80 slots, LCG, acceleration, turn phases and velocity reset; both incoming changed-byte branches agree')


if __name__ == '__main__':
    main()
