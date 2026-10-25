"""VS caller ABI, raw native ownership and bounded character-selection interface."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import json,sys,unittest

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from lib.op_vs_layout import START,verify
from lib.op_vs_runtime import Machine,negative_controls
from review_th03_op_cfg_work import images
from review_th03_op_vs_work import witness

WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP'

@unittest.skipUnless((WORK/'bin/th03/op.exe').is_file(),'private current OP absent')
class VsCaller(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.work,cls.target,cls.candidate,*_=images(ROOT)

    def machine(self):
        m=Machine(self.target,0x3000);self.addCleanup(m.close);return m

    def test_complete_native_caller_excludes_title_and_character_selection_credit(self):
        r=verify(self.work,self.target,self.candidate)
        self.assertEqual((r['functions'],r['code_bytes'],len(r['ordered_native_fields']),len(r['ordered_relocations'])),(1,365,23,7))
        self.assertEqual(r['box_dependency']['size'],44)
        for key in ('character_selection_procedures_owned','containing_producer_accepted','whole_product_accepted'):
            self.assertFalse(r[key])
        self.assertFalse(r['box_dependency']['source_credit_added'])

    def test_same_mutation_in_both_images_cannot_hide_native_mismatch(self):
        def change(image):
            raw=bytearray(image.program_image);raw[START+1]^=1
            return replace(image,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'complete native VS bytes'):
            verify(self.work,change(self.target),change(self.candidate))

    def test_held_input_on_entry_moves_before_confirm(self):
        r=self.machine().run(samples=((0x21,0,0,0),))
        self.assertEqual((r['selection'],r['polled_samples'],r['renderer_calls'],r['delay_calls']),(2,1,5,13))

    def test_both_directions_execute_and_CANCEL_only_delays(self):
        r=self.machine().run(samples=((3,0,0,0),(0,0,0,0),(0x4000,0,0,0),(0,0,0,0),(0x20,0,0,0)))
        self.assertEqual((r['selection'],r['polled_samples'],r['renderer_calls'],r['delay_calls']),(0,5,7,17))

    def test_full_previous_WORD_blocks_confirm_until_release(self):
        r=self.machine().run(samples=((0x8000,0,0,0),(0x20,0,0,0),(0,0,0,0),(0x2000,0,0,0)))
        self.assertEqual((r['polled_samples'],r['delay_calls']),(4,16))

    def test_post_match_unsigned_BYTE_has_no_range_check_or_render(self):
        r=self.machine().run(mode=255,samples=(),selection_ax=0xA580)
        self.assertEqual((r['selection'],r['polled_samples'],r['renderer_calls'],r['delay_calls']),(127,0,0,0))
        self.assertTrue(r['cancelled']);self.assertEqual(r['registers']['ax'],0xA501)

    def test_only_AL_controls_selection_reply_and_failed_exec_returns_false(self):
        m=self.machine()
        for response in (0,0x100,0x8000):
            r=m.run(mode=129,samples=(),selection_ax=response,status=0xBEEF)
            self.assertFalse(r['cancelled']);self.assertEqual(r['registers']['ax'],0xBE00)
            self.assertEqual(r['file_hex'][:8],'d263b4d3')
        r=m.run(mode=129,samples=(),selection_ax=0xFF80)
        self.assertTrue(r['cancelled']);self.assertEqual(r['registers']['ax'],0xFF01)

    def test_private_stack_and_near_return_preserve_caller_words(self):
        m=self.machine();r=m.run(selection_ax=0,stack=0x80,flags=0xED7,resoff=0xFF80)
        self.assertEqual(m.r('sp'),0x82);self.assertEqual(r['flags']&0x600,0x600)
        self.assertEqual(bytes(m.uc.mem_read(0x70080,4)),b'\xff\xff\x5a\xa5')

    def test_thirty_one_real_instruction_mutations_fail(self):
        self.assertEqual(negative_controls(self.target)['count'],31)

    @unittest.skipUnless((ROOT/'.analysis/work/op-vs-build.json').is_file(),'complete VS report absent')
    def test_witness_cannot_add_unexecuted_character_selection_or_title_ownership(self):
        s=json.loads((ROOT/'.analysis/work/op-vs-build.json').read_bytes())['scope']
        witness(s)
        for part,key in (('runtime','character_selection_implementations_executed'),('layout','character_selection_procedures_owned')):
            bad=deepcopy(s);bad[part][key]=True
            with self.assertRaises(ValueError):witness(bad)
        bad=deepcopy(s);bad['layout']['box_dependency']['source_credit_added']=True
        with self.assertRaisesRegex(ValueError,'bounded caller ownership'):witness(bad)
