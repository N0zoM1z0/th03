"""Eight source-bound original 8086 DOS/pointer/IBM/arith CRT member bodies."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after328_work import MODES, NATIVE, PREFIX, WORK, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from review_th03_mainl_after328_work import review

SCOPE = {
    'n_pcmp': (33, [(0, 'N_PCMP@')], []),
    'f_pcmp': (33, [(0, 'F_PCMP@'), (0, 'PCMP@')], []),
    'dosclose': (26, [(0, '__dos_close')], ['__DOSERROR']),
    'doscmmit': (26, [(0, '__dos_commit')], ['__DOSERROR']),
    'cibmtxmd': (36, [(0, '___ibm_textmode')], ['__video', '___ibm_crtinit']),
    'cibmgtxy': (24, [(0, '__IBM_GOTOXY')], ['__IBM_VIDEOINT']),
    'f_lxmul': (23, [(0, 'F_LXMUL@'), (0, 'LXMUL@')], []),
    'textknj': (15, [(0, '_textkanji')], ['__wkanji']),
}
LITERAL_GAPS = {'dosclose', 'doscmmit', 'cibmtxmd', 'cibmgtxy'}


class OriginalEightLeaves(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'dos-pointer-ibm-leaves-build.json')).is_file(),
                         'local 340-source native receipts absent')
    def test_all_eight_complete_code_and_native_link(self):
        r = review('dos-pointer-ibm-leaves')
        self.assertEqual(set(MODES['dos-pointer-ibm-leaves']), set(SCOPE))
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 340, 553))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (216, 111057))
        for name, (size, publics, imports) in SCOPE.items():
            with self.subTest(member=name):
                p = r['profiles'][name]
                self.assertEqual((p['CODE_bytes'], p['DATA_bytes'],
                                  p['BSS_bytes']), (size, 0, 0))
                self.assertEqual(p['publics'], publics)
                self.assertEqual(p['imports'], imports)
                self.assertEqual(len(p['relocation_sites_targets']),
                                 NATIVE[name]['fields'])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']),
                         (2, 677))

    @unittest.skipUnless((ROOT / (PREFIX + 'dos-pointer-ibm-leaves-build.json')).is_file(),
                         'raw source-bound OBJ/LIB/EXE/MAP pairs absent')
    def test_both_original_obj_rounds_and_real_borland_frame_discrepancies(self):
        _, _, _, members, _, _ = retained()
        receipt = json.loads((ROOT / (PREFIX + 'dos-pointer-ibm-leaves-build.json')).read_text())
        for name in SCOPE:
            original = original_library_member(members[NATIVE[name]['index']])
            original_fields = literal_fields(original)
            for row in receipt['rounds']:
                with self.subTest(member=name, round=row['round']):
                    made = (ROOT / row['outputs'][name]['path']).read_bytes()
                    made_fields = literal_fields(made)
                    self.assertEqual(payload(made), payload(original))
                    keys = ('segment', 'site', 'location_type', 'width',
                            'segment_relative', 'target_method', 'target', 'addend')
                    shape = lambda fields: sorted(tuple(f[k] for k in keys) for f in fields)
                    self.assertEqual(shape(made_fields), shape(original_fields))
                    self.assertEqual(row['literal_omf_fixupp_equal_by_member'][name],
                                     name not in LITERAL_GAPS)
                    self.assertEqual(made_fields == original_fields,
                                     name not in LITERAL_GAPS)
                    self.assertFalse(row['original_program_equal_by_member'][name])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[name]['index']].program_records)
                    group = [x.data.hex() for x in parse_omf(made) if x.name == 'GRPDEF']
                    self.assertEqual(group, [NATIVE[name]['group']])
        # The original near calls are target-framed; TASM uses CODE frame.
        original = original_library_member(members[NATIVE['dosclose']['index']])
        self.assertEqual(literal_fields(original)[0]['frame_method'], 5)
        made = (ROOT / receipt['rounds'][0]['outputs']['dosclose']['path']).read_bytes()
        self.assertEqual(literal_fields(made)[0]['frame_method'], 0)
        # Explicit DGROUP frame for the original IBM mode/global data.
        original = original_library_member(members[NATIVE['cibmtxmd']['index']])
        made = (ROOT / receipt['rounds'][0]['outputs']['cibmtxmd']['path']).read_bytes()
        before = {f['site']: f for f in literal_fields(original)}
        after = {f['site']: f for f in literal_fields(made)}
        for site in (12, 30):
            self.assertEqual(before[site], after[site])


if __name__ == '__main__':
    unittest.main()
