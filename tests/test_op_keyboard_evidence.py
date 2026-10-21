"""Decoded scanner evidence must not invent canonical packed-file offsets."""
import csv
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ScannerEvidenceTests(unittest.TestCase):
    def test_decoded_scope_does_not_claim_packed_extent(self):
        with (ROOT / 'config/evidence.csv').open() as stream:
            rows = list(csv.DictReader(stream))
        ids = {'ev-th03-op-keyboard-source-proof', 'ev-th03-op-keyboard-native-structure', 'ev-th03-op-keyboard-modeled-runtime'}
        selected = [row for row in rows if row['id'] in ids]
        self.assertEqual(len(selected), 3)
        self.assertEqual({row['id'] for row in selected}, ids)
        for row in selected:
            self.assertEqual((row['extent_start'], row['extent_size']), ('', ''))
            self.assertEqual((row['artifact'], row['unit_id']), ('th03-op', 'th03-op-decoded-input-sense'))
            self.assertEqual(row['input_sha256'], 'd7bfa7f1f8afe0943763ce76437d12ed412b8452716dd64f937c94796eba57ab')
            self.assertIn('Decoded scope 0BEB:0304, 417 bytes', row['notes'])
        runtime = next(row for row in selected if row['id'].endswith('modeled-runtime'))
        self.assertEqual(runtime['observed_utc'], '2026-10-21T23:22:49.150854+00:00')
        with (ROOT / 'config/units.csv').open() as stream:
            units = [row for row in csv.DictReader(stream) if row['id'] == 'th03-op-decoded-input-sense']
        self.assertEqual(len(units), 1)
        unit = units[0]
        self.assertEqual(tuple(unit[key] for key in ('segment', 'offset', 'size', 'compare_size', 'file_offset', 'state')), ('decoded:0BEB', '0x304', '417', '417', '', 'source-present'))
