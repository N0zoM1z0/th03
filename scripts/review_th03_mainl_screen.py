#!/usr/bin/env python3
"""Complete MAINL screen mode, clear and page-copy candidates with native stack context."""
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
from review_th03_mainl_super import SuperProbe
from review_th03_mainl_graphics import initial_flags,COLD,COLD_SHA

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-mainl-gaiji-review-20261006.json'
PROOF_SHA='862d1c5a3085db80ee350eb9e1257f46d0a6a632b870edf880f083dce8eb74dc'
OWN_RANGES=[('mode',0xe24,77,0),('clear',0xe72,35,0),('plane',0xe96,21,'near'),('copy',0xeac,85,2)]
CONTEXT=heap.RANGES+smem.OWN_RANGES;RANGES=OWN_RANGES+CONTEXT
ENTRY={n:a for n,a,_,_ in RANGES};ENTRY['get']=0x1ec0
ALIGNMENT={a:0x90 for a in (0xe71,0xe95,0xeab,0xf01)}
INTERIOR={0xeb7:0x90,0xef6:0x90}
CALLS={**heap.CALLS,0x1ebb:0x2186,0xeb9:0x1ec0,0xef8:0x1eaa}
NEAR={a:0xe96 for a in (0xed1,0xed4,0xeda,0xedd,0xee3,0xee6,0xeec,0xeef)}
DOS=heap.DOS
PORTS={0xe76:0x7c,0xe7e:0x7e,0xe7f:0x7e,0xe80:0x7e,0xe81:0x7e,0xe92:0x7c,0xe98:0xa6,0xec1:0x7c}
VRAM_SEG,VRAM_WORDS,VRAM_LINES,VRAM_WIDTH,VRAM_ZOOM=0x564,0x566,0x568,0x56a,0x56c
APERTURES=[(0xa8000,0x8000),(0xb0000,0x8000),(0xb8000,0x8000),(0xe0000,0x8000)]
OVERFLOW=[(0xc0000,0x8001),(0xe8000,0x8001)]
STATE=[(TOP,6),(OUT,8),(0x522,16),(VRAM_SEG,10)]
PUBLICS={'GRAPH_400LINE':0xe24,'GRAPH_CLEAR':0xe72,'GRAPH_COPY_PAGE':0xeac}
PROVIDERS=list(dict.fromkeys(smem.PROVIDERS+['libs/master.lib/'+n+'.asm' for n in ('graph_400line','graph_clear','graph_copy_page','grp[data]','clip[data]')]))
PATTERN_IMAGE=bytes((i*37+3)&255 for i in range(0x50001))
PAGE_IMAGES=[b''.join(bytes((page*97+plane*53+i*13+11)&255 for i in range(size)) for plane,(_,size) in enumerate(APERTURES)) for page in range(2)]


