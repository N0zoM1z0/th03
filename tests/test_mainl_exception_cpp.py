"""Natural C++ replay stays explicitly unaccepted while complete native bytes differ."""
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_exception_cpp import review,REPORT


@unittest.skipUnless((ROOT/REPORT).is_file(),'private C++ replay absent')
class ExceptionCppCandidate(unittest.TestCase):
    def test_real_candidates_repeat_without_gaining_exact_credit(self):
        p=review(ROOT)
        self.assertEqual((p['accepted_source_bytes'],p['source_acceptance']),(0,False))
        self.assertFalse(p['whole_EXE_equal']);self.assertFalse(p['whole_MAP_equal'])
        self.assertEqual((p['normal_library_members'],p['untouched_current_library_members'],p['source_providers_in_candidate_library']),(893,871,28))
        self.assertEqual(sum(len(m['original_literal_native_fields']) for m in p['modules'].values()),122)
        self.assertEqual(sum(m['original_CODE_bytes'] for m in p['modules'].values()),1563)
        self.assertEqual(sum(m['original_inline_CS_DATA_bytes'] for m in p['modules'].values()),659)
        self.assertTrue(all(not m['complete_initialized_payload_equal'] for m in p['modules'].values()))
        self.assertEqual(p['modules']['xalloc']['original_literal_ordered_MZ'][:2],[[0,0x543A],[0,0x53BB]])
        self.assertEqual(p['modules']['xalloc']['candidate_publics'][1][0],123)
        self.assertEqual(p['modules']['xalloc']['original_publics'][1][0],127)

    def test_stale_source_binding_is_rejected(self):
        r=json.loads((ROOT/REPORT).read_bytes());r['source_sha256']['src/mainl/crt/xalloc.cpp']='0'*64
        with self.assertRaisesRegex(ValueError,r'maintained C\+\+ source'):review(ROOT,r)

    def test_reproducibility_does_not_authorize_source_acceptance(self):
        r=json.loads((ROOT/REPORT).read_bytes());r.update(source_acceptance=True,accepted_source_bytes=2258)
        with self.assertRaisesRegex(ValueError,'unaccepted bounded candidate'):review(ROOT,r)

    def test_a_false_whole_EXE_equality_claim_is_rejected(self):
        r=json.loads((ROOT/REPORT).read_bytes());r['whole_EXE_equal']=True
        with self.assertRaisesRegex(ValueError,'whole EXE/MAP comparison is honest'):review(ROOT,r)


if __name__=='__main__':unittest.main()
