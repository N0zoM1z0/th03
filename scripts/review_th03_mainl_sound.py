#!/usr/bin/env python3
"""Complete MAINL sound candidate chain; native bodies, explicit DOS/driver clocks."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import re
import struct
import subprocess
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import DS, Probe, REVISION, sha
from review_th03_mainl_snow import u16

ROOT=Path(__file__).resolve().parents[1]
CS=0xc7e
PROOF='.analysis/sol-mainl-input-review-20261006.json'
PROOF_SHA256='92e5256f36e595ac0bccf94f0bee5f9be9738bcd98976a9b14cc6e71ec594d0a'
# Cleanup is native far cleanup: C callers retain arguments, Pascal callers remove them.
RANGES=[('mode',0x2c,29,0),('pmd',0x4a,57,0),('volume',0x84,27,0),
        ('load',0xa0,112,0),('reset',0x65e,11,0),('play',0x66a,60,2),
        ('update',0x6a6,60,0),('kaja',0x6e2,30,2),('measure',0xc1c,49,4),
        ('frame_delay',0x372,21,2)]
ALIGN=(0x49,0x83,0x9f,0x669)
MODULES=[('th02/snd_mode.c',0x2c,30),('th02/snd_pmdr.c',0x4a,58),
         ('th02/snd_dlyv.c',0x84,28),('th02/snd_load.cpp',0xa0,112),
         ('th02/snd_se_r.cpp',0x65e,12),('th03/snd_se.cpp',0x66a,120),
         ('th03/snd_kaja.cpp',0x6e2,30),('th03/snd_dlym.cpp',0xc1c,49)]
PROVIDERS=[m for m,_,_ in MODULES]+['th02/snd/detmode.c','th02/snd/pmd_res.c',
 'th02/snd/delayvol.c','th02/snd/load.cpp','th02/snd/se_reset.cpp','th02/snd/se.cpp',
 'th02/snd/kajaint.cpp','th03/snd/delaymea.cpp','th02/snd/impl.hpp','th02/snd/snd.h',
 'th03/snd/snd.h','th02/snd/measure.hpp','libs/kaja/kaja.h','game/pf.h','defconv.h',
 'x86real.h','platform.h','th03/snd/se_priority[data].asm','th03/snd/se_state[data].asm',
 'th02/snd/load[bss].asm','th02/snd/snd[bss].asm','th02/hardware/frmdelay.h',
 'th02/frmdely1.cpp','th02/hardware/frmdely1.cpp']
REMAPS={'th03/snd_se.cpp':'src/main/sound/se.cpp','th03/snd_kaja.cpp':'src/main/sound/kaja.cpp',
        'th02/frmdely1.cpp':'src/main/hardware/frame_delay.cpp'}
LOCAL=[*REMAPS.values(),'src/main/sound/se.hpp','src/main/sound/kaja.hpp','src/main/hardware/frame_delay.hpp']
ACTIVE,PLAYING,FRAME,PRIORITY,DURATION,FM,MIDI,VECTOR,POSSIBLE,FILENAME,CLOCK=0x880,0x88c,0x88d,0x896,0x8b7,0x1c70,0x1c71,0x1c72,0x1c73,0x1c74,0x144e


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[]
    for name,start,size,cleanup in RANGES:
        body=image[CS*16+start:CS*16+start+size]
        if len(body)!=size:raise ValueError('sound complete body/far cleanup differs')
        ins=list(decoder.disasm(body,start));bounds={i.address for i in ins}
        wanted=('retf',str(cleanup) if cleanup else '')
        if not ins or sum(i.size for i in ins)!=size or (ins[-1].mnemonic,ins[-1].op_str)!=wanted:raise ValueError('sound complete body/far cleanup differs')
        edges=[]
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf') and (i.mnemonic,i.op_str)!=wanted:raise ValueError('sound interior return differs')
            if i.mnemonic in ('in','out'):raise ValueError('sound unknown port')
            if i.mnemonic=='int' and (name not in ('mode','volume','load','update','kaja','measure') or i.op_str not in (('0x60',) if name in ('mode','update') else ('0x60','0x61','0x21') if name=='load' else ('0x60','0x61'))):raise ValueError('sound unknown interrupt')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('sound indirect edge')
            if i.mnemonic=='lcall':raise ValueError('sound unknown far interface')
            dest=i.operands[0].imm
            if i.mnemonic=='call':
                if name!='measure' or dest!=0x372 or not j or ins[j-1].bytes!=b'\x0e':raise ValueError('sound near call lacks PUSH CS/far entry')
            elif dest not in bounds:raise ValueError('sound branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=start,size=size,cleanup=cleanup,instructions=len(ins),sha256=sha(body),edges=edges))
    if any(image[CS*16+a:CS*16+a+1]!=b'\x90' for a in ALIGN):raise ValueError('sound complete producer alignment differs')
    return dict(bodies=rows[:-1],frame_helper=rows[-1],body_bytes=535,producer_bytes=4,producer_offsets=ALIGN)


class SoundProbe(Probe):
    """Native sound CODE; injected interrupt registers, DOS requests, signature and IRQ."""
    def __init__(self,mz,s):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x2c7e0,0x2e3f0,0x40000
        for name,value in [('CS',0x2c7e),('DS',0x2e3f),('SS',0x4000),('ES',0x3333),('BP',0x7777),('SI',0x1357),('DI',0x2468),('AX',0xace1),('EFLAGS',0x202|(0x400 if s.get('df') else 0))]:self.set(name,value)
        self.s=s;self.errors=[];self.events=[];self.writes=[];self.stop=False;self.polls=self.delays=0
        def guard(fn):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop()
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2c7e:raise ValueError('sound terminal segment alias')
                self.stop=True;uc.emu_stop();return
            off=address-self.code
            if self.get('CS')!=0x2c7e or not any(a<=off<a+n for _,a,n,_ in RANGES):raise ValueError('CPU escaped sound bodies')
            if off==0x372:self.delays+=1
            if off==0x37b and not s.get('stalled_clock'):self.word(CLOCK,u16(self.word(CLOCK)+s.get('tick',1)))
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            if self.data<=address and address+size<=self.data+65536:
                self.writes.append([address-self.data,size,value]);return
            raise ValueError('sound unexpected memory write')
        def intr(uc,number,user):
            ax=self.get('AX');ds=self.get('DS');dx=self.get('DX');bx=self.get('BX');cx=self.get('CX')
            if number==0x21 and s.get('name')=='load':
                if ax==0x3d00:
                    if (ds,dx)!=(0x2e3f,FILENAME):raise ValueError('sound open filename differs')
                    self.events.append(dict(kind='open',ax=ax,ds=ds,dx=dx,filename=self.cstring(ds,dx)))
                    self.set('AX',s.get('handle',7));self.set('EFLAGS',(self.get('EFLAGS')&~1)|s.get('open_cf',0))
                elif ax==0x3f00:
                    self.events.append(dict(kind='read',ax=ax,ds=ds,dx=dx,bx=bx,cx=cx))
                    self.set('AX',s.get('read_result',3));self.set('EFLAGS',(self.get('EFLAGS')&~1)|s.get('read_cf',0))
                elif ax>>8==0x3e:
                    self.events.append(dict(kind='close',ax=ax,ds=ds,bx=bx));self.set('AX',s.get('close_result',0xffff))
                else:raise ValueError('sound unknown DOS function')
            elif number in (0x60,0x61):
                self.events.append(dict(kind='driver',vector=number,ax=ax,dx=dx,bx=bx))
                if s.get('name')=='load':
                    if ax!=s.get('func',0x600):raise ValueError('sound load driver function differs')
                    self.set('DS',s.get('buffer_segment',0x6000));self.set('DX',s.get('buffer_offset',0x1234))
                    self.set('BX',s.get('driver_bx',bx));self.set('AX',s.get('driver_result',0xbeef))
                elif s.get('name') in ('volume','measure'):
                    if ax>>8!=(8 if s['name']=='volume' else 5):raise ValueError('sound poll function differs')
                    sequence=s.get('sequence',[0]);value=sequence[min(self.polls,len(sequence)-1)];self.polls+=1;self.set('AX',value)
                elif s.get('name')=='mode':
                    if ax>>8!=9 or number!=0x60:raise ValueError('sound mode function differs')
                    self.set('AX',s.get('driver_result',0))
                elif s.get('name')=='update':
                    if ax>>8!=12 or number!=0x60:raise ValueError('sound SE function differs')
                    self.set('AX',s.get('driver_result',0xffff))
                elif s.get('name')=='kaja':self.set('AX',s.get('driver_result',0xffff))
                else:raise ValueError('sound unexpected driver interrupt')
            else:raise ValueError('sound unknown interrupt')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))

    def word(self,at,value=None):
        if value is None:return struct.unpack('<H',self.uc.mem_read(self.data+at,2))[0]
        self.uc.mem_write(self.data+at,struct.pack('<H',u16(value)))

    def byte(self,at,value=None):
        if value is None:return self.uc.mem_read(self.data+u16(at),1)[0]
        self.uc.mem_write(self.data+u16(at),bytes([value&255]))

    def cstring(self,seg,off):
        values=[]
        for i in range(65536):
            value=self.uc.mem_read(seg*16+u16(off+i),1)[0]
            if not value:return values
            values.append(value)
        raise ValueError('sound fixture filename has no terminator')

    def run(self,name,args=(),*,terminal=True,budget=30000):
        self.s['name']=name;self.stop=False;self.errors.clear();self.set('CS',0x2c7e);self.set('SP',0xffc0)
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2c7e,*map(u16,args)))
        start,cleanup=next((a,c) for n,a,_,c in RANGES if n==name)
        self.uc.emu_start(self.code+start,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if self.stop!=terminal:raise ValueError('sound terminal/budget differs')
        if terminal and (self.get('SP')!=0xffc4+cleanup or self.get('DS')!=0x2e3f or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]):raise ValueError('sound far cleanup/callee-saved differs')
        if bool(self.get('EFLAGS')&0x400)!=bool(self.s.get('df')):raise ValueError('sound inherited DF differs')


def matrix(mz):
    rows=[]
    def observe(name,s,args=(),terminal=True):
        s=dict(s);p=SoundProbe(mz,s)
        if s.get('full_nonzero'):p.uc.mem_write(p.data,b'A'*65536)
        for at,key,default in [(ACTIVE,'active',1),(FM,'fm',1),(MIDI,'midi',0),(POSSIBLE,'possible',255),(VECTOR,'vector',255),(PLAYING,'playing',255),(FRAME,'frame',7)]:p.byte(at,s.get(key,default))
        p.word(CLOCK,0xbeef)
        if name=='pmd':
            pointer=s.get('pointer',0x3210);p.uc.mem_write(0x180,struct.pack('<2H',pointer,0x5000))
            signature=bytes(s.get('signature',[0x90,0x90,80,77,68]))
            for i,b in enumerate(signature):p.uc.mem_write(0x50000+u16(pointer+i),bytes([b]))
        if name=='load':
            filename=bytes(s.get('filename',list(b'staff\0abcdefg')))
            if len(filename)!=13:raise ValueError('sound source filename fixture length differs')
            source=s.get('source_offset',0xfff8)
            for i,b in enumerate(filename):p.uc.mem_write(0x50000+u16(source+i),bytes([b]))
            args=(source,0x5000,s.get('func',0x600))
            if not s.get('full_nonzero'):p.uc.mem_write(p.data+FILENAME,b'X'*40+b'\0')
        before=bytes(p.uc.mem_read(p.data,65536));expected=bytearray(before);expected_events=[];expected_ax=None
        if name=='mode':
            mode=1 if s.get('driver_result',0)&255!=255 else before[MIDI]
            expected[ACTIVE]=mode
            if mode==1 and s.get('driver_result',0)&255!=255:expected[FM]=1
            expected_ax=mode
        elif name=='pmd':
            expected[MIDI]=expected[FM]=expected[POSSIBLE]=0;expected[VECTOR]=0x60
            expected_ax=int(bytes(s.get('signature',[0x90,0x90,80,77,68]))[2:5]==b'PMD')
        elif name=='reset':expected[FRAME]=0;expected[PLAYING]=255
        elif name=='play':
            new=u16(args[0]);old=before[PLAYING]
            if before[FM] and (old==255 or before[u16(PRIORITY+old)]<=before[u16(PRIORITY+new)]):
                expected[PLAYING]=new&255
                if old!=255:expected[FRAME]=0
        elif name=='update':
            old=before[PLAYING]
            if before[FM] and old!=255:
                frame=(before[FRAME]+1)&255
                if before[u16(DURATION+old)]<frame:expected[FRAME]=0;expected[PLAYING]=255
                else:expected[FRAME]=frame
                if before[FRAME]==0:expected_events=[(0x60,0xc00|old)]
        elif name=='kaja':
            expected_ax=s.get('driver_result',0xffff) if before[ACTIVE] else 0xace1
            if before[ACTIVE]:expected_events=[(0x61 if before[MIDI]==1 else 0x60,u16(args[0]))]
        elif name=='load':
            expected[FILENAME:FILENAME+13]=filename
            if terminal and s.get('func',0x600)==0x600 and before[MIDI]:
                i=1
                while expected[u16(FILENAME+i)]:
                    i=u16(i+1)
                    if not i:raise ValueError('sound scalar scan has no terminator')
                for j,b in enumerate(b'md\0'):expected[u16(FILENAME+i+j)]=b
            if terminal:expected_ax=s.get('close_result',0xffff)
        elif name=='measure' and not before[ACTIVE]:
            if terminal:struct.pack_into('<H',expected,CLOCK,u16(s.get('tick',1)))
            else:expected[CLOCK:CLOCK+2]=b'\0\0'
        p.run(name,args,terminal=terminal,budget=30000 if terminal else 3000)
        after=bytes(p.uc.mem_read(p.data,65536))
        if after!=bytes(expected):raise ValueError('sound full DGROUP scalar differs: '+str((name,s,args)))
        if expected_ax is not None and p.get('AX')!=u16(expected_ax):raise ValueError('sound scalar AX differs')
        if name in ('update','kaja') and [(e['vector'],e['ax']) for e in p.events]!=expected_events:raise ValueError('sound ordered interrupt differs')
        if name in ('volume','measure') and (name!='measure' or before[ACTIVE]):
            if any(e['vector']!=(0x61 if before[MIDI]==1 else 0x60) or (name=='measure' and before[MIDI]==1 and e['dx']!=0xc0) for e in p.events):raise ValueError('sound poll vector/divisor differs')
            if terminal and p.polls!=s['expected_polls']:raise ValueError('sound poll count differs')
        if name=='load' and terminal:
            events=p.events;handle=s.get('handle',7);driverbx=s.get('driver_bx',handle);readresult=s.get('read_result',3)
            filename_expected=[]
            for value in expected[FILENAME:]:
                if not value:break
                filename_expected.append(value)
            wanted=[dict(kind='open',ax=0x3d00,ds=0x2e3f,dx=FILENAME,filename=filename_expected),
              dict(kind='driver',vector=0x61 if s.get('func',0x600)==0x600 and before[MIDI] else 0x60,ax=s.get('func',0x600),dx=FILENAME,bx=handle),
              dict(kind='read',ax=0x3f00,ds=s.get('buffer_segment',0x6000),dx=s.get('buffer_offset',0x1234),bx=driverbx,cx=0x5000),
              dict(kind='close',ax=0x3e00|(readresult&255),ds=0x2e3f,bx=driverbx)]
            if events!=wanted:raise ValueError('sound full ordered DOS/driver requests differ')
        if name=='load' and not terminal and p.events:raise ValueError('sound scan budget reached external interrupt')
        if name=='measure' and not before[ACTIVE] and p.delays!=1:raise ValueError('sound fallback native delay differs')
        rows.append(dict(name=name,scenario=s,args=args,terminal=terminal,events=p.events,polls=p.polls,delays=p.delays,
                         writes=p.writes,ax=p.get('AX') if expected_ax is not None else None,before_sha256=sha(before),after_sha256=sha(after)))
    for df in (0,1):
        for result in (0,1,0xfe,0xff,0x12ff):
            for midi in (0,1,255):observe('mode',dict(df=df,driver_result=result,midi=midi,fm=231))
        for pointer in (0x3210,0xfffd):
            for signature in ([0x90,0x90,80,77,68],[0,0,80,77,68],[0,0,0,77,68],[0,0,80,0,68],[0,0,80,77,0]):observe('pmd',dict(df=df,pointer=pointer,signature=signature))
        observe('reset',dict(df=df))
        for active in (0,1,255):
            for midi in (0,1,255):observe('kaja',dict(df=df,active=active,midi=midi,driver_result=0x1234),(0xb00,))
        for midi in (0,1,255):
            for volume in (0,128,255):observe('volume',dict(df=df,midi=midi,sequence=[volume^255,0xab00|volume],expected_polls=2),(0x1200|volume,))
            observe('volume',dict(df=df,midi=midi,sequence=[0]),(1,),False)
            for measure,sequence in [(0,[0]),(1,[0,1]),(0xffff,[0x7fff,0xffff]),(0x8000,[0x7fff,0x8000])]:observe('measure',dict(df=df,midi=midi,sequence=sequence,expected_polls=len(sequence)),(3,measure))
            observe('measure',dict(df=df,midi=midi,sequence=[0x7fff]),(3,0xffff),False)
        for frames in (0,1,3,0xffff):observe('measure',dict(df=df,active=0,tick=0xffff),(frames,0xffff))
        observe('measure',dict(df=df,active=0,stalled_clock=True),(1,0),False)
        for midi in (0,1,255):
            for func in (0x600,0xb00,0x1234):
                for filename in (b'staff\0abcdefg',b'\0X\0abcdefghij',b'ABCDEFGHIJKL\0',b'ABCDEFGHIJKLM'):
                    observe('load',dict(df=df,midi=midi,func=func,filename=list(filename),handle=5,open_cf=1,read_result=0xffff,read_cf=1,driver_bx=0x2345))
        observe('volume',dict(df=df,active=0,midi=255,sequence=[128],expected_polls=1),(128,))
        for handle,cf,read_result in ((0,0,0),(7,0,0x5000),(0xffff,1,0xffff)):
            observe('load',dict(df=df,midi=1,handle=handle,open_cf=cf,read_result=read_result,read_cf=cf,buffer_segment=0x6100,buffer_offset=0xfff0))
        observe('load',dict(df=df,full_nonzero=True,filename=list(b'A'*13),midi=1),terminal=False)
    for old in range(33):
        for new in range(33):observe('play',dict(playing=old,frame=7),(new,))
    for fm in (0,1,255):
        for old in (255,0,254):
            for new in (33,255,256,0x8000,0xffff):observe('play',dict(fm=fm,playing=old,frame=255,df=1),(new,))
    for old in list(range(33))+[255,254]:
        for frame in (0,1,80,254,255):observe('update',dict(playing=old,frame=frame))
    for fm in (0,255):observe('update',dict(fm=fm,playing=2,frame=0,df=1))
    for se in range(33):
        scenario={'df':se&1};p=SoundProbe(mz,scenario);p.byte(FM,1)
        before=bytes(p.uc.mem_read(p.data,65536));expected=bytearray(before)
        duration=before[DURATION+se];history=[]
        p.run('reset');p.run('play',(se,))
        for _ in range(duration+2):
            p.run('update');history.append([p.byte(PLAYING),p.byte(FRAME)])
        wanted=[[se,frame] for frame in range(1,duration+1)]+[[255,0],[255,0]]
        expected[PLAYING]=255;expected[FRAME]=0;after=bytes(p.uc.mem_read(p.data,65536))
        if history!=wanted or after!=bytes(expected):raise ValueError('sound continuous effect scalar differs')
        if [(e['vector'],e['ax']) for e in p.events]!=[(0x60,0xc00|se)]:raise ValueError('sound continuous effect interrupts differ')
        rows.append(dict(name='effect_chain',scenario=scenario,se=se,terminal=True,native_calls=duration+4,
            history=history,events=p.events,before_sha256=sha(before),after_sha256=sha(after)))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('sound prior input proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_sound.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    local={p:(ROOT/p).read_bytes() for p in LOCAL};inputs.update({p:sha(d) for p,d in local.items()})
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('sound input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    table=bytes(int(n) for n in re.findall(rb'\bdb\s+(\d+)',providers['th03/snd/se_priority[data].asm']))
    if len(table)!=66:raise ValueError('sound frozen table ownership differs')
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('sound invalid image')
        if mz.program_image[DS*16+PRIORITY:DS*16+PRIORITY+66]!=table:raise ValueError('sound complete priority/duration data differs')
        observed=dict(path=path,analysis=analyze(mz.program_image),table_sha256=sha(table),cpu=matrix(mz))
        if observations:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('sound complete body/helper bytes or CFG differ')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                wanted=(f'#include "{REMAPS[p]}"\n'.encode() if p in REMAPS else d)
                if p.endswith('.asm'):wanted=wanted.replace(b'\r\n',b'\n');cached=cached.replace(b'\r\n',b'\n')
                if cached!=wanted:raise ValueError('sound cached frozen/remapped provider differs: '+p)
            for p,d in local.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                if cached!=d:raise ValueError('sound maintained MAIN cached provider differs')
            rows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));target=parse_mz((ROOT/observations[0]['path']).read_bytes())
            observed['comparisons']={}
            for module,at,size in MODULES:
                row=next(r for r in rows if r['module']==module and r['size'])
                if (row['segment'],row['offset'],row['size'])!=(CS,at,size):raise ValueError('sound complete MAP contribution differs')
                observed['comparisons'][module]=extent_observation(target,mz,row)
                if not observed['comparisons'][module]['raw_slice_equal'] or observed['comparisons'][module]['target_ordered_relocations'] or observed['comparisons'][module]['candidate_ordered_relocations']:raise ValueError('sound raw bytes/empty relocation sites differ')
            def normalized(cpu):return [{k:v for k,v in row.items() if k not in ('before_sha256','after_sha256')} for row in cpu]
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']):raise ValueError('sound target/cached CPU differs')
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('sound canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('sound frozen provider changed')
    result=dict(kind='th03-mainl-complete-sound-chain-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,
        providers={p:sha(d) for p,d in providers.items()},producer_remaps=REMAPS,observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),
        diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS complete sound535/producer4/native delay21 and explicit interrupt contracts:',args.output)


if __name__=='__main__':main()
