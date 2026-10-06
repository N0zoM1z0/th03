#!/usr/bin/env python3
"""Complete MAINL gaiji candidates with native font helpers, heap and BFNT services."""
import argparse
from collections import Counter
from datetime import datetime,timezone
from importlib.metadata import version
import json
from pathlib import Path
import re
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
import review_th03_mainl_heap as heap
import review_th03_mainl_smem as smem
from review_th03_mainl_heap import TOP,OWN,ID,RESERVE,OUT,HEAP,HOLE,END,cached_provider,BUILD_REMAPS
from review_th03_mainl_super import Scalar as SuperScalar,SuperProbe,make_header as super_header
from review_th03_mainl_graphics import initial_flags,COLD,COLD_SHA

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-mainl-graphics-review-20261006.json'
PROOF_SHA='3b6525b43cf3f75885987ba9c190d0cf70bb2329e42d7fe7808c999c47773bd1'
OWN_RANGES=[('backup',0xc72,36,0),('restore',0xc96,28,0),('load',0xcb2,150,4),('getfont',0xd48,33,'near'),('read',0xd6a,37,6),('read_all',0xd90,36,4),('setfont',0xdb4,33,'near'),('write',0xdd6,39,6),('write_all',0xdfe,38,4)]
CONTEXT=heap.RANGES+smem.OWN_RANGES+[('skip',0x3b4,34,6),('header',0x3d6,59,6),('dos_open',0xaae,26,4)]
RANGES=OWN_RANGES+CONTEXT
ENTRY={n:a for n,a,_,_ in RANGES};ENTRY['get']=0x1ec0
NEW_ALIGN={a:0x90 for a in (0xd69,0xd8f,0xdd5,0xdfd)}
INTERIOR={a:0x90 for a in (0xc7e,0xca9,0xcc0,0xcd0,0xce1,0xd07,0xd31)}
CALLS={**heap.CALLS,0x1ebb:0x2186,0xc80:0x21c2,0xc8f:0xd90,0xca6:0xdfe,0xcab:0x22b2,0xcc2:0xaae,0xcd2:0x1ec0,0xce3:0x3d6,0xd09:0x3b4,0xd25:0xdfe,0xd33:0x1eaa}
NEAR={0xd84:0xd48,0xda5:0xd48,0xdf1:0xdb4,0xe14:0xdb4}
DOS={**heap.DOS,0x3c9:0x42,0x3e5:0x3f,0xaba:0x3d,0xd18:0x3f,0xd3c:0x3e}
PORTS={**{a:0x68 for a in (0xd81,0xd89,0xd99,0xdae,0xdee,0xdf6,0xe08,0xe1d)},0xd48:0xa1,0xd4c:0xa3,0xd56:0xa5,0xd60:0xa5,0xdb4:0xa1,0xdb8:0xa3,0xdc4:0xa5,0xdc7:0xa9,0xdcb:0xa5,0xdcf:0xa9}
INPUTS={0xd58:0xa9,0xd62:0xa9}
BACKUP,TEMPLATE=0x55a,0x55c
PROVIDERS=list(dict.fromkeys(smem.PROVIDERS+['libs/master.lib/'+n+'.asm' for n in ('gaiji_backup','gaiji_entry_bfnt','gaiji_read','gaiji_write','gaiji_backup[data]','gaiji_entry_bfnt[data]','bfnt_extend_header_skip','bfnt_header_read','bfnt_id[data]','dos_ropen')]))
PUBLICS={'GAIJI_BACKUP':0xc72,'GAIJI_RESTORE':0xc96,'GAIJI_ENTRY_BFNT':0xcb2,'GAIJI_READ':0xd6a,'GAIJI_READ_ALL':0xd90,'GAIJI_WRITE':0xdd6,'GAIJI_WRITE_ALL':0xdfe}
PATTERN_IMAGE=bytes((i*37+3)&255 for i in range(0x50001))


def make_header(s):return super_header(dict(color=0,height=16,last=255)|s)


def initial_fonts(seed=11):return bytes((index*29+row*7+half*113+seed)&255 for index in range(256) for row in range(16) for half in range(2))


