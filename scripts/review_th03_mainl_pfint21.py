#!/usr/bin/env python3
"""Complete MAINL archive INT21 hook and connected native archive/buffer callers."""
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
import review_th03_mainl_buffer as bf
import review_th03_mainl_pfread as pf
import review_th03_mainl_pfopen as op

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-mainl-buffer-review-20261006.json'
PROOF_SHA256='87de65dc0b936f5e57a016164fd9be4a7f571a9463c8a97e2204010cfeb90cae'
ORG,ACTIVE,PAR,FILE,HANDLE,ENTRIES=0x2850,0x2854,0x1c82,0x1d02,0x1d04,0x1d06
OWN=[('start',0x2856,188),('end',0x2912,56),('hook-entry',0x294a,56),('hook-main',0x29b2,198),('hook-tail',0x2a7a,51)]
TABLE=[(0x3d,0x29b2),(0x3e,0x29e7),(0x3f,0x2a05),(0x42,0x2a19),(0x46,0x2a7a),
 (0x40,0x2a7e),(0x45,0x2a7e),(0x4c,0x2a5c),(0x57,0x2a7e),(0x5c,0x2a7e),(0x44,0x2a68),(0,0x2a82)]
FILE_MODELS={0x966:('file_open',4),0x8b2:('file_read',6),0x846:('file_close',0)}
HEAP={0x21ae:('allocate',2),0x22b2:('free',2)}
NATIVE=[('buffer_'+n,a,z,k) for n,a,z,k in bf.RANGES]+[('archive_'+n,a,z,int(k or '0')) for n,a,z,_,k in pf.RANGES]+[('archive_open',0x2b16,281,8),('compare',0x2c30,56,8)]
PROVIDERS=list(dict.fromkeys(bf.PROVIDERS+pf.PROVIDERS+op.PROVIDERS+['libs/master.lib/pfint21[bss].asm','libs/master.lib/file_ropen.asm','libs/master.lib/file_read.asm','libs/master.lib/file_close.asm']))
LOCAL=['src/main/formats/pfopen.inl','src/main/formats/pfopen.hpp']


def analyze(image):
    contexts=dict(buffer=bf.analyze(image),archive=pf.analyze(image),open=op.analyze(image))
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[];instructions=[]
    for name,a,z in OWN:
        body=image[a:a+z]
        if len(body)!=z:raise ValueError('hook complete CODE range differs')
        ins=list(decoder.disasm(body,a))
        if sum(i.size for i in ins)!=z:raise ValueError('hook complete instruction partition differs')
        rows.append(dict(name=name,offset=a,size=z,instructions=len(ins),sha256=sha(body)));instructions+=ins
    bounds={i.address for i in instructions};native={a for _,a,_,_ in NATIVE};allowed_calls=native|set(FILE_MODELS)|set(HEAP)
    if image[0x2982:0x29b2]!=b''.join(struct.pack('<2H',*x) for x in TABLE) or image[0x2a78:0x2a7a]!=struct.pack('<H',0x14cf):raise ValueError('hook complete dispatch/IOCTL table differs')
    if image[ORG:0x2856]!=b'\0'*5+b'\x90' or image[0x2aad:0x2aae]!=b'\0':raise ValueError('hook CS state/alignment or excluded root byte differs')
    edges=[];returns={}
    all_native_ins=[]
    for _,a,z,_ in NATIVE:all_native_ins+=list(decoder.disasm(image[a:a+z],a))
    for i in instructions+all_native_ins:
        if i.mnemonic=='call' and i.operands and all(o.type==X86_OP_IMM for o in i.operands):returns.setdefault(i.operands[0].imm,set()).add(i.address+i.size)
    for site,(_,destinations) in pf.INDIRECT.items():
        for dest in destinations:returns.setdefault(dest,set()).add(site+5)
    for j,i in enumerate(instructions):
        if i.mnemonic in ('in','out'):raise ValueError('hook unexpected port')
        if i.mnemonic=='int':
            if i.address not in (0x28c5,0x28e6,0x2926,0x2a64) or i.bytes!=b'\xcd\x21':raise ValueError('hook unknown vector interrupt site')
        if i.mnemonic=='retf' and (i.address,i.op_str) not in ((0x290f,'4'),(0x2949,'')):raise ValueError('hook far cleanup differs')
        if i.mnemonic=='iret' and i.address!=0x2aac:raise ValueError('hook unknown IRET')
        if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
        if i.address in (0x2952,0x2a8f):
            if i.bytes!=b'\x2e\xff\x2e\x50\x28':raise ValueError('hook saved-vector far jump differs')
            edges.append(dict(instruction=i.address,kind='saved-vector-far-jump'));continue
        if i.address==0x297e:
            if i.bytes!=b'\x2e\xff\x64\x02':raise ValueError('hook native dispatch operand differs')
            edges.append(dict(instruction=i.address,kind='checked-dispatch'));continue
        if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('hook unknown indirect edge')
        if i.mnemonic in ('lcall','ljmp'):raise ValueError('hook unknown far edge')
        dest=i.operands[0].imm
        if i.mnemonic=='call':
            if dest not in allowed_calls or not j or instructions[j-1].bytes!=b'\x0e':raise ValueError('hook far call/PUSH CS differs')
        elif dest not in bounds:raise ValueError('hook branch enters data/operand/neighbor')
        edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
    if image[0x290f:0x2912]!=b'\xca\x04\0' or image[0x2949:0x294a]!=b'\xcb' or image[0x2aac:0x2aad]!=b'\xcf':raise ValueError('hook terminal return differs')
    return dict(code=rows,code_bytes=549,table_bytes=50,cs_state_bytes=5,alignment_bytes=1,complete_include_bytes=605,excluded_root_byte=0x2aad,edges=edges,far_returns={str(k):sorted(v) for k,v in returns.items()},contexts=contexts)


