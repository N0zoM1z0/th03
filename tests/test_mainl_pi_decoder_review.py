"""Decoder ownership, real private/far frames, service and memory span guards."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from test_mainl_smem_review import fixture as context_fixture
import review_th03_mainl_pi_decoder as d


def fixture():
    data = context_fixture()
    for _, start, size, cleanup in d.OWN_RANGES + [('dos_open',0xaae,26,4)]:
        data[start:start+size] = b'\x90'*size
        tail = b'\xc3' if cleanup == 'near' else b'\xca'+struct.pack('<H',cleanup)
        data[start+size-len(tail):start+size] = tail
    for address,value in d.ALIGNMENT.items():
        data[address] = value
    return data


def jump(address,target):
    return b'\xe9'+struct.pack('<h',target-address-3)


class DecoderBoundaryTests(unittest.TestCase):
    def test_complete_partition_shared_error_tail_and_cleanup(self):
        meta=d.analyze(fixture())
        self.assertEqual((meta['new_body_bytes'],meta['new_extent_bytes'],meta['prior_context_bytes']),(1598,1600,730))
        for address in (0x1035,0x1040,0x14fc,0x15ed,0x1619,0x162b):
            data=fixture();data[address]=0x90
            with self.assertRaisesRegex(ValueError,'terminal cleanup'):
                d.analyze(data)
        data=fixture();data[0x1044:0x1047]=jump(0x1044,0x1038)
        d.analyze(data)
        data=fixture();data[0x1044]=0xc3
        with self.assertRaisesRegex(ValueError,'interior cleanup'):
            d.analyze(data)

    def test_edges_reject_operands_neighbors_and_unknown_helpers(self):
        for code,message in ((jump(0x1044,0x1045),'branch enters'),(jump(0x1044,0x162c),'branch enters'),
                             (b'\xe8\x00\x00','unknown native call'),(b'\xff\xd0','unknown indirect'),
                             (b'\x9a\x00\x00\x00\x00','unknown far')):
            data=fixture();data[0x1044:0x1044+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):d.analyze(data)
        data=fixture();data[0x1052:0x1055]=b'\xe8'+struct.pack('<h',0xaae-0x1055)
        with self.assertRaisesRegex(ValueError,'lacks PUSH CS'):d.analyze(data)
        data[0x1051]=0x0e;d.analyze(data)

    def test_dos_sites_ports_and_alignment(self):
        for code,address,message in ((b'\xcd\x20',0x107e,'unknown DOS'),(b'\xcd\x21',0x1044,'unknown DOS'),
                                     (b'\xe6\x60',0x1044,'unexpected port'),(b'\xe4\x60',0x1044,'unexpected port')):
            data=fixture();data[address:address+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):d.analyze(data)
        for address in d.ALIGNMENT:
            data=fixture();data[address]=0
            with self.assertRaisesRegex(ValueError,'producer alignment'):d.analyze(data)

    def test_fixture_grammar_validation(self):
        self.assertEqual(d.color_bits(0),'10')
        self.assertEqual(d.color_bits(15),'011111')
        self.assertEqual(d.copy_bits(4,8),'1111110000')
        for fn,values in ((d.color_bits,(-1,16)),(d.position_bits,(-1,5)),(d.length_bits,(0,1<<32))):
            for value in values:
                with self.assertRaisesRegex(ValueError,'outside'):fn(value)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class DecoderRuntimeTests(unittest.TestCase):
    def probe(self,code=b'',address=0x1044,patches=(),scenario=None):
        __import__('unicorn')
        data=fixture();meta=d.analyze(data);data[address:address+len(code)]=code
        for address,code in patches:data[address:address+len(code)]=code
        return d.DecoderProbe(SimpleNamespace(program_image=data,relocations=[]),scenario or {},meta)

    def test_real_near_return_frame_and_private_entry_rejection(self):
        call=b'\xe8'+struct.pack('<h',0x15ee-0x10a4)
        p=self.probe(jump(0x1044,0x10a1),patches=[(0x10a1,call),(0x10a4,jump(0x10a4,0x14fc)),(0x15ee,jump(0x15ee,0x1619))])
        p.run('load',d.LOAD_ARGS)
        self.assertEqual(dict(p.native),dict(load=1,read_byte=1))
        for name in ('read_byte','read_color','refill','free','error'):
            with self.assertRaisesRegex(ValueError,'complete public caller'):p.run(name)
        with self.assertRaisesRegex(ValueError,'native entry frame'):
            self.probe(jump(0x1044,0x15ee)).run('load',d.LOAD_ARGS)
        with self.assertRaisesRegex(ValueError,'native return frame'):
            self.probe(b'\x83\xc4\x02'+jump(0x1047,0x14fc)).run('load',d.LOAD_ARGS)

    def test_real_far_call_cleanup_and_shared_error_return(self):
        call=b'\x50\x0e\xe8'+struct.pack('<h',0x22b2-0x1002)
        p=self.probe(jump(0xfec,0xffd),0xfec,[(0xffd,call),(0x1002,jump(0x1002,0x1035))])
        p.run('graph_free',[0,0,0x200,0x5000])
        self.assertEqual(dict(p.native),dict(graph_free=1,free=1))
        p=self.probe(jump(0x1044,0x1038));p.run('load',d.LOAD_ARGS)
        self.assertEqual(p.get('SP'),0xffd0)

    def test_unknown_services_and_whole_store_spans_outside_ffi(self):
        for code,message in ((b'\xcd\x21','unknown DOS request/site'),(b'\xe6\x60','unexpected output'),
                             (b'\xe4\x60','unexpected input'),(b'\xb8\x00\xa0\x8e\xc0\x26\xc7\x06\x00\x00\x01\x00','outside declared')):
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):self.probe(code).run('load',d.LOAD_ARGS)
            self.assertEqual(stderr.getvalue(),'')
        code=b'\xb4\x3e\xcd\x21'
        with self.assertRaisesRegex(ValueError,'unknown DOS request/site'):
            self.probe(jump(0x1044,0x107c),patches=[(0x107c,code)]).run('load',d.LOAD_ARGS)

    def test_budget_stale_completion_and_segment_aliases(self):
        p=self.probe(jump(0x1044,0x14fc));p.run('load',d.LOAD_ARGS)
        p.uc.mem_write(p.code+0x1044,b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('load',d.LOAD_ARGS,budget=50)
        self.assertFalse(p.stop)
        for code,message in ((b'\xea\x10\xff\xff\x1f','terminal segment alias'),(b'\xea\x54\x10\xff\x1f','CODE/stack segment alias'),
                             (jump(0x1044,0x162c),'instruction boundaries')):
            with self.assertRaisesRegex(ValueError,message):self.probe(code).run('load',d.LOAD_ARGS)

    def test_byte_prefix_pause_leaves_real_public_frame_open(self):
        call=b'\xe8'+struct.pack('<h',0x15ee-0x10a4)
        p=self.probe(jump(0x1044,0x10a1),patches=[(0x10a1,call)],scenario=dict(pause_after_bytes=0))
        p.run('load',d.LOAD_ARGS)
        self.assertTrue(p.paused);self.assertFalse(p.stop)
        self.assertEqual((p.get('IP'),p.pending['name'],len(p.frames)),(0x15ee,'read_byte',1))

    def test_unobserved_control_memory_mutant_is_detected(self):
        p=self.probe(scenario=dict(flags=2));model=d.Scalar(p)
        d.compare(p,model,None,None,'unchanged fixture')
        p.uc.mem_write(0x6400c,b'\xff')
        with self.assertRaisesRegex(ValueError,'full physical memory differs'):
            d.compare(p,model,None,None,'color-table mutant')


if __name__=='__main__':unittest.main()
