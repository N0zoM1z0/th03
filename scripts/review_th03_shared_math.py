#!/usr/bin/env python3
"""Complete TH03 vector/LUT carriers with native IATAN2 and physical-state checks."""
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
from review_th03_mainl_cutscene import Probe, REVISION, sha
from review_th03_mainl_snow import u16, signed, sine_words
from review_th03_mainl_math import PROVIDERS, atan_table, reverse, numeric_literals, INITIAL, OUT_START

ROOT=Path(__file__).resolve().parents[1]
PARENT='.analysis/th03-shared-text/sol-shared-text-source-20261006-b/receipt.json'
PARENT_SHA='384f6dbf5072c3cc61a93fa7a02ae8c9c395935c3acb98002ddd6e5d5951e870'
PROFILES={
 'op':dict(cs=0xbeb,ds=0xd7f,lut=0xcb8,table=0x1e70),
 'mainl':dict(cs=0xc7e,ds=0xe3f,lut=0xfa4,table=0x20d6,vector=0x110,between=0x156,atan=0x175e,sine=0x5ba,cosine=0x63a,atan_table=0x41c),
}


def ranges(p):
    result=[('lut',p['cs'],p['lut'],30,0)]
    if 'vector' in p: result=[('vector',p['cs'],p['vector'],69,12),('between',p['cs'],p['between'],90,20),*result,('atan',0,p['atan'],107,4)]
    return result


