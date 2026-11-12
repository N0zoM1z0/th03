#!/usr/bin/env python3
"""Check round-loop clocks and page cadence against the original scheduler.

The original loop runs its actual branches, counters and hardware page writes.
Foreign gameplay/drawing calls are skipped here: their real portable owners run
in the native fixture, and have separate original-instruction comparisons.
"""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def original(image, first, ticks, timing):
    from capstone import Cs, CS_ARCH_X86, CS_MODE_16
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INSN
    from unicorn.x86_const import UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_SS, UC_X86_REG_IP, UC_X86_INS_OUT
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    ds = 0x2d560
    for at in (0x1a9a, 0x38dc, 0x65a0):
        u.mem_write(ds + at, bytes(2))
    u.mem_write(ds + 0x658e, bytes((0, 1)))
    u.mem_write(ds + 0x6592, struct.pack('<IHBBB', first, first, 126, 1, timing))
    for at, damage, frame in ((0x65a6, 5, 777), (0x6626, 2, 888)):
        u.mem_write(ds + at + 0x73, struct.pack('<BH', damage, frame))
    code = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(image.program_image[0x9778:0x9ad6], 0x9778))
    calls = {i.address: i for i in code if i.mnemonic in ('call', 'lcall')}
    cleanups = {0x9824: 4, 0x9833: 4, 0x984e: 2, 0x9855: 2,
                0x98e5: 2, 0x98f0: 2, 0x9900: 2, 0x990b: 2,
                0x996c: 2, 0x99aa: 2, 0x99be: 2, 0x99c5: 2, 0x9a41: 4, 0x9a52: 4}
    for before, instruction in zip(code, code[1:]):
        if before.mnemonic == 'push' and before.op_str == 'cs' and instruction.address in calls:
            cleanups[instruction.address] = cleanups.get(instruction.address, 0) + 2
    draws = 0

    def hook(uc, address, size, unused):
        off = address - 0x10000
        if off == 0x977e:
            if uc.reg_read(UC_X86_REG_SP) != 0xfefe:
                raise ValueError('scheduler service cleanup changed SP')
            frame = struct.unpack('<I', uc.mem_read(ds + 0x6592, 4))[0]
            if frame == first + ticks:
                uc.emu_stop()
                return
        if off in (0x99e4, 0x9a09):
            uc.mem_write(ds + 0x11ea, b'\xff\xff')
        if off in calls:
            uc.reg_write(UC_X86_REG_SP, uc.reg_read(UC_X86_REG_SP) + cleanups.get(off, 0))
            uc.reg_write(UC_X86_REG_IP, off - 0x96e0 + calls[off].size)

    def out(uc, port, size, value, unused):
        nonlocal draws
        if port == 0xa6:
            draws += 1

    u.hook_add(UC_HOOK_CODE, hook)
    u.hook_add(UC_HOOK_INSN, out, None, 1, 0, UC_X86_INS_OUT)
    for reg, value in ((UC_X86_REG_CS, 0x196e), (UC_X86_REG_DS, 0x2d56),
                       (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
        u.reg_write(reg, value)
    u.emu_start(0x19778, 0x286e0, count=200000)
    b = bytes(u.mem_read(ds, 65536))
    if struct.unpack_from('<I', b, 0x6592)[0] != first + ticks:
        raise ValueError('original scheduler did not reach the requested frame')
    word = lambda at: struct.unpack_from('<H', b, at)[0]
    return [struct.unpack_from('<I', b, 0x6592)[0], word(0x6596), b[0x6598], b[0x6619], b[0x6699], word(0x661a), word(0x669a), draws, b[0x658e]]


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
    disk = root / '.analysis/runtime/images/zun.hdi'
    # Windows data paths are accepted through the usual WSL interop mapping.
    if args.native_checks.suffix == '.exe':
        disk = subprocess.check_output(['wslpath', '-w', str(disk)], text=True).strip()
    for case in ((0, 66, 0), (1000, 64, 0), (65490, 60, 0), (0, 66, 1), (1000, 64, 1)):
        native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--loop-clock', str(disk), *map(str, case)], text=True).split()))
        expected = original(image, *case)
        if native != expected:
            raise ValueError(f'loop cadence {case}: native={native}, original={expected}')
        print(f'Original round-loop counters, speed/recovery/CPU gates and page cadence agree: {case}', flush=True)
    for control in ('flash', 'pause', 'wait'):
        subprocess.run([str(args.native_checks.resolve()), '--loop-control', str(disk), control], check=True)


if __name__ == '__main__':
    main()
