#!/usr/bin/env python3
"""Complete MAINL CDG blitters: self-modifying CODE over explicit flat memory."""
import argparse
from datetime import datetime,timezone
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

ROOT=Path(__file__).resolve().parents[1]
CS=0xc7e
PROOF='.analysis/sol-mainl-lifecycle-review-20261006.json'
PROOF_SHA256='c47ee7ddd9ba4d10ad43914143766ca46be3be13f7101413b119eefaf8c49eab'
RANGES=[('alpha',0x1f4,179),('hflip',0x2a8,201),('noalpha',0xf32,113)]
ALIGNMENTS=[0x2a7,0x371,0xfa3]
PATCHES={'alpha':[0x26c,0x265,0x257,0x271,0x253],
         'hflip':[0x329,0x351,0x313,0x33f,0x30f,0x33b],
         'noalpha':[0xf79]}
PROVIDERS=['th03/cdg_put.asm','th03/formats/cdg_put.asm','th03/cdg_p_na.asm',
           'th03/formats/cdg.h','th03/formats/cdg.inc','th03/formats/cdg[bss].asm',
           'th03/formats/hfliplut.h','th03/formats/hfliplut[bss].asm',
           'pc98.inc','libs/master.lib/master.inc','libs/master.lib/macros.inc']


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[]
    for name,start,size in RANGES:
        body=image[CS*16+start:CS*16+start+size]
        if len(body)!=size:raise ValueError('CDG complete body/cleanup differs')
        ins=list(decoder.disasm(body,start));bounds={i.address for i in ins}
        if sum(i.size for i in ins)!=size or not ins or (ins[-1].mnemonic,ins[-1].op_str)!=('retf','6'):raise ValueError('CDG complete body/cleanup differs')
        edges=[]
        for i in ins:
            if i.mnemonic in ('ret','retf') and (i.mnemonic,i.op_str)!=('retf','6'):raise ValueError('CDG interior return differs')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('unexpected CDG indirect edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (CS,i.operands[0].imm)
            if i.mnemonic in ('call','lcall'):
                if i.mnemonic!='lcall' or dest!=(0,0xc36):raise ValueError('CDG unknown call/interface')
            elif dest[1] not in bounds:raise ValueError('CDG branch enters operand/neighbor')
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        for patch in PATCHES[name]:
            owners=[i for i in ins if i.address<patch and patch+2<=i.address+i.size]
            if len(owners)!=1 or owners[0].address+1!=patch or owners[0].mnemonic!='mov':raise ValueError('CDG patch not complete MOV immediate word')
        rows.append(dict(name=name,offset=start,size=size,sha256=sha(body),instructions=len(ins),edges=edges,patches=PATCHES[name]))
    if any(image[CS*16+a]!=0x90 for a in ALIGNMENTS):raise ValueError('CDG observed EVEN byte differs')
    return dict(bodies=rows,body_bytes=493,observed_even_bytes=ALIGNMENTS,contribution_bytes=496)


def reverse_bits(byte):return sum(((byte>>i)&1)<<(7-i) for i in range(8))
ALPHA=bytes((i*13+23)&255 for i in range(65536))
COLORS=bytes((i*29+71)&255 for i in range(65536))
INITIAL=bytes((i*7+0x55)&255 for i in range(0x60000))


def scalar(name,width,bottom,left,top):
    """Word arithmetic and scalar bytes; no GRCG broadcast or pixel model."""
    out=bytearray(INITIAL);writes=[];width_bytes=u16(width*4)
    origin=u16(signed(u16(left))//8+bottom)
    segment=u16(0xa800+u16(top)*5);si=0
    def row_pass(segment,source,di,flip,combine):
        nonlocal si
        while True:
            for x in range(width_bytes) if flip else range(0,width_bytes,4):
                off=u16(di-x) if flip else u16(di+x)
                at=segment*16+off-0xa0000
                amount=1 if flip else 4
                if not 0<=at<=len(out)-amount:raise ValueError('scalar CDG address outside flat window')
                values=source[u16(si+x):u16(si+x)+amount]
                for j,value in enumerate(values):
                    if flip:value=reverse_bits(value)
                    if combine:value|=out[at+j]
                    out[at+j]=value
                writes.append([segment*16+off,amount,int.from_bytes(out[at:at+amount],'little')])
            si=u16(si+width_bytes);di=u16(di-80)
            if signed(di)<0:break
    if name!='noalpha':
        last=u16(origin+width_bytes-1) if name=='hflip' else origin
        row_pass(segment,ALPHA,last,name=='hflip',False);si=0
    segments=[]
    while True:
        segments.append(segment)
        last=u16(origin+width_bytes-1) if name=='hflip' else origin
        row_pass(segment,COLORS,last,name=='hflip',name!='noalpha')
        segment=u16(segment+0x800)
        if segment<0xc000:continue
        if segment>=0xc800:break
        segment=u16(segment+0x2000)
    return bytes(out),writes,segments


class CdgProbe(Probe):
    """Actual blitters/SMC; color setup is a far interface, memory is flat."""
    def __init__(self,mz,*,df=False):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code,self.data,self.stack=0x2c7e0,0x2e3f0,0x40000
        for name,value in [('CS',0x2c7e),('DS',0x2e3f),('SS',0x4000),('ES',0x3333),('FS',0x4444),('BP',0x7777),('SI',0x1357),('DI',0x2468),('EFLAGS',0x202|(0x400 if df else 0))]:self.set(name,value)
        self.uc.mem_write(0x50000,ALPHA);self.uc.mem_write(0x70000,COLORS);self.uc.mem_write(0xa0000,INITIAL)
        self.uc.mem_write(self.data+0x20d6,bytes(reverse_bits(i) for i in range(256)))
        self.errors,self.ports,self.events,self.writes,self.patches=[],[],[],[],[];self.stop=False
        def guard(callback):
            def invoke(*args):
                try:return callback(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop()
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=0x2c7e:raise ValueError('CDG terminal segment alias')
                self.stop=True;uc.emu_stop();return
            if address==0x20000+0xc36:
                if self.get('CS')!=0x2000:raise ValueError('CDG color interface segment alias')
                sp=self.get('SP');words=list(struct.unpack('<4H',uc.mem_read(self.stack+sp,8)));self.events.append(dict(name='grcg_color',args=words[2:]))
                self.set('SP',sp+8);self.set('CS',words[1]);self.set('IP',words[0]);return
            off=address-self.code
            if self.get('CS')!=0x2c7e or not any(a<=off<a+n for _,a,n in RANGES):raise ValueError('CPU escaped reviewed CDG bodies')
        def write(uc,access,address,size,value,user):
            if 0xa0000<=address<0x100000:self.writes.append([address,size,value])
            elif self.code<=address<self.code+0x1000:self.patches.append([address-self.code,size,value])
            elif self.stack<=address<self.stack+65536:return
            else:raise ValueError('unexpected CDG data write')
        def output(uc,port,width,value,user):
            if (port,width,value)!=(0x7c,1,0):raise ValueError('unexpected CDG port/width/value')
            self.ports.append([port,width,value])
        def intr(uc,number,user):raise ValueError('unexpected CDG interrupt')
        def inp(uc,port,width,user):self.errors.append('unexpected CDG input port');uc.emu_stop();return 0
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,inp,None,1,0,reg.UC_X86_INS_IN)

    def metadata(self,slot,width,bottom,pixel_w=1,pixel_h=32767):
        at=self.data+u16(0x1d0e+u16(slot*16))
        self.uc.mem_write(at,struct.pack('<5H2B2H',0,u16(pixel_w),u16(pixel_h),u16(bottom),u16(width),0,0,0x5000,0x7000))

    def run(self,name,slot,left,top,*,terminal=True,budget=100000):
        self.stop=False;self.errors.clear();self.set('CS',0x2c7e);self.set('SP',0xffd0)
        self.uc.mem_write(self.stack+0xffd0,struct.pack('<5H',0xff00,0x2c7e,u16(slot),u16(top),u16(left)))
        start=next(a for n,a,_ in RANGES if n==name);self.uc.emu_start(self.code+start,0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if self.stop!=terminal:raise ValueError('CDG terminal/budget differs')
        if terminal and (self.get('SP')!=0xffda or self.get('DS')!=0x2e3f or [self.get(r) for r in ('BP','SI','DI')]!=[0x7777,0x1357,0x2468]):raise ValueError('CDG far cleanup/callee-saved differs')


def matrix(mz):
    cases=[]
    parameters=[(1,0,0,0,0),(2,80,7,5,31),(3,160,-1,-1,32),(2,240,641,399,65535),(1,0,0,0,32),(1,80,8,0,0),(1,0,-1,0,0)]
    for name,_,_ in RANGES:
        for width,bottom,left,top,slot in parameters:
            for df in (False,True):
                p=CdgProbe(mz,df=df);p.metadata(slot,width,bottom);before=bytes(p.uc.mem_read(p.data,65536));p.run(name,slot,left,top)
                expected,writes,segments=scalar(name,width,bottom,left,top)
                if bytes(p.uc.mem_read(0xa0000,0x60000))!=expected or p.writes!=writes or bytes(p.uc.mem_read(p.data,65536))!=before:raise ValueError('CDG full flat-memory/scalar stores or unchanged DGROUP differs')
                origin=u16(signed(u16(left))//8+bottom);w=u16(width*4);last=u16(origin+w-1)
                values=[0x7000,origin,width,width,u16(w+80)] if name=='alpha' else [last,last,w,w,u16(80-w),u16(80-w)] if name=='hflip' else [width]
                if p.patches!=[[at,2,value] for at,value in zip(PATCHES[name],values)]:raise ValueError('CDG complete self-modifying operand stores differ')
                if p.events!=([] if name=='noalpha' else [dict(name='grcg_color',args=[0,0xc0])]) or p.ports!=([] if name=='noalpha' else [[0x7c,1,0]]):raise ValueError('CDG color request/off ports differ')
                if bool(p.get('EFLAGS')&0x400)!=(df if name=='hflip' else False):raise ValueError('CDG DF contract differs')
                # Re-entry uses new geometry and exercises existing translated-code state.
                p.uc.mem_write(0xa0000,INITIAL);p.metadata(slot,1,0);p.writes.clear();p.patches.clear();p.events.clear();p.ports.clear();p.run(name,slot,0,0)
                after,writes2,_=scalar(name,1,0,0,0)
                if bytes(p.uc.mem_read(0xa0000,0x60000))!=after or p.writes!=writes2:raise ValueError('CDG re-entry uses stale patched geometry')
                cases.append(dict(name=name,width=width,bottom=bottom,left=left,top=top,slot=slot,initial_df=df,flat_sha256=sha(expected),store_count=len(writes),segments=segments,patch_values=values,reentry_checked=True))
        p=CdgProbe(mz);p.metadata(0,0,0);p.run(name,0,0,0,terminal=name=='noalpha',budget=2000)
        if name=='noalpha' and p.writes:raise ValueError('zero-width noalpha unexpectedly stores pixels')
        cases.append(dict(name=name,zero_width=True,terminal=name=='noalpha',writes_before_stop=len(p.writes),patches=p.patches,ports=p.ports))
    return cases


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA256:raise ValueError('CDG prior lifecycle proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw),'scripts/review_th03_mainl_cdg_put.py':sha(Path(__file__).read_bytes())}
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('CDG input changed: '+p)
    verify();artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-mainl');stored=read_verified_artifact(ROOT,artifact);observations=[]
    maps=[p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path=entry['path'];mz=parse_mz((ROOT/path).read_bytes())
        if not mz.valid:raise ValueError('CDG invalid image')
        observed=dict(path=path,analysis=analyze(mz.program_image),cpu=matrix(mz))
        if observations:
            tree=Path(path).parents[2]
            for p,data in providers.items():
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                if cached!=(data.replace(b'\n',b'\r\n') if p.endswith('.asm') else data):raise ValueError('CDG frozen cached provider association differs')
            rows=code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(),len(mz.program_image));target=parse_mz((ROOT/observations[0]['path']).read_bytes())
            observed['comparisons']={}
            for module,at,size in [('th03/cdg_put.asm',0x1f4,382),('th03/cdg_p_na.asm',0xf32,114)]:
                row=next(r for r in rows if r['module']==module and r['size'])
                if (row['segment'],row['offset'],row['size'])!=(CS,at,size):raise ValueError('CDG complete MAP contribution differs')
                observed['comparisons'][module]=extent_observation(target,mz,row)
                observed['comparisons'][module]['raw_difference_offsets']=[a for a in range(at,at+size) if target.program_image[CS*16+a]!=mz.program_image[CS*16+a]]
            if observed['cpu']!=observations[0]['cpu']:raise ValueError('CDG target/cached CPU diagnostics differ')
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('CDG canonical target changed')
    for p,d in providers.items():
        if subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98')!=d:raise ValueError('CDG frozen provider changed')
    result=dict(kind='th03-mainl-complete-cdg-blitter-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,fresh_build=False,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS complete CDG blitters496 and explicit flat-memory CPU diagnostics:',args.output)


if __name__=='__main__':main()
