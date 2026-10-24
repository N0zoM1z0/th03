"""Native producer bindings do not turn a byte match into behavior acceptance."""

from pathlib import Path
import re
import shutil
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.main_hitcirc_context import verify
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from test_main_enemy_layout import mutate_record

WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03WORK"


@unittest.skipUnless(all((WORK / f"obj/th03/{n}.obj").is_file()
                        for n in ("gf_ctx", "execl", "tr_ctx")), "current executable-chain producer absent")
class ExecutableChainCandidate(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.work = Path(self.folder.name)
        (self.work / "obj/th03").mkdir(parents=True)
        for name in ("main.map", "main.obj", "gf_ctx.obj", "execl.obj", "tr_ctx.obj"):
            shutil.copyfile(WORK / "obj/th03" / name, self.work / "obj/th03" / name)
        self.target = parse_mz((ROOT / ".analysis/targets/th03/main.exe").read_bytes())
        self.candidate = parse_mz((WORK / "bin/th03/main.exe").read_bytes())

    def test_byte_layout_gate_alone_has_no_acceptance_authority(self):
        result = verify(self.work, self.target, self.candidate)
        self.assertEqual((result["candidate_bytes"], result["ordered_relocations"]), (79, 9))
        self.assertEqual((result["transition_candidate_bytes"], result["reference_context_bytes"]), (663, 216))
        self.assertFalse(result["exact_acceptance"] or result["behavior_acceptance"])

    def test_equal_program_bytes_do_not_hide_swapped_literal_relocations(self):
        sites = [i for i, r in enumerate(self.candidate.relocations) if 0xB454 <= r.linear < 0xB4A3]
        self.assertEqual(len(sites), 9)
        raw = bytearray(self.candidate.raw)
        table = self.candidate.header.relocation_table_offset
        a, b = (table + i * 4 for i in sites[:2])
        raw[a:a + 4], raw[b:b + 4] = raw[b:b + 4], raw[a:a + 4]
        changed = parse_mz(raw)
        self.assertEqual(changed.program_image, self.candidate.program_image)
        with self.assertRaisesRegex(ValueError, r"nine literal C\+\+ relocations"):
            verify(self.work, self.target, changed)

    def test_one_wrong_argument_byte_is_not_a_raw_match(self):
        raw = bytearray(self.candidate.raw)
        raw[self.candidate.header.header_paragraphs * 16 + 0xB459] ^= 2
        with self.assertRaisesRegex(ValueError, r"raw context or C\+\+ body"):
            verify(self.work, self.target, parse_mz(raw))

    def test_transition_alignment_cannot_borrow_unchanged_instructions(self):
        path = self.work / "obj/th03/main.map"
        text, count = re.subn(r"(?m)^(\s*096E:1DC3\s+0297\s+C=CODE\s+S=HITCIRC_TEXT\s+G=MAIN_01\s+M=th03[\\/]tr_ctx\.cpp\s+ACBP=)28(\s*)$",
                              r"\g<1>48\2", path.read_text(), count=1)
        self.assertEqual(count, 1)
        path.write_text(text)
        with self.assertRaisesRegex(ValueError, "literal MAP contribution"):
            verify(self.work, self.target, self.candidate)

    def test_checksum_valid_private_storage_is_rejected(self):
        path = self.work / "obj/th03/execl.obj"
        raw = path.read_bytes()
        index, = [s["index"] for s in segment_definitions(raw) if s["name"] == "_DATA"]
        chosen = [r for r in parse_omf(raw) if r.record_type == 0x98][index - 1]
        path.write_bytes(mutate_record(raw, lambda r: r.offset == chosen.offset,
                                      lambda data: data[:1] + b"\x02\0" + data[3:]))
        with self.assertRaisesRegex(ValueError, "CODE or private storage"):
            verify(self.work, self.target, self.candidate)

    def test_wrong_native_public_cannot_borrow_the_link_map(self):
        path = self.work / "obj/th03/execl.obj"
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: r.record_type == 0x90,
                                      lambda data: data.replace(b"MAIN_EXEC", b"MAIN_EXED")))
        with self.assertRaisesRegex(ValueError, r"complete C\+\+ producer ownership"):
            verify(self.work, self.target, self.candidate)

    def test_empty_root_word_alignment_cannot_borrow_an_unchanged_map(self):
        path = self.work / "obj/th03/main.obj"
        raw = path.read_bytes()
        segment, = [s for s in segment_definitions(raw) if s["name"] == "HITCIRC_TEXT"]
        record = [r for r in parse_omf(raw) if r.name == "SEGDEF"][segment["index"] - 1]
        self.assertEqual(segment["size"], 0)
        path.write_bytes(mutate_record(raw, lambda r: r.offset == record.offset,
                                      lambda data: b"\x48" + data[1:]))
        with self.assertRaisesRegex(ValueError, "empty root HITCIRC must remain BYTE"):
            verify(self.work, self.target, self.candidate)
