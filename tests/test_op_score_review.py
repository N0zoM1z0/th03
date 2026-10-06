"""Score format specification and guarded native/public-call boundaries."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import review_th03_op_score as d


def fixture():
    image=bytearray(d.DS*16+0x3000)
    for name,seg,a,z,cleanup,owner in d.RANGES:
        at=seg*16+a;image[at:at+z]=b'\x90'*z
        tail=b'\xcb' if cleanup=='far' else b'\xc2'+struct.pack('<H',cleanup) if cleanup else b'\xc3'
        image[at+z-len(tail):at+z]=tail
    image[d.DS*16+d.FNPTR:d.DS*16+d.FNPTR+2]=struct.pack('<H',0xa04)
    image[d.DS*16+0xa04:d.DS*16+0xa0d]=b'YUME.NEM\0'
    return image


class BoundaryAndFormatTests(unittest.TestCase):
    def test_complete_functions_and_interior_cleanup(self):
        self.assertEqual(len(d.analyze(fixture())['bodies']),6)
        for name,seg,a,z,cleanup,owner in d.RANGES:
            data=fixture();data[seg*16+a+z-1]=0x90
            with self.assertRaisesRegex(ValueError,'complete body'):d.analyze(data)
        data=fixture();data[d.CS*16+0x1868]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):d.analyze(data)

    def test_bad_edges_calls_and_devices(self):
        for code,message in [(b'\xeb\xff','operand/neighbor'),(b'\xff\xe0','indirect/operand'),
                             (b'\xe8\0\0','unknown native/model'),(b'\xcd\x21','device/interrupt')]:
            data=fixture();data[d.CS*16+0x1868:d.CS*16+0x1868+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):d.analyze(data)

    def test_independent_known_format_vectors_and_rank_wrap(self):
        data=bytearray(206);data[204:]=b'\x01\x02'
        self.assertEqual(d.encrypt(data)[200:204],bytes.fromhex('4bb542fd'))
        self.assertEqual(d.decrypt(d.encrypt(data)),data)
        spec=d.ScoreSpec(d.sample(),1,{},0,[0xa04,0x2d7f]);spec.encode(65535)
        self.assertEqual(next(e['args'] for e in spec.events if e['name']=='seek'),[0,65330,0])
        self.assertEqual(d.next_random(1),(22695478,346))

    def test_recreated_flags_and_stale_read_return_are_retained(self):
        data=bytearray(d.sample());data[82]=99;valid=d.encrypt(d.sealed(data))
        spec=d.ScoreSpec(valid,1,dict(read_hex='',exists=65535),0,[0xa04,0x2d7f])
        self.assertEqual(spec.load(0),0);self.assertEqual(spec.data[82],99)
        spec=d.ScoreSpec(valid,1,dict(exists=0),0,[0xa04,0x2d7f])
        self.assertEqual(spec.load(0),1);self.assertEqual(spec.data[82],18)
        self.assertEqual([e['args'][1] for e in spec.events if e['name']=='seek'],[0,206,412,618])


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class NativeTests(unittest.TestCase):
    def probe(self):
        __import__('unicorn')
        return d.ScoreProbe(SimpleNamespace(program_image=fixture(),relocations=[]),d.sample(),1,{})

    def test_native_far_and_near_caller_frames(self):
        p=self.probe();p.run('irand');self.assertEqual(p.get('SP'),0xffd4)
        p=self.probe();p.run('encode',[3]);self.assertEqual(p.get('SP'),0xffd4)
        p=self.probe();p.run('decode');self.assertEqual(p.get('SP'),0xffd2)

    def test_full_span_and_segment_alias_are_rejected_without_ffi_errors(self):
        for code,message in [(b'\xc7\x06'+struct.pack('<H',d.HI+d.SIZE-1)+b'\x01\0','complete declared span'),
                             (b'\xea\x78\x18\x8f\x29','CODE segment alias'),(b'\xcd\x21','unexpected interrupt')]:
            p=self.probe();p.uc.mem_write(p.code+0x1868,code);stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):p.run('encode',[1])
            self.assertEqual(stderr.getvalue(),'')

    def test_native_return_cleanup_and_stale_completion_are_rejected(self):
        p=self.probe();p.uc.mem_write(p.code+0x1868,b'\x83\xc4\x02')
        with self.assertRaisesRegex(ValueError,'native return frame'):p.run('encode',[1])
        p=self.probe();p.run('decode');p.uc.mem_write(p.code+0x190d,b'\x90\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('decode',budget=10)

    def test_model_destination_requires_its_original_complete_caller(self):
        p=self.probe();p.uc.mem_write(p.code+0x1868,b'\x9a\xd8\x08\0\x20')
        with self.assertRaisesRegex(ValueError,'interface caller'):p.run('encode',[0])


if __name__=='__main__':unittest.main()
