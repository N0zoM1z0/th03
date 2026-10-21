"""Strict hybrid diagnostic OMF/MAP schemas; no equality normalization."""
import importlib.util,struct,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('hybrid_verify',ROOT/'scripts/verify_th03_zun_driver_hybrid.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def record(kind,data):
 x=bytes([kind])+struct.pack('<H',len(data)+1)+data;return x+bytes([-sum(x)&255])
def object_fixture(publics=None):
 parts=[record(0x80,b'\0'),record(0x98,b'\x48\x80\x11\x02\x03\x01'),record(0x98,b'\x48\0\0\x04\x05\x01')]
 for name,address in (publics or v.PUBLICS).items():
  n=name.encode();parts.append(record(0x90,b'\1\1'+bytes([len(n)])+n+struct.pack('<H',address)+b'\0'))
 return b''.join(parts)+record(0x8a,b'\0')
def map_fixture(publics=None):
 rows=publics or v.PUBLICS
 header=' Start Stop Length Name Class\n 00000H 0117FH 01180H _TEXT CODE\n 01180H 01180H 00000H _DATA DATA\n'
 return (header+''.join('\n Address Publics by '+mode+'\n'+''.join(' 0000:%05X idle %s\n'%(address,name) for name,address in rows.items()) for mode in ('Name','Value'))).encode()
class HybridTests(unittest.TestCase):
 def test_six_boundaries(self):
  self.assertEqual(v.omf(object_fixture())['publics'],v.PUBLICS)
  self.assertEqual(v.map_boundaries(map_fixture()),[v.PUBLICS,v.PUBLICS])
 def test_fourteen_boundaries(self):
  rows=v.PUBLICS|{n:a for n,a,b in v.RESIDENT_PROCS}
  self.assertEqual(v.omf(object_fixture(rows),rows)['publics'],rows)
  self.assertEqual(v.map_boundaries(map_fixture(rows),rows),[rows,rows])
 def test_thirty_boundaries(self):
  rows=v.PUBLICS|{n:a for n,a,b in v.RESIDENT_PROCS+v.COMMAND_PROCS}
  self.assertEqual(len(rows),31)
  self.assertEqual(v.omf(object_fixture(rows),rows)['publics'],rows)
  self.assertEqual(v.map_boundaries(map_fixture(rows),rows),[rows,rows])
 def test_bad_checksums_and_truncation(self):
  for raw in (object_fixture()[:-1],object_fixture()[:-1]+b'\x55'):
   with self.assertRaises(ValueError):v.omf(raw)
 def test_changed_or_missing_boundary(self):
  rows=dict(v.PUBLICS);rows[v.NAMES[0]]+=1
  for fn,raw in ((v.omf,object_fixture(rows)),(v.map_boundaries,map_fixture(rows))):
   with self.assertRaises(ValueError):fn(raw)
  del rows[v.NAMES[0]]
  with self.assertRaises(ValueError):v.map_boundaries(map_fixture(rows))
 def test_target_identity_not_synthesized(self):
  raw=b'0'*4224
  with self.assertRaisesRegex(ValueError,'identity'):v.verify(object_fixture(),raw,map_fixture(),raw,raw)
 def test_unknown_scope(self):
  with self.assertRaisesRegex(ValueError,'scope'):v.verify(b'',b'',b'',b'',b'',scope='arbitrary')
if __name__=='__main__':unittest.main()
