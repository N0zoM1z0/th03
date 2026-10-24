"""Independent OP addresses, file protocol, counter ABI and acceptance bounds."""
from copy import deepcopy
from pathlib import Path
import json,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from lib.op_sound_layout import verify,RUNTIME_FIELDS as F
from lib.op_sound_runtime import Machine,negative_controls
from review_th03_op_cfg_work import images
from review_th03_op_sound_work import witness
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP'

@unittest.skipUnless((WORK/'bin/th03/op.exe').is_file(),'private current OP absent')
class Sound(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.work,cls.target,cls.candidate,*_=images(ROOT)
    def machine(self):
        m=Machine(self.target,0x3000);self.addCleanup(m.close);return m
    def test_complete_native_producers_and_literal_external_fields(self):
        r=verify(self.work,self.target,self.candidate)
        self.assertEqual((r['functions'],r['code_bytes'],sum(len(o['fields']) for o in r['native_objects'])),(2,133,10))
        self.assertEqual(r['ordered_relocations'],[])
        self.assertEqual([o['callee_pop_bytes'] for o in r['owners']],[0,2])
        self.assertTrue(all(o['canonical_file_offset'] is None for o in r['owners']))
        self.assertFalse(r['whole_product_accepted'])
    def test_OP_buffer_handles_far_offset_wrap_and_suffix_overflow(self):
        m=self.machine();name=b'\0'+b'Q'*12
        m.run('load',filename=name,filename_offset=0xFFFF,midi=2,suffix_end=32)
        self.assertEqual(bytes(m.uc.mem_read(m.data+F['load_fn'],13)),name)
        self.assertEqual(bytes(m.uc.mem_read(m.data+F['load_fn']+32,3)),b'md\0')
    def test_failed_open_still_reads_and_closes_with_original_DS(self):
        m=self.machine();r=m.run('load',midi=255,open_failure=True,open_result=5,read_failure=True,read_result=6)
        self.assertEqual((r['driver_calls'],r['registers']['ds'],m.r('sp')),(1,m.ds,0xF804))
        self.assertEqual(r['registers']['ax'],0xBEEF)
    def test_counter_limit_is_unsigned_and_pascal_pops_only_argument(self):
        m=self.machine();r=m.run('frame_delay',frames=0x8000,ticks=(0x7FFF,0x8000),flags=0xED7)
        self.assertEqual((r['registers']['ax'],r['counter_updates'],m.r('sp'),r['flags']&0x600),(0x8000,2,0xF806,0x600))
        self.assertEqual(bytes(m.uc.mem_read(m.data+F['counter'],2)),b'\0\x80')
    def test_fourteen_literal_guest_mutations_fail(self):
        self.assertEqual(negative_controls(self.target)['count'],14)
    @unittest.skipUnless((ROOT/'.analysis/work/op-sound-build.json').is_file(),'OP sound report absent')
    def test_partial_MIDI_domain_and_stack_witness_are_rejected(self):
        s=json.loads((ROOT/'.analysis/work/op-sound-build.json').read_bytes())['scope']
        bad=deepcopy(s);bad['runtime']['exhaustive_MIDI_bytes']=255
        with self.assertRaisesRegex(ValueError,'runtime dimensions'):witness(bad)
        bad=deepcopy(s);bad['runtime']['observations'][0]['maximum_observed_stack_depth']=4
        with self.assertRaisesRegex(ValueError,'load/state/stack'):witness(bad)
