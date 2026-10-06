#!/usr/bin/env python3
"""Complete MAINL buffered file includes with native DOS-open and explicit DOS/heap."""
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
PROOF='.analysis/sol-mainl-pfread-review-20261006.json'
PROOF_SHA256='00a1b319423b649f2edbabdbe298e9d2536a96d0cf9fa16aba72922b603c68a1'
RANGES=[('close',0x472,24,2),('fill',0x48a,59,2),('getc',0x506,48,2),
 ('open',0x5b8,83,4),('read',0x60c,48,8),('seek',0x63c,65,6),
 ('seek_base',0x67e,47,8),('dos_open',0xaae,26,4)]
ALIGNMENT={0x4c5:0x90,0x60b:0x90,0x67d:0x90,0x6ad:0x90}
MODELS={0x21ae:('allocate',2,{0x5cc}),0x22b2:('free',2,{0x486,0x600})}
NATIVE_CALLS={0x48a:{0x532},0x506:{0x623},0xaae:{0x5da}}
DOS={0x47f:0x3e,0x49e:0x3f,0x671:0x42,0x6a5:0x42,0xaba:0x3d}
PROVIDERS=['th03_mainl.asm','ReC98.inc','th03/th03.inc','libs/master.lib/pf.inc',
 'libs/master.lib/pf[data].asm','libs/master.lib/dos_ropen[data].asm',
 'libs/master.lib/master.inc','libs/master.lib/macros.inc','libs/master.lib/func.hpp',
 'libs/master.lib/super.inc','libs/master.lib/bcloser.asm','libs/master.lib/bfill.asm',
 'libs/master.lib/bgetc.asm','libs/master.lib/bopenr.asm','libs/master.lib/bread.asm',
 'libs/master.lib/bseek.asm','libs/master.lib/bseek_.asm','libs/master.lib/dos_ropen.asm','libs/master.lib/memheap.asm']
