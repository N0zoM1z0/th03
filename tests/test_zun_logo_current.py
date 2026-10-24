"""Native logo ownership and independent word-width/port/ABI controls."""

from pathlib import Path
import shutil
import struct
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.zun import parse_launcher
from lib.zun_logo_layout import verify, BSS_PUBLICS
from lib.zun_logo_runtime import Machine, BSS_SIZE, BSS, put, negative_controls
from test_main_enemy_layout import mutate_record

WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03ZUN"


@unittest.skipUnless((WORK / "product/zun.target.com").is_file(), "private current ZUN target absent")
class CurrentLogo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        decoded = (WORK / "product/zun.target.com").read_bytes()
        row = parse_launcher(decoded, 223)["payloads"][2]
        cls.offset = row["decoded_file_offset"]
        cls.target = decoded[cls.offset:cls.offset + row["size"]]
        cls.candidate = (WORK / "bin/th01/zunsoft.com").read_bytes()

    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.work = Path(folder.name)
        for name in ("obj/th01/zunsoft.obj", "obj/th01/zunsoft.map"):
            dest = self.work / name; dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(WORK / name, dest)

    def machine(self):
        result = Machine(self.target, 0x3000)
        self.addCleanup(result.close)
        return result

    def test_native_word_alignment_has_no_padding_public(self):
        result = verify(self.work, self.target, self.candidate, self.offset)
        self.assertEqual((result["code_bytes"], result["data_bytes"], result["bss_bytes"]), (1299, 15, 293))
        self.assertEqual((result["omf_bss_publics"], result["map_public_table_entries"]), (14, 48))
        self.assertNotIn(7, [offset for offset, _ in BSS_PUBLICS])
        self.assertNotIn(b"char wave_padding;", (ROOT / "src/zun/zunsoft.cpp").read_bytes())
        self.assertEqual({o["format"] for o in result["owners"]}, {"COM"})
        self.assertTrue(all(o["canonical_file_offset"] is None for o in result["owners"]))

    def test_source_dependency_cannot_be_replaced_by_reference_context(self):
        path = self.work / "obj/th01/zunsoft.obj"
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: b"src/zun/zunsoft.cpp" in r.data,
                                      lambda d: d.replace(b"src/zun/zunsoft.cpp", b"src/zun/oldlogo.cpp")))
        with self.assertRaisesRegex(ValueError, "maintained source dependency"):
            verify(self.work, self.target, self.candidate, self.offset)

    def test_complete_bss_public_ownership_is_required(self):
        path = self.work / "obj/th01/zunsoft.obj"
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: r.record_type == 0x90 and b"_circle_pos" in r.data,
                                      lambda d: d.replace(b"_circle_pos", b"_circle_pad")))
        with self.assertRaisesRegex(ValueError, "BSS public layout"):
            verify(self.work, self.target, self.candidate, self.offset)

    def test_last_owned_code_byte_and_initialized_data_are_compared(self):
        for offset, error in ((0x879 - 0x100, "raw procedure"), (0x20DC, "DATA bytes")):
            raw = bytearray(self.candidate); raw[offset] ^= 1
            with self.subTest(offset=offset), self.assertRaisesRegex(ValueError, error):
                verify(self.work, self.target, bytes(raw), self.offset)

    def test_signed_vector_rounding_near_aliases_and_pascal_return(self):
        m = self.machine()
        m.run("zunsoft_vector2", length=37, angle=0xAB00 | 160, refs=(0x3501, 0x3503), sp=0xE800, flags=0x602)
        self.assertEqual(struct.unpack("<hh", m.u.mem_read(m.base + 0x3501, 4)), (-27, -27))
        m.run("zunsoft_vector2", length=-32768, angle=64, refs=(0x3504, 0x3504))
        self.assertEqual(struct.unpack("<h", m.u.mem_read(m.base + 0x3504, 2))[0], -32768)

    def test_char_argument_preserves_the_opaque_alignment_byte(self):
        state = bytearray(BSS_SIZE); put(state, 224, 90)
        state[3:8] = bytes((6, 23, 250, 128, 0xA5))
        m = self.machine(); m.run("logo_render_and_update", state)
        wave = [e for e in m.events if e[0] == "SUPER_WAVE_PUT"]
        self.assertEqual([e[5] for e in wave], [0xA580, 0xA580])
        self.assertEqual(m.u.mem_read(m.base + BSS + 7, 1), b"\xA5")

    def test_star_wrap_is_one_signed_correction_and_angle_wraps_as_byte(self):
        state = bytearray(BSS_SIZE); state[242] = 255
        put(state, 24, 32767); put(state, 26, -1)
        m = self.machine(); m.run("stars_render_and_update", state)
        self.assertEqual(struct.unpack("<hh", m.u.mem_read(m.base + BSS + 24, 4)), (32127, 399))
        self.assertEqual(m.u.mem_read(m.base + BSS + 242, 1), b"\0")

    def test_keyboard_checks_all_eight_groups_and_pc9821_preserves_low_bits(self):
        m = self.machine(); m.run("main", key_frame=0, key_group=7, key_value=0x8000, hardware=True, bios=0xFF)
        keys = [e for e in m.events if e[0] == "KEY_SENSE"]
        self.assertEqual([e[1] for e in keys], list(range(8)))
        self.assertEqual(keys[-1][2], 0x8000)
        self.assertEqual(m.u.mem_read(0x54D, 1), b"\x7F")

    def test_eighteen_actual_guest_mutations_fail(self):
        self.assertEqual(negative_controls(self.target)["count"], 18)
