"""Graphics CPU/port/page contracts, with physical EGC raster effects excluded."""
from copy import deepcopy
from pathlib import Path
import json
import sys
import unittest
from unicorn import UC_HOOK_CODE

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.zun_driver_graphics_layout import control_flow,verify
from lib.zun_driver_graphics_runtime import Machine,BANKS,FIELDS,negative_controls
from review_th03_zun_format_work import images
from review_th03_zun_graphics_work import witness
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ZUN'

@unittest.skipUnless((WORK/'driver/driver.com').is_file(),'private current driver absent')
class Graphics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.image=(WORK/'driver/driver.com').read_bytes()
    def machine(self):
        m=Machine(self.image,0x3000);self.addCleanup(m.close);return m
    def field(self,m,name):return int.from_bytes(m.uc.mem_read(m.base+FIELDS[name],2),'little')
    def test_complete_graphics_scope_and_two_dead_clipping_jumps(self):
        work,target,candidate,at,files,maintained,cold=images(ROOT);r=verify(work,target,candidate,at,files,maintained)
        self.assertEqual((r['functions'],r['code_bytes'],len(r['ordered_native_fixups'])),(12,814,62))
        self.assertEqual(sum(f['self_relative'] for f in r['ordered_native_fixups']),9)
        self.assertEqual(r['control_flow']['unreachable_owner_bytes'],4)
        self.assertFalse(r['enclosing_driver_accepted']);self.assertFalse(r['reserved_spans_owned'])
    def test_redirected_rejection_branch_cannot_reuse_dead_code_partition(self):
        raw=bytearray(self.image);raw[0x39E-256]=0
        with self.assertRaisesRegex(ValueError,'unreachable'):control_flow(bytes(raw))
    def test_both_EGC_helpers_force_IF_on_and_preserve_DF(self):
        m=self.machine()
        for kind in ('egc_begin','egc_end'):
            for flags in (2,0x402):self.assertEqual(m.run(kind,flags=flags)['if_df'],(flags&0x400)|0x200)
    def test_zero_height_really_visits_65536_empty_rows(self):
        m=self.machine();counts=[0]
        h=m.uc.hook_add(UC_HOOK_CODE,lambda uc,a,s,u:counts.__setitem__(0,counts[0]+1),begin=m.base+0x508,end=m.base+0x508)
        try:r=m.run('copy_rows',height=0,words=0,skip=80,flags=2)
        finally:m.uc.hook_del(h)
        self.assertEqual(counts[0],65536);self.assertEqual(r['event_count'],0)
        self.assertEqual((r['registers']['ax'],r['registers']['bx'],r['registers']['cx'],r['registers']['dx']),(80,0,0,0))
        self.assertEqual(r['if_df'],0)
    def test_top_clip_does_not_apply_a_second_bottom_clip(self):
        m=self.machine();m.run('draw_clipped',x=0,y=-1,width=2,height=202,mono=1)
        self.assertEqual((self.field(m,'y'),self.field(m,'height'),self.field(m,'source')),(0,201,0x250))
    def test_fully_clipped_rows_issue_no_ports_or_video_writes(self):
        m=self.machine()
        for y,height in ((-3,3),(200,1),(0x7FFF,3)):
            self.assertEqual(m.run('draw_clipped',y=y,height=height)['event_count'],6)
    def test_shift_adds_one_word_without_clamping_horizontal_position(self):
        m=self.machine();m.run('draw_clipped',x=0xFFFF,width=2,height=1)
        self.assertEqual((self.field(m,'shift'),self.field(m,'has_shift'),self.field(m,'words'),self.field(m,'skip')),(15,1,3,74))
    def test_page_copy_uses_page_zero_and_leaves_access_page_one(self):
        m=self.machine();r=m.run('copy_lower_page',page=1,flags=0xED7)
        self.assertEqual(r['access_page'],1)
        self.assertEqual(m.pages[1][0][16000:32000],m.page_templates[0][0][16000:32000])
        self.assertEqual(m.pages[0][0],m.page_templates[0][0])
    def test_prepare_restores_access_and_display_pages_to_zero(self):
        r=self.machine().run('prepare_vram',page=1,flags=2)
        self.assertEqual((r['access_page'],r['if_df']),(0,0x200))
        self.assertEqual(r['event_count'],40055)
    def test_mask_ORs_all_four_plane_words_then_inverts(self):
        m=self.machine();m.run('build_mask',page=1)
        for off in (0,84,15998):
            expected=0
            for bank in m.page_templates[0]:expected|=int.from_bytes(bank[off+16000:off+16002],'little')
            self.assertEqual(int.from_bytes(m.uc.mem_read(0x50000+off,2),'little'),expected)
            self.assertEqual(int.from_bytes(m.uc.mem_read(0x60000+off,2),'little'),expected^65535)
    def test_compress_reads_every_other_source_row(self):
        m=self.machine();m.run('compress_rows',page=1)
        expected=b''.join(m.page_templates[1][0][row*160:row*160+80] for row in range(200))
        self.assertEqual(m.uc.mem_read(BANKS[0],16000),expected)
    def test_forward_copy_precondition_does_not_apply_to_explicit_address_copy(self):
        m=self.machine()
        with self.assertRaisesRegex(ValueError,'forward graphics'):m.run('compress_rows',flags=0x402)
        self.assertEqual(m.run('copy_lower_page',flags=0x402)['if_df'],0x600)
    def test_all_twenty_six_real_mutations_fail(self):
        self.assertEqual(negative_controls(self.image)['count'],26)
    @unittest.skipUnless((ROOT/'.analysis/work/zun-graphics-build.json').is_file(),'complete graphics witness absent')
    def test_single_page_or_dead_execution_credit_cannot_inherit_witness(self):
        original=json.loads((ROOT/'.analysis/work/zun-graphics-build.json').read_bytes())['scope']
        for key,value in (('video_pages',1),('executed_owner_bytes',814)):
            s=deepcopy(original);s['runtime'][key]=value
            with self.assertRaisesRegex(ValueError,'runtime dimensions'):witness(s)
