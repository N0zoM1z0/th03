#!/usr/bin/env python3
"""Review the complete TH03 OP Music Room carrier with native random/polar helpers."""
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
PROOF='.analysis/th03-op-entry/sol-op-entry-source-20261006/receipt.json'
PROOF_SHA='8bb73e41c37e0f8d20d0f5b03fa83076827ef36d1d522cf7625ca21659c810e7'
DECODED='.analysis/th03-diet/sol-diet-restoration-20261006-b/op.exe'
CS,DS=0x990,0xd7f
# name, segment, offset, full size, callee cleanup, far return.
RANGES=[('track',CS,0xc1e,114,4,False),('tracklist',CS,0xc90,39,2,False),
 ('snap',CS,0xcb7,49,0,False),('free',CS,0xce8,14,0,False),('put',CS,0xcf6,30,0,False),
 ('build',CS,0xd14,143,12,False),('polygons',CS,0xda3,502,0,False),('flip',CS,0xf99,54,0,False),
 ('bg_snap',CS,0xfcf,315,0,False),('load',CS,0x110a,73,2,False),('bg_free',CS,0x1153,41,0,False),
 ('unput',CS,0x117c,285,0,False),('comment',CS,0x1299,109,2,False),('music',CS,0x1306,476,0,True),
 ('irand',0,0x1d12,42,0,True),('polar',0xbeb,0x155,26,0,True)]
# Foreign name, argument bytes, callee cleanup. All foreign frames are far.
MODELS={(0xbeb,0x82b):('text',10,10),(0,0x24ca):('alloc',2,2),(0,0x25ce):('hfree',2,2),
 (0,0xc6a):('polygon',6,6),(0,0xec6):('grcg-color',4,4),(0,0xef0):('grcg-off',0,0),
 (0xbeb,0xcd6):('frame',2,2),(0,0x9a8):('open',4,4),(0,0x9e4):('seek',6,6),
 (0,0x8f4):('read',6,6),(0,0x888):('close',0,0),(0xbeb,0x7ec):('cdg-free',2,2),
 (0,0x269a):('super-free',0,0),(0,0x21f4):('text-clear',0,0),(0,0x1aa4):('palette',0,0),
 (0,0x114c):('graph-clear',0,0),(0xbeb,0xa90):('pi-load',6,6),(0xbeb,0x4a6):('pi-palette',2,2),
 (0xbeb,0x4cb):('pi-put',6,6),(0,0x12dc):('pi-free',8,8),(0,0x1186):('copy-page',2,2),
 (0xbeb,0xad6):('input',0,0),(0xbeb,0x553):('kaja',2,2),(0xbeb,0xa2):('snd-load',6,0)}
CALLS={}
for sites,dest in [([0xc55,0xc87,0x12b6,0x12d6],(0xbeb,0x82b)),([0xcbe,0xfdf],(0,0x24ca)),
 ([0xcef,0x115a,0x1163,0x116c,0x1175],(0,0x25ce)),([0xd48,0xd6b],(0xbeb,0x155)),
 ([0xdb5,0xdc9,0xddd,0xe0a,0xe21,0xe2a,0xef2,0xf11,0xf3e,0xf55,0xf5e],(0,0x1d12)),
 ([0xf89],(0,0xc6a)),([0xfa5],(0,0xec6)),([0xfad],(0,0xef0)),([0xfc8],(0xbeb,0xcd6)),
 ([0x1112],(0,0x9a8)),([0x1124],(0,0x9e4)),([0x1130],(0,0x8f4)),([0x1135],(0,0x888)),
 ([0x130f],(0xbeb,0x7ec)),([0x131a],(0,0x269a)),([0x131f],(0,0x21f4)),
 ([0x132f,0x13bd],(0,0x1aa4)),([0x133e,0x14d1],(0,0x114c)),([0x134f],(0xbeb,0xa90)),
 ([0x1356],(0xbeb,0x4a6)),([0x1360],(0xbeb,0x4cb)),([0x136e],(0,0x12dc)),([0x1382],(0,0x1186)),
 ([0x13c2,0x13d3,0x14b0],(0xbeb,0xad6)),([0x145c,0x147d],(0xbeb,0x553)),([0x1473],(0xbeb,0xa2))]:
    for site in sites:CALLS[site]=dest
for site,dest in [(0xca9,0xc1e),(0xe89,0xd14),(0xf9c,0xcf6),(0xfaa,0xda3),(0x12a1,0x110a),
 (0x12a4,0xcf6),(0x12a7,0x117c),(0x137d,0xc90),(0x1393,0xcb7),(0x1396,0xfcf),
 (0x13a5,0x1299),(0x13b4,0x1299),(0x13ce,0xf99),(0x13e5,0xc1e),(0x140b,0xc1e),
 (0x141b,0xc1e),(0x1441,0xc1e),(0x148b,0x1299),(0x148e,0xf99),(0x1497,0x1299),
 (0x14aa,0xf99),(0x14bc,0xf99),(0x14c1,0xce8),(0x14c4,0x1153)]:CALLS[site]=(CS,dest)
