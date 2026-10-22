"""Strict declared legacy encoding support must retain include-policy checks."""
from pathlib import Path
import tempfile
import unittest
from validate_tracking import SOURCE_ENCODINGS, validate_source_tree

class SourceEncodingTests(unittest.TestCase):
    def source(self, root, name, raw):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        return path

    def test_declared_cp932_source_bytes_are_preserved(self):
        for name in SOURCE_ENCODINGS:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                raw = '// 日本語\nconst char *message = "日本";\n'.encode('cp932')
                path = self.source(root, name, raw)
                validate_source_tree(root)
                self.assertEqual(path.read_bytes(), raw)

    def test_other_sources_remain_strict_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.source(root, 'src/zun/unlisted.cpp', '// 日本語\n'.encode('cp932'))
            with self.assertRaises(UnicodeDecodeError):
                validate_source_tree(root)

    def test_malformed_declared_encoding_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.source(root, 'src/zun/res_init.inl', bytes([0x81]))
            with self.assertRaises(UnicodeDecodeError):
                validate_source_tree(root)

    def test_cp932_does_not_bypass_direct_include_rejection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.source(root, 'src/zun/res_init.inl', '// 日本語\n#include "th03/common.h"\n'.encode('cp932'))
            with self.assertRaisesRegex(ValueError, 'direct ReC98 include'):
                validate_source_tree(root)

    def test_cp932_still_requires_real_compat_forwarder(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.source(root, 'src/zun/res_init.inl', '// 日本語\n#include "compat/rec98/th03/common.h"\n'.encode('cp932'))
            with self.assertRaisesRegex(ValueError, 'missing checked-in'):
                validate_source_tree(root)
            self.source(root, 'compat/rec98/th03/common.h', b'#include "th03/common.h"\n')
            validate_source_tree(root)
