"""Whole formatter ownership, four dead jumps and target-specific rendering."""
from copy import deepcopy
from pathlib import Path
import json
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.zun_driver_format_layout import control_flow,verify
from lib.zun_driver_format_runtime import Machine,negative_controls
from review_th03_zun_format_work import images,witness

WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ZUN'


@unittest.skipUnless((WORK/'driver/driver.com').is_file(),'current private ZUN driver absent')
class Formatter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.image=(WORK/'driver/driver.com').read_bytes()
    def machine(self):
        m=Machine(self.image,0x3000);self.addCleanup(m.close);return m
    def buffer(self,m,count):return bytes(m.uc.mem_read(0x64001,count))
    def test_677_owner_bytes_partition_into_666_reachable_and_11_dead(self):
        instructions,reachable,cfg=control_flow(self.image)
        self.assertEqual((cfg['instruction_bytes'],len(reachable),cfg['unreachable_owner_bytes']),(677,666,11))
        self.assertEqual([j['address'] for j in cfg['unreachable_jumps']],[0x7A0,0x7C0,0x7E0,0x800])
    def test_redirected_predecessor_cannot_inherit_dead_jump_proof(self):
        raw=bytearray(self.image);raw[0x79E-256]=0xE8
        with self.assertRaises(ValueError):control_flow(bytes(raw))
    def test_sign_precedes_both_kinds_of_numeric_padding(self):
        m=self.machine()
        for fmt,result in ((b'%6d',b'-    5\0'),(b'%06d',b'-00005\0'),(b'%-06d',b'-5    \0')):
            m.run('format_into',text=fmt,args=(0xFFFFFFFB,));self.assertEqual(self.buffer(m,len(result)),result)
    def test_unknown_specifier_and_double_percent_are_not_printf_escapes(self):
        m=self.machine();m.run('format_into',text=b'[%5q][%%]%',args=())
        self.assertEqual(self.buffer(m,6),b'[q][]\0')
    def test_char_NUL_does_not_stop_formatting_but_stops_DOS_printing(self):
        m=self.machine();m.run('format_into',text=b'%c!',args=(0,));self.assertEqual(self.buffer(m,3),b'\0!\0')
        self.assertEqual(m.run('format_print',text=b'%c!',args=(0,))['output_hex'],'')
    def test_WORD_width_wrap_and_signed_padding_boundary(self):
        m=self.machine();m.run('format_into',text=b'%65536u',args=(7,));self.assertEqual(self.buffer(m,2),b'7\0')
        m.run('format_into',text=b'%32768u',args=(7,));self.assertEqual(self.buffer(m,32769),b' '*32767+b'7\0')
        m.run('format_into',text=b'%32768s',args=(b'',));self.assertEqual(self.buffer(m,1),b'\0')
    def test_far_strings_use_SS_slots_and_ignore_zero_pad_flag(self):
        m=self.machine();m.run('format_into',text=b'%05s/%X',args=(b'Q',0xABCDEF01),split_stack=True)
        self.assertEqual(self.buffer(m,15),b'    Q/ABCDEF01\0')
    def test_PUSHA_preserves_WORDs_while_numeric_high_halves_change(self):
        r=self.machine().run('format_into',text=b'%u',args=(0xFFFFFFFF,))
        self.assertEqual(r['full_registers']['dx'],0xFFFF2001)
        self.assertEqual(r['full_registers']['cx'],0x1298)
        self.assertEqual(r['full_registers']['ax'],0xA5A5B53A)
    def test_wrapper_keeps_original_saved_BP_overwrite(self):
        m=self.machine()
        self.assertEqual(m.run('format_print',text=b'A'*208,args=())['registers']['bp'],0xA600)
        self.assertEqual(m.run('format_print',text=b'A'*209,args=(),split_stack=True)['registers']['bp'],0x41)
    def test_forward_direction_precondition_does_not_restrict_plain_printing(self):
        m=self.machine()
        with self.assertRaisesRegex(ValueError,'forward DF'):m.run('append_string',flags=0xED7)
        self.assertEqual(m.run('print_stack_string',text=b'foreign stack',split_stack=True,flags=0xED7)['output_hex'],b'foreign stack'.hex())
    def test_unsigned_formatter_supports_every_radix_from_two_through_sixteen(self):
        m=self.machine()
        m.run('format_unsigned',value=0xFFFFFFFF,radix=16,lower=1)
        self.assertEqual(m.uc.mem_read(0x54001,9),b'ffffffff\0')
        m.run('format_unsigned',value=0,radix=2);self.assertEqual(m.uc.mem_read(0x54001,2),b'0\0')
    def test_all_twenty_four_instruction_mutations_fail(self):
        self.assertEqual(negative_controls(self.image)['count'],24)
    @unittest.skipUnless((ROOT/'.analysis/work/zun-format-build.json').is_file(),'current full formatter witness absent')
    def test_runtime_cannot_claim_executed_credit_for_dead_bytes(self):
        scope=deepcopy(json.loads((ROOT/'.analysis/work/zun-format-build.json').read_text())['scope'])
        scope['runtime']['executed_owner_bytes']=677
        with self.assertRaisesRegex(ValueError,'runtime dimensions'):witness(scope)
    def test_whole_native_owners_exclude_digit_table_and_enclosing_padding(self):
        work,target,candidate,at,files,maintained,cold=images(ROOT)
        r=verify(work,target,candidate,at,files,maintained)
        self.assertEqual((r['functions'],r['code_bytes'],len(r['ordered_native_fixups'])),(10,677,4))
        self.assertEqual([f['width'] for f in r['ordered_native_fixups']],[2,2,2,4])
        self.assertEqual(r['digit_table_dependency_bytes'],16)
        self.assertFalse(r['enclosing_driver_accepted']);self.assertFalse(r['reserved_spans_owned'])
