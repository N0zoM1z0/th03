#!/usr/bin/env python3
"""Execute MAINL Staff Roll owners against native snow, pages and scheduler.

Only file/graphics/font devices and audio clocks are foreign. CDG loads/blits
use the external original files; snow, transitions, dissolve, verdict selection
and roll control execute the pinned original instructions.
"""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def machine(image):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16
    from unicorn import x86_const as reg
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        value = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (value + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    for register, value in ((reg.UC_X86_REG_CS, 0x195f), (reg.UC_X86_REG_DS, 0x1e3f),
                            (reg.UC_X86_REG_SS, 0x8000), (reg.UC_X86_REG_SP, 0xff00)):
        u.reg_write(register, value)
    u.mem_write(0x8ff00, struct.pack('<H', 0xf000))
    return u


def verdict_calls(image, score, character, rank, skill):
    from unicorn import UC_HOOK_CODE
    from unicorn import x86_const as reg
    u = machine(image)
    u.mem_write(0x1e3f0 + 0x27dc, bytes(score))
    u.mem_write(0x1e3f0 + 0x27e6, bytes((rank, character, skill)))
    calls = []

    def render(uc, address, size, unused):
        sp = uc.reg_read(reg.UC_X86_REG_SP)
        ip, cs, offset, segment, fx, y, x = struct.unpack('<7H', uc.mem_read(0x80000 + sp, 14))
        if fx != 0x2f:
            raise ValueError('original verdict changed its font weight/color')
        text = bytes(uc.mem_read(segment * 16 + offset, 128)).split(b'\0')[0]
        calls.append((x, y, text))
        uc.reg_write(reg.UC_X86_REG_SP, sp + 14)
        uc.reg_write(reg.UC_X86_REG_CS, cs)
        uc.reg_write(reg.UC_X86_REG_IP, ip)

    u.hook_add(UC_HOOK_CODE, render, begin=0x1c7e0 + 0x9b7, end=0x1c7e0 + 0x9b7)
    u.emu_start(0x195f0 + 0x2c98, 0x195f0 + 0xf000, count=10000)
    if u.reg_read(reg.UC_X86_REG_IP) != 0xf000:
        raise ValueError('original verdict did not return')
    return calls


def original(image, resources, native_dir, font_ink, slow, music):
    from unicorn import UC_HOOK_CODE, UC_HOOK_INSN
    from unicorn import x86_const as reg
    u = machine(image)
    ds, stack = 0x1e3f0, 0x80000
    planes = (0xa8000, 0xb0000, 0xb8000, 0xe0000)
    pages = [[bytearray(32000) for _ in planes] for _ in range(2)]
    access = shown = count = color = 0
    trace = bytearray()
    native_trace = (native_dir / "trace.bin").read_bytes()
    font_calls = []
    sounds = []
    snapshots = {int(p.stem): p for p in native_dir.glob('*.pixels') if p.stem.isdecimal()}
    fade_refreshes = 0
    fade_trace = []

    def get(name):
        return u.reg_read(getattr(reg, 'UC_X86_REG_' + name))

    def word(offset):
        return struct.unpack('<H', u.mem_read(ds + offset, 2))[0]

    def returning(clean=0, far=True):
        sp = get('SP')
        frame = struct.unpack('<2H' if far else '<H', u.mem_read(stack + sp, 4 if far else 2))
        u.reg_write(reg.UC_X86_REG_SP, sp + (4 if far else 2) + clean)
        if far:
            u.reg_write(reg.UC_X86_REG_CS, frame[1])
        u.reg_write(reg.UC_X86_REG_IP, frame[0])

    def args(n):
        return struct.unpack('<' + 'H' * n, u.mem_read(stack + get('SP') + 4, n * 2))

    def text(segment, offset):
        return bytes(u.mem_read(segment * 16 + offset, 128)).split(b'\0')[0]

    def pixels():
        out = bytearray(640 * 400 * 2)
        for page in range(2):
            for plane in range(4):
                raw = pages[page][plane]
                for i, value in enumerate(raw):
                    if not value:
                        continue
                    start = page * 640 * 400 + i * 8
                    for bit in range(8):
                        if value & (128 >> bit):
                            out[start + bit] |= 1 << plane
        return bytes(out)

    def store_page():
        for i, at in enumerate(planes):
            pages[access][i][:] = u.mem_read(at, 32000)

    def blit(alpha):
        slot, y, x = args(3)
        raw = resources[slot]
        size, width, height = struct.unpack_from('<3H', raw)
        origin = y * 80 + x // 8
        mask = raw[16:16 + size]
        for plane, at in enumerate(planes):
            dest = bytearray(u.mem_read(at, 32000))
            data = raw[16 + (plane + 1) * size:16 + (plane + 2) * size]
            stride = width // 8
            for row in range(height):
                src, dst = (height - row - 1) * stride, origin + row * 80
                if alpha:
                    for col in range(stride):
                        dest[dst + col] = (dest[dst + col] & ~mask[src + col]) | data[src + col]
                else:
                    dest[dst:dst + stride] = data[src:src + stride]
            u.mem_write(at, bytes(dest))
        returning(6)

    def code(uc, address, size, unused):
        nonlocal count, color, fade_refreshes
        if address == 0x195f0 + 0x26e5:
            uc.mem_write(ds + 0x144e, struct.pack('<H', 2 if count == slow else 1))
        elif address == 0x195f0 + 0x2561:
            uc.mem_write(planes[0], bytes(32000))
            returning(far=False)
        elif address == 0x10000 + 0xc36:
            color = args(2)[0]
            returning(4)
        elif address == 0x10000 + 0xb9e:
            bottom, right, top, left = args(4)
            for plane, at in enumerate(planes):
                dest = bytearray(uc.mem_read(at, 32000))
                fill = bytes([255 if color & (1 << plane) else 0]) * (right - left + 1)
                for y in range(top, bottom + 1):
                    start = y * 80 + left
                    dest[start:start + len(fill)] = fill
                uc.mem_write(at, bytes(dest))
            returning(8)
        elif address == 0x1c7e0 + 0x73e or address == 0x1c7e0 + 0x7c8:
            image_index, offset, segment, slot = args(4)
            if text(segment, offset).decode().upper() != resources['names'][slot]:
                raise ValueError('original Staff asset order differs')
            uc.mem_write(ds + 0x1d0e + slot * 16, resources[slot][:16])
            returning(8)
        elif address == 0x1c7e0 + 0xf32:
            blit(False)
        elif address == 0x1c7e0 + 0x1f4:
            blit(True)
        elif address == 0x1c7e0 + 0x9b7:
            offset, segment, fx, y, x = args(5)
            font_calls.append((x, y, text(segment, offset)))
            # Font raster has its separate original comparison. This mask is
            # generated from the original verdict's complete text call list.
            if font_ink:
                for plane, at in enumerate(planes):
                    dest = bytearray(uc.mem_read(at, 32000))
                    for i, mask in enumerate(font_ink):
                        dest[i] |= mask
                    uc.mem_write(at, bytes(dest))
            returning(10)
        elif address == 0x1c7e0 + 0xdc2:
            uc.mem_write(ds + 0x1d0c, struct.pack('<H', 32))
            returning()
        elif address == 0x10000 + 0x2064:
            fade_refreshes += 1
            returning()
        elif address == 0x10000 + 0x17d0:
            if count == 0:
                fade_trace.append((fade_refreshes, word(0x578)))
            returning()
        elif address == 0x10000 + 0x1a68:
            returning(4)
        elif address == 0x1c7e0 + 0x372:
            fade_refreshes += args(1)[0]
            returning(2)
        elif address == 0x1c7e0 + 0x6e2:
            sounds.append(args(1)[0]);returning(2)
        elif address == 0x1c7e0 + 0xa0:
            returning()
        elif address == 0x1c7e0 + 0x84:
            returning()
        elif address == 0x1c7e0 + 0x950:
            returning(2)
        elif address == 0x10000 + 0xc60:
            returning()
        else:
            raise ValueError(f'unhandled foreign service {address:x}')

    def output(uc, port, width, value, unused):
        nonlocal access, shown, count
        if port == 0xa6:
            store_page();access = value & 1
            for i, at in enumerate(planes):
                uc.mem_write(at, bytes(pages[access][i]))
        elif port == 0xa4:
            shown = value & 1
            if get('CS') == 0x195f and get('IP') == 0x2721:
                count += 1
                frame = struct.unpack('<h', uc.mem_read(ds + 0x27c2, 2))[0]
                seed = struct.unpack('<I', uc.mem_read(ds + 0x5b6, 4))[0]
                limit = uc.mem_read(ds + 0x22c0, 1)[0]
                requested, adapt = uc.mem_read(ds + 0x27c5, 2)
                values = [frame & 0xffffffff, shown, seed, limit, requested, adapt, word(0x578)]
                raw = bytes(uc.mem_read(ds + 0x22c2, 80 * 16))
                for i in range(80):
                    alive, x, y, vx, vy, cel = struct.unpack_from('<Bx4hH', raw, i * 16)
                    values.extend((alive, x & 0xffffffff, y & 0xffffffff, vx & 0xffffffff, vy & 0xffffffff, cel))
                row = struct.pack('<' + 'I' * len(values), *values)
                start = (count - 1) * len(row)
                expected_row = native_trace[start:start + len(row)]
                if expected_row != row:
                    field = next(i for i, (a, b) in enumerate(zip(expected_row, row)) if a != b) // 4
                    a = struct.unpack_from('<I', expected_row, field * 4)[0]
                    b = values[field]
                    raise ValueError(f'presentation{count}, field{field}: native={a}, original={b}')
                trace.extend(row)
                # The native tick also draws the verdict after presentation
                # 5156; compare its later snapshots after both pages receive it.
                if count in snapshots and count != 5156:
                    store_page();actual = snapshots[count].read_bytes();expected = pixels()
                    if actual != expected:
                        where = next(i for i, (a, b) in enumerate(zip(actual, expected)) if a != b)
                        raise ValueError(f'original Staff pixels at presentation{count}, page{where // 256000}, x{where % 640}, y{where // 640 % 400}: {actual[where]} != {expected[where]}')
        elif port not in (0xa2, 0x6a, 0x7c, 0x7e):
            raise ValueError(f'unexpected Staff port {port:x}')

    def interrupt(uc, number, unused):
        if number != 0x60 or not music:
            raise ValueError(f'unexpected interrupt {number:x}')
        uc.reg_write(reg.UC_X86_REG_AX, count // 24)

    from unicorn import UC_HOOK_INTR
    u.hook_add(UC_HOOK_INTR, interrupt)
    addresses = [0x195f0 + 0x26e5, 0x195f0 + 0x2561]
    addresses += [0x10000 + x for x in (0xc36, 0xb9e, 0xc60, 0x2064, 0x17d0, 0x1a68)]
    addresses += [0x1c7e0 + x for x in (0x73e, 0x7c8, 0xf32, 0x1f4, 0x9b7, 0xdc2, 0x372, 0x6e2, 0xa0, 0x84, 0x950)]
    for address in addresses:
        u.hook_add(UC_HOOK_CODE, code, begin=address, end=address)
    u.hook_add(UC_HOOK_INSN, output, None, 1, 0, reg.UC_X86_INS_OUT)
    # Original resident, including the final score and RNG, lives separately.
    resident = bytearray(80)
    resident[0xb:0xe] = bytes((1, 5, 17))
    resident[0x18:0x20] = bytes((1, 2, 3, 4, 5, 6, 3, 0))
    struct.pack_into('<I', resident, 0x10, 2000)
    resident[0x36], resident[0x38] = 2, 70
    u.mem_write(0x60000, bytes(resident))
    u.mem_write(ds + 0x21ea, struct.pack('<HH', 0, 0x6000))
    u.mem_write(ds + 0x880, bytes((bool(music),)))
    u.mem_write(ds + 0x578, struct.pack('<H', 0))
    u.emu_start(0x195f0 + 0x2e1d, 0x195f0 + 0xf000, count=250000000)
    if u.reg_read(reg.UC_X86_REG_IP) != 0xf000:
        raise ValueError('original Staff Roll did not return')
    actual = (native_dir / 'trace.bin').read_bytes()
    if actual != trace:
        row = 487 * 4
        where = next((i for i, (a, b) in enumerate(zip(actual, trace)) if a != b), min(len(actual), len(trace)))
        start = where // 4 * 4
        raise ValueError(f'original snow/scheduler differs at presentation{where // row + 1}, field{where % row // 4}: native={actual[start:start+4].hex()}, original={trace[start:start+4].hex()}; lengths={len(actual), len(trace)}')
    fade = bytearray()
    for age in range(1, fade_refreshes + 1):
        value = 0
        for written, tone in fade_trace:
            if written <= age:
                value = tone
        fade.append(value)
    if (native_dir / 'fade.bin').read_bytes() != fade:
        raise ValueError(f'initial palette fade timing differs: original={list(fade)}, native={list((native_dir / "fade.bin").read_bytes())}')
    if (native_dir / 'sounds.bin').read_bytes() != struct.pack('<' + 'H' * len(sounds), *sounds):
        raise ValueError('Staff sound requests differ')
    return font_calls, fade_trace, sounds, count, bytes(u.mem_read(ds + 0x27dc, 13))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', required=True, type=Path)
    parser.add_argument('--native-checks', required=True, type=Path)
    parser.add_argument('--dos-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--slow', type=int, default=99999)
    parser.add_argument('--music', action='store_true')
    args = parser.parse_args()
    root = args.dos_root.resolve()
    sys.path.insert(0, str(root / 'scripts'))
    from lib.pc98 import parse_mz
    raw = (root / '.analysis/toolchain/wineprefix/drive_c/TH03PKG/af1409l/r1/mainl.exe').read_bytes()
    manifest = tomllib.loads((root / 'config/th03_diet.toml').read_text())
    expected = next(row['decoded_sha256'] for row in manifest['artifacts'] if row['id'] == 'th03-mainl')
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('original MAINL identity changed')
    disk = root / '.analysis/runtime/images/zun.hdi'
    targets = tomllib.loads((root / 'config/targets.toml').read_text())
    if hashlib.sha256(disk.read_bytes()).hexdigest() != targets['source']['hdi_sha256']:
        raise ValueError('original HDI identity changed')
    font = root / '.analysis/runtime/fonts/FREECG98.BMP'
    output = args.output.resolve();output.mkdir(parents=True, exist_ok=True)
    native = str(args.native.resolve());checks = str(args.native_checks.resolve())

    def path(file):
        return subprocess.check_output(['wslpath', '-w', str(file)], text=True).strip() if args.native_checks.suffix == '.exe' else str(file)

    subprocess.run([checks, '--staff-run', path(disk), path(font), '9000', str(args.slow), str(int(args.music)), path(output)], check=True)
    names = ['STF1.CDG', 'STF11.CDG', 'STF3.CDG', 'STF4.CDG', 'STF5.CDG', 'STF6.CDG', 'STF7.CDG', 'STF8.CDG', 'STF9.CDG', 'STF10.CDG', 'STF2.CDG', 'STF12.CDG']
    resources = {'names': names}
    for i, name in enumerate(names):
        dest = output / name
        subprocess.run([native, '--hdi', str(disk), '--extract', name, '--output', str(dest)], check=True)
        resources[i] = dest.read_bytes()
    calls = verdict_calls(parse_mz(raw), [1, 1, 2, 3, 4, 5, 6, 3, 0], 2, 1, 85)
    ops = bytearray()
    for x, y, text in calls:
        ops.extend(struct.pack('<3H', x, y, len(text)));ops.extend(text)
    ops_file = output / 'font.ops';ops_file.write_bytes(ops)
    mask_file = output / 'font.pixels'
    subprocess.run([checks, '--font-ops', path(font), path(ops_file), path(mask_file)], check=True)
    raw_ink = mask_file.read_bytes();ink = bytearray(32000)
    for i, pixel in enumerate(raw_ink):
        if pixel:
            ink[i // 8] |= 128 >> (i & 7)
    calls_both, fade, sounds, count, verdict = original(parse_mz(raw), resources, output, ink, args.slow, args.music)
    if calls_both != calls * 2:
        raise ValueError('Staff Roll changed the verdict calls between pages')
    print(f'{count} original presentations: complete snow/RNG/page trace and selected full pages agree; verdict={verdict.hex()}, sounds={sounds}, fade={fade}', flush=True)


if __name__ == '__main__':
    main()
