#!/usr/bin/env python3
"""Complete MAINL file includes and native DOS wrappers; scoped diagnostics only."""
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

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-mainl-pfint21-review-20261006.json'
PROOF_SHA256='f2943277c228adc1b193af46e1fd58a6cb9636e84ac46ad4d122ea70bebcb6cd'
RANGES=[('append',0x786,84,4),('flush',0x7da,107,0),('close',0x846,15,0),
 ('create',0x856,64,4),('exist',0x896,28,4),('read',0x8b2,180,6),
 ('open',0x966,59,4),('seek',0x9a2,52,6),('tell',0x9d6,14,0),
 ('size',0x9e4,14,0),('write',0x9f2,166,6),
 ('dos_axdx',0x6ae,23,6),('dos_size',0x6c6,55,2),('dos_open',0xaae,26,4)]
ALIGNMENT={0x845:0x90,0x855:0x90,0x9a1:0x90,0x6c5:0x90,0x6fd:0x90}
CALLS={0x7a0:0x6ae,0x847:0x7da,0x873:0x6ae,0x8a2:0xaae,0x97c:0xaae,0x9a3:0x7da,0x9e9:0x6c6}
DOS={0x7ca:{0x42},0x7f7:{0x40},0x83b:{0x42},0x84c:{0x3e},0x8aa:{0x3e},
 0x8e6:{0x3f},0x943:{0x3f},0x9b9:{0x42},0x9c4:{0x42},0xa43:{0x40},0xa75:{0x40},
 0x6b8:{0x3c,0x3d},0x6d3:{0x42},0x6e0:{0x42},0x6eb:{0x42},0xaba:{0x3d}}
PROVIDERS=['th03_mainl.asm','ReC98.inc','th03/th03.inc','libs/master.lib/master.inc',
 'libs/master.lib/macros.inc','libs/master.lib/func.hpp','libs/master.lib/super.inc',
 'libs/master.lib/fil[data].asm','libs/master.lib/fil[bss].asm',
 'libs/master.lib/dos_ropen[data].asm','libs/master.lib/dos_ropen.asm',
 'libs/master.lib/dos_axdx.asm','libs/master.lib/dos_filesize.asm']
