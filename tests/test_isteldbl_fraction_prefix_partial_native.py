"""Original isteldbl sign, integer and fractional digit parsing prefix."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_isteldbl_fraction_prefix_partial import SOURCE,verify
class OriginalLongDoubleFractionPrefix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_genuine_754_byte_parser_range(self):
        r=self.r
        self.assertEqual((r['original_member_CODE_bytes'],
                          r['original_prefix_CODE_bytes'],
                          r['original_equal_prefix_CODE_bytes']),(1947,754,752))
        self.assertEqual(r['original_unresolved_jump_operand_sites'],[30,31])
        self.assertEqual(r['original_unresolved_jump_destination'],0x78f)
        s=SOURCE.read_bytes()
        for term in (b'call @istream@ipfx$qi',
                     b'call dword ptr [bx+0ch]',
                     b'call @streambuf@do_snextc$qv',
                     b'call @ios@setstate$qi',
                     b'test byte ptr DGROUP:__ctype[bx+1],2',
                     b'fldz',b'fstp tbyte ptr es:[bx]',
                     b'fmul dword ptr DGROUP:digit_ten',
                     b'fild word ptr [bp-2]',b'faddp st(1),st(0)',
                     b'fractional_start label near',
                     b'fraction_digit_loop:',
                     b'sub word ptr [bp-14h],1',
                     b'sbb word ptr [bp-12h],0',
                     b'exponent_start label near'):
            self.assertIn(term,s)
    def test_all_27_original_symbolic_references_with_bounded_exception(self):
        r=self.r
        self.assertEqual(r['original_prefix_fixups'],27)
        self.assertEqual(r['native_total_fixups_including_unresolved_jump'],28)
        self.assertEqual(r['original_x87_frame4_vs_tasm_frame5_count'],15)
        self.assertEqual(len(set(r['original_x87_frame4_sites'])),15)
        self.assertEqual(r['original_initialized_DATA_prefix_bytes_equal'],4)
    def test_two_native_rounds_without_unearned_member_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertFalse(r['complete_native_MAINL_link'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
