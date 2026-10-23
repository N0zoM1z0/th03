"""Fast bound-receipt/partition controls; full replay separately runs CPU models."""

# This integration suite needs an optional archived native run.
from pathlib import Path as _ArchivePath
import unittest as _archive_unittest
if not (_ArchivePath(__file__).resolve().parents[1] / '.analysis/mainl-staff-link-proposal-20261021-v01/manifest.json').is_file():
    raise _archive_unittest.SkipTest("archived native fixtures unavailable")

import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import replay_th03_mainl_staff_link as replay

class StaffLinkTests(unittest.TestCase):
 def recipe(self):return json.loads((ROOT/replay.RECIPE).read_text())
 def test_existing_eleven_units_partition3339(self):
  replay.validate_partition(self.recipe()['units'])
 def test_gap_and_overlap_rejected(self):
  for delta in (-1,1):
   units=copy.deepcopy(self.recipe()['units']);units[1]['offset']+=delta
   with self.assertRaises(ValueError):replay.validate_partition(units)
 def test_duplicate_unit_rejected(self):
  units=copy.deepcopy(self.recipe()['units']);units[1]['unit_id']=units[0]['unit_id']
  with self.assertRaises(ValueError):replay.validate_partition(units)
 def test_snow_requires_both_sources(self):
  units=copy.deepcopy(self.recipe()['units']);units[1]['source_paths']=['src/mainl/staff/snow.asm']
  with self.assertRaises(ValueError):replay.validate_partition(units)
 def test_recipe_mutation_rejected_before_models(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p=root/replay.RECIPE;p.parent.mkdir();p.write_text('{}')
   with self.assertRaisesRegex(ValueError,'recipe identity'):replay.replay(root)
 def test_native_record_mutation_rejected_before_models(self):
  class Changed:
   def read_bytes(self):return b'{}'
  class Overlay:
   def __truediv__(self,name):return Changed() if name.endswith('/root-finished.json') else ROOT/name
  with self.assertRaisesRegex(ValueError,'retained link input changed'):replay.replay(Overlay())
 def test_all_receipt_and_consumed_input_pins(self):
  c=self.recipe();self.assertEqual(hashlib.sha256((ROOT/replay.RECIPE).read_bytes()).hexdigest(),replay.RECIPE_SHA)
  for n,h in c['proof_inputs_sha256'].items():self.assertEqual(hashlib.sha256((ROOT/n).read_bytes()).hexdigest(),h,n)
  self.assertTrue(c['native_fragment_consumption_proven']);self.assertFalse(c['cold_aggregate']);self.assertFalse(c['exact_acceptance'])

if __name__=='__main__':unittest.main()
