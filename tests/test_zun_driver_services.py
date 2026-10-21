"""Source ownership and source-composition checks; no compiler or target fallback."""
import importlib.util,re,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('driver_stage',ROOT/'scripts/stage_th03_zun_driver_services.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
OWN=(ROOT/s.SERVICES).read_text()
def fixture():
 rows=['; before setters\ncall sub_340\nmov ax,word_106C\n']
 for old,_,field,_ in s.SETTERS:rows.append(f'{old} proc near\n mov cs:{field}, dx\n retn\n{old} endp\n; separator\n')
 rows+=['; after setters\nservice_table dw '+','.join(row[0] for row in s.SETTERS)+'\n']
 rows += [f'{field} dw 0\n' for _,_,field,_ in s.SETTERS]
 return ''.join(rows)
class DriverServiceTests(unittest.TestCase):
 def test_six_complete_owned_bodies(self):s.validate_services(OWN);self.assertEqual(len(s.SETTERS),6)
 def test_no_bytes_padding_or_hardcoded_addresses(self):
  active='\n'.join(s.tokens(OWN))
  self.assertFalse(re.search(r'\b(db|dw|dd|org|align|include|equ)\b',active))
  self.assertNotRegex(active,r'\b[0-9][0-9a-f]*h\b')
 def test_actual_include_and_all_references(self):
  out=s.compose(fixture(),OWN)
  self.assertEqual(out.count('include src\\zun\\driver_services.inl'),1)
  for old,new,field,name in s.SETTERS:
   self.assertNotRegex(out,r'\b'+old+r'\b');self.assertNotRegex(out,r'\b'+field+r'\b')
   self.assertIn(new,out);self.assertIn(name+' dw 0',out)
 def test_outside_setters_unchanged_except_symbols(self):
  before=fixture();first=before.index('sub_340 proc');last=before.index('sub_35E endp')+len('sub_35E endp')
  expected=s.rename_symbols(before[:first]+'include src\\zun\\driver_services.inl'+before[last:])
  self.assertEqual(s.compose(before,OWN),expected)
 def test_unowned_gap_code_rejected(self):
  with self.assertRaisesRegex(ValueError,'unowned'):s.compose(fixture().replace('; separator','nop',1),OWN)
 def test_retained_body_change_rejected(self):
  with self.assertRaisesRegex(ValueError,'body'):s.compose(fixture().replace('mov cs:word_1064, dx','mov cs:word_1064, ax'),OWN)
 def test_owned_body_and_abi_changes_rejected(self):
  for changed in (OWN.replace('retn','retf',1),OWN.replace(', dx',', ax',1),OWN+'\ndb 0\n'):
   with self.assertRaises(ValueError):s.validate_services(changed)
 def test_duplicate_procedure_rejected(self):
  with self.assertRaisesRegex(ValueError,'unique'):s.compose(fixture()+fixture(),OWN)
 def test_strict_transcode(self):
  self.assertEqual(s.dos_text('x\n'),b'x\r\n')
  for bad in ('x\ry\n','x'):
   with self.assertRaises(ValueError):s.dos_text(bad)
 def test_two_command_recipe_only(self):
  a,b=s.native_commands('/usr/bin/wine-stable','/path/msdos.exe')
  self.assertIn('/dTHIEF',a);self.assertEqual(a[-1],'driver.asm,driver.obj')
  self.assertEqual(b[-3:],['-x','tlink','@link.rsp'])
if __name__=='__main__':unittest.main()
