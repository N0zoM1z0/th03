"""Original core for 12 signed/unsigned long DIV/MOD public ABI aliases."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_h_ldiv_scoped import SOURCE,verify,PUBLICS

class OriginalLongDivisionCore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_all_twelve_public_aliases_original_174_code_bytes(self):
        r=self.r
        self.assertEqual(r['original_MEMBER_CODE_bytes'],174)
        self.assertEqual(r['exact_original_CODE_bytes'],174)
        self.assertEqual(r['original_publics'],PUBLICS)
        self.assertEqual(len(r['original_publics']),12)
        self.assertEqual(r['original_OMF_FIXUPP_count'],0)
        self.assertTrue(r['complete_segment_and_logical_OMF_match'])
        source=SOURCE.read_bytes()
        for ins in (b'pop cx',b'push cs',b'rcl si,1',
                    b'rcl di,1',b'sbb di,bp',b'loop long_division_loop',
                    b'div bx',b'retf 8'):
            self.assertIn(ins,source)
    def test_linked_exe_is_exact_but_two_map_alias_ties_are_not(self):
        r=self.r
        self.assertTrue(r['retained_target_link_diagnostic'])
        self.assertTrue(r['actual_linked_EXE_original_equal'])
        self.assertEqual(r['actual_linked_MZ_relocations'],677)
        self.assertFalse(r['actual_linked_MAP_original_equal'])
        self.assertEqual(r['different_MAP_line_indices'],[1321,1322,1330,1331])
        self.assertEqual(r['alias_tie_groups'],
                         [['LDIV@','F_LDIV@'],['F_LUMOD@','LUMOD@']])
    def test_two_fresh_tasm_rounds_and_fail_closed_full_source_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['nonvolatile_native_OMF_rounds_equal'])
        self.assertFalse(r['complete_original_native_MAP_equal'])
        self.assertFalse(r['complete_original_source_link_acceptance'])
        self.assertEqual(r['source_linked_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
