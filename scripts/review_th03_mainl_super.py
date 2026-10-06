#!/usr/bin/env python3
"""Complete MAINL BFNT and super sprite candidates with native heap/stack context."""
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
import review_th03_mainl_heap as heap
import review_th03_mainl_smem as smem
from review_th03_mainl_heap import TOP,OWN,ID,RESERVE,OUT,HEAP,HOLE,END,cached_provider,BUILD_REMAPS
from review_th03_mainl_palette import RANGES as PALETTE_RANGES
from review_th03_mainl_vsync import PROVIDERS as VSYNC_PROVIDERS

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-mainl-vsync-review-20261006.json'
PROOF_SHA256='d09b66220f232c57e69d45eccd8ab98e1f24efbfba365abfa832f49566e022e4'
OWN_RANGES=[('bfnt',0x272,322,8),('skip',0x3b4,34,6),('header',0x3d6,59,6),('extend',0x412,95,6),
 ('free_all',0x237e,48,0),('entry',0x23ae,191,8),('entry_at',0x246e,116,6),
 ('load',0x24e2,137,4),('cancel',0x256c,79,2),('put',0x25bc,240,6),
 ('draw1',0x26ac,35,'near'),('draw2',0x26d0,45,'near'),('draw3',0x26fe,54,'near'),('draw4',0x2734,49,'near'),('draw',0x2766,8,'near'),('dos_close',0xa98,21,2)]
CONTEXT=heap.RANGES+smem.OWN_RANGES+[r for r in PALETTE_RANGES if r[0] in ('bfnt','dos_open')]
CONTEXT=[('palette' if n=='bfnt' else n,a,z,c) for n,a,z,c in CONTEXT]
RANGES=OWN_RANGES+CONTEXT
ENTRIES={n:a for n,a,_,_ in RANGES};ENTRIES.update(bfnt=0x286,entry=0x23c2,get=0x1ec0)
ALIGNMENT={0x411:0x90,0x471:0x90,0x246d:0x90,0x256b:0x90,0x25bb:0x90,0x26cf:0x90,0x26fd:0x90,0x2765:0x90,0xaad:0x90}
CALLS={0x279:0x1eaa,0x2d6:0x1ec0,0x2de:0x1ec0,0x371:0x23c2,0x388:0x1eaa,0x38c:0x1eaa,0x3a2:0x1eaa,0x3a6:0x1eaa,0x429:0x1ec0,0x469:0x1eaa,
 0x238a:0x22b2,0x2398:0x256c,0x23b1:0x22b2,0x23e3:0x21ae,0x23f1:0x246e,0x2491:0x21c2,0x24c4:0x22b2,0x24ef:0xaae,0x24ff:0x3d6,0x2521:0x412,0x2535:0x4c6,0x2542:0x286,0x254a:0xa98,0x255f:0xa98,0x258b:0x22b2}
NEAR_CALLS={a:0x2766 for a in (0x2677,0x2689,0x2690,0x2697,0x269e)}
DRAW_TARGETS=(0x26ac,0x26d0,0x26fe,0x2734)
DOS={0x2f1:0x3f,0x3c9:0x42,0x3e5:0x3f,0x438:0x3f,0xaa0:0x3e,0x4df:0x3f,0xaba:0x3d,**heap.DOS}
PORTS={a:0x7c for a in (0x2666,0x267d,0x268e,0x2695,0x269c,0x26a3)}|{a:0x7e for a in (0x266a,0x266c,0x266e,0x2670,0x2681,0x2683,0x2685,0x2687)}
SMC={0x35f:2,0x36d:2,0x2ed:2,0x309:1,0x364:2,0x307:1,0x302:2,0x2e8:2,0x2769:2,0x26c9:1,0x26c7:1,0x276c:2,0x26f7:1,0x26f5:1,0x272e:1,0x272c:1,0x275f:1,0x275d:1}
BUFFER,PATNUM,CHARFREE,PATDATA,PATSIZE,HEADER,PALETTE=0x87a,0x87c,0x87e,0x1460,0x1860,0x85a,0x141e
PROVIDERS=list(dict.fromkeys(VSYNC_PROVIDERS+smem.PROVIDERS+['libs/master.lib/'+n+'.asm' for n in ('bfnt_entry_pat','bfnt_extend_header_skip','bfnt_header_read','bfnt_header_analysis','super_free','super_entry_pat','super_entry_at','super_entry_bfnt','super_cancel_pat','super_put','dos_close','bfnt_id[data]','superpa[data]','superpa[bss]','super_entry_bfnt[data]','wordmask[data]')]))


