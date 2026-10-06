#!/usr/bin/env python3
"""Bind complete OP/MAINL sound loaders to native copies and declared INT replies."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import itertools
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
from review_th03_mainl_snow import u16

ROOT=Path(__file__).resolve().parents[1]
PARENT='.analysis/th03-shared-math/sol-shared-math-source-20261006-b/receipt.json'
PARENT_SHA='2e8c4c6205510417b8b298b0ed182ecd11b17ad45b5a52682b581ac3f88f31c1'
PROFILES={'op':dict(cs=0xbeb,ds=0xd7f,start=0xa2,filename=0x1a0e,midi=0x1a0b),
          'mainl':dict(cs=0xc7e,ds=0xe3f,start=0xa0,filename=0x1c74,midi=0x1c71)}
PROVIDERS=['th02/snd_load.cpp','th02/snd/load.cpp','th02/snd/snd.h',
           'th02/snd/impl.hpp','th02/snd/load[bss].asm','th02/snd/snd[bss].asm',
           'libs/kaja/kaja.h','game/pf.h','defconv.h','x86real.h','platform.h','Tupfile.lua']
REGS=('AX','BX','CX','DX','DS','ES','SS','SP','BP','SI','DI','FS')


def analyze(image,p):
    start=p['start'];body=image[p['cs']*16+start:p['cs']*16+start+112]
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;ins=list(decoder.disasm(body,start));bounds={i.address for i in ins};edges=[]
    if len(body)!=112 or sum(i.size for i in ins)!=112 or (ins[-1].mnemonic,ins[-1].op_str)!=('retf',''):
        raise ValueError('sound loader complete far C body differs')
    by={i.address-start:i for i in ins}
    for i in ins:
        at=i.address-start
        if i.mnemonic in ('call','lcall','ret','in','out') or i.mnemonic=='retf' and at!=111:raise ValueError('sound loader unknown interface')
        if i.mnemonic=='int' and (at,i.op_str) not in [(0x47,'0x21'),(0x5a,'0x61'),(0x5e,'0x60'),(0x66,'0x21'),(0x6b,'0x21')]:raise ValueError('sound loader interrupt binding differs')
        if i.mnemonic.startswith(('j','loop')):
            if len(i.operands)!=1 or i.operands[0].type!=X86_OP_IMM or i.operands[0].imm not in bounds:raise ValueError('sound loader branch enters operand/neighbor')
            edges.append([at,i.mnemonic,i.operands[0].imm-start])
    expected={5:('mov','cx, 0xd'),10:('les','bx, ptr [bp + 6]'),0x19:('mov','ax, word ptr [bp + 0xa]'),
              0x1c:('cmp','ax, 0x600'),0x4b:('mov','ax, word ptr [bp + 0xa]'),0x4e:('cmp','ax, 0x600'),
              0x63:('mov','cx, 0x5000'),0x68:('pop','ds'),0x69:('mov','ah, 0x3e')}
    for at,pair in expected.items():
        if (by[at].mnemonic,by[at].op_str)!=pair:raise ValueError('sound loader ABI/count binding differs')
    # Freeze complete encoded operands, not a displacement substring search.
    bindings={0x12:b'\x88\x84'+struct.pack('<H',p['filename']),0x21:b'\x80\x3e'+struct.pack('<H',p['midi'])+b'\0',
              0x2b:b'\x80\xbf'+struct.pack('<H',p['filename'])+b'\0',0x32:b'\xc6\x87'+struct.pack('<H',p['filename'])+b'm',
              0x37:b'\xc6\x87'+struct.pack('<H',p['filename']+1)+b'd',0x3c:b'\xc6\x87'+struct.pack('<H',p['filename']+2)+b'\0',
              0x41:b'\xba'+struct.pack('<H',p['filename']),0x53:b'\x80\x3e'+struct.pack('<H',p['midi'])+b'\0'}
    if any(bytes(by[at].bytes)!=raw for at,raw in bindings.items()):raise ValueError('sound loader filename/MIDI DATA binding differs')
    if edges!=[[0x17,'loop',0xa],[0x1f,'jne',0x41],[0x26,'je',0x41],[0x30,'jne',0x2a],[0x51,'jne',0x5e],[0x58,'je',0x5e],[0x5c,'jmp',0x60]]:
        raise ValueError('sound loader complete control flow differs')
    return dict(segment=p['cs'],offset=start,size=112,positions=sorted(by),instructions=len(ins),edges=edges,sha256=sha(body),cleanup=0)


def reply(s,stage):
    defaults={'open':{'AX':7},'driver':{'DS':0x6000,'DX':0x100,'AX':0x4567},'read':{'AX':len(bytes.fromhex(s.get('payload','01020304050607')))},'close':{'AX':0}}
    return {**defaults[stage],**s.get(stage+'_reply',{})}


class LoadSpec:
    """Scalar copy/scan and register flow; all bytes come from the physical pre-state."""
    def __init__(self,before,p,s,regs):self.memory=bytearray(before);self.p=p;self.s=s;self.regs=dict(regs);self.prefix=False
    def word(self,a):return struct.unpack_from('<H',self.memory,a)[0]
    def events(self):
        r,m,p,s=self.regs,self.memory,self.p,self.s;sp=r['SP'];stack=r['SS']*16
        for at,value in [(sp-2,r['BP']),(sp-4,r['SI']),(sp-6,r['DS'])]:struct.pack_into('<H',m,stack+u16(at),value)
        r.update(SP=u16(sp-6),BP=u16(sp-2),CX=13,SI=0)
        for i in range(13):
            fp=stack+u16(r['BP']+6);r['BX']=u16(self.word(fp)+i);r['ES']=self.word(fp+2)
            value=m[r['ES']*16+r['BX']];r['AX']=(r['AX']&0xff00)|value;at=r['DS']*16+u16(p['filename']+i)
            m[at]=value;yield ['store',at,1,value];r['SI']=i+1;r['CX']-=1
        r['AX']=self.word(stack+u16(r['BP']+10))
        if r['AX']==0x600 and m[r['DS']*16+p['midi']]:
            r['BX']=0
            for _ in range(s.get('scan_limit',65536)):
                r['BX']=u16(r['BX']+1)
                if not m[r['DS']*16+u16(p['filename']+r['BX'])]:break
            else:self.prefix=True;return
            for j,value in enumerate(b'md\0'):
                at=r['DS']*16+u16(p['filename']+r['BX']+j);m[at]=value;yield ['store',at,1,value]
        r.update(DX=p['filename'],AX=0x3d00)
        for stage in ('open','driver','read','close'):
            if stage=='driver':
                r['BX']=r['AX'];r['AX']=self.word(stack+u16(r['BP']+10))
                number=0x61 if r['AX']==0x600 and m[r['DS']*16+p['midi']] else 0x60
            else:
                number=0x21
                if stage=='read':r.update(AX=0x3f00,CX=0x5000)
                if stage=='close':r.update(DS=self.word(stack+u16(sp-6)),SP=u16(sp-4),AX=(r['AX']&255)|0x3e00)
            yield ['interrupt',stage,number,{k:r[k] for k in REGS}]
            if stage=='read':
                payload=bytes.fromhex(s.get('payload','01020304050607'));at=r['DS']*16+r['DX'];m[at:at+len(payload)]=payload
            for at,data in s.get(stage+'_writes',[]):m[at:at+len(bytes.fromhex(data))]=bytes.fromhex(data)
            r.update({k:v for k,v in reply(s,stage).items() if k!='CF'})
        r.update(SI=self.word(stack+u16(sp-4)),BP=self.word(stack+u16(sp-2)),SP=u16(sp+4))


class LoadProbe(Probe):
    """Only the complete loader executes; software interrupts have declared fixtures."""
    def __init__(self,mz,p):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR
        from unicorn import x86_const as reg
        self.uc,self.reg,self.p=Uc(UC_ARCH_X86,UC_MODE_16),reg,p;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for rel in mz.relocations:
            at=rel.segment*16+rel.offset;struct.pack_into('<H',image,at,u16(struct.unpack_from('<H',image,at)[0]+0x2000))
        self.uc.mem_write(0x20000,bytes(image));self.code=(p['cs']+0x2000)*16;self.ds=(p['ds']+0x2000)*16;self.meta=analyze(mz.program_image,p)
        self.uc.mem_write(self.ds+p['filename'],b'Z'*32+b'\0');self.active=False
        def guard(fn):
            def call(*args):
                if not self.active:return
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop()
            return call
        def code(uc,address,size,user):
            if address==self.code+0xff00:self.terminal=True;self.uc.emu_stop();return
            at=address-self.code-p['start']
            if at not in self.meta['positions']:raise ValueError('sound loader escaped complete body')
            self.at=at;self.visited.add(at)
            if at==0x2a:
                self.scans+=1
                if self.scans>self.s.get('scan_limit',65536):self.prefix=True;self.uc.emu_stop()
        def write(uc,access,address,size,value,user):
            if self.at in (0,3,4):
                index={0:0,3:1,4:2}[self.at];wanted=(0x40000+0xffbe-index*2,2,[0x7777,0x1357,self.p['ds']+0x2000][index])
                if (address,size,value)!=wanted:raise ValueError('sound loader prologue stack write differs')
                return
            event=['store',address,size,value];self.consume(event);self.events.append(event)
        def interrupt(uc,number,user):
            stage={0x47:'open',0x5a:'driver',0x5e:'driver',0x66:'read',0x6b:'close'}.get(self.at)
            if stage is None:raise ValueError('sound loader unknown interrupt position')
            event=['interrupt',stage,number,{k:self.get(k) for k in REGS}];self.consume(event);self.events.append(event)
            if self.get('EFLAGS')&0x600!=self.flags&0x600:raise ValueError('sound loader incoming IF/DF changed')
            if stage=='read':
                data=bytes.fromhex(self.s.get('payload','01020304050607'));at=self.get('DS')*16+self.get('DX')
                if len(data)>0x5000 or at+len(data)>0x100000:raise ValueError('sound loader read fixture out of bounds')
                self.uc.mem_write(at,data);self.fixture_writes.append([at,data.hex()])
            for at,data in self.s.get(stage+'_writes',[]):self.uc.mem_write(at,bytes.fromhex(data));self.fixture_writes.append([at,data])
            for name,value in reply(self.s,stage).items():
                if name=='CF':self.set('EFLAGS',(self.get('EFLAGS')&~1)|(value&1))
                else:self.set(name,value)
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(interrupt))
    def consume(self,event):
        if next(self.iterator,None)!=event:raise ValueError('sound loader native event differs: '+str(event))
    def run(self,s,persistent=False):
        self.s=s;self.flags=2|(0x200 if s.get('if',True) else 0)|(0x400 if s.get('df') else 0)
        regs=dict(AX=0xace1,BX=0x9876,CX=0x5432,DX=0x8765,DS=self.p['ds']+0x2000,ES=0x3333,SS=0x4000,SP=0xffc0,BP=0x7777,SI=0x1357,DI=0x2468,FS=0x3456)
        for name,value in regs.items():self.set(name,value)
        self.set('CS',self.p['cs']+0x2000);self.set('IP',self.p['start']);self.set('EFLAGS',self.flags)
        self.uc.mem_write(0x4ffc0,struct.pack('<5H',0xff00,self.p['cs']+0x2000,s.get('offset',0xfff8),s.get('segment',0x5000),s.get('func',0x600)))
        if not persistent:self.uc.mem_write(self.ds+self.p['filename'],bytes.fromhex(s.get('stale','5a'*32+'00')))
        self.uc.mem_write(self.ds+self.p['midi'],bytes([s.get('midi',1)]))
        source=bytes.fromhex(s.get('source','4142434445464748494a4b4c00'));seg=s.get('segment',0x5000);off=s.get('offset',0xfff8)
        if not s.get('leave_source'):
            for i,value in enumerate(source):self.uc.mem_write(seg*16+u16(off+i),bytes([value]))
        for at,data in s.get('initial_writes',[]):self.uc.mem_write(at,bytes.fromhex(data))
        before=bytes(self.uc.mem_read(0,0x100000));self.spec=LoadSpec(before,self.p,s,regs);self.iterator=self.spec.events()
        self.errors=[];self.events=[];self.fixture_writes=[];self.visited=set();self.scans=0;self.terminal=self.prefix=False;self.active=True
        self.uc.emu_start(self.code+self.p['start'],0,count=1000000);self.active=False
        if self.errors:raise ValueError(self.errors[0])
        if next(self.iterator,None) is not None or self.terminal==self.prefix or self.spec.prefix!=self.prefix:raise ValueError('sound loader termination/prefix differs')
        after=bytes(self.uc.mem_read(0,0x100000))
        if after!=bytes(self.spec.memory):raise ValueError('sound loader complete physical memory differs')
        if self.terminal:
            # Unicorn's code-hook IP is the low physical address in this version;
            # the complete far return is bound by the physical sentinel and CS.
            if {k:self.get(k) for k in REGS}!=self.spec.regs or self.get('CS')!=self.p['cs']+0x2000:raise ValueError('sound loader native far frame/register flow differs')
            if self.get('EFLAGS')&0x600!=self.flags&0x600:raise ValueError('sound loader final IF/DF differs')
        return dict(case=s,terminal=self.terminal,prefix=self.prefix,visited=sorted(self.visited),events=self.events,fixture_writes=self.fixture_writes,registers={k:self.get(k) for k in REGS} if self.terminal else None,filename=after[self.ds+self.p['filename']:self.ds+self.p['filename']+36].hex(),memory_before_sha256=sha(before),memory_after_sha256=sha(after))


def cases(p,focused=False):
    ds=p['ds']+0x2000;filename=p['filename'];rows=[]
    funcs=[0x600,0xb00] if focused else [0x600,0xb00,0,0x601,0xffff]
    for func,midi,end,df,iff in itertools.product(funcs,[0,1,255],[0,1,12],(0,1),(0,1)):
        src=bytearray(b'ABCDEFGHIJKLQ');src[end]=0;rows.append(dict(func=func,midi=midi,source=src.hex(),df=df,if_=iff))
        rows[-1]['if']=rows[-1].pop('if_')
    for end in ([2,7,11] if focused else range(2,12)):
        src=bytearray(b'ABCDEFGHIJKLQ');src[end]=0;rows.append(dict(source=src.hex()))
    for delta in [-2,-1,0,1,2,12]:rows.append(dict(segment=ds,offset=u16(filename+delta),source='4142434445464748494a4b4c00'))
    rows.extend([dict(segment=ds-1,offset=filename+16),dict(segment=0,offset=0,leave_source=True),dict(segment=0x4000,offset=0xffba,leave_source=True),
                 dict(source='41'*13,stale='5a'*20+'00'+'a5'*15),dict(open_reply={'AX':2,'CF':1},payload='',read_reply={'AX':6,'CF':1}),
                 dict(driver_reply={'DS':ds,'DX':filename},payload='00'*13),dict(driver_reply={'DS':0x4000,'DX':0xffba},payload='34127856bc9a'),
                 dict(driver_reply={'BX':0x4321}),dict(read_reply={'BX':0xbeef,'DX':0xfedc,'CX':1,'CF':1},payload=''),
                 dict(driver_reply={'DS':0x6000,'DX':0xffff},payload='aabbccdd'),
                 dict(open_writes=[[(ds*16+p['midi']),'00']]),dict(open_writes=[[(ds*16+p['midi']),'ff']],midi=0),
                 dict(open_reply={'DS':0x6100},initial_writes=[[(0x61000+p['midi']),'00']]),
                 dict(payload=bytes((i*17+3)&255 for i in range(0x5000)).hex(),read_reply={'AX':0x5000}),
                 dict(source='41'*13,stale='41'*32,initial_writes=[[(ds*16+filename+32),'41'*128]],scan_limit=64)])
    return rows


def matrix(mz,p,focused=False):
    rows=[LoadProbe(mz,p).run(s) for s in cases(p,focused)]
    probe=LoadProbe(mz,p)
    for i,s in enumerate([dict(source='4c4f4e474e414d452e4d000000'),dict(source='00'+'58'*12),dict(midi=0,source='414200'+'59'*10)]):
        r=probe.run(s,persistent=True);r['persistent_sequence_index']=i;rows.append(r)
    return rows


def coverage(meta,rows):
    seen={i for r in rows for i in r['visited']}
    if seen!=set(meta['positions']):raise ValueError('sound loader incomplete instruction coverage')
    return dict(positions=len(seen),complete=True,invocations=len(rows),returns=sum(r['terminal'] for r in rows),prefixes=sum(r['prefix'] for r in rows),stores=sum(sum(e[0]=='store' for e in r['events']) for r in rows),interrupts=sum(sum(e[0]=='interrupt' for e in r['events']) for r in rows))


def semantic(rows):return json.loads(json.dumps([{k:v for k,v in r.items() if not k.startswith('memory_')} for r in rows]))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    raw=(ROOT/PARENT).read_bytes()
    if sha(raw)!=PARENT_SHA:raise ValueError('sound loader parent cold proof differs')
    previous=json.loads(raw);inputs={**previous['inputs'],PARENT:sha(raw)}
    for path in ['scripts/review_th03_shared_snd_load.py','.analysis/sol-shared-snd-load-op-ghidra-check-20261006.log','.analysis/sol-shared-snd-load-mainl-ghidra-check-20261006.log']:inputs[path]=sha((ROOT/path).read_bytes())
    providers={p:subprocess.check_output(['git','show',f'{REVISION}:{p}'],cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    def verify():
        for p,h in inputs.items():
            if sha((ROOT/p).read_bytes())!=h:raise ValueError('sound loader input changed: '+p)
    verify();prior=json.loads((ROOT/'.analysis/sol-shared-math-review-20261006.json').read_bytes());observations={}
    for art,p in PROFILES.items():
        artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-'+art);stored=read_verified_artifact(ROOT,artifact)
        paths=[prior['observations'][art][0]['path']]+[str(Path(PARENT).parent/f'round{n}/source/bin/th03/{art}.exe') for n in (1,2)]
        observations[art]=[];target=parse_mz((ROOT/paths[0]).read_bytes())
        for path in paths:
            inputs[path]=sha((ROOT/path).read_bytes());mz=parse_mz((ROOT/path).read_bytes())
            if not mz.valid:raise ValueError('sound loader invalid MZ')
            meta=analyze(mz.program_image,p);cpu=matrix(mz,p);row=dict(path=path,analysis=meta,cpu=cpu,coverage=coverage(meta,cpu))
            if observations[art]:
                tree=Path(path).parents[2];mp=tree/f'obj/th03/{art}.map';inputs[str(mp)]=sha((ROOT/mp).read_bytes());mr=next(r for r in code_rows((ROOT/mp).read_text(),len(mz.program_image)) if r['module']=='th02/snd_load.cpp' and r['size'])
                if (mr['segment'],mr['offset'],mr['size'])!=(p['cs'],p['start'],112):raise ValueError('sound loader original MAP ownership differs')
                comp=extent_observation(target,mz,mr)
                if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('sound loader original raw/ordered carrier differs')
                row['comparison']=comp;obj=tree/'obj/th02/snd_load.obj';inputs[str(obj)]=sha((ROOT/obj).read_bytes())
                buildlog=Path(PARENT).parent/f'round{len(observations[art])}/cold-build.log';log=(ROOT/buildlog).read_text();inputs[str(buildlog)]=sha((ROOT/buildlog).read_bytes())
                if '-DGAME=2 -ml -DBINARY=\'O\' -nobj/th02/ th02/snd_load.cpp' not in log:raise ValueError('sound loader physical GAME2 compiler association differs')
                for name,data in providers.items():
                    cp=tree/name;cached=(ROOT/cp).read_bytes();inputs[str(cp)]=sha(cached)
                    if name.endswith(('.asm','.inc')):cached=cached.replace(b'\r\n',b'\n');data=data.replace(b'\r\n',b'\n')
                    if name=='Tupfile.lua':cached=cached.replace(b'"th03/vector_far.asm"',b'"th03/vector.cpp"')
                    if cached!=data:raise ValueError('sound loader actual frozen provider differs: '+name)
                if meta!=observations[art][0]['analysis'] or semantic(cpu)!=semantic(observations[art][0]['cpu']):raise ValueError('sound loader independent artifact observations differ')
            observations[art].append(row)
        if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('sound loader canonical target changed')
        print('PASS shared sound loader',art,observations[art][0]['coverage'],flush=True)
    verify();report=dict(kind='th03-shared-snd-load-complete-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,providers={p:sha(d) for p,d in providers.items()},observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
