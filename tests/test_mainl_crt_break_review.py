"""Guard CRT ownership, library framing, near/far bridges and failure state."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import review_th03_mainl_crt_break as d


def fixture():
    data=bytearray(0xe3f0+0x1200)
    for name,a,z,c in d.RANGES:
        data[a:a+z]=b'\x90'*z
        if c=='bridge': data[a:a+z]=b'\x5b\x0e\x53' if name=='shift_near' else b'\x07\x0e\x06'
        else:
            tail=(b'\xc2'+struct.pack('<H',c[1]) if c[1] else b'\xc3') if isinstance(c,tuple) else b'\xcb'
            data[a+z-len(tail):a+z]=tail
    for site,name in d.CALLS.items():
        data[site:site+3]=b'\xe8'+struct.pack('<h',d.ENTRY[name]-site-3)
        if name=='setblock': data[site-1]=0x0e
    return data


def jump(address,target): return b'\xe9'+struct.pack('<h',target-address-3)
def record(kind,payload):
    block=bytes([kind])+struct.pack('<H',len(payload)+1)+payload
    return block+bytes([-sum(block)&255])
def library():
    data=bytearray(16); data[0]=0xf0; data[1:3]=(13).to_bytes(2,'little')
    for name,(_,start,size) in d.MEMBERS.items():
        module=record(0x80,bytes([len(name)])+name.encode())
        module+=record(0x88,b'\x00\xa3'+bytes([len(name.split('.')[0])])+name.split('.')[0].encode())
        module+=record(0x98,b'\x28'+struct.pack('<H',size)+b'\x02\x03\x01')
        module+=record(0xa0,b'\x01\x00\x00'+bytes(fixture()[start:start+size]))
        module+=record(0x8a,b'\x00')
        data.extend(module); data.extend(b'\x00'*((-len(data))%16))
    data[3:7]=len(data).to_bytes(4,'little'); data.extend(b'\x00'*16)
    return data


class BoundaryTests(unittest.TestCase):
    def test_symbolic_fixups_relaxation_and_rejected_ownership(self):
        def member(code,fixups):
            return dict(records=[(0x8c,b'\x06symbol\x00',0,0),(0xa0,b'\x01\x00\x00'+code,0,0),(0x9c,fixups,0,0)])
        code,fixups=d.linked_member(member(b'\xe8\0\0',b'\x84\x01\x06\x01\x01'),0x100,None,dict(symbol=(0,0x300)))
        self.assertEqual(code,b'\xe8\xfd\x01'); self.assertEqual(fixups[0]['action'],'self-relative CODE')
        code,fixups=d.linked_member(member(b'\x9a\0\0\0\0',b'\xcc\x01\x56\x01'),0x100,None,dict(symbol=(0,0x300)))
        self.assertEqual(code,b'\x90\x0e\xe8\xfb\x01')
        for code,fixups,symbols,message in ((b'\xe8\0\0',b'\x84\x01\x86\x01\x01',dict(symbol=(0,0x300)),'method/thread'),
                                           (b'\xe8\0\0',b'\x84\x02\x06\x01\x01',dict(symbol=(0,0x300)),'exceeds declared'),
                                           (b'\x9a\0\0\0\0',b'\xcc\x01\x56\x01',dict(symbol=(1,0x300)),'relaxation precondition'),
                                           (b'\xe8\0\0',b'\x84\x01\x06\x01\x01'*2,dict(symbol=(0,0x300)),'overlapping fixup')):
            with self.assertRaisesRegex(ValueError,message): d.linked_member(member(code,fixups),0x100,None,symbols)

    def test_complete_partition_bridges_and_cleanup(self):
        data=fixture(); self.assertEqual(d.analyze(data)['owned_code_bytes'],628)
        for name,a,z,c in d.RANGES:
            modified=fixture(); modified[a+z-1]^=1 if c=='bridge' else 0x90
            with self.assertRaises(ValueError): d.analyze(modified)
        data=fixture(); data[0x3182]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'): d.analyze(data)

    def test_only_known_native_edges_services_and_far_call_prefix(self):
        for code,message in ((jump(0x3182,0x3183),'operand/neighbor'),(jump(0x3182,0x357c),'operand/neighbor'),
                             (b'\xe8\x00\x00','native call'),(b'\xff\xd0','indirect edge'),(b'\xcd\x21','unexpected interrupt'),
                             (b'\xe6\x7c','unexpected port')):
            data=fixture(); data[0x3182:0x3182+len(code)]=code
            with self.assertRaisesRegex(ValueError,message): d.analyze(data)
        data=fixture(); data[0x3ebd]=0x90
        with self.assertRaisesRegex(ValueError,'lacks PUSH CS'): d.analyze(data)

    def test_library_code_checksum_bounds_and_narrow_comment_exception(self):
        data=library(); self.assertEqual(set(d.library_members(data)),set(d.MEMBERS))
        # Deliberately stale librarian name comments are reported, not repaired.
        name=next(iter(d.MEMBERS)); comment=record(0x88,b'\x00\xa3'+bytes([len(name.split('.')[0])])+name.split('.')[0].encode())
        at=data.index(comment); data[at+len(comment)-1]^=1
        self.assertEqual(len(d.library_members(data)[name]['checksum_exceptions']),1)
        data=library(); needle=b'\xa0'+struct.pack('<H',d.MEMBERS[name][2]+4)+b'\x01\x00\x00'; at=data.index(needle); data[at+6]^=1
        with self.assertRaisesRegex(ValueError,'non-comment checksum'): d.library_members(data)
        data=library(); data[1:3]=(12).to_bytes(2,'little')
        with self.assertRaisesRegex(ValueError,'page/dictionary'): d.library_members(data)
        data=library(); data[3:7]=(len(data)+1).to_bytes(4,'little')
        with self.assertRaisesRegex(ValueError,'page/dictionary'): d.library_members(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class NativeControlTests(unittest.TestCase):
    def probe(self,patches=(),scenario=None):
        __import__('unicorn'); data=fixture(); meta=d.analyze(data)
        for a,code in patches: data[a:a+len(code)]=code
        return d.BreakProbe(SimpleNamespace(program_image=data,relocations=[]),scenario or {},meta)

    def test_real_near_to_far_bridges_and_private_helper_rejection(self):
        for name in ('shift_near','add_near','sub_near','shift_far','add_far','sub_far'):
            p=self.probe(); p.run(name)
            self.assertEqual(p.get('SP'),0xffc4 if name.endswith('_far') else 0xffc2)
        with self.assertRaisesRegex(ValueError,'complete public caller'): self.probe().run('grow',[0,0])
        with self.assertRaisesRegex(ValueError,'native entry frame'): self.probe([(0x3efe,jump(0x3efe,0x3e70))]).run('brk',[0,0])

    def test_bridge_return_frames_services_and_store_spans(self):
        __import__('unicorn')
        for address,code,name,message in ((0x3161,b'\xc3','shift_near','unfinished native frame'),(0x3182,b'\x83\xc4\x02','add_near','return frame'),
                                         (0x3efe,b'\xcd\x21','brk','unknown DOS'),(0x3efe,b'\xe4\x60','brk','port interface'),
                                         (0x3efe,b'\xc7\x06\x7f\x00\x01\x00','brk','complete state span')):
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message): self.probe([(address,code)]).run(name)
            self.assertEqual(stderr.getvalue(),'')

    def test_stale_completion_and_segment_aliases(self):
        p=self.probe([(0x3efe,jump(0x3efe,0x3f40))]); p.run('brk')
        p.uc.mem_write(p.code+0x3efe,b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'): p.run('brk',budget=20)
        with self.assertRaisesRegex(ValueError,'segment alias'): self.probe([(0x3efe,b'\xea\x10\xff\xff\x1f')]).run('brk')


class ScalarContractTests(unittest.TestCase):
    def model(self,scenario=None):
        # Runtime state comes from a diagnostic fixture, never a target file.
        p=NativeControlTests().probe(scenario=scenario); return d.Scalar(p)

    @unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
    def test_negative_megabyte_increment_can_alias_the_current_break(self):
        m=self.model(); self.assertEqual(m.run('sbrk',[0,65520]),dict(ax=0,dx=0x6100))
        self.assertEqual(m.pointer(d.BREAK),(0,0x6100)); self.assertFalse(m.events)
        self.assertEqual(m.run('sbrk',[0,16]),dict(ax=65535,dx=65535))

    @unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
    def test_failed_setblock_bx_ffff_collides_with_success_sentinel(self):
        m=self.model(dict(granule=0,replies=[dict(cf=1,ax=8,bx=65535)]))
        self.assertEqual(m.run('brk',[0,0x6200]),dict(ax=0))
        self.assertEqual(m.pointer(d.BREAK),(0,0x6200)); self.assertEqual(m.word(d.DOSERR),8)
        self.assertEqual(m.word(d.GRANULE),0x49)

    @unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
    def test_failed_setblock_changes_top_without_advancing_break(self):
        m=self.model(dict(granule=0,replies=[dict(cf=1,ax=8,bx=0x1234)]))
        self.assertEqual(m.run('brk',[0,0x6200]),dict(ax=65535))
        self.assertEqual(m.pointer(d.BREAK),(0,0x6100)); self.assertEqual(m.pointer(d.TOP),(0,0x6234)); self.assertEqual(m.word(d.GRANULE),0)
        self.assertEqual([z[0]-m.data for z in m.writes],[d.DOSERR,d.ERRNO,d.TOP+2,d.TOP])

    @unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
    def test_signed_error_int_min_and_pointer_normalization(self):
        m=self.model(); m.error(32768)
        self.assertEqual((m.word(d.ERRNO),m.word(d.DOSERR)),(32768,65535))
        self.assertEqual(d.normalized_pointer(65535,65535),(4094,15))
        self.assertEqual(d.pointer_add(65535,65535,1),(0,4095))


if __name__=='__main__': unittest.main()
