"""Original root-tail statements, explicit root declarations, and producer-only ownership."""

# This integration suite needs an optional archived native run.
from pathlib import Path as _ArchivePath
import unittest as _archive_unittest
if not (_ArchivePath(__file__).resolve().parents[1] / '.analysis/toolchain/wineprefix/drive_c/MDH02/th03_mainl.asm').is_file():
    raise _archive_unittest.SkipTest("archived native fixtures unavailable")

import hashlib,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib import mainl_root_tail_source as tail
from lib.mainl_staff_source import statements
class RootTailSourceTests(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((ROOT/'config/th03_mainl_root_tail_source.json').read_text())
  def load(row):
   raw=(ROOT/row['path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256']);return raw
  self.root=load(self.c['previous_generated_root']);load(self.c['composer'])
  self.p={};self.m={}
  for unit in self.c['units']:
   for row in unit['providers']:
    raw=load(row['provider'])
    self.p[row['name']]=b'\t\tdb 0\n' if 'root_anchor' in row else raw
    self.m[row['name']]=load(row['source'])
   if 'existing_producer' in unit:load(unit['existing_producer']['source'])
 def test_statement_expansion_and_all_original_positions(self):
  out=tail.compose(self.root,self.p,self.m);before=self.root;after=out['th03_mainl.asm']
  for name,path in tail.PROVIDER_PATHS.items():
   old=('include '+path).encode();new=('include src/mainl/root_tail/'+name+'.asm').encode()
   self.assertEqual(after.count(new),1);self.assertNotIn(old,after)
   before=before.replace(old,self.p[name]);after=after.replace(new,self.m[name])
  for name in tail.ROOT_ANCHORS:
   marker=('include src/mainl/root_tail/'+name+'.asm').encode()
   self.assertEqual(after.count(marker),1);after=after.replace(marker,self.m[name].strip())
  self.assertEqual(statements(before),statements(after))
  for path in ('src/mainl/root/root.asm','src/mainl/formats/pi_decode.asm','src/mainl/archive_io/pfopen.asm'):
   self.assertIn(('include '+path).encode(),out['th03_mainl.asm'])
 def test_exact_boundaries_no_duplicate_body_credit(self):
  self.assertEqual((len(self.c['units']),sum(u['bytes'] for u in self.c['units'])),(16,722))
  self.assertEqual(self.c['body_bytes']+self.c['producer_bytes'],722)
  self.assertEqual(len(self.m),16);self.assertEqual(len(tail.NAMES),13)
  self.assertEqual(len({u['unit_id'] for u in self.c['units']}),16)
  self.assertEqual(sum('existing_producer' in u for u in self.c['units']),8)
  for field in ('source_progress_changed','native_fragment_consumption_proven','exact_acceptance'):self.assertFalse(self.c[field])
 def test_mutations_and_missing_members_rejected(self):
  for name in self.m:
   altered=dict(self.m);altered[name]+=b'\ndb 90h\n'
   with self.assertRaises(ValueError):tail.compose(self.root,self.p,altered)
   altered=dict(self.m);del altered[name]
   with self.assertRaises(ValueError):tail.compose(self.root,self.p,altered)
  for name in tail.ROOT_ANCHORS:
   altered=dict(self.m);altered[name]=b'db 90h\n'
   with self.assertRaises(ValueError):tail.compose(self.root,self.p,altered)
 def test_root_anchor_removal_duplication_and_reconsumption_rejected(self):
  for anchor in tail.ROOT_ANCHORS.values():
   marker=anchor.encode()+b'\r\n\t\tdb 0\r\n'
   self.assertEqual(self.root.count(marker),1)
   for root in (self.root.replace(marker,b''),self.root+marker,self.root.replace(marker,marker.replace(b'db 0',b'db 90h'))):
    with self.assertRaises(ValueError):tail.compose(root,self.p,self.m)
  for name,path in tail.PROVIDER_PATHS.items():
   marker=('include '+path).encode()
   for root in (self.root.replace(marker,b''),self.root+b'\n'+marker):
    with self.assertRaises(ValueError):tail.compose(root,self.p,self.m)
  with self.assertRaises(ValueError):tail.compose(tail.compose(self.root,self.p,self.m)['th03_mainl.asm'],self.p,self.m)
 def test_no_overwrite_stage(self):
  out=tail.compose(self.root,self.p,self.m)
  with tempfile.TemporaryDirectory() as tmp:
   dest=Path(tmp)/'stage';tail.stage(dest,out)
   with self.assertRaises(FileExistsError):tail.stage(dest,out)
   self.assertEqual(out,{n:(dest/n).read_bytes() for n in out})
if __name__=='__main__':unittest.main()
