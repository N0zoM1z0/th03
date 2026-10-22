from pathlib import Path
import hashlib,json,unittest
ROOT=Path(__file__).resolve().parents[1]
SHA="fd19475aea02ec5aa6ae8e4c48f6ab88170f1d73e0f6ee7dbfa7231d50dc8c68"
NAME=".analysis/gpt-dots-player-cpu-acceptance-install-v01/support.py"
class RecoveryTests(unittest.TestCase):
 def test_versioned_exact_bytes(self):
  raw=(ROOT/"config/recovery/native_support_20261020.py.txt").read_bytes()
  self.assertEqual(len(raw),5324);self.assertEqual(hashlib.sha256(raw).hexdigest(),SHA)
 def test_original_bindings_unchanged(self):
  for name in ["config/op_fullcold_exact/proof.json","config/op_alignment/proof.json"]:
   rows=[r for r in json.loads((ROOT/name).read_text())["pins"] if r["path"]==NAME]
   self.assertEqual(len(rows),1);self.assertEqual(rows[0]["sha256"],SHA);self.assertEqual(rows[0]["bytes"],5324)
 def test_private_copy_when_available(self):
  p=ROOT/NAME
  if not p.exists():self.skipTest("private retained helper is not installed")
  self.assertFalse(p.is_symlink());self.assertEqual(p.read_bytes(),(ROOT/"config/recovery/native_support_20261020.py.txt").read_bytes())
if __name__=="__main__":unittest.main()
