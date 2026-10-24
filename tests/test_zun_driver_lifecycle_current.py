"""DOS lifecycle and real nested helper contracts without whole-driver credit."""
from copy import deepcopy
from pathlib import Path
import json
import sys
import unittest
from unicorn import UC_HOOK_CODE

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.zun_driver_lifecycle_layout import control_flow,verify
from lib.zun_driver_lifecycle_runtime import Machine,NAMES,negative_controls
from review_th03_zun_format_work import images
from review_th03_zun_lifecycle_work import witness
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ZUN'

@unittest.skipUnless((WORK/'driver/driver.com').is_file(),'private current driver absent')
class Lifecycle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.image=(WORK/'driver/driver.com').read_bytes()
    def machine(self):
        m=Machine(self.image,0x3000);self.addCleanup(m.close);return m
    def word(self,m,offset,base=None):
        return int.from_bytes(m.uc.mem_read((m.base if base is None else base)+offset,2),'little')
    def test_complete_native_scopes_and_terminal_control_flow(self):
        work,target,candidate,at,files,maintained,cold=images(ROOT);r=verify(work,target,candidate,at,files,maintained)
        self.assertEqual((r['functions'],r['code_bytes'],len(r['ordered_native_fixups'])),(8,564,69))
        self.assertEqual(sum(f['self_relative'] for f in r['ordered_native_fixups']),27)
        self.assertEqual(r['control_flow']['terminal_unreachable_owner_bytes'],15)
        self.assertFalse(r['enclosing_driver_accepted']);self.assertFalse(r['reserved_spans_owned'])
    def test_changed_terminal_service_cannot_reuse_dead_code_partition(self):
        raw=bytearray(self.image);raw[0x180-256]=0x30
        with self.assertRaisesRegex(ValueError,'terminal DOS'):control_flow(bytes(raw))
    def test_partial_allocation_failure_preserves_first_allocation_and_size(self):
        m=self.machine();r=m.run('allocate_buffers',allocation_failure=1,paragraphs=1)
        self.assertEqual(r['terminal'],0x4C01)
        self.assertEqual((self.word(m,0xF3C),self.word(m,0xF3E),self.word(m,0xF43)),(0x6000,0x5000,1001))
        self.assertEqual(r['maintained_calls'],1)
        self.assertEqual([e for e in m.plan.events if e[0]=='store'],[('store',m.base+0xF3C,2,0x6000),('store',m.base+0xF43,2,1001)])
    def test_allocation_uses_decimal_1000_and_wraps_WORD_size(self):
        m=self.machine();r=m.run('allocate_buffers',paragraphs=0xFFFF)
        self.assertEqual((r['registers']['bx'],self.word(m,0xF43)),(1000,1999))
    def test_interrupt_argument_stores_only_AL_and_keeps_neighbor(self):
        m=self.machine();r=m.run('set_interrupt_argument',arguments=(b'511',),paragraphs=0x1234)
        self.assertEqual((r['registers']['ax'],m.uc.mem_read(m.base+0xF42,3)),(511,b'\xFF\x34\x12'))
    def test_signature_compares_fixed_0102_ignoring_vector_offset(self):
        m=self.machine();r=m.run('install',present=True,vector=0x80)
        self.assertIsNone(r['terminal']);self.assertEqual(self.word(m,0x80*4,0),0x7654)
        r=m.run('uninstall',present=False,prefix=9);self.assertIsNone(r['terminal'])
    def test_install_uses_zero_extended_DWORD_vector_and_TSR_size(self):
        m=self.machine();r=m.run('install',vector=0x80,paragraphs=1)
        self.assertEqual((r['terminal'],r['registers']['dx']),(0x3100,2001))
        self.assertEqual((self.word(m,0x200,0),self.word(m,0x202,0)),(0x22A,0x3000))
        self.assertEqual((self.word(m,0xF38),self.word(m,0xF3A)),(0x9000,0x7654))
    def test_uninstall_restores_zero_offset_and_continues_after_free_errors(self):
        m=self.machine();r=m.run('uninstall',present=True,free_failures=7)
        self.assertEqual((self.word(m,0x108,0),self.word(m,0x10A,0)),(0,0xBEEF))
        self.assertEqual(r['registers']['ax'],0)
        frees=[e[2] for e in m.plan.events if e[:2]==('dos','free')]
        self.assertEqual(frees,[0x8800,0x6100,0x5100,0x9000])
        self.assertEqual(m.plan.events[-1],('call','print_stack_string',{'pointer':0xD12}))
    def test_IRET_restores_six_byte_frame_and_stacked_flags_after_STI(self):
        m=self.machine()
        for service,flags in ((3,2),(9,0xED7)):
            r=m.run('interrupt_dispatch',service=service,flags=flags)
            self.assertEqual(r['flags'],flags);self.assertEqual(r['registers']['cs'],0x9800)
            self.assertEqual(self.word(m,0xF45),m.service_target)
    def test_mask_adapter_executes_all_real_helpers(self):
        m=self.machine();seen=set()
        h=m.uc.hook_add(UC_HOOK_CODE,lambda uc,a,s,u:seen.add(NAMES.get(a-m.base,'')))
        try:r=m.run('mask_test_command')
        finally:m.uc.hook_del(h)
        self.assertTrue({'allocate_buffers','prepare_vram','build_mask','clear_upper'}<=seen)
        self.assertEqual(m.uc.mem_read(0xA8000,16000),m.uc.mem_read(0x60000,16000))
        self.assertIsNone(r['terminal'])
    def test_draw_adapter_stops_at_first_missing_argument(self):
        m=self.machine();r=m.run('draw_command',arguments=(b'8',b'2'))
        self.assertEqual(r['terminal'],0x4C01)
        self.assertNotIn('draw_clipped',[e[1] for e in m.plan.events if e[0]=='call'])
    def test_entry_clears_DF_and_no_CR_scan_records_code_boundary_write(self):
        m=self.machine();r=m.run('entry',tail=b' '*127,flags=0xED7)
        self.assertEqual((r['terminal'],r['flags']&0x400),(0x4C01,0))
        self.assertEqual(m.uc.mem_read(m.base+0x100,1),b'\0')
        self.assertEqual(self.word(m,0xF43),0x119)
    def test_error_strings_follow_foreign_SS(self):
        m=self.machine();r=m.run('uninstall',present=True,free_failures=15,split_stack=True)
        self.assertEqual(r['registers']['ax'],7)
        self.assertEqual(m.console,b'S06S07S08S09')
    def test_all_twenty_five_actual_instruction_mutations_fail(self):
        self.assertEqual(negative_controls(self.image)['count'],25)
    @unittest.skipUnless((ROOT/'.analysis/work/zun-lifecycle-build.json').is_file(),'complete lifecycle witness absent')
    def test_dead_execution_credit_and_incomplete_vector_domain_are_rejected(self):
        original=json.loads((ROOT/'.analysis/work/zun-lifecycle-build.json').read_bytes())['scope']
        for key,value in (('executed_owner_bytes',564),('exhaustive_vector_bytes',255)):
            s=deepcopy(original);s['runtime'][key]=value
            with self.assertRaisesRegex(ValueError,'runtime dimensions'):witness(s)
