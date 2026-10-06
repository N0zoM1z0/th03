#!/usr/bin/env python3
"""Complete MAINL graph_putsa_fx candidate: native CG/GRCG ports and flat stores."""
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
from review_th03_mainl_snow import u16,signed

ROOT=Path(__file__).resolve().parents[1];CS=0xc7e
PROOF='.analysis/sol-mainl-sound-review-20261006.json'
PROOF_SHA256='bb1ed881f4eaeb90a9c82b73b07c843159e6b6539bd133a939c5416dee2cd293'
RANGES=[('text',CS,0x9b7,613,10),('setcolor',0,0xc36,41,4),('off',0,0xc60,5,0)]
FOREIGN={(0,0xc36),(0,0xc60),(0,0x924c)}
PROVIDERS=['th03/grppsafx.cpp','th02/hardware/grppsafx.cpp','th01/hardware/grppsafx.cpp',
 'th01/hardware/grppsafx.h','planar.h','pc98.h','shiftjis.hpp','defconv.h','decomp.hpp',
 'x86real.h','platform.h','libs/master.lib/pc98_gfx.hpp','libs/master.lib/func.hpp',
 'libs/master.lib/grcg_setcolor.asm','libs/master.lib/master.inc','libs/master.lib/macros.inc']
HEADERS=['.analysis/toolchain/wineprefix/drive_c/TC4/INCLUDE/'+p for p in ('MBCTYPE.H','MBSTRING.H','CTYPE.H')]
INITIAL=bytes((i*29+83)&255 for i in range(65536))


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[]
    for name,segment,start,size,cleanup in RANGES:
        body=image[segment*16+start:segment*16+start+size]
        if len(body)!=size:raise ValueError('text complete body/far cleanup differs')
        ins=list(decoder.disasm(body,start));bounds={i.address for i in ins};wanted=('retf',hex(cleanup) if cleanup>=10 else str(cleanup) if cleanup else '')
        if not ins or sum(i.size for i in ins)!=size or (ins[-1].mnemonic,ins[-1].op_str)!=wanted:raise ValueError('text complete body/far cleanup differs')
        edges=[]
        for i in ins:
            if i.mnemonic in ('ret','retf') and (i.mnemonic,i.op_str)!=wanted:raise ValueError('text interior return differs')
            if i.mnemonic=='int':raise ValueError('text unknown interrupt')
            if i.mnemonic in ('in','out'):
                allowed=(('out','dx, al'),('in','al, dx')) if name=='text' else (('out','0x7c, al'),('out','dx, al')) if name=='setcolor' else (('out','0x7c, al'),)
                if (i.mnemonic,i.op_str) not in allowed:raise ValueError('text port encoding differs')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('text indirect edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (segment,i.operands[0].imm)
            if i.mnemonic in ('call','lcall'):
                if name!='text' or i.mnemonic!='lcall' or dest not in FOREIGN:raise ValueError('text unknown call/interface')
            elif dest[1] not in bounds:raise ValueError('text branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,segment=segment,offset=start,size=size,cleanup=cleanup,instructions=len(ins),sha256=sha(body),edges=edges))
    return dict(body=rows[0],native_helpers=rows[1:],body_bytes=613,helper_bytes=46)


def font_byte(codepoint,selector):
    """Synthetic ROM bytes; no NEC font or assets are read."""
    return ((codepoint*13)^((selector&15)*29)^(0xa5 if selector&32 else 0x3c))&255


def weight_row(row,weight):
    if weight==0:return row
    if weight==1:return u16(row|(row<<1))
    if weight==3:row=u16(row|(row<<1))
    doubled=u16(row|(row<<1));new=row^doubled
    return doubled & u16(~(new<<1))


def scalar(data,string,s):
    """Source-level signed arithmetic and bit rows; ports and flat bytes only."""
    left=signed(u16(s.get('left',0)));top=signed(u16(s.get('top',0)));fx=u16(s.get('fx',0));position=u16(s.get('offset',0xfff8))
    out=bytearray(INITIAL);writes=[];ports=[['out',0x7c,1,0xc0]]+[['out',0x7e,1,255 if fx&(1<<p) else 0] for p in range(4)]+[['out',0x68,1,0xb]]
    converted=[];glyphs=[]
    for _ in range(65536):
        byte=string[position]
        if not byte:break
        division=(abs(left)//8)*(-1 if left<0 else 1);remainder=left-division*8;vram=u16(top*80+division)
        if data[0x11ef+byte]&4:
            argument=u16(((byte if byte<128 else byte-256)<<8)+string[u16(position+1)])
            codepoint=u16(s.get('jis',0x2121));converted.append([argument,codepoint]);position=u16(position+2)
        elif data[0x11ef+byte]&3:codepoint=byte+0x2980;position=u16(position+1)
        elif data[u16(0xf05+(byte if byte<128 else byte-256))]&0x5e:codepoint=byte+0x2900;position=u16(position+1)
        else:codepoint=0x2b21;position=u16(position+1)
        ports.extend([['out',0xa1,1,codepoint&255],['out',0xa3,1,((codepoint>>8)-32)&255]])
        half=0x2921<=codepoint<=0x2b7e
        glyphs.append(dict(codepoint=codepoint,left=left,half=half,clipped=left>(632 if half else 624)))
        if glyphs[-1]['clipped']:break
        for line in range(16):
            ports.append(['out',0xa5,1,line|32]);high=font_byte(codepoint,line|32);ports.append(['in',0xa9,1,high]);row=high<<8
            if not half:
                ports.append(['out',0xa5,1,line]);low=font_byte(codepoint,line);ports.append(['in',0xa9,1,low]);row+=low
            row=weight_row(row,(fx>>4)&3)
            if remainder:
                shift1=(remainder+8)&31;shift2=remainder&31;shift3=(8-remainder)&31
                values=[(row>>shift1)&255,(row>>shift2)&255,((row&255)<<shift3)&255]
            else:values=[row>>8,row&255]
            for j,value in enumerate(values):
                at=u16(vram+j);writes.append([at,1,value]);out[at]=value
            vram=u16(vram+80)
        left=signed(u16(left+((fx>>6)&7)+(8 if half else 16)))
    else:raise ValueError('text scalar exceeded logical right-edge bound')
    ports.extend([['out',0x68,1,0xa],['out',0x7c,1,0]])
    return dict(flat_sha256=sha(out),writes=writes,ports=ports,converted=converted,glyphs=glyphs,string_offset=position)


class TextProbe(Probe):
    """Native font body/GRCG helpers; one cdecl converter and synthetic ROM reads."""
    def __init__(self,mz,s):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.uc.mem_write(0xa8000,INITIAL)
        self.code,self.data,self.stack=0x2c7e0,0x2e3f0,0x40000
        for name,value in [('CS',0x2c7e),('DS',0x2e3f),('SS',0x4000),('ES',0x3333),('BP',0x7777),('SI',0x1357),('DI',0x2468),('EFLAGS',0x202|(0x400 if s.get('df') else 0))]:self.set(name,value)
        self.s=s;self.errors=[];self.writes=[];self.ports=[];self.converted=[];self.stop=False
        self.low=self.high=self.selector=None
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2c7e:raise ValueError('text terminal segment alias')
                self.stop=True;uc.emu_stop();return
            if address==0x2924c:
                if self.get('CS')!=0x2000:raise ValueError('text converter segment alias')
                sp=self.get('SP');ip,cs,arg=struct.unpack('<3H',uc.mem_read(self.stack+sp,6))
                if (cs,ip)!=(0x2c7e,0xa3b):raise ValueError('text converter return frame differs')
                value=u16(s.get('jis',0x2121));self.converted.append([arg,value]);self.set('AX',value)
                self.set('SP',sp+4);self.set('CS',cs);self.set('IP',ip);return
            if not any(self.get('CS')==seg+0x2000 and (seg+0x2000)*16+at<=address<(seg+0x2000)*16+at+n for _,seg,at,n,_ in RANGES):raise ValueError('CPU escaped text bodies')
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            if 0xa8000<=address and address+size<=0xb8000:
                if size!=1:raise ValueError('text flat store width differs')
                self.writes.append([address-0xa8000,size,value]);return
            raise ValueError('text unexpected memory write')
        def output(uc,port,width,value,user):
            if width!=1 or port not in (0x7c,0x7e,0x68,0xa1,0xa3,0xa5):raise ValueError('text unknown output port/width')
            if port==0xa1:self.low=value
            elif port==0xa3:self.high=(value+32)&255
            elif port==0xa5:
                if value not in (*range(16),*range(32,48)):raise ValueError('text unknown ROM row')
                self.selector=value
            self.ports.append(['out',port,width,value])
        def inp(uc,port,width,user):
            if (port,width)!=(0xa9,1) or self.low is None or self.high is None or self.selector is None:raise ValueError('text unknown input port/ROM selection')
            value=font_byte((self.high<<8)|self.low,self.selector);self.ports.append(['in',port,width,value]);return value
        def intr(uc,number,user):raise ValueError('text unexpected interrupt')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT)
        self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)

    def run(self,*,terminal=True,budget=50000):
        self.stop=False;self.errors.clear();self.set('CS',0x2c7e);self.set('SP',0xffc0)
        args=[0xff00,0x2c7e,u16(self.s.get('offset',0xfff8)),0x5000,u16(self.s.get('fx',0)),u16(self.s.get('top',0)),u16(self.s.get('left',0))]
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<7H',*args));self.uc.emu_start(self.code+0x9b7,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if self.stop!=terminal:raise ValueError('text terminal/budget differs')
        if terminal and (self.get('SP')!=0xffce or self.get('DS')!=0x2e3f or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]):raise ValueError('text far cleanup/callee-saved differs')
        if bool(self.get('EFLAGS')&0x400)!=bool(self.s.get('df')):raise ValueError('text inherited DF differs')


