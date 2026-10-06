"""Palette scope, mutable CODE, native frames and device-interface guards."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_palette import ALIGNMENT,RANGES,PaletteProbe,analyze


def fixture():
    data=bytearray(b'\x90'*0x237e)
    for _,a,z,c in RANGES:
        tail=b'\xca'+struct.pack('<H',c) if c else b'\xcb'
        data[a+z-len(tail):a+z]=tail
    data[0x1854:0x1858]=b'\x2e\xa2\xb8\x18';data[0x18b6:0x18b9]=b'\x80\xf4\x00'
    for a,v in ALIGNMENT.items():data[a]=v
    return data


def jump(at,to):return b'\xe9'+struct.pack('<h',to-at-3)


class PaletteBoundaryTests(unittest.TestCase):
    def test_complete_bodies_cleanup_and_interior_returns(self):
        self.assertEqual(analyze(fixture())['complete_include_bytes'],692)
        with self.assertRaisesRegex(ValueError,'complete include'):analyze(fixture()[:0x2109])
        data=fixture();data[0x504]=4
        with self.assertRaisesRegex(ValueError,'complete body/far cleanup'):analyze(data)
        data=fixture();data[0x4c6]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)

    def test_operand_neighbor_and_unknown_edges(self):
        for target in (0x4c7,0x506):
            data=fixture();data[0x4c6:0x4c9]=jump(0x4c6,target)
            with self.assertRaisesRegex(ValueError,'branch enters operand/neighbor'):analyze(data)
        for code,msg in ((b'\xe8\x00\x00','unknown native call'),(b'\xff\xd0','unknown indirect'),(b'\x9a\x00\x00\x00\x00','unknown far')):
            data=fixture();data[0x4c6:0x4c6+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)
        data=fixture();data[0x1a74:0x1a77]=b'\xe8'+struct.pack('<h',0xaae-0x1a77)
        with self.assertRaisesRegex(ValueError,'lacks PUSH CS'):analyze(data)

    def test_dos_and_port_sites(self):
        for code,msg in ((b'\xcd\x21','unknown DOS'),(b'\xcd\x20','unknown DOS'),(b'\xe6\xa8','unknown port'),(b'\xe4\xa0','unknown port')):
            data=fixture();data[0x4c6:0x4c6+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)

    def test_mutable_operand_opcode_target_and_alignment(self):
        for at in (0x1854,0x1856,0x18b6,0x18b8):
            data=fixture();data[at]^=1
            with self.assertRaisesRegex(ValueError,'mutable CODE operand'):analyze(data)
        data=fixture();data[0x579]=0
        with self.assertRaisesRegex(ValueError,'producer alignment'):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class PaletteRuntimeTests(unittest.TestCase):
    def probe(self,code,at=0x4c6,patches=(),s=None):
        __import__('unicorn');data=fixture();observed=analyze(data);data[at:at+len(code)]=code
        for a,b in patches:data[a:a+len(b)]=b
        return PaletteProbe(SimpleNamespace(program_image=data,relocations=[]),s or {},observed)

    def test_guarded_callbacks_and_whole_write_spans(self):
        __import__('unicorn')
        for code,msg in ((b'\xcd\x21','unknown DOS request/site'),(b'\xe6\xa8','unknown output port/site/width'),(b'\xe4\xa0','unknown input port/site/width'),(b'\xc7\x06\x4d\x14\x00\x00','outside owned state/operand'),(b'\x2e\xc6\x06\xb8\x18\x01','outside owned state/operand'),(b'\x2e\xc7\x06\xb8\x18\xff\x00','outside owned state/operand')):
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,msg):self.probe(code).run('bfnt',[0x200,0x5000,0x1234])
            self.assertEqual(stderr.getvalue(),'')
        code=b'\x2e\xc6\x06\xb8\x18\xff';code+=jump(0x4c6+len(code),0x503)
        p=self.probe(code);p.run('bfnt',[0x200,0x5000,0x1234]);self.assertEqual(p.uc.mem_read(p.code+0x18b8,1),b'\xff')

    def test_known_dos_site_rejects_ah_destination_and_count(self):
        for prefix,msg in ((b'\xb4\x3e','unknown DOS request/site'),(b'\xb4\x3f\xba\x1f\x14\xb9\x30\x00','read destination/count'),(b'\xb4\x3f\xba\x1e\x14\xb9\x2f\x00','read destination/count'),(b'\xb8\x00\x50\x8e\xd8\xb4\x3f\xba\x1e\x14\xb9\x30\x00','read destination/count')):
            code=prefix+jump(0x4c6+len(prefix),0x4df)
            with self.assertRaisesRegex(ValueError,msg):self.probe(code,patches=[(0x4df,b'\xcd\x21')]).run('bfnt',[0x200,0x5000,0x1234])
        for portcode in (b'\xe6\xa9',b'\xe7\xa8'):
            with self.assertRaisesRegex(ValueError,'unknown output port/site/width'):self.probe(jump(0x17d0,0x1803),0x17d0,[(0x1803,portcode)]).run('show')

    def test_native_entries_return_frames_cleanup_and_df(self):
        with self.assertRaisesRegex(ValueError,'native far frame'):self.probe(jump(0x4c6,0xaae)).run('bfnt',[0x200,0x5000,0x1234])
        code=b'\x83\xc4\x02'+jump(0x4c9,0x503)
        with self.assertRaisesRegex(ValueError,'native return frame'):self.probe(code).run('bfnt',[0x200,0x5000,0x1234])
        with self.assertRaisesRegex(ValueError,'far cleanup/callee-saved'):self.probe(jump(0x4c6,0x503),patches=[(0x503,b'\xca\x04\x00')]).run('bfnt',[0x200,0x5000,0x1234])
        with self.assertRaisesRegex(ValueError,'DF differs'):self.probe(jump(0x17d0,0x18d9),0x17d0,s=dict(df=True)).run('show')
        p=self.probe(b'\xfc'+jump(0x17d1,0x18d9),0x17d0,s=dict(df=True));p.run('show');self.assertFalse(p.get('EFLAGS')&0x400)

    def test_stale_completion_and_segment_aliases(self):
        p=self.probe(jump(0x4c6,0x503));p.run('bfnt',[0x200,0x5000,0x1234]);p.uc.mem_write(p.code+0x4c6,b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('bfnt',[0x200,0x5000,0x1234],budget=50)
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\xff\x1f').run('bfnt',[0x200,0x5000,0x1234])
        with self.assertRaisesRegex(ValueError,'escaped palette bodies/segment alias'):self.probe(b'\xea\xd6\x04\xff\x1f').run('bfnt',[0x200,0x5000,0x1234])


if __name__=='__main__':unittest.main()
