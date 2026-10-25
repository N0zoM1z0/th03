"""Whole CDG producer, live resource semantics and real nested native frames."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_sound_work import images
from review_th03_mainl_cdg_work import REPORT, witness
from lib.decoded_mainl_cdg_layout import verify, CS, SLOTS, FLAG
from lib.decoded_mainl_cdg_runtime import Machine, header

WORK = ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class CDGCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files = images(ROOT)

    def machine(self):
        m = Machine(self.target,0x3000)
        self.addCleanup(m.close)
        return m

    def calls(self,m,kind):
        return [e[2] for e in m.events if e[:2]==('call',kind)]

    def test_one_whole_TU_five_procedures_and_all_ordered_fields(self):
        r = verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((r['functions'],r['code_bytes'],len(r['ordered_native_fields']),r['mz_relocation_count']),(5,593,35,24))
        self.assertEqual((r['normal_tlink_relaxed_calls'],r['compiler_backward_bridge_calls']),(4,1))
        self.assertEqual(sum(len(o['ordered_relocations']) for o in r['owners']),24)
        self.assertFalse(r['enclosing_DATA_or_interfaces_accepted'])
        self.assertFalse(r['whole_product_accepted'])

    def test_equal_corruption_in_both_images_is_not_native_ownership(self):
        def changed(image):
            raw = bytearray(image.program_image)
            raw[CS*16+0x76D] ^= 1
            return replace(image,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'independently linked native bytes'):
            verify(self.work,changed(self.target),changed(self.candidate),self.graph,self.files)

    def test_MZ_order_is_literal_not_a_set(self):
        changed = replace(self.target,relocations=tuple(reversed(self.target.relocations)))
        with self.assertRaisesRegex(ValueError,'complete ordered MZ'):
            verify(self.work,changed,self.candidate,self.graph,self.files)

    def test_WORD_image_size_truncates_before_signed_index_multiply(self):
        m = self.machine()
        r = m.run('single',size=0x3334,n=0xFFFF)
        self.assertEqual(self.calls(m,'seek'),[[1,0xFFFC,0xFFFF]])
        self.assertEqual(r['registers']['ax']>>16,0xFFFF)
        self.assertEqual(self.calls(m,'alloc'),[[0x3334],[0xCCD0]])

    def test_noalpha_extra_seek_zero_extends_and_clears_EAX_high_half(self):
        m = self.machine()
        r = m.run('single_noalpha',size=0xFFFF,n=0x8000)
        seeks = self.calls(m,'seek')
        self.assertEqual(seeks[-1],[1,0xFFFF,0])
        self.assertEqual(r['registers']['ax']>>16,0)
        self.assertEqual(self.calls(m,'alloc'),[[0xFFFC]])

    def test_zero_allocations_still_issue_both_native_reads(self):
        m = self.machine()
        r = m.run('single',allocations=(0,))
        self.assertEqual(self.calls(m,'read')[1:],[[4,0,0],[16,0,0]])
        self.assertEqual(r['interfaces']['alloc'],2)
        self.assertEqual(bytes(m.u.mem_read(0,5)),b'\x37\xC9\x18\xAF\xE1')

    def test_zero_color_length_is_not_an_early_return(self):
        m = self.machine()
        r = m.run('single',size=0x4000)
        self.assertEqual(self.calls(m,'alloc'),[[0x4000],[0]])
        self.assertEqual(self.calls(m,'read')[-1],[0,0,0x6000])
        self.assertEqual(r['interfaces']['close'],1)

    def test_failed_header_reads_use_actual_stale_metadata(self):
        m = self.machine()
        r = m.run('all',count=2,size=7,read_limits=(0,),status=0xFFFF)
        self.assertEqual(r['native_entries']['free'],2)
        self.assertEqual(self.calls(m,'alloc'),[[7],[28],[7],[28]])
        self.assertEqual(r['interfaces']['close'],1)

    def test_header_count_zero_does_not_free_file_header_segment_words(self):
        m = self.machine()
        r = m.run('all',count=0,header_segments=(0x4444,0x5555))
        self.assertEqual(r['interfaces'].get('alloc',0),0)
        self.assertEqual(bytes(m.u.mem_read(m.ds*16+SLOTS+12,4)),b'\x44\x44\x55\x55')

    def test_count_high_bit_is_unsigned_and_all_nested_frees_execute(self):
        m = self.machine()
        r = m.run('all',count=128)
        self.assertEqual(r['native_entries']['free'],128)
        self.assertEqual(r['interfaces']['alloc'],256)
        self.assertEqual(r['interfaces']['read'],257)

    def test_live_count_growth_separates_cleanup_and_loading_passes(self):
        m = self.machine()
        r = m.run('all',count=1,writes=(('read',2,m.ds*16+SLOTS+10,b'\x03'),))
        self.assertEqual(r['native_entries']['free'],1)
        self.assertEqual(r['interfaces']['alloc'],6)
        self.assertEqual(r['interfaces']['read'],7)

    def test_all_noalpha_executes_all_and_resets_flag_instead_of_restoring(self):
        m = self.machine()
        r = m.run('all_noalpha',count=3,noalpha=0xFF)
        self.assertEqual(r['native_entries']['all'],1)
        self.assertEqual(r['native_entries']['free'],3)
        self.assertEqual(r['noalpha'],0)
        self.assertEqual(r['interfaces']['alloc'],3)
        self.assertEqual(r['interfaces']['seek'],3)

    def test_malformed_slot_aliases_global_flag_through_the_header(self):
        m = self.machine()
        r = m.run('all_noalpha',slot=0xEB8,bottom=0,count=2,noalpha=0xFF)
        # This unchecked slot places bottom_left's low byte at cdg_noalpha.
        # Reading the header writes zero there after the wrapper wrote true.
        self.assertEqual(r['interfaces']['alloc'],4)
        self.assertEqual(r['interfaces'].get('seek',0),0)
        self.assertEqual(r['noalpha'],0)

    def test_alloc_callback_changes_the_subsequent_live_read_length(self):
        m = self.machine()
        m.run('single',size=4,writes=(('alloc',1,m.ds*16+SLOTS,b'\x03\0'),))
        self.assertEqual(self.calls(m,'alloc'),[[4],[12]])
        self.assertEqual(self.calls(m,'read')[1][0],3)

    def test_self_aliasing_file_payload_changes_live_metadata_without_sanitizing(self):
        m = self.machine()
        r = m.run('all',slot=0xE30,count=3,allocations=(m.ds,),payload=b'\0'*32)
        self.assertEqual(r['native_entries']['free'],3)
        # Four alpha bytes cannot reach metadata. The following 16 color bytes
        # reach bitplane_size at offset 14, but not image_count at offset 24.
        self.assertEqual(r['interfaces']['alloc'],6)
        self.assertEqual(r['interfaces']['read'],7)
        self.assertEqual(self.calls(m,'alloc'),[[4],[16],[0],[0],[0],[0]])
        self.assertEqual(self.calls(m,'read')[-1][0],0)

    def test_a_longer_self_aliasing_prefix_can_shorten_the_loading_loop(self):
        m = self.machine()
        r = m.run('all',slot=0xE30,size=32,count=3,allocations=(m.ds,),payload=b'\0'*32)
        self.assertEqual(r['native_entries']['free'],3)
        self.assertEqual(r['interfaces']['alloc'],2)
        self.assertEqual(r['interfaces']['read'],3)
        self.assertEqual(self.calls(m,'read')[-1][0],0)

    def test_zero_and_repeated_segment_frees_keep_order_and_clear_after_failure(self):
        m = self.machine()
        r = m.run('free',old_segments=(0xFFFF,0xFFFF),status=0xFFFF)
        self.assertEqual(self.calls(m,'free'),[[0xFFFF],[0xFFFF]])
        self.assertEqual(bytes(m.u.mem_read(m.ds*16+SLOTS+12,4)),b'\0'*4)
        r = m.run('free',old_segments=(0,0x8000))
        self.assertEqual(self.calls(m,'free'),[[0x8000]])

    def test_reentry_consumes_real_new_segment_values(self):
        m = self.machine()
        m.run('single',allocations=(0x5000,0x6000))
        m.run('single',persistent=True,allocations=(0x8000,0))
        self.assertEqual(self.calls(m,'free'),[[0x5000],[0x6000]])

    @unittest.skipUnless(REPORT.is_file(),'complete CDG report absent')
    def test_full_witness_rejects_partial_instruction_or_stack_credit(self):
        r = json.loads(REPORT.read_bytes())
        if not r['complete']:
            self.skipTest('CDG review running')
        s = r['scope']
        witness(s)
        self.assertEqual(s['negative_controls']['count'],66)
        for part,key,value in (('runtime','ignored_stack_bytes',64),('runtime','executed_owner_bytes',592),
                               ('runtime','actual_owned_nested_helpers',False),('layout','normal_tlink_relaxed_calls',0)):
            bad = deepcopy(s)
            bad[part][key] = value
            with self.assertRaises(ValueError):
                witness(bad)


class HeaderFormat(unittest.TestCase):
    def test_header_is_16_bytes_and_count_is_a_BYTE(self):
        raw = header(size=0xFFFF,count=255,segments=(0x1234,0x5678))
        self.assertEqual(len(raw),16)
        self.assertEqual(raw[10:12],b'\xFF\x7F')
        self.assertEqual(raw[12:],b'\x34\x12\x78\x56')
