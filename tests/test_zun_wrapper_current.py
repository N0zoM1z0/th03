"""Whole native wrapper ownership, independent PSP/FCB semantics and hard stops."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.zun_wrapper_layout import native, verify
from lib.zun_wrapper_runtime import Machine, negative_controls
from review_th03_zun_format_work import images
from review_th03_zun_wrapper_work import witness
from test_main_enemy_layout import mutate_record

WORK = ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ZUN'


@unittest.skipUnless((WORK/'product/zun.target.com').is_file(),'private current wrapper absent')
class Wrapper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image = (WORK/'product/zun.target.com').read_bytes()

    def machine(self,split=False):
        m = Machine(self.image,0x3000,split)
        self.addCleanup(m.close)
        return m

    def test_complete_whole_TUs_and_outer_coordinates_exclude_directory_and_payloads(self):
        work,_,_,_,files,maintained,cold = images(ROOT)
        r = verify(work,self.image,(work/'product/zun.com').read_bytes(),files,maintained)
        self.assertEqual((r['functions'],r['code_bytes'],r['data_bytes']),(3,213,21))
        self.assertEqual(len(r['ordered_native_fixups']),9)
        self.assertEqual(r['directory_bytes_excluded'],324)
        self.assertFalse(r['payloads_owned']);self.assertFalse(r['enclosing_product_accepted'])
        for o in r['owners']:
            self.assertEqual(o['coordinate_space'],'decoded-launcher-com')
            self.assertEqual(o['decoded_file_offset'],o['start']-256)
            self.assertIsNone(o['payload_option']);self.assertIsNone(o['canonical_file_offset'])

    def test_ordinary_MAP_alignment_and_native_group_frame_cannot_be_changed(self):
        obj = (WORK/'wrapper/stub.obj').read_bytes()
        linked = (WORK/'wrapper/stub.com').read_bytes()
        map_raw = (WORK/'wrapper/stub.map').read_bytes()
        with self.assertRaises(ValueError):
            native(obj,linked,map_raw.replace(b'ACBP=48',b'ACBP=68',1),'stub')
        changed = mutate_record(obj,lambda r:r.name == 'FIXUPP',lambda d:d[:3]+b'\x02'+d[4:])
        with self.assertRaisesRegex(ValueError,'group frame'):
            native(changed,linked,map_raw,'stub')

    def test_FCB_selects_payload_independently_of_selector_text_and_leaves_count(self):
        m = self.machine(True)
        r = m.run(command=b'  -5 hello',fcb=b'-2')
        self.assertEqual((r['outcome'],r['copied_bytes'],r['registers']['sp']),('payload-entry',1390,0xFFFC))
        self.assertEqual(m.uc.mem_read(m.base+0x5C,16),b'0123456789ABCDEF')
        self.assertEqual(m.uc.mem_read(m.base+0x80,8),b'\x06 hello\r')
        self.assertEqual(m.uc.mem_read(0x80000+0xFFFC,2),b'\x04\0')

    def test_DOS_AL_replies_determine_unmasked_exit_status(self):
        m = self.machine()
        listings = [m.run(reply=i)['terminal_AX'] for i in range(3)]
        errors = [m.run(command=b' -X',fcb=b'-X',reply=i)['terminal_AX'] for i in range(3)]
        self.assertEqual(listings,[0x4C20,0x4C0A,0x4CA7])
        self.assertEqual(errors,[0x4C2D,0x4C24,0x4CA7])

    def test_zero_PSP_length_lists_even_with_nonempty_command_and_matching_FCB(self):
        m = self.machine()
        r = m.run(command=b' -2 ignored',fcb=b'-2',length=0)
        self.assertEqual(r['outcome'],'dos-exit')
        self.assertEqual(r['copied_bytes'],0)

    def test_full_eight_byte_FCB_comparison_rejects_nonspace_suffix(self):
        m = self.machine()
        r = m.run(command=b'-1',fcb=b'-1 X')
        self.assertEqual(r['outcome'],'dos-exit')
        self.assertEqual(bytes(m.output),b'No COM-Soft !!!\r\n\n')

    def test_helper_discards_return_and_wraps_SP_without_payload_execution(self):
        m = self.machine(True)
        r = m.run('helper',size=0,flags=0x202)
        self.assertEqual((r['registers']['sp'],r['registers']['ax'],r['copied_bytes']),(0,0x100,0))
        self.assertEqual(m.uc.mem_read(0x80000+0xFFFE,2),b'\0\x01')
        self.assertEqual(r['flags'],0x202)
        with self.assertRaisesRegex(ValueError,'forward direction'):
            m.run('helper',size=0,flags=0x602)

    def test_all_21_actual_instruction_mutations_are_rejected(self):
        self.assertEqual(negative_controls(self.image)['count'],21)

    @unittest.skipUnless((ROOT/'.analysis/work/zun-wrapper-build.json').is_file(),'full wrapper witness absent')
    def test_partial_model_or_payload_execution_cannot_borrow_wrapper_witness(self):
        scope = json.loads((ROOT/'.analysis/work/zun-wrapper-build.json').read_bytes())['scope']
        for key,value in (('cases_per_image',14),('payload_instructions_executed',True),('stack_windows_ignored',True)):
            changed = deepcopy(scope)
            changed['runtime'][key] = value
            with self.assertRaises(ValueError):
                witness(changed)
