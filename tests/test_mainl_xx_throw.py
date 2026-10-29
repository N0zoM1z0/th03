"""Actual DOS throw context,wrapper frames and global-unwind ownership."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_xx_throw import review,REPORT


@unittest.skipUnless((ROOT/REPORT).is_file(),'private integrated throw pair absent')
class XxThrow(unittest.TestCase):
    def test_native_throw_bank_and_register_resume(self):
        r=review(ROOT)
        self.assertEqual((r['original_bank_size'],r['original_instruction_bytes'],r['original_inline_data_bytes']),(2524,2446,78))
        self.assertEqual((len(r['original_bodies']),len(r['original_literal_native_fields'])),(8,24))
        self.assertTrue(r['same_TU_global_unwind_edge_resolved'])
        self.assertTrue(r['raw_dispatcher_body_equal'])
        self.assertEqual(len(r['actual_dispatch_global_unwind_calls']),1)
        self.assertEqual(r['original_covered_bytes'],10838)
        a,b=r['target_and_source_throw_probes'][0]
        self.assertEqual(a['restored_registers'],b['restored_registers'])
        self.assertEqual(a['restored_registers'][0],0xDEADBEEF)
        self.assertEqual(a['record_header'][-1],15)
        self.assertEqual(r['saved_eflags_observations'],[132,128])
        self.assertFalse(r['saved_eflags_equal'])
        for a,b in r['target_and_source_throw_probes'][1:]:
            self.assertEqual(a,b)
        self.assertFalse(r['complete_bank_raw_equal'])
        self.assertEqual((r['source_acceptance'],r['accepted_source_bytes'],r['whole_product_linked']),(False,0,False))


if __name__=='__main__':unittest.main()
