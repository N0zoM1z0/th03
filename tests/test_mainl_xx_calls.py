"""Native register/stack evidence for the original DOS member-call adapters."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_xx_calls import review,REPORT


@unittest.skipUnless((ROOT/REPORT).is_file(),'private xx call-adapter pair absent')
class XxCalls(unittest.TestCase):
    def test_native_call_bank_and_three_concrete_ABIs(self):
        r=review(ROOT)
        self.assertEqual((r['original_bank_size'],r['original_instruction_bytes'],r['original_inline_table_bytes']),(1495,1327,168))
        self.assertEqual(len(r['original_bodies']),3)
        self.assertEqual(len(r['original_literal_native_fields']),88)
        self.assertTrue(r['same_TU_destructor_and_member_edges_resolved'])
        self.assertEqual(len(r['unresolved_interfaces']),15)
        for a,b in r['target_and_source_callback_probes']:
            self.assertEqual(a,b)
            self.assertEqual((a['sp'],a['ds'],a['actual_callback_calls']),(0xFF02,0xE3F,1))
        self.assertEqual(r['target_and_source_callback_probes'][0][0]['callback_words'],[0,0x3456,0x4567,0x6400,1])
        self.assertFalse(r['complete_call_bank_raw_equal'])
        self.assertEqual((r['source_acceptance'],r['accepted_source_bytes'],r['whole_product_linked']),(False,0,False))


if __name__=='__main__':unittest.main()
