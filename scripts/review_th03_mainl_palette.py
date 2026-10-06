#!/usr/bin/env python3
"""Complete MAINL palettes/loaders/fades and native VSYNC wait diagnostics."""
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

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-mainl-smem-review-20261006-final.json'
PROOF_SHA256='bca18a2a9cc1c61c27bfbff37921f4f5c38df9ddcb8443fe419c9f84d8491c95'
RANGES=[('bfnt',0x4c6,64,6),('black_in',0x536,67,2),('black_out',0x57a,62,2),
 ('show',0x17d0,266,0),('rgb',0x1a68,66,4),('wait',0x2064,38,0),
 ('white_in',0x208a,63,2),('white_out',0x20ca,64,2),('dos_open',0xaae,26,4)]
ALIGNMENT={0x579:0x90,0x20c9:0x90}
CALLS={0x546:0x2064,0x54b:0x17d0,0x557:0x2064,0x571:0x17d0,
 0x58a:0x2064,0x58f:0x17d0,0x59b:0x2064,0x5b0:0x17d0,0x1a74:0xaae,
 0x2099:0x2064,0x209d:0x17d0,0x20a8:0x2064,0x20c1:0x17d0,
 0x20d9:0x2064,0x20dd:0x17d0,0x20e8:0x2064,0x2102:0x17d0}
DOS={0x4df:0x3f,0x1a83:0x3f,0x1a9c:0x3e,0xaba:0x3d}
OUT_PORTS={0x1803:0xa8,0x1815:0xac,0x1821:0xaa,0x182f:0xae,0x1841:0xf6,
 0x1860:0xa8,0x18bf:0xae,0x18c7:0xac,0x18cf:0xaa}
IN_PORTS={0x1843:0x871e,0x184b:0xae8e,0x206f:0xa0,0x2079:0xa0}
TONE,NOTE,PALETTE,MASK,COUNT,SHARING,XORVAL=0x578,0x5aa,0x141e,0x848,0x144e,0x558,0x18b8
NAMES={a:n for n,a,_,_ in RANGES}
PROVIDERS=['th03_mainl.asm','ReC98.inc','th03/th03.inc','Tupfile.lua',
 'libs/master.lib/func.inc','libs/master.lib/func.hpp','libs/master.lib/master.inc',
 'libs/master.lib/macros.inc','libs/master.lib/super.inc','libs/master.lib/pal[data].asm',
 'libs/master.lib/pal[bss].asm','libs/master.lib/vs[data].asm','libs/master.lib/vs[bss].asm',
 'libs/master.lib/dos_ropen.asm','libs/master.lib/dos_ropen[data].asm']
