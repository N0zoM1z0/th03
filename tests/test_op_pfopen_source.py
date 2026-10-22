import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pfopen_stage',ROOT/'scripts/stage_th03_op_pfopen_source.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
class PFOpenSource(unittest.TestCase):
 def setUp(self):self.c,self.overlay=s.read_inputs(ROOT)
 def test_complete_source_and_headers(self):
  self.assertEqual(len(self.overlay),13);self.assertIn(b'PFOPEN',self.overlay['th03/formats/pfopen.asm']);self.assertEqual(self.c['size'],281)
 def test_exact_path_attributes(self):
  a=(ROOT/'.gitattributes').read_text().splitlines()
  for n in [self.c['source']]+[q['path'] for q in self.c['compatibility_closure']]:self.assertIn(n+' -text',a)
 def test_utf8_and_crlf_preserved(self):
  for b in self.overlay.values():b.decode('utf8')
  self.assertIn(b'\r\n',self.overlay['th03/formats/pfopen.asm'])
 def test_extent_mutations(self):
  for k,v in [('size',282),('offset',0x2ef1),('segment','canonical:0000'),('canonical_extent',0),('whole_root_credit',True),('source_acceptance',True),('exact_acceptance',True),('physical_object','obj/th03/pfopen.obj'),('retained_context_objects',26)]:
   c=copy.deepcopy(self.c);c[k]=v
   with self.assertRaises(ValueError):s.validate_config(c)
 def test_header_inventory_mutations(self):
  for k in ['physical_context','compatibility_closure']:
   c=copy.deepcopy(self.c);c[k].pop()
   with self.assertRaises(ValueError):s.validate_config(c)
 def test_instruction_comments_only(self):
  self.assertEqual(s.instructions(b'mov ax,bx ; x\r\n; y\r\n'),s.instructions(b'MOV AX,BX\r\n'));self.assertNotEqual(s.instructions(b'mov ax,bx'),s.instructions(b'mov ax,cx'))
 def test_no_payload_or_fake_abi(self):
  b=self.overlay['th03/formats/pfopen.asm'];self.assertNotIn(b'__emit__',b);self.assertNotIn(b'org ',b.lower());self.assertIn(b'func PFOPEN',b)
if __name__=='__main__':unittest.main()
