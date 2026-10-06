#!/usr/bin/env python3
"""Complete MAINL PFOPEN with native near STR_IEQ and explicit buffer interfaces."""
import argparse
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
from review_th03_mainl_cutscene import DS,Probe,REVISION,sha
from review_th03_mainl_snow import u16

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-mainl-math-review-20261006.json'
PROOF_SHA256='1e652ce847388d66be02fbe864be9aab428dac3988bc9324d44f1adbf5fbfe3f'
RANGES=[('open',0x2b16,281,'retf','8'),('compare',0x2c30,56,'ret','8')]
MODELS={0x21ae:('allocate',2),0x5b8:('open_buffer',4),0x67e:('seek',8),0x472:('close_buffer',2),0x22b2:('free',2)}
PROVIDERS=['th03_mainl.asm','th03/formats/pfopen.asm','libs/master.lib/pf_str_ieq.asm',
 'libs/master.lib/pf.inc','libs/master.lib/pf\u005bdata\u005d.asm','libs/master.lib/super.inc',
 'libs/master.lib/master.inc','libs/master.lib/macros.inc','libs/master.lib/func.hpp',
 'libs/master.lib/bopenr.asm','libs/master.lib/bseek_.asm','libs/master.lib/bcloser.asm',
 'libs/master.lib/memheap.asm','libs/master.lib/pfint21.asm','libs/master.lib/graph_pack_put_8_noclip.asm',
 'ReC98.inc','th03/th03.inc']
