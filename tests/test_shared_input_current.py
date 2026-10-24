"""Two real products independently bind one complete input producer."""
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
from lib.shared_input_layout import PROFILES,OBJECT,native_image,verify
from lib.shared_input_runtime import Machine,negative_controls
from review_th03_shared_input_work import witness
from test_main_enemy_layout import mutate_record


@unittest.skipUnless(all((ROOT/'.analysis/toolchain/wineprefix/drive_c'/p['folder']/f'bin/th03/{name}.target.exe').is_file() for name,p in PROFILES.items()),'private current OP/MAINL targets absent')
class SharedInput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data={}
        for profile,p in PROFILES.items():
            w=ROOT/'.analysis/toolchain/wineprefix/drive_c'/p['folder']
            cls.data[profile]=(w,parse_mz((w/f'bin/th03/{profile}.target.exe').read_bytes()),parse_mz((w/f'bin/th03/{profile}.exe').read_bytes()))
    def machine(self,profile='op'):
        m=Machine(self.data[profile][1],0x3000,profile);self.addCleanup(m.close);return m
    def test_all_native_fields_and_ordinary_tlink_call_relaxations(self):
        for profile,(work,target,candidate) in self.data.items():
            r=verify(work,target,candidate,profile)
            self.assertEqual((r['functions'],r['code_bytes'],r['private_data_bytes'],r['private_bss_bytes']),(9,367,0,0))
            self.assertEqual(len(r['ordered_native_fields']),58)
            self.assertEqual((len(r['normal_tlink_relaxed_calls']),len(r['ordered_relocations'])),(10,6))
            self.assertTrue(r['native_ownership_reviewed']);self.assertTrue(r['acceptance_requires_current_publication'])
            self.assertFalse(r['whole_product_accepted'])
            self.assertTrue(all(o['canonical_file_offset'] is None for o in r['owners']))
    def test_product_coordinates_cannot_be_interchanged(self):
        work,target,candidate=self.data['op']
        with self.assertRaisesRegex(ValueError,'complete naturally resolved'):verify(work,target,candidate,'mainl')
    def test_complete_native_symbolic_external_order_is_required(self):
        raw=(self.data['op'][0]/OBJECT).read_bytes()
        changed=mutate_record(raw,lambda r:r.name=='EXTDEF',lambda d:d.replace(b'_js_bexist',b'_js_bexisX'))
        with self.assertRaisesRegex(ValueError,'symbolic external order'):native_image(changed,'op')
    def test_high_byte_input_tests_have_real_nonzero_omf_addends(self):
        raw=(self.data['op'][0]/OBJECT).read_bytes()
        def change(d):
            value=bytearray(d);self.assertEqual(value[3+211],1);value[3+211]=0;return bytes(value)
        changed=mutate_record(raw,lambda r:r.name=='LEDATA',change)
        with self.assertRaisesRegex(ValueError,'literal native external addend'):native_image(changed,'op')
    def test_map_owner_and_both_public_tables_are_not_optional(self):
        work,target,candidate=self.data['op']
        with TemporaryDirectory() as folder:
            temporary=Path(folder);shutil.copytree(work/'obj',temporary/'obj');shutil.copytree(work/'th03',temporary/'th03')
            path=temporary/'obj/th03/op.map';path.write_text(path.read_text().replace('M=th03/inp_m_w.cpp ACBP=28','M=th03/unknown.cpp ACBP=28',1))
            with self.assertRaisesRegex(ValueError,'literal MAP allocation'):verify(temporary,target,candidate,'op')
    def test_input_presence_is_a_word_and_merge_preserves_all_bits(self):
        for profile in PROFILES:
            m=self.machine(profile)
            for present in (0,0x8000,0xFFFF):
                row=m.run('input_mode_interface',present=present,sample=(0x8000,0x20,0x400,0x4000),flags=0xED7)
                self.assertEqual(row['states']['single'],0xC020 if present else 0x8020)
                self.assertEqual(row['service_calls'],2 if present else 1)
    def test_joystick_modes_keep_p1_p2_assignment_order(self):
        m=self.machine()
        for kind,p1,p2 in [('input_mode_joy_vs_key',0x4567,0x1234),('input_mode_key_vs_joy',0x1234,0x4567)]:
            r=m.run(kind,sample=(0x1234,0x10,0x20,0x4567));self.assertEqual((r['states']['player1'],r['states']['player2']),(p1,p2))
    def test_cpu_mode_tests_only_the_ok_cancel_bits_and_keeps_other_sp_bits(self):
        m=self.machine()
        for sp,wanted in ((0x800,0x800),(0x1001,0x1000),(0x2002,0x1000),(0xC004,0xC004)):
            r=m.run('input_mode_cpu_vs_cpu',sample=(sp,0xFFFF,0xFFFF,0xFFFF),flags=0xED7)
            self.assertEqual(r['states']['single'],wanted);self.assertEqual((r['states']['player1'],r['states']['player2']),(0,0))
    def test_release_is_not_limited_by_negative_press_timeout(self):
        m=self.machine();r=m.run('input_wait_for_change',frames=0xFFFF,samples=[(1,0,0,0)]*4+[(0,0,0,0)])
        self.assertEqual((r['sample_polls'],r['service_calls']),(5,14))
        self.assertEqual(m.r('sp'),0xF806)
    def test_finite_wait_timeout_counts_only_press_phase(self):
        m=self.machine();r=m.run('input_wait_for_change',frames=2,samples=[(1,0,0,0)]*3+[(0,0,0,0)]*3)
        self.assertEqual(r['sample_polls'],6);self.assertEqual(r['states']['single'],0)
    def test_both_products_reject_nineteen_instruction_mutations(self):
        for profile,(_,target,_) in self.data.items():self.assertEqual(negative_controls(target,profile)['count'],19)
    @unittest.skipUnless((ROOT/'.analysis/work/shared-input-build.json').is_file(),'current full shared input witness absent')
    def test_partial_domain_or_wrong_load_cannot_inherit_full_witness(self):
        report=json.loads((ROOT/'.analysis/work/shared-input-build.json').read_text())
        scope=deepcopy(report['profiles']['op']);scope['runtime']['observations'][1]['load_segment']=0x1000
        with self.assertRaisesRegex(ValueError,'coverage/wait/stack'):witness(scope)
        scope=deepcopy(report['profiles']['op']);scope['runtime']['executed_owner_bytes']=366
        with self.assertRaisesRegex(ValueError,'runtime dimensions'):witness(scope)
