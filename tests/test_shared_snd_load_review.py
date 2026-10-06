from dataclasses import replace
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from lib.pc98 import parse_mz
import review_th03_shared_snd_load as m


class SharedSoundLoadControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.images={a:parse_mz(p.read_bytes()) for a in m.PROFILES if (p:=m.ROOT/f'.analysis/th03-diet/sol-diet-restoration-20261006-b/{a}.exe').exists()}
    def targets(self):
        if not self.images:self.skipTest('private decoded targets absent')
        return [(a,mz,m.PROFILES[a]) for a,mz in self.images.items()]
    def test_complete_binding_and_branch_controls(self):
        for a,mz,p in self.targets():
            for at in (0x14,0x23,0x64,0x18,0x6f):
                with self.subTest(artifact=a,offset=at):
                    image=bytearray(mz.program_image);image[p['cs']*16+p['start']+at]^=1
                    with self.assertRaises(ValueError):m.analyze(image,p)
    def test_all_reachable_positions_and_incoming_flags(self):
        for a,mz,p in self.targets():
            rows=m.matrix(mz,p,True);cov=m.coverage(m.analyze(mz.program_image,p),rows)
            self.assertEqual((cov['positions'],cov['returns'],cov['prefixes']),(45,98,1))
    def test_open_error_is_used_as_handle_and_still_read_and_closed(self):
        for a,mz,p in self.targets():
            row=m.LoadProbe(mz,p).run(dict(open_reply={'AX':2,'CF':1},read_reply={'AX':6,'CF':1},payload=''))
            calls=[e for e in row['events'] if e[0]=='interrupt']
            self.assertEqual([e[1] for e in calls],['open','driver','read','close'])
            self.assertEqual([e[3]['BX'] for e in calls[1:]],[2,2,2]);self.assertEqual(calls[-1][3]['AX'],0x3e06)
    def test_empty_filename_starts_scan_at_one_and_can_overrun_object(self):
        for a,mz,p in self.targets():
            probe=m.LoadProbe(mz,p);row=probe.run(dict(source='00'+'41'*12,stale='5a'*20+'00'+'a5'*15))
            stores=[e for e in row['events'] if e[0]=='store']
            self.assertEqual(stores[-3:], [['store',probe.ds+p['filename']+20+i,1,v] for i,v in enumerate(b'md\0')])
    def test_overlapping_forward_copy_reads_previous_writes(self):
        for a,mz,p in self.targets():
            probe=m.LoadProbe(mz,p);row=probe.run(dict(segment=p['ds']+0x2000,offset=p['filename']-1,midi=0))
            self.assertEqual(bytes.fromhex(row['filename'])[:13],b'A'*13)
    def test_driver_and_read_bx_replies_reach_close(self):
        for a,mz,p in self.targets():
            row=m.LoadProbe(mz,p).run(dict(driver_reply={'BX':0x4321},read_reply={'BX':0xbeef}))
            calls=[e for e in row['events'] if e[0]=='interrupt']
            self.assertEqual(calls[2][3]['BX'],0x4321);self.assertEqual(calls[3][3]['BX'],0xbeef)
    def test_open_can_change_midi_branch_between_filename_and_driver(self):
        for a,mz,p in self.targets():
            probe=m.LoadProbe(mz,p);row=probe.run(dict(open_writes=[[probe.ds+p['midi'],'00']]))
            self.assertEqual([e[3] for e in row['events'] if e[0]=='store'][-3:],[109,100,0])
            self.assertEqual([e[2] for e in row['events'] if e[0]=='interrupt'][1],0x60)
    def test_read_aliases_saved_registers_without_hiding_stack_bytes(self):
        for a,mz,p in self.targets():
            row=m.LoadProbe(mz,p).run(dict(driver_reply={'DS':0x4000,'DX':0xffba},payload='34127856bc9a'))
            self.assertEqual((row['registers']['DS'],row['registers']['SI'],row['registers']['BP']),(0x1234,0x5678,0x9abc))
    def test_native_copy_direction_mutation_is_rejected(self):
        for a,mz,p in self.targets():
            image=bytearray(mz.program_image);image[p['cs']*16+p['start']+0x16]=0x4e;altered=replace(mz,program_image=bytes(image))
            with self.assertRaisesRegex(ValueError,'native event'):m.LoadProbe(altered,p).run(dict(midi=0))
    def test_full_physical_guard_rejects_extra_scalar_byte(self):
        original=m.LoadSpec.events
        def changed(spec):
            yield from original(spec)
            spec.memory[0x8fff0]^=1
        for a,mz,p in self.targets():
            with patch.object(m.LoadSpec,'events',changed),self.assertRaisesRegex(ValueError,'physical memory'):m.LoadProbe(mz,p).run({})


if __name__=='__main__':unittest.main()
