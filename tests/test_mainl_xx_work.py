"""Real normal-library xx replacement and full native MAINL link."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_xx_work import review
from build_th03_mainl_xx_work import REPORT


@unittest.skipUnless((ROOT/REPORT).is_file(),'private whole MAINL xx pair absent')
class XxWholeProduct(unittest.TestCase):
    def test_native_library_integration_and_real_helper_linkage(self):
        r=review(ROOT)
        self.assertTrue(r['whole_product_linked'])
        self.assertEqual((r['normal_library_members'],r['unchanged_surrounding_members']),(893,892))
        self.assertEqual((r['source_CRT_providers'],r['reused_source_CRT_providers']),(29,28))
        self.assertEqual((r['retained_project_objects'],r['retained_binary_inputs']),(36,39))
        self.assertEqual((r['original_file_bytes'],r['candidate_file_bytes']),(67372,67324))
        self.assertEqual((r['original_relocation_count'],r['candidate_relocation_count']),(677,677))
        self.assertEqual(len(r['candidate_ordered_xx_MZ_words']),20)
        self.assertEqual(len(r['actual22_public_bindings']),22)
        self.assertTrue(r['all_source_CODE_bytes_resolved'])
        self.assertTrue(r['all18_interfaces_resolved_to_real_library'])
        dispatcher=next(q for q in r['raw_function_comparisons'] if q['name']=='dispatchException')
        self.assertEqual(dispatcher['candidate_bytes'],140)
        self.assertTrue(dispatcher['raw_equal'])
        cleanup=next(q for q in r['raw_function_comparisons'] if q['name']=='dtorCleanup')
        self.assertEqual(cleanup['candidate_bytes'],1035)
        self.assertFalse(cleanup['raw_equal'])
        compatibility=next(q for q in r['raw_function_comparisons'] if q['name']=='compatibleType')
        self.assertEqual(compatibility['candidate_bytes'],372)
        self.assertFalse(compatibility['raw_equal'])
        for a,b in r['target_and_source_RTTI_probes']:
            self.assertEqual(a,b)
        a,b=r['target_and_source_real_memcpy_raise_probe']
        self.assertEqual(a['restored_registers'],b['restored_registers'])
        self.assertEqual((a['actual_memcpy_calls'],b['actual_memcpy_calls']),(2,2))
        self.assertEqual(a,b)
        self.assertEqual((a['context'][13],b['context'][13]),(132,132))
        a,b=r['alternate_stack_real_memcpy_raise_probe']
        self.assertEqual((a['context'][13],b['context'][13]),(128,132))
        self.assertEqual(r['raw_Raise_argument_copy_bytes'],71)
        self.assertFalse(r['whole_EXE_raw_equal'])
        self.assertFalse(r['whole_MAP_raw_equal'])
        self.assertEqual((r['source_acceptance'],r['accepted_source_bytes'],r['original_cold_rebuilt']),(False,0,False))


if __name__=='__main__':unittest.main()
