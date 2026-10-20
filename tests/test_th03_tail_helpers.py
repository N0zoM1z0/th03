from pathlib import Path
import json,sys,unittest,copy,os
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
PRIVATE=Path(os.environ.get('TH03_TAIL_PRIVATE_ROOT',Path.cwd())).resolve()
sys.path.insert(0,str(PRIVATE/'scripts'));sys.path.insert(0,str(ROOT/'scripts'));import lib
lib.__path__.insert(0,str(ROOT/'scripts/lib'))
from lib import th03_tail_map as m
from lib import th03_tail_model as tm
from lib import th03_tail_warning_gate as wg
from lib import th03_tail_compare as tc
from lib import pc98
from lib import th03_score_candidate as parser
P=PRIVATE/Path('.analysis/gpt-dots-player-tail-map-supplement-v02');B=PRIVATE/Path('.analysis/th03-main-exact/gpt-dots-yumemi-bomb-default-cold-v01/round1/source');W=PRIVATE/Path('.analysis/gpt-dots-player-tail-retained-probe-v06/run-first-v01/source')
HAS_PRIVATE=(W/'obj/th03/main.obj').is_file() and (B/'obj/th03/main.obj').is_file() and (P/'production-validation.json').is_file()
@unittest.skipUnless(HAS_PRIVATE,'private retained proof fixtures unavailable')
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.text=(W/'obj/th03/main.map').read_text('latin1');c.model=m.derive_zero_and_contribution_model(B,W);c.inv=m.derive_public_inventory(B,W,c.model);c.display=json.loads((ROOT/'scripts/lib/th03_tail_public_display.json').read_text())
 def test_literal_aggregate_prefix(self):
  self.assertTrue(m.validate_aggregate_prefix((B/'obj/th03/main.map').read_bytes(),(W/'obj/th03/main.map').read_bytes(),self.model))
 def test_unparsed_prefix_drift_rejected(self):
  raw=(W/'obj/th03/main.map').read_bytes().replace(b'Start  Stop',b'Start   Stop',1)
  with self.assertRaisesRegex(ValueError,'literal aggregate prefix'):m.validate_aggregate_prefix((B/'obj/th03/main.map').read_bytes(),raw,self.model)
 def test_added_prefix_row_whitespace_rejected(self):
  raw=(W/'obj/th03/main.map').read_bytes().replace(b'WARNING_TEXT ',b'WARNING_TEXT  ',1)
  with self.assertRaisesRegex(ValueError,'literal aggregate prefix'):m.validate_aggregate_prefix((B/'obj/th03/main.map').read_bytes(),raw,self.model)
 def test_actual_group_field_drift_rejected(self):
  text=self.text.replace('G=MAIN_01','G=MAIN_02',1)
  with self.assertRaisesRegex(ValueError,'detailed contributions'):m.validate_rows(self.model,text)
 def test_all_rows(self):self.assertTrue(m.validate_rows(self.model,self.text))
 def test_public_vectors(self):self.assertTrue(m.validate_public_vectors(self.display,self.text))
 def test_derive_inventory(self):self.assertEqual((len(self.inv['additions']),len(self.inv['removals']),len(self.inv['root_tie_provider_proof'])),(36,3,22))
 def test_runtime_provider_records(self):self.assertEqual(len(m.runtime_provider_proof(PRIVATE,(B/'obj/th03/main.map').read_text('latin1'))['records_literal_provider_order']),7)
 def test_zero_moved_rejected(self):
  x=copy.deepcopy(self.model);i=next(i for i,r in enumerate(x['detailed_rows']) if r[6]=='src/main/player/warning.cpp' and r[4]=='_DATA');r=list(x['detailed_rows'][i]);r[1]+=1;x['detailed_rows'][i]=r
  with self.assertRaises(ValueError):m.validate_rows(x,self.text)
 def test_zero_reordered_rejected(self):
  x=copy.deepcopy(self.model);i=next(i for i,r in enumerate(x['detailed_rows']) if r[4]=='WARNING_TEXT');x['detailed_rows'][i],x['detailed_rows'][i+1]=x['detailed_rows'][i+1],x['detailed_rows'][i]
  with self.assertRaises(ValueError):m.validate_rows(x,self.text)
 def test_aggregate_zero_missing_rejected(self):
  x=copy.deepcopy(self.model);x['aggregate_rows']=[r for r in x['aggregate_rows'] if r[3]!='WARNING_TEXT']
  with self.assertRaises(ValueError):m.validate_rows(x,self.text)
 def test_new_name_moved_rejected(self):
  x=copy.deepcopy(self.display);i=x['observed_new_entry_positions'][0][0]['index'];x['complete_names'][i],x['complete_names'][i+1]=x['complete_names'][i+1],x['complete_names'][i]
  with self.assertRaises(ValueError):m.validate_public_vectors(x,self.text)
 def test_new_value_moved_rejected(self):
  x=copy.deepcopy(self.display);i=x['observed_new_entry_positions'][1][0]['index'];x['complete_values'][i],x['complete_values'][i+1]=x['complete_values'][i+1],x['complete_values'][i]
  with self.assertRaises(ValueError):m.validate_public_vectors(x,self.text)
 def test_rename_rejected(self):
  with self.assertRaises(ValueError):m.validate_public_vectors(self.display,self.text.replace('_warning_brightness','_wrong_brightness'))
 def test_duplicate_rejected(self):
  x=copy.deepcopy(self.display);x['complete_values'].append(x['complete_values'][0])
  with self.assertRaises(ValueError):m.validate_public_vectors(x,self.text)
 def test_unlisted_order_rejected(self):
  x=copy.deepcopy(self.display);x['complete_values'][0],x['complete_values'][1]=x['complete_values'][1],x['complete_values'][0]
  with self.assertRaises(ValueError):m.validate_public_vectors(x,self.text)
 def test_listed_tie_wrong_direction_rejected(self):
  x=copy.deepcopy(self.display);p=[i for i,r in enumerate(x['complete_values']) if r[:2]==[0,0x8d2]];a,b=p;x['complete_values'][a],x['complete_values'][b]=x['complete_values'][b],x['complete_values'][a]
  with self.assertRaises(ValueError):m.validate_public_vectors(x,self.text)
 def test_unlisted_old_tie_capture_rejected(self):
  text=self.text.replace('EGC_END','TEMP_UNLISTED').replace('EGC_START','EGC_END').replace('TEMP_UNLISTED','EGC_START')
  with self.assertRaises(ValueError):m.capture_observed_public_positions((B/'obj/th03/main.map').read_text('latin1'),text,self.inv)
 def test_idle_provider_reference_proof(self):self.assertEqual(len(m.idle_provider_reference_proof(B,W,self.model)['genuine_warning_references']),2)
 def test_idle_provider_drift_rejected(self):
  original=m.publics
  def bad(path):
   values=original(path)
   if path==W/'obj/th03/main.obj':
    next(p for p in values if p['name']=='TEXT_PUTSA')['offset']+=1
   return values
  with patch.object(m,'publics',side_effect=bad),self.assertRaises(ValueError):m.idle_provider_reference_proof(B,W,self.model)
 def test_missing_genuine_reference_rejected(self):
  import review_th03_cpu_link_order as decoder
  mod,blocks=decoder.omf(W/'obj/th03/warning.obj',[dict(module='src/main/player/warning.cpp',segment='PLAYER_M_TEXT',start=0xc7a5)])
  for b in blocks:b['fixups']=[f for f in b['fixups'] if f['target']!='TEXT_PUTSA']
  with patch.object(decoder,'omf',return_value=(mod,blocks)),self.assertRaises(ValueError):m.idle_provider_reference_proof(B,W,self.model)
 def test_wrong_idle_reference_target_rejected(self):
  import review_th03_cpu_link_order as decoder
  mod,blocks=decoder.omf(W/'obj/th03/warning.obj',[dict(module='src/main/player/warning.cpp',segment='PLAYER_M_TEXT',start=0xc7a5)])
  next(f for b in blocks for f in b['fixups'] if f['target']=='TEXT_PUTSA')['target']='WRONG'
  with patch.object(decoder,'omf',return_value=(mod,blocks)),self.assertRaises(ValueError):m.idle_provider_reference_proof(B,W,self.model)
 def test_wrong_resolved_idle_address_rejected(self):
  original=m.resolved_public
  def bad(p,rows):
   x=original(p,rows);return (x[0],x[1]+1,x[2]) if p['name']=='TEXT_PUTSA' else x
  with patch.object(m,'resolved_public',side_effect=bad),self.assertRaises(ValueError):m.idle_provider_reference_proof(B,W,self.model)
 def test_modified_idle_provider_record_rejected(self):
  original=m.publics
  def bad(path):
   values=original(path)
   if path==W/'obj/th03/main.obj':next(p for p in values if p['name']=='TEXT_PUTSA')['record_sha256']='bad'
   return values
  with patch.object(m,'publics',side_effect=bad),self.assertRaises(ValueError):m.idle_provider_reference_proof(B,W,self.model)
 def test_modified_idle_provider_order_rejected(self):
  original=m.publics
  def bad(path):
   values=original(path)
   if path==W/'obj/th03/main.obj':
    a,b=[i for i,p in enumerate(values) if p['name'] in ('TEXT_PUTSA','PALETTE_BLACK_OUT')];values[a],values[b]=values[b],values[a]
   return values
  with patch.object(m,'publics',side_effect=bad),self.assertRaises(ValueError):m.idle_provider_reference_proof(B,W,self.model)
 def test_production_entry_requires_idle_proof(self):
  with patch.object(m,'idle_provider_reference_proof',side_effect=ValueError('required proof')),self.assertRaisesRegex(ValueError,'required proof'):m.validate(PRIVATE,B,W)
 def test_production_entry_positive(self):self.assertTrue(m.validate(PRIVATE,B,W)['retained_map_supplement_pass'])
 def test_exact_two_idle_transitions(self):self.assertEqual(len(m.check_idle_transitions((B/'obj/th03/main.map').read_text('latin1'),self.text)),2)
 def test_missing_idle_change_rejected(self):
  text=self.text.replace('       PALETTE_BLACK_OUT',' idle  PALETTE_BLACK_OUT')
  with self.assertRaises(ValueError):m.check_idle_transitions((B/'obj/th03/main.map').read_text('latin1'),text)
 def test_wrong_idle_flag_rejected(self):
  text=self.text.replace('       TEXT_PUTSA',' idle  TEXT_PUTSA')
  with self.assertRaises(ValueError):m.validate_public_vectors(self.display,text)
 def test_extra_idle_change_rejected(self):
  before=(B/'obj/th03/main.map').read_text('latin1');flags=m.flags_by_section(before)[0];key=next(k for k,v in flags.items() if v and k not in m.IDLE_TRANSITIONS and k in m.flags_by_section(self.text)[0]);name=key[2];text=self.text.replace('idle  '+name,'      '+name)
  with self.assertRaises(ValueError):m.check_idle_transitions(before,text)
