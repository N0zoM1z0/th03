
# This integration suite needs an optional archived native run.
from pathlib import Path as _ArchivePath
import unittest as _archive_unittest
if not (_ArchivePath(__file__).resolve().parents[1] / '.analysis/op-source-packing-checkpoint-proposal-v02/files/scripts/replay_th03_op_source_packing.py').is_file():
    raise _archive_unittest.SkipTest("archived native fixtures unavailable")

from pathlib import Path
import unittest,importlib.util,json,copy
ROOT=Path('.').resolve();FILES=ROOT/'.analysis/op-source-packing-checkpoint-proposal-v02/files';S=importlib.util.spec_from_file_location('packing_replay',FILES/'scripts/replay_th03_op_source_packing.py');R=importlib.util.module_from_spec(S);S.loader.exec_module(R)
class Tests(unittest.TestCase):
 def test_actual_five_phase_replay(self):self.assertTrue(R.replay(Path('.'),FILES.relative_to(ROOT))['replay_pass'])
 def test_proof_mutations(self):
  good=json.loads((FILES/'config/op_source_packing/proof.json').read_text())
  for key in ['expected_packed_equal','expected_restored_source_equal','expected_restored_target_equal','acceptance','full_cold','original_nopcall_native_completion']:
   bad=copy.deepcopy(good);bad[key]=not bad[key]
   with self.assertRaises(ValueError):R.validate_proof(bad,ROOT)
 def test_pin_mutation(self):
  p=json.loads((FILES/'config/op_source_packing/proof.json').read_text());p['pins'][0]['sha256']='0'*64
  with self.assertRaises(ValueError):R.validate_proof(p,ROOT)
 def test_authored_credit_rejected(self):
  p=json.loads((FILES/'config/op_source_packing/proof.json').read_text());p['new_authored_credit']=1
  with self.assertRaises(ValueError):R.validate_proof(p,ROOT)
if __name__=='__main__':unittest.main(verbosity=2)