def encode(data,key):
    out=[]
    for value in data:out.append(value^key);key=(key-value)&255
    return bytes(out)


class HookProbe(Probe):
    """Native installation/dispatcher/archive/buffers; DOS and heap remain models."""
    def __init__(self,mz,s,observed=None):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x20000,0x2e3f0,0x40000
        self.s=s;self.stop=False;self.errors=[];self.events=[];self.writes=[];self.native=Counter();self.cursor=0;self.read_calls=0;self.direct=None
        self.frames=(observed or analyze(mz.program_image))['far_returns'];self.models={**FILE_MODELS,**HEAP};self.starts={a:n for n,a,_,_ in NATIVE};self.write_count=0
        self.name=(b'A'*s['name_length'] if 'name_length' in s else b'arc.par')+b'\0';self.directory=s.get('directory',op.header(packed=len(s.get('payload',[])),original=s.get('original',9),offset=s.get('home',0))+bytes(32))
        self.directory=bytes(self.directory);self.header=struct.pack('<4H8s',s.get('entries_size',len(self.directory)),0x3456,0xffff,s.get('key',0xa5),b'\0'*8)
        self.uc.mem_write(0x50000,b'A'*65536);self.uc.mem_write(0x50100,self.name)
        self.uc.mem_write(0x62000,b'\xa5'*65536);self.uc.mem_write(0x60000,b'\xa5'*16);self.uc.mem_write(0x61000,b'\xa5'*31);self.uc.mem_write(0x80000,b'\xa5'*65536)
        self.uc.mem_write(0x70000,b'\xa5'*65536);self.uc.mem_write(0x70100,b'NAME.DAT\0');self.uc.mem_write(0x90100,b'\xcf')
        self.uc.mem_write(self.data+bf.BBUFSIZ,struct.pack('<H',s.get('buffer_size',2)));self.uc.mem_write(self.data+bf.ERR,b'\xef\xbe');self.uc.mem_write(self.data+bf.ALLOC_ID,b'\x00\x02')
        self.uc.mem_write(self.data+PAR,b'arc.par\0');self.uc.mem_write(self.data+FILE,struct.pack('<3H',0,65535,0x8000))
        self.uc.mem_write(self.code+ORG,struct.pack('<2HB',0x100 if s.get('installed') else 0,0x9000 if s.get('installed') else 0,s.get('active',0)))
        if s.get('installed'):self.uc.mem_write(0x80000,self.directory)
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2000:raise ValueError('hook terminal segment alias')
                self.stop=True;uc.emu_stop();return
            if address==0x90100:
                if self.get('CS')!=0x9000:raise ValueError('hook old-kernel segment alias')
                if self.direct!='hook' or self.get('SP')!=0xffc0:raise ValueError('hook old-kernel stack/entry differs')
                sp=self.get('SP');ip,cs,flags=struct.unpack('<3H',uc.mem_read(self.stack+sp,6))
                if (ip,cs)!=(0xff00,0x2000):raise ValueError('hook old-kernel interrupt frame differs')
                self.events.append(dict(name='old_dos',ax=self.get('AX'),bx=self.get('BX'),cx=self.get('CX'),dx=self.get('DX'),ds=self.get('DS'),live_if=bool(self.get('EFLAGS')&0x200)))
                self.set('AX',s.get('old_ax',0xbeef));self.set('DX',s.get('old_dx',0xcafe));uc.mem_write(self.stack+sp+4,struct.pack('<H',(flags&~1)|s.get('old_cf',1)));return
            off=address-self.code
            if off in self.models:
                if self.get('CS')!=0x2000:raise ValueError('hook model segment alias')
                name,cleanup=self.models[off];sp=self.get('SP');frame=list(struct.unpack('<'+'H'*(2+cleanup//2),uc.mem_read(self.stack+sp,4+cleanup)))
                if frame[1]!=0x2000 or frame[0] not in self.frames.get(str(off),[]):raise ValueError('hook modeled far frame differs')
                args=frame[2:];ax=s.get('model_ax',0xf00d);cf=s.get('model_cf',1);payload=b''
                if name=='allocate':
                    owner='header' if frame[0]==0x287a else 'directory' if frame[0]==0x289d else 'pfile' if frame[0]==0x2b28 else 'buffer'
                    ax={'header':0x6000,'directory':0x8000,'pfile':0x6100,'buffer':0x6200}[owner];cf=s.get(owner+'_cf',0)
                    ax=s.get(owner+'_segment',ax);self.events.append(dict(name=name,owner=owner,args=args,ax=ax,cf=cf,id=self.word(bf.ALLOC_ID)))
                else:
                    if name in ('file_open','file_close'):
                        ax=s.get(name+'_ax',1 if name=='file_open' else 0);cf=s.get(name+'_cf',0)
                    if name=='file_read':
                        payload=self.header if frame[0]==0x2885 else encode(self.directory,s.get('key',0xa5)&255)
                        if s.get('short_header') and frame[0]==0x2885:payload=payload[:s['short_header']]
                        payload=payload[:args[0]];uc.mem_write(args[2]*16+args[1],payload);ax=s.get('file_read_ax',len(payload));cf=s.get('file_read_cf',0)
                    self.events.append(dict(name=name,args=args,ax=ax,cf=cf,payload_hex=payload.hex()))
                self.set('AX',ax);self.set('EFLAGS',(self.get('EFLAGS')&~1)|cf);self.set('SP',sp+4+cleanup);self.set('CS',frame[1]);self.set('IP',frame[0]);return
            if self.get('CS')!=0x2000 or not (any(a<=off<a+z for _,a,z in OWN) or any(a<=off<a+z for _,a,z,_ in NATIVE)):raise ValueError('CPU escaped hook/native contexts')
            if off in self.starts:
                self.native[self.starts[off]]+=1
                if off in (0x1904,0x1952,0x1996,0x2c30):
                    ip=struct.unpack('<H',uc.mem_read(self.stack+self.get('SP'),2))[0]
                    if ip not in self.frames.get(str(off),[]):raise ValueError('hook native near frame differs')
                    if off!=0x2c30 and self.get('ES')!=0x6100:raise ValueError('hook native near segment differs')
                else:
                    sp=self.get('SP');ip,cs=struct.unpack('<2H',uc.mem_read(self.stack+sp,4))
                    if cs!=0x2000 or (ip not in self.frames.get(str(off),[]) and not(self.direct==self.starts[off] and ip==0xff00)):raise ValueError('hook native far frame differs')
            if off in pf.INDIRECT:
                field,allowed=pf.INDIRECT[off];segment=self.get('ES');dest=struct.unpack('<H',uc.mem_read(segment*16+field,2))[0]
                if segment!=0x6100 or dest not in allowed:raise ValueError('hook native archive pointer differs')
            if off==0x297e:
                index=self.get('SI')
                if index not in range(0x2982,0x29b2,4):raise ValueError('hook dispatch index differs')
                dest=struct.unpack('<H',uc.mem_read(self.code+index+2,2))[0]
                if dest!=TABLE[(index-0x2982)//4][1]:raise ValueError('hook dispatch target differs')
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            data_ranges=[(self.data+PAR,max(128,len(self.name))),(self.data+FILE,6),(self.data+bf.ERR,2),(self.data+bf.ALLOC_ID,2)]
            allowed=(any(a<=address and address+size<=a+z for a,z in data_ranges) or any(a<=address and address+size<=a+z for a,z in [(0x61000,31),(0x62000,8),(0x70000,65536),(0x80000,65536),(self.code+ORG,5),(self.code+0x29ae,1)]))
            if not allowed:raise ValueError('hook write outside owned state')
            self.write_count+=1
            if len(self.writes)<2048:self.writes.append([address,size,value])
        def intr(uc,number,user):
            site=u16(self.get('IP')-2);ah=self.get('AH')
            if number!=0x21 or self.get('CS')!=0x2000:raise ValueError('hook unexpected interrupt')
            ax=self.get('AX');cf=s.get('dos_cf',0);event={}
            if site in (0x28c5,0x28e6,0x2926,0x2a64):
                expected=0x35 if site==0x28c5 else 0x25
                if (ah,self.get('AL'))!=(expected,0x21):raise ValueError('hook vector DOS request differs')
                if ah==0x35:self.set('BX',0x100);self.set('ES',0x9000);event=dict(name='get_vector',number=0x21)
                else:event=dict(name='set_vector',number=0x21,pointer=[self.get('DX'),self.get('DS')])
                self.events.append(event);return
            if bf.DOS.get(site)!=ah:raise ValueError('hook unknown native DOS site')
            if ah==0x3d:
                ax=s.get('open_handle',0x1234);cf=s.get('open_cf',0);event=dict(name='dos_open',mode=self.get('AL'),filename=[self.get('DX'),self.get('DS')])
            elif ah==0x3e:event=dict(name='dos_close',handle=self.get('BX'));ax=s.get('close_ax',0xabcd)
            elif ah==0x3f:
                count=self.get('CX');payload=bytes(s.get('payload',[]))[self.cursor:self.cursor+count];self.cursor+=len(payload);self.read_calls+=1
                if self.get('DS')!=0x6200 or self.get('DX')!=8:raise ValueError('hook buffer read destination differs')
                uc.mem_write(0x62008,payload);ax=s.get('read_ax',len(payload));cf=s.get('read_cf',0)
                event=dict(name='dos_read',handle=self.get('BX'),size=count,destination=[8,0x6200],payload_hex=payload.hex())
            else:
                whence=self.get('AL');offset=(self.get('CX')<<16)|self.get('DX');cf=s.get('seek_cf',0);ax=s.get('seek_ax',0x4567)
                if not cf:self.cursor=offset-s.get('home',0) if whence==0 else self.cursor+(offset if offset<0x80000000 else offset-0x100000000)
                event=dict(name='dos_seek',handle=self.get('BX'),whence=whence,offset=offset);self.set('DX',s.get('seek_dx',0x89ab))
            event.update(ax=ax,cf=cf);self.events.append(event);self.set('AX',ax);self.set('EFLAGS',(self.get('EFLAGS')&~1)|cf)
        def out(uc,port,width,value,user):raise ValueError('hook unexpected output port')
        def inp(uc,port,width,user):raise ValueError('hook unexpected input port')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(out),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)

    def run(self,name,regs=None,*,budget=2000000):
        regs=regs or {};self.direct=name;self.stop=False;self.errors.clear();self.set('SP',0xffc0)
        setup=dict(CS=0x2000,DS=0x2e3f,SS=0x4000,ES=0x3333,BP=0x7777,SI=0x1357,DI=0x2468,AX=0x1111,BX=0x2222,CX=0x3333,DX=0x4444,EFLAGS=0x202|(0x400 if self.s.get('df') else 0));setup.update(regs)
        for key,value in setup.items():self.set(key,value)
        if name=='hook':
            frame=[0xff00,0x2000,self.get('EFLAGS')];start=0x294a;cleanup=6;self.set('EFLAGS',self.get('EFLAGS')&~0x300)
        else:frame=[0xff00,0x2000]+([0x100,0x5000] if name=='start' else []);start=0x2856 if name=='start' else 0x2912;cleanup=8 if name=='start' else 4
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*len(frame),*frame));self.uc.emu_start(self.code+start,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('hook terminal/budget differs')
        if self.get('SP')!=0xffc0+cleanup:raise ValueError('hook far/interrupt cleanup differs')


class Spec:
    """Shared physical memory, native archive semantics and declared boundary results."""
    def __init__(self,p):
        self.mem=bytearray(p.uc.mem_read(0,0x100000));self.s=p.s;self.p=p;self.events=[];self.cursor=0
    def word(self,address):return struct.unpack_from('<H',self.mem,address)[0]
    def dword(self,address):return struct.unpack_from('<I',self.mem,address)[0]
    def w(self,address,value):struct.pack_into('<H',self.mem,address,u16(value))
    def dw(self,address,value):struct.pack_into('<I',self.mem,address,value&0xffffffff)
    def heap(self,name,args,owner=None):
        s=self.s;ax=s.get('model_ax',0xf00d);cf=s.get('model_cf',1)
        event=dict(name=name,args=args,ax=ax,cf=cf,payload_hex='')
        if name=='allocate':
            ax=s.get(owner+'_segment',{'header':0x6000,'directory':0x8000,'pfile':0x6100,'buffer':0x6200}[owner]);cf=s.get(owner+'_cf',0)
            event=dict(name=name,owner=owner,args=args,ax=ax,cf=cf,id=self.word(self.p.data+bf.ALLOC_ID))
        self.events.append(event);return ax,cf
    def file_call(self,name,args,payload=b''):
        ax=self.s.get('model_ax',0xf00d);cf=self.s.get('model_cf',1)
        if name in ('file_open','file_close'):ax=self.s.get(name+'_ax',1 if name=='file_open' else 0);cf=self.s.get(name+'_cf',0)
        if name=='file_read':
            self.mem[args[2]*16+args[1]:args[2]*16+args[1]+len(payload)]=payload;ax=self.s.get('file_read_ax',len(payload));cf=self.s.get('file_read_cf',0)
        self.events.append(dict(name=name,args=args,ax=ax,cf=cf,payload_hex=payload.hex()))
    def start(self):
        p,s=self.p,self.s
        if not self.dword(p.code+ORG):
            self.file_call('file_open',[0x100,0x5000]);header,_=self.heap('allocate',[16],'header')
            payload=p.header[:s.get('short_header',16)];self.file_call('file_read',[16,0,header],payload)
            size=self.word(header*16);key=self.word(header*16+6)&255;self.heap('free',[header]);directory,_=self.heap('allocate',[size],'directory')
            self.w(p.data+ENTRIES,directory);self.file_call('file_read',[size,0,directory],encode(p.directory,s.get('key',0xa5)&255)[:size]);self.file_call('file_close',[])
            for i in range(size or 65536):
                at=directory*16+i;value=self.mem[at]^key;self.mem[at]=value;key=(key-value)&255
            self.events.append(dict(name='get_vector',number=0x21));self.w(p.code+ORG,0x100);self.w(p.code+ORG+2,0x9000)
            self.w(p.data+FILE,0);self.w(p.data+HANDLE,65535);self.events.append(dict(name='set_vector',number=0x21,pointer=[0x294a,0x2000]))
        size=0
        for i in range(65535):
            size+=1
            if not self.mem[0x50000+u16(0x100+i)]:break
        source=[self.mem[0x50000+u16(0x100+i)] for i in range(size)]
        for i,value in enumerate(source):self.mem[p.data+u16(PAR+i)]=value
    def end(self):
        p=self.p
        if not self.dword(p.code+ORG):return
        self.events.append(dict(name='set_vector',number=0x21,pointer=[self.word(p.code+ORG),self.word(p.code+ORG+2)]));self.dw(p.code+ORG,0)
        if self.word(p.data+FILE):self.close_archive();self.heap('free',[self.word(p.data+ENTRIES)])
    def buffer_open(self):
        p,s=self.p,self.s;self.w(p.data+bf.ALLOC_ID,6);size=self.word(p.data+bf.BBUFSIZ);segment,cf=self.heap('allocate',[u16(size+9)],'buffer')
        if cf:self.mem[p.data+bf.ERR]=3;return 0
        ax=s.get('open_handle',0x1234);cf=s.get('open_cf',0)
        self.events.append(dict(name='dos_open',mode=self.mem[p.data+bf.SHARING],filename=[PAR,0x2e3f],ax=ax,cf=cf))
        if cf:self.heap('free',[segment]);self.mem[p.data+bf.ERR]=1;return 0
        self.w(segment*16,ax);self.w(segment*16+2,0);self.w(segment*16+6,size);return segment
    def seek_buffer(self,offset):
        s=self.s;segment=self.word(0x61000);base=segment*16;handle=self.word(base);self.w(base+2,0)
        cf=s.get('seek_cf',0);self.events.append(dict(name='dos_seek',handle=handle,whence=0,offset=offset,ax=s.get('seek_ax',0x4567),cf=cf))
        if not cf:self.cursor=offset-s.get('home',0)
    def open_archive(self,request_offset):
        p,s=self.p,self.s;self.w(p.data+bf.ALLOC_ID,7);segment,cf=self.heap('allocate',[31],'pfile')
        if cf:self.mem[p.data+bf.ERR]=3;return 0
        buffer=self.buffer_open()
        if not buffer:self.heap('free',[segment]);return 0
        base=segment*16;self.w(base,buffer);directory=self.word(p.data+ENTRIES);index=0
        for _ in range(2048):
            at=directory*16+index
            if not self.mem[at]:break
            equal=True
            for count in range(65536):
                a=self.mem[0x70000+u16(request_offset+count)];b=self.mem[directory*16+u16(index+3+count)]
                if op.casefold(a)!=op.casefold(b):equal=False;break
                if not a:break
            if equal:break
            index=u16(index+32)
        else:raise ValueError('hook constructed scalar search lacks end')
        kind,aux,_,packed,original,home,_=struct.unpack('<HB13sHHI8s',self.mem[at:at+32]);self.dw(base+14,home);self.seek_buffer(home)
        getx=0x1996 if aux else 0x1952;self.w(base+4,getx)
        if aux:self.mem[base+30]=aux
        if kind not in (0xf388,0x9595):
            self.w(p.data+bf.ERR,5);self.close_archive();return 0
        self.w(base+2,getx if kind==0xf388 else 0x1904)
        if kind==0x9595:self.w(base+26,0);self.w(base+28,65535)
        self.dw(base+6,packed);self.dw(base+22,original);self.dw(base+10,0);self.dw(base+18,0);return segment
    def close_archive(self):
        segment=self.word(self.p.data+FILE) or 0x6100;base=segment*16;buffer=self.word(base)
        self.events.append(dict(name='dos_close',handle=self.word(buffer*16),ax=self.s.get('close_ax',0xabcd),cf=self.s.get('dos_cf',0)))
        self.heap('free',[buffer]);self.heap('free',[segment]);return self.s.get('model_ax',0xf00d)
    def buffer_byte(self):
        s=self.s;base=self.word(0x61000)*16;left=self.word(base+2)
        if left:
            pos=self.word(base+4);self.w(base+2,left-1);self.w(base+4,pos+1);return self.mem[base+u16(pos+8)]
        size=self.word(base+6);payload=bytes(s.get('payload',[]))[self.cursor:self.cursor+size];self.cursor+=len(payload)
        self.mem[base+8:base+8+len(payload)]=payload;ax=s.get('read_ax',len(payload));cf=s.get('read_cf',0)
        self.events.append(dict(name='dos_read',handle=self.word(base),size=size,destination=[8,0x6200],payload_hex=payload.hex(),ax=ax,cf=cf))
        if cf or not ax:self.w(base+2,0);return 65535
        self.w(base+2,ax-1);self.w(base+4,1);return self.mem[base+8]
    def getx(self):
        base=0x61000
        if self.dword(base+10)>=self.dword(base+6):return 65535
        self.dw(base+10,self.dword(base+10)+1);self.dw(base+18,self.dword(base+18)+1);value=self.buffer_byte()
        return value^self.mem[base+30] if value<256 and self.word(base+4)==0x1996 else value
    def byte(self):
        base=0x61000
        if self.word(base+2)!=0x1904:return self.getx()
        if self.word(base+26):self.w(base+26,self.word(base+26)-1);self.dw(base+18,self.dword(base+18)+1);return self.word(base+28)
        value=self.getx()
        if value>=256:return value
        previous=self.word(base+28);self.w(base+28,value)
        if value==previous:
            count=self.getx()
            if count<256:self.w(base+26,count);self.dw(base+18,self.dword(base+18)-1)
        return value
    def rewind(self):
        base=0x61000;self.w(base+26,0);self.w(base+28,65535);self.dw(base+10,0);self.dw(base+18,0);self.seek_buffer(self.dword(base+14))
    def relative(self,offset):
        for _ in range(min(offset,10000)):
            if self.byte()>=256:break
        else:
            if offset>10000:raise ValueError('hook scalar unbounded constructed seek')
        return self.dword(0x61000+18)
    def old(self,regs):
        self.events.append(dict(name='old_dos',ax=regs['AX'],bx=regs['BX'],cx=regs['CX'],dx=regs['DX'],ds=regs['DS'],live_if=False));out=dict(regs)
        out['AX']=self.s.get('old_ax',0xbeef);out['DX']=self.s.get('old_dx',0xcafe);out['EFLAGS']=(out['EFLAGS']&~1)|self.s.get('old_cf',1);return out
    def hook(self,regs):
        p=self.p;ah=regs['AX']>>8;al=regs['AX']&255;handle=self.word(p.data+HANDLE);match=regs['BX']==handle
        if self.mem[p.code+ACTIVE]:return self.old(regs)
        self.mem[p.code+0x29ae]=ah;out=dict(regs);through=False;error=False
        if ah==0x3d:
            if al&15 or handle<32768:through=True
            else:
                segment=self.open_archive(regs['DX'])
                if not segment:through=True
                else:self.w(p.data+FILE,segment);out['AX']=self.word(self.word(segment*16)*16);self.w(p.data+HANDLE,out['AX'])
        elif ah==0x3e:
            if not match:through=True
            else:out['AX']=self.close_archive();self.w(p.data+FILE,0);self.w(p.data+HANDLE,65535)
        elif ah==0x3f:
            if not match:through=True
            else:
                count=0
                for _ in range(regs['CX']):
                    value=self.byte()
                    if value>>8==255:break
                    self.mem[regs['DS']*16+u16(regs['DX']+count)]=value&255;count+=1
                out['AX']=count
        elif ah==0x42:
            if not match:through=True
            elif regs['CX']>=32768:error=True
            else:
                offset=(regs['CX']<<16)|regs['DX']
                if al==0 or al>=128:self.rewind()
                elif al!=1:offset=(self.dword(0x61000+22)-self.dword(0x61000+18))&0xffffffff
                result=self.relative(offset);out['AX']=result&65535;out['DX']=result>>16
        elif ah==0x46:error=True
        elif ah in (0x40,0x45,0x57,0x5c):error=match;through=not match
        elif ah==0x44:error=match and bool((1<<(al&31))&0xffff&0x14cf);through=not error
        else:
            if ah==0x4c:self.events.append(dict(name='set_vector',number=0x21,pointer=[self.word(p.code+ORG),self.word(p.code+ORG+2)]))
            through=True
        if through:return self.old(regs)
        out['AX']=1 if error else out['AX'];out['EFLAGS']=(out['EFLAGS']&~1)|int(error);return out


def seed_open(p):
    s=p.s;getx=0x1996 if s.get('aux') else 0x1952;getc=0x1904 if s.get('compressed') else getx
    p.uc.mem_write(p.data+FILE,struct.pack('<2H',0x6100,s.get('handle',0x1234)))
    p.uc.mem_write(0x61000,struct.pack('<3H5I2HB',0x6200,getc,getx,s.get('packed',len(s.get('payload',[]))),s.get('physical',0),s.get('home',0),s.get('logical',0),s.get('original',9),s.get('count',0),s.get('previous',65535),s.get('aux',0)))
    p.uc.mem_write(0x62000,struct.pack('<4H',s.get('handle',0x1234),0,0,s.get('buffer_size',2)))


def matrix(mz,observed):
    rows=[]
    def observe(s,steps,live=False):
        s=dict(s);p=HookProbe(mz,s,observed)
        if live:seed_open(p)
        spec=Spec(p);before=bytes(spec.mem);results=[]
        for step in steps:
            name=step['function'];regs=dict(CS=0x2000,DS=0x7000 if name=='hook' else 0x2e3f,SS=0x4000,ES=0x3333,BP=0x7777,SI=0x1357,DI=0x2468,AX=0x1111,BX=0x2222,CX=0x3333,DX=0x4444,EFLAGS=0x202|(0x400 if s.get('df') else 0));regs.update(step.get('regs',{}))
            expected=None
            if name=='start':spec.start()
            elif name=='end':spec.end()
            else:expected=spec.hook(regs)
            p.run(name,regs);actual=bytes(p.uc.mem_read(0,0x100000))
            if actual[:p.stack]!=spec.mem[:p.stack] or actual[p.stack+65536:]!=spec.mem[p.stack+65536:]:
                diffs=[hex(i) for i,(a,b) in enumerate(zip(actual,spec.mem)) if a!=b and not p.stack<=i<p.stack+65536][:12]
                raise ValueError('hook full memory scalar differs: '+str((s,step,diffs)))
            if p.events!=spec.events:raise ValueError('hook ordered request scalar differs: '+str((s,step,p.events,spec.events)))
            if expected is not None:
                if any(p.get(r)!=expected[r] for r in ('AX','BX','CX','DX','DS','ES','BP','SI','DI','SS')) or (p.get('EFLAGS')&0xfd5)!=(expected['EFLAGS']&0xfd5):raise ValueError('hook native IRET registers/flags differ: '+str((step,{r:p.get(r) for r in ('AX','DX','EFLAGS')},expected)))
            else:
                if [p.get(r) for r in ('BP','SI','DI','DS')]!=[0x7777,0x1357,0x2468,0x2e3f] or name=='start' and p.get('EFLAGS')&0x400:raise ValueError('hook install/end callee state differs')
            results.append(dict(function=name,step=step,ax=p.get('AX'),dx=p.get('DX'),flags=p.get('EFLAGS')&0xfd5))
        rows.append(dict(scenario={k:v.hex() if isinstance(v,bytes) else v for k,v in s.items()},live_fixture=live,steps=results,top_level_calls=len(results),events=p.events,native_entries=dict(p.native),writes=p.write_count,first_writes=p.writes[:32],memory_before_sha256=sha(before),memory_after_sha256=sha(actual),scoped_state_sha256=sha(actual[p.code+ORG:p.code+0x2aad]+actual[p.data+PAR:p.data+ENTRIES+2]+actual[0x60000:0x63000]+actual[0x70000:0x90000])))
    for df in (False,True):
        for size in (1,32,64,128):
            for key in (0,1,0xa5,0xffff):observe(dict(df=df,entries_size=size,key=key),[dict(function='start'),dict(function='end')])
        observe(dict(df=df,entries_size=0),[dict(function='start'),dict(function='end')])
        for length in (0,1,127,128,129,134):observe(dict(df=df,installed=True,name_length=length),[dict(function='start')])
        for name in ('header','directory'):
            observe(dict(df=df,**{name+'_cf':1},file_read_cf=1,file_read_ax=0),[dict(function='start'),dict(function='end')])
        for live in (False,True):observe(dict(df=df,installed=True,payload=[1,2,3]),[dict(function='end'),dict(function='end')],live)
        observe(dict(df=df,file_open_ax=0,file_open_cf=1),[dict(function='start'),dict(function='start'),dict(function='end')])
        observe(dict(df=df,installed=True,read_cf=1,payload=[1,2,3]),[dict(function='hook',regs=dict(AX=0x3f00,BX=0x1234,CX=4,DX=0x300))],True)
        observe(dict(df=df,installed=True,seek_cf=1,payload=[1,2,3]),[dict(function='hook',regs=dict(AX=0x4200,BX=0x1234,CX=0,DX=1)),dict(function='hook',regs=dict(AX=0x3f00,BX=0x1234,CX=4,DX=0x300))],True)
        for mode in (0,1,15,16,32,128,255):
            for installed_handle in (0,0x1234,0x8000,0xffff):
                s=dict(df=df,installed=True,payload=[1,2,3]);psteps=[dict(function='hook',regs=dict(AX=0x3d00|mode,DX=0x100))]
                # Handle-only fixture tests the signed acceptance gate.
                if installed_handle!=0xffff:s['handle']=installed_handle
                observe(s,psteps,installed_handle!=0xffff)
        for key in ('pfile_cf','buffer_cf','open_cf','seek_cf'):
            observe(dict(df=df,installed=True,payload=[1,2],**{key:1}),[dict(function='hook',regs=dict(AX=0x3d00,DX=0x100))])
        observe(dict(df=df,installed=True,payload=[1,2]),[dict(function='hook',regs=dict(AX=0x3d00,DX=0x200))])
        for ah in (0,0x3e,0x3f,0x40,0x45,0x46,0x4c,0x57,0x5c,0xff):
            for match in (False,True):
                for carry in (0,1):observe(dict(df=df,installed=True,payload=[7,7,3],compressed=True),[dict(function='hook',regs=dict(AX=ah<<8,BX=0x1234 if match else 5,CX=4,DX=0xfffe,EFLAGS=0x202|(0x400 if df else 0)|carry))],True)
        for mode in range(256):
            for match in (False,True):observe(dict(df=df,installed=True),[dict(function='hook',regs=dict(AX=0x4400|mode,BX=0x1234 if match else 5))],True)
        for mode in (0,1,2,127,128,255):
            for high in (0,1,0x7fff,0x8000,0xffff):observe(dict(df=df,installed=True,payload=[1,2,3,4]),[dict(function='hook',regs=dict(AX=0x4200|mode,BX=0x1234,CX=high,DX=2))],True)
        for active in (1,255):observe(dict(df=df,installed=True,active=active),[dict(function='hook',regs=dict(AX=0x3f00,BX=0x1234,CX=4,DX=0x100))],True)
        for compressed in (False,True):
            for aux in (0,0xa5):
                payload=[7,7,3,8] if compressed else [1,2,3,4];payload=[v^aux for v in payload]
                directory=op.header(kind=0x9595 if compressed else 0xf388,aux=aux,packed=len(payload),original=9,offset=0)+bytes(32)
                observe(dict(df=df,payload=payload,directory=directory),[dict(function='start'),dict(function='hook',regs=dict(AX=0x3d00,DX=0x100)),dict(function='hook',regs=dict(AX=0x3f00,BX=0x1234,CX=8,DX=0xfffe)),dict(function='hook',regs=dict(AX=0x4200,BX=0x1234,CX=0,DX=1)),dict(function='hook',regs=dict(AX=0x3f00,BX=0x1234,CX=3,DX=0x300)),dict(function='hook',regs=dict(AX=0x3e00,BX=0x1234)),dict(function='end')])
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('hook prior buffer proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_pfint21.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    local={p:(ROOT/p).read_bytes() for p in LOCAL};inputs.update({p:sha(d) for p,d in local.items()})
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('hook input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];objects=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('hook invalid image')
        analysis=analyze(mz.program_image);observed=dict(path=path,analysis=analysis,cpu=matrix(mz,analysis))
        if observations:
            if analysis!=observations[0]['analysis']:raise ValueError('hook complete CODE/table/native context differs')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                wanted=local['src/main/formats/pfopen.inl'] if p=='th03/formats/pfopen.asm' else d
                expected=wanted.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else wanted;actual=cached.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else cached
                if actual!=expected:raise ValueError('hook cached frozen provider differs: '+p)
            for p,d in local.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                if cached!=d:raise ValueError('hook cached maintained PFOPEN provider differs')
            opath=str(tree/'obj/th03/mainl.obj');obj_data=(ROOT/opath).read_bytes();inputs[opath]=sha(obj_data);obj=describe_omf(obj_data)
            if not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0']:raise ValueError('hook cached root OMF identity differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments','record_count','record_counts')}
            if objects and obj['dependency_timestamp_normalized_sha256']!=objects[0]['dependency_timestamp_normalized_sha256']:raise ValueError('hook cached OMF differs beyond dependency timestamps')
            objects.append(observed['object']);maprows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));carrier=next(row for row in maprows if row['module']=='th03_mainl.asm' and row['segment']==0 and row['size'])
            if not carrier['start']<=ORG<0x2aad<=carrier['start']+carrier['size']:raise ValueError('hook include outside complete root carrier')
            observed['carrier']=carrier;target=parse_mz((ROOT/observations[0]['path']).read_bytes())
            extents=[('hook-include',ORG,605),('buffer-close-fill',0x472,84),('buffer-getc',0x506,48),('buffer-open-read-seek',0x5b8,246),('dos-open',0xaae,26),('archive-readers',0x18da,356),('archive-open-compare',0x2b16,338)]
            observed['comparisons']={n:extent_observation(target,mz,dict(start=a,size=z,segment=0,offset=a)) for n,a,z in extents}
            if any(not x['raw_slice_equal'] or not x['ordered_relocations_equal'] for x in observed['comparisons'].values()):raise ValueError('hook complete raw/ordered relocations differ')
            def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('memory_before_sha256','memory_after_sha256')} for row in cpu]
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']):raise ValueError('hook original/cached CPU differs')
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('hook canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('hook frozen provider changed')
    result=dict(kind='th03-mainl-complete-pfint21-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},producer_overlay={'th03/formats/pfopen.asm':'src/main/formats/pfopen.inl'},observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL full archive hook605/native archive+buffer1198 and explicit DOS/file/heap:',args.output)


if __name__=='__main__':main()
