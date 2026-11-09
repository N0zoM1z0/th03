"""Current native scopes remain independent of the broad decoded publication."""
import csv
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import progress
import status


class NativeProgress(unittest.TestCase):
    def test_missing_private_evidence_is_visible_and_does_not_run_a_reviewer(self):
        with TemporaryDirectory() as folder, patch.object(status.subprocess, 'run') as run:
            rows = status.native_source_reviews(Path(folder), 'th03-mainl')
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(not row['verified'] and 'unavailable' in row['reason'] for row in rows))
        run.assert_not_called()

    def test_main_native_selection_excludes_superseded_composite(self):
        expected = ['af1172f', 'af1173c', 'af1181b', 'af1182a',
                    'af1184d', 'af1174e', 'af1176e',
                    'af1178a', 'af1179a', 'af1180b', 'af1129e', 'af1127g', 'af1128c',
                    'af1112h', 'af1113c', 'af1121d', 'af1122c',
                    'af1124d', 'af1125e', 'af1188c', 'af1189d',
                    'af1190d', 'af1158e', 'af1175f', 'af1168b',
                    'af1183f', 'af1187e', 'af1185e', 'af1107c',
                    'af1177g', 'af1192d', 'af1120c', 'af1194c',
                    'af1115b', 'af1171d', 'af1164e', 'af1166i',
                    'af1165h', 'af1191e', 'af1163i', 'af1169a',
                    'af1134f',
                    'af1135h', 'af1136f', 'af1138f', 'af1140e',
                    'af1141f', 'af1142d', 'af1143h', 'af1146d', 'af1147c',
                    'af1148f', 'af1149e', 'af1152f', 'af1153d', 'af1154d',
                    'af1155b', 'af1156b', 'af1159d',
                    'af1131a', 'af1132b', 'af1133a', 'af1160e',
                    'af1161f', 'af1170d']
        with TemporaryDirectory() as folder, patch.object(status.subprocess, 'run') as run:
            rows = status.native_source_reviews(Path(folder), 'th03-main')
        self.assertEqual([row['stage'] for row in rows], expected)
        self.assertTrue(all(not row['verified'] and 'unavailable' in row['reason']
                            for row in rows))
        run.assert_not_called()

    def test_main_source_review_requires_complete_two_round_link(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            for stage in ('af1194c', 'af1170d', 'af1175f', 'af1168b',
                          'af1106d', 'af1107c', 'af1177g', 'af1172f', 'af1173c', 'af1181b', 'af1182a', 'af1184d',
                          'af1174e', 'af1176e', 'af1178a', 'af1179a',
                          'af1180b',
                          'af1183f', 'af1187e', 'af1112h', 'af1113c',
                          'af1192d', 'af1115b', 'af1191e', 'af1189d',
                          'af1188c', 'af1190d', 'af1120c', 'af1121d',
                          'af1122c', 'af1158e', 'af1124d', 'af1125e',
                          'af1171d', 'af1127g', 'af1128c', 'af1129e',
                          'af1185e', 'af1131a', 'af1132b', 'af1133a',
                          'af1134f', 'af1135h', 'af1136f', 'af1138f',
                          'af1140e', 'af1141f', 'af1142d', 'af1143h', 'af1183f',
                          'af1187e', 'af1146d', 'af1147c', 'af1148f',
                          'af1149e', 'af1152f', 'af1153d', 'af1154d',
                          'af1155b', 'af1156b', 'af1159d', 'af1160e',
                          'af1161f', 'af1185e', 'af1163i', 'af1164e',
                          'af1165h', 'af1166i', 'af1192d', 'af1168b',
                          'af1169a', 'af1170d', 'af1171d', 'af1172f', 'af1173c', 'af1181b', 'af1182a', 'af1184d',
                          'af1174e', 'af1175f', 'af1176e', 'af1177g',
                          'af1178a', 'af1179a', 'af1180b'):
                path = root / f'.analysis/work/exatt-layout-{stage}/report.json'
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('{}')
            for value in (dict(full_Japanese_MAIN_equal=True, native_rounds=2,
                               complete_original_units=1,
                               original_scope=dict(CODE_bytes=32, PUBLICs=1,
                                                   ordered_native_fields=4)),
                          dict(full_Japanese_MAIN_equal=False, native_rounds=2)):
                result = SimpleNamespace(returncode=0, stderr='', stdout=json.dumps(value))
                with self.subTest(link_ok=value['full_Japanese_MAIN_equal']), \
                     patch.object(status.subprocess, 'run', return_value=result):
                    rows = status.native_source_reviews(root, 'th03-main')
                fresh = [row for row in rows if row['stage'].startswith(('af110', 'af111', 'af112', 'af113', 'af114', 'af115', 'af116', 'af117', 'af118', 'af119'))]
                self.assertEqual(len(fresh), 65)
                self.assertTrue(all(row['verified'] == value['full_Japanese_MAIN_equal']
                                    for row in fresh))

    def test_failed_or_incomplete_review_cannot_earn_native_credit(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            for path in ('.analysis/work/mainl-staff-af942s-native-build.json',
                         '.analysis/work/mainl-root-af944r-native-build.json'):
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('{}')
            for result in (SimpleNamespace(returncode=1, stderr='source binding drift', stdout=''),
                           SimpleNamespace(returncode=0, stderr='', stdout='{}')):
                with self.subTest(result=result), patch.object(status.subprocess, 'run', return_value=result):
                    rows = status.native_source_reviews(root, 'th03-mainl')
                self.assertTrue(all(not row['verified'] for row in rows))

    def test_pending_publication_does_not_erase_scoped_native_work(self):
        units = list(csv.DictReader((status.ROOT / 'config/units.csv').read_text().splitlines()))
        functions = list(csv.DictReader((status.ROOT / 'config/th03_main_authored_functions.csv').read_text().splitlines()))
        pending = dict(product_exact=False, decoded_exact_units=0, reason='source graph drift')
        scopes = [dict(artifact='th03-mainl', scope='Staff Roll', stage='af942s', verified=True,
                       modules=1, code_bytes=3695, initialized_data_bytes=224, procedures=19,
                       report='.analysis/work/mainl-staff-af942s-native-build.json')]
        svg = progress.render_svg(units, functions, [], op_status={'decoded_accepted': False},
                                  op_products={'retained_equality': False}, zun_status={'decoded_accepted': False},
                                  mainl_status=pending, native_reviews=scopes)
        ET.fromstring(svg)
        self.assertIn('Decoded acceptance: pending', svg)
        self.assertNotIn('Unit acceptance: exact 0/259', svg)
        self.assertIn('Staff Roll (af942s): 1 physical owners / 3,695 CODE B', svg)
        self.assertIn('106 tracked unit extents', svg)
        self.assertNotIn('459 tracked functions', svg)
        self.assertEqual(pending['decoded_exact_units'], 0)

    def test_publication_inventory_validation_has_no_frozen_count(self):
        rows = [dict(id='one', artifact='th03-zun', state='source-present')]
        with TemporaryDirectory() as folder:
            root = Path(folder)
            publication = root / status.ZUN_SCOPED_PUBLICATION
            publication.parent.mkdir(parents=True)
            publication.write_text('{}')
            with (root / 'config/units.csv').open('w', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=['id', 'artifact', 'state'])
                writer.writeheader()
                writer.writerows(rows)
            with patch('lib.decoded_zun_acceptance.verify', return_value={'decoded_accepted': True}) as verify:
                self.assertTrue(status.zun_product_status(root, rows)['decoded_accepted'])
                verify.assert_called_once()
                verify.reset_mock()
                self.assertFalse(status.zun_product_status(root, rows + rows)['decoded_accepted'])
                verify.assert_not_called()


if __name__ == '__main__':
    unittest.main()
