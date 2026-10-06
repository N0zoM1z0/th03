#!/usr/bin/env python3
"""Independently review all remaining MAINL root CODE gaps and their producers."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import re
import struct
import subprocess
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import Probe, REVISION, sha
from review_th03_mainl_snow import u16
from review_th03_mainl_super import SuperProbe
from review_th03_mainl_draw import return_cleanup, trace_hash
from review_th03_mainl_graphics import initial_flags, COLD, COLD_SHA
from review_th03_mainl_heap import cached_provider, BUILD_REMAPS
from review_th03_mainl_math import atan_scalar, atan_table, numeric_literals
import review_th03_mainl_pfopen as pf

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-mainl-pi-decoder-borrow-review-20261006.json'
PROOF_SHA='d723fa6225cfd1b9eaa6dbfa44a8e804332b83f73b6c2f6177c4cd646ed43935'
RANGES=[('keyclear',0x6fe,6,0),('color',0xc36,41,4),('off',0xc60,5,0),('atan',0x175e,107,4),
        ('end',0x17ca,6,0),('rand',0x1a3e,42,0),('sound_out',0x1ef6,22,'near'),('sound_in',0x1f0c,20,'near'),
        ('clear',0x1f20,17,0),('fill',0x1f32,55,4),('exist',0x276e,60,0),('create',0x27aa,117,0),('set',0x2820,47,0),
        ('start',0x2aae,41,0),('joy',0x2ad8,17,'near'),('sense',0x2aea,33,0),('sajout',0x2b0c,9,'near')]
PRIVATE={'sound_out','sound_in','joy','sajout'}
ENTRY={n:a for n,a,_,_ in RANGES}
CALLS={0x17cc:0x6fe,0x27ae:0x276e,0x2ac3:0x1f0c,0x2acc:0x1ef6,0x2ada:0x1ef6,0x2afa:0x2ad8}
FAR={0x17cc,0x27ae}
PORTS={0xc45:0x7c,0xc4b:0x7e,0xc50:0x7e,0xc55:0x7e,0xc5a:0x7e,0xc62:0x7c,
       0x1f00:0x188,0x1f0a:0x18a,0x1f16:0x188,0x2ae2:0x188,0x2b0e:'saj-port'}
INPUTS={0x1ef9:0x188,0x1f01:0x188,0x1f0f:0x188,0x1f17:0x188,0x1f1e:0x18a,0x2ab4:0x188,0x2ae5:0x18a,0x2b11:0x188}
DOS={0x701:0xc00,0x2772:0x52,0x27bb:0x5800,0x27c5:0x5801,0x27cc:0x48,0x27dd:0x49,0x27e5:0x5801,0x27ec:0x48,0x2818:0x5801}
CONSOLE={0x1f22:27,0x1f26:91,0x1f2a:50,0x1f2e:74}
PRODUCERS={0x4c5:0x90,0x60b:0x90,0x67d:0x90,0x6ad:0x90,0xc5f:0x90,0xc65:0x90,0xc71:0,
           0x17c9:0x90,0x1903:0x90,0x19a3:0,0x1a0d:0x90,0x1f31:0x90,0x1f69:0x90,
           0x281f:0x90,0x284f:0x90,0x2aad:0,0x2ad7:0x90,0x2ae9:0x90,0x2b0b:0x90,0x2b15:0,0x2c2f:0x90}
EXTENTS=[('align-bfnt',0x4c5,1),('align-bread',0x60b,1),('align-bseek',0x67d,1),('align-filesize',0x6ad,1),
         ('keyclear',0x6fe,6),('grcg',0xc36,48),('root-zero-font',0xc71,1),('atan-end',0x175e,114),
         ('align-pfgetc',0x1903,1),('pfgetc-zero',0x19a3,1),('align-pfread',0x1a0d,1),('rand',0x1a3e,42),
         ('sound-text',0x1ef6,116),('resident',0x276e,226),('joystick',0x2aad,105),('compare-align',0x2c2f,57)]
PUBLICS={'DOS_KEYCLEAR':0x6fe,'GRCG_SETCOLOR':0xc36,'GRCG_OFF':0xc60,'IATAN2':0x175e,'JS_END':0x17ca,'IRAND':0x1a3e,
         'TEXT_CLEAR':0x1f20,'TEXT_FILLCA':0x1f32,'RESPAL_EXIST':0x276e,'RESPAL_CREATE':0x27aa,'RESPAL_SET_PALETTES':0x2820,
         'JS_START':0x2aae,'JS_SENSE':0x2aea}
PROVIDERS=list(dict.fromkeys(['th03_mainl.asm','ReC98.inc','th03/th03.inc','libs/master.lib/master.inc','libs/master.lib/macros.inc',
    'libs/master.lib/func.hpp','libs/master.lib/func.inc','Tupfile.lua']+['libs/master.lib/'+n+'.asm' for n in (
    'dos_keyclear','grcg_setcolor','iatan2','atan8[data]','random','rand[data]','soundio','text_clear','text_fillca','tx[data]',
    'respal_exist','respal_exist[data]','respal_set_palettes','pal[data]','js_start','js_sense','js_end','js[data]','js[bss]',
    'pf_str_ieq','bfnt_extend_header_skip','bfill','bopenr','bread','bseek','bseek_','dos_filesize','pfgetc','pfread','pfrewind','pfseek')]))
SEED,JOYSTICK,STAT,RESIDENT,TONE,PALETTE,ID,TEXT=0x5b6,0x570,0x141a,0x5ac,0x578,0x141e,0x882,0x83c
LOW_IMAGE=bytes((i*13+3)&255 for i in range(0x1c000))
MCB_IMAGE=bytes((i*37+3)&255 for i in range(0x40000))
VIDEO_IMAGE=bytes((i*17+5)&255 for i in range(0x50000))


def analyze(image):
    dec=Cs(CS_ARCH_X86,CS_MODE_16);dec.detail=True
    decoded=[];bounds=set();returns={};rows=[]
    for name,start,size,cleanup in RANGES:
        body=image[start:start+size];ins=list(dec.disasm(body,start))
        if len(body)!=size or not ins or sum(i.size for i in ins)!=size or return_cleanup(ins[-1])!=cleanup:
            raise ValueError('root tail complete body/cleanup differs')
        decoded.append((name,start,size,cleanup,ins));bounds.update(i.address for i in ins)
    for name,start,size,cleanup,ins in decoded:
        edges=[]
        for index,i in enumerate(ins):
            if i.mnemonic in ('ret','retf'):
                if return_cleanup(i)!=cleanup:raise ValueError('root tail interior cleanup differs')
                returns[i.address]=cleanup
            if i.mnemonic=='int' and not (i.bytes==b'\xcd\x21' and i.address in DOS or i.bytes==b'\xcd\x29' and i.address in CONSOLE):
                raise ValueError('root tail unknown interrupt site')
            if i.mnemonic in ('in','out'):
                sites=INPUTS if i.mnemonic=='in' else PORTS
                if i.address not in sites:raise ValueError('root tail unknown port site')
                if i.op_str not in ('al, dx','dx, al','0x7c, al'):raise ValueError('root tail unknown port width')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('root tail unknown indirect edge')
            if i.mnemonic in ('lcall','ljmp'):raise ValueError('root tail unknown far edge')
            destination=i.operands[0].imm
            if i.mnemonic=='call':
                if CALLS.get(i.address)!=destination:raise ValueError('root tail unknown native call')
                if i.address in FAR and (not index or ins[index-1].bytes!=b'\x0e'):raise ValueError('root tail far call lacks PUSH CS')
            elif destination not in bounds:raise ValueError('root tail branch enters operand/neighbor/producer')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=destination))
        rows.append(dict(name=name,offset=start,size=size,instructions=len(ins),cleanup=cleanup,sha256=sha(image[start:start+size]),edges=edges))
    if any(image[a:a+1]!=bytes([v]) for a,v in PRODUCERS.items()):raise ValueError('root tail producer byte differs')
    context=pf.analyze(image)
    return dict(bodies=rows,bounds=sorted(bounds),returns=returns,producer_bytes=PRODUCERS,new_body_bytes=sum(z for _,_,z,_ in RANGES)+56,
                new_extent_bytes=722,prior_pfopen_context_bytes=281,native_compare=context,private_unreferenced='sajout')


class PrefixStop(Exception):pass


class TailProbe(Probe):
    prepare=SuperProbe.prepare;enter=SuperProbe.enter;leave=SuperProbe.leave
    def __init__(self,mz,scenario,meta=None):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x20000,0x2e3f0,0x40000
        self.meta=meta or analyze(mz.program_image);self.s=scenario;self.bounds=set(self.meta['bounds']);self.returns=self.meta['returns']
        self.entry_names={a:n for n,a,_,_ in RANGES};self.frames=[];self.pending=None;self.stop=False;self.errors=[]
        self.native=Counter();self.visited=set();self.writes=[];self.ports=[];self.events=[];self.status_index=0;self.search_index=0;self.paused=False;self.fault=None
        self.low,self.high=7,128
        self.uc.mem_write(0,LOW_IMAGE)
        self.uc.mem_write(0x50000,MCB_IMAGE)
        self.uc.mem_write(0xa0000,VIDEO_IMAGE)
        self.uc.mem_write(0x712,bytes([scenario.get('lines',24)]))
        for offset,key,default in ((JOYSTICK,'joystick',0),(STAT,'state',0x8000),(RESIDENT,'resident',0),(TONE,'tone',100),(TEXT,'text_seg',0xa000)):
            self.uc.mem_write(self.data+offset,struct.pack('<H',scenario.get(key,default)))
        self.uc.mem_write(self.data+SEED,struct.pack('<I',scenario.get('seed',1)))
        self.uc.mem_write(self.data+PALETTE,bytes(scenario.get('palette',[(i*13+7)&255 for i in range(48)])))
        self.uc.mem_write(0x10100,struct.pack('<H',scenario.get('first_mcb',0x5000)))
        identity=bytes(self.uc.mem_read(self.data+ID,10))
        blocks=scenario.get('blocks',[[0x5000,90,0x1234,4,'miss']])
        for segment,flag,owner,size,value in blocks:
            self.uc.mem_write(segment*16,struct.pack('<BHH',flag,owner,size))
            data=identity if value=='match' else bytes.fromhex(value) if value not in ('miss','') else b'missxxxxxx'
            self.uc.mem_write(segment*16+16,data)
        for segment,offset,values in scenario.get('initial_values',[]):self.uc.mem_write(segment*16+offset,bytes(values))
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2000:raise ValueError('root tail terminal segment alias')
                if self.frames or self.pending:raise ValueError('root tail unfinished native frame')
                self.stop=True;uc.emu_stop();return
            off=address-self.code
            if self.get('CS')!=0x2000 or self.get('SS')!=0x4000:raise ValueError('root tail CODE/stack segment alias')
            if off not in self.bounds:raise ValueError('CPU escaped root tail instruction boundaries')
            if off in INPUTS and INPUTS[off]==0x188 and self.status_index==scenario.get('pause_after_status'):
                self.paused=True;uc.emu_stop();return
            if off==0x2779:
                if self.search_index==scenario.get('pause_after_mcb'):
                    self.paused=True;uc.emu_stop();return
                self.search_index+=1
            self.visited.add(off)
            if off in self.entry_names:
                name=self.entry_names[off];self.enter(name,next(c for n,_,_,c in RANGES if n==name));self.native[name]+=1
            if off in CALLS:
                name=self.entry_names[CALLS[off]];cleanup=next(c for n,_,_,c in RANGES if n==name)
                self.prepare(name,self.get('SP')-2,off+3,cleanup)
            if off in self.returns:self.leave(self.returns[off])
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            if not any(a<=address and address+size<=b for a,b in ((0,0x1c000),(self.data,self.data+65536),(0x50000,0x90000),(0xa0000,0xf0000))):
                raise ValueError('root tail store outside declared state/MCB/text span')
            self.writes.append([address,size,value])
        def intr(uc,number,user):
            site=u16(self.get('IP')-2)
            if number==0:
                if site+2 not in (0x1791,0x17a8) or self.get('CS')!=0x2000 or bytes(uc.mem_read(self.code+self.get('IP'),2))!=b'\xf7\xf3':
                    raise ValueError('root tail unknown divide trap')
                self.fault=self.get('IP');uc.emu_stop();return
            if number==0x29:
                if CONSOLE.get(site)!=self.get('AL'):raise ValueError('root tail unknown console request/site')
                self.events.append(dict(site=site,name='console',value=self.get('AL')));return
            request=self.get('AX') if site in (0x701,0x27bb,0x27c5,0x27e5,0x2818) else self.get('AH')
            if number!=0x21 or DOS.get(site)!=request:raise ValueError('root tail unknown DOS request/site')
            event=dict(site=site,name='dos',request=request)
            if site==0x701:ax,cf=scenario.get('key_ax',0xbeef),scenario.get('key_cf',0)
            elif site==0x2772:
                ax,cf=scenario.get('list_ax',0x52ee),scenario.get('list_cf',0);self.set('ES',0x1000);self.set('BX',0x102)
                event.update(list_pointer=[0x102,0x1000])
            elif site==0x27bb:ax,cf=scenario.get('strategy',0x77),scenario.get('strategy_cf',0)
            elif site in (0x27c5,0x27e5,0x2818):
                ax,cf=scenario.get('strategy_ax',0xdead),scenario.get('strategy_set_cf',0);event.update(strategy=self.get('BX'))
            elif site==0x27dd:ax,cf=scenario.get('free_ax',7),scenario.get('free_cf',1);event.update(segment=self.get('ES'))
            else:
                reply=scenario.get('allocations',[{}]*2)[int(site==0x27ec)]
                ax,cf=reply.get('ax',0x1500),reply.get('cf',0);event.update(paragraphs=self.get('BX'))
            event.update(ax=ax,cf=cf);self.events.append(event);self.set('AX',ax);self.set('EFLAGS',(self.get('EFLAGS')&~1)|cf)
        def output(uc,port,width,value,user):
            site=self.get('IP');expected=PORTS.get(site)
            if width!=1 or expected!=port:raise ValueError('root tail unknown output port/site/width')
            self.ports.append(dict(site=site,port=port,value=value,direction='out',live_if=bool(self.get('EFLAGS')&512)))
            if port==0x188:self.low=value
        def inp(uc,port,width,user):
            site=self.get('IP')
            if width!=1 or INPUTS.get(site)!=port:raise ValueError('root tail unknown input port/site/width')
            if port==0x188:
                values=scenario.get('statuses',[0]);value=values[min(self.status_index,len(values)-1)];self.status_index+=1
            else:value=scenario.get('register7',0x55) if site==0x1f1e else scenario.get('joy_value',0xc3)
            self.ports.append(dict(site=site,port=port,value=value,direction='in',live_if=bool(self.get('EFLAGS')&512)));return value
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)
    def run(self,name,args=(),budget=3000000,fault=False,terminal=True):
        if name in PRIVATE or name not in ENTRY:raise ValueError('root tail private helper requires complete public caller')
        self.stop=False;self.errors.clear();self.frames.clear();self.pending=None;self.paused=False;self.fault=None
        cleanup=next(c for n,_,_,c in RANGES if n==name)
        saved=dict(CS=0x2000,DS=0x2e3f,SS=0x4000,ES=0x3333,AX=0x1111,BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,SP=0xffc0,EFLAGS=initial_flags(self.s))
        for r,v in saved.items():self.set(r,v)
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2000,*args));self.prepare(name,0xffc0,0xff00,cleanup)
        self.uc.emu_start(self.code+ENTRY[name],0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if bool(self.fault)!=fault or (self.stop!=terminal and not self.paused):raise ValueError('root tail terminal/budget/fault differs')
        if terminal and not fault and (self.get('SP')!=0xffc4+cleanup or any(self.get(r)!=saved[r] for r in ('BP','SI','DI','DS'))):
            raise ValueError('root tail cleanup/preserved register differs')


class Scalar:
    def __init__(self,p):
        self.mem=bytearray(p.uc.mem_read(0,0x100000));self.data=p.data;self.s=p.s;self.flags=initial_flags(p.s)
        self.native=Counter();self.events=[];self.ports=[];self.writes=[];self.status_index=0;self.search_index=0
    def word(self,a):return struct.unpack_from('<H',self.mem,a)[0]
    def put(self,a,value,size=2):
        value=value&((1<<(size*8))-1);self.mem[a:a+size]=value.to_bytes(size,'little');self.writes.append([a,size,value])
    def port(self,site,port,value,direction):
        self.ports.append(dict(site=site,port=port,value=value,direction=direction,live_if=bool(self.flags&512)));return value
    def input(self,site,port):
        if port==0x188:
            if self.status_index==self.s.get('pause_after_status'):
                self.poll_site=site;raise PrefixStop()
            values=self.s.get('statuses',[0]);value=values[min(self.status_index,len(values)-1)];self.status_index+=1
        else:value=self.s.get('register7',0x55) if site==0x1f1e else self.s.get('joy_value',0xc3)
        return self.port(site,port,value,'in')
    def wait(self,site):
        for _ in range(10000):
            if not self.input(site,0x188)&128:return
        raise ValueError('scalar root sound poll budget')
    def sound_out(self,register,value):
        self.native['sound_out']+=1;self.wait(0x1ef9);self.port(0x1f00,0x188,register,'out');self.wait(0x1f01);self.port(0x1f0a,0x18a,value,'out')
    def sound_in(self,register):
        self.native['sound_in']+=1;self.wait(0x1f0f);self.port(0x1f16,0x188,register,'out');self.wait(0x1f17);return self.input(0x1f1e,0x18a)
    def dos(self,site,segment=0,strategy=0):
        s=self.s;request=DOS[site];event=dict(site=site,name='dos',request=request)
        if site==0x701:ax,cf=s.get('key_ax',0xbeef),s.get('key_cf',0)
        elif site==0x2772:ax,cf=s.get('list_ax',0x52ee),s.get('list_cf',0);event.update(list_pointer=[0x102,0x1000])
        elif site==0x27bb:ax,cf=s.get('strategy',0x77),s.get('strategy_cf',0)
        elif site in (0x27c5,0x27e5,0x2818):ax,cf=s.get('strategy_ax',0xdead),s.get('strategy_set_cf',0);event.update(strategy=strategy)
        elif site==0x27dd:ax,cf=s.get('free_ax',7),s.get('free_cf',1);event.update(segment=segment)
        else:
            reply=s.get('allocations',[{}]*2)[int(site==0x27ec)];ax,cf=reply.get('ax',0x1500),reply.get('cf',0);event.update(paragraphs=4)
        event.update(ax=ax,cf=cf);self.events.append(event);return ax,cf
    def exist(self):
        self.native['exist']+=1;self.dos(0x2772);self.flags&=~1024;current=self.word(0x10100)
        for _ in range(10000):
            if self.search_index==self.s.get('pause_after_mcb'):
                self.mcb=current;raise PrefixStop()
            self.search_index+=1;at=current*16
            if self.word(at+1) and self.mem[at+16:at+26]==self.mem[self.data+ID:self.data+ID+10]:result=u16(current+1);break
            next_=u16(current+1+self.word(at+3))
            if self.mem[at]!=77:result=0;break
            current=next_
        else:raise ValueError('scalar resident search budget')
        self.put(self.data+RESIDENT,result);return result
    def run(self,name,args=()):
        self.flags=initial_flags(self.s)
        if name=='exist':return self.exist(),None
        self.native[name]+=1
        if name in ('keyclear','end'):
            if name=='end':self.native['keyclear']+=1
            return self.dos(0x701)
        if name=='color':
            color,mode=args;self.flags&=~512;self.port(0xc45,0x7c,mode&255,'out')
            for bit,site in enumerate((0xc4b,0xc50,0xc55,0xc5a)):self.port(site,0x7e,255 if color&(1<<bit) else 0,'out')
            self.flags=initial_flags(self.s);return None,self.flags&1
        if name=='off':self.port(0xc62,0x7c,0,'out');return None,0
        if name=='atan':return atan_scalar(args[1],args[0]),0
        if name=='rand':
            seed=struct.unpack_from('<I',self.mem,self.data+SEED)[0];seed=(seed*0x15a4e35+1)&0xffffffff
            self.put(self.data+SEED,seed&65535);self.put(self.data+SEED+2,seed>>16);return (seed>>16)&32767,0
        if name=='clear':
            for site,value in CONSOLE.items():self.events.append(dict(site=site,name='console',value=value))
            return None,None
        if name=='fill':
            attr,char=args;count=80*(self.mem[0x712]+1);segment=self.word(self.data+TEXT);step=-2 if self.flags&1024 else 2
            for offset,value in ((0,char),(0x2000,attr)):
                for _ in range(count):self.put(segment*16+offset,value);offset=u16(offset+step)
            return None,None
        if name=='create':
            if self.exist():return 2,None
            strategy,_=self.dos(0x27bb);self.dos(0x27c5,strategy=1);segment,carry=self.dos(0x27cc)
            result=0
            if not carry:
                if segment>0x2000:
                    self.dos(0x27dd,segment=segment);self.dos(0x27e5,strategy=2);segment,carry=self.dos(0x27ec)
                self.put(self.data+RESIDENT,segment);self.put(u16(segment-1)*16+1,65535)
                self.flags&=~1024
                for index in range(10):self.put(segment*16+index,self.mem[self.data+ID+index],1)
                for offset in (10,12,14):self.put(segment*16+offset,0)
                result=1
            _,carry=self.dos(0x2818,strategy=strategy);return result,carry
        if name=='set':
            self.flags&=~1024;segment=self.word(self.data+RESIDENT)
            if segment:
                self.put(segment*16+10,self.mem[self.data+TONE],1)
                for index in range(16):
                    at=self.data+PALETTE+index*3
                    # R,G,B high nibbles become packed nibbleR/nibbleG then nibbleB.
                    a,b=self.mem[at:at+2];word=((a>>4)<<8)|(b>>4)
                    self.put(segment*16+16+index*3,word)
                    self.put(segment*16+18+index*3,self.mem[at+2]>>4,1)
            return None,None
        if name=='start':
            present=False
            for _ in range(256):
                if self.input(0x2ab4,0x188)!=255:present=True;break
            if present:
                old=self.flags;self.flags&=~512;value=self.sound_in(7);self.sound_out(7,(value&63)|128);self.flags=old
            self.put(self.data+JOYSTICK,int(present));return int(present),None
        if name=='sense':
            value=0x1357;result=0x1111
            if self.word(self.data+JOYSTICK):
                old=self.flags;self.flags&=~512;self.native['joy']+=1;self.sound_out(15,128)
                self.port(0x2ae2,0x188,14,'out');result=(self.input(0x2ae5,0x18a)^255)&63;value=result;self.flags=old
            self.put(self.data+STAT,self.word(self.data+STAT)|value);return result,0
        raise ValueError('unknown root tail scalar entry')


def compare(p,m,ax,carry,label):
    if (ax is not None and p.get('AX')!=ax or carry is not None and p.get('EFLAGS')&1!=carry or
        (p.get('EFLAGS')^m.flags)&(512|1024) or p.native!=m.native or p.events!=m.events or p.ports!=m.ports or p.writes!=m.writes or
        p.status_index!=m.status_index or p.search_index!=m.search_index):
        raise ValueError('root tail scalar registers/flags/events/native/stores differ: '+str((label,p.get('AX'),ax,dict(p.native),dict(m.native),p.events,m.events,p.ports[:8],m.ports[:8],len(p.writes),len(m.writes))))
    actual=bytes(p.uc.mem_read(0,0x100000))
    if actual[:p.stack]!=m.mem[:p.stack] or actual[p.stack+65536:]!=m.mem[p.stack+65536:]:
        changes=[i for i,(a,b) in enumerate(zip(actual,m.mem)) if a!=b and not p.stack<=i<p.stack+65536]
        raise ValueError('root tail full memory differs: '+str((label,changes[:16],[(i,actual[i],m.mem[i]) for i in changes[:8]])))


def matrix(mz):
    meta=analyze(mz.program_image);rows=[]
    flags=[dict(df=df,flags=2|irq,initial_cf=cf) for df,irq,cf in ((False,0,0),(True,0,1),(False,512,1),(True,512,0))]
    def observe(label,scenario,steps):
        p=TailProbe(mz,scenario,meta);m=Scalar(p);before=sha(bytes(m.mem));results=[]
        for name,args in steps:
            trap=False
            try:ax,cf=m.run(name,args)
            except ArithmeticError:ax,cf=None,None;trap=True
            p.run(name,args,fault=trap,terminal=not trap)
            compare(p,m,ax,cf,label)
            results.append(dict(function=name,args=args,ax=ax,cf=cf,fault=p.fault,terminal=not trap))
        rows.append(dict(label=label,scenario=scenario,steps=results,top_level_calls=len(results),visited=sorted(p.visited),native_entries=dict(p.native),
                         events=p.events,ports=p.ports,store_count=len(p.writes),stores_sha256=trace_hash(p.writes),
                         memory_before_sha256=before,memory_after_sha256=sha(bytes(m.mem))))
    for base in flags:
        for ax in (0,1,65535,0xbeef):
            for cf in (0,1):observe('native-keyclear-through-js-end',dict(base,key_ax=ax,key_cf=cf),[('keyclear',[]),('end',[])])
        for color in range(16):
            for mode in (0,0xc0,0xff,0x1234):observe('grcg-mode-color-flags',base,[('color',[0x7700|color,mode]),('off',[])])
        for lines in (0,1,24,30,127,255):
            for segment in (0xa000,0xe000):observe('text-bios-row-DF-wrap',dict(base,lines=lines,text_seg=segment),[('fill',[0x9abc,0xdef0]),('clear',[])])
        for joy in (0,1,2,65535):
            observe('joystick-no-board-SI-state',dict(base,joystick=joy),[('sense',[])])
        for statuses in ([255],[255]*255+[0],[255]*256+[0],[0,128,0,128,0],[127,0],[254,0]):
            observe('joystick-probe-count-and-polls',dict(base,statuses=statuses),[('start',[]),('sense',[]),('end',[])])
        for resident in (0,0x6000,0x2f80):
            observe('resident-palette-skip-or-alias',dict(base,resident=resident,tone=0x1234),[('set',[])])
        for scenario in ({},{'strategy_cf':1,'strategy_set_cf':1},{'list_cf':1},{'allocations':[{'cf':1},{}]},
                         {'allocations':[{'ax':0x6000},{'ax':0x7000}]},{'allocations':[{'ax':0x6000},{'ax':8,'cf':1}]},
                         {'blocks':[[0x5000,90,0x1111,4,'match']]},{'blocks':[[0x5000,77,0,4,'match'],[0x5005,90,0x2222,4,'match']]}):
            observe('resident-find-create-DOS-failures',dict(base,**scenario),[('exist',[]),('create',[]),('set',[])])
    for value in range(256):
        observe('joystick-status-and-register7-bytes',dict(flags[value&3],statuses=[value,0],register7=value),[('start',[])])
        observe('joystick-input-all-bytes',dict(flags[value&3],joystick=1,joy_value=value,state=value<<8),[('sense',[])])
        for slot in range(3):
            palette=[0]*48;palette[slot]=value
            observe('resident-palette-nibble-basis',dict(flags[value&3],resident=0x6000,palette=palette,tone=value),[('set',[])])
    for seed in [0,1,2,0x7fffffff,0x80000000,0xffffffff]+[1<<bit for bit in range(32)]+[0x12345678,0xfedcba98]:
        observe('random-seed-word-carry-basis',dict(flags[seed&3],seed=seed),[('rand',[])])
    for base in flags:observe('random-native-chain',dict(base,seed=0xffffffff),[('rand',[])]*1024)
    for ratio in range(256):
        for swap in (False,True):
            for sx,sy in ((1,1),(-1,1),(-1,-1),(1,-1)):
                x,y=(ratio,256) if swap else (256,ratio)
                observe('atan-all-quotients-octants',flags[ratio&3],[('atan',[u16(x*sx),u16(y*sy)])])
    for x in (0,1,-1,127,128,129,256,32767,-32768):
        for y in (0,1,-1,127,128,129,256,32767,-32768):observe('atan-word-extremes-faults',flags[(x+y)&3],[('atan',[u16(x),u16(y)])])
    identity=b'pal98 grb\0'
    for offset in range(10):
        damaged=bytearray(identity);damaged[offset]^=1
        observe('resident-signature-every-byte',dict(blocks=[[0x5000,77,1,4,damaged.hex()],[0x5005,90,1,4,'match']]),[('exist',[]),('create',[])])
    for owner in (0,1,65535):
        for flag in (0,77,90,255):
            observe('resident-owner-type-termination',dict(blocks=[[0x5000,flag,owner,4,'match'],[0x5005,90,1,4,'miss']]),[('exist',[])])
    return rows


def prefixes(mz):
    meta=analyze(mz.program_image);rows=[]
    for base in [dict(df=df,flags=2|irq) for df in (False,True) for irq in (0,512)]:
        for name,statuses in (('start',[0,128]),('start',[0,0,128]),('sense',[128]),('sense',[0,128])):
            scenario=dict(base,statuses=statuses,joystick=1,pause_after_status=20)
            p=TailProbe(mz,scenario,meta);m=Scalar(p);before=sha(bytes(m.mem))
            try:m.run(name)
            except PrefixStop:pass
            else:raise ValueError('root sound scalar poll unexpectedly returned')
            p.run(name,terminal=False);compare(p,m,None,None,'native sound polling prefix')
            if not p.paused or p.stop or p.get('IP')!=m.poll_site or not p.frames or p.pending:raise ValueError('root sound prefix phase/native frame differs')
            rows.append(dict(function=name,scenario=scenario,outcome='native-busy-semantic-prefix',instruction=p.get('IP'),frames=p.frames,
                             native_entries=dict(p.native),events=p.events,ports=p.ports,visited=sorted(p.visited),store_count=len(p.writes),
                             memory_before_sha256=before,memory_after_sha256=sha(bytes(m.mem))))
        for name in ('exist','create'):
            scenario=dict(base,blocks=[[0x5000,77,1,65535,'miss']],pause_after_mcb=7)
            p=TailProbe(mz,scenario,meta);m=Scalar(p);before=sha(bytes(m.mem))
            try:m.run(name)
            except PrefixStop:pass
            else:raise ValueError('root resident scalar cyclic search unexpectedly returned')
            p.run(name,terminal=False);compare(p,m,None,None,'native MCB cyclic prefix')
            if not p.paused or p.stop or p.get('IP')!=0x2779 or p.get('BX')!=m.mcb or len(p.frames)!=(2 if name=='create' else 1):
                raise ValueError('root resident prefix phase/native frame differs')
            rows.append(dict(function=name,scenario=scenario,outcome='native-MCB-cycle-semantic-prefix',instruction=p.get('IP'),frames=p.frames,
                             native_entries=dict(p.native),events=p.events,ports=p.ports,visited=sorted(p.visited),store_count=len(p.writes),
                             memory_before_sha256=before,memory_after_sha256=sha(bytes(m.mem))))
    return rows


def pf_context(mz):
    """Keep legacy explicit buffer/heap models; execute STR_IEQ only through PFOPEN."""
    from unicorn import UC_HOOK_CODE
    probes=[];original=pf.PfProbe
    class Tracking(original):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs);self.visited=set();probes.append(self)
            self.uc.hook_add(UC_HOOK_CODE,lambda uc,address,size,user:self.visited.add(address-self.code))
    try:
        pf.PfProbe=Tracking;rows=pf.matrix(mz)
    finally:pf.PfProbe=original
    if len(rows)!=len(probes):raise ValueError('root compare contextual probe count differs')
    for row,p in zip(rows,probes):row['visited']=sorted(a for a in p.visited if 0x2c30<=a<0x2c68)
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes();cold_raw=(ROOT/COLD).read_bytes()
    if sha(raw)!=PROOF_SHA or sha(cold_raw)!=COLD_SHA:raise ValueError('root tail prior PI/cold receipt differs')
    proof,cold=json.loads(raw),json.loads(cold_raw)
    inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_root_tail.py':sha(Path(__file__).read_bytes()),
            'tests/test_mainl_root_tail_review.py':sha((ROOT/'tests/test_mainl_root_tail_review.py').read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    if bytes(numeric_literals(providers['libs/master.lib/atan8[data].asm'],'db'))!=atan_table():raise ValueError('root atan frozen coefficients differ')
    def verify():
        for p,d in inputs.items():
            if sha((ROOT/p).read_bytes())!=d:raise ValueError('root tail input changed: '+p)
    def normalized(rows):
        return [{k:v for k,v in row.items() if k not in ('memory_before_sha256','memory_after_sha256','data_before_sha256','data_after_sha256')} for row in rows]
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];target=parse_mz((ROOT/proof['observations'][0]['path']).read_bytes())
    for index,prior in enumerate(proof['observations']):
        path=prior['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid or mz.program_image[0xe3f0+0x41c:0xe3f0+0x51c]!=atan_table():raise ValueError('root tail invalid image/atan table')
        observed=dict(path=path,analysis=analyze(mz.program_image))
        if index:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('root tail complete bodies/CFG/producers differ')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);data=(ROOT/cp).read_bytes();inputs[cp]=sha(data)
                actual=data.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else data
                if actual!=cached_provider(p,d):raise ValueError('root tail frozen provider differs: '+p)
            object_path=str(tree/'obj/th03/mainl.obj');data=(ROOT/object_path).read_bytes();obj=describe_omf(data);inputs[object_path]=sha(data)
            if (not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0']
                or obj['dependency_timestamp_normalized_sha256']!=cold['rounds'][index-1]['all_objects']['obj/th03/mainl.obj']):
                raise ValueError('root tail cold OMF identity differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments')}
            map_path=str(tree/'obj/th03/mainl.map');data=(ROOT/map_path).read_bytes();inputs[map_path]=sha(data);text=data.decode()
            carrier=next(r for r in code_rows(text,len(mz.program_image)) if r['module']=='th03_mainl.asm' and r['segment']==0 and r['size'])
            if not all(carrier['start']<=a<a+z<=carrier['start']+carrier['size'] for _,a,z in EXTENTS):raise ValueError('root tail escapes MAP carrier')
            for name,offset in PUBLICS.items():
                coords={(int(s,16),int(o,16)) for s,o in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(name)+r'\s*$',text,re.MULTILINE)}
                if coords!={(0,offset)}:raise ValueError('root tail public MAP entry differs: '+name)
            observed['carrier'],observed['public_entries']=carrier,PUBLICS
            observed['comparisons']={n:extent_observation(target,mz,dict(start=a,size=z,segment=0,offset=a)) for n,a,z in EXTENTS+[('prior-pfopen',0x2b16,281)]}
            observed['data_comparisons']={n:extent_observation(target,mz,dict(start=0xe3f0+a,size=z,segment=0xe3f,offset=a)) for n,a,z in
                                        [('atan',0x41c,256),('random',SEED,4),('joystick',JOYSTICK,8),('text',0x83a,8),('resident',RESIDENT,2),('tone',TONE,2),('identity',ID,10)]}
            if any(not r['raw_slice_equal'] or not r['ordered_relocations_equal'] for r in list(observed['comparisons'].values())+list(observed['data_comparisons'].values())):
                raise ValueError('root tail raw/ordered relocations differ')
        observed['cpu'],observed['prefixes'],observed['pf_context']=matrix(mz),prefixes(mz),pf_context(mz)
        visited={a for rows in (observed['cpu'],observed['prefixes'],observed['pf_context']) for row in rows for a in row['visited']}
        compare_body=observed['analysis']['native_compare']['native_compare']
        compare_bounds={i.address for i in Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[0x2c30:0x2c68],0x2c30)}
        own=set(observed['analysis']['bounds'])|compare_bounds
        observed['instruction_coverage']=dict(new_instructions=len(own),visited=len(own&visited),unvisited=sorted(own-visited),
                                              contextual_compare_instructions=compare_body['instructions'])
        if index and any(normalized(observed[key])!=normalized(observations[0][key]) for key in ('cpu','prefixes','pf_context')):
            raise ValueError('root tail target/cold CPU differs')
        observations.append(observed);print('Reviewed',path,len(observed['cpu']),'scenarios',len(observed['prefixes']),'prefixes',observed['instruction_coverage'],flush=True)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('root tail stored canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('root tail frozen provider changed')
    result=dict(kind='th03-mainl-complete-remaining-root-tail-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},
                observations=observations,build_scaffold_main_remaps=BUILD_REMAPS,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),
                diagnostic_checks_pass=True,new_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS remaining MAINL root722 with native/DOS/device/legacy PF context; source/exact open:',args.output)


if __name__=='__main__':main()
