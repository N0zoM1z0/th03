"""Native PI producers, full state, real nested context and closed-loop proof."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_sound_work import images
from review_th03_mainl_pi_work import REPORT, witness
from lib.decoded_mainl_pi_layout import verify, CS, DATA
from lib.decoded_mainl_pi_runtime import Machine, closed_prefix_proof, negative_controls, arithmetic

WORK = ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class PiCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files = images(ROOT)

    def machine(self):
        m = Machine(self.target,0x3000)
        self.addCleanup(m.close)
        return m

    def calls(self,machine,kind):
        return [e[2] for e in machine.events if e[:2]==('call',kind)]

    def test_five_complete_functions_four_producers_and_all_literal_fields(self):
        scope = verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((scope['functions'],scope['code_bytes'],scope['ordered_native_fields'],scope['mz_relocation_count']), (5,555,25,7))
        self.assertEqual(len(scope['native_objects']),4)
        self.assertEqual(sum(len(o['ordered_relocations']) for o in scope['owners']),7)
        self.assertFalse(scope['library_context_accepted'])
        self.assertFalse(scope['whole_product_accepted'])

    def test_equal_corruption_in_both_images_cannot_hide_disagreement_with_object(self):
        def corrupt(image):
            raw = bytearray(image.program_image)
            raw[CS*16+0x5AB] ^= 1
            return replace(image,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'independently resolved native bytes'):
            verify(self.work,corrupt(self.target),corrupt(self.candidate),self.graph,self.files)

    def test_reordered_literal_MZ_fields_are_not_a_set(self):
        changed = replace(self.target,relocations=tuple(reversed(self.target.relocations)))
        with self.assertRaisesRegex(ValueError,'ordered complete MZ'):
            verify(self.work,changed,self.candidate,self.graph,self.files)

    def test_row_offset_wrap_discards_carry_before_paragraph_normalization(self):
        m = self.machine()
        m.run('put',width=3,height=2,pointer=(0xFFFF,0x5000))
        calls = self.calls(m,'packed')
        self.assertEqual([a[1:3] for a in calls],[[0xFFFF,0x5000],[0,0x5000]])
        m.run('interlace',width=3,height=3,pointer=(0xFFFF,0x5000))
        self.assertEqual([a[1:3] for a in self.calls(m,'packed')],[[0xFFFF,0x5000],[2,0x5000]])

    def test_signed_top_wrap_and_original_WORD_coordinates(self):
        m = self.machine()
        m.run('put',height=2,top=0x7FFF,left=0x8000)
        self.assertEqual([a[3:] for a in self.calls(m,'packed')],[[0x7FFF,0x8000],[0x8000,0x8000]])
        m.run('interlace',height=4,top=0xFFFF)
        self.assertEqual([a[3] for a in self.calls(m,'packed')],[0xFFFF,0])

    def test_quarter_ignores_image_dimensions_and_emits_exactly_200_rows(self):
        m = self.machine()
        r = m.run('quarter',quarter=2,width=0,height=0,pointer=(0xFFFF,0x5000))
        calls = self.calls(m,'packed')
        self.assertEqual(r['counts']['rows'],200)
        self.assertTrue(all(a[0]==320 for a in calls))
        self.assertEqual(calls[0][1:3],[15,0x5F9F])

    def test_live_width_changes_but_buffer_pointer_is_latched(self):
        m = self.machine()
        ds = m.ds*16
        m.run('put',width=0,height=3,pointer=(0xFFFF,0x5000),writes=(
            ('packed',1,ds+DATA['_pi_headers']+20,b'\x02\0'),
            ('packed',1,ds+DATA['_pi_buffers'],b'\x34\x12\x67\x45')))
        calls = self.calls(m,'packed')
        self.assertEqual([a[0] for a in calls],[0,2,2])
        self.assertEqual(calls[1][1:3],[0,0x5000])

    def test_unsigned_high_height_can_be_changed_by_the_first_graphics_reply(self):
        m = self.machine()
        at = m.ds*16+DATA['_pi_headers']+22
        for kind in ('put','interlace'):
            r = m.run(kind,height=0xFFFF,writes=(('packed',1,at,b'\0\0'),))
            self.assertEqual(r['counts']['rows'],1)
            self.assertFalse(r['nonterminal'])

    def test_FFFF_interlace_prefix_has_an_inductive_CFG_not_a_timeout(self):
        p = closed_prefix_proof(self.target)
        self.assertEqual(p['invariant_counter_states'],32768)
        self.assertFalse(p['budget_expiry_used'])
        m = self.machine()
        r = m.run('interlace',height=0xFFFF,prefix=7)
        self.assertTrue(r['nonterminal'])
        self.assertEqual(r['counts']['rows'],7)
        self.assertEqual(int.from_bytes(m.u.mem_read(0x70000+0xF7F8,2),'little'),14)
        with self.assertRaisesRegex(ValueError,'explicit proved prefix'):
            m.run('interlace',height=0xFFFF)

    def test_counter_step_mutation_rejects_the_static_closed_cycle(self):
        raw = bytearray(self.target.program_image)
        raw[CS*16+0x649] ^= 1
        with self.assertRaises(ValueError):
            closed_prefix_proof(replace(self.target,program_image=bytes(raw)))

    def test_palette_is_a_forward_overlapping_native_copy_and_clears_DF(self):
        m = self.machine()
        slot = (((DATA['_Palettes']-(DATA['_pi_headers']+24)-8)//8)*pow(9,-1,8192))&8191
        r = m.run('palette',slot=slot,flags=0xED7)
        copied = bytes(m.u.mem_read(m.ds*16+DATA['_Palettes'],48))
        self.assertEqual(copied,copied[:8]*6)
        self.assertEqual(r['flags']&0x400,0)
        self.assertEqual(r['checked_far_frames'],2)

    def test_load_executes_actual_release_and_preserves_filename_and_failed_status(self):
        m = self.machine()
        r = m.run('load',slot=0xFFFF,filename=(0xFFFF,0x6000),status=0x8000)
        self.assertEqual(len([e for e in m.events if e[0]=='heap']),3)
        self.assertEqual(self.calls(m,'decoder')[0][-2:],[0xFFFF,0x6000])
        self.assertEqual(r['registers']['ax']&65535,0x8000)
        self.assertTrue(set(range(0xFEC,0x1038))<=m.covered)

    def test_reentry_reads_real_post_release_header_and_new_decoder_buffer(self):
        m = self.machine()
        writes = (('decoder',1,m.ds*16+DATA['_pi_buffers'],b'\x07\0\0\x50'),)
        a = m.run('load',writes=writes)
        b = m.run('load',persistent=True,writes=writes)
        self.assertEqual((a['counts']['heap'],b['counts']['heap']),(3,1))

    def test_all_49_owner_and_nested_context_instruction_controls_fail(self):
        self.assertEqual(negative_controls(self.target)['count'],49)

    @unittest.skipUnless(REPORT.is_file(),'complete PI report absent')
    def test_witness_cannot_ignore_stack_library_boundaries_or_prefix_proof(self):
        report = json.loads(REPORT.read_bytes())
        if not report['complete']:
            self.skipTest('PI review running')
        scope = report['scope']
        witness(scope)
        for part,key,value in (('runtime','ignored_stack_bytes',64),('runtime','executed_owner_bytes',554),
                               ('runtime','library_context_accepted',True),('layout','ordered_native_fields',24)):
            bad = deepcopy(scope)
            bad[part][key] = value
            with self.assertRaises(ValueError):
                witness(bad)


class ScalarFlags(unittest.TestCase):
    def test_signed_overflow_and_unsigned_carry_are_separate(self):
        self.assertEqual(arithmetic(0xFFFF,1),(0,0x55))
        self.assertEqual(arithmetic(0x7FFF,1),(0x8000,0x894))
        self.assertEqual(arithmetic(0x8000,1,True),(0x7FFF,0x814))