def matrix(mz):
    rows=[]
    def observe(s,terminal=True):
        s=dict(s);p=TextProbe(mz,s);string=bytearray(b'A'*65536 if s.get('unterminated') else b'\0'*65536);offset=u16(s.get('offset',0xfff8))
        for i,b in enumerate(s.get('string',[] if s.get('unterminated') else list(b'A\0'))):string[u16(offset+i)]=b
        p.uc.mem_write(0x50000,bytes(string));before=bytes(p.uc.mem_read(p.data,65536))
        wanted=scalar(before,string,s) if terminal else None
        p.run(terminal=terminal,budget=50000 if terminal else 10000)
        after=bytes(p.uc.mem_read(p.data,65536));flat=bytes(p.uc.mem_read(0xa8000,65536));endoffset=struct.unpack('<H',p.uc.mem_read(p.stack+0xffc4,2))[0]
        actual=dict(flat_sha256=sha(flat),writes=p.writes,ports=p.ports,converted=p.converted,string_offset=endoffset)
        if after!=before:raise ValueError('text changed DGROUP')
        if terminal and any(actual[k]!=wanted[k] for k in actual):raise ValueError('text full scalar/port/store result differs: '+str(s))
        if not terminal:
            expected=bytearray(INITIAL)
            for at,_,value in p.writes:expected[at]=value
            if flat!=bytes(expected):raise ValueError('text budget flat writes differ')
        rows.append(dict(scenario=s,terminal=terminal,**actual,glyphs=wanted['glyphs'] if terminal else None,before_sha256=sha(before),after_sha256=sha(after)))
    observe(dict(string=[0]))
    for byte in range(1,256):observe(dict(string=[byte,0x40,0] if mz.program_image[DS*16+0x11ef+byte]&4 else [byte,0],jis=0x2121))
    for df in (0,1):
        for weight in range(4):
            for left in range(8):
                for string,jis in (([65,0],0x2121),([0x81,0x40,0],0x2121)):observe(dict(df=df,fx=0x10*weight|15,left=left,string=string,jis=jis))
        for jis in (0,0x2920,0x2921,0x2b7e,0x2b7f,0x7fff,0xffff):observe(dict(df=df,jis=jis,string=[0x81,0,90,0],offset=0xffff,left=1))
        for spacing in range(8):
            for left in (1,623):observe(dict(df=df,fx=(spacing<<6)|0x30|5,string=[65,0x81,0x40,0xa1,9,90,0],left=left))
        for color in range(16):observe(dict(df=df,fx=0xfff0|color,string=[65,0]))
        observe(dict(df=df,left=-32768,unterminated=True),False)
    for left in (623,624,625,631,632,633,639,640,32767,-32768,-1,-7,-8,-9):
        for top in (-1,0,399,400,819,820,32767):
            for string in ([65,0],[0x81,0x40,0]):observe(dict(left=left,top=top,string=string,fx=0x3f))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('text prior sound proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_text.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    for p in HEADERS:inputs[p]=sha((ROOT/p).read_bytes())
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('text input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact)
    observations=[];maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('text invalid image')
        tables={'mbctype':sha(mz.program_image[DS*16+0x11ef:DS*16+0x12ef]),'signed_graph':sha(mz.program_image[DS*16+0xe85:DS*16+0xf85])}
        observed=dict(path=path,analysis=analyze(mz.program_image),classification_tables=tables,cpu=matrix(mz))
        if observations:
            if (observed['analysis'],tables)!=(observations[0]['analysis'],observations[0]['classification_tables']):raise ValueError('text complete bodies/CFG/classifier tables differ')
            tree=Path(path).parents[2]
            for p,d in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                if p.endswith(('.asm','.inc')):d=d.replace(b'\r\n',b'\n');cached=cached.replace(b'\r\n',b'\n')
                if cached!=d:raise ValueError('text cached frozen provider differs: '+p)
            maprows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));row=next(r for r in maprows if r['module']=='th03/grppsafx.cpp' and r['size'])
            if (row['segment'],row['offset'],row['size'])!=(CS,0x9b7,613):raise ValueError('text complete MAP contribution differs')
            target=parse_mz((ROOT/observations[0]['path']).read_bytes());observed['comparison']=extent_observation(target,mz,row)
            if not observed['comparison']['raw_slice_equal'] or not observed['comparison']['ordered_relocations_equal']:raise ValueError('text raw bytes/ordered relocations differ')
            def normalized(cpu):return [{k:v for k,v in r.items() if k not in ('before_sha256','after_sha256')} for r in cpu]
            if normalized(observed['cpu'])!=normalized(observations[0]['cpu']):raise ValueError('text target/cached CPU differs')
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('text canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('text frozen provider changed')
    result=dict(kind='th03-mainl-complete-graph-putsa-fx-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},
        observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS complete MAINL text613/native GRCG46 and explicit ROM/converter:',args.output)


if __name__=='__main__':main()
