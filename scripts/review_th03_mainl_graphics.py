#!/usr/bin/env python3
"""Complete MAINL EGC/GRCG boxes and public near GDC helper candidates."""
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
from review_th03_mainl_snow import u16,signed
from review_th03_mainl_heap import cached_provider,BUILD_REMAPS

ROOT=Path(__file__).resolve().parents[1]
PRIOR='.analysis/sol-mainl-super-review-20261006.json'
PRIOR_SHA='d78e3b9410ed314ded32ab5a9b45f6a4b6609fe5785b70b59460e8b39a7c620b'
COLD='.analysis/th03-main-exact/sol-main-restored-aggregate-20261006/receipt.json'
COLD_SHA='8184d36dbc70c478ec4d8bb3461fa065c4352dff88305695bc7a4e7e284600ae'
OWN=[('egc_on',0x724,21,0),('egc_off',0x73a,31,0),('egc_start',0x75a,43,0),('box',0xac8,213,8),('bytebox',0xb9e,151,8),('gdc',0xc66,11,'near')]
CONTEXT=[('color',0xc36,41,4),('off',0xc60,5,0)]
RANGES=OWN+CONTEXT
ENTRY={n:a for n,a,_,_ in RANGES};ENTRY['box']=0xace
ALIGNMENT={0x739:0x90,0x759:0x90,0x785:0x90,0xb9d:0x90,0xc35:0x90}
CONTEXT_ALIGN={0xc5f:0x90,0xc65:0x90}
INTERIOR_ALIGN={a:0x90 for a in (0xb89,0xb91,0xbf9,0xc13,0xc19)}
CALLS={0x75b:0x724,0x781:0x73a}
PORTS={0x726:(0x7c,1),0x72a:(0x6a,1),0x72e:(0x6a,1),0x732:(0x7c,1),0x736:(0x6a,1),0x740:(0x4a0,2),0x747:(0x4a8,2),0x74a:(0x6a,1),0x74e:(0x6a,1),0x752:(0x7c,1),0x756:(0x6a,1),0x764:(0x4a0,2),0x76b:(0x4a2,2),0x772:(0x4a8,2),0x778:(0x4ac,2),0x77f:(0x4ae,2),0xc45:(0x7c,1),**{a:(0x7e,1) for a in (0xc4b,0xc50,0xc55,0xc5a)},0xc62:(0x7c,1),0xc66:(0xa0,1),0xc6e:(0xa0,1)}
CLIP_XL,CLIP_XW,CLIP_YT,CLIP_YH,CLIP_SEG,EDGES=0x522,0x524,0x528,0x52a,0x52e,0x532
SURFACE=0xa8000;SURFACE_END=0xc0001
STATUS=0x8d5
PROVIDERS=['th03_mainl.asm','Tupfile.lua','libs/master.lib/master.inc','libs/master.lib/macros.inc']+['libs/master.lib/'+n+'.asm' for n in ('egc','grcg_boxfill','grcg_byteboxfill_x','grcg_setcolor','gdc_outpw','clip[data]','clip[bss]')]
PUBLICS={'EGC_ON':0x724,'EGC_OFF':0x73a,'EGC_START':0x75a,'EGC_END':0x75a,'GRCG_BOXFILL':0xace,'GRCG_BYTEBOXFILL_X':0xb9e,'GRCG_SETCOLOR':0xc36,'GRCG_OFF':0xc60,'gdc_outpw':0xc66}


def edge(bits):
    value=(65535<<(16-bits))&65535
    return ((value&255)<<8)|(value>>8)


