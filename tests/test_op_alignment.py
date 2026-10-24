"""Source-only graph and read-only actual alignment regression tests."""
from pathlib import Path
import copy,json,os,sys,types,unittest
from unittest.mock import patch
R=Path(os.environ.get('TH03_REPOSITORY_ROOT',Path(__file__).resolve().parents[1])).resolve();F=Path(os.environ.get('TH03_ALIGNMENT_FILES',R)).resolve();O=Path(os.environ.get('TH03_GLOBAL_ORDER_FILES',R)).resolve();P=Path(os.environ.get('TH03_PFOPEN_FILES',R)).resolve();sys.path.insert(0,str(R/'scripts'))
def load(p):
 m=types.ModuleType(p.stem);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
S=load(F/'scripts/stage_th03_op_alignment.py');Q=load(F/'scripts/replay_th03_op_alignment.py')
native = unittest.skipUnless((R/'.analysis/toolchain/wineprefix/drive_c/OPVA181/bin/th03/op.exe').is_file(),
                            'archived OP alignment build unavailable; source archive is independent')
@unittest.skipUnless((R/".analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar").is_file(), "archived native fixtures unavailable")
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  d=load(R/'scripts/stage_th03_op_fullcold.py').payload(R)
  for n in ['exit_helpers','remaining_helpers']:d.update(load(R/f'scripts/stage_th03_op_{n}.py').payload(R))
  d=load(R/'scripts/stage_th03_op_raster.py').compose(d,R);d=load(P/'scripts/stage_th03_op_pfopen_source.py').compose(d,P);cls.inputs=load(O/'scripts/stage_th03_op_global_order.py').compose(d,O);cls.outputs=S.compose(cls.inputs,F);cls.c=S.config(F)
 @native
 def test_330_exact_actual_sources(self):
  w=R/'.analysis/toolchain/wineprefix/drive_c/OPVA181';self.assertEqual(len(self.outputs),330)
  for n,b in self.outputs.items():self.assertEqual(b,(w/n).read_bytes(),n)
 def test_determinism(self):self.assertEqual(self.outputs,S.compose(dict(reversed(list(self.inputs.items()))),F))
 def test_only_three_overlay_files(self):
  changed={n for n,b in self.outputs.items() if self.inputs.get(n)!=b};self.assertEqual(changed,{'th03_op.asm','src/op/hardware/vsync_data.asm','src/op/hardware/cdg_data.asm'})
 def test_input_membership_drift(self):
  d=dict(self.inputs);d['bad.asm']=b''
  with self.assertRaises(ValueError):S.compose(d,F)
 def test_every_input_hash_bound(self):
  for n in self.inputs:
   d=dict(self.inputs);d[n]+=b'x'
   with self.assertRaises(ValueError):S.compose(d,F)
 def test_output_inventory_mutation(self):
  c=copy.deepcopy(self.c);c['output_inventory']['th03_op.asm']['sha256']='0'*64
  with patch.object(S,'config',return_value=c):
   with self.assertRaises(ValueError):S.compose(self.inputs,F)
 def test_historical_parity_not_raw_byte(self):
  b=self.outputs['src/op/hardware/vsync_data.asm'];self.assertIn(b'if (($ - origin) and 1)',b);self.assertIn(b'        nop',b);self.assertNotIn(b'90h',b);self.assertIn(b'evendata',self.outputs['src/op/hardware/cdg_data.asm'])
 @native
 def test_literal_actual_replay(self):
  r=Q.replay(R,F);self.assertTrue(r['replay_pass']);self.assertTrue(r['whole_target_program_equal']);self.assertTrue(r['literal607_target_order']);self.assertFalse(r['whole_decoded_file_equal']);self.assertEqual(r['new_authored_code_credit'],0)
 def test_proof_hash_mutation(self):
  with patch.object(Q,'PROOF_SHA','0'*64):
   with self.assertRaises(ValueError):Q.replay(R,F)
 def test_actual_source_drift_bound(self):
  q=json.loads((F/Q.PROOF).read_text())['current_report'];q['sha256']='0'*64
  with self.assertRaises(ValueError):Q.read(R,q)
if __name__=='__main__':unittest.main(verbosity=2)
