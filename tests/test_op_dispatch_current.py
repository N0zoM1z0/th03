"""Whole dispatch bodies and target-specific wrap/exec/cleanup behavior."""
from copy import deepcopy
from pathlib import Path
import csv
import json
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.pc98 import parse_mz
from lib.op_dispatch_layout import verify,OBJECT,FUNCTIONS,native_image
from lib.op_dispatch_runtime import Machine,negative_controls
from review_th03_op_dispatch_work import witness
from test_main_enemy_layout import mutate_record

WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP'


@unittest.skipUnless((WORK/'bin/th03/op.target.exe').is_file(),'private current OP target absent')
class Dispatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target=parse_mz((WORK/'bin/th03/op.target.exe').read_bytes());cls.candidate=parse_mz((WORK/'bin/th03/op.exe').read_bytes())
    def machine(self):
        m=Machine(self.target,0x3000);self.addCleanup(m.close);return m
    def test_whole_demo_and_score_bodies_exclude_attract_wait(self):
        r=verify(WORK,self.target,self.candidate)
        self.assertEqual((r['functions'],r['code_bytes']),(2,296))
        self.assertEqual((len(r['ordered_native_fields']),len(r['ordered_relocations'])),(25,10))
        self.assertEqual(r['reviewed_initialized_dependency_bytes'],32)
        self.assertFalse(r['containing_producer_accepted']);self.assertFalse(r['whole_product_accepted'])
        self.assertEqual([o['size'] for o in r['owners']],[202,94])
    def test_containing_public_identity_cannot_be_borrowed(self):
        raw=(WORK/OBJECT).read_bytes()
        changed=mutate_record(raw,lambda r:r.name=='PUBDEF' and b'@start_demo$qv' in r.data,lambda d:d.replace(b'@start_demo$qv',b'@start_fake$qv'))
        with self.assertRaisesRegex(ValueError,'fifteen containing CODE publics'):native_image(changed)
    def test_all_four_demo_pairings_and_independent_DWORD_seeds(self):
        m=self.machine()
        for demo,pair,seed in ((0,b'\x03\x01',600),(1,b'\x05\x0D',1000),(2,b'\x07\x0B',3200),(3,b'\x09\x05',500),(4,b'\x03\x01',600),(254,b'\x03\x01',600)):
            m.run('start_demo',demo=demo)
            self.assertEqual(m.uc.mem_read(0x60031+0xC,2),pair)
            self.assertEqual(int.from_bytes(m.uc.mem_read(0x60031+0x10,4),'little'),seed)
    def test_255_wrap_reads_adjacent_bytes_instead_of_normalizing_to_one(self):
        m=self.machine();m.run('start_demo',demo=255)
        self.assertEqual(m.uc.mem_read(0x60031+0x39,1),b'\0')
        self.assertEqual(m.uc.mem_read(0x60031+0xC,2),b'\x8F\0')
        self.assertEqual(m.uc.mem_read(0x60031+0x10,4),b'\x07\x0B\x09\x05')
    def test_real_cfg_save_preserves_fourth_stack_byte_and_file_tail(self):
        m=self.machine();r=m.run('score_menu',trash=0xA7,options=(1,2,3))
        self.assertEqual(bytes.fromhex(r['file_hex']),b'\x01\x02\x03\xA7\x57\0\x50\xA7')
        self.assertEqual(m.maximum_stack,26)
    def test_score_bool_return_is_AL_not_BOOL16(self):
        m=self.machine()
        self.assertEqual(m.run('score_menu',status=0xABCD)['registers']['ax'],0xAB00)
        self.assertEqual(m.run('start_demo',status=0xABCD)['registers']['ax'],0xABCD)
    def test_score_only_frees_super_and_preserves_demo_state(self):
        m=self.machine();r=m.run('score_menu',demo=0x81,resident_seed=0x6C)
        self.assertIn(('service','super_free',None),r['events'])
        self.assertEqual(m.uc.mem_read(0x60031+0x39,1),b'\x81')
        self.assertEqual(m.uc.mem_read(0x60031+0x18,16),bytes(16))
        self.assertEqual(m.uc.mem_read(0x60031+0xE,2),b'\x6C\x6C')
        self.assertNotIn(('service','super_free',None),m.run('start_demo')['events'])
    def test_real_MIDI_routing_requires_BYTE_one(self):
        m=self.machine()
        for midi,interrupt in ((0,0x60),(1,0x61),(0x80,0x60)):
            r=m.run('score_menu',midi=midi,flags=0xED7)
            self.assertIn(('interrupt',interrupt,0x100),r['events'])
        self.assertFalse(any(e[0]=='interrupt' for e in m.run('score_menu',active=0)['events']))
    def test_real_cleanup_has_both_pages_and_final_display_page(self):
        r=self.machine().run('score_menu')
        self.assertEqual([e for e in r['events'] if e[0]=='out'],[('out',0xA6,1),('out',0xA6,0),('out',0xA6,0),('out',0xA4,0)])
    def test_all_twenty_three_actual_instruction_mutations_fail(self):
        self.assertEqual(negative_controls(self.target)['count'],23)
    @unittest.skipUnless((ROOT/'.analysis/work/op-dispatch-build.json').is_file(),'full current dispatch witness absent')
    def test_no_partial_helper_domain_can_inherit_full_witness(self):
        scope=deepcopy(json.loads((ROOT/'.analysis/work/op-dispatch-build.json').read_text())['scope'])
        scope['runtime']['observations'][0]['executed_nested_bytes']=0
        with self.assertRaisesRegex(ValueError,'coverage/helper/stack'):witness(scope)


class LedgerRefinement(unittest.TestCase):
    def test_entry_split_partitions_original_span_without_extra_source_bytes(self):
        with (ROOT/'config/units.csv').open() as stream:
            units={r['id']:r for r in csv.DictReader(stream)}
        ids=('th03-op-decoded-entry-screens','th03-op-decoded-entry-demo','th03-op-decoded-entry-attract-wait','th03-op-decoded-entry-score')
        spans=[(int(units[i]['offset'],0),int(units[i]['size'],0)) for i in ids]
        self.assertEqual(spans,[(0x117,821),(0x44C,202),(0x516,105),(0x57F,94)])
        self.assertEqual(sum(s for _,s in spans),1222)
        self.assertTrue(all(a+s==b for (a,s),(b,_) in zip(spans,spans[1:])))
        self.assertNotIn(ids[2],{u[0] for u in FUNCTIONS})
