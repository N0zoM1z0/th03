#!/usr/bin/env python3
"""Compare Reimu Bomb fill, portrait and overlaid particles with original MAIN.

Execute the real update/draw owners, GRCG fill and MRS blitter. Only the sound
service and resident sprite device are supplied at their hardware boundaries.
The sprite atlas comes from the independently checked original PI decoder.
"""

import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import tomllib
from unicorn import (
    Uc,
    UC_ARCH_X86,
    UC_MODE_16,
    UC_HOOK_CODE,
    UC_HOOK_INTR,
    UC_HOOK_INSN,
    UC_HOOK_MEM_WRITE,
)
from unicorn.x86_const import (
    UC_X86_REG_CS,
    UC_X86_REG_DS,
    UC_X86_REG_SS,
    UC_X86_REG_SP,
    UC_X86_REG_IP,
    UC_X86_REG_AX,
    UC_X86_REG_BX,
    UC_X86_REG_CX,
    UC_X86_REG_DX,
    UC_X86_REG_DI,
    UC_X86_INS_OUT,
)


def compare(program, pid, native, atlas, mrs):
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    u.mem_write(0x10000, bytes(program))
    ds = 0x2D560
    for at, size in ((0x6580, 2), (0x307E, 514), (0x659C, 4), (0x65A6, 256)):
        u.mem_write(ds + at, bytes(size))
    u.mem_write(ds + 0x6580 + pid, b"\x01")
    u.mem_write(ds + 0x65A6 + pid * 128 + 8, bytes([pid + 1]))
    u.mem_write(ds + 0x2928, bytes([pid]))
    u.mem_write(ds + 0x6590, bytes([pid * 40]))
    u.mem_write(ds + 0x1E52, bytes((i * 13 + 7) & 255 for i in range(256)))
    u.mem_write(ds + 0x1F52, b"\xfe")
    u.mem_write(ds + 0x2D4, struct.pack("<H", 100))
    u.mem_write(0x60000, mrs)
    u.mem_write(ds + 0x1D64 + (pid + 2) * 4, struct.pack("<HH", 0, 0x6000))
    bases = (0xA8000, 0xB0000, 0xB8000, 0xE0000)
    planes = []
    mode = 0
    dirty = False
    tiles = [0] * 4
    tile_i = 0

    def call(seg, off, args=()):
        for reg, value in (
            (UC_X86_REG_CS, seg + 0x1000),
            (UC_X86_REG_DS, 0x2D56),
            (UC_X86_REG_SS, 0x8000),
            (UC_X86_REG_SP, 0xFF00),
        ):
            u.reg_write(reg, value)
        u.mem_write(
            0x8FF00,
            struct.pack("<HH", 0xF000, 0x239D)
            + b"".join(struct.pack("<H", a & 65535) for a in reversed(args)),
        )
        u.emu_start((seg + 0x1000) * 16 + off, 0x329D0, count=2000000)
        assert u.reg_read(UC_X86_REG_IP) == 0xF000, (
            pid,
            seg,
            off,
            u.reg_read(UC_X86_REG_IP),
        )

    def sync():
        for base, plane in zip(bases, planes):
            u.mem_write(base, bytes(plane))

    def out(uc, port, size, value, unused):
        nonlocal mode, tile_i, planes, dirty
        if port == 0x7C:
            # EGC_ON also writes 7Ch, but has no pending CPU fill to commit.
            if dirty:
                sync()
            mode = value
            tile_i = 0
            dirty = False
            if mode & 0x80:
                planes = [bytearray(uc.mem_read(base, 16000)) for base in bases]
        elif port == 0x7E:
            tiles[tile_i] = value
            tile_i = (tile_i + 1) % 4

    def write(uc, access, address, size, value, unused):
        nonlocal dirty
        if not mode & 0x80:
            return
        for i in range(size):
            at = address + i - bases[0]
            if not 0 <= at < 16000:
                continue
            dirty = True
            mask = (value >> (i * 8)) & 255
            for p in range(4):
                if not mode & (1 << p):
                    planes[p][at] = (planes[p][at] & (~mask & 255)) | (tiles[p] & mask)

    def code(uc, address, size, unused):
        if address != 0x1EC3A:
            return
        sp = uc.reg_read(UC_X86_REG_SP)
        ip, cs = struct.unpack("<HH", uc.mem_read(0x80000 + sp, 4))
        uc.reg_write(UC_X86_REG_SP, sp + 6)
        uc.reg_write(UC_X86_REG_CS, cs)
        uc.reg_write(UC_X86_REG_IP, ip)

    def interrupt(uc, number, unused):
        assert number == 0x42 and uc.reg_read(UC_X86_REG_AX) >> 8 == 2, (
            number,
            uc.reg_read(UC_X86_REG_AX),
        )
        left = uc.reg_read(UC_X86_REG_DX)
        top = uc.reg_read(UC_X86_REG_BX)
        top = top if top < 32768 else top - 65536
        source = uc.reg_read(UC_X86_REG_DI)
        height = uc.reg_read(UC_X86_REG_CX) & 255
        width = (uc.reg_read(UC_X86_REG_AX) & 255) * 16
        if top < 0:
            source -= top * 80
            height += top
            top = 0
        else:
            height = min(height, 200 - top)
        planes = [bytearray(uc.mem_read(base, 16000)) for base in bases]
        for y in range(height):
            for x in range(width):
                color = atlas[(source + y * 80) * 8 + x]
                if color:
                    at = (top + y) * 80 + (left + x) // 8
                    mask = 128 >> ((left + x) % 8)
                    for p in range(4):
                        planes[p][at] = (planes[p][at] & (~mask & 255)) | (
                            mask if color & (1 << p) else 0
                        )
        for base, plane in zip(bases, planes):
            uc.mem_write(base, bytes(plane))

    u.hook_add(UC_HOOK_INSN, out, None, 1, 0, UC_X86_INS_OUT)
    u.hook_add(UC_HOOK_MEM_WRITE, write, begin=0xA8000, end=0xABFFF)
    u.hook_add(UC_HOOK_CODE, code)
    u.hook_add(UC_HOOK_INTR, interrupt)
    if pid:
        call(0xE8F, 0x5D4)
        call(0xE8F, 0x7B6, (pid + 2,))
    checked = 0
    for frame in range(180):
        for base, value in zip(bases, (0xAA, 0x33, 0x55, 0xFF)):
            u.mem_write(base, bytes([value]) * 16000)
        call(0x139D, 0x16BC)
        call(0x139D, 0x1811)
        # Cover spawn/fill, portrait overlap, shaking, fading and deactivation.
        if frame + 1 not in (
            1,
            8,
            31,
            32,
            63,
            64,
            65,
            80,
            95,
            96,
            97,
            111,
            112,
            128,
            170,
            179,
            180,
        ):
            continue
        planes = [bytes(u.mem_read(base, 16000)) for base in bases]
        pixels = bytearray(128000)
        for at in range(16000):
            for bit in range(8):
                pixels[at * 8 + bit] = sum(
                    1 << p for p in range(4) if planes[p][at] & (128 >> bit)
                )
        expected = native[frame * 128000 : (frame + 1) * 128000]
        if pixels != expected:
            mismatches = [
                (at % 640, at // 640, a, b)
                for at, (a, b) in enumerate(zip(pixels, expected))
                if a != b
            ]
            raise ValueError(
                f"Reimu Bomb pid={pid} frame={frame + 1}: {len(mismatches)} differing dots, first={mismatches[:12]}"
            )
        checked += 1
    print(
        "Original Reimu bomb draw pixels agree for player",
        pid,
        "across",
        checked,
        "phase boundaries including portrait, particles, fill and finish",
        flush=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native", type=Path, required=True)
    parser.add_argument("--native-checks", type=Path, required=True)
    parser.add_argument("--dos-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.dos_root.resolve()
    cfg = tomllib.loads((root / "config/targets.toml").read_text())
    target = next(x for x in cfg["artifacts"] if x["id"] == "th03-main")
    raw = (root / target["private_path"]).read_bytes()
    disk = root / ".analysis/runtime/images/zun.hdi"
    if (
        hashlib.sha256(raw).hexdigest() != target["sha256"]
        or hashlib.sha256(disk.read_bytes()).hexdigest() != cfg["source"]["hdi_sha256"]
    ):
        raise ValueError("Original MAIN/HDI identity changed")
    sys.path.insert(0, str(root / "scripts"))
    from lib.pc98 import parse_mz

    image = parse_mz(raw)
    program = bytearray(image.program_image)
    for rel in image.relocations:
        struct.pack_into(
            "<H",
            program,
            rel.linear,
            (struct.unpack_from("<H", program, rel.linear)[0] + 0x1000) & 65535,
        )
    native, checks = args.native.resolve(), args.native_checks.resolve()

    def path(p, binary):
        return (
            subprocess.check_output(["wslpath", "-w", str(p)], text=True).strip()
            if binary.suffix == ".exe"
            else str(p)
        )

    with tempfile.TemporaryDirectory(prefix="th03-reimu-bomb-") as temporary:
        work = Path(temporary)
        atlas = bytearray(128000)
        for pid in (0, 1):
            pi = work / f"{pid}.pi"
            output = work / f"{pid}.pixels"
            mrs = work / f"{pid}.mrs"
            subprocess.run(
                [
                    str(native),
                    "--hdi",
                    path(disk, native),
                    "--pi",
                    f"{pid:02d}16.PI",
                    "--packed",
                    path(pi, native),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            packed = pi.read_bytes()
            if len(packed) != 320 * 16 // 2:
                raise ValueError("Unexpected Reimu sprite PI geometry")
            for y in range(8):
                for x in range(320):
                    value = packed[(y * 2 * 320 + x) // 2]
                    atlas[y * 640 + pid * 320 + x] = value & 15 if x & 1 else value >> 4
            subprocess.run(
                [
                    str(native),
                    "--hdi",
                    path(disk, native),
                    "--main-assets",
                    "--extract",
                    f"{pid:02d}BM.MRS",
                    "--output",
                    path(mrs, native),
                ],
                check=True,
            )
            subprocess.run(
                [
                    str(checks),
                    "--reimu-bomb-raster",
                    path(disk, checks),
                    str(pid),
                    path(output, checks),
                ],
                check=True,
            )
            data = output.read_bytes()
            if len(data) != 180 * 128000:
                raise ValueError("Incomplete native Bomb raster sequence")
            compare(bytes(program), pid, data, atlas, mrs.read_bytes())


if __name__ == "__main__":
    main()
