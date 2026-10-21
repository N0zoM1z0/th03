"""All-procedure source placement without claiming retained data or exact target bytes."""
import importlib.util,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('all_stage',ROOT/'scripts/stage_th03_zun_driver_services.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
def own(path):return (ROOT/path).read_text()
def fixture(text):
 mapping={b:a for a,b,_,_ in s.RESIDENT_PROCS}|{b:a for a,b in s.RESIDENT_SYMBOLS.items()}|{b:a for _,g in s.COMMAND_GROUPS+s.SCATTERED_GROUPS for a,b,_,_ in g}|{b:a for a,b in s.COMMAND_SYMBOLS.items()}|{b:a for a,b in s.SCATTERED_SYMBOLS.items()}
 for a,b,c,d in s.SETTERS:mapping[b]=a;mapping[d]=c
 text='\n'.join(x for x in text.splitlines() if not x.startswith('public '))
 return re.sub(r'\b('+'|'.join(mapping)+r')\b',lambda m:mapping[m[0]],text)
class ProcedureTests(unittest.TestCase):
 def test_twenty_five_complete_procedures(self):
  self.assertEqual(sum(len(g) for _,g in s.SCATTERED_GROUPS),25)
  self.assertEqual(sum(b-a for _,g in s.SCATTERED_GROUPS for _,_,a,b in g),1519)
  for path,procs in s.SCATTERED_GROUPS:
   output=s.compose_scattered(fixture(own(path)),own(path),procs)
   for old,name,a,b in procs:self.assertIn('public '+name,output)
 def test_exact_gap_preservation(self):
  path,procs=s.SCATTERED_GROUPS[0];text=fixture(own(path));gap='\ndb 10 dup(0)\naUnowned db 1,2,3\n'
  old=procs[1][0];text=text.replace(old+'\t\tproc near',gap+old+'\t\tproc near',1)
  output=s.compose_scattered(text,own(path),procs)
  self.assertEqual(output.count(gap),1)
 def test_no_data_or_padding_in_owned_files(self):
  for path,_ in s.SCATTERED_GROUPS:self.assertFalse(re.search(r'\b(db|dw|dd|org|align|include)\b','\n'.join(s.tokens(own(path)))))
 def test_changed_body_and_extra_code_rejected(self):
  for path,procs in s.SCATTERED_GROUPS:
   for changed in (own(path).replace('retn','retf',1),own(path)+'\nnop\n'):
    with self.assertRaises(ValueError):s.compose_scattered(fixture(own(path)),changed,procs)
 def test_missing_duplicate_and_public_rejected(self):
  for path,procs in s.SCATTERED_GROUPS:
   for changed in (own(path)+own(path),own(path).replace('endp','missing',1),own(path).replace('public ','; public ',1)):
    with self.assertRaises(ValueError):s.compose_scattered(fixture(own(path)),changed,procs)
 def test_stack_return_and_interrupt_policy_preserved(self):
  text=own(s.SCATTERED_GROUPS[1][0]);self.assertIn('retn\t2',text)
  graphics=own(s.SCATTERED_GROUPS[0][0]);self.assertEqual(s.tokens(graphics).count('cli'),2);self.assertEqual(s.tokens(graphics).count('sti'),2)
 def test_no_hardware_safety_repair(self):
  text=own(s.SCATTERED_GROUPS[0][0]);self.assertNotIn('cld',s.tokens(text))
  self.assertIn('cmp ax, 0',s.tokens(text));self.assertIn('and ax, 0fffeh',s.tokens(text));self.assertIn('and ax, 0fh',s.tokens(text))
if __name__=='__main__':unittest.main()
