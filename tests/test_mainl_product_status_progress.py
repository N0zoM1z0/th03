"""Current MAINL publication cannot inherit a historical or partial inventory."""
import csv
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import status


class MainlStatus(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.rows = [dict(id='first', artifact='th03-mainl', state='source-present'),
                     dict(id='second', artifact='th03-mainl', state='source-present')]
        publication = self.root / status.MAINL_SCOPED_PUBLICATION
        publication.parent.mkdir(parents=True)
        publication.write_text('{}')
        with (self.root / 'config/units.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=['id', 'artifact', 'state'])
            writer.writeheader()
            writer.writerows(self.rows)

    def test_identical_inventory_uses_current_verifier_without_a_frozen_count(self):
        result = dict(product_exact=False, decoded_exact_units=1, decoded_exact_unit_ids=['first'])
        with patch('lib.decoded_mainl_acceptance.verify', return_value=result) as verify:
            self.assertEqual(status.mainl_product_status(self.root, self.rows), result)
        verify.assert_called_once()

    def test_partial_duplicate_or_changed_inventory_cannot_inherit_acceptance(self):
        variants = [self.rows[:1], self.rows + self.rows[:1],
                    [dict(self.rows[0], id='wrong'), self.rows[1]],
                    [dict(self.rows[0], source='wrong'), self.rows[1]]]
        for rows in variants:
            with self.subTest(rows=rows), patch('lib.decoded_mainl_acceptance.verify') as verify, \
                    patch('lib.decoded_mainl_acceptance.audit') as audit:
                result = status.mainl_product_status(self.root, rows)
            self.assertFalse(result['product_exact'])
            self.assertEqual(result['decoded_exact_units'], 0)
            verify.assert_not_called()
            audit.assert_not_called()

    def test_excluded_or_unrelated_rows_do_not_change_the_active_inventory(self):
        rows = self.rows + [dict(id='old', artifact='th03-mainl', state='excluded'),
                            dict(id='other', artifact='th03-op', state='exact')]
        with patch('lib.decoded_mainl_acceptance.verify', return_value={'decoded_exact_units': 1}):
            self.assertEqual(status.mainl_product_status(self.root, rows)['decoded_exact_units'], 1)

    def test_verifier_failure_reports_publication_and_native_blockers(self):
        with patch('lib.decoded_mainl_acceptance.verify', side_effect=ValueError('verifier input drift')), \
                patch('lib.decoded_mainl_acceptance.audit', side_effect=ValueError('staff source binding drift')):
            result = status.mainl_product_status(self.root, self.rows)
        self.assertFalse(result['product_exact'])
        self.assertEqual(result['decoded_exact_unit_ids'], [])
        self.assertIn('verifier input drift', result['reason'])
        self.assertIn('staff source binding drift', result['reason'])

    def test_missing_current_publication_never_selects_a_historical_proposal(self):
        (self.root / status.MAINL_SCOPED_PUBLICATION).unlink()
        with patch('lib.mainl_product_acceptance.load_status') as historical:
            result = status.mainl_product_status(self.root, self.rows)
        historical.assert_not_called()
        self.assertFalse(result['product_exact'])
        self.assertEqual(result['decoded_exact_units'], 0)
        self.assertIn('publication missing', result['reason'])


if __name__ == '__main__':
    unittest.main()
