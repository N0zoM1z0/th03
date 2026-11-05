"""Do not mistake byte-exact 32-bit division CODE for a MAP-exact CRT member."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_th03_mainl_h_ldiv_source import audit


class OriginalLongDivisionScope(unittest.TestCase):
    def test_complete_174_byte_signed_unsigned_divmod_and_honest_map_gap(self):
        r=audit()
        self.assertEqual((r['original_CRT_index'],r['original_CODE_bytes'],
                          r['original_public_aliases'],r['original_FIXUPP_count']),
                         (67,174,12,0))
        self.assertTrue(r['original_source_CODE_equal'])
        self.assertTrue(r['original_publics_equal'])
        self.assertTrue(r['original_segment_group_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_counted'])
        self.assertTrue(r['native_full_MAP_equality_not_claimed'])
        self.assertEqual(r['original_fully_linked_source_members_remain'],408)
        self.assertEqual(r['known_MAP_alias_order_gaps'],
                         [['LDIV@','F_LDIV@'],['F_LUMOD@','LUMOD@']])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])


if __name__=='__main__':unittest.main()