BBUFSIZ,ERR,ALLOC_ID,SHARING=0x5b0,0x5b2,0x856,0x558
NAMES={a:n for n,a,_,_ in RANGES}


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[]
    for name,start,size,cleanup in RANGES:
        body=image[start:start+size]
        if len(body)!=size:raise ValueError('buffer complete body/far cleanup differs')
        ins=list(decoder.disasm(body,start));bounds={i.address for i in ins}
        if not ins or sum(i.size for i in ins)!=size or (ins[-1].mnemonic,ins[-1].op_str)!=('retf',hex(cleanup) if cleanup>=10 else str(cleanup)):raise ValueError('buffer complete body/far cleanup differs')
        edges=[]
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf') and (i.mnemonic,i.op_str)!=('retf',str(cleanup)):raise ValueError('buffer interior return differs')
            if i.mnemonic in ('in','out'):raise ValueError('buffer unexpected port')
            if i.mnemonic=='int':
                if i.address not in DOS or i.bytes!=b'\xcd\x21':raise ValueError('buffer unknown DOS interrupt site')
                edges.append(dict(instruction=i.address,kind='modeled-int21',ah=DOS[i.address]));continue
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('buffer unknown indirect edge')
            if i.mnemonic=='lcall':raise ValueError('buffer unknown far interface')
            dest=i.operands[0].imm
            if i.mnemonic=='call':
                if dest not in MODELS and dest not in NATIVE_CALLS:raise ValueError('buffer unknown near interface')
                if not j or ins[j-1].bytes!=b'\x0e':raise ValueError('buffer far interface lacks PUSH CS')
            elif dest not in bounds:raise ValueError('buffer branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=start,size=size,instructions=len(ins),sha256=sha(body),cleanup=cleanup,edges=edges))
    if any(image[a:a+1]!=bytes([v]) for a,v in ALIGNMENT.items()):raise ValueError('buffer complete producer alignment differs')
    return dict(bodies=rows,body_bytes=500,producer_bytes=4,buffer_includes_bytes=478,dos_open_bytes=26,producers=ALIGNMENT)


class BufferProbe(Probe):
    def __init__(self,mz,s):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x20000,0x2e3f0,0x40000
        self.s=s;self.buffer=s.get('allocation',0x6000)*16;self.output=s.get('output_segment',0x7000)*16
        self.errors=[];self.events=[];self.native=Counter();self.writes=[];self.stop=False;self.read_index=0;self.direct=None
        for name,value in [('CS',0x2000),('DS',0x2e3f),('SS',0x4000),('ES',0x3333),('FS',0x4444),('BP',0x7777),('SI',0x1357),('DI',0x2468),('EFLAGS',0x202|(0x400 if s.get('df') else 0))]:self.set(name,value)
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2000:raise ValueError('buffer terminal segment alias')
                self.stop=True;uc.emu_stop();return
            off=address-self.code
            if off in MODELS:
                if self.get('CS')!=0x2000:raise ValueError('buffer model segment alias')
                name,cleanup,returns=MODELS[off];sp=self.get('SP');frame=list(struct.unpack('<'+'H'*(2+cleanup//2),uc.mem_read(self.stack+sp,4+cleanup)))
                if frame[0] not in returns or frame[1]!=0x2000:raise ValueError('buffer modeled far frame differs')
                ax=s.get('allocation',0x6000) if name=='allocate' else s.get('free_ax',0xf00d)
                cf=s.get('allocation_cf',0) if name=='allocate' else s.get('free_cf',1)
                self.events.append(dict(name=name,args=frame[2:],ax=ax,cf=cf));self.set('AX',ax);self.set('EFLAGS',(self.get('EFLAGS')&~1)|cf)
                self.set('SP',sp+4+cleanup);self.set('CS',frame[1]);self.set('IP',frame[0]);return
            if self.get('CS')!=0x2000 or not any(a<=off<a+n for _,a,n,_ in RANGES):raise ValueError('CPU escaped buffer bodies')
            if off in NAMES:
                self.native[NAMES[off]]+=1
                sp=self.get('SP');ip,cs=struct.unpack('<2H',uc.mem_read(self.stack+sp,4))
                if cs!=0x2000 or (off in NATIVE_CALLS and ip not in NATIVE_CALLS[off] and not (self.direct==NAMES[off] and ip==0xff00)):raise ValueError('buffer native far frame differs')
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            allowed=(self.buffer<=address and address+size<=self.buffer+8 or self.output<=address and address+size<=self.output+65536 or any(self.data+a<=address and address+size<=self.data+a+2 for a in (ERR,ALLOC_ID)))
            if not allowed:raise ValueError('buffer write outside owned state')
            self.writes.append([address,size,value])
        def interrupt(uc,number,user):
            site=u16(self.get('IP')-2);ah=self.get('AH')
            if number!=0x21 or self.get('CS')!=0x2000 or DOS.get(site)!=ah:raise ValueError('buffer unknown DOS request/site')
            cf=0;ax=0;event={}
            if ah==0x3d:
                ax=s.get('open_handle',0x1234);cf=s.get('open_cf',0);event=dict(name='dos_open',mode=self.get('AL'),filename=[self.get('DX'),self.get('DS')])
            elif ah==0x3e:
                ax=s.get('close_ax',0xbeef);cf=s.get('close_cf',1);event=dict(name='dos_close',handle=self.get('BX'))
            elif ah==0x3f:
                reads=s.get('reads',[]);item=reads[self.read_index] if self.read_index<len(reads) else {};self.read_index+=1
                payload=bytes(item.get('data',[]));ax=item.get('ax',len(payload));cf=item.get('cf',0)
                if self.get('DS')*16!=self.buffer or self.get('DX')!=8 or len(payload)>65528:raise ValueError('buffer modeled read destination differs')
                uc.mem_write(self.buffer+8,payload)
                event=dict(name='dos_read',handle=self.get('BX'),destination=[8,self.get('DS')],size=self.get('CX'),payload_hex=payload.hex())
            else:
                ax=s.get('seek_ax',0x4567);cf=s.get('seek_cf',0)
                event=dict(name='dos_seek',handle=self.get('BX'),whence=self.get('AL'),offset=(self.get('CX')<<16)|self.get('DX'))
                self.set('DX',s.get('seek_dx',0x89ab))
            event.update(ax=ax,cf=cf);self.events.append(event);self.set('AX',ax);self.set('EFLAGS',(self.get('EFLAGS')&~1)|cf)
        def output(uc,port,width,value,user):raise ValueError('buffer unexpected output port')
        def inp(uc,port,width,user):raise ValueError('buffer unexpected input port')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(interrupt))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)

    def run(self,name,args=()):
        self.direct=name;self.stop=False;self.errors.clear();self.set('SP',0xffc0)
        _,start,_,cleanup=next(r for r in RANGES if r[0]==name)
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2000,*args))
        self.uc.emu_start(self.code+start,0x100000,count=200000)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('buffer terminal/budget differs')
        if self.get('SP')!=0xffc4+cleanup or self.get('DS')!=0x2e3f or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]:raise ValueError('buffer far cleanup/callee-saved differs')


