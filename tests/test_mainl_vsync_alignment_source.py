"""Pure source tests; native producer evidence is checked by the separate replay."""
import hashlib
import importlib.util
import os
from pathlib import Path
import unittest
ROOT=Path.cwd()
PAYLOAD=Path(os.environ.get('TH03_MAINL_ALIGNMENT_PAYLOAD',ROOT))
spec=importlib.util.spec_from_file_location('mainl_alignment',PAYLOAD/'scripts/lib/mainl_vsync_alignment_source.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
def reference(path):
 import subprocess
 return subprocess.check_output(['git','show','b6ba5b0a529edbb31efdf8c0e939263804f8ee47:'+path],cwd=ROOT/'_reference/ReC98')
class AlignmentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=reference('th03_mainl.asm');cls.original=reference('libs/master.lib/vs[data].asm');cls.cdg=reference('th03/formats/cdg[data].asm')
  cls.source=(PAYLOAD/c.SOURCE).read_bytes();cls.maintained_cdg=(PAYLOAD/c.CDG_SOURCE).read_bytes()
 def args(self):return [self.root,self.original,self.source,self.cdg,self.maintained_cdg]
 def test_reversible_root_edits(self):
  raw=c.compose(*self.args())['th03_mainl.asm']
  raw=raw.replace(b'mainl_data_origin label byte\n',b'').replace(('include '+c.SOURCE+'\n').encode(),b'include libs/master.lib/vs[data].asm\n').replace(('include '+c.CDG_SOURCE+'\n').encode(),b'include th03/formats/cdg[data].asm\n').replace(b"_CUTSCENE_KANJI\tdb  '  ', 0\n\tevendata\n",b"_CUTSCENE_KANJI\tdb  '  ', 0\n\teven\n")
  self.assertEqual(raw,c.lf(self.root))
 def test_declarations_preserved(self):
  body=self.source[self.source.index(b'\tpublic _vsync_Proc'):].replace(b'    mainl_vsync_storage_even mainl_data_origin\n',b'\tEVEN\n')
  self.assertEqual(body,c.lf(self.original))
  self.assertEqual(self.maintained_cdg.replace(b'\tevendata\n',b'\talign 2\n'),c.lf(self.cdg))
 def test_symbolic_parity(self):
  self.assertIn(b'if (($ - origin) and 1)\n        nop\n    endif',self.source)
  for n in range(64):self.assertEqual(n+(n&1),(n+1)&~1)
 def test_no_target_literal(self):
  for bad in [b'90h',b'0x90',b'60473',b'0849',b'org ',b'dup(']:self.assertNotIn(bad,self.source.lower())
 def test_provider_mutations_rejected(self):
  for i in range(1,5):
   args=self.args();args[i]+=b'; drift'
   with self.assertRaises(ValueError):c.compose(*args)
 def test_duplicate_anchor_rejected(self):
  for extra in [b'\t.data\n',b'include libs/master.lib/vs[data].asm\n',b'include th03/formats/cdg[data].asm\n',b'mainl_data_origin']:
   args=self.args();args[0]+=extra
   with self.assertRaises(ValueError):c.compose(*args)
 def test_repeat_composition_rejected(self):
  args=self.args();args[0]=c.compose(*args)['th03_mainl.asm']
  with self.assertRaises(ValueError):c.compose(*args)
if __name__=='__main__':unittest.main()
