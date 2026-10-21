import unittest
from pathlib import Path
from lib.mainl_graphics_source import generate
from lib.mainl_graphics_link import check_far_pointer_call
import replay_th03_mainl_graphics_link as replay
ROOT=Path(__file__).resolve().parents[1]
FIXTURE=b"""group_01 group CFG_LRES_TEXT, MAINL_SC_TEXT, CUTSCENE_TEXT, SCOREDAT_TEXT, REGIST_TEXT, STAFF_TEXT, mainl_03_TEXT
mainl_03_TEXT segment byte public 'CODE' use16
include th03/formats/cdg_unput_upwards.asm
sub_BB51\tproc near
sub_BB51\tendp
include th03/formats/cdg_put_dissolve.asm
mainl_03_TEXT\tends
byte_10BC7\tdb ?
byte_10BB5\tdb ?
include th03/formats/cdg_put_dissolve[data].asm
\t\tcall\t@cutscene_script_load$qnxc pascal, [off_EE4E]
"""
class GraphicsLinkTests(unittest.TestCase):
 def source(self):return (ROOT/'src/mainl/formats/cdg_effects.cpp').read_bytes()
 def test_source_split_preserves_group_and_symbols(self):
  out=generate(FIXTURE,self.source());root=out['th03_mainl.asm']
  self.assertIn(b'mainl_03_TEXT, MAINL_SNOW_TEXT, MAINL_DISSOLVE_TEXT, MAINL_STAFF_TEXT',root)
  self.assertEqual(root.count(b'label byte'),2)
  self.assertEqual(root.count(b'label word'),1)
  self.assertNotIn(b'sub_BB51',root)
  self.assertNotIn(b'include th03/formats/cdg_put_dissolve.asm',root)
 def test_function_partition(self):
  out=generate(FIXTURE,self.source())
  self.assertIn(b'void near pascal cdg_unput_for_upwards_motion_e_8(',out['gfxpre.cpp'])
  self.assertNotIn(b'void near pascal cdg_put_dissolve_e_8(',out['gfxpre.cpp'])
  self.assertNotIn(b'void near pascal cdg_unput_for_upwards_motion_e_8(',out['gfxdis.cpp'])
  self.assertIn(b'void near pascal cdg_put_dissolve_e_8(',out['gfxdis.cpp'])
 def test_missing_or_duplicate_boundary_fails(self):
  for raw in [FIXTURE.replace(b'byte_10BC7',b'missing'),FIXTURE+FIXTURE]:
   with self.assertRaises(ValueError):generate(raw,self.source())
 def test_far_pointer_argument_source(self):
  out=generate(FIXTURE,self.source())['th03_mainl.asm']
  self.assertIn(b'push\tdword ptr [off_EE4E]\r\n\t\tcall\t@cutscene_script_load$qnxc',out)
 def test_far_pointer_argument_instruction(self):
  check_far_pointer_call(bytes.fromhex('66ff360000e80000'))
  for wrong in ['ff360000e80000','66ff3600009a0000']:
   with self.assertRaises(ValueError):check_far_pointer_call(bytes.fromhex(wrong))
 def test_recipe_identity_required(self):
  class P:
   def read_bytes(self):return b'{}'
  class R:
   def __truediv__(self,n):return P()
  with self.assertRaisesRegex(ValueError,'recipe identity'):replay.replay(R())
 def test_native_evidence_identity_required(self):
  raw=(ROOT/replay.RECIPE).read_bytes()
  class P:
   def __init__(self,n):self.n=n
   def read_bytes(self):return raw if self.n==replay.RECIPE else b'corrupted native evidence'
  class R:
   def __truediv__(self,n):return P(n)
  with self.assertRaisesRegex(ValueError,'retained link input changed'):replay.replay(R())
if __name__=='__main__':unittest.main()