PROVIDERS+=['libs/master.lib/'+n+'.asm' for n in ('bfnt_palette_set','palette_black_in',
 'palette_black_out','palette_show','palette_entry_rgb','vsync_wait','palette_white_in','palette_white_out')]


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[];returns={}
    for name,start,size,cleanup in RANGES:
        body=image[start:start+size]
        if len(body)!=size:raise ValueError('palette complete include body differs')
        ins=list(decoder.disasm(body,start));bounds={i.address for i in ins};edges=[]
        if not ins or sum(i.size for i in ins)!=size or (ins[-1].mnemonic,ins[-1].op_str)!=('retf',str(cleanup) if cleanup else ''):raise ValueError('palette complete body/far cleanup differs')
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf'):
                if (i.mnemonic,i.op_str)!=('retf',str(cleanup) if cleanup else ''):raise ValueError('palette interior return differs')
                returns[i.address]=cleanup
            if i.mnemonic in ('in','out'):
                sites=IN_PORTS if i.mnemonic=='in' else OUT_PORTS
                if i.address not in sites:raise ValueError('palette unknown port site')
                edges.append(dict(instruction=i.address,kind=i.mnemonic,port=sites[i.address]));continue
            if i.mnemonic=='int':
                if i.address not in DOS or i.bytes!=b'\xcd\x21':raise ValueError('palette unknown DOS site')
                edges.append(dict(instruction=i.address,kind='modeled-int21',ah=DOS[i.address]));continue
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('palette unknown indirect edge')
            if i.mnemonic=='lcall':raise ValueError('palette unknown far interface')
            dest=i.operands[0].imm
            if i.mnemonic=='call':
                if CALLS.get(i.address)!=dest:raise ValueError('palette unknown native call site/target')
                if not j or ins[j-1].bytes!=b'\x0e':raise ValueError('palette far call lacks PUSH CS')
            elif dest not in bounds:raise ValueError('palette branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=start,size=size,instructions=len(ins),sha256=sha(body),cleanup=cleanup,edges=edges))
    if any(image[a:a+1]!=bytes([v]) for a,v in ALIGNMENT.items()):raise ValueError('palette complete producer alignment differs')
    if image[0x1854:0x1858]!=b'\x2e\xa2\xb8\x18' or image[0x18b6:0x18b9]!=b'\x80\xf4\x00':raise ValueError('palette mutable CODE operand differs')
    return dict(bodies=rows,body_bytes=690,producer_bytes=2,complete_include_bytes=692,prior_dos_open_context=26,returns=returns,producers=ALIGNMENT,mutable_operand=XORVAL)


class PaletteProbe(Probe):
    def __init__(self,mz,s,observed=None):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x20000,0x2e3f0,0x40000
        self.s=s;self.errors=[];self.events=[];self.ports=[];self.native=Counter();self.stop=False;self.frames=[];self.direct=None;self.write_count=0;self.clock=[];self.poll=0;self.input_counts=Counter()
        self.returns=(observed or analyze(mz.program_image))['returns']
        self.uc.mem_write(0x50000,b'\xa5'*65536);self.uc.mem_write(0x50100,b'palette.rgb\0')
        self.uc.mem_write(0x50000+u16(s.get('header_offset',0x200)+5),bytes([s.get('color',0x80)]))
        for a,v in ((TONE,s.get('tone',100)),(NOTE,s.get('note',0)),(MASK,s.get('mask',0)),(COUNT,s.get('count',65535)),(SHARING,s.get('sharing',0xa500))):self.uc.mem_write(self.data+a,struct.pack('<H',v))
        self.uc.mem_write(self.data+PALETTE,bytes(s.get('palette',[(i*37+s.get('seed',11))&255 for i in range(48)])))
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2000:raise ValueError('palette terminal segment alias')
                if self.frames:raise ValueError('palette unfinished native frame')
                self.stop=True;uc.emu_stop();return
            off=address-self.code
            if self.get('CS')!=0x2000 or not any(a<=off<a+n for _,a,n,_ in RANGES):raise ValueError('CPU escaped palette bodies/segment alias')
            if off in NAMES:
                sp=self.get('SP');ip,cs=struct.unpack('<2H',uc.mem_read(self.stack+sp,4));direct=not self.frames and off==self.direct and ip==0xff00
                if cs!=0x2000 or (not direct and CALLS.get(ip-3)!=off):raise ValueError('palette native far frame differs')
                self.frames.append((sp,ip,cs,next(z for _,a,_,z in RANGES if a==off)));self.native[NAMES[off]]+=1
                if off==0x2064:self.poll=0;self.input_counts['wait']=0
            if off==0x2083:
                self.poll+=1
                if not s.get('stuck') and self.poll==s.get('ticks',3):
                    value=u16(struct.unpack('<H',uc.mem_read(self.data+COUNT,2))[0]+1);uc.mem_write(self.data+COUNT,struct.pack('<H',value));self.clock.append(value)
            if off in self.returns:
                if not self.frames:raise ValueError('palette orphan far return')
                sp,ip,cs,cleanup=self.frames.pop()
                if self.get('SP')!=sp or tuple(struct.unpack('<2H',uc.mem_read(self.stack+sp,4)))!=(ip,cs) or self.returns[off]!=cleanup:raise ValueError('palette native return frame differs')
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            allowed=(self.data+PALETTE<=address and address+size<=self.data+PALETTE+48 or self.data+TONE<=address and address+size<=self.data+TONE+2 or address==self.code+XORVAL and size==1 and value in (0,255))
            if not allowed:raise ValueError('palette write outside owned state/operand')
            self.write_count+=1
        def intr(uc,number,user):
            site=u16(self.get('IP')-2);ah=self.get('AH')
            if number!=0x21 or self.get('CS')!=0x2000 or DOS.get(site)!=ah:raise ValueError('palette unknown DOS request/site')
            if ah==0x3d:
                ax=s.get('open_ax',0x1234);cf=s.get('open_cf',0);event=dict(name='dos_open',site=site,mode=self.get('AL'),filename=[self.get('DX'),self.get('DS')])
            elif ah==0x3f:
                if self.get('DS')!=0x2e3f or self.get('DX')!=PALETTE or self.get('CX')!=48:raise ValueError('palette modeled read destination/count differs')
                payload=bytes(s.get('payload',list(range(48))))[:48];ax=s.get('read_ax',len(payload));cf=s.get('read_cf',0)
                if cf and not s.get('inject_on_failure'):payload=b''
                if payload:uc.mem_write(self.data+PALETTE,payload)
                event=dict(name='dos_read',site=site,handle=self.get('BX'),destination=[PALETTE,0x2e3f],size=48,payload_hex=payload.hex())
            else:ax=s.get('close_ax',7);cf=s.get('close_cf',1);event=dict(name='dos_close',site=site,handle=self.get('BX'))
            event.update(ax=ax,cf=cf);self.events.append(event);self.set('AX',ax);self.set('EFLAGS',(self.get('EFLAGS')&~1)|cf)
        def out(uc,port,width,value,user):
            site=self.get('IP')
            if self.get('CS')!=0x2000 or OUT_PORTS.get(site)!=port or width!=1:raise ValueError('palette unknown output port/site/width')
            self.ports.append(dict(site=site,kind='out',port=port,value=value))
        def inp(uc,port,width,user):
            site=self.get('IP')
            if self.get('CS')!=0x2000 or IN_PORTS.get(site)!=port or width!=1:raise ValueError('palette unknown input port/site/width')
            if port==0xa0:
                index=self.input_counts['wait'];self.input_counts['wait']+=1;pattern=s.get('port_pattern',[0x20,0,0,0x20]);value=pattern[index%len(pattern)]
            else:value=s.get('new_note',1) if port==0x871e else s.get('old_note',4)
            self.ports.append(dict(site=site,kind='in',port=port,value=value));return value
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(out),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)

    def run(self,name,args=(),budget=1000000):
        _,start,_,cleanup=next(r for r in RANGES if r[0]==name);self.direct=start;self.stop=False;self.errors.clear();self.frames.clear()
        for r,v in dict(CS=0x2000,DS=0x2e3f,SS=0x4000,ES=0x3333,AX=0x1111,BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,SP=0xffc0,EFLAGS=0x202|(0x400 if self.s.get('df') else 0)).items():self.set(r,v)
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2000,*args));self.uc.emu_start(self.code+start,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('palette terminal/budget differs')
        expected=dict(BP=0x7777,SI=0x1357,DI=0x2468,DS=0x2e3f,ES=0x3333)
        if self.get('SP')!=0xffc4+cleanup or any(self.get(r)!=v for r,v in expected.items()):raise ValueError('palette far cleanup/callee-saved differs')
        clear=name in ('show','black_in','black_out','white_in','white_out')
        if bool(self.get('EFLAGS')&0x400)!=(bool(self.s.get('df')) and not clear):raise ValueError('palette DF differs')


class Scalar:
    def __init__(self,p):
        self.mem=bytearray(p.uc.mem_read(0,0x100000));self.data=p.data;self.code=p.code;self.s=p.s;self.events=[];self.ports=[];self.clock=[];self.native=Counter()
    def word(self,a):return struct.unpack_from('<H',self.mem,a)[0]
    def get(self,a):return self.word(self.data+a)
    def put(self,a,v):struct.pack_into('<H',self.mem,self.data+a,u16(v))
    def port(self,site,kind,port,value):self.ports.append(dict(site=site,kind=kind,port=port,value=value))
    def dos_open(self):
        s=self.s;self.native['dos_open']+=1;ax=s.get('open_ax',0x1234);cf=s.get('open_cf',0)
        self.events.append(dict(name='dos_open',site=0xaba,mode=self.get(SHARING)&255,filename=[0x100,0x5000],ax=ax,cf=cf));return 65534 if cf else ax,cf
    def read(self,site,handle):
        s=self.s;payload=bytes(s.get('payload',list(range(48))))[:48];ax=s.get('read_ax',len(payload));cf=s.get('read_cf',0)
        if cf and not s.get('inject_on_failure'):payload=b''
        self.mem[self.data+PALETTE:self.data+PALETTE+len(payload)]=payload
        self.events.append(dict(name='dos_read',site=site,handle=handle,destination=[PALETTE,0x2e3f],size=48,payload_hex=payload.hex(),ax=ax,cf=cf));return cf
    def show(self):
        tone=self.get(TONE);tone=0 if tone>=32768 else min(tone,200);mask=15 if tone>100 else 0;factor=200-tone if mask else tone
        values=self.mem[self.data+PALETTE:self.data+PALETTE+48]
        if not self.get(NOTE):
            for n in range(16):
                self.port(0x1803,'out',0xa8,n)
                for value,site,port in zip(values[n*3:n*3+3],(0x1815,0x1821,0x182f),(0xac,0xaa,0xae)):
                    out=(((value>>4)^mask)*factor//100)^mask;self.port(site,'out',port,out)
            return
        new=self.s.get('new_note',1);self.port(0x1841,'out',0xf6,0xa0);self.port(0x1843,'in',0x871e,new)
        if new==255:
            old=self.s.get('old_note',4);self.port(0x184b,'in',0xae8e,old);bit=(old>>2)&1
        else:bit=new&1
        invert=255 if not bit else 0;self.mem[self.code+XORVAL]=invert
        for n in range(16):
            r,g,b=values[n*3:n*3+3];r=(r>>4)&mask;g>>=4;b&=mask
            r=((r^mask)*factor//100)^mask;g=((g^mask)*factor//100)^mask;b=((b^mask)*factor//100)^mask
            weighted=4*g+2*r+b+max(r,g,b);gray=max(((weighted*3//20)+1)//2-2,0)^invert
            self.port(0x1860,'out',0xa8,n)
            for shift,site,port in ((0,0x18bf,0xae),(1,0x18c7,0xac),(2,0x18cf,0xaa)):self.port(site,'out',port,15 if gray&(1<<shift) else 0)
    def wait(self):
        if self.get(MASK)&255:
            value=u16(self.get(COUNT)+1);self.put(COUNT,value);self.clock.append(value);return
        pattern=self.s.get('port_pattern',[0x20,0,0,0x20]);index=0
        for site,condition in ((0x206f,False),(0x2079,True)):
            for _ in range(10000):
                value=pattern[index%len(pattern)];index+=1;self.port(site,'in',0xa0,value)
                if bool(value&0x20)==condition:break
            else:raise ValueError('scalar palette wait budget')
    def run(self,name):
        s=self.s;self.native[name]+=1
        if name=='dos_open':self.native[name]-=1;return self.dos_open()
        if name=='show':self.show();return None,None
        if name=='wait':self.wait();return None,None
        if name=='bfnt':
            if not s.get('color',0x80)&128:return 65523,1
            cf=self.read(0x4df,0x1234)
            if cf:return 65523,1
            for n in range(16):
                at=self.data+PALETTE+n*3;b,r,g=self.mem[at:at+3];self.mem[at:at+3]=bytes([r,g,b])
            return 0,0
        if name=='rgb':
            ax,cf=self.dos_open()
            if cf:return ax,cf
            failed=self.read(0x1a83,ax)
            for i in range(48):at=self.data+PALETTE+i;v=self.mem[at];self.mem[at]=v|((v<<4)&255)
            closecf=s.get('close_cf',1);self.events.append(dict(name='dos_close',site=0x1a9c,handle=ax,ax=s.get('close_ax',7),cf=closecf))
            return (65523,1) if failed else (0,closecf)
        initial,delta,final={'black_in':(0,6,100),'black_out':(100,-6,0),'white_in':(200,-6,100),'white_out':(100,6,200)}[name]
        self.put(TONE,initial);self.run('wait');tone=initial;speed=s.get('speed',0);speed=speed if speed<32768 else 0
        while True:
            self.run('show')
            for _ in range(speed):self.run('wait')
            tone+=delta;self.put(TONE,tone)
            if delta>0 and tone>=final or delta<0 and tone<=final:break
        self.put(TONE,final);self.run('show');return None,None


def matrix(mz):
    rows=[]
    def observe(name,s,steps=None):
        p=PaletteProbe(mz,s);scalar=Scalar(p);before=sha(bytes(scalar.mem));results=[]
        for step in steps or [dict(function=name)]:
            fn=step['function']
            for key,at in (('tone',TONE),('note',NOTE)):
                if key in step:p.uc.mem_write(p.data+at,struct.pack('<H',step[key]));scalar.put(at,step[key])
            args=[]
            if fn=='bfnt':args=[s.get('header_offset',0x200),0x5000,0x1234]
            elif fn in ('rgb','dos_open'):args=[0x100,0x5000]
            elif fn in ('black_in','black_out','white_in','white_out'):args=[s.get('speed',0)]
            ax,cf=scalar.run(fn);p.run(fn,args)
            if (ax is not None and p.get('AX')!=ax) or (cf is not None and p.get('EFLAGS')&1!=cf) or p.events!=scalar.events or p.ports!=scalar.ports or p.clock!=scalar.clock or p.native!=scalar.native:raise ValueError('palette result/native/port/DOS/clock scalar differs: '+str((fn,s,step,p.get('AX'),ax,p.events,scalar.events,p.ports[:8],scalar.ports[:8])))
            actual=bytes(p.uc.mem_read(0,0x100000))
            if actual[:p.stack]!=scalar.mem[:p.stack] or actual[p.stack+65536:]!=scalar.mem[p.stack+65536:]:
                changed=[i for i,(a,b) in enumerate(zip(actual,scalar.mem)) if a!=b and not p.stack<=i<p.stack+65536]
                raise ValueError('palette full physical memory scalar differs: '+str((fn,s,step,changed[:20])))
            results.append(dict(function=fn,step=step,ax=ax,cf=cf,tone=scalar.get(TONE),count=scalar.get(COUNT),xor_operand=scalar.mem[p.code+XORVAL],df=bool(p.get('EFLAGS')&0x400)))
        rows.append(dict(function=name,scenario=s,steps=results,top_level_calls=len(results),native_entries=dict(p.native),events=p.events,ports=p.ports,clock=p.clock,write_count=p.write_count,memory_before_sha256=before,memory_after_sha256=sha(bytes(scalar.mem))))
    for df in (False,True):
        for note in (0,1):
            for tone in (0,1,6,50,99,100,101,150,199,200,201,32767,32768,65535):
                for detection in ((1,4),(0,0),(255,4),(255,0)) if note else ((1,4),):observe('show',dict(df=df,note=note,tone=tone,new_note=detection[0],old_note=detection[1]))
            for byte in range(256):
                for tone in (100,150):observe('show',dict(df=df,note=note,tone=tone,palette=[byte]*48))
        for color in (0,1,127,128,255):
            for length in (0,1,2,3,47,48):
                for cf in (0,1):observe('bfnt',dict(df=df,color=color,payload=list(range(length)),read_cf=cf,inject_on_failure=True,header_offset=65535))
        for open_cf in (0,1):
            for read_cf in (0,1):
                for close_cf in (0,1):
                    for length in (0,1,47,48):observe('rgb',dict(df=df,open_cf=open_cf,read_cf=read_cf,close_cf=close_cf,payload=list(range(length)),inject_on_failure=True))
        for ax in (0,1,47,48,65535):
            observe('bfnt',dict(df=df,read_ax=ax,payload=[0xff,0x12,0x34]))
            observe('rgb',dict(df=df,read_ax=ax,payload=[0xff,0x12,0x34],open_ax=0))
        for mask in (0,1,255,256,257,65535):
            for count in (0,65535):observe('wait',dict(df=df,mask=mask,count=count))
        for name in ('black_in','black_out','white_in','white_out'):
            for speed in (0,1,2,32768,65535):
                for note in (0,1):observe(name,dict(df=df,speed=speed,note=note,mask=1,count=65535))
        observe('load-show-chain',dict(df=df,close_cf=1),[dict(function='rgb'),dict(function='show',tone=150),dict(function='show',tone=100,note=1),dict(function='show',tone=100,note=0)])
    return rows


def nonterminal(mz):
    rows=[]
    for df in (False,True):
        for s in (dict(df=df,mask=1,stuck=True),dict(df=df,mask=0,port_pattern=[32]),dict(df=df,mask=0,port_pattern=[0])):
            p=PaletteProbe(mz,s);before=bytes(p.uc.mem_read(0,0x100000))
            try:p.run('wait',budget=1000)
            except ValueError as e:
                if str(e)!='palette terminal/budget differs':raise
            else:raise ValueError('palette stalled wait unexpectedly returned')
            actual=bytes(p.uc.mem_read(0,0x100000))
            if actual[:p.stack]!=before[:p.stack] or actual[p.stack+65536:]!=before[p.stack+65536:] or p.clock or p.events or dict(p.native)!={'wait':1}:raise ValueError('palette stalled wait changed state')
            site=0x2083 if s['mask'] else 0x206f if s['port_pattern']==[32] else 0x2079
            expected_ports=[] if s['mask'] else ([dict(site=0x206f,kind='in',port=0xa0,value=0)] if s['port_pattern']==[0] else [])
            expected_ports += [dict(site=site,kind='in',port=0xa0,value=s['port_pattern'][0]) for _ in range(len(p.ports)-len(expected_ports))] if not s['mask'] else []
            if p.ports!=expected_ports:raise ValueError('palette stalled wait port trace differs')
            rows.append(dict(function='wait',scenario=s,budget=1000,outcome='native-wait-budget',instruction=p.get('IP'),native_entries=dict(p.native),ports=p.ports,memory_before_sha256=sha(before)))
        s=dict(df=df,mask=1,speed=32767);p=PaletteProbe(mz,s);spec=Scalar(p);before=sha(bytes(spec.mem));spec.put(TONE,0);spec.show()
        try:p.run('black_in',[32767],budget=1000)
        except ValueError as e:
            if str(e)!='palette terminal/budget differs':raise
        else:raise ValueError('palette maximum speed unexpectedly completed budget')
        spec.put(COUNT,65535+len(p.clock));actual=bytes(p.uc.mem_read(0,0x100000))
        if actual[:p.stack]!=spec.mem[:p.stack] or actual[p.stack+65536:]!=spec.mem[p.stack+65536:] or p.ports!=spec.ports or p.events or p.native['show']!=1 or p.native['wait']<2 or p.get('EFLAGS')&0x400:raise ValueError('palette maximum-speed partial state differs')
        rows.append(dict(function='black_in',scenario=s,budget=1000,outcome='native-positive-speed-budget',instruction=p.get('IP'),native_entries=dict(p.native),ports=p.ports,clock=p.clock,memory_before_sha256=before))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('palette prior stack proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_palette.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('palette input changed: '+p)
    def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('memory_before_sha256','memory_after_sha256')} for row in cpu]
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];objects=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('palette invalid image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz),nonterminal=nonterminal(mz))
        if observations:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('palette complete body/CFG differs')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                expected=cached_provider(p,d)
                actual=cached.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else cached
                if actual!=expected:raise ValueError('palette cached frozen provider differs: '+p)
            op=str(tree/'obj/th03/mainl.obj');obj_data=(ROOT/op).read_bytes();inputs[op]=sha(obj_data);obj=describe_omf(obj_data)
            if not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0']:raise ValueError('palette cached root OMF identity differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments','record_count','record_counts')}
            if objects and obj['dependency_timestamp_normalized_sha256']!=objects[0]['dependency_timestamp_normalized_sha256']:raise ValueError('palette cached OMF differs beyond dependency timestamps')
            objects.append(observed['object']);maprows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));carrier=next(row for row in maprows if row['module']=='th03_mainl.asm' and row['segment']==0 and row['size'])
            if not all(carrier['start']<=a<a+n<=carrier['start']+carrier['size'] for _,a,n,_ in RANGES):raise ValueError('palette includes outside complete root carrier')
            observed['carrier']=carrier;target=parse_mz((ROOT/observations[0]['path']).read_bytes())
            extents=[('bfnt',0x4c6,64),('black-fades',0x536,130),('show',0x17d0,266),('rgb',0x1a68,66),('wait-white-fades',0x2064,166),('prior-dos-open',0xaae,26)]
            observed['comparisons']={n:extent_observation(target,mz,dict(start=a,size=z,segment=0,offset=a)) for n,a,z in extents}
            if any(not x['raw_slice_equal'] or not x['ordered_relocations_equal'] for x in observed['comparisons'].values()):raise ValueError('palette complete raw/ordered relocations differ')
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']) or normalized(observed['nonterminal'])!=normalized(observations[0]['nonterminal']):raise ValueError('palette target/cached CPU differs')
        observations.append(observed);print('Reviewed',path,len(observed['cpu']),'scenarios',len(observed['nonterminal']),'budgets',flush=True)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('palette canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('palette frozen provider changed')
    result=dict(kind='th03-mainl-complete-palette-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},build_scaffold_main_remaps=BUILD_REMAPS,observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL complete palettes/wait692bytes, native DOS-open26context and explicit device/clock/DOS:',args.output)


if __name__=='__main__':main()
