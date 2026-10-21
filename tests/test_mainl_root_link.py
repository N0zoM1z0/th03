"""Root existing-unit and source-bound receipt controls, without native builds."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import replay_th03_mainl_root_link as replay
class RootLinkTests(unittest.TestCase):
    def recipe(self): return json.loads((ROOT/replay.RECIPE).read_text())
    def test_existing_single_unit_partition(self): replay.validate_partition(self.recipe()['unit'])
    def test_changed_range_rejected(self):
        for key in ['segment','offset','bytes']:
            unit=copy.deepcopy(self.recipe()['unit']);unit[key]+=1
            with self.assertRaises(ValueError): replay.validate_partition(unit)
    def test_missing_source_rejected(self):
        unit=copy.deepcopy(self.recipe()['unit']);unit['source_paths']=[]
        with self.assertRaises(ValueError): replay.validate_partition(unit)
    def test_recipe_mutation_rejected_before_models(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/replay.RECIPE;p.parent.mkdir();p.write_text('{}')
            with self.assertRaisesRegex(ValueError,'recipe identity'): replay.replay(root)
    def test_native_receipt_mutation_rejected(self):
        class Changed:
            def read_bytes(self): return b'{}'
        class Overlay:
            def __truediv__(self,name): return Changed() if name.endswith('/root-finished.json') else ROOT/name
        with self.assertRaisesRegex(ValueError,'retained input differs'): replay.replay(Overlay())
    def test_every_proof_pin(self):
        c=self.recipe()
        self.assertEqual(hashlib.sha256((ROOT/replay.RECIPE).read_bytes()).hexdigest(),replay.RECIPE_SHA)
        for path,h in c['proof_inputs_sha256'].items(): self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),h,path)
        self.assertFalse(c['cold_aggregate']);self.assertFalse(c['exact_acceptance'])
        self.assertEqual(len(c['builds']),2)
if __name__=='__main__': unittest.main()
