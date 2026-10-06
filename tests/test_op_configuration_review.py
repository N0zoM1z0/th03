"""Portable OP contract controls; encoded fixtures never become product source."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import review_th03_op_configuration as d


def fixture():
    image=bytearray(0xd7f0+0x3000)
    for name,seg,a,cold,z,cleanup,owner in d.RANGES:
        at=seg*16+a;image[at:at+z]=b'\x90'*z
        tail=b'\xc3' if cleanup=='near' else b'\xca'+struct.pack('<H',cleanup) if cleanup else b'\xcb'
        image[at+z-len(tail):at+z]=tail
    at=d.SHARED*16+0x21
    body=b'\x55\x8b\xec'
    for i,v in enumerate((0xa8000000,0xb0000000,0xb8000000,0xe0000000)):
        body+=b'\x66\xc7\x06'+struct.pack('<HI',d.PLANES+i*4,v)
    image[at:at+41]=body+b'\x5d\xcb'
    image[d.SHARED*16+0x67]=0x90
    at=d.SHARED*16+8
    image[at:at+25]=b'\x55\x8b\xec\x90\x0e\xe8\x02\x01'+b'\x9a\x2e\x1a\0\0\x9a\x38\x22\0\0\x9a\x2c\x22\0\0\x5d\xcb'
    at=d.GROUP*16+0xc3
    start=b'\xc8\x08\0\0\x8d\x46\xf8\x16\x50\x1e\x68\x91\0\xb9\x08\0\x9a\x7e\x33\0\0'
    image[at:at+len(start)]=start;image[at+82:at+84]=b'\xc9\xc3'
    image[0x337e:0x339a]=b'\x55\x8b\xec\x56\x57\x1e\xc5\x76\x06\xc4\x7e\x0a\xfc\xd1\xe9\xf3\xa5\x13\xc9\xf3\xa4\x1f\x5f\x5e\x5d\xca\x08\0'
    image[d.SHARED*16+0x4a:d.SHARED*16+0x4e]=b'\xb4\x09\xcd\x60'
    at=d.GROUP*16+8;image[at:at+5]=b'\x9a\x4a\0\xeb\x0b'
    return image


class BoundaryTests(unittest.TestCase):
    def test_complete_near_far_functions_cleanup_and_producer(self):
        image=fixture();self.assertEqual(len(d.analyze(image)['bodies']),8)
        for name,seg,a,cold,z,cleanup,owner in d.RANGES:
            mutant=fixture();mutant[seg*16+a+z-1]=0x90
            with self.assertRaisesRegex(ValueError,'complete function'):d.analyze(mutant)
        image[d.SHARED*16+0x67]=0
        with self.assertRaisesRegex(ValueError,'sound producer'):d.analyze(image)

    def test_bad_edges_native_frame_unknown_calls_and_devices(self):
        for code,message in [(b'\xeb\xff','operand/neighbor'),(b'\xff\xe0','indirect/operand'),
                             (b'\xe8\x16\0','native far frame'),(b'\x9a\xff\xff\0\0','unknown call'),
                             (b'\xcd\x21','device instruction')]:
            image=fixture();at=d.GROUP*16+8;image[at:at+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):d.analyze(image)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class NativeTests(unittest.TestCase):
    def probe(self,scenario=None):
        __import__('unicorn')
        image=fixture();relocs=[]
        for row in d.analyze(image)['bodies']:
            for edge in row['edges']:
                if edge['kind']=='lcall':relocs.append(SimpleNamespace(segment=row['segment'],offset=edge['site']+3))
        return d.ConfigurationProbe(SimpleNamespace(program_image=image,relocations=relocs),scenario or {})

    def test_native_copy_clears_df_and_preserves_near_caller_frame(self):
        p=self.probe(dict(df=True));p.run('cfg_save_exit')
        self.assertEqual(bytes(p.uc.mem_read(p.stack+0xffc6,8)),b'\0'*8)
        self.assertFalse(p.get('EFLAGS')&0x400);self.assertEqual(p.native['scopy'],1)
        self.assertEqual(p.helpers,[]);self.assertEqual(p.get('SP'),0xffd2)
        for name in ('scopy','snd_mode'):
            with self.assertRaisesRegex(ValueError,'complete public caller'):p.run(name)

    def test_mode_driver_contract_and_unexpected_interrupt_are_guarded(self):
        p=self.probe(dict(driver=0xfe));p.run('cfg_load')
        self.assertEqual(p.drivers,[dict(number=96,ah=9,reply=254)])
        p=self.probe();p.uc.mem_write(0x20000+d.SHARED*16+0x4c,b'\xcd\x21');stderr=io.StringIO()
        with redirect_stderr(stderr):
            with self.assertRaisesRegex(ValueError,'unexpected interrupt'):p.run('cfg_load')
        self.assertEqual(stderr.getvalue(),'')

    def test_declared_store_full_spans_segment_alias_and_far_return(self):
        for code,message in [(b'\xc7\x06'+struct.pack('<H',d.PLANES+15)+b'\x01\0','complete declared span'),
                             (b'\xea\x31\0\xea\x2b','CODE segment alias'),
                             (b'\x83\xc4\x02','far native return frame')]:
            p=self.probe();p.uc.mem_write(0x20000+d.SHARED*16+0x21,code)
            with self.assertRaisesRegex(ValueError,message):p.run('planes')

    def test_modeled_interface_callers_cannot_change_to_another_known_model(self):
        p=self.probe();p.uc.mem_write(0x20000+d.SHARED*16+0x10,b'\x9a\x38\x22\0\x20')
        with self.assertRaisesRegex(ValueError,'interface caller frame'):p.run('exit_dos')

    def test_stale_terminal_and_branch_operand_do_not_pass(self):
        p=self.probe();p.run('planes');p.uc.mem_write(0x20000+d.SHARED*16+0x21,b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('planes',budget=20)
        p=self.probe();p.uc.mem_write(0x20000+d.SHARED*16+0x21,b'\xeb\xff')
        with self.assertRaisesRegex(ValueError,'instruction boundary'):p.run('planes')

    def test_native_helper_stack_corruption_is_rejected(self):
        p=self.probe();p.uc.mem_write(0x20000+0x3381,b'\x44')
        with self.assertRaisesRegex(ValueError,'native return frame|helper return|instruction boundary'):p.run('cfg_save_exit')


if __name__=='__main__':unittest.main()
