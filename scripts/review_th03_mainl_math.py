#!/usr/bin/env python3
"""Complete MAINL vectors/LUT; actual IATAN2, table arithmetic and divide traps."""
import argparse
from datetime import datetime,timezone
from importlib.metadata import version
import json
import math
from pathlib import Path
import re
import struct
import subprocess
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact
from review_th03_decoded_code import code_rows,extent_observation
from review_th03_mainl_cutscene import DS,Probe,REVISION,sha
from review_th03_mainl_snow import u16,signed,sine_words

ROOT=Path(__file__).resolve().parents[1];CS=0xc7e
PROOF='.analysis/sol-mainl-text-review-20261006.json'
PROOF_SHA256='43dc371d75d7dfb5ca734e31569ba80bcd675f41d6f332fe02649fbf307d4a1d'
RANGES=[('vector',CS,0x110,69,12),('between',CS,0x156,90,20),('lut',CS,0xfa4,30,0),('atan',0,0x175e,107,4)]
MODULES=[('th03/vector.cpp',0x110,160),('th03/hfliplut.asm',0xfa4,30)]
PROVIDERS=['th03/vector.cpp','th03/math/vector.cpp','th03/math/vector.hpp','th02/math/vector.hpp',
 'platform.h','x86real.h','libs/master.lib/master.hpp','libs/master.lib/sin8[data].asm',
 'libs/master.lib/atan8[data].asm','libs/master.lib/iatan2.asm','libs/master.lib/func.hpp',
 'th03/hfliplut.asm','th03/formats/hfliplut.asm','th03/formats/hfliplut.h',
 'th03/formats/hfliplut[bss].asm','libs/master.lib/master.inc','libs/master.lib/macros.inc']