PROVIDERS += ['libs/master.lib/file_'+n+'.asm' for n in ('append','close','create','exist','read','ropen','seek','size','write')]
BUFFER_SIZE,HANDLE,SHARING,BUFFER,POSITION,PTR,INBUF,EOF,ERROR=0x554,0x556,0x558,0x140a,0x140e,0x1412,0x1414,0x1416,0x1418
NAMES={a:n for n,a,_,_ in RANGES}


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[];returns={}
    for name,start,size,cleanup in RANGES:
        body=image[start:start+size]
        if len(body)!=size:raise ValueError('file complete body/cleanup differs')
        ins=list(decoder.disasm(body,start));bounds={i.address for i in ins}
        expected=('retf',str(cleanup) if cleanup else '')
        if not ins or sum(i.size for i in ins)!=size or (ins[-1].mnemonic,ins[-1].op_str)!=expected:raise ValueError('file complete body/cleanup differs')
        edges=[]
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf'):
                if (i.mnemonic,i.op_str)!=expected:raise ValueError('file interior return differs')
                returns[i.address]=cleanup
            if i.mnemonic in ('in','out'):raise ValueError('file unexpected port')
            if i.mnemonic=='int':
                if i.address not in DOS or i.bytes!=b'\xcd\x21':raise ValueError('file unknown DOS site')
                edges.append(dict(instruction=i.address,kind='modeled-int21',ah=sorted(DOS[i.address])));continue
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('file unknown indirect edge')
            if i.mnemonic=='lcall':raise ValueError('file unknown far interface')
            dest=i.operands[0].imm
            if i.mnemonic=='call':
                if CALLS.get(i.address)!=dest:raise ValueError('file unknown native call site/target')
                if not j or ins[j-1].bytes!=b'\x0e':raise ValueError('file far native call lacks PUSH CS')
            elif dest not in bounds:raise ValueError('file branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=start,size=size,instructions=len(ins),sha256=sha(body),cleanup=cleanup,edges=edges))
    if any(image[a:a+1]!=bytes([v]) for a,v in ALIGNMENT.items()):raise ValueError('file complete producer alignment differs')
    return dict(bodies=rows,file_body_bytes=783,file_producer_bytes=3,file_include_bytes=786,
                new_helper_body_bytes=78,new_helper_producer_bytes=2,prior_dos_open_context_bytes=26,returns=returns,producers=ALIGNMENT)


class FileProbe(Probe):
    """No MEM_READ hook; all file/DOS wrapper instructions and RETFs execute."""
    def __init__(self,mz,s,observed=None):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x20000,0x2e3f0,0x40000
        self.s=s;self.errors=[];self.events=[];self.native=Counter();self.stop=False;self.direct=None;self.frames=[];self.write_count=0
        self.returns=(observed or analyze(mz.program_image))['returns'];self.counts=Counter();self.cursor=s.get('cursor',3)
        for segment in (0x5000,0x6000,0x7000):self.uc.mem_write(segment*16,bytes((i*37+11)&255 for i in range(65536))+b'\xa5\x5a')
        self.uc.mem_write(0x50100,b'archive.dat\0')
        for a,v in [(BUFFER_SIZE,s.get('buffer_size',8)),(HANDLE,s.get('handle',0xffff)),(SHARING,s.get('sharing',0xa500)),(PTR,s.get('ptr',0)),(INBUF,s.get('inbuf',0)),(EOF,s.get('eof',0xbeef)),(ERROR,s.get('error',0xcafe))]:self.uc.mem_write(self.data+a,struct.pack('<H',v))
        self.uc.mem_write(self.data+BUFFER,struct.pack('<2H',s.get('buffer_offset',0x100),s.get('buffer_segment',0x6000)))
        self.uc.mem_write(self.data+POSITION,struct.pack('<I',s.get('position',0x1234fff0)))
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2000:raise ValueError('file terminal segment alias')
                if self.frames:raise ValueError('file unfinished native frame')
                self.stop=True;uc.emu_stop();return
            off=address-self.code
            if self.get('CS')!=0x2000 or not any(a<=off<a+n for _,a,n,_ in RANGES):raise ValueError('CPU escaped file bodies/segment alias')
            if off in NAMES:
                sp=self.get('SP');ip,cs=struct.unpack('<2H',uc.mem_read(self.stack+sp,4))
                direct=not self.frames and off==self.direct and ip==0xff00
                if cs!=0x2000 or (not direct and CALLS.get(ip-3)!=off):raise ValueError('file native far frame differs')
                self.frames.append((sp,ip,cs,next(z for _,a,_,z in RANGES if a==off)));self.native[NAMES[off]]+=1
            if off in self.returns:
                if not self.frames:raise ValueError('file orphan far return')
                sp,ip,cs,cleanup=self.frames.pop()
                if self.get('SP')!=sp or tuple(struct.unpack('<2H',uc.mem_read(self.stack+sp,4)))!=(ip,cs) or self.returns[off]!=cleanup:raise ValueError('file native return frame differs')
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            state=any(self.data+a<=address and address+size<=self.data+a+z for a,z in ((HANDLE,2),(POSITION,12)))
            spans=[(s.get('buffer_segment',0x6000)*16,65538)]
            client=s.get('client_segment',0x7000)
            if client!=0x2e3f:spans.append((client*16,65538))
            if not state and not any(a<=address and address+size<=a+z for a,z in spans):raise ValueError('file write outside owned state')
            self.write_count+=1
        def interrupt(uc,number,user):
            site=u16(self.get('IP')-2);ah=self.get('AH')
            if number!=0x21 or self.get('CS')!=0x2000 or ah not in DOS.get(site,set()):raise ValueError('file unknown DOS request/site')
            result,event=self.dos(site,ah)
            self.events.append(event);self.set('AX',result['ax']);self.set('EFLAGS',(self.get('EFLAGS')&~1)|result['cf'])
            if ah==0x42:self.set('DX',result['dx'])
        def out(uc,port,width,value,user):raise ValueError('file unexpected output port')
        def inp(uc,port,width,user):raise ValueError('file unexpected input port')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(interrupt))
        self.uc.hook_add(UC_HOOK_INSN,guard(out),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)

    def dos(self,site,ah):
        s=self.s;group='open' if ah in (0x3c,0x3d) else {0x3e:'close',0x3f:'read',0x40:'write',0x42:'seek'}[ah]
        i=self.counts[group];self.counts[group]+=1;items=s.get(group+'s',[]);item=items[i] if i<len(items) else {}
        cf=item.get('cf',s.get(group+'_cf',0));result={'cf':cf,'ax':0,'dx':0}
        event=dict(site=site,name='dos_'+group)
        if group=='open':
            result['ax']=item.get('ax',s.get('open_ax',0x1234));event.update(mode=self.get('AX'),filename=[self.get('DX'),self.get('DS')],attributes=self.get('CX') if ah==0x3c else None)
        elif group=='close':result['ax']=item.get('ax',s.get('close_ax',0));event['handle']=self.get('BX')
        elif group=='read':
            count=self.get('CX');segment=self.get('DS');off=self.get('DX');destination=segment*16+off
            if site==0x8e6 and (off,segment)!=struct.unpack('<2H',self.uc.mem_read(self.data+BUFFER,4)):raise ValueError('file buffer read destination differs')
            if site==0x943 and (off,segment)!=self.client:raise ValueError('file direct read destination differs')
            payload=bytes(item.get('data',s.get('stream',[1,2,3,4,5,6,7,8])[self.cursor:self.cursor+count]))[:count]
            if cf and not item.get('inject_on_failure'):payload=b''
            ax=item.get('ax',len(payload))
            if destination+len(payload)>0x100000:raise ValueError('file DOS read outside mapped fixture')
            if payload:self.uc.mem_write(destination,payload)
            if not cf:self.cursor+=ax
            result['ax']=ax;event.update(handle=self.get('BX'),size=count,destination=[off,segment],payload_sha256=sha(payload),payload_size=len(payload))
        elif group=='write':
            count=self.get('CX');off=self.get('DX');segment=self.get('DS')
            if site in (0x7f7,0xa43) and (off,segment)!=struct.unpack('<2H',self.uc.mem_read(self.data+BUFFER,4)):raise ValueError('file buffer write source differs')
            if site==0xa75 and (off,segment)!=self.client:raise ValueError('file direct write source differs')
            payload=bytes(self.uc.mem_read(segment*16+off,count));result['ax']=item.get('ax',count)
            if not cf:self.cursor+=result['ax']
            event.update(handle=self.get('BX'),size=count,source=[off,segment],payload_sha256=sha(payload))
        else:
            offset=(self.get('CX')<<16)|self.get('DX');mode=self.get('AL');signed=offset if offset<0x80000000 else offset-0x100000000
            if not cf:self.cursor=(offset if mode==0 else self.cursor+signed if mode==1 else s.get('file_size',13)+signed)&0xffffffff
            value=item.get('value',self.cursor if not cf else s.get('seek_error_value',0xdead0006));result['ax']=value&65535;result['dx']=value>>16
            event.update(handle=self.get('BX'),whence=mode,offset=offset)
        event.update(result);return result,event

    def run(self,name,step=None,budget=10000000):
        step=step or {};_,start,_,cleanup=next(r for r in RANGES if r[0]==name);self.direct=start;self.stop=False;self.errors.clear();self.frames.clear()
        for r,v in dict(CS=0x2000,DS=0x2e3f,SS=0x4000,ES=0x3333,AX=0x1111,BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,SP=0xffc0,EFLAGS=0x202|(0x400 if self.s.get('df') else 0)).items():self.set(r,v)
        self.client=(step.get('offset',self.s.get('client_offset',0x100)),self.s.get('client_segment',0x7000))
        args=[]
        if name in ('append','create','exist','open','dos_open'):args=[0x100,0x5000]
        if name in ('read','write'):args=[step.get('size',self.s.get('size',9)),*self.client]
        if name=='seek':args=[step.get('whence',self.s.get('whence',1)),step.get('position',self.s.get('seek_offset',7))&65535,step.get('position',self.s.get('seek_offset',7))>>16]
        if name=='dos_axdx':args=[0x100,0x5000,step.get('ax',0x3d02)]
        if name=='dos_size':args=[self.s.get('handle',0xffff)]
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2000,*args));self.uc.emu_start(self.code+start,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('file terminal/budget differs')
        if self.get('SP')!=0xffc4+cleanup or self.get('DS')!=0x2e3f or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]:raise ValueError('file far cleanup/callee-saved differs')
        if bool(self.get('EFLAGS')&0x400)!=bool(self.s.get('df')):raise ValueError('file DF differs')


