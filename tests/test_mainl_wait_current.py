"""Full ending wait ownership and target-specific AX/timer semantics."""
from copy import deepcopy
from pathlib import Path
import json
import shutil
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.pc98 import parse_mz
from lib.mainl_wait_layout import verify,native_image,OBJECT
from lib.mainl_wait_runtime import Machine,negative_controls
from review_th03_shared_input_work import wait_witness
from test_main_enemy_layout import mutate_record

WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/'bin/th03/mainl.target.exe').is_file(),'private current MAINL target absent')
class EndingWait(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target=parse_mz((WORK/'bin/th03/mainl.target.exe').read_bytes());cls.candidate=parse_mz((WORK/'bin/th03/mainl.exe').read_bytes())
    def machine(self):
        m=Machine(self.target,0x3000);self.addCleanup(m.close);return m
    def test_two_whole_procedures_resolve_all_native_fields(self):
        r=verify(WORK,self.target,self.candidate)
        self.assertEqual((r['functions'],r['code_bytes'],r['private_data_bytes'],r['private_bss_bytes']),(2,126,0,0))
        self.assertEqual(len(r['ordered_native_fields']),11)
        self.assertEqual(len(r['normal_tlink_relaxed_calls']),3)
        self.assertEqual(r['ordered_relocations'],[])
        self.assertEqual([o['callee_pop_bytes'] for o in r['owners']],[4,2])
        self.assertTrue(all(o['canonical_file_offset'] is None for o in r['owners']))
    def test_native_high_byte_addends_cannot_be_normalized_away(self):
        raw=(WORK/OBJECT).read_bytes()
        def change(d):
            value=bytearray(d);self.assertEqual(value[3+54],1);value[3+54]=0;return bytes(value)
        changed=mutate_record(raw,lambda r:r.name=='LEDATA',change)
        with self.assertRaisesRegex(ValueError,'eleven ordered fields'):native_image(changed)
    def test_both_map_tables_bind_the_real_sound_flag_address(self):
        with TemporaryDirectory() as folder:
            work=Path(folder);shutil.copytree(WORK/'obj',work/'obj');shutil.copytree(WORK/'th03',work/'th03')
            path=work/'obj/th03/mainl.map';original=path.read_text();changed=original.replace('0E3F:0880','0E3F:0881',1)
            self.assertNotEqual(original,changed);path.write_text(changed)
            with self.assertRaisesRegex(ValueError,'external MAP tables'):verify(work,self.target,self.candidate)
    def test_music_query_AX_is_replaced_by_real_player1_input(self):
        m=self.machine();zero=(0,0,0,0,0)
        row=m.run('input_wait_for_ok_or_measure',measure=0x100,samples=[zero,(0,0x100,0,0,0)],replies=[0xFFFF,0xFFFF])
        self.assertEqual((row['registers']['ax'],row['polls'],row['sound_queries']),(0,2,2))
        row=m.run('input_wait_for_ok_or_measure',measure=0x100,samples=[(0,0x4000,0,0,0)],replies=[0])
        self.assertEqual((row['registers']['ax'],row['polls']),(0,1))
    def test_measure_comparison_is_unsigned_despite_signed_parameter(self):
        row=self.machine().run('input_wait_for_ok_or_measure',measure=0x8000,samples=[(0,0x4000,0,0,0),(0,0x8000,0,0,0)])
        self.assertEqual((row['registers']['ax'],row['polls']),(0,2))
    def test_inactive_music_uses_frame_fallback_and_four_byte_cleanup(self):
        m=self.machine();row=m.run('input_wait_for_ok_or_measure',active=0,frames=0,measure=0xFFFF,samples=[(0,0,0,0,0)],flags=0xED7)
        self.assertEqual((row['registers']['ax'],row['polls'],row['sound_queries']),(0,1,0))
        self.assertEqual(m.r('sp'),0xF808)
    def test_MIDI_selector_is_exactly_byte_one_and_uses_command_port(self):
        m=self.machine()
        for value,vector in ((0,0x60),(1,0x61),(2,0x60),(0xFF,0x60)):
            m.run('input_wait_for_ok_or_measure',measure=0,midi=value,samples=[(0,0,0,0,0)])
            event=next(e for e in m.expected.events if e[0]=='interrupt')
            self.assertEqual((event[1],event[2]>>8),(vector,5));self.assertEqual(event[3],0xC0 if vector==0x61 else None)
    def test_unsigned_irq_counter_wrap_and_zero_frame_poll(self):
        m=self.machine();zero=(0,0,0,0,0)
        row=m.run('input_wait_for_ok',frames=0,samples=[zero]);self.assertEqual((row['polls'],row['counter']),(1,0))
        row=m.run('input_wait_for_ok',frames=0xFFFF,samples=[(0,0,0,0,0xFFFE),zero,(0,0,0,0,0xFFFF)])
        self.assertEqual((row['polls'],row['counter'],m.r('sp')),(3,0xFFFF,0xF806))
    def test_shot_or_OK_return_exact_BOOL16_one_before_timeout(self):
        for kind in ('input_wait_for_ok','input_wait_for_ok_or_measure'):
            for bit in (0x20,0x2000):
                row=self.machine().run(kind,frames=0,samples=[(bit,0,0,0,0)],flags=0xED7)
                self.assertEqual(row['registers']['ax'],1)
    def test_eighteen_real_guest_mutations_fail(self):
        self.assertEqual(negative_controls(self.target)['count'],18)
    @unittest.skipUnless((ROOT/'.analysis/work/shared-input-build.json').is_file(),'current full wait witness absent')
    def test_partial_wait_coverage_cannot_inherit_the_input_witness(self):
        scope=deepcopy(json.loads((ROOT/'.analysis/work/shared-input-build.json').read_text())['profiles']['mainl']['ending_wait'])
        scope['runtime']['executed_owner_bytes']=125
        with self.assertRaisesRegex(ValueError,'ending wait runtime dimensions'):wait_witness(scope)
