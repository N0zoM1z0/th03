"""Original long-double parser's significant natural integer-prefix source."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_isteldbl_integer_prefix_partial import SOURCE,verify
class OriginalLongDoubleIntegerPrefix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_true_initial_decimal_parsing_and_buffer_refill(self):
        r=self.r
        self.assertEqual((r['original_member_CODE_bytes'],
                          r['original_prefix_CODE_bytes'],
                          r['original_equal_prefix_CODE_bytes']),(1947,460,458))
        self.assertEqual(r['original_unresolved_jump_operand_sites'],[30,31])
        self.assertEqual(r['original_unresolved_jump_destination'],0x78f)
        s=SOURCE.read_bytes()
        for op in (b'call @istream@ipfx$qi',
                   b'call dword ptr [bx+0ch]',
                   b'call @streambuf@do_snextc$qv',
                   b'call @ios@setstate$qi',
                   b'test byte ptr DGROUP:__ctype[bx+1],2',
                   b'fldz',b'fstp tbyte ptr es:[bx]',
                   b'fmul dword ptr DGROUP:digit_ten',
                   b'fild word ptr [bp-2]',b'faddp st(1),st(0)',
                   b'digit_loop:',b'fractional_start label near'):
            self.assertIn(op,s)
    def test_all_original_prefix_relocations_except_unresolved_exit(self):
        r=self.r
        self.assertEqual(r['original_prefix_fixups'],16)
        self.assertEqual(r['native_total_fixups_including_unresolved_jump'],17)
        self.assertEqual(r['original_x87_frame4_vs_tasm_frame5_count'],9)
        self.assertEqual(len(set(r['original_x87_frame4_sites'])),9)
        self.assertEqual(r['original_initialized_DATA_prefix_bytes_equal'],4)
        self.assertTrue(r['original_publics_equal'])
    def test_two_native_tasm_rounds_and_no_unearned_full_boss_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertFalse(r['complete_native_MAINL_link'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
