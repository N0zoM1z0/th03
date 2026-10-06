#!/usr/bin/env python3
"""Review the complete PI wrapper chain with native free/memcpy and physical effects."""
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
from review_th03_mainl_cutscene import Probe, REVISION, sha
from review_th03_mainl_snow import u16, signed
from review_th03_mainl_pi import PROVIDERS, advance, next_top

ROOT=Path(__file__).resolve().parents[1]
PARENT='.analysis/th03-shared-snd-load/sol-shared-snd-load-source-20261006-d/receipt.json'
PARENT_SHA='0f54d49eb2f0f9c6db517fe6f367bf784826544a15b26860497f13b2f0dafdf9'
PROFILES={
 'op':dict(cs=0xbeb,ds=0xd7f,palette=0x4a6,put=0x4cb,load=0xa90,headers=0x1cc0,buffers=0x1ca8,palettes=0x11b8,memcpy=0x4e5f,free=0x12dc,show=0x1aa4,packed=0x1922,load_pack=0x1334,heap=0x25ce),
 'mainl':dict(cs=0xc7e,ds=0xe3f,palette=0x52a,put=0x54f,interlace=0x5d7,quarter=0xd11,load=0xccb,headers=0x1f26,buffers=0x1f0e,palettes=0x141e,memcpy=0x4b7d,free=0xfec,show=0x17d0,packed=0x1632,load_pack=0x1044,heap=0x22b2),
}
MODULES=[('th03/pi_put.cpp','palette',173),('th03/pi_load.cpp','load',70),('th03/pi_put_i.cpp','interlace',135),('th03/pi_put_q.cpp','quarter',177)]


def ranges(p):
    result=[(n,p['cs'],p[n],size,c) for n,size,c in [('palette',37,2),('put',136,6),('load',70,6),('interlace',135,6),('quarter',177,8)] if n in p]
    return result+[('free',0,p['free'],76,8),('memcpy',0,p['memcpy'],36,0)]


def models(p):return {p['show']:('palette_show',0),p['packed']:('packed_put',10),p['load_pack']:('load_pack',12),p['heap']:('heap_free',2)}


