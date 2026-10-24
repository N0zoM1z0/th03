"""Portable UI and negative controls; no retained replay/native/model execution."""
import ast
import copy
import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path.cwd()
SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
def module(name, path):
    spec=importlib.util.spec_from_file_location(name,path)
    value=importlib.util.module_from_spec(spec);sys.modules[name]=value
    spec.loader.exec_module(value);return value
a=module('lib.op_decoded_progress',SOURCE/'scripts/lib/op_decoded_progress.py')
p=module('op_progress_under_test',SOURCE/'scripts/progress.py');p.ROOT=ROOT
import status
CORE=ROOT/'scripts/lib/op_decoded_acceptance.py'
if not CORE.exists():
    CORE=ROOT/'.analysis/op-decoded-acceptance-proposal-v02/scripts/lib/op_decoded_acceptance.py'
core=module('lib.op_decoded_acceptance',CORE)
UNITS=list(csv.DictReader((ROOT/'config/units.csv').open()))
FUNCTIONS=list(csv.DictReader((ROOT/'config/th03_main_authored_functions.csv').open()))
EVIDENCE=list(csv.DictReader((ROOT/'config/evidence.csv').open()))
COHORT=ROOT/'config/op_decoded_acceptance/cohort.json'
if not COHORT.exists():
    COHORT=ROOT/'.analysis/op-decoded-acceptance-proposal-v02/config/op_decoded_acceptance/cohort.json'
IDS=sorted(x['unit_id'] for x in json.loads(COHORT.read_text())['owners'])
VALID=dict(repository_local=True,reviewed_proof_ready=True,product_exact=False,
    factory_accepted=False,canonical_credit_changed=False,whole_game_percentage=None,
    mixed_physical_exact_bytes=0,decoded_exact_units=33,decoded_authored_bytes=9530,
    decoded_exact_unit_ids=IDS)
