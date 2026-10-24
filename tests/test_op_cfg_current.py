"""Near cfg scope, partial reads and deliberately uninitialized save bytes."""
from copy import deepcopy
from pathlib import Path
import json
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.pc98 import parse_mz
from lib.op_cfg_layout import verify,native_image,OBJECT
from lib.op_cfg_runtime import Machine,negative_controls,RESIDENT,ACTIVE,FM,DISABLED
from review_th03_op_cfg_work import witness,sdk_inventory
from test_main_enemy_layout import mutate_record

WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP'


@unittest.skipUnless((WORK/'bin/th03/op.target.exe').is_file(),'private current OP target absent')
class Configuration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target=parse_mz((WORK/'bin/th03/op.target.exe').read_bytes());cls.candidate=parse_mz((WORK/'bin/th03/op.exe').read_bytes())
    def machine(self):
        m=Machine(self.target,0x3000);self.addCleanup(m.close);return m
    def test_three_full_near_functions_exclude_menu_siblings(self):
        r=verify(WORK,self.target,self.candidate)
        self.assertEqual((r['functions'],r['code_bytes']),(3,271))
        self.assertEqual((len(r['ordered_native_fields']),len(r['ordered_relocations'])),(28,13))
        self.assertEqual((r['containing_code_bytes'],r['containing_data_bytes'],r['containing_bss_bytes']),(3094,487,6))
        self.assertFalse(r['containing_producer_accepted']);self.assertFalse(r['whole_product_accepted'])
        self.assertEqual(r['reviewed_initialized_dependency_bytes'],18)
        self.assertTrue(all(o['canonical_file_offset'] is None for o in r['owners']))
    def test_containing_pub_cannot_be_renamed_to_borrow_the_cfg_scope(self):
        raw=(WORK/OBJECT).read_bytes()
        changed=mutate_record(raw,lambda r:r.name=='PUBDEF' and b'@cfg_load$qv' in r.data,lambda d:d.replace(b'@cfg_load$qv',b'@cfg_fake$qv'))
        with self.assertRaisesRegex(ValueError,'fifteen containing CODE publics'):native_image(changed)
    def test_real_segment_addend_is_not_a_normalized_pointer(self):
        raw=(WORK/OBJECT).read_bytes()
        def change(d):
            value=bytearray(d);self.assertEqual(value[3+37],2);value[3+37]=0;return bytes(value)
        changed=mutate_record(raw,lambda r:r.name=='LEDATA' and r.data[:3]==b'\x01\0\0',change)
        with self.assertRaisesRegex(ValueError,'twenty-eight literal ordered'):native_image(changed)
    def test_actual_sdk_headers_match_all_five_pinned_copies(self):
        self.assertEqual(len(sdk_inventory(ROOT)),5)
    def test_partial_failed_read_still_uses_unsanitized_stack_fields(self):
        m=self.machine();r=m.run('cfg_load',read_bytes=0,trash=0x5A,status=0xFFFF)
        self.assertEqual(m.uc.mem_read(m.data+RESIDENT,4),b'\0\0\x5A\x5A')
        self.assertEqual(r['registers']['ax'],0x5A)
        self.assertEqual(m.uc.mem_read(0x5A5A0+0xB,1),b'\x5A')
        self.assertEqual(m.r('sp'),0xF802)
    def test_plain_save_writes_four_including_the_original_stack_byte(self):
        m=self.machine()
        for trash in (0,0xA7,0xFF):
            r=m.run('cfg_save',trash=trash,status=0x8000)
            self.assertEqual(bytes.fromhex(r['file_hex']),bytes((0x81,0x52,0xA3,trash,0x57,0,0x50,0xA7)))
    def test_exit_save_runs_real_copy_and_clears_the_remaining_five_bytes(self):
        m=self.machine();r=m.run('cfg_save_exit',trash=0xA7,flags=0xED7)
        self.assertEqual(bytes.fromhex(r['file_hex']),b'\x81\x52\xA3'+bytes(5));self.assertFalse(r['final_df'])
        self.assertEqual(r['events'][0][0],'copy')
        self.assertTrue(m.run('cfg_save',flags=0xED7)['final_df'])
    def test_requested_off_differs_from_unavailable_sound(self):
        m=self.machine();cfg=b'\0\x01\x03\x48\x57\0\x50\xA7'
        m.run('cfg_load',cfg=cfg,driver=0)
        self.assertEqual(m.uc.mem_read(m.data+ACTIVE,1),b'\0');self.assertEqual(m.uc.mem_read(m.data+DISABLED,1),b'\0')
        m.run('cfg_load',driver=0xFF,midi=0)
        self.assertEqual(m.uc.mem_read(m.data+DISABLED,1),b'\x01');self.assertEqual(m.uc.mem_read(0x50000+0x15,1),b'\0')
    def test_midi_byte_is_not_normalized_and_failed_probe_keeps_fm_flag(self):
        m=self.machine();m.run('cfg_load',driver=0xFF,midi=0x80,fm=0x37)
        self.assertEqual(m.uc.mem_read(m.data+ACTIVE,1),b'\x80');self.assertEqual(m.uc.mem_read(m.data+FM,1),b'\x37')
    def test_twenty_one_real_mutations_fail_the_cfg_contract(self):
        self.assertEqual(negative_controls(self.target)['count'],21)
    @unittest.skipUnless((ROOT/'.analysis/work/op-cfg-build.json').is_file(),'current full cfg witness absent')
    def test_partial_read_domain_cannot_inherit_complete_cfg_witness(self):
        scope=deepcopy(json.loads((ROOT/'.analysis/work/op-cfg-build.json').read_text())['scope']);scope['runtime']['read_prefix_lengths']=1
        with self.assertRaisesRegex(ValueError,'cfg runtime dimensions'):witness(scope)
