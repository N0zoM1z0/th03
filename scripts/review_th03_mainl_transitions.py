#!/usr/bin/env python3
"""Remaining MAINL staff bodies: native effects and explicit orchestration models."""
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
from review_th03_mainl_cutscene import CS, DS, Probe, REVISION, sha
from review_th03_mainl_snow import signed, u16, PAGE, FRAME, VSYNC, CAP, SEED

ROOT=Path(__file__).resolve().parents[1]
SNOW_PROOF_SHA256='37de7058e3e2bf7fb66eeefbd464d85425469b2f481d0e80a0299c2dddfbe40a'
RANGES=[('unput',0x24e6,123,'6'),('dissolve',0x2731,211,'8'),
        ('entrance',0x2804,211,'2'),('leave',0x28d7,183,'2'),('gallery',0x298e,52,'6'),
        ('normal',0x29c2,229,'6'),('double',0x2aa7,358,'6'),('hold',0x2c0d,139,'6'),
        ('verdict',0x2c98,389,''),('staff',0x2e1d,980,'')]
# Snow frame and clear are declared near interfaces; their prior actual CPU proof remains separate.
NEAR={(CS,0x2561):('blue_clear',0,0),(CS,0x2576):('reset',0,0),
      (CS,0x26e5):('snow_frame',0,0),(CS,0x26b5):('measure_gate',4,4)}
FAR={(0,0xc36):('grcg_color',4,4),(0,0xb9e):('grcg_box',8,8),(0,0xc60):('grcg_off',0,0),
     (0,0x57a):('fade_out',2,2),(0,0x17d0):('palette_show',0,0),(0,0x1a68):('rgb',4,4),
     (0xc7e,0x6e2):('music',2,2),(0xc7e,0x84):('volume',2,0),(0xc7e,0xa0):('music_load',6,0),
     (0xc7e,0x7c8):('load_noalpha',8,8),(0xc7e,0x73e):('load_alpha',8,8),
     (0xc7e,0x372):('delay',2,2),(0xc7e,0x950):('free',2,2),(0xc7e,0xdc2):('input',0,0),
     (0xc7e,0x9b7):('font',10,10),(0xc7e,0xf32):('put_noalpha',6,6),(0xc7e,0x1f4):('put_alpha',6,6)}
SOURCES=['th03_mainl.asm','th03/formats/cdg_unput_upwards.asm','th03/formats/cdg_put_dissolve.asm',
         'th03/formats/cdg_put_dissolve[data].asm','th03/formats/cdg.inc','th03/formats/cdg.h',
         'th03/resident.hpp','th03/playchar.hpp','th03/score.hpp','th03/snd/snd.h',
         'th02/snd/snd.h','libs/kaja/kaja.h','libs/master.lib/func.hpp']


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    entries={a for _,a,_,_ in RANGES};result=[]
    for name,start,size,cleanup in RANGES:
        body=image[CS*16+start:CS*16+start+size];instructions=list(decoder.disasm(body,start))
        if sum(i.size for i in instructions)!=size or not instructions or instructions[-1].mnemonic!='ret' or instructions[-1].op_str!=cleanup:
            raise ValueError('staff transition complete body/near cleanup differs')
        boundaries={i.address for i in instructions};edges=[]
        for i in instructions:
            if i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall'):
                if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('unexpected indirect staff transition edge')
                dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (CS,i.operands[0].imm)
                if i.mnemonic=='lcall':
                    if dest not in FAR:raise ValueError('unknown staff transition far interface')
                elif i.mnemonic=='call':
                    if dest not in NEAR and dest[1] not in entries:raise ValueError('staff transition near call enters unknown/interior body')
                elif dest[1] not in boundaries:raise ValueError('staff transition branch leaves body/enters operand')
                edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        result.append(dict(name=name,offset=start,size=size,instructions=len(instructions),sha256=sha(body),edges=edges))
    return result


