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
        self.assertEqual((r['original_file_bytes'],r['candidate_file_bytes']),(67372,67372))
        self.assertEqual((r['original_relocation_count'],r['candidate_relocation_count']),(677,677))
        self.assertEqual(len(r['candidate_ordered_xx_MZ_words']),20)
        self.assertEqual(len(r['actual22_public_bindings']),22)
        self.assertTrue(r['native_object_compiler'])
        self.assertEqual(len(r['native_procedures']),50)
        self.assertEqual((r['original_xx_CODE_bytes'],r['candidate_xx_CODE_bytes']),(12622,12622))
        catch=r['catch_storage_codegen']['exceptionHandled']
        self.assertEqual((catch['original_bytes'],catch['candidate_bytes'],catch['stack_bytes']),(216,216,8))
        self.assertTrue(catch['complete_object_raw_equal'])
        self.assertEqual(catch['remaining_instruction_forms'],[])
        self.assertEqual([[f['site']-at for f in fields] for fields,at in
            zip(catch['original_and_candidate_literal_fields'],(5468,
                next(q['start'] for q in r['native_procedures'] if q['source_name']=='exceptionHandled')))],[[95,29],[95,29]])
        self.assertEqual(len(r['candidate_literal_native_fields']),187)
        self.assertEqual(r['original_prefix_raw_bytes'],2822)
        self.assertEqual(r['original_and_candidate_prefix_fields'][0],r['original_and_candidate_prefix_fields'][1])
        self.assertEqual(r['original_call_bank_raw_bytes'],1495)
        self.assertEqual(r['original_and_candidate_call_bank_fields'][0],r['original_and_candidate_call_bank_fields'][1])
        self.assertEqual(len(r['original_and_candidate_call_bank_fields'][0]),88)
        self.assertTrue(r['all_source_CODE_bytes_resolved'])
        self.assertTrue(r['all18_interfaces_resolved_to_real_library'])
        dispatcher=next(q for q in r['raw_function_comparisons'] if q['name']=='dispatchException')
        self.assertEqual(dispatcher['candidate_bytes'],140)
        self.assertTrue(dispatcher['raw_equal'])
        cleanup=next(q for q in r['raw_function_comparisons'] if q['name']=='dtorCleanup')
        self.assertEqual(cleanup['candidate_bytes'],1035)
        self.assertTrue(cleanup['raw_equal'])
        compatibility=next(q for q in r['raw_function_comparisons'] if q['name']=='compatibleType')
        self.assertEqual(compatibility['candidate_bytes'],372)
        self.assertTrue(compatibility['raw_equal'])
        for name,size in [('findBaseType',339),('callCopyCtor',750),('callDestructor',392),
                ('callMemberFunc',185),('destroyBases',129),('destroyVariable',715)]:
            body=next(q for q in r['raw_function_comparisons'] if q['name']==name)
            self.assertEqual(body['candidate_bytes'],size)
            self.assertTrue(body['raw_equal'])
        handler=next(q for q in r['raw_function_comparisons'] if q['name']=='_ExceptionHandler')
        self.assertEqual(handler['candidate_bytes'],880)
        self.assertTrue(handler['raw_equal'])
        for a,b in r['target_and_source_RTTI_probes']:
            self.assertEqual(a,b)
        a,b=r['target_and_source_real_memcpy_raise_probe']
        self.assertEqual(a['restored_registers'],b['restored_registers'])
        self.assertEqual((a['actual_memcpy_calls'],b['actual_memcpy_calls']),(2,2))
        self.assertEqual(a,b)
        self.assertEqual((a['context'][13],b['context'][13]),(132,132))
        a,b=r['alternate_stack_real_memcpy_raise_probe']
        self.assertEqual((a['context'][13],b['context'][13]),(128,128))
        self.assertEqual(a,b)
        raise_native=r['RaiseException_codegen']
        self.assertEqual((raise_native['original_bytes'],raise_native['candidate_bytes']),(1151,1151))
        self.assertTrue(raise_native['complete_object_raw_equal'])
        self.assertTrue(raise_native['complete_linked_body_raw_equal'])
        self.assertEqual(raise_native['original_and_candidate_literal_fields'][0],
            raise_native['original_and_candidate_literal_fields'][1])
        self.assertEqual([f['site'] for f in raise_native['original_and_candidate_literal_fields'][0]],
            [772,404,61,33,1134])
        self.assertEqual(r['RaiseException_stack_allocations'],[390,390])
        self.assertTrue(next(q for q in r['raw_function_comparisons']
            if q['name']=='exceptionHandled')['raw_equal'])
        self.assertEqual(sum(q['raw_equal'] for q in r['raw_function_comparisons']),50)
        self.assertTrue(r['native_full_CODE_raw_equal'])
        self.assertTrue(r['all187_literal_native_fields_equal'])
        self.assertTrue(r['all50_linked_bodies_raw_equal'])
        self.assertEqual([(q['name'],q['bytes'],q['native_object_raw_equal'])
            for q in r['exact_throw_wrappers']],
            [('_ThrowException',89,True),('_ReThrowException',170,True)])
        for wrapper in r['exact_throw_wrappers']:
            self.assertEqual(wrapper['original_and_candidate_fields'][0],
                wrapper['original_and_candidate_fields'][1])
            self.assertTrue(next(q for q in r['raw_function_comparisons']
                if q['name']==wrapper['name'])['raw_equal'])
        init=r['catch_storage_codegen']['initCatchArg']
        self.assertEqual((init['original_bytes'],init['candidate_bytes'],init['stack_bytes']),
                         (678,678,24))
        self.assertTrue(init['complete_object_raw_equal'])
        self.assertEqual(init['remaining_instruction_forms'],[])
        self.assertEqual([[f['site']-start for f in ff] for ff,start in
                          zip(init['original_and_candidate_literal_fields'],(6144,6144))],
                         [[611,544,206]]*2)
        self.assertEqual([q['name'] for q in r['raw_function_comparisons'] if not q['raw_equal']],[])
        self.assertEqual(r['raw_Raise_argument_copy_bytes'],71)
        self.assertEqual(r['RaiseException_stack_allocations'],[390,390])
        self.assertTrue(r['native_Raise_object_raw_equal'])
        self.assertEqual(len(r['original_and_candidate_Raise_fields'][0]),5)
        self.assertEqual(r['original_and_candidate_Raise_fields'][0],
            r['original_and_candidate_Raise_fields'][1])
        raise_body=next(q for q in r['raw_function_comparisons'] if q['name']=='RaiseException')
        self.assertEqual((raise_body['original_bytes'],raise_body['candidate_bytes']),(1151,1151))
        self.assertTrue(raise_body['raw_equal'])
        self.assertTrue(r['whole_EXE_raw_equal'])
        self.assertTrue(r['whole_MAP_raw_equal'])
        self.assertEqual((r['source_acceptance'],r['accepted_source_bytes'],r['original_cold_rebuilt']),(False,0,False))


if __name__=='__main__':unittest.main()