class Scalar:
    def __init__(self,state,data,s):
        self.state=bytearray(state);self.data=bytearray(data);self.s=s;self.events=[];self.native=Counter();self.read_index=0
        self.output=self.state if s.get('output_segment',0x7000)==s.get('allocation',0x6000) else bytearray(b'\xa5'*65536)
    def word(self,at):return struct.unpack_from('<H',self.state,at)[0]
    def put(self,at,value):struct.pack_into('<H',self.state,at,u16(value))
    def heap(self,name,args):
        ax=self.s.get('allocation',0x6000) if name=='allocate' else self.s.get('free_ax',0xf00d)
        cf=self.s.get('allocation_cf',0) if name=='allocate' else self.s.get('free_cf',1)
        self.events.append(dict(name=name,args=args,ax=ax,cf=cf));return ax,cf
    def run(self,name,step=None):
        step=step or {};s=self.s;self.native[name]+=1
        if name=='dos_open':
            ax=s.get('open_handle',0x1234);cf=s.get('open_cf',0)
            self.events.append(dict(name='dos_open',mode=s.get('sharing',0)&255,filename=[0x100,0x5000],ax=ax,cf=cf));return 0xfffe if cf else ax
        if name=='open':
            struct.pack_into('<H',self.data,ALLOC_ID,6);size=s.get('buffer_size',512)
            allocation,cf=self.heap('allocate',[u16(size+9)])
            if cf:self.data[ERR]=3;return 0
            handle=self.run('dos_open')
            if s.get('open_cf'):
                self.heap('free',[allocation]);self.data[ERR]=1;return 0
            self.put(0,handle);self.put(2,0);self.put(6,size);return allocation
        if name=='close':
            self.events.append(dict(name='dos_close',handle=self.word(0),ax=s.get('close_ax',0xbeef),cf=s.get('close_cf',1)))
            return self.heap('free',[s.get('allocation',0x6000)])[0]
        if name=='fill':
            reads=s.get('reads',[]);item=reads[self.read_index] if self.read_index<len(reads) else {};self.read_index+=1
            payload=bytes(item.get('data',[]));ax=item.get('ax',len(payload));cf=item.get('cf',0)
            self.events.append(dict(name='dos_read',handle=self.word(0),destination=[8,s.get('allocation',0x6000)],size=self.word(6),payload_hex=payload.hex(),ax=ax,cf=cf));self.state[8:8+len(payload)]=payload
            if cf or not ax:self.put(2,0);return 65535
            self.put(2,ax-1);self.put(4,1);return self.state[8]
        if name=='getc':
            if not self.word(2):return self.run('fill')
            pos=self.word(4);self.put(2,self.word(2)-1);self.put(4,pos+1);return self.state[u16(pos+8)]
        if name=='read':
            size=step.get('size',s.get('size',16));offset=step.get('output_offset',s.get('output_offset',0xfffe));count=0
            if size>=32768:return 0
            for _ in range(size):
                value=self.run('getc')
                if value==65535:break
                self.output[u16(offset+count)]=value;count+=1
            return count
        offset=step.get('offset',s.get('offset',0));left=self.word(2)
        if name=='seek' and offset>>16==0 and (offset&65535)<=left:
            self.put(2,left-offset);self.put(4,self.word(4)+offset);return 0
        whence=1 if name=='seek' else step.get('whence',s.get('whence',0))&255
        if name=='seek_base':self.put(2,0)
        requested=(offset-left)&0xffffffff if whence==1 else offset
        cf=s.get('seek_cf',0);self.events.append(dict(name='dos_seek',handle=self.word(0),whence=whence,offset=requested,ax=s.get('seek_ax',0x4567),cf=cf))
        value=65535 if cf else 0
        if name=='seek':self.put(2,value)
        return value


