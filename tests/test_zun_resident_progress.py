"""Resident publication is two existing decoded units, never a canonical extent."""
import copy,csv,importlib.util,os,sys,unittest,xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch
ROOT=Path.cwd().resolve();SOURCE=Path(os.environ.get('TH03_RESIDENT_SOURCE_ROOT',str(ROOT))).resolve();sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('resident_progress_test',SOURCE/'scripts/progress.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
UNITS=list(csv.DictReader((SOURCE/'config/units.csv').read_text().splitlines()));EVIDENCE=list(csv.DictReader((SOURCE/'config/evidence.csv').read_text().splitlines()))
class ResidentProgressTests(unittest.TestCase):
 def proven(self,u=UNITS,e=EVIDENCE):
  with patch.object(p,'ROOT',SOURCE):return p.zun_resident_root_source_proven(u,e)
 def test_current_scope(self):
  # Maintained original ASM is visible separately and adds no authored credit.
  self.assertTrue(self.proven());z=[u for u in UNITS if u['artifact']=='th03-zun' and u['source'] and u['origin']=='authored'];self.assertEqual((len(z),sum(int(u['size']) for u in z)),(16,2179));self.assertFalse(any(u['state']=='exact' for u in z))
 def test_reject_owner_geometry_or_scope_drift(self):
  for key,value in [('offset','0x368'),('size','629'),('file_offset','0x4589'),('source','src/zun/zunsoft.cpp'),('state','exact'),('origin','library'),('segment','decoded:-3')]:
   q=copy.deepcopy(UNITS);next(u for u in q if u['id'] in p.ZUN_RESIDENT_UNITS)[key]=value
   with self.subTest(key=key):self.assertFalse(self.proven(q))
 def test_missing_duplicate_unit(self):
  row=next(u for u in UNITS if u['id'] in p.ZUN_RESIDENT_UNITS)
  self.assertFalse(self.proven([u for u in UNITS if u is not row]));self.assertFalse(self.proven(UNITS+[row]))
 def test_evidence_canonical_extent_forbidden(self):
  for key,value in [('extent_start','0x367'),('extent_size','322'),('result','fail'),('output_sha256','0'*64)]:
   q=copy.deepcopy(EVIDENCE);next(e for e in q if e['id']=='ev-th03-zun-resident-maintained-cold-pair')[key]=value
   with self.subTest(key=key):self.assertFalse(self.proven(e=q))
 def test_four_annotations_fit_existing_canvas(self):
  with patch.object(p,'zun_init_standalone_retained',return_value=True),patch.object(p,'zun_driver_hybrid_retained',return_value=True),patch.object(p,'zunsoft_root_source_proven',return_value=True),patch.object(p,'zun_resident_root_source_proven',return_value=True):svg=p.render_svg([],[],[])
  root=ET.fromstring(svg);self.assertEqual(root.attrib['viewBox'],'0 0 788 550');texts=root.findall('.//{http://www.w3.org/2000/svg}text');ys=[float(t.attrib['y']) for t in texts if ''.join(t.itertext()).startswith(('Retained standalone init:','Maintained -2/-4 composition:','Logo root:','Resident root:'))];self.assertEqual(sorted(ys),[394,410,426,442]);self.assertLess(max(ys),452)
if __name__=='__main__':unittest.main()
