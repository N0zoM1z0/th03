"""Native staff drawing ownership, unchecked WORD inputs and caller effects."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import struct
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_sound_work import images
from review_th03_mainl_staff_draw_work import REPORT, witness
from lib.decoded_mainl_staff_draw_layout import verify, native_image, CS, OBJECT
from lib.decoded_mainl_staff_draw_runtime import Machine, geometry_proof, ARITH
from test_main_enemy_layout import mutate_record

WORK = ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class StaffDrawCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files = images(ROOT)

    def machine(self,image=None,load=0x3000):
        m = Machine(image or self.target,load)
        self.addCleanup(m.close)
        return m

    def blue_zero(self,m):
        raw = bytearray(m.initial)
        raw[0xA8000:0xB8002] = b'\0'*65538
        m.initial = bytes(raw)

    def graph_events(self,m,base):
        return [e for e in m.events if e[0]=='store' and base<=e[1]<base+65538]

    def test_complete_two_procedures_and_separate_enclosing_DATA(self):
        r = verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((r['functions'],r['code_bytes'],len(r['ordered_native_fields']),r['mz_relocation_count']),(2,199,3,0))
        self.assertEqual((r['enclosing_CODE_bytes'],r['enclosing_initialized_DATA_bytes'],r['enclosing_procedures']),(3695,224,19))
        self.assertFalse(r['enclosing_DATA_or_other_functions_accepted'])
        self.assertFalse(r['sprite_assets_or_physical_graphics_accepted'])

    def test_equal_corruption_in_both_images_cannot_substitute_native_bytes(self):
        def changed(image):
            raw = bytearray(image.program_image)
            raw[CS*16+0x24E3] ^= 1
            return replace(image,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'independently linked native drawing bodies'):
            verify(self.work,changed(self.target),changed(self.candidate),self.graph,self.files)

    def test_ordered_native_member_fields_are_not_a_set(self):
        first,second = bytes.fromhex('c57f16021f'),bytes.fromhex('c57216021f')
        raw = (self.work/OBJECT).read_bytes()
        changed = mutate_record(raw,lambda r:r.name=='FIXUPP' and first in r.data and second in r.data,
            lambda data:data.replace(first,b'\xFE'*5,1).replace(second,first,1).replace(b'\xFE'*5,second,1))
        with self.assertRaisesRegex(ValueError,'literal ordered fields'):
            native_image(changed)

    def test_empty_MZ_vector_is_actually_checked(self):
        extra = replace(self.target.relocations[0],segment=CS,offset=0x24BF)
        changed = replace(self.target,relocations=(*self.target.relocations,extra))
        with self.assertRaisesRegex(ValueError,'empty ordered MZ'):
            verify(self.work,changed,self.candidate,self.graph,self.files)

    def test_flake_rotates_WORD_right_and_ORs_eight_unclipped_rows(self):
        m = self.machine()
        self.blue_zero(m)
        r = m.run('flake',left=1,top=0,source_word=1)
        for row in range(8):
            self.assertEqual(bytes(m.u.mem_read(0xA8000+row*80,2)),b'\0\x80')
        self.assertEqual((r['graph_WORD_stores'],r['stack_depth'],r['registers']['ax']&65535),(8,6,0x8000))

    def test_flake_cel_WORD_is_unchecked_and_aliases_every_4096_values(self):
        m = self.machine()
        a = m.run('flake',index=0)
        first = bytes(m.u.mem_read(0xA8000,65538))
        b = m.run('flake',index=0x1000)
        self.assertEqual(bytes(m.u.mem_read(0xA8000,65538)),first)
        self.assertEqual(a['registers'],b['registers'])
        m.run('flake',index=4)
        self.assertNotEqual(bytes(m.u.mem_read(0xA8000,65538)),first)

    def test_flake_final_DEC_flags_include_inherited_source_advance_CF(self):
        m = self.machine()
        for index in (0,0xF59,0xFFF,0xFFFF):
            r = m.run('flake',index=index,left=0xFFFF,flags=0xED7)
            self.assertEqual(r['flags']&ARITH,0x44)
            self.assertEqual(r['flags']&0x600,0x600)

    def test_unput_writes_the_actual_caller_coordinate_argument_words(self):
        m = self.machine()
        r = m.run('unput',left=320,top=200,width=32,height=16,stack=0x80)
        self.assertEqual(struct.unpack('<4H',bytes(m.u.mem_read(0x70080,8))),(0xFFFF,0,206,304))
        self.assertEqual((r['registers']['sp']&65535,r['stack_depth']),(0x88,10))

    def test_unput_DF_set_changes_the_row_recurrence(self):
        m = self.machine()
        m.run('unput',left=16,top=2,width=32,height=0,flags=0x202)
        self.assertEqual([e[1]-0xE0000 for e in self.graph_events(m,0xE0000)],[0,2,80,82,160,162])
        m.run('unput',left=16,top=2,width=32,height=0,flags=0x402)
        self.assertEqual([e[1]-0xE0000 for e in self.graph_events(m,0xE0000)],[0,0xFFFE,72,70,144,142])

    def test_negative_width_uses_signed_half_but_unsigned_store_count(self):
        m = self.machine()
        r = m.run('unput',width=0x8001,height=0,top=2,left=0,stack=0x80)
        self.assertEqual(r['registers']['dx']&65535,2048)
        self.assertEqual(r['graph_WORD_stores'],6144)
        self.assertEqual(int.from_bytes(m.u.mem_read(0x70086,2),'little'),16383)

    def test_zero_REP_count_still_updates_parameters_and_executes_three_rows(self):
        m = self.machine()
        r = m.run('unput',left=0,top=0,width=15,height=0,stack=0x80)
        self.assertEqual(r['graph_WORD_stores'],0)
        self.assertEqual(struct.unpack('<4H',bytes(m.u.mem_read(0x70080,8))),(0xFFFF,0,0xFFFE,0xFFF9))
        self.assertEqual(r['registers']['sp']&65535,0x88)

    def test_maximum_unchecked_width_is_finite_without_instruction_skipping(self):
        m = self.machine()
        r = m.run('unput',width=0xFFFF,height=0xFFFF,flags=0xED7)
        self.assertEqual((r['graph_WORD_stores'],r['registers']['dx']&65535),(12285,4095))

    def test_WORD_at_FFFF_spans_physical_bytes_in_both_images_and_loads(self):
        for image in (self.target,self.candidate):
            for load in (0x1000,0x3000):
                m = self.machine(image,load)
                self.blue_zero(m)
                m.run('flake',left=0xFFFF,top=0,source_word=1)
                self.assertEqual(bytes(m.u.mem_read(0xB7FFF,2)),b'\0\x02')
                self.assertEqual(bytes(m.u.mem_read(0xA8000,1)),b'\0')
                m.run('unput',left=15,top=2,width=32,height=0)
                self.assertEqual(self.graph_events(m,0xE0000)[:2],[('store',0xEFFFF,2,0),('store',0xE0001,2,0)])
                self.assertEqual(bytes(m.u.mem_read(0xF0000,1)),b'\0')
                self.assertEqual(bytes(m.u.mem_read(0xE0000,1)),b'\xA5')

    def test_foreign_SS_full_high_halves_and_FS_GS_are_preserved(self):
        m = self.machine()
        for kind in ('flake','unput'):
            r = m.run(kind,ss=0x8000,stack=0x80,seed=0xECA8,flags=0xED7)
            self.assertEqual((r['registers']['ss'],r['registers']['sp']&65535),(0x8000,0x88))
            self.assertEqual((r['registers']['fs'],r['registers']['gs'],r['registers']['ds']),(0x3456,0x4567,m.ds))
            self.assertTrue(all(r['registers'][n]>>16==0xECA8^0x5AA5 for n in ('ax','bx','cx','dx','si','di','bp','sp')))

    def test_persistent_reentry_observes_existing_VRAM(self):
        m = self.machine()
        self.blue_zero(m)
        m.run('flake',left=0,top=0,source_word=1)
        m.run('flake',left=1,top=0,source_word=1,persistent=True)
        self.assertEqual(bytes(m.u.mem_read(0xA8000,2)),b'\x01\x80')

    def test_native_arithmetic_proof_rechecks_changed_opcode(self):
        proof = geometry_proof(self.target)
        self.assertEqual((proof['distinct_flake_source_offsets'],proof['maximum_unput_WORD_stores']),(4096,12285))
        raw = bytearray(self.target.program_image)
        raw[CS*16+0x2541] ^= 1
        with self.assertRaisesRegex(ValueError,'native index / count / row recurrence'):
            geometry_proof(replace(self.target,program_image=bytes(raw)))

    @unittest.skipUnless(REPORT.is_file(),'complete staff drawing witness absent')
    def test_witness_rejects_ignored_caller_bytes_and_unowned_DATA_credit(self):
        report = json.loads(REPORT.read_bytes())
        if not report['complete']:
            self.skipTest('staff drawing review running')
        scope = report['scope']
        witness(scope)
        for part,key,value in (('runtime','ignored_stack_bytes',16),('runtime','caller_argument_stores_checked',False),
                ('runtime','executed_owner_bytes',198),('runtime','sprite_assets_or_physical_graphics_owned',True),
                ('layout','enclosing_DATA_or_other_functions_accepted',True),('layout','mz_relocation_count',1),
                ('negative_controls','count',36)):
            bad = deepcopy(scope)
            bad[part][key] = value
            with self.assertRaises(ValueError):
                witness(bad)
