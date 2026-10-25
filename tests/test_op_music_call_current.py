"""Natural far-call ownership boundary, full ABI and explicit live source staging."""
from pathlib import Path
from dataclasses import replace
import hashlib,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_op_cfg_work import images
from lib.op_music_call import SITE,layout,runtime,negative_controls
from lib.op_current_source import payload,LIVE_SOURCES
import stage_th03_op_fullcold as historical
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP'

@unittest.skipUnless((WORK/'bin/th03/op.exe').is_file(),'current OP native pair absent')
class MusicCallCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.work,cls.target,cls.candidate,*_=images(ROOT)
    def test_native_far_field_and_linker_relaxation_add_no_source_credit(self):
        r=layout(ROOT,self.work,self.target,self.candidate)
        self.assertEqual(r['native_field'],[2221,4,0xCC,0x16,1,14])
        self.assertEqual(r['linked_instruction_kinds'],['nop','push cs','near call'])
        self.assertFalse(r['source_acceptance']);self.assertFalse(r['enclosing_menu_accepted']);self.assertFalse(r['callee_implementation_executed'])
    def test_equal_mutated_linked_images_cannot_hide_native_call_mismatch(self):
        raw=bytearray(self.target.program_image);raw[SITE+1]=0x1E
        bad=replace(self.target,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'actual TLINK'):layout(ROOT,self.work,bad,bad)
    def test_every_memory_byte_and_register_survive_the_real_four_byte_frame(self):
        r=runtime(self.target,self.candidate)
        self.assertEqual(r['cases_per_image'],192)
        self.assertEqual([(o['cases'],o['maximum_stack_depth'],o['ignored_stack_bytes']) for o in r['observations']],[(96,4,0),(96,4,0)])
        self.assertFalse(r['callee_implementation_executed'])
    def test_actual_instruction_controls_reject_flag_segment_and_target_changes(self):
        r=negative_controls(self.target);self.assertEqual(r['actual_instruction_mutations'],3)
        self.assertFalse(r['source_or_stored_product_modified'])
    def test_historical_pin_stays_fixed_while_the_current_source_reaches_staging(self):
        before=set((ROOT/'.analysis').glob('OP-source-read-*'));files=payload(ROOT)
        self.assertEqual(LIVE_SOURCES,('src/op/menu/menu_state.inl',))
        name=LIVE_SOURCES[0];self.assertEqual(files[name],(ROOT/name).read_bytes())
        self.assertNotEqual(hashlib.sha256(files[name]).hexdigest(),historical.INPUT_HASHES[name])
        self.assertEqual(historical.INPUT_HASHES[name],'d5717cb7effea171092eb6d4ad5ee561dd9e9b9f8269880212d0295603bdb52d')
        self.assertEqual(set((ROOT/'.analysis').glob('OP-source-read-*')),before)
