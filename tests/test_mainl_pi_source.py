"""Read-only complete PI source contracts; no native compiler invocation."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib import mainl_pi_source as pi
from lib.mainl_staff_source import statements

class PiSourceTests(unittest.TestCase):
    def setUp(self):
        self.c = json.loads((ROOT / "config/th03_mainl_pi_source.json").read_text())
        for key in ("previous_generated_root", "provider", "source", "composer"):
            row = self.c[key]
            raw = (ROOT / row["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row["sha256"])
            setattr(self, key, raw)
    def test_complete_statement_identity_and_consumption(self):
        out = pi.compose(self.previous_generated_root, self.provider, self.source)
        marker = ("include " + pi.SOURCE).encode()
        self.assertEqual(out["th03_mainl.asm"].count(marker), 1)
        self.assertEqual(statements(out["th03_mainl.asm"].replace(marker, out[pi.SOURCE])),
                         statements(self.previous_generated_root.replace(pi.PROVIDER, self.provider)))
        self.assertIn(b"include libs/master.lib/graph_pi_free.asm", out["th03_mainl.asm"])
        self.assertIn(b"include src/mainl/root/root.asm", out["th03_mainl.asm"])
    def test_partition_and_abi(self):
        self.assertEqual(self.c["body_bytes"] + len(self.c["outer_even_offsets"]), 1524)
        self.assertEqual(self.c["ordered_relocations"], [[0,4156],[0,4384],[0,4473],[0,5356]])
        self.assertEqual(self.source.count(b"ret\t(DATASIZE+DATASIZE+DATASIZE)*2"), 2)
        for name in (b"_too",b"_tor",b"_bitl",b"_bitl8",b"_bitl1"):
            self.assertIn(name+b"\tmacro", self.source)
        self.assertFalse(self.c["exact_acceptance"])
        self.assertFalse(self.c["source_progress_changed"])
    def test_instructions_branches_and_padding_rejected(self):
        for old,new in [(b"\tCLD",b"\tSTD"),(b"jc\tshort _minfo_skipB",b"jnc\tshort _minfo_skipB"),(b"\tpopa",b"\tpop\tax")]:
            altered=self.source.replace(old,new,1)
            self.assertNotEqual(altered,self.source)
            with self.assertRaises(ValueError): pi.compose(self.previous_generated_root,self.provider,altered)
        with self.assertRaises(ValueError): pi.compose(self.previous_generated_root,self.provider,self.source+b"\ndb 90h\n")
        with self.assertRaises(ValueError): pi.compose(self.previous_generated_root,self.provider,self.source.replace(b"_buffer_load endp",b""))
    def test_duplicate_missing_and_reconsumed_boundary_rejected(self):
        for carrier in (self.previous_generated_root+pi.PROVIDER,self.previous_generated_root.replace(pi.PROVIDER,b""),pi.compose(self.previous_generated_root,self.provider,self.source)["th03_mainl.asm"]):
            with self.assertRaises(ValueError): pi.compose(carrier,self.provider,self.source)
    def test_no_overwrite_stage(self):
        out=pi.compose(self.previous_generated_root,self.provider,self.source)
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)/"new"
            pi.stage(dest,out)
            before={name:(dest/name).read_bytes() for name in out}
            with self.assertRaises(FileExistsError): pi.stage(dest,out)
            self.assertEqual(before,{name:(dest/name).read_bytes() for name in out})
if __name__ == "__main__": unittest.main()
