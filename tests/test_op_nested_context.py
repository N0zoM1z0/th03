"""Physical caller-frame inputs, arbitrary saved registers and static reentry."""
from dataclasses import replace
from pathlib import Path
import struct,sys,unittest
from unicorn import x86_const as x
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from lib.op_nested_context import Context,GPRS,SEGMENTS
from lib.op_dispatch_runtime import Machine as Dispatch
from lib.op_attract_runtime import Machine as Attract
from lib.op_vs_runtime import Machine as VS
from lib.op_story_runtime import Machine as Story
from review_th03_op_cfg_work import images
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP'
@unittest.skipUnless((WORK/'bin/th03/op.exe').is_file(),'private current OP absent')
class Nested(unittest.TestCase):
    @classmethod
    def setUpClass(cls):_,cls.target,*_=images(ROOT)
    def prepare(self,cls,*,reset=True,m=None):
        if m is None:m=cls(self.target,0x3000);self.addCleanup(m.close)
        if reset:m.uc.mem_write(0,bytes(m.initial))
        stack=0xF7FA;physical=0x70000+stack;resident=0x60031
        m.uc.mem_write(physical-80,b'\xD3'*80);m.uc.mem_write(physical,struct.pack('<H',0x887));m.uc.mem_write(m.data+0x2464,struct.pack('<HH',0x31,0x6000))
        if reset:
            m.uc.mem_write(resident,b'\xA5'*0x60)
            for at,value in ((m.data+0x5DC,1),(m.data+0x1A0B,1),(resident+0x28,0),(resident+0x15,1),(resident+0x16,2),(resident+0xB,3)):
                m.uc.mem_write(at,bytes((value,)))
        registers={n:0x3412+i*0x123 for i,n in enumerate(GPRS)};registers['sp']=stack
        registers.update(cs=m.cs,ds=m.ds,es=0x4321,ss=0x7000,fs=0xA596,gs=0x5A69)
        full={n:0xABCD0000|registers[n] for n in GPRS}
        for n,r in GPRS.items():m.uc.reg_write(r,full[n])
        for n,r in SEGMENTS.items():m.uc.reg_write(r,registers[n])
        m.uc.reg_write(x.UC_X86_REG_EFLAGS,0xED7)
        return m,Context(bytearray(m.uc.mem_read(0,1<<20)),registers,full,0xED7,0x8D5,stack,m.cs*16+0x887)
    def test_all_four_callees_use_the_original_UC_and_return_word(self):
        for cls in (Dispatch,Attract,VS,Story):
            m,ctx=self.prepare(cls);uc=m.uc
            if cls==Dispatch:m.run('score_menu',_context=ctx)
            else:m.run(_context=ctx)
            self.assertIs(m.uc,uc);result=m.contract_result
            self.assertEqual(result['registers']['sp'],ctx.stack+2)
            self.assertEqual(result['registers']['si'],ctx.registers['si'])
            self.assertEqual(result['full_registers']['sp']>>16,0xABCD)
            self.assertEqual(bytes(m.uc.mem_read(0x70000+ctx.stack,2)),struct.pack('<H',0x887))
    def test_input_mismatch_rejects_before_any_fixture_or_guest_store(self):
        m,ctx=self.prepare(Story);before=bytes(m.uc.mem_read(0,1<<20))
        bad=replace(ctx,full_registers=dict(ctx.full_registers,ax=ctx.full_registers['ax']^1))
        with self.assertRaisesRegex(ValueError,'entering DWORD'):m.run(_context=bad)
        self.assertEqual(bytes(m.uc.mem_read(0,1<<20)),before)
        bad_memory=bytearray(ctx.memory);bad_memory[0x60031]^=1
        with self.assertRaisesRegex(ValueError,'physical input'):m.run(_context=replace(ctx,memory=bad_memory))
        self.assertEqual(bytes(m.uc.mem_read(0,1<<20)),before)
    def test_actual_story_reentry_keeps_seen_state_and_closes_the_loop(self):
        m,ctx=self.prepare(Story);first=m.run(_context=ctx,selection_ax=0)
        self.assertFalse(first['nonterminal']);self.assertEqual(sum(bool(v) for v in first['seen']),6)
        m,ctx=self.prepare(Story,m=m,reset=False);second=m.run(_context=ctx,selection_ax=0)
        self.assertTrue(second['nonterminal']);self.assertTrue(m.contract_result['held'])
        self.assertEqual(m.contract_result['registers']['sp'],ctx.stack-8)
    def test_score_preserves_external_file_tail_and_live_private_cfg_BYTE(self):
        m,ctx=self.prepare(Dispatch);tail=b'preserved tail\0\xA7';ctx=replace(ctx,file=b'abcd'+tail)
        m.run('score_menu',_context=ctx)
        self.assertEqual(m.contract_result['file'],b'\1\2\3\xD3'+tail)
        self.assertEqual(m.contract_result['registers']['bp'],ctx.registers['bp'])