def analyze(image):
    context=smem.analyze(image);decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;decoded=[];bounds=set();returns={};rows=[]
    for n,a,z,c in RANGES:
        body=image[a:a+z]
        if len(body)!=z:raise ValueError('gaiji complete body differs')
        ins=list(decoder.disasm(body,a))
        if not ins or sum(i.size for i in ins)!=z:raise ValueError('gaiji complete partition differs')
        expected=('ret','') if c=='near' else ('retf',str(c) if c else '')
        if n!='byte' and (ins[-1].mnemonic,ins[-1].op_str)!=expected:raise ValueError('gaiji terminal cleanup differs')
        decoded.append((n,a,z,c,ins,expected));bounds.update(i.address for i in ins)
    for n,a,z,c,ins,expected in decoded:
        edges=[]
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf'):
                if (i.mnemonic,i.op_str)!=expected:raise ValueError('gaiji interior cleanup differs')
                returns[i.address]=c
            if i.mnemonic=='int' and (i.bytes!=b'\xcd\x21' or i.address not in DOS):raise ValueError('gaiji unknown DOS site')
            if i.mnemonic in ('in','out'):
                sites=INPUTS if i.mnemonic=='in' else PORTS
                wanted=('al, '+hex(sites[i.address])) if i.mnemonic=='in' and i.address in sites else (hex(sites[i.address])+', al') if i.address in sites else None
                if i.op_str!=wanted:raise ValueError('gaiji unknown port site/width')
            if not(i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('gaiji unknown indirect edge')
            if i.mnemonic in ('lcall','ljmp'):raise ValueError('gaiji unknown far edge')
            dest=i.operands[0].imm
            if i.mnemonic=='call':
                if NEAR.get(i.address)!=dest:
                    if CALLS.get(i.address)!=dest:raise ValueError('gaiji unknown native call')
                    if not j or ins[j-1].bytes!=b'\x0e':raise ValueError('gaiji far call lacks PUSH CS')
            elif dest not in bounds:raise ValueError('gaiji branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=n,offset=a,size=z,instructions=len(ins),cleanup=c,sha256=sha(image[a:a+z]),edges=edges))
    if any(image[a:a+1]!=bytes([v]) for a,v in {**NEW_ALIGN,**INTERIOR,**heap.ALIGNMENT,**smem.ALIGNMENT}.items()):raise ValueError('gaiji producer alignment differs')
    if image[0xe3f0+TEMPLATE:0xe3f0+TEMPLATE+8]!=struct.pack('<4H',16,16,0,255):raise ValueError('gaiji header template differs')
    return dict(bodies=rows,bounds=sorted(bounds),returns=returns,new_body_bytes=430,new_alignment_bytes=4,new_extent_bytes=434,prior_context_bytes=823,heap_stack=context,alignment=NEW_ALIGN,interior_nopcall=INTERIOR,unowned_preceding_byte=dict(offset=0xc71,value=image[0xc71]),template_sha256=sha(image[0xe3f0+TEMPLATE:0xe3f0+TEMPLATE+8]))


class GaijiProbe(Probe):
    prepare=SuperProbe.prepare
    enter=SuperProbe.enter
    leave=SuperProbe.leave
    def __init__(self,mz,s,meta=None):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000);image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x20000,0x2e3f0,0x40000;self.s=s;self.meta=meta or analyze(mz.program_image);self.bounds=set(self.meta['bounds']);self.returns=self.meta['returns'];self.frames=[];self.pending=None;self.stop=False;self.errors=[];self.native=Counter();self.events=[];self.ports=[];self.visits=Counter();self.dos_index=0;self.fonts=bytearray(initial_fonts(s.get('seed',11)));self.low=0;self.high=0x56;self.row=0;self.mode=10;self.font_writes=0;self.memory_stores=0
        self.uc.mem_write(0x50000,PATTERN_IMAGE)
        self.uc.mem_write(0x50100,b'synthetic.bft\0')
        for a,key,default in ((TOP,'top',0x6000),(OWN,'own',0),(ID,'id',0xbeef),(RESERVE,'reserve',256),(OUT,'out',0x8800),(HEAP,'heap',0x8800),(HOLE,'hole',0),(END,'end',0x6000),(BACKUP,'backup',0)):
            self.uc.mem_write(self.data+a,struct.pack('<H',s.get(key,default)))
        self.uc.mem_write(self.data+0x558,struct.pack('<H',s.get('sharing',0xa500)))
        for seg,using,nextseg,ident in s.get('blocks',[]):self.uc.mem_write(seg*16,struct.pack('<3H',using,nextseg,ident))
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2000:raise ValueError('gaiji terminal segment alias')
                if self.frames or self.pending:raise ValueError('gaiji unfinished native frame')
                self.stop=True;uc.emu_stop();return
            off=address-self.code
            if self.get('CS')!=0x2000 or self.get('SS')!=0x4000:raise ValueError('gaiji CODE/stack segment alias')
            if off not in self.bounds:raise ValueError('CPU escaped gaiji instruction boundaries')
            self.visits[off]+=1
            if off in ENTRY.values():
                name=next(n for n,a in ENTRY.items() if a==off)
                if not(name=='get' and self.pending is None and self.frames and self.frames[-1]['name']=='get'):
                    self.enter(name,next(c for n,_,_,c in RANGES if n==name));self.native[name]+=1
            calls=CALLS|NEAR
            if off in calls:
                name=next(n for n,a in ENTRY.items() if a==calls[off]);cleanup='near' if off in NEAR else next(c for n,_,_,c in RANGES if n==name);self.prepare(name,self.get('SP')-2,off+3,cleanup)
            if off in self.returns:self.leave(self.returns[off])
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            state=any(self.data+a<=address and address+size<=self.data+a+z for a,z in ((TOP,6),(OUT,8),(BACKUP,2)))
            if not state and not(0x50000<=address and address+size<=0xa0001):raise ValueError('gaiji store outside declared state/pattern/heap span')
            self.memory_stores+=1
        def intr(uc,number,user):
            site=u16(self.get('IP')-2);ah=self.get('AH')
            if number!=0x21 or self.get('CS')!=0x2000 or DOS.get(site)!=ah:raise ValueError('gaiji unknown DOS request/site')
            if ah in (0x48,0x49):
                if ah==0x48:
                    i=self.dos_index;self.dos_index+=1;item=(s.get('dos_allocs',[])+[{}]*3)[i];query=site==0x218c;request=self.get('BX');ax=item.get('ax',8 if query else 0x6000);cf=item.get('cf',1 if query else 0);bx=item.get('bx',s.get('largest',0x200) if query else request);self.set('BX',bx);event=dict(site=site,name='dos_allocate',size=request,ax=ax,bx=bx,cf=cf)
                else:ax=s.get('dos_free_ax',7);cf=s.get('dos_free_cf',1);event=dict(site=site,name='dos_free',segment=self.get('ES'),ax=ax,cf=cf)
            elif ah==0x3d:ax=s.get('open_ax',0x1234);cf=s.get('open_cf',0);event=dict(site=site,name='dos_open',mode=self.get('AL'),filename=[self.get('DX'),self.get('DS')],ax=ax,cf=cf)
            elif ah==0x3e:ax=s.get('close_ax',7);cf=s.get('close_cf',0);event=dict(site=site,name='dos_close',handle=self.get('BX'),ax=ax,cf=cf)
            elif ah==0x42:ax=s.get('seek_ax',0);cf=s.get('seek_cf',0);event=dict(site=site,name='dos_seek',handle=self.get('BX'),offset=(self.get('CX')<<16)|self.get('DX'),origin=self.get('AL'),ax=ax,cf=cf)
            else:
                kind='header' if site==0x3e5 else 'font';count=self.get('CX');seg=self.get('DS');offset=self.get('DX');default=make_header(s) if kind=='header' else bytes((i*19+7)&255 for i in range(count));item=s.get(kind+'_read',{});payload=bytes(item.get('payload',list(default)))[:count];ax=item.get('ax',len(payload));cf=item.get('cf',0)
                if cf and not item.get('inject_on_failure'):payload=b''
                first=min(len(payload),65536-offset)
                if first:uc.mem_write(seg*16+offset,payload[:first])
                if first<len(payload):uc.mem_write(seg*16,payload[first:])
                event=dict(site=site,name='dos_read',kind=kind,handle=self.get('BX'),destination=[offset,seg],count=count,payload_hex=payload.hex(),ax=ax,cf=cf)
            self.events.append(event);self.set('AX',ax);self.set('EFLAGS',(self.get('EFLAGS')&~1)|cf)
        def font_position():
            if self.mode!=11 or self.high not in (0x56,0x57) or self.low>=128 or self.row&~0x2f:raise ValueError('gaiji unknown font latch/mode')
            return ((self.high-0x56)*128+self.low)*32+(self.row&15)*2+(0 if self.row&32 else 1)
        def event(site,port,value,direction):return dict(site=site,port=port,width=1,value=value,direction=direction,live_if=bool(self.get('EFLAGS')&512),live_df=bool(self.get('EFLAGS')&1024))
        def out(uc,port,width,value,user):
            if self.get('CS')!=0x2000 or PORTS.get(self.get('IP'))!=port or width!=1:raise ValueError('gaiji unknown output port/site/width')
            self.ports.append(event(self.get('IP'),port,value,'out'))
            if port==0x68:
                if value not in (10,11):raise ValueError('gaiji unknown font access mode')
                self.mode=value
            elif port==0xa1:self.low=value
            elif port==0xa3:self.high=value
            elif port==0xa5:self.row=value
            else:self.fonts[font_position()]=value;self.font_writes+=1
        def inp(uc,port,width,user):
            if self.get('CS')!=0x2000 or INPUTS.get(self.get('IP'))!=port or width!=1:raise ValueError('gaiji unknown input port/site/width')
            value=self.fonts[font_position()];self.ports.append(event(self.get('IP'),port,value,'in'));return value
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr));self.uc.hook_add(UC_HOOK_INSN,guard(out),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)
    def word(self,a):return struct.unpack('<H',self.uc.mem_read(self.data+a,2))[0]
    def run(self,name,args=(),budget=3000000):
        if name in ('getfont','setfont'):raise ValueError('gaiji private near helper requires complete public caller')
        self.stop=False;self.errors.clear();self.frames.clear();self.pending=None;cleanup=next(c for n,_,_,c in RANGES if n==name)
        values=dict(CS=0x2000,DS=0x2e3f,SS=0x4000,ES=0x3333,AX=0x1111,BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,SP=0xffc0,EFLAGS=initial_flags(self.s))
        for r,v in values.items():self.set(r,v)
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2000,*args));self.prepare(name,0xffc0,0xff00,cleanup);self.uc.emu_start(self.code+ENTRY[name],0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('gaiji terminal/budget differs')
        if self.get('SP')!=0xffc4+cleanup or any(self.get(r)!=values[r] for r in ('BP','SI','DI','DS')):raise ValueError('gaiji cleanup/preserved-register differs')


class Scalar(SuperScalar):
    def __init__(self,p):
        super().__init__(p);self.fonts=bytearray(p.fonts);self.flags=initial_flags(p.s);self.df=bool(self.flags&1024);self.mode=10;self.low=0;self.high=0x56;self.row=0
    def port(self,site,port,value,direction='out'):
        self.ports.append(dict(site=site,port=port,width=1,value=value,direction=direction,live_if=bool(self.flags&512),live_df=self.df))
        if direction=='in':return
        if port==0x68:self.mode=value
        elif port==0xa1:self.low=value
        elif port==0xa3:self.high=value
        elif port==0xa5:self.row=value
    def glyphs(self,name,args):
        writing=name in ('write','write_all');all_=name.endswith('_all');offset,segment=args[:2]
        if not all_:self.flags|=512
        mode_sites=(0xe08,0xe1d) if writing and all_ else (0xdee,0xdf6) if writing else (0xd99,0xdae) if all_ else (0xd81,0xd89)
        self.port(mode_sites[0],0x68,11);cursor=offset;direction=-2 if self.df else 2
        for i in range(256 if all_ else 1):
            chr_=i if all_ else args[2]&255;code=u16(0x5680+chr_+(int(bool(self.flags&1)) if all_ and i==0 else 0));index=((code>>8)-0x56)*128+(code&127);self.flags&=~1;self.native['setfont' if writing else 'getfont']+=1
            self.port(0xdb4 if writing else 0xd48,0xa1,code&127);self.port(0xdb8 if writing else 0xd4c,0xa3,code>>8)
            for row in range(16):
                address=segment*16+cursor;pos=index*32+row*2
                if writing:
                    word=self.mem[address:address+2];self.port(0xdc4,0xa5,row|32);self.port(0xdc7,0xa9,word[0]);self.fonts[pos]=word[0];self.port(0xdcb,0xa5,row);self.port(0xdcf,0xa9,word[1]);self.fonts[pos+1]=word[1]
                else:
                    self.port(0xd56,0xa5,row);self.port(0xd58,0xa9,self.fonts[pos+1],'in');self.port(0xd60,0xa5,row|32);self.port(0xd62,0xa9,self.fonts[pos],'in');self.mem[address:address+2]=self.fonts[pos:pos+2]
                cursor=u16(cursor+direction)
        self.port(mode_sites[1],0x68,10);return None,0
    def read(self,site,kind,handle,seg,offset,count):
        default=make_header(self.s) if kind=='header' else bytes((i*19+7)&255 for i in range(count));item=self.s.get(kind+'_read',{});payload=bytes(item.get('payload',list(default)))[:count];ax=item.get('ax',len(payload));cf=item.get('cf',0)
        if cf and not item.get('inject_on_failure'):payload=b''
        for i,v in enumerate(payload):self.mem[seg*16+u16(offset+i)]=v
        self.events.append(dict(site=site,name='dos_read',kind=kind,handle=handle,destination=[offset,seg],count=count,payload_hex=payload.hex(),ax=ax,cf=cf));return ax,cf
    def load(self,args):
        handle,cf=self.run('dos_open',args)
        if cf:return 0,0
        segment,cf=self.run('get',[8192]);success=0
        if not cf:
            off=0xff9a;_,fault=self.run('header',[off,0x4000,handle])
            if not fault and self.mem[0x40000+off+5]==0:
                stride=-2 if self.df else 2
                matches=all(self.mem[self.data+u16(TEMPLATE+j*stride):self.data+u16(TEMPLATE+j*stride)+2]==self.mem[0x40000+u16(off+8+j*stride):0x40000+u16(off+8+j*stride)+2] for j in range(4))
                if matches:
                    self.run('skip',[off,0x4000,handle]);ax,_=self.read(0xd18,'font',handle,segment,0,8192)
                    if ax==8192:self.flags&=~1;self.run('write_all',[0,segment]);success=1
            self.run('release',[segment])
        self.events.append(dict(site=0xd3c,name='dos_close',handle=handle,ax=self.s.get('close_ax',7),cf=self.s.get('close_cf',0)))
        return success,0
    def run(self,name,args=()):
        if name not in {n for n,_,_,_ in OWN_RANGES}:return super().run(name,args)
        self.native[name]+=1
        if name in ('read','read_all','write','write_all'):return self.glyphs(name,args)
        if name=='backup':
            if self.get(BACKUP):return 0,0
            segment,_=self.run('allocate',[512])
            if not segment:return 0,0
            self.put(BACKUP,segment);self.flags&=~1;self.run('read_all',[0,segment]);return 1,0
        if name=='restore':
            segment=self.get(BACKUP)
            if not segment:return 0,0
            self.put(BACKUP,0);self.flags&=~1;self.run('write_all',[0,segment]);_,cf=self.run('free',[segment]);return 1,cf
        if name=='load':return self.load(args)
        raise ValueError('scalar private font helper requires caller')


def compare(p,spec,ax,cf,label):
    actual=bytes(p.uc.mem_read(0,0x100000))
    if (ax is not None and p.get('AX')!=ax) or (cf is not None and p.get('EFLAGS')&1!=cf) or bool(p.get('EFLAGS')&512)!=bool(spec.flags&512) or bool(p.get('EFLAGS')&1024)!=spec.df or p.native!=spec.native or p.events!=spec.events or p.ports!=spec.ports or p.fonts!=spec.fonts or (p.mode,p.low,p.high,p.row)!=(spec.mode,spec.low,spec.high,spec.row):
        raise ValueError('gaiji scalar AX/CF/IF/DF/entries/DOS/ports/font-latches differs: '+str((label,p.get('AX'),ax,p.get('EFLAGS')&1,cf,dict(p.native),dict(spec.native),p.events,spec.events,p.ports[:8],spec.ports[:8])))
    if actual[:p.stack]!=spec.mem[:p.stack] or actual[p.stack+65536:]!=spec.mem[p.stack+65536:]:
        changed=[i for i,(a,b) in enumerate(zip(actual,spec.mem)) if a!=b and not p.stack<=i<p.stack+65536];raise ValueError('gaiji full physical memory differs: '+str((label,changed[:24])))


def trace_hash(rows):return sha(json.dumps(rows,separators=(',',':')).encode())


def matrix(mz):
    meta=analyze(mz.program_image);rows=[]
    def observe(label,s,steps):
        p=GaijiProbe(mz,s,meta);spec=Scalar(p);before=sha(bytes(spec.mem));results=[]
        for name,args in steps:
            spec.flags=initial_flags(s);spec.df=bool(spec.flags&1024);ax,cf=spec.run(name,args);p.run(name,args);compare(p,spec,ax,cf,(label,s,name,args))
            results.append(dict(function=name,args=args,ax=ax,cf=cf,live_if=bool(spec.flags&512),df=spec.df,registers={r:p.get(r) for r in ('AX','BX','CX','DX','BP','SI','DI','DS','ES','SP')},backup=spec.get(BACKUP),heap=spec.get(HEAP),end=spec.get(END),fonts_sha256=sha(bytes(spec.fonts))))
        rows.append(dict(function=label,scenario=s,steps=results,top_level_calls=len(steps),native_entries=dict(p.native),events=p.events,ports_count=len(p.ports),ports_sha256=trace_hash(p.ports),ports_prefix=p.ports[:8],ports_suffix=p.ports[-8:],font_writes=p.font_writes,memory_stores=p.memory_stores,visited=sorted(p.visits),memory_before_sha256=before,memory_after_sha256=sha(bytes(spec.mem))))
    for df in (False,True):
        for irq in (0,512):
            base=dict(df=df,flags=2|irq)
            for char in list(range(256))+[256,257,511,512,0xffff]:
                for name in ('read','write'):observe('single-all-low-byte-codes',dict(base),[(name,[0x200,0x5000,char])])
            for offset in (0,1,0xffe0,0xffff):
                for name in ('read','write'):observe('single-pointer-wrap',dict(base),[(name,[offset,0x5000,255])])
            for cf in (0,1):
                for name in ('read_all','write_all'):observe('all-incoming-carry',dict(base,flags=2|irq|cf),[(name,[0,0x5000])])
            for offset in (1,0xfff1):
                for name in ('read_all','write_all'):observe('all-pointer-wrap',dict(base),[(name,[offset,0x5000])])
            observe('connected-font-backup-restore',dict(base),[('backup',[]),('backup',[]),('write',[0x200,0x5000,17]),('restore',[]),('restore',[])])
            observe('restore-invalid-free',dict(base,backup=0x5000),[('restore',[])])
            for heap_ in (0x6000,0x61ff,0x6200,0x6201):observe('backup-allocation-boundary',dict(base,heap=heap_,out=heap_),[('backup',[])])
            for name,args in (('backup',[]),('load',[0x100,0x5000])):
                for item in ({},{'cf':1,'ax':8}):observe('native-automatic-assignment',dict(base,top=0,largest=0x2800,dos_allocs=[{},item]),[(name,args)])
            for s in ({},{'open_cf':1},{'heap':0x6000},{'color':3},{'width':8},{'height':15},{'first':1},{'last':254},{'extension_size':7},{'extension_size':7,'seek_cf':1},{'close_cf':1}):observe('loader-header-status',dict(base,**s),[('load',[0x100,0x5000])])
            for key in ('header_read','font_read'):
                for item in ({'cf':1,'ax':5},{'cf':1,'ax':0},{'cf':0,'ax':0,'payload':[]},{'cf':0,'ax':2,'payload':[66,70]},{'cf':0,'ax':8191},{'cf':0,'ax':8192},{'cf':1,'ax':8192},{'cf':0,'ax':8193}):observe('loader-short-carry-status',dict(base,**{key:item}),[('load',[0x100,0x5000])])
            if not df:observe('connected-backup-load-restore',dict(base),[('backup',[]),('load',[0x100,0x5000]),('restore',[])])
    return rows


def nonterminal(mz):
    rows=[];meta=analyze(mz.program_image)
    for df in (False,True):
        for irq in (0,512):
            s=dict(df=df,flags=2|irq,hole=0x7000,blocks=[[0x7000,1,0x7000,0xbeef]])
            p=GaijiProbe(mz,s,meta);spec=Scalar(p);before=sha(bytes(spec.mem));budget=1000
            try:p.run('backup',[],budget)
            except ValueError as e:
                if str(e)!='gaiji terminal/budget differs':raise
            else:raise ValueError('gaiji cyclic heap unexpectedly returned')
            spec.native.update(backup=1,allocate=1);compare(p,spec,None,None,'cyclic heap native prefix')
            if len(p.frames)!=2 or p.pending or p.stop or p.memory_stores or p.font_writes:raise ValueError('gaiji cyclic prefix state/frame differs')
            rows.append(dict(function='backup',scenario=s,budget=budget,outcome='native-execution-budget',instruction=p.get('IP'),native_entries=dict(p.native),backup=p.word(BACKUP),memory_stores=p.memory_stores,ports_count=len(p.ports),fonts_sha256=sha(bytes(p.fonts)),memory_before_sha256=before,memory_after_sha256=sha(bytes(spec.mem))))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('gaiji prior graphics proof differs')
    proof=json.loads(raw);cold_raw=(ROOT/COLD).read_bytes()
    if sha(cold_raw)!=COLD_SHA:raise ValueError('gaiji cold proof differs')
    cold=json.loads(cold_raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_gaiji.py':sha(Path(__file__).read_bytes()),'tests/test_mainl_gaiji_review.py':sha((ROOT/'tests/test_mainl_gaiji_review.py').read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('gaiji input changed: '+p)
    def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('memory_before_sha256','memory_after_sha256')} for row in cpu]
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact);observations=[];objects=[]
    for i,prior in enumerate(proof['observations']):
        path=prior['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('gaiji invalid decoded image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz),nonterminal=nonterminal(mz))
        if i:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('gaiji complete bodies/CFG differ')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);data=(ROOT/cp).read_bytes();inputs[cp]=sha(data);actual=data.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else data
                if actual!=cached_provider(p,d):raise ValueError('gaiji frozen cached provider differs: '+p)
            op=str(tree/'obj/th03/mainl.obj');data=(ROOT/op).read_bytes();obj=describe_omf(data);inputs[op]=sha(data)
            if not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0'] or obj['dependency_timestamp_normalized_sha256']!=cold['rounds'][i-1]['all_objects']['obj/th03/mainl.obj']:raise ValueError('gaiji root cold OMF identity differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments')};objects.append(observed['object'])
            if len(objects)>1 and objects[-1]['dependency_timestamp_normalized_sha256']!=objects[0]['dependency_timestamp_normalized_sha256']:raise ValueError('gaiji root OMF changes beyond timestamps')
            mp=str(tree/'obj/th03/mainl.map');text=(ROOT/mp).read_text();inputs[mp]=sha((ROOT/mp).read_bytes());carrier=next(r for r in code_rows(text,len(mz.program_image)) if r['module']=='th03_mainl.asm' and r['segment']==0 and r['size'])
            if not all(carrier['start']<=a<a+z<=carrier['start']+carrier['size'] for _,a,z,_ in RANGES):raise ValueError('gaiji complete includes outside MAP carrier')
            for name,off in PUBLICS.items():
                coords={(int(s,16),int(o,16)) for s,o in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(name)+r'\s*$',text,re.MULTILINE)}
                if coords!={(0,off)}:raise ValueError('gaiji public MAP entry differs')
            observed['carrier']=carrier;observed['public_entries']=PUBLICS;target=parse_mz((ROOT/proof['observations'][0]['path']).read_bytes());extents=[('gaiji-backup',0xc72,64),('gaiji-load',0xcb2,150),('gaiji-read',0xd48,108),('gaiji-write',0xdb4,112)]+[(f'prior-{n}',a,z) for n,a,z,_ in CONTEXT]+[(f'prior-even-{a:x}',a,1) for a in heap.ALIGNMENT|smem.ALIGNMENT]
            observed['comparisons']={n:extent_observation(target,mz,dict(start=a,size=z,segment=0,offset=a)) for n,a,z in extents}
            observed['data_comparison']=extent_observation(target,mz,dict(start=0xe3f0+BACKUP,size=10,segment=0xe3f,offset=BACKUP))
            if any(not v['raw_slice_equal'] or not v['ordered_relocations_equal'] for v in list(observed['comparisons'].values())+[observed['data_comparison']]):raise ValueError('gaiji raw/ordered relocations differ')
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']) or normalized(observed['nonterminal'])!=normalized(observations[0]['nonterminal']):raise ValueError('gaiji target/cold CPU differs')
        observations.append(observed);print('Reviewed',path,len(observed['cpu']),'scenarios',len(observed['nonterminal']),'budgets',flush=True)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('gaiji canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('gaiji frozen provider changed')
    result=dict(kind='th03-mainl-complete-gaiji-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},build_scaffold_main_remaps=BUILD_REMAPS,observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,new_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL gaiji434bytes, native heap/stack/header/open823context; exact open:',args.output)


if __name__=='__main__':main()
