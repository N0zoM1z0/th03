#!/usr/bin/env python3
"""Review complete OP menu state machines, native render callbacks and tables."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import version
import itertools
import json
from pathlib import Path
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from inventory_rec98_th03 import frozen_files
from lib.pc98 import parse_mz
from lib.omf import describe_omf
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import Probe, REVISION, sha
from replay_th03_op_score import normalized_contracts

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/th03-op-title/sol-op-title-source-20261006-b/receipt.json'
PROOF_SHA='626257123d424e373e7e1c051b168f305e57e1f3e9fc35a0894e63ca0ef2eea5'
DECODED='.analysis/th03-diet/sol-diet-restoration-20261006-b/op.exe'
DECODED_SHA='efd858aef69a240af3a27c747a5beae150f55f0b41b8afdd1eda1760a759ecc0'
CS,DS=0x990,0xd7f
SEL,QUIT,INMAIN,MAININIT,OPTINIT=0x161,0x162,0x163,0x164,0x165
MAINLOCK,OPTLOCK,INOPT,PUT=0x118a,0x118b,0x118c,0x118e
INPUT,RESIDENT,DISABLED,ACTIVE=0x1aa6,0x2464,0x90,0x5dc
RANGES=[('main_choice',0x5dd,122,4),('option_choice',0x657,330,4),
        ('move',0x7a1,63,4),('main',0x7e0,291,0),('option',0x903,532,0)]
TABLES={0x799:[0x6a2,0x6af,0x6bc,0x6c9],0x8f7:[0x884,0x889,0x8b4,0x8bb,0x8c0,0x8d1]}
INDIRECT={0x69d:('table',0x799),0x87f:('table',0x8f7),0x7ab:('callback',PUT),0x7d8:('callback',PUT)}
CALLS={0x64c:(0,0xfcc),0x671:(0,0xfcc),0x683:(0,0x2254),0x6e6:(0,0xfcc),0x73a:(0,0xfcc),0x78d:(0,0xfcc),
 0x7eb:(0,0x21f4),0x7f7:(CS,0x17db),0x81a:(CS,0x5dd),0x853:(CS,0x7a1),0x861:(CS,0x7a1),
 0x884:(CS,0x117),0x897:(CS,0x2df),0x89a:(CS,0x1708),0x89d:(CS,0x516),0x8a0:(CS,0x1ac3),
 0x8b6:(CS,0x1306),0x8bb:(CS,0x57f),0x90e:(0,0x21f4),0x913:(CS,0x17af),0x931:(CS,0x657),
 0x96a:(CS,0x7a1),0x978:(CS,0x7a1),0x9c8:(0xbeb,0x553),0x9cd:(0xbeb,0x4a),0x9d4:(0xbeb,0x553),
 0x9e7:(0xbeb,0x553),0x9f9:(CS,0x657),0xa1a:(CS,0x657),0xa71:(0xbeb,0x553),0xa76:(0xbeb,0x4a),
 0xa7d:(0xbeb,0x553),0xa90:(0xbeb,0x553),0xaa2:(CS,0x657),0xac9:(CS,0x657)}
MODELS={(0,0xfcc):('gaiji',10,True),(0,0x2254):('text',10,True),(0,0x21f4):('clear',0,True),
 (CS,0x17db):('shrink',0,False),(CS,0x117):('story',0,False),(CS,0x2df):('vs',0,False),
 (CS,0x1708):('fade',0,False),(CS,0x516):('wait',0,False),(CS,0x1ac3):('cdg2',0,False),
 (CS,0x1306):('music',0,True),(CS,0x57f):('score',0,False),(CS,0x17af):('expand',0,False),
 (0xbeb,0x553):('kaja',2,True),(0xbeb,0x4a):('determine',0,True)}
PROVIDERS=['th03/op_01.cpp','th02/op/menu.hpp','th01/rank.h','th03/resident.hpp',
 'th03/hardware/input.h','th03/gaiji/gaiji.h','th03/op/m_main.hpp','th03/op/m_select.hpp',
 'th03/common.h','th03/snd/snd.h','libs/master.lib/master.hpp','libs/master.lib/pc98_gfx.hpp',
 'th02/gaiji/str.hpp','th01/math/clamp.hpp']


def analyze(image):
    d=Cs(CS_ARCH_X86,CS_MODE_16);d.detail=True
    bounds=set();returns={};entries={};calls={};rows=[];table_bytes={}
    for at,values in TABLES.items():
        raw=image[CS*16+at:CS*16+at+2*len(values)]
        if raw!=struct.pack('<'+'H'*len(values),*values) or image[CS*16+at-1]!=0:
            raise ValueError('OP menu complete table/pad differs')
        table_bytes[at]=raw.hex()
    for name,a,z,cleanup in RANGES:
        end={0x657:0x798,0x7e0:0x8f6}.get(a,a+z)
        body=image[CS*16+a:CS*16+a+z];ins=list(d.disasm(body[:end-a],a));local={i.address for i in ins}
        if len(body)!=z or sum(i.size for i in ins)!=end-a or (ins[-1].mnemonic,ins[-1].op_str)!=('ret',str(cleanup) if cleanup else ''):
            raise ValueError('OP menu complete native return differs')
        entries[a]=name;bounds.update(local);edges=[]
        for i in ins:
            if i.mnemonic in ('ret','retf'):
                if (i.mnemonic,i.op_str)!=('ret',str(cleanup) if cleanup else ''):raise ValueError('OP menu interior return differs')
                returns[i.address]=cleanup
            if i.mnemonic in ('in','out','int','iret'):raise ValueError('OP menu unexpected device instruction')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
            if i.address in INDIRECT:
                kind,at=INDIRECT[i.address]
                expected='word ptr cs:[bx + '+hex(at)+']' if kind=='table' else 'word ptr ['+hex(at)+']'
                if i.op_str!=expected or i.mnemonic!=('jmp' if kind=='table' else 'call'):
                    raise ValueError('OP menu indirect operand differs')
                if kind=='table' and any(v not in local for v in TABLES[at]):raise ValueError('OP menu table enters operand/neighbor')
                if kind=='callback':calls[i.address+i.size]=dict(site=i.address,destination=None)
                edges.append(dict(site=i.address,kind=kind,operand=at));continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('OP menu unknown indirect edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (CS,i.operands[0].imm)
            if i.mnemonic in ('call','lcall'):
                if CALLS.get(i.address)!=dest:raise ValueError('OP menu unknown caller destination')
                calls[i.address+i.size]=dict(site=i.address,destination=dest)
            elif i.mnemonic=='ljmp' or dest[1] not in local:raise ValueError('OP menu branch enters operand/neighbor')
            edges.append(dict(site=i.address,kind=i.mnemonic,destination=list(dest)))
        rows.append(dict(name=name,offset=a,size=z,cleanup=cleanup,sha256=sha(body),instructions=len(ins),edges=edges))
    if set(CALLS)!={c['site'] for c in calls.values() if c['destination'] is not None}:raise ValueError('OP menu complete call closure differs')
    return dict(bounds=bounds,entries=entries,returns=returns,calls=calls,bodies=rows,tables=table_bytes)


class MenuSpec:
    """Scalar state/event model independent of native instruction decoding."""
    def __init__(self,before,data,resident,s):
        self.memory=bytearray(before);self.data=data;self.resident=resident;self.s=s
        self.events=[];self.writes=[];self.external=[];self.native=Counter()
    def get(self,a,z=1):return int.from_bytes(self.memory[a:a+z],'little')
    def put(self,a,z,v,external=False):
        v&=(1<<(8*z))-1;self.memory[a:a+z]=v.to_bytes(z,'little')
        (self.external if external else self.writes).append((a,z,v))
    def dg(self,a):return self.get(self.data+a)
    def setdg(self,a,v,z=1):self.put(self.data+a,z,v)
    def signed(self,v):return v-256 if v>127 else v
    def call(self,name,args=()):
        event=dict(name=name,args=list(args))
        if name in ('gaiji','text'):
            off,seg=args[1:3];raw=self.memory[seg*16+off:seg*16+off+32];end=raw.index(0)
            event['string']=bytes(raw[:end+1]).hex()
        self.events.append(event)
        if name=='determine':self.put(self.data+ACTIVE,1,self.s['mode_active'],True)
        if name in ('story','vs','music','score'):
            self.put(self.data+INPUT,2,self.s['callee_input'],True)
    def draw(self,which,sel,atrb):
        self.native[which+'_choice']+=1
        def gaiji(x,y,ptr):self.call('gaiji',[atrb,ptr,0x2000+DS,y,x])
        # Native Pascal args are [atrb, offset, segment, y, x].
        if which=='main':
            if 0<=sel<6:gaiji([25,23,22,24,25,26][sel],17+sel,[0xdc,0xe0,0xe7,0xef,0xf5,0xfa][sel])
            return
        if sel==0:
            gaiji(25,17,0xfe);self.call('text',[0xe1,0x175,0x2000+DS,17,37])
            rank=self.get(self.resident+0xb)
            if rank<4:gaiji([38,37,38,37][rank],17,[0x113,0x117,0x11c,0x120][rank])
        elif sel==1:
            gaiji(25,19,0x102);bgm=self.get(self.resident+0x15)
            if bgm<3:gaiji(35,19,[0x125,0x12d,0x135][bgm])
        elif sel==2:
            gaiji(23,21,0x107);key=self.get(self.resident+0x16)
            if key<3:gaiji(37,21,[0x14c,0x153,0x15a][key])
        elif sel==3:gaiji(32,22,0xfa)
    def main_choice(self,args):self.draw('main',self.signed_word(args[1]),args[0])
    def option_choice(self,args):self.draw('option',self.signed_word(args[1]),args[0])
    @staticmethod
    def signed_word(v):return v-65536 if v>32767 else v
    def move(self,args):
        self.native['move']+=1;direction=self.signed(args[0]&255);maximum=self.signed(args[1]&255)
        which='main' if self.get(self.data+PUT,2)==0x5dd else 'option'
        self.draw(which,self.signed(self.dg(SEL)),1);self.setdg(SEL,self.dg(SEL)+direction)
        if self.signed(self.dg(SEL))<0:self.setdg(SEL,maximum)
        if self.signed(self.dg(SEL))>maximum:self.setdg(SEL,0)
        self.draw(which,self.signed(self.dg(SEL)),0xe1)
    def main(self,args):
        self.native['main']+=1
        if not self.dg(MAININIT):
            self.call('clear')
            if not self.dg(INMAIN):self.call('shrink')
            self.setdg(INMAIN,0);self.setdg(MAINLOCK,0)
            for i in range(6):self.draw('main',i,0xe1 if self.signed(self.dg(SEL))==i else 1)
            self.setdg(PUT,0x5dd,2);self.setdg(MAININIT,1);self.setdg(MAINLOCK,0)
        inp=self.get(self.data+INPUT,2)
        if inp==0:self.setdg(MAINLOCK,1)
        if not self.dg(MAINLOCK):return
        if inp&1:self.move([0xffff,5])
        if inp&2:self.move([1,5])
        if inp&(0x2000|0x20):
            sel=self.dg(SEL)
            if sel in (0,1,2):
                if sel==1:
                    self.put(self.resident+0xc,1,1);self.put(self.resident+0xd,1,1)
                self.call(['story','vs','music'][sel]);self.call('fade');self.call('wait');self.call('cdg2')
                self.setdg(MAININIT,0);self.setdg(MAINLOCK,0);self.setdg(INMAIN,1);return
            if sel==3:self.call('score')
            if sel==4:self.setdg(MAININIT,0);self.setdg(INOPT,1);self.setdg(SEL,0)
            if sel==5:self.setdg(MAININIT,0);self.setdg(QUIT,1)
        inp=self.get(self.data+INPUT,2)
        if inp&0x1000:self.setdg(QUIT,1)
        if inp:self.setdg(MAINLOCK,0)
    def option(self,args):
        self.native['option']+=1
        if not self.dg(OPTINIT):
            self.call('clear');self.call('expand');self.setdg(OPTLOCK,0)
            for i in range(4):self.draw('option',i,0xe1 if self.signed(self.dg(SEL))==i else 1)
            self.setdg(PUT,0x657,2);self.setdg(OPTINIT,1);self.setdg(OPTLOCK,0)
        inp=self.get(self.data+INPUT,2)
        if inp==0:self.setdg(OPTLOCK,1)
        if not self.dg(OPTLOCK):return
        if inp&1:self.move([0xffff,3])
        if inp&2:self.move([1,3])
        for bit,direction in ((8,1),(4,-1)):
            if not(inp&bit):continue
            sel=self.dg(SEL)
            if sel in (0,2):
                field,maximum=(0xb,3) if sel==0 else (0x16,2);v=self.get(self.resident+field)
                if direction==1:
                    self.put(self.resident+field,1,v+1)
                    if self.get(self.resident+field)>maximum:self.put(self.resident+field,1,0)
                elif v==0:self.put(self.resident+field,1,maximum)
                else:self.put(self.resident+field,1,v-1)
            elif sel==1 and not self.dg(DISABLED):
                if self.get(self.resident+0x15)==0:
                    self.put(self.resident+0x15,1,1);self.call('kaja',[256]);self.call('determine');self.call('kaja',[0])
                else:
                    self.put(self.resident+0x15,1,0);self.call('kaja',[256]);self.setdg(ACTIVE,0)
                self.draw('option',self.signed(sel),0xe1)
            self.draw('option',self.signed(sel),0xe1)
        def exit_option():self.setdg(OPTINIT,0);self.setdg(SEL,4);self.setdg(INOPT,0)
        if inp&(0x2000|0x20) and self.dg(SEL)==3:exit_option()
        if inp&0x1000:exit_option()
        if inp:self.setdg(OPTLOCK,0)


class MenuProbe(Probe):
    def __init__(self,mz,s):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,(struct.unpack_from('<H',image,at)[0]+0x2000)&65535)
        self.uc.mem_write(0x20000,bytes(image));self.code=(0x2000+CS)*16;self.data=(0x2000+DS)*16;self.stack=0x40000
        self.resident=0x60031;self.uc.mem_write(0x60000,bytes((i*17+31)&255 for i in range(256)))
        self.uc.mem_write(self.data+RESIDENT,struct.pack('<HH',0x31,0x6000))
        for a,v in ((SEL,s['sel']),(QUIT,s['quit']),(INMAIN,s['inmain']),(MAININIT,s['maininit']),
                    (OPTINIT,s['optinit']),(MAINLOCK,s['mainlock']),(OPTLOCK,s['optlock']),
                    (INOPT,s['inopt']),(DISABLED,s['disabled']),(ACTIVE,s['active'])):
            self.uc.mem_write(self.data+a,bytes([v&255]))
        for a,k in ((0xb,'rank'),(0x15,'bgm'),(0x16,'key')):self.uc.mem_write(self.resident+a,bytes([s[k]]))
        self.uc.mem_write(self.data+PUT,struct.pack('<H',s['put']));self.uc.mem_write(self.data+INPUT,struct.pack('<H',s['input']))
        self.s=s;self.meta=analyze(mz.program_image);self.events=[];self.writes=[];self.external=[];self.native=Counter()
        self.visited=set();self.frames=[];self.top=None;self.errors=[];self.stop=False;self.position=None
        for r,v in dict(DS=0x2000+DS,SS=0x4000,ES=0x3333,BP=0x7777,SI=0x1357,DI=0x2468,BX=0xbeef).items():self.set(r,v)
        self.set('EFLAGS',2|(0x200 if s['if'] else 0)|(0x400 if s['df'] else 0))
        def guard(fn):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop()
            return invoke
        def code(uc,address,size,user):
            seg=self.get('CS')-0x2000;off=address-self.get('CS')*16;self.position=(seg,off)
            if self.get('SS')!=0x4000:raise ValueError('OP menu stack segment alias')
            if address==self.code+0xff00:
                f=self.top
                if seg!=CS or self.get('SP')!=f['sp']+2+f['cleanup'] or self.frames or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('OP menu terminal frame differs')
                self.stop=True;uc.emu_stop();return
            if self.frames and (seg,off)==(CS,self.frames[-1]['ret']):
                f=self.frames.pop()
                if self.get('SP')!=f['sp']+2+f['cleanup'] or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('OP menu native callback return differs')
            if seg==CS and off in self.meta['bounds']:
                self.visited.add(off)
                if off in (0x7ab,0x7d8) and self.word(PUT) not in (0x5dd,0x657):raise ValueError('OP menu callback target differs')
                if off in self.meta['entries']:
                    name=self.meta['entries'][off];self.native[name]+=1
                    if self.entered:
                        sp=self.get('SP');ret=int.from_bytes(uc.mem_read(self.stack+sp,2),'little');caller=self.meta['calls'].get(ret)
                        dest=caller['destination'] if caller else 'missing'
                        if dest is None:
                            ptr=self.word(PUT)
                            if ptr!=off or off not in (0x5dd,0x657):raise ValueError('OP menu callback target differs')
                        elif dest!=(CS,off):raise ValueError('OP menu native caller differs')
                        cleanup=next(r[3] for r in RANGES if r[1]==off)
                        self.frames.append(dict(ret=ret,sp=sp,cleanup=cleanup,saved={r:self.get(r) for r in ('BP','SI','DI','DS')}))
                    self.entered=True
                if off in self.meta['returns']:
                    f=self.frames[-1] if self.frames else self.top;sp=self.get('SP')
                    if sp!=f['sp'] or int.from_bytes(uc.mem_read(self.stack+sp,2),'little')!=f['ret'] or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('OP menu native return stack differs')
                return
            dest=(seg,off)
            if dest not in MODELS:raise ValueError('OP menu escape/operand boundary differs')
            name,cleanup,far=MODELS[dest];sp=self.get('SP');width=4 if far else 2
            words=struct.unpack('<'+'H'*(width//2),uc.mem_read(self.stack+sp,width));ret=words[0];retcs=words[1] if far else self.get('CS')
            caller=self.meta['calls'].get(ret)
            if retcs!=0x2000+CS or not caller or caller['destination']!=dest:raise ValueError('OP menu foreign caller frame differs')
            if name=='music' and caller['site']!=0x8b6:raise ValueError('OP menu music pushed-CS call differs')
            args=list(struct.unpack('<'+'H'*(cleanup//2),uc.mem_read(self.stack+sp+width,cleanup))) if cleanup else []
            event=dict(name=name,args=args)
            if name in ('gaiji','text'):
                if args[2]!=0x2000+DS:raise ValueError('OP menu string segment differs')
                raw=bytes(uc.mem_read(args[2]*16+args[1],32));event['string']=raw[:raw.index(0)+1].hex()
            self.events.append(event)
            def external(a,z,v):uc.mem_write(a,v.to_bytes(z,'little'));self.external.append((a,z,v))
            if name=='determine':external(self.data+ACTIVE,1,s['mode_active'])
            if name in ('story','vs','music','score'):external(self.data+INPUT,2,s['callee_input'])
            self.set('AX',s['reply']);self.set('EFLAGS',(self.get('EFLAGS')&~1)|s['cf'])
            self.set('SP',sp+width+cleanup);self.set('CS',retcs);self.set('IP',ret)
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            allowed=(size==1 and (address in [self.data+a for a in (SEL,QUIT,INMAIN,MAININIT,OPTINIT,MAINLOCK,OPTLOCK,INOPT,ACTIVE)] or
                                  address in [self.resident+a for a in (0xb,0xc,0xd,0x15,0x16)])) or (size==2 and address==self.data+PUT)
            if not allowed or self.position[0]!=CS:raise ValueError('OP menu complete store span differs')
            self.writes.append((address,size,value&((1<<(size*8))-1)))
        def intr(*args):raise ValueError('OP menu unexpected interrupt')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
    def run(self,name,args=(),budget=10000):
        self.stop=False;self.errors.clear();self.entered=False
        row=next(r for r in self.meta['bodies'] if r['name']==name)
        self.set('CS',0x2000+CS);self.set('SP',0xffd0)
        self.uc.mem_write(self.stack+0xffd0,struct.pack('<'+'H'*(1+len(args)),0xff00,*args))
        self.top=dict(sp=0xffd0,ret=0xff00,cleanup=row['cleanup'],saved={r:self.get(r) for r in ('BP','SI','DI','DS')})
        self.uc.emu_start(self.code+row['offset'],0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('OP menu terminal/budget differs')


def scenario(**kw):
    s=dict(sel=0,quit=0,inmain=1,maininit=1,optinit=1,mainlock=1,optlock=1,inopt=1,disabled=0,active=0x7e,
           put=0x5dd,input=0,rank=0,bgm=0,key=0,reply=0,cf=0,callee_input=0x1000,mode_active=0xfe,**{'if':True,'df':False})
    s.update(kw);return s


def observe(mz,name,s,args=(),sequence=None):
    p=MenuProbe(mz,s);before=bytes(p.uc.mem_read(0,0x100000));spec=MenuSpec(before,p.data,p.resident,s)
    for n,a,inp in sequence or [(name,args,None)]:
        if inp is not None:
            p.uc.mem_write(p.data+INPUT,struct.pack('<H',inp));spec.memory[p.data+INPUT:p.data+INPUT+2]=struct.pack('<H',inp)
        getattr(spec,n)(a);p.run(n,a)
    if p.events!=spec.events or p.writes!=spec.writes or p.external!=spec.external or p.native!=spec.native:
        raise ValueError('OP menu independent scalar events/stores/native/external differ: '+str((name,s,args)))
    actual=bytes(p.uc.mem_read(0,0x100000))
    if actual[:p.stack]!=spec.memory[:p.stack] or actual[p.stack+65536:]!=spec.memory[p.stack+65536:]:raise ValueError('OP menu whole physical preservation differs')
    if bool(p.get('EFLAGS')&0x200)!=s['if'] or bool(p.get('EFLAGS')&0x400)!=s['df']:raise ValueError('OP menu IF/DF differs')
    def digest(x):return sha(json.dumps(x,separators=(',',':')).encode())
    return dict(function=name,args=list(args),sequence=sequence,scenario=s,events=p.events,native_entries=dict(p.native),stores=len(p.writes),
                stores_sha256=digest(p.writes),external_inputs=p.external,visited=sorted(p.visited),memory_before_sha256=sha(before),memory_after_sha256=sha(spec.memory))


def matrix(mz):
    rows=[];bits=(1,2,4,8,0x20,0x1000,0x2000,0x8000)
    for name,count,ptr in (('main',6,0x5dd),('option',4,0x657)):
        for sel in range(count):
            for mask in range(256):
                inp=sum(b for i,b in enumerate(bits) if mask&(1<<i))
                rows.append(observe(mz,name,scenario(sel=sel,input=inp,put=ptr,bgm=sel%3,rank=sel%4,key=sel%3)))
    for irq,df in itertools.product((False,True),repeat=2):
        for name,ptr in (('main',0x5dd),('option',0x657)):
            for sel,field in itertools.product((0,1,2,3,4,5,127,128,255),(0,1,2,3,4,255)):
                s=scenario(sel=sel,put=ptr,rank=field,bgm=field,key=field,input=0xc,disabled=0xff if field==4 else 0,reply=0xffff,cf=1,**{'if':irq,'df':df})
                rows.append(observe(mz,name,s))
        for name,ptr,lockkey,initkey in (('main',0x5dd,'mainlock','maininit'),('option',0x657,'optlock','optinit')):
            for initialized,allowed,inmain in itertools.product((0,1),(0,0xff),(0,1)):
                s=scenario(put=ptr,inmain=inmain,input=0x302f,**{lockkey:allowed,initkey:initialized,'if':irq,'df':df})
                seq=[(name,[],0x302f),(name,[],0x302f),(name,[],0),(name,[],8),(name,[],8),(name,[],0),(name,[],0x1000)]
                rows.append(observe(mz,name,s,sequence=seq))
        for sel,field in itertools.product((0,1,2,3,4,5,6,0xffff),(0,1,2,3,4,255)):
            s=scenario(rank=field,bgm=field,key=field,**{'if':irq,'df':df})
            for name in ('main_choice','option_choice'):rows.append(observe(mz,name,s,[0xf3a5,sel]))
        for ptr,sel,direction,maximum in itertools.product((0x5dd,0x657),(0,3,5,127,128,255),(0,1,0xffff,0x7f,0x80),(3,5,0xff)):
            rows.append(observe(mz,'move',scenario(sel=sel,put=ptr,**{'if':irq,'df':df}),[direction,maximum]))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('OP menu parent compiler proof differs')
    parent=json.loads(raw);inputs=dict(parent['inputs']);inputs[PROOF]=sha(raw);inputs[DECODED]=DECODED_SHA
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP menu parent input differs: '+p)
    for p in ('scripts/review_th03_op_menu.py','tests/test_op_menu_review.py','scripts/review_th03_decoded_code.py','scripts/inventory_rec98_th03.py',
              'scripts/replay_th03_op_score.py','scripts/review_th03_mainl_cutscene.py'):
        inputs[p]=sha((ROOT/p).read_bytes())
    artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-op');stored=read_verified_artifact(ROOT,artifact)
    frozen=frozen_files(REVISION);target=parse_mz((ROOT/DECODED).read_bytes());observations=[]
    paths=[DECODED]+[str(Path(PROOF).parent/f'round{r["number"]}'/'source/bin/th03/op.exe') for r in parent['rounds']]
    for index,path in enumerate(paths):
        raw=(ROOT/path).read_bytes();inputs[path]=sha(raw);mz=parse_mz(raw)
        if not mz.valid:raise ValueError('OP menu invalid decoded MZ')
        meta=analyze(mz.program_image);o=dict(path=path,bodies=meta['bodies'],tables=meta['tables'])
        if index:
            round=parent['rounds'][index-1]
            if inputs[path]!=round['products']['bin/th03/op.exe']:raise ValueError('OP menu parent product differs')
            tree=Path(path).parents[2];o['source_lineage']={}
            for p in PROVIDERS:
                cp=str(tree/p);raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw)
                if raw!=frozen[p]:raise ValueError('OP menu frozen provider differs: '+p)
                o['source_lineage'][p]=sha(raw)
            cp=str(tree/'obj/th03/op_01.obj');raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw);obj=describe_omf(raw)
            if not obj['valid'] or obj['dependency_timestamp_normalized_sha256']!=round['all_objects']['obj/th03/op_01.obj']:raise ValueError('OP menu OMF differs')
            o['object']=dict(path=cp,normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'])
            cp=str(tree/'obj/th03/op.map');raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw)
            carrier=next(c for c in code_rows(raw.decode(),len(mz.program_image)) if c['module']=='th03/op_01.cpp' and c['size'])
            if (carrier['segment'],carrier['offset'],carrier['size'])!=(CS,8,3094):raise ValueError('OP menu original carrier differs')
            o['comparisons']={}
            for name,a,z,c in RANGES:
                comp=extent_observation(target,mz,dict(segment=CS,offset=a,start=CS*16+a,size=z));o['comparisons'][name]=comp
                if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('OP menu raw/ordered inequality')
            if mz.program_image[DS*16+0xdc:DS*16+0x166]!=target.program_image[DS*16+0xdc:DS*16+0x166]:raise ValueError('OP menu original labels/static bytes differ')
        o['cpu']=matrix(mz);visited={a for r in o['cpu'] for a in r['visited']}
        o['coverage']=dict(instructions=len(meta['bounds']),visited=len(meta['bounds']&visited),unvisited=sorted(meta['bounds']-visited))
        if o['coverage']['unvisited']:raise ValueError('OP menu native coverage incomplete')
        if index and normalized_contracts(o['cpu'])!=normalized_contracts(observations[0]['cpu']):raise ValueError('OP menu target/cold native contracts differ')
        observations.append(o);print('Reviewed',path,len(o['cpu']),'calls',o['coverage'],flush=True)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP menu input changed: '+p)
    final=frozen_files(REVISION)
    if any(final[p]!=frozen[p] for p in PROVIDERS) or read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('OP menu frozen/canonical target changed')
    report=dict(kind='th03-op-menu-complete-callers-native-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,observations=observations,
                tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),new_decoded_bytes=1338,diagnostic_checks_pass=True,
                source_acceptance=False,exact_acceptance=False,new_build=False,
                notes='Five complete functions including both original indirect switch tables, native Pascal renderer callbacks, signed-byte movement, caller frame/cleanup and ordered physical stores checked. Foreign screen transitions, sound driver and text rendering use explicit reply fixtures; original startup/story/VS/demo/score caller/resource/heap/DOS/device behavior and canonical stored/full-product/exact Oracles remain open.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n');print('PASS OP menu diagnostics; exact open')


if __name__=='__main__':main()
