"""Source-closure controls independent of native tools and old build receipts."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib.zun_work_source import include_closure


class ZunSourceClosureTests(unittest.TestCase):
    def test_relative_include_precedes_the_root_search_path(self):
        data = {"src/a.cpp": b'#include "same.hpp"\n',
                "src/same.hpp": b"local declaration\n", "same.hpp": b"different declaration\n"}
        files, external = include_closure(data, ["src/a.cpp"])
        self.assertEqual(set(files), {"src/a.cpp", "src/same.hpp"})
        self.assertEqual(external, [])

    def test_forwarding_and_parent_paths_close_without_unrelated_files(self):
        data = {"src/a.cpp": b'#include "../compat/fwd.hpp"\n',
                "compat/fwd.hpp": b'#include "vendor/header.hpp"\n',
                "vendor/header.hpp": b"declaration\n", "old.obj": b"not a source input"}
        files, external = include_closure(data, ["src/a.cpp"])
        self.assertEqual(set(files), {"src/a.cpp", "compat/fwd.hpp", "vendor/header.hpp"})
        self.assertEqual(external, [])

    def test_cycles_terminate_and_vendor_includes_remain_explicit(self):
        data = {"a.hpp": b'#include "b.hpp"\n#include <math.h>\n',
                "b.hpp": b'#include "a.hpp"\n'}
        files, external = include_closure(data, ["a.hpp"])
        self.assertEqual(set(files), set(data))
        self.assertEqual(external, [dict(source="a.hpp", include="math.h")])

    def test_missing_root_cannot_fall_back_to_a_retained_product(self):
        with self.assertRaisesRegex(ValueError, "missing source dependency"):
            include_closure({"a.obj": b"old native output"}, ["a.cpp"])


if __name__ == "__main__":
    unittest.main()