class Scalar:
    """Independent physical-memory/file algorithm, with offset-only MOVS increments."""
    def __init__(self,p):
        self.mem=bytearray(p.uc.mem_read(0,0x100000));self.data=p.data;self.s=p.s
        self.events=[];self.native=Counter();self.counts=Counter();self.cursor=self.s.get('cursor',3)
    def word(self,a):return struct.unpack_from('<H',self.mem,a)[0]
    def w(self,a,v):struct.pack_into('<H',self.mem,a,u16(v))
    def get(self,a):return self.word(self.data+a)
    def put(self,a,v):self.w(self.data+a,v)
    def pos(self):return struct.unpack_from('<I',self.mem,self.data+POSITION)[0]
    def position(self,v):struct.pack_into('<I',self.mem,self.data+POSITION,v&0xffffffff)
    def buffer(self):return self.get(BUFFER),self.get(BUFFER+2)
    def transfer(self,source,dest,count):
        si,ds=source;di,es=dest;delta=-1 if self.s.get('df') else 1
        for _ in range(count//2):
            chunk=bytes(self.mem[ds*16+si:ds*16+si+2]);self.mem[es*16+di:es*16+di+2]=chunk
            si=u16(si+delta*2);di=u16(di+delta*2)
        if count&1:self.mem[es*16+di]=self.mem[ds*16+si];si=u16(si+delta);di=u16(di+delta)
        return si,di
    def dos(self,site,group,*,handle=0,mode=0,offset=0,pointer=(0,0),count=0,attributes=None):
        s=self.s;i=self.counts[group];self.counts[group]+=1;items=s.get(group+'s',[]);item=items[i] if i<len(items) else {}
        cf=item.get('cf',s.get(group+'_cf',0));ax=dx=0;event=dict(site=site,name='dos_'+group)
        if group=='open':ax=item.get('ax',s.get('open_ax',0x1234));event.update(mode=mode,filename=list(pointer),attributes=attributes)
        elif group=='close':ax=item.get('ax',s.get('close_ax',0));event['handle']=handle
        elif group=='read':
            payload=bytes(item.get('data',s.get('stream',[1,2,3,4,5,6,7,8])[self.cursor:self.cursor+count]))[:count]
            if cf and not item.get('inject_on_failure'):payload=b''
            ax=item.get('ax',len(payload));address=pointer[1]*16+pointer[0];self.mem[address:address+len(payload)]=payload
            if not cf:self.cursor+=ax
            event.update(handle=handle,size=count,destination=list(pointer),payload_sha256=sha(payload),payload_size=len(payload))
        elif group=='write':
            address=pointer[1]*16+pointer[0];payload=bytes(self.mem[address:address+count]);ax=item.get('ax',count)
            if not cf:self.cursor+=ax
            event.update(handle=handle,size=count,source=list(pointer),payload_sha256=sha(payload))
        else:
            signed=offset if offset<0x80000000 else offset-0x100000000
            if not cf:self.cursor=(offset if mode==0 else self.cursor+signed if mode==1 else s.get('file_size',13)+signed)&0xffffffff
            value=item.get('value',self.cursor if not cf else s.get('seek_error_value',0xdead0006));ax=value&65535;dx=value>>16
            event.update(handle=handle,whence=mode,offset=offset)
        event.update(ax=ax,dx=dx,cf=cf);self.events.append(event);return ax,dx,cf
    def clear(self):
        for a in (INBUF,PTR,EOF,ERROR):self.put(a,0)
        self.position(0)
    def run(self,name,step=None):
        step=step or {};s=self.s;self.native[name]+=1;handle=self.get(HANDLE)
        client=(step.get('offset',s.get('client_offset',0x100)),s.get('client_segment',0x7000));size=step.get('size',s.get('size',9))
        if name=='dos_open':
            ax,_,cf=self.dos(0xaba,'open',mode=0x3d00|(self.get(SHARING)&255),pointer=(0x100,0x5000));return (65534 if cf else ax),None
        if name=='dos_axdx':
            val=step.get('ax',0x3d02);ax,_,cf=self.dos(0x6b8,'open',mode=val,pointer=(0x100,0x5000),attributes=0x20 if val>>8==0x3c else None)
            return u16(-ax) if cf else ax,65535 if cf else 0
        if name in ('append','create','open'):
            if handle!=65535:return 0,None
            if name=='open':
                ax,_=self.run('dos_open');cf=self.events[-1]['cf'];dx=65535 if cf else 0
            else:
                ax,dx=self.run('dos_axdx',dict(ax=0x3d02 if name=='append' else 0x3c00))
            self.put(HANDLE,ax|dx);self.clear();failed=dx==65535
            if name=='append' and dx==0:
                ax,dx,_=self.dos(0x7ca,'seek',handle=self.get(HANDLE),mode=2);self.position((dx<<16)|ax)
            return (0 if failed else 1),None
        if name=='exist':
            ax,_=self.run('dos_open');cf=self.events[-1]['cf']
            if not cf:_,_,cf=self.dos(0x8aa,'close',handle=ax)
            return 0 if cf else 1,None
        if name=='flush':
            if handle==65535:return None,None
            ptr=self.get(PTR);inbuf=self.get(INBUF)
            if inbuf<ptr:
                ax,_,cf=self.dos(0x7f7,'write',handle=handle,pointer=self.buffer(),count=ptr)
                if not cf:self.position(self.pos()+ax)
                if cf or self.get(PTR)!=ax:self.put(ERROR,1)
                self.put(PTR,0)
            elif inbuf:
                request=(self.pos()+ptr)&0xffffffff;self.put(INBUF,0);self.put(PTR,0)
                ax,dx,_=self.dos(0x83b,'seek',handle=handle,offset=request);self.position((dx<<16)|ax)
            return None,None
        if name=='close':
            self.run('flush');self.dos(0x84c,'close',handle=self.get(HANDLE));self.put(HANDLE,65535);return None,None
        if name=='tell':v=(self.pos()+self.get(PTR))&0xffffffff;return v&65535,v>>16
        if name=='seek':
            self.run('flush')
            if handle!=65535:
                self.dos(0x9b9,'seek',handle=handle,mode=step.get('whence',s.get('whence',1))&255,offset=step.get('position',s.get('seek_offset',7)))
                ax,dx,_=self.dos(0x9c4,'seek',handle=handle,mode=1);self.put(EOF,0);self.position((dx<<16)|ax)
            return None,None
        if name=='dos_size':
            ax,dx,cf=self.dos(0x6d3,'seek',handle=handle,mode=1)
            if cf:return u16(-ax),65535 if ax else 0
            original=(dx<<16)|ax
            ax,dx,_=self.dos(0x6e0,'seek',handle=handle,mode=2)
            self.dos(0x6eb,'seek',handle=handle,offset=original);return ax,dx
        if name=='size':
            ax,dx=self.run('dos_size')
            # The wrapper branches on final CF, including failed restore and NEG(0).
            if self.events[-1]['cf'] and (self.events[-1]['site']!=0x6d3 or self.events[-1]['ax']):ax=dx
            return ax,dx
        if name=='read':
            if not self.get(BUFFER_SIZE):
                ax,_,_=self.dos(0x943,'read',handle=handle,pointer=client,count=size);self.position(self.pos()+ax)
                if u16(size-ax):self.put(EOF,1)
                return ax,None
            rest=size;di,es=client
            for _ in range(65537):
                count=self.get(INBUF)
                if self.get(PTR)>=count:
                    self.position(self.pos()+count)
                    ax,_,cf=self.dos(0x8e6,'read',handle=self.get(HANDLE),pointer=self.buffer(),count=self.get(BUFFER_SIZE));count=0 if cf else ax
                    self.put(INBUF,count)
                    if not count:self.put(EOF,1);return u16(size-rest),None
                    self.put(PTR,0)
                count=min(u16(self.get(INBUF)-self.get(PTR)),rest)
                if (es or di) and count:
                    off,seg=self.buffer();_,di=self.transfer((u16(off+self.get(PTR)),seg),(di,es),count)
                self.put(PTR,self.get(PTR)+count);rest=u16(rest-count)
                if not rest:return u16(size-rest),None
            raise ValueError('scalar file read budget')
        if name=='write':
            if not self.get(BUFFER_SIZE):
                ax,_,cf=self.dos(0xa75,'write',handle=handle,pointer=client,count=size)
                if cf:self.put(ERROR,1);ax=0
                self.position(self.pos()+ax);return 65535 if ax else 0,None
            rest=size;si,ds=client
            for _ in range(65537):
                available=u16(self.get(BUFFER_SIZE)-self.get(PTR));full=available<rest;count=available if full else rest
                off,seg=self.buffer();dest=(u16(off+self.get(PTR)),seg);rest=u16(rest-count);self.put(PTR,self.get(PTR)+count)
                si,_=self.transfer((si,ds),dest,count)
                if full:
                    ax,_,cf=self.dos(0xa43,'write',handle=self.get(HANDLE),pointer=self.buffer(),count=self.get(BUFFER_SIZE))
                    if cf or self.get(BUFFER_SIZE)!=ax:self.put(ERROR,1);return 0,None
                    self.put(PTR,0);self.position(self.pos()+ax)
                if not rest:return 1,None
            raise ValueError('scalar file write budget')
        raise ValueError('scalar unowned file entry')


def matrix(mz):
    rows=[]
    def observe(name,s,steps=None):
        p=FileProbe(mz,s);scalar=Scalar(p);before=sha(bytes(scalar.mem));results=[]
        for step in steps or [dict(function=name)]:
            fn=step['function'];ax,dx=scalar.run(fn,step);p.run(fn,step)
            if (ax is not None and p.get('AX')!=ax) or (dx is not None and p.get('DX')!=dx) or p.events!=scalar.events or p.native!=scalar.native or p.cursor!=scalar.cursor:raise ValueError('file result/native/DOS scalar differs: '+str((fn,s,step,p.get('AX'),ax,p.get('DX'),dx,p.events,scalar.events)))
            actual=bytes(p.uc.mem_read(0,0x100000))
            if actual[:p.stack]!=scalar.mem[:p.stack] or actual[p.stack+65536:]!=scalar.mem[p.stack+65536:]:
                changed=[i for i,(a,b) in enumerate(zip(actual,scalar.mem)) if a!=b and not p.stack<=i<p.stack+65536]
                raise ValueError('file full physical memory scalar differs: '+str((fn,s,step,changed[:20])))
            results.append(dict(function=fn,step=step,ax=ax,dx=dx,carry=p.get('EFLAGS')&1,position=scalar.pos(),ptr=scalar.get(PTR),inbuf=scalar.get(INBUF),eof=scalar.get(EOF),error=scalar.get(ERROR)))
        rows.append(dict(function=name,scenario=s,steps=results,top_level_calls=len(results),events=p.events,native_entries=dict(p.native),write_count=p.write_count,memory_before_sha256=before,memory_after_sha256=sha(bytes(scalar.mem)),cursor=p.cursor))
    for df in (False,True):
        for name in ('append','create','open'):
            for handle in (0,1,32768,65535):
                for ax in (0,1,5,65535):
                    for cf in (0,1):observe(name,dict(df=df,handle=handle,open_ax=ax,open_cf=cf))
        for cf in (0,1):
            for close_cf in (0,1):observe('exist',dict(df=df,open_cf=cf,close_cf=close_cf))
        for handle in (0,65535):
            for ptr,inbuf in ((0,0),(0,8),(3,8),(8,8),(9,8),(8,0),(65535,1)):
                for cf in (0,1):
                    for name in ('flush','close','seek'):observe(name,dict(df=df,handle=handle,ptr=ptr,inbuf=inbuf,write_cf=cf,seek_cf=cf))
        for ptr in (0,1,65535):
            for pos in (0,65535,0xffffffff):observe('tell',dict(df=df,ptr=ptr,position=pos))
        for name in ('size','dos_size'):
            for failures in ((0,0,0),(1,0,0),(0,1,0),(0,0,1),(0,1,1)):
                for error_ax in (0,6,65535):observe(name,dict(df=df,seeks=[dict(cf=failures[0],value=error_ax if failures[0] else 0x12345678),dict(cf=failures[1],value=0x9abc0006),dict(cf=failures[2])]))
        for whence in (0,1,2,127,255,256,65535):
            for offset in (0,1,65535,65536,0x80000000,0xffffffff):observe('seek',dict(df=df,handle=1,whence=whence,seek_offset=offset))
        for name in ('read','write'):
            for buffer_size in (0,1,2,8):
                for size in (0,1,2,7,8,9,17,32768,65535):
                    for cf in (0,1):observe(name,dict(df=df,buffer_size=buffer_size,size=size,read_cf=cf,write_cf=cf,cursor=0))
            for ptr,inbuf in ((0,8),(1,8),(7,8),(8,8),(9,8),(65535,8)):
                for size in (0,1,8,9):observe(name,dict(df=df,ptr=ptr,inbuf=inbuf,size=size,cursor=0))
            for segment,off in ((0,0),(0x7000,0xffff),(0x7000,0xfffe),(0x6000,0x100),(0x6000,0x102),(0x6000,0x101)):
                observe(name,dict(df=df,client_segment=segment,client_offset=off,size=9,cursor=0))
            for cf in (0,1):
                for ax in (0,1,2,7,8,9,65535):
                    observe(name,dict(df=df,buffer_size=0,size=8,reads=[dict(cf=cf,ax=ax,data=[91,92])],writes=[dict(cf=cf,ax=ax)],cursor=0))
                    observe(name,dict(df=df,buffer_size=8,size=9,reads=[dict(cf=cf,ax=ax,data=[91,92],inject_on_failure=True)],writes=[dict(cf=cf,ax=ax)],cursor=0))
        for byte in range(256):
            observe('read',dict(df=df,size=1,cursor=0,stream=[byte]))
            observe('write',dict(df=df,size=1,client_offset=byte))
        for size in (0,1,8,9):observe('read',dict(df=df,client_segment=0,client_offset=0,size=size,cursor=0))
        for offset in (PTR,INBUF,EOF,ERROR,HANDLE):
            # Small declared field aliases; no arbitrary overwrite of buffer far pointers.
            if not df:observe('read',dict(df=df,client_segment=0x2e3f,client_offset=offset,size=2,cursor=0))
        observe('read-chain',dict(df=df,handle=65535,cursor=0),[dict(function='open'),dict(function='read',size=3),dict(function='tell'),dict(function='read',size=0),dict(function='seek',position=0,whence=0),dict(function='read',size=9),dict(function='close')])
        observe('write-chain',dict(df=df,handle=65535,cursor=0),[dict(function='create'),dict(function='write',size=9),dict(function='tell'),dict(function='flush'),dict(function='size'),dict(function='close')])
        observe('append-chain',dict(df=df,handle=65535),[dict(function='append'),dict(function='write',size=8),dict(function='flush'),dict(function='close')])
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('file prior hook proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_file.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('file input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];objects=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('file invalid image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz))
        if observations:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('file complete body/CFG differs')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                expected=d.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else d
                actual=cached.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else cached
                if actual!=expected:raise ValueError('file cached frozen provider differs: '+p)
            op=str(tree/'obj/th03/mainl.obj');obj_data=(ROOT/op).read_bytes();inputs[op]=sha(obj_data);obj=describe_omf(obj_data)
            if not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0']:raise ValueError('file cached root OMF identity differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments','record_count','record_counts')}
            if objects and obj['dependency_timestamp_normalized_sha256']!=objects[0]['dependency_timestamp_normalized_sha256']:raise ValueError('file cached OMF differs beyond dependency timestamps')
            objects.append(observed['object']);maprows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));carrier=next(row for row in maprows if row['module']=='th03_mainl.asm' and row['segment']==0 and row['size'])
            if not all(carrier['start']<=a<a+n<=carrier['start']+carrier['size'] for _,a,n,_ in RANGES):raise ValueError('file includes outside complete root carrier')
            observed['carrier']=carrier;target=parse_mz((ROOT/observations[0]['path']).read_bytes())
            extents=[('file-includes',0x786,786),('dos-axdx-size',0x6ae,80),('prior-dos-open-context',0xaae,26)]
            observed['comparisons']={n:extent_observation(target,mz,dict(start=a,size=z,segment=0,offset=a)) for n,a,z in extents}
            if any(not x['raw_slice_equal'] or not x['ordered_relocations_equal'] for x in observed['comparisons'].values()):raise ValueError('file complete raw/ordered relocations differ')
            def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('memory_before_sha256','memory_after_sha256')} for row in cpu]
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']):raise ValueError('file target/cached CPU differs')
        observations.append(observed);print('Reviewed',path,len(observed['cpu']),'scenarios',flush=True)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('file canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('file frozen provider changed')
    result=dict(kind='th03-mainl-complete-file-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL complete file786/native helper80/context26 bytes with explicit DOS:',args.output)


if __name__=='__main__':main()
