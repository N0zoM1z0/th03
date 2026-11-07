"""Guard against mistaking exact input_s OBJ for an exact full MAIN link."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from review_th03_input_s_link_gap_after744 import review


@unittest.skipUnless(
    (ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03WORK/probe/af744d/r1.exe').exists(),
    'private retained original compiler and MAIN evidence unavailable',
)
class InputScannerNativeLinkGap(unittest.TestCase):
    def test_actual_original_source_object_but_no_full_MAIN_exactness(self):
        result = review()
        self.assertTrue(result['native_current_source_object_CODE_exact'])
        self.assertEqual(result['input_s_original_CODE_bytes'], 417)
        self.assertEqual(result['parent_link_object_CODE_bytes'], 418)
        self.assertEqual(result['native_ordered_FIXUPPs'], 42)
        self.assertEqual(result['native_original_PUBLICs'], 1)
        self.assertEqual(result['historical_extra_byte'], '90')
        self.assertFalse(result['normal_MAIN_exact'])
        self.assertFalse(result['canonical_Factory_credit'])


if __name__ == '__main__':
    unittest.main()