BULK_LOADS={0xcd0,0x1029,0x103c,0x104f,0x1062,0x10ac,0x10bf,0x10d2,0x10e5,
            0x11aa,0x11bf,0x11d4,0x11e9,0x1232,0x1247,0x125c,0x1271,0x12eb}
PROVIDERS=['th03/op_music.cpp','th02/op/m_music.cpp','planar.h','game/coords.hpp','libs/master.lib/master.hpp',
 'th02/v_colors.hpp','th02/hardware/frmdelay.h','th02/formats/musiccmt.hpp','th03/hardware/input.h',
 'th01/hardware/grppsafx.h','th02/snd/snd.h','th03/formats/cdg.h','th03/math/polar.hpp',
 'th02/op/m_music.hpp','th02/formats/pi.h','th03/shiftjis/music.hpp','libs/master.lib/random.asm',
 'libs/master.lib/rand[data].asm','th03/math/polar.cpp']


def analyze(image):
    d=Cs(CS_ARCH_X86,CS_MODE_16);d.detail=True
    bounds=set();entries={};returns={};calls={};bodies=[]
    for name,seg,a,z,cleanup,far in RANGES:
        body=image[seg*16+a:seg*16+a+z];ins=list(d.disasm(body,a));local={i.address for i in ins}
        expected=('retf' if far else 'ret',cleanup)
        signature=lambda i:(i.mnemonic,int(i.op_str,0) if i.op_str else 0)
        if len(body)!=z or sum(i.size for i in ins)!=z or signature(ins[-1])!=expected:raise ValueError('Music Room complete body/return differs: '+name)
        entries[(seg,a)]=name;bounds.update((seg,i.address) for i in ins);edges=[]
        for i in ins:
            if i.mnemonic in ('ret','retf'):
                if signature(i)!=expected:raise ValueError('Music Room interior return differs')
                returns[(seg,i.address)]=cleanup
            if i.mnemonic in ('int','in','iret'):raise ValueError('Music Room unexpected device instruction')
            if not(i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('Music Room unknown indirect edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (seg,i.operands[0].imm)
            if i.mnemonic in ('call','lcall'):
                if seg!=CS or CALLS.get(i.address)!=dest:raise ValueError('Music Room unknown caller')
                calls[(seg,i.address+i.size)]=dict(site=i.address,destination=dest)
            elif i.mnemonic=='ljmp' or dest[1] not in local:raise ValueError('Music Room branch enters operand/neighbor')
            edges.append(dict(site=i.address,kind=i.mnemonic,destination=list(dest)))
        bodies.append(dict(name=name,segment=seg,offset=a,size=z,cleanup=cleanup,far=far,instructions=len(ins),sha256=sha(body),edges=edges))
    if set(CALLS)!={v['site'] for v in calls.values()}:raise ValueError('Music Room complete call closure differs')
    if any(v['destination'] not in entries and v['destination'] not in MODELS for v in calls.values()):raise ValueError('Music Room missing callee model')
    return dict(bounds=bounds,entries=entries,returns=returns,calls=calls,bodies=bodies)


def signed(v):return (v&65535)-65536 if v&32768 else v&65535


class MusicSpec:
    """Independent scalar 16-bit behavior. Foreign replies are explicit fixtures."""
    def __init__(self,before,data,s):
        self.memory=bytearray(before);self.data=data;self.s=s;self.events=[];self.writes=[];self.reads=[]
        self.external=[];self.native=Counter();self.inputs=0;self.allocations=0;self.seek=0
    def get(self,a,z=1):
        value=int.from_bytes(self.memory[a:a+z],'little')
        if a>=0x50000:self.reads.append((a,z))
        return value
    def store(self,a,z,v,external=False):
        v&=(1<<(z*8))-1;self.memory[a:a+z]=v.to_bytes(z,'little')
        (self.external if external else self.writes).append((a,z,v))
    def dg(self,a,z=1):return self.get(self.data+a,z)
    def setdg(self,a,v,z=1):self.store(self.data+a,z,v)
    def ptr(self,a,p=0):return self.dg(a+2,2)*16+((self.dg(a,2)+p)&65535)
    def port(self,p,v):self.events.append(dict(name='out',port=p,width=1,value=v&255))
    def call(self,name,args=()):
        event=dict(name=name,args=list(args))
        if name in ('text','open','pi-load','snd-load'):
            a,b=(0,1);raw=self.memory[args[b]*16+args[a]:args[b]*16+args[a]+256]
            event['string']=bytes(raw[:raw.index(0)+1]).hex()
        if name=='polygon':
            event['points']=bytes(self.memory[args[2]*16+args[1]:args[2]*16+args[1]+4*(args[0]+1)]).hex()
        if name=='palette':event['tone']=self.dg(0x2d4,2)
        if name=='alloc':
            event['reply']=self.s['alloc'][self.allocations%5];self.allocations+=1
        if name=='seek':self.seek=signed(args[1]);event['signed_offset']=self.seek
        if name=='read':
            n=self.s['read'];block=bytes(((self.seek+j)*13+71)%255+1 for j in range(n));event['bytes']=block.hex()
            for j,value in enumerate(block):self.store(args[2]*16+args[1]+j,1,value,True)
        if name=='input':
            if self.inputs>=len(self.s['inputs']):raise ValueError('Music Room scalar input fixture exhausted')
            event['input']=self.s['inputs'][self.inputs];self.inputs+=1;self.store(self.data+0x1aa6,2,event['input'],True)
        # Device callbacks deliberately preserve flat VRAM. Real banking,
        # graphics, DOS file I/O and hardware timing are outside this fixture.
        self.events.append(event)
        return event.get('reply',self.s['reply'])
    def invoke(self,name,args=()):
        self.native[name]+=1;return getattr(self,name)(args)
    def irand(self,args):
        n=(self.dg(0x312,4)*22695477+1)&0xffffffff
        self.setdg(0x312,n&65535,2);self.setdg(0x314,n>>16,2);return (n>>16)&0x7fff
    def polar(self,args):return (signed(args[0])+((signed(args[1])*signed(args[2]))>>8))&65535
    def track(self,args):
        col,i=args[0]&255,args[1]&255
        for page in ((1-self.dg(0x2039))&255,self.dg(0x2039)):
            self.port(0xa6,page);self.call('text',[self.dg(0x5f2+4*i,2),self.dg(0x5f4+4*i,2),col|0x20,40+i*16,16])
    def tracklist(self,args):
        for i in range(21):self.invoke('track',[15 if i==(args[0]&255) else 3,i])
    def snap(self,args):
        seg=self.call('alloc',[32000]);self.setdg(0x203a,seg,2)
        for p in range(0,32000,4):self.store(seg*16+p,4,self.get(self.ptr(0x19fa,p),4))
    def free(self,args):self.call('hfree',[self.dg(0x203a,2)])
    def put(self,args):
        base=self.dg(0x203a,2)*16;step=-2 if self.s['df'] else 2
        for i in range(16000):p=(i*step)&65535;self.put_word(base,p)
    def put_word(self,base,p):self.store(0xa8000+p,2,self.get(base+p,2))
    def build(self,args):
        angle,count,radius,y,x,ptr=args;count=signed(count);y=signed(y)>>4
        for i in range(max(0,count)):
            ratio=((int(signed(i<<8)/count))+(angle&255))&255
            for axis,origin,table in ((0,x,0x396),(2,y,0x316)):
                value=self.invoke('polar',[origin&65535,radius,self.dg(table+2*ratio,2)])
                self.setdg(ptr+4*i+axis,value,2)
        i=max(0,count)
        for axis in (0,2):self.setdg(ptr+4*i+axis,self.dg(ptr+axis,2),2)
    def init_polygon(self,i,reset):
        self.setdg(0x1f98+4*i,self.invoke('irand')%640,2)
        self.setdg(0x1f9a+4*i,(-1600 if reset else self.invoke('irand')%6400),2)
        self.setdg(0x1fd8+4*i,(8-(self.invoke('irand')&15)) if reset else (4-(self.invoke('irand')&7)),2)
        if self.dg(0x1fd8+4*i,2)==0:self.setdg(0x1fd8+4*i,1,2)
        self.setdg(0x1fda+4*i,32+((self.invoke('irand')&3)<<4),2)
        self.setdg(0x2018+i,self.invoke('irand'))
        self.setdg(0x2028+i,4-(self.invoke('irand')&7))
        if self.dg(0x2028+i)==0:self.setdg(0x2028+i,4)
    def polygons(self,args):
        if not self.dg(0x692):
            for i in range(16):self.init_polygon(i,False)
            self.setdg(0x692,1)
        for i in range(16):
            self.invoke('build',[self.dg(0x2018+i),i//4+3,64+(i&3)*16,self.dg(0x1f9a+4*i,2),self.dg(0x1f98+4*i,2),0x1f70])
            self.setdg(0x1f98+4*i,self.dg(0x1f98+4*i,2)+self.dg(0x1fd8+4*i,2),2)
            self.setdg(0x1f9a+4*i,self.dg(0x1f9a+4*i,2)+self.dg(0x1fda+4*i,2),2)
            self.setdg(0x2018+i,self.dg(0x2018+i)+self.dg(0x2028+i))
            if signed(self.dg(0x1f98+4*i,2))<=0 or signed(self.dg(0x1f98+4*i,2))>=639:
                self.setdg(0x1fd8+4*i,-signed(self.dg(0x1fd8+4*i,2)),2)
            if signed(self.dg(0x1f9a+4*i,2))>=8000:self.init_polygon(i,True)
            self.call('polygon',[i//4+3,0x1f70,0x2000+DS])
    def flip(self,args):
        self.invoke('put');self.call('grcg-color',[15,0xce]);self.invoke('polygons');self.call('grcg-off')
        self.port(0xa4,self.dg(0x2039));self.setdg(0x2039,1-self.dg(0x2039));self.port(0xa6,self.dg(0x2039));self.call('frame',[1])
    def bg_snap(self,args):
        for i in range(4):
            seg=self.call('alloc',[12800]);self.setdg(0x203e+4*i,seg,2);self.setdg(0x203c+4*i,0,2)
        self.blit(False)
    def blit(self,restore):
        p=0
        for y in range(64,384):
            for x in range(304,624,32):
                vo=y*80+x//8
                for i in range(4):
                    a,b=self.ptr(0x19fa+4*i,vo),self.ptr(0x203c+4*i,p)
                    if restore:a,b=b,a
                    self.store(b,4,self.get(a,4))
                p+=4
    def load(self,args):
        off=signed(signed(args[0])*840)&0xffffffff
        self.call('open',[0x9d1,0x2000+DS]);self.call('seek',[0,off&65535,off>>16]);self.call('read',[840,0x204c,0x2000+DS]);self.call('close')
        for line in range(20):self.setdg(0x2074+42*line,0)
    def bg_free(self,args):
        for i in range(4):self.call('hfree',[self.dg(0x203e+4*i,2)])
    def unput(self,args):self.blit(True)
    def comment(self,args):
        self.invoke('load',args);self.invoke('put');self.invoke('unput')
        for line in range(20):self.call('text',[0x204c+42*line,0x2000+DS,31 if line==0 else 29,64+16*line,304])
        for p in range(0,32000,4):self.store(self.dg(0x203a,2)*16+p,4,self.get(self.ptr(0x19fa,p),4))
    def release(self):
        while True:
            self.call('input')
            if not self.dg(0x1aa6,2):return
            self.invoke('flip')
    def music(self,args):
        for i in range(32):self.call('cdg-free',[i])
        self.call('super-free');self.call('text-clear');self.setdg(0x2039,1);self.setdg(0x2d4,0,2);self.call('palette')
        self.port(0xa4,0);self.port(0xa6,0);self.call('graph-clear');self.port(0xa6,1)
        self.call('pi-load',[0x9db,0x2000+DS,0]);self.call('pi-palette',[0]);self.call('pi-put',[0,0,0])
        self.call('pi-free',[self.dg(0x1ca8,2),self.dg(0x1caa,2),0x1cc0,0x2000+DS])
        self.setdg(0x2038,self.dg(0x693));self.invoke('tracklist',[self.dg(0x2038,2)]);self.call('copy-page',[0])
        self.port(0xa6,1);self.port(0xa4,0);self.invoke('snap');self.invoke('bg_snap')
        for page in (1,0):self.port(0xa6,page);self.invoke('comment',[self.dg(0x693)])
        self.setdg(0x2d4,100,2);self.call('palette');self.release()
        while True:
            self.call('input');inp=self.dg(0x1aa6,2)
            for bit,delta in ((1,-1),(2,1)):
                if inp&bit:
                    self.invoke('track',[3,self.dg(0x2038,2)]);v=self.dg(0x2038)
                    v=(v-1 if v>0 else 20) if delta<0 else (v+1 if v<20 else 0)
                    self.setdg(0x2038,v)
                    if v==19:self.setdg(0x2038,v+delta)
                    self.invoke('track',[15,self.dg(0x2038,2)])
            if inp&(0x20|0x2000):
                if self.dg(0x2038)==20:break
                self.call('kaja',[256]);sel=self.dg(0x2038)
                self.call('snd-load',[self.dg(0x646+4*sel,2),self.dg(0x648+4*sel,2),0x600]);self.call('kaja',[0])
                self.setdg(0x693,self.dg(0x2038));self.invoke('comment',[self.dg(0x2038)]);self.invoke('flip');self.invoke('comment',[self.dg(0x2038)])
            if inp&0x1000:break
            if inp:self.release()
            else:self.invoke('flip')
        self.release();self.invoke('free');self.invoke('bg_free');self.port(0xa4,0);self.port(0xa6,0)
        self.call('graph-clear');self.port(0xa6,1);self.port(0xa6,0)


class MusicProbe(Probe):
    """Execute all original instructions, validating complete near/far caller frames."""
    def __init__(self,mz,s):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR, UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,(struct.unpack_from('<H',image,at)[0]+0x2000)&65535)
        self.uc.mem_write(0x20000,bytes(image));self.code=(0x2000+CS)*16;self.data=(0x2000+DS)*16;self.stack=0x40000
        self.uc.mem_write(self.stack,bytes([0xa5])*65536)
        for i,seg in enumerate((0x5000,0x6000,0x6400,0x6800,0x6c00,0xa800,0xb000,0xb800,0xe000)):
            self.uc.mem_write(seg*16,bytes((j*17+i*31+11)&255 for j in range(65536 if i in (0,5,6,7,8) else 16384)))
        for a,v,z in ((0x692,s['initialized'],1),(0x693,s['track'],1),(0x2038,s['sel'],1),(0x2039,s['page'],1),
                      (0x203a,0x5000,2),(0x312,s['seed'],4)):
            self.uc.mem_write(self.data+a,v.to_bytes(z,'little'))
        self.uc.mem_write(self.data+0x204c,bytes([0x7e])*840)
        for i,seg in enumerate((0xa800,0xb000,0xb800,0xe000)):
            self.uc.mem_write(self.data+0x19fa+4*i,struct.pack('<HH',s['vram_offset'],seg))
            self.uc.mem_write(self.data+0x203c+4*i,struct.pack('<HH',s['bg_offset'],0x6000+0x400*i))
        self.uc.mem_write(self.data+0x1f70,bytes(range(40)))
        for i in range(16):
            x,y,vx,vy=s['centers'][i%len(s['centers'])]
            self.uc.mem_write(self.data+0x1f98+4*i,struct.pack('<HH',x&65535,y&65535))
            self.uc.mem_write(self.data+0x1fd8+4*i,struct.pack('<HH',vx&65535,vy&65535))
        self.uc.mem_write(self.data+0x2018,bytes((13*i+251)&255 for i in range(16)))
        self.uc.mem_write(self.data+0x2028,bytes((i*37)&255 for i in range(16)))
        self.s=s;self.meta=analyze(mz.program_image);self.events=[];self.writes=[];self.reads=[];self.external=[];self.native=Counter()
        self.inputs=0;self.allocations=0;self.seek=0;self.visited=set();self.frames=[];self.top=None;self.errors=[];self.position=None
        self.entry_specs={(r['segment'],r['offset']):r for r in self.meta['bodies']}
        for r,v in dict(DS=0x2000+DS,SS=0x4000,ES=0x3333,BP=0x7777,SI=0x1357,DI=0x2468,BX=0xbeef).items():self.set(r,v)
        self.set('EFLAGS',2|(0x200 if s['if'] else 0)|(0x400 if s['df'] else 0))
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            seg=self.get('CS')-0x2000;off=address-self.get('CS')*16;position=(seg,off);self.position=position
            if self.get('SS')!=0x4000:raise ValueError('Music Room stack segment alias')
            if address==self.code+0xff00:
                f=self.top
                if seg!=CS or self.get('SP')!=f['sp']+f['width']+f['cleanup'] or self.frames or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('Music Room terminal frame differs')
                self.stop=True;uc.emu_stop();return
            if self.frames and position==self.frames[-1]['ret']:
                f=self.frames.pop()
                if self.get('SP')!=f['sp']+f['width']+f['cleanup'] or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('Music Room native callback return differs')
            if position in self.meta['bounds']:
                self.visited.add(position)
                # Unicorn 1.0.2rc4 misexecutes RETF when a memory-read hook is
                # installed, even outside the stack. Record the actual bulk
                # load operands at these attested instruction boundaries.
                if seg==CS and off in BULK_LOADS:
                    self.reads.append((self.get('ES')*16+self.get('BX'),4))
                if position==(CS,0xd0d) and self.get('CX'):
                    self.reads.append((self.get('DS')*16+self.get('SI'),2))
                if position in self.meta['entries']:
                    row=self.entry_specs[position];self.native[row['name']]+=1
                    if self.entered:
                        sp=self.get('SP');width=4 if row['far'] else 2
                        words=struct.unpack('<'+'H'*(width//2),uc.mem_read(self.stack+sp,width));ret=(words[1]-0x2000 if width==4 else seg,words[0]);caller=self.meta['calls'].get(ret)
                        if not caller or caller['destination']!=position:raise ValueError('Music Room native caller differs')
                        self.frames.append(dict(ret=ret,sp=sp,width=width,cleanup=row['cleanup'],saved={r:self.get(r) for r in ('BP','SI','DI','DS')}))
                    self.entered=True
                if position in self.meta['returns']:
                    f=self.frames[-1] if self.frames else self.top;sp=self.get('SP');width=f['width']
                    words=struct.unpack('<'+'H'*(width//2),uc.mem_read(self.stack+sp,width));ret=(words[1]-0x2000 if width==4 else seg,words[0])
                    if sp!=f['sp'] or ret!=f['ret'] or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('Music Room native return stack differs')
                return
            if position not in MODELS:raise ValueError('Music Room escape/operand boundary differs: '+str(position))
            name,count,cleanup=MODELS[position];sp=self.get('SP');words=struct.unpack('<HH',uc.mem_read(self.stack+sp,4));ret=(words[1]-0x2000,words[0]);caller=self.meta['calls'].get(ret)
            if not caller or caller['destination']!=position:raise ValueError('Music Room foreign caller frame differs')
            args=list(struct.unpack('<'+'H'*(count//2),uc.mem_read(self.stack+sp+4,count))) if count else []
            event=dict(name=name,args=args);reply=s['reply']
            if name in ('text','open','pi-load','snd-load'):
                if args[1]!=0x2000+DS:raise ValueError('Music Room filename/text segment differs')
                raw=bytes(uc.mem_read(args[1]*16+args[0],256));event['string']=raw[:raw.index(0)+1].hex()
            if name=='polygon':
                if args[1:]!=[0x1f70,0x2000+DS] or args[0] not in (3,4,5,6):raise ValueError('Music Room polygon pointer/count differs')
                event['points']=bytes(uc.mem_read(self.data+0x1f70,4*(args[0]+1))).hex()
            if name=='palette':event['tone']=int.from_bytes(uc.mem_read(self.data+0x2d4,2),'little')
            if name=='alloc':reply=s['alloc'][self.allocations%5];self.allocations+=1;event['reply']=reply
            if name=='seek':self.seek=signed(args[1]);event['signed_offset']=self.seek
            if name=='read':
                if args!=[840,0x204c,0x2000+DS] or not 0<=s['read']<=840:raise ValueError('Music Room comment read fixture differs')
                block=bytes(((self.seek+j)*13+71)%255+1 for j in range(s['read']));event['bytes']=block.hex();uc.mem_write(self.data+0x204c,block)
                self.external.extend((self.data+0x204c+j,1,v) for j,v in enumerate(block))
            if name=='input':
                if self.inputs>=len(s['inputs']):raise ValueError('Music Room input fixture exhausted')
                event['input']=s['inputs'][self.inputs];self.inputs+=1;uc.mem_write(self.data+0x1aa6,struct.pack('<H',event['input']));self.external.append((self.data+0x1aa6,2,event['input']))
            self.events.append(event);self.set('AX',reply);self.set('EFLAGS',(self.get('EFLAGS')&~1)|s['cf'])
            self.set('SP',sp+4+cleanup);self.set('CS',words[1]);self.set('IP',words[0])
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            dg=address-self.data
            allowed=(size==1 and (dg in (0x692,0x693,0x2038,0x2039) or 0x2018<=dg<0x2038 or dg in range(0x2074,0x2394,42))) or (size==2 and (dg in (0x312,0x314,0x2d4,0x203a) or 0x1f70<=dg<0x2018 or 0x203c<=dg<0x204c))
            allowed=allowed or (size in (2,4) and 0x50000<=address and address+size<=0xf0000)
            if not allowed or self.position not in self.meta['bounds']:raise ValueError('Music Room complete native store span differs')
            self.writes.append((address,size,value&((1<<(size*8))-1)))
        def intr(*args):raise ValueError('Music Room unexpected interrupt')
        def output(uc,port,width,value,user):
            if port not in (0xa4,0xa6) or width!=1 or self.position not in self.meta['bounds']:raise ValueError('Music Room port caller/width differs')
            self.events.append(dict(name='out',port=port,width=width,value=value))
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
        if not self.stop:raise ValueError('Music Room terminal/budget differs')


def scenario(**kw):
    s=dict(initialized=0,track=0,sel=0,page=1,seed=1,read=840,vram_offset=0,bg_offset=0,
           alloc=[0x5000,0x6000,0x6400,0x6800,0x6c00],inputs=[0,0x1000,0],reply=0,cf=0,
           centers=[(0,7990,-1,16),(639,8000,1,32),(320,-1600,0,80),(32767,32760,1,80)],**{'if':True,'df':False})
    s.update(kw);return s


def observe(mz,name,s,args=(),sequence=None):
    p=MusicProbe(mz,s);before=bytes(p.uc.mem_read(0,0x100000));spec=MusicSpec(before,p.data,s)
    for n,a in sequence or [(name,args)]:spec.invoke(n,a);p.run(n,a)
    for label,a,b in [('events',p.events,spec.events),('writes',p.writes,spec.writes),('reads',p.reads,spec.reads),('external',p.external,spec.external),('native',p.native,spec.native)]:
        if a!=b:
            if isinstance(a,list):
                i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)));detail=str((i,a[i:i+1],b[i:i+1],len(a),len(b)))
            else:detail=str((a,b))
            raise ValueError('Music Room independent scalar '+label+' differs: '+name+' '+detail)
    actual=bytes(p.uc.mem_read(0,0x100000))
    if actual[:p.stack]!=spec.memory[:p.stack] or actual[p.stack+65536:]!=spec.memory[p.stack+65536:]:raise ValueError('Music Room whole physical preservation differs')
    if bool(p.get('EFLAGS')&0x200)!=s['if'] or bool(p.get('EFLAGS')&0x400)!=s['df']:raise ValueError('Music Room IF/DF differs')
    digest=lambda x:sha(json.dumps(x,separators=(',',':')).encode())
    return dict(function=name,args=list(args),sequence=sequence,scenario=s,events=p.events,native_entries=dict(p.native),
                stores=len(p.writes),stores_sha256=digest(p.writes),reads=len(p.reads),reads_sha256=digest(p.reads),
                external_inputs=p.external,visited=[list(a) for a in sorted(p.visited)],memory_before_sha256=sha(before),memory_after_sha256=sha(spec.memory))


def matrix(mz):
    rows=[]
    for irq,df in itertools.product((False,True),repeat=2):
        flags={'if':irq,'df':df}
        for sel in (0,18,19,20):rows.append(observe(mz,'track',scenario(page=255,**flags),[0xf3a5,sel]))
        rows.append(observe(mz,'tracklist',scenario(**flags),[255]))
        for name in ('snap','free','put','bg_snap','bg_free','unput','comment'):
            rows.append(observe(mz,name,scenario(vram_offset=19,bg_offset=17,reply=0xffff,cf=1,**flags),[18] if name=='comment' else []))
        for count,origin,radius in ((0,32767,0),(-1,-32768,-32768),(3,-32768,-1),(4,32767,32767),(5,-9,0),(6,0,96),(9,640,-96)):
            rows.append(observe(mz,'build',scenario(**flags),[255,count&65535,radius&65535,(-1617)&65535,origin&65535,0x1f70]))
        for track,n in itertools.product((0,18,39,40,255,32767,65535),(0,41,839,840)):
            rows.append(observe(mz,'load',scenario(read=n,**flags),[track]))
        for seed in (0,1,2,0x7fffffff,0xffffffff):
            rows.append(observe(mz,'polygons',scenario(seed=seed,**flags)))
            rows.append(observe(mz,'polygons',scenario(seed=seed,initialized=255,**flags),sequence=[('polygons',[]),('polygons',[])]))
        rows.append(observe(mz,'flip',scenario(initialized=1,**flags)))
        # All control bits, wrap/empty-line paths, held/released input and
        # shot+cancel processing. Each input list explicitly ends in release.
        for track,inp in ((0,1),(20,1),(18,2),(20,2),(1,3),(0,0x20),(18,0x2000),(20,0x20),(1,0x3023)):
            inputs=[1,1,0,inp,inp,0,0,0x1000,0x1000,0]
            if track==20 and inp==0x20:inputs=[0,inp,inp,0]
            if inp&0x1000:inputs=[0,inp,inp,0]
            rows.append(observe(mz,'music',scenario(track=track,inputs=inputs,initialized=1,**flags)))
        rows.append(observe(mz,'music',scenario(inputs=[0,0,0x8000,0,0x1000,0],**flags)))
        rows.append(observe(mz,'music',scenario(initialized=1,inputs=[0,0x2020,0,0,0x1000,0,0,0x1000,0],**flags),sequence=[('music',[]),('music',[])]))
        print('Music Room profile',flags,'cases',len(rows),flush=True)
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('Music Room source parent proof differs')
    parent=json.loads(raw);inputs=dict(parent['inputs']);inputs[PROOF]=sha(raw)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('Music Room prerequisite differs: '+p)
    for p in ('config/targets.toml','scripts/review_th03_op_music.py','scripts/probe_th03_unicorn_far_return.py','scripts/review_th03_mainl_cutscene.py','scripts/review_th03_decoded_code.py',
              'scripts/inventory_rec98_th03.py','scripts/replay_th03_op_score.py','scripts/lib/omf.py','scripts/lib/pc98.py','scripts/lib/targets.py'):inputs[p]=sha((ROOT/p).read_bytes())
    artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-op');stored=read_verified_artifact(ROOT,artifact)
    frozen=frozen_files(REVISION);target=parse_mz((ROOT/DECODED).read_bytes());observations=[]
    paths=[DECODED]+[str(Path(PROOF).parent/f'round{r["number"]}'/'source/bin/th03/op.exe') for r in parent['rounds']]
    for index,path in enumerate(paths):
        raw=(ROOT/path).read_bytes();inputs[path]=sha(raw);mz=parse_mz(raw)
        if not mz.valid:raise ValueError('Music Room invalid decoded MZ')
        meta=analyze(mz.program_image);o=dict(path=path,bodies=meta['bodies'])
        if index:
            round=parent['rounds'][index-1];tree=Path(path).parents[2];o['source_lineage']={}
            if inputs[path]!=round['products']['bin/th03/op.exe']:raise ValueError('Music Room parent product differs')
            for p in PROVIDERS:
                cp=str(tree/p);raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw)
                if raw!=frozen[p]:raise ValueError('Music Room frozen provider differs: '+p)
                o['source_lineage'][p]=dict(frozen_sha256=sha(frozen[p]),cached_sha256=sha(raw))
            cp=str(tree/'obj/th03/op_music.obj');raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw);obj=describe_omf(raw)
            if not obj['valid'] or obj['dependency_timestamp_normalized_sha256']!=round['all_objects']['obj/th03/op_music.obj']:raise ValueError('Music Room OMF differs')
            o['object']=dict(path=cp,normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'])
            cp=str(tree/'obj/th03/op.map');raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw)
            carrier=next(c for c in code_rows(raw.decode(),len(mz.program_image)) if c['module']=='th03/op_music.cpp' and c['size'])
            if (carrier['segment'],carrier['offset'],carrier['size'])!=(CS,0xc1e,2244):raise ValueError('Music Room original carrier differs')
            o['comparisons']={}
            for name,seg,a,z,c,f in RANGES:
                comp=extent_observation(target,mz,dict(segment=seg,offset=a,start=seg*16+a,size=z));o['comparisons'][name]=comp
                if not comp['ordered_relocations_equal'] or (name!='put' and not comp['raw_slice_equal']):raise ValueError('Music Room complete raw/ordered inequality')
                if name=='put' and comp['raw_slice_equal']:raise ValueError('Music Room two-byte encoding failure disappeared')
            if mz.program_image[DS*16+0x5f2:DS*16+0x9e2]!=target.program_image[DS*16+0x5f2:DS*16+0x9e2]:raise ValueError('Music Room native text/statics/data differ')
        o['cpu']=matrix(mz);visited={tuple(a) for r in o['cpu'] for a in r['visited']}
        o['coverage']=dict(instructions=len(meta['bounds']),visited=len(meta['bounds']&visited),unvisited=[list(a) for a in sorted(meta['bounds']-visited)])
        if o['coverage']['unvisited']:raise ValueError('Music Room native coverage incomplete: '+str(o['coverage']['unvisited']))
        if index and normalized_contracts(o['cpu'])!=normalized_contracts(observations[0]['cpu']):raise ValueError('Music Room target/cold contracts differ')
        observations.append(o);print('Reviewed',path,len(o['cpu']),'cases',o['coverage'],flush=True)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('Music Room input changed: '+p)
    final=frozen_files(REVISION)
    if any(final[p]!=frozen[p] for p in PROVIDERS) or read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('Music Room frozen/canonical target changed')
    from probe_th03_unicorn_far_return import probe
    read_hook_control=probe()
    report=dict(read_hook_control=read_hook_control,kind='th03-op-complete-music-room-native-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,observations=observations,
                tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),new_decoded_bytes=2244,eligible_decoded_bytes=2214,
                diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,new_build=False,
                notes='Complete2244-byte14-function carrier; native IRAND42/POLAR26 context only, no duplicate coverage. Flat writable memory and explicit foreign file/heap/input/graphics/timing/sound replies. Full ordered native stores/bulk reads/calls/ports and physical memory outside64KiBstack checked. Original nopoly_B_put30 retains two raw encoding inequalities; REP MOVSW does not clear DF. Signed16 comment seek multiplication wraps; unchecked short reads preserve stale bytes except20 terminators. Polygon initialization and song choice persist across calls. Actual graphics/banking/ROM/heap/DOS/devices/ISR/resource/canonicalstorage/fullproduct/exact remain open.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n');print('PASS complete OP Music Room diagnostics; exact open')


if __name__=='__main__':main()