LOCAL=['src/main/formats/pfopen.inl','src/main/formats/pfopen.hpp']
ERR,ALLOC_ID,ENTRIES=0x5b2,0x856,0x1d06


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[]
    for name,start,size,kind,cleanup in RANGES:
        body=image[start:start+size]
        if len(body)!=size:raise ValueError('PFOPEN complete body/cleanup differs')
        ins=list(decoder.disasm(body,start));bounds={i.address for i in ins}
        if not ins or sum(i.size for i in ins)!=size or (ins[-1].mnemonic,ins[-1].op_str)!=(kind,cleanup):raise ValueError('PFOPEN complete body/cleanup differs')
        edges=[]
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf') and (i.mnemonic,i.op_str)!=(kind,cleanup):raise ValueError('PFOPEN interior return differs')
            if i.mnemonic in ('in','out','int'):raise ValueError('PFOPEN unexpected port/interrupt')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('PFOPEN indirect edge')
            if i.mnemonic=='lcall':raise ValueError('PFOPEN unknown far interface')
            dest=i.operands[0].imm
            if i.mnemonic=='call':
                if name!='open' or dest not in (*MODELS,0x2c30):raise ValueError('PFOPEN unknown near call')
                if dest in MODELS and (not j or ins[j-1].bytes!=b'\x0e'):raise ValueError('PFOPEN far interface lacks PUSH CS')
            elif dest not in bounds:raise ValueError('PFOPEN branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=start,size=size,return_kind=kind,cleanup=cleanup,instructions=len(ins),sha256=sha(body),edges=edges))
    if image[0x2c2f:0x2c30]!=b'\x90':raise ValueError('PFOPEN complete producer alignment differs')
    return dict(body=rows[0],native_compare=rows[1],body_bytes=281,producer_offset=0x2c2f,producer_bytes=1,compare_bytes=56)


def header(kind=0xf388,name=b'name.dat',aux=0,packed=7,original=9,offset=0x12345678):
    if len(name)>13:raise ValueError('PFOPEN constructed header filename too long')
    return struct.pack('<HB13sHHI8s',kind,aux,name,packed,original,offset,b'\x91'*8)


def casefold(byte):return byte-32 if 97<=byte<=122 else byte


def compare_scalar(table,at,string,offset):
    for count in range(65536):
        a,b=string[u16(offset+count)],table[u16(at+count)]
        if casefold(a)!=casefold(b):return False,count+1
        if not a:return True,count+1
    raise ValueError('PFOPEN scalar comparison has no terminator')


class PfProbe(Probe):
    """Native PFOPEN and STR_IEQ; buffer/heap requests have explicit ABI/status."""
    def __init__(self,mz,s):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x20000,0x2e3f0,0x40000
        for name,value in [('CS',0x2000),('DS',0x2e3f),('SS',0x4000),('ES',0x3333),('FS',0x4444),('BP',0x7777),('SI',0x1357),('DI',0x2468),('EFLAGS',0x202|(0x400 if s.get('df') else 0))]:self.set(name,value)
        self.s=s;self.heap=s.get('allocation',0x6000)*16;self.errors=[];self.events=[];self.writes=[];self.comparisons=[];self.stop=False
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2000:raise ValueError('PFOPEN terminal segment alias')
                self.stop=True;uc.emu_stop();return
            off=address-self.code
            if off in MODELS:
                if self.get('CS')!=0x2000:raise ValueError('PFOPEN model segment alias')
                name,cleanup=MODELS[off];sp=self.get('SP');frame=list(struct.unpack('<'+'H'*(2+cleanup//2),uc.mem_read(self.stack+sp,4+cleanup)))
                if frame[1]!=0x2000:raise ValueError('PFOPEN model return segment differs')
                self.events.append(dict(name=name,args=frame[2:]));value=0xffff
                if name=='allocate':value=s.get('allocation',0x6000);self.set('EFLAGS',(self.get('EFLAGS')&~1)|s.get('allocation_cf',0))
                elif name=='open_buffer':
                    value=s.get('buffer',0x1234);self.set('EFLAGS',(self.get('EFLAGS')&~1)|s.get('open_cf',0))
                    if 'open_errno' in s:self.uc.mem_write(self.data+ERR,struct.pack('<H',s['open_errno']))
                elif name=='seek':value=s.get('seek_ax',0xdead);self.set('EFLAGS',(self.get('EFLAGS')&~1)|s.get('seek_cf',1))
                self.set('AX',value);self.set('SP',sp+4+cleanup);self.set('CS',frame[1]);self.set('IP',frame[0]);return
            if self.get('CS')!=0x2000 or not any(at<=off<at+n for _,at,n,_,_ in RANGES):raise ValueError('CPU escaped PFOPEN bodies')
            if off==0x2c30:
                sp=self.get('SP');frame=list(struct.unpack('<5H',uc.mem_read(self.stack+sp,10)))
                if frame[0]!=0x2b68 or frame[2]!=0x8000 or frame[4]!=0x7000:raise ValueError('PFOPEN compare native near frame differs')
                self.comparisons.append(dict(table_offset=frame[1],string_offset=frame[3],iterations=0))
            elif off==0x2c3c:
                if not self.comparisons:raise ValueError('PFOPEN compare loop lacks frame')
                self.comparisons[-1]['iterations']+=1
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            if self.heap<=address and address+size<=self.heap+31:self.writes.append([address,size,value]);return
            if any(self.data+at<=address and address+size<=self.data+at+2 for at in (ERR,ALLOC_ID)):self.writes.append([address,size,value]);return
            raise ValueError('PFOPEN write outside owned state')
        def intr(uc,number,user):raise ValueError('PFOPEN unexpected interrupt')
        def output(uc,port,width,value,user):raise ValueError('PFOPEN unexpected output port')
        def inp(uc,port,width,user):raise ValueError('PFOPEN unexpected input port')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)

    def run(self,*,terminal=True):
        self.stop=False;self.errors.clear();self.set('SP',0xffc0)
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<6H',0xff00,0x2000,self.s.get('string_offset',0xfff8),0x7000,0x100,0x5000))
        self.uc.emu_start(self.code+0x2b16,0x100000,count=30000 if terminal else 10000)
        if self.errors:raise ValueError(self.errors[0])
        if self.stop!=terminal:raise ValueError('PFOPEN terminal/budget differs')
        if terminal and (self.get('SP')!=0xffcc or self.get('DS')!=0x2e3f or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]):raise ValueError('PFOPEN far cleanup/callee-saved differs')


def matrix(mz):
    rows=[]
    def observe(s,terminal=True):
        s=dict(s);p=PfProbe(mz,s);table=bytearray(header(name=b'miss.dat')*2048 if s.get('endless') else b'\0'*65536)
        for i,h in enumerate(s.get('headers',[header()])):table[i*32:i*32+32]=h
        string=bytearray(b'\0'*65536);offset=s.get('string_offset',0xfff8)
        for i,b in enumerate(s.get('request',b'NAME.DAT\0')):string[u16(offset+i)]=b
        p.uc.mem_write(0x80000,bytes(table));p.uc.mem_write(0x70000,bytes(string));p.uc.mem_write(0x50100,b'archive.dat\0');p.uc.mem_write(p.heap,b'\xa5'*31)
        p.uc.mem_write(p.data+ENTRIES,struct.pack('<H',0x8000));p.uc.mem_write(p.data+ERR,struct.pack('<H',0xbeef));before=bytes(p.uc.mem_read(p.data,65536));expected=bytearray(before)
        struct.pack_into('<H',expected,ALLOC_ID,7);heap=bytearray(b'\xa5'*31);events=[dict(name='allocate',args=[31])];wanted_comparisons=[];ax=0;searched=False
        if s.get('allocation_cf'):
            expected[ERR]=3
        else:
            events.append(dict(name='open_buffer',args=[0x100,0x5000]));buffer=s.get('buffer',0x1234)
            if 'open_errno' in s:struct.pack_into('<H',expected,ERR,s['open_errno'])
            if not buffer:events.append(dict(name='free',args=[s.get('allocation',0x6000)]))
            else:
                struct.pack_into('<H',heap,0,buffer)
                if terminal:
                    index=0
                    while table[index]:
                        equal,iterations=compare_scalar(table,u16(index+3),string,offset);searched=True
                        wanted_comparisons.append(dict(table_offset=u16(index+3),string_offset=offset,iterations=iterations))
                        if equal:break
                        index=u16(index+32)
                    kind,aux,_,packed,original,home,_=struct.unpack('<HB13sHHI8s',table[index:index+32])
                    struct.pack_into('<I',heap,14,home);events.append(dict(name='seek',args=[0,home&65535,home>>16,buffer]))
                    getx=0x1996 if aux else 0x1952
                    if aux:heap[30]=aux
                    struct.pack_into('<H',heap,4,getx)
                    if kind not in (0xf388,0x9595):
                        struct.pack_into('<H',expected,ERR,5);events.extend([dict(name='close_buffer',args=[buffer]),dict(name='free',args=[s.get('allocation',0x6000)])])
                    else:
                        struct.pack_into('<H',heap,2,getx if kind==0xf388 else 0x1904)
                        if kind==0x9595:struct.pack_into('<2H',heap,26,0,65535)
                        struct.pack_into('<I',heap,6,packed);struct.pack_into('<I',heap,22,original);struct.pack_into('<I',heap,10,0);struct.pack_into('<I',heap,18,0)
                        ax=s.get('allocation',0x6000)
        p.run(terminal=terminal);after=bytes(p.uc.mem_read(p.data,65536));actual_heap=bytes(p.uc.mem_read(p.heap,31))
        if after!=bytes(expected) or actual_heap!=bytes(heap) or bytes(p.uc.mem_read(0x80000,65536))!=bytes(table) or bytes(p.uc.mem_read(0x70000,65536))!=bytes(string):raise ValueError('PFOPEN full memory scalar differs: '+str(s))
        if p.events!=events:raise ValueError('PFOPEN ordered interface requests differ')
        if terminal:
            if p.get('AX')!=ax or p.comparisons!=wanted_comparisons:raise ValueError('PFOPEN result/native compare contracts differ')
            if bool(p.get('EFLAGS')&0x400)!=(bool(s.get('df')) and not searched):raise ValueError('PFOPEN conditional native CLD differs')
        elif not p.comparisons:raise ValueError('PFOPEN budget did not reach real search')
        rows.append(dict(scenario={k:([h.hex() for h in v] if k=='headers' else v.hex() if isinstance(v,bytes) else v) for k,v in s.items()},terminal=terminal,
            ax=p.get('AX') if terminal else None,df=bool(p.get('EFLAGS')&0x400),events=p.events,comparisons=p.comparisons,heap_hex=actual_heap.hex(),writes=p.writes,
            data_before_sha256=sha(before),data_after_sha256=sha(after)))
    for df in (False,True):
        for allocation in (0,0x6000,0x6100):
            for cf in (0,1):observe(dict(df=df,allocation=allocation,allocation_cf=cf))
        for buffer in (0,1,0xffff):
            for cf in (0,1):observe(dict(df=df,buffer=buffer,open_cf=cf,open_errno=0x3456))
        for kind in (0xf388,0x9595,0,0xf300,0x1234):
            for aux in (0,1,255):
                for seek_cf in (0,1):observe(dict(df=df,headers=[header(kind=kind,aux=aux,packed=0xffff,original=0x8000,offset=0xfedcba98)],seek_cf=seek_cf))
        for request in (b'name.dat\0',b'NAME.DAT\0',b'NaMe.DaT\0',b'miss.dat\0',b'\0',b'name.datx\0'):
            observe(dict(df=df,request=request,headers=[header(name=b'miss'),header(name=b'name.dat')]))
        observe(dict(df=df,headers=[header(kind=0,offset=0xcafebabe,aux=255)]))
        observe(dict(df=df,request=b'A'*16+b'\0',headers=[header(name=b'A'*13,packed=0x4141,original=0x0041)]))
        observe(dict(df=df,request=b'NAME.DAT\0',string_offset=0xffff))
        observe(dict(df=df,request=b'name.dat\0',headers=[header(kind=0xf300,name=b'miss'),header()]))
        observe(dict(df=df,endless=True,headers=[],request=b'absent\0'),False)
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('PFOPEN prior math proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_pfopen.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS};local={p:(ROOT/p).read_bytes() for p in LOCAL};inputs.update({p:sha(d) for p,d in local.items()})
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('PFOPEN input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];object_rounds=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('PFOPEN invalid image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz))
        if observations:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('PFOPEN complete bodies/CFG differ')
            tree=Path(path).parents[2]
            op=str(tree/'obj/th03/mainl.obj');obj_data=(ROOT/op).read_bytes();inputs[op]=sha(obj_data);obj=describe_omf(obj_data)
            if not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0']:raise ValueError('PFOPEN cached OMF producer association differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments','record_count','record_counts')}
            if object_rounds and obj['dependency_timestamp_normalized_sha256']!=object_rounds[0]['dependency_timestamp_normalized_sha256']:raise ValueError('PFOPEN cached OMF differs beyond dependency timestamps')
            object_rounds.append(observed['object'])
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached);wanted=local['src/main/formats/pfopen.inl'] if p=='th03/formats/pfopen.asm' else d
                if p.endswith(('.asm','.inc')):wanted=wanted.replace(b'\r\n',b'\n');cached=cached.replace(b'\r\n',b'\n')
                if cached!=wanted:raise ValueError('PFOPEN cached frozen/overlaid provider differs: '+p)
            for p,d in local.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                if cached!=d:raise ValueError('PFOPEN maintained MAIN cached source differs')
            maprows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));carrier=next(row for row in maprows if row['module']=='th03_mainl.asm' and row['segment']==0 and row['size'])
            if not carrier['start']<=0x2b16<0x2c68<=carrier['start']+carrier['size']:raise ValueError('PFOPEN bounded include outside complete carrier')
            target=parse_mz((ROOT/observations[0]['path']).read_bytes());observed['carrier']=carrier
            observed['comparisons']={n:extent_observation(target,mz,dict(start=a,size=z,segment=0,offset=a)) for n,a,z in [('open',0x2b16,282),('compare',0x2c30,56)]}
            if any(not c['raw_slice_equal'] or not c['ordered_relocations_equal'] for c in observed['comparisons'].values()):raise ValueError('PFOPEN complete raw/relocation diagnostics differ')
            def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('data_before_sha256','data_after_sha256')} for row in cpu]
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']):raise ValueError('PFOPEN target/cached CPU differs')
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('PFOPEN canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('PFOPEN frozen provider changed')
    result=dict(kind='th03-mainl-complete-pfopen-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},producer_overlay={'th03/formats/pfopen.asm':'src/main/formats/pfopen.inl'},
        observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL PFOPEN281/producer1/native compare56 and explicit buffer interfaces:',args.output)


if __name__=='__main__':main()
