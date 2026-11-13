#!/usr/bin/env python3
"""Check player sprite pixels through original BFNT, atlas preparation and draw calls."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import tomllib
from check_collision import console_startup


def original(image, banks, center_y=336):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_INTR, UC_HOOK_MEM_WRITE, UC_HOOK_INSN
    from unicorn.x86_const import (UC_X86_REG_AX, UC_X86_REG_BX, UC_X86_REG_CS, UC_X86_REG_CX,
                                  UC_X86_REG_DI, UC_X86_REG_DS, UC_X86_REG_DX, UC_X86_REG_EFLAGS,
                                  UC_X86_REG_IP, UC_X86_REG_SP, UC_X86_REG_SS, UC_X86_INS_OUT)
    u = Uc(UC_ARCH_X86, UC_MODE_16);u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        value = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (value + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program));console_startup(u, image)
    state = {'cursor': 0, 'segment': 0x7000, 'file': b''}

    def dos(uc, number, unused):
        ax = uc.reg_read(UC_X86_REG_AX);ah = ax >> 8
        if number != 0x21:
            raise ValueError(f'unexpected BFNT interrupt {number:02x}/{ax:04x}')
        uc.reg_write(UC_X86_REG_EFLAGS, uc.reg_read(UC_X86_REG_EFLAGS) & ~1)
        if ah == 0x3f:
            if uc.reg_read(UC_X86_REG_BX) != 7:
                raise ValueError('BFNT requested an undeclared file handle')
            count = uc.reg_read(UC_X86_REG_CX)
            data = state['file'][state['cursor']:state['cursor'] + count];state['cursor'] += len(data)
            uc.mem_write(uc.reg_read(UC_X86_REG_DS) * 16 + uc.reg_read(UC_X86_REG_DX), data)
            uc.reg_write(UC_X86_REG_AX, len(data))
        elif ah == 0x48:
            segment = state['segment'];paragraphs = uc.reg_read(UC_X86_REG_BX)
            available = 0xa000 - segment
            if paragraphs > available:
                uc.reg_write(UC_X86_REG_AX, 8);uc.reg_write(UC_X86_REG_BX, available)
                uc.reg_write(UC_X86_REG_EFLAGS, uc.reg_read(UC_X86_REG_EFLAGS) | 1);return
            state['segment'] += paragraphs + 1
            uc.mem_write((segment - 1) * 16, b'M' + struct.pack('<HH', 0xff0, paragraphs) + bytes(11))
            uc.reg_write(UC_X86_REG_AX, segment)
        elif ah not in (0x49, 0x4a):
            raise ValueError(f'unexpected BFNT DOS service {ax:04x}')
    dos_hook = u.hook_add(UC_HOOK_INTR, dos)

    def call(segment, offset, arguments=(), far=True):
        for reg, value in ((UC_X86_REG_DS, 0x2d56), (UC_X86_REG_CS, segment + 0x1000),
                           (UC_X86_REG_IP, offset), (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
            u.reg_write(reg, value)
        ret = (0xf000, 0x239d) if far else (0xf000,)
        u.mem_write(0x8ff00, struct.pack('<' + 'H' * (len(ret) + len(arguments)), *ret, *reversed(arguments)))
        u.emu_start((segment + 0x1000) * 16 + offset,
                    0x329d0 if far else (segment + 0x1000) * 16 + 0xf000, count=2000000)
        if u.reg_read(UC_X86_REG_IP) != 0xf000:
            raise ValueError('original player graphics owner did not return')
    for bank in banks:
        if bank[:5] != b'BFNT\x1a' or struct.unpack_from('<4H', bank, 8) != (32, 32, 0, 8):
            raise ValueError('original normal-pose bank geometry changed')
        if struct.unpack_from('<H', bank, 28)[0] != 0:
            raise ValueError('normal-pose bank needs extension analysis')
        state['file'] = bank;state['cursor'] = 32 + (48 if bank[5] & 128 else 0)
        u.mem_write(0x60000, bank[:32]);call(0, 0x286, (7, 0x6000, 0, 0))
        if u.reg_read(UC_X86_REG_AX) != 0 or state['cursor'] != len(bank):
            raise ValueError('original BFNT/pattern allocation did not consume its bank')
    if int.from_bytes(u.mem_read(0x2d560 + 0x5d8, 2), 'little') != 18:
        raise ValueError('original BFNT pattern count differs')

    # SUPER_PUT runs its original planar GRCG masks into the lower 200 rows.
    planes = [bytearray(32000) for _ in range(4)]
    grcg = {'mode': 0, 'index': 0, 'tiles': [0, 0, 0, 0]}

    def out(uc, port, size, value, unused):
        if port == 0x7c:
            grcg['mode'] = value
        elif port == 0x7e:
            grcg['tiles'][grcg['index']] = value;grcg['index'] = (grcg['index'] + 1) % 4
    u.hook_add(UC_HOOK_INSN, out, None, 1, 0, UC_X86_INS_OUT)

    def write(uc, access, address, size, value, unused):
        if not grcg['mode'] & 0x80:
            return
        for i in range(size):
            at = address + i - 0xa8000
            if not 0 <= at < 32000:
                continue
            mask = (value >> (i * 8)) & 255
            for plane in range(4):
                if not grcg['mode'] & (1 << plane):
                    planes[plane][at] = (planes[plane][at] & ~mask) | (grcg['tiles'][plane] & mask)
    u.hook_add(UC_HOOK_MEM_WRITE, write, begin=0xa8000, end=0xaffff)
    call(0x96e, 0x4b86, far=False)  # stage_prepare_shot_sprites, both hardware pages.
    u.hook_del(dos_hook)
    draws = []

    def sprite16(uc, number, unused):
        ax = uc.reg_read(UC_X86_REG_AX)
        if number != 0x42 or ax >> 8 != 2:
            raise ValueError('original player requested an unexpected device service')
        left, top = uc.reg_read(UC_X86_REG_DX), uc.reg_read(UC_X86_REG_BX)
        if top >= 32768:
            top -= 65536
        source = uc.reg_read(UC_X86_REG_DI);height = uc.reg_read(UC_X86_REG_CX) & 255;width = (ax & 255) * 16
        draws.append((left, top, source, width, height))
        if left + width > 640 or left % 16:
            raise ValueError('player device fixture requires an aligned sprite')
        # The original resident's vertical clip advances the source for
        # negative Y; its other branch clips a nonnegative sprite's bottom.
        if top < 0:
            source -= top * 80;height += top;top = 0
        else:
            height = min(height, 200 - top)
        for y in range(height):
            for x in range(width):
                at = 16000 + source + y * 80 + x // 8;mask = 128 >> (x % 8)
                color = sum(1 << p for p in range(4) if planes[p][at] & mask)
                if color:
                    destination = (top + y) * 80 + (left + x) // 8;bit = 128 >> ((left + x) % 8)
                    for plane in range(4):
                        planes[plane][destination] = (planes[plane][destination] & ~bit) | (bit if color & (1 << plane) else 0)
    u.hook_add(UC_HOOK_INTR, sprite16)
    result = []
    for image_index in range(9):
        for plane in planes:
            plane[:16000] = bytes(16000)
        draws.clear()
        for pid in range(2):
            player = 0x65a6 + pid * 128;data = bytearray(128)
            struct.pack_into('<hh', data, 0, 2304, center_y * 16);data[0xe] = image_index // 3;data[0xf] = image_index % 3
            u.mem_write(0x2d560 + player, bytes(data));u.mem_write(0x2d560 + 0x6590, bytes([pid]))
            call(0x96e, 0x47b5, (player,), far=False)
        call(0, 0x71a)  # EGC_OFF before the overlay pass.
        for pid in range(2):
            u.mem_write(0x2d560 + 0x6590, bytes([pid]));call(0x96e, 0x4838, (0x65a6 + pid * 128,), far=False)
        if len(draws) != (2 if image_index % 3 == 0 else 0):
            raise ValueError('original normal player draw count changed')
        pixels = bytearray(128000)
        for at in range(16000):
            for bit in range(8):
                mask = 128 >> bit
                pixels[at * 8 + bit] = sum(1 << p for p in range(4) if planes[p][at] & mask)
        result.append(bytes(pixels))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', required=True, type=Path)
    parser.add_argument('--native-checks', required=True, type=Path)
    parser.add_argument('--dos-root', required=True, type=Path)
    parser.add_argument('--character', type=int, choices=range(9))
    args = parser.parse_args();root = args.dos_root.resolve()
    cfg = tomllib.loads((root / 'config/targets.toml').read_text());target = next(x for x in cfg['artifacts'] if x['id'] == 'th03-main')
    raw = (root / target['private_path']).read_bytes();disk = root / '.analysis/runtime/images/zun.hdi'
    if hashlib.sha256(raw).hexdigest() != target['sha256'] or hashlib.sha256(disk.read_bytes()).hexdigest() != cfg['source']['hdi_sha256']:
        raise ValueError('original MAIN/HDI identity changed')
    sys.path.insert(0, str(root / 'scripts'));from lib.pc98 import parse_mz
    image = parse_mz(raw);native, checks = args.native.resolve(), args.native_checks.resolve()
    def path(p, binary):
        return subprocess.check_output(['wslpath', '-w', str(p)], text=True).strip() if binary.suffix == '.exe' else str(p)
    with tempfile.TemporaryDirectory(prefix='th03-player-') as temporary:
        work = Path(temporary)
        for character in range(9) if args.character is None else (args.character,):
            banks = []
            for palette in range(2):
                name = f'{character * 2 + palette:02d}CH.BF2';file = work / name
                subprocess.run([str(native), '--hdi', path(disk, native), '--main-assets', '--extract', name, '--output', path(file, native)], check=True)
                banks.append(file.read_bytes())
            for center_y in (336, 11):
                expected = original(image, banks, center_y)
                for image_index in range(9):
                    output = work / 'native.pixels'
                    subprocess.run([str(checks), '--player-sprite', path(disk, checks), str(character * 2 + 1), str(character * 2 + 2), str(image_index), str(center_y), path(output, checks)], check=True)
                    actual = output.read_bytes()
                    if actual != expected[image_index]:
                        differences = [(i % 640, i // 640, a, b) for i, (a, b) in enumerate(zip(actual, expected[image_index])) if a != b]
                        raise ValueError(f'character={character} image={image_index} Y={center_y}: differing dots={len(differences)}, first={differences[:8]}')
                print(f'Character{character} Y={center_y}: both palette banks, three poses and all glow images agree in every pixel with original BFNT/atlas/player calls', flush=True)


if __name__ == '__main__':
    main()
