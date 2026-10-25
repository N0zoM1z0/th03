"""Independent complete-state ONGCHK contracts and source ownership limits."""
from copy import deepcopy
from pathlib import Path
import json,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from lib.zun_ongchk_runtime import Machine,LOOPS,PATTERN,negative_controls
from lib.zun_ongchk_layout import verify
from review_th03_zun_ongchk_work import witness
from review_th03_zun_format_work import images
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ZUN'

@unittest.skipUnless((WORK/'ongchk/ongchk.com').is_file(),'current native ONGCHK absent')
class OngchkExact(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.image=(WORK/'ongchk/ongchk.com').read_bytes()
    def machine(self):
        m=Machine(self.image,0x3000);self.addCleanup(m.close);return m
    def test_whole_native_owner_and_seven_closed_polling_cycles(self):
        work,_,_,_,files,maintained,raw=images(ROOT)
        target=(work/'product/zun.target.com').read_bytes();candidate=(work/'product/zun.com').read_bytes()
        r=verify(work,target,candidate,files,maintained,json.loads(raw))
        self.assertEqual((r['source_extents'],r['entry_points'],r['code_bytes'],r['data_bytes'],r['bss_bytes']),(1,10,892,34,42))
        self.assertEqual(len(r['native']['native_fields']),38);self.assertEqual(len(r['polling_cycles']),7)
        self.assertEqual(r['owners'][0]['payload_option'],'-1');self.assertFalse(r['whole_product_accepted'])
    def test_both_changed_images_cannot_hide_the_actual_native_producer(self):
        work,_,_,_,files,maintained,raw=images(ROOT);image=bytearray((work/'product/zun.target.com').read_bytes());image[0x226]^=1
        with self.assertRaisesRegex(ValueError,'complete attested target payload equality'):
            verify(work,bytes(image),bytes(image),files,maintained,json.loads(raw))
    def test_PSP_space_scan_and_length_priority_are_distinct_from_literal_tail_8(self):
        m=self.machine();boards=((0x88,2),(0x188,3))
        self.assertEqual(m.run(boards=boards,tail=b'8')['result'],5)
        self.assertEqual(m.run(boards=boards,tail=b'x'*56)['result'],4)
        r=m.run(fallback=0x88,tail=b' '*32)
        self.assertEqual((r['result'],r['registers']['si']),(1,0xA2))
    def test_full_WORD_port_bank_and_inherited_SS_and_count_survive(self):
        m=self.machine();r=m.run(fallback=0xFE88,override=254,ss=0x8000,stack=0x80,flags=2)
        self.assertEqual((r['registers']['dx'],r['registers']['sp'],r['registers']['ss']),(0xFE8E,0x80,0x8000))
        self.assertEqual(r['flags']&0x280,0x280)
        self.assertEqual(bytes(m.u.mem_read(0x80080,4)),b'\x5C\xA7\x69\xC3')
    def test_success_executes_sixty_real_register_writes_and_copies_actual_pattern(self):
        m=self.machine();r=m.run(boards=((0x188,3),),busy=1,rom_word=0x2A27)
        self.assertEqual((r['result'],r['register_write_calls'],r['spin_calls']),(5,60,128))
        self.assertEqual(bytes(m.u.mem_read(m.base+0x47C,32)),PATTERN)
        self.assertEqual(bytes(m.u.mem_read(m.base+0x4A8,32)),PATTERN)
        self.assertEqual((r['registers']['cx'],r['registers']['si'],r['registers']['di']),(0,0x49C,0x4C8))
    def test_each_mismatch_preserves_early_compare_registers_and_defined_flags(self):
        m=self.machine()
        for index in (0,15,31):
            r=m.run(boards=((0x188,3),),mismatch_index=index,mismatch_mask=0x80)
            self.assertEqual((r['result'],r['registers']['cx'],r['registers']['si'],r['registers']['di']),
                             (3,31-index,0x47D+index,0x4A9+index))
            self.assertEqual(r['flags']&1,0)
    def test_timeout_preserves_remaining_counter_and_does_not_run_read_cleanup(self):
        m=self.machine()
        for index in (0,31):
            r=m.run(boards=((0x188,3),),timeout_index=index)
            self.assertEqual((r['result'],r['registers']['cx'],r['registers']['si'],r['register_write_calls']),(3,32-index,0x47D+index,11))
            self.assertEqual(r['flags_mask'],0x8C5);self.assertEqual(r['flags']&0x45,0x44)
    def test_seven_nonterminal_cycles_have_independent_live_frame_and_IF_contracts(self):
        m=self.machine()
        for hold,(_,_,depth) in LOOPS.items():
            r=m.run(boards=((0x188,3),),hold=hold,ss=0x8000,stack=0x80,flags=0xED7)
            self.assertTrue(r['nonterminal']);self.assertEqual(r['rounds'],5)
            self.assertEqual(r['registers']['sp'],0x80-depth)
            self.assertEqual(r['flags']&0x600,0x200 if hold=='write_complete' else 0)
    def test_independent_instruction_and_consumed_DATA_controls_are_separate(self):
        r=negative_controls(self.image)
        self.assertEqual((r['instruction_mutations'],r['actual_consumed_DATA_mutations'],r['static_initialized_DATA_mutations_rejected']),(43,33,34))
        self.assertFalse(r['result_initializer_is_consumed_before_store']);self.assertFalse(r['static_DATA_controls_have_instruction_credit'])
    @unittest.skipUnless((ROOT/'.analysis/work/zun-ongchk-build.json').is_file(),'full ONGCHK report absent')
    def test_full_witness_cannot_turn_DATA_into_executed_code_or_claim_hardware(self):
        r=json.loads((ROOT/'.analysis/work/zun-ongchk-build.json').read_bytes())
        if not r['complete']:self.skipTest('ONGCHK review still running')
        s=r['scope'];witness(s)
        for part,key,value in (('runtime','executed_owner_bytes',926),('runtime','physical_timing_or_devices_emulated',True),
                               ('negative_controls','actual_consumed_DATA_mutations',34),('layout','whole_product_accepted',True)):
            bad=deepcopy(s);bad[part][key]=value
            with self.assertRaises(ValueError):witness(bad)
