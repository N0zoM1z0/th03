"""Source-only checks. Token equivalence is not a native or hardware proof."""
import hashlib
import importlib.util
from pathlib import Path
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT
spec = importlib.util.spec_from_file_location("stage_mainl_regist", ROOT / "scripts/stage_th03_mainl_regist.py")
stager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stager)

REFERENCE_HASHES = {'th03/hiscore/regist.cpp': '15355e761d8999b091c9c5b7405879ff371ef67909380e9aa2f58637657f345e', 'th03/formats/scoredat.cpp': 'f566b491cb41d9bdd878fe0031de2904653499081a321f8ac6701de1ce8139e3', 'th03/hiscore/regist.hpp': '03f49d417df57ae851fc3fd88d11653103f5a97804b767b77d7549758e1c8d25', 'th03/formats/scoredat.hpp': '9ec2bd5929d5413b0d9c90ad30f27275c91738d1cfe96fb4db5d72c0f16141db', 'th03/formats/score_ld.cpp': 'cdbc6fc7d4f5a4cff0b5e0e7b44ee10f593f27211aef16c8bd4468e4fd6f0e08', 'th03/formats/score_es.cpp': 'b827cd3f82b71b7ad3a8bcc545877836fc19d0d07aa2916f992259ed71beea2b', 'th03/formats/scorecry.hpp': 'f4c5265b445636c9a8d5e1df22b975b87153709fe4936297cd9d25bb497d5dfe', 'th03/sprites/regi.h': '6b1114f268aef0edbe4ae58d427c208178db550748d6b574d32cbebc6b04ca3f', 'th03/shiftjis/regist.hpp': '5e13629d70746110d0eb8ee35b9b61266fb9f4715cd7ebba5d119b72ae8d9bd6'}
ALIASES = {'src/mainl/regist.cpp': 'th03/hiscore/regist.cpp', 'src/mainl/scoredat.cpp': 'th03/formats/scoredat.cpp', 'src/mainl/hiscore/regist.hpp': 'th03/hiscore/regist.hpp', 'src/mainl/hiscore/scoredat.hpp': 'th03/formats/scoredat.hpp', 'src/mainl/hiscore/score_load.inl': 'th03/formats/score_ld.cpp', 'src/mainl/hiscore/score_save.inl': 'th03/formats/score_es.cpp', 'src/mainl/hiscore/scorecry.hpp': 'th03/formats/scorecry.hpp', 'src/mainl/hiscore/regi.h': 'th03/sprites/regi.h', 'src/mainl/hiscore/regist_text.hpp': 'th03/shiftjis/regist.hpp'}

def tokens(text):
    # Lex strings/chars before comments, so quoted punctuation is never erased.
    pattern = r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|[A-Za-z_][A-Za-z_0-9]*|[0-9]+|[^\s]'
    return [m[0] for m in re.finditer(pattern, text) if not m[0].startswith(("//", "/*"))]

def original_includes(text):
    def replace(match):
        path = match[1]
        return '#include "' + ALIASES.get(path, path.removeprefix("compat/rec98/")) + '"'
    return re.sub(r'#include "([^"]+)"', replace, text)

class SourceEquivalence(unittest.TestCase):
    def reference(self, name):
        path = ROOT / "_reference/ReC98" / name
        if not path.is_file():
            self.skipTest("frozen reference unavailable; source-only checks cannot substitute for it")
        body = path.read_bytes()
        self.assertEqual(hashlib.sha256(body).hexdigest(), REFERENCE_HASHES[name])
        return body.decode("utf-8")

    def source(self, name):
        return original_includes((SOURCE_ROOT / name).read_text())

    def test_all_owned_tokens_preserve_frozen_semantics(self):
        for owned, reference in ALIASES.items():
            with self.subTest(owner=owned):
                self.assertEqual(tokens(self.source(owned)), tokens(self.reference(reference)))

    def test_unchecked_paths_and_binary_contract_remain(self):
        load = self.source("src/mainl/hiscore/score_load.inl")
        save = self.source("src/mainl/hiscore/score_save.inl")
        self.assertIn("#if (BINARY == 'L')", load)
        self.assertIn("return recreated;", load)
        self.assertIn("file_read(&hi, sizeof(scoredat_section_t));", load)
        self.assertIn("resident->story_stage == STAGE_ALL", save)
        self.assertNotIn("resident->rank == rank) &&", save)


class SourceStaging(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / ".analysis")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        for name in stager.INPUTS:
            source = SOURCE_ROOT / name
            if not source.exists():
                source = ROOT / name
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(source.read_bytes())
        self.output = Path(self.temp.name) / "overlay"

    def test_consumed_overlay_preserves_inputs_and_slot(self):
        report = stager.stage(self.root, self.output)
        for slot, owner in stager.SLOTS.items():
            self.assertEqual((self.output / slot).read_bytes(), ('#include "' + owner + '"\n').encode())
        for name in stager.INPUTS:
            self.assertEqual((self.output / name).read_bytes(), (self.root / name).read_bytes())
        self.assertEqual(report["native_runs"], 0)
        self.assertFalse(report["exact"])
        self.assertFalse(report["cold_reproducible"])
        self.assertEqual(len(report["files"]), len(stager.INPUTS) + 2)
        self.assertEqual(report["compile_slots"], stager.SLOTS)
        with self.assertRaises(FileExistsError):
            stager.stage(self.root, self.output)

    def test_missing_input_fails_before_output(self):
        (self.root / stager.OWNED[2]).unlink()
        with self.assertRaises(FileNotFoundError):
            stager.stage(self.root, self.output)
        self.assertFalse(self.output.exists())

    def test_unregistered_include_rejected(self):
        with (self.root / next(iter(stager.SLOTS.values()))).open("a") as stream:
            stream.write('#include "th03/hidden.cpp"\n')
        with self.assertRaisesRegex(ValueError, "undeclared"):
            stager.stage(self.root, self.output)
        self.assertFalse(self.output.exists())

    def test_source_symlink_rejected(self):
        path = self.root / stager.OWNED[2]
        data = path.read_bytes()
        path.unlink()
        alternate = self.root / "alternate.inl"
        alternate.write_bytes(data)
        path.symlink_to(alternate)
        with self.assertRaisesRegex(ValueError, "symlink"):
            stager.stage(self.root, self.output)
        self.assertFalse(self.output.exists())

    def test_missing_group_rejected(self):
        path = self.root / next(iter(stager.SLOTS.values()))
        path.write_bytes(path.read_bytes().replace(b"#pragma option -zPgroup_01", b""))
        with self.assertRaisesRegex(ValueError, "group pragma"):
            stager.stage(self.root, self.output)
        self.assertFalse(self.output.exists())

if __name__ == "__main__":
    unittest.main()
