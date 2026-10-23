"""Portable retained annotation controls. No full replay/native/model execution."""
import ast
import csv
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
ROOT=Path.cwd()
SOURCE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
m=load('lib.op_product_diagnostics',SOURCE/'scripts/lib/op_product_diagnostics.py')
p=load('product_progress_test',SOURCE/'scripts/progress.py');p.ROOT=ROOT
import status
UNITS=list(csv.DictReader((ROOT/'config/units.csv').open()))
FUNCTIONS=list(csv.DictReader((ROOT/'config/th03_main_authored_functions.csv').open()))
EVIDENCE=list(csv.DictReader((ROOT/'config/evidence.csv').open()))
ORIGINAL_CHECKED=m.checked
def fixture_read(root,name):
    # Explicit synthetic helper-retention fixture; never used by production guard.
    if name=='.analysis/gpt-dots-player-cpu-acceptance-install-v01/support.py' and not (Path(root)/name).exists():
        return b'fixture only: helper presence/hash are mocked, never executed'
    return ORIGINAL_CHECKED(root,name)
class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.started=time.perf_counter()
        cls.actual=m.retained_op_products(ROOT)
        cls.seconds=time.perf_counter()-cls.started
        cls.display=dict(cls.actual,retained_equality=True)  # Explicit UI-only valid fixture.
    def svg(self,products):
        with patch.object(status,'mainl_product_status',return_value={'product_exact':False}):
            return p.render_svg(UNITS,FUNCTIONS,EVIDENCE,
                op_status={'decoded_accepted':False},op_products=products)
    def test_actual_retained_allowlist(self):
        unavailable=[]
        for name in m.PINS:
            try:m.checked(ROOT,name)
            except (OSError,ValueError):unavailable.append(name)
        self.assertEqual(self.actual['retained_equality'],not unavailable,self.actual.get('reason'))
        self.assertFalse(self.actual['product_acceptance'])
        self.assertFalse(self.actual['canonical_credit_changed'])
        self.assertFalse(self.actual['full_replay_now'])
        self.assertFalse(self.actual['current_source_compatibility_checked'])
        self.assertFalse(self.actual['cold_outputs_packed'])
        self.assertIsNone(self.actual['whole_game_percentage'])
    @unittest.skipUnless(all((ROOT/name).is_file() for name in m.PINS), "archived native fixtures unavailable")
    def test_valid_contract_with_explicit_helper_retention_fixture(self):
        with patch.object(m,'checked',side_effect=fixture_read):
            result=m.retained_op_products(ROOT)
            self.assertTrue(result['retained_equality'],result.get('reason'))
    def test_missing_or_drifted_pin_fails_closed(self):
        for name in m.PINS:
            with self.subTest(path=name):
                original=fixture_read
                def bad(root,n):
                    if n==name: raise ValueError('missing or drifted selected pin')
                    return original(root,n)
                with patch.object(m,'checked',side_effect=bad):
                    self.assertFalse(m.retained_op_products(ROOT)['retained_equality'])
    def test_pin_hash_rejects_changed_bytes(self):
        with tempfile.TemporaryDirectory(dir=SOURCE) as td:
            root=Path(td);f=root/'fixture';f.write_bytes(b'wrong')
            with patch.object(m,'PINS',{'fixture':{'bytes':5,'sha256':'0'*64}}):
                with self.assertRaisesRegex(ValueError,'drift'):m.checked(root,'fixture')
    def test_symlink_pin_rejects(self):
        with tempfile.TemporaryDirectory(dir=SOURCE) as td:
            root=Path(td);(root/'target').write_bytes(b'wrong');(root/'fixture').symlink_to(root/'target')
            with patch.object(m,'PINS',{'fixture':{'bytes':5,'sha256':'0'*64}}):
                with self.assertRaisesRegex(ValueError,'regular'):m.checked(root,'fixture')
    def test_retained_claim_cannot_promote_cold_packing_or_acceptance(self):
        original=fixture_read
        for key,value in [('packed_equality',True),('exact_acceptance',True),
                          ('runtime',True),('actual_native_phases',61)]:
            def bad(root,n):
                raw=original(root,n)
                if n=='.analysis/op-fullcold-exact-terminal-20261022-v01.json':
                    obj=json.loads(raw);obj[key]=value;return json.dumps(obj).encode()
                return raw
            with self.subTest(key=key),patch.object(m,'checked',side_effect=bad):
                self.assertFalse(m.retained_op_products(ROOT)['retained_equality'])
    def test_display_preserves_source_counts_and_scoped_axis(self):
        svg=self.svg(self.display)
        self.assertIn('Source 45/46',svg)
        self.assertIn('Unit acceptance: exact 0/46',svg)
        self.assertIn('Retained: cold decoded 63,866 B = target',svg)
        self.assertIn('separate packed 36,041 B = canonical',svg)
        self.assertNotIn('whole product open',svg)
        ET.fromstring(svg)
    def test_no_diagnostic_on_failure_retains_historical_annotation(self):
        svg=self.svg({'retained_equality':False,'reason':'missing'})
        self.assertNotIn('Retained: cold decoded',svg)
        self.assertIn('Retained equality check unavailable',svg)
        self.assertIn('Retained cold pair: 29 raw pairs',svg)
    def test_accepted33_axis_unchanged(self):
        with patch.object(status,'mainl_product_status',return_value={'product_exact':False}):
            svg=p.render_svg(UNITS,FUNCTIONS,EVIDENCE,
                op_status={'decoded_accepted':True,'decoded_exact_units':33},op_products=self.display)
        self.assertIn('Decoded extents 33/46',svg)
        self.assertIn('Published decoded scopes: 9,530 B',svg)
        self.assertIn('product acceptance open',svg)
    def test_non_op_svg_layout_unchanged(self):
        a=ET.fromstring(self.svg(self.display));b=ET.fromstring(self.svg({'retained_equality':False}))
        for tree in [a,b]:
            for node in list(tree):
                if ''.join(node.itertext()).startswith(('Retained: cold decoded','Retained equality check unavailable')):
                    tree.remove(node)
        # Whitespace-only XML tails are formatting, not rendered positions/content.
        for tree in [a,b]:
            for node in tree.iter():
                if node.tail is not None and not node.tail.strip():node.tail=None
        self.assertEqual(ET.tostring(a),ET.tostring(b))
    def test_prose_states_separate_runs_and_limits(self):
        text=m.product_diagnostic_summary(self.display)
        for phrase in ['separate source-fed packing','cold outputs themselves were not packed',
                       'does not rerun','Product acceptance, runtime and whole-product authorship remain open',
                       'fixed 33-owner']:
            self.assertIn(phrase,text)
    def test_no_slow_replay_or_native_import(self):
        tree=ast.parse((SOURCE/'scripts/lib/op_product_diagnostics.py').read_text())
        imports=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
        imports += [a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names]
        self.assertEqual(set(imports),{'hashlib','json','pathlib'})
        self.assertFalse(any(isinstance(n,ast.Attribute) and n.attr in ['rglob','glob','replay','run','system']
                             for n in ast.walk(tree)))
    def test_docs_svg_share_one_product_guard(self):
        tree=ast.parse((SOURCE/'scripts/progress.py').read_text())
        main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
        calls=[n for n in ast.walk(main) if isinstance(n,ast.Call)]
        self.assertEqual(sum(isinstance(n.func,ast.Name) and n.func.id=='retained_op_products' for n in calls),1)
        render=next(n for n in calls if isinstance(n.func,ast.Name) and n.func.id=='render_svg')
        self.assertIn('op_products',[k.arg for k in render.keywords])
if __name__=='__main__':unittest.main()
