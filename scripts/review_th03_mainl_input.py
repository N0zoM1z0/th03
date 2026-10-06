#!/usr/bin/env python3
"""Complete MAINL input chain: native keyboard/modes/waits, explicit device clocks."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import struct
import subprocess
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import DS, Probe, REVISION, sha
from review_th03_mainl_snow import u16, signed

ROOT = Path(__file__).resolve().parents[1]
CS = 0xc7e
PROOF = '.analysis/sol-mainl-pi-review-20261006.json'
PROOF_SHA256 = '4e59fa60e4dee0a7422990a2120ffcd9bb667cb0c5300050ad5cf25fcca04197'
RANGES = [('sense',0x388,417,0),('measure_wait',0xc4d,77,4),('ok_wait',0xc9a,49,2),
          ('interface',0xdc2,36,0),('key_key',0xde6,10,0),('joy_key',0xdf0,34,0),
          ('key_joy',0xe12,34,0),('one_cpu',0xe34,42,0),('cpu_one',0xe5e,45,0),
          ('cpu_cpu',0xe8b,42,0),('attract',0xeb5,48,0),('change',0xee5,76,2),
          ('frame_delay',0x372,21,2)]
MODULES = [('th03/input_s.cpp',0x388,417),('th03/inp_wait.cpp',0xc4d,126),
           ('th03/inp_m_w.cpp',0xdc2,367)]
PROVIDERS = ['th03/input_s.cpp','th03/hardware/input_s.cpp','th03/inp_wait.cpp',
             'th03/hardware/inp_wait.cpp','th03/inp_m_w.cpp','th03/hardware/input.h',
             'th02/hardware/frmdelay.h','th02/snd/measure.hpp','th03/snd/snd.h',
             'platform/x86real/pc98/keyboard.hpp','platform/x86real/flags.hpp',
             'x86real.h','platform.h','libs/master.lib/master.hpp',
             'th02/frmdely1.cpp','th02/hardware/frmdely1.cpp','th02/snd/snd.h','libs/kaja/kaja.h']
REMAPS = {'th03/input_s.cpp':'src/main/hardware/input_sense.cpp',
          'th03/inp_m_w.cpp':'src/main/hardware/input_modes.cpp',
          'th02/frmdely1.cpp':'src/main/hardware/frame_delay.cpp'}
LOCAL = [*REMAPS.values(),'src/main/hardware/input.hpp','src/main/hardware/frame_delay.hpp']
P1,P2,SP,JOY,CLOCK = 0x1d08,0x1d0a,0x1d0c,0x141a,0x144e
# (BIOS group, mask, P1, P2, SP). This is a source-level key specification.
KEYS = [(7,4,0,0,1),(7,32,0,0,2),(7,8,0,32,4),(7,16,0,16,8),
        (9,1,0,8,8),(9,4,0,0x200,0x200),(9,8,0,2,2),(9,16,0,0x800,0x800),
        (8,64,0,4,4),(8,4,0,0x100,0x100),(8,8,0,1,1),(8,16,0,0x400,0x400),
        (5,2,32,0,32),(5,4,16,0,16),(5,16,0x200,0,0),(5,32,2,0,0),(5,64,0x800,0,0),
        (4,1,4,0,0),(4,4,8,0,0),(2,8,0x100,0,0),(2,16,1,0,0),(2,32,0x400,0,0),
        (2,1,0,0,0x4000),(0,1,0,0,0x1000),(3,16,0,0,0x2000),(6,16,0,0,32)]


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[]
    entries={a for _,a,_,_ in RANGES}
    for name,start,size,cleanup in RANGES:
        body=image[CS*16+start:CS*16+start+size]
        if len(body)!=size:raise ValueError('input complete body/far cleanup differs')
        ins=list(decoder.disasm(body,start));bounds={i.address for i in ins}
        wanted=('retf',str(cleanup) if cleanup else '')
        if sum(i.size for i in ins)!=size or not ins or (ins[-1].mnemonic,ins[-1].op_str)!=wanted:
            raise ValueError('input complete body/far cleanup differs')
        edges=[]
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf') and (i.mnemonic,i.op_str)!=wanted:
                raise ValueError('input interior return differs')
            if i.mnemonic=='int' and (name!='measure_wait' or i.op_str not in ('0x60','0x61')):
                raise ValueError('input unknown interrupt')
            if i.mnemonic=='out' and (name!='sense' or i.op_str!='0x5f, al'):
                raise ValueError('input unknown output port')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('input indirect edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (CS,i.operands[0].imm)
            if i.mnemonic=='lcall':
                if dest!=(0,0x2aea):raise ValueError('input unknown far interface')
            elif i.mnemonic=='call':
                if dest[1] not in entries or not j or ins[j-1].bytes!=b'\x0e':
                    raise ValueError('input near call lacks PUSH CS/far entry')
            elif dest[1] not in bounds:raise ValueError('input branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=start,size=size,cleanup=cleanup,instructions=len(ins),sha256=sha(body),edges=edges))
    return dict(bodies=rows[:-1],frame_helper=rows[-1],body_bytes=910,helper_bytes=21)


def key_state(first,second):
    result=[0,0,0]
    for group,mask,p1,p2,sp in KEYS:
        if (first[group]|second[group]) & mask:
            for i,value in enumerate((p1,p2,sp)):result[i]|=value
    return result


def mode_state(name,values,present,joy):
    p1,p2,sp=values
    if name in ('interface','attract'):sp|=p1|(joy if present else 0)
    elif name=='joy_key' and present:p1,p2=joy,sp
    elif name=='key_joy' and present:p1,p2=sp,joy
    elif name=='one_cpu':p1|=sp|(joy if present else 0);p2=0
    elif name=='cpu_one':p2=sp|p1|(joy if present else 0);p1=0
    elif name=='cpu_cpu':
        if sp & 0x3000:sp=0x1000
        p1=p2=0
    if name=='attract':p1=p2=0
    sensed=present and name not in ('sense','key_key','cpu_cpu')
    return [u16(p1),u16(p2),u16(sp)],joy if sensed else 0,sensed


class InputProbe(Probe):
    """Native keyboard and waits; joystick, music interrupt and IRQ counter fixtures."""
    def __init__(self,mz,scenario):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x2c7e0,0x2e3f0,0x40000
        for name,value in [('CS',0x2c7e),('DS',0x2e3f),('SS',0x4000),('BP',0x7777),('SI',0x1357),('DI',0x2468),('EFLAGS',0x202|(0x400 if scenario.get('df') else 0))]:self.set(name,value)
        self.errors,self.events,self.writes=[],[],[];self.stop=False;self.senses=self.outs=self.delays=0
        self.active=scenario;self.measure_comparisons=[]
        def guard(callback):
            def invoke(*args):
                try:return callback(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop()
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2c7e:raise ValueError('input terminal segment alias')
                self.stop=True;uc.emu_stop();return
            if address==0x20000+0x2aea:
                if self.get('CS')!=0x2000:raise ValueError('input joystick segment alias')
                sp=self.get('SP');ip,cs=struct.unpack('<2H',uc.mem_read(self.stack+sp,4))
                if cs!=0x2c7e:raise ValueError('input joystick return segment differs')
                self.word(JOY,scenario.get('joy',0));self.set('AX',scenario.get('joy_status',0xffff))
                self.events.append(dict(name='joystick',value=scenario.get('joy',0)))
                self.set('SP',sp+4);self.set('CS',cs);self.set('IP',ip);return
            off=address-self.code
            if self.get('CS')!=0x2c7e or not any(a<=off<a+n for _,a,n,_ in RANGES):raise ValueError('CPU escaped input bodies')
            if off==0x388:
                samples=scenario.get('samples',[[[0]*10,[0]*10]])
                self.sample=samples[min(self.senses,len(samples)-1)];self.senses+=1
                uc.mem_write(0x52a,bytes(self.sample[0]))
                if scenario.get('tick'):self.word(CLOCK,u16(self.word(CLOCK)+scenario['tick']))
            elif off==0x372:
                self.delays+=1
                sp=self.get('SP');ip,cs,arg=struct.unpack('<3H',uc.mem_read(self.stack+sp,6))
                if cs!=0x2c7e or arg!=1:raise ValueError('input native delay frame differs')
            elif off==0x37b and not scenario.get('stalled_delay'):
                self.word(CLOCK,u16(self.word(CLOCK)+1))
            elif off==0xc8f:self.measure_comparisons.append([self.get('AX'),self.word_at_stack(self.get('BP')+8)])
        def write(uc,access,address,size,value,user):
            if self.data<=address and address+size<=self.data+65536:
                if address-self.data not in (P1,P2,SP,JOY,CLOCK):raise ValueError('input write outside owned state')
                self.writes.append([address-self.data,size,value])
            elif self.stack<=address and address+size<=self.stack+65536:return
            else:raise ValueError('input unexpected memory write')
        def output(uc,port,width,value,user):
            if (port,width,value)!=(0x5f,1,0):raise ValueError('input port/width/value differs')
            self.outs+=1
            if self.outs%1024==0:uc.mem_write(0x52a,bytes(self.sample[1]))
        def intr(uc,number,user):
            if number not in (0x60,0x61) or self.get('AX')>>8!=5:raise ValueError('input unknown interrupt/function')
            if number==0x61 and self.get('DX')!=0xc0:raise ValueError('input MMD measure divisor differs')
            self.events.append(dict(name='measure',vector=number,value=scenario.get('measure_value',0)))
            self.set('AX',scenario.get('measure_value',0))
        def inp(uc,port,width,user):self.errors.append('input unexpected input port');uc.emu_stop();return 0
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,inp,None,1,0,reg.UC_X86_INS_IN)

    def word(self,at,value=None):
        if value is None:return struct.unpack('<H',self.uc.mem_read(self.data+at,2))[0]
        self.uc.mem_write(self.data+at,struct.pack('<H',u16(value)))

    def word_at_stack(self,at):return struct.unpack('<H',self.uc.mem_read(self.stack+at,2))[0]

    def run(self,name,scenario,*,terminal=True,budget=100000):
        self.stop=False;self.errors.clear();self.set('CS',0x2c7e);self.set('SP',0xffc0)
        args=([u16(scenario.get('frames',0)),u16(scenario.get('measure',0))] if name=='measure_wait'
              else [u16(scenario.get('frames',0))] if name in ('ok_wait','change') else [])
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2c7e,*args))
        start,cleanup=next((a,c) for n,a,_,c in RANGES if n==name)
        self.uc.emu_start(self.code+start,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if self.stop!=terminal:raise ValueError('input terminal/budget differs')
        if terminal and (self.get('SP')!=0xffc4+cleanup or self.get('DS')!=0x2e3f or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]):raise ValueError('input far cleanup/callee-saved differs')


def samples(group=None,mask=0):
    bank=[0]*10
    if group is not None:bank[group]=mask
    return [bank,bank.copy()]


def matrix(mz):
    rows=[]
    def observe(name,s,*,terminal=True,expected_senses=None,expected_ax=None,expected_delays=None):
        p=InputProbe(mz,s)
        for at in (P1,P2,SP,JOY):p.word(at,0xdead)
        p.word(0x570,s.get('present',0));p.word(CLOCK,0xbeef)
        p.uc.mem_write(p.data+0x880,bytes([s.get('sound',0)]));p.uc.mem_write(p.data+0x1c71,bytes([s.get('midi_active',0)]))
        before=bytes(p.uc.mem_read(p.data,65536));p.run(name,s,terminal=terminal,budget=100000 if terminal else 14000)
        after=bytes(p.uc.mem_read(p.data,65536));expected=bytearray(before)
        if terminal:
            first,second=s.get('samples',[samples()])[min(p.senses-1,len(s.get('samples',[samples()]))-1)]
            mode=name if name not in ('ok_wait','measure_wait','change') else 'interface'
            values,joy,sensed=mode_state(mode,key_state(first,second),s.get('present',0),s.get('joy',0))
            for at,value in zip((P1,P2,SP,JOY),[*values,joy]):struct.pack_into('<H',expected,at,value)
            if name in ('ok_wait','measure_wait','change'):
                expected_clock=(1 if p.delays else 0xbeef) if name=='change' else (s.get('tick',0)*p.senses if name=='ok_wait' or not s.get('sound') else u16(0xbeef+s.get('tick',0)*p.senses))
                struct.pack_into('<H',expected,CLOCK,u16(expected_clock))
            if after!=bytes(expected):raise ValueError('input full DGROUP scalar result differs: '+str((name,s)))
            if p.outs!=p.senses*1024:raise ValueError('input complete two-sample port count differs')
            if expected_senses is not None and p.senses!=expected_senses:raise ValueError('input sense count differs')
            if expected_ax is not None and p.get('AX')!=expected_ax:raise ValueError('input wait result differs')
            if expected_delays is not None and p.delays!=expected_delays:raise ValueError('input native delay count differs')
        else:
            for at in (P1,P2,SP,JOY,CLOCK):expected[at:at+2]=after[at:at+2]
            if after!=bytes(expected):raise ValueError('input budget changed unrelated DGROUP')
        if bool(p.get('EFLAGS')&0x400)!=bool(s.get('df')):raise ValueError('input inherited DF differs')
        if s.get('sound') and name=='measure_wait':
            if any(ax!=p1 for ax,_ in p.measure_comparisons for p1 in [key_state(*s.get('samples',[samples()])[0])[0]]):
                raise ValueError('input song-measure AX clobber differs')
        rows.append(dict(name=name,scenario=s,terminal=terminal,senses=p.senses,port_count=p.outs,delays=p.delays,
            events=p.events,measure_comparisons=p.measure_comparisons,ax=p.get('AX') if terminal and name.endswith('wait') else None,
            states=[p.word(at) for at in (P1,P2,SP,JOY,CLOCK)],full_dgroup_checked=terminal,
            unchanged_outside_state_checked=True,before_sha256=sha(before),after_sha256=sha(after)))
    # Every BIOS bit, including unused bits; alternate first/second-only presses.
    for group in (0,2,3,4,5,6,7,8,9):
        for bit in range(8):
            a,b=samples(group,1<<bit);pair=[a,[0]*10] if bit%2 else [[0]*10,b]
            observe('sense',dict(samples=[pair],df=bool(bit%2)),expected_senses=1)
    for pair in ([[255]*10,[0]*10],[[0]*10,[255]*10],[[255]*10,[255]*10]):
        observe('sense',dict(samples=[pair]),expected_senses=1)
    mixed=samples(7,8);mixed[0][4]=mixed[1][4]=1; mixed[0][0]=mixed[1][0]=1
    for name in ('interface','key_key','joy_key','key_joy','one_cpu','cpu_one','cpu_cpu','attract'):
        for present in (0,1,0xffff):
            for df in (False,True):
                for pair in (samples(3,16),samples(6,16),mixed):
                    observe(name,dict(samples=[pair],present=present,joy=0x8104,df=df),expected_senses=1)
    for frames,tick in [(0,0),(1,1),(3,1),(65535,65535)]:
        observe('ok_wait',dict(frames=frames,tick=tick),expected_senses=max(1,frames//tick) if tick else 1,expected_ax=0)
    observe('ok_wait',dict(frames=65535,samples=[samples(6,16)]),expected_ax=1,expected_senses=1)
    observe('ok_wait',dict(frames=1),terminal=False)
    for midi_active in (0,1,255):
        for measured in (0,1,65535):
            observe('measure_wait',dict(sound=1,midi_active=midi_active,measure_value=measured,measure=3,samples=[samples(4,1)]),expected_ax=0,expected_senses=1)
            observe('measure_wait',dict(sound=1,midi_active=midi_active,measure_value=measured,measure=1),terminal=False)
        observe('measure_wait',dict(sound=1,midi_active=midi_active,measure=65535,samples=[samples(3,16)]),expected_ax=1,expected_senses=1)
    observe('measure_wait',dict(sound=0,frames=0,measure=65535),expected_ax=0,expected_senses=1)
    for frames in (-1,1,0,9999):
        schedule=[samples(),samples(0,1)] if frames in (0,9999) else [samples()]
        observe('change',dict(frames=frames,samples=schedule),expected_senses=1 if frames<0 else 2,expected_delays=1 if frames==1 else 0)
    observe('change',dict(frames=-1,samples=[samples(0,1),samples()]),expected_senses=2,expected_delays=1)
    observe('change',dict(frames=-1,samples=[samples(0,1)]),terminal=False)
    observe('change',dict(frames=0),terminal=False)
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('input prior PI proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_input.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    local={p:(ROOT/p).read_bytes() for p in LOCAL};inputs.update({p:sha(d) for p,d in local.items()})
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('input invalid image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz))
        if observations:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('input complete body/helper bytes or CFG differ')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                wanted=(f'#include "{REMAPS[p]}"\n'.encode() if p in REMAPS else d)
                if cached!=wanted:raise ValueError('input cached frozen/remapped provider differs: '+p)
            for p,d in local.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                if cached!=d:raise ValueError('input maintained MAIN cached provider differs')
            rows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));target=parse_mz((ROOT/observations[0]['path']).read_bytes())
            observed['comparisons']={}
            for module,at,size in MODULES:
                row=next(r for r in rows if r['module']==module and r['size'])
                if (row['segment'],row['offset'],row['size'])!=(CS,at,size):raise ValueError('input complete MAP contribution differs')
                observed['comparisons'][module]=extent_observation(target,mz,row)
            def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('before_sha256','after_sha256')} for row in cpu]
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']):raise ValueError('input target/cached CPU differs')
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('input canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('input frozen provider changed')
    result=dict(kind='th03-mainl-complete-input-chain-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,
        providers={p:sha(d) for p,d in providers.items()},producer_remaps=REMAPS,observations=observations,
        tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS complete input910/native delay21 and explicit device/clock contracts:',args.output)


if __name__=='__main__':main()