class Tests(unittest.TestCase):
    def accepted(self, value=None, units=None):
        with patch.object(a,'read_publication',return_value=VALID if value is None else value):
            return a.op_decoded_status(ROOT,UNITS if units is None else units)
    def render(self,value):
        with patch.object(status,'mainl_product_status',return_value={'product_exact':False}):
            # The historical OP fixture does not select the live ZUN axis.
            return p.render_svg(UNITS,FUNCTIONS,EVIDENCE,op_status=value,zun_status={'decoded_accepted':False})
    def test_synthetic_inventory_never_runs_verifier(self):
        with patch.object(a,'read_publication') as read:
            self.assertFalse(a.op_decoded_status(ROOT,[])['decoded_accepted'])
            read.assert_not_called()
    def test_valid_fixed_scopes_use_current_49_denominator(self):
        s=self.accepted()
        self.assertTrue(s['decoded_accepted']);self.assertEqual(s['tracked_decoded_extents'],49)
        self.assertEqual(s['decoded_exact_units'],33);self.assertEqual(s['decoded_authored_bytes'],9530)
        self.assertFalse(s['canonical_credit_changed']);self.assertFalse(s['product_exact'])
    def test_false_boundaries_fail_closed(self):
        for key,value in [('product_exact',True),('factory_accepted',True),
            ('canonical_credit_changed',True),('whole_game_percentage',73),
            ('mixed_physical_exact_bytes',9530),('reviewed_proof_ready',False),
            ('decoded_exact_units',44),('decoded_authored_bytes',12940)]:
            with self.subTest(key=key):
                s=self.accepted(dict(VALID,**{key:value}))
                self.assertFalse(s['decoded_accepted']);self.assertEqual(s['decoded_exact_units'],0)
    def test_missing_stale_fabricated_status_falls_back(self):
        for reason in ['publication missing','binding drift config/units.csv','publication schema']:
            s=self.accepted(a.unavailable(reason))
            self.assertFalse(s['decoded_accepted']);self.assertIn(reason,a.decoded_summary(s))
            self.assertIn('Retained cold pair: 29 raw pairs',self.render(s))
            self.assertIn('Unit acceptance: exact 0/49',self.render(s))
    def test_duplicate_accepted_ids_reject(self):
        self.assertFalse(self.accepted(dict(VALID,decoded_exact_unit_ids=IDS[:-1]+[IDS[0]]))['decoded_accepted'])
    def test_unknown_accepted_id_reject(self):
        self.assertFalse(self.accepted(dict(VALID,decoded_exact_unit_ids=IDS[:-1]+['unknown']))['decoded_accepted'])
    def test_caller_source_size_state_or_id_changes_reject(self):
        for field,value in [('source','wrong'),('size','1'),('state','excluded'),('id','wrong')]:
            units=copy.deepcopy(UNITS);next(u for u in units if u['id']==IDS[0])[field]=value
            with self.subTest(field=field):
                self.assertFalse(self.accepted(units=units)['decoded_accepted'])
    def test_duplicate_caller_rows_reject(self):
        self.assertFalse(self.accepted(units=UNITS+[next(u for u in UNITS if u['id']==IDS[0])])['decoded_accepted'])
    def test_later_source_units_not_automatically_enrolled(self):
        s=self.accepted()
        active=[u for u in UNITS if u['artifact']=='th03-op' and u['state']=='source-present']
        self.assertEqual(len(active),48)
        self.assertEqual(len(set(u['id'] for u in active)-set(s['decoded_exact_unit_ids'])),15)
        self.assertFalse(any('character-selection' in i for i in s['decoded_exact_unit_ids']))
    def test_svg_scoped_extent_axis_and_original_layout(self):
        s=self.accepted();svg=self.render(s);root=ET.fromstring(svg)
        self.assertIn('Decoded extents 33/49',svg);self.assertNotIn('33/33',svg)
        self.assertIn('Published decoded scopes: 9,530 B',svg)
        self.assertNotIn('Retained cold pair: 29 raw pairs',svg)
        self.assertIn('Source 48/49',svg)
        texts=[''.join(x.itertext()) for x in root.iter() if x.tag.endswith('text')]
        zun_units=sum(u['artifact']=='th03-zun' and u['state']!='excluded' for u in UNITS)
        self.assertIn(f'Unit acceptance: exact 0/{zun_units}',texts)
        baseline=ET.fromstring(self.render(a.unavailable('missing')))
        # Every non-OP element remains byte-identical in this branch.
        self.assertEqual([ET.tostring(x) for x in list(root)[15:]],
                         [ET.tostring(x) for x in list(baseline)[15:]])
    def test_docs_scope_and_no_whole_completion(self):
        text=a.decoded_summary(self.accepted())
        for needle in ['33/49 tracked decoded extents','9,530 scoped decoded bytes',
                       'excludes selection','whole-game percentage remains unknown',
                       'not a pure-instruction']:
            self.assertIn(needle,text)
    def test_missing_publication_does_not_import_or_spawn(self):
        with tempfile.TemporaryDirectory(dir=SOURCE) as temp, patch.object(a.subprocess,'run') as run:
            self.assertEqual(a.read_publication(Path(temp))['reason'],'publication missing')
            run.assert_not_called()
    def test_fabricated_publication_rejected_by_real_core(self):
        with tempfile.TemporaryDirectory(dir=SOURCE) as temp:
            root=Path(temp);f=root/a.PUBLICATION;f.parent.mkdir(parents=True);f.write_text('{"schema":"fake"}')
            with patch.object(a.importlib.util,'find_spec',return_value=object()),patch.object(a.subprocess,'run') as run:
                self.assertEqual(a.read_publication(root)['decoded_exact_units'],0)
                run.assert_not_called()
    def test_missing_dependency_without_fallback_is_visible(self):
        with tempfile.TemporaryDirectory(dir=SOURCE) as temp:
            root=Path(temp);f=root/a.PUBLICATION;f.parent.mkdir(parents=True);f.write_text('{}')
            with patch.object(a.importlib.util,'find_spec',return_value=None):
                self.assertIn('Capstone missing',a.read_publication(root)['reason'])
    def test_missing_dependency_uses_only_readonly_venv_status(self):
        with tempfile.TemporaryDirectory(dir=SOURCE) as temp:
            root=Path(temp);f=root/a.PUBLICATION;f.parent.mkdir(parents=True);f.write_text('{}')
            python=root/'.venv/bin/python';python.parent.mkdir(parents=True);python.touch()
            result=types.SimpleNamespace(stdout=json.dumps(VALID))
            with patch.object(a.importlib.util,'find_spec',return_value=None),patch.object(a.subprocess,'run',return_value=result) as run:
                self.assertEqual(a.read_publication(root)['decoded_exact_units'],33)
                args=run.call_args.args[0]
                self.assertEqual(args[1:3],['-B','-c'])
                self.assertIn('load_status',args[3]);self.assertNotIn('prepare',args[3])
                self.assertNotIn('replay_th03_op',args[3]);self.assertEqual(run.call_args.kwargs['timeout'],120)
    def test_fallback_failure_and_bad_json_are_visible(self):
        with tempfile.TemporaryDirectory(dir=SOURCE) as temp:
            root=Path(temp);f=root/a.PUBLICATION;f.parent.mkdir(parents=True);f.write_text('{}')
            python=root/'.venv/bin/python';python.parent.mkdir(parents=True);python.touch()
            with patch.object(a.importlib.util,'find_spec',return_value=None),patch.object(a.subprocess,'run',side_effect=RuntimeError('no capstone')):
                self.assertIn('fallback failed',a.read_publication(root)['reason'])
    def test_core_status_verify_has_no_cold_replay_calls(self):
        tree=ast.parse(CORE.read_text())
        for node in tree.body:
            if isinstance(node,ast.FunctionDef) and node.name in ['verify','load_status','physical_audit']:
                calls=[x for x in ast.walk(node) if isinstance(x,ast.Call)]
                self.assertFalse(any(isinstance(x.func,ast.Attribute) and x.func.attr in ['replay','prepare','run'] for x in calls))
    def test_progress_main_shares_one_status_for_docs_and_svg(self):
        tree=ast.parse((SOURCE/'scripts/progress.py').read_text())
        main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
        calls=[n for n in ast.walk(main) if isinstance(n,ast.Call)]
        self.assertEqual(sum(isinstance(n.func,ast.Name) and n.func.id=='op_decoded_status' for n in calls),1)
        render=next(n for n in calls if isinstance(n.func,ast.Name) and n.func.id=='render_svg')
        self.assertIn('op_status',[k.arg for k in render.keywords])
if __name__=='__main__':unittest.main()
