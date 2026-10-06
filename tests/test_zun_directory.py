"""Synthetic negative controls; no game assets or executable fixtures."""
import sys
import struct
from pathlib import Path
import unittest
import io
from contextlib import redirect_stderr
from importlib.util import find_spec

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib.zun import parse_launcher, compose_launcher, dispatch_observation, DIRECTORY_SIZE


def fixture():
    size = 16
    start = size + DIRECTORY_SIZE
    data = bytearray(b"\0" * size)
    data += struct.pack("<H", 2)
    data += b"-1      -2      " + b" " * (30 * 8)
    data += struct.pack("<33H", 0x100 + start, 0x100 + start + 2,
                        0x100 + start + 4, *([0] * 30))
    data += b"\xe8" + struct.pack("<h", 4)
    data += b"ABCD\xf3\xa4\x58\xb8\x00\x01\x50\xc3"
    return data, size


class DirectoryTests(unittest.TestCase):
    def test_complete_partition(self):
        data, size = fixture()
        result = parse_launcher(data, size)
        self.assertEqual([p["size"] for p in result["payloads"]], [2, 2])
        self.assertEqual(result["helper_offset"], len(data) - 8)

    def test_bad_directory_fields(self):
        for offset, value in [(16, 33), (18 + 16, 0), (18 + 256, 0),
                              (18 + 256 + 6, 1)]:
            data, size = fixture()
            data[offset] = value
            with self.assertRaises(ValueError):
                parse_launcher(data, size)

    def test_overlap_and_bad_call(self):
        data, size = fixture()
        data[18 + 256 + 2:18 + 256 + 4] = data[18 + 256:18 + 256 + 2]
        with self.assertRaisesRegex(ValueError, "partition"):
            parse_launcher(data, size)
        data, size = fixture()
        data[size + DIRECTORY_SIZE - 2] += 1
        with self.assertRaisesRegex(ValueError, "trailing helper"):
            parse_launcher(data, size)

    def test_helper_mutation_and_truncation(self):
        data, size = fixture()
        data[-1] = 0xcb
        with self.assertRaisesRegex(ValueError, "helper"):
            parse_launcher(data, size)
        with self.assertRaises(ValueError):
            parse_launcher(data[:20], size)

    def test_composer_rejects_bad_compiled_transfer_and_names(self):
        data, size = fixture()
        call = bytes(data[size + DIRECTORY_SIZE - 3:size + DIRECTORY_SIZE])
        helper = bytes(data[-8:])
        with self.assertRaisesRegex(ValueError, "compiled transfer"):
            compose_launcher(bytes(data[:size]), call[:2], helper, ["-1", "-2"], [b"AB", b"CD"])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            compose_launcher(bytes(data[:size]), call, helper, ["-1", "-1"], [b"AB", b"CD"])
        with self.assertRaisesRegex(ValueError, "overlong"):
            compose_launcher(bytes(data[:size]), call, helper, ["overlongname", "-2"], [b"AB", b"CD"])

    def test_composer_rejects_com_overflow(self):
        data, size = fixture()
        call = bytes(data[size + DIRECTORY_SIZE - 3:size + DIRECTORY_SIZE])
        with self.assertRaisesRegex(ValueError, "address space"):
            compose_launcher(bytes(data[:size]), call, bytes(data[-8:]), ["-1"], [b"X" * 65500])

    @unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
    def test_runtime_wrong_transfer_stops_without_escaping_the_callback(self):
        # Small synthetic wrapper: copy FCB2, copy a two-byte payload, transfer.
        payload_address = 0x100 + 24 + DIRECTORY_SIZE
        stub = (b"\xfc\xbe\x6c\x00\xbf\x5c\x00\xb9\x10\x00\xf3\xa4\xbe" +
                struct.pack("<H", payload_address) + b"\xbf\x00\x01\xb9\x02\x00\xe9" +
                struct.pack("<h", DIRECTORY_SIZE - 3))
        helper = b"\xf3\xa4\x58\xb8\x00\x01\x50\xc3"
        data = compose_launcher(stub, b"\xe8\x04\x00", helper, ["-1", "-2"], [b"AB", b"CD"])
        directory = parse_launcher(data, len(stub))
        observed = dispatch_observation(data, directory, "", "-1")
        self.assertEqual(observed["outcome"], "payload-entry")
        mutation = bytearray(data)
        mutation[directory["helper_offset"] + 4] = 1
        output = io.StringIO()
        with redirect_stderr(output):
            with self.assertRaisesRegex(ValueError, "missed the payload entry"):
                dispatch_observation(bytes(mutation), directory, "", "-1")
        self.assertEqual(output.getvalue(), "")
