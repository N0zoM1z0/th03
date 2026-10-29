"""Native DOS catch-copy/free and far virtual-base/type-comparison evidence."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_xx_catch import review,REPORT


@unittest.skipUnless((ROOT/REPORT).is_file(),'private integrated catch/type pair absent')
class XxCatch(unittest.TestCase):
    def test_actual_catch_bank_and_connected_copy_path(self):
        r=review(ROOT)
        self.assertEqual((r['original_bank_size'],r['original_instruction_bytes'],r['original_inline_EH_bytes']),(1476,1434,42))
        self.assertEqual(r['original_comparator']['size'],157)
        self.assertEqual((len(r['original_literal_native_fields']),len(r['original_MZ_sites'])),(13,3))
        self.assertEqual(len(r['original_bodies']),6)
        self.assertTrue(r['same_TU_catch_copy_edges_resolved'])
        self.assertEqual(len(r['unresolved_interfaces']),14)
        for a,b in r['target_and_source_catch_probes']:self.assertEqual(a,b)
        copied=r['target_and_source_catch_probes'][0][0]
        self.assertEqual((copied['argument_address'],copied['buffer_and_copy'],copied['actual_callback_calls']),(0x3FF0,[1,1],1))
        self.assertEqual(r['target_and_source_catch_probes'][2][0]['address'],[0x220,0x6500])
        self.assertFalse(r['complete_catch_bank_raw_equal'])
        self.assertEqual((r['source_acceptance'],r['accepted_source_bytes'],r['whole_product_linked']),(False,0,False))


if __name__=='__main__':unittest.main()
