#!/usr/bin/env python3
"""Bounded MAINL snow CPU review; flat blue plane and explicit clock/music models."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
import math
from pathlib import Path
import re
import struct
import subprocess

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows
from review_th03_mainl_cutscene import CS, DS, Probe, REVISION, sha

ROOT = Path(__file__).resolve().parents[1]
PROOF_SHA256 = "5a8afb0c78b4c2303258d8e0c8c152ccc5a62c1945807c89b227263cdc909ac4"
FLAKES, CAP, FRAME, PAGE, SLOW, ADAPT, VSYNC, SEED = 0x22c2, 0x22c0, 0x27c2, 0x27c4, 0x27c5, 0x27c6, 0x144e, 0x5b6
# name, original segment, offset, size, return kind, cleanup
RANGES = [("clear_blue",CS,0x2561,21,"ret",""), ("reset",CS,0x2576,26,"ret",""),
          ("spawn",CS,0x2590,169,"ret",""), ("update",CS,0x2639,70,"ret",""),
          ("render",CS,0x267f,54,"ret",""), ("measure_gate",CS,0x26b5,48,"ret","4"),
          ("snow_frame",CS,0x26e5,76,"ret",""),
          ("flake_put",CS,0x249a,76,"ret","6"),
          ("irand",0,0x1a3e,42,"retf",""), ("vector2",0xc7e,0x110,69,"retf","0xc")]
PROVIDERS = ["th03_mainl.asm","th03/staff.cpp","th03/end/staff.cpp","th03/sprites/flake.h",
             "th03/sprites/flake.bmp","th03/vector.cpp","th03/math/vector.cpp","th03/math/vector.hpp",
             "th02/math/vector.hpp","th01/math/subpixel.hpp","libs/master.lib/random.asm",
             "libs/master.lib/sin8[data].asm","libs/master.lib/func.hpp","th03/snd/snd.h",
             "th02/snd/snd.h","libs/kaja/kaja.h","Tupfile.lua"]


def signed(word):
    return word-65536 if word&32768 else word


def sine_words():
    return [int(math.floor(math.sin(i*math.pi/128)*256+0.5)) for i in range(320)]


def sprite_from_bmp(data):
    if (len(data)!=190 or data[:2]!=b"BM" or struct.unpack_from('<I',data,10)[0]!=62 or
            struct.unpack_from('<IiiHHI',data,14)!=(40,16,32,1,1,0) or
            data[54:62]!=b'\0\0\0\0\xff\xff\xff\0'):
        raise ValueError('snow BMP bounded one-bit layout/palette differs')
    return b''.join(data[62+row*4:64+row*4] for row in range(31,-1,-1))


def analysis(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    entries={(s,a) for _,s,a,_,_,_ in RANGES};rows=[]
    for name,segment,start,size,kind,cleanup in RANGES:
        body=image[segment*16+start:segment*16+start+size]
        instructions=list(decoder.disasm(body,start));bounds={i.address for i in instructions}
        if sum(i.size for i in instructions)!=size or not instructions or instructions[-1].mnemonic!=kind or instructions[-1].op_str!=cleanup:
            raise ValueError('snow complete body/return cleanup differs')
        edges=[]
        for i in instructions:
            if i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall'):
                if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):
                    raise ValueError('unexpected indirect snow edge')
                destination=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (segment,i.operands[0].imm)
                if i.mnemonic in ('call','lcall'):
                    if destination not in entries:raise ValueError('snow call enters unreviewed/interior body')
                elif destination[1] not in bounds:raise ValueError('snow branch leaves body or enters operand')
                edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=destination))
        rows.append(dict(name=name,segment=segment,offset=start,size=size,sha256=sha(body),instruction_count=len(instructions),edges=edges))
    table=struct.pack('<320h',*sine_words())
    if image[DS*16+0x5ba:DS*16+0x83a]!=table:raise ValueError('snow sine/cosine scalar table differs')
    return dict(bodies=rows,table_offset=0x5ba,table_size=640,table_sha256=sha(table),root_bytes=464,
                dependency_bytes=187,vector_following_byte=image[0xc7e*16+0x155])


def u16(value):return value&65535


def random_next(seed):
    seed=(seed*0x15a4e35+1)&0xffffffff
    return seed,(seed>>16)&32767


def state_digest(data):
    """Compare declared constructed state; retain full per-image unchanged checks."""
    return sha(data[SEED:SEED+4]+data[0x880:0x881]+data[VSYNC:VSYNC+2]+data[CAP:FLAKES+255*16])


def expected_spawn(data,seed):
    data=bytearray(data);new=[]
    for i in range(data[CAP]):
        at=FLAKES+i*16
        if data[at] or i*8>signed(struct.unpack_from('<H',data,FRAME)[0]):continue
        data[at]=1;values=[]
        for _ in range(4):seed,value=random_next(seed);values.append(value)
        left,top=(values[0]%10112,0) if i%4 else (10112,values[0]%6272)
        angle,length=80+values[1]%32,48+values[2]%64
        sine=sine_words();vx=(length*sine[angle+64])//256;vy=(length*sine[angle])//256
        struct.pack_into('<4H',data,at+2,left,top,u16(vx),u16(vy));struct.pack_into('<H',data,at+10,values[3]&3)
        new.append(dict(index=i,random_words=values,angle=angle,length=length,velocity=[vx,vy]))
    struct.pack_into('<I',data,SEED,seed)
    return bytes(data),new


def expected_update(data):
    data=bytearray(data)
    for i in range(data[CAP]):
        at=FLAKES+i*16
        if not data[at]:continue
        data[at]=1
        left,top,vx,vy=struct.unpack_from('<4H',data,at+2)
        left,top=u16(left+vx),u16(top+vy)
        if signed(left)<=0:left=u16(left+10112)
        if signed(top)>=6272:top=u16(top-6272)
        struct.pack_into('<2H',data,at+2,left,top)
    return bytes(data)


def expected_render(data,blue,sprites):
    blue=bytearray(blue);writes=[]
    for i in range(data[CAP]):
        at=FLAKES+i*16
        if not data[at]:continue
        left,top=map(lambda v:signed(v)//16,struct.unpack_from('<2H',data,at+2))
        cel=struct.unpack_from('<H',data,at+10)[0]
        if cel>=4:raise ValueError('constructed snow scalar cel outside reviewed sprite scope')
        offset=u16(left//8+top*80);rotation=left&7
        for word in struct.unpack_from('<8H',sprites,cel*16):
            dots=((word>>rotation)|(word<<(16-rotation)))&65535
            value=struct.unpack_from('<H',blue,offset)[0]|dots
            struct.pack_into('<H',blue,offset,value);writes.append([offset,2,value]);offset=u16(offset+80)
    return bytes(blue),writes


class SnowProbe(Probe):
    """Actual bounded code including far returns; only music/clock/banks modeled."""
    def __init__(self,mz,*,measure=4,inject_tick=None,df=False):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg
        self.uc.mem_map(0,0x100000);image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image))
        self.code,self.data,self.stack=0x295f0,0x2e3f0,0x40000
        for name,value in (('CS',0x295f),('DS',0x2e3f),('SS',0x4000),('ES',0x3333),('BP',0x7777),('SI',0x1357),('DI',0x2468),('EFLAGS',0x202|(0x400 if df else 0))):self.set(name,value)
        self.errors,self.ports,self.writes,self.far_frames,self.vectors,self.interrupts=[],[],[],[],[],[]
        self.stop=False;self.polls=0
        self.uc.mem_write(self.data+FLAKES,b'\0'*(16*255))
        self.uc.mem_write(0xa8000,b'\x5a\xa5'*32769)
        self.sprites=bytes(self.uc.mem_read(self.data+0xa62,64))

        def guard(callback):
            def invoke(*args):
                try:return callback(*args)
                except Exception as error:self.errors.append(str(error));self.uc.emu_stop()
            return invoke

        def code(uc,address,size,user):
            if address==self.code+0xff00 and self.get('CS')==0x295f:
                self.stop=True;uc.emu_stop();return
            if address==self.code+0x270e:
                self.polls+=1
                if inject_tick is not None and self.polls==inject_tick[0]:self.word(VSYNC,inject_tick[1])
            if address==0x2c7e0+0x110:
                sp=self.get('SP');words=list(struct.unpack('<8H',uc.mem_read(self.stack+sp,16)))
                if words[3]&255 not in range(80,112) and self.direct_entry!=(0xc7e,0x110):raise ValueError('spawn vector angle outside observed range')
                self.vectors.append(words)
            if address in (0x20000+0x1a67,0x2c7e0+0x152):
                sp=self.get('SP');self.far_frames.append(dict(address=address,sp=sp,words=list(struct.unpack('<HH',uc.mem_read(self.stack+sp,4)))))
            seg=self.get('CS')-0x2000;offset=address-(0x2000+seg)*16
            if not any(s==seg and a<=offset<a+n for _,s,a,n,_,_ in RANGES):raise ValueError('CPU escaped reviewed snow bodies')

        def write(uc,access,address,size,value,user):
            if 0xa8000<=address<0xb8002:self.writes.append([address-0xa8000,size,value])

        def output(uc,port,width,value,user):
            if port not in (0xa4,0xa6) or width!=1:raise ValueError('unexpected snow port/width')
            self.ports.append([port,value])

        def interrupt(uc,number,user):
            if number!=0x60 or self.get('AH')!=5:raise ValueError('unexpected snow interrupt/interface')
            self.interrupts.append(dict(number=number,ah=5,measure=measure));self.set('AX',measure)

        def input_port(uc,port,width,user):self.errors.append('unexpected snow input port');uc.emu_stop();return 0
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write))
        self.uc.hook_add(UC_HOOK_INTR,guard(interrupt))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT)
        self.uc.hook_add(UC_HOOK_INSN,input_port,None,1,0,reg.UC_X86_INS_IN)

    def state(self):return bytes(self.uc.mem_read(self.data,0x3300))

    def run(self,entry,args=(),segment=CS,budget=500000,terminal=True):
        self.stop=False;self.errors.clear();self.direct_entry=(segment,entry)
        far=segment!=CS;return_words=[0xff00,0x295f] if far else [0xff00]
        self.set('CS',0x2000+segment);self.set('SP',0xffd0)
        self.uc.mem_write(self.stack+0xffd0,struct.pack('<'+'H'*(len(args)+len(return_words)),*return_words,*args))
        self.uc.emu_start((0x2000+segment)*16+entry,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if self.stop!=terminal:raise ValueError('snow terminal/budget observation differs')
        if terminal and (self.get('SP')!=0xffd0+len(return_words)*2+len(args)*2 or self.get('DS')!=0x2e3f or self.get('CS')!=0x295f or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]):
            raise ValueError('snow cleanup/callee-saved contract differs')


def setup(p,cap=80,frame=639,seed=1,alive=False):
    for i in range(255):
        at=FLAKES+i*16
        p.uc.mem_write(p.data+at,struct.pack('<BB4HH4B',int(alive and i%3!=0),0x71,160+i*16,320+i*16,u16(-17),31,i%4,1,2,3,4))
    p.uc.mem_write(p.data+CAP,bytes([cap]));p.word(FRAME,u16(frame));p.word(VSYNC,1)
    p.uc.mem_write(p.data+PAGE,bytes([0,1,1]));p.uc.mem_write(p.data+SEED,struct.pack('<I',seed))


def matrix(mz):
    result={};p=SnowProbe(mz);setup(p,alive=True);before=bytearray(p.state())
    for i in range(80):before[FLAKES+i*16]=0
    p.run(0x2576)
    if p.state()!=before:raise ValueError('reset touches fields outside eighty alive bytes')
    result['reset']=dict(scoped_state_sha256=state_digest(p.state()),cleared=80)
    spawns=[]
    for cap in (0,1,4,50,80,81,255):
        for frame in (-1,0,7,8,2040):
            p=SnowProbe(mz);setup(p,cap,frame)
            expected,new=expected_spawn(p.state(),1);p.run(0x2590)
            if p.state()!=expected or len(p.vectors)!=len(new) or len(p.far_frames)!=len(new)*5:raise ValueError('spawn LCG/threshold/vector/stores/far returns differ')
            spawns.append(dict(capacity=cap,frame=frame,spawned=new,scoped_state_sha256=state_digest(p.state()),outside_array_indices=[r['index'] for r in new if r['index']>=80],vector_stack_words=p.vectors))
    result['spawn_cases']=spawns
    updates=[]
    for cap in (0,1,4,50,80,81,255):
        for left,top,vx,vy in ((0,6271,0,1),(1,6272,-2,0),(-10113,-1,0,0),(32767,32767,1,1)):
            p=SnowProbe(mz);setup(p,cap,alive=True)
            p.uc.mem_write(p.data+FLAKES,struct.pack('<BB4HH4B',2,0x71,u16(left),u16(top),u16(vx),u16(vy),0,1,2,3,4))
            expected=expected_update(p.state());p.run(0x2639)
            if p.state()!=expected:raise ValueError('snow single-wrap/signed-overflow/capacity update differs')
            updates.append(dict(capacity=cap,constructed_fields=[left,top,vx,vy],first_record=list(p.state()[FLAKES:FLAKES+16]),scoped_state_sha256=state_digest(p.state())))
    result['update_cases']=updates
    renders=[]
    for cap in (0,1,4,50,80):
        p=SnowProbe(mz);setup(p,cap,alive=True);before=p.state();blue=bytes(p.uc.mem_read(0xa8000,65538))
        expected,writes=expected_render(before,blue,p.sprites);p.run(0x267f)
        if bytes(p.uc.mem_read(0xa8000,65538))!=expected or p.writes!=writes or p.state()!=before:raise ValueError('snow actual glyph calls/flat blue writes differ')
        renders.append(dict(capacity=cap,writes=len(writes),blue_sha256=sha(expected)))
    result['render_cases']=renders
    clears=[]
    for df in (False,True):
        p=SnowProbe(mz,df=df);before=bytes(p.uc.mem_read(0xa8000,65538));p.run(0x2561)
        expected=bytearray(before)
        offsets=[u16((-2 if df else 2)*i) for i in range(16000)]
        for at in offsets:expected[at:at+2]=b'\0\0'
        if bytes(p.uc.mem_read(0xa8000,65538))!=expected or p.writes!=[[at,2,0] for at in offsets] or bool(p.get('EFLAGS')&0x400)!=df:raise ValueError('blue clear inherited DF/window differs')
        clears.append(dict(inherited_df=df,word_writes=len(offsets),blue_sha256=sha(expected)))
    result['clear_cases']=clears
    gates=[]
    for active in (0,1):
        for frame in (-32768,-1,192,193,32767):
            for measure in (3,4,65535):
                p=SnowProbe(mz,measure=measure);setup(p,frame=frame);p.uc.mem_write(p.data+0x880,bytes([active]));p.run(0x26b5,(256,4))
                expected=int(frame>192 and measure>=4) if active else int(frame>256)
                if p.get('AX')!=expected or len(p.interrupts)!=active:raise ValueError('music unsigned-measure/signed-frame gate differs')
                gates.append(dict(active=active,frame=frame,measure=measure,result=expected,interrupts=p.interrupts))
    result['gate_cases']=gates
    frames=[]
    for tick,page,adaptive,inject in ((1,0,1,None),(2,1,1,None),(2,0,0,None),(1,2,1,None),(1,255,1,None),(0,0,1,(5,2))):
        p=SnowProbe(mz,inject_tick=inject);setup(p);p.word(VSYNC,tick);p.uc.mem_write(p.data+PAGE,bytes([page,1,adaptive]))
        before=p.state();seed=struct.unpack_from('<I',before,SEED)[0];expected,new=expected_spawn(before,seed);expected=bytearray(expected_update(expected))
        blue,writes=expected_render(expected,bytes(p.uc.mem_read(0xa8000,65538)),p.sprites)
        if adaptive and tick>1:expected[CAP]=50;expected[SLOW]=expected[ADAPT]=0
        struct.pack_into('<H',expected,VSYNC,0);expected[PAGE]=(1-page)&255
        p.run(0x26e5)
        if p.state()!=expected or p.writes!=writes or bytes(p.uc.mem_read(0xa8000,65538))!=blue or p.ports!=[[0xa4,page],[0xa6,(1-page)&255]]:raise ValueError('snow frame spawn/update/render/adaptation/wait/page order differs')
        frames.append(dict(initial_tick=tick,page=page,adaptive=adaptive,injected_tick=inject,polls=p.polls,final_capacity=expected[CAP],ports=p.ports,draw_word_writes=len(writes),scoped_state_sha256=state_digest(p.state()),blue_sha256=sha(blue)))
    p=SnowProbe(mz);setup(p,cap=0);p.word(VSYNC,0);p.run(0x26e5,budget=10000,terminal=False)
    if p.ports or not p.polls:raise ValueError('snow zero-vsync budget must retain wait without page change')
    result['frame_cases']=frames;result['zero_vsync_budget']=dict(polls=p.polls,terminal=False,ports=p.ports)
    random_cases=[]
    for seed in (0,1,0xffffffff,0x80000000,0x12345678):
        p=SnowProbe(mz);p.uc.mem_write(p.data+SEED,struct.pack('<I',seed));expected=seed;values=[]
        for _ in range(20):
            expected,value=random_next(expected);p.run(0x1a3e,segment=0)
            if p.get('AX')!=value or bytes(p.uc.mem_read(p.data+SEED,4))!=struct.pack('<I',expected):raise ValueError('actual IRand LCG differs')
            values.append(value)
        random_cases.append(dict(initial_seed=seed,returned_words=values,final_seed=expected,executed_far_returns=len(p.far_frames)))
    result['random_cases']=random_cases
    vectors=[];sine=sine_words()
    for angle in (0,1,63,64,80,95,96,111,127,128,160,191,192,255):
        for length in (-32768,-1,0,1,48,111,32767):
            p=SnowProbe(mz);p.run(0x110,(u16(length),0x7700|angle,0x3402,0x2e3f,0x3400,0x2e3f),segment=0xc7e)
            expected=[u16(length*sine[angle+64]//256),u16(length*sine[angle]//256)]
            actual=list(struct.unpack('<2H',p.uc.mem_read(p.data+0x3400,4)))
            if actual!=expected or len(p.far_frames)!=1:raise ValueError('actual vector arithmetic floor/byte-angle/far cleanup differs')
            vectors.append(dict(angle=angle,unused_argument_high_byte=0x77,length=length,result_words=actual,executed_far_returns=1))
    result['vector_cases']=vectors
    result['top_level_calls_per_image']=1+35+28+5+2+30+6+1+100+98
    result['scope']='Actual snow/flake/LCG/vector instructions and far returns; no memory-read hook; clock/music explicit models and flat blue plane/page request log only'
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    proof_path='.analysis/sol-mainl-cutscene-review-20261006.json';raw=(ROOT/proof_path).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('snow decoded lineage proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],proof_path:sha(raw),'scripts/review_th03_mainl_snow.py':sha(Path(__file__).read_bytes())}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('snow input changed: '+p)
    verify();providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    if sha(stored)!=proof['stored_sha256']:raise ValueError('snow canonical MAINL differs')
    paths=[p for p in inputs if p.endswith('mainl.exe')]
    if len(paths)!=3:raise ValueError('snow target/two candidates absent')
    images=[parse_mz((ROOT/p).read_bytes()) for p in paths]
    if not all(m.valid for m in images):raise ValueError('invalid snow MZ')
    sprite=sprite_from_bmp(providers['th03/sprites/flake.bmp']);sine=struct.pack('<320h',*sine_words())
    literals=[int(n) for line in providers['libs/master.lib/sin8[data].asm'].decode('cp932').splitlines() if 'dw' in line for n in re.findall(r'-?\d+',line.split('dw',1)[1])]
    if struct.pack('<320h',*literals)!=sine:raise ValueError('frozen sine literals differ from independent scalar')
    observations=[];objects=[]
    for path,mz in zip(paths,images):
        if mz.program_image[DS*16+0xa62:DS*16+0xaa2]!=sprite:raise ValueError('snow target sprite differs from frozen BMP')
        result=dict(path=path,analysis=analysis(mz.program_image),runtime=matrix(mz))
        result['ordered_relocations']={name:[[r.segment,r.offset] for r in mz.relocations if segment*16+start<=r.segment*16+r.offset<segment*16+start+size]
                                       for name,segment,start,size,_,_ in RANGES}
        if path!=paths[0]:
            tree=Path(path).parents[2]
            map_path=next(p for p in inputs if str(tree) in p and p.endswith('mainl.map'))
            root_rows=[r for r in code_rows((ROOT/map_path).read_text(encoding='ascii'),len(mz.program_image)) if r['name']=='MAINL_03_TEXT' and r['size']]
            if [(r['module'],r['segment'],r['offset'],r['size']) for r in root_rows]!=[('th03_mainl.asm',CS,0x24e6,3339)]:raise ValueError('snow generated carrier MAP containment differs')
            result['generated_carrier_containment']=root_rows
            for p,original in providers.items():
                if p=='Tupfile.lua':
                    # The cached cold scaffold deliberately patches build orchestration.
                    # Consult the frozen resource rule without claiming cached byte identity.
                    result['frozen_build_rule_only']=sha(original)
                    continue
                cached_path=str(tree/p);cached=(ROOT/cached_path).read_bytes()
                if cached!=(original.replace(b'\n',b'\r\n') if p.endswith('.asm') else original):raise ValueError('snow cached provider association differs: '+p)
                inputs[cached_path]=sha(cached)
            asp_path=str(tree/'th03/sprites/flake.asp');asp=(ROOT/asp_path).read_bytes();inputs[asp_path]=sha(asp)
            generated=bytes(int(n,2) for n in re.findall(rb'([01]{8})b',asp))
            if generated!=sprite:raise ValueError('snow generated sprite differs from independent BMP extraction')
            obj_path=str(tree/'obj/th03/vector.obj');obj=describe_omf((ROOT/obj_path).read_bytes());inputs[obj_path]=sha((ROOT/obj_path).read_bytes())
            if not obj['valid'] or obj['module_name']!='th03/vector.cpp' or obj['translator_comments']!=['TC86 Borland C++ 4.02']:raise ValueError('snow vector cached OMF association differs')
            objects.append(obj);result['vector_object']=obj
        if observations:
            result['ordered_relocations_equal']=result['ordered_relocations']==observations[0]['ordered_relocations']
            if observations[0]['ordered_relocations']['spawn']!=list(reversed(result['ordered_relocations']['spawn'])) or len(result['ordered_relocations']['spawn'])!=6 or result['ordered_relocations_equal']:
                raise ValueError('snow retained original relocation-order failure differs')
            result['raw_body_differences']={name:[start+i for i,(a,b) in enumerate(zip(images[0].program_image[segment*16+start:segment*16+start+size],mz.program_image[segment*16+start:segment*16+start+size])) if a!=b]
                                            for name,segment,start,size,_,_ in RANGES}
            if result['raw_body_differences']!={name:([0x256a,0x256c,0x256d] if name=='clear_blue' else []) for name,*_ in RANGES}:raise ValueError('snow retained raw zero-producer failure differs')
            result['unowned_initial_dgroup_differences']=[dict(offset=i,target=a,candidate=b) for i,(a,b) in enumerate(zip(SnowProbe(images[0]).state(),SnowProbe(mz).state())) if a!=b]
            if result['runtime']!=observations[0]['runtime']:raise ValueError('target/candidate snow operations differ')
        observations.append(result)
    if objects[0]['dependency_timestamp_normalized_sha256']!=objects[1]['dependency_timestamp_normalized_sha256']:raise ValueError('snow vector objects differ beyond dependency timestamps')
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('snow canonical MAINL changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('snow frozen source changed')
    result=dict(kind='th03-mainl-bounded-generated-snow-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},observations=observations,sprite_bytes=64,sprite_sha256=sha(sprite),
                root_bytes=464,dependency_bytes=187,state_digest_scopes=[[SEED,4],[0x880,1],[VSYNC,2],[CAP,FLAKES+255*16-CAP]],tools=dict(capstone_distribution=version('capstone'),unicorn_distribution=version('unicorn')),diagnostic_checks_pass=True,root_raw_equal=False,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(f'PASS snow root464/dependencies187 and {observations[0]["runtime"]["top_level_calls_per_image"]*3} CPU/clock/music cases: {args.output}')


if __name__=='__main__':main()
