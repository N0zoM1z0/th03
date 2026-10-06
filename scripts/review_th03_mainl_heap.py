#!/usr/bin/env python3
"""Complete MAINL heap manager, shared tails and DOS assignment diagnostics."""
import argparse
from collections import Counter
from datetime import datetime,timezone
from importlib.metadata import version
from itertools import permutations,product
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

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-mainl-file-review-20261006.json'
PROOF_SHA256='1ff567ea3b16ed511d3a0222f3a111dc55097f973d2a2e10b38d77c62aad07ef'
RANGES=[('long',0x210a,52,4),('assign_dos',0x213e,33,2),('assign',0x2160,38,4),
 ('assign_all',0x2186,39,0),('byte',0x21ae,20,2),('allocate',0x21c2,240,2),
 ('free',0x22b2,168,2),('unassign',0x235a,35,0)]
ALIGNMENT={0x215f:0x90,0x21ad:0x90,0x237d:0x90}
CALLS={0x212f:0x21c2,0x214e:0x2160,0x21a1:0x2160,0x21d1:0x2186}
CROSS={0x21c0:0x21c9,0x22c4:0x22ac,0x22cc:0x22ac}
DOS={0x2147:0x48,0x218c:0x48,0x2199:0x48,0x2373:0x49}
TOP,OWN,ID,RESERVE,OUT,HEAP,HOLE,END=0x852,0x854,0x856,0x858,0x1458,0x145a,0x145c,0x145e
PROVIDERS=['th03_mainl.asm','ReC98.inc','th03/th03.inc','libs/master.lib/master.inc',
 'libs/master.lib/macros.inc','libs/master.lib/func.hpp','libs/master.lib/super.inc',
 'libs/master.lib/mem[data].asm','libs/master.lib/mem[bss].asm',
 'libs/master.lib/hmem_lallocate.asm','libs/master.lib/mem_assign_dos.asm',
 'libs/master.lib/mem_assign.asm','libs/master.lib/memheap.asm','libs/master.lib/mem_unassign.asm',
 'libs/master.lib/func.inc','Tupfile.lua']
NAMES={a:n for n,a,_,_ in RANGES}

BUILD_REMAPS={'th03/playfld.cpp':'th03/playfld.asm','th02/snd_mode.c':'th03/snd_mode_main.asm',
 'th02/snd_pmdr.c':'th03/snd_pmdr_main.asm','th03/vector.cpp':'th03/vectorfar.asm',
 'th02/snd_se_r.cpp':'th03/snd_se_r_main.asm','th03/mrs.cpp':'th03/mrs.asm',
 'th03/sprite16.cpp':'th03/sprite16.asm'}


