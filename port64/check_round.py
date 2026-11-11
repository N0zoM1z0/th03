#!/usr/bin/env python3
"""Compare portable round initialization with original MAIN instructions.

Runs the actual initializer, LCG, backward ring fill and formation randomizer.
Unrelated object pools/resetters are bounded foreign services. The randomizer's
uninitialized first previous byte is supplied as its attested cold value 5Eh.
"""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import tomllib


def original(image, count, seed, rank, mode, round_id, credits, stage):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE
    from unicorn.x86_const import (UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS,
                                  UC_X86_REG_ES, UC_X86_REG_SS, UC_X86_REG_IP)
    load, ds, ss, sp = 0x1000, 0x2d56, 0x8000, 0xff00
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + load) & 65535)
    u.mem_write(load * 16, bytes(program))
    # Keep initialized safety tables, clear BSS and choose controlled input state.
    u.mem_write(ds * 16 + 0x3283, bytes([round_id]))
    u.mem_write(ds * 16 + 0x1d90, struct.pack('<HH', 0, 0x6000))
    u.mem_write(ds * 16 + 0x312, struct.pack('<I', seed))
    u.mem_write(ds * 16 + 0x1ff6, struct.pack('<HH', 0x6400, 0x6600))
    u.mem_write(ds * 16 + 0x1ffc, bytes([count]))
    u.mem_write(ds * 16 + 0x2d56, bytes([3, 5]))
    u.mem_write(ds * 16 + 0x6614, struct.pack('<H', 777))
    u.mem_write(ds * 16 + 0x6694, struct.pack('<H', 888))
    for offset, value in ((0xb, rank), (0xc, 5), (0xd, 13), (0xe, 0), (0xf, 1),
                          (0x28, mode), (0x33, stage), (0x36, credits)):
        u.mem_write(0x60000 + offset, bytes([value]))
    for register, value in ((UC_X86_REG_SP, sp), (UC_X86_REG_CS, load + 0x96e),
                            (UC_X86_REG_DS, ds), (UC_X86_REG_ES, ds), (UC_X86_REG_SS, ss)):
        u.reg_write(register, value)
    u.mem_write(ss * 16 + sp, struct.pack('<H', 0x100))
    skipped = {0xe313: False, 0x17384: True, 0x14a76: True, 0x153bb: True,
               0x142d0: True, 0x1b653: True, 0x193bc: True}
    stopped = False

    def hook(uc, address, size, unused):
        nonlocal stopped
        relative = address - load * 16
        if address == (load + 0x96e) * 16 + 0x100:
            stopped = True
            uc.emu_stop()
        elif relative == 0x13d9c:
            # ENTER pushes BP then reserves two bytes. [BP-2] is SP-4 here.
            stack = uc.reg_read(UC_X86_REG_SP)
            uc.mem_write(ss * 16 + stack - 4, b'\x5e')
        elif relative in skipped:
            far = skipped[relative]
            stack = uc.reg_read(UC_X86_REG_SP)
            ip = struct.unpack('<H', uc.mem_read(ss * 16 + stack, 2))[0]
            cs = struct.unpack('<H', uc.mem_read(ss * 16 + stack + 2, 2))[0] if far else uc.reg_read(UC_X86_REG_CS)
            uc.reg_write(UC_X86_REG_SP, stack + (4 if far else 2))
            uc.reg_write(UC_X86_REG_CS, cs)
            uc.reg_write(UC_X86_REG_IP, ip)

    u.hook_add(UC_HOOK_CODE, hook)
    u.emu_start(load * 16 + 0x9ebf, 0, count=100000)
    if not stopped:
        raise ValueError('original round initializer did not return')
    data = bytes(u.mem_read(ds * 16, 65536))
    word = lambda at: struct.unpack_from('<H', data, at)[0]
    rows = [[count, struct.unpack_from('<I', data, 0x312)[0], data[0x6598], data[0x68dc],
             data[0x1e3e], data[0x2d56], data[0x2d57], word(0x6614), word(0x6694)],
            list(data[0x1e52:0x1f52]), list(u.mem_read(0x64000, 256)), list(u.mem_read(0x66000, 256))]
    for pid in range(2):
        base = 0x65a6 + pid * 128
        rows.append([word(base), word(base + 2)] +
                    [data[base + offset] for offset in (6, 7, 8, 0x15, 0xd)] +
                    [word(base + 0x18)] +
                    [data[base + offset] for offset in (0x22, 0x73, 0x1c, 0x1d, 0x1f, 0x1e)] +
                    [word(base + 0x74)])
        rows.append(list(data[base + 0x24:base + 0x64]))
    return rows


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
    # Normal play, byte wrap and later-stage safety saturation. No invalid rank
    # or negative original table index is required for the portable game path.
    cases = [(0, 0, 1, 0, 3, 0), (1, 1, 1, 1, 2, 4), (0xffffffff, 2, 1, 4, 3, 8),
             (500, 3, 1, 0, 3, 8), (3200, 0, 0x80, 16, 3, 0), (600, 3, 0x81, 0, 3, 0)]
    with tempfile.TemporaryDirectory(prefix='th03-round-') as work:
        enedat = Path(work) / 'ENEDAT.DAT'
        subprocess.run([str(args.native.resolve()), '--hdi', str(root / '.analysis/runtime/images/zun.hdi'),
                        '--main-assets', '--extract', 'ENEDAT.DAT', '--output', str(enedat)], check=True)
        for case in cases:
            reply = subprocess.check_output([str(args.native_checks.resolve()), '--round', str(enedat),
                                             *map(str, case)], text=True)
            native = [list(map(int, line.split())) for line in reply.splitlines()]
            expected = original(image, native[0][0], *case)
            if native != expected:
                for row, (actual, want) in enumerate(zip(native, expected)):
                    if actual != want:
                        index = next(i for i, pair in enumerate(zip(actual, want)) if pair[0] != pair[1])
                        raise ValueError(f'case={case}, row={row}, index={index}: native={actual[index]}, original={want[index]}')
    print(f'{len(cases)} original MAIN round cases agree: scalar state, player thresholds, LCG, backward ring and formation rings.')


if __name__ == '__main__':
    main()