def analyze(image):
    dec=Cs(CS_ARCH_X86,CS_MODE_16);dec.detail=True;parts=[];bounds=set();returns={};rows=[]
    for n,a,z,c in RANGES:
        body=image[a:a+z]
        if len(body)!=z:raise ValueError('graphics complete body differs')
        ins=list(dec.disasm(body,a));expected=('ret','') if c=='near' else ('retf',str(c) if c else '')
        if not ins or sum(i.size for i in ins)!=z or (ins[-1].mnemonic,ins[-1].op_str)!=expected:raise ValueError('graphics complete instruction/terminal cleanup differs')
        parts.append((n,a,z,c,expected,ins));bounds.update(i.address for i in ins)
    for n,a,z,c,expected,ins in parts:
        edges=[]
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf'):
                if (i.mnemonic,i.op_str)!=expected:raise ValueError('graphics interior cleanup differs')
                returns[i.address]=c
            if i.mnemonic=='int' or i.mnemonic=='in':raise ValueError('graphics unexpected interrupt/input')
            if i.mnemonic=='out':
                if i.address not in PORTS:raise ValueError('graphics unknown port site')
                actual=i.op_str
                wanted='dx, ax' if PORTS[i.address][1]==2 else 'dx, al' if i.address in (0xc4b,0xc50,0xc55,0xc5a) else hex(PORTS[i.address][0])+', al'
                if actual!=wanted:raise ValueError('graphics port encoding/width differs')
            if not(i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('graphics indirect edge')
            if i.mnemonic in ('lcall','ljmp'):raise ValueError('graphics unknown far edge')
            dest=i.operands[0].imm
            if i.mnemonic=='call':
                if CALLS.get(i.address)!=dest:raise ValueError('graphics unknown native call')
                if not j or ins[j-1].bytes!=b'\x0e':raise ValueError('graphics call lacks PUSH CS')
            elif dest not in bounds:raise ValueError('graphics branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=n,offset=a,size=z,instructions=len(ins),cleanup=c,sha256=sha(image[a:a+z]),edges=edges))
    if any(image[a:a+1]!=bytes([v]) for a,v in {**ALIGNMENT,**CONTEXT_ALIGN,**INTERIOR_ALIGN}.items()):raise ValueError('graphics producer alignment differs')
    table=struct.pack('<17H',*(edge(i) for i in range(17)))
    if image[0xe3f0+EDGES:0xe3f0+EDGES+34]!=table:raise ValueError('graphics edge table differs')
    return dict(bodies=rows,bounds=sorted(bounds),returns=returns,new_extent_bytes=475,new_body_bytes=470,new_alignment_bytes=5,interior_alignment_in_body_bytes=5,prior_color_body_bytes=46,uncredited_context_alignment_bytes=2,edge_table_sha256=sha(table),aliases={'egc_end':'egc_start'},alignment=ALIGNMENT,context_alignment=CONTEXT_ALIGN,interior_alignment=INTERIOR_ALIGN)


def initial_flags(s):return (s.get('flags',0x202)|2|(0x400 if s.get('df') else 0))&65535


def subflags(a,b):
    result=u16(a-b)
    return int(a<b)|(4 if (result&255).bit_count()%2==0 else 0)|(16 if (a^b^result)&16 else 0)|(64 if not result else 0)|(128 if result&32768 else 0)|(2048 if (a^b)&(a^result)&32768 else 0)


class GraphicsProbe(Probe):
    def __init__(self,mz,s,meta=None):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000);image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x20000,0x2e3f0,0x40000
        self.uc.mem_write(SURFACE,b'\xa5'*(SURFACE_END-SURFACE))
        self.s=s;self.meta=meta or analyze(mz.program_image);self.bounds=set(self.meta['bounds']);self.returns=self.meta['returns'];self.frames=[];self.pending=None;self.errors=[];self.stop=False;self.native=Counter();self.ports=[];self.writes=[];self.visits=Counter()
        for a,key,default in ((CLIP_XL,'clip_x',0),(CLIP_XW,'clip_w',639),(CLIP_YT,'clip_y',0),(CLIP_YH,'clip_h',399),(CLIP_SEG,'clip_seg',0xa800)):
            self.uc.mem_write(self.data+a,struct.pack('<H',s.get(key,default)))
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2000:raise ValueError('graphics terminal segment alias')
                if self.frames or self.pending:raise ValueError('graphics unfinished native frame')
                self.stop=True;uc.emu_stop();return
            off=address-self.code
            if self.get('CS')!=0x2000 or self.get('SS')!=0x4000:raise ValueError('graphics CODE/stack segment alias')
            if off not in self.bounds:raise ValueError('CPU escaped graphics instruction boundaries')
            self.visits[off]+=1
            if off in ENTRY.values():
                name=next(n for n,a in ENTRY.items() if a==off);cleanup=next(c for n,_,_,c in RANGES if n==name);self.enter(name,cleanup);self.native[name]+=1
            if off in CALLS:
                dest=CALLS[off];name=next(n for n,a in ENTRY.items() if a==dest);self.prepare(name,self.get('SP')-2,off+3,0)
            if off in self.returns:self.leave(self.returns[off])
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            if not SURFACE<=address or address+size>SURFACE_END or size not in (1,2):raise ValueError('graphics store outside declared surface/width')
            self.writes.append([address,size,value])
        def out(uc,port,width,value,user):
            if self.get('CS')!=0x2000 or PORTS.get(self.get('IP'))!=(port,width):raise ValueError('graphics unknown port/site/width')
            self.ports.append(dict(site=self.get('IP'),port=port,width=width,value=value,live_if=bool(self.get('EFLAGS')&512),live_df=bool(self.get('EFLAGS')&1024)))
        def inp(*args):raise ValueError('graphics unexpected input')
        def intr(*args):raise ValueError('graphics unexpected interrupt')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr));self.uc.hook_add(UC_HOOK_INSN,guard(out),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)
    def word(self,offset):return struct.unpack('<H',self.uc.mem_read(self.data+offset,2))[0]
    def prepare(self,name,sp,ip,cleanup):
        if self.pending:raise ValueError('graphics overlapping native frame')
        self.pending=dict(name=name,sp=u16(sp),ip=ip,cleanup=cleanup)
    def enter(self,name,cleanup):
        frame=self.pending;sp=self.get('SP');near=cleanup=='near';words=tuple(struct.unpack('<H' if near else '<2H',self.uc.mem_read(self.stack+sp,2 if near else 4)))
        if not frame or frame['name']!=name or frame['cleanup']!=cleanup or frame['sp']!=sp or words!=((frame['ip'],) if near else (frame['ip'],0x2000)):raise ValueError('graphics native entry frame differs')
        self.frames.append(frame);self.pending=None
    def leave(self,cleanup):
        if not self.frames:raise ValueError('graphics orphan native return')
        frame=self.frames.pop();sp=self.get('SP');near=cleanup=='near';words=tuple(struct.unpack('<H' if near else '<2H',self.uc.mem_read(self.stack+sp,2 if near else 4)))
        if frame['cleanup']!=cleanup or frame['sp']!=sp or words!=((frame['ip'],) if near else (frame['ip'],0x2000)):raise ValueError('graphics native return frame differs')
    def run(self,name,args=(),budget=2000000):
        name='egc_start' if name=='egc_end' else name;self.stop=False;self.errors.clear();self.frames.clear();self.pending=None;cleanup=next(c for n,_,_,c in RANGES if n==name)
        values=dict(CS=0x2000,DS=0x2e3f,SS=0x4000,ES=0x3333,AX=self.s.get('ax',0x1111),BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,SP=0xffc0,EFLAGS=initial_flags(self.s))
        for r,v in values.items():self.set(r,v)
        words=[0xff00]+([] if cleanup=='near' else [0x2000])+list(args);self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*len(words),*words));self.prepare(name,0xffc0,0xff00,cleanup);self.uc.emu_start(self.code+ENTRY[name],0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('graphics terminal/budget differs')
        if self.get('SP')!=0xffc0+(2 if cleanup=='near' else 4+cleanup):raise ValueError('graphics root cleanup differs')
        preserved=['BP','SI','DI','DS']
        if name not in ('box','bytebox'):preserved+=['ES','CX']
        if name in ('egc_on','egc_off','egc_start','gdc','off'):preserved+=['BX']
        if name in ('egc_on','gdc','off'):preserved+=['DX']
        if any(self.get(r)!=values[r] for r in preserved):raise ValueError('graphics register observation differs')


class Scalar:
    """Inclusive masks, clipped coordinates, modular strides and ordered ports."""
    def __init__(self,p):
        self.mem=bytearray(p.uc.mem_read(0,0x100000));self.data=p.data;self.s=p.s;self.native=Counter();self.ports=[];self.writes=[];self.flags=initial_flags(p.s)
    def word(self,a):return struct.unpack_from('<H',self.mem,self.data+a)[0]
    def port(self,site,port,width,value,flags=None):
        flags=self.flags if flags is None else flags;self.ports.append(dict(site=site,port=port,width=width,value=value,live_if=bool(flags&512),live_df=bool(flags&1024)))
    def on(self):
        for a,p,v in ((0x726,0x7c,0),(0x72a,0x6a,7),(0x72e,0x6a,5),(0x732,0x7c,128),(0x736,0x6a,6)):self.port(a,p,1,v)
    def off_egc(self):
        for a,p,z,v in ((0x740,0x4a0,2,65520),(0x747,0x4a8,2,65535),(0x74a,0x6a,1,7),(0x74e,0x6a,1,4),(0x752,0x7c,1,0),(0x756,0x6a,1,6)):self.port(a,p,z,v)
    def geometry(self,name,args):
        y2,x2,y1,x1=args;xl=self.word(CLIP_XL);xw=self.word(CLIP_XW);yt=self.word(CLIP_YT);yh=self.word(CLIP_YH);base=self.word(CLIP_SEG)
        if name=='box':
            self.flags|=512
            if signed(x1)>signed(x2):x1,x2=x2,x1
            if signed(x2)<signed(xl):return None,subflags(x2,xl),None
            left=u16(x1-xl);left=left if left<32768 else 0;right=min(u16(x2-xl),xw)
            if signed(right)<signed(left):return None,subflags(right,left),None
            absolute=u16(left+xl);span=u16(right-left)
            if signed(y1)>signed(y2):y1,y2=y2,y1
            bottom=u16(y2-yt)
            if bottom&32768:return None,subflags(y2,yt),None
            top=u16(y1-yt);top=top if top<32768 else 0;bottom=min(bottom,yh)
            if signed(bottom)<signed(top):return None,subflags(bottom,top),None
            height=u16(bottom-top);segment=u16(base+top*5);di=u16(height*80+(absolute>>4)*2);leftbits=absolute&15;tail=u16(span+leftbits-16);middle=signed(tail)>>4;first=u16(~edge(leftbits));last=edge((tail&15)+1)
            return dict(segment=segment,di=di,middle=middle,first=first,last=last,gap=u16((42+middle)*2) if middle>=0 else 82),None,segment
        top=u16(y1-yt) if signed(y1)>signed(yt) else 0;segment=u16(base+top*5);bottom=u16(y2-yt)
        if signed(bottom)>=signed(yh):bottom=yh
        if signed(bottom)<signed(top):return None,subflags(bottom,top),segment
        height=u16(bottom-top)
        if signed(x2)<signed(x1):return None,subflags(x2,x1),segment
        width=u16(x2-x1+1);di=u16(height*80+x1);odd=di&1
        return dict(segment=segment,di=di,width=width,odd=odd,gap=u16(width+80)),None,segment
    def stream(self,name,g):
        di=g['di'];direction=-1 if self.flags&1024 else 1;segment=g['segment']
        for _ in range(65536):
            if name=='box':
                row=[(2,g['first'])]+[(2,65535)]*g['middle']+[(2,g['last'])] if g['middle']>=0 else [(2,g['first']&g['last'])]
            else:
                width=g['width'];pairs=width>>1;row=[]
                if g['odd']:row.append((1,255));pairs=u16(pairs-int(not(width&1)))
                row.extend([(2,65535)]*pairs)
                if (g['odd'] and not width&1) or (not g['odd'] and width&1):row.append((1,255))
            for size,value in row:
                yield segment*16+di,size,value;di=u16(di+direction*size)
            before=di;di=u16(di-g['gap']);self.flags=(self.flags&~STATUS)|subflags(before,g['gap'])
            if before<g['gap']:return
        raise ValueError('scalar graphics row budget')
    def run(self,name,args=()):
        name='egc_start' if name=='egc_end' else name;self.flags=initial_flags(self.s);self.native[name]+=1;ax=None;es=None;mask=STATUS|512|1024
        if name=='egc_on':self.on();ax=(self.s.get('ax',0x1111)&0xff00)|6
        elif name=='egc_off':self.off_egc();ax=0xff06
        elif name=='egc_start':
            self.native['egc_on']+=1;self.on()
            for a,p,v in ((0x764,0x4a0,65520),(0x76b,0x4a2,255),(0x772,0x4a8,65535)):self.port(a,p,2,v)
            self.flags=(self.flags&~STATUS)|68;mask&=~16
            self.port(0x778,0x4ac,2,0);self.port(0x77f,0x4ae,2,15);self.native['egc_off']+=1;self.off_egc();ax=0xff06
        elif name=='gdc':
            value=self.s.get('ax',0x1111);self.port(0xc66,0xa0,1,value&255);self.port(0xc6e,0xa0,1,value>>8);ax=(value&0xff00)|(value>>8)
        elif name=='color':
            color,mode=args;flags=self.flags&~512;self.port(0xc45,0x7c,1,mode&255,flags)
            for channel,a in enumerate((0xc4b,0xc50,0xc55,0xc5a)):self.port(a,0x7e,1,255 if color&(1<<channel) else 0,flags)
            ax=((color&255)>>4)<<8|(255 if color&8 else 0)
        elif name=='off':self.flags=(self.flags&~STATUS)|68;mask&=~16;self.port(0xc62,0x7c,1,0);ax=self.s.get('ax',0x1111)&0xff00
        else:
            g,status,es=self.geometry(name,args)
            if g:
                for address,size,value in self.stream(name,g):self.mem[address:address+size]=value.to_bytes(size,'little');self.writes.append([address,size,value])
            else:self.flags=(self.flags&~STATUS)|status
        return dict(ax=ax,es=es,flags=self.flags,flag_mask=mask)


def compare(p,spec,result,label):
    actual=bytes(p.uc.mem_read(0,0x100000))
    if (result['ax'] is not None and p.get('AX')!=result['ax']) or (result['es'] is not None and p.get('ES')!=result['es']) or (p.get('EFLAGS')^result['flags'])&result['flag_mask'] or p.native!=spec.native or p.ports!=spec.ports or p.writes!=spec.writes:
        raise ValueError('graphics scalar AX/ES/flags/native/ports/stores differs: '+str((label,p.get('AX'),result['ax'],p.get('ES'),result['es'],hex(p.get('EFLAGS')),hex(result['flags']),dict(p.native),dict(spec.native),p.ports,spec.ports,p.writes[:12],spec.writes[:12])))
    if actual[:p.stack]!=spec.mem[:p.stack] or actual[p.stack+65536:]!=spec.mem[p.stack+65536:]:
        changes=[i for i,(a,b) in enumerate(zip(actual,spec.mem)) if a!=b and not p.stack<=i<p.stack+65536]
        raise ValueError('graphics whole physical memory differs: '+str((label,changes[:30])))


def matrix(mz):
    rows=[];meta=analyze(mz.program_image)
    def observe(label,s,steps):
        p=GraphicsProbe(mz,s,meta);spec=Scalar(p);before=sha(bytes(spec.mem));results=[]
        for name,args in steps:
            result=spec.run(name,args);p.run(name,args);compare(p,spec,result,(label,s,name,args))
            results.append(dict(function=name,args=args,scalar=result,registers={r:p.get(r) for r in ('AX','BX','CX','DX','BP','SI','DI','DS','ES','SP')},flags=p.get('EFLAGS')&(STATUS|512|1024)))
        rows.append(dict(function=label,scenario=s,steps=results,top_level_calls=len(steps),native_entries=dict(p.native),ports=p.ports,stores=len(p.writes),store_sha256=sha(json.dumps(p.writes,separators=(',',':')).encode()),visited=sorted(p.visits),memory_before_sha256=before,memory_after_sha256=sha(bytes(spec.mem))))
    for df in (False,True):
        for irq in (0,512):
            base=dict(df=df,flags=2|irq)
            for bits in range(64):
                flags=2|irq|sum(bit for i,bit in enumerate((1,4,16,64,128,2048)) if bits>>i&1)
                for name,args in (('egc_on',[]),('egc_off',[]),('egc_start',[]),('egc_end',[]),('off',[]),('color',[bits,0xc0]),('gdc',[])):
                    observe('status-flags',dict(base,flags=flags),[(name,args)])
            for color in list(range(16))+[0x100,0x10f,0xfff0,0xffff]:
                for mode in (0,0x80,0xc0,0x1c0,0xffff):observe('color-bits-mode',dict(base),[('color',[color,mode])])
            for ax in (0,1,255,256,0xff00,0xffff,0x1234,0x80fe):observe('near-gdc-byte-order',dict(base,ax=ax),[('gdc',[])])
            for left in range(16):
                for width in (1,2,7,8,15,16,17,31,32,33,639):observe('pixel-masks',dict(base),[('box',[2,u16(left+width-1),0,left])])
            for coords in ((0,0,0,0),(399,639,399,639),(401,641,400,640),(2,9,7,40),(0,0,65535,65535),(65535,65535,65534,65534),(1,1,32768,32768),(32767,32767,32768,32768),(32768,32768,32767,32767),(0,32768,0,32768)):
                observe('pixel-coordinate-order',dict(base),[('box',list(coords))])
            for x1,x2 in ((0,639),(36,36),(36,37),(37,37),(217,217),(218,219),(40,80),(80,40),(32768,32767)):
                observe('pixel-nonzero-clip',dict(base,clip_x=37,clip_w=180,clip_y=19,clip_h=73,clip_seg=0xa85f),[('box',[93,x2,18,x1])])
            for s,args in ((dict(clip_w=0,clip_h=0),[0,0,0,0]),(dict(clip_w=0),[1,639,0,0]),(dict(clip_h=0),[399,30,0,0]),(dict(clip_x=0xffff),[0,0,0,0]),(dict(clip_y=0x8000,clip_h=0),[0x8000,1,0x7fff,0])):
                observe('pixel-clip-word-boundary',dict(base,**s),[('box',args)])
            for x1 in (0,1,2,3):
                for width in (1,2,3,4,79,80,81,255):observe('byte-four-parities',dict(base),[('bytebox',[2,x1+width-1,0,x1])])
            for args in ([0,0,0,0],[399,79,399,79],[401,81,400,80],[0,0,65535,65535],[1,0xffff,0,0xfffe],[0,0x7fff,0,0x8000],[0,1,1,0],[0,0,0,1],[0x8000,2,0x7fff,1]):
                observe('byte-unchecked-coordinate',dict(base),[('bytebox',args)])
            for y1,y2 in ((18,18),(18,19),(19,19),(20,20),(90,100),(93,94),(100,90)):
                observe('byte-nonzero-clip',dict(base,clip_x=37,clip_w=0,clip_y=19,clip_h=73,clip_seg=0xa85f),[('bytebox',[y2,81,y1,79])])
            observe('connected-device-drawing',dict(base),[('egc_start',[]),('color',[13,0xc0]),('box',[3,47,1,7]),('bytebox',[4,7,2,1]),('off',[]),('egc_off',[])])
    return rows


def nonterminal(mz):
    rows=[];meta=analyze(mz.program_image)
    for df in (False,True):
        for irq in (0,512):
            s=dict(df=df,flags=2|irq);args=[0,0x7fff,0,0x8001];p=GraphicsProbe(mz,s,meta);spec=Scalar(p);budget=1000;before=sha(bytes(spec.mem))
            try:p.run('bytebox',args,budget)
            except ValueError as e:
                if str(e)!='graphics terminal/budget differs':raise
            else:raise ValueError('graphics large-width budget unexpectedly returned')
            spec.native['bytebox']+=1;g,_,_=spec.geometry('bytebox',args);stream=spec.stream('bytebox',g)
            for _ in range(len(p.writes)):
                address,size,value=next(stream);spec.mem[address:address+size]=value.to_bytes(size,'little');spec.writes.append([address,size,value])
            compare(p,spec,dict(ax=None,es=g['segment'],flags=initial_flags(s),flag_mask=512|1024),'large width native prefix')
            if not p.frames or p.stop:raise ValueError('graphics budget falsely completed native frame')
            rows.append(dict(function='bytebox',scenario=s,args=args,budget=budget,outcome='native-execution-budget',instruction=p.get('IP'),native_entries=dict(p.native),stores=len(p.writes),store_sha256=sha(json.dumps(p.writes,separators=(',',':')).encode()),memory_before_sha256=before,memory_after_sha256=sha(bytes(spec.mem))))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    prior_raw=(ROOT/PRIOR).read_bytes();cold_raw=(ROOT/COLD).read_bytes()
    if sha(prior_raw)!=PRIOR_SHA or sha(cold_raw)!=COLD_SHA:raise ValueError('graphics pinned prior/cold receipt differs')
    prior=json.loads(prior_raw);cold=json.loads(cold_raw)
    if not cold['pass'] or cold['reference_revision']!=REVISION or not cold['all_products_equal'] or len(cold['rounds'])!=2 or not all(r['fresh_owned_objects'] and all(c['exit_code']==0 for c in r['commands']) for r in cold['rounds']):raise ValueError('graphics fresh cold lineage differs')
    inputs={**prior['inputs'],PRIOR:sha(prior_raw),COLD:sha(cold_raw),'scripts/review_th03_mainl_graphics.py':sha(Path(__file__).read_bytes()),'tests/test_mainl_graphics_review.py':sha((ROOT/'tests/test_mainl_graphics_review.py').read_bytes())}
    coldroot=Path(COLD).parent
    for p,h in cold['source_inputs'].items():
        archived=str(coldroot/'repository-inputs'/p)
        if sha((ROOT/archived).read_bytes())!=h:raise ValueError('graphics cold archived input differs: '+p)
        inputs[archived]=h
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('graphics input changed: '+p)
    def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('memory_before_sha256','memory_after_sha256')} for row in cpu]
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    paths=[prior['observations'][0]['path']]+[str(coldroot/f'round{i}/source/bin/th03/mainl.exe') for i in (1,2)]
    observations=[];objects=[]
    for index,path in enumerate(paths):
        raw=(ROOT/path).read_bytes();inputs[path]=sha(raw);mz=parse_mz(raw)
        if not mz.valid:raise ValueError('graphics invalid complete image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz),nonterminal=nonterminal(mz))
        if index:
            if sha(raw)!=cold['rounds'][index-1]['products']['bin/th03/mainl.exe']:raise ValueError('graphics cold product hash differs')
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('graphics complete body/CFG differs')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached);actual=cached.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else cached
                if actual!=cached_provider(p,d):raise ValueError('graphics frozen cached provider differs: '+p)
            op=str(tree/'obj/th03/mainl.obj');data=(ROOT/op).read_bytes();inputs[op]=sha(data);obj=describe_omf(data)
            if not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0'] or obj['dependency_timestamp_normalized_sha256']!=cold['rounds'][index-1]['all_objects']['obj/th03/mainl.obj']:raise ValueError('graphics cold root OMF identity differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments','record_count','record_counts')}
            if objects and obj['dependency_timestamp_normalized_sha256']!=objects[0]['dependency_timestamp_normalized_sha256']:raise ValueError('graphics OMF differs beyond timestamps')
            objects.append(observed['object']);mp=str(tree/'obj/th03/mainl.map');mapdata=(ROOT/mp).read_bytes();inputs[mp]=sha(mapdata);maptext=mapdata.decode();maprows=code_rows(maptext,len(mz.program_image));carrier=next(row for row in maprows if row['module']=='th03_mainl.asm' and row['segment']==0 and row['size'])
            for name,offset in PUBLICS.items():
                addresses={(int(s,16),int(o,16)) for s,o in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(name)+r'\s*$',maptext,re.MULTILINE)}
                if addresses!={(0,offset)}:raise ValueError('graphics public MAP entry/alias differs: '+name)
            observed['public_entries']=PUBLICS
            if not all(carrier['start']<=a<a+n<=carrier['start']+carrier['size'] for _,a,n,_ in RANGES):raise ValueError('graphics includes outside root MAP carrier')
            observed['carrier']=carrier;target=parse_mz((ROOT/paths[0]).read_bytes());extents=[('egc',0x724,98),('boxes',0xac8,366),('near-gdc',0xc66,11),('prior-color',0xc36,48),('read-only-edges',0xe3f0+EDGES,34)]
            observed['comparisons']={n:extent_observation(target,mz,dict(start=a,size=z,segment=0xe3f if n=='read-only-edges' else 0,offset=EDGES if n=='read-only-edges' else a)) for n,a,z in extents}
            if any(not x['raw_slice_equal'] or not x['ordered_relocations_equal'] for x in observed['comparisons'].values()):raise ValueError('graphics raw/ordered relocation differs')
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']) or normalized(observed['nonterminal'])!=normalized(observations[0]['nonterminal']):raise ValueError('graphics target/cold CPU differs')
        observations.append(observed);print('Reviewed',path,len(observed['cpu']),'scenarios',len(observed['nonterminal']),'budgets',flush=True)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('graphics canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('graphics frozen provider changed')
    result=dict(kind='th03-mainl-complete-egc-grcg-gdc-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},build_scaffold_main_remaps=BUILD_REMAPS,cold_lineage=dict(receipt=COLD,sha256=COLD_SHA,fresh_compiler_rounds=2,archived_source_inputs=len(cold['source_inputs'])),observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,new_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL EGC/boxes/near GDC475newbytes, prior color46context, exact open:',args.output)


if __name__=='__main__':main()