def analyze(image,p):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[]
    for name,seg,start,size,cleanup in ranges(p):
        body=image[seg*16+start:seg*16+start+size];ins=list(decoder.disasm(body,start));bounds={i.address for i in ins}
        wanted=('retf',hex(cleanup) if cleanup>=10 else str(cleanup) if cleanup else '')
        if len(body)!=size or not ins or sum(i.size for i in ins)!=size or (ins[-1].mnemonic,ins[-1].op_str)!=wanted:raise ValueError('math complete body/far cleanup differs')
        edges=[]
        for i in ins:
            if i.mnemonic in ('ret','retf') and (i.mnemonic,i.op_str)!=wanted:raise ValueError('math interior return differs')
            if i.mnemonic in ('in','out','int'):raise ValueError('math unexpected port/interrupt opcode')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('math indirect edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (seg,i.operands[0].imm)
            if i.mnemonic in ('call','lcall'):
                if name!='between' or i.mnemonic!='lcall' or dest!=(0,p['atan']) or i.address-start!=0x15:raise ValueError('math native atan caller binding differs')
            elif dest[1] not in bounds:raise ValueError('math branch enters operand/neighbor')
            edges.append(dict(position=i.address-start,kind=i.mnemonic,destination=dest))
        if name in ('vector','between'):
            globals=[(i.mnemonic,o.mem.disp) for i in ins for o in i.operands if o.type==X86_OP_MEM and o.mem.disp in (p['sine'],p['cosine'])]
            if globals!=[('movsx',p['cosine']),('movsx',p['sine'])]:raise ValueError('math actual sine/cosine bindings differ')
        if name=='lut' and (ins[2].mnemonic,ins[2].op_str)!=('mov','di, '+hex(p['table'])):raise ValueError('math LUT actual binding differs')
        if name=='atan' and not any(i.mnemonic=='mov' and i.op_str=='bx, '+hex(p['atan_table']) for i in ins):raise ValueError('math atan lookup binding differs')
        unreachable=[]
        if name=='atan':
            by={i.address-start:i for i in ins}
            if (by[0x3b].mnemonic,by[0x3b].size)!=('nop',1) or by[0x39].mnemonic!='jmp' or any(e['destination']==(seg,start+0x3b) for e in edges):raise ValueError('math unreachable atan alignment differs')
            unreachable=[0x3b]
        rows.append(dict(name=name,segment=seg,offset=start,size=size,instructions=len(ins),positions=[i.address-start for i in ins],unreachable_positions=unreachable,sha256=sha(body),edges=edges))
    if 'vector' in p and image[p['cs']*16+p['vector']+69:p['cs']*16+p['vector']+70]!=b'\x90':raise ValueError('math separate producer byte differs')
    return dict(bodies=rows,owned_body_bytes=189 if 'vector' in p else 30,producer_bytes=1 if 'vector' in p else 0,contextual_bytes=107 if 'vector' in p else 0)


def atan_scalar(y,x,table):
    y,x=signed(u16(y)),signed(u16(x));ay,ax=u16(abs(y)),u16(abs(x))
    if not (x or y):return 0
    if ax==ay:angle=32
    else:
        swap=signed(ax)<signed(ay);numerator=(ax if swap else ay)*256;denominator=ay if swap else ax
        if not denominator or numerator//denominator>65535:raise ArithmeticError('native unsigned DIV quotient fault')
        angle=table[(numerator//denominator)&255]
        if swap:angle=(64-angle)&255
    if x<0:angle=128-angle
    if y<0:angle=-angle
    return angle&255


class MathSpec:
    def __init__(self,before,p):self.memory=bytearray(before);self.p=p;self.stores=[];self.frames=[];self.fault=False;self.angle=None
    def store(self,at,width,value):
        self.stores.append([at,width,value]);self.memory[at:at+width]=value.to_bytes(width,'little')
    def invoke(self,name,s):
        p=self.p;ds=(p['ds']+0x2000)*16
        if name=='lut':
            for i in range(256):self.store(ds+p['table']+i,1,reverse(i))
            return
        table=self.memory[ds+p['atan_table']:ds+p['atan_table']+256]
        angle=s.get('angle',0)&255
        if name=='atan':x,y=s['x'],s['y']
        elif name=='between':
            x1,y1,x2,y2=s['points'];x,y=u16(x2-x1),u16(y2-y1)
        if name in ('atan','between'):
            self.frames.append([u16(x),u16(y)])
            try:angle=atan_scalar(y,x,table)
            except ArithmeticError:self.fault=True;return
            if name=='between':angle=(angle+s.get('plus',0))&255
        self.angle=angle
        if name=='atan':return
        length=signed(u16(s['length']));cosine=struct.unpack_from('<h',self.memory,ds+p['cosine']+angle*2)[0];sine=struct.unpack_from('<h',self.memory,ds+p['sine']+angle*2)[0]
        xp,yp=s.get('xp',[0x5000,0x1000]),s.get('yp',[0x5000,0x1010])
        self.store(xp[0]*16+xp[1],2,u16(length*cosine//256));self.store(yp[0]*16+yp[1],2,u16(length*sine//256))


class MathProbe(Probe):
    def __init__(self,mz,p):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.uc.mem_write(OUT_START,INITIAL)
        self.p=p;self.code=(p['cs']+0x2000)*16;self.data=(p['ds']+0x2000)*16;self.stack=0x40000
        self.initial=bytes(self.uc.mem_read(0,0x100000));self.allowed=[];self.errors=[];self.writes=[];self.frames=[];self.visited=set();self.stop=False;self.fault=None;self.name=None
        meta=analyze(mz.program_image,p);self.positions={(seg+0x2000,start+i):(name,i) for b,(name,seg,start,_,_) in zip(meta['bodies'],ranges(p)) for i in b['positions']}
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            cs=self.get('CS');ip=address-cs*16
            if address==self.code+0xff00:
                if (cs,ip)!=(p['cs']+0x2000,0xff00):raise ValueError('math terminal segment alias')
                self.stop=True;uc.emu_stop();return
            if (cs,ip) not in self.positions:raise ValueError('CPU escaped math instruction boundaries')
            self.visited.add(self.positions[(cs,ip)])
            if 'atan' in p and (cs,ip)==(0x2000,p['atan']):
                sp=self.get('SP');ret,seg,x,y=struct.unpack('<4H',uc.mem_read(self.stack+sp,8))
                if self.get('SS')!=0x4000 or seg!=p['cs']+0x2000 or (ret,sp,self.get('BP'))!=((0xff00,0xffc0,0x7777) if self.name=='atan' else (p['between']+0x1a,0xffb4,0xffbe)):raise ValueError('math native atan far frame differs')
                self.frames.append([x,y])
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            if not any(a<=address and address+size<=b for a,b in self.allowed):raise ValueError('math write outside declared physical output')
            self.writes.append([address,size,value])
        def intr(uc,number,user):
            ip=self.get('IP')
            if 'atan' not in p or number!=0 or self.get('CS')!=0x2000 or ip-p['atan'] not in (0x33,0x4a) or bytes(uc.mem_read(0x20000+ip,2))!=b'\xf7\xf3':raise ValueError('math unexpected interrupt/fault')
            self.fault=dict(vector=number,cs=self.get('CS'),ip=ip);uc.emu_stop()
        def port(*args):raise ValueError('math unexpected port')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(port),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(port,0),None,1,0,reg.UC_X86_INS_IN)

    def run(self,name,s,persistent=False):
        if self.fault:raise ValueError('math post-trap instance must be discarded')
        if not persistent:self.uc.mem_write(0,self.initial)
        self.name=name;self.stop=False;self.fault=None;self.errors=[];self.writes=[];self.frames=[];self.visited=set()
        for key,value in [('CS',self.p['cs']+0x2000),('DS',self.p['ds']+0x2000),('SS',0x4000),('ES',0x3333),('FS',0x3456),('SP',0xffc0),('BP',0x7777),('SI',0x1357),('DI',0x2468),('EFLAGS',2|(0x200 if s.get('if',1) else 0)|(0x400 if s.get('df') else 0))]:self.set(key,value)
        args=[]
        if name=='lut':
            self.uc.mem_write(self.data+self.p['table'],bytes([s.get('fill',0xa5)])*256);self.allowed=[(self.data+self.p['table'],self.data+self.p['table']+256)]
        elif name=='atan':args=[s['x'],s['y']];self.allowed=[]
        else:
            xp,yp=s.get('xp',[0x5000,0x1000]),s.get('yp',[0x5000,0x1010]);self.allowed=[(seg*16+off,seg*16+off+2) for seg,off in (xp,yp)]
            if any(self.stack<=a<self.stack+65536 or 0x20000<=a<self.data for a,b in self.allowed):raise ValueError('math output aliases CODE/stack fixture')
            if name=='vector':args=[s['length'],0x7700|(s.get('angle',0)&255),yp[1],yp[0],xp[1],xp[0]]
            else:
                x1,y1,x2,y2=s['points'];args=[s['length'],yp[1],yp[0],xp[1],xp[0],0xa500|(s.get('plus',0)&255),y2,x2,y1,x1]
        self.uc.mem_write(self.stack+0xffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,self.p['cs']+0x2000,*map(u16,args)))
        before=bytes(self.uc.mem_read(0,0x100000));spec=MathSpec(before,self.p);spec.invoke(name,s)
        _,seg,start,_,cleanup=next(r for r in ranges(self.p) if r[0]==name);self.set('CS',seg+0x2000)
        self.uc.emu_start((seg+0x2000)*16+start,0x100000,count=20000)
        if self.errors:raise ValueError(self.errors[0])
        if bool(self.fault)!=spec.fault or self.stop==spec.fault:raise ValueError('math terminal/divide fault differs')
        after=bytes(self.uc.mem_read(0,0x100000))
        if self.writes!=spec.stores or self.frames!=spec.frames:raise ValueError('math ordered scalar stores/native arguments differ')
        if after[:self.stack]!=spec.memory[:self.stack] or after[self.stack+65536:]!=spec.memory[self.stack+65536:]:raise ValueError('math full physical memory differs')
        if not self.fault and (self.get('SS')!=0x4000 or self.get('SP')!=0xffc4+cleanup or self.get('DS')!=self.p['ds']+0x2000 or [self.get(r) for r in ('BP','SI','DI','FS')]!=[0x7777,0x1357,0x2468,0x3456]):raise ValueError('math far cleanup/saved registers differ')
        if (self.get('EFLAGS')&0x600)!=(0x200 if s.get('if',1) else 0)|(0x400 if s.get('df') else 0):raise ValueError('math incoming IF/DF differs')
        if name=='atan' and not self.fault and self.get('AX')!=spec.angle:raise ValueError('math actual atan angle differs')
        return dict(name=name,scenario=s,terminal=not bool(self.fault),fault=self.fault,angle=spec.angle,stores=self.writes,atan_frames=self.frames,visited=sorted(self.visited),es=self.get('ES'),fs=self.get('FS'),if_df=self.get('EFLAGS')&0x600,memory_before_sha256=sha(before),memory_after_sha256=sha(after))


def cases(p,focused=False):
    rows=[('lut',dict(df=df,**{'if':flag})) for df in (0,1) for flag in (0,1)]
    if 'vector' not in p:return rows
    lengths=(-32768,-32767,-257,-256,-255,-1,0,1,255,256,257,32767)
    for angle in range(256) if not focused else (0,1,32,64,96,127,128,160,192,224,255):
        for length in lengths:rows.append(('vector',dict(angle=angle,length=length,df=bool(angle&1))))
    for ratio in range(256) if not focused else (0,1,127,128,255):
        for swap in (False,True):
            for sx,sy in ((1,1),(-1,1),(-1,-1),(1,-1)):
                x,y=(ratio,256) if swap else (256,ratio);x*=sx;y*=sy
                rows.extend([('atan',dict(x=x,y=y,df=bool(ratio&1))),('between',dict(points=[0,0,x,y],length=-257,plus=193,df=bool(ratio&1)))])
    for x in (0,1,-1,127,128,129,256,32767,-32768):
        for y in (0,1,-1,127,128,129,256,32767,-32768):rows.extend([('atan',dict(x=x,y=y)),('between',dict(points=[0,0,x,y],length=32767,plus=255))])
    for points in ([32767,32767,-32768,-32768],[-32768,-32768,32767,32767],[-32768,0,0,0],[0,32767,0,-1],[10,20,10,20]):
        for plus in (0,1,127,128,255):rows.append(('between',dict(points=points,length=-32768,plus=plus,df=1)))
    pointers=[([0x5000,0x1000],[0x5000,0x1000]),([0x5000,0x1000],[0x5001,0xff0]),([0x5000,0x1000],[0x5000,0x1001]),([0x5000,0xffff],[0x6000,1]),([p['ds']+0x2000,p['sine']],[p['ds']+0x2000,p['sine']+1]),([0,0xffff],[p['ds']+0x2000,0xffff])]
    for xp,yp in pointers:
        for angle in (1,32,127,192,255):rows.extend([('vector',dict(xp=xp,yp=yp,angle=angle,length=-32768)),('between',dict(xp=xp,yp=yp,points=[0,0,3,-4],plus=angle,length=-32768,df=1))])
    return rows


def matrix(mz,p,focused=False):
    rows=[];probe=MathProbe(mz,p)
    for name,s in cases(p,focused):
        if probe.fault:probe=MathProbe(mz,p)
        rows.append(probe.run(name,s))
    if 'vector' in p:
        probe=MathProbe(mz,p)
        sequence=[('vector',dict(angle=1,length=-32768,xp=[p['ds']+0x2000,p['sine']+2],yp=[p['ds']+0x2000,p['sine']+130])),('vector',dict(angle=1,length=257)),('between',dict(points=[0,0,256,6],plus=0,length=257)),('lut',dict(fill=0x55)),('vector',dict(angle=1,length=-1))]
        for i,(name,s) in enumerate(sequence):
            row=probe.run(name,s,True);row['persistent_sequence_index']=i;rows.append(row)
    return rows


def coverage(meta,rows):
    wanted={(b['name'],i) for b in meta['bodies'] for i in b['positions'] if i not in b['unreachable_positions']};seen={(n,i) for r in rows for n,i in r['visited']}
    if wanted!=seen:raise ValueError('math incomplete native coverage: '+str(sorted(wanted-seen)))
    return dict(positions=len(wanted),decoded_positions=sum(len(b['positions']) for b in meta['bodies']),unreachable_positions=[(b['name'],i) for b in meta['bodies'] for i in b['unreachable_positions']],complete=True,invocations=len(rows),returns=sum(r['terminal'] for r in rows),faults=sum(not r['terminal'] for r in rows),stores=sum(len(r['stores']) for r in rows))


def semantic(rows):
    return json.loads(json.dumps([{k:v for k,v in r.items() if k not in ('memory_before_sha256','memory_after_sha256')} for r in rows]))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    raw=(ROOT/PARENT).read_bytes()
    if sha(raw)!=PARENT_SHA:raise ValueError('math previous cold proof differs')
    previous=json.loads(raw);inputs={**previous['inputs'],PARENT:sha(raw)}
    for name in ['scripts/review_th03_shared_math.py','scripts/review_th03_mainl_math.py','src/main/math/vector_far.asm','.analysis/sol-shared-math-op-ghidra-check-20261006.log','.analysis/sol-shared-math-mainl-ghidra-check-20261006.log']:inputs[name]=sha((ROOT/name).read_bytes())
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in [*PROVIDERS,'Tupfile.lua']}
    sine=struct.pack('<320h',*sine_words());atan=atan_table()
    if numeric_literals(providers['libs/master.lib/sin8[data].asm'],'dw')!=sine_words() or bytes(numeric_literals(providers['libs/master.lib/atan8[data].asm'],'db'))!=atan:raise ValueError('math regenerated frozen tables differ')
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('math prerequisite changed: '+p)
    verify();prior=json.loads((ROOT/'.analysis/sol-shared-text-review-20261006.json').read_bytes());observations={}
    for art,p in PROFILES.items():
        artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-'+art);stored=read_verified_artifact(ROOT,artifact)
        paths=[prior['observations'][art][0]['path']]+[f'.analysis/th03-shared-text/sol-shared-text-source-20261006-b/round{n}/source/bin/th03/{art}.exe' for n in (1,2)]
        observations[art]=[];target=parse_mz((ROOT/paths[0]).read_bytes())
        for path in paths:
            inputs[path]=sha((ROOT/path).read_bytes());mz=parse_mz((ROOT/path).read_bytes());meta=analyze(mz.program_image,p)
            if not mz.valid:raise ValueError('math invalid MZ')
            if 'vector' in p and (mz.program_image[p['ds']*16+p['sine']:p['ds']*16+p['sine']+640]!=sine or mz.program_image[p['ds']*16+p['atan_table']:p['ds']*16+p['atan_table']+256]!=atan):raise ValueError('math complete regenerated target tables differ')
            cpu=matrix(mz,p);row=dict(path=path,analysis=meta,cpu=cpu,coverage=coverage(meta,cpu))
            if observations[art]:
                tree=Path(path).parents[2];mp=tree/f'obj/th03/{art}.map';inputs[str(mp)]=sha((ROOT/mp).read_bytes());maprows=code_rows((ROOT/mp).read_text(),len(mz.program_image));row['comparisons']={}
                modules=[('th03/hfliplut.asm',p['lut'],30)]+([('th03/vector.cpp',p['vector'],160)] if 'vector' in p else [])
                for module,start,size in modules:
                    mr=next(r for r in maprows if r['module']==module and r['size'])
                    if (mr['segment'],mr['offset'],mr['size'])!=(p['cs'],start,size):raise ValueError('math original MAP ownership differs')
                    comp=extent_observation(target,mz,mr)
                    if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('math original complete raw/ordered carrier differs')
                    row['comparisons'][module]=comp
                    obj=tree/'obj/th03'/('vector.obj' if module.endswith('.cpp') else 'hfliplut.obj');inputs[str(obj)]=sha((ROOT/obj).read_bytes())
                for name,data in providers.items():
                    cp=tree/name;cached=(ROOT/cp).read_bytes();inputs[str(cp)]=sha(cached)
                    if name.endswith(('.asm','.inc')):cached=cached.replace(b'\r\n',b'\n');data=data.replace(b'\r\n',b'\n')
                    if cached!=data:raise ValueError('math actual frozen producer differs: '+name)
                if meta!=observations[art][0]['analysis'] or semantic(cpu)!=semantic(observations[art][0]['cpu']):raise ValueError('math independent artifact observations differ')
            observations[art].append(row)
        if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('math canonical target changed')
        print('PASS shared math',art,observations[art][0]['coverage'],flush=True)
    verify()
    report=dict(kind='th03-shared-math-complete-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},tables=dict(sine_cosine_sha256=sha(sine),atan_sha256=sha(atan)),observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