class TransitionProbe(Probe):
    """Actual ten bodies; snow/timing/graphics/font/load/sound are declared models."""
    def __init__(self,mz,*,sound=False,keys=(1,),io_result=1):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x295f0,0x2e3f0,0x40000
        for name,value in (('CS',0x295f),('DS',0x2e3f),('ES',0x3333),('SS',0x4000),('BP',0x7777),('SI',0x1357),('DI',0x2468),('EFLAGS',0x202)):self.set(name,value)
        self.events,self.ports,self.writes,self.errors,self.effects=[],[],[],[],[];self.stop=False;self.trap=None
        self.snow_frames=0;self.input_calls=0;self.fault_address=0;self.call_count=0
        self.uc.mem_write(self.data+0x21ea,struct.pack('<HH',0,0x5000));self.uc.mem_write(0x50000,b'\0'*256)
        self.uc.mem_write(0xe0000,b'\xff'*65538);self.uc.mem_write(self.data+0x880,bytes([sound]))
        for slot in range(32):self.slot(slot,32,4)
        self.word(PAGE,0);self.word(0x27cc,2);self.word(0x27ce,65);self.word(0x27d0,200)
        self.word(0x27d2,200);self.word(0x27d4,0);self.word(0x27d8,264);self.word(0x27da,263)
        self.uc.mem_write(self.data+0x27c5,b'\x01\x01');self.uc.mem_write(self.data+0x27d6,b'\0\0')
        imports={(0x2000+s)*16+o:(name,count,cleanup,4) for (s,o),(name,count,cleanup) in FAR.items()}
        imports.update({self.code+o:(name,count,cleanup,2) for (s,o),(name,count,cleanup) in NEAR.items()})

        def guard(callback):
            def invoke(*args):
                try:return callback(*args)
                except Exception as error:self.errors.append(str(error));self.uc.emu_stop()
            return invoke

        def code(uc,address,size,user):
            self.fault_address=address
            if address==self.code+0xff00:
                self.stop=True;uc.emu_stop();return
            if address==self.code+0x2731:
                sp=self.get('SP');args=list(struct.unpack('<4H',uc.mem_read(self.stack+sp+2,8)))
                self.effects.append(dict(args=args,frame=self.word(FRAME),page=bytes(uc.mem_read(self.data+PAGE,1))[0],alpha_flag=bytes(uc.mem_read(self.data+0x27d7,1))[0]))
            if address in imports:
                name,count,cleanup,retbytes=imports[address];sp=self.get('SP')
                coordinate=(self.get('CS')-0x2000,address-self.get('CS')*16)
                if coordinate not in (FAR if retbytes==4 else NEAR):raise ValueError('staff transition interface segment alias')
                words=list(struct.unpack('<'+'H'*((retbytes+count)//2),uc.mem_read(self.stack+sp,retbytes+count)))
                args=words[retbytes//2:];event=dict(name=name,args=args,frame=self.word(FRAME),page=bytes(uc.mem_read(self.data+PAGE,1))[0])
                if name=='blue_clear':event['modeled_words']=16000
                elif name=='reset':
                    for i in range(80):uc.mem_write(self.data+0x22c2+i*16,b'\0')
                elif name=='snow_frame':
                    # Prior actual snow proof is separate. This model supplies one tick/page flip.
                    page=bytes(uc.mem_read(self.data+PAGE,1))[0];self.ports.extend([[0xa4,page],[0xa6,(1-page)&255]])
                    uc.mem_write(self.data+PAGE,bytes([(1-page)&255]));self.word(VSYNC,0);self.snow_frames+=1
                elif name=='measure_gate':
                    value=int(signed(self.word(FRAME))>(192 if sound else signed(args[0])))
                    # Explicit music model returns measure FFFF, above all supplied thresholds.
                    self.set('AX',value);event['returned_ax']=value;event['modeled_measure']=65535 if sound else None
                elif name in ('put_alpha','put_noalpha'):
                    event['alpha_flag']=bytes(uc.mem_read(self.data+0x27d7,1))[0]
                    event['slow_flag']=bytes(uc.mem_read(self.data+0x27c5,1))[0]
                elif name in ('load_alpha','load_noalpha'):
                    event['filename_hex']=self.cstring(args[1],args[2]).hex();self.slot(args[3],32,4);self.set('AX',io_result)
                elif name in ('music_load','rgb'):
                    event['filename_hex']=self.cstring(*args[:2]).hex();self.set('AX',io_result)
                elif name=='font':event['text_hex']=self.cstring(*args[:2]).hex()
                elif name=='input':
                    key=keys[min(self.input_calls,len(keys)-1)];self.word(0x1d0c,key);self.input_calls+=1;event['key']=key
                elif name=='palette_show':event['tone']=self.word(0x578)
                self.events.append(event);self.set('SP',sp+retbytes+cleanup)
                self.set('CS',words[1] if retbytes==4 else 0x295f);self.set('IP',words[0]);return
            offset=address-self.code
            if self.get('CS')!=0x295f or not any(a<=offset<a+n for _,a,n,_ in RANGES):raise ValueError('CPU escaped reviewed staff transition bodies')

        def write(uc,access,address,size,value,user):
            if 0xe0000<=address<0xf0002:self.writes.append([address-0xe0000,size,value])

        def output(uc,port,width,value,user):
            if port not in (0xa4,0xa6) or width!=1:raise ValueError('unexpected staff transition port/width')
            self.ports.append([port,value])

        def interrupt(uc,number,user):
            if number==0:self.trap=dict(number=0,address=self.fault_address);uc.emu_stop()
            else:raise ValueError('unexpected staff transition interrupt')

        def input_port(uc,port,width,user):self.errors.append('unexpected staff transition input port');uc.emu_stop();return 0
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(interrupt))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,input_port,None,1,0,reg.UC_X86_INS_IN)

    def cstring(self,offset,segment):
        data=bytes(self.uc.mem_read(segment*16+offset,256))
        if b'\0' not in data:raise ValueError('staff transition model string exceeds256 bytes')
        return data.split(b'\0',1)[0]

    def slot(self,slot,width,height):
        self.uc.mem_write(self.data+0x1d0e+u16(slot*16),struct.pack('<8H',0,u16(width),u16(height),0,0,0,0,0))

    def run(self,entry,args=(),budget=5000000,terminal=True,trap=False):
        self.stop=False;self.trap=None;self.errors.clear();self.call_count+=1
        self.set('SP',0xffd0);self.uc.mem_write(self.stack+0xffd0,struct.pack('<'+'H'*(len(args)+1),0xff00,*args))
        self.uc.emu_start(self.code+entry,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if bool(self.trap)!=trap or self.stop!=terminal:raise ValueError('staff transition terminal/trap/budget differs')
        if terminal and (self.get('SP')!=0xffd2+len(args)*2 or self.get('DS')!=0x2e3f or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]):raise ValueError('staff transition stack/callee-saved differs')


def quotient(n,d):return abs(n)//abs(d)*(1 if (n>=0)==(d>=0) else -1)


def native_matrix(mz):
    unputs=[];dissolves=[]
    for width in (0,16,32,33):
        for height in (8,9):
            for df in (False,True):
                p=TransitionProbe(mz);p.slot(0,width,height)
                if df:p.set('EFLAGS',0x602)
                p.run(0x24e6,(0,200,320));words=width>>4;start=u16((320-quotient(width,2))//8+(200+quotient(height,2)-2)*80)
                offsets=[];at=start
                for _ in range(3):
                    for _ in range(words):offsets.append(at);at=u16(at+(-2 if df else 2))
                    at=u16(at+80-words*2)
                expected=bytearray(b'\xff'*65538)
                for at in offsets:expected[at:at+2]=b'\0\0'
                if p.writes!=[[at,2,0] for at in offsets] or bytes(p.uc.mem_read(0xe0000,65538))!=expected or bool(p.get('EFLAGS')&0x400)!=df:raise ValueError('native unput three-row/rounding/DF arithmetic differs')
                unputs.append(dict(width=width,height=height,df=df,writes=p.writes,e_sha256=sha(expected)))
    for strength in (*range(9),65535):
        for alpha in (0,1):
            for slow in (0,1):
                p=TransitionProbe(mz);p.uc.mem_write(p.data+0x27d7,bytes([alpha]));p.uc.mem_write(p.data+0x27c5,bytes([slow]))
                p.run(0x2731,(strength,0,200,320));effective=strength&7;expected=bytearray(b'\xff'*65538);writes=[]
                if effective:
                    for row in range(198,202):
                        mask=struct.unpack('<H',p.uc.mem_read(p.data+0xaa2+effective*8+(row&3)*2,2))[0]
                        for word in range(2):
                            at=u16(38+row*80+word*2);value=(~mask)&65535;struct.pack_into('<H',expected,at,value);writes.append([at,2,value])
                if p.writes!=writes or bytes(p.uc.mem_read(0xe0000,65538))!=expected or p.events[0]['name']!=('put_alpha' if alpha and slow else 'put_noalpha') or p.events[0]['args']!=[0,198,304]:raise ValueError('native dissolve modulo/alpha/mask/window differs')
                dissolves.append(dict(strength=strength,alpha=alpha,slow=slow,effective=effective,events=p.events,writes=writes,e_sha256=sha(expected)))
    p=TransitionProbe(mz);p.slot(0,0,0);p.run(0x2731,(1,0,200,320),budget=1000,terminal=False)
    return dict(unput_cases=unputs,dissolve_cases=dissolves,zero_width_budget=dict(terminal=False,word_writes=len(p.writes)))


def frame_matrix(mz):
    cases=[]
    for entry in (0x2804,0x28d7,0x298e):
        for frame in (-1,0,63,64,65,66,159,160,161,162):
            p=TransitionProbe(mz);p.word(FRAME,u16(frame));p.uc.mem_write(p.data+0x27d6,b'\x07')
            p.run(entry,(0,200,320) if entry==0x298e else (0,))
            puts=[e for e in p.events if e['name'].startswith('put_')]
            if entry==0x2804:
                strengths=[max(0,7-quotient(frame,8))]*2 if frame<=65 else []
                if p.word(0x27d8)!=(262 if frame<=65 else 264):raise ValueError('entrance position clamp differs')
            elif entry==0x28d7:
                strengths=[min(7,quotient(frame,20))]*2 if frame<160 else []
                if p.word(0x27d8)!=(263 if frame<160 else 264):raise ValueError('leave upward position differs')
            else:strengths=[max(0,7-quotient(frame,20))] if frame<=160 else []
            effective=[s&7 for s in strengths]
            actual=[e['frame'] for e in puts]
            if len(puts)!=len(strengths) or actual!=[u16(frame)]*len(strengths):raise ValueError('frame effect invocation count differs')
            if [e['args'][0] for e in p.effects]!=[u16(s) for s in strengths]:raise ValueError('actual frame dissolve-strength arguments differ')
            cases.append(dict(entry=entry,frame=frame,requested_strengths=strengths,effective_strengths=effective,actual_effect_args=p.effects,puts=puts,words_written=len(p.writes),grcg=[e for e in p.events if e['name'].startswith('grcg')]))
    p=TransitionProbe(mz);p.word(0x27ce,7);p.run(0x2804,(0,),terminal=False,trap=True)
    return dict(cases=cases,short_duration_divide_trap=p.trap)


def transition_matrix(mz):
    cases=[]
    for entry in (0x29c2,0x2aa7,0x2c0d):
        for speed in (1,2):
            for sound in (False,True):
                p=TransitionProbe(mz,sound=sound);p.word(0x27cc,speed);p.run(entry,(10,8,3))
                length=193 if sound else 257;expected=length*2+(0 if entry==0x2c0d else 2)
                if p.snow_frames!=expected or p.word(FRAME)!=(length if entry==0x2c0d else length):raise ValueError('two phase transition/gate/cleanup frame counts differ')
                expected_center=(200 if speed==2 else 247)-(0 if entry==0x2c0d else 80)
                if [p.word(0x27d8),p.word(0x27da)]!=[expected_center]*2:raise ValueError('transition final centered row differs')
                cases.append(dict(entry=entry,speed=speed,sound=sound,snow_frames=p.snow_frames,centers=[p.word(0x27d8),p.word(0x27da)],held_center=p.word(0x27d2),effect_calls=len([e for e in p.events if e['name'].startswith('put_')]),grcg_calls=len([e for e in p.events if e['name']=='grcg_box']),ports_count=len(p.ports)))
    return cases


def expected_skill(base,d6,d7,d8):
    if d7==3:base=(base+d6//2+2)&255
    if d7 in (3,4):base=(base+d6//2+7)&255
    if d7>=5:base=(base+15)&255
    return 100 if d8 else min(base,100)


def verdict_matrix(mz):
    cases=[]
    for digits in ([0]*8,[1]+[0]*7,[0,0,1]+[0]*5,list(range(1,9)),[9]*8):
        for skill in (0,9,10,99,100):
            p=TransitionProbe(mz);p.uc.mem_write(p.data+0x27dc,bytes([3,*digits]))
            p.uc.mem_write(p.data+0x27e6,bytes([3,8,skill]))
            def label(table,index):return list(struct.unpack('<HH',p.uc.mem_read(p.data+table+index*4,4)))
            expected=[label(0xae2,8)+[47,174,352],label(0xb06,3)+[47,199,360]]
            highest=max((i+1 for i,d in enumerate(digits) if d),default=0)
            x=408-highest*8
            for d in reversed(digits[:highest]):expected.append(label(0xb16,d)+[47,224,x]);x+=16
            expected.extend([label(0xb16,3)+[47,224,x],label(0xb16,3)+[47,248,408]])
            x=392 if skill>=100 else 400 if skill>=10 else 408
            for d in str(skill):expected.append(label(0xb16,int(d))+[47,291,x]);x+=16
            expected.append([0xc25,0x2e3f,47,291,x]);p.run(0x2c98)
            if [e['args'] for e in p.events]!=expected:raise ValueError('verdict leading zeros/continue append/skill centering/font ABI differs')
            cases.append(dict(score_digits=digits,skill=skill,font_requests=p.events))
    return cases


def staff_matrix(mz):
    cases=[]
    for base,d6,d7,d8,credits,sound in ((0,9,3,0,3,True),(0,9,4,0,3,True),(0,9,5,0,0,True),(0,9,3,1,2,True),(250,9,3,0,3,False)):
        p=TransitionProbe(mz,sound=sound,io_result=0)
        p.uc.mem_write(0x5000c,b'\x01');p.uc.mem_write(0x5000b,b'\x03');p.uc.mem_write(0x50036,bytes([credits]));p.uc.mem_write(0x50038,bytes([base]))
        digits=bytes([1,2,3,4,5,d6,d7,d8]);p.uc.mem_write(0x50018,digits);p.uc.mem_write(0x50010,struct.pack('<I',0x12345678))
        p.run(0x2e1d)
        skill=expected_skill(base,d6,d7,d8);length=193 if sound else 257
        if bytes(p.uc.mem_read(p.data+0x27e8,1))[0]!=skill or bytes(p.uc.mem_read(p.data+0x27dd,8))!=digits or p.input_calls!=456 or p.snow_frames!=length*20+472:raise ValueError('full staff score/skill/input/fade/orchestration differs')
        loads=[e for e in p.events if e['name'] in ('load_alpha','load_noalpha')]
        expected_files=['stf1.cdg','stf11.cdg','stf3.cdg','stf4.cdg','stf5.cdg','stf6.cdg','stf7.cdg','stf8.cdg','stf9.cdg','stf10.cdg','stf2.cdg','stf12.cdg']
        if [bytes.fromhex(e['filename_hex']).decode() for e in loads]!=expected_files or [e['args'][3] for e in loads]!=list(range(12)) or [e['args'][0] for e in p.events if e['name']=='free']!=list(range(32)):raise ValueError('staff load/free order differs')
        tones=[e['tone'] for e in p.events if e['name']=='palette_show']
        if tones[:3]!=[0,0,100] or tones[3:]!=[100]+[v for v in range(99,0,-1) for _ in range(2)]:raise ValueError('staff odd-frame fade tones differ')
        cases.append(dict(initial_skill=base,score_digits=list(digits),credits=credits,sound=sound,final_skill=skill,snow_frames=p.snow_frames,input_calls=p.input_calls,loads=loads,music=[e for e in p.events if e['name']=='music'],tones=tones,verdict_fonts=[e for e in p.events if e['name']=='font'],free_slots=32,ports_count=len(p.ports),final_frame=p.word(FRAME),final_page=bytes(p.uc.mem_read(p.data+PAGE,1))[0]))
    p=TransitionProbe(mz,keys=(0,));p.run(0x2e1d,budget=1500000,terminal=False)
    return dict(cases=cases,no_input_budget=dict(input_calls=p.input_calls,snow_frames=p.snow_frames,terminal=False,free_calls=len([e for e in p.events if e['name']=='free'])))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    path='.analysis/sol-mainl-snow-review-20261006.json';raw=(ROOT/path).read_bytes()
    if sha(raw)!=SNOW_PROOF_SHA256:raise ValueError('staff transition prior snow proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],path:sha(raw),'scripts/review_th03_mainl_transitions.py':sha(Path(__file__).read_bytes())}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('staff transition input changed: '+p)
    verify();providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in SOURCES}
    artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    patterns=struct.pack('<32H',*(int(n,2) for n in re.findall(rb'([01]{16})b',providers['th03/formats/cdg_put_dissolve[data].asm'])))
    observations=[]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid or mz.program_image[DS*16+0xaa2:DS*16+0xae2]!=patterns:raise ValueError('staff transition image/dissolve pattern differs')
        observed=dict(path=path,bodies=analyze(mz.program_image),native=native_matrix(mz),frames=frame_matrix(mz),transitions=transition_matrix(mz),verdict=verdict_matrix(mz),staff=staff_matrix(mz))
        observed['ordered_relocations']={name:[[r.segment,r.offset] for r in mz.relocations if CS*16+at<=r.segment*16+r.offset<CS*16+at+size] for name,at,size,_ in RANGES}
        if observations:
            tree=Path(path).parents[2]
            for p,original in providers.items():
                cached_path=str(tree/p);cached=(ROOT/cached_path).read_bytes();inputs[cached_path]=sha(cached)
                if cached!=(original.replace(b'\n',b'\r\n') if p.endswith('.asm') else original):raise ValueError('staff transition cached source association differs: '+p)
            for key in ('native','frames','transitions','verdict','staff'):
                if observed[key]!=observations[0][key]:raise ValueError('staff transition target/candidate CPU/model diagnostics differ: '+key)
            target=parse_mz((ROOT/observations[0]['path']).read_bytes())
            observed['raw_differences']={name:[at+i for i,(a,b) in enumerate(zip(target.program_image[CS*16+at:CS*16+at+size],mz.program_image[CS*16+at:CS*16+at+size])) if a!=b] for name,at,size,_ in RANGES}
            observed['ordered_relocations_equal']=observed['ordered_relocations']==observations[0]['ordered_relocations']
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('staff transition canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('staff transition frozen provider changed')
    result=dict(kind='th03-mainl-remaining-staff-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},observations=observations,new_body_bytes=2875,prior_snow_bytes=464,complete_carrier_bytes=3339,tools=dict(capstone_distribution=version('capstone'),unicorn_distribution=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print(f'PASS ten remaining staff bodies2875 and declared CPU/interface scopes: {args.output}')


if __name__=='__main__':main()
