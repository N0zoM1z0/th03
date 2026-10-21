"""Bounded source composition tests; no native build or acceptance inference."""
import json,unittest
from pathlib import Path
from lib import mainl_linked_game_source as c
ROOT=Path(__file__).resolve().parents[1]
class TestLinkedGame(unittest.TestCase):
    def setUp(self):
        self.r=json.loads((ROOT/"config/th03_mainl_linked_game_source.json").read_text())
        def read(row):return (ROOT/row["path"]).read_bytes()
        self.args=(read(self.r["previous_generated_root"]),{p["name"]:read(p["provider"]) for p in self.r["providers"]},{p["name"]:read(p["wrapper"]) for p in self.r["providers"]},{p["name"]:read(p["source"]) for p in self.r["providers"]},read(self.r["staff_source"]),self.r)
    def test_scope(self):
        self.assertEqual((len(self.r["units"]),sum(u["bytes"] for u in self.r["units"])),(23,1765))
        self.assertEqual(len({u["unit_id"] for u in self.r["units"]}),23)
        self.assertEqual(sum(u["bytes"] for u in self.r["units"] if "producer-" in u["unit_id"]),4)
        self.assertFalse(self.r["exact_acceptance"]);self.assertFalse(self.r["source_progress_changed"])
    def test_generate_and_expand(self):
        out=c.compose(*self.args);self.assertEqual(len(out),32+len(self.r["compatibility_inputs"]))
        raw=c.lf(out["th03_mainl.asm"]);path=self.r["staff_source"]["path"]
        expanded=raw.replace(("include "+path+"\n").encode(),c.lf(out[path])[len(c.ASM_HEADER):],1)
        self.assertEqual(expanded,c.lf(self.args[0]))
        for p in self.r["providers"]:
            body=c.lf(out[p["source"]["path"]])[len(c.CPP_HEADER):]
            for shim in self.r["compatibility_inputs"]:
                body=body.replace(('#include "'+shim["path"]+'"').encode(),('#include "'+shim["original_include"]+'"').encode())
            self.assertEqual(body,c.lf(self.args[1][p["name"]]))
    def test_body_mutation_rejected(self):
        args=list(self.args);args[3]=dict(args[3]);args[3]["input_sense"]+=b"\nasm nop;\n"
        with self.assertRaises(ValueError):c.compose(*args)
    def test_wrapper_mutation_rejected(self):
        args=list(self.args);args[2]=dict(args[2]);args[2]["win"]+=b"\n"
        with self.assertRaises(ValueError):c.compose(*args)
    def test_staff_far_pointer_rejected(self):
        args=list(self.args);args[4]=args[4].replace(b"push\tdword ptr",b"push\tword ptr")
        self.assertNotEqual(args[4],self.args[4])
        with self.assertRaises(ValueError):c.compose(*args)
    def test_context_nop_retained(self):
        raw=self.args[3]["input_sense"];self.assertTrue(raw.rstrip().endswith(b'\x23pragma codestring "\\x90"'))
        self.assertFalse(any(u["offset"]==0x529 for u in self.r["units"]))
    def test_actual_first_use_slots(self):
        self.assertEqual([(p["game"],p["binary"]) for p in self.r["providers"]],[(1,"O"),(2,"O"),(2,"O"),(2,"M"),(2,"O"),(3,"O"),(3,"O"),(3,"O"),(3,"M"),(3,"M"),(3,"M"),(3,"L"),(3,"L"),(3,"L"),(3,"L")])
    def test_staff_context_interface(self):
        self.assertIn(b"@FLAKE_PUT$QIII procdesc",self.args[4])
        self.assertEqual(sum(u["bytes"] for u in self.r["units"] if u["producer"]=="staff_flow"),348)
if __name__=="__main__":unittest.main()
