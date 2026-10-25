"""Portable source composition and exact-order observation regressions. Never launches native tools."""
from pathlib import Path
import collections,copy,hashlib,json,os,sys,types,unittest
from unittest.mock import patch
R=Path(os.environ.get('TH03_REPOSITORY_ROOT',Path(__file__).resolve().parents[1])).resolve();F=Path(os.environ.get('TH03_GLOBAL_ORDER_FILES',R)).resolve();P=Path(os.environ.get('TH03_PFOPEN_FILES',R)).resolve();sys.path.insert(0,str(R/'scripts'))
def load(p):
 m=types.ModuleType(p.stem);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
S=load(F/'scripts/stage_th03_op_global_order.py');V=load(F/'scripts/lib/op_global_order.py');V.ROOT=R;Q=load(F/'scripts/replay_th03_op_global_order.py')
manifest = json.loads((F/Q.PROOF).read_text())['current_manifest']['path']
native = unittest.skipUnless((R/manifest).is_file(),
                            'archived OP order build unavailable; source archive is independent')
def base():
 d=load(Path(__file__).with_name('op_historical_fixture.py')).payload(R,load(R/'scripts/stage_th03_op_fullcold.py'))
 for n in ['exit_helpers','remaining_helpers']:d.update(load(R/f'scripts/stage_th03_op_{n}.py').payload(R))
 d=load(R/'scripts/stage_th03_op_raster.py').compose(d,R);return load(P/'scripts/stage_th03_op_pfopen_source.py').compose(d,P)
@unittest.skipUnless((R/".analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar").is_file(), "archived native fixtures unavailable")
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.inputs=base();cls.outputs=S.compose(cls.inputs,F);cls.c=S.config(F);cls.proof=json.loads((F/Q.PROOF).read_text())
  if (R/manifest).is_file():
   cls.m=json.loads((R/manifest).read_text());cls.w=R/cls.m['work']
 @native
 def test_all328_native_source_files_exact(self):
  self.assertEqual(len(self.inputs),322);self.assertEqual(len(self.outputs),328)
  for n,b in self.outputs.items():self.assertEqual(b,(self.w/n).read_bytes(),n)
 def test_determinism(self):self.assertEqual(S.compose(self.inputs,F),S.compose(dict(reversed(list(self.inputs.items()))),F))
 def test_required_pfopen_dependency(self):
  d=dict(self.inputs);d['th03/formats/pfopen.asm']=b'wrong original context'
  with self.assertRaises(ValueError):S.compose(d,F)
 def test_input_closure_mutation(self):
  d=dict(self.inputs);d['unexpected.asm']=b''
  with self.assertRaises(ValueError):S.compose(d,F)
 def test_selection_whole_functions(self):
  self.assertEqual(self.outputs['probe/select155_helper.inl']+self.outputs['probe/select155_tail.inl'],self.inputs['src/op/menu/character_selection.inl']);self.assertEqual(self.outputs['probe/select155_helper.inl'].count(b'unsigned char near playchars_available_load(void)'),1)
 def test_root_original_storage_preserved(self):
  old=self.inputs['th03_op.asm'].decode().replace('\r\n','\n');new=self.outputs['th03_op.asm'].decode();tail=old[old.index('_TEXT\tends'):];self.assertTrue(new.endswith(tail));self.assertNotIn(b'db ',self.outputs['oplayout.asm'])
 def test_current_existing_call_macro(self):
  before=self.inputs['libs/master.lib/pfint21.asm'].decode().replace('\r\n','\n');after=self.outputs['libs/master.lib/pfint21.asm'].decode();self.assertEqual(before.count('\n\tcall')-after.count('\n\tcall'),11)
 def test_response_exact_thirty_objects(self):
  recipe=json.loads((F/'config/op_global_order/build_recipe.json').read_text());self.assertEqual(len(recipe['producers']),30);self.assertEqual(len(set(self.c['object_order'])),30);self.assertFalse(recipe['whole_recipe_cold_build_observed'])
 def test_response_permutation_rejected(self):
  c=copy.deepcopy(self.c);c['object_order'][0],c['object_order'][1]=c['object_order'][1],c['object_order'][0]
  with patch.object(S,'config',return_value=c):
   with self.assertRaises(ValueError):S.compose(self.inputs,F)
 @native
 def test_actual_replay(self):self.assertTrue(Q.replay(R,F)['replay_pass'])
 @native
 def test_actual_object_gates(self):
  self.assertTrue(V.verify_split_object(self.w/'obj/th03/op.obj','prefix')['pass_checks']);self.assertTrue(V.verify_split_object(self.w/'obj/th03/optail.obj','suffix')['pass_checks']);self.assertTrue(V.verify_anchor(self.w/'obj/th03/oplayout.obj')['pass_checks'])
 @native
 def test_literal_order_not_membership(self):
  b=(self.w/'bin/th03/op.exe').read_bytes();x=bytearray(b);at=int.from_bytes(b[24:26],'little');x[at:at+4],x[at+4:at+8]=x[at+4:at+8],x[at:at+4];a,z=map(V.parse_mz,(b,bytes(x)));self.assertEqual(a.program_image,z.program_image);self.assertEqual(collections.Counter(map(tuple,V.rels(a))),collections.Counter(map(tuple,V.rels(z))));self.assertNotEqual(V.rels(a),V.rels(z))
 @native
 def test_known_byte_remains_negative(self):self.assertEqual(Q.replay(R,F)['remaining_target_program_differences'],[0xdd95])
 @native
 def test_public_metadata_exact_dated_delta(self):
  a=(self.w/'obj/th03/op.map').read_text();b=(R/self.m['baseline_map']['path']).read_text();d=V.public_delta(a,b);self.assertTrue(d['pass_checks']);self.assertEqual(len(d['sections']['name']['added']),7);self.assertEqual(len(d['sections']['name']['idle_changes']),21);self.assertFalse(V.same_publics(a.replace('SOUND_I','FAKE_I'),b))
 @native
 def test_historical_failures_preserved(self):
  outcomes=[json.loads((R/q['path']).read_text()) for q in self.proof['history'] if q['path'].endswith('completion.json')];self.assertEqual([x['complete'] for x in outcomes],[False,True,False,True]);self.assertFalse(self.proof['source_acceptance']);self.assertFalse(self.proof['exact_acceptance']);self.assertEqual(self.proof['new_authored_code_credit'],0)
 @native
 def test_evidence_hash_mutation_rejected(self):
  q=copy.deepcopy(self.proof['observed_exe']);q['sha256']='0'*64
  with self.assertRaises(ValueError):Q.read(R,q)
if __name__=='__main__':unittest.main(verbosity=2)
