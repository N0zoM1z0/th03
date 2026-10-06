#!/usr/bin/env python3
"""Close independent MAINL direct-link CODE gaps; keep acceptance separate."""
import argparse
from collections import Counter
from datetime import datetime,timezone
from importlib.metadata import version
import json
from pathlib import Path
import re
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from inventory_rec98_th03 import frozen_files,link_roots
from lib.omf import parse_omf,describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact
from review_th03_decoded_code import code_rows,extent_observation
from review_th03_mainl_cutscene import Probe,REVISION,sha
from review_th03_mainl_snow import u16
from review_th03_mainl_graphics import COLD,COLD_SHA
from review_th03_mainl_heap import cached_provider
import review_th03_mainl_vsync as vsync

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-mainl-crt-break-review-20261006.json'
PROOF_SHA='fb467a0a852767eba985dbb5ca76ad674cb3b65d165cab4d7ffa3d006af2fbd5'
CS,DS=0xc7e,0xe3f
RANGES=[('planes',2,41,0),('delay',0x372,21,2)]
PRODUCERS={0x49:'th02/snd_mode.c',0x83:'th02/snd_pmdr.c',0x9f:'th02/snd_dlyv.c',0x155:'th03/vector.cpp',
           0x2a7:'th03/cdg_put.asm',0x371:'th03/cdg_put.asm',0x669:'th02/snd_se_r.cpp',0xfa3:'th03/cdg_p_na.asm'}
FORWARDERS={'th01/vplanset.cpp':'src/main/hardware/vram_planes.cpp','th02/frmdely1.cpp':'src/main/hardware/frame_delay.cpp',
            'th03/cfg_lres.cpp':'src/main/formats/cfg_lres.cpp','th03/exit.cpp':'src/main/core/exit.cpp',
            'th03/initmain.cpp':'src/main/core/initmain.cpp','th03/inp_m_w.cpp':'src/main/hardware/input_modes.cpp',
            'th03/input_s.cpp':'src/main/hardware/input_sense.cpp','th03/pi_load.cpp':'src/main/formats/pi_load.cpp',
            'th03/snd_kaja.cpp':'src/main/sound/kaja.cpp','th03/snd_se.cpp':'src/main/sound/se.cpp'}
COPIES={'th03/hfliplut.asm':'src/main/formats/hfliplut.asm'}
SUPPORT=['th01/hardware/vplanset.cpp','th01/hardware/vplanset.h','th02/hardware/frmdely1.cpp','th02/hardware/frmdelay.h',
         'planar.h','platform.h','x86real.h','libs/master.lib/master.hpp','libs/master.lib/vsync.asm',
         'libs/master.lib/vsync[bss].asm','libs/master.lib/func.hpp','libs/master.lib/func.inc','libs/master.lib/macros.inc','Tupfile.lua']
PLANES,COUNT1,COUNT2,ACC,DELAY,PROC=0x1c60,vsync.COUNT1,vsync.COUNT2,vsync.ACC,vsync.DELAY,vsync.PROC
GPRS=('AX','BX','CX','DX','BP','SI','DI','DS','ES')


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[];bounds=set();returns={}
    for name,a,z,cleanup in RANGES:
        body=image[CS*16+a:CS*16+a+z];ins=list(decoder.disasm(body,a));local={i.address for i in ins}
        if len(body)!=z or not ins or sum(i.size for i in ins)!=z or (ins[-1].mnemonic,ins[-1].op_str)!=('retf',str(cleanup) if cleanup else ''):
            raise ValueError('linked tail complete body/far cleanup differs')
        edges=[]
        for i in ins:
            if i.mnemonic in ('ret','retf'):
                if (i.mnemonic,i.op_str)!=('retf',str(cleanup) if cleanup else ''):raise ValueError('linked tail interior cleanup differs')
                returns[i.address]=cleanup
            if i.mnemonic in ('in','out','int','call','lcall','ljmp'):raise ValueError('linked tail unknown interface')
            if i.mnemonic.startswith(('j','loop')):
                if len(i.operands)!=1 or i.operands[0].type!=X86_OP_IMM or i.operands[0].imm not in local:
                    raise ValueError('linked tail branch enters operand/neighbor/producer')
                edges.append(dict(site=i.address,destination=i.operands[0].imm))
        rows.append(dict(name=name,segment=CS,offset=a,size=z,cleanup=cleanup,instructions=len(ins),sha256=sha(body),edges=edges));bounds|=local
    if any(image[CS*16+a:CS*16+a+1]!=b'\x90' for a in PRODUCERS):raise ValueError('linked tail producer byte differs')
    context=vsync.analyze(image);irq=next(r for r in context['bodies'] if r['name']=='irq')
    irq_bounds={i.address for i in decoder.disasm(image[irq['offset']:irq['offset']+irq['size']],irq['offset'])}
    return dict(bodies=rows,bounds=sorted(bounds),returns=returns,body_bytes=62,producer_bytes=8,new_bytes=70,
                irq_context=irq,irq_bounds=sorted(irq_bounds),producers=PRODUCERS)


