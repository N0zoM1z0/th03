"""Whole DOS xx carrier,compiler storage and concrete RTTI address questions."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_xx_rtti import review,REPORT


@unittest.skipUnless((ROOT/REPORT).is_file(),'private full xx pair absent')
class XxRtti(unittest.TestCase):
    def test_native_whole_carrier_and_rtti(self):
        r=review(ROOT)
        self.assertEqual((r['original_CODE_bytes'],r['original_instruction_bytes'],r['original_inline_data_bytes']),(12622,12088,534))
        self.assertEqual((len(r['original_bodies']),len(r['original_literal_native_fields']),len(r['original_MZ_words'])),(50,187,20))
        self.assertTrue(r['all22_original_public_interfaces'])
        self.assertEqual(len(r['original18_imports']),18)
        self.assertTrue(r['whole_xx_source_graph_present'])
        self.assertTrue(r['complete_DATA_raw_equal'])
        self.assertEqual((r['candidate_DATA_bytes'],r['candidate_BSS_bytes']),(18,10))
        self.assertEqual(r['original_RTTI_metadata_bytes'],136)
        self.assertTrue(r['all_RTTI_metadata_bytes_owned'])
        self.assertEqual(sum(q['size'] for q in r['candidate_LIDATA_records']),r['candidate_RTTI_metadata_bytes']-135)
        self.assertEqual(r['RaiseException_stack_allocations'],[390,342])
        self.assertTrue(r['before_object_body_raw_equal'])
        self.assertEqual([len(q) for q in r['original_and_candidate_before_fields']],[1,1])
        results={}
        for a,b in r['target_and_source_RTTI_probes']:
            self.assertEqual(a,b);results[a['case']]=a
        self.assertEqual((results['virtual-shared-address']['dx'],results['virtual-shared-address']['ax']),(0x6500,0x500))
        self.assertEqual(results['distinct-base-ambiguity']['ax'],0)
        self.assertEqual(results['downcast-source-address']['ax'],0x120)
        self.assertEqual(results['jump-to-catch-registers']['sp'],0xE000)
        self.assertFalse(r['complete_CODE_raw_equal'])
        self.assertEqual((r['source_acceptance'],r['accepted_source_bytes'],r['whole_product_linked']),(False,0,False))


if __name__=='__main__':unittest.main()
