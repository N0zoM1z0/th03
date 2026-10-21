"""Resident ownership/ABI tests without a compiler, target bytes or device calls."""
import importlib.util,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('resident_stage',ROOT/'scripts/stage_th03_zun_driver_services.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
OWN=(ROOT/s.RESIDENT).read_text()
def inverse(text):
 mapping={b:a for a,b,_,_ in s.RESIDENT_PROCS}|{b:a for a,b in s.RESIDENT_SYMBOLS.items()}
 return re.sub(r'\b('+'|'.join(mapping)+r')\b',lambda m:mapping[m[0]],text)
def fixture():
 body='\n'.join(x for x in OWN.splitlines() if not x.startswith('public '))
 return '; outside\nstart: jmp short sub_10C\n'+inverse(body)+'\nretained_data dw 0\n'
class ResidentTests(unittest.TestCase):
 def test_complete_eight_procedures(self):
  out=s.compose_resident(fixture(),OWN)
  self.assertEqual(out.count('include src\\zun\\driver_resident.inl'),1)
  self.assertEqual(sum(b-a for _,_,a,b in s.RESIDENT_PROCS),564)
  self.assertEqual(len(s.RESIDENT_PROCS),8)
 def test_original_far_interrupt_abi(self):
  self.assertIn('sprite16_interrupt_dispatch\t\tproc far',OWN)
  self.assertIn('iret',s.tokens(OWN));self.assertEqual(s.tokens(OWN).count('iret'),1)
 def test_no_owned_data_padding_or_includes(self):
  self.assertFalse(re.search(r'\b(db|dw|dd|org|align|include|equ)\b','\n'.join(s.tokens(OWN))))
 def test_changed_return_or_vector_restore_rejected(self):
  for value in (OWN.replace('iret','retf',1),OWN.replace('xor\tax, ax','mov\tax, 1',1)):
   with self.assertRaises(ValueError):s.compose_resident(fixture(),value)
 def test_unowned_gap_and_duplicate_rejected(self):
  bad=fixture().replace('sub_19C\t\tproc near','nop\nsub_19C\t\tproc near',1)
  with self.assertRaises(ValueError):s.compose_resident(bad,OWN)
  with self.assertRaises(ValueError):s.compose_resident(fixture()+fixture(),OWN)
 def test_all_references_named(self):
  text=s.rename_symbols(fixture())
  for old,new,_,_ in s.RESIDENT_PROCS:
   self.assertNotRegex(text,r'\b'+old+r'\b');self.assertIn(new,text)
if __name__=='__main__':unittest.main()