def analyze(image):
    context=smem.analyze(image);dec=Cs(CS_ARCH_X86,CS_MODE_16);dec.detail=True;decoded=[];bounds=set();returns={};rows=[]
    for n,a,z,c in RANGES:
        body=image[a:a+z]
        if len(body)!=z:raise ValueError('screen complete body differs')
        ins=list(dec.disasm(body,a));expected=('ret','') if c=='near' else ('retf',str(c) if c else '')
        if not ins or sum(i.size for i in ins)!=z:raise ValueError('screen instruction partition differs')
        if n!='byte' and (ins[-1].mnemonic,ins[-1].op_str)!=expected:raise ValueError('screen terminal cleanup differs')
        bounds.update(i.address for i in ins);decoded.append((n,a,z,c,ins,expected))
    for n,a,z,c,ins,expected in decoded:
        edges=[]
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf'):
                if (i.mnemonic,i.op_str)!=expected:raise ValueError('screen interior cleanup differs')
                returns[i.address]=c
            if i.mnemonic=='int':
                if i.address==0xe28:
                    if i.bytes!=b'\xcd\x18':raise ValueError('screen mode BIOS site differs')
                elif i.address not in DOS or i.bytes!=b'\xcd\x21':raise ValueError('screen unknown interrupt site')
            if i.mnemonic in ('in','out'):
                expected_port=('dx, al' if PORTS.get(i.address)==0x7e else hex(PORTS[i.address])+', al') if i.address in PORTS else None
                if i.mnemonic!='out' or i.op_str!=expected_port:raise ValueError('screen unknown port/site/width')
            if not(i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('screen unknown indirect edge')
            if i.mnemonic in ('lcall','ljmp'):raise ValueError('screen unknown far edge')
            dest=i.operands[0].imm
            if i.mnemonic=='call':
                if NEAR.get(i.address)!=dest:
                    if CALLS.get(i.address)!=dest:raise ValueError('screen unknown native call')
                    if not j or ins[j-1].bytes!=b'\x0e':raise ValueError('screen far call lacks PUSH CS')
            elif dest not in bounds:raise ValueError('screen branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=n,offset=a,size=z,instructions=len(ins),cleanup=c,sha256=sha(image[a:a+z]),edges=edges))
    if any(image[a:a+1]!=bytes([v]) for a,v in {**ALIGNMENT,**INTERIOR,**heap.ALIGNMENT,**smem.ALIGNMENT}.items()):raise ValueError('screen producer alignment differs')
    return dict(bodies=rows,bounds=sorted(bounds),returns=returns,new_body_bytes=218,new_alignment_bytes=4,new_extent_bytes=222,interior_nopcall_bytes=2,prior_context_bytes=704,heap_stack=context,alignment=ALIGNMENT,interior_nopcall=INTERIOR)


class ScreenProbe(Probe):
    prepare=SuperProbe.prepare
    enter=SuperProbe.enter
    leave=SuperProbe.leave
    def __init__(self,mz,s,meta=None):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000);image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x20000,0x2e3f0,0x40000;self.s=s;self.meta=meta or analyze(mz.program_image);self.bounds=set(self.meta['bounds']);self.returns=self.meta['returns'];self.entry_names={a:n for n,a in ENTRY.items()};self.calls=CALLS|NEAR;self.frames=[];self.pending=None;self.stop=False;self.errors=[];self.native=Counter();self.events=[];self.ports=[];self.visited=set();self.dos_index=0;self.writes=[];self.context_stores=0
        self.uc.mem_write(0x50000,PATTERN_IMAGE)
        for a,z in OVERFLOW:self.uc.mem_write(a,bytes((i*29+0xa5)&255 for i in range(z)))
        self.uc.mem_write(0x54d,bytes([s.get('clock',0)]))
        for a,key,default in ((TOP,'top',0x6000),(OWN,'own',0),(ID,'id',0xbeef),(RESERVE,'reserve',256),(OUT,'out',0x8800),(HEAP,'heap',0x8800),(HOLE,'hole',0),(END,'end',0x6000),(VRAM_SEG,'vram_seg',0xa800),(VRAM_WORDS,'words',16000),(VRAM_WIDTH,'vram_width',80)):
            self.uc.mem_write(self.data+a,struct.pack('<H',s.get(key,default)))
        for seg,using,nextseg,ident in s.get('blocks',[]):self.uc.mem_write(seg*16,struct.pack('<3H',using,nextseg,ident))
        self.pages=[bytearray(p) for p in PAGE_IMAGES];self.selected=s.get('page',0);self.mode=s.get('grcg',0xc0);self.tiles=[17,34,51,68];self.load_page(self.selected)
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2000:raise ValueError('screen terminal segment alias')
                if self.frames or self.pending:raise ValueError('screen unfinished native frame')
                self.stop=True;uc.emu_stop();return
            off=address-self.code
            if self.get('CS')!=0x2000 or self.get('SS')!=0x4000:raise ValueError('screen CODE/stack segment alias')
            if off not in self.bounds:raise ValueError('CPU escaped screen instruction boundaries')
            self.visited.add(off);name=self.entry_names.get(off)
            if name and not(name=='get' and self.pending is None and self.frames and self.frames[-1]['name']=='get'):
                self.enter(name,next(c for n,_,_,c in RANGES if n==name));self.native[name]+=1
            if off==0x1ec0 and s.get('assignment_budget') and self.native['assign']==s['assignment_budget']:
                if self.frames[-1]['name']!='get' or self.word(TOP)!=0:raise ValueError('screen assignment budget phase differs')
                uc.emu_stop();return
            if off in self.calls:
                name=self.entry_names[self.calls[off]];cleanup='near' if off in NEAR else next(c for n,_,_,c in RANGES if n==name);self.prepare(name,self.get('SP')-2,off+3,cleanup)
            if off in self.returns:self.leave(self.returns[off])
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            allowed=any(self.data+a<=address and address+size<=self.data+a+z for a,z in STATE) or 0x50000<=address and address+size<=0xa0001 or 0xa8000<=address and address+size<=0xc8001 or 0xe0000<=address and address+size<=0xf0001
            if not allowed:raise ValueError('screen store outside declared state/buffer/aperture/overflow span')
            if 0xe24<=self.get('IP')<0xf02:self.writes.append([address,size,value])
            else:self.context_stores+=1
        def intr(uc,number,user):
            site=u16(self.get('IP')-2);ah=self.get('AH')
            if number==0x18 and self.get('CS')==0x2000 and site==0xe28 and ah==0x42 and self.get('CH')==0xc0:
                ax=s.get('bios_ax',0xabcd);cf=s.get('bios_cf',0);event=dict(site=site,name='modeled-int18-mode',ax_request=self.get('AX'),cx_request=self.get('CX'),ax=ax,cf=cf)
            elif number==0x21 and self.get('CS')==0x2000 and DOS.get(site)==ah:
                if ah==0x48:
                    i=self.dos_index;self.dos_index+=1;item=(s.get('dos_allocs',[])+[{}]*3)[i];query=site==0x218c;request=self.get('BX');ax=item.get('ax',8 if query else 0x6000);cf=item.get('cf',1 if query else 0);bx=item.get('bx',s.get('largest',0x200) if query else request);self.set('BX',bx);event=dict(site=site,name='dos_allocate',size=request,ax=ax,bx=bx,cf=cf)
                else:ax=s.get('dos_free_ax',7);cf=s.get('dos_free_cf',1);event=dict(site=site,name='dos_free',segment=self.get('ES'),ax=ax,cf=cf)
            else:raise ValueError('screen unknown BIOS/DOS request/site')
            self.events.append(event);self.set('AX',ax);self.set('EFLAGS',(self.get('EFLAGS')&~1)|cf)
        def out(uc,port,width,value,user):
            if self.get('CS')!=0x2000 or PORTS.get(self.get('IP'))!=port or width!=1:raise ValueError('screen unknown output port/site/width')
            self.ports.append(dict(site=self.get('IP'),port=port,width=width,value=value,live_if=bool(self.get('EFLAGS')&512),live_df=bool(self.get('EFLAGS')&1024)))
            if port==0xa6:
                if value not in (0,1):raise ValueError('screen unknown page selector')
                self.save_page();self.selected=value;self.load_page(value)
            elif port==0x7c:self.mode=value
            else:self.tiles=self.tiles[1:]+[value]
        def inp(*args):raise ValueError('screen unexpected input port')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr));self.uc.hook_add(UC_HOOK_INSN,guard(out),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)
    def save_page(self):self.pages[self.selected]=bytearray(b''.join(bytes(self.uc.mem_read(a,z)) for a,z in APERTURES))
    def load_page(self,page):
        offset=0
        for a,z in APERTURES:self.uc.mem_write(a,bytes(self.pages[page][offset:offset+z]));offset+=z
    def word(self,a):return struct.unpack('<H',self.uc.mem_read(self.data+a,2))[0]
    def run(self,name,args=(),budget=2000000):
        if name=='plane':raise ValueError('screen private plane requires complete public caller')
        self.stop=False;self.errors.clear();self.frames.clear();self.pending=None;cleanup=next(c for n,_,_,c in RANGES if n==name)
        values=dict(CS=0x2000,DS=0x2e3f,SS=0x4000,ES=0x3333,AX=0x1111,BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,SP=0xffc0,EFLAGS=initial_flags(self.s))
        for r,v in values.items():self.set(r,v)
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2000,*args));self.prepare(name,0xffc0,0xff00,cleanup);self.uc.emu_start(self.code+ENTRY[name],0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('screen terminal/budget differs')
        if self.get('SP')!=0xffc4+cleanup or any(self.get(r)!=values[r] for r in ('BP','SI','DI','DS')):raise ValueError('screen cleanup/preserved-register differs')
        self.save_page()


class Scalar(smem.Scalar):
    def __init__(self,p):
        super().__init__(p);self.s=p.s;self.pages=[bytearray(b) for b in p.pages];self.selected=p.selected;self.mode=p.mode;self.tiles=list(p.tiles);self.ports=[];self.writes=[];self.flags=initial_flags(p.s)
    def save_page(self):self.pages[self.selected]=bytearray(b''.join(bytes(self.mem[a:a+z]) for a,z in APERTURES))
    def load_page(self,page):
        offset=0
        for a,z in APERTURES:self.mem[a:a+z]=self.pages[page][offset:offset+z];offset+=z
    def port(self,site,port,value,flags=None):
        flags=self.flags if flags is None else flags;self.ports.append(dict(site=site,port=port,width=1,value=value,live_if=bool(flags&512),live_df=bool(flags&1024)))
        if port==0xa6:self.save_page();self.selected=value;self.load_page(value)
        elif port==0x7c:self.mode=value
        else:self.tiles=self.tiles[1:]+[value]
    def own_write(self,address,value):self.mem[address:address+2]=u16(value).to_bytes(2,'little');self.writes.append([address,2,u16(value)])
    def mode400(self):
        self.events.append(dict(site=0xe28,name='modeled-int18-mode',ax_request=0x4211,cx_request=0xc033,ax=self.s.get('bios_ax',0xabcd),cf=self.s.get('bios_cf',0)))
        for a,v in ((VRAM_SEG,0xa800),(0x52e,0xa800),(VRAM_WORDS,16000),(0x522,0),(0x528,0),(VRAM_ZOOM,0x4000 if self.mem[0x54d]&4 else 0),(0x526,639),(0x524,639),(VRAM_LINES,400),(0x52c,399),(0x52a,399),(0x530,31920)):self.own_write(self.data+a,v)
        return 399,0
    def clear(self):
        self.port(0xe76,0x7c,128,self.flags&~512)
        for site in (0xe7e,0xe7f,0xe80,0xe81):self.port(site,0x7e,0)
        cursor=0;direction=-2 if self.flags&1024 else 2;base=self.get(VRAM_SEG)*16
        for _ in range(self.get(VRAM_WORDS)):self.own_write(base+cursor,0);cursor=u16(cursor+direction)
        self.port(0xe92,0x7c,0);return 0,0
    def copying(self,args):
        words=self.get(VRAM_WORDS);segment,cf=self.run('get',[u16(words*2)])
        if cf:return 0,1
        self.port(0xec1,0x7c,0);page=args[0]&1;direction=-2 if self.flags&1024 else 2
        for plane in (0xa800,0xb000,0xb800,0xe000):
            src,dst=plane,segment
            for _ in range(2):
                self.native['plane']+=1;page^=1;self.port(0xe98,0xa6,page);cursor=0
                for _ in range(words):
                    value=self.word(src*16+cursor);self.own_write(dst*16+cursor,value);cursor=u16(cursor+direction)
                words=cursor>>1;src,dst=dst,src
        self.run('release',[segment]);return 1,0
    def run(self,name,args=()):
        if name not in ('mode','clear','copy'):return super().run(name,args)
        self.native[name]+=1
        result=self.mode400() if name=='mode' else self.clear() if name=='clear' else self.copying(args)
        self.save_page();return result


def trace_hash(rows):return sha(json.dumps(rows,separators=(',',':')).encode())


def compare(p,spec,ax,cf,label):
    p.save_page();spec.save_page();actual=bytes(p.uc.mem_read(0,0x100000))
    if (ax is not None and p.get('AX')!=ax) or (cf is not None and p.get('EFLAGS')&1!=cf) or (p.get('EFLAGS')^spec.flags)&(512|1024) or p.native!=spec.native or p.events!=spec.events or p.ports!=spec.ports or p.writes!=spec.writes or p.pages!=spec.pages or (p.selected,p.mode,p.tiles)!=(spec.selected,spec.mode,spec.tiles):raise ValueError('screen scalar AX/CF/IF/DF/native/interfaces/stores/pages differs: '+str((label,p.get('AX'),ax,p.get('EFLAGS')&1,cf,dict(p.native),dict(spec.native),p.events,spec.events,p.ports,spec.ports,len(p.writes),len(spec.writes),p.writes[:8],spec.writes[:8])))
    if actual[:p.stack]!=spec.mem[:p.stack] or actual[p.stack+65536:]!=spec.mem[p.stack+65536:]:
        changed=[i for i,(a,b) in enumerate(zip(actual,spec.mem)) if a!=b and not p.stack<=i<p.stack+65536];raise ValueError('screen full physical memory differs: '+str((label,changed[:24])))


def matrix(mz):
    rows=[];meta=analyze(mz.program_image)
    def observe(label,s,steps):
        p=ScreenProbe(mz,s,meta);spec=Scalar(p);before=sha(bytes(spec.mem));results=[]
        for name,args in steps:
            spec.flags=initial_flags(s);ax,cf=spec.run(name,args);p.run(name,args);compare(p,spec,ax,cf,(label,s,name,args))
            results.append(dict(function=name,args=args,ax=ax,cf=cf,if_=bool(spec.flags&512),df=bool(spec.flags&1024),registers={r:p.get(r) for r in ('AX','BX','CX','DX','BP','SI','DI','DS','ES','SP')},end=spec.get(END),selected_page=spec.selected,mode=spec.mode,pages_sha256=[sha(bytes(b)) for b in spec.pages]))
        rows.append(dict(function=label,scenario=s,steps=results,top_level_calls=len(steps),native_entries=dict(p.native),events=p.events,ports=p.ports,store_count=len(p.writes),stores_sha256=trace_hash(p.writes),context_stores=p.context_stores,visited=sorted(p.visited),memory_before_sha256=before,memory_after_sha256=sha(bytes(spec.mem))))
    for df in (False,True):
        for irq in (0,512):
            base=dict(df=df,flags=2|irq)
            for clock in range(256):observe('mode-clock-byte',dict(base,clock=clock,vram_width=0x1234),[('mode',[])])
            for cf in (0,1):observe('mode-BIOS-carry',dict(base,bios_cf=cf,bios_ax=0xffff),[('mode',[])])
            for words in (0,1,2,3,255,15999,16000,16384,16385,32767,32768,32769,65535):observe('clear-word-boundaries',dict(base,words=words,page=irq>>9),[('clear',[])])
            for page in (0,1,2,255,256,0xffff):observe('copy-page-low-bit',dict(base,words=7,page=irq>>9),[('copy',[page])])
            for words in (0,1,2,255,15999,16000,16384,16385,32767,32768,32769,65535):observe('copy-word-boundaries',dict(base,words=words),[('copy',[1])])
            for heap_ in (0x6000,0x6001,0x61ff,0x6200):observe('copy-stack-collision',dict(base,heap=heap_,out=heap_),[('copy',[0])])
            for item in ({},{'cf':1,'ax':8}):observe('copy-native-assignment',dict(base,top=0,largest=0x2800,dos_allocs=[{},item],words=7),[('copy',[1])])
            observe('connected-mode-clear-copy',dict(base,clock=4,page=1),[('mode',[]),('clear',[]),('copy',[0]),('copy',[1])])
            observe('temporary-buffer-aliases-page',dict(base,words=7,end=0xa800,heap=0xb000,out=0xb000),[('copy',[1])])
    return rows


def nonterminal(mz):
    rows=[];meta=analyze(mz.program_image)
    for df in (False,True):
        for irq in (0,512):
            s=dict(df=df,flags=2|irq,top=0,words=7,largest=0x2800,assignment_budget=5,dos_allocs=[{},dict(ax=0,cf=0)]*5);p=ScreenProbe(mz,s,meta);spec=Scalar(p);budget=1000;before=sha(bytes(spec.mem))
            try:p.run('copy',[1],budget)
            except ValueError as e:
                if str(e)!='screen terminal/budget differs':raise
            else:raise ValueError('screen zero-TOP assignment unexpectedly returned')
            # Each successful assignment to segment0 leaves TOP zero and retries.
            repeats=s['assignment_budget'];spec.native.update(copy=1,get=1)
            for _ in range(repeats):
                spec.run('assign_all')
            compare(p,spec,None,None,'zero TOP repeated assignment prefix')
            if len(p.frames)!=2 or p.pending or p.stop:raise ValueError('screen assignment prefix falsely completed frame')
            rows.append(dict(function='copy',scenario=s,budget=dict(instructions=budget,complete_zero_top_assignments=repeats),outcome='native-assignment-budget',instruction=p.get('IP'),native_entries=dict(p.native),events=p.events,ports=p.ports,store_count=len(p.writes),memory_before_sha256=before,memory_after_sha256=sha(bytes(spec.mem))))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('screen prior gaiji proof differs')
    proof=json.loads(raw);cold_raw=(ROOT/COLD).read_bytes()
    if sha(cold_raw)!=COLD_SHA:raise ValueError('screen cold proof differs')
    cold=json.loads(cold_raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_screen.py':sha(Path(__file__).read_bytes()),'tests/test_mainl_screen_review.py':sha((ROOT/'tests/test_mainl_screen_review.py').read_bytes())};providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('screen input changed: '+p)
    def normalized(rows):return [{k:v for k,v in r.items() if k not in ('memory_before_sha256','memory_after_sha256')} for r in rows]
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact);observations=[];objects=[]
    for i,prior in enumerate(proof['observations']):
        path=prior['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('screen invalid decoded image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz),nonterminal=nonterminal(mz))
        if i:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('screen complete bodies/CFG differ')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);data=(ROOT/cp).read_bytes();inputs[cp]=sha(data);actual=data.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else data
                if actual!=cached_provider(p,d):raise ValueError('screen frozen cached provider differs: '+p)
            op=str(tree/'obj/th03/mainl.obj');data=(ROOT/op).read_bytes();obj=describe_omf(data);inputs[op]=sha(data)
            if not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0'] or obj['dependency_timestamp_normalized_sha256']!=cold['rounds'][i-1]['all_objects']['obj/th03/mainl.obj']:raise ValueError('screen cold root OMF differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments')};objects.append(observed['object'])
            if len(objects)>1 and objects[-1]['dependency_timestamp_normalized_sha256']!=objects[0]['dependency_timestamp_normalized_sha256']:raise ValueError('screen OMF differs beyond timestamps')
            mp=str(tree/'obj/th03/mainl.map');text=(ROOT/mp).read_text();inputs[mp]=sha((ROOT/mp).read_bytes());carrier=next(r for r in code_rows(text,len(mz.program_image)) if r['module']=='th03_mainl.asm' and r['segment']==0 and r['size'])
            if not all(carrier['start']<=a<a+z<=carrier['start']+carrier['size'] for _,a,z,_ in RANGES):raise ValueError('screen includes outside MAP carrier')
            for name,off in PUBLICS.items():
                coords={(int(s,16),int(o,16)) for s,o in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(name)+r'\s*$',text,re.MULTILINE)}
                if coords!={(0,off)}:raise ValueError('screen public MAP entry differs')
            observed['carrier']=carrier;observed['public_entries']=PUBLICS;target=parse_mz((ROOT/proof['observations'][0]['path']).read_bytes());extents=[('mode',0xe24,78),('clear',0xe72,36),('copy',0xe96,108)]+[(f'prior-{n}',a,z) for n,a,z,_ in CONTEXT]+[(f'prior-even-{a:x}',a,1) for a in heap.ALIGNMENT|smem.ALIGNMENT]
            observed['comparisons']={n:extent_observation(target,mz,dict(start=a,size=z,segment=0,offset=a)) for n,a,z in extents}
            observed['data_comparisons']={name:extent_observation(target,mz,dict(start=0xe3f0+a,size=z,segment=0xe3f,offset=a)) for name,a,z in [('clip-data',0x522,16),('vram-data',0x564,12)]}
            if any(not r['raw_slice_equal'] or not r['ordered_relocations_equal'] for r in list(observed['comparisons'].values())+list(observed['data_comparisons'].values())):raise ValueError('screen raw/ordered relocations differ')
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']) or normalized(observed['nonterminal'])!=normalized(observations[0]['nonterminal']):raise ValueError('screen target/cold CPU differs')
        observations.append(observed);print('Reviewed',path,len(observed['cpu']),'scenarios',len(observed['nonterminal']),'budgets',flush=True)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('screen canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('screen frozen provider changed')
    result=dict(kind='th03-mainl-complete-screen-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},build_scaffold_main_remaps=BUILD_REMAPS,observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,new_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL screen222bytes/native heap-stack704context/synthetic page banks; exact open:',args.output)


if __name__=='__main__':main()
