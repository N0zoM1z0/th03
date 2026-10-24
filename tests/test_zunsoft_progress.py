"""Logo source visibility stays scoped and preserves the MAINL accepted axis."""
import copy,csv,importlib.util,sys,unittest,tempfile,shutil
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path.cwd()/'scripts'))
spec=importlib.util.spec_from_file_location('zun_progress',ROOT/'scripts/progress.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p);p.ROOT=ROOT
UNITS=list(csv.DictReader((ROOT/'config/units.csv').read_text().splitlines()))
EVIDENCE=list(csv.DictReader((ROOT/'config/evidence.csv').read_text().splitlines()))
class ZunsoftProgressTests(unittest.TestCase):
 def setUp(self):
  # These tests describe the historical precursor with an explicit padding
  # char. Keep that fixture separate from the current native -a2 producer.
  folder=tempfile.TemporaryDirectory();self.addCleanup(folder.cleanup);legacy=Path(folder.name)
  source=(ROOT/'src/zun/zunsoft.cpp').read_bytes()
  source=source.replace(b'#pragma option -2 -d- -a2 // ZUN bloat; native word alignment',b'#pragma option -2 -d- // ZUN bloat')
  if b'char wave_padding;' not in source:source=source.replace(b'char wave_amp;\n',b'char wave_amp;\nchar wave_padding;\n')
  target=legacy/'src/zun/zunsoft.cpp';target.parent.mkdir(parents=True);target.write_bytes(source)
  for name in ['config/zunsoft_root/proof.json','config/zunsoft_repeat/proof.json']:
   target=legacy/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
  current=patch.object(p,'ROOT',legacy);current.start();self.addCleanup(current.stop)
 def test_current_scope(self):
  self.assertTrue(p.zunsoft_root_source_proven(UNITS,EVIDENCE))
  z=[u for u in UNITS if u['artifact']=='th03-zun' and u['source']]
  self.assertEqual((len(z),sum(int(u['size']) for u in z)),(15,1855))
  self.assertFalse(any(u['state']=='exact' for u in z))
 def test_rejects_changed_source_and_extent_and_packed_offset(self):
  for key,value in [('source','src/zun/other.cpp'),('size','10096'),('file_offset','0x367'),('state','exact'),('origin','library'),('offset','0x368')]:
   q=copy.deepcopy(UNITS);next(u for u in q if u['id'] in p.ZUNSOFT_ROOT_UNITS)[key]=value
   with self.subTest(key=key):self.assertFalse(p.zunsoft_root_source_proven(q,EVIDENCE))
 def test_missing_duplicate_and_extra_units(self):
  u=next(u for u in UNITS if u['id'] in p.ZUNSOFT_ROOT_UNITS)
  self.assertFalse(p.zunsoft_root_source_proven([v for v in UNITS if v['id']!=u['id']],EVIDENCE))
  self.assertFalse(p.zunsoft_root_source_proven(UNITS+[u],EVIDENCE))
 def test_evidence_mutants(self):
  for key,value in [('result','fail'),('extent_size','10096'),('output_sha256','0'*64)]:
   q=copy.deepcopy(EVIDENCE);next(e for e in q if e['id']=='ev-th03-zunsoft-maintained-runtime')[key]=value
   with self.subTest(key=key):self.assertFalse(p.zunsoft_root_source_proven(UNITS,q))
 def test_missing_source_or_proof(self):
  with patch.object(p,'ROOT',ROOT/'absent'):self.assertFalse(p.zunsoft_root_source_proven(UNITS,EVIDENCE))
 def test_mainl_accepted_axis_and_logo_annotation_coexist(self):
  with patch('status.mainl_product_status',return_value={'product_exact':True,'decoded_exact_units':145}):
   svg=p.render_svg(UNITS,[],EVIDENCE)
  self.assertIn('Decoded acceptance: exact 145/145',svg)
  self.assertIn('MAINL product + decoded accepted',svg)
  self.assertIn('Logo root: 10 source units / 1,299 B',svg)
  self.assertIn('2 cold builds · 2,600 retained calls · exact 0',svg)
  self.assertNotIn('no second cold build',svg)
  self.assertNotIn('10,096 source',svg)
 def test_source_drift_hides_logo_not_mainl(self):
  q=copy.deepcopy(UNITS);next(u for u in q if u['id'] in p.ZUNSOFT_ROOT_UNITS)['source']=''
  with patch('status.mainl_product_status',return_value={'product_exact':True,'decoded_exact_units':145}):svg=p.render_svg(q,[],EVIDENCE)
  self.assertNotIn('Logo root: 10 source units',svg);self.assertIn('MAINL product + decoded accepted',svg)
 def test_repeat_proof_and_evidence_gate(self):
  self.assertTrue(p.zunsoft_root_repeat_proven(UNITS,EVIDENCE))
  for key,value in [('result','fail'),('extent_size','10096'),('output_sha256','0'*64),('evidence_class','runtime')]:
   q=copy.deepcopy(EVIDENCE);next(e for e in q if e['id']=='ev-th03-zunsoft-maintained-cold-repeat')[key]=value
   with self.subTest(key=key):
    self.assertFalse(p.zunsoft_root_repeat_proven(UNITS,q));self.assertTrue(p.zunsoft_root_source_proven(UNITS,q))
 def test_repeat_rejects_fabricated_packed_offsets(self):
  for eid in ['ev-th03-zunsoft-repeat-structure','ev-th03-zunsoft-maintained-cold-repeat']:
   row=next(e for e in EVIDENCE if e['id']==eid)
   self.assertEqual((row['extent_start'],row['extent_size']),('',''))
   self.assertIn('Decoded inner scope -3:0367/1299 CODE bytes',row['notes'])
   for key,value in [('extent_start','0x367'),('extent_start','0xC32'),('extent_size','1299')]:
    q=copy.deepcopy(EVIDENCE);next(e for e in q if e['id']==eid)[key]=value
    with self.subTest(evidence=eid,key=key,value=value):
     self.assertFalse(p.zunsoft_root_repeat_proven(UNITS,q));self.assertTrue(p.zunsoft_root_source_proven(UNITS,q))
 def test_repeat_missing_evidence_falls_back_to_original(self):
  q=[e for e in EVIDENCE if e['id']!='ev-th03-zunsoft-maintained-cold-repeat']
  self.assertFalse(p.zunsoft_root_repeat_proven(UNITS,q));self.assertTrue(p.zunsoft_root_source_proven(UNITS,q))
  with patch('status.mainl_product_status',return_value={'product_exact':True,'decoded_exact_units':145}):svg=p.render_svg(UNITS,[],q)
  self.assertIn('one build · exact 0',svg);self.assertNotIn('2,600 retained calls',svg)
 def test_repeat_requires_unit_links(self):
  q=copy.deepcopy(UNITS);u=next(u for u in q if u['id'] in p.ZUNSOFT_ROOT_UNITS);u['evidence_ids']=u['evidence_ids'].replace(';ev-th03-zunsoft-maintained-cold-repeat','')
  self.assertFalse(p.zunsoft_root_repeat_proven(q,EVIDENCE))
if __name__=='__main__':unittest.main()
