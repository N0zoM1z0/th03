#!/usr/bin/env python3
"""Complete MAINL archive readers/RLE/relative seek with explicit buffer models."""
import argparse
from collections import Counter
from datetime import datetime,timezone
import hashlib
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
PROOF='.analysis/sol-mainl-pfopen-review-20261006.json'
PROOF_SHA256='f2837fa69fde8390e27192c57411b1071125572ff0dd44056cd775952b6b9e74'
RANGES=[('close',0x18da,26,'retf','2'),('getc',0x18f4,15,'retf','2'),
 ('len',0x1904,78,'ret',''),('plain',0x1952,68,'ret',''),('keyed',0x1996,13,'ret',''),
 ('read',0x19a4,46,'retf','8'),('rewind',0x19d2,59,'retf','2'),('seek',0x1a0e,48,'retf','6')]
ALIGNMENT={0x1903:0x90,0x19a3:0,0x1a0d:0x90}
MODELS={0x506:('buffer_getc',2,0x1994),0x472:('close_buffer',2,0x18e9),
 0x22b2:('free',2,0x18f0),0x67e:('buffer_seek',8,0x1a09)}
INDIRECT={0x18fa:(2,(0x1904,0x1952,0x1996)),0x1922:(4,(0x1952,0x1996)),
 0x1937:(4,(0x1952,0x1996)),0x19b7:(2,(0x1904,0x1952,0x1996)),0x1a1f:(2,(0x1904,0x1952,0x1996))}
NEAR_RETURNS={'len':{0x18ff,0x19bc,0x1a24},
 'plain':{0x18ff,0x19bc,0x1a24,0x1927,0x193c,0x1999},
 'keyed':{0x18ff,0x19bc,0x1a24,0x1927,0x193c}}
PROVIDERS=['th03_mainl.asm','ReC98.inc','th03/th03.inc','libs/master.lib/pf.inc',
 'libs/master.lib/master.inc','libs/master.lib/macros.inc','libs/master.lib/func.hpp',
 'libs/master.lib/super.inc','libs/master.lib/pfclose.asm','libs/master.lib/pfgetc.asm',
 'libs/master.lib/pfread.asm','libs/master.lib/pfrewind.asm','libs/master.lib/pfseek.asm',
 'libs/master.lib/bgetc.asm','libs/master.lib/bseek_.asm','libs/master.lib/bcloser.asm','libs/master.lib/memheap.asm']
