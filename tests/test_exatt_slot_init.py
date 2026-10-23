"""Execute the relocated native initializer and check every pointer/history byte."""

from pathlib import Path
import struct
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.pc98 import parse_mz
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact
from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn import x86_const as x86

CANDIDATE = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03WORK/bin/th03/main.exe"


@unittest.skipUnless(CANDIDATE.is_file(), "local MAIN work tree absent")
class SlotInitializer(unittest.TestCase):
    def test_pointer_mapping_writes_and_far_abi(self):
        target = parse_mz(
            read_verified_artifact(
                ROOT,
                find_artifact(
                    load_target_manifest(ROOT / "config/targets.toml"), "th03-main"
                ),
            )
        )
        for label, image in (
            ("target", target),
            ("candidate", parse_mz(CANDIDATE.read_bytes())),
        ):
            for load in (0x1000, 0x2000):
                for seed in (0, 1):
                    with self.subTest(image=label, load=load, seed=seed):
                        self.execute(image, load, seed)

    def execute(self, image, load, seed):
        u = Uc(UC_ARCH_X86, UC_MODE_16)
        u.mem_map(0, 0x100000)
        program = bytearray(image.program_image)
        for r in image.relocations:
            v = struct.unpack_from("<H", program, r.linear)[0]
            struct.pack_into("<H", program, r.linear, (v + load) & 65535)
        u.mem_write(load * 16, bytes(program))
        regs = dict(
            SI=0x1357,
            DI=0x2468,
            BP=0xBEEF,
            SP=0xFF00,
            DS=load + 0x1D56,
            SS=0x8000,
            CS=load + 0x18FE,
            IP=0x3DC,
            AX=0xA55A,
            BX=0x5AA5,
            CX=0x1234,
            DX=0x5678,
            ES=0x4444,
            EFLAGS=0x202 | (seed << 10),
        )
        for name, value in regs.items():
            u.reg_write(getattr(x86, "UC_X86_REG_" + name), value)
        data, stack = regs["DS"] * 16, regs["SS"] * 16 + regs["SP"]
        slots, entities = 0x230A, 0x292A
        u.mem_write(data + slots, bytes((i * 37 + seed) & 255 for i in range(720)))
        u.mem_write(data + entities, bytes((i * 17 + seed) & 255 for i in range(1024)))
        u.mem_write(stack, struct.pack("<HH", 0x200, 0x7E00))
        initial = bytes(u.mem_read(0, 0x100000))
        expected = bytearray(initial)
        expected_writes = []
        for i in range(12):
            for pid in (0, 1):
                at = data + slots + (pid * 12 + i) * 30
                value = entities + (pid * 16 + i) * 32
                struct.pack_into("<H", expected, at, value)
                expected_writes.append((at, 2, value))
        writes, seen = [], set()
        stopped = False

        def hook(uc, address, size, unused):
            nonlocal stopped
            if address == 0x7E200:
                stopped = True
                uc.emu_stop()
                return
            self.assertTrue(load * 16 + 0x193BC <= address < load * 16 + 0x193EF)
            seen.update(range(address, address + size))

        def write(uc, access, address, size, value, unused):
            if stack - 128 <= address and address + size <= stack + 4:
                return
            writes.append((address, size, value))

        u.hook_add(UC_HOOK_CODE, hook)
        u.hook_add(UC_HOOK_MEM_WRITE, write)
        u.emu_start(load * 16 + 0x193BC, 0, count=1000)
        self.assertTrue(stopped)
        self.assertEqual(len(seen), 51)
        self.assertEqual(writes, expected_writes)
        actual = bytes(u.mem_read(0, 0x100000))
        self.assertEqual(actual[: stack - 128], expected[: stack - 128])
        self.assertEqual(actual[stack + 4 :], expected[stack + 4 :])
        for name in ("SI", "DI", "BP", "DS", "SS"):
            self.assertEqual(u.reg_read(getattr(x86, "UC_X86_REG_" + name)), regs[name])
        self.assertEqual(u.reg_read(x86.UC_X86_REG_SP), regs["SP"] + 4)
        self.assertEqual(
            u.reg_read(x86.UC_X86_REG_EFLAGS) & 0x600, regs["EFLAGS"] & 0x600
        )


if __name__ == "__main__":
    unittest.main()
