#!/usr/bin/env python3
"""Complete MAINL stack allocator with native heap/assignment collision context."""
import argparse
from datetime import datetime,timezone
from importlib.metadata import version
import json
from pathlib import Path
import struct
import subprocess
from collections import Counter
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact
from review_th03_decoded_code import code_rows,extent_observation
from review_th03_mainl_cutscene import Probe,REVISION,sha
from review_th03_mainl_snow import u16
import review_th03_mainl_heap as heap
from review_th03_mainl_heap import TOP,OWN,ID,RESERVE,OUT,HEAP,HOLE,END,cached_provider,BUILD_REMAPS

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-mainl-heap-review-20261006.json'
PROOF_SHA256='42b80d31600405985b8e87b7618e662062a7850fc24c87149a18a548da0a3e49'
OWN_RANGES=[('release',0x1eaa,15,2),('get',0x1eba,59,2)]
RANGES=OWN_RANGES+heap.RANGES
NAMES={**heap.NAMES,0x1eaa:'release',0x1ec0:'get'}
CALLS={**heap.CALLS,0x1ebb:0x2186};DOS=heap.DOS
ALIGNMENT={0x1eb9:0x90,0x1ef5:0x90}
PROVIDERS=heap.PROVIDERS+['libs/master.lib/smem_release.asm','libs/master.lib/smem_wget.asm']


