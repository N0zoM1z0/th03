"""Native root ownership, byte/WORD semantics and physical stack contracts."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import csv,json,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_sound_work import images
from lib.decoded_mainl_root_helpers_layout import verify,ENTRIES
from lib.decoded_mainl_root_helpers_runtime import Machine,negative_controls
from review_th03_mainl_root_helpers_work import witness
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'

@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class RootHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files=images(ROOT)
    def machine(self):
        m=Machine(self.target,0x3000);self.addCleanup(m.close);return m
    def test_complete_native_procedures_exclude_three_NOPs_and_enclosing_root(self):
        r=verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((r['functions'],r['code_bytes'],len(r['ordered_native_fields'])),(5,150,5))
        self.assertEqual(r['excluded_adjacent_NOPs'],[0xC5F,0xC65,0x2C2F]);self.assertEqual(r['ordered_relocations'],[])
        self.assertFalse(r['containing_producer_accepted']);self.assertFalse(r['whole_product_accepted'])
    def test_both_images_cannot_hide_a_changed_seed_reference(self):
        def changed(image):
            raw=bytearray(image.program_image);raw[0x1A43]^=1
            return replace(image,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'whole resolved native helper bytes'):
            verify(self.work,changed(self.target),changed(self.candidate),self.graph,self.files)
    def test_DWORD_recurrence_preserves_the_carry_into_the_high_WORD(self):
        m=self.machine()
        for seed in (0,1,0xEBE3,0xFFFF,0xFFFF0000,0xFFFFFFFF):
            r=m.run('rand',random_seed=seed);new=(seed*22695477+1)&0xFFFFFFFF
            self.assertEqual(r['random_seed'],new);self.assertEqual(r['registers']['ax'],(new>>16)&32767)
            self.assertEqual(r['registers']['dx'],new>>16)
    def test_random_flags_describe_AH_not_the_complete_return_AX(self):
        # The final AND is byte-sized: AX can be nonzero while ZF is set.
        m=self.machine();seed=((0x00420000-1)*pow(22695477,-1,1<<32))&0xFFFFFFFF
        r=m.run('rand',random_seed=seed)
        self.assertEqual(r['registers']['ax'],0x42);self.assertEqual(r['flags']&64,64)
    def test_GRCG_ignores_argument_high_bytes_and_restores_flags_after_CLI(self):
        m=self.machine()
        r=m.run('setcolor',mode=0xFEA5,color=0xFF8A,flags=0xED7,ss=0x8000,stack=0x80)
        self.assertEqual([e[1:4] for e in r['events'] if e[0]=='out'],[(0x7C,1,0xA5),(0x7E,1,0),(0x7E,1,255),(0x7E,1,0),(0x7E,1,255)])
        self.assertTrue(all(e[4]==0 for e in r['events'] if e[0]=='out'))
        self.assertEqual(r['flags']&0x8D5,0xED7&0x8D5);self.assertEqual(r['flags']&0x600,0x600)
        self.assertEqual(r['registers']['ax'],0x08FF);self.assertEqual(r['registers']['sp'],0x88)
    def test_GRCG_off_preserves_AH_and_does_not_disable_IF(self):
        r=self.machine().run('off',seed=0xF3A5)
        self.assertEqual(r['registers']['ax'],0xF300);self.assertEqual(r['events'],[('out',0x7C,1,0,0x200)])
    def test_string_comparison_returns_9F00_for_equality_and_zero_for_mismatch(self):
        m=self.machine()
        for a,b,expected in ((b'AZ\0',b'az\0',0x9F00),(b'\xFF\0',b'\xFF\0',0x9F00),(b'\0',b'\0',0x9F00),(b'[\0',b'{\0',0)):
            r=m.run('compare',strings=(a,b),flags=0xED7)
            self.assertEqual(r['registers']['ax'],expected);self.assertEqual(r['flags']&0x400,0)
    def test_string_far_pointers_wrap_offsets_and_preserve_argument_bytes(self):
        m=self.machine();r=m.run('compare',strings=(b'abC\0',b'ABc\0'),pointers=((0x5000,0xFFFF),(0x6000,0xFFFE)),stack=0x80,ss=0x8000)
        self.assertEqual((r['registers']['bx'],r['registers']['sp'],r['stack_depth']),(3,0x8A,6))
        self.assertEqual(bytes(m.u.mem_read(0x80082,8)),b'\xfe\xff\0\x60\xff\xff\0\x50')
    def test_DOS_request_is_exact_and_reply_registers_are_forwarded(self):
        r=self.machine().run('keyclear',dos_status=0xFFFF,reply_seed=0,flags=0x402)
        self.assertEqual(r['events'][0][1],0x21);self.assertEqual(r['events'][0][2]['ax'],0xC00)
        self.assertEqual(r['registers']['ax'],0xFFFF)
    def test_all_twenty_six_guest_instruction_mutations_fail(self):
        self.assertEqual(negative_controls(self.target)['count'],26)
    @unittest.skipUnless((ROOT/'.analysis/work/mainl-root-helpers-build.json').is_file(),'complete root report absent')
    def test_full_witness_cannot_ignore_stack_or_accept_adjacent_layout(self):
        r=json.loads((ROOT/'.analysis/work/mainl-root-helpers-build.json').read_bytes())
        if not r['complete']:self.skipTest('root report is still running')
        s=r['scope'];witness(s)
        for part,key,value in (('runtime','ignored_stack_bytes',6),('runtime','executed_owner_bytes',153),('layout','containing_producer_accepted',True)):
            bad=deepcopy(s);bad[part][key]=value
            with self.assertRaises(ValueError):witness(bad)

class RootLedger(unittest.TestCase):
    def test_disjoint_partitions_keep_all_old_source_bytes(self):
        with (ROOT/'config/units.csv').open() as stream:units={r['id']:r for r in csv.DictReader(stream)}
        for suffixes,start,total in ((('grcg','grcg-setcolor-align','grcg-off','grcg-off-align'),0xC36,48),
                                     (('compare-align','string-compare'),0x2C2F,57)):
            at=start
            for suffix in suffixes:
                r=units['th03-mainl-decoded-root-tail-'+suffix]
                self.assertEqual(int(r['offset'],0),at);at+=int(r['size'])
                self.assertEqual(r['state'],'source-present')
            self.assertEqual(at,start+total)
    def test_historical_source_caption_requires_every_current_partition(self):
        import progress
        with (ROOT/'config/units.csv').open() as f:units=list(csv.DictReader(f))
        with (ROOT/'config/evidence.csv').open() as f:evidence=list(csv.DictReader(f))
        self.assertTrue(progress.mainl_root_tail_source_proven(units,evidence))
        for suffix in ('grcg-off','grcg-setcolor-align','grcg-off-align','string-compare'):
            self.assertFalse(progress.mainl_root_tail_source_proven([u for u in units if u['id']!='th03-mainl-decoded-root-tail-'+suffix],evidence))