def analyze(image):
    contexts=smem.analyze(image);decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[];returns={};bounds=set();all_ins=[]
    for n,a,z,c in RANGES:
        body=image[a:a+z]
        if len(body)!=z:raise ValueError('super complete include body differs')
        ins=list(decoder.disasm(body,a))
        if not ins or sum(i.size for i in ins)!=z:raise ValueError('super complete instruction partition differs')
        bounds.update(i.address for i in ins);all_ins.append((n,a,z,c,ins))
    for n,a,z,c,ins in all_ins:
        edges=[];own=n in {x[0] for x in OWN_RANGES}
        expected=('ret','') if c=='near' else ('retf',str(c) if c else '')
        if own and n!='draw' and (ins[-1].mnemonic,ins[-1].op_str)!=expected:raise ValueError('super terminal cleanup differs')
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf'):
                if (i.mnemonic,i.op_str)!=expected:raise ValueError('super near/far cleanup differs')
                returns[i.address]=c
            if not own:continue
            if i.mnemonic in ('int','in','out'):
                if i.mnemonic=='int':
                    if DOS.get(i.address) is None or i.bytes!=b'\xcd\x21':raise ValueError('super unknown DOS site')
                elif i.mnemonic!='out' or i.address not in PORTS:raise ValueError('super unknown port site')
                edges.append(dict(instruction=i.address,kind=i.mnemonic));continue
            if i.address==0x23a9:
                if i.bytes!=b'\xff\x16\x7e\x08':raise ValueError('super character-free operand differs')
                edges.append(dict(instruction=i.address,kind='declared-near-callback'));continue
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('super unknown indirect edge')
            if i.mnemonic in ('lcall','ljmp'):raise ValueError('super unknown far edge')
            dest=i.operands[0].imm
            if i.mnemonic=='call':
                if NEAR_CALLS.get(i.address)!=dest:
                    if CALLS.get(i.address)!=dest:raise ValueError('super unknown native call')
                    if not j or ins[j-1].bytes!=b'\x0e':raise ValueError('super far call lacks PUSH CS')
            elif dest not in bounds:raise ValueError('super branch enters data/operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=n,offset=a,size=z,instructions=len(ins),sha256=sha(image[a:a+z]),cleanup=c,edges=edges))
    if any(image[a:a+1]!=bytes([v]) for a,v in ALIGNMENT.items()):raise ValueError('super complete producer alignment differs')
    if image[0x276b:0x276e]!=b'\xe9\x3e\xff':raise ValueError('super initial mutable dispatch differs')
    if image[0x23b7]!=0x90 or image[0x25b3]!=0x90 or image[0x399]!=0x90:raise ValueError('super interior EVEN differs')
    return dict(bodies=rows,returns=returns,bounds=sorted(bounds),heap_stack=contexts,new_extent_bytes=1542,prior_context_bytes=794,smc=SMC,alignment=ALIGNMENT,draw_targets=DRAW_TARGETS)


def make_header(s):
    data=bytearray(32);data[:5]=b'BFNT\x1a';data[5]=s.get('color',3)
    for off,key,default in ((8,'width',16),(10,'height',2),(12,'first',0),(14,'last',0),(28,'extension_size',0),(30,'extension_header_size',4)):struct.pack_into('<H',data,off,s.get(key,default))
    return bytes(data)


class SuperProbe(Probe):
    def __init__(self,mz,s,observed=None):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x20000,0x2e3f0,0x40000
        self.s=s;self.errors=[];self.events=[];self.ports=[];self.native=Counter();self.stop=False;self.frames=[];self.pending=None;self.direct=None;self.write_count=0;self.read_index=0;self.dos_index=0;self.temps=[];self.source='bfnt';self.char_calls=0;self.dispatch_pending=False;self.vram_writes=0;self.conversion_writes=0
        self.meta=observed or analyze(mz.program_image);self.returns=self.meta['returns'];self.bounds=set(self.meta['bounds']);self.entry_names={a:n for n,a in ENTRIES.items()}
        self.uc.mem_write(0x50000,bytes((i*37+s.get('seed',11))&255 for i in range(65536)));self.uc.mem_write(0x50100,b'synthetic.bft\0');self.uc.mem_write(0x51000,make_header(s));self.uc.mem_write(0x60000,b'\xa5'*0x30000);self.uc.mem_write(0xa8000,b'\xa5'*65537);self.uc.mem_write(self.code+0x8000,b'\xc3')
        self.uc.mem_write(self.data+HEADER,make_header(s));self.uc.mem_write(self.data+PATDATA,b'\0'*2048);self.uc.mem_write(self.data+PALETTE,bytes((i*13+3)&255 for i in range(48)))
        for a,key,default in ((TOP,'top',0x6000),(OWN,'own',0),(ID,'id',0xbeef),(RESERVE,'reserve',256),(OUT,'out',0x8800),(HEAP,'heap',0x8800),(HOLE,'hole',0),(END,'end',0x6000),(BUFFER,'buffer',0),(PATNUM,'patnum',0),(CHARFREE,'charfree',0)):
            self.uc.mem_write(self.data+a,struct.pack('<H',s.get(key,default)))
        for num,size,seg in s.get('patterns',[]):
            self.uc.mem_write(self.data+u16(PATSIZE+u16(num*2)),struct.pack('<H',size));self.uc.mem_write(self.data+u16(PATDATA+u16(num*2)),struct.pack('<H',seg))
        for seg,using,nextseg,ident in s.get('blocks',[]):self.uc.mem_write(seg*16,struct.pack('<3H',using,nextseg,ident))
        self.uc.mem_write(self.data+0x558,struct.pack('<H',s.get('sharing',0xa500)))
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2000:raise ValueError('super terminal segment alias')
                if self.frames or self.pending:raise ValueError('super unfinished native frame')
                self.stop=True;uc.emu_stop();return
            off=address-self.code
            if self.get('CS')!=0x2000 or self.get('SS')!=0x4000:raise ValueError('super CODE/stack segment alias')
            if off==0x8000:
                self.enter('character_free','near');self.char_calls+=1;self.events.append(dict(name='character_free',patnum=self.word(PATNUM),buffer=self.word(BUFFER)));self.leave('near');return
            if off not in self.bounds:raise ValueError('CPU escaped super instruction ownership')
            if off in DRAW_TARGETS and self.pending is None and self.frames and self.frames[-1]['name']=='draw':
                if self.dispatch_pending:self.native[self.entry_names[off]]+=1;self.dispatch_pending=False
            elif off in self.entry_names:
                name=self.entry_names[off]
                if not(name=='get' and self.pending is None and self.frames and self.frames[-1]['name']=='get'):
                    self.enter(name,next(c for n,_,_,c in RANGES if n==name));self.native[name]+=1
            calls={**heap.CALLS,0x1ebb:0x2186,**CALLS,**NEAR_CALLS}
            if off in calls:self.prepare(self.entry_names[calls[off]],self.get('SP')-2,off+3,'near' if off in NEAR_CALLS else next(c for n,_,_,c in RANGES if ENTRIES.get(n)==calls[off]))
            if off==0x23a9:
                if self.word(CHARFREE)!=0x8000:raise ValueError('super undeclared character-free target')
                self.prepare('character_free',self.get('SP')-2,0x23ad,'near')
            if off==0x276b:
                displacement=struct.unpack('<h',uc.mem_read(self.code+0x276c,2))[0];target=0x276e+displacement
                if target not in DRAW_TARGETS:raise ValueError('super mutable dispatch enters operand/neighbor')
                self.dispatch_pending=True
            if off in self.returns:
                if self.frames and self.frames[-1]['name']=='get' and not self.get('EFLAGS')&1:self.temps.append(self.get('AX'))
                self.leave(self.returns[off])
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            state=[(self.data+TOP,8),(self.data+OUT,8),(self.data+BUFFER,6),(self.data+PATDATA,2048),(self.data+PALETTE,48)]
            allowed=any(a<=address and address+size<=a+z for a,z in state) or any(address==self.code+a and size==z for a,z in SMC.items()) or 0x60000<=address and address+size<=0x90000 or 0xa8000<=address and address+size<=0xb8001
            if not allowed:raise ValueError('super write outside declared state/heap/temporary/VRAM span: '+str((hex(address),size,hex(self.get('IP')))))
            self.write_count+=1
            if 0xa8000<=address<0xb8001:self.vram_writes+=1
            if self.get('IP') in (0x341,0x346,0x34b,0x350):self.conversion_writes+=1
        def intr(uc,number,user):
            site=u16(self.get('IP')-2);ah=self.get('AH')
            if number!=0x21 or self.get('CS')!=0x2000 or DOS.get(site)!=ah:raise ValueError('super unknown DOS request/site')
            if ah in (0x48,0x49):
                if ah==0x48:
                    i=self.dos_index;self.dos_index+=1;item=(s.get('dos_allocs',[])+[{}]*3)[i];query=site==0x218c;request=self.get('BX');ax=item.get('ax',8 if query else 0x6000);cf=item.get('cf',1 if query else 0);bx=item.get('bx',s.get('largest',0x2800) if query else request);self.set('BX',bx);event=dict(site=site,name='dos_allocate',size=request,ax=ax,bx=bx,cf=cf)
                else:ax=s.get('dos_free_ax',7);cf=s.get('dos_free_cf',1);event=dict(site=site,name='dos_free',segment=self.get('ES'),ax=ax,cf=cf)
            elif ah==0x3d:ax=s.get('open_ax',0x1234);cf=s.get('open_cf',0);event=dict(site=site,name='dos_open',mode=self.get('AL'),filename=[self.get('DX'),self.get('DS')],ax=ax,cf=cf)
            elif ah==0x3e:ax=s.get('close_ax',7);cf=s.get('close_cf',0);event=dict(site=site,name='dos_close',handle=self.get('BX'),ax=ax,cf=cf)
            elif ah==0x42:ax=s.get('seek_ax',0);cf=s.get('seek_cf',0);event=dict(site=site,name='dos_seek',handle=self.get('BX'),offset=(self.get('CX')<<16)|self.get('DX'),origin=self.get('AL'),ax=ax,cf=cf)
            else:
                kind={0x3e5:'header',0x438:'extension',0x4df:'palette',0x2f1:'pixels'}[site];count=self.get('CX');seg=self.get('DS');offset=self.get('DX')
                default=make_header(s) if kind=='header' else bytes(s.get('extension',[0x10,0,0,7])) if kind=='extension' else bytes(range(48)) if kind=='palette' else bytes((i*29+self.read_index*7+1)&255 for i in range(count))
                item=s.get(kind+'_read',{});payload=bytes(item.get('payload',list(default)))[:count];ax=item.get('ax',len(payload));cf=item.get('cf',0)
                if cf and not item.get('inject_on_failure'):payload=b''
                for i,v in enumerate(payload):uc.mem_write(seg*16+u16(offset+i),bytes([v]))
                event=dict(site=site,name='dos_read',kind=kind,handle=self.get('BX'),destination=[offset,seg],count=count,payload_hex=payload.hex(),ax=ax,cf=cf);self.read_index+=kind=='pixels'
            self.events.append(event);self.set('AX',ax);self.set('EFLAGS',(self.get('EFLAGS')&~1)|cf)
        def out(uc,port,width,value,user):
            if self.get('CS')!=0x2000 or PORTS.get(self.get('IP'))!=port or width!=1:raise ValueError('super unknown output port/site/width')
            self.ports.append(dict(site=self.get('IP'),port=port,value=value))
        def inp(uc,port,width,user):raise ValueError('super unexpected input port')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(out),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)
    def word(self,a):return struct.unpack('<H',self.uc.mem_read(self.data+a,2))[0]
    def prepare(self,name,sp,ip,cleanup):
        if self.pending:raise ValueError('super overlapping native entry')
        self.pending=dict(name=name,sp=u16(sp),ip=ip,cleanup=cleanup)
    def enter(self,name,cleanup):
        f=self.pending;sp=self.get('SP');frame=tuple(struct.unpack('<'+'H'*(1 if cleanup=='near' else 2),self.uc.mem_read(self.stack+sp,2 if cleanup=='near' else 4)))
        if not f or f['name']!=name or f['cleanup']!=cleanup or f['sp']!=sp or frame!=((f['ip'],) if cleanup=='near' else (f['ip'],0x2000)):raise ValueError('super native entry frame differs')
        self.frames.append(f);self.pending=None
    def leave(self,cleanup):
        if not self.frames:raise ValueError('super orphan native return')
        f=self.frames.pop();sp=self.get('SP');frame=tuple(struct.unpack('<'+'H'*(1 if cleanup=='near' else 2),self.uc.mem_read(self.stack+sp,2 if cleanup=='near' else 4)))
        if f['cleanup']!=cleanup or f['sp']!=sp or frame!=((f['ip'],) if cleanup=='near' else (f['ip'],0x2000)):raise ValueError('super native return frame differs')
    def run(self,name,args=(),budget=3000000):
        self.stop=False;self.errors.clear();self.frames.clear();self.pending=None;self.direct=name;cleanup=next(c for n,_,_,c in RANGES if n==name)
        for r,v in dict(CS=0x2000,DS=0x2e3f,SS=0x4000,ES=0x3333,AX=0x1111,BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,SP=0xffc0,EFLAGS=0x202|(0x400 if self.s.get('df') else 0)).items():self.set(r,v)
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2000,*args));self.prepare(name,0xffc0,0xff00,cleanup);self.uc.emu_start(self.code+ENTRIES[name],0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('super terminal/budget differs')
        saved=dict(BP=0x7777,SI=0x2468 if name=='bfnt' else 0x1357,DI=0x1357 if name=='bfnt' else 0x2468,DS=0x2e3f)
        if self.get('SP')!=0xffc4+cleanup or any(self.get(r)!=v for r,v in saved.items()):raise ValueError('super far cleanup/register observation differs')


class Scalar(smem.Scalar):
    """Segment-list context, nibble/plane conversion and ordered flat stores."""
    def __init__(self,p):
        super().__init__(p);self.code=p.code;self.ports=[];self.df=bool(p.s.get('df'));self.read_index=0;self.char_calls=0
    def cs(self,a,v,z=2):self.mem[self.code+a:self.code+a+z]=int(v).to_bytes(z,'little')
    def read(self,site,kind,handle,seg,offset,count):
        s=self.s;default=make_header(s) if kind=='header' else bytes(s.get('extension',[0x10,0,0,7])) if kind=='extension' else bytes(range(48)) if kind=='palette' else bytes((i*29+self.read_index*7+1)&255 for i in range(count))
        item=s.get(kind+'_read',{});payload=bytes(item.get('payload',list(default)))[:count];ax=item.get('ax',len(payload));cf=item.get('cf',0)
        if cf and not item.get('inject_on_failure'):payload=b''
        for i,v in enumerate(payload):self.mem[seg*16+u16(offset+i)]=v
        self.events.append(dict(site=site,name='dos_read',kind=kind,handle=handle,destination=[offset,seg],count=count,payload_hex=payload.hex(),ax=ax,cf=cf));self.read_index+=kind=='pixels';return ax,cf
    def close(self,handle):
        self.native['dos_close']+=1;ax=self.s.get('close_ax',7);cf=self.s.get('close_cf',0);self.events.append(dict(site=0xaa0,name='dos_close',handle=handle,ax=ax,cf=cf));return (65523 if cf else 0),cf
    def entry_at(self,num,size,segment):
        self.df=False
        if num>=512:return 65505,1
        if not self.get(BUFFER):
            self.put(ID,4);ax,cf=self.run('allocate',[576]);self.put(BUFFER,ax)
            if cf:return 65528,1
            self.mem[self.data+PATSIZE:self.data+PATSIZE+1024]=bytes(1024)
        pos=num*2
        if num<self.get(PATNUM):
            if self.get(PATSIZE+pos):self.run('free',[self.get(PATDATA+pos)])
        else:self.put(PATNUM,num+1)
        self.put(PATSIZE+pos,size);self.put(PATDATA+pos,segment);return 0,0
    def entry(self,args):
        clear,offset,src,patsize=args;plane=(patsize&255)*(patsize>>8);self.put(ID,4);segment,cf=self.run('byte',[u16(plane*5)])
        if cf:return 65528,1
        ax,cf=self.run('entry_at',[segment,patsize,self.get(PATNUM)])
        if cf:self.run('free',[segment]);return ax,1
        si=offset;di=plane
        for _ in range(u16(plane*2)):
            value=self.mem[src*16+si:src*16+si+2];self.mem[segment*16+di:segment*16+di+2]=value;si=u16(si+2);di=u16(di+2)
        si=plane
        for channel in range(4):
            invert=255 if clear&(1<<channel) else 0
            for i in range(plane):
                value=self.mem[segment*16+si]^invert;si=u16(si+1);at=segment*16+i
                self.mem[at]=value if channel==0 else self.mem[at]|value
        if clear&255:
            for channel in range(4):
                for i in range(plane):at=segment*16+u16(plane*(channel+1)+i);self.mem[at]&=self.mem[segment*16+i]
        return u16(self.get(PATNUM)-1),0
    def cancel(self,num):
        if num>=self.get(PATNUM):return 65505,1
        slot=u16(num*2);size=self.get(u16(PATSIZE+slot))
        if not size:return 65505,1
        self.run('free',[self.get(u16(PATDATA+slot))]);self.put(u16(PATDATA+slot),0);self.put(u16(PATSIZE+slot),0)
        if u16(num+1)==self.get(PATNUM):
            cur=slot
            for _ in range(65536):
                self.put(PATNUM,self.get(PATNUM)-1)
                if not self.get(PATNUM):break
                cur=u16(cur-2)
                if self.get(u16(PATDATA+cur)):break
            else:raise ValueError('scalar cancel search budget')
        return 0,0
    def read_header(self,handle,seg,off):
        ax,cf=self.read(0x3e5,'header',handle,seg,off,32)
        if cf and ax:return u16(-ax),1
        stride=-1 if self.df else 1
        for i in range(5):
            if self.mem[self.data+u16(0x51c+i*stride)]!=self.mem[seg*16+u16(off+i*stride)]:return 65523,1
        return 0,0
    def extend(self,handle,seg,off):
        self.df=False;size=self.word(seg*16+u16(off+28));length=self.word(seg*16+u16(off+30))
        if not size:return 0,0
        target,cf=self.run('get',[size])
        if cf:return target,cf
        _,cf=self.read(0x438,'extension',handle,target,0,size);value=65523
        if not cf:
            cursor=0;remaining=size
            for _ in range(1000):
                ident=self.mem[target*16+cursor];cursor=u16(cursor+1)
                if ident==16:value=self.mem[target*16+u16(cursor+2)]&15;break
                cursor=u16(cursor+length-3);next_length=self.word(target*16+cursor);cursor=u16(cursor+2)
                if not next_length:value=0;break
                borrow=remaining<length;remaining=u16(remaining-length);length=next_length
                if borrow or not remaining:value=0;break
            else:raise ValueError('scalar extension traversal budget')
        self.run('release',[target]);return value,cf
    def bfnt(self,args):
        clear,off,seg,handle=args;width=self.word(seg*16+u16(off+8));height=self.word(seg*16+u16(off+10));first=self.word(seg*16+u16(off+12));last=self.word(seg*16+u16(off+14));count=u16(last-first+1);columns=(width>>3)&255;rows=height&255;plane=u16((width>>3)*height);amount=u16(plane*4);patsize=(columns<<8)|rows
        for a,v,z in ((0x36d,clear,2),(0x35f,0x2e3f,2),(0x2ed,handle,2),(0x309,columns,1),(0x364,patsize,2),(0x307,rows,1),(0x302,plane,2),(0x2e8,amount,2)):self.cs(a,v,z)
        packed,cf=self.run('get',[amount])
        if cf:return packed,cf
        converted,cf=self.run('get',[amount])
        if cf:return converted,cf
        for _ in range(count or 65536):
            ax,cf=self.read(0x2f1,'pixels',handle,packed,0,amount)
            if cf or ax!=amount:self.run('release',[packed]);return 65523,cf or int(ax<amount)
            cursor=0;index=0;direction=-2 if self.df else 2
            for _ in range((columns or 256)*(rows or 256)):
                chunk=bytes(self.mem[packed*16+cursor:packed*16+cursor+2]);cursor=u16(cursor+direction);chunk+=bytes(self.mem[packed*16+cursor:packed*16+cursor+2]);cursor=u16(cursor+direction)
                pixels=[n for b in chunk for n in (b>>4,b&15)]
                for channel in range(4):
                    value=sum(((pixel>>channel)&1)<<(7-j) for j,pixel in enumerate(pixels));self.mem[converted*16+u16(index+channel*plane)]=value
                index=u16(index+1)
            ax,cf=self.run('entry',[clear,0,converted,patsize])
            if cf:self.run('release',[converted]);self.run('release',[packed]);return ax,1
        self.run('release',[converted]);self.run('release',[packed]);return 0,0
    def port(self,site,port,value):self.ports.append(dict(site=site,port=port,value=value))
    def geometry(self,num,y,x):
        size=self.get(u16(PATSIZE+u16(num*2)));width=size>>8;height=size&255;origin=u16(y*80+(x>>3));shift=x&7;odd=origin&1;variant=(3 if width&1 else 2) if odd else (1 if width&1 else 0);origin=u16(origin-odd);loops=width>>1
        if variant==2:loops=u16(loops-1)&255
        count_at=(0x26c9,0x26f7,0x272e,0x275f)[variant];add_at=(0x26c7,0x26f5,0x272c,0x275d)[variant];gap=((80 if variant<2 else 78 if variant==2 else 79)-width)&255;gap=gap if gap<128 else gap-256
        self.cs(0x2769,height|((255>>shift)<<8));self.cs(count_at,loops,1);self.cs(add_at,gap&255,1);self.cs(0x276c,u16(DRAW_TARGETS[variant]-0x276e))
        return size,origin,shift,variant,loops,gap,self.get(u16(PATDATA+u16(num*2)))
    def drawing(self,geometry,si=0):
        size,origin,shift,variant,loops,gap,segment=geometry;direction=-1 if self.df else 1;mask=255>>shift
        def load(z):
            nonlocal si
            value=int.from_bytes(self.mem[segment*16+si:segment*16+si+z],'little');si=u16(si+direction*z);return value
        def rotate(value):return ((value>>shift)|(value<<(16-shift)))&65535 if shift else value
        for _ in range((size&255) or 256):
            di=origin;carry=0
            if variant>=2:
                v=rotate(load(1));carry=v>>8;yield di,2,(v&255)<<8;di=u16(di+direction*2)
            pairs=loops or (256 if variant==0 else 0)
            for _ in range(pairs):
                v=rotate(load(2));low=v&255;kept=low&mask;yield di,2,(v&0xff00)|kept|carry;di=u16(di+direction*2);carry=low^kept
            if variant in (1,2):
                v=rotate(load(1));yield di,2,v|carry;di=u16(di+direction*2)
                if variant==1:di=u16(di-1)
            else:yield di,1,carry
            origin=u16(di+gap)
    def put_sprite(self,args):
        num,y,x=args;g=self.geometry(num,y,x);si=0;steps=(0x26ac,0x26d0,0x26fe,0x2734);variant=g[3]
        self.port(0x2666,0x7c,192)
        for a in (0x266a,0x266c,0x266e,0x2670):self.port(a,0x7e,0)
        for channel in range(5):
            if channel==1:
                self.port(0x267d,0x7c,206)
                for a in (0x2681,0x2683,0x2685,0x2687):self.port(a,0x7e,255)
            elif channel>1:self.port((0x268e,0x2695,0x269c)[channel-2],0x7c,(205,203,199)[channel-2])
            self.native['draw']+=1;self.native['draw'+str(variant+1)]+=1
            consumed=((g[4] or (256 if variant==0 else 0))*2+(2 if variant==2 else 1 if variant in (1,3) else 0))*((g[0]&255) or 256)
            for di,z,v in self.drawing(g,si):self.mem[0xa8000+di:0xa8000+di+z]=v.to_bytes(z,'little')
            si=u16(si+(-consumed if self.df else consumed))
        self.port(0x26a3,0x7c,0);return None,None
    def run(self,name,args=()):
        if name in {n for n,_,_,_ in heap.RANGES}|{'get','release'}:return super().run(name,args)
        self.native[name]+=1
        if name=='entry_at':return self.entry_at(args[2],args[1],args[0])
        if name=='entry':return self.entry(args)
        if name=='cancel':return self.cancel(args[0])
        if name=='free_all':
            if not self.get(BUFFER):return None,None
            self.run('free',[self.get(BUFFER)]);self.put(BUFFER,0)
            for _ in range(1000):
                if not self.get(PATNUM):break
                _,cf=self.run('cancel',[u16(self.get(PATNUM)-1)])
                if cf:raise ValueError('scalar free-all empty-tail budget')
            else:raise ValueError('scalar free-all count budget')
            if self.get(CHARFREE):self.char_calls+=1;self.events.append(dict(name='character_free',patnum=self.get(PATNUM),buffer=self.get(BUFFER)))
            return None,None
        if name=='header':return self.read_header(args[2],args[1],args[0])
        if name=='extend':return self.extend(args[2],args[1],args[0])
        if name=='skip':
            offset=self.word(args[1]*16+u16(args[0]+28));ax=self.s.get('seek_ax',0);cf=self.s.get('seek_cf',0);self.events.append(dict(site=0x3c9,name='dos_seek',handle=args[2],offset=offset,origin=1,ax=ax,cf=cf));return (65523 if cf else 0),cf
        if name=='bfnt':return self.bfnt(args)
        if name=='palette':
            if not self.mem[args[1]*16+u16(args[0]+5)]&128:return 65523,1
            _,cf=self.read(0x4df,'palette',args[2],0x2e3f,PALETTE,48)
            if cf:return 65523,1
            for i in range(16):at=self.data+PALETTE+i*3;b,r,g=self.mem[at:at+3];self.mem[at:at+3]=bytes([r,g,b])
            return 0,0
        if name=='dos_close':self.native[name]-=1;return self.close(args[0])
        if name=='dos_open':
            ax=self.s.get('open_ax',0x1234);cf=self.s.get('open_cf',0);self.events.append(dict(site=0xaba,name='dos_open',mode=self.get(0x558)&255,filename=[args[0],args[1]],ax=ax,cf=cf));return (65534 if cf else ax),cf
        if name=='put':return self.put_sprite(args)
        if name=='load':
            handle,cf=self.run('dos_open',args)
            if cf:return handle,cf
            ax,cf=self.run('header',[HEADER,0x2e3f,handle]);clear=0
            if not cf and self.mem[self.data+HEADER+5]&127!=3:ax=65523;cf=1
            if not cf:
                if self.get(HEADER+28):clear,_=self.run('extend',[HEADER,0x2e3f,handle])
                if self.mem[self.data+HEADER+5]&128:ax,cf=self.run('palette',[HEADER,0x2e3f,handle])
            if not cf:ax,cf=self.run('bfnt',[clear,HEADER,0x2e3f,handle])
            self.close(handle)
            if cf:return ax,1
            first=self.get(HEADER+12);last=self.get(HEADER+14);return u16(last-first+1),int(last<first)
        raise ValueError('scalar unknown super entry')


def matrix(mz):
    rows=[];meta=analyze(mz.program_image)
    def observe(label,s,steps):
        p=SuperProbe(mz,s,meta);spec=Scalar(p);before=sha(bytes(spec.mem));results=[]
        for name,args in steps:
            spec.df=bool(s.get('df'));ax,cf=spec.run(name,args);p.run(name,args)
            actual=bytes(p.uc.mem_read(0,0x100000))
            if (ax is not None and p.get('AX')!=ax) or (cf is not None and p.get('EFLAGS')&1!=cf) or bool(p.get('EFLAGS')&1024)!=spec.df or p.events!=spec.events or p.native!=spec.native or p.ports!=spec.ports or p.char_calls!=spec.char_calls:
                raise ValueError('super scalar result/DF/native/DOS/port differs: '+str((label,s,name,args,p.get('AX'),ax,p.get('EFLAGS')&1,cf,bool(p.get('EFLAGS')&1024),spec.df,dict(p.native),dict(spec.native),p.events,spec.events,p.ports,spec.ports)))
            if actual[:p.stack]!=spec.mem[:p.stack] or actual[p.stack+65536:]!=spec.mem[p.stack+65536:]:
                changes=[i for i,(a,b) in enumerate(zip(actual,spec.mem)) if a!=b and not p.stack<=i<p.stack+65536];raise ValueError('super full physical memory differs: '+str((label,s,name,args,changes[:30])))
            results.append(dict(function=name,args=args,ax=ax,cf=cf,df=spec.df,registers={r:p.get(r) for r in ('SI','DI','DS','ES')},patnum=spec.get(PATNUM),buffer=spec.get(BUFFER),end=spec.get(END),heap=spec.get(HEAP)))
        rows.append(dict(function=label,scenario=s,steps=results,top_level_calls=len(steps),events=p.events,ports=p.ports,native_entries=dict(p.native),write_count=p.write_count,memory_before_sha256=before,memory_after_sha256=sha(bytes(spec.mem))))
    for df in (False,True):
        base=dict(df=df)
        for clear in list(range(16))+[256,257,65535]:
            for size in (0x101,0x202,0x703):observe('entry',dict(base),[('entry',[clear,0x200,0x5000,size])])
        for num in (0,1,511,512,32768,65535):
            for size in (0,0x101,0xffff):observe('entry-at',dict(base),[('entry_at',[0x7000,size,num])])
        for size in (0,0x101):
            observe('entry-at-existing',dict(base,buffer=0x7000,patnum=2,patterns=[[0,0x101,0x7501],[1,size,0x7401]],heap=0x7400,blocks=[[0x7400,1,0x7500,4],[0x7500,1,0x8800,4]]),[('entry_at',[0x7100,0x202,1])])
        for gap in (0,1,2,4,577,578):
            for name,args in (('entry',[0,0,0x5000,0x202]),('entry_at',[0x7000,0x101,0]),('bfnt',[0,0,0x5100,7])):observe('memory-failure',dict(base,heap=0x6000+gap,out=0x6000+gap),[(name,args)])
        for num in (0,1,2,511,512,32768,65535):
            observe('cancel',dict(base,buffer=0x7700,patnum=3,patterns=[[0,0x101,0x7501],[1,0,0x7601],[2,0x201,0x7401]],heap=0x7400,blocks=[[0x7400,1,0x7500,4],[0x7500,1,0x8800,4]]),[('cancel',[num])])
        observe('cancel-word-alias',dict(base,patnum=32769,patterns=[[0,0x101,0x7501]],heap=0x7500,blocks=[[0x7500,1,0x8800,4]]),[('cancel',[32768])])
        observe('free-skip',dict(base,patnum=1,patterns=[[0,0x101,0x7501]],charfree=0x8000),[('free_all',[])])
        observe('connected-entry-put-cancel-free',dict(base,charfree=0x8000),[('entry',[3,0,0x5000,0x202]),('put',[0,7,13]),('entry',[14,0x20,0x5000,0x301]),('put',[1,5,4]),('cancel',[0]),('free_all',[]),('free_all',[])])
        for item in ({},{'cf':1,'ax':5},{'cf':1,'ax':0},{'cf':0,'ax':0,'payload':[]},{'cf':0,'ax':2,'payload':[66,70]},{'cf':0,'ax':33},{'payload':[0]*32}):observe('header',dict(base,header_read=item),[('header',[0,0x5100,7])])
        for cf in (0,1):
            for value in (0,1,65535):
                observe('skip',dict(base,extension_size=value,seek_cf=cf,seek_ax=7),[('skip',[0,0x5100,7])])
                observe('close',dict(base,close_cf=cf,close_ax=value),[('dos_close',[7])])
        for value in range(32):observe('extend-color',dict(base,extension_size=4,extension=[16,0,0,value]),[('extend',[0,0x5100,7])])
        for payload in ([0,0,0,0],[0,0,0,4,0,16,0,0,5],[0,0,0,255,255],[16],[16,0,0,31]):
            observe('extend-record',dict(base,extension_size=len(payload),extension=payload),[('extend',[0,0x5100,7])])
        for item in ({'cf':1,'ax':5},{'cf':0,'ax':0,'payload':[]},{'cf':0,'ax':65535}):observe('extend-read',dict(base,extension_size=4,extension_read=item),[('extend',[0,0x5100,7])])
        observe('extend-no-memory',dict(base,extension_size=4,heap=0x6000),[('extend',[0,0x5100,7])])
        for width,height in ((8,1),(16,2),(24,3),(7,1),(2048,1),(8,256),(2056,257)):
            if width in (7,2048) or height==256:continue # zero low-byte loops are budget scopes below
            for clear in (0,3,15,256):observe('bfnt',dict(base,width=width,height=height),[('bfnt',[clear,0,0x5100,7])])
        for item in ({'cf':1,'ax':5},{'cf':1,'ax':0},{'cf':0,'ax':0},{'cf':0,'ax':15},{'cf':0,'ax':16},{'cf':0,'ax':17},{'cf':0,'ax':65535}):observe('bfnt-read-status',dict(base,pixels_read=item),[('bfnt',[0,0,0x5100,7])])
        for first,last,patnum in ((0,1,0),(10,11,511),(1,0,511),(0,0,512)):
            observe('bfnt-count',dict(base,first=first,last=last,patnum=patnum,buffer=0x7000 if patnum else 0),[('bfnt',[3,0,0x5100,7])])
        for color in (0,3,0x83,255):observe('load-color',dict(base,color=color),[('load',[0x100,0x5000])])
        for cf in (0,1):
            for itemkey in ('open_cf','close_cf','header_read','extension_read','palette_read','pixels_read'):
                s=dict(base,color=0x83,extension_size=4)
                s[itemkey]={'cf':cf,'ax':5} if itemkey.endswith('_read') else cf
                observe('load-status',s,[('load',[0x100,0x5000])])
        if not df:observe('connected-load-draw-free',dict(base,color=0x83,extension_size=4,last=1,charfree=0x8000),[('load',[0x100,0x5000]),('put',[0,0,7]),('put',[1,1,8]),('free_all',[])])
        for width in (1,2,3,4,7,8,9,79,80,81,127,128,129,254,255):
            for x in range(16):observe('draw-variants',dict(base,patterns=[[0,(width<<8)|2,0x5000]]),[('put',[0,5,x])])
        for y,x in ((0,0),(399,639),(65535,65535),(819,15),(820,7),(32768,32768)):
            for width in (1,2,3,4):observe('draw-coordinate',dict(base,patterns=[[0,(width<<8)|2,0x5000]]),[('put',[0,y,x])])
        observe('draw-zero-width',dict(base,patterns=[[0,1,0x5000]]),[('put',[0,0,0])])
        observe('draw-zero-height',dict(base,patterns=[[0,0x100,0x5000]]),[('put',[0,0,8])])
    return rows


def nonterminal(mz):
    rows=[];meta=analyze(mz.program_image)
    for df in (False,True):
        for name,s,args in [('free_all',dict(df=df,buffer=0x7501,patnum=1,patterns=[[0,0,0x7601]],heap=0x7500,blocks=[[0x7500,1,0x8800,4]]),[]),('put',dict(df=df,patterns=[[0,0,0x5000]]),[0,0,0]),('bfnt',dict(df=df,width=0,height=0),[0,0,0x5100,7]),('bfnt',dict(df=df,width=7,height=1),[0,0,0x5100,7]),('bfnt',dict(df=df,width=8,height=0),[0,0,0x5100,7])]:
            p=SuperProbe(mz,s,meta);spec=Scalar(p);before=sha(bytes(spec.mem));budget=3000
            try:p.run(name,args,budget)
            except ValueError as e:
                if str(e)!='super terminal/budget differs':raise
            else:raise ValueError('super budget unexpectedly returned')
            spec.native[name]+=1
            if name=='free_all':
                spec.run('free',[spec.get(BUFFER)]);spec.put(BUFFER,0);spec.native['cancel']=p.native['cancel']
            elif name=='put':
                g=spec.geometry(*args);spec.port(0x2666,0x7c,192)
                for site in (0x266a,0x266c,0x266e,0x2670):spec.port(site,0x7e,0)
                spec.native['draw']=spec.native['draw1']=1
                stream=spec.drawing(g)
                for _ in range(p.vram_writes):di,z,v=next(stream);spec.mem[0xa8000+di:0xa8000+di+z]=v.to_bytes(z,'little')
            else:
                clear,off,seg,handle=args;width=spec.word(seg*16+off+8);height=spec.word(seg*16+off+10);columns=(width>>3)&255;rowsize=height&255;plane=u16((width>>3)*height);amount=u16(plane*4)
                for a,v,z in ((0x36d,clear,2),(0x35f,0x2e3f,2),(0x2ed,handle,2),(0x309,columns,1),(0x364,(columns<<8)|rowsize,2),(0x307,rowsize,1),(0x302,plane,2),(0x2e8,amount,2)):spec.cs(a,v,z)
                packed,_=spec.run('get',[amount]);converted,_=spec.run('get',[amount]);spec.read(0x2f1,'pixels',handle,packed,0,amount)
                cursor=0;index=0;remaining=p.conversion_writes;direction=-2 if df else 2
                while remaining:
                    chunk=bytes(spec.mem[packed*16+cursor:packed*16+cursor+2]);cursor=u16(cursor+direction);chunk+=bytes(spec.mem[packed*16+cursor:packed*16+cursor+2]);cursor=u16(cursor+direction);pixels=[n for b in chunk for n in (b>>4,b&15)]
                    for channel in range(4):
                        if not remaining:break
                        value=sum(((pixel>>channel)&1)<<(7-j) for j,pixel in enumerate(pixels));spec.mem[converted*16+u16(index+channel*plane)]=value;remaining-=1
                    index=u16(index+1)
            actual=bytes(p.uc.mem_read(0,0x100000))
            if actual[:p.stack]!=spec.mem[:p.stack] or actual[p.stack+65536:]!=spec.mem[p.stack+65536:] or p.events!=spec.events or p.ports!=spec.ports or p.native!=spec.native:raise ValueError('super bounded prefix full memory/trace differs: '+str((name,s,dict(p.native),dict(spec.native))))
            rows.append(dict(function=name,scenario=s,args=args,budget=budget,outcome='native-execution-budget',instruction=p.get('IP'),native_entries=dict(p.native),events=p.events,ports=p.ports,vram_writes=p.vram_writes,conversion_writes=p.conversion_writes,memory_before_sha256=before,memory_after_sha256=sha(bytes(spec.mem))))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('super prior VSYNC proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_super.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('super input changed: '+p)
    def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('memory_before_sha256','memory_after_sha256')} for row in cpu]
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];objects=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('super invalid image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz),nonterminal=nonterminal(mz))
        if observations:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('super complete body/CFG differs')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached);actual=cached.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else cached
                if actual!=cached_provider(p,d):raise ValueError('super cached frozen provider differs: '+p)
            op=str(tree/'obj/th03/mainl.obj');obj_data=(ROOT/op).read_bytes();inputs[op]=sha(obj_data);obj=describe_omf(obj_data)
            if not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0']:raise ValueError('super cached root OMF identity differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments','record_count','record_counts')}
            if objects and obj['dependency_timestamp_normalized_sha256']!=objects[0]['dependency_timestamp_normalized_sha256']:raise ValueError('super cached OMF differs beyond dependency timestamps')
            objects.append(observed['object']);maprows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));carrier=next(row for row in maprows if row['module']=='th03_mainl.asm' and row['segment']==0 and row['size'])
            if not all(carrier['start']<=a<a+n<=carrier['start']+carrier['size'] for _,a,n,_ in RANGES):raise ValueError('super includes outside complete root carrier')
            observed['carrier']=carrier;target=parse_mz((ROOT/observations[0]['path']).read_bytes());extents=[('bfnt',0x272,512),('super',0x237e,1008),('dos-close',0xa98,22)]+[(f'prior-{n}',a,z) for n,a,z,_ in CONTEXT]
            extents += [(f'prior-heap-even-{a:x}',a,1) for a in heap.ALIGNMENT]+[(f'prior-stack-even-{a:x}',a,1) for a in smem.ALIGNMENT]
            observed['comparisons']={n:extent_observation(target,mz,dict(start=a,size=z,segment=0,offset=a)) for n,a,z in extents}
            if any(not x['raw_slice_equal'] or not x['ordered_relocations_equal'] for x in observed['comparisons'].values()):raise ValueError('super complete raw/ordered relocations differ')
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']) or normalized(observed['nonterminal'])!=normalized(observations[0]['nonterminal']):raise ValueError('super target/cached CPU differs')
        observations.append(observed);print('Reviewed',path,len(observed['cpu']),'scenarios',len(observed['nonterminal']),'budgets',flush=True)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('super canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('super frozen provider changed')
    result=dict(kind='th03-mainl-complete-bfnt-super-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},build_scaffold_main_remaps=BUILD_REMAPS,observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL BFNT/super/DOS-close1542bytes with native heap/stack/palette/open794context and declared DOS/flat VRAM:',args.output)


if __name__=='__main__':main()
