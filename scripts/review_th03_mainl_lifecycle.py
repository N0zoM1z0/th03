#!/usr/bin/env python3
"""MAINL lifecycle candidates: actual CODE, declared library interfaces only."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import struct
import subprocess

from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.pc98 import parse_mz
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact
from review_th03_decoded_code import code_rows,extent_observation
from review_th03_mainl_cutscene import DS,Probe,REVISION,sha

ROOT=Path(__file__).resolve().parents[1]
CS=0xc7e
PROOF='.analysis/sol-mainl-root-review-20261006.json'
PROOF_SHA256='164cd6e5e04b8ff41dda51aa0deecfbf8df4a931dbf800ac012efd878eb0fdce'
RANGES=[('planes',2,41,''),('exit',0x1b0,67,''),('init',0x700,62,'4'),('exit_to_main',0x98f,40,'')]
MODULES={'planes':'th01/vplanset.cpp','exit':'th03/exit.cpp','init':'th03/initmain.cpp','exit_to_main':'th03/exitmain.cpp'}
IMPORTS={(0,0x213e):('assign',2),(0,0x235a):('unassign',0),
         (0,0x1f6e):('vsync_start',0),(0,0x201c):('vsync_end',0),
         (0,0x75a):('egc_start',0),(0,0xe24):('graph_400line',0),
         (0,0x2aae):('js_start',0),(0,0x17ca):('js_end',0),
         (0,0x2856):('pfstart',4),(0,0x2912):('pfend',0),
         (0,0xe72):('clear',0),(0,0x1f20):('text_clear',0)}
PROVIDERS=['th03/initmain.cpp','th03/core/initmain.cpp','th03/exit.cpp','th02/core/exit.cpp',
           'th03/exitmain.cpp','th03/core/exitmain.cpp','th03/core/initexit.h','th02/core/initexit.h',
           'th01/vplanset.cpp','th01/hardware/vplanset.cpp','th01/hardware/vplanset.h',
           'planar.h','pc98.h','platform.h','libs/master.lib/func.hpp',
           'libs/master.lib/master.hpp','libs/master.lib/pc98_gfx.hpp']
POINTERS=struct.pack('<8H',0,0xa800,0,0xb000,0,0xb800,0,0xe000)
REMAPS={'th03/initmain.cpp':'src/main/core/initmain.cpp',
        'th03/exit.cpp':'src/main/core/exit.cpp',
        'th01/vplanset.cpp':'src/main/hardware/vram_planes.cpp'}
LOCAL_PROVIDERS=['src/main/core/initmain.cpp','src/main/core/initmain.hpp',
                 'src/main/core/exit.cpp','src/main/core/exit.hpp',
                 'src/main/hardware/vram_planes.cpp','src/main/hardware/vram_planes.hpp',
                 'compat/rec98/planar.h','compat/rec98/pc98.h']


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;result=[]
    for name,start,size,cleanup in RANGES:
        body=image[CS*16+start:CS*16+start+size]
        if len(body)!=size:raise ValueError('lifecycle complete body/far cleanup differs')
        ins=list(decoder.disasm(body,start));bounds={i.address for i in ins}
        if sum(i.size for i in ins)!=size or not ins or (ins[-1].mnemonic,ins[-1].op_str)!=('retf',cleanup):raise ValueError('lifecycle complete body/far cleanup differs')
        edges=[]
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf') and (i.mnemonic,i.op_str)!=('retf',cleanup):raise ValueError('lifecycle interior return contract differs')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('unexpected lifecycle indirect edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (CS,i.operands[0].imm)
            if i.mnemonic=='lcall':
                if dest not in IMPORTS:raise ValueError('unknown lifecycle far interface')
            elif i.mnemonic=='call':
                if dest!=(CS,2) or not j or ins[j-1].bytes!=b'\x0e':raise ValueError('lifecycle near call lacks PUSH CS/far entry')
            elif dest[1] not in bounds:raise ValueError('lifecycle branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        result.append(dict(name=name,offset=start,size=size,cleanup=cleanup,sha256=sha(body),instructions=len(ins),edges=edges))
    return result


class LifecycleProbe(Probe):
    """Actual lifecycle and plane helper; all twelve imported bodies are models."""
    def __init__(self,mz,*,assign=0,carry=False,library_return=0xace1,df=False):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,(struct.unpack_from('<H',image,at)[0]+0x2000)&65535)
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x2c7e0,0x2e3f0,0x40000
        for name,value in [('CS',0x2c7e),('DS',0x2e3f),('SS',0x4000),('ES',0x3333),('BP',0x7777),('SI',0x1357),('DI',0x2468),('EFLAGS',0x202|(0x400 if df else 0))]:self.set(name,value)
        self.events,self.ports,self.writes,self.errors,self.helper_frames=[],[],[],[],[]
        self.stop=False;self.caller_stop=False;self.caller=False
        self.uc.mem_write(self.data+0x1c60,b'\x5a\xa5'*8)
        models={(0x2000+s)*16+o:(s,o,n,count) for (s,o),(n,count) in IMPORTS.items()}
        def guard(callback):
            def invoke(*args):
                try:return callback(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop()
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2c7e:raise ValueError('lifecycle terminal segment alias')
                self.stop=True;uc.emu_stop();return
            if self.caller and address==0x295f0+0x7a3:
                if self.get('CS')!=0x295f:raise ValueError('lifecycle caller segment alias')
                self.caller_stop=True;uc.emu_stop();return
            if self.caller and address==0x295f0+3:
                if self.get('CS')!=0x295f:raise ValueError('lifecycle cfg segment alias')
                sp=self.get('SP');self.events.append(dict(name='cfg',args=[]));self.set('AX',1)
                self.set('IP',struct.unpack('<H',uc.mem_read(self.stack+sp,2))[0]);self.set('SP',sp+2);return
            if address==self.code+2:
                sp=self.get('SP');self.helper_frames.append(list(struct.unpack('<HH',uc.mem_read(self.stack+sp,4))))
            if address in models:
                seg,off,name,count=models[address]
                if (self.get('CS'),address-self.get('CS')*16)!=(0x2000+seg,off):raise ValueError('lifecycle interface segment alias')
                sp=self.get('SP');words=list(struct.unpack('<'+'H'*((4+count)//2),uc.mem_read(self.stack+sp,4+count)))
                self.events.append(dict(name=name,args=words[2:]));self.set('AX',assign if name=='assign' else library_return)
                self.set('EFLAGS',(self.get('EFLAGS')&~1)|int(carry));self.set('SP',sp+4+count);self.set('CS',words[1]);self.set('IP',words[0]);return
            off=address-self.code
            in_root=self.caller and self.get('CS')==0x295f and 0x78d<=address-0x295f0<0x7a3
            if not in_root and (self.get('CS')!=0x2c7e or not any(a<=off<a+n for _,a,n,_ in RANGES)):raise ValueError('CPU escaped reviewed lifecycle bodies/caller prefix')
        def write(uc,access,address,size,value,user):
            if self.data<=address<self.data+65536:self.writes.append([address-self.data,size,value])
        def output(uc,port,width,value,user):
            if port not in (0xa4,0xa6) or width!=1:raise ValueError('unexpected lifecycle port/width')
            self.ports.append([port,value])
        def intr(uc,number,user):raise ValueError('unexpected lifecycle interrupt')
        def inp(uc,port,width,user):self.errors.append('unexpected lifecycle input port');uc.emu_stop();return 0
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,inp,None,1,0,reg.UC_X86_INS_IN)

    def run(self,entry,args=(),*,caller=False,terminal=True,budget=10000):
        self.stop=False;self.caller_stop=False;self.errors.clear();self.caller=caller
        self.set('CS',0x295f if caller else 0x2c7e);self.set('SP',0xffd0)
        self.uc.mem_write(self.stack+0xffd0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2c7e,*args))
        self.uc.emu_start((0x295f0 if caller else self.code)+entry,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if self.stop!=(terminal and not caller) or self.caller_stop!=(terminal and caller):raise ValueError('lifecycle terminal/caller/budget differs')
        if terminal and not caller and (self.get('SP')!=0xffd4+(4 if entry==0x700 else 0) or self.get('DS')!=0x2e3f or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]):raise ValueError('lifecycle return stack/callee-saved differs')
        if terminal and caller and (self.get('SP')!=0xffcc or self.get('BP')!=0xffce or self.get('DS')!=0x2e3f):raise ValueError('lifecycle caller stack differs')

    def result(self):
        return dict(ax=self.get('AX'),events=self.events,ports=self.ports,writes=self.writes,planes_hex=bytes(self.uc.mem_read(self.data+0x1c60,16)).hex(),helper_frames=self.helper_frames,df=bool(self.get('EFLAGS')&0x400))


def matrix(mz):
    cases=[]
    def check(p,changes):
        expected=bytearray(p.before)
        if changes:expected[0x1c60:0x1c70]=POINTERS
        if bytes(p.uc.mem_read(p.data,65536))!=bytes(expected):raise ValueError('lifecycle plane/unchanged DGROUP differs')
        expected_writes=[[0x1c60+i*4,4,v] for i,v in enumerate((0xa8000000,0xb0000000,0xb8000000,0xe0000000))] if changes else []
        if p.writes!=expected_writes:raise ValueError('lifecycle complete data stores differ')
    for assign in (0,1,2,0x7fff,0x8000,0xffff):
        for carry in (False,True):
            for pointer in ((0,0),(0x3f7,0x2e3f),(0xfffe,0x6000)):
                p=LifecycleProbe(mz,assign=assign,carry=carry);p.before=bytes(p.uc.mem_read(p.data,65536));p.run(0x700,pointer)
                names=[e['name'] for e in p.events];expected=['assign']+([] if assign else ['vsync_start','egc_start','graph_400line','js_start','pfstart'])
                if names!=expected or p.events[0]['args']!=[18000] or p.get('AX')!=int(bool(assign)):raise ValueError('lifecycle assign AX/paragraph gate or init order differs')
                if not assign and p.events[-1]['args']!=list(pointer):raise ValueError('lifecycle unchanged far filename argument differs')
                check(p,not assign);cases.append(dict(scope='init',assign=assign,carry=carry,pointer=pointer,result=p.result()))
    for entry in (2,0x1b0,0x98f):
        for df in (False,True):
            for library_return in (0,0xffff):
                p=LifecycleProbe(mz,df=df,library_return=library_return);p.before=bytes(p.uc.mem_read(p.data,65536));p.run(entry)
                names=[e['name'] for e in p.events]
                expected=[] if entry==2 else ['pfend','clear','clear','vsync_end','unassign','text_clear','js_end','egc_start'] if entry==0x1b0 else ['pfend','vsync_end','unassign','js_end','egc_start']
                ports=[] if entry==2 else [[0xa6,1],[0xa6,0],[0xa6,0],[0xa4,0]] if entry==0x1b0 else [[0xa6,0],[0xa4,0]]
                if names!=expected or p.ports!=ports or bool(p.get('EFLAGS')&0x400)!=df:raise ValueError('lifecycle exit sequence/ports/DF differs')
                check(p,entry==2);cases.append(dict(scope='planes' if entry==2 else 'exit',entry=entry,df=df,library_return=library_return,result=p.result()))
    for assign in (0,1,0xffff):
        p=LifecycleProbe(mz,assign=assign);p.before=bytes(p.uc.mem_read(p.data,65536));p.run(0x78d,caller=True)
        names=[e['name'] for e in p.events]
        if names!=['cfg','assign']+([] if assign else ['vsync_start','egc_start','graph_400line','js_start','pfstart']) or p.get('AX')!=int(bool(assign)):raise ValueError('lifecycle actual main caller ignored-result prefix differs')
        check(p,not assign);cases.append(dict(scope='main_caller_prefix',assign=assign,reached_respal_exist_call=True,result=p.result()))
    return cases


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('lifecycle prior root proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_lifecycle.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    local={p:(ROOT/p).read_bytes() for p in LOCAL_PROVIDERS}
    inputs.update({p:sha(data) for p,data in local.items()})
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('lifecycle input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact);observations=[]
    maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('lifecycle invalid image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz))
        if observations:
            tree=Path(path).parents[2]
            for p,data in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                expected=(f'#include "{REMAPS[p]}"\n'.encode() if p in REMAPS else data)
                if cached!=expected:raise ValueError('lifecycle frozen/remapped provider association differs')
            for p,data in local.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                if cached!=data:raise ValueError('lifecycle cached maintained MAIN provider differs')
            mp=next(p for p in maps if str(tree) in p);rows=code_rows((ROOT/mp).read_text(),len(mz.program_image));decoded=parse_mz((ROOT/observations[0]['path']).read_bytes());comparisons={}
            for name,at,size,_ in RANGES:
                row=next(r for r in rows if r['module']==MODULES[name] and r['size'])
                if (row['segment'],row['offset'],row['size'])!=(CS,at,size):raise ValueError('lifecycle complete MAP contribution differs')
                comparisons[name]=extent_observation(decoded,mz,row)
            observed['comparisons']=comparisons
            if observed['cpu']!=observations[0]['cpu']:raise ValueError('lifecycle target/cached CPU diagnostics differ')
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('lifecycle canonical target changed')
    for p,data in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=data:raise ValueError('lifecycle frozen provider changed')
    result=dict(kind='th03-mainl-lifecycle-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},cached_main_forwarder_remaps=REMAPS,localized_main_providers={p:sha(d) for p,d in local.items()},observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS MAINL lifecycle169/helper41 and actual main caller-prefix diagnostics:',args.output)


if __name__=='__main__':main()
