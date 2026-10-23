from __future__ import annotations

import contextlib
import csv
import io
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
import tomllib
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_tracking import (
    EVIDENCE_HEADER,
    FUNCTION_HEADER,
    HYPOTHESIS_HEADER,
    KNOWLEDGE_HEADER,
    UNIT_HEADER,
    main as validate_tracking,
    validate_source_tree,
)


class ExactTrackingTests(unittest.TestCase):
    def make_fixture(self, root: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
        repository = Path(__file__).resolve().parents[1]
        config = root / "config"
        config.mkdir()
        shutil.copyfile(repository / "config" / "targets.toml", config / "targets.toml")
        shutil.copyfile(repository / "config" / "oracles.toml", config / "oracles.toml")
        (root / "src" / "main").mkdir(parents=True)
        (root / "src" / "main" / "unit.c").write_text(
            "int unit(void) { return 0; }\n", encoding="utf-8"
        )
        (root / "scripts").mkdir()
        (root / "scripts" / "replay.py").write_text("# replay fixture\n", encoding="utf-8")

        unit = {
            "id": "unit-main-100",
            "artifact": "th03-main",
            "kind": "code",
            "segment": "CODE",
            "offset": "0x100",
            "file_offset": "0x100",
            "size": "16",
            "compare_size": "16",
            "boundary_state": "reviewed",
            "origin": "authored",
            "state": "exact",
            "name": "unit",
            "source": "src/main/unit.c",
            "evidence_ids": "",
            "replay_command": "python3 scripts/replay.py --unit unit-main-100",
            "notes": "synthetic exact-promotion fixture",
        }
        other = dict(unit)
        other.update(
            {
                "id": "unit-main-200",
                "offset": "0x200",
                "file_offset": "0x200",
                "state": "candidate",
                "evidence_ids": "",
            }
        )
        oracle_config = tomllib.loads((config / "oracles.toml").read_text(encoding="utf-8"))
        accepted = {
            item["id"]: item.get("accepts_evidence_classes", ["control-plane"])[0]
            for item in oracle_config["oracles"]
        }
        global_oracles = set(oracle_config["policy"]["global_evidence_oracles"])
        artifact_oracles = set(oracle_config["policy"]["artifact_evidence_oracles"])
        evidence: list[dict[str, str]] = []
        for oracle in oracle_config["policy"]["exact_requires"]:
            row = {field: "" for field in EVIDENCE_HEADER}
            row.update(
                {
                    "id": f"ev-{oracle}",
                    "oracle": oracle,
                    "location": "synthetic fixture",
                    "evidence_class": accepted[oracle],
                    "result": "pass",
                    "tool": "scripts/replay.py",
                    "command": "python3 scripts/replay.py --unit unit-main-100",
                    "input_sha256": "1" * 64,
                    "output_sha256": "1" * 64,
                    "observed_utc": "2026-09-06T00:00:00Z",
                    "notes": "synthetic exact evidence",
                }
            )
            if oracle in global_oracles:
                pass
            elif oracle in artifact_oracles:
                row["artifact"] = "th03-main"
            else:
                row.update(
                    {
                        "artifact": "th03-main",
                        "unit_id": unit["id"],
                        "extent_start": unit["file_offset"],
                        "extent_size": unit["compare_size"],
                    }
                )
            evidence.append(row)
        unit["evidence_ids"] = ";".join(row["id"] for row in evidence)
        return [unit, other], evidence

    @staticmethod
    def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=header)
            writer.writeheader()
            writer.writerows(rows)

    def run_fixture(
        self,
        root: Path,
        units: list[dict[str, str]],
        evidence: list[dict[str, str]],
        functions: list[dict[str, str]] | None = None,
    ) -> int:
        config = root / "config"
        self.write_csv(config / "units.csv", UNIT_HEADER, units)
        self.write_csv(config / "evidence.csv", EVIDENCE_HEADER, evidence)
        self.write_csv(config / "hypotheses.csv", HYPOTHESIS_HEADER, [])
        self.write_csv(config / "knowledge.csv", KNOWLEDGE_HEADER, [])
        if functions is not None:
            self.write_csv(
                config / "th03_main_authored_functions.csv", FUNCTION_HEADER, functions
            )
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return validate_tracking(root)

    def test_complete_unit_bound_exact_fixture_passes(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            units, evidence = self.make_fixture(root)
            self.assertEqual(self.run_fixture(root, units, evidence), 0)

    def test_source_state_directory_is_rejected(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            units, evidence = self.make_fixture(root)
            forbidden = root / "src" / "main" / "exact"
            forbidden.mkdir()
            (forbidden / "unit.c").write_text("int forbidden;\n", encoding="utf-8")
            self.assertEqual(self.run_fixture(root, units, evidence), 1)

    def test_direct_cross_game_include_is_rejected(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            units, evidence = self.make_fixture(root)
            (root / "src" / "main" / "unit.c").write_text(
                '#include "th03/core/initexit.h"\n', encoding="utf-8"
            )
            self.assertEqual(self.run_fixture(root, units, evidence), 1)

    def test_rec98_forwarder_cannot_hide_copied_declarations(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            units, evidence = self.make_fixture(root)
            forwarder = root / "compat" / "rec98" / "th02" / "core" / "initexit.h"
            forwarder.parent.mkdir(parents=True)
            forwarder.write_text("int copied_declaration;\n", encoding="utf-8")
            self.assertEqual(self.run_fixture(root, units, evidence), 1)

    def test_assembly_reference_includes_require_native_forwarders(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            units, evidence = self.make_fixture(root)
            source = root / "src" / "main" / "unit.asm"
            source.write_text("include compat/rec98/th03/main/playfld.inc\n")
            forwarder = root / "compat" / "rec98" / "th03" / "main" / "playfld.inc"
            forwarder.parent.mkdir(parents=True)
            forwarder.write_text("include th03/main/playfld.inc\n")
            self.assertEqual(self.run_fixture(root, units, evidence), 0)
            forwarder.write_text("include th03/main/playfld.inc\nPLAYFIELD_W = 288\n")
            self.assertEqual(self.run_fixture(root, units, evidence), 1)
            forwarder.unlink()
            self.assertEqual(self.run_fixture(root, units, evidence), 1)

    def test_direct_assembly_reference_include_is_rejected(self) -> None:
        for include in ("th03/main/playfld.inc", '"libs/master.lib/macros.inc"',
                        "platform\\x86real\\types.inc"):
            with self.subTest(include=include), TemporaryDirectory() as temporary:
                root = Path(temporary)
                units, evidence = self.make_fixture(root)
                (root / "src" / "main" / "unit.asm").write_text(f"INCLUDE {include}\n")
                self.assertEqual(self.run_fixture(root, units, evidence), 1)

    def test_bounded_include_checks_c_and_assembly_dependencies(self) -> None:
        for line in ('#include "th03/main/playfld.inc"',
                     'INCLUDE "th03\\main\\playfld.inc"'):
            with self.subTest(line=line), TemporaryDirectory() as temporary:
                root = Path(temporary)
                units, evidence = self.make_fixture(root)
                (root / "src" / "main" / "unit.inl").write_text(line + "\n")
                self.assertEqual(self.run_fixture(root, units, evidence), 1)

    def test_adversarial_exact_claims_fail_closed(self) -> None:
        mutations = {
            "evidence reused by another unit": lambda units, evidence: next(
                row for row in evidence if row["oracle"] == "raw-bytes"
            ).update({"unit_id": "unit-main-200"}),
            "blank replay metadata": lambda units, evidence: next(
                row for row in evidence if row["oracle"] == "raw-bytes"
            ).update({"command": ""}),
            "unequal raw hashes": lambda units, evidence: next(
                row for row in evidence if row["oracle"] == "raw-bytes"
            ).update({"output_sha256": "2" * 64}),
            "missing source": lambda units, evidence: units[0].update(
                {"source": "src/missing.c"}
            ),
            "missing address": lambda units, evidence: units[0].update({"segment": ""}),
            "extent outside artifact": lambda units, evidence: units[0].update(
                {"file_offset": "156250"}
            ),
            "private replay driver": lambda units, evidence: units[0].update(
                {"replay_command": "python3 .analysis/fake.py"}
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name), TemporaryDirectory() as temporary:
                root = Path(temporary)
                units, evidence = self.make_fixture(root)
                mutate(units, evidence)
                self.assertEqual(self.run_fixture(root, units, evidence), 1)

    def test_exact_function_requires_exact_authored_owner(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            units, evidence = self.make_fixture(root)
            function = {field: "" for field in FUNCTION_HEADER}
            function.update(
                {
                    "id": "fn-main-104",
                    "artifact": "th03-main",
                    "address": "0x10104",
                    "file_offset": "0x104",
                    "size": "4",
                    "boundary_state": "reviewed",
                    "state": "exact",
                    "name": "fixture_function",
                    "owner_unit": "unit-main-100",
                    "source": "src/main/unit.c",
                    "evidence_ids": "ev-boundary-ownership",
                    "notes": "synthetic reviewed function",
                }
            )
            self.assertEqual(self.run_fixture(root, units, evidence, [function]), 0)

            function["owner_unit"] = "unit-main-200"
            self.assertEqual(self.run_fixture(root, units, evidence, [function]), 1)

    def test_exact_function_cannot_escape_owner_or_use_provisional_boundary(self) -> None:
        for name, mutation in (
            ("escape owner", {"file_offset": "0x10F", "size": "4"}),
            ("provisional boundary", {"boundary_state": "provisional"}),
        ):
            with self.subTest(name=name), TemporaryDirectory() as temporary:
                root = Path(temporary)
                units, evidence = self.make_fixture(root)
                function = {field: "" for field in FUNCTION_HEADER}
                function.update(
                    {
                        "id": "fn-main-104",
                        "artifact": "th03-main",
                        "address": "0x10104",
                        "file_offset": "0x104",
                        "size": "4",
                        "boundary_state": "reviewed",
                        "state": "exact",
                        "name": "fixture_function",
                        "owner_unit": "unit-main-100",
                        "source": "src/main/unit.c",
                        "evidence_ids": "ev-boundary-ownership",
                        "notes": "synthetic reviewed function",
                    }
                )
                function.update(mutation)
                self.assertEqual(self.run_fixture(root, units, evidence, [function]), 1)


class Rec98ForwarderTests(unittest.TestCase):
    GUARDED_HEADERS = (
        ("th03/main/chars/speed.hpp", "TH03_COMPAT_REC98_MAIN_CHARS_SPEED_HPP"),
        ("th03/hardware/input.h", "TH03_COMPAT_REC98_HARDWARE_INPUT_H"),
        ("th03/main/player/cur.hpp", "TH03_COMPAT_REC98_MAIN_PLAYER_CUR_HPP"),
    )

    @staticmethod
    def guarded_content(relative: str, guard: str) -> str:
        return f'#ifndef {guard}\n#define {guard}\n\n#include "{relative}"\n\n#endif\n'

    @staticmethod
    def make_forwarder(root: Path, relative: str, content: str) -> Path:
        source = root / "src/main/unit.c"
        source.parent.mkdir(parents=True, exist_ok=True)
        if relative.endswith(".inc"):
            source = source.with_suffix(".asm")
            include = f"include compat/rec98/{relative}\n"
        else:
            include = f'#include "compat/rec98/{relative}"\n'
        source.write_text(include, encoding="utf-8")
        forwarder = root / "compat/rec98" / relative
        forwarder.parent.mkdir(parents=True, exist_ok=True)
        forwarder.write_text(content, encoding="utf-8")
        return forwarder

    def test_unguarded_cpp_and_assembly_forwarders_still_pass(self) -> None:
        for relative in (
            *(relative for relative, _ in self.GUARDED_HEADERS),
            "th03/core/initexit.h", "th03/main/playfld.inc",
        ):
            with self.subTest(relative=relative), TemporaryDirectory() as temporary:
                root = Path(temporary)
                content = (f"include {relative}\n" if relative.endswith(".inc")
                           else f'#include "{relative}"\n')
                self.make_forwarder(root, relative, content)
                validate_source_tree(root)

    def test_reviewed_guards_accept_only_line_padding_and_blank_lines(self) -> None:
        for relative, guard in self.GUARDED_HEADERS:
            content = self.guarded_content(relative, guard)
            variants = (
                content,
                "\n \t\n" + "\n".join(" \t" + line + " \t"
                                          for line in content.split("\n")),
                content.rstrip("\n"),
            )
            for index, variant in enumerate(variants):
                with self.subTest(relative=relative, variant=index), TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self.make_forwarder(root, relative, variant)
                    validate_source_tree(root)

    def test_guarded_forwarders_reject_extra_or_malformed_content(self) -> None:
        for relative, guard in self.GUARDED_HEADERS:
            content = self.guarded_content(relative, guard)
            include = f'#include "{relative}"'
            other_guard = next(value for _, value in self.GUARDED_HEADERS if value != guard)
            mutations = {
                "empty": "",
                "missing define": content.replace(f"#define {guard}\n", ""),
                "mismatched guard": content.replace(f"#define {guard}", "#define OTHER_GUARD"),
                "unapproved matching guard": content.replace(guard, "OTHER_GUARD"),
                "other reviewed guard": content.replace(guard, other_guard),
                "valued guard": content.replace(f"#define {guard}", f"#define {guard} 1"),
                "function-like guard": content.replace(f"#define {guard}", f"#define {guard}()"),
                "wrong include": content.replace(include, '#include "th03/other.h"'),
                "traversal include": content.replace(include, f'#include "../{relative}"'),
                "angle include": content.replace(include, f"#include <{relative}>"),
                "duplicate include": content.replace(include, include + "\n" + include),
                "additional include": content.replace(include, include + '\n#include "other.h"'),
                "extra definition": content.replace(include, "#define EXTRA\n" + include),
                "nested conditional": content.replace(include, "#if ENABLED\n" + include + "\n#endif"),
                "conditional alternate": content.replace("#endif", '#else\n#include "other.h"\n#endif'),
                "conditional elif": content.replace("#endif", "#elif ENABLED\n#endif"),
                "undefinition": content.replace("#endif", f"#undef {guard}\n#endif"),
                "layout pragma": content.replace(include, "#pragma pack(1)\n" + include),
                "declaration": content.replace(include, include + "\nint extra;"),
                "code outside guard": content + "int extra;\n",
                "comment": content.replace("#endif", "#endif // guard"),
                "line continuation": content.replace(f"#ifndef {guard}\n", f"#ifndef {guard}\\\n"),
                "missing endif": content.replace("#endif", ""),
                "duplicate endif": content + "#endif\n",
                "endif tokens": content.replace("#endif", "#endif extra"),
                "non-newline separator": content.replace("\n", "\v"),
            }
            for name, mutated in mutations.items():
                with self.subTest(relative=relative, mutation=name), TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self.make_forwarder(root, relative, mutated)
                    with self.assertRaisesRegex(ValueError, "forwarding header must contain only"):
                        validate_source_tree(root)

    def test_other_paths_cannot_use_guards(self) -> None:
        for relative in ("th03/core/initexit.h", "th03/main/playfld.inc"):
            with self.subTest(relative=relative), TemporaryDirectory() as temporary:
                root = Path(temporary)
                content = self.guarded_content(relative, self.GUARDED_HEADERS[0][1])
                if relative.endswith(".inc"):
                    content = content.replace(f'#include "{relative}"', f"include {relative}")
                self.make_forwarder(root, relative, content)
                with self.assertRaisesRegex(ValueError, "forwarding header must contain only"):
                    validate_source_tree(root)

    def test_unguarded_forwarders_still_require_exact_content(self) -> None:
        for relative in ("th03/core/initexit.h", "th03/main/playfld.inc"):
            content = (f"include {relative}\n" if relative.endswith(".inc")
                       else f'#include "{relative}"\n')
            for mutated in (content.rstrip("\n"), "\n" + content, content + "int extra;\n",
                            content.replace(relative, "th03/wrong.h")):
                with self.subTest(relative=relative, content=mutated), TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self.make_forwarder(root, relative, mutated)
                    with self.assertRaisesRegex(ValueError, "forwarding header must contain only"):
                        validate_source_tree(root)

    def test_guarded_headers_do_not_allow_direct_product_includes(self) -> None:
        for relative, guard in self.GUARDED_HEADERS:
            with self.subTest(relative=relative), TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.make_forwarder(root, relative, self.guarded_content(relative, guard))
                (root / "src/main/unit.c").write_text(f'#include "{relative}"\n', encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "direct ReC98 include"):
                    validate_source_tree(root)

    def test_guarded_forwarders_still_reject_missing_files_and_symlinks(self) -> None:
        relative, guard = self.GUARDED_HEADERS[0]
        for mode in ("missing", "referenced symlink", "unreferenced symlink", "directory symlink"):
            with self.subTest(mode=mode), TemporaryDirectory() as temporary:
                root = Path(temporary)
                content = self.guarded_content(relative, guard)
                forwarder = self.make_forwarder(root, relative, content)
                if mode == "directory symlink":
                    (root / "compat/rec98/linked").symlink_to(root / "src", target_is_directory=True)
                else:
                    forwarder.unlink()
                    if mode != "missing":
                        target = root / "header.h"
                        target.write_text(content, encoding="utf-8")
                        forwarder.symlink_to(target)
                    if mode == "unreferenced symlink":
                        (root / "src/main/unit.c").write_text("int unit;\n", encoding="utf-8")
                message = ("forbids symlinks" if mode in {"unreferenced symlink", "directory symlink"}
                           else "missing checked-in ReC98 forwarding header")
                with self.assertRaisesRegex(ValueError, message):
                    validate_source_tree(root)


if __name__ == "__main__":
    unittest.main()