def analyze(image,p):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[]
    for name,seg,start,size,cleanup in ranges(p):
        raw=image[seg*16+start:seg*16+start+size];ins=list(decoder.disasm(raw,start));by={i.address-start:i for i in ins};bounds={i.address for i in ins};edges=[]
        if len(raw)!=size or not ins or sum(i.size for i in ins)!=size or (ins[-1].mnemonic,ins[-1].op_str)!=('retf',str(cleanup) if cleanup else ''):raise ValueError('PI complete body/far cleanup differs')
        for j,i in enumerate(ins):
            at=i.address-start
            if i.mnemonic in ('int','in','out','ret') or i.mnemonic=='retf' and j!=len(ins)-1:raise ValueError('PI unknown native interface')
            if not i.mnemonic.startswith(('j','loop')) and i.mnemonic not in ('call','lcall'):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('PI indirect edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (seg,i.operands[0].imm)
            if i.mnemonic=='lcall':
                calls={'palette':{0x14:p['memcpy'],0x1c:p['show']},'put':{0x37:p['packed']},'interlace':{0x37:p['packed']},'quarter':{0x70:p['packed']},'load':{0x1c:p['free'],0x39:p['load_pack']}}
                if dest!=(0,calls.get(name,{}).get(at)):raise ValueError('PI complete far-call binding differs')
            elif i.mnemonic=='call':
                if name!='free' or dest!=(0,p['heap']) or not j or bytes(ins[j-1].bytes)!=b'\x0e':raise ValueError('PI native heap frame binding differs')
            elif dest[1] not in bounds:raise ValueError('PI branch enters operand/neighbor')
            edges.append([at,i.mnemonic,list(dest)])
        bindings={}
        if name=='palette':bindings={0xc:b'\x05'+struct.pack('<H',p['headers']+24),0x11:b'\x68'+struct.pack('<H',p['palettes'])}
        if name in ('put','interlace'):
            bindings={0x11:b'\x8b\x87'+struct.pack('<H',p['buffers']+2),0x15:b'\x8b\x97'+struct.pack('<H',p['buffers']),0x33:b'\xff\xb7'+struct.pack('<H',p['headers']+20),0x4c:b'\x8b\x87'+struct.pack('<H',p['headers']+20),(0x79 if name=='put' else 0x78):b'\x8b\x87'+struct.pack('<H',p['headers']+22)}
        if name=='quarter':bindings={0x12:b'\x8b\x87'+struct.pack('<H',p['buffers']+2),0x16:b'\x8b\x97'+struct.pack('<H',p['buffers']),0x6d:b'\x68\x40\x01',0xa4:b'\x81\x7e\xfa\xc8\x00'}
        if name=='load':bindings={0xd:b'\x05'+struct.pack('<H',p['headers']),0x17:b'\x66\xff\xb7'+struct.pack('<H',p['buffers']),0x2a:b'\x05'+struct.pack('<H',p['headers']),0x34:b'\x05'+struct.pack('<H',p['buffers'])}
        if any(bytes(by[a].bytes)!=b for a,b in bindings.items()):raise ValueError('PI header/buffer/palette DATA binding differs')
        rows.append(dict(name=name,segment=seg,offset=start,size=size,cleanup=cleanup,positions=sorted(by),instructions=len(ins),edges=edges,sha256=sha(raw)))
    return dict(bodies=rows,owned_bytes=sum(r['size'] for r in rows if r['name'] not in ('free','memcpy')),contextual_bytes=112)


class PiSpec:
    """Source scalar reads live physical headers; native library stores remain ordered."""
    def __init__(self,before,p,s):self.memory=bytearray(before);self.p=p;self.s=s;self.counts={}
    def word(self,at):return struct.unpack_from('<H',self.memory,at)[0]
    def store(self,at,size,value):
        self.memory[at:at+size]=value.to_bytes(size,'little');return ['store',at,size,value]
    def call(self,name,args):
        self.counts[name]=self.counts.get(name,0)+1
        yield ['call',name,args]
        for kind,index,at,data in self.s.get('callback_writes',[]):
            if (kind,index)==(name,self.counts[name]):self.memory[at:at+len(bytes.fromhex(data))]=bytes.fromhex(data)
    def events(self,name):
        p,s,m=self.p,self.s,self.memory;ds=(p['ds']+0x2000)*16;slot=u16(s.get('slot',0));header=u16(p['headers']+slot*72);buffer=u16(p['buffers']+slot*4)
        if name in ('palette','memcpy'):
            src=(ds,u16(header+24)) if name=='palette' else (s.get('src_seg',0x5000)*16,s.get('src_off',0x100))
            dst=(ds,p['palettes']) if name=='palette' else (s.get('dst_seg',0x6000)*16,s.get('dst_off',0x100))
            count=48 if name=='palette' else s.get('count',3)
            for i in range(count//2):yield self.store(dst[0]+u16(dst[1]+i*2),2,self.word(src[0]+u16(src[1]+i*2)))
            if count&1:yield self.store(dst[0]+u16(dst[1]+count-1),1,m[src[0]+u16(src[1]+count-1)])
            if name=='palette':yield from self.call('palette_show',[])
            return
        if name=='load':
            # Header far pointer/buffer far pointer are evaluated before graph_free.
            pointer=[self.word(ds+buffer),self.word(ds+u16(buffer+2))]
            for seg_at,zeros in [(2,(4,2,0)),(18,(14,18,16))]:
                segment=self.word(ds+u16(header+seg_at))
                if segment:
                    yield from self.call('heap_free',[segment])
                    for off in zeros:yield self.store(ds+u16(header+off),2,0)
            if pointer[1]:yield from self.call('heap_free',[pointer[1]])
            yield from self.call('load_pack',[buffer,p['ds']+0x2000,header,p['ds']+0x2000,s.get('fn_off',0x1234),s.get('fn_seg',0x5678)])
            return
        offset=self.word(ds+buffer);segment=self.word(ds+u16(buffer+2));top=u16(s.get('top',399));counter=0
        if name=='quarter':offset,segment=advance(offset,segment,{1:160,2:64000,3:64160}.get(u16(s.get('quarter',0)),0))
        while counter<(200 if name=='quarter' else self.word(ds+u16(header+22))):
            width=320 if name=='quarter' else self.word(ds+u16(header+20))
            yield from self.call('packed_put',[width,offset,segment,top,u16(s.get('left',-7))])
            top=next_top(top);width=320 if name=='quarter' else self.word(ds+u16(header+20))
            offset,segment=advance(offset,segment,width if name in ('interlace','quarter') else width//2);counter=u16(counter+(2 if name=='interlace' else 1))


class PiProbe(Probe):
    def __init__(self,mz,p):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR
        from unicorn import x86_const as reg
        self.uc,self.reg,self.p=Uc(UC_ARCH_X86,UC_MODE_16),reg,p;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for rel in mz.relocations:
            at=rel.segment*16+rel.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code=(p['cs']+0x2000)*16;self.data=(p['ds']+0x2000)*16;self.meta=analyze(mz.program_image,p);self.active=False
        self.positions={seg*16+start+i:(name,i,seg) for name,seg,start,size,cleanup in ranges(p) for i in next(b['positions'] for b in self.meta['bodies'] if b['name']==name)}
        def guard(fn):
            def invoke(*args):
                if not self.active:return
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop()
            return invoke
        def code(uc,address,size,user):
            if address==self.code+0xff00:
                if self.get('CS')!=p['cs']+0x2000:raise ValueError('PI terminal CS alias')
                self.terminal=True;self.uc.emu_stop();return
            at=address-0x20000
            if at in models(p):
                kind,cleanup=models(p)[at];sp=self.get('SP');frame=list(struct.unpack('<'+'H'*(2+cleanup//2),self.uc.mem_read(0x40000+sp,4+cleanup)))
                wanted={'palette_show':[(p['cs']+0x2000,p['palette']+0x21)],'packed_put':[(p['cs']+0x2000,p[n]+(0x75 if n=='quarter' else 0x3c)) for n in ('put','interlace','quarter') if n in p],'load_pack':[(p['cs']+0x2000,p['load']+0x3e)],'heap_free':[(0x2000,p['free']+a) for a in (0x16,0x2f,0x48)]}[kind]
                if self.get('CS')!=0x2000 or self.get('SS')!=0x4000 or (frame[1],frame[0]) not in wanted:raise ValueError('PI modeled native far frame differs')
                event=['call',kind,frame[2:]];self.consume(event);self.events.append(event);self.counts[kind]=self.counts.get(kind,0)+1
                for k,index,addr,data in self.s.get('callback_writes',[]):
                    if (k,index)==(kind,self.counts[kind]):self.uc.mem_write(addr,bytes.fromhex(data));self.fixture_writes.append([k,index,addr,data])
                self.set('AX',u16(self.s.get('status',0)));self.set('EFLAGS',(self.get('EFLAGS')&~1)|int(bool(self.s.get('carry'))))
                self.set('SP',sp+4+cleanup);self.set('CS',frame[1]);self.set('IP',frame[0]);return
            if at not in self.positions:raise ValueError('PI escaped decoded instruction boundary')
            name,pos,seg=self.positions[at]
            if self.get('CS')!=seg+0x2000 or self.get('SS')!=0x4000:raise ValueError('PI native code/stack segment alias')
            self.visited.add((name,pos))
        def write(uc,access,addr,size,value,user):
            if 0x40000<=addr and addr+size<=0x50000:return
            event=['store',addr,size,value];self.consume(event);self.events.append(event)
        def intr(uc,n,user):raise ValueError('PI unknown interrupt')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
    def consume(self,event):
        if next(self.iterator,None)!=event:raise ValueError('PI ordered scalar event differs: '+str(event))
    def initialize(self,s):
        slot=u16(s.get('slot',0));header=u16(self.p['headers']+slot*72);buffer=u16(self.p['buffers']+slot*4)
        raw=bytearray((i*11+17)&255 for i in range(72));struct.pack_into('<3H',raw,0,0x1234,s.get('comment',0x8000),9);struct.pack_into('<3H',raw,14,8,0x4321,s.get('machine',0x9000));struct.pack_into('<2H',raw,20,s.get('width',640),s.get('height',3))
        for i,value in enumerate(raw):self.uc.mem_write(self.data+u16(header+i),bytes([value]))
        for i,value in enumerate(struct.pack('<2H',*s.get('pointer',(0xfffe,0x5000)))):self.uc.mem_write(self.data+u16(buffer+i),bytes([value]))
    def run(self,name,s,persistent=False):
        self.s=s
        for n,v in [('CS',self.p['cs']+0x2000),('DS',self.p['ds']+0x2000),('SS',0x4000),('SP',0xffc0),('BP',0x7777),('SI',0x1357),('DI',0x2468),('ES',0x3333),('FS',0x3456),('AX',0xace1)]:self.set(n,v)
        flags=2|(0x200 if s.get('if',1) else 0)|(0x400 if s.get('df') else 0);self.set('EFLAGS',flags)
        if not persistent:self.initialize(s)
        if name=='memcpy':
            source=bytes((i*17+5)&255 for i in range(s.get('count',3)))
            for i,v in enumerate(source):self.uc.mem_write(s.get('src_seg',0x5000)*16+u16(s.get('src_off',0x100)+i),bytes([v]))
        for at,data in s.get('initial_writes',[]):self.uc.mem_write(at,bytes.fromhex(data))
        slot=u16(s.get('slot',0));args=[slot] if name=='palette' else [s.get('fn_off',0x1234),s.get('fn_seg',0x5678),slot] if name=='load' else [u16(s.get('quarter',0)),slot,u16(s.get('top',399)),u16(s.get('left',-7))] if name=='quarter' else [s.get('dst_off',0x100),s.get('dst_seg',0x6000),s.get('src_off',0x100),s.get('src_seg',0x5000),s.get('count',3)] if name=='memcpy' else [slot,u16(s.get('top',399)),u16(s.get('left',-7))]
        self.uc.mem_write(0x4ffc0,struct.pack('<'+'H'*(2+len(args)),0xff00,self.p['cs']+0x2000,*args))
        before=bytes(self.uc.mem_read(0,0x100000));self.spec=PiSpec(before,self.p,s);self.iterator=self.spec.events(name);self.events=[];self.fixture_writes=[];self.counts={};self.visited=set();self.errors=[];self.terminal=False;self.active=True
        seg=0 if name=='memcpy' else self.p['cs'];start=self.p[name];self.set('CS',seg+0x2000);self.uc.emu_start(0x20000+seg*16+start,0,count=s.get('budget',1000000));self.active=False
        if self.errors:raise ValueError(self.errors[0])
        if self.terminal==bool(s.get('prefix')):raise ValueError('PI terminal/budget differs')
        if self.terminal and next(self.iterator,None) is not None:raise ValueError('PI scalar events remain after native return')
        after=bytes(self.uc.mem_read(0,0x100000));expected=bytes(self.spec.memory)
        if after[:0x40000]+after[0x50000:]!=expected[:0x40000]+expected[0x50000:]:raise ValueError('PI full physical memory outside caller stack differs')
        if self.terminal:
            cleanup=0 if name=='memcpy' else len(args)*2
            if self.get('SP')!=0xffc4+cleanup or [self.get(r) for r in ('BP','SI','DI','DS','FS')]!=[0x7777,0x1357,0x2468,self.p['ds']+0x2000,0x3456]:raise ValueError('PI native ABI/frame/callee-saved differs')
            if self.get('EFLAGS')&0x600!=(flags&~0x400 if name in ('palette','memcpy') else flags)&0x600:raise ValueError('PI native IF/DF differs')
            if name=='load' and self.get('AX')!=u16(s.get('status',0)):raise ValueError('PI load status differs')
        return dict(name=name,case=s,terminal=self.terminal,visited=sorted(self.visited),events=self.events,fixture_writes=self.fixture_writes,status=self.get('AX') if name=='load' else None,memory_before_sha256=sha(before),memory_after_sha256=sha(after))


def cases(p,focused=False):
    result=[];ds=(p['ds']+0x2000)*16
    for name in ('put','interlace'):
        if name not in p:continue
        for width,height in [(640,3),(3,5),(1,3),(0,3),(65535,2),(320,0)]:
            for pointer in [(0,0x5000),(0xfffe,0x5000),(0xfff0,0xffff)]:result.append((name,dict(width=width,height=height,pointer=pointer)))
        for slot,top in [(5,800),(6,-1),(65535,32767),(0,-32768)]:result.append((name,dict(slot=slot,width=8,height=3,pointer=(0xffff,0x5000),left=641,top=top)))
        for index in (1,2):result.append((name,dict(height=20,callback_writes=[['packed_put',index,ds+p['headers']+20,'03000300']])))
        result.append((name,dict(height=65535,prefix=True,budget=2000)))
    if 'quarter' in p:
        for q in (-1,0,1,2,3,4,255):
            for pointer in [(0,0x5000),(0xfffe,0x5000)]:result.append(('quarter',dict(quarter=q,pointer=pointer,top=800)))
        for slot in (5,6,65535):result.append(('quarter',dict(slot=slot,quarter=3,pointer=(0xfff0,0xffff),top=32767)))
    for slot in (0,5,6,65535):
        result.append(('palette',dict(slot=slot)))
        for status in ([0,0xffff] if focused else [0,1,0x7fff,0x8000,0xffff]):result.append(('load',dict(slot=slot,status=status,carry=status&1,pointer=(0xabcd,0x5000))))
    for slot in (2691,6332,1781):result.append(('palette',dict(slot=slot)))
    for comment,machine,pointer in [(0,0,(9,0)),(0x8000,0,(0,0)),(0,0x9000,(0,0x5000)),(0x8000,0x8000,(7,0x8000))]:result.append(('load',dict(comment=comment,machine=machine,pointer=pointer,status=0xffff)))
    result.append(('load',dict(callback_writes=[['load_pack',1,ds+p['buffers'],'07000070']])))
    result.append(('load',dict(callback_writes=[['heap_free',1,ds+p['headers']+18,'0000']])))
    for count in (0,1,2,3,47,48):
        for delta in (0,1,2,-1):result.append(('memcpy',dict(count=count,src_seg=0x6000,dst_seg=0x6000,src_off=0xfff8,dst_off=u16(0xfff8+delta))))
    result=[(n,dict(s,df=df,**{'if':iff})) for n,s in result for df,iff in ((0,0),(0,1),(1,0),(1,1))]
    return result


def matrix(mz,p,focused=False):
    rows=[PiProbe(mz,p).run(n,s) for n,s in cases(p,focused)]
    probe=PiProbe(mz,p);s=dict(pointer=(4,0x5000),status=0xffff)
    for i in range(3):
        row=probe.run('load',s,persistent=i>0);row['persistent_sequence_index']=i;rows.append(row)
    return rows


def coverage(meta,rows):
    wanted={(b['name'],i) for b in meta['bodies'] for i in b['positions']};seen={tuple(v) for r in rows for v in r['visited']}
    if wanted!=seen:raise ValueError('PI incomplete native coverage: '+str(sorted(wanted-seen)))
    return dict(positions=len(wanted),complete=True,invocations=len(rows),returns=sum(r['terminal'] for r in rows),prefixes=sum(not r['terminal'] for r in rows),stores=sum(sum(e[0]=='store' for e in r['events']) for r in rows),calls=sum(sum(e[0]=='call' for e in r['events']) for r in rows))


def semantic(rows):return json.loads(json.dumps([{k:v for k,v in r.items() if not k.startswith('memory_')} for r in rows]))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args();raw=(ROOT/PARENT).read_bytes()
    if sha(raw)!=PARENT_SHA:raise ValueError('PI previous cold proof differs')
    previous=json.loads(raw);inputs={**previous['inputs'],PARENT:sha(raw)}
    for path in ['scripts/review_th03_shared_pi.py','scripts/review_th03_mainl_pi.py','.analysis/sol-shared-pi-op-ghidra-check-20261006.log','.analysis/sol-shared-pi-mainl-ghidra-check-20261006.log']:inputs[path]=sha((ROOT/path).read_bytes())
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in [*PROVIDERS,'Tupfile.lua']}
    def verify():
        for path,h in inputs.items():
            if sha((ROOT/path).read_bytes())!=h:raise ValueError('PI prerequisite changed: '+path)
    verify();prior=json.loads((ROOT/'.analysis/sol-shared-snd-load-review-20261006.json').read_bytes());observations={}
    for art,p in PROFILES.items():
        artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-'+art);stored=read_verified_artifact(ROOT,artifact)
        paths=[prior['observations'][art][0]['path']]+[str(Path(PARENT).parent/f'round{n}/source/bin/th03/{art}.exe') for n in (1,2)];observations[art]=[];target=parse_mz((ROOT/paths[0]).read_bytes())
        for path in paths:
            inputs[path]=sha((ROOT/path).read_bytes());mz=parse_mz((ROOT/path).read_bytes())
            if not mz.valid:raise ValueError('PI invalid MZ')
            meta=analyze(mz.program_image,p);cpu=matrix(mz,p);row=dict(path=path,analysis=meta,cpu=cpu,coverage=coverage(meta,cpu))
            if observations[art]:
                tree=Path(path).parents[2];mp=tree/f'obj/th03/{art}.map';inputs[str(mp)]=sha((ROOT/mp).read_bytes());maprows=code_rows((ROOT/mp).read_text(),len(mz.program_image));comparisons={}
                for module,key,size in MODULES:
                    if key not in p:continue
                    mr=next(r for r in maprows if r['module']==module and r['size'])
                    if (mr['segment'],mr['offset'],mr['size'])!=(p['cs'],p[key],size):raise ValueError('PI original complete MAP ownership differs')
                    comp=extent_observation(target,mz,mr)
                    if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('PI original complete raw/ordered carrier differs')
                    comparisons[module]=comp;obj=tree/'obj/th03'/(Path(module).stem+'.obj');inputs[str(obj)]=sha((ROOT/obj).read_bytes())
                row['comparisons']=comparisons
                for name,data in providers.items():
                    cp=tree/name;cached=(ROOT/cp).read_bytes();inputs[str(cp)]=sha(cached)
                    if name.endswith(('.asm','.inc')):cached=cached.replace(b'\r\n',b'\n');data=data.replace(b'\r\n',b'\n')
                    if name=='Tupfile.lua':cached=cached.replace(b'"th03/vector_far.asm"',b'"th03/vector.cpp"')
                    if cached!=data:raise ValueError('PI actual frozen provider differs: '+name)
                if meta!=observations[art][0]['analysis'] or semantic(cpu)!=semantic(observations[art][0]['cpu']):raise ValueError('PI independent artifact observations differ')
            observations[art].append(row)
        if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('PI canonical target changed')
        print('PASS shared PI',art,observations[art][0]['coverage'],flush=True)
    verify();report=dict(kind='th03-shared-pi-complete-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