@unittest.skipUnless(HAS_PRIVATE,'private retained proof fixtures unavailable')
class HelperEquivalenceTests(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.frozen=json.loads((W.parent/'prelink-model.json').read_text());c.paths={n:W/spec['path'] for n,spec in tc.PRODUCERS.items()}
 def test_whole_model_matches_retained_v06(self):
  fresh=tm.build_model(PRIVATE,B,W/'obj/th03/main.obj',self.paths,(W/'obj/th03/main.@l').read_bytes());self.assertEqual(json.loads(json.dumps(fresh)),self.frozen)
 def test_map_matches_reviewed_supplement(self):
  expected=json.loads((P/'production-validation.json').read_text());self.assertEqual(json.loads(json.dumps(m.validate(PRIVATE,B,W))),expected)
 def test_warning_gate_matches_frozen_prelink(self):self.assertEqual(wg.validate(W/'obj/th03/warning.obj',PRIVATE),self.frozen['warning_call_validation'])
 def test_retained_link_all_conjunctive_gates(self):
  r=tc.check_link(W,PRIVATE,B,self.frozen,pc98,parser);self.assertTrue(r['pass_']);self.assertTrue(r['actual_fresh_OMF_structure_pass']);self.assertEqual((r['full_raw_owned_bytes'],r['whole_literal_count'],r['owned_literal_count'],r['outside_literal_count']),(3433,1553,83,1470))
 def test_structural_fail_rejects_raw_exact_product(self):
  with patch.object(tm,'root_stream',side_effect=ValueError('structural FAIL raw PASS')),self.assertRaisesRegex(ValueError,'structural FAIL raw PASS'):tc.check_link(W,PRIVATE,B,self.frozen,pc98,parser)
 def test_real_wrong_root_object_rejects_existing_exact_exe(self):
  original=Path.read_bytes;bad=(B/'obj/th03/main.obj').read_bytes()
  with patch.object(Path,'read_bytes',lambda path:bad if path==W/'obj/th03/main.obj' else original(path)),self.assertRaisesRegex(ValueError,'SEGDEF vector'):tc.check_link(W,PRIVATE,B,self.frozen,pc98,parser)
 def test_real_old_warning_object_rejects_existing_exact_exe(self):
  original=Path.read_bytes;bad=(PRIVATE/wg.REFERENCE).read_bytes()
  with patch.object(Path,'read_bytes',lambda path:bad if path==W/'obj/th03/warning.obj' else original(path)),self.assertRaisesRegex(ValueError,'four-call critical record delta'):tc.check_link(W,PRIVATE,B,self.frozen,pc98,parser)
 def test_full_map_fail_rejects_raw_exact_product(self):
  with patch.object(m,'validate',side_effect=ValueError('MAP structure FAIL')),self.assertRaisesRegex(ValueError,'MAP structure FAIL'):tc.check_link(W,PRIVATE,B,self.frozen,pc98,parser)
 def test_nonrelocation_header_mutation_rejected(self):
  original=Path.read_bytes;dest=W/'bin/th03/main.exe';bad=bytearray(dest.read_bytes());bad[18]^=1
  with patch.object(Path,'read_bytes',lambda p:bytes(bad) if p==dest else original(p)),self.assertRaisesRegex(ValueError,'header'):tc.check_link(W,PRIVATE,B,self.frozen,pc98,parser)
 def test_extra_overlay_mutation_rejected(self):
  original=Path.read_bytes;dest=W/'bin/th03/main.exe';bad=dest.read_bytes()+b'overlay mutation'
  with patch.object(Path,'read_bytes',lambda p:bad if p==dest else original(p)),self.assertRaisesRegex(ValueError,'file size'):tc.check_link(W,PRIVATE,B,self.frozen,pc98,parser)
 def test_bad_frozen_stream_rejected(self):
  x=copy.deepcopy(self.frozen);x['full_literal_stream'][0],x['full_literal_stream'][1]=x['full_literal_stream'][1],x['full_literal_stream'][0]
  with self.assertRaises(ValueError):tc.check_link(W,PRIVATE,B,x,pc98,parser)
class PortableTests(unittest.TestCase):
 def test_production_no_ignored_executable_imports(self):
  import ast
  for name in ('th03_tail_model.py','th03_tail_warning_gate.py','th03_tail_map.py','th03_tail_compare.py'):
   text=(ROOT/'scripts/lib'/name).read_text();tree=ast.parse(text)
   self.assertNotIn('spec_from_file_location',text);self.assertNotIn('exec(',text)
   for node in ast.walk(tree):
    if isinstance(node,ast.ImportFrom):self.assertFalse((node.module or '').startswith('.analysis'))
if __name__=='__main__':unittest.main(verbosity=2)
