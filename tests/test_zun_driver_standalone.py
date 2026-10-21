"""Maintained driver staging without any reference tree or binary target."""
import importlib.util,re,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('standalone_driver',ROOT/'scripts/stage_th03_zun_driver.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
def inputs():return {n:(ROOT/n).read_bytes() for n in (s.LAYOUT,s.DATA,s.HARDWARE,*s.MODULES)}
class StandaloneDriverTests(unittest.TestCase):
 def test_all_fifty_five_complete_bodies(self):
  files=s.prepare(inputs());procs=[n for n in files if n.startswith('procs/')]
  self.assertEqual(len(procs),55)
  for n in procs:self.assertIn(b'public sprite16_',files[n])
 def test_stage_without_reference_tree(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)
   for n,raw in inputs().items():
    p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
   out=root/'stage';result=s.stage(out,root)
   self.assertTrue(result['complete_driver_source_owned']);self.assertEqual(result['retained_source_inputs'],[])
   self.assertEqual(result['native_invocations'],0);self.assertFalse(result['exact_acceptance'])
   self.assertEqual(len(result['inputs']),10)
   self.assertEqual(result['maintained_nonprocedure_bytes'],1380)
   self.assertNotIn(b'_reference',(out/'driver.asm').read_bytes())
   with self.assertRaises(FileExistsError):s.stage(out,root)
 def test_missing_duplicate_or_foreign_include_rejected(self):
  for operation in ('missing','duplicate','foreign'):
   raw=inputs();line=b'include procs\\sprite16_entry.inc'
   if operation=='missing':raw[s.LAYOUT]=raw[s.LAYOUT].replace(line,b'; missing')
   elif operation=='duplicate':raw[s.LAYOUT]+=line+b'\n'
   else:raw[s.LAYOUT]=raw[s.LAYOUT].replace(line,b'include ..\\foreign.inc')
   with self.assertRaises(ValueError):s.prepare(raw)
 def test_unowned_source_outside_procedure_rejected(self):
  for suffix in (b'\nnop\n',b'\ndb 0\n',b'\ninclude foreign.inc\n'):
   raw=inputs();raw[s.MODULES[0]]+=suffix
   with self.assertRaises(ValueError):s.prepare(raw)
 def test_duplicate_missing_and_public_mismatch_rejected(self):
  raw=inputs()
  for text in (raw[s.MODULES[0]]*2,raw[s.MODULES[0]].replace(b'endp',b'missing',1),raw[s.MODULES[0]].replace(b'public ',b'; public ',1)):
   changed=dict(raw);changed[s.MODULES[0]]=text
   with self.assertRaises(ValueError):s.prepare(changed)
 def test_strict_encoding_and_transitive_inputs(self):
  for replacement in (inputs()[s.DATA].replace(b'\n',b'\r\n'),inputs()[s.DATA]+b'include foreign.inc\n',inputs()[s.DATA]+b'org 1180h\n'):
   raw=inputs();raw[s.DATA]=replacement
   with self.assertRaises(ValueError):s.prepare(raw)
  self.assertEqual(s.dos_text('x\n'),b'x\r\n')
 def test_stack_table_and_defaults_are_typed(self):
  text=inputs()[s.DATA].decode()
  for literal in ('sprite16_startup_stack db 200h dup(0)','sprite16_startup_stack_top label byte','sprite16_argument_vector dw 64 dup(0)',
                  'sprite16_interrupt_number\tdb 42h','sprite16_mono_color\tdw 0Fh','sprite16_rop\tdw 28FCh'):
   self.assertIn(literal,text)
  self.assertEqual(text.count('dw offset '),17)
 def test_reserved_layout_is_explicit_not_fitted(self):
  text=inputs()[s.LAYOUT].decode();counts=[int(n) for n in re.findall(r'^layout_reserved_\w+ db (\d+) dup\(0\)$',text,re.M)]
  self.assertEqual(sum(counts),71)
  self.assertIn("sprite16_hex_digits db '0123456789ABCDEF'",text)
  self.assertEqual(len(re.findall(r'^nop$',text,re.M)),1)
  self.assertNotRegex(text.lower(),r'(?m)^\s*(align|incbin)\b')
 def test_hardware_order_and_subset(self):
  text=inputs()[s.HARDWARE].decode()
  self.assertIn('mov dx, port\n    mov ax, value\n    out dx, ax',text)
  self.assertEqual(len(re.findall(r'^\w+ macro\b',text,re.M)),6)
  self.assertNotIn('EGC_SETUP_COPY',text);self.assertNotIn('outw2',text)
 def test_named_data_ranges_and_packed_state(self):
  offset=0xc80;labels={}
  def number(n):return int(n[:-1],16) if n.lower().endswith('h') else int(n)
  for line in inputs()[s.DATA].decode().splitlines():
   line=line.split(';',1)[0].strip()
   if not line:continue
   m=re.fullmatch(r'(?:(\w+)\s+)?(db|dw|label)\s+(.+)',line,re.I)
   self.assertIsNotNone(m,line);name,kind,args=m.groups()
   if name:labels[name]=offset
   if kind.lower()=='label':continue
   width=1 if kind.lower()=='db' else 2
   dup=re.fullmatch(r'([0-9A-Fa-f]+h?) dup\(0\)',args)
   if dup:offset+=number(dup[1])*width;continue
   for value in re.findall(r"'[^']*'|[^,]+",args):
    value=value.strip()
    offset+=len(value[1:-1].encode('shift_jis')) if value.startswith("'") else width
  self.assertEqual(offset,0x1180)
  for name,address in {'sprite16_startup_stack':0xd38,'sprite16_startup_stack_top':0xf38,
   'sprite16_previous_vector_segment':0xf38,'sprite16_previous_vector_offset':0xf3a,
   'sprite16_interrupt_number':0xf42,'sprite16_resident_paragraphs':0xf43,
   'sprite16_dispatch_target':0xf45,'sprite16_banner':0xf7a,'sprite16_usage':0xfb9,
   'sprite16_option_table':0x101c,'sprite16_service_table':0x103e,
   'sprite16_argument_vector':0x1072,'sprite16_argument_cursor':0x10f2,
   'sprite16_switch_on':0x1170,'sprite16_switch_off':0x1173}.items():self.assertEqual(labels[name],address,name)
 def test_compiler_include_names_are_short_and_bodies_unchanged(self):
  raw=inputs();files=s.prepare(raw)
  names=re.findall(r'^include (.+)$',files['driver.asm'].decode('shift_jis').replace('\r\n','\n'),re.M)
  expected={}
  for module in s.MODULES:expected.update(s.bodies(raw[module].decode()))
  seen=set()
  self.assertEqual(len(names),len(set(names)))
  for name in names:
   self.assertLessEqual(len(name),16)
   for part in name.split('\\'):self.assertRegex(part,r'^[a-z0-9_]{1,8}(?:\.[a-z0-9_]{1,3})?$')
   data=files[name.replace('\\','/')]
   if name.startswith('procs'):
    text=data.decode('shift_jis').replace('\r\n','\n');proc=text.splitlines()[0].split()[1]
    self.assertEqual(text,expected[proc]);seen.add(proc)
  self.assertEqual(seen,set(expected));self.assertEqual(len(seen),55)
 def test_native_recipe_remains_two_commands(self):
  a,b=s.native_commands('/wine','/msdos')
  self.assertEqual(a[-1],'driver.asm,driver.obj');self.assertEqual(b[-3:],['-x','tlink','@link.rsp'])
if __name__=='__main__':unittest.main()
