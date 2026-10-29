"""Real target/source evidence for the recovered DOS destruction bank."""
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_xx_destruction import review,REPORT


@unittest.skipUnless((ROOT/REPORT).is_file(),'private integrated xx source pair absent')
class XxDestruction(unittest.TestCase):
    def test_original_bank_and_integrated_native_ABI(self):
        r=review(ROOT)
        self.assertEqual((r['original_bank_size'],r['original_instruction_bytes'],r['original_inline_EH_bytes']),(2500,2422,78))
        self.assertEqual(len(r['original_bodies']),6)
        self.assertEqual(len(r['original_literal_native_fields']),19)
        self.assertEqual(len(r['original_MZ_sites']),5)
        self.assertTrue(r['same_TU_cleanup_resolved'])
        for key in ('empty_offset_target_and_source','far_vtable_target_and_source'):
            a,b=r[key];self.assertEqual(a,b)
        self.assertEqual(r['empty_offset_target_and_source'][0]['sp'],0xFF02)
        self.assertEqual(r['far_vtable_target_and_source'][0]['type'],[0x400,0x6000])
        self.assertFalse(r['complete_integrated_bank_raw_equal'])
        self.assertEqual((r['source_acceptance'],r['accepted_source_bytes'],r['whole_product_linked']),(False,0,False))


if __name__=='__main__':unittest.main()
