import importlib.util, unittest
from pathlib import Path
from datetime import datetime,timezone
from types import SimpleNamespace as NS
p=Path(__file__).resolve().parents[1]/"scripts/verify_th03_main_preservation.py"
s=importlib.util.spec_from_file_location("preserve",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def fixture():
 gate={"raw_equal":True,"relocations_equal":True}
 rd=lambda i:dict(round=i,fresh_owned_objects=True,behavior_pass=True,units=[gate.copy() for _ in range(74)],functions=[gate.copy() for _ in range(334)],producer_ranges=[],auxiliary_map_contributions=[])
 return dict(kind="th03-main-owned-extent-cold-replay",**{"pass":True},target_sha256=m.TARGET_SHA,
 observed_utc="2026-10-19T05:00:00+00:00",candidate_manifest=None,selected_units=["a"],aggregate_units=["a"],
 owned_extent_bytes=53122,rounds=[rd(1),rd(2)],objects_metadata_normalized_equal=True,candidate_equal=True,
 all_products_equal=True,game_objects_metadata_normalized_equal=True)
cut=datetime(2026,10,19,4,55,tzinfo=timezone.utc)
class Tests(unittest.TestCase):
 def test_valid_shape(self):m.receipt_shape(fixture(),False,cut)
 def test_missing_gate(self):
  r=fixture();r.pop("pass")
  with self.assertRaises(ValueError):m.receipt_shape(r,False,cut)
 def test_failed_gate(self):
  r=fixture();r["rounds"][1]["units"][0]["relocations_equal"]=False
  with self.assertRaises(ValueError):m.receipt_shape(r,False,cut)
 def test_old_receipt(self):
  r=fixture();r["observed_utc"]="2026-10-18T05:00:00+00:00"
  with self.assertRaises(ValueError):m.receipt_shape(r,False,cut)
 def test_missing_round(self):
  r=fixture();r["rounds"].pop()
  with self.assertRaises(ValueError):m.receipt_shape(r,False,cut)
 def test_partial_scope(self):
  r=fixture();r["selected_units"]=[]
  with self.assertRaises(ValueError):m.receipt_shape(r,False,cut)
 def test_role_mismatch(self):
  with self.assertRaises(ValueError):m.receipt_shape(fixture(),True,cut)
 def test_literal_order_and_duplicates(self):
  image=NS(relocations=[NS(linear=1,segment=0,offset=1),NS(linear=1,segment=0,offset=1),NS(linear=3,segment=0,offset=3)])
  self.assertEqual(m.outside_relocs(image),[(0,1),(0,1),(0,3)])
 def test_cross_boundary(self):
  image=NS(relocations=[NS(linear=m.LO-1,segment=0,offset=m.LO-1)])
  with self.assertRaises(ValueError):m.outside_relocs(image)
if __name__=="__main__":unittest.main()
