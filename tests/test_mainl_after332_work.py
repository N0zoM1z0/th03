"""Original Japanese Borland farheap: complete allocator state and literal OMF."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after332_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from review_th03_mainl_after332_work import review

EXPECTED_PUBLICS = [
    (0,'___first'), (2,'___last'), (4,'___rover'),
    (320,'_farfree'), (320,'_free'),
    (627,'_malloc'), (637,'_farmalloc'),
    (986,'_realloc'), (993,'_farrealloc'),
]


class OriginalBorlandFarheap(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'farheap-manager-build.json')).is_file(),
                         'native 344-source original Japanese carrier absent')
    def test_entire_original_allocator_and_exact_japanese_exe(self):
        r = review('farheap-manager')
        p = r['profiles']['farheap']
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 344, 549))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (1115, 114620))
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (1115,0,0))
        self.assertEqual(p['CODE_implicit_sites'], [6,7,8,9,10,11])
        self.assertEqual(p['DATA_implicit_sites'], [])
        self.assertEqual(p['publics'], EXPECTED_PUBLICS)
        self.assertEqual(p['imports'], ['__brk','__sbrk'])
        self.assertEqual(len(p['relocation_sites_targets']), 49)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertTrue(r['original_library_member_program_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),
                         (2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT / (PREFIX + 'farheap-manager-build.json')).is_file(),
                         'both native original/compiled OMF pairs absent')
    def test_literal_original_full_omf_including_implicit_uninitialized_code(self):
        _, _, _, members, _, _ = retained()
        m = members[NATIVE['farheap']['index']]
        self.assertEqual(m.name, 'farheap')
        orig = original_library_member(m)
        original_program = m.program_records
        fields = literal_fields(orig)
        self.assertEqual(len(fields), 49)
        self.assertEqual([r.data.hex() for r in parse_omf(orig)
                          if r.name=='GRPDEF'], ['06ff02'])
        original_payload = payload(orig)
        self.assertEqual([i for i in range(1115) if (1,i) not in original_payload],
                         [6,7,8,9,10,11])
        self.assertEqual([original_payload[1,i] for i in range(6)], [0]*6)
        receipt = json.loads((ROOT / (PREFIX+'farheap-manager-build.json')).read_text())
        for row in receipt['rounds']:
            with self.subTest(native_round=row['round']):
                made = (ROOT / row['outputs']['farheap']['path']).read_bytes()
                self.assertEqual(payload(made),original_payload)
                self.assertEqual(literal_fields(made),fields)
                self.assertEqual(object_program_records(made),original_program)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['farheap'])
                self.assertTrue(row['original_program_equal_by_member']['farheap'])
                exe = (ROOT / row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__ == '__main__':
    unittest.main()
