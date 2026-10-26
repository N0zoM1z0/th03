"""Music Room controls must reject guests, never forgive verifier defects."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.op_music_state_runtime import Machine,ContractError,negative_controls
from lib.op_music_state_layout import START,SIZE,verify as layout
from review_th03_op_cfg_work import images
import review_th03_op_music_state_work as review

@unittest.skipUnless((ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe').is_file(),
                     'current private OP proof absent')
class OpMusicStateCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.work,cls.target,cls.candidate,*_=images(ROOT)

    def test_complete_native_layout(self):
        result=layout(ROOT,self.work,self.target,self.candidate)
        self.assertEqual((result['functions'],result['code_bytes'],len(result['ordered_native_fields']),
                          len(result['ordered_relocations'])),(4,216,12,4))

    def test_all38_mutants_reject(self):
        result=negative_controls(self.target)
        self.assertEqual(result['actual_instruction_mutations'],38)
        self.assertEqual(len(set(result['rejected'])),38)
        for name in ('page-field','bold-FX','live-page-second-read','live-pointer-second-read',
                     'DWORD-store','free-near-return'):
            self.assertIn(name,result['rejected'])

    def test_constructor_failure_is_fatal_not_rejection(self):
        with patch.object(Machine,'__init__',side_effect=RuntimeError('constructor defect')):
            with self.assertRaisesRegex(ValueError,'control construction failed: track-ENTER-locals') as caught:
                negative_controls(self.target)
            self.assertIsInstance(caught.exception.__cause__,RuntimeError)

    def test_unexpected_hook_exception_is_fatal_not_rejection(self):
        for exception in (IndexError,TypeError,AssertionError,ValueError):
            with self.subTest(exception=exception):
                with patch.object(Machine,'event',side_effect=exception('injected hook defect')):
                    with self.assertRaisesRegex(exception,'injected hook defect'):
                        negative_controls(self.target)

    def test_list_first_callback_updates_second_draw_and_later_pages(self):
        m=Machine(self.target,0x3000)
        try:
            row=m.run('tracklist_put_both',index=0,page=128,page_after_first=255,pointer_after_first=0xDEADBEEF)
            self.assertEqual(len(row['text']),42)
            self.assertEqual(row['text'][1][:2],[0xBEEF,0xDEAD])
            self.assertEqual(row['ports'],[129,255]+[2,255]*20)
            self.assertEqual([row['text'][2*i][3] for i in range(21)],[40+16*i for i in range(21)])
        finally:m.close()

    def test_equal_mutated_images_cannot_inherit_native_layout(self):
        raw=bytearray(self.target.program_image);raw[START+1]^=1
        bad=replace(self.target,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'all216 independently resolved'):
            layout(ROOT,self.work,bad,bad)

    def test_prior_invariance_rejects_unrelated_owner_and_changed_observation(self):
        current=json.loads((ROOT/'config/op_work/scoped_acceptance.json').read_bytes())['audit']['scope']
        review.invariance(ROOT,current)
        bad=deepcopy(current)
        extra=deepcopy(bad['owners'][0]);extra['unit_id']='unrelated-new-owner'
        bad['owners'].append(extra)
        with self.assertRaisesRegex(ValueError,'entire prior accepted'):
            review.invariance(ROOT,bad)
        bad=deepcopy(current);bad['runtime']['unexpected_observation']=True
        with self.assertRaisesRegex(ValueError,'entire prior accepted'):
            review.invariance(ROOT,bad)

    def test_witness_rejects_partial_or_wider_claims(self):
        scope=json.loads(review.REPORT.read_bytes())['scope'];review.witness(scope)
        for path,value in ((('runtime','images'),1),(('runtime','cases_per_image'),894),
                           (('layout','whole_product_accepted'),True),(('negative_controls','actual_instruction_mutations'),37)):
            bad=deepcopy(scope);at=bad
            for key in path[:-1]:at=at[key]
            at[path[-1]]=value
            with self.assertRaises(ValueError):review.witness(bad)

if __name__=='__main__':unittest.main()
