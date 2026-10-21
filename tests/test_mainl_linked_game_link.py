"""LinkedGame existing-unit and source-bound receipt controls, without native builds."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import replay_th03_mainl_linked_game_link as replay
class LinkedGameLinkTests(unittest.TestCase):
    def recipe(self):return json.loads((ROOT/replay.RECIPE).read_text())
    def test_existing_twenty_three_unit_partition(self):replay.validate_partition(self.recipe()["units"])
    def test_changed_range_rejected(self):
        for key in ("segment","offset","bytes"):
            unit=copy.deepcopy(self.recipe()["units"]);unit[0][key]+=1
            with self.assertRaises(ValueError):replay.validate_partition(unit)
    def test_missing_source_rejected(self):
        unit=copy.deepcopy(self.recipe()["units"]);unit[0]["source_paths"]=[]
        with self.assertRaises(ValueError):replay.validate_partition(unit)
    def test_recipe_mutation_rejected_before_models(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/replay.RECIPE;p.parent.mkdir();p.write_text("{}")
            with self.assertRaisesRegex(ValueError,"recipe identity"):replay.replay(root)
    def test_native_receipt_mutation_rejected(self):
        class Changed:
            def read_bytes(self):return b"{}"
        class Overlay:
            def __truediv__(self,name):return Changed() if name.endswith("/root-finished.json") else ROOT/name
        with self.assertRaisesRegex(ValueError,"retained input differs"):replay.replay(Overlay())
    def test_model_receipt_mutation_rejected(self):
        model=self.recipe()["model_phases"]["sound"]["candidate"]
        class Changed:
            def read_bytes(self):return b"{}"
        class Overlay:
            def __truediv__(self,name):return Changed() if name==model else ROOT/name
        with self.assertRaisesRegex(ValueError,"retained input differs"):replay.replay(Overlay())
    def test_unrelated_progress_is_not_live_model_dependency(self):
        self.assertNotIn("scripts/progress.py",self.recipe()["proof_inputs_sha256"])
        class Changed:
            def read_bytes(self):return b"unrelated presentation changed"
        class Overlay:
            def __truediv__(self,name):return Changed() if name=="scripts/progress.py" else ROOT/name
        self.assertTrue(replay.replay(Overlay())["runtime_observations_equal"])
    def test_actual_model_dependency_mutation_rejected(self):
        class Changed:
            def read_bytes(self):return b"changed model"
        class Overlay:
            def __truediv__(self,name):return Changed() if name=="scripts/review_th03_mainl_sound.py" else ROOT/name
        with self.assertRaisesRegex(ValueError,"retained input differs"):replay.replay(Overlay())
    def test_only_each_original_model_hash_field_is_excluded(self):
        row=dict(before_sha256="a",after_sha256="b",memory_before_sha256="m-a",memory_after_sha256="m-b",events=["kept"])
        exclusions={"input":("before_sha256","after_sha256"),"sound":("before_sha256","after_sha256"),"linked_tail":("memory_before_sha256","memory_after_sha256")}
        for name in ("lifecycle","input","sound","linked_tail","staff","cfg_windows"):
            normalized=replay.comparable([row],name)[0]
            self.assertEqual(normalized,{k:v for k,v in row.items() if k not in exclusions.get(name,())})
        with self.assertRaises(ValueError):replay.comparable([row],"unknown")
    def test_scanner_context_and_crt_do_not_gain_source_credit(self):
        units=self.recipe()["units"]
        self.assertFalse(any("crt-" in u["unit_id"] or u["offset"]==0x529 for u in units))
        self.assertEqual(sum(u["bytes"] for u in units if "producer-" in u["unit_id"]),4)
    def test_prior_resource_and_archive_units_are_not_new_units(self):
        units=self.recipe()['units']
        self.assertEqual(len(units),23)
        self.assertEqual(sum(u['bytes'] for u in units),1765)
        self.assertFalse(any(u['unit_id'].endswith(('buffer-dos-open','dos-close','gdc-outpw','palette-bfnt','heap')) for u in units))
    def test_every_proof_pin(self):
        c=self.recipe()
        self.assertEqual(hashlib.sha256((ROOT/replay.RECIPE).read_bytes()).hexdigest(),replay.RECIPE_SHA)
        for path,h in c["proof_inputs_sha256"].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),h,path)
        self.assertFalse(c["cold_aggregate"]);self.assertFalse(c["exact_acceptance"])
        self.assertEqual(len(c["builds"]),2)
        self.assertTrue(all(len(b["groups"])==4 for b in c["builds"]))
if __name__=="__main__":unittest.main()
