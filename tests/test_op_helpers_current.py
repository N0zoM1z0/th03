"""OP helper ownership, same IRQ counter and initializer failure/cdecl contracts."""
from copy import deepcopy
from pathlib import Path
import json,shutil,struct,sys,tempfile,unittest
from unicorn import UC_HOOK_INTR
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from lib.op_helpers_layout import verify,FORWARDING
from lib.op_helpers_sound_runtime import Machine as SoundMachine,negative_controls as sound_controls
from lib.op_init_runtime import Machine,negative_controls,POINTERS
from review_th03_op_cfg_work import images
from review_th03_op_helpers_work import witness
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP'
@unittest.skipUnless((WORK/'bin/th03/op.exe').is_file(),'private current OP absent')
class Helpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.work,cls.target,cls.candidate,*_=images(ROOT)
    def machine(self,cls=Machine):
        m=cls(self.target,0x3000);self.addCleanup(m.close);return m
    def test_three_whole_objects_and_real_TLINK_relaxation(self):
        r=verify(self.work,self.target,self.candidate)
        self.assertEqual((r['functions'],r['code_bytes'],len(r['ordered_relocations']),r['normal_tlink_relaxed_calls']),(3,156,11,1))
        self.assertEqual(sum(len(o['ordered_fields']) for o in r['native_objects']),16)
        self.assertEqual([o['callee_pop_bytes'] for o in r['owners']],[2,2,0])
        self.assertTrue(all(o['canonical_file_offset'] is None for o in r['owners']));self.assertFalse(r['whole_product_accepted'])
    def test_equal_native_bytes_cannot_hide_a_changed_intermediate_forwarder(self):
        # Keep every native output and target byte, changing only source provenance.
        files=['obj/th03/op.map','obj/th02/frmdely2.obj','obj/th03/snd_kaja.obj','obj/th03/initop.obj','th02/frmdely2.cpp']
        files += [p for chain in FORWARDING.values() for p in chain[:-1]]
        with tempfile.TemporaryDirectory() as tmp:
            work=Path(tmp)
            for path in files:
                (work/path).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(self.work/path,work/path)
            (work/'th02/snd/kajaint.cpp').write_text('#include "unreviewed.cpp"\n')
            with self.assertRaisesRegex(ValueError,'literal maintained forwarding layer'):verify(work,self.target,self.candidate)
    def test_delay_2_uses_Count1_and_preserves_the_other_counter(self):
        m=self.machine(SoundMachine);other=bytes(m.initial[m.data+0x11EA:m.data+0x11EC])
        r=m.run('frame_delay',frames=0x8000,ticks=(0x7FFF,0x8000),flags=0xED7)
        self.assertEqual((r['registers']['ax'],r['counter_updates'],m.r('sp'),r['flags']&0x600),(0x8000,2,0xF806,0x600))
        self.assertEqual(bytes(m.uc.mem_read(m.data+0x11E8,2)),b'\0\x80');self.assertEqual(bytes(m.uc.mem_read(m.data+0x11EA,2)),other)
    def test_inactive_KAJA_returns_incoming_AX_without_loading_argument(self):
        r=self.machine(SoundMachine).run('kaja',active=0,argument=0xFFFF)
        self.assertEqual((r['registers']['ax'],r['driver_calls']),(0x1357,0))
    def test_KAJA_selects_MMD_only_for_MIDI_byte_one(self):
        m=self.machine(SoundMachine);vectors=[];h=m.uc.hook_add(UC_HOOK_INTR,lambda uc,n,u:vectors.append(n))
        try:
            for midi in (2,1,255):m.run('kaja',midi=midi)
        finally:m.uc.hook_del(h)
        self.assertEqual(vectors,[0x60,0x61,0x60])
    def test_allocation_high_byte_errors_return_one_before_side_effects(self):
        m=self.machine()
        for assign in (0x100,0x7FFF,0x8000,0xFFFF):
            r=m.run(assign=assign)
            self.assertEqual((r['registers']['ax'],r['library_calls'],r['actual_plane_calls']),(1,1,0))
            self.assertEqual(r['events'],[('service','assign',22000)])
    def test_success_executes_planes_ports_and_ignores_later_errors(self):
        m=self.machine();r=m.run(status=0xFFFF,flags=0xED7)
        self.assertEqual((r['registers']['ax'],r['library_calls'],r['actual_plane_calls'],r['flags']&0x600),(0,11,1,0x600))
        self.assertEqual(struct.unpack('<4I',bytes(m.uc.mem_read(m.data+0x19FA,16))),POINTERS)
        self.assertEqual([e for e in r['events'] if e[0]=='out'],[('out',0xA6,1),('out',0xA6,0),('out',0xA6,0),('out',0xA4,0)])
    def test_far_filename_is_forwarded_unchanged_and_remains_caller_owned(self):
        m=self.machine();r=m.run(filename=(0xFFFF,0xFFFF),stack=0x80)
        self.assertEqual(r['events'][-1],('service','pfstart',(0xFFFF,0xFFFF)))
        self.assertEqual((m.r('sp'),bytes(m.uc.mem_read(0x70084,4))),(0x84,b'\xFF'*4))
    def test_twenty_four_actual_instruction_mutations_fail(self):
        self.assertEqual(sound_controls(self.target)['count']+negative_controls(self.target)['count'],24)
    @unittest.skipUnless((ROOT/'.analysis/work/op-helpers-build.json').is_file(),'full OP helpers witness absent')
    def test_partial_success_or_nested_coverage_cannot_inherit_acceptance(self):
        s=json.loads((ROOT/'.analysis/work/op-helpers-build.json').read_bytes())['scope']
        for key,value in (('allocation_success_cases',228),('executed_nested_bytes',0)):
            bad=deepcopy(s);bad['init_runtime']['observations'][0][key]=value
            with self.assertRaisesRegex(ValueError,'success/failure/plane/stack'):witness(bad)