LOCAL=['src/main/formats/hfliplut.asm','src/main/formats/hfliplut.hpp']
LUT=0x20d6
OUT_START,OUT_SIZE=0x50000,0x20000
INITIAL=bytes((i*13+41)&255 for i in range(OUT_SIZE))


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[]
    for name,segment,start,size,cleanup in RANGES:
        body=image[segment*16+start:segment*16+start+size]
        if len(body)!=size:raise ValueError('math complete body/far cleanup differs')
        ins=list(decoder.disasm(body,start));bounds={i.address for i in ins};wanted=('retf',hex(cleanup) if cleanup>=10 else str(cleanup) if cleanup else '')
        if not ins or sum(i.size for i in ins)!=size or (ins[-1].mnemonic,ins[-1].op_str)!=wanted:raise ValueError('math complete body/far cleanup differs')
        edges=[]
        for i in ins:
            if i.mnemonic in ('ret','retf') and (i.mnemonic,i.op_str)!=wanted:raise ValueError('math interior return differs')
            if i.mnemonic in ('in','out','int'):raise ValueError('math unexpected port/interrupt opcode')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('math indirect edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (segment,i.operands[0].imm)
            if i.mnemonic in ('call','lcall'):
                if name!='between' or i.mnemonic!='lcall' or dest!=(0,0x175e):raise ValueError('math unknown call/interface')
            elif dest[1] not in bounds:raise ValueError('math branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,segment=segment,offset=start,size=size,cleanup=cleanup,instructions=len(ins),sha256=sha(body),edges=edges))
    if image[CS*16+0x155:CS*16+0x156]!=b'\x90':raise ValueError('math vector producer byte differs')
    return dict(bodies=rows[:3],atan_helper=rows[3],body_bytes=189,producer_offset=0x155,producer_bytes=1,contribution_bytes=190)


def atan_table():return bytes(int(math.floor(math.atan(i/256)*128/math.pi+0.5)) for i in range(256))
def reverse(byte):return int(f'{byte:08b}'[::-1],2)


def atan_scalar(y,x):
    """Word absolute values and signed branch, then unsigned division/low-byte XLAT."""
    y,x=signed(u16(y)),signed(u16(x));ay,ax=u16(abs(y)),u16(abs(x))
    if not (x or y):return 0
    if ax==ay:angle=32
    else:
        swap=signed(ax)<signed(ay);numerator=(ax if swap else ay)*256;denominator=ay if swap else ax
        if not denominator or numerator//denominator>65535:raise ArithmeticError('native unsigned DIV quotient fault')
        angle=atan_table()[(numerator//denominator)&255]
        if swap:angle=(64-angle)&255
    if x<0:angle=128-angle
    if y<0:angle=-angle
    return angle&255


def vector_scalar(angle,length):
    s=sine_words();length=signed(u16(length));angle&=255
    return [u16(length*s[angle+64]//256),u16(length*s[angle]//256)]


class MathProbe(Probe):
    """All reviewed arithmetic instructions execute; no substituted functions."""
    def __init__(self,mz):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x2c7e0,0x2e3f0,0x40000
        self.initial_data=bytes(self.uc.mem_read(self.data,65536));self.allowed=[]
        self.errors=[];self.writes=[];self.atan_frames=[];self.stop=False;self.fault=None
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2c7e:raise ValueError('math terminal segment alias')
                self.stop=True;uc.emu_stop();return
            if not any(self.get('CS')==seg+0x2000 and (seg+0x2000)*16+at<=address<(seg+0x2000)*16+at+n for _,seg,at,n,_ in RANGES):raise ValueError('CPU escaped math bodies')
            if address==0x2175e:
                sp=self.get('SP');ip,cs,x,y=struct.unpack('<4H',uc.mem_read(self.stack+sp,8))
                if cs!=0x2c7e or ip not in (0x170,0xff00):raise ValueError('math atan native far frame differs')
                self.atan_frames.append([x,y])
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            if not any(a<=address and address+size<=b for a,b in self.allowed):raise ValueError('math write outside owned output')
            self.writes.append([address,size,value])
        def intr(uc,number,user):
            if number!=0 or self.get('CS')!=0x2000 or self.get('IP') not in (0x1791,0x17a8) or bytes(uc.mem_read(0x20000+self.get('IP'),2))!=b'\xf7\xf3':raise ValueError('math unexpected interrupt/fault: '+str((number,self.get('CS'),self.get('IP'))))
            self.fault=dict(vector=number,cs=self.get('CS'),ip=self.get('IP'));uc.emu_stop()
        def output(uc,port,width,value,user):raise ValueError('math unexpected output port')
        def inp(uc,port,width,user):raise ValueError('math unexpected input port')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)

    def reset(self,df=False):
        self.uc.mem_write(self.data,self.initial_data);self.uc.mem_write(OUT_START,INITIAL)
        for name,value in [('CS',0x2c7e),('DS',0x2e3f),('SS',0x4000),('ES',0x3333),('BP',0x7777),('SI',0x1357),('DI',0x2468),('EFLAGS',0x202|(0x400 if df else 0))]:self.set(name,value)
        self.stop=False;self.fault=None;self.errors.clear();self.writes.clear();self.atan_frames.clear()

    def run(self,name,args=(),*,fault=False,df=False):
        self.stop=False;self.fault=None;self.errors.clear();self.atan_frames.clear();self.writes.clear()
        self.set('SP',0xffc0);self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,0x2c7e,*map(u16,args)))
        _,segment,at,_,cleanup=next(r for r in RANGES if r[0]==name);self.set('CS',segment+0x2000)
        self.uc.emu_start((segment+0x2000)*16+at,0x100000,count=20000)
        if self.errors:raise ValueError(self.errors[0])
        if bool(self.fault)!=fault or self.stop==fault:raise ValueError('math terminal/divide fault differs')
        if not fault and (self.get('SP')!=0xffc4+cleanup or self.get('DS')!=0x2e3f or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]):raise ValueError('math far cleanup/callee-saved differs')
        if bool(self.get('EFLAGS')&0x400)!=df:raise ValueError('math inherited DF differs')


def matrix(mz):
    rows=[];p=MathProbe(mz)
    def observe(name,s):
        nonlocal p
        # Unicorn retains pending exception state after a stopped DIV trap.
        if p.fault:p=MathProbe(mz)
        p.reset(s.get('df',False));args=[];fault=False;angle=s.get('angle',0)&255;expected_frames=[];expected_data=bytearray(p.initial_data);expected_output=bytearray(INITIAL);wanted=[]
        if name=='lut':
            p.uc.mem_write(p.data+LUT,b'\xa5'*256);expected_data[LUT:LUT+256]=bytes(reverse(i) for i in range(256));p.allowed=[(p.data+LUT,p.data+LUT+256)]
            wanted=[[p.data+LUT+i,1,reverse(i)] for i in range(256)]
        elif name=='atan':
            x,y=s['x'],s['y'];args=[x,y];p.allowed=[];expected_frames=[[u16(x),u16(y)]]
            try:angle=atan_scalar(y,x)
            except ArithmeticError:fault=True
        else:
            xp,yp=s.get('xp',[0x5000,0x1000]),s.get('yp',[0x5000,0x1010]);xa,ya=xp[0]*16+xp[1],yp[0]*16+yp[1]
            p.allowed=[(xa,xa+2),(ya,ya+2)]
            if name=='vector':args=[s['length'],0x7700|angle,yp[1],yp[0],xp[1],xp[0]]
            else:
                x1,y1,x2,y2=s['points'];dx,dy=u16(x2-x1),u16(y2-y1);expected_frames=[[dx,dy]]
                args=[s['length'],yp[1],yp[0],xp[1],xp[0],0xa500|(s.get('plus',0)&255),y2,x2,y1,x1]
                try:angle=(atan_scalar(dy,dx)+s.get('plus',0))&255
                except ArithmeticError:fault=True
            if not fault:
                values=vector_scalar(angle,s['length']);wanted=[[xa,2,values[0]],[ya,2,values[1]]]
                for at,_,value in wanted:
                    target=expected_data if p.data<=at and at+2<=p.data+65536 else expected_output
                    off=at-p.data if target is expected_data else at-OUT_START
                    struct.pack_into('<H',target,off,value)
        before=bytes(p.uc.mem_read(p.data,65536));p.run(name,args,fault=fault,df=s.get('df',False));after=bytes(p.uc.mem_read(p.data,65536));output=bytes(p.uc.mem_read(OUT_START,OUT_SIZE))
        if after!=bytes(expected_data) or output!=bytes(expected_output) or p.writes!=wanted or p.atan_frames!=expected_frames:raise ValueError('math full memory/stores/native frames differ: '+str((name,s)))
        if name=='atan' and not fault and p.get('AX')!=angle:raise ValueError('math atan scalar angle differs')
        rows.append(dict(name=name,scenario=s,terminal=not fault,fault=p.fault,angle=None if fault else angle,stores=p.writes.copy(),atan_frames=p.atan_frames.copy(),
                         data_before_sha256=sha(before),data_after_sha256=sha(after),output_sha256=sha(output)))
    for df in (False,True):observe('lut',dict(df=df))
    lengths=(-32768,-32767,-257,-256,-255,-1,0,1,255,256,257,32767)
    for angle in range(256):
        for length in lengths:observe('vector',dict(angle=angle,length=length,df=bool(angle&1)))
    for ratio in range(256):
        for swap in (False,True):
            for sx,sy in ((1,1),(-1,1),(-1,-1),(1,-1)):
                x,y=(ratio,256) if swap else (256,ratio);x*=sx;y*=sy
                observe('atan',dict(x=x,y=y,df=bool(ratio&1)))
                observe('between',dict(points=[0,0,x,y],length=-257,plus=193,df=bool(ratio&1)))
    for x in (0,1,-1,127,128,129,256,32767,-32768):
        for y in (0,1,-1,127,128,129,256,32767,-32768):
            observe('atan',dict(x=x,y=y));observe('between',dict(points=[0,0,x,y],length=32767,plus=255))
    for points in ([32767,32767,-32768,-32768],[-32768,-32768,32767,32767],[-32768,0,0,0],[0,32767,0,-1],[10,20,10,20]):
        for plus in (0,1,127,128,255):observe('between',dict(points=points,length=-32768,plus=plus,df=True))
    pointers=[([0x5000,0x1000],[0x5000,0x1000]),([0x5000,0x1000],[0x5001,0xff0]),
              ([0x5000,0x1000],[0x5000,0x1001]),([0x5000,0xffff],[0x6000,1]),
              ([0x2e3f,0x5ba],[0x2e3f,0x5bb])]
    for xp,yp in pointers:
        for angle in (1,32,127,192,255):
            observe('vector',dict(xp=xp,yp=yp,angle=angle,length=-32768))
            observe('between',dict(xp=xp,yp=yp,points=[0,0,3,-4],plus=angle,length=-32768,df=True))
    return rows


def numeric_literals(data,directive):
    values=[]
    for line in data.decode('ascii').splitlines():
        match=re.search(r'\b'+directive+r'\s+([^;]+)',line)
        if match:values.extend(int(n.strip()) for n in match.group(1).split(','))
    return values


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('math prior text proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_math.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS};local={p:(ROOT/p).read_bytes() for p in LOCAL};inputs.update({p:sha(d) for p,d in local.items()})
    sine=struct.pack('<320h',*sine_words());atan=atan_table()
    if numeric_literals(providers['libs/master.lib/sin8[data].asm'],'dw')!=sine_words() or bytes(numeric_literals(providers['libs/master.lib/atan8[data].asm'],'db'))!=atan:raise ValueError('math frozen mathematical tables differ')
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('math input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];object_rounds=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('math invalid image')
        if mz.program_image[DS*16+0x5ba:DS*16+0x83a]!=sine or mz.program_image[DS*16+0x41c:DS*16+0x51c]!=atan:raise ValueError('math complete target tables differ')
        observed=dict(path=path,analysis=analyze(mz.program_image),tables=dict(sine_cosine_sha256=sha(sine),atan_sha256=sha(atan)),cpu=matrix(mz))
        if observations:
            if observed['analysis']!=observations[0]['analysis']:raise ValueError('math complete body/helper/CFG differ')
            tree=Path(path).parents[2];objects={}
            for obj_name,module,translator in [('vector','th03/vector.cpp','TC86 Borland C++ 4.02'),('hfliplut','th03\\hfliplut.asm','Turbo Assembler  Version 5.0')]:
                op=str(tree/'obj/th03'/f'{obj_name}.obj');obj_data=(ROOT/op).read_bytes();inputs[op]=sha(obj_data);obj=describe_omf(obj_data)
                if not obj['valid'] or obj['module_name']!=module or obj['translator_comments']!=[translator]:raise ValueError('math cached OMF producer association differs')
                objects[obj_name]={k:obj[k] for k in ('valid','sha256','dependency_timestamp_normalized_sha256','module_name','translator_comments','record_count','record_counts')}
            if object_rounds and any(objects[n]['dependency_timestamp_normalized_sha256']!=object_rounds[0][n]['dependency_timestamp_normalized_sha256'] for n in objects):raise ValueError('math cached OMF differs beyond dependency timestamps')
            object_rounds.append(objects);observed['objects']=objects
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                wanted=local['src/main/formats/hfliplut.asm'] if p=='th03/hfliplut.asm' else d
                if p.endswith(('.asm','.inc')):wanted=wanted.replace(b'\r\n',b'\n');cached=cached.replace(b'\r\n',b'\n')
                if cached!=wanted:raise ValueError('math cached frozen/overlaid provider differs: '+p)
            for p,d in local.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                if cached!=d:raise ValueError('math maintained MAIN cached source differs')
            rows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));target=parse_mz((ROOT/observations[0]['path']).read_bytes());observed['comparisons']={}
            for module,at,size in MODULES:
                row=next(r for r in rows if r['module']==module and r['size'])
                if (row['segment'],row['offset'],row['size'])!=(CS,at,size):raise ValueError('math complete MAP contribution differs')
                compared=extent_observation(target,mz,row);observed['comparisons'][module]=compared
                if not compared['raw_slice_equal'] or not compared['ordered_relocations_equal']:raise ValueError('math raw bytes/ordered relocations differ')
            def normalized(cpu):return [{k:v for k,v in r.items() if k not in ('data_before_sha256','data_after_sha256')} for r in cpu]
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']):raise ValueError('math target/cached CPU differs')
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('math canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('math frozen provider changed')
    result=dict(kind='th03-mainl-complete-vector-and-hflip-lut-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},producer_overlay={'th03/hfliplut.asm':'src/main/formats/hfliplut.asm'},
        observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS complete MAINL math190/native atan107 and mathematical table/scalar contracts:',args.output)


if __name__=='__main__':main()
