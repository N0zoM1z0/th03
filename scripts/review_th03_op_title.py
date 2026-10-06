#!/usr/bin/env python3
"""Bound complete OP title animations and native column write attempts."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import re
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from inventory_rec98_th03 import frozen_files
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import Probe, REVISION, sha

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/th03-op-score/sol-op-score-source-20261006-d/receipt.json'
PROOF_SHA='638b462b6306c5e3d31670b133bc8d558806284a5ee01b4a3dfd4dce0f000125'
ORIGINAL='.analysis/sol-op-score-review-20261006.json'
CS,DS=0x990,0xd7f
TONE,SHADOW,BG,CLOCK=0x2d4,0x11d9,0x11e5,0x11e8
RANGES=[('intro',0x14e2,550,0),('fade',0x1708,167,0),('expand',0x17af,44,0),
        ('shrink',0x17db,47,0),('column',0x180a,94,2)]
MODELS={
 (0,0x27fe):('super-entry',4,[0x14f4,0x1710]),
 (0xbeb,0x553):('kaja',2,[0x14fc,0x1718,0x1677,0x178b]),
 (0xbeb,0xa2):('snd-load',0,[0x1508,0x1724]),
 (0xbeb,0xa90):('pi-load',6,[0x1516,0x1590,0x173d]),
 (0,0x1aa4):('palette',0,[0x1521,0x1563,0x1577,0x15b3,0x15cb,0x15dc,0x1615,
                           0x1646,0x1658,0x1670,0x16a4,0x16ba,0x16cc,0x1732,0x1798]),
 (0xbeb,0x4cb):('pi-put',6,[0x1531,0x1548,0x1692,0x16e9,0x1756,0x176d]),
 (0xbeb,0x4a6):('pi-palette',2,[0x153e,0x1688,0x1763]),
 (0,0x734):('shift',2,[0x154f,0x15fa]),
 (0,0x12dc):('pi-free',8,[0x1585,0x16fd,0x1781]),
 (0xbeb,0x2ee):('frame',2,[0x15a2,0x1620,0x164d,0x165f,0x1699,0x16ab,0x16c1,0x16d3,0x179f,0x17ca,0x17f9]),
 (CS,0x1aef):('cdg3',0,[0x1632,0x1748]),
 (CS,0x1a8d):('cdg1',0,[0x1702,0x1786]),
 (0,0x28d8):('super-put',6,[0x17c3,0x17f2]),
}
CALLS={site:dest for dest,(_,_,sites) in MODELS.items() for site in sites}
CALLS.update({0x17b9:(CS,0x180a),0x17e8:(CS,0x180a)})
PROVIDERS=['th03/op_main.cpp','th03/op/m_main.cpp','th03/op/m_main.hpp','th03/op/m_select.hpp',
           'th03/sprites/opwin.hpp','th03/common.h','th03/shiftjis/fns.hpp','th03/snd/snd.h',
           'th02/hardware/frmdelay.h','th02/formats/pi.h','platform/x86real/pc98/page.hpp',
           'platform/x86real/flags.hpp','planar.h','libs/master.lib/master.hpp']


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    rows=[];bounds=set();returns={};entries={};calls={};ports=set();semantics=[]
    for name,start,size,cleanup in RANGES:
        body=image[CS*16+start:CS*16+start+size];ins=list(decoder.disasm(body,start));local={i.address for i in ins}
        expected=('ret',str(cleanup) if cleanup else '')
        if len(body)!=size or not ins or sum(i.size for i in ins)!=size or (ins[-1].mnemonic,ins[-1].op_str)!=expected:
            raise ValueError('OP title complete body/cleanup differs')
        entries[start]=name;bounds.update(i.address for i in ins);edges=[]
        for i in ins:
            semantics.append([i.address,i.mnemonic,i.op_str])
            if i.mnemonic in ('ret','retf'):
                if (i.mnemonic,i.op_str)!=expected:raise ValueError('OP title interior return differs')
                returns[i.address]=cleanup
            if i.mnemonic in ('in','int','iret'):raise ValueError('OP title unexpected input/interrupt')
            if i.mnemonic=='out':ports.add(i.address)
            if not(i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('OP title indirect/operand edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (CS,i.operands[0].imm)
            if i.mnemonic in ('call','lcall'):
                if CALLS.get(i.address)!=dest or i.mnemonic!=('call' if dest[0]==CS else 'lcall'):
                    raise ValueError('OP title unknown native/model call')
                calls[i.address+i.size]=dict(site=i.address,destination=dest)
            elif i.mnemonic=='ljmp' or dest[1] not in local:raise ValueError('OP title branch enters operand/neighbor')
            edges.append(dict(site=i.address,kind=i.mnemonic,destination=list(dest)))
        rows.append(dict(name=name,offset=start,size=size,cleanup=cleanup,sha256=sha(body),instructions=len(ins),edges=edges))
    return dict(bodies=rows,bounds=bounds,returns=returns,entries=entries,calls=calls,ports=ports,semantics=semantics)


class TitleSpec:
    """Independent scalar loops and writable flat-memory write-attempt fixture."""
    def __init__(self,before,data,scenario):
        self.memory=bytearray(before);self.data=data;self.s=scenario
        self.events=[];self.writes=[];self.reads=[];self.native=Counter();self.external=[]
    def put(self,address,size,value):
        value&=(1<<(size*8))-1;self.writes.append((address,size,value))
        self.memory[address:address+size]=value.to_bytes(size,'little')
    def call(self,name,args=()):
        event=dict(name=name,args=list(args))
        if name=='palette':
            event.update(tone=int.from_bytes(self.memory[self.data+TONE:self.data+TONE+2],'little'),
                         shadow=list(self.memory[self.data+SHADOW:self.data+SHADOW+3]),
                         background=list(self.memory[self.data+BG:self.data+BG+3]))
        self.events.append(event)
    def port(self,port,value):self.call('out',[port,value])
    def tone(self,value):self.put(self.data+TONE,2,value);self.call('palette')
    def color(self,offset,value):
        for i in range(3):self.put(self.data+offset+i,1,value)
    def free(self):
        p=int.from_bytes(self.memory[self.data+0x1ca8:self.data+0x1cac],'little')
        self.call('pi-free',[p&65535,p>>16,0x1cc0,0x2000+DS])
    def opening(self):
        self.call('super-entry',[0x9e2,0x2000+DS]);self.call('kaja',[256]);self.call('snd-load',[0x9ec,0x2000+DS,0x600])
    def column(self,left):
        self.native['column']+=1;di=(0x77b0+((left&65535)>>3))&65535
        while True:
            self.port(0xa6,1);addresses=[base+di for base in (0xad000,0xb5000,0xbd000,0xe5000)]
            values=[int.from_bytes(self.memory[a:a+2],'little') for a in addresses]
            self.reads.extend((a,2,v) for a,v in zip(addresses,values));self.port(0xa6,0)
            for a,v in reversed(list(zip(addresses,values))):self.put(a,2,v)
            if di<80:break
            di-=80
    def expand(self):
        self.native['expand']+=1
        for left in range(288,392,8):self.column(left);self.call('super-put',[2,256,left]);self.call('frame',[1])
    def shrink(self):
        self.native['shrink']+=1
        for left in range(384,279,-8):self.column(left+8);self.call('super-put',[2,256,left]);self.call('frame',[1])
    def fade(self):
        self.native['fade']+=1;self.opening();self.tone(0);self.call('pi-load',[0x9f9,0x2000+DS,0])
        self.port(0xa4,0);self.call('cdg3');self.port(0xa6,1);self.call('pi-put',[0,0,0])
        self.port(0xa6,0);self.call('pi-palette',[0]);self.call('pi-put',[0,0,0]);self.port(0xa6,0)
        self.free();self.call('cdg1');self.call('kaja',[0])
        for level in range(0,101,4):self.tone(level);self.call('frame',[1])
    def intro(self):
        self.native['intro']+=1;self.opening();self.call('pi-load',[0x9f1,0x2000+DS,0]);self.tone(0)
        self.port(0xa6,1);self.call('pi-put',[0,0,0]);self.port(0xa6,0);self.call('pi-palette',[0])
        self.call('pi-put',[0,0,0]);self.call('shift',[2])
        self.color(BG,0);self.call('palette');self.color(SHADOW,0);self.call('palette');self.free()
        self.call('pi-load',[0x9f9,0x2000+DS,0]);self.port(0xa4,1)
        level=0;page=0
        for x in range(160,17,-2):
            self.call('frame',[1]);self.color(BG,level);self.call('palette')
            if level<=128:self.color(SHADOW,level)
            self.call('palette')
            if level<=100:self.tone(level)
            level+=2;self.port(0xa4,page);page=1-page;self.port(0xa6,page);self.call('shift',[4])
        while level<255:self.color(BG,level);self.call('palette');level+=2;self.call('frame',[1])
        self.put(self.data+CLOCK,2,0);self.call('cdg3')
        self.call('timer-input',[self.s['tick_visits'],16]);self.external.append((self.data+CLOCK,2,16))
        self.memory[self.data+CLOCK:self.data+CLOCK+2]=(16).to_bytes(2,'little')
        for i in range(8):self.tone(200);self.call('frame',[1]);self.tone(100);self.call('frame',[1])
        self.tone(200);self.call('kaja',[0]);self.port(0xa4,0);self.port(0xa6,0);self.call('pi-palette',[0])
        self.call('pi-put',[0,0,0]);self.call('frame',[1]);self.tone(100);self.call('frame',[1])
        for i in range(8):self.tone(200);self.call('frame',[1]);self.tone(100);self.call('frame',[1])
        self.port(0xa6,1);self.call('pi-put',[0,0,0]);self.port(0xa6,0);self.free();self.call('cdg1')


class TitleProbe(Probe):
    def __init__(self,mz,scenario):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,(struct.unpack_from('<H',image,at)[0]+0x2000)&65535)
        self.uc.mem_write(0x20000,bytes(image));self.code=(0x2000+CS)*16;self.data=(0x2000+DS)*16;self.stack=0x40000
        profile=scenario['profile'];fixture=bytes((i*17+(i>>8)*29+profile*113)&255 for i in range(0x60000))
        self.uc.mem_write(0xa0000,fixture)
        self.uc.mem_write(self.data+TONE,(0x1234+profile).to_bytes(2,'little'))
        self.uc.mem_write(self.data+SHADOW,bytes([19+profile,37+profile,71+profile]))
        self.uc.mem_write(self.data+BG,bytes([89+profile,103+profile,127+profile]))
        self.uc.mem_write(self.data+CLOCK,(0xabcd).to_bytes(2,'little'))
        self.uc.mem_write(self.data+0x1ca8,struct.pack('<HH',0x1234+profile,0x6000+profile))
        self.meta=analyze(mz.program_image);self.s=scenario;self.frames=[];self.top=None;self.errors=[];self.stop=False
        self.visited=set();self.events=[];self.writes=[];self.reads=[];self.native=Counter();self.external=[];self.ticks=0;self.position=None
        for r,v in dict(DS=0x2000+DS,SS=0x4000,ES=0x3333,BP=0x7777,SI=0x1357,DI=0x2468,BX=0xbeef).items():self.set(r,v)
        self.set('EFLAGS',2|(0x200 if scenario['if'] else 0)|(0x400 if scenario['df'] else 0))
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            off=address-self.get('CS')*16;seg=self.get('CS')-0x2000;self.position=(seg,off)
            if self.get('SS')!=0x4000:raise ValueError('OP title stack segment alias')
            if address==self.code+0xff00:
                f=self.top
                if seg!=CS or self.get('SP')!=f['sp']+2+f['cleanup'] or self.frames or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('OP title terminal frame differs')
                self.stop=True;uc.emu_stop();return
            if seg==CS and off in self.meta['bounds']:
                self.visited.add(off)
                if off in self.meta['entries']:
                    name=self.meta['entries'][off]
                    if not self.visited_entry:self.visited_entry=True
                    else:
                        sp=self.get('SP');ret=int.from_bytes(uc.mem_read(self.stack+sp,2),'little');caller=self.meta['calls'].get(ret)
                        if name!='column' or not caller or caller['destination']!=(CS,off):raise ValueError('OP title native helper caller differs')
                        self.frames.append(dict(ret=ret,sp=sp,saved={r:self.get(r) for r in ('BP','SI','DI','DS')}))
                    self.native[name]+=1
                if off in self.meta['returns'] and self.frames:
                    f=self.frames.pop()
                    if self.get('SP')!=f['sp'] or int.from_bytes(uc.mem_read(self.stack+f['sp'],2),'little')!=f['ret'] or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('OP title native helper return differs')
                if off==0x1635:
                    self.ticks+=1
                    if self.ticks==self.s.get('tick_visits'):
                        self.events.append(dict(name='timer-input',args=[self.ticks,16]));self.external.append((self.data+CLOCK,2,16))
                        uc.mem_write(self.data+CLOCK,(16).to_bytes(2,'little'))
                return
            dest=(seg,off)
            if dest not in MODELS:raise ValueError('OP title native escape/instruction boundary differs')
            name,cleanup,sites=MODELS[dest];sp=self.get('SP');far=seg!=CS;frame=4 if far else 2
            ret=struct.unpack('<'+'H'*(frame//2),uc.mem_read(self.stack+sp,frame));return_cs=ret[1]-0x2000 if far else seg
            caller=self.meta['calls'].get(ret[0])
            if return_cs!=CS or not caller or caller['destination']!=dest or caller['site'] not in sites:raise ValueError('OP title modeled callee caller differs')
            count=6 if name=='snd-load' else cleanup
            words=list(struct.unpack('<'+'H'*(count//2),uc.mem_read(self.stack+sp+frame,count))) if count else []
            event=dict(name=name,args=words)
            if name=='palette':event.update(tone=self.word(TONE),shadow=list(uc.mem_read(self.data+SHADOW,3)),background=list(uc.mem_read(self.data+BG,3)))
            if name in ('super-entry','pi-load','snd-load'):
                offptr,segptr=words[:2]
                if segptr!=0x2000+DS or offptr not in (0x9e2,0x9ec,0x9f1,0x9f9):raise ValueError('OP title filename pointer differs')
            self.events.append(event);self.set('AX',self.s['reply']);self.set('EFLAGS',(self.get('EFLAGS')&~1)|int(self.s['cf']))
            self.set('SP',sp+frame+cleanup);self.set('CS',0x2000+CS);self.set('IP',ret[0])
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            if not 0<=address or address+size>0x100000:raise ValueError('OP title complete store exceeds map')
            if self.position[0]!=CS:raise ValueError('OP title foreign CPU write')
            if self.position[1] in (0x1842,0x184a,0x1852,0x185a):
                if size!=2:raise ValueError('OP title column store width differs')
            elif not ((address==self.data+TONE and size==2) or (address==self.data+CLOCK and size==2) or
                      (size==1 and any(self.data+a<=address<self.data+a+3 for a in (SHADOW,BG)))):
                raise ValueError('OP title complete store span differs')
            self.writes.append((address,size,value&((1<<(size*8))-1)))
        def read(uc,access,address,size,value,user):
            if self.position in ((CS,0x1823),(CS,0x182b),(CS,0x1833),(CS,0x183b)):
                if size!=2:raise ValueError('OP title column read width differs')
                self.reads.append((address,size,int.from_bytes(uc.mem_read(address,size),'little')))
        def port(uc,port,size,value,user):
            if self.position[0]!=CS or self.position[1] not in self.meta['ports'] or size!=1 or port not in (0xa4,0xa6) or value not in (0,1):raise ValueError('OP title unexpected port interface')
            self.events.append(dict(name='out',args=[port,value]))
        def intr(*args):raise ValueError('OP title unexpected interrupt')
        def input_port(*args):raise ValueError('OP title unexpected input port')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_MEM_READ,guard(read))
        self.uc.hook_add(UC_HOOK_INTR,guard(intr));self.uc.hook_add(UC_HOOK_INSN,guard(port),None,1,0,reg.UC_X86_INS_OUT)
        self.uc.hook_add(UC_HOOK_INSN,guard(input_port,0),None,1,0,reg.UC_X86_INS_IN)
    def run(self,name,args=(),budget=400000):
        self.stop=False;self.errors.clear();self.visited_entry=False
        row=next(r for r in self.meta['bodies'] if r['name']==name)
        self.set('CS',0x2000+CS);self.set('SP',0xffd0)
        self.uc.mem_write(self.stack+0xffd0,struct.pack('<'+'H'*(1+len(args)),0xff00,*args))
        self.top=dict(sp=0xffd0,cleanup=row['cleanup'],saved={r:self.get(r) for r in ('BP','SI','DI','DS')})
        self.uc.emu_start(self.code+row['offset'],0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('OP title terminal/budget differs')


def observe(mz,name,s,args=()):
    p=TitleProbe(mz,s);before=bytes(p.uc.mem_read(0,0x100000));spec=TitleSpec(before,p.data,s)
    getattr(spec,name)(*args);p.run(name,args)
    if p.events!=spec.events or p.writes!=spec.writes or p.reads!=spec.reads or p.external!=spec.external or p.native!=spec.native:
        raise ValueError('OP title scalar events/stores/reads/native/external inputs differ: '+name)
    actual=bytes(p.uc.mem_read(0,0x100000))
    if actual[:p.stack]!=spec.memory[:p.stack] or actual[p.stack+65536:]!=spec.memory[p.stack+65536:]:raise ValueError('OP title whole physical memory outside stack differs')
    if bool(p.get('EFLAGS')&0x200)!=s['if'] or bool(p.get('EFLAGS')&0x400)!=s['df']:raise ValueError('OP title IF/DF differs')
    ports=[e for e in p.events if e['name']=='out']
    return dict(function=name,args=list(args),scenario=s,events=[e for e in p.events if e['name']!='out'],native_entries=dict(p.native),
                ordered_events=len(p.events),events_sha256=sha(json.dumps(p.events,separators=(',',':')).encode()),
                port_events=len(ports),port_events_sha256=sha(json.dumps(ports,separators=(',',':')).encode()),
                stores=len(p.writes),stores_sha256=sha(json.dumps(p.writes,separators=(',',':')).encode()),
                reads=len(p.reads),reads_sha256=sha(json.dumps(p.reads,separators=(',',':')).encode()),
                external_inputs=p.external,visited=sorted(p.visited),memory_before_sha256=sha(before),memory_after_sha256=sha(spec.memory))


def matrix(mz):
    rows=[]
    for irq in (False,True):
        for df in (False,True):
            for profile in (0,1):
                s=dict(profile=profile,reply=0xffff if profile else 0,cf=bool(profile),tick_visits=3 if profile else 17,**{'if':irq,'df':df})
                for name in ('intro','fade','expand','shrink'):rows.append(observe(mz,name,s))
                for left in (0,288,392,639,640,0x7fff,0x8000,0xffff):rows.append(observe(mz,'column',s,[left]))
    return rows


def contracts(rows):return [{k:v for k,v in r.items() if k not in ('memory_before_sha256','memory_after_sha256')} for r in rows]


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('OP title parent compiler proof differs')
    parent=json.loads(raw);inputs=dict(parent['inputs']);inputs[PROOF]=sha(raw)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP title parent input differs: '+p)
    for p in ('scripts/review_th03_op_title.py','tests/test_op_title_review.py','scripts/review_th03_decoded_code.py','scripts/inventory_rec98_th03.py'):
        inputs[p]=sha((ROOT/p).read_bytes())
    original=json.loads((ROOT/ORIGINAL).read_bytes());inputs[ORIGINAL]=sha((ROOT/ORIGINAL).read_bytes())
    artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-op');stored=read_verified_artifact(ROOT,artifact)
    target_path=original['observations'][0]['path'];inputs[target_path]=original['inputs'][target_path]
    frozen=frozen_files(REVISION);observations=[];target=parse_mz((ROOT/target_path).read_bytes())
    paths=[target_path]+[str(Path(PROOF).parent/f'round{r["number"]}'/'source/bin/th03/op.exe') for r in parent['rounds']]
    for index,path in enumerate(paths):
        data=(ROOT/path).read_bytes();inputs[path]=sha(data);mz=parse_mz(data)
        if not mz.valid:raise ValueError('OP title invalid MZ')
        meta=analyze(mz.program_image);o=dict(path=path,bodies=meta['bodies'])
        if index:
            round=parent['rounds'][index-1]
            if inputs[path]!=round['products']['bin/th03/op.exe']:raise ValueError('OP title parent product differs')
            tree=Path(path).parents[2];o['source_lineage']={}
            for p in PROVIDERS:
                cp=str(tree/p);raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw)
                if raw!=frozen[p]:raise ValueError('OP title frozen provider differs: '+p)
                o['source_lineage'][p]=dict(frozen_sha256=sha(frozen[p]),cached_sha256=sha(raw))
            cp=str(tree/'obj/th03/op_main.obj');raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw);obj=describe_omf(raw)
            if not obj['valid'] or obj['dependency_timestamp_normalized_sha256']!=round['all_objects']['obj/th03/op_main.obj']:raise ValueError('OP title cold normalized OMF differs')
            o['object']=dict(path=cp,normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'])
            cp=str(tree/'obj/th03/op.map');raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw);text=raw.decode();carriers=code_rows(text,len(mz.program_image))
            carrier=next(c for c in carriers if c['module']=='th03/op_main.cpp' and c['size'])
            if carrier['segment']!=CS or carrier['offset']!=0x14e2 or carrier['size']!=902:raise ValueError('OP title complete carrier differs')
            o['comparisons']={}
            for name,a,z,cleanup in RANGES:
                comp=extent_observation(target,mz,dict(segment=CS,offset=a,start=CS*16+a,size=z));o['comparisons'][name]=comp
                if not comp['ordered_relocations_equal'] or (name!='column' and not comp['raw_slice_equal']):raise ValueError('OP title original raw/ordered comparison differs')
                if name=='column' and comp['raw_slice_equal']:raise ValueError('OP title known column inequality disappeared')
            if meta['semantics']!=analyze(target.program_image)['semantics']:raise ValueError('OP title semantic topology differs; raw inequality remains separate')
        o['cpu']=matrix(mz);visited={a for r in o['cpu'] for a in r['visited']};o['coverage']=dict(instructions=len(meta['bounds']),visited=len(meta['bounds']&visited),unvisited=sorted(meta['bounds']-visited))
        if index and contracts(o['cpu'])!=contracts(observations[0]['cpu']):raise ValueError('OP title target/cold native contracts differ')
        observations.append(o);print('Reviewed',path,len(o['cpu']),'calls',o['coverage'],flush=True)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP title input changed: '+p)
    final=frozen_files(REVISION)
    if any(final[p]!=frozen[p] for p in PROVIDERS) or read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('OP title provider/stored target changed')
    report=dict(kind='th03-op-title-complete-carrier-native-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,
                observations=observations,tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),new_decoded_bytes=902,
                diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,new_build=False,
                notes='Four complete title/menu animation functions808bytes agree unchanged raw/ordered slices; column94 has three raw encoding bytes unequal but same decoded operations and native modeled contracts. Full902 carrier reviewed. Flat writable memory and library/timer reply fixtures record CPU read/write/port attempts only; VRAM banking, ROM writability, real ISR timing, files/resources/heap ownership and canonical storage/fullproduct/source/exact Oracles remain open.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n');print('PASS OP title bounded diagnostics; raw column failure/exact open')


if __name__=='__main__':main()