def object_code(data):
    """Read complete emitted SHARED CODE from checksummed OMF, without fixes."""
    records=parse_omf(data);names=[''];segments=[]
    def index(payload,at):
        if at>=len(payload):raise ValueError('linked tail truncated OMF index')
        if payload[at]&128:
            if at+1>=len(payload):raise ValueError('linked tail truncated OMF index')
            return ((payload[at]&127)<<8)|payload[at+1],at+2
        return payload[at],at+1
    for r in records:
        if r.record_type==0x96:
            at=0
            while at<len(r.data):
                z=r.data[at];at+=1
                if at+z>len(r.data):raise ValueError('linked tail truncated OMF name')
                names.append(r.data[at:at+z].decode('ascii'));at+=z
        if r.record_type==0x98:
            if r.data[0]>>5==0:raise ValueError('linked tail unsupported absolute segment')
            size=int.from_bytes(r.data[1:3],'little');name,at=index(r.data,3);kind,at=index(r.data,at)
            if name>=len(names) or kind>=len(names):raise ValueError('linked tail OMF name index differs')
            segments.append(dict(size=size,name=names[name],kind=names[kind]))
    selected=[(i+1,s) for i,s in enumerate(segments) if s['name']=='SHARED' and s['kind']=='CODE' and s['size']]
    if len(selected)!=1:raise ValueError('linked tail SHARED CODE ownership differs')
    segment,meta=selected[0];code=bytearray(meta['size']);owned=set()
    for r in records:
        if r.record_type==0xa2:raise ValueError('linked tail unsupported iterated OMF data')
        if r.record_type!=0xa0:continue
        seg,at=index(r.data,0)
        if seg!=segment:continue
        if at+2>len(r.data):raise ValueError('linked tail truncated LEDATA offset')
        offset=int.from_bytes(r.data[at:at+2],'little');payload=r.data[at+2:];positions=set(range(offset,offset+len(payload)))
        if offset+len(payload)>len(code) or positions&owned:raise ValueError('linked tail OMF CODE overlap/bounds differ')
        code[offset:offset+len(payload)]=payload;owned|=positions
    if len(owned)!=len(code):raise ValueError('linked tail OMF CODE emission incomplete')
    return bytes(code)