def initial(s):
    state=bytearray(b'\xa5'*65536);struct.pack_into('<4H',state,0,s.get('handle',0x1234),s.get('left',0),s.get('pos',0x4321),s.get('buffer_size',512))
    payload=bytes(s.get('buffered',[11,22,33,44,55]));state[8:8+len(payload)]=payload;return state


def matrix(mz):
    rows=[]
    def observe(function,s,steps=None):
        s=dict(s);p=BufferProbe(mz,s);state=initial(s);p.uc.mem_write(p.buffer,bytes(state))
        if p.output!=p.buffer:p.uc.mem_write(p.output,b'\xa5'*65536)
        p.uc.mem_write(0x50100,b'archive.dat\0');p.uc.mem_write(p.data+BBUFSIZ,struct.pack('<H',s.get('buffer_size',512)))
        p.uc.mem_write(p.data+ERR,b'\xef\xbe');p.uc.mem_write(p.data+SHARING,struct.pack('<H',s.get('sharing',0)))
        before=bytes(p.uc.mem_read(p.data,65536));scalar=Scalar(state,before,s);results=[]
        for step in steps or [dict(function=function)]:
            name=step['function'];allocation=s.get('allocation',0x6000);args=[allocation]
            if name in ('open','dos_open'):args=[0x100,0x5000]
            elif name=='read':args=[allocation,step.get('size',s.get('size',16)),step.get('output_offset',s.get('output_offset',0xfffe)),s.get('output_segment',0x7000)]
            elif name=='seek':args=[step.get('offset',s.get('offset',0))&65535,step.get('offset',s.get('offset',0))>>16,allocation]
            elif name=='seek_base':args=[step.get('whence',s.get('whence',0)),step.get('offset',s.get('offset',0))&65535,step.get('offset',s.get('offset',0))>>16,allocation]
            ax=scalar.run(name,step);p.run(name,args)
            if p.get('AX')!=ax or p.events!=scalar.events or p.native!=scalar.native:raise ValueError('buffer result/native/request scalar differs: '+str((name,s,step,p.events,scalar.events)))
            if bytes(p.uc.mem_read(p.buffer,65536))!=bytes(scalar.state) or bytes(p.uc.mem_read(p.output,65536))!=bytes(scalar.output) or bytes(p.uc.mem_read(p.data,65536))!=bytes(scalar.data):raise ValueError('buffer full memory scalar differs: '+str((name,s,step)))
            if bool(p.get('EFLAGS')&0x400)!=bool(s.get('df')):raise ValueError('buffer DF differs')
            results.append(dict(function=name,step=step,ax=ax,carry=p.get('EFLAGS')&1))
        rows.append(dict(function=function,scenario=s,steps=results,top_level_calls=len(results),events=p.events,native_entries=dict(p.native),writes=p.writes,buffer_sha256=sha(bytes(scalar.state)),output_sha256=sha(bytes(scalar.output)),data_before_sha256=sha(before),data_after_sha256=sha(bytes(scalar.data))))
    for df in (False,True):
        for byte in range(256):
            observe('fill',dict(df=df,reads=[dict(data=[byte])]))
            observe('getc',dict(df=df,left=1,pos=0,buffered=[byte]))
        for size in (0,1,512,32767,32768,65526,65527,65535):
            for allocation in (0,0x6000,0x6100):
                for allocation_cf in (0,1):
                    for open_cf in (0,1):observe('open',dict(df=df,buffer_size=size,allocation=allocation,allocation_cf=allocation_cf,open_cf=open_cf,sharing=0xffa5))
        for name in ('fill','getc'):
            for cf in (0,1):
                for ax in (0,1,2,255,512,65535):observe(name,dict(df=df,reads=[dict(data=[7,8,9],ax=ax,cf=cf)],pos=0xffff))
        for left in (0,1,2,512,65535):
            for pos in (0,1,0xfff7,0xfff8,0xffff):observe('getc',dict(df=df,left=left,pos=pos,reads=[dict(data=[7,8])]))
            for offset in (0,1,2,512,513,65535,65536,0x10001,0x80000000,0xffffffff):
                for cf in (0,1):observe('seek',dict(df=df,left=left,pos=0xffff,offset=offset,seek_cf=cf))
            for whence in (0,1,2,255,256,257,65535):
                for cf in (0,1):observe('seek_base',dict(df=df,left=left,whence=whence,offset=0x10000,seek_cf=cf))
        for size in (0,1,4,16,32767,32768,65535):
            for offset in (0,0xfffe,0xffff):observe('read',dict(df=df,size=size,output_offset=offset,reads=[dict(data=[1,2]),dict(data=[3,4,5])]))
        for field in (0,2,4,6):observe('read',dict(df=df,left=4,pos=0,size=4,output_segment=0x6000,output_offset=field))
        for field in (0,6):observe('read',dict(df=df,left=1,pos=0,size=4,output_segment=0x6000,output_offset=field,reads=[dict(data=[91,92])]))
        for handle in (0,1,65535):
            for cf in (0,1):observe('open',dict(df=df,open_handle=handle,open_cf=cf))
        for cf in (0,1):observe('close',dict(df=df,close_cf=cf,free_cf=cf))
        for sharing in (0,1,255,256,65535):
            for cf in (0,1):observe('dos_open',dict(df=df,sharing=sharing,open_cf=cf))
        observe('read-chain',dict(df=df,buffer_size=2,reads=[dict(data=[1,2]),dict(data=[3,4]),dict(data=[5])]),[dict(function='open'),dict(function='getc'),dict(function='read',size=5),dict(function='close')])
        for kind in ('seek','seek_base'):
            for cf in (0,1):observe('seek-read-chain',dict(df=df,seek_cf=cf,left=2,pos=0,reads=[dict(data=[91,92])]),[dict(function=kind,offset=3,whence=1),dict(function='getc'),dict(function='read',size=3)])
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('buffer prior reader proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_buffer.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('buffer input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];objects=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('buffer invalid image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz))
        if observations:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('buffer complete body/CFG differs')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                expected=d.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else d
                actual=cached.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else cached
                if actual!=expected:raise ValueError('buffer cached frozen provider differs: '+p)
            op=str(tree/'obj/th03/mainl.obj');obj_data=(ROOT/op).read_bytes();inputs[op]=sha(obj_data);obj=describe_omf(obj_data)
            if not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0']:raise ValueError('buffer cached root OMF identity differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments','record_count','record_counts')}
            if objects and obj['dependency_timestamp_normalized_sha256']!=objects[0]['dependency_timestamp_normalized_sha256']:raise ValueError('buffer cached OMF differs beyond dependency timestamps')
            objects.append(observed['object']);maprows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));carrier=next(row for row in maprows if row['module']=='th03_mainl.asm' and row['segment']==0 and row['size'])
            if not all(carrier['start']<=a<a+n<=carrier['start']+carrier['size'] for _,a,n,_ in RANGES):raise ValueError('buffer includes outside complete root carrier')
            observed['carrier']=carrier;target=parse_mz((ROOT/observations[0]['path']).read_bytes())
            extents=[('close-fill',0x472,84),('getc',0x506,48),('open-read-seek',0x5b8,246),('dos_open',0xaae,26)]
            observed['comparisons']={n:extent_observation(target,mz,dict(start=a,size=z,segment=0,offset=a)) for n,a,z in extents}
            if any(not x['raw_slice_equal'] or not x['ordered_relocations_equal'] for x in observed['comparisons'].values()):raise ValueError('buffer complete raw/ordered relocations differ')
            def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('data_before_sha256','data_after_sha256')} for row in cpu]
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']):raise ValueError('buffer target/cached CPU differs')
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('buffer canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('buffer frozen provider changed')
    result=dict(kind='th03-mainl-complete-buffer-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL buffered files/native DOS-open504bytes and explicit DOS/heap:',args.output)


if __name__=='__main__':main()
