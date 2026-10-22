import copy,hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('op_raster_stage',ROOT/'scripts/stage_th03_op_raster.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
class RasterSource(unittest.TestCase):
 def test_source_hashes_and_scope(self):
  c,b=S.read_inputs(ROOT);self.assertEqual(sum(u['size'] for u in c['units']),124);self.assertEqual(set(b),{u['source'] for u in c['units']});self.assertEqual(len(b),2)
 def test_no_canonical_offsets(self):
  c,_=S.read_inputs(ROOT)
  for u in c['units']:self.assertNotIn('file_offset',u);self.assertNotIn('extent_start',u);self.assertEqual(u['segment'],'decoded:0990')
 def test_historical_failure_remains(self):
  c,_=S.read_inputs(ROOT);self.assertFalse(c['original_runner_complete']);self.assertTrue(c['separate_offline_audit_pass']);self.assertFalse(c['source_acceptance']);self.assertFalse(c['exact_acceptance'])
 def test_real_signatures(self):
  c,b=S.read_inputs(ROOT)
  for u in c['units']:self.assertEqual(b[u['source']].count(u['signature'].encode()),1)
 def test_native_frames_not_faked(self):
  _,b=S.read_inputs(ROOT)
  for raw in b.values():
   active=b'\n'.join(line.split(b'//')[0] for line in raw.splitlines())
   for forbidden in (b'__emit__',b'push bp',b'pop bp',b'mov bp,',b'ret;',b'ret 2',b'cld;'):self.assertNotIn(forbidden,active)
 def test_named_hardware_operations(self):
  _,b=S.read_inputs(ROOT);music=b['src/op/music/nopoly_blit.inl'];box=b['src/op/menu/column_restore.inl'];self.assertIn(b'rep movsw;',music);self.assertIn(b'mov ax, nopoly_B;',music);self.assertIn(b'LAST_ROW_OFFSET = (BOX_BOTTOM - 1) * ROW_SIZE',box);self.assertIn(b'mov ax, left;',box);self.assertIn(b'jnc restore_row;',box)
 def test_original_cpp_game3_commands(self):
  c,_=S.read_inputs(ROOT)
  for u in c['units']:self.assertEqual(u['physical_game_macro'],3);self.assertEqual(u['language'],'cpp');self.assertIn('-DGAME=3',u['original_command'])
 def test_changed_source_rejected(self):
  c,b=S.read_inputs(ROOT)
  with tempfile.TemporaryDirectory() as temp:
   t=Path(temp);(t/'config').mkdir();(t/S.CONFIG).write_bytes((ROOT/S.CONFIG).read_bytes())
   for n,raw in b.items():p=t/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw+b' ')
   with self.assertRaisesRegex(ValueError,'maintained source changed'):S.read_inputs(t)
 def test_changed_config_rejected(self):
  with tempfile.TemporaryDirectory() as temp:
   t=Path(temp);(t/'config').mkdir();(t/S.CONFIG).write_bytes((ROOT/S.CONFIG).read_bytes()+b' ')
   with self.assertRaisesRegex(ValueError,'candidate config changed'):S.read_inputs(t)
 def test_changed_reference_rejected(self):
  c,_=S.read_inputs(ROOT)
  for u in c['units']:
   with self.assertRaisesRegex(ValueError,'carrier drift'):S.replace_function(b'not the original complete TU',u)
for key,value in [('code_bytes',125),('physical_translation_units',3),('retained_context_objects',24),('preserved_prior_owner_count',41),('preserved_prior_code_bytes',12815),('source_acceptance',True),('exact_acceptance',True),('original_runner_complete',True)]:
 def check(self,key=key,value=value):
  c,_=S.read_inputs(ROOT);c[key]=value
  with self.assertRaises(ValueError):S.validate_config(c)
 setattr(RasterSource,'test_config_rejects_'+key,check)
if __name__=='__main__':unittest.main()