class TailProbe(Probe):
    def __init__(self,mz,scenario):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x2c7e0,0x2e3f0,0x40000
        self.s=scenario;self.meta=analyze(mz.program_image);self.errors=[];self.stop=False;self.frame=None;self.irq=None
        self.irq_returning=False;self.resuming=False;self.polls=0;self.reason=None;self.native=Counter();self.visited=set();self.writes=[];self.ports=[];self.instructions=0
        self.uc.mem_write(self.data+PLANES,bytes(scenario.get('planes',[(i*13+7)&255 for i in range(16)])))
        for a,key,default in ((COUNT1,'count1',0xbeef),(COUNT2,'count2',65535),(ACC,'acc',0),(DELAY,'delay',0)):
            self.uc.mem_write(self.data+a,struct.pack('<H',scenario.get(key,default)))
        self.uc.mem_write(self.data+PROC,b'\0'*4)
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if self.get('SS')!=0x4000:raise ValueError('linked tail stack segment alias')
            self.instructions+=1
            if self.irq_returning:
                f=self.irq
                if self.get('CS')!=f['cs'] or address!=f['cs']*16+f['ip'] or self.get('SP')!=f['sp'] or self.get('EFLAGS')&65535!=f['flags'] or any(self.get(r)!=v for r,v in f['regs'].items()):
                    raise ValueError('linked tail native IRET restoration differs')
                self.irq=None;self.irq_returning=False;self.reason='irq-done';uc.emu_stop();return
            if self.get('CS')==0x2c7e:
                off=address-self.code
                if off==0xff00:
                    if self.frame or self.irq:raise ValueError('linked tail unfinished native frame')
                    self.stop=True;self.reason='return';uc.emu_stop();return
                if off not in self.meta['bounds']:raise ValueError('CPU escaped linked tail instruction boundaries')
                if off in (2,0x372):
                    if not self.frame or self.get('SP')!=self.frame['sp'] or tuple(struct.unpack('<2H',uc.mem_read(self.stack+self.get('SP'),4)))!=(0xff00,0x2c7e):
                        raise ValueError('linked tail native public entry frame differs')
                    self.native['planes' if off==2 else 'delay']+=1
                if off==0x37b:
                    if self.resuming:self.resuming=False
                    else:
                        if self.polls==scenario.get('limit',128):self.reason='prefix';uc.emu_stop();return
                        self.polls+=1
                        if self.get('EFLAGS')&512 and self.polls%scenario.get('period',1)==0:
                            self.reason='deliver';uc.emu_stop();return
                self.visited.add(CS*65536+off)
                if off in self.meta['returns']:
                    if not self.frame or self.get('SP')!=self.frame['sp'] or tuple(struct.unpack('<2H',uc.mem_read(self.stack+self.get('SP'),4)))!=(0xff00,0x2c7e):
                        raise ValueError('linked tail native far return frame differs')
                    self.frame=None
            elif self.get('CS')==0x2000:
                off=address-0x20000
                if off not in self.meta['irq_bounds'] or not self.irq:raise ValueError('CPU escaped connected IRQ context')
                if off==0x1fe2:
                    if self.get('SP')!=u16(self.irq['sp']-6) or tuple(struct.unpack('<3H',uc.mem_read(self.stack+self.get('SP'),6)))!=(self.irq['ip'],self.irq['cs'],self.irq['flags']):
                        raise ValueError('linked tail native IRQ entry frame differs')
                    self.native['irq']+=1
                if off==0x2008:raise ValueError('linked tail callback is outside declared no-callback IRQ context')
                self.visited.add(off)
                if off==0x201b:
                    if self.get('SP')!=u16(self.irq['sp']-6) or tuple(struct.unpack('<3H',uc.mem_read(self.stack+self.get('SP'),6)))!=(self.irq['ip'],self.irq['cs'],self.irq['flags']):
                        raise ValueError('linked tail native IRET frame differs')
                    self.irq_returning=True
            else:raise ValueError('linked tail CODE segment alias')
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            if not any(self.data+a<=address and address+size<=self.data+a+z for a,z in ((PLANES,16),(COUNT1,4),(ACC,2))):
                raise ValueError('linked tail write outside complete planes/IRQ state span')
            self.writes.append([address,size,value])
        def output(uc,port,width,value,user):
            if self.get('CS')!=0x2000 or {0x2016:0,0x2018:0x64}.get(self.get('IP'))!=port or width!=1 or value!=0x20 or self.get('EFLAGS')&512:
                raise ValueError('linked tail unknown IRQ port/site/width/live IF')
            self.ports.append([port,value,bool(self.get('EFLAGS')&512),bool(self.get('EFLAGS')&1024)])
        def forbidden(*args):raise ValueError('linked tail unexpected interrupt/input interface')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(forbidden))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(forbidden,0),None,1,0,reg.UC_X86_INS_IN)
    def run(self,name,args=(),budget=5000000):
        if name not in ('planes','delay'):raise ValueError('linked tail private IRQ requires complete public caller')
        self.errors.clear();self.stop=False;self.polls=0;self.irq=None;self.irq_returning=False;self.resuming=False;self.instructions=0
        flags=2|(512 if self.s.get('if',True) else 0)|(1024 if self.s.get('df') else 0)
        saved=dict(CS=0x2c7e,DS=0x2e3f,SS=0x4000,ES=0x3333,AX=0x1111,BX=0x2222,CX=0x3333,DX=0x4444,BP=0x7777,SI=0x1357,DI=0x2468,SP=0xffc0,EFLAGS=flags)
        for r,v in saved.items():self.set(r,v)
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2c7e,*args));self.frame=dict(sp=0xffc0)
        begin=self.code+(2 if name=='planes' else 0x372)
        while self.instructions<budget:
            self.reason=None;self.uc.emu_start(begin,0x100000,count=budget-self.instructions)
            if self.errors:raise ValueError(self.errors[0])
            if self.reason in ('return','prefix'):break
            if self.reason=='deliver':
                self.irq=dict(cs=self.get('CS'),ip=0x37b,sp=self.get('SP'),flags=self.get('EFLAGS')&65535,regs={r:self.get(r) for r in GPRS})
                self.uc.mem_write(self.stack+u16(self.get('SP')-6),struct.pack('<3H',self.irq['ip'],self.irq['cs'],self.irq['flags']))
                self.set('SP',u16(self.get('SP')-6));self.set('EFLAGS',self.get('EFLAGS')&~0x300);self.set('CS',0x2000);self.set('IP',0x1fe2);begin=0x21fe2
            elif self.reason=='irq-done':self.resuming=True;begin=self.code+0x37b
            else:raise ValueError('linked tail terminal/budget differs')
        else:raise ValueError('linked tail terminal/budget differs')
        if self.stop:
            if self.get('SP')!=0xffc4+(2 if name=='delay' else 0) or any(self.get(r)!=saved[r] for r in ('BP','SI','DI','DS','ES')):
                raise ValueError('linked tail far cleanup/preserved registers differ')
        elif self.reason!='prefix' or name!='delay' or self.polls!=self.s.get('limit',128) or not self.frame or self.irq:
            raise ValueError('linked tail semantic prefix phase differs')
        if self.get('EFLAGS')&1536!=flags&1536:raise ValueError('linked tail IF/DF preservation differs')