def cached_provider(path,source):
    if path!='Tupfile.lua':return source.replace(b'\r\n',b'\n') if path.endswith(('.asm','.inc')) else source
    # Only the prior maintained MAIN graph changes; MAINL GAME=3 flags stay frozen.
    first=source.index(b'th03:branch(MODEL_LARGE, { cflags = "-DBINARY=\'M\'" })')
    last=source.index(b'th03:branch(MODEL_LARGE, { cflags = "-DBINARY=\'L\'" })',first)
    body=source[first:last]
    for old,new in BUILD_REMAPS.items():
        old=b'"'+old.encode()+b'"';new=b'"'+new.encode()+b'"'
        if body.count(old)!=1:raise ValueError('heap scaffold MAIN remap differs')
        body=body.replace(old,new)
    return source[:first]+body+source[last:]


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[];returns={};all_bounds=set();decoded=[]
    for name,start,size,cleanup in RANGES:
        body=image[start:start+size]
        if len(body)!=size:raise ValueError('heap complete include body differs')
        ins=list(decoder.disasm(body,start))
        if not ins or sum(i.size for i in ins)!=size:raise ValueError('heap complete instruction partition differs')
        if name=='byte':
            if ins[-1].bytes!=b'\xeb\x07':raise ValueError('heap byte shared-tail jump differs')
        elif (ins[-1].mnemonic,ins[-1].op_str)!=('retf',str(cleanup) if cleanup else ''):raise ValueError('heap final far cleanup differs')
        all_bounds.update(i.address for i in ins);decoded.append((name,start,size,cleanup,ins))
    for name,start,size,cleanup,ins in decoded:
        bounds={i.address for i in ins};edges=[]
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf'):
                if (i.mnemonic,i.op_str)!=('retf',str(cleanup) if cleanup else ''):raise ValueError('heap interior return differs')
                returns[i.address]=cleanup
            if i.mnemonic in ('in','out'):raise ValueError('heap unexpected port')
            if i.mnemonic=='int':
                if i.address not in DOS or i.bytes!=b'\xcd\x21':raise ValueError('heap unknown DOS site')
                edges.append(dict(instruction=i.address,kind='modeled-int21',ah=DOS[i.address]));continue
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('heap unknown indirect edge')
            if i.mnemonic=='lcall':raise ValueError('heap unknown far interface')
            dest=i.operands[0].imm
            if i.mnemonic=='call':
                if CALLS.get(i.address)!=dest:raise ValueError('heap unknown native call site/target')
                if not j or ins[j-1].bytes!=b'\x0e':raise ValueError('heap far call lacks PUSH CS')
            elif CROSS.get(i.address)==dest:
                if dest not in all_bounds:raise ValueError('heap shared tail enters operand')
            elif dest not in bounds:raise ValueError('heap branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=start,size=size,instructions=len(ins),sha256=sha(image[start:start+size]),cleanup=cleanup,edges=edges))
    if any(image[a:a+1]!=bytes([v]) for a,v in ALIGNMENT.items()):raise ValueError('heap complete producer alignment differs')
    if image[0x2379:0x237d]!=b'\x33\xc0\xf9\xcb':raise ValueError('heap emitted unreachable failure tail differs')
    return dict(bodies=rows,body_bytes=625,producer_bytes=3,complete_include_bytes=628,returns=returns,producers=ALIGNMENT,shared_edges=CROSS,unreachable_failure_tail=dict(offset=0x2379,size=4))


class HeapProbe(Probe):
    """Native routines and far returns; DOS allocation/free is the sole interface."""
    def __init__(self,mz,s,observed=None):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x20000,0x2e3f0,0x40000
        self.s=s;self.frames=[];self.errors=[];self.events=[];self.native=Counter();self.stop=False;self.direct=None;self.write_count=0
        self.returns=(observed or analyze(mz.program_image))['returns'];self.dos_index=0
        self.uc.mem_write(0x50000,b'\xa5'*0x40000)
        defaults={TOP:0x6000,OWN:0,ID:0xbeef,RESERVE:256,OUT:0x6100,HEAP:0x6100,HOLE:0,END:0x6000}
        for a,v in defaults.items():self.uc.mem_write(self.data+a,struct.pack('<H',s.get({TOP:'top',OWN:'own',ID:'id',RESERVE:'reserve',OUT:'out',HEAP:'heap',HOLE:'hole',END:'end'}[a],v)))
        for seg,using,nextseg,ident in s.get('blocks',[]):self.uc.mem_write(seg*16,struct.pack('<3H',using,nextseg,ident))
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2000:raise ValueError('heap terminal segment alias')
                if self.frames:raise ValueError('heap unfinished native frame')
                self.stop=True;uc.emu_stop();return
            off=address-self.code
            if self.get('CS')!=0x2000 or not any(a<=off<a+n for _,a,n,_ in RANGES):raise ValueError('CPU escaped heap bodies/segment alias')
            if off in NAMES:
                sp=self.get('SP');ip,cs=struct.unpack('<2H',uc.mem_read(self.stack+sp,4));direct=not self.frames and off==self.direct and ip==0xff00
                if cs!=0x2000 or (not direct and CALLS.get(ip-3)!=off):raise ValueError('heap native far frame differs')
                self.frames.append((sp,ip,cs,next(z for _,a,_,z in RANGES if a==off)));self.native[NAMES[off]]+=1
            if off in self.returns:
                if not self.frames:raise ValueError('heap orphan far return')
                sp,ip,cs,cleanup=self.frames.pop()
                if self.get('SP')!=sp or tuple(struct.unpack('<2H',uc.mem_read(self.stack+sp,4)))!=(ip,cs) or self.returns[off]!=cleanup:raise ValueError('heap native return frame differs')
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            state=any(self.data+a<=address and address+size<=self.data+a+z for a,z in ((TOP,6),(OUT,8)))
            header=size==2 and address%16 in (0,2,4) and (0x50000<=address and address+size<=0x90000 or any(seg*16<=address and address+size<=seg*16+6 for seg,_,_,_ in s.get('blocks',[])))
            if not state and not header:raise ValueError('heap write outside owned state/header')
            self.write_count+=1
        def intr(uc,number,user):
            site=u16(self.get('IP')-2);ah=self.get('AH')
            if number!=0x21 or self.get('CS')!=0x2000 or DOS.get(site)!=ah:raise ValueError('heap unknown DOS request/site')
            if ah==0x48:
                i=self.dos_index;self.dos_index+=1;items=s.get('dos_allocs',[]);query=site==0x218c
                item=items[i] if i<len(items) else {};ax=item.get('ax',8 if query else 0x6000);cf=item.get('cf',1 if query else 0);bx=item.get('bx',s.get('largest',0x200) if query else self.get('BX'))
                self.events.append(dict(site=site,name='dos_allocate',size=self.get('BX'),ax=ax,bx=bx,cf=cf));self.set('BX',bx)
            else:
                ax=s.get('dos_free_ax',7);cf=s.get('dos_free_cf',1);self.events.append(dict(site=site,name='dos_free',segment=self.get('ES'),ax=ax,cf=cf))
            self.set('AX',ax);self.set('EFLAGS',(self.get('EFLAGS')&~1)|cf)
        def out(uc,port,width,value,user):raise ValueError('heap unexpected output port')
        def inp(uc,port,width,user):raise ValueError('heap unexpected input port')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(out),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)

    def run(self,name,args=(),budget=100000):
        _,start,_,cleanup=next(r for r in RANGES if r[0]==name);self.direct=start;self.stop=False;self.errors.clear();self.frames.clear()
        for r,v in dict(CS=0x2000,DS=0x2e3f,SS=0x4000,ES=0x3333,AX=0x1111,BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,SP=0xffc0,EFLAGS=0x202|(0x400 if self.s.get('df') else 0)|self.s.get('initial_cf',0)).items():self.set(r,v)
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2000,*args));self.uc.emu_start(self.code+start,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('heap terminal/budget differs')
        regs=['BX','CX','DX','BP','SI','DI','DS']+([] if name=='unassign' else ['ES'])
        expected=dict(BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,DS=0x2e3f,ES=0x3333)
        if self.get('SP')!=0xffc4+cleanup or any(self.get(r)!=expected[r] for r in regs):raise ValueError('heap far cleanup/callee-saved differs')
        if bool(self.get('EFLAGS')&0x400)!=bool(self.s.get('df')):raise ValueError('heap DF differs')


class Scalar:
    """Independent segment-list algorithm over the same physical memory fixture."""
    def __init__(self,p):
        self.mem=bytearray(p.uc.mem_read(0,0x100000));self.data=p.data;self.s=p.s;self.events=[];self.native=Counter();self.dos_index=0
    def word(self,a):return struct.unpack_from('<H',self.mem,a)[0]
    def w(self,a,v):struct.pack_into('<H',self.mem,a,u16(v))
    def get(self,a):return self.word(self.data+a)
    def put(self,a,v):self.w(self.data+a,v)
    def head(self,segment,offset=0):return self.word(segment*16+offset)
    def header(self,segment,offset,value):self.w(segment*16+offset,value)
    def dos(self,site,size=0):
        s=self.s
        if site!=0x2373:
            i=self.dos_index;self.dos_index+=1;items=s.get('dos_allocs',[]);query=site==0x218c
            item=items[i] if i<len(items) else {};ax=item.get('ax',8 if query else 0x6000);cf=item.get('cf',1 if query else 0);bx=item.get('bx',s.get('largest',0x200) if query else size)
            self.events.append(dict(site=site,name='dos_allocate',size=size,ax=ax,bx=bx,cf=cf));return ax,bx,cf
        ax=s.get('dos_free_ax',7);cf=s.get('dos_free_cf',1);self.events.append(dict(site=site,name='dos_free',segment=self.get(TOP),ax=ax,cf=cf));return ax,0,cf
    def assign(self,top,size):
        self.put(TOP,top);self.put(END,top);self.put(OUT,top+size);self.put(HEAP,top+size);self.put(HOLE,0);self.put(OWN,0)
    def allocation(self,size):
        if not self.get(TOP):self.run('assign_all')
        if not size or size>=u16(self.get(OUT)-self.get(END)):self.put(ID,0);return 0,1
        need=size+1;cur=self.get(HOLE);chosen=None
        for _ in range(10000):
            if not cur:break
            nextseg=self.head(cur,2);using=self.head(cur);end=cur+need
            if not using and end<=65535 and end<=nextseg:
                chosen=cur
                if nextseg-end>1:
                    self.header(cur,0,1);self.header(cur,2,end);self.header(end,2,nextseg);self.header(end,0,0)
                    if cur==self.get(HOLE):self.put(HOLE,end)
                else:
                    self.header(cur,0,1)
                    if cur==self.get(HOLE):
                        bx=cur;es=cur
                        for _ in range(10000):
                            state=self.head(es);next_=self.head(es,2);es=next_
                            if not state:break
                            if es>=self.get(OUT):bx=0;break
                            bx=es
                        else:raise ValueError('scalar next-hole budget')
                        self.put(HOLE,bx)
                break
            cur=nextseg
            if cur==self.get(OUT):break
        else:raise ValueError('scalar search-hole budget')
        if chosen is None:
            old=self.get(HEAP);chosen=old-need
            if chosen<0 or chosen<self.get(END):self.put(ID,0);return 0,1
            self.put(HEAP,chosen);self.header(chosen,2,old);self.header(chosen,0,1)
        ident=self.get(ID);self.put(ID,0);self.header(chosen,4,ident);return u16(chosen+1),0
    def free(self,segment):
        cur=u16(segment-1);top=self.get(HEAP)
        if cur<top:return None,1
        if cur==top:
            next_=self.head(cur,2);self.put(HEAP,next_)
            if next_==self.get(OUT) or self.head(next_)!=0:return None,0
            es=next_;next_=self.head(es,2);self.put(HEAP,next_);hole=0
            for _ in range(10000):
                if next_==self.get(OUT):break
                es=next_
                if not self.head(es):hole=es;break
                next_=self.head(es,2)
            else:raise ValueError('scalar expand-center budget')
            self.put(HOLE,hole);return None,0
        using=self.head(cur)
        if using!=1:return None,int(using<1)
        self.header(cur,0,0);oldhole=self.get(HOLE);self.put(HOLE,cur)
        if not oldhole:return None,0
        first=min(cur,oldhole);self.put(HOLE,first);limit=self.head(cur,2)
        if limit==self.get(OUT):limit=cur
        current=first
        for _ in range(10000):
            next_=self.head(current,2)
            if next_>limit:break
            if self.head(current)!=0:current=next_;continue
            if self.head(next_)!=0:current=next_;continue
            while True:
                next_=self.head(next_,2);self.header(current,2,next_)
                if next_>limit:break
                if self.head(next_)!=0:current=next_;break
            if next_>limit:break
        else:raise ValueError('scalar connect-free budget')
        return None,0
    def run(self,name,args=()):
        self.native[name]+=1;s=self.s
        if name=='assign':self.assign(args[1],args[0]);return u16(args[1]+args[0]),0
        if name=='assign_dos':
            ax,bx,cf=self.dos(0x2147,args[0])
            if not cf:self.run('assign',[bx,ax]);self.put(OWN,1);ax=0
            return u16(-ax),int(ax!=0)
        if name=='assign_all':
            _,largest,_=self.dos(0x218c,65535);reserve=self.get(RESERVE);size=largest-reserve if largest>reserve else largest
            ax,bx,cf=self.dos(0x2199,size)
            if not cf:self.run('assign',[bx,ax]);self.put(OWN,1);cf=0
            return ax,cf
        if name=='allocate':return self.allocation(args[0])
        if name=='byte':return self.allocation((args[0]+15)>>4)
        if name=='long':
            rounded=((args[1]<<16)|args[0])+15;rounded&=0xffffffff
            if rounded>>4>65535:return 0,1
            return self.run('allocate',[rounded>>4])
        if name=='free':return self.free(args[0])
        if name=='unassign':
            if not self.get(TOP):return 1,0
            cf=0
            if self.get(OWN):_,_,cf=self.dos(0x2373)
            self.put(TOP,0);return 1,cf
        raise ValueError('scalar unknown heap entry')


def matrix(mz):
    rows=[]
    def observe(name,s,steps=None):
        p=HeapProbe(mz,s);scalar=Scalar(p);before=sha(bytes(scalar.mem));results=[];allocations=[]
        for step in steps or [dict(function=name)]:
            fn=step['function'];args=step.get('args',[])
            if fn=='free' and 'allocation' in step:args=[allocations[step['allocation']]]
            ax,cf=scalar.run(fn,args);p.run(fn,args)
            if (ax is not None and p.get('AX')!=ax) or p.get('EFLAGS')&1!=cf or p.events!=scalar.events or p.native!=scalar.native:raise ValueError('heap result/CF/native/DOS scalar differs: '+str((fn,s,step,p.get('AX'),ax,p.get('EFLAGS')&1,cf,p.events,scalar.events)))
            actual=bytes(p.uc.mem_read(0,0x100000))
            if actual[:p.stack]!=scalar.mem[:p.stack] or actual[p.stack+65536:]!=scalar.mem[p.stack+65536:]:
                changed=[i for i,(a,b) in enumerate(zip(actual,scalar.mem)) if a!=b and not p.stack<=i<p.stack+65536]
                raise ValueError('heap full physical memory scalar differs: '+str((fn,s,step,changed[:20])))
            if fn in ('byte','allocate','long'):allocations.append(p.get('AX'))
            results.append(dict(function=fn,args=args,ax=ax,cf=cf,top=scalar.get(TOP),heap=scalar.get(HEAP),hole=scalar.get(HOLE),out=scalar.get(OUT),end=scalar.get(END),id=scalar.get(ID),own=scalar.get(OWN)))
        rows.append(dict(function=name,scenario=s,steps=results,top_level_calls=len(results),events=p.events,native_entries=dict(p.native),write_count=p.write_count,memory_before_sha256=before,memory_after_sha256=sha(bytes(scalar.mem))))
    for df in (False,True):
        for size in (0,1,2,15,16,17,254,255,256,257,32767,32768,65520,65521,65535):
            for fn in ('byte','allocate'):observe(fn,dict(df=df),[dict(function=fn,args=[size])])
        for size in (0,1,15,16,17,65520,65521,65535,65536,0xffff0,0xffff1,0x100000,0xfffffff0,0xfffffff1,0xffffffff):
            observe('long',dict(df=df),[dict(function='long',args=[size&65535,size>>16])])
        for heap,end,out in ((0x6100,0x6000,0x6100),(0x6002,0x6000,0x6100),(0x6001,0x6000,0x6100),(1,0,0x100),(0x6100,0x6200,0x6000)):
            for size in (0,1,2,255,65535):observe('allocate',dict(df=df,heap=heap,end=end,out=out),[dict(function='allocate',args=[size])])
        for top in (0,1,0x6000,0xffff):
            for size in (0,1,256,65535):observe('assign',dict(df=df),[dict(function='assign',args=[size,top])])
        for own in (0,1,2,65535):
            for top in (0,0x6000):
                for cf in (0,1):observe('unassign',dict(df=df,own=own,top=top,heap=0x60f0,end=0x6001,dos_free_cf=cf))
        for cf in (0,1):
            for ax in (0,8,0x6000):observe('assign_dos',dict(df=df,dos_allocs=[dict(ax=ax,cf=cf)]),[dict(function='assign_dos',args=[512])])
        for largest in (0,1,255,256,257,512,65535):
            for reserve in (0,256,65535):
                for cf in (0,1):observe('assign_all',dict(df=df,largest=largest,reserve=reserve,dos_allocs=[dict(cf=0),dict(cf=cf)]))
        for size in (0,1,15,16,17,65535):
            for cf in (0,1):observe('lazy',dict(df=df,top=0,dos_allocs=[dict(cf=1),dict(cf=cf)]),[dict(function='byte',args=[size])])
        # Every combination of free/used/odd-using headers exercises search/split/fit.
        for states in product((0,1,2),repeat=3):
            blocks=[[0x6000,states[0],0x6010,0x1111],[0x6010,states[1],0x6020,0x2222],[0x6020,states[2],0x6100,0x3333]]
            first=next((b[0] for b in blocks if b[1]==0),0)
            for size in (1,14,15,16,17,127):observe('holes',dict(df=df,heap=0x6000,hole=first,blocks=blocks),[dict(function='allocate',args=[size])])
        for using in (0,1,2,65535):
            for segment in (0,0x5fff,0x6000,0x6001,0x6011,0x6021,0x6101):
                blocks=[[0x6000,using,0x6010,0x1111],[0x6010,using,0x6020,0x2222],[0x6020,1,0x6100,0x3333],[0x6100,using,0x6100,0x4444],[0xffff,using,0x6100,0x5555]]
                observe('free',dict(df=df,heap=0x6000,blocks=blocks),[dict(function='free',args=[segment])])
        for hole in (0x6000,0x6010,0x6020):
            for states in product((0,1),repeat=3):
                blocks=[[0x6000,states[0],0x6010,1],[0x6010,states[1],0x6020,2],[0x6020,states[2],0x6100,3]]
                observe('free-connect',dict(df=df,heap=0x6000,hole=hole,blocks=blocks),[dict(function='free',args=[0x6011])])
        observe('hole-add-carry',dict(df=df,hole=0xfff0,blocks=[[0xfff0,0,0x6100,7]]),[dict(function='allocate',args=[31])])
        for order in permutations(range(4)):
            steps=[dict(function='allocate',args=[8]) for _ in range(4)]+[dict(function='free',allocation=i) for i in order]+[dict(function='allocate',args=[255]),dict(function='unassign')]
            observe('free-order-chain',dict(df=df),steps)
        for size in (14,15,16,127):
            observe('reuse-chain',dict(df=df),[dict(function='allocate',args=[15]),dict(function='allocate',args=[15]),dict(function='allocate',args=[15]),dict(function='free',allocation=0),dict(function='allocate',args=[size]),dict(function='free',allocation=1),dict(function='free',allocation=2)])
        for cf in (0,1):observe('assignment-chain',dict(df=df,top=0,dos_allocs=[dict(cf=1),dict(cf=cf)]),[dict(function='assign_all'),dict(function='byte',args=[32]),dict(function='unassign')])
    return rows


def nonterminal(mz):
    """Two malformed cyclic lists stop at bounded native loops, without fake returns."""
    rows=[]
    for df in (False,True):
        for name,s,args,changed,loop in [
            ('allocate',dict(df=df,hole=0x6500,out=0x6600,heap=0x6600,blocks=[[0x6500,1,0x6500,7]]),[1],None,{0x21f1,0x21f3,0x21f7,0x21fd,0x220d,0x220f}),
            ('free',dict(df=df,heap=0x6000,hole=0x6010,blocks=[[0x6010,1,0x6010,7],[0x6020,1,0x6030,8]]),[0x6021],0x60200,{0x22f4,0x22f6,0x22f9,0x22fb,0x22fd,0x22ff})]:
            p=HeapProbe(mz,s);expected=bytearray(p.uc.mem_read(0,0x100000));before=sha(bytes(expected))
            if changed is not None:struct.pack_into('<H',expected,changed,0)
            try:p.run(name,args,budget=1000)
            except ValueError as e:
                if str(e)!='heap terminal/budget differs':raise
            else:raise ValueError('heap cyclic list unexpectedly returned')
            actual=bytes(p.uc.mem_read(0,0x100000))
            if actual[:p.stack]!=expected[:p.stack] or actual[p.stack+65536:]!=expected[p.stack+65536:] or p.events or dict(p.native)!={name:1} or p.get('IP') not in loop:raise ValueError('heap cyclic-loop boundary/state differs')
            rows.append(dict(function=name,scenario=s,args=args,budget=1000,outcome='native-cyclic-list-budget',instruction=p.get('IP'),native_entries=dict(p.native),events=p.events,write_count=p.write_count,memory_before_sha256=before,memory_after_sha256=sha(bytes(expected))))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('heap prior file proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_heap.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('heap input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];objects=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('heap invalid image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz),nonterminal=nonterminal(mz))
        if observations:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('heap complete body/CFG differs')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                expected=cached_provider(p,d)
                actual=cached.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else cached
                if actual!=expected:raise ValueError('heap cached frozen provider differs: '+p)
            op=str(tree/'obj/th03/mainl.obj');obj_data=(ROOT/op).read_bytes();inputs[op]=sha(obj_data);obj=describe_omf(obj_data)
            if not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0']:raise ValueError('heap cached root OMF identity differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments','record_count','record_counts')}
            if objects and obj['dependency_timestamp_normalized_sha256']!=objects[0]['dependency_timestamp_normalized_sha256']:raise ValueError('heap cached OMF differs beyond dependency timestamps')
            objects.append(observed['object']);maprows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));carrier=next(row for row in maprows if row['module']=='th03_mainl.asm' and row['segment']==0 and row['size'])
            if not all(carrier['start']<=a<a+n<=carrier['start']+carrier['size'] for _,a,n,_ in RANGES):raise ValueError('heap includes outside complete root carrier')
            observed['carrier']=carrier;target=parse_mz((ROOT/observations[0]['path']).read_bytes())
            extents=[('complete-heap-includes',0x210a,628)]
            observed['comparisons']={n:extent_observation(target,mz,dict(start=a,size=z,segment=0,offset=a)) for n,a,z in extents}
            if any(not x['raw_slice_equal'] or not x['ordered_relocations_equal'] for x in observed['comparisons'].values()):raise ValueError('heap complete raw/ordered relocations differ')
            def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('memory_before_sha256','memory_after_sha256')} for row in cpu]
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']) or normalized(observed['nonterminal'])!=normalized(observations[0]['nonterminal']):raise ValueError('heap target/cached CPU differs')
        observations.append(observed);print('Reviewed',path,len(observed['cpu']),'scenarios',flush=True)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('heap canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('heap frozen provider changed')
    result=dict(kind='th03-mainl-complete-heap-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},build_scaffold_main_remaps=BUILD_REMAPS,observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL complete heap628bytes, shared tails and explicit DOS:',args.output)


if __name__=='__main__':main()
