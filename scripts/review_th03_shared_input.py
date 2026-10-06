#!/usr/bin/env python3
"""Complete Complete shared input/timing carriers, independently bound OP and MAINL."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import struct
import subprocess
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import DS, Probe, REVISION, sha
from review_th03_mainl_snow import u16, signed

ROOT = Path(__file__).resolve().parents[1]
PARENT = '.analysis/th03-shared-pi/sol-shared-pi-source-20261006/receipt.json'
PARENT_SHA = '464ba04649e071f3f5a2a59f7c2fcbd703ac80f00c8fc615f82e5a960d7a026b'
PROFILES = {
 'mainl': dict(cs=0xc7e,ds=0xe3f,p1=0x1d08,p2=0x1d0a,sp=0x1d0c,joy=0x141a,clock=0x144e,present=0x570,sound=0x880,midi=0x1c71,joy_call=0x2aea,
  ranges=[('sense',0x388,417,0),('measure_wait',0xc4d,77,4),('ok_wait',0xc9a,49,2),('interface',0xdc2,36,0),('key_key',0xde6,10,0),('joy_key',0xdf0,34,0),('key_joy',0xe12,34,0),('one_cpu',0xe34,42,0),('cpu_one',0xe5e,45,0),('cpu_cpu',0xe8b,42,0),('attract',0xeb5,48,0),('change',0xee5,76,2),('frame_delay',0x372,21,2)]),
 'op': dict(cs=0xbeb,ds=0xd7f,p1=0x1aa2,p2=0x1aa4,sp=0x1aa6,joy=0x11b4,clock=0x11e8,present=0x2cc,sound=0x5dc,midi=0x1a0b,joy_call=0x2df4,
  ranges=[('sense',0x304,417,0),('interface',0xad6,36,0),('key_key',0xafa,10,0),('joy_key',0xb04,34,0),('key_joy',0xb26,34,0),('one_cpu',0xb48,42,0),('cpu_one',0xb72,45,0),('cpu_cpu',0xb9f,42,0),('attract',0xbc9,48,0),('change',0xbf9,76,2),('frame_delay',0x2ee,21,2),('frame_delay_2',0xcd6,21,2)])}
MODULES = [('th03/inp_m_w.cpp','interface',367),('th03/inp_wait.cpp','measure_wait',126),('th02/frmdely1.cpp','frame_delay',21),('th02/frmdely2.cpp','frame_delay_2',21)]
PROVIDERS = ['th03/inp_m_w.cpp','th03/inp_wait.cpp','th03/hardware/inp_wait.cpp','th03/input_s.cpp','th03/hardware/input_s.cpp','th03/hardware/input.h','th02/frmdely1.cpp','th02/hardware/frmdely1.cpp','th02/frmdely2.cpp','th02/hardware/frmdelay.h','th02/snd/measure.hpp','th03/snd/snd.h','platform/x86real/pc98/keyboard.hpp','platform/x86real/flags.hpp','x86real.h','platform.h','libs/master.lib/master.hpp','Tupfile.lua']
# (BIOS group, mask, P1, P2, SP). This is a source-level key specification.
KEYS = [(7,4,0,0,1),(7,32,0,0,2),(7,8,0,32,4),(7,16,0,16,8),
        (9,1,0,8,8),(9,4,0,0x200,0x200),(9,8,0,2,2),(9,16,0,0x800,0x800),
        (8,64,0,4,4),(8,4,0,0x100,0x100),(8,8,0,1,1),(8,16,0,0x400,0x400),
        (5,2,32,0,32),(5,4,16,0,16),(5,16,0x200,0,0),(5,32,2,0,0),(5,64,0x800,0,0),
        (4,1,4,0,0),(4,4,8,0,0),(2,8,0x100,0,0),(2,16,1,0,0),(2,32,0x400,0,0),
        (2,1,0,0,0x4000),(0,1,0,0,0x1000),(3,16,0,0,0x2000),(6,16,0,0,32)]


def analyze(image,p):
    CS=p["cs"];RANGES=p["ranges"];known={p[k] for k in ("p1","p2","sp","joy","clock","present","sound","midi")}|{p["sp"]+1}
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
            for o in i.operands:
                if o.type==X86_OP_MEM and not o.mem.base and not o.mem.index:
                    if i.reg_name(o.mem.segment)=='es':
                        if name!='sense' or o.mem.disp not in (0x52a,0x52c,0x52d,0x52e,0x52f,0x530,0x531,0x532,0x533):raise ValueError('input BIOS binding differs')
                    elif o.mem.disp not in known:raise ValueError('input DATA binding differs')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('input indirect edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (CS,i.operands[0].imm)
            if i.mnemonic=='lcall':
                if dest!=(0,p["joy_call"]):raise ValueError('input unknown far interface')
            elif i.mnemonic=='call':
                if dest[1] not in entries or not j or ins[j-1].bytes!=b'\x0e':
                    raise ValueError('input near call lacks PUSH CS/far entry')
            elif dest[1] not in bounds:raise ValueError('input branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=start,size=size,cleanup=cleanup,instructions=len(ins),positions=sorted(bounds),sha256=sha(body),edges=edges))
    return dict(bodies=rows,owned_bytes=sum(n for name,_,n,_ in RANGES if name!="sense"),context_bytes=417)


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
    def __init__(self,mz,p,scenario):
        self.p=p;P1,P2,SP,JOY,CLOCK=(p[k] for k in ("p1","p2","sp","joy","clock"));RANGES=p["ranges"]
        entries={name:start for name,start,_,_ in RANGES};cs=p["cs"]+0x2000;ds=p["ds"]+0x2000
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=cs*16,ds*16,0x40000
        for name,value in [('CS',cs),('DS',ds),('SS',0x4000),('BP',0x7777),('SI',0x1357),('DI',0x2468),('EFLAGS',2|(0x200 if scenario.get('if',True) else 0)|(0x400 if scenario.get('df') else 0))]:self.set(name,value)
        self.errors,self.events,self.writes=[],[],[];self.stop=False;self.senses=self.outs=self.delays=self.delay_ticks=0
        self.active=scenario;self.measure_comparisons=[];self.visited=set()
        def guard(callback):
            def invoke(*args):
                try:return callback(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop()
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=cs:raise ValueError('input terminal segment alias')
                self.stop=True;uc.emu_stop();return
            if address==0x20000+p["joy_call"]:
                if self.get('CS')!=0x2000:raise ValueError('input joystick segment alias')
                sp=self.get('SP');ip,ret_cs=struct.unpack('<2H',uc.mem_read(self.stack+sp,4))
                if ret_cs!=cs:raise ValueError('input joystick return segment differs')
                self.word(JOY,scenario.get('joy',0));self.set('AX',scenario.get('joy_status',0xffff))
                self.events.append(dict(name='joystick',value=scenario.get('joy',0)))
                self.set('SP',sp+4);self.set('CS',ret_cs);self.set('IP',ip);return
            off=address-self.code
            if self.get('CS')!=cs or not any(a<=off<a+n for _,a,n,_ in RANGES):raise ValueError('CPU escaped input bodies')
            self.visited.add(off)
            if off==entries["sense"]:
                samples=scenario.get('samples',[[[0]*10,[0]*10]])
                self.sample=samples[min(self.senses,len(samples)-1)];self.senses+=1
                uc.mem_write(0x52a,bytes(self.sample[0]))
                if scenario.get('tick'):self.word(CLOCK,u16(self.word(CLOCK)+scenario['tick']))
            elif off in [at for name,at in entries.items() if name.startswith("frame_delay")]:
                self.delays+=1
                sp=self.get('SP');ip,ret_cs,arg=struct.unpack('<3H',uc.mem_read(self.stack+sp,6))
                if ret_cs!=cs or arg!=u16(scenario.get("frames",0) if scenario.get("direct_delay") else 1):raise ValueError('input native delay frame differs')
            elif off in [at+9 for name,at in entries.items() if name.startswith('frame_delay')] and not scenario.get('stalled_delay'):
                self.delay_ticks+=1;self.word(CLOCK,u16(self.word(CLOCK)+scenario.get("delay_tick",1)))
            elif off==entries.get("measure_wait",-100)+0x42:self.measure_comparisons.append([self.get('AX'),self.word_at_stack(self.get('BP')+8)])
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
        p=self.p;cs=p["cs"]+0x2000;ds=p["ds"]+0x2000;RANGES=p["ranges"]
        self.stop=False;self.errors.clear();self.set('CS',cs);self.set('SP',0xffc0)
        args=([u16(scenario.get('frames',0)),u16(scenario.get('measure',0))] if name=='measure_wait'
              else [u16(scenario.get('frames',0))] if name in ('ok_wait','change','frame_delay','frame_delay_2') else [])
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,cs,*args))
        start,cleanup=next((a,c) for n,a,_,c in RANGES if n==name)
        self.uc.emu_start(self.code+start,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if self.stop!=terminal:raise ValueError('input terminal/budget differs')
        if terminal and (self.get('SP')!=0xffc4+cleanup or self.get('DS')!=ds or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]):raise ValueError('input far cleanup/callee-saved differs')


def samples(group=None,mask=0):
    bank=[0]*10
    if group is not None:bank[group]=mask
    return [bank,bank.copy()]


def matrix(mz,p):
    P1,P2,SP,JOY,CLOCK=(p[k] for k in ("p1","p2","sp","joy","clock"))
    profile=p;rows=[]
    def observe(name,s,*,terminal=True,expected_senses=None,expected_ax=None,expected_delays=None):
        p=InputProbe(mz,profile,s)
        for at in (P1,P2,SP,JOY):p.word(at,0xdead)
        p.word(profile["present"],s.get('present',0));p.word(CLOCK,0xbeef)
        p.uc.mem_write(p.data+profile["sound"],bytes([s.get('sound',0)]));p.uc.mem_write(p.data+profile["midi"],bytes([s.get('midi_active',0)]))
        before=bytes(p.uc.mem_read(p.data,65536));memory_before=bytes(p.uc.mem_read(0,0x100000));p.run(name,s,terminal=terminal,budget=400000 if terminal else 14000)
        after=bytes(p.uc.mem_read(p.data,65536));expected=bytearray(before)
        if terminal and not name.startswith('frame_delay'):
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
        elif not terminal:
            for at in (P1,P2,SP,JOY,CLOCK):expected[at:at+2]=after[at:at+2]
            if after!=bytes(expected):raise ValueError('input budget changed unrelated DGROUP')
        else:
            struct.pack_into('<H',expected,CLOCK,u16(s.get('delay_tick',1)*p.delay_ticks))
            if after!=bytes(expected):raise ValueError('input direct frame scalar differs')
        memory_after=bytes(p.uc.mem_read(0,0x100000));full=bytearray(memory_before)
        full[p.data:p.data+65536]=expected
        full[0x52a:0x534]=memory_after[0x52a:0x534]
        full[p.stack:p.stack+65536]=memory_after[p.stack:p.stack+65536]
        if memory_after!=bytes(full):raise ValueError('input complete physical memory outside caller stack differs')
        if bool(p.get('EFLAGS')&0x200)!=bool(s.get('if',True)):raise ValueError('input inherited IF differs')
        if bool(p.get('EFLAGS')&0x400)!=bool(s.get('df')):raise ValueError('input inherited DF differs')
        if s.get('sound') and name=='measure_wait':
            if any(ax!=p1 for ax,_ in p.measure_comparisons for p1 in [key_state(*s.get('samples',[samples()])[0])[0]]):
                raise ValueError('input song-measure AX clobber differs')
        rows.append(dict(name=name,scenario=s,terminal=terminal,senses=p.senses,port_count=p.outs,delays=p.delays,
            events=p.events,measure_comparisons=p.measure_comparisons,ax=p.get('AX') if terminal and name.endswith('wait') else None,
            visited=sorted(p.visited),ordered_writes=p.writes,physical_outside_stack_checked=True,
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
    if "measure_wait" in {n for n,_,_,_ in profile["ranges"]}:
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
    for name,_,_,_ in profile['ranges']:
        if not name.startswith('frame_delay'):continue
        for frames,tick in [(0,1),(1,1),(3,1),(0x8000,0x8000),(0xffff,0xffff)]:
            for df in (False,True):
                for enabled in (False,True):observe(name,dict(frames=frames,delay_tick=tick,direct_delay=True,df=df,**{'if':enabled}))
        observe(name,dict(frames=1,direct_delay=True,stalled_delay=True),terminal=False)
    return rows


def coverage(meta,rows):
    wanted={i for b in meta['bodies'] for i in b['positions']};seen={i for r in rows for i in r['visited']}
    if wanted!=seen:raise ValueError('input incomplete native coverage: '+str(sorted(wanted-seen)))
    return dict(positions=len(wanted),complete=True,invocations=len(rows),returns=sum(r['terminal'] for r in rows),prefixes=sum(not r['terminal'] for r in rows))


def semantic(rows):return json.loads(json.dumps([{k:v for k,v in r.items() if k not in ('before_sha256','after_sha256')} for r in rows]))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    raw=(ROOT/PARENT).read_bytes()
    if sha(raw)!=PARENT_SHA:raise ValueError('input previous cold proof differs')
    previous=json.loads(raw);inputs={**previous['inputs'],PARENT:sha(raw)}
    for path in ['scripts/review_th03_shared_input.py','.analysis/sol-shared-input-op-ghidra-check-20261006.log','.analysis/sol-shared-input-mainl-ghidra-check-20261006.log']:inputs[path]=sha((ROOT/path).read_bytes())
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for path,h in inputs.items():
            if sha((ROOT/path).read_bytes())!=h:raise ValueError('input prerequisite changed: '+path)
    verify();observations={}
    for art,p in PROFILES.items():
        artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-'+art);stored=read_verified_artifact(ROOT,artifact)
        paths=[f'.analysis/th03-diet/sol-diet-restoration-20261006-b/{art}.exe']+[str(Path(PARENT).parent/f'round{n}/source/bin/th03/{art}.exe') for n in (1,2)]
        observations[art]=[];target=parse_mz((ROOT/paths[0]).read_bytes());entries={n:a for n,a,_,_ in p['ranges']}
        for path in paths:
            inputs[path]=sha((ROOT/path).read_bytes());mz=parse_mz((ROOT/path).read_bytes())
            if not mz.valid:raise ValueError('input invalid MZ')
            meta=analyze(mz.program_image,p);cpu=matrix(mz,p);row=dict(path=path,analysis=meta,cpu=cpu,coverage=coverage(meta,cpu))
            if observations[art]:
                tree=Path(path).parents[2];mp=tree/f'obj/th03/{art}.map';inputs[str(mp)]=sha((ROOT/mp).read_bytes());maprows=code_rows((ROOT/mp).read_text(),len(mz.program_image));comparisons={}
                for module,key,size in MODULES:
                    if key not in entries:continue
                    mr=next(r for r in maprows if r['module']==module and r['size'])
                    if (mr['segment'],mr['offset'],mr['size'])!=(p['cs'],entries[key],size):raise ValueError('input original complete MAP ownership differs')
                    comp=extent_observation(target,mz,mr)
                    if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('input original raw/ordered carrier differs')
                    comparisons[module]=comp;obj=tree/'obj'/Path(module).parent/(Path(module).stem+'.obj');inputs[str(obj)]=sha((ROOT/obj).read_bytes())
                row['comparisons']=comparisons
                for name,data in providers.items():
                    cp=tree/name;cached=(ROOT/cp).read_bytes();inputs[str(cp)]=sha(cached)
                    if name=='Tupfile.lua':cached=cached.replace(b'"th03/vector_far.asm"',b'"th03/vector.cpp"')
                    if cached!=data:raise ValueError('input preceding frozen/remapped provider differs: '+name)
                if meta!=observations[art][0]['analysis'] or semantic(cpu)!=semantic(observations[art][0]['cpu']):raise ValueError('input target/cached observations differ')
            observations[art].append(row)
        if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('input canonical target changed')
        print('PASS shared input',art,observations[art][0]['coverage'],flush=True)
    verify();report=dict(kind='th03-shared-input-complete-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
