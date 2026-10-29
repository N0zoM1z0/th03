"""The recovered bank has real native ABI evidence while remaining unaccepted."""
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_xx_dispatch import review,REPORT


@unittest.skipUnless((ROOT/REPORT).is_file(),'private dispatch source pair absent')
class XxDispatch(unittest.TestCase):
    def test_actual_native_bank_and_negative_filter_preserve_SS_frame(self):
        p=review(ROOT)
        self.assertEqual((p['source_acceptance'],p['accepted_source_bytes']),(False,0))
        self.assertEqual((p['original_bank_size'],p['original_instruction_bytes'],p['original_inline_DATA_bytes']),(1565,1533,32))
        self.assertEqual(p['candidate_CODE_segment_bytes'],1566)
        self.assertEqual(len(p['original_bodies']),5)
        self.assertFalse(p['complete_bank_raw_equal']);self.assertFalse(p['whole_product_linked'])
        self.assertEqual(len(p['unresolved_private_and_runtime_interfaces']),7)
        a,b=p['negative_constant_filter_target_and_source']
        self.assertEqual(a,b)
        self.assertEqual((a['return_value'],a['context'],a['sp'],a['exception_info']),(0,6,0xFF04,0x550))
        self.assertEqual((a['runtime_saved_ds'],a['runtime_saved_si']),(0x1357,0x2468))

    def test_miniature_repeatability_cannot_authorize_source_acceptance(self):
        r=json.loads((ROOT/REPORT).read_bytes());r.update(source_acceptance=True,accepted_source_bytes=1565)
        with self.assertRaisesRegex(ValueError,'unaccepted isolated dispatch bank'):review(ROOT,r)


if __name__=='__main__':unittest.main()
