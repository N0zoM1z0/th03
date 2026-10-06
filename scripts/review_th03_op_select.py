#!/usr/bin/env python3
"""Review the complete OP character-selection carrier, preserving native state."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import version
import itertools
import json
from pathlib import Path
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM
from inventory_rec98_th03 import frozen_files
from lib.pc98 import parse_mz
from lib.omf import describe_omf
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import Probe, REVISION, sha
from replay_th03_op_score import normalized_contracts
from review_th03_op_score import ScoreSpec, encrypt, sealed, sample, SIZE, HI, CALLS as SCORE_CALLS

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/th03-op-music/sol-op-music-source-20261006/receipt.json'
PROOF_SHA='4f83a27f4c10adafdedfb1baee615c55153169ea549a82b55aeb1a69f8c24d25'
DECODED='.analysis/th03-diet/sol-diet-restoration-20261006-b/op.exe'
CS,DS=0x990,0xd7f
# Full function, near/far return and Pascal cleanup; score/random/polar context
# remains separately owned. The carrier has19functions, not18.
RANGES=[('load',CS,0x19f2,107,2,False),('unlock',CS,0x1a5d,48,0,False),
 ('cdg1',CS,0x1a8d,54,0,False),('cdg2',CS,0x1ac3,44,0,False),('cdg3',CS,0x1aef,53,0,False),
 ('init',CS,0x1b24,179,0,False),('free',CS,0x1bd7,28,0,False),('vs_pics',CS,0x1bf3,66,0,False),
 ('storypics',CS,0x1c35,48,0,False),('stats',CS,0x1c65,209,0,False),('names',CS,0x1d36,58,0,False),
 ('extras',CS,0x1d70,80,0,False),('curve',CS,0x1dc0,135,10,False),('curves',CS,0x1e47,351,0,False),
 ('cursor',CS,0x1fa6,98,4,False),('update',CS,0x2008,384,4,False),('versus',CS,0x2188,407,0,False),
 ('cpu',CS,0x231f,379,0,False),('story',CS,0x249a,285,0,False),
 ('encode',CS,0x1868,165,2,False),('decode',CS,0x190d,60,0,False),
 ('recreate',CS,0x1949,127,0,False),('sum',CS,0x19c8,42,0,False),
 ('irand',0,0x1d12,42,0,True),('polar',0xbeb,0x155,26,0,True)]
MODELS={(0xbeb,0xcb8):('hflip',0,0),(0xbeb,0x5da):('cdg-load',8,8),
 (0xbeb,0x7d0):('cdg-all-noalpha',6,6),(0xbeb,0x664):('cdg-load-noalpha',8,8),
 (0xbeb,0x553):('kaja',2,2),(0xbeb,0xa2):('snd-load',6,0),
 (0,0x21f4):('text-clear',0,0),(0,0x269a):('super-free',0,0),(0,0x27fe):('bfnt',4,4),
 (0,0x114c):('graph-clear',0,0),(0,0x1d3c):('palette-entry',4,4),(0,0x1aa4):('palette',0,0),
 (0xbeb,0x7ec):('cdg-free',2,2),(0xbeb,0x170):('cdg-put',6,6),(0xbeb,0x224):('cdg-hflip',6,6),
 (0xbeb,0xc46):('cdg-noalpha',6,6),(0,0xec6):('grcg-color',4,4),(0,0xb02):('boxfill',8,8),
 (0,0xef0):('grcg-off',0,0),(0,0x28d8):('super',6,6),(0,0xe82):('pset',4,4),
 (0,0x1232):('gaiji',12,12),(0,0x23e6):('white-in',2,2),(0xbeb,0x2ee):('frame',2,2),
 (0xbeb,0x304):('input-reset',0,0),(0,0xbd2):('boxfill8',8,8)}
for off in (0xad6,0xafa,0xb04,0xb26):MODELS[(0xbeb,off)]=('input-'+format(off,'x'),0,0)
for off,(name,count) in {0x8d8:('exist',4),0x898:('create',4),0x888:('close',0),0x9a8:('open',4),
                       0x9e4:('seek',6),0x8f4:('read',6),0x7c8:('append',4),0xa26:('write',6)}.items():
    MODELS[(0,off)]=(name,count,count)
CALLS=dict(SCORE_CALLS)
for dest,sites in {
 (CS,0x19f2):[0x1a6b],(0xbeb,0xcb8):[0x1a91],(0xbeb,0x5da):[0x1aaa,0x1ace,0x1afc,0x1b16,0x1bb6,0x20da,0x2161],
 (0xbeb,0x7d0):[0x1abb],(0xbeb,0x664):[0x1adb,0x1ae8],(0xbeb,0x553):[0x1b31,0x1b47,0x2279,0x23d9,0x2518],
 (0xbeb,0xa2):[0x1b3d],(0,0x21f4):[0x1b5f,0x218e,0x226e,0x2290,0x23ce,0x2402,0x250d,0x2528],
 (0,0x269a):[0x1b64,0x1beb],(0,0x27fe):[0x1b6d],(0,0x114c):[0x1b78,0x1b83,0x2263,0x23c3,0x2502],
 (0,0x1d3c):[0x1b97],(0,0x1aa4):[0x1b9c,0x22ab,0x241d,0x2543],(CS,0x1a5d):[0x1bce],
 (0xbeb,0x7ec):[0x1be0],(0xbeb,0x170):[0x1c0f,0x1c51,0x1c5e],(0xbeb,0x224):[0x1c2e],
 (0xbeb,0xc46):[0x1c73,0x1c8b,0x1d7b,0x1d8e,0x1da6,0x1db9],
 (0,0xec6):[0x1c96,0x1e7c,0x1eb6,0x1f2f,0x22f0,0x2462,0x2588],(0,0xb02):[0x1cbe,0x1cff],
 (0,0xef0):[0x1d2d,0x1f95,0x2303,0x2475,0x259b],(0,0x28d8):[0x1d4b,0x1d5a],
 (0xbeb,0x155):[0x1df4,0x1e24],(0,0xe82):[0x1e33],(CS,0x1dc0):[0x1e92,0x1ead,0x1ef5,0x1f1e,0x1f5d,0x1f86],
 (0,0x1232):[0x1fde,0x1ffd],(0,0x23e6):[0x2097,0x211e],(CS,0x1b24):[0x218b,0x2323,0x249d],
 (0xbeb,0x2ee):[0x21fb],(CS,0x1e47):[0x2206,0x2369,0x24c1],(CS,0x1bf3):[0x2209,0x236c],
 (CS,0x1c35):[0x24c4],(CS,0x1c65):[0x220c,0x236f,0x24c7],(CS,0x1d36):[0x220f,0x2372,0x24ca],
 (CS,0x1d70):[0x2212,0x2375,0x24cd],(CS,0x1fa6):[0x2225,0x2238,0x2391,0x23ab,0x24e0],
 (0xbeb,0x304):[0x223b,0x2378,0x24e3],(CS,0x2008):[0x224a,0x2253,0x23b3,0x24f2],
 (CS,0x1bd7):[0x2273,0x2318,0x23d3,0x2492,0x2512,0x25b0],(0,0xbd2):[0x22fe,0x2470,0x2596]
 }.items():
    for site in sites:CALLS[site]=dest
INDIRECT={0x2240,0x237d,0x24e8}
CLOCK_SITES={0x1bc1:30,0x22b7:3,0x2429:3,0x254f:3}
PROVIDERS=['th03/op_sel.cpp','th03/op/m_select.cpp','th03/op/m_select.hpp','decomp.hpp',
 'libs/master.lib/master.hpp','libs/master.lib/pc98_gfx.hpp','th01/math/clamp.hpp','th02/v_colors.hpp',
 'th02/hardware/frmdelay.h','th02/formats/bfnt.h','th03/common.h','th03/resident.hpp','th03/formats/cdg.h',
 'th03/formats/hfliplut.h','th03/formats/scoredat.hpp','th03/gaiji/gaiji.h','th03/hardware/input.h',
 'th03/math/polar.hpp','th03/shiftjis/fns.hpp','th03/snd/snd.h','th03/sprites/op_cdg.hpp',
 'th03/formats/score_ld.cpp','th03/formats/score_es.cpp','th03/formats/scoredat.cpp',
 'th03/op_02.cpp','th03/scoredat.cpp','th03/playchar.hpp','libs/master.lib/random.asm',
 'libs/master.lib/rand[data].asm','th03/math/polar.cpp']


def analyze(image):
    d=Cs(CS_ARCH_X86,CS_MODE_16);d.detail=True
    bounds=set();entries={};returns={};calls={};bodies=[];found=set();indirect=set()
    for name,seg,a,z,cleanup,far in RANGES:
        body=image[seg*16+a:seg*16+a+z];ins=list(d.disasm(body,a));local={i.address for i in ins}
        expected=('retf' if far else 'ret',cleanup)
        signature=lambda i:(i.mnemonic,int(i.op_str,0) if i.op_str else 0)
        if len(body)!=z or sum(i.size for i in ins)!=z or signature(ins[-1])!=expected:raise ValueError('Select complete body/return differs: '+name)
        entries[(seg,a)]=name;bounds.update((seg,i.address) for i in ins);edges=[]
        for i in ins:
            if i.mnemonic in ('ret','retf'):
                if signature(i)!=expected:raise ValueError('Select interior return differs')
                returns[(seg,i.address)]=cleanup
            if i.mnemonic in ('int','in','iret'):raise ValueError('Select unexpected device instruction')
            if not(i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
            if seg==CS and i.address in INDIRECT:
                if i.mnemonic!='lcall' or len(i.operands)!=1 or i.operands[0].type!=X86_OP_MEM or i.operands[0].mem.disp!=0x246e or i.operands[0].mem.base or i.operands[0].mem.index:
                    raise ValueError('Select indirect operand differs')
                dest=None;indirect.add(i.address)
            else:
                if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('Select unknown indirect edge')
                dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (seg,i.operands[0].imm)
            if i.mnemonic in ('call','lcall'):
                if dest is not None:
                    if seg!=CS or CALLS.get(i.address)!=dest:raise ValueError('Select unknown caller '+hex(i.address))
                    found.add(i.address)
                calls[(seg,i.address+i.size)]=dict(site=i.address,destination=dest)
            elif i.mnemonic=='ljmp' or dest[1] not in local:raise ValueError('Select branch enters operand/neighbor')
            edges.append(dict(site=i.address,kind=i.mnemonic,destination=list(dest) if dest else None))
        bodies.append(dict(name=name,segment=seg,offset=a,size=z,cleanup=cleanup,far=far,instructions=len(ins),sha256=sha(body),edges=edges))
    if found!=set(CALLS) or indirect!=INDIRECT:raise ValueError('Select complete call closure differs')
    if any(v['destination'] and v['destination'] not in entries and v['destination'] not in MODELS for v in calls.values()):raise ValueError('Select missing callee model')
    return dict(bounds=bounds,entries=entries,returns=returns,calls=calls,bodies=bodies)


def signed(v):return (v&65535)-65536 if v&32768 else v&65535

def byte_signed(v):return (v&255)-256 if v&128 else v&255

def trunc(n,d):return (abs(n)//d)*(-1 if n<0 else 1)


class ScoreAdapter(ScoreSpec):
    """Reuse the independently reviewed scalar format, with shared physical stores."""
    def __init__(self,parent,rank):
        self.parent=parent
        super().__init__(parent.memory[parent.data+HI:parent.data+HI+SIZE],parent.dg(0x312,4),
                         parent.s['ranks'][rank%4],parent.data,[parent.dg(0xa02,2),0x2000+DS])
        self.native=parent.native
    def put(self,offset,value,width=1):
        super().put(offset,value,width);self.parent.store(self.base+HI+offset,width,value)
    def random(self):return self.parent.invoke('irand')
    def event(self,name,args,**extra):self.parent.call(name,args,extra)


class SelectSpec:
    """Independent scalar16-bit state. Foreign device/file replies are fixtures."""
    def __init__(self,before,data,s):
        self.memory=bytearray(before);self.data=data;self.s=s;self.events=[];self.writes=[];self.external=[]
        self.native=Counter();self.inputs=0;self.rank=0;self.polls=Counter();self.replies=[]
    def get(self,a,z=1):return int.from_bytes(self.memory[a:a+z],'little')
    def store(self,a,z,v,external=False):
        v&=(1<<(z*8))-1;self.memory[a:a+z]=v.to_bytes(z,'little')
        (self.external if external else self.writes).append((a,z,v))
    def dg(self,a,z=1):return self.get(self.data+a,z)
    def setdg(self,a,v,z=1):self.store(self.data+a,z,v)
    def resident(self):return self.dg(0x2466,2)*16+self.dg(0x2464,2)
    def rg(self,a,z=1):return self.get(self.resident()+a,z)
    def setrg(self,a,v,z=1):self.store(self.resident()+a,z,v)
    def port(self,p,v):self.events.append(dict(name='out',port=p,width=1,value=v&255))
    def picture(self,i):
        a=(0xa0e+4*i)&65535;return [self.dg(a,2),self.dg(a+2,2)]
    def call(self,name,args=(),extra=None):
        event=dict(name=name,args=list(args));reply=self.s['reply']
        if name in ('cdg-load','cdg-load-noalpha','cdg-all-noalpha','snd-load','bfnt','palette-entry','exist','create','open','append'):
            a,b=(1,2) if name in ('cdg-load','cdg-load-noalpha') else (0,1)
            raw=self.memory[args[b]*16+args[a]:args[b]*16+args[a]+256];event['string']=bytes(raw[:raw.index(0)+1]).hex()
        if name=='palette':event['tone']=self.dg(0x2d4,2)
        if name=='gaiji':event['glyphs']=bytes(self.memory[args[2]*16+args[1]:args[2]*16+args[1]+3]).hex()
        if name=='exist':reply=self.s['ranks'][self.rank%4].get('exists',1);event['reply']=reply
        if name=='read':
            raw=bytes.fromhex(self.s['ranks'][self.rank%4].get('read_hex',''));event['bytes']=raw.hex()
            for j,v in enumerate(raw):self.store(args[2]*16+args[1]+j,1,v,True)
        if name=='write':event['bytes']=bytes(self.memory[args[2]*16+args[1]:args[2]*16+args[1]+args[0]]).hex()
        if name.startswith('input-') and name!='input-reset':
            if self.inputs>=len(self.s['inputs']):raise ValueError('Select scalar input fixture exhausted')
            event['input']=self.s['inputs'][self.inputs];self.inputs+=1
            for a,v in zip((0x1aa2,0x1aa4,0x1aa6),event['input']):self.store(self.data+a,2,v,True)
        if extra and any(event.get(k)!=v for k,v in extra.items()):raise ValueError('Select score adapter payload differs')
        self.events.append(event);return reply
    def invoke(self,name,args=()):
        if name in ('load','encode','decode','recreate','sum'):
            self.rank=args[0] if args else self.rank;adapter=ScoreAdapter(self,self.rank)
            if name=='sum':return adapter.invalid()
            return getattr(adapter,name)(*args)
        self.native[name]+=1;return getattr(self,name)(args)
    def irand(self,args):
        n=(self.dg(0x312,4)*22695477+1)&0xffffffff
        self.setdg(0x312,n&65535,2);self.setdg(0x314,n>>16,2);return (n>>16)&0x7fff
    def polar(self,args):return (signed(args[0])+((signed(args[1])*signed(args[2]))>>8))&65535
    def unlock(self,args):
        ret=7
        for i in range(4):
            if self.invoke('load',[i]):return 7
            if self.dg(HI+82)==99:ret=9
        return ret
    def cdg1(self,args):
        self.call('hflip')
        for i in range(3):self.call('cdg-load',[0,*self.picture(i),i+2])
        self.call('cdg-all-noalpha',[0xaac,0x2000+DS,13])
    def cdg2(self,args):
        self.call('cdg-load',[0,0xab5,0x2000+DS,1])
        self.call('cdg-load-noalpha',[0,0xabe,0x2000+DS,11]);self.call('cdg-load-noalpha',[0,0xac8,0x2000+DS,12])
    def cdg3(self,args):
        self.call('cdg-load',[0,*self.picture(0),0])
        for i in range(3,6):self.call('cdg-load',[0,*self.picture(i),i+2])
    def clock(self,site):
        limit=CLOCK_SITES[site]
        while True:
            cur=self.dg(0x11e8,2)
            if cur<limit:
                seq=[0,29,30] if limit==30 else [0,2,self.s['clock']]
                n=self.polls[site];self.polls[site]+=1
                self.store(self.data+0x11e8,2,seq[min(n,len(seq)-1)],True);cur=self.dg(0x11e8,2)
            if cur>=limit:break
        self.polls[site]=0
    def init(self,args):
        self.setdg(0x11e8,0,2);self.call('kaja',[256]);self.call('snd-load',[0xad1,0x2000+DS,0x600]);self.call('kaja',[0])
        self.setdg(0x2474,200,2);self.setdg(0x312,self.rg(0x10,4),4)
        self.call('text-clear');self.call('super-free');self.call('bfnt',[0xada,0x2000+DS])
        for page in (0,1):self.port(0xa6,page);self.call('graph-clear')
        self.port(0xa4,0);self.setdg(0x246c,0);self.call('palette-entry',[0xae5,0x2000+DS]);self.call('palette')
        for i in range(6,9):self.call('cdg-load',[0,*self.picture(i),i+2])
        self.clock(0x1bc1);self.setdg(0x2476,8,2);self.setdg(0x2478,self.invoke('unlock'))
    def free(self,args):
        for i in range(22):self.call('cdg-free',[i])
        self.call('super-free')
    def vs_pics(self,args):
        p1=0 if self.dg(0x246a) else byte_signed(self.dg(0x2468))+2
        p2=1 if self.dg(0x246b) else byte_signed(self.dg(0x2469))+2
        self.call('cdg-put',[p1&65535,96,32]);self.call('cdg-hflip',[p2&65535,96,416])
    def storypics(self,args):
        p1=0 if self.dg(0x246a) else byte_signed(self.dg(0x2468))+2
        self.call('cdg-put',[p1&65535,96,32]);self.call('cdg-put',[1,96,416])
    def stats(self,args):
        self.call('cdg-noalpha',[11,304,32])
        if self.rg(0x28)!=1:self.call('cdg-noalpha',[11,304,416])
        self.call('grcg-color',[14,0xc0])
        for row in range(3):
            top=315+16*row
            for pid in range(1 if self.rg(0x28)==1 else 2):
                stars=self.dg((0xa32+3*byte_signed(self.dg(0x2468+pid))+row)&65535);i=5;left=140+384*pid
                while stars<i:self.call('boxfill',[top+15,left+8,top,left]);i-=1;left-=11
        self.call('grcg-off')
    def names(self,args):
        for i in range(self.dg(0x2478)):
            self.call('super',[2*i,(136+20*i)&65535,256]);self.call('super',[2*i+1,(136+20*i)&65535,320])
    def extras(self,args):
        for pid in range(1 if self.rg(0x28)==1 else 2):
            self.call('cdg-noalpha',[12,304,160+384*pid]);self.call('cdg-noalpha',[(13+byte_signed(self.dg(0x2468+pid)))&65535,316,176+384*pid])
    def curve(self,args):
        fy,fx,radius,oy,ox=args
        for a in range(256):
            ax=trunc(signed(((a+(ox&255))&255)*signed(fx)),256)&255
            ay=trunc(signed(((a+(oy&255))&255)*signed(fy)),256)&255
            x=self.invoke('polar',[320,radius,self.dg(0x396+2*ax,2)]);y=self.invoke('polar',[200,radius,self.dg(0x316+2*ay,2)])
            self.call('pset',[y,x])
    def curves(self,args):
        c=self.dg(0x2462);t=c if c<128 else 256-c;other=256+t;fx=256+2*t;fy=2*other
        def pair(i):
            self.invoke('curve',[fy,other,220,(2*c-4*i)&255,(c-2*i)&255])
            self.invoke('curve',[other,fx,120,trunc(signed(c-2*i),2)&255,(-c+2*i)&255])
        self.call('grcg-color',[6,0xc0]);pair(0);self.call('grcg-color',[5,0xc0])
        n=signed(self.dg(0x2476,2));half=trunc(n,2)+(n&1)
        for i in range(1,half+1):pair(i)
        self.call('grcg-color',[1,0xc0])
        for i in range(half+1,n+1):pair(i)
        self.call('grcg-off');self.setdg(0x2462,c+2)
    def cursor(self,args):
        col,pid=args;top=(128+20*byte_signed(self.dg(0x2468+pid)))&65535;left=240+128*pid
        self.call('gaiji',[col&255,0xa4d+3*pid,0x2000+DS,16,top,left]);self.call('gaiji',[col&255,0xa53+3*pid,0x2000+DS,16,(top+16)&65535,left])
    def update(self,args):
        pid,inp=args
        if self.dg(0x246a+pid):return
        if self.dg(0xa59+pid):
            if inp==0:self.setdg(0xa59+pid,0)
            return
        if inp&1:
            self.setdg(0x2468+pid,self.dg(0x2468+pid)-1)
            if byte_signed(self.dg(0x2468+pid))<0:self.setdg(0x2468+pid,self.dg(0x2478)-1)
            self.setdg(0xa59+pid,1)
        if inp&2:
            self.setdg(0x2468+pid,self.dg(0x2468+pid)+1)
            if byte_signed(self.dg(0x2468+pid))>=self.dg(0x2478):self.setdg(0x2468+pid,0)
            self.setdg(0xa59+pid,1)
        for bit,palette in ((0x20,0),(0x10,1)):
            if not inp&bit:continue
            char=byte_signed(self.dg(0x2468+pid));self.setrg(0xc+pid,2*char+1+palette);self.call('white-in',[1])
            collision=self.dg(0x246a+1-pid) and self.rg(0xc)==self.rg(0xd)
            if collision:self.setrg(0xc+pid,self.rg(0xc+pid)+(1 if palette==0 else -1))
            self.call('cdg-load',[1-palette if collision else palette,*self.picture(char),pid])
            if self.dg(0x246a+1-pid):self.setdg(0x2472,0,2)
            self.setdg(0x246a+pid,1);self.setdg(0xa59+pid,1)
    def mode(self,off):self.setdg(0x2470,0x2000+0xbeb,2);self.setdg(0x246e,off,2)
    def init_vs(self):
        for p in (0,1):self.setdg(0x2468+p,trunc(self.rg(0xc+p)-1,2))
        self.setdg(0x246a,0);self.setdg(0x246b,0)
    def base_render(self,story=False):
        for name in ('curves','storypics' if story else 'vs_pics','stats','names','extras'):self.invoke(name)
    def cursors(self,p2=True):
        self.invoke('cursor',[15 if self.dg(0x246a) else 8,0])
        if p2:self.invoke('cursor',[15 if self.dg(0x246b) else 10,1])
    def input_sense(self):
        self.call('input-reset');self.call('input-'+format(self.dg(0x246e,2),'x'))
    def cancel(self):
        self.port(0xa6,0);self.call('graph-clear');self.port(0xa4,0);self.call('text-clear');self.invoke('free');self.call('kaja',[256]);return 1
    def fadeout(self):
        self.call('text-clear');n=self.dg(0x2472,2)
        if n>=16:self.setdg(0x2d4,200-6*n,2);self.call('palette')
        return n>32
    def wait_flip(self,site):
        self.clock(site)
        if self.dg(0x11e8,2)>4 and signed(self.dg(0x2476,2))>1:self.setdg(0x2476,self.dg(0x2476,2)-1,2)
        self.setdg(0x11e8,0,2);self.port(0xa6,self.dg(0x246c));self.setdg(0x246c,1-self.dg(0x246c));self.port(0xa4,self.dg(0x246c))
        self.call('grcg-color',[0,0xc0]);self.call('boxfill8',[399,79,0,0]);self.call('grcg-off')
        self.setdg(0x2472,self.dg(0x2472,2)+1,2);self.setrg(0x10,self.rg(0x10,4)+1,4)
    def versus(self,args):
        self.invoke('init');self.call('text-clear');self.init_vs();key=self.rg(0x16)
        self.mode(0xafa if key==0 else 0xb04 if key==1 else 0xb26);self.call('frame',[16]);self.setdg(0x2472,0,2)
        while True:
            self.base_render();self.cursors();self.input_sense();self.invoke('update',[0,self.dg(0x1aa2,2)]);self.invoke('update',[1,self.dg(0x1aa4,2)])
            if self.dg(0x1aa6,2)&0x1000:return self.cancel()
            if self.dg(0x246a) and self.dg(0x246b) and self.fadeout():break
            self.wait_flip(0x22b7)
        self.invoke('free');return 0
    def cpu(self,args):
        self.invoke('init');self.init_vs();self.mode(0xad6)
        for pid in (0,1):
            self.setdg(0x2472,0,2)
            while True:
                self.base_render();self.input_sense();self.cursors(bool(self.dg(0x246a)));self.invoke('update',[pid,self.dg(0x1aa6,2)])
                if self.dg(0x1aa6,2)&0x1000:return self.cancel()
                if pid==0 and self.dg(0x246a) and self.dg(0x2472,2)>12:break
                if pid==1 and self.dg(0x246b) and self.fadeout():break
                self.wait_flip(0x2429)
        self.invoke('free');return 0
    def story(self,args):
        self.invoke('init');self.setdg(0x2468,0);self.setdg(0x246a,0);self.setdg(0x246b,1);self.mode(0xad6);self.setdg(0x2472,0,2)
        while True:
            self.base_render(True);self.cursors(False);self.input_sense();self.invoke('update',[0,self.dg(0x1aa6,2)])
            if self.dg(0x1aa6,2)&0x1000:return self.cancel()
            if self.dg(0x246a) and self.fadeout():break
            self.wait_flip(0x254f)
        self.invoke('free');return 0


class SelectProbe(Probe):
    """Run original instructions; audit every call, return, store and port."""
    def __init__(self,mz,s):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR, UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,(struct.unpack_from('<H',image,at)[0]+0x2000)&65535)
        self.uc.mem_write(0x20000,bytes(image));self.code=(0x2000+CS)*16;self.data=(0x2000+DS)*16;self.stack=0x40000
        self.uc.mem_write(self.stack,bytes([0xa5])*65536);self.uc.mem_write(0x60000,bytes((j*17+11)&255 for j in range(512)))
        for seg in (0xa800,0xb000,0xb800,0xe000):self.uc.mem_write(seg*16,bytes((j*13+7)&255 for j in range(65536)))
        values=[(0x2464,0x31,2),(0x2466,0x6000,2),(0x2462,s['cycle'],1),(0x246c,s['page'],1),
                (0x2472,s['fade'],2),(0x2474,0x7788,2),(0x2476,s['trail']&65535,2),(0x2478,s['available'],1),
                (0x312,s['seed'],4),(0x2d4,s['tone'],2),(0x11e8,s['vsync'],2)]
        for i in (0,1):values.extend([(0x2468+i,s['sel'][i],1),(0x246a+i,s['confirmed'][i],1),(0xa59+i,s['locked'][i],1)])
        for a,v,z in values:self.uc.mem_write(self.data+a,v.to_bytes(z,'little'))
        for a,v,z in ((0xc,s['paletted'][0],1),(0xd,s['paletted'][1],1),(0x10,s['resident_seed'],4),(0x16,s['key_mode'],1),(0x28,s['game_mode'],1)):
            self.uc.mem_write(0x60031+a,v.to_bytes(z,'little'))
        self.uc.mem_write(self.data+HI,bytes.fromhex(s['hi']))
        self.s=s;self.meta=analyze(mz.program_image);self.events=[];self.writes=[];self.external=[];self.native=Counter()
        self.inputs=0;self.rank=0;self.polls=Counter();self.visited=set();self.frames=[];self.top=None;self.errors=[];self.position=None
        self.entry_specs={(r['segment'],r['offset']):r for r in self.meta['bodies']}
        for r,v in dict(DS=0x2000+DS,SS=0x4000,ES=0x3333,BP=0x7777,SI=0x1357,DI=0x2468,BX=0xbeef).items():self.set(r,v)
        self.set('EFLAGS',2|(0x200 if s['if'] else 0)|(0x400 if s['df'] else 0))
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def matches(caller,dest):
            if not caller:return False
            if caller['destination'] is not None:return caller['destination']==dest
            ptr=struct.unpack('<HH',self.uc.mem_read(self.data+0x246e,4))
            return dest==(ptr[1]-0x2000,ptr[0]) and dest[0]==0xbeb and dest[1] in (0xad6,0xafa,0xb04,0xb26)
        def code(uc,address,size,user):
            seg=self.get('CS')-0x2000;off=address-self.get('CS')*16;position=(seg,off);self.position=position
            if self.get('SS')!=0x4000:raise ValueError('Select stack segment alias')
            if address==self.code+0xff00:
                f=self.top
                if seg!=CS or self.get('SP')!=f['sp']+f['width']+f['cleanup'] or self.frames or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('Select terminal frame differs')
                self.stop=True;uc.emu_stop();return
            if self.frames and position==self.frames[-1]['ret']:
                f=self.frames.pop()
                if self.get('SP')!=f['sp']+f['width']+f['cleanup'] or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('Select native callback return differs')
            if position in self.meta['bounds']:
                self.visited.add(position)
                if seg==CS and off in CLOCK_SITES:
                    limit=CLOCK_SITES[off];cur=int.from_bytes(uc.mem_read(self.data+0x11e8,2),'little')
                    if cur<limit:
                        seq=[0,29,30] if limit==30 else [0,2,s['clock']];n=self.polls[off];self.polls[off]+=1
                        v=seq[min(n,len(seq)-1)];uc.mem_write(self.data+0x11e8,struct.pack('<H',v));self.external.append((self.data+0x11e8,2,v))
                        if v>=limit:self.polls[off]=0
                    else:self.polls[off]=0
                if position in self.meta['entries']:
                    row=self.entry_specs[position];self.native[row['name']]+=1
                    if row['name'] in ('load','encode'):self.rank=int.from_bytes(uc.mem_read(self.stack+self.get('SP')+2,2),'little')
                    if self.entered:
                        sp=self.get('SP');width=4 if row['far'] else 2
                        words=struct.unpack('<'+'H'*(width//2),uc.mem_read(self.stack+sp,width));ret=(words[1]-0x2000 if width==4 else seg,words[0]);caller=self.meta['calls'].get(ret)
                        if not matches(caller,position):raise ValueError('Select native caller differs')
                        self.frames.append(dict(ret=ret,sp=sp,width=width,cleanup=row['cleanup'],saved={r:self.get(r) for r in ('BP','SI','DI','DS')}))
                    self.entered=True
                if position in self.meta['returns']:
                    f=self.frames[-1] if self.frames else self.top;sp=self.get('SP');width=f['width']
                    words=struct.unpack('<'+'H'*(width//2),uc.mem_read(self.stack+sp,width));ret=(words[1]-0x2000 if width==4 else seg,words[0])
                    if sp!=f['sp'] or ret!=f['ret'] or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('Select native return stack differs')
                return
            if position not in MODELS:raise ValueError('Select escape/operand boundary differs: '+str(position))
            name,count,cleanup=MODELS[position];sp=self.get('SP');words=struct.unpack('<HH',uc.mem_read(self.stack+sp,4));ret=(words[1]-0x2000,words[0]);caller=self.meta['calls'].get(ret)
            if not matches(caller,position):raise ValueError('Select foreign caller frame differs')
            args=list(struct.unpack('<'+'H'*(count//2),uc.mem_read(self.stack+sp+4,count))) if count else []
            if name=='gaiji':args[0]&=255 # The source vc_t is byte-wide; upper argument byte is unspecified.
            event=dict(name=name,args=args);reply=s['reply']
            if name in ('cdg-load','cdg-load-noalpha','cdg-all-noalpha','snd-load','bfnt','palette-entry','exist','create','open','append'):
                a,b=(1,2) if name in ('cdg-load','cdg-load-noalpha') else (0,1)
                if args[b]!=0x2000+DS:raise ValueError('Select filename segment differs')
                raw=bytes(uc.mem_read(args[b]*16+args[a],256));event['string']=raw[:raw.index(0)+1].hex()
            if name=='palette':event['tone']=int.from_bytes(uc.mem_read(self.data+0x2d4,2),'little')
            if name=='gaiji':event['glyphs']=bytes(uc.mem_read(args[2]*16+args[1],3)).hex()
            if name=='exist':reply=s['ranks'][self.rank%4].get('exists',1);event['reply']=reply
            if name=='read':
                if args!=[SIZE,HI,0x2000+DS]:raise ValueError('Select score read span differs')
                raw=bytes.fromhex(s['ranks'][self.rank%4].get('read_hex',''))
                if len(raw)>SIZE:raise ValueError('Select score fixture exceeds206bytes')
                event['bytes']=raw.hex();uc.mem_write(self.data+HI,raw);self.external.extend((self.data+HI+j,1,v) for j,v in enumerate(raw))
            if name=='write':event['bytes']=bytes(uc.mem_read(args[2]*16+args[1],args[0])).hex()
            if name.startswith('input-') and name!='input-reset':
                if self.inputs>=len(s['inputs']):raise ValueError('Select input fixture exhausted')
                event['input']=s['inputs'][self.inputs];self.inputs+=1
                for a,v in zip((0x1aa2,0x1aa4,0x1aa6),event['input']):
                    uc.mem_write(self.data+a,struct.pack('<H',v));self.external.append((self.data+a,2,v))
            self.events.append(event);self.set('AX',reply);self.set('EFLAGS',(self.get('EFLAGS')&~1)|s['cf'])
            self.set('SP',sp+4+cleanup);self.set('CS',words[1]);self.set('IP',words[0])
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            dg=address-self.data
            allowed=(size==1 and (dg in (0xa59,0xa5a,0x2462,0x2468,0x2469,0x246a,0x246b,0x246c,0x2478) or HI<=dg<HI+SIZE))
            allowed=allowed or (size==2 and (dg in (0x312,0x314,0x2d4,0x11e8,0x246e,0x2470,0x2472,0x2474,0x2476,HI))) or (size==4 and dg==0x312)
            allowed=allowed or (size==1 and address in (0x6003d,0x6003e)) or (size==4 and address==0x60041)
            if not allowed or self.position not in self.meta['bounds']:raise ValueError('Select complete native store span differs: '+str((hex(address),size,self.position)))
            self.writes.append((address,size,value&((1<<(size*8))-1)))
        def intr(*args):raise ValueError('Select unexpected interrupt')
        def output(uc,port,width,value,user):
            if port not in (0xa4,0xa6) or width!=1 or self.position not in self.meta['bounds']:raise ValueError('Select port caller/width differs')
            self.events.append(dict(name='out',port=port,width=width,value=value))
        # No memory-read hook: Unicorn1.0.2rc4's RETF regression is separately
        # reproduced by probe_th03_unicorn_far_return.py. All returns stay native.
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write))
        self.uc.hook_add(UC_HOOK_INTR,guard(intr));self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT)
    def run(self,name,args=(),budget=5000000):
        self.stop=False;self.errors.clear();self.entered=False
        row=next(r for r in self.meta['bodies'] if r['name']==name);width=4 if row['far'] else 2
        self.set('CS',row['segment']+0x2000);self.set('SP',0xffd0)
        words=[0xff00]+([CS+0x2000] if width==4 else [])+list(args)
        self.uc.mem_write(self.stack+0xffd0,struct.pack('<'+'H'*len(words),*words))
        self.top=dict(sp=0xffd0,ret=(CS,0xff00),width=width,cleanup=row['cleanup'],saved={r:self.get(r) for r in ('BP','SI','DI','DS')})
        self.uc.emu_start(0x20000+row['segment']*16+row['offset'],0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('Select terminal/budget differs')
        return self.get('AX')&255 if name in ('unlock','load','sum','versus','cpu','story') else self.get('AX')


def rank_fixture(cleared=18,exists=1,invalid=False,n=SIZE):
    raw=bytearray(sample(3));raw[82]=cleared;raw=bytearray(sealed(raw))
    if invalid:raw[0]^=1
    return dict(exists=exists,read_hex=encrypt(raw)[:n].hex())


def scenario(**kw):
    s=dict(sel=[0,1],confirmed=[0,0],locked=[0,0],available=7,cycle=0,trail=8,page=1,fade=0x3344,
           seed=1,resident_seed=0x12345678,tone=100,vsync=0,key_mode=0,game_mode=0,paletted=[1,3],
           ranks=[rank_fixture() for _ in range(4)],hi=sample().hex(),inputs=[[0,0,0x1000]],clock=5,reply=0,cf=0,
           **{'if':True,'df':False})
    s.update(kw);return s


def observe(mz,name,s,args=(),sequence=None):
    p=SelectProbe(mz,s);before=bytes(p.uc.mem_read(0,0x100000));spec=SelectSpec(before,p.data,s);replies=[]
    for n,a in sequence or [(name,args)]:
        expected=spec.invoke(n,a);actual=p.run(n,a)
        if n in ('unlock','load','sum','versus','cpu','story') and actual!=expected:raise ValueError('Select return value differs')
        replies.append(actual if n in ('unlock','load','sum','versus','cpu','story') else None)
    for label,a,b in [('events',p.events,spec.events),('writes',p.writes,spec.writes),('external',p.external,spec.external),('native',p.native,spec.native)]:
        if a!=b:
            if isinstance(a,list):
                i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)));detail=str((i,a[i:i+1],b[i:i+1],len(a),len(b)))
            else:detail=str((a,b))
            raise ValueError('Select independent scalar '+label+' differs: '+name+' '+detail)
    actual=bytes(p.uc.mem_read(0,0x100000))
    if actual[:p.stack]!=spec.memory[:p.stack] or actual[p.stack+65536:]!=spec.memory[p.stack+65536:]:
        i=next(i for i,(x,y) in enumerate(zip(actual,spec.memory)) if x!=y and not p.stack<=i<p.stack+65536)
        raise ValueError('Select whole physical preservation differs: '+hex(i))
    if bool(p.get('EFLAGS')&0x200)!=s['if'] or bool(p.get('EFLAGS')&0x400)!=s['df']:raise ValueError('Select IF/DF differs')
    digest=lambda x:sha(json.dumps(x,separators=(',',':')).encode())
    return dict(function=name,args=list(args),sequence=sequence,scenario=s,replies=replies,native_entries=dict(p.native),
                events=len(p.events),events_sha256=digest(p.events),nonpoint_events=[e for e in p.events if e['name']!='pset'],
                stores=len(p.writes),stores_sha256=digest(p.writes),external_inputs=p.external,
                visited=[list(a) for a in sorted(p.visited)],memory_before_sha256=sha(before),memory_after_sha256=sha(spec.memory),
                state=dict(sel=[spec.dg(0x2468+i) for i in (0,1)],confirmed=[spec.dg(0x246a+i) for i in (0,1)],
                           locked=[spec.dg(0xa59+i) for i in (0,1)],paletted=[spec.rg(0xc+i) for i in (0,1)],
                           fade=spec.dg(0x2472,2),trail=signed(spec.dg(0x2476,2)),cycle=spec.dg(0x2462),tone=spec.dg(0x2d4,2)))


def matrix(mz):
    rows=[]
    for irq,df in itertools.product((False,True),repeat=2):
        flags={'if':irq,'df':df}
        for name in ('cdg1','cdg2','cdg3','free','vs_pics','storypics','names','extras','cursor'):
            for mode in (0,1):rows.append(observe(mz,name,scenario(game_mode=mode,available=9,sel=[8,7],**flags),[0xf3a5,mode] if name=='cursor' else []))
        for char in range(9):rows.append(observe(mz,'stats',scenario(sel=[char,8-char],game_mode=char%2,**flags)))
        for cleared,error in ((-1,-1),(0,-1),(3,-1),(0,1),(3,0)):
            ranks=[rank_fixture(99 if i==cleared else 18,exists=0 if i==error else 1) for i in range(4)]
            rows.append(observe(mz,'unlock',scenario(ranks=ranks,reply=0xbeef,cf=1,**flags)))
        rows.append(observe(mz,'unlock',scenario(ranks=[rank_fixture(invalid=True)]+[rank_fixture()]*3,**flags)))
        rows.append(observe(mz,'init',scenario(locked=[1,255],cycle=255,confirmed=[255,1],**flags)))
        for pid,inp in itertools.product((0,1),(0,1,2,3,0x10,0x20,0x30,0x33,0x1000,0xffff)):
            for other in (0,1):
                pal=[1,1];pal[1-pid]=1 if inp&0x20 else 2
                rows.append(observe(mz,'update',scenario(sel=[0,0],confirmed=[0,other] if pid==0 else [other,0],paletted=pal,**flags),[pid,inp]))
        for locked,confirmed,inp in itertools.product((1,255),(0,1),(0,0x33)):
            rows.append(observe(mz,'update',scenario(locked=[locked,0],confirmed=[confirmed,0],**flags),[0,inp]))
        # Both directions and byte wrap without confirming an invalid resource index.
        for sel,available,inp in ((6,7,2),(8,9,2),(127,255,2),(128,255,2),(255,0,1),(0,0,3)):
            rows.append(observe(mz,'update',scenario(sel=[sel,0],available=available,**flags),[0,inp]))
        for fy,fx,radius,oy,ox in ((256,256,220,0,0),(768,512,120,255,255),(0,1,0,1,127),
                                  (32767,32768,65535,128,1),(65535,257,32767,2,254)):
            rows.append(observe(mz,'curve',scenario(**flags),[fy,fx,radius,oy,ox]))
        for c,n in ((0,0),(1,1),(2,2),(127,3),(128,8),(129,-1),(254,-2),(255,8)):
            rows.append(observe(mz,'curves',scenario(cycle=c,trail=n,**flags)))
        for mode in (0,1,2,255):rows.append(observe(mz,'versus',scenario(key_mode=mode,**flags)))
        for name in ('cpu','story'):rows.append(observe(mz,name,scenario(game_mode=1 if name=='story' else 0,**flags)))
        # Cancel after two confirmation bits, native update is still executed first.
        rows.append(observe(mz,'story',scenario(game_mode=1,inputs=[[0,0,0x1030]],paletted=[1,1],**flags)))
        # Persistent lock: held input does not clear it; a release then confirms.
        rows.append(observe(mz,'story',scenario(game_mode=1,locked=[1,1],inputs=[[0,0,0x20],[0,0,0],[0,0,0x1030]],**flags)))
        print('Select profile',flags,'cases',len(rows),flush=True)
    # Complete successful public callers run all subordinate native instructions.
    for name,inputs,mode in (
        ('versus',[[0x30,0x20,0]]+[[0,0,0]]*35,0),
        ('cpu',[[0,0,0x30]]+[[0,0,0]]*13+[[0,0,0x20]]+[[0,0,0]]*35,0),
        ('story',[[0,0,0x30]]+[[0,0,0]]*35,1)):
        rows.append(observe(mz,name,scenario(game_mode=mode,inputs=inputs,paletted=[1,1])))
    rows.append(observe(mz,'story',scenario(game_mode=1,inputs=[[0,0,0x1000],[0,0,0x1000]]),
                        sequence=[('story',[]),('story',[])]))
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('Select source parent proof differs')
    parent=json.loads(raw);inputs=dict(parent['inputs']);inputs[PROOF]=sha(raw)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('Select prerequisite differs: '+p)
    for p in ('scripts/review_th03_op_select.py','scripts/review_th03_op_score.py','scripts/probe_th03_unicorn_far_return.py'):
        inputs[p]=sha((ROOT/p).read_bytes())
    artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-op');stored=read_verified_artifact(ROOT,artifact)
    frozen=frozen_files(REVISION);target=parse_mz((ROOT/DECODED).read_bytes());observations=[]
    paths=[DECODED]+[str(Path(PROOF).parent/f'round{r["number"]}'/'source/bin/th03/op.exe') for r in parent['rounds']]
    for index,path in enumerate(paths):
        raw=(ROOT/path).read_bytes();inputs[path]=sha(raw);mz=parse_mz(raw)
        if not mz.valid:raise ValueError('Select invalid decoded MZ')
        meta=analyze(mz.program_image);o=dict(path=path,bodies=meta['bodies'])
        if index:
            round=parent['rounds'][index-1];tree=Path(path).parents[2];o['source_lineage']={}
            if inputs[path]!=round['products']['bin/th03/op.exe']:raise ValueError('Select parent product differs')
            for p in PROVIDERS:
                cp=str(tree/p);raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw);expected=frozen[p]
                if p=='th03/op/m_select.cpp':
                    expected=expected.replace(b'#include "th03/formats/score_ld.cpp"',b'#include "src/op/formats/score_load.inl"')
                if p in ('th03/op_02.cpp','th03/scoredat.cpp'):
                    source='src/op/formats/score_encode.cpp' if p=='th03/op_02.cpp' else 'src/op/formats/score_data.cpp'
                    expected=f'#include "{source}"\n'.encode()
                if raw!=expected:raise ValueError('Select frozen/maintained-loader provider differs: '+p)
                o['source_lineage'][p]=dict(frozen_sha256=sha(frozen[p]),cached_sha256=sha(raw),maintained_overlay=(raw!=frozen[p]))
            cp=str(tree/'obj/th03/op_sel.obj');raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw);obj=describe_omf(raw)
            if not obj['valid'] or obj['dependency_timestamp_normalized_sha256']!=round['all_objects']['obj/th03/op_sel.obj']:raise ValueError('Select OMF differs')
            o['object']=dict(path=cp,normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'])
            cp=str(tree/'obj/th03/op.map');raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw)
            carrier=next(c for c in code_rows(raw.decode(),len(mz.program_image)) if c['module']=='th03/op_sel.cpp' and c['size'])
            if (carrier['segment'],carrier['offset'],carrier['size'])!=(CS,0x19f2,3013):raise ValueError('Select original carrier differs')
            o['comparisons']={}
            for name,seg,a,z,c,f in RANGES:
                comp=extent_observation(target,mz,dict(segment=seg,offset=a,start=seg*16+a,size=z));o['comparisons'][name]=comp
                if not comp['raw_slice_equal'] or comp['ordered_relocations_equal']!=(name not in ('curves','versus')):raise ValueError('Select original raw/ordered observation differs')
            comp=extent_observation(target,mz,dict(segment=DS,offset=0xa0e,start=DS*16+0xa0e,size=0xe3))
            if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('Select original DATA bytes/relocations differ')
            o['data']=comp
        o['cpu']=matrix(mz);visited={tuple(a) for r in o['cpu'] for a in r['visited']}
        o['coverage']=dict(instructions=len(meta['bounds']),visited=len(meta['bounds']&visited),unvisited=[list(a) for a in sorted(meta['bounds']-visited)])
        if o['coverage']['unvisited']:raise ValueError('Select native coverage incomplete: '+str(o['coverage']['unvisited']))
        if index and normalized_contracts(o['cpu'])!=normalized_contracts(observations[0]['cpu']):raise ValueError('Select target/cold contracts differ')
        observations.append(o);print('Reviewed',path,len(o['cpu']),'cases',o['coverage'],flush=True)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('Select input changed: '+p)
    final=frozen_files(REVISION)
    if any(final[p]!=frozen[p] for p in PROVIDERS) or read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('Select frozen/canonical target changed')
    report=dict(kind='th03-op-complete-character-selection-native-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,observations=observations,
                tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),new_decoded_bytes=2906,carrier_bytes=3013,carrier_functions=19,
                context_bytes=569,ordered_relocation_failures=['curves','versus'],diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,new_build=False,
                notes='Complete3013-byte19-function carrier;107-byte score loader previously owned. Other score394/IRAND42/POLAR26 context only. Three complete native public menus and independent scalar state/curves/score formats; ordered native stores, foreign calls, ports, explicit external input/clock writes and whole1MiB outside64KiBstack compared. Persistent input locks, SHOT then BOMB, palette collisions, unsigned fade and adaptive trail preserved. Original curves351/versus407 relocation order differs despite full raw equality; failure retained without sorting. Native far function pointer and original near/far/Pascal/C frames audited. Explicit flat graphics/sound/file/input/clock fixtures grant no actual VRAM banking/resources/DOS/ISR/header/CRT/canonicalstorage/fullproduct/exact acceptance.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n');print('PASS complete OP selection diagnostics; exact open')


if __name__=='__main__':main()