def analyze(image):
    context=heap.analyze(image);decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[];returns=dict(context['returns'])
    for name,start,size,cleanup in OWN_RANGES:
        body=image[start:start+size]
        if len(body)!=size:raise ValueError('smem complete include body differs')
        ins=list(decoder.disasm(body,start));bounds={i.address for i in ins};edges=[]
        if not ins or sum(i.size for i in ins)!=size or (ins[-1].mnemonic,ins[-1].op_str)!=('retf','2'):raise ValueError('smem complete body/far cleanup differs')
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf'):
                if (i.mnemonic,i.op_str)!=('retf','2'):raise ValueError('smem interior return differs')
                returns[i.address]=2
            if i.mnemonic in ('in','out','int'):raise ValueError('smem unexpected port/interrupt')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('smem unknown indirect edge')
            if i.mnemonic=='lcall':raise ValueError('smem unknown far interface')
            dest=i.operands[0].imm
            if i.mnemonic=='call':
                if i.address!=0x1ebb or dest!=0x2186:raise ValueError('smem unknown native call site/target')
                if not j or ins[j-1].bytes!=b'\x0e':raise ValueError('smem far call lacks PUSH CS')
            elif dest not in bounds:raise ValueError('smem branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=start,size=size,instructions=len(ins),sha256=sha(body),cleanup=cleanup,public_entry=0x1ec0 if name=='get' else start,edges=edges))
    if any(image[a:a+1]!=bytes([v]) for a,v in ALIGNMENT.items()):raise ValueError('smem complete producer alignment differs')
    if image[0x1eba:0x1ec0]!=b'\x0e\xe8\xc8\x02\x72\x2f':raise ValueError('smem private assignment prefix differs')
    return dict(bodies=rows,body_bytes=74,producer_bytes=2,complete_include_bytes=76,context_bytes=628,context=context,returns=returns,producers=ALIGNMENT,private_prefix=dict(offset=0x1eba,size=6))


class SmemProbe(Probe):
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
                if self.get('CS')!=0x2000:raise ValueError('smem terminal segment alias')
                if self.frames:raise ValueError('smem unfinished native frame')
                self.stop=True;uc.emu_stop();return
            off=address-self.code
            if self.get('CS')!=0x2000 or not any(a<=off<a+n for _,a,n,_ in RANGES):raise ValueError('CPU escaped smem bodies/segment alias')
            if off in NAMES and not (off==0x1ec0 and self.frames and self.frames[-1][0]==0x1ec0):
                sp=self.get('SP');ip,cs=struct.unpack('<2H',uc.mem_read(self.stack+sp,4));direct=not self.frames and off==self.direct and ip==0xff00
                if cs!=0x2000 or (not direct and CALLS.get(ip-3)!=off):raise ValueError('smem native far frame differs')
                self.frames.append((off,sp,ip,cs,2 if off==0x1ec0 else next(z for _,a,_,z in RANGES if a==off)));self.native[NAMES[off]]+=1
            if off in self.returns:
                if not self.frames:raise ValueError('smem orphan far return')
                _,sp,ip,cs,cleanup=self.frames.pop()
                if self.get('SP')!=sp or tuple(struct.unpack('<2H',uc.mem_read(self.stack+sp,4)))!=(ip,cs) or self.returns[off]!=cleanup:raise ValueError('smem native return frame differs')
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            state=any(self.data+a<=address and address+size<=self.data+a+z for a,z in ((TOP,6),(OUT,8)))
            header=size==2 and address%16 in (0,2,4) and (0x50000<=address and address+size<=0x90000 or any(seg*16<=address and address+size<=seg*16+6 for seg,_,_,_ in s.get('blocks',[])))
            if not state and not header:raise ValueError('smem write outside owned state/header')
            self.write_count+=1
        def intr(uc,number,user):
            site=u16(self.get('IP')-2);ah=self.get('AH')
            if number!=0x21 or self.get('CS')!=0x2000 or DOS.get(site)!=ah:raise ValueError('smem unknown DOS request/site')
            if ah==0x48:
                i=self.dos_index;self.dos_index+=1;items=s.get('dos_allocs',[]);query=site==0x218c
                item=items[i] if i<len(items) else {};ax=item.get('ax',8 if query else 0x6000);cf=item.get('cf',1 if query else 0);bx=item.get('bx',s.get('largest',0x200) if query else self.get('BX'))
                self.events.append(dict(site=site,name='dos_allocate',size=self.get('BX'),ax=ax,bx=bx,cf=cf));self.set('BX',bx)
            else:
                ax=s.get('dos_free_ax',7);cf=s.get('dos_free_cf',1);self.events.append(dict(site=site,name='dos_free',segment=self.get('ES'),ax=ax,cf=cf))
            self.set('AX',ax);self.set('EFLAGS',(self.get('EFLAGS')&~1)|cf)
        def out(uc,port,width,value,user):raise ValueError('smem unexpected output port')
        def inp(uc,port,width,user):raise ValueError('smem unexpected input port')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(out),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)

    def run(self,name,args=(),budget=100000):
        _,start,_,cleanup=next(r for r in RANGES if r[0]==name);start=0x1ec0 if name=='get' else start;self.direct=start;self.stop=False;self.errors.clear();self.frames.clear()
        for r,v in dict(CS=0x2000,DS=0x2e3f,SS=0x4000,ES=0x3333,AX=0x1111,BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,SP=0xffc0,EFLAGS=self.s.get('initial_flags',0x202)|(0x400 if self.s.get('df') else 0)|self.s.get('initial_cf',0)).items():self.set(r,v)
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2000,*args));self.uc.emu_start(self.code+start,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('smem terminal/budget differs')
        regs=['BX','CX','DX','BP','SI','DI','DS']+([] if name=='unassign' else ['ES'])
        expected=dict(BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,DS=0x2e3f,ES=0x3333)
        if name=='release':regs.append('AX');expected['AX']=0x1111
        if self.get('SP')!=0xffc4+cleanup or any(self.get(r)!=expected[r] for r in regs):raise ValueError('smem far cleanup/callee-saved differs')
        if bool(self.get('EFLAGS')&0x400)!=bool(self.s.get('df')):raise ValueError('smem DF differs')
        if name=='release' and self.get('EFLAGS')&0xfd5!=(self.s.get('initial_flags',0x202)|(0x400 if self.s.get('df') else 0)|self.s.get('initial_cf',0))&0xfd5:raise ValueError('smem release flags differ')


class Scalar(heap.Scalar):
    def run(self,name,args=()):
        if name=='release':
            self.native[name]+=1;self.put(END,args[0]);return 0x1111,(self.s.get('initial_flags',0x202)&1)|self.s.get('initial_cf',0)
        if name!='get':return super().run(name,args)
        self.native[name]+=1
        for _ in range(100):
            if self.get(TOP):break
            _,cf=self.run('assign_all')
            if cf:return 65528,1
        else:raise ValueError('scalar smem zero-top assignment budget')
        old=self.get(END);new=old+((args[0]+15)>>4)
        if new>65535 or new>self.get(HEAP):return 65528,1
        self.put(END,new);return old,0


def matrix(mz):
    rows=[]
    def observe(name,s,steps):
        p=SmemProbe(mz,s);scalar=Scalar(p);before=sha(bytes(scalar.mem));results=[];saved=[]
        for step in steps:
            fn=step['function'];args=step.get('args',[])
            if 'from_result' in step:args=[saved[step['from_result']]]
            ax,cf=scalar.run(fn,args);p.run(fn,args)
            if (ax is not None and p.get('AX')!=ax) or p.get('EFLAGS')&1!=cf or p.events!=scalar.events or p.native!=scalar.native:raise ValueError('smem result/CF/native/DOS scalar differs: '+str((s,step,p.get('AX'),ax,p.get('EFLAGS')&1,cf,p.events,scalar.events)))
            actual=bytes(p.uc.mem_read(0,0x100000))
            if actual[:p.stack]!=scalar.mem[:p.stack] or actual[p.stack+65536:]!=scalar.mem[p.stack+65536:]:
                changed=[i for i,(a,b) in enumerate(zip(actual,scalar.mem)) if a!=b and not p.stack<=i<p.stack+65536]
                raise ValueError('smem full physical memory scalar differs: '+str((s,step,changed[:20])))
            saved.append(p.get('AX'));results.append(dict(function=fn,args=args,ax=ax,cf=cf,end=scalar.get(END),heap=scalar.get(HEAP),id=scalar.get(ID),top=scalar.get(TOP),own=scalar.get(OWN)))
        rows.append(dict(function=name,scenario=s,steps=results,top_level_calls=len(results),events=p.events,native_entries=dict(p.native),write_count=p.write_count,memory_before_sha256=before,memory_after_sha256=sha(bytes(scalar.mem))))
    for df in (False,True):
        for end in (0,1,0x6000,0x60ff,0x6100,0x6101,0xfff0,0xffff):
            for size in (0,1,2,15,16,17,255,256,257,4095,4096,4097,65520,65521,65535):
                observe('get',dict(df=df,end=end),[dict(function='get',args=[size])])
        for cf in (0,1):
            for end in (0,1,0x6000,0x6100,0xffff):
                for top in (0,0x6000):observe('release',dict(df=df,top=top,initial_cf=cf),[dict(function='release',args=[end])])
        for bits in range(32):
            flags=0x202|sum(flag for index,flag in enumerate((4,16,64,128,2048)) if bits&(1<<index))
            for cf in (0,1):observe('release-flags',dict(df=df,initial_cf=cf,initial_flags=flags),[dict(function='release',args=[0x6000])])
        for size in (0,1,16,4096,65535):
            for cf in (0,1):observe('lazy',dict(df=df,top=0,dos_allocs=[dict(cf=1),dict(cf=cf)]),[dict(function='get',args=[size])])
        for first_cf in (0,1):
            for second_cf in (0,1):
                for ax in (0,8,0x6000):observe('lazy-status',dict(df=df,top=0,dos_allocs=[dict(cf=first_cf),dict(cf=second_cf,ax=ax)]),[dict(function='get',args=[17])])
        for reserve in (0,256,65535):
            for largest in (0,256,512):observe('reserve',dict(df=df,top=0,reserve=reserve,largest=largest),[dict(function='get',args=[0]),dict(function='get',args=[1])])
        for release in (0,0x5fff,0x6000,0x60ff,0x6100,0x6200,0xffff):
            observe('release-get-chain',dict(df=df),[dict(function='get',args=[256]),dict(function='release',args=[release]),dict(function='get',args=[0]),dict(function='get',args=[16])])
        observe('collision-chain',dict(df=df),[dict(function='allocate',args=[8]),dict(function='get',args=[512]),dict(function='allocate',args=[222]),dict(function='release',from_result=1),dict(function='free',from_result=0),dict(function='allocate',args=[255]),dict(function='get',args=[0]),dict(function='get',args=[1]),dict(function='free',from_result=5),dict(function='get',args=[4096]),dict(function='get',args=[1]),dict(function='release',from_result=9),dict(function='unassign')])
        observe('reuse-stack-chain',dict(df=df),[dict(function='get',args=[17]),dict(function='get',args=[17]),dict(function='release',from_result=0),dict(function='get',args=[17]),dict(function='get',args=[0]),dict(function='unassign')])
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('smem prior smem proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_smem.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('smem input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];objects=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('smem invalid image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz))
        if observations:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('smem complete body/CFG differs')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                expected=cached_provider(p,d)
                actual=cached.replace(b'\r\n',b'\n') if p.endswith(('.asm','.inc')) else cached
                if actual!=expected:raise ValueError('smem cached frozen provider differs: '+p)
            op=str(tree/'obj/th03/mainl.obj');obj_data=(ROOT/op).read_bytes();inputs[op]=sha(obj_data);obj=describe_omf(obj_data)
            if not obj['valid'] or obj['module_name']!='th03_mainl.asm' or obj['translator_comments']!=['Turbo Assembler  Version 5.0']:raise ValueError('smem cached root OMF identity differs')
            observed['object']={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments','record_count','record_counts')}
            if objects and obj['dependency_timestamp_normalized_sha256']!=objects[0]['dependency_timestamp_normalized_sha256']:raise ValueError('smem cached OMF differs beyond dependency timestamps')
            objects.append(observed['object']);maprows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));carrier=next(row for row in maprows if row['module']=='th03_mainl.asm' and row['segment']==0 and row['size'])
            if not all(carrier['start']<=a<a+n<=carrier['start']+carrier['size'] for _,a,n,_ in RANGES):raise ValueError('smem includes outside complete root carrier')
            observed['carrier']=carrier;target=parse_mz((ROOT/observations[0]['path']).read_bytes())
            extents=[('complete-stack-includes',0x1eaa,76),('prior-heap-context',0x210a,628)]
            observed['comparisons']={n:extent_observation(target,mz,dict(start=a,size=z,segment=0,offset=a)) for n,a,z in extents}
            if any(not x['raw_slice_equal'] or not x['ordered_relocations_equal'] for x in observed['comparisons'].values()):raise ValueError('smem complete raw/ordered relocations differ')
            def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('memory_before_sha256','memory_after_sha256')} for row in cpu]
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']):raise ValueError('smem target/cached CPU differs')
        observations.append(observed);print('Reviewed',path,len(observed['cpu']),'scenarios',flush=True)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('smem canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('smem frozen provider changed')
    result=dict(kind='th03-mainl-complete-smem-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},build_scaffold_main_remaps=BUILD_REMAPS,observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL complete stack76bytes, native heap628context and explicit DOS:',args.output)


if __name__=='__main__':main()
