"""Renderer ABI/state and complete inline-data ownership, independent of pixels."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import csv,json,struct,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from lib.op_render_layout import verify,BRANCHES
from lib.op_render_runtime import Machine,negative_controls
from review_th03_op_cfg_work import images
from review_th03_op_render_work import witness
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP'
@unittest.skipUnless((WORK/'bin/th03/op.exe').is_file(),'private current OP absent')
class Renderers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.work,cls.target,cls.candidate,*_=images(ROOT)
    def machine(self):
        m=Machine(self.target,0x3000);self.addCleanup(m.close);return m
    def test_whole_renderers_include_nine_non_instruction_bytes(self):
        r=verify(self.work,self.target,self.candidate)
        self.assertEqual((r['functions'],r['code_bytes'],r['instruction_bytes'],r['inline_non_instruction_bytes']),(3,518,509,9))
        self.assertEqual((len(r['ordered_native_fields']),len(r['ordered_relocations']),r['reviewed_initialized_dependency_bytes']),(39,7,169))
        self.assertEqual(r['switch_table_targets'],list(BRANCHES));self.assertFalse(r['containing_producer_accepted']);self.assertFalse(r['whole_product_accepted'])
    def test_VS_default_includes_negative_and_high_WORD_selectors(self):
        m=self.machine()
        for selection in (2,3,0x100,0xFFFF):
            r=m.run('vs',selection=selection,attribute=0xF3A5)
            self.assertEqual(r['events'][0]['arguments'],(0xF3A5,0xBB,m.ds,20,27))
    def test_invalid_main_WORD_draws_nothing_and_preserves_AX(self):
        r=self.machine().run('main',selection=0x100)
        self.assertEqual(r['events'],[]);self.assertEqual(r['registers']['ax'],0x1357)
    def test_all_four_rank_table_targets_draw_distinct_values(self):
        m=self.machine()
        for rank,off,x in ((0,0x113,38),(1,0x117,37),(2,0x11C,38),(3,0x120,37)):
            r=m.run('option',selection=0,rank=rank)
            self.assertEqual(r['events'][-1]['arguments'],(0xE1,off,m.ds,17,x))
    def test_rank_erasure_remains_white_with_full_WORD_gaiji_attribute(self):
        r=self.machine().run('option',selection=0,attribute=0xF3A5)
        self.assertEqual([e['arguments'][0] for e in r['events']],[0xF3A5,0xE1,0xF3A5])
        self.assertEqual(r['events'][1]['string_hex'],(b' '*8+b'\0').hex())
    def test_unknown_option_BYTE_values_keep_label_and_leak_native_registers(self):
        m=self.machine();r=m.run('option',selection=0,rank=255,resseg=0x5000,resoff=0xFF80)
        self.assertEqual((len(r['events']),r['registers']['ax'],r['registers']['bx'],r['registers']['es']),(2,255,255,0x5000))
        for sel,p in ((1,dict(bgm=255)),(2,dict(key=255))):
            r=m.run('option',selection=sel,resseg=0x5000,resoff=0xFF80,**p)
            self.assertEqual((len(r['events']),r['registers']['ax'],r['registers']['bx'],r['registers']['es']),(1,255,0xFF80,0x5000))
    def test_near_Pascal_return_preserves_caller_arguments_and_IF_DF(self):
        m=self.machine()
        for flags in (2,0x202,0x402,0xED7):
            r=m.run('option',selection=2,key=2,attribute=0xF3A5,stack=0x80,flags=flags)
            self.assertEqual((m.r('sp'),r['registers']['bp'],r['registers']['si'],r['registers']['di']),(0x86,0x207D,0x1C1B,0x1E4C))
            self.assertEqual(r['flags']&0x600,flags&0x600);self.assertEqual(bytes(m.uc.mem_read(0x70082,4)),struct.pack('<2H',0xF3A5,2))
    def test_equal_target_candidate_cannot_hide_changed_inline_separator(self):
        at=0x9900+0x798
        def changed(image):
            raw=bytearray(image.program_image);raw[at]=1;return replace(image,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'complete resolved renderer bytes including inline non-instructions'):verify(self.work,changed(self.target),changed(self.candidate))
    def test_all_twenty_four_actual_mutations_fail(self):self.assertEqual(negative_controls(self.target)['count'],24)
    @unittest.skipUnless((ROOT/'.analysis/work/op-render-build.json').is_file(),'complete renderer report absent')
    def test_inline_table_is_not_execution_coverage_or_whole_TU_ownership(self):
        s=json.loads((ROOT/'.analysis/work/op-render-build.json').read_bytes())['scope']
        bad=deepcopy(s);bad['runtime']['executed_owner_bytes']=518
        with self.assertRaisesRegex(ValueError,'runtime dimensions'):witness(bad)
        bad=deepcopy(s);bad['layout']['containing_producer_accepted']=True
        with self.assertRaisesRegex(ValueError,'bounded complete native'):witness(bad)
class MenuLedger(unittest.TestCase):
    def test_two_renderers_and_three_menu_functions_partition_the_old_span(self):
        with (ROOT/'config/units.csv').open() as stream:units={u['id']:u for u in csv.DictReader(stream)}
        spans=[(int(units[i]['offset'],0),int(units[i]['size'],0)) for i in ('th03-op-decoded-render-main-choice','th03-op-decoded-render-option-choice','th03-op-decoded-menu-move','th03-op-decoded-menu-state','th03-op-decoded-menu-option')]
        self.assertEqual(spans,[(0x5DD,122),(0x657,330),(0x7A1,63),(0x7E0,291),(0x903,532)]);self.assertEqual(sum(s for _,s in spans),1338)
        self.assertTrue(all(a+s==b for (a,s),(b,_) in zip(spans,spans[1:])))
