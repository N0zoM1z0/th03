"""Complete roll ownership stays distinct from prefix and external-interface evidence."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.decoded_mainl_staff_roll_layout import CS,DS,START,SIZE,DATA,verify as layout
from lib.decoded_mainl_staff_roll_runtime import Machine
from lib.decoded_mainl_staff_roll_proofs import geometry_proof
import review_th03_mainl_staff_roll_work as review
import review_th03_mainl_sound_work as sound


@unittest.skipUnless((ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML/bin/th03/mainl.target.exe').is_file(),
                     'current private MAINL proof absent')
class MainlStaffRollCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,cls.cold,cls.graph,cls.files=sound.images(ROOT)

    def test_entire_native_roll_and_literal_ordered_call_graph(self):
        result=layout(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((result['code_bytes'],len(result['ordered_native_fields']),result['mz_relocation_count'],
                          len(result['internal_near_calls']),len(result['far_calls'])),(980,108,34,22,34))
        self.assertEqual(result['owners'][0]['source'],'src/mainl/staff/data.cpp')
        self.assertFalse(result['whole_product_accepted'])
        self.assertFalse(result['enclosing_DATA_or_other_CODE_newly_accepted'])

    def test_native_raw_or_order_drift_cannot_inherit_the_roll(self):
        start=CS*16+START
        raw=bytearray(self.target.program_image)
        raw[start+SIZE-1]^=1
        with self.assertRaises(ValueError):
            layout(self.work,replace(self.target,program_image=bytes(raw)),self.candidate,self.graph,self.files)
        reloc=list(self.target.relocations)
        positions=[i for i,r in enumerate(reloc) if start<=r.linear<start+SIZE]
        reloc[positions[0]],reloc[positions[1]]=reloc[positions[1]],reloc[positions[0]]
        with self.assertRaisesRegex(ValueError,'ordered MZ'):
            layout(self.work,replace(self.target,relocations=tuple(reloc)),self.candidate,self.graph,self.files)

    def test_preparation_keeps_BYTE_overflow_and_zero_character_quotient(self):
        machine=Machine(self.target,0x3000)
        try:
            result=machine.run(prepare_only=True,character=0,credits=4,skill=250,score=(0,0,0,0,0,255,3,0))
            self.assertTrue(result['prepare_only'])
            for name,expected in (('playchar',0),('score',255),('skill',1)):
                self.assertEqual(bytes(machine.u.mem_read(machine.ds*16+DATA[name],1)),bytes([expected]))
            self.assertEqual(result['counts'],{'kaja':2})
        finally:
            machine.close()

    def test_no_input_prefix_has_actual_nested_calls_and_no_return_credit(self):
        machine=Machine(self.target,0x1000)
        try:
            result=machine.run(sample=(0,0,0,0),input_prefix=3)
            self.assertEqual((result['input_iterations'],result['fade_iterations'],result['stack_depth'],
                              result['actual_clear_WORD_callbacks']),(3,0,78,368000))
            self.assertNotIn('cdg-free',result['counts'])
            self.assertEqual(result['counts']['verdict'],2)
        finally:
            machine.close()

    def test_fade_and_closed_wait_proofs_remain_conditional(self):
        proof=geometry_proof(self.target)
        self.assertEqual((proof['skill_pair_cases'],proof['minimum_constant_nonzero_input_iterations'],
                          proof['fade_iterations'],len(proof['cleanup_slots'])),(262144,257,199,32))
        self.assertFalse(proof['no_input_prefixes_are_returns'])
        self.assertFalse(proof['guest_iterations_skipped'])
        self.assertFalse(proof['budget_expiry_used'])
        self.assertFalse(proof['physical_IRQ_audio_input_or_pixels_proved'])
        self.assertEqual(len(proof['returning_assumptions']),4)

    def test_complete_staff_TU_and_DATA_have_disjoint_owners(self):
        publication=json.loads((ROOT/'config/mainl_work/scoped_acceptance.json').read_bytes())
        owners=[o for o in publication['audit']['scope']['owners'] if o['source']=='src/mainl/staff/data.cpp']
        code=[o for o in owners if o['segment']==CS]
        data=[o for o in owners if o['segment']==DS]
        self.assertEqual((sum(o['size'] for o in code),sum(o['size'] for o in data)),(3695,224))
        self.assertEqual(sum(o.get('procedure_count',1) for o in owners),19)
        coverage=set()
        for owner in code:
            span=set(range(owner['offset'],owner['offset']+owner['size']))
            self.assertFalse(coverage&span)
            coverage|=span
        self.assertEqual(coverage,set(range(0x2382,0x31F1)))

    def test_witness_cannot_relabel_preparation_or_prefix_as_complete_returns(self):
        report=json.loads(review.REPORT.read_bytes())
        self.assertTrue(report['complete'])
        scope=deepcopy(report['scope'])
        review.witness(scope)
        scope['runtime']['complete_returns_per_image']+=scope['runtime']['preparation_boundaries_per_image']
        with self.assertRaises(ValueError):
            review.witness(scope)


if __name__=='__main__':
    unittest.main()
