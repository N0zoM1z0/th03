"""UI integration uses exact published inventory without physical/authored inflation."""
import copy
import csv
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

ROOT = Path.cwd()
SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
def load(name):
    spec = importlib.util.spec_from_file_location('acceptance_ui_' + name, SOURCE / ('scripts/' + name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ROOT = ROOT
    return module
status = load('status')
progress = load('progress')
CURRENT_UNITS = list(csv.DictReader((ROOT / 'config/units.csv').read_text().splitlines()))
# This suite exercises the frozen 145-owner publication, with its original
# containing GRCG/STR_IEQ boundaries. Current source scopes use 150 extents.
UNITS = [dict(u) for u in CURRENT_UNITS if u['id'] not in {
    'th03-mainl-decoded-staff-data',
    'th03-mainl-decoded-root-tail-grcg-setcolor-align','th03-mainl-decoded-root-tail-grcg-off',
    'th03-mainl-decoded-root-tail-grcg-off-align','th03-mainl-decoded-root-tail-string-compare'}]
for unit in UNITS:
    if unit['id']=='th03-mainl-decoded-root-tail-grcg':unit.update(size='48',compare_size='48')
    if unit['id']=='th03-mainl-decoded-root-tail-compare-align':unit.update(size='57',compare_size='57')
IDS = sorted(u['id'] for u in UNITS if u['artifact'] == 'th03-mainl' and u['state'] != 'excluded')
def accepted():
    return dict(product_exact=True, decoded_exact_units=145, decoded_exact_unit_ids=IDS,
                decoded_authored_exact_units=144, decoded_library_exact_units=1,
                decoded_authored_bytes=27753, decoded_library_bytes=628,
                mixed_physical_exact_bytes=37975, mixed_authored_credit_bytes=0)

class Tests(unittest.TestCase):
    def setUp(self):
        # This suite models the historical full-product publication. A live
        # current scoped publication must not select a different test namespace.
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        scoped = patch.object(status, 'MAINL_SCOPED_PUBLICATION', Path(folder.name) / 'absent.json')
        scoped.start()
        self.addCleanup(scoped.stop)
    def run_status(self, receipt=None, units=None):
        loader = SimpleNamespace(load_status=Mock(return_value=accepted() if receipt is None else receipt))
        with patch.dict(sys.modules, {'lib.mainl_product_acceptance': loader}):
            return status.mainl_product_status(ROOT, UNITS if units is None else units)
    def render(self, receipt, units=None):
        loader = SimpleNamespace(load_status=Mock(return_value=receipt))
        with patch.dict(sys.modules, {'lib.mainl_product_acceptance': loader, 'status': status}), patch.object(progress, 'mainl_fullcold_current_proven', return_value=True):
            return progress.render_svg(UNITS if units is None else units, [], [])
    def assert_zero(self, result):
        self.assertFalse(result['product_exact'])
        for key in ['decoded_exact_units', 'decoded_authored_exact_units', 'decoded_library_exact_units', 'decoded_authored_bytes', 'decoded_library_bytes', 'mixed_physical_exact_bytes', 'mixed_authored_credit_bytes']:
            self.assertEqual(result[key], 0, key)
        self.assertEqual(result['decoded_exact_unit_ids'], [])
    def test_published_identical_inventory_accepts_145(self):
        result = self.run_status()
        self.assertEqual(result['decoded_exact_units'], 145)
        self.assertEqual(set(result['decoded_exact_unit_ids']), set(IDS))
        self.assertEqual(result['mixed_authored_credit_bytes'], 0)
    def test_pending_receipt_cannot_leak_stale_counts(self):
        receipt = accepted(); receipt['product_exact'] = False
        self.assert_zero(self.run_status(receipt))
    def test_historical_receipt_cannot_accept_the_refined_current_inventory(self):
        self.assert_zero(self.run_status(units=CURRENT_UNITS))
    def test_missing_publication_is_zero(self):
        self.assert_zero(self.run_status({'product_exact': False}))
    def test_arbitrary_145_fixture_ids_never_inherit_live_acceptance(self):
        rows = copy.deepcopy(UNITS)
        for row in rows:
            if row['artifact'] == 'th03-mainl': row['id'] = 'fixture-' + row['id']
        self.assert_zero(self.run_status(units=rows))
    def test_duplicate_or_partial_caller_inventory_rejected(self):
        rows = [u for u in UNITS if u['artifact'] == 'th03-mainl' and u['state'] != 'excluded']
        for bad in [rows[:-1], rows + [rows[0]], rows[:-1] + [rows[0]]]:
            with self.subTest(length=len(bad)): self.assert_zero(self.run_status(units=bad))
    def test_duplicate_partial_or_wrong_published_ids_rejected(self):
        for ids in [IDS[:-1], IDS[:-1] + [IDS[0]], IDS[:-1] + ['fixture-extra']]:
            receipt = accepted(); receipt['decoded_exact_unit_ids'] = ids
            with self.subTest(ids=ids[-2:]): self.assert_zero(self.run_status(receipt))
    def test_published_count_disagrees_with_ids_rejected(self):
        receipt = accepted(); receipt['decoded_exact_units'] = 144
        self.assert_zero(self.run_status(receipt))
    def test_excluded_and_other_artifact_rows_do_not_change_inventory(self):
        rows = UNITS + [dict(id=IDS[0], artifact='th03-mainl', state='excluded'), dict(id='other', artifact='th03-op', state='exact')]
        self.assertEqual(self.run_status(units=rows)['decoded_exact_units'], 145)
    def test_svg_pending_zero_and_published_145_footer(self):
        receipt = accepted(); receipt['product_exact'] = False
        pending = self.render(receipt)
        self.assertIn('Unit acceptance: exact 0/145', pending)
        self.assertIn('order 0 / 677 · exact 0', pending)
        published = self.render(accepted())
        self.assertIn('Decoded acceptance: exact 145/145', published)
        self.assertIn('MAINL product + decoded accepted', published)
        self.assertNotIn('order 0 / 677 · exact 0', published)
        self.assertIn('width="270.00" height="12" fill="#55c7a6"', published)
        self.assertIn('whole-game % unknown', published)
    def test_svg_fixture_does_not_paint_accepted_footer(self):
        rows = [copy.deepcopy(next(u for u in UNITS if u['id'] == IDS[0]))]
        rows[0]['id'] = 'synthetic-owner'
        svg = self.render(accepted(), rows)
        self.assertIn('Unit acceptance: exact 0/1', svg)
        self.assertNotIn('MAINL product + decoded accepted', svg)
    def test_file_backed_and_source_accounting_unchanged(self):
        before = status.artifact_report({'id': 'th03-mainl', 'size': 37975}, UNITS, [], [])
        counts = progress.mainl_unit_progress(UNITS)
        self.run_status()
        after = status.artifact_report({'id': 'th03-mainl', 'size': 37975}, UNITS, [], [])
        self.assertEqual(before, after)
        self.assertEqual(progress.mainl_unit_progress(UNITS), counts)
        self.assertEqual((counts['source'], counts['source_bytes'], counts['exact']), (145, 28381, 0))
        self.assertEqual(after['exact_authored_bytes'], 0)
        self.assertEqual(after['known_authored_bytes'], 0)
        self.assertIsNone(after['exact_authored_percent'])
if __name__ == '__main__': unittest.main()
