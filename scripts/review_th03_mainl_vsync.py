#!/usr/bin/env python3
"""Complete MAINL VSYNC installation/handlers plus native vector/mode helpers."""
import argparse
from collections import Counter
from datetime import datetime,timezone
from importlib.metadata import version
import json
from pathlib import Path
import struct
import subprocess
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact
from review_th03_decoded_code import code_rows,extent_observation
from review_th03_mainl_cutscene import Probe,REVISION,sha
from review_th03_mainl_snow import u16
from review_th03_mainl_heap import cached_provider,BUILD_REMAPS
from review_th03_mainl_palette import PROVIDERS as PALETTE_PROVIDERS

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-mainl-palette-review-20261006.json'
PROOF_SHA256='24faf33ba4e44f0f700f3b033f98a07bb95d3914c7c9fe5d79cfc41dade0c388'
RANGES=[('start',0x1f6e,106,0),('crt',0x1fd8,9,None),('irq',0x1fe2,58,None),
 ('end',0x201c,71,0),('vector',0x704,31,6),('mode',0xf02,86,4),('wait',0x2064,38,0)]
ALIGNMENT={0x1fe1:0x90,0x2063:0x90,0x723:0x90}
CALLS={0x1f73:0xf02,0x1fa2:0x704,0x1fc9:0x704,0x2033:0x704,0x204d:0x704}
INDIRECT={0x1fd9:b'\x2e\xff\x1e\x6a\x1f',0x2008:b'\xff\x1e\x42\x08'}
BIOS={0xf1a:0x31,0xf2e:0x30,0xf3a:0x0c,0xf45:0x0e,0xf51:0x11}
DOS={0x712:0x35,0x716:0x25}
IN_PORTS={0x1fae:2,0x2038:2,0x2052:2,0x206f:0xa0,0x2079:0xa0}
OUT_PORTS={0x1fb4:2,0x1fd5:0x64,0x1fde:0x64,0x2016:0,0x2018:0x64,0x203c:2,0x2058:2,0x205b:0x64}
PROC,DELAY,MASK,COUNT1,COUNT2,OLDVECT,ACC,TEXT,RAW=0x842,0x846,0x848,0x144e,0x1450,0x1452,0x1456,0x840,0x1f6a
STARTS={a:n for n,a,_,_ in RANGES}
PROVIDERS=list(dict.fromkeys(PALETTE_PROVIDERS+['libs/master.lib/'+p for p in ('vsync.asm','vsync[bss].asm','dos_setvect.asm','graph_extmode.asm','tx[data].asm')]))
GPRS=('AX','BX','CX','DX','BP','SI','DI','DS','ES')


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[];returns={};bounds=set()
    for name,a,z,cleanup in RANGES:
        body=image[a:a+z]
        if len(body)!=z:raise ValueError('vsync complete include body differs')
        ins=list(decoder.disasm(body,a));local={i.address for i in ins};bounds|=local;edges=[]
        tail=('iret','') if cleanup is None else ('retf',str(cleanup) if cleanup else '')
        if not ins or sum(i.size for i in ins)!=z or (ins[-1].mnemonic,ins[-1].op_str)!=tail:raise ValueError('vsync complete body/terminal cleanup differs')
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf','iret'):
                if (i.mnemonic,i.op_str)!=tail:raise ValueError('vsync interior return differs')
                returns[i.address]=(name,cleanup)
            if i.mnemonic in ('in','out'):
                sites=IN_PORTS if i.mnemonic=='in' else OUT_PORTS
                if i.address not in sites:raise ValueError('vsync unknown port site')
                edges.append(dict(instruction=i.address,kind=i.mnemonic,port=sites[i.address]));continue
            if i.mnemonic=='int':
                if not (i.address in BIOS and i.bytes==b'\xcd\x18' or i.address in DOS and i.bytes==b'\xcd\x21'):raise ValueError('vsync unknown interrupt site')
                edges.append(dict(instruction=i.address,kind='modeled-service',number=i.operands[0].imm));continue
            if i.address in INDIRECT:
                if i.bytes!=INDIRECT[i.address]:raise ValueError('vsync declared indirect operand differs')
                edges.append(dict(instruction=i.address,kind='declared-external-far-call'));continue
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('vsync unknown indirect edge')
            if i.mnemonic in ('lcall','ljmp'):raise ValueError('vsync unknown far edge')
            dest=i.operands[0].imm
            if i.mnemonic=='call':
                if CALLS.get(i.address)!=dest:raise ValueError('vsync unknown native call site/target')
                if not j or ins[j-1].bytes!=b'\x0e':raise ValueError('vsync far call lacks PUSH CS')
            elif dest not in local:raise ValueError('vsync branch enters data/operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=a,size=z,instructions=len(ins),sha256=sha(body),cleanup=cleanup,edges=edges))
    if any(image[a:a+1]!=bytes([v]) for a,v in ALIGNMENT.items()):raise ValueError('vsync producer alignment differs')
    if image[RAW:RAW+4]!=b'\0'*4:raise ValueError('vsync initial CS saved-vector state differs')
    if image[0x1fe4:0x1fe7]!=b'\xb8\x3f\x0e':raise ValueError('vsync original DGROUP relocation operand differs')
    return dict(bodies=rows,returns=returns,instruction_boundaries=sorted(bounds),vsync_body_bytes=244,cs_state_bytes=4,vsync_alignment_bytes=2,vsync_include_bytes=250,vector_include_bytes=32,mode_include_bytes=86,new_include_bytes=368,prior_wait_context_bytes=38)


class VsyncProbe(Probe):
    def __init__(self,mz,s,observed=None):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x20000,0x2e3f0,0x40000
        self.s=s;self.errors=[];self.events=[];self.ports=[];self.native=Counter();self.external=Counter();self.frames=[];self.pending=None;self.stop=False;self.direct=None;self.imr=s.get('imr',0xa5);self.poll=0;self.deliveries=0;self.wait_inputs=0;self.dos_get_index=0;self.dos_set_index=0;self.write_count=0;self.vector_returns=[]
        self.observed=observed or analyze(mz.program_image);self.returns=self.observed['returns'];self.bounds=set(self.observed['instruction_boundaries'])
        self.uc.mem_write(0x90100,b'\xcf');self.uc.mem_write(0x90300,b'\xcf')
        self.callback=tuple(s.get('callback_pointer',[0x200,0x9000]));self.uc.mem_write(self.callback[1]*16+self.callback[0],b'\xcb')
        self.uc.mem_write(0x45c,bytes([s.get('mate',0x40)]));self.uc.mem_write(0x711,bytes([s.get('cursor',1)]))
        for a,v in ((DELAY,s.get('delay',0)),(COUNT1,s.get('count1',65535)),(COUNT2,s.get('count2',32767)),(ACC,s.get('acc',0)),(TEXT,s.get('text',1)),(MASK,s.get('old_mask',0xfb if s.get('installed') else 0)|(s.get('mask_high',0xa5)<<8))):self.uc.mem_write(self.data+a,struct.pack('<H',v))
        self.uc.mem_write(self.data+PROC,struct.pack('<2H',*s.get('proc',[0,0])));self.uc.mem_write(self.data+OLDVECT,struct.pack('<2H',0x300,0x9000));self.uc.mem_write(self.code+RAW,struct.pack('<2H',0x100,0x9000))
        for n,ptr in ((10,(0x1fe2,0x2000) if s.get('installed') else (0x300,0x9000)),(24,(0x1fd8,0x2000) if s.get('installed') else (0x100,0x9000))):self.uc.mem_write(n*4,struct.pack('<2H',*ptr))
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2000:raise ValueError('vsync terminal segment alias')
                if self.frames or self.pending:raise ValueError('vsync unfinished native frame')
                self.stop=True;uc.emu_stop();return
            if self.get('SS')!=0x4000:raise ValueError('vsync stack segment differs')
            off=address-self.code
            special={0x90100:'old_bios',0x90300:'old_irq',self.callback[1]*16+self.callback[0]:'callback'}
            if address in special:
                name=special[address];expected_cs=self.callback[1] if name=='callback' else 0x9000
                if self.get('CS')!=expected_cs:raise ValueError('vsync external segment alias')
                self.enter(name,None if name!='callback' else 0)
                if name=='old_bios':
                    ah=self.get('AH');wrapped=len(self.frames)>1 and self.frames[-2]['name']=='crt';self.events.append(dict(name=name,ah=ah,wrapped=wrapped,live_if=bool(self.get('EFLAGS')&0x200),live_df=bool(self.get('EFLAGS')&0x400)))
                    if ah==0x31:self.set('AL',s.get('mode',0x330c)&255);self.set('BH',s.get('mode',0x330c)>>8)
                    else:self.set('AX',s.get('bios_other_ax',self.get('AX')))
                elif name=='old_irq':self.events.append(dict(name=name,live_if=bool(self.get('EFLAGS')&0x200),live_df=bool(self.get('EFLAGS')&0x400)))
                else:
                    if self.get('DS')!=0x2e3f or self.get('EFLAGS')&0x600:raise ValueError('vsync callback DS/CLD/live IF differs')
                    self.events.append(dict(name=name,pointer=list(self.callback),live_if=False,live_df=False,count1=self.word(COUNT1),count2=self.word(COUNT2)))
                    for r in GPRS:self.set(r,s.get('callback_regs',{}).get(r,0xaaaa))
                    self.set('EFLAGS',(self.get('EFLAGS')&~0x600)|(0x200 if s.get('callback_if',True) else 0)|(0x400 if s.get('callback_df',True) else 0))
                self.external[name]+=1;self.leave(name,None if name!='callback' else 0);return
            if self.get('CS')!=0x2000 or off not in self.bounds:raise ValueError('CPU escaped vsync instruction ownership/segment alias')
            if off in STARTS:
                name=STARTS[off];cleanup=next(c for n,_,_,c in RANGES if n==name);self.enter(name,cleanup);self.native[name]+=1
                if name=='wait':self.poll=0;self.wait_inputs=0
            if off in CALLS:self.prepare(STARTS[CALLS[off]],self.get('SP')-2,off+3,0x2000,None)
            if off in INDIRECT:
                ptr=tuple(struct.unpack('<2H',uc.mem_read(self.code+RAW if off==0x1fd9 else self.get('DS')*16+PROC,4)))
                expected=(0x100,0x9000) if off==0x1fd9 else self.callback
                if ptr!=expected:raise ValueError('vsync undeclared external pointer')
                self.prepare('old_bios' if off==0x1fd9 else 'callback',self.get('SP')-4,off+5 if off==0x1fd9 else off+4,0x2000,self.get('EFLAGS')&65535 if off==0x1fd9 else None)
            if off==0x2083 and self.s.get('deliver_irq'):
                self.poll+=1
                if self.poll%self.s.get('ticks',3)==0:
                    self.deliveries+=1;self.interrupt(10,off);return
            if off in self.returns:
                name,cleanup=self.returns[off];self.leave(name,cleanup)
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            allowed=[(self.data+DELAY,2),(self.data+MASK,1),(self.data+COUNT1,10),(self.code+RAW,4)]
            if not any(a<=address and address+size<=a+z for a,z in allowed):raise ValueError('vsync write outside owned state/span')
            self.write_count+=1
        def intr(uc,number,user):
            site=u16(self.get('IP')-2);ah=self.get('AH')
            if self.get('CS')!=0x2000:raise ValueError('vsync service segment alias')
            if number==0x18:
                if BIOS.get(site)!=ah:raise ValueError('vsync unknown BIOS request/site')
                self.interrupt(24,site+2);return
            if number!=0x21 or DOS.get(site)!=ah:raise ValueError('vsync unknown DOS request/site')
            n=self.get('AL');cf=s.get('get_cf' if ah==0x35 else 'set_cf',0)
            if ah==0x35:
                ptr=tuple(struct.unpack('<2H',uc.mem_read(n*4,4)));self.set('BX',ptr[0]);self.set('ES',ptr[1]);self.events.append(dict(name='get_vector',number=n,pointer=list(ptr),cf=cf));self.dos_get_index+=1
            else:
                ptr=(self.get('DX'),self.get('DS'));self.events.append(dict(name='set_vector',number=n,pointer=list(ptr),cf=cf))
                if not cf:uc.mem_write(n*4,struct.pack('<2H',*ptr))
                self.dos_set_index+=1
            self.set('EFLAGS',(self.get('EFLAGS')&~1)|cf)
        def out(uc,port,width,value,user):
            site=self.get('IP')
            if self.get('CS')!=0x2000 or OUT_PORTS.get(site)!=port or width!=1:raise ValueError('vsync unknown output port/site/width')
            self.ports.append(dict(site=site,kind='out',port=port,value=value,live_if=bool(self.get('EFLAGS')&0x200),live_df=bool(self.get('EFLAGS')&0x400)))
            if port==2:self.imr=value
        def inp(uc,port,width,user):
            site=self.get('IP')
            if self.get('CS')!=0x2000 or IN_PORTS.get(site)!=port or width!=1:raise ValueError('vsync unknown input port/site/width')
            if port==2:value=self.imr
            else:
                pattern=s.get('port_pattern',[32,0,0,32]);value=pattern[self.wait_inputs%len(pattern)];self.wait_inputs+=1
            self.ports.append(dict(site=site,kind='in',port=port,value=value,live_if=bool(self.get('EFLAGS')&0x200),live_df=bool(self.get('EFLAGS')&0x400)));return value
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(out),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)

    def word(self,a):return struct.unpack('<H',self.uc.mem_read(self.data+a,2))[0]
    def prepare(self,name,sp,ip,cs,flags):
        if self.pending:raise ValueError('vsync overlapping native entry')
        self.pending=dict(name=name,sp=u16(sp),ip=ip,cs=cs,flags=flags)
    def enter(self,name,cleanup):
        sp=self.get('SP');expected=self.pending
        if not expected or expected['name']!=name or expected['sp']!=sp:raise ValueError('vsync native entry frame differs')
        ip,cs=struct.unpack('<2H',self.uc.mem_read(self.stack+sp,4))
        if (ip,cs)!=(expected['ip'],expected['cs']):raise ValueError('vsync native entry return differs')
        if cleanup is None and struct.unpack('<H',self.uc.mem_read(self.stack+sp+4,2))[0]!=expected['flags']:raise ValueError('vsync interrupt entry flags differ')
        self.frames.append({**expected,'cleanup':cleanup});self.pending=None
    def leave(self,name,cleanup):
        if not self.frames:raise ValueError('vsync orphan return')
        f=self.frames.pop();sp=self.get('SP');frame=tuple(struct.unpack('<'+'H'*(3 if cleanup is None else 2),self.uc.mem_read(self.stack+sp,6 if cleanup is None else 4)))
        expected=(f['ip'],f['cs'],f['flags']) if cleanup is None else (f['ip'],f['cs'])
        if f['name']!=name or f['cleanup']!=cleanup or f['sp']!=sp or frame!=expected:raise ValueError('vsync native return frame differs')
    def interrupt(self,n,ip):
        ptr=tuple(struct.unpack('<2H',self.uc.mem_read(n*4,4)));known={(0x1fd8,0x2000):'crt',(0x1fe2,0x2000):'irq',(0x100,0x9000):'old_bios',(0x300,0x9000):'old_irq'}
        if ptr not in known:raise ValueError('vsync undeclared vector dispatch')
        flags=self.get('EFLAGS')&65535;sp=u16(self.get('SP')-6);self.uc.mem_write(self.stack+sp,struct.pack('<3H',ip,self.get('CS'),flags));self.prepare(known[ptr],sp,ip,self.get('CS'),flags)
        self.set('SP',sp);self.set('EFLAGS',self.get('EFLAGS')&~0x300);self.set('CS',ptr[1]);self.set('IP',ptr[0])

    def run(self,name,args=(),budget=100000):
        self.stop=False;self.errors.clear();self.frames.clear();self.pending=None;self.direct=name;self._callback_before=self.external['callback']
        flags=self.s.get('flags',0x202)|(0x400 if self.s.get('df') else 0);regs=dict(CS=0x2000,DS=self.s.get('entry_ds',0x2e3f) if name in ('irq','crt','vector_irq') else 0x2e3f,SS=0x4000,ES=0x3333,AX=self.s.get('entry_ax',0x1111),BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,SP=0xffc0,EFLAGS=flags)
        for r,v in regs.items():self.set(r,v)
        initial={r:self.get(r) for r in GPRS}
        if name=='vector_irq':
            ptr=tuple(struct.unpack('<2H',self.uc.mem_read(40,4)))
            if ptr not in ((0x1fe2,0x2000),(0x300,0x9000)):raise ValueError('vsync undeclared vector dispatch')
            start=ptr[1]*16+ptr[0];kind='irq' if ptr==(0x1fe2,0x2000) else 'old_irq';self.set('CS',ptr[1])
        else:kind=name;start=self.code+next(a for n,a,_,_ in RANGES if n==name)
        irq=kind in ('irq','crt','old_irq');cleanup=next((c for n,_,_,c in RANGES if n==kind),None)
        tail=[0xff00,0x2000,flags] if irq else [0xff00,0x2000,*args]
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*len(tail),*tail));self.prepare(kind,0xffc0,0xff00,0x2000,flags if irq else None)
        if irq:self.set('EFLAGS',flags&~0x300)
        self.uc.emu_start(start,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('vsync terminal/budget differs')
        if self.get('SP')!=0xffc0+(6 if irq else 4+cleanup):raise ValueError('vsync far/interrupt cleanup differs')
        if irq:
            expected=dict(initial)
            if kind=='crt':
                if initial['AX']>>8==0x31:expected['AX']=(initial['AX']&0xff00)|(self.s.get('mode',0x330c)&255);expected['BX']=(initial['BX']&255)|(self.s.get('mode',0x330c)&0xff00)
                else:expected['AX']=self.s.get('bios_other_ax',initial['AX'])
            elif kind=='irq' and self.external['callback']>self.callback_before:expected['BP']=self.s.get('callback_regs',{}).get('BP',0xaaaa)
            if any(self.get(r)!=v for r,v in expected.items()) or self.get('EFLAGS')&0xfd5!=flags&0xfd5:raise ValueError('vsync IRET register/flag restoration differs')
        else:
            if any(self.get(r)!=initial[r] for r in ('BP','SI','DI','DS')) or self.get('EFLAGS')&0x600!=flags&0x600:raise ValueError('vsync ordinary callee-saved/IF/DF differs')
            if name in ('vector','end','wait') and self.get('ES')!=initial['ES']:raise ValueError('vsync helper/end/wait ES differs')

    @property
    def callback_before(self):return self._callback_before


class Scalar:
    def __init__(self,p):
        self.mem=bytearray(p.uc.mem_read(0,0x100000));self.data=p.data;self.code=p.code;self.s=p.s;self.imr=p.imr;self.events=[];self.ports=[];self.native=Counter();self.external=Counter();self.deliveries=0
    def get(self,a):return struct.unpack_from('<H',self.mem,self.data+a)[0]
    def put(self,a,v):struct.pack_into('<H',self.mem,self.data+a,u16(v))
    def mask(self):return self.mem[self.data+MASK]
    def ptr(self,n):return tuple(struct.unpack_from('<2H',self.mem,n*4))
    def port(self,site,kind,port,value,live_if=None,df=None):
        self.ports.append(dict(site=site,kind=kind,port=port,value=value,live_if=bool(self.s.get('flags',0x202)&0x200) if live_if is None else live_if,live_df=bool(self.s.get('df')) if df is None else df))
        if kind=='out' and port==2:self.imr=value
    def vector(self,n,ptr):
        self.native['vector']+=1;n&=255;old=self.ptr(n);gcf=self.s.get('get_cf',0);scf=self.s.get('set_cf',0)
        self.events.extend([dict(name='get_vector',number=n,pointer=list(old),cf=gcf),dict(name='set_vector',number=n,pointer=list(ptr),cf=scf)])
        if not scf:struct.pack_into('<2H',self.mem,n*4,*ptr)
        return (old[0],old[1])
    def bios(self,ah,al):
        wrapped=self.ptr(24)==(0x1fd8,0x2000)
        if wrapped:self.native['crt']+=1
        elif self.ptr(24)!=(0x100,0x9000):raise ValueError('scalar undeclared BIOS vector')
        self.external['old_bios']+=1;self.events.append(dict(name='old_bios',ah=ah,wrapped=wrapped,live_if=False,live_df=bool(self.s.get('df'))))
        value=self.s.get('mode',0x330c)&255 if ah==0x31 else self.s.get('bios_other_ax',(ah<<8)|al)&255
        if wrapped:self.port(0x1fde,'out',0x64,value,False)
        return value
    def mode(self,args):
        self.native['mode']+=1
        if not self.s.get('mate',0x40)&64:return (0,None)
        low=self.bios(0x31,0);mode=(self.s.get('mode',0x330c)&0xff00)|low;bhal,mask=args
        if not mask:return (mode,None)
        value=(mode&(~mask&65535))|(bhal&mask);al=self.bios(0x30,value&255)
        if self.get(TEXT)&1:al=self.bios(0x0c,al)
        if value&1:al=self.bios(0x0e,al)
        if self.s.get('cursor',1)&1:self.bios(0x11,al)
        return (value,None)
    def irq(self,via_vector=False):
        if via_vector and self.ptr(10)==(0x300,0x9000):
            self.external['old_irq']+=1;self.events.append(dict(name='old_irq',live_if=False,live_df=bool(self.s.get('df'))));return (None,None)
        self.native['irq']+=1;total=self.get(ACC)+self.get(DELAY);self.put(ACC,total);df=bool(self.s.get('df'))
        if total<=65535:
            self.put(COUNT1,self.get(COUNT1)+1);self.put(COUNT2,self.get(COUNT2)+1)
            ptr=tuple(struct.unpack_from('<2H',self.mem,self.data+PROC))
            if ptr[1]:
                if ptr!=tuple(self.s.get('callback_pointer',[0x200,0x9000])):raise ValueError('scalar undeclared callback')
                self.external['callback']+=1;self.events.append(dict(name='callback',pointer=list(ptr),live_if=False,live_df=False,count1=self.get(COUNT1),count2=self.get(COUNT2)));df=self.s.get('callback_df',True)
        self.port(0x2016,'out',0,32,False,df);self.port(0x2018,'out',0x64,32,False,df);return (None,None)
    def run(self,name,args=()):
        if name=='vector_irq':return self.irq(True)
        if name=='irq':return self.irq()
        if name=='vector':return self.vector(args[2],(args[0],args[1]))
        if name=='mode':return self.mode(args)
        self.native[name]+=1
        if name=='crt':
            self.native[name]-=1;self.native[name]+=1;ah=self.s.get('entry_ax',0x1111)>>8;self.external['old_bios']+=1
            self.events.append(dict(name='old_bios',ah=ah,wrapped=True,live_if=False,live_df=bool(self.s.get('df'))));value=self.s.get('mode',0x330c)&255 if ah==0x31 else self.s.get('bios_other_ax',self.s.get('entry_ax',0x1111))&255;self.port(0x1fde,'out',0x64,value,False);return (None,None)
        if name=='start':
            mode,_=self.mode([0,0]);self.put(DELAY,13311 if mode&12==12 else 0);self.put(COUNT1,0);self.put(COUNT2,0)
            if self.mask():return (None,None)
            old=self.vector(10,(0x1fe2,0x2000));struct.pack_into('<2H',self.mem,self.data+OLDVECT,*old)
            original=self.imr;self.port(0x1fae,'in',2,original,False);self.port(0x1fb4,'out',2,original&251,False);self.mem[self.data+MASK]=original|251
            old=self.vector(24,(0x1fd8,0x2000));struct.pack_into('<2H',self.mem,self.code+RAW,*old);self.port(0x1fd5,'out',0x64,old[0]&255);return (None,None)
        if name=='end':
            if not self.mask():return (None,None)
            self.vector(24,tuple(struct.unpack_from('<2H',self.mem,self.code+RAW)))
            self.port(0x2038,'in',2,self.imr,False);self.port(0x203c,'out',2,self.imr|4,False)
            self.vector(10,tuple(struct.unpack_from('<2H',self.mem,self.data+OLDVECT)))
            self.port(0x2052,'in',2,self.imr,False);self.port(0x2058,'out',2,self.imr&self.mask(),False);self.port(0x205b,'out',0x64,self.imr);self.mem[self.data+MASK]=0;return (None,None)
        if name=='wait':
            if self.mask():
                old=self.get(COUNT1)
                for _ in range(100):
                    if not self.s.get('deliver_irq'):raise ValueError('scalar missing IRQ delivery')
                    self.deliveries+=1;self.irq(True)
                    if self.get(COUNT1)!=old:break
                else:raise ValueError('scalar native IRQ wait budget')
            else:
                pattern=self.s.get('port_pattern',[32,0,0,32]);idx=0
                for site,wanted in ((0x206f,False),(0x2079,True)):
                    for _ in range(100):
                        value=pattern[idx%len(pattern)];idx+=1;self.port(site,'in',0xa0,value)
                        if bool(value&32)==wanted:break
                    else:raise ValueError('scalar port wait budget')
            return (None,None)
        raise ValueError('scalar unknown function')


def matrix(mz):
    rows=[]
    def observe(label,s,steps):
        scenario=json.loads(json.dumps(s));p=VsyncProbe(mz,s);scalar=Scalar(p);before=sha(bytes(scalar.mem));results=[]
        for step in steps:
            fn=step['function'];args=step.get('args',[])
            if 'imr' in step:p.imr=scalar.imr=step['imr']
            if 'mode' in step:p.s['mode']=scalar.s['mode']=step['mode']
            ax,dx=scalar.run(fn,args);p._callback_before=p.external['callback'];p.run(fn,args)
            if (ax is not None and p.get('AX')!=ax) or (dx is not None and p.get('DX')!=dx) or p.events!=scalar.events or p.ports!=scalar.ports or p.native!=scalar.native or p.external!=scalar.external or p.imr!=scalar.imr or p.deliveries!=scalar.deliveries:raise ValueError('vsync scalar result/native/external/port/DOS differs: '+str((label,s,step,p.events,scalar.events,p.ports,scalar.ports,dict(p.native),dict(scalar.native))))
            actual=bytes(p.uc.mem_read(0,0x100000))
            if actual[:p.stack]!=scalar.mem[:p.stack] or actual[p.stack+65536:]!=scalar.mem[p.stack+65536:]:
                changed=[i for i,(a,b) in enumerate(zip(actual,scalar.mem)) if a!=b and not p.stack<=i<p.stack+65536];raise ValueError('vsync full physical memory scalar differs: '+str((label,s,step,changed[:20])))
            results.append(dict(function=fn,step=step,args=args,ax=ax,dx=dx,registers={r:p.get(r) for r in GPRS},flags=p.get('EFLAGS')&65535,count1=scalar.get(COUNT1),count2=scalar.get(COUNT2),delay=scalar.get(DELAY),acc=scalar.get(ACC),old_mask=scalar.mask(),imr=scalar.imr))
        rows.append(dict(function=label,scenario=scenario,steps=results,top_level_calls=len(results),events=p.events,ports=p.ports,native_entries=dict(p.native),external_entries=dict(p.external),deliveries=p.deliveries,write_count=p.write_count,memory_before_sha256=before,memory_after_sha256=sha(bytes(scalar.mem))))
    for df in (False,True):
        for enable in (False,True):
            base=dict(df=df,flags=0x202 if enable else 2)
            for mate in (0,64):
                for mode in (0,4,8,12,65535):
                    for old in (0,1,251,255):observe('start',dict(base,mate=mate,mode=mode,old_mask=old,acc=65535),[dict(function='start')])
            for imr in range(256):
                observe('lifecycle',dict(base,imr=imr,deliver_irq=True,proc=[0x200,0x9000],callback_regs=dict(BP=0x7777),acc=60000),[dict(function='start'),dict(function='wait'),dict(function='vector_irq'),dict(function='end',imr=imr^0x80),dict(function='end')])
                for old in (0,1,4,251,255):observe('end-mask',dict(base,imr=imr,old_mask=old),[dict(function='end')])
            for delay in (0,1,13311,32767,32768,65534,65535):
                for acc in (0,1,13310,13311,32767,32768,65534,65535):
                    for proc in ([0,0],[0x1234,0],[0,0x9000],[0x200,0x9000]):observe('irq',dict(base,delay=delay,acc=acc,proc=proc,callback_pointer=proc if proc[1] else [0x200,0x9000],entry_ds=0x5000),[dict(function='irq')])
            for bits in range(64):
                flags=base['flags']|sum(flag for index,flag in enumerate((1,4,16,64,128,2048)) if bits&(1<<index));observe('irq-flags',dict(base,flags=flags,proc=[0x200,0x9000]),[dict(function='irq')])
            for mask in (0,1,255,256,257,0x30c,65535):
                for value in (0,1,15,0x330c,65535):
                    for mate in (0,64):
                        for text in (0,1):
                            for cursor in (0,1):observe('mode',dict(base,mate=mate,text=text,cursor=cursor),[dict(function='mode',args=[value,mask])])
            for n in range(256):observe('vector',dict(base),[dict(function='vector',args=[0xffff,0xffff,n])])
            for n in (0x100,0x1ff,0xff00,0xffff):observe('vector-word-alias',dict(base),[dict(function='vector',args=[0,0,n])])
            for gcf in (0,1):
                for scf in (0,1):
                    observe('DOS-status',dict(base,get_cf=gcf,set_cf=scf),[dict(function='start'),dict(function='vector_irq'),dict(function='end')])
            for mode in (0,12,65535):observe('repeat-start',dict(base,acc=65000),[dict(function='start'),dict(function='irq'),dict(function='start',mode=mode),dict(function='irq'),dict(function='end')])
            for ax in (0,0x0300,0x31ff,0xffff):observe('crt',dict(base,entry_ax=ax,bios_other_ax=0xbeef),[dict(function='crt')])
            observe('connected-mode',dict(base,proc=[0x200,0x9000],callback_regs=dict(BP=0x7777)),[dict(function='start'),dict(function='mode',args=[0xffff,0xffff]),dict(function='irq'),dict(function='end')])
    return rows


def nonterminal(mz):
    rows=[]
    for df in (False,True):
        for enable in (False,True):
            base=dict(df=df,flags=0x202 if enable else 2)
            scenarios=[dict(base,old_mask=1),dict(base,old_mask=0,port_pattern=[32]),dict(base,old_mask=0,port_pattern=[0]),dict(base,installed=True,deliver_irq=True,delay=65535,acc=65535),dict(base,old_mask=1,deliver_irq=True)]
            for s in scenarios:
                p=VsyncProbe(mz,s);spec=Scalar(p);before=sha(bytes(spec.mem))
                try:p.run('wait',budget=2000)
                except ValueError as e:
                    if str(e)!='vsync terminal/budget differs':raise
                else:raise ValueError('vsync stalled native wait unexpectedly returned')
                spec.native['wait']+=1
                for _ in range(p.deliveries):spec.deliveries+=1;spec.irq(True)
                if s.get('old_mask')==0:
                    prefix=[dict(site=0x206f,kind='in',port=0xa0,value=0,live_if=enable,live_df=df)] if s.get('port_pattern')==[0] else []
                    site=0x2079 if prefix else 0x206f;value=s['port_pattern'][0]
                    spec.ports=prefix+[dict(site=site,kind='in',port=0xa0,value=value,live_if=enable,live_df=df) for _ in range(len(p.ports)-len(prefix))]
                actual=bytes(p.uc.mem_read(0,0x100000))
                if actual[:p.stack]!=spec.mem[:p.stack] or actual[p.stack+65536:]!=spec.mem[p.stack+65536:] or p.events!=spec.events or p.ports!=spec.ports or p.native!=spec.native or p.external!=spec.external or spec.get(COUNT1)!=s.get('count1',65535):raise ValueError('vsync nonterminal partial memory/trace differs')
                rows.append(dict(function='wait',scenario=s,budget=2000,instruction=p.get('IP'),outcome='native-wait-budget',events=p.events,ports=p.ports,native_entries=dict(p.native),external_entries=dict(p.external),deliveries=p.deliveries,count1=spec.get(COUNT1),acc=spec.get(ACC),memory_before_sha256=before))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('vsync prior palette proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_vsync.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('vsync input changed: '+p)
    def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('memory_before_sha256','memory_after_sha256')} for row in cpu]
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];objects=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('vsync invalid image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz),nonterminal=nonterminal(mz))
        if observations:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('vsync complete body/CFG differs')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached);actual=cached.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else cached
                if actual!=cached_provider(p,d):raise ValueError('vsync cached frozen provider differs: '+p)
            op=str(tree/'obj/th03/mainl.obj');obj_data=(ROOT/op).read_bytes();inputs[op]=sha(obj_data);obj=describe_omf(obj_data)
            if not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0']:raise ValueError('vsync cached root OMF identity differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments','record_count','record_counts')}
            if objects and obj['dependency_timestamp_normalized_sha256']!=objects[0]['dependency_timestamp_normalized_sha256']:raise ValueError('vsync cached OMF differs beyond dependency timestamps')
            objects.append(observed['object']);maprows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));carrier=next(row for row in maprows if row['module']=='th03_mainl.asm' and row['segment']==0 and row['size'])
            if not all(carrier['start']<=a<a+n<=carrier['start']+carrier['size'] for _,a,n,_ in RANGES):raise ValueError('vsync includes outside complete root carrier')
            observed['carrier']=carrier;target=parse_mz((ROOT/observations[0]['path']).read_bytes());extents=[('vsync',0x1f6a,250),('vector',0x704,32),('mode',0xf02,86),('prior-wait',0x2064,38)]
            observed['comparisons']={n:extent_observation(target,mz,dict(start=a,size=z,segment=0,offset=a)) for n,a,z in extents}
            if any(not x['raw_slice_equal'] or not x['ordered_relocations_equal'] for x in observed['comparisons'].values()):raise ValueError('vsync complete raw/ordered relocations differ')
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']) or normalized(observed['nonterminal'])!=normalized(observations[0]['nonterminal']):raise ValueError('vsync target/cached CPU differs')
        observations.append(observed);print('Reviewed',path,len(observed['cpu']),'scenarios',len(observed['nonterminal']),'budgets',flush=True)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('vsync canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('vsync frozen provider changed')
    result=dict(kind='th03-mainl-complete-vsync-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},build_scaffold_main_remaps=BUILD_REMAPS,observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL VSYNC/vector/mode368bytes with native WAIT38context and explicit DOS/BIOS/ports/interrupt-entry fixtures:',args.output)


if __name__=='__main__':main()
