"""RootTail existing-unit and source-bound receipt controls, without native builds."""

# This integration suite needs an optional archived native run.
from pathlib import Path as _ArchivePath
import unittest as _archive_unittest
if not (_ArchivePath(__file__).resolve().parents[1] / '.analysis/toolchain/wineprefix/drive_c/MDH02/th03_mainl.asm').is_file():
    raise _archive_unittest.SkipTest("archived native fixtures unavailable")

import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import replay_th03_mainl_root_tail_link as replay
class RootTailLinkTests(unittest.TestCase):
    def recipe(self):return json.loads((ROOT/replay.RECIPE).read_text())
    def test_existing_sixteen_unit_partition(self):replay.validate_partition(self.recipe()["units"])
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
        model=self.recipe()["model_phases"]["tail"]["candidate"]
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
            def __truediv__(self,name):return Changed() if name=="scripts/review_th03_mainl_root_tail.py" else ROOT/name
        with self.assertRaisesRegex(ValueError,"retained input differs"):replay.replay(Overlay())
    def test_only_each_original_model_hash_field_is_excluded(self):
        row=dict(data_before_sha256='data-a',data_after_sha256='data-b',memory_before_sha256='memory-a',memory_after_sha256='memory-b',events=['kept'])
        for name in ('tail',):
            normalized=replay.comparable([row],name)[0]
            self.assertNotIn('memory_before_sha256',normalized)
            self.assertNotIn('memory_after_sha256',normalized)
            self.assertNotIn('data_before_sha256',normalized)
            self.assertNotIn('data_after_sha256',normalized)
            self.assertEqual(normalized['events'],['kept'])
        with self.assertRaises(ValueError):replay.comparable([row],'unknown')
    def test_prior_resource_and_archive_units_are_not_new_units(self):
        units=self.recipe()['units']
        self.assertEqual(len(units),16)
        self.assertEqual(sum(u['bytes'] for u in units),722)
        self.assertFalse(any(u['unit_id'].endswith(('buffer-dos-open','dos-close','gdc-outpw','palette-bfnt','heap')) for u in units))
    def test_every_proof_pin(self):
        c=self.recipe()
        self.assertEqual(hashlib.sha256((ROOT/replay.RECIPE).read_bytes()).hexdigest(),replay.RECIPE_SHA)
        for path,h in c["proof_inputs_sha256"].items():self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),h,path)
        self.assertFalse(c["cold_aggregate"]);self.assertFalse(c["exact_acceptance"])
        self.assertEqual(len(c["builds"]),2)
if __name__=="__main__":unittest.main()
