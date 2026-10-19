import importlib.util, sys, unittest
from pathlib import Path
from types import SimpleNamespace as NS
scripts=Path(__file__).resolve().parents[1]/"scripts"
sys.path.insert(0,str(scripts))
p=scripts/"lib/th03_preservation_layout.py"
s=importlib.util.spec_from_file_location("layout",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def row(off,size,module,kind="CODE"):
 return (0x139D,off,size,kind,"HITBOX_TEXT","MAIN_04",module,28)
def rows(split=False):
 parts=[row(0x900,0x5E5,"th03/cs_mari.cpp"),row(0xEE5,0x1C1,"th03/bm_mari.cpp")] if split else [row(0x900,0x7A6,"th03/cs_mari.cpp")]
 return parts+[row(0x10A6,0xE7F,"th03_main.asm"),row(0x1F25,0x10A,"th03/hitbox.cpp")]+[row(0,0,x[6],k) for x in parts for k in ("DATA","BSS")]
def image(sites):
 return NS(relocations=[NS(linear=x,segment=0,offset=x) for x in sites])
class Tests(unittest.TestCase):
 def test_good_parts(self):
  m.check_layout(rows(),False);m.check_layout(rows(True),True)
 def test_missing_part(self):
  with self.assertRaises(ValueError):m.check_layout(rows()[1:],False)
 def test_extra_overlap(self):
  with self.assertRaises(ValueError):m.check_layout(rows()+[row(0x10A6,1,"bad.cpp")],False)
 def test_nonzero_data(self):
  with self.assertRaises(ValueError):m.check_layout(rows()+[row(0,1,"th03/cs_mari.cpp","DATA")],False)
 def test_cross_start(self):
  with self.assertRaises(ValueError):m.relocs(image([9]),10,20)
 def test_cross_end(self):
  with self.assertRaises(ValueError):m.relocs(image([19]),10,20)
 def test_order_preserved(self):
  self.assertNotEqual(m.relocs(image([12,10]),10,20),m.relocs(image([10,12]),10,20))
 def test_alias_moved(self):
  with self.assertRaises(ValueError):m.check_aliases(" 1D56:FFFF _marisa_gauge_y\n")
if __name__=="__main__":unittest.main()
