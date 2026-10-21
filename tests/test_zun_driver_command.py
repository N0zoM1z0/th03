"""Bounded command-group source contracts, not emulator or DOS behavior proof."""
import importlib.util,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('command_stage',ROOT/'scripts/stage_th03_zun_driver_services.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
def own(path):return (ROOT/path).read_text()
def inverse(text):
 mapping={b:a for a,b,_,_ in s.RESIDENT_PROCS}|{b:a for a,b in s.RESIDENT_SYMBOLS.items()}|{b:a for _,group in s.COMMAND_GROUPS for a,b,_,_ in group}|{b:a for a,b in s.COMMAND_SYMBOLS.items()}
 return re.sub(r'\b('+'|'.join(mapping)+r')\b',lambda m:mapping[m[0]],text)
def fixture(text):return inverse('\n'.join(x for x in text.splitlines() if not x.startswith('public ')))
class CommandTests(unittest.TestCase):
 def test_sixteen_complete_procedures(self):
  self.assertEqual(sum(len(g) for _,g in s.COMMAND_GROUPS),16)
  self.assertEqual(sum(b-a for _,g in s.COMMAND_GROUPS for _,_,a,b in g),725)
  for path,group in s.COMMAND_GROUPS:
   self.assertIn('include '+path.replace('/','\\'),s.compose_command_group(fixture(own(path)),own(path),path,group))
 def test_no_data_or_gap_ownership(self):
  for path,group in s.COMMAND_GROUPS:
   self.assertFalse(re.search(r'\b(db|dw|dd|org|align|include|equ)\b','\n'.join(s.tokens(own(path)))))
   out=s.compose_command_group(fixture(own(path))+'\ndb 7 dup(0)\n',own(path),path,group)
   self.assertTrue(out.endswith('\ndb 7 dup(0)\n'))
 def test_changed_body_or_return_rejected(self):
  for path,group in s.COMMAND_GROUPS:
   changed=own(path).replace('retn','retf',1)
   with self.assertRaises(ValueError):s.compose_command_group(fixture(own(path)),changed,path,group)
 def test_missing_or_duplicate_procedure_rejected(self):
  for path,group in s.COMMAND_GROUPS:
   text=fixture(own(path))
   with self.assertRaises(ValueError):s.compose_command_group(text+text,own(path),path,group)
   with self.assertRaises(ValueError):s.compose_command_group(text.replace('endp','missing',1),own(path),path,group)
 def test_injected_unowned_gap_rejected(self):
  path,group=s.COMMAND_GROUPS[0];text=fixture(own(path));old=group[1][0]
  text=text.replace(old+'\t\tproc near','db 0\n'+old+'\t\tproc near',1)
  with self.assertRaises(ValueError):s.compose_command_group(text,own(path),path,group)
 def test_legacy_optional_branch_preserved(self):
  text=own(s.COMMAND_GROUPS[0][0]);body=text.split('sprite16_optional_number_legacy\t\tproc near',1)[1].split('endp',1)[0]
  self.assertLess(body.index('mov\tax, 0'),body.index('call\tsprite16_optional_argument'))
  self.assertIn('jnb\tshort optional_number_return',body)
  self.assertIn('call\tsprite16_parse_number',body)
 def test_no_native_or_target_dependency(self):
  for path,_ in s.COMMAND_GROUPS:self.assertNotIn('target', '\n'.join(s.tokens(own(path))))
if __name__=='__main__':unittest.main()
