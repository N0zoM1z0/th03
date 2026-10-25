"""Complete CDG blitters: live SMC, real color setup and bounded bus effects."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_sound_work import images
from review_th03_mainl_cdg_draw_work import REPORT, witness, ZERO
from lib.decoded_mainl_cdg_draw_layout import verify, CS, ENTRIES, PATCHES
from lib.decoded_mainl_cdg_draw_runtime import Machine, geometry_proof

WORK = ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class CDGDrawCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files = images(ROOT)

    def machine(self):
        m = Machine(self.target,0x3000)
        self.addCleanup(m.close)
        return m

    def changed(self,image,offset):
        raw = bytearray(image.program_image)
        raw[CS*16+offset] ^= 1
        return replace(image,program_image=bytes(raw))

    def test_whole_native_producers_separate_three_outer_EVEN_bytes(self):
        r = verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((r['functions'],r['code_bytes'],r['natural_producer_bytes']),(3,493,496))
        self.assertEqual((r['ordered_native_field_count'],r['mz_relocation_count'],r['self_modifying_WORDs']),(19,2,12))
        self.assertEqual(r['excluded_outer_EVEN_bytes'],[0x2A7,0x371,0xFA3])
        self.assertFalse(r['enclosing_alignment_accepted'])

    def test_equal_corruption_in_both_images_fails_native_producer(self):
        with self.assertRaisesRegex(ValueError,'independently resolved native producer'):
            verify(self.work,self.changed(self.target,0x259),self.changed(self.candidate,0x259),self.graph,self.files)

    def test_outer_EVEN_is_checked_without_function_credit(self):
        with self.assertRaisesRegex(ValueError,'independently resolved native producer'):
            verify(self.work,self.changed(self.target,0x2A7),self.changed(self.candidate,0x2A7),self.graph,self.files)

    def test_duplicate_MZ_field_is_rejected(self):
        field, = [r for r in self.target.relocations if r.linear==CS*16+0x202]
        changed = replace(self.target,relocations=(*self.target.relocations,field))
        with self.assertRaisesRegex(ValueError,'literal ordered MZ'):
            verify(self.work,changed,self.candidate,self.graph,self.files)

    def test_real_color_setup_disables_interrupts_and_restores_IF(self):
        m = self.machine()
        r = m.run('alpha',flags=0xED7)
        ports = [e for e in m.events if e[0]=='out']
        self.assertEqual((r['actual_color_calls'],r['ports'],r['stack_depth']),(1,6,16))
        self.assertEqual([e[4] for e in ports],[0]*5+[0x200])
        self.assertEqual([e[1] for e in ports],[0x7C]+[0x7E]*4+[0x7C])
        self.assertTrue(any(e[0]=='color-entry' and len(bytes.fromhex(e[2]))==8 for e in m.events))

    def test_alpha_flat_bus_OR_and_last_DWORD_high_half(self):
        m = self.machine()
        r = m.run('alpha')
        self.assertEqual(bytes(m.u.mem_read(0xA8000,4)),bytes.fromhex('5764b1be'))
        self.assertEqual(r['registers']['ax']&0xFFFF0000,0xFADD0000)

    def test_hflip_consumes_external_LUT_and_returns_color_FS(self):
        m = self.machine()
        r = m.run('hflip',source_byte=1)
        self.assertEqual(bytes(m.u.mem_read(0xA8000,4)),b'\x80'*4)
        self.assertEqual(r['registers']['fs'],0x6000)
        m.run('hflip',source_byte=1,lookup='identity')
        self.assertEqual(bytes(m.u.mem_read(0xA8000,4)),b'\x01'*4)

    def test_DF_and_segment_effects_follow_each_procedure(self):
        m = self.machine()
        for kind in ENTRIES:
            r = m.run(kind,flags=0xED7)
            self.assertEqual(r['flags']&0x400,0x400 if kind=='hflip' else 0)
            self.assertEqual((r['registers']['ds'],r['registers']['gs']),(m.ds,0x4567))
            self.assertEqual(r['registers']['fs'],0x6000 if kind=='hflip' else 0x4444)
            if kind!='alpha':
                self.assertEqual(r['registers']['ax']>>16,0x1357^0x5AA5)

    def test_SMC_writes_real_immediates_and_changes_on_persistent_reentry(self):
        m = self.machine()
        for kind in ENTRIES:
            m.run(kind,width=1)
            r = m.run(kind,width=2,bottom=80,persistent=True)
            self.assertEqual(r['summary']['SMC_WORD_writes'],len(PATCHES[kind]))
            start = m.cs*16+ENTRIES[kind][0]
            widths = {'alpha':(2,3,2),'hflip':(2,3,8),'noalpha':(0,0,2)}
            first,last,value = widths[kind]
            for relative in PATCHES[kind][first:last+1]:
                self.assertEqual(int.from_bytes(m.u.mem_read(start+relative,2),'little'),value)

    def test_noalpha_zero_REP_still_traverses_planes_without_ports(self):
        m = self.machine()
        r = m.run('noalpha',width=0,flags=0xED7)
        self.assertEqual(r['summary'],ZERO['noalpha'])
        self.assertEqual((r['ports'],r['actual_color_calls'],r['stack_depth']),(0,0,8))

    def test_foreign_SS_and_short_stack_keep_complete_return_frame(self):
        m = self.machine()
        for kind in ENTRIES:
            r = m.run(kind,ss=0x8000,stack=0x80,flags=2)
            self.assertEqual((r['registers']['ss'],r['registers']['sp']&65535),(0x8000,0x8A))

    def test_cached_arithmetic_never_hides_changed_native_stride(self):
        p = geometry_proof(self.target)
        self.assertEqual((p['maximum_rows_per_plane'],p['maximum_color_planes']),(411,26))
        self.assertEqual((p['LOOP_zero_counter_iterations'],p['REP_zero_counter_iterations']),(65536,0))
        with self.assertRaisesRegex(ValueError,'native REP/LOOP'):
            geometry_proof(self.changed(self.target,0x233))

    @unittest.skipUnless(REPORT.is_file(),'complete CDG draw report absent')
    def test_witness_binds_complete_zero_LOOPS_and_refuses_expanded_credit(self):
        report = json.loads(REPORT.read_bytes())
        if not report['complete']:
            self.skipTest('CDG draw review running')
        scope = report['scope']
        witness(scope)
        self.assertEqual(scope['runtime']['observations'][0]['zero_width_terminal_summaries'],ZERO)
        for part,key,value in (('runtime','ignored_stack_bytes',16),('runtime','executed_owner_bytes',492),
                ('runtime','physical_GRCG_or_pixels_emulated',True),('runtime','external_LUT_owned',True),
                ('layout','enclosing_alignment_accepted',True),('negative_controls','count',58)):
            bad = deepcopy(scope)
            bad[part][key] = value
            with self.assertRaises(ValueError):
                witness(bad)
        bad = deepcopy(scope)
        bad['runtime']['native_geometry_proof']['nonterminal_claim'] = True
        with self.assertRaises(ValueError):
            witness(bad)
