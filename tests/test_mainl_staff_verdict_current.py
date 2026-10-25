"""Complete verdict: native field namespaces, far pointers and live callbacks."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import struct
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_sound_work import images
from review_th03_mainl_staff_verdict_work import REPORT,witness
from lib.decoded_mainl_staff_verdict_layout import verify,CS,START,DATA
from lib.decoded_mainl_staff_verdict_runtime import Machine,DEFAULT_SCORE,geometry_proof,renderer_reply

WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class StaffVerdictCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files=images(ROOT)

    def machine(self):
        m=Machine(self.target,0x3000)
        self.addCleanup(m.close)
        return m

    def byte(self,m,off):
        return m.u.mem_read(m.data_ds*16+off,1)[0]

    def pointer(self,m,table,index):
        raw=bytes(m.u.mem_read(m.data_ds*16+DATA[table]+index*4,4))
        off,seg=struct.unpack('<2H',raw)
        return [seg,off]

    def test_complete_native_owner_separates_local_SEGDEF_from_external_fields(self):
        p=verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((p['code_bytes'],len(p['ordered_native_fields']),p['mz_relocation_count'],len(p['far_calls'])),(389,25,9,9))
        fields=p['ordered_native_fields']
        local=[f for f in fields if f['namespace']=='SEGDEF']
        self.assertEqual(len(local),8)
        self.assertTrue(all((f['target'],f['fixdat'],f['frame'],f['width'])==(2,0x14,2,2) for f in local))
        self.assertEqual({f['addend'] for f in local},{132,168,184})
        self.assertNotIn('_random_seed',{f['name'] for f in local})
        self.assertEqual(p['owners'][0]['name'],'_mainl_staff_verdict')
        self.assertEqual((p['owners'][0]['argument_bytes'],p['owners'][0]['callee_pop_bytes']),(0,0))
        self.assertTrue(all(c['argument_bytes']==c['callee_pop_bytes']==10 for c in p['far_calls']))
        self.assertFalse(p['renderer_code_or_strings_tables_accepted'])

    def test_equal_image_corruption_cannot_replace_independent_native_source(self):
        raw=bytearray(self.target.program_image)
        raw[CS*16+START]^=1
        bad=replace(self.target,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'independently linked native'):
            verify(self.work,bad,bad,self.graph,self.files)

    def test_same_MZ_membership_with_wrong_order_is_rejected(self):
        positions=[i for i,r in enumerate(self.target.relocations) if CS*16+START<=r.linear<CS*16+START+389]
        rows=list(self.target.relocations)
        rows[positions[0]],rows[positions[1]]=rows[positions[1]],rows[positions[0]]
        with self.assertRaisesRegex(ValueError,'literal ordered MZ'):
            verify(self.work,replace(self.target,relocations=tuple(rows)),self.candidate,self.graph,self.files)

    def test_far_pointer_preserves_both_WORDs_in_real_fourteen_byte_frame(self):
        m=self.machine()
        r=m.run(pointer=(DATA['playchars']+2*4,0xABCDFFFF))
        self.assertEqual(r['rendered'][0]['pointer'],[0xABCD,0xFFFF])
        event=next(e for e in m.events if e[0]=='render-entry')
        frame=struct.unpack('<7H',bytes.fromhex(event[3]))
        self.assertEqual(frame,(0x2CBA,m.cs,0xFFFF,0xABCD,0x2F,174,352))
        self.assertEqual(r['stack_depth'],24)

    def test_uncapped_BYTE_selectors_read_full_DWORD_tables(self):
        m=self.machine()
        r=m.run(playchar=255,rank=255,score=(255,)*9)
        self.assertEqual(r['rendered'][0]['pointer'],self.pointer(m,'playchars',255))
        self.assertEqual(r['rendered'][1]['pointer'],self.pointer(m,'ranks',255))
        self.assertEqual(r['rendered'][2]['pointer'],self.pointer(m,'numbers',255))
        self.assertEqual(r['renderer_calls'],16)

    def test_zero_score_and_skill_have_six_calls_and_keep_continues_draws(self):
        m=self.machine()
        r=m.run(score=(0,)*9,skill=0)
        self.assertEqual((r['renderer_calls'],r['score_iterations']),(6,8))
        self.assertEqual([(v['x'],v['y']) for v in r['rendered']],[(352,174),(360,199),(408,224),(408,248),(408,291),(424,291)])
        self.assertEqual(r['rendered'][2]['pointer'],self.pointer(m,'numbers',0))

    def test_leading_position_controls_x_and_preserves_interior_zeroes(self):
        m=self.machine()
        score=(2,3,0,7,0,0,0,0,0)
        r=m.run(score=score,skill=0)
        rendered=[v for v in r['rendered'] if v['y']==224]
        self.assertEqual([v['x'] for v in rendered],[384,400,416,432])
        self.assertEqual([v['pointer'] for v in rendered],[self.pointer(m,'numbers',v) for v in (7,0,3,2)])
        self.assertEqual(r['score_iterations'],8)

    def test_maximal_score_layout_ends_continues_at472(self):
        m=self.machine()
        r=m.run()
        rendered=[v for v in r['rendered'] if v['y']==224]
        self.assertEqual([v['x'] for v in rendered],list(range(344,473,16)))
        self.assertEqual((r['renderer_calls'],r['stack_depth']),(16,24))

    def test_score_packet_written_after_rank_is_loaded_by_the_eight_step_loop(self):
        m=self.machine()
        score=bytes((2,3,0,7,0,0,0,0,0))
        r=m.run(writes=((2,DATA['score'],score),),skill=0)
        self.assertEqual([v['x'] for v in r['rendered'] if v['y']==224],[384,400,416,432])
        self.assertEqual(r['renderer_calls'],9)

    def test_score_digit_is_reloaded_after_the_previous_render_callback(self):
        m=self.machine()
        r=m.run(writes=((3,DATA['score']+7,b'\xFF'),))
        self.assertEqual(r['rendered'][3]['pointer'],self.pointer(m,'numbers',255))
        self.assertEqual((r['rendered'][3]['x'],r['rendered'][3]['y']),(360,224))

    def test_continues_keeps_saved_digit_but_reloads_its_far_pointer(self):
        m=self.machine()
        r=m.run(writes=((11,DATA['score'],b'\xFF'),(11,DATA['numbers']+2*4,bytes.fromhex('ffffcdab'))))
        self.assertEqual(r['rendered'][11]['pointer'],[0xABCD,0xFFFF])
        self.assertNotEqual(r['rendered'][10]['pointer'],r['rendered'][11]['pointer'])
        self.assertNotEqual(r['rendered'][11]['pointer'],self.pointer(m,'numbers',255))
        self.assertEqual(self.byte(m,DATA['score']),255)

    def test_continues_aliases_score_byte_zero_without_a_tenth_byte(self):
        m=self.machine()
        r=m.run(score=(255,*DEFAULT_SCORE[1:]))
        self.assertEqual(r['rendered'][10]['pointer'],self.pointer(m,'numbers',255))
        self.assertEqual(r['rendered'][11]['pointer'],self.pointer(m,'numbers',255))
        self.assertEqual([v['x'] for v in r['rendered'][2:10]],list(range(344,457,16)))

    def test_rank_pointer_is_read_after_character_callback(self):
        m=self.machine()
        r=m.run(writes=((1,DATA['ranks']+3*4,bytes.fromhex('ffff0000')),(1,DATA['playchar'],b'\xFF')))
        self.assertEqual(r['rendered'][1]['pointer'],[0,0xFFFF])
        self.assertNotEqual(r['rendered'][0]['pointer'],self.pointer(m,'playchars',255))
        self.assertEqual(self.byte(m,DATA['playchar']),255)

    def test_skill_hundreds_tens_ones_are_three_live_BYTE_reads(self):
        m=self.machine()
        r=m.run(score=(0,)*9,skill=100,writes=((5,DATA['skill'],b'\x09'),(6,DATA['skill'],b'\xFF')))
        rendered=[v for v in r['rendered'] if v['y']==291]
        self.assertEqual([v['x'] for v in rendered],[392,408,424,440])
        self.assertEqual([v['pointer'] for v in rendered[:3]],[self.pointer(m,'numbers',v) for v in (1,0,5)])
        self.assertEqual(self.byte(m,DATA['skill']),255)

    def test_tens_only_skill_uses_half_width_leading_adjustment(self):
        m=self.machine()
        r=m.run(score=(0,)*9,skill=10)
        self.assertEqual([v['x'] for v in r['rendered'] if v['y']==291],[400,416,432])

    def test_unit_far_pointer_uses_actual_DS_and_near_RET_pops_only_return_word(self):
        m=self.machine()
        r=m.run(foreign_ds=True,ss=0x8000,stack=0x80,flags=0xED7)
        self.assertEqual(r['rendered'][-1]['pointer'],[0x5000,DATA['unit']])
        self.assertEqual((r['registers']['sp']&65535,r['registers']['ss'],r['registers']['ds']),(0x82,0x8000,0x5000))
        self.assertEqual((r['registers']['fs'],r['registers']['gs']),(0x3456,0x4567))
        high=(0x1357^0x5AA5)<<16
        self.assertEqual(r['registers']['si'],high|((0x1357+4*0x231)&65535))
        self.assertEqual(r['registers']['di'],high|((0x1357+5*0x231)&65535))
        self.assertEqual(r['registers']['bp'],high|((0x1357+6*0x231)&65535))

    def test_full_DWORD_renderer_replies_survive_word_only_owner_instructions(self):
        m=self.machine()
        r=m.run(reply_seed=0xFFFF0000)
        reply=renderer_reply(0xFFFF0000,r['renderer_calls'])
        self.assertEqual({k:r['registers'][k] for k in ('ax','bx','cx','dx','es')},reply)
        self.assertNotEqual(r['registers']['ax']>>16,0x1357^0x5AA5)

    def test_shift_flags_exclude_undefined_AF_OF_and_reply_IF_DF_are_retained(self):
        m=self.machine()
        r=m.run(flags=0xED7,flag_schedule=(2,0x202,0x402,0xED7))
        first=next(e for e in m.events if e[0]=='render-entry')
        self.assertEqual(first[-1],0x6C5)
        self.assertEqual(r['flags']&0x600,0x600)
        self.assertEqual(r['flag_mask'],0xED5)

    def test_persistent_reentry_uses_previous_live_skill_and_table_memory(self):
        m=self.machine()
        a=m.run(writes=((1,DATA['skill'],b'\x64'),(1,DATA['numbers']+2*4,bytes.fromhex('ffffcdab'))))
        b=m.run(persistent=True)
        self.assertEqual(self.byte(m,DATA['skill']),100)
        self.assertEqual(b['rendered'][10]['pointer'],[0xABCD,0xFFFF])
        self.assertEqual(a['score_iterations'],b['score_iterations'])

    def test_geometry_proves_fixed_loop_and_all_BYTE_division_inputs(self):
        p=geometry_proof(self.target)
        self.assertEqual((p['score_iterations'],p['renderer_call_bounds'],p['far_string_bytes']),(8,[6,16],4))
        self.assertEqual((p['skill_hundreds_range'],p['skill_tens_and_ones_range']),([0,2],[0,9]))
        self.assertTrue(p['loop_termination_proved'] and p['all_DIV_inputs_safe'])
        for at in (0x2CE1,0x2D26,0x2D2D,0x2D3F,0x2DA6,0x2E10):
            raw=bytearray(self.target.program_image)
            raw[CS*16+at]^=1
            with self.subTest(at=at),self.assertRaises(ValueError):geometry_proof(replace(self.target,program_image=bytes(raw)))

    def test_full_witness_keeps_all_returns_and_no_context_credit(self):
        if not REPORT.is_file() or not json.loads(REPORT.read_text()).get('complete'):
            self.skipTest('complete verdict witness absent')
        scope=json.loads(REPORT.read_text())['scope']
        witness(scope)
        self.assertEqual(scope['runtime']['actual_context_bytes'],0)
        bad=deepcopy(scope)
        bad['runtime']['native_geometry_proof']['loop_termination_proved']=False
        with self.assertRaises(ValueError):witness(bad)

    def test_witness_rejects_unowned_renderer_and_data_promotion(self):
        if not REPORT.is_file() or not json.loads(REPORT.read_text()).get('complete'):
            self.skipTest('complete verdict witness absent')
        scope=json.loads(REPORT.read_text())['scope']
        for field in ('renderer_code_or_strings_tables_accepted','enclosing_DATA_or_other_functions_accepted','physical_text_or_pixels_proved'):
            bad=deepcopy(scope)
            bad['layout'][field]=True
            with self.subTest(field=field),self.assertRaises(ValueError):witness(bad)


if __name__=='__main__':
    unittest.main()