NAMES={a:n for n,a,_,_,_ in RANGES}


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[]
    for name,start,size,kind,cleanup in RANGES:
        body=image[start:start+size]
        if len(body)!=size:raise ValueError('PFREAD complete body/return differs')
        ins=list(decoder.disasm(body,start));bounds={i.address for i in ins}
        if not ins or sum(i.size for i in ins)!=size or (ins[-1].mnemonic,ins[-1].op_str)!=(kind,cleanup):raise ValueError('PFREAD complete body/return differs')
        edges=[]
        for index,i in enumerate(ins):
            if i.mnemonic in ('ret','retf') and (i.mnemonic,i.op_str)!=(kind,cleanup):raise ValueError('PFREAD interior return differs')
            if i.mnemonic in ('in','out','int'):raise ValueError('PFREAD unexpected port/interrupt')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if i.address in INDIRECT:
                field,_=INDIRECT[i.address]
                if i.mnemonic!='call' or i.bytes!=b'\x26\xff\x16'+struct.pack('<H',field):raise ValueError('PFREAD indirect field differs')
                edges.append(dict(instruction=i.address,kind='native-pfile-pointer',field=field));continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('PFREAD unknown indirect edge')
            if i.mnemonic=='lcall':raise ValueError('PFREAD unknown far interface')
            dest=i.operands[0].imm
            if i.mnemonic=='call':
                if dest not in MODELS and (name,dest)!=('keyed',0x1952):raise ValueError('PFREAD unknown near call')
                if dest in MODELS and (not index or ins[index-1].bytes!=b'\x0e'):raise ValueError('PFREAD far interface lacks PUSH CS')
            elif dest not in bounds:raise ValueError('PFREAD branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=start,size=size,instructions=len(ins),sha256=sha(body),edges=edges,return_kind=kind,cleanup=cleanup))
    if any(image[a:a+1]!=bytes([v]) for a,v in ALIGNMENT.items()):raise ValueError('PFREAD complete producer bytes differ')
    return dict(bodies=rows,body_bytes=353,producer_bytes=3,complete_contribution_bytes=356,producers=ALIGNMENT)


class ReadProbe(Probe):
    def __init__(self,mz,s):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack,self.pfile=0x20000,0x2e3f0,0x40000,0x60000
        self.output=s.get('output_segment',0x7000)*16;self.s=s;self.direct=None
        self.stop=False;self.boundary_stop=False;self.errors=[];self.events=[];self.native=Counter();self.dynamic=Counter();self.position=0
        self.write_count=0;self.first_writes=[];self.write_hash=hashlib.sha256()
        for name,value in [('CS',0x2000),('DS',0x2e3f),('SS',0x4000),('ES',0x6000),('FS',0x4444),('BP',0x7777),('SI',0x1357),('DI',0x2468),('EFLAGS',0x202|(0x400 if s.get('df') else 0))]:self.set(name,value)
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2000:raise ValueError('PFREAD terminal segment alias')
                self.stop=True;uc.emu_stop();return
            off=address-self.code
            if off in MODELS:
                if self.get('CS')!=0x2000:raise ValueError('PFREAD model segment alias')
                name,cleanup,return_ip=MODELS[off];sp=self.get('SP');frame=list(struct.unpack('<'+'H'*(2+cleanup//2),uc.mem_read(self.stack+sp,4+cleanup)))
                if frame[:2]!=[return_ip,0x2000]:raise ValueError('PFREAD modeled far frame differs')
                value=s.get('interface_ax',0xf00d)
                if name=='buffer_getc':
                    values=s.get('payload',[]);value=values[self.position] if self.position<len(values) else s.get('missing',0xffff);self.position+=1
                    self.set('ES',frame[2])
                self.events.append(dict(name=name,args=frame[2:],ax=value));self.set('AX',value)
                self.set('EFLAGS',(self.get('EFLAGS')&~1)|s.get('interface_cf',1));self.set('SP',sp+4+cleanup);self.set('CS',frame[1]);self.set('IP',frame[0]);return
            if self.get('CS')!=0x2000 or not any(a<=off<a+n for _,a,n,_,_ in RANGES):raise ValueError('CPU escaped PFREAD bodies')
            if off in NAMES:
                name=NAMES[off];self.native[name]+=1
                if name in NEAR_RETURNS:
                    ip=struct.unpack('<H',uc.mem_read(self.stack+self.get('SP'),2))[0]
                    if self.get('ES')!=0x6000 or (ip not in NEAR_RETURNS[name] and not (self.direct==name and ip==0xff00)):raise ValueError('PFREAD native near frame differs')
            if off in INDIRECT:
                field,allowed=INDIRECT[off]
                if self.get('ES')!=0x6000:raise ValueError('PFREAD native pointer segment differs')
                dest=struct.unpack('<H',uc.mem_read(self.pfile+field,2))[0]
                if dest not in allowed:raise ValueError('PFREAD native pointer destination differs')
                if off==0x1a1f and s.get('seek_steps') is not None and sum(self.dynamic.values())==s['seek_steps']:
                    self.boundary_stop=True;uc.emu_stop();return
                self.dynamic[dest]+=1
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            if not (self.pfile<=address and address+size<=self.pfile+31 or self.output<=address and address+size<=self.output+65536):raise ValueError('PFREAD write outside owned state')
            self.write_count+=1;record=[address,size,value]
            if len(self.first_writes)<32:self.first_writes.append(record)
            self.write_hash.update(struct.pack('<IIQ',*record))
        def intr(uc,number,user):raise ValueError('PFREAD unexpected interrupt')
        def output(uc,port,width,value,user):raise ValueError('PFREAD unexpected output port')
        def inp(uc,port,width,user):raise ValueError('PFREAD unexpected input port')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)

    def run(self,name,args=(),*,terminal=True,budget=2000000):
        self.direct=name;self.stop=False;self.boundary_stop=False;self.errors.clear();self.set('SP',0xffc0)
        _,start,_,kind,cleanup=next(r for r in RANGES if r[0]==name)
        words=[0xff00,0x2000,*args] if kind=='retf' else [0xff00]
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*len(words),*words))
        self.uc.emu_start(self.code+start,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if self.stop!=terminal:raise ValueError('PFREAD terminal/budget differs')
        if not terminal and not self.boundary_stop:raise ValueError('PFREAD budget lacks native loop boundary')
        expected_sp=0xffc0+(4+int(cleanup) if kind=='retf' else 2)
        if terminal and (self.get('SP')!=expected_sp or self.get('DS')!=0x2e3f or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]):raise ValueError('PFREAD cleanup/callee-saved differs')


class Scalar:
    """Independent PFILE stream semantics, including output aliases and status words."""
    def __init__(self,state,s):
        self.state=bytearray(state);self.output=self.state if s.get('output_segment',0x7000)==0x6000 else bytearray(b'\xa5'*65536)
        self.s=s;self.position=0;self.events=[];self.native=Counter();self.dynamic=Counter()
    def word(self,at):return struct.unpack_from('<H',self.state,at)[0]
    def dword(self,at):return struct.unpack_from('<I',self.state,at)[0]
    def putword(self,at,value):struct.pack_into('<H',self.state,at,u16(value))
    def putdword(self,at,value):struct.pack_into('<I',self.state,at,value&0xffffffff)
    def interface(self,name,args):
        value=self.s.get('interface_ax',0xf00d)
        if name=='buffer_getc':
            values=self.s.get('payload',[]);value=values[self.position] if self.position<len(values) else self.s.get('missing',0xffff);self.position+=1
        self.events.append(dict(name=name,args=args,ax=value));return value
    def dynamic_call(self,field):
        at=self.word(field);self.dynamic[at]+=1;return self.byte(NAMES[at])
    def byte(self,name):
        self.native[name]+=1
        if name=='plain':
            if self.dword(10)>=self.dword(6):return 0xffff
            self.putdword(10,self.dword(10)+1);self.putdword(18,self.dword(18)+1)
            return self.interface('buffer_getc',[self.word(0)])
        if name=='keyed':
            value=self.byte('plain');return value^self.state[30] if value<256 else value
        if name=='len':
            if self.word(26):
                self.putword(26,self.word(26)-1);self.putdword(18,self.dword(18)+1);return self.word(28)
            value=self.dynamic_call(4)
            if value>=256:return value
            previous=self.word(28);self.putword(28,value)
            if value==previous:
                count=self.dynamic_call(4)
                if count<256:self.putword(26,count);self.putdword(18,self.dword(18)-1)
            return value
        raise ValueError('PFREAD unknown scalar byte decoder')
    def run(self,name):
        self.native[name]+=1;ax=None;dx=None;high=None;offset=self.s.get('output_offset',0xfffe)
        if name in ('plain','keyed','len'):
            self.native[name]-=1;ax=self.byte(name)
        elif name=='getc':ax=self.dynamic_call(2)
        elif name=='read':
            written=0
            for _ in range(self.s.get('size',16)):
                value=self.dynamic_call(2)
                if value>>8==255:break
                self.output[u16(offset+written)]=value&255;written+=1
            ax=written
        elif name=='seek':
            remaining=self.s.get('offset',0);high=u16((remaining>>16)+1);low=remaining&65535
            if not low:high=u16(high-1)
            steps=0
            while remaining and steps<self.s.get('seek_steps',remaining+steps):
                value=self.dynamic_call(2)
                if value>=256:break
                low=u16(low-1);remaining-=1;steps+=1
                if not low:high=u16(high-1)
            ax=self.dword(18)&65535;dx=self.dword(18)>>16
        elif name=='rewind':
            self.putword(26,0);self.putword(28,65535);self.putdword(10,0);self.putdword(18,0)
            home=self.dword(14);ax=self.interface('buffer_seek',[0,home&65535,home>>16,self.word(0)])
        elif name=='close':
            self.interface('close_buffer',[self.word(0)]);ax=self.interface('free',[0x6000])
        return ax,dx,high


def state_for(s):
    state=bytearray(b'\xa5'*65536);keyed=s.get('keyed',bool(s.get('key',0)))
    getx=0x1996 if keyed else 0x1952;getc=0x1904 if s.get('compressed') else getx
    struct.pack_into('<3H5I2HB',state,0,s.get('buffer',0x1234),getc,getx,s.get('packed',len(s.get('payload',[]))),s.get('physical',0),s.get('home',0x89abcdef),s.get('logical',0),s.get('original',0xffffffff),s.get('count',0),s.get('previous',65535),s.get('key',0))
    return state


def matrix(mz):
    rows=[]
    def observe(name,s):
        s=dict(s);p=ReadProbe(mz,s);state=state_for(s);p.uc.mem_write(p.pfile,bytes(state))
        if p.output!=p.pfile:p.uc.mem_write(p.output,b'\xa5'*65536)
        before=bytes(p.uc.mem_read(p.data,65536));scalar=Scalar(state,s);ax,dx,high=scalar.run(name)
        args=[0x6000]
        if name=='read':args=[0x6000,s.get('size',16),s.get('output_offset',0xfffe),s.get('output_segment',0x7000)]
        if name=='seek':args=[s.get('offset',0)&65535,s.get('offset',0)>>16,0x6000]
        if name in NEAR_RETURNS:args=[]
        terminal=s.get('seek_steps') is None;p.run(name,args,terminal=terminal)
        if bytes(p.uc.mem_read(p.pfile,65536))!=bytes(scalar.state) or bytes(p.uc.mem_read(p.output,65536))!=bytes(scalar.output) or bytes(p.uc.mem_read(p.data,65536))!=before:raise ValueError('PFREAD full memory scalar differs: '+str((name,s)))
        if p.events!=scalar.events or p.native!=scalar.native or p.dynamic!=scalar.dynamic:raise ValueError('PFREAD native dispatch/ordered buffer requests differ')
        if terminal and (p.get('AX')!=ax or dx is not None and p.get('DX')!=dx):raise ValueError('PFREAD return value differs')
        if high is not None and struct.unpack('<H',p.uc.mem_read(p.stack+0xffc6,2))[0]!=high:raise ValueError('PFREAD seek caller argument mutation differs')
        if bool(p.get('EFLAGS')&0x400)!=(bool(s.get('df')) and name!='read'):raise ValueError('PFREAD direction flag differs')
        rows.append(dict(function=name,scenario=s,terminal=terminal,ax=ax if terminal else None,dx=dx if terminal else None,seek_argument_high=high,events=p.events,native_entries=dict(p.native),dynamic_entries=dict(p.dynamic),writes=p.write_count,first_writes=p.first_writes,ordered_writes_sha256=p.write_hash.hexdigest(),pfile_sha256=sha(bytes(scalar.state)),output_sha256=sha(bytes(scalar.output)),data_before_sha256=sha(before),data_after_sha256=sha(bytes(p.uc.mem_read(p.data,65536)))))
    for df in (False,True):
        for name in ('close','rewind'):
            for cf in (0,1):observe(name,dict(df=df,interface_cf=cf,physical=0xffffffff,logical=0x12345678,count=65535,previous=0x4321))
        for byte in range(256):
            observe('getc',dict(df=df,payload=[byte],key=0xaa))
            observe('read',dict(df=df,compressed=True,payload=[byte,byte,3],size=8))
        streams=[[],[1],[1,2,3],[7,7],[7,7,0],[7,7,1],[7,7,255],[7,7,255,7,255,7,1,9],[1,1,2,2,2,3,3,3,0],list(range(256)),[0x100,0x1234,0xff00,0xffff]]
        for compressed in (False,True):
            for keyed in (False,True):
                for values in streams:
                    for name in ('getc','read','seek'):
                        observe(name,dict(df=df,compressed=compressed,keyed=keyed,key=0xa5,payload=values,size=16,offset=16))
        for name in ('plain','keyed','len','getc','read','seek'):
            for packed,physical,logical in [(0,0,0),(1,0,0xffffffff),(0x10000,0xffff,0xffff),(0xffffffff,0xfffffffe,0xffffffff),(0x80000000,0x7fffffff,0x7fffffff),(1,2,3)]:
                observe(name,dict(df=df,key=255,compressed=True,packed=packed,physical=physical,logical=logical,payload=[7,7,3],offset=4,size=4))
        for count in (0,1,255,65535):
            for previous in (0,255,0x100,0xffff):
                observe('read',dict(df=df,compressed=True,count=count,previous=previous,logical=0xffffffff,packed=0,size=3))
        for offset in (0,1,255,65535,65536,65537,0xffffffff,0xffff0000):
            observe('seek',dict(df=df,compressed=True,count=65535,previous=42,packed=0,offset=offset))
        for output_offset in (0,0xfffe,0xffff):
            observe('read',dict(df=df,payload=[1,2,3,4],size=4,output_offset=output_offset))
        for field in (10,18,26,30):
            observe('read',dict(df=df,output_segment=0x6000,output_offset=field,key=0xaa,payload=[1,2,3,4],size=4))
        for name in ('getc','read','seek','len','plain','keyed'):
            for missing in (0xffff,0xff00,0x100,0x1234):
                observe(name,dict(df=df,compressed=True,packed=3,missing=missing,size=4,offset=4))
        observe('seek',dict(df=df,compressed=True,count=65535,previous=42,payload=[42],offset=65536))
        observe('seek',dict(df=df,offset=0xffffffff,packed=0xffffffff,missing=42,seek_steps=500))
        observe('read',dict(df=df,compressed=True,payload=[7,7,255],size=300))
        observe('read',dict(df=df,compressed=True,key=0xaa,payload=[0xad,0xad,0x55],size=300))
        for field in (18,26,30):
            observe('read',dict(df=df,compressed=True,count=2,previous=5,output_segment=0x6000,output_offset=field,payload=[1,2,3,4],size=4))
        observe('read',dict(df=df,size=0,payload=[7],packed=1))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('PFREAD prior PFOPEN proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_pfread.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('PFREAD input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];objects=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('PFREAD invalid image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz))
        if observations:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('PFREAD complete body/CFG differs')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                if cached.replace(b'\r\n',b'\n')!=d.replace(b'\r\n',b'\n'):raise ValueError('PFREAD cached frozen provider differs: '+p)
            op=str(tree/'obj/th03/mainl.obj');obj_data=(ROOT/op).read_bytes();inputs[op]=sha(obj_data);obj=describe_omf(obj_data)
            if not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0']:raise ValueError('PFREAD root OMF identity differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments','record_count','record_counts')}
            if objects and obj['dependency_timestamp_normalized_sha256']!=objects[0]['dependency_timestamp_normalized_sha256']:raise ValueError('PFREAD cached OMF differs beyond dependency timestamps')
            objects.append(observed['object'])
            maprows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));carrier=next(row for row in maprows if row['module']=='th03_mainl.asm' and row['segment']==0 and row['size'])
            if not carrier['start']<=0x18da<0x1a3e<=carrier['start']+carrier['size']:raise ValueError('PFREAD includes outside complete root carrier')
            observed['carrier']=carrier;target=parse_mz((ROOT/observations[0]['path']).read_bytes())
            observed['comparison']=extent_observation(target,mz,dict(start=0x18da,size=356,segment=0,offset=0x18da))
            if not observed['comparison']['raw_slice_equal'] or not observed['comparison']['ordered_relocations_equal']:raise ValueError('PFREAD complete raw/ordered relocations differ')
            def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('data_before_sha256','data_after_sha256')} for row in cpu]
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']):raise ValueError('PFREAD original/cached CPU differs')
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('PFREAD canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('PFREAD frozen provider changed')
    result=dict(kind='th03-mainl-complete-pfread-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL archive readers353+3producer/native RLE and explicit buffer interfaces:',args.output)


if __name__=='__main__':main()