def matrix(mz):
    rows=[]
    def observe(name,s,frames=0):
        p=TailProbe(mz,s);memory=bytearray(p.uc.mem_read(0,0x100000));before=sha(bytes(memory));writes=[];ports=[];native=Counter({name:1});polls=0;terminal=True
        def word(a):return int.from_bytes(memory[p.data+a:p.data+a+2],'little')
        def put(a,value,width=2):
            value&=(1<<(width*8))-1;memory[p.data+a:p.data+a+width]=value.to_bytes(width,'little');writes.append([p.data+a,width,value])
        if name=='planes':
            for i,segment in enumerate((0xa800,0xb000,0xb800,0xe000)):put(PLANES+i*4,segment<<16,4)
        else:
            put(COUNT1,0)
            while True:
                if polls==s.get('limit',128):terminal=False;break
                polls+=1
                if s.get('if',True) and polls%s.get('period',1)==0:
                    native['irq']+=1;total=word(ACC)+word(DELAY);put(ACC,total)
                    if total<65536:put(COUNT1,word(COUNT1)+1);put(COUNT2,word(COUNT2)+1)
                    ports.extend([[0,32,False,bool(s.get('df'))],[100,32,False,bool(s.get('df'))]])
                if word(COUNT1)>=frames:break
        p.run(name,[] if name=='planes' else [frames])
        actual=bytes(p.uc.mem_read(0,0x100000));wanted=bytes(memory)
        if p.stop!=terminal or p.polls!=polls or p.native!=native or p.writes!=writes or p.ports!=ports:
            raise ValueError('linked tail independent terminal/IRQ/stores/ports differ: '+str((name,s,frames,p.stop,terminal,p.polls,p.native,native)))
        if actual[:p.stack]!=wanted[:p.stack] or actual[p.stack+65536:]!=wanted[p.stack+65536:]:raise ValueError('linked tail whole physical memory outside stack differs')
        rows.append(dict(function=name,scenario=s,frames=frames,terminal=terminal,polls=polls,native_entries=dict(native),visited=sorted(p.visited),
                         stores=len(writes),stores_sha256=sha(json.dumps(writes,separators=(',',':')).encode()),ports=len(ports),ports_sha256=sha(json.dumps(ports,separators=(',',':')).encode()),
                         memory_before_sha256=before,memory_after_sha256=sha(wanted)))
    for irq in (False,True):
        for df in (False,True):
            for initial in ([0]*16,[255]*16,list(range(16))):observe('planes',dict(df=df,planes=initial,**{'if':irq}))
            for period in (1,2,3):
                for delay in (0,1,32768,65535):
                    for frames in (0,1,2,16,127,128,255,32767,32768,65535):
                        observe('delay',dict(df=df,period=period,delay=delay,acc=65535 if delay==32768 else 0,limit=128,**{'if':irq}),frames)
    observe('delay',dict(period=1,delay=0,limit=65536,df=True),65535)
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes();cold_raw=(ROOT/COLD).read_bytes()
    if sha(raw)!=PROOF_SHA or sha(cold_raw)!=COLD_SHA:raise ValueError('linked tail prior/cold proof differs')
    proof,cold=json.loads(raw),json.loads(cold_raw);frozen=frozen_files(REVISION);direct=sorted(link_roots(frozen)['th03-mainl'])
    inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_linked_tail.py':sha(Path(__file__).read_bytes()),
            'tests/test_mainl_linked_tail_review.py':sha((ROOT/'tests/test_mainl_linked_tail_review.py').read_bytes())}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('linked tail input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];target=parse_mz((ROOT/proof['observations'][0]['path']).read_bytes())
    for index,prior in enumerate(proof['observations']):
        path=prior['path'];mz=parse_mz((ROOT/path).read_bytes());observed=dict(path=path,analysis=analyze(mz.program_image))
        if not mz.valid:raise ValueError('linked tail invalid image')
        if index:
            tree=Path(path).parents[2];observed['source_lineage']={}
            for p in sorted(set(direct+SUPPORT)):
                cp=str(tree/p);data=(ROOT/cp).read_bytes();inputs[cp]=sha(data);wanted=frozen[p]
                if p in FORWARDERS:wanted=f'#include "{FORWARDERS[p]}"\n'.encode()
                elif p in COPIES:wanted=(ROOT/tree/COPIES[p]).read_bytes()
                elif p=='Tupfile.lua':wanted=cached_provider(p,wanted)
                if p.endswith(('.asm','.inc')):data=data.replace(b'\r\n',b'\n');wanted=wanted.replace(b'\r\n',b'\n')
                if data!=wanted:raise ValueError('linked tail frozen/declared MAIN provider differs: '+p)
                observed['source_lineage'][p]=dict(frozen_sha256=sha(frozen[p]),cached_sha256=inputs[cp],forwarder=FORWARDERS.get(p),copy=COPIES.get(p))
                local=FORWARDERS.get(p) or COPIES.get(p)
                if local:
                    lp=str(tree/local);data=(ROOT/lp).read_bytes();inputs[lp]=sha(data)
                    if sha(data)!=cold['source_inputs'][local]:raise ValueError('linked tail archived maintained MAIN provider differs')
            mappath=str(tree/'obj/th03/mainl.map');text=(ROOT/mappath).read_text();inputs[mappath]=sha((ROOT/mappath).read_bytes());carriers=code_rows(text,len(mz.program_image))
            observed['comparisons']={};observed['objects']={}
            for module in sorted(set(PRODUCERS.values())|{'th01/vplanset.cpp','th02/frmdely1.cpp'}):
                carrier=next(r for r in carriers if r['module']==module and r['size']);objpath=str(tree/'obj'/Path(module).with_suffix('.obj'));data=(ROOT/objpath).read_bytes();inputs[objpath]=sha(data);obj=describe_omf(data)
                if not obj['valid'] or obj['dependency_timestamp_normalized_sha256']!=cold['rounds'][index-1]['all_objects'][str(Path('obj')/Path(module).with_suffix('.obj'))]:raise ValueError('linked tail pinned cold OMF differs')
                emitted=object_code(data)
                if len(emitted)!=carrier['size']:raise ValueError('linked tail complete OMF/MAP CODE size differs')
                for off,owner in PRODUCERS.items():
                    if owner==module and (not carrier['offset']<=off<carrier['offset']+len(emitted) or emitted[off-carrier['offset']]!=0x90):raise ValueError('linked tail OMF producer ownership differs')
                observed['objects'][module]=dict(path=objpath,sha256=sha(data),normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'],emitted_code_sha256=sha(emitted))
            for name,a,z,cleanup in RANGES:
                row=dict(segment=CS,offset=a,start=CS*16+a,size=z);observed['comparisons'][name]=extent_observation(target,mz,row)
                symbol=r'vram_planes_set\(\)' if name=='planes' else r'frame_delay\(int\)'
                coords={(int(s,16),int(o,16)) for s,o in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+symbol+r'\s*$',text,re.MULTILINE)}
                if coords!={(CS,a)}:raise ValueError('linked tail public MAP entry differs')
            for a in PRODUCERS:observed['comparisons']['producer-'+hex(a)]=extent_observation(target,mz,dict(segment=CS,offset=a,start=CS*16+a,size=1))
            observed['comparisons']['irq-context']=extent_observation(target,mz,dict(segment=0,offset=0x1fe2,start=0x1fe2,size=58))
            if any(not r['raw_slice_equal'] or not r['ordered_relocations_equal'] for r in observed['comparisons'].values()):raise ValueError('linked tail raw/ordered relocations differ')
        observed['cpu']=matrix(mz);visited={a for r in observed['cpu'] for a in r['visited']};owned={CS*65536+a for a in observed['analysis']['bounds']}
        observed['instruction_coverage']=dict(new_instructions=len(owned),visited=len(owned&visited),unvisited=sorted(owned-visited))
        normalize=lambda rows:[{k:v for k,v in r.items() if k not in ('memory_before_sha256','memory_after_sha256')} for r in rows]
        if index and (observed['analysis']!=observations[0]['analysis'] or normalize(observed['cpu'])!=normalize(observations[0]['cpu'])):raise ValueError('linked tail target/cold CPU/partition differs')
        observations.append(observed);print('Reviewed',path,len(observed['cpu']),'calls',observed['instruction_coverage'],flush=True)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('linked tail canonical stored target changed')
    if {p:sha(d) for p,d in frozen_files(REVISION).items() if p in set(direct+SUPPORT)}!={p:sha(frozen[p]) for p in set(direct+SUPPORT)}:raise ValueError('linked tail frozen providers changed')
    result=dict(kind='th03-mainl-remaining-direct-link-code-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,observations=observations,
                frozen_direct_sources=direct,main_forwarders=FORWARDERS,main_source_copies=COPIES,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),
                diagnostic_checks_pass=True,new_build=False,source_acceptance=False,exact_acceptance=False,
                notes='70newdecodedbytes;PI0529remainsunowned,priorIRQ58contextonly. Host poll schedule manually delivers native no-callback IRQ/IRET with IF gating; no hardware/asynchronous eligibility/complete callback/DATA/BSS/wholeproduct/DIET/source/exact acceptance.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL direct-link CODE tail; source/exact open:',args.output)


if __name__=='__main__':main()
