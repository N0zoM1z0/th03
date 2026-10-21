"""Source-only checks. Token equivalence is not a native or hardware proof."""
import hashlib
import importlib.util
from pathlib import Path
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT
spec = importlib.util.spec_from_file_location("stage_mainl_cutscene", ROOT / "scripts/stage_th03_mainl_cutscene.py")
stager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stager)

REFERENCE_HASHES = {
    "th03/cutscene/cutscene.cpp": "49fbde7cc661dda1d8a290debe285d625f4d274abb9c68c42d28150c59afb760",
    "th03/cutscene/cutscene.hpp": "d049daefdc5341b40c4437da941b944531a0f11cb12146ce3ee648002d59d182",
    "th03/formats/script.hpp": "b43f978834d21ea9d63f2525a48cbc30a25378a3209eef305473b2b03cd41598",
    "th01/hardware/egcstart.cpp": "acefacdc5bf56cb274cb252480690166d0dbb379ffa95c62d729ea1a852e2b1a",
}
ALIASES = {
    "src/mainl/cutscene/cutscene.hpp": "th03/cutscene/cutscene.hpp",
    "src/mainl/cutscene/script.inl": "th03/formats/script.hpp",
    "src/mainl/cutscene/egc_start_copy.inl": "th01/hardware/egcstart.cpp",
}

def tokens(text):
    # Lex strings/chars before comments, so quoted punctuation is never erased.
    pattern = r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|[A-Za-z_][A-Za-z_0-9]*|[0-9]+|[^\s]'
    return [m[0] for m in re.finditer(pattern, text) if not m[0].startswith(("//", "/*"))]

def original_includes(text):
    def replace(match):
        path = match[1]
        return '#include "' + ALIASES.get(path, path.removeprefix("compat/rec98/")) + '"'
    return re.sub(r'#include "([^"]+)"', replace, text)

def game_three(text):
    # Restricted evaluator: no C preprocessor, compiler, or external execution.
    truth = {"==": lambda n: 3 == n, "!=": lambda n: 3 != n,
             ">=": lambda n: 3 >= n, "<=": lambda n: 3 <= n}
    frames = []
    active = True
    output = []
    for line in text.splitlines(True):
        match = re.match(r'\s*#(if|elif)\s+\(GAME\s*(==|!=|>=|<=)\s*([345])\)', line)
        if match:
            value = truth[match[2]](int(match[3]))
            if match[1] == "if":
                frames.append([active, value])
                active = active and value
            else:
                parent, seen = frames[-1]
                active = parent and not seen and value
                frames[-1][1] = seen or value
        elif re.match(r'\s*#else\b', line):
            parent, seen = frames[-1]
            active = parent and not seen
            frames[-1][1] = True
        elif re.match(r'\s*#endif\b', line):
            active = frames.pop()[0]
        elif re.match(r'\s*#(if|elif|ifdef|ifndef)\b', line):
            raise ValueError("unreviewed conditional: " + line)
        elif active:
            output.append(line)
    if frames:
        raise ValueError("unterminated conditional")
    return "".join(output)

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

    def test_complete_th03_active_owner(self):
        expected = game_three(self.reference("th03/cutscene/cutscene.cpp"))
        self.assertEqual(tokens(self.source(stager.OWNER)), tokens(expected))

    def test_public_declarations(self):
        self.assertEqual(tokens(self.source(stager.OWNED[1])),
                         tokens(game_three(self.reference("th03/cutscene/cutscene.hpp"))))

    def test_parser_helpers(self):
        expected = self.reference("th03/formats/script.hpp")
        branch = "#if ((GAME == 5) && (BINARY == 'E'))\nint script_param_number_default;\n#else\nextern int script_param_number_default;\n#endif"
        self.assertEqual(expected.count(branch), 1)
        expected = expected.replace(branch, "extern int script_param_number_default;")
        self.assertEqual(tokens(self.source(stager.OWNED[2])), tokens(expected))

    def test_egc_producer(self):
        self.assertEqual(tokens(self.source(stager.OWNED[3])),
                         tokens(self.reference("th01/hardware/egcstart.cpp")))

    def test_specializer_nested_and_elif(self):
        self.assertEqual(game_three("#if (GAME == 5)\na\n#elif (GAME == 4)\nb\n#else\n#if (GAME != 5)\nc\n#endif\n#endif\n"), "c\n")
        with self.assertRaises(ValueError):
            game_three("#ifdef UNKNOWN\na\n#endif\n")

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
        self.assertEqual((self.output / stager.SLOT).read_bytes(), stager.WRAPPER)
        for name in stager.INPUTS:
            self.assertEqual((self.output / name).read_bytes(), (self.root / name).read_bytes())
        self.assertEqual(report["native_runs"], 0)
        self.assertFalse(report["exact"])
        self.assertFalse(report["cold_reproducible"])
        self.assertEqual(len(report["files"]), len(stager.INPUTS) + 1)
        self.assertEqual(report["compile_slot"], "th03/cutscene.cpp")
        with self.assertRaises(FileExistsError):
            stager.stage(self.root, self.output)

    def test_missing_input_fails_before_output(self):
        (self.root / stager.OWNED[2]).unlink()
        with self.assertRaises(FileNotFoundError):
            stager.stage(self.root, self.output)
        self.assertFalse(self.output.exists())

    def test_unregistered_include_rejected(self):
        with (self.root / stager.OWNER).open("a") as stream:
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
        path = self.root / stager.OWNER
        path.write_bytes(path.read_bytes().replace(b"#pragma option -zPgroup_01", b""))
        with self.assertRaisesRegex(ValueError, "group pragma"):
            stager.stage(self.root, self.output)
        self.assertFalse(self.output.exists())

if __name__ == "__main__":
    unittest.main()
