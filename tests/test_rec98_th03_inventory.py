"""Controls for conservative intake coverage and artifact-scoped credit."""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from inventory_rec98_th03 import inventory


def fixture():
    files = {
        "Tupfile.lua": b'''-- TH03
-- ----
th03:link("op", {
 "th03/op.cpp",
})
th03:link("main", {
 "th03/main.cpp",
})
th03:link("mainl", {
 "th03/mainl.cpp",
})
-- TH04
''',
        "th03/main.cpp": b'#if OTHER_GAME\n#include "th04/branch.hpp"\n#endif\n',
        "th04/branch.hpp": b'#include "generated.asm"\n',
        "th03/op.cpp": b'', "th03/mainl.cpp": b'',
        "th03/unlinked.cpp": b'', "th03/sprites/private.bmp": b'asset',
        "th03_extra.asm": b'include th03/shared.inc\n',
        "th03/shared.inc": b'',
    }
    for path in ("th02_zuninit.asm", "th01/zunsoft.cpp",
                 "libs/sprite16/sprite16.asm", "th03/res_yume.cpp",
                 "Pipeline/zungen.c", "Pipeline/zun_stub.asm"):
        files[path] = b''
    return files


class IntakeTests(unittest.TestCase):
    def test_unlinked_files_assets_and_conditional_branches_remain_visible(self):
        rows = {r["path"]: r for r in inventory(fixture(), [])}
        self.assertEqual(rows["th03/unlinked.cpp"]["artifacts"], "unassigned")
        self.assertEqual(rows["th03/sprites/private.bmp"]["kind"], "asset-metadata-only")
        self.assertEqual(rows["th04/branch.hpp"]["artifacts"], "th03-main")
        self.assertEqual(rows["th04/branch.hpp"]["unresolved_includes"], "generated.asm")
        self.assertIn("th03/shared.inc", rows)
        self.assertFalse(any(r["reviewed_code_artifacts"] for r in rows.values()))

    def test_main_owner_cannot_grant_mainl_credit(self):
        with self.assertRaisesRegex(ValueError, "artifact differs"):
            inventory(fixture(), [{
                "artifact": "th03-mainl", "path": "th03/mainl.cpp",
                "state": "accepted-code-extents", "source": "src/main/math/polar.cpp",
                "owner_ids": "th03-main-polar", "evidence_ids": "irrelevant",
                "notes": "attempt to inherit other product acceptance",
            }])

    def test_missing_frozen_link_root_fails_instead_of_shrinking_scope(self):
        files = fixture()
        del files["th03/mainl.cpp"]
        with self.assertRaisesRegex(ValueError, "link root missing"):
            inventory(files, [])
