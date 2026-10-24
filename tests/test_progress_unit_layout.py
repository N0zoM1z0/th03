"""Unit axes and layout do not turn historical diagnostics into exact credit."""
import csv
from contextlib import ExitStack
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
ROOT=Path.cwd()
SOURCE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('unit_layout_progress',SOURCE/'scripts/progress.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p);p.ROOT=ROOT
N={'s':'http://www.w3.org/2000/svg'}
def row(i='one',artifact='th03-zun',**kw):
 r=dict(id=i,artifact=artifact,state='source-present',boundary_state='reviewed',source='src/owner.asm',size='10');r.update(kw);return r
class Tests(unittest.TestCase):
 def test_source_state_requires_path_and_excluded_not_counted(self):
  rows=[row(),row('none',source=''),row('pending',state='candidate'),row('old',state='excluded')]
  self.assertEqual(p.tracked_unit_progress(rows,'th03-zun'),dict(total=3,reviewed=3,source=1,exact=0))
 def test_duplicate_active_ids_reject_both_unit_axes(self):
  for artifact in ['th03-op','th03-zun']:
   with self.subTest(artifact=artifact),self.assertRaisesRegex(ValueError,'duplicate'):
    p.tracked_unit_progress([row(artifact=artifact),row(artifact=artifact)],artifact)
 def test_unrelated_function_rows_cannot_inflate_op_or_zun(self):
  rows=[row(artifact='th03-op'),row(artifact='th03-zun')]
  funcs=[dict(artifact=a,boundary_state='reviewed',state='exact') for a in ['th03-op','th03-zun'] for _ in range(99)]
  svg=p.render_svg(rows,funcs,[])
  self.assertNotIn('99 tracked functions',svg)
  self.assertEqual(svg.count('Unit acceptance: exact 0/1'),2)
 def test_real_unit_source_totals_and_main_function_axis(self):
  units=list(csv.DictReader((ROOT/'config/units.csv').read_text().splitlines()))
  self.assertEqual((p.tracked_unit_progress(units,'th03-op')['source'],p.tracked_unit_progress(units,'th03-op')['total']),(45,46))
  self.assertEqual((p.tracked_unit_progress(units,'th03-zun')['source'],p.tracked_unit_progress(units,'th03-zun')['total']),(32,34))
  authored=[u for u in units if u['artifact']=='th03-zun' and u['source'] and u['origin']=='authored']
  self.assertEqual((len(authored),sum(int(u['size'],0) for u in authored)),(15,1855))
  funcs=[dict(artifact='th03-main',boundary_state='reviewed',state='candidate')]*413
  svg=p.render_svg(units,funcs,[])
  self.assertIn('413 tracked functions',svg)
  self.assertIn('Source 45/46',svg);self.assertIn('Source 32/34',svg)
 def test_empty_unit_inventory_has_zero_width_not_fake_function_counts(self):
  svg=p.render_svg([],[],[])
  root=ET.fromstring(svg)
  groups=[g for g in root.findall('s:g',N) if g.attrib.get('aria-label','').startswith(('OP.EXE','ZUN.COM'))]
  self.assertEqual(len(groups),2)
  for g in groups:
   self.assertIn('0 tracked unit extents',''.join(g.itertext()))
   green=[x for x in g.findall('s:rect',N) if x.attrib.get('fill')=='#55c7a6']
   self.assertEqual([float(x.attrib['width']) for x in green],[0.0])
 def test_annotations_and_footer_fit_distinct_reserved_regions(self):
  with patch.object(p,'zun_init_standalone_retained',return_value=True),patch.object(p,'zun_driver_hybrid_retained',return_value=True),patch.object(p,'zunsoft_root_source_proven',return_value=True),patch.object(p,'zun_resident_root_source_proven',return_value=True):
   root=ET.fromstring(p.render_svg([],[],[]))
  self.assertEqual(root.attrib['viewBox'],'0 0 788 550')
  texts=root.findall('.//s:text',N)
  ys={''.join(t.itertext()):float(t.attrib['y']) for t in texts}
  self.assertEqual(ys['ZUN.COM'],354)
  annotation_ys=[v for k,v in ys.items() if k.startswith(('Retained standalone init:','Maintained -2/-4 composition:','ZUN -3 root:','Maintained ZUN -3','Logo root:','Resident root:'))]
  self.assertEqual(sorted(annotation_ys),[394,410,426,442])
  self.assertTrue(all(380<y<=442 for y in annotation_ys))
  self.assertTrue(all(float(t.attrib['y'])<550 for t in texts))
  self.assertIn('452',ET.tostring(root,encoding='unicode'))
 def test_accepted_mainl_hides_only_stale_retained_and_open_order(self):
  import status
  accepted=dict(product_exact=True,decoded_exact_units=145)
  flags=['mainl_heap_retained','mainl_crt_source_proven','mainl_linked_game_source_proven','mainl_root_tail_source_proven','mainl_display_hardware_source_proven','mainl_archive_io_source_proven','mainl_resources_source_proven','mainl_pi_decoder_source_proven','mainl_root_source_proven','mainl_staff_source_proven','mainl_vsync_alignment_proven']
  with ExitStack() as stack:
   for name in flags: stack.enter_context(patch.object(p,name,return_value=True))
   with patch.object(status,'mainl_product_status',return_value=accepted): svg=p.render_svg([],[],[])
   with patch.object(status,'mainl_product_status',return_value=dict(product_exact=False,decoded_exact_units=0)): pending=p.render_svg([],[],[])
  self.assertIn('Heap: 8 procedures / 628 B retained-only',pending)
  self.assertIn('full program equal / order open',pending)
  self.assertNotIn('Heap: 8 procedures / 628 B retained-only',svg)
  self.assertNotIn('relocation order open',svg)
  self.assertNotIn('full program equal / order open',svg)
  self.assertIn('MAINL product + decoded accepted',svg)
if __name__=='__main__':unittest.main()
