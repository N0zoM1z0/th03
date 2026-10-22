"""Portable dated-proof controls; no native execution or live-state gate."""
from pathlib import Path
import copy,importlib.util,json,sys,unittest
ROOT=Path.cwd().resolve();FILES=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
p=FILES/'scripts/replay_th03_op_fullcold_exact.py';sp=importlib.util.spec_from_file_location('cold_exact_test',p);a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
PAYLOAD_PATHS=(
 'config/op_fullcold_exact/proof.json',
 'docs/reconstruction/OP_FULLCOLD_EXACT.md',
 'scripts/lib/op_fullcold_exact.py',
 'scripts/replay_th03_op_fullcold_exact.py',
 'tests/test_op_fullcold_exact.py',
)
def check_text_payload(payload):
 # Inspect this checkpoint's complete five-file payload, not repository artifacts.
 if set(payload)!=set(PAYLOAD_PATHS):raise ValueError('checkpoint payload closure')
 for name,raw in payload.items():
  if Path(name).suffix.lower() in {'.obj','.exe','.map','.lib','.com'}:raise ValueError('binary payload path')
  if b'\0' in raw:raise ValueError('binary payload content')
  raw.decode('utf-8')
 return True
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=a.proof(ROOT,FILES);cls.t=json.loads(a.pin(ROOT,cls.p['terminal_attestation']));cls.m=json.loads(a.pin(ROOT,cls.p['final_manifests'][0]));cls.v=a.load(FILES/cls.p['observer']['path']);cls.v.ROOT=ROOT;cls.v.HERE=ROOT/'.analysis/op-fullcold-ordered-deferred-v03';cls.v.ENV['WINEPREFIX']=str(ROOT/'.analysis/toolchain/wineprefix');cls.plan=json.loads(cls.v.pin(cls.m['cold_plan']));cls.work=ROOT/cls.m['work'];cls.raw=(cls.work/'bin/th03/op.exe').read_bytes();cls.target=cls.v.pin(cls.m['target'])
 def test_all2350_artifact_pins(self):
  self.assertEqual(len(self.p['pins']),2350)
  for q in self.p['pins']:a.pin(ROOT,q)
 def test_no_live_native_tool_or_registry_pins(self):
  paths={q['path'] for q in self.p['pins']};self.assertFalse(paths&{q['path'] for q in self.m['toolchain_inputs']});self.assertFalse(any(n.endswith('/wineprefix/user.reg') or n.endswith('/wineprefix/system.reg') for n in paths))
 def test_dated_terminal(self):self.assertTrue(a.terminal_contract(self.t,self.p))
 def test_terminal_mutations(self):
  for k,val in [('comparison_pass',False),('owned_lock_released',False),('current_source_tool_mtime_HEAD_guards',False),('actual_native_phases',61),('whole_product_ownership',True)]:
   t=copy.deepcopy(self.t);t[k]=val
   with self.assertRaises(ValueError):a.terminal_contract(t,self.p)
 def test_wrong_root_manifest(self):
  t=copy.deepcopy(self.t);t['final_frozen_manifest_sha256']['1']='0'*64
  with self.assertRaises(ValueError):a.terminal_contract(t,self.p)
 def test_raw30_OMF_pairs(self):
  from lib.omf import parse_omf
  self.assertEqual(len(self.p['raw_object_pairs']),30);total=0
  for q in self.p['raw_object_pairs']:
   x,y=(a.pin(ROOT,q[k]) for k in ('round1','round2'));self.assertEqual(x,y);self.assertTrue(parse_omf(x));total+=len(x)
  self.assertEqual(total,80839)
 def test_corrupt_object_pin(self):
  q=dict(self.p['raw_object_pairs'][0]['round1'],sha256='0'*64)
  with self.assertRaises(ValueError):a.pin(ROOT,q)
 def test_wholefile_and607(self):
  self.assertEqual(len(self.raw),63866);self.assertEqual(self.raw,self.target);c,t=map(self.v.parse_mz,(self.raw,self.target));self.assertTrue(all(self.v.core_checks(c,c,t).values()));self.assertEqual(len(c.relocations),607)
 def test_header_only_mutation(self):
  x=bytearray(self.raw);x[0xb00]^=1;self.assertFalse(any(self.v.file_checks(bytes(x),self.target).values()))
 def test_tool_descriptors(self):self.assertTrue(self.v.dated_descriptors(self.m))
 def test_tool_hash_mutation(self):
  m=copy.deepcopy(self.m);m['toolchain_inputs'][0]['sha256']='0'*64
  with self.assertRaises(ValueError):self.v.dated_descriptors(m)
 def test_tool_timestamp_mutation(self):
  m=copy.deepcopy(self.m);m['fixed_mtimes'].pop(next(iter(m['fixed_mtimes'])))
  with self.assertRaises(ValueError):self.v.dated_descriptors(m)
 def test_wrong_group_round(self):
  group=self.plan['groups'][-1];self.v.group_contract(self.m,self.m,group,self.plan);m=copy.deepcopy(self.m);m['round']=2
  with self.assertRaises(ValueError):self.v.group_contract(m,self.m,group,self.plan)
 def test_exact14_receipt_closures(self):
  for r in (1,2):
   for g in self.plan['groups']:
    out=ROOT/f'.analysis/op-fullcold-exact-r{r}-g{g["group"]}-output-v01';self.assertEqual({p.name for p in out.iterdir() if p.is_file()},self.v.expected_receipts(g['phases'],True))
 def test_current330_sources(self):
  virtual=FILES!=ROOT
  result=a.check_current_sources(ROOT,FILES,virtual=virtual)
  self.assertTrue(result['current_source_composition_pass'])
  self.assertEqual(result['virtual_uninstalled_proposals'],virtual)
 def test_no_live_guard(self):
  s=(FILES/self.p['observer']['path']).read_text()
  for text in ('st_mtime_ns','runner.guard','subprocess','SharedLock'):self.assertNotIn(text,s)
 def test_no_binary_payload(self):
  self.assertTrue(check_text_payload({n:(FILES/n).read_bytes() for n in PAYLOAD_PATHS}))
 def test_binary_payload_mutations(self):
  payload={n:(FILES/n).read_bytes() for n in PAYLOAD_PATHS}
  with self.assertRaises(ValueError):check_text_payload(dict(payload,**{'seed.obj':b'object'}))
  for raw in (b'MZ\0binary',b'\xff\xfe'):
   changed=dict(payload);changed[PAYLOAD_PATHS[0]]=raw
   with self.assertRaises(ValueError):check_text_payload(changed)
 def test_missing_payload_mutation(self):
  payload={n:(FILES/n).read_bytes() for n in PAYLOAD_PATHS[1:]}
  with self.assertRaises(ValueError):check_text_payload(payload)
if __name__=='__main__':unittest.main()
