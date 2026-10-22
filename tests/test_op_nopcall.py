from pathlib import Path
import unittest,os,importlib.util,json
ROOT=Path(os.environ.get('TH03_REPOSITORY_ROOT','.')).resolve();FILES=Path(os.environ.get('TH03_NOPCALL_FILES','.analysis/op-nopcall-checkpoint-proposal-v01/files')).resolve()
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
S=load('nopcall_stage',FILES/'scripts/stage_th03_op_nopcall.py');R=load('nopcall_replay',FILES/'scripts/replay_th03_op_nopcall.py')
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  m=json.loads((ROOT/'.analysis/op-final-alignment-native-output-v01/manifest.json').read_text());w=ROOT/m['work'];c.inputs={n:(w/n).read_bytes() for n in m['repeat_inputs'] if not n.endswith('.obj')}
 def test_exact330(self):self.assertEqual(len(S.compose(self.inputs,FILES)),330)
 def test_only_macro(self):self.assertEqual([n for n,b in S.compose(self.inputs,FILES).items() if b!=self.inputs[n]],['ReC98.inc'])
 def test_deterministic(self):self.assertEqual(S.compose(self.inputs,FILES),S.compose(self.inputs,FILES))
 def test_each_source_drift(self):
  for n in self.inputs:
   bad=dict(self.inputs);bad[n]+=b' '
   with self.assertRaises(ValueError):S.compose(bad,FILES)
 def test_membership(self):
  bad=dict(self.inputs);bad.pop('ReC98.inc')
  with self.assertRaises(ValueError):S.compose(bad,FILES)
 def test_actual_sources(self):
  m=json.loads((ROOT/'.analysis/op-nopcall-native-output-v01/manifest.json').read_text());w=ROOT/m['work'];self.assertEqual(S.compose(self.inputs,FILES),{n:(w/n).read_bytes() for n in m['repeat_inputs'] if not n.endswith('.obj')})
 def test_actual_offline_replay(self):self.assertTrue(R.replay(ROOT,FILES)['replay_pass'])
if __name__=='__main__':unittest.main(verbosity=2)
