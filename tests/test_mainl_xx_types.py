"""Real DOS type rules,private dispatch linkage and emergency-slot ownership."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_xx_types import review,REPORT


@unittest.skipUnless((ROOT/REPORT).is_file(),'private integrated types pair absent')
class XxTypes(unittest.TestCase):
    def test_native_type_bank_and_original_rules(self):
        r=review(ROOT)
        self.assertEqual((r['original_bank_size'],r['original_instruction_bytes'],r['original_inline_data_bytes']),(1121,1121,0))
        self.assertEqual((len(r['original_bodies']),len(r['original_literal_native_fields']),r['original_MZ_words']),(5,3,0))
        self.assertTrue(r['same_TU_type_match_edge_resolved'])
        self.assertEqual(len(r['actual_dispatch_type_calls']),2)
        codegen=r['compatibility_codegen']
        self.assertEqual((codegen['candidate_bytes'],codegen['stack_bytes']),(372,4))
        self.assertTrue(codegen['all368_bytes_outside_call_operands_equal'])
        self.assertEqual([q['offset'] for q in codegen['raw_byte_differences']],[298,357])
        self.assertEqual([q['target'] for q in codegen['local_calls']],['sameTypeID','findBaseType'])
        self.assertEqual(codegen['original_and_candidate_literal_fields'],[[],[]])
        self.assertFalse(codegen['complete_object_raw_equal'])
        results={}
        for a,b in r['target_and_source_type_probes']:
            self.assertEqual(a,b);results[a['case']]=a
        self.assertEqual([results[k]['matched'] for k in ('public-reference-base','private-reference-base','near-far-unrelated','void-equal-cv','void-added-cv')],[1,0,1,1,0])
        self.assertEqual(results['near-far-unrelated']['actual_name_comparisons'],0)
        self.assertEqual(results['emergency-free']['runtime_flags'],0xA500)
        self.assertFalse(r['complete_bank_raw_equal'])
        self.assertEqual((r['source_acceptance'],r['accepted_source_bytes'],r['whole_product_linked']),(False,0,False))


if __name__=='__main__':unittest.main()
