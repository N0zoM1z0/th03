#!/usr/bin/env python3
"""Review the complete OP entry carrier and native configuration/random helpers."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import version
import itertools
import json
from pathlib import Path
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from inventory_rec98_th03 import frozen_files
from lib.pc98 import parse_mz
from lib.omf import describe_omf
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact
from review_th03_decoded_code import code_rows,extent_observation
from review_th03_mainl_cutscene import Probe,REVISION,sha
import review_th03_op_menu as menu
from replay_th03_op_score import normalized_contracts

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/th03-op-menu/sol-op-menu-source-20261006/receipt.json'
PROOF_SHA='088915e25bf97951160b090e9d4a2d5ea5c139731aa903031b0fdc1a944c5344'
CS,DS=menu.CS,menu.DS
RANGES=[('cfg_load',CS,8,120,0,False),('cfg_save',CS,0x80,67,0,False),('cfg_exit',CS,0xc3,84,0,False),
 ('story',CS,0x117,390,0,False),('vs_choice',CS,0x29d,66,4,False),('vs',CS,0x2df,365,0,False),
 ('demo',CS,0x44c,202,0,False),('wait',CS,0x516,105,0,False),('score',CS,0x57f,94,0,False),
 *[(n,CS,a,z,c,False) for n,a,z,c in menu.RANGES],('entry',CS,0xb17,263,0,True),
 ('irand',0,0x1d12,42,0,True),('scopy',0,0x337e,28,8,True)]
MODELS=dict(menu.MODELS)
for a in (0x117,0x2df,0x516,0x57f):MODELS.pop((CS,a))
# name, argument bytes, far frame, callee cleanup (C declarations leave args).
MODELS={p:(n,c,f,c) for p,(n,c,f) in MODELS.items()}
MODELS.update({(CS,0x249a):('select-story',0,False,0),(CS,0x2188):('select-2p',0,False,0),
 (CS,0x231f):('select-cpu',0,False,0),(0,0xf1a):('restore',0,True,0),
 (0xbeb,0x112):('game-exit',0,True,0),(0,0x9119):('execl',12,True,0),
 (0,0x536):('black',2,True,2),(0xbeb,0xad6):('input',0,True,0),
 (0xbeb,0x2ee):('frame',2,True,2),(0,0x28d8):('super',6,True,6),
 (CS,0x180a):('column',2,False,2),(0,0x269a):('super-free',0,True,0),
 (0,0x10fe):('graph',0,True,0),(0,0x2ac6):('respal-create',0,True,0),
 (0,0x688):('puts',4,True,4),(0,0x952e):('getch',0,True,0),
 (0xbeb,0x571):('init',4,True,0),(0,0xef6):('backup',0,True,0),
 (0,0xf36):('gaiji-entry',4,True,4),(CS,0x1a8d):('cdg1',0,False,0),
 (CS,0x1aef):('cdg3',0,False,0),(CS,0x14e2):('intro',0,False,0),
 (0xbeb,8):('exit-dos',0,True,0),(0,0x2b3c):('respal-free',0,True,0),
 (0,0x9a8):('open',4,True,4),(0,0x8f4):('read',6,True,6),(0,0x888):('close',0,True,0),
 (0,0x7c8):('append',4,True,4),(0,0x9e4):('seek',6,True,6),(0,0xa26):('write',6,True,6)})
CALLS=dict(menu.CALLS)
CALLS.update({0x10:(0,0x9a8),0x1c:(0,0x8f4),0x21:(0,0x888),0x40:(0xbeb,0x4a),
 0x88:(0,0x7c8),0x92:(0,0x9e4),0xb7:(0,0xa26),0xbc:(0,0x888),0xd3:(0,0x337e),
 0xdc:(0,0x7c8),0xe6:(0,0x9e4),0x10b:(0,0xa26),0x110:(0,0x888),0x14d:(CS,0x249a),0x185:(0,0x1d12),
 0x270:(CS,0x80),0x273:(0,0xf1a),0x27b:(0xbeb,0x553),0x280:(0xbeb,0x112),0x290:(0,0x9119),
 0x2d4:(0,0xfcc),0x2f3:(0,0x21f4),0x2f8:(CS,0x17af),0x306:(CS,0x29d),0x30f:(CS,0x29d),
 0x318:(CS,0x29d),0x31b:(0xbeb,0xad6),0x330:(CS,0x29d),0x347:(CS,0x29d),0x356:(CS,0x29d),
 0x36d:(CS,0x29d),0x384:(0xbeb,0x2ee),0x3e6:(CS,0x2188),0x3ef:(CS,0x231f),0x41f:(CS,0x80),
 0x422:(0,0xf1a),0x42a:(0xbeb,0x553),0x42f:(0xbeb,0x112),0x43f:(0,0x9119),0x4e6:(0,0x536),
 0x4eb:(CS,0x80),0x4ee:(0,0xf1a),0x4f6:(0xbeb,0x553),0x4fb:(0xbeb,0x112),0x50b:(0,0x9119),
 0x524:(0xbeb,0xad6),0x539:(CS,0x44c),0x53e:(0xbeb,0x2ee),0x552:(0,0x28d8),0x55d:(CS,0x180a),
 0x567:(0,0x28d8),0x56e:(0xbeb,0x2ee),0x5ab:(CS,0x80),0x5ae:(0,0xf1a),0x5b6:(0xbeb,0x553),
 0x5bb:(0,0x269a),0x5c0:(0xbeb,0x112),0x5d0:(0,0x9119),0xb1a:(0,0x10fe),0xb1f:(0,0x21f4),
 0xb24:(0,0x2ac6),0xb34:(0,0x688),0xb3d:(0,0x688),0xb46:(0,0x688),0xb4b:(0,0x952e),0xb56:(0xbeb,0x571),
 0xb71:(0,0xf36),0xb68:(0,0xef6),0xb76:(CS,8),0xb8b:(CS,0x1a8d),0xb8e:(CS,0x1aef),0xb91:(CS,0x1ac3),
 0xb94:(CS,0x2df),0xba2:(CS,0x14e2),0xbb9:(CS,0x1708),0xbbc:(CS,0x516),0xbca:(CS,0x7e0),0xbcd:(CS,0x1ac3),
 0xbd2:(0xbeb,0xad6),0xbe6:(CS,0x7e0),0xbeb:(CS,0x903),0xbf9:(0xbeb,0x2ee),0xc05:(CS,0xc3),
 0xc08:(0,0xf1a),0xc0d:(0,0x21f4),0xc12:(0xbeb,8),0xc17:(0,0x2b3c)})
PROVIDERS=list(dict.fromkeys([*menu.PROVIDERS,'th03/playchar.hpp','th03/score.hpp','th03/formats/cfg_impl.hpp',
 'th03/formats/cfg.hpp','th02/formats/cfg.hpp','th01/core/initexit.hpp','th03/core/initexit.h',
 'th03/shiftjis/main.hpp','th03/shiftjis/fns.hpp','th02/op/m_music.hpp','th02/hardware/frmdelay.h','libs/master.lib/random.asm','libs/master.lib/rand[data].asm']))


def analyze(image):
    base=menu.analyze(image);d=Cs(CS_ARCH_X86,CS_MODE_16);d.detail=True
    bounds={(CS,a) for a in base['bounds']};entries={(CS,a):n for a,n in base['entries'].items()}
    returns={(CS,a):c for a,c in base['returns'].items()};calls={(CS,a):v for a,v in base['calls'].items()}
    rows=[dict(r,segment=CS,far=False) for r in base['bodies']]
    for name,seg,a,z,cleanup,far in RANGES:
        if (seg,a) in entries:continue
        body=image[seg*16+a:seg*16+a+z];ins=list(d.disasm(body,a));local={i.address for i in ins}
        expected=('retf' if far else 'ret',str(cleanup) if cleanup else '')
        if len(body)!=z or sum(i.size for i in ins)!=z or (ins[-1].mnemonic,ins[-1].op_str)!=expected:raise ValueError('OP entry complete native body/return differs: '+name)
        entries[(seg,a)]=name;bounds.update((seg,i.address) for i in ins);edges=[]
        for i in ins:
            if i.mnemonic in ('ret','retf'):
                if (i.mnemonic,i.op_str)!=expected:raise ValueError('OP entry interior return differs')
                returns[(seg,i.address)]=cleanup
            if i.mnemonic in ('int','in','out','iret'):raise ValueError('OP entry unexpected device instruction')
            if not(i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('OP entry unknown indirect edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (seg,i.operands[0].imm)
            if i.mnemonic in ('call','lcall'):
                if seg!=CS or CALLS.get(i.address)!=dest:raise ValueError('OP entry unknown foreign/native caller')
                calls[(seg,i.address+i.size)]=dict(site=i.address,destination=dest)
            elif i.mnemonic=='ljmp' or dest!=(seg,dest[1]) or dest[1] not in local:raise ValueError('OP entry branch enters operand/neighbor')
            edges.append(dict(site=i.address,kind=i.mnemonic,destination=list(dest)))
        rows.append(dict(name=name,segment=seg,offset=a,size=z,cleanup=cleanup,far=far,instructions=len(ins),sha256=sha(body),edges=edges))
    if set(CALLS)!={v['site'] for v in calls.values() if v['destination'] is not None}:raise ValueError('OP entry complete call closure differs')
    if any(v['destination'] is not None and v['destination'] not in entries and v['destination'] not in MODELS for v in calls.values()):raise ValueError('OP entry missing callee model')
    return dict(bounds=bounds,entries=entries,returns=returns,calls=calls,bodies=rows,tables=base['tables'])


PROLOGUE={'cfg_load':12,'cfg_save':10,'cfg_exit':10,'story':8,'vs_choice':6,'vs':6,'demo':4,'wait':4,'score':4,
          'main':4,'option':4,'move':2,'main_choice':6,'option_choice':6,'entry':2,'irand':0,'scopy':8}


class EntrySpec(menu.MenuSpec):
    def __init__(self,before,data,resident,s):
        super().__init__(before,data,resident,s);self.context=[];self.inputs=0;self.df=s['df'];self.result=None
    def native_call(self,name,args=(),top=False):
        sp=0xffd0 if top else self.context[-1][1]-PROLOGUE[self.context[-1][0]]-2*len(args)-(4 if name in ('irand','scopy') else 2)
        self.context.append((name,sp))
        try:getattr(self,name)(args)
        finally:self.context.pop()
    def setr(self,a,v,z=1):self.put(self.resident+a,z,v)
    def res(self,a,z=1):return self.get(self.resident+a,z)
    def call(self,name,args=()):
        if name in ('story','vs','score','wait'):
            self.native_call(name,args);return
        event=dict(name=name,args=list(args))
        if name in ('gaiji','text','puts','init','gaiji-entry','open','append','execl'):
            pairs=[(1,2)] if name in ('gaiji','text') else [(0,1)]
            if name=='execl':pairs=[(0,1),(2,3)]
            event['strings']=[]
            for offi,segi in pairs:
                raw=self.memory[args[segi]*16+args[offi]:args[segi]*16+args[offi]+160];event['strings'].append(bytes(raw[:raw.index(0)+1]).hex())
        if name=='input':
            if self.inputs>=len(self.s['inputs']):raise ValueError('OP entry input fixture exhausted')
            value=self.s['inputs'][self.inputs];self.inputs+=1;event['input']=value
            self.put(self.data+menu.INPUT,2,value,True)
            if self.inputs==self.s.get('corrupt_poll'):
                self.put(self.data+menu.INOPT,1,2,True);self.put(self.data+menu.QUIT,1,1,True)
        if name.startswith('select-'):
            event['reply']=self.s['selection_reply']
            if name=='select-story':self.put(self.resident+0xc,1,self.s['selected_char'],True)
        if name=='determine':self.put(self.data+menu.ACTIVE,1,self.s['mode_active'],True)
        if name=='read':
            event['bytes']=bytes(self.s['cfg'][:self.s['read']]).hex()
        if name=='write':
            count=args[0];event['defined_bytes']=bytes([self.res(0x15),self.res(0x16),self.res(0xb)]).hex()
            if count==8:event['defined_bytes']+='0000000000'
            elif count!=4:raise ValueError('OP entry scalar file write count differs')
        self.events.append(event)
    def cfg_load(self,args):
        self.native['cfg_load']+=1;sp=self.context[-1][1];buf=sp-10
        self.call('open',[0x166,0x2000+DS]);self.call('read',[8,buf,0x4000]);self.call('close')
        cfg=list(self.s['cfg'][:self.s['read']])+[0xa5]*(8-self.s['read']);seg=cfg[5]+cfg[6]*256
        self.setdg(menu.RESIDENT+2,seg,2);self.setdg(menu.RESIDENT,0,2);self.resident=seg*16
        self.setr(0x15,cfg[0]);self.call('determine');self.setdg(menu.DISABLED,0)
        if not self.dg(menu.ACTIVE):self.setr(0x15,0);self.setdg(menu.DISABLED,1)
        elif cfg[0]==0:self.setdg(menu.ACTIVE,0)
        self.setr(0x16,cfg[1]);self.setr(0xb,cfg[2])
    def cfg_write(self,exit):
        name='cfg_exit' if exit else 'cfg_save';self.native[name]+=1;sp=self.context[-1][1]
        if exit:self.native_call('scopy',[0x91,0x2000+DS,sp-10,0x4000])
        self.call('append',[0x166,0x2000+DS]);self.call('seek',[0,0,0]);self.call('write',[8 if exit else 4,sp-10,0x4000]);self.call('close')
    def cfg_save(self,args):self.cfg_write(False)
    def cfg_exit(self,args):self.cfg_write(True)
    def scopy(self,args):self.native['scopy']+=1;self.df=False
    def reset_scores(self):
        for i in range(16):self.setr(0x18+i,0)
    def handoff(self,free=False):
        self.native_call('cfg_save');self.call('restore');self.call('kaja',[256])
        if free:self.call('super-free')
        self.call('game-exit');self.call('execl',[0x16f,0x2000+DS,0x16f,0x2000+DS,0,0]);self.result=0
    def irand(self,args):
        self.native['irand']+=1;n=(self.get(self.data+0x312,4)*22695477+1)&0xffffffff
        self.put(self.data+0x312,2,n&65535);self.put(self.data+0x314,2,n>>16);self.result=(n>>16)&0x7fff
    def story(self,args):
        self.native['story']+=1
        for a,v in ((0x39,0),(0x17,0),(0x33,0),(0xe,0),(0xf,1),(0x28,1),(0x34,2),(0x35,0),(0xd,255)):self.setr(a,v)
        self.call('select-story')
        if self.s['selection_reply']&255:self.result=1;return
        char=self.res(0xc);index=int((char-1)/2);stage7=self.get(self.data+0xa0+index)
        self.put(self.data+0x312,4,self.res(0x10,4))
        for stage in range(6):
            while True:
                self.native_call('irand');candidate=self.result%7
                if not self.get(self.data+0x99+candidate) and candidate!=stage7:break
            self.setdg(0x99+candidate,1);pal=2*candidate+1;self.setr(0x29+stage,pal)
            if pal==char:self.setr(0x29+stage,pal+1)
        self.setr(0xd,self.res(0x29));self.setr(0x2f,2*stage7+1);self.setr(0x30,15)
        if char==15:self.setr(0x30,16)
        self.setr(0x31,17)
        if char==17:self.setr(0x31,18)
        if any(int((self.res(0x29+i)-1)/2)>=9 for i in range(9)):raise ValueError('OP entry scalar invalid opponent retries; fixture withheld')
        self.reset_scores();self.setr(0x36,3);self.setr(0x37,0);self.setr(0x38,70+self.res(0xb)*25);self.handoff()
    def vs_choice(self,args):
        self.native['vs_choice']+=1;sel=self.signed_word(args[1]);line=1 if sel==0 else 2 if sel==1 else 3
        self.call('gaiji',[args[0],[0xa9,0xb2,0xbb][line-1],0x2000+DS,17+line,27])
    def vs(self,args):
        self.native['vs']+=1
        if self.res(0x28)<128:
            self.call('clear');self.call('expand');sel=0
            for i in range(3):self.native_call('vs_choice',[0xe1 if i==0 else 1,i])
            prev=0
            while True:
                self.call('input');inp=self.get(self.data+menu.INPUT,2)
                if prev==0:
                    if inp&1:
                        self.native_call('vs_choice',[1,sel]);sel=(sel-1)%3;self.native_call('vs_choice',[0xe1,sel])
                    if inp&2:
                        self.native_call('vs_choice',[1,sel]);sel=(sel+1)%3;self.native_call('vs_choice',[0xe1,sel])
                    if inp&(0x20|0x2000):break
                prev=inp;self.call('frame',[1])
        else:sel=self.res(0x28)-128
        self.setr(0xe,int(sel==2));self.setr(0xf,int(sel!=1))
        for a,v in ((0x39,0),(0x17,0),(0x33,0),(0x28,128+sel),(0x35,0)):self.setr(a,v)
        self.call('select-2p' if sel==1 else 'select-cpu')
        if self.s['selection_reply']&255:self.setr(0x28,0);self.result=1;return
        self.reset_scores();self.handoff()
    def demo(self,args):
        self.native['demo']+=1;self.setr(0xe,1);self.setr(0xf,1);self.setr(0x39,self.res(0x39)+1)
        if self.res(0x39)>4:self.setr(0x39,1)
        for a,v in ((0x17,0),(0x33,0),(0x28,127),(0x35,0)):self.setr(a,v)
        number=self.res(0x39);self.setr(0xc,self.get(self.data+0xc2+2*number));self.setr(0xd,self.get(self.data+0xc3+2*number))
        self.setr(0x10,self.get(self.data+0xc8+4*number,4),4)
        self.reset_scores();self.call('black',[1]);self.handoff()
    def wait(self,args):
        self.native['wait']+=1;self.setdg(menu.INPUT,0,2);frame=0
        while self.get(self.data+menu.INPUT,2)==0:
            self.call('input');self.setr(0x10,self.res(0x10,4)+1,4);frame=(frame+1)&65535
            if self.signed_word(frame)>520:self.native_call('demo')
            self.call('frame',[1])
        self.call('super',[0,256,160])
        for left in range(176,288,8):self.call('column',[left]);self.call('super',[2,256,left]);self.call('frame',[1])
    def score(self,args):
        self.native['score']+=1
        for a,v in ((0x33,255),(0x35,1),(0x28,0)):self.setr(a,v)
        self.reset_scores();self.handoff(True)
    def entry(self,args):
        self.native['entry']+=1;self.call('graph');self.call('clear');self.call('respal-create')
        if self.get(self.data+0x2c8,2):
            for ptr in (0x17e,0x1a8,0x1e8):self.call('puts',[ptr,0x2000+DS])
            self.call('getch');return
        self.call('init',[0x225,0x2000+DS])
        if self.s['init_reply']:
            self.call('puts',[0x231,0x2000+DS]);self.call('getch');return
        self.call('backup');self.call('gaiji-entry',[0x26c,0x2000+DS]);self.native_call('cfg_load')
        if self.res(0x28)>=128 and self.res(0x39)==0:
            self.call('cdg1');self.call('cdg3');self.call('cdg2');self.native_call('vs')
        if self.res(0x37):self.setr(0x37,0);self.call('fade')
        else:self.call('intro');self.setr(0x37,1)
        self.native_call('wait');self.setdg(menu.INOPT,0);self.setdg(menu.INPUT,0,2);self.native_call('main');self.call('cdg2')
        while not self.dg(menu.QUIT):
            self.call('input');which=self.dg(menu.INOPT)
            if which in (0,1):self.native_call('main' if which==0 else 'option')
            self.setr(0x10,self.res(0x10,4)+1,4);self.call('frame',[1])
        self.native_call('cfg_exit');self.call('restore');self.call('clear');self.call('exit-dos');self.call('respal-free')
    # Menu methods retain their independent scalar checks; establish native
    # stack contexts for their direct Pascal helper calls.
    def move(self,args):
        if self.context[-1][0]=='move':return super().move(args)
        return self.native_call('move',args)
    def draw(self,which,sel,atrb):
        name=which+'_choice'
        if self.context[-1][0]==name:return super().draw(which,sel,atrb)
        # Two Pascal arguments are pushed, then a near return word.
        self.context.append((name,self.context[-1][1]-PROLOGUE[self.context[-1][0]]-6))
        try:return super().draw(which,sel,atrb)
        finally:self.context.pop()


class EntryProbe(Probe):
    def __init__(self,mz,s):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,(struct.unpack_from('<H',image,at)[0]+0x2000)&65535)
        self.uc.mem_write(0x20000,bytes(image));self.code=(0x2000+CS)*16;self.data=(0x2000+DS)*16;self.stack=0x40000
        self.uc.mem_write(self.stack,b'\xa5'*65536);self.resident=0x60000+s['offset']
        self.uc.mem_write(0x60000,bytes((i*17+31)&255 for i in range(512)))
        self.uc.mem_write(self.data+menu.RESIDENT,struct.pack('<HH',s['offset'],0x6000))
        for a,k in ((0xb,'rank'),(0xc,'char'),(0x15,'bgm'),(0x16,'key'),(0x28,'mode'),(0x37,'fast'),(0x39,'demo')):
            self.uc.mem_write(self.resident+a,bytes([s[k]]))
        self.uc.mem_write(self.resident+0x10,struct.pack('<I',s['seed']))
        for a,v in ((menu.SEL,s['sel']),(menu.QUIT,s['quit']),(menu.INMAIN,s['inmain']),(menu.MAININIT,s['maininit']),
                    (menu.OPTINIT,s['optinit']),(menu.MAINLOCK,s['mainlock']),(menu.OPTLOCK,s['optlock']),
                    (menu.INOPT,s['inopt']),(menu.DISABLED,s['disabled']),(menu.ACTIVE,s['active'])):
            self.uc.mem_write(self.data+a,bytes([v&255]))
        self.uc.mem_write(self.data+menu.PUT,struct.pack('<H',s['put']));self.uc.mem_write(self.data+menu.INPUT,struct.pack('<H',s['input']))
        self.uc.mem_write(self.data+0x2c8,struct.pack('<H',s['zoom']));self.uc.mem_write(self.data+0x99,bytes(s['seen']))
        self.s=s;self.meta=analyze(mz.program_image);self.events=[];self.writes=[];self.external=[];self.native=Counter();self.files=[];self.inputs=0
        self.visited=set();self.frames=[];self.top=None;self.errors=[];self.stop=False;self.position=None;self.entry_specs={}
        for row in self.meta['bodies']:self.entry_specs[(row['segment'],row['offset'])]=row
        for r,v in dict(DS=0x2000+DS,SS=0x4000,ES=0x3333,BP=0x7777,SI=0x1357,DI=0x2468,BX=0xbeef).items():self.set(r,v)
        self.set('EFLAGS',2|(0x200 if s['if'] else 0)|(0x400 if s['df'] else 0))
        def guard(fn):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop()
            return invoke
        def code(uc,address,size,user):
            seg=self.get('CS')-0x2000;off=address-self.get('CS')*16;position=(seg,off);self.position=position
            if self.get('SS')!=0x4000:raise ValueError('OP entry stack segment alias')
            if address==self.code+0xff00:
                f=self.top
                if seg!=CS or self.get('SP')!=f['sp']+f['width']+f['cleanup'] or self.frames or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('OP entry terminal frame differs')
                self.stop=True;uc.emu_stop();return
            if self.frames and position==self.frames[-1]['ret']:
                f=self.frames.pop()
                if self.get('SP')!=f['sp']+f['width']+f['cleanup'] or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('OP entry native callback return differs')
            if position in self.meta['bounds']:
                self.visited.add(position)
                if seg==CS and off in (0x7ab,0x7d8) and self.word(menu.PUT) not in (0x5dd,0x657):raise ValueError('OP entry callback target differs')
                if position in self.meta['entries']:
                    row=self.entry_specs[position];self.native[row['name']]+=1
                    if self.entered:
                        sp=self.get('SP');width=4 if row['far'] else 2
                        words=struct.unpack('<'+'H'*(width//2),uc.mem_read(self.stack+sp,width));ret=(words[1]-0x2000 if width==4 else seg,words[0]);caller=self.meta['calls'].get(ret)
                        dest=caller['destination'] if caller else 'missing'
                        if dest is None:
                            if self.word(menu.PUT)!=off or position not in ((CS,0x5dd),(CS,0x657)):raise ValueError('OP entry native callback target differs')
                        elif dest!=position:raise ValueError('OP entry native caller differs')
                        self.frames.append(dict(ret=ret,sp=sp,width=width,cleanup=row['cleanup'],name=row['name'],saved={r:self.get(r) for r in ('BP','SI','DI','DS')}))
                    self.entered=True
                if position in self.meta['returns']:
                    f=self.frames[-1] if self.frames else self.top;sp=self.get('SP');width=f['width']
                    words=struct.unpack('<'+'H'*(width//2),uc.mem_read(self.stack+sp,width));ret=(words[1]-0x2000 if width==4 else seg,words[0])
                    if sp!=f['sp'] or ret!=f['ret'] or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('OP entry native return stack differs')
                return
            if position not in MODELS:raise ValueError('OP entry escape/operand boundary differs')
            name,count,far,cleanup=MODELS[position];sp=self.get('SP');width=4 if far else 2
            words=struct.unpack('<'+'H'*(width//2),uc.mem_read(self.stack+sp,width));ret=(words[1]-0x2000 if far else seg,words[0]);caller=self.meta['calls'].get(ret)
            if not caller or caller['destination']!=position:raise ValueError('OP entry foreign caller frame differs')
            args=list(struct.unpack('<'+'H'*(count//2),uc.mem_read(self.stack+sp+width,count))) if count else []
            event=dict(name=name,args=args)
            if name in ('gaiji','text','puts','init','gaiji-entry','open','append','execl'):
                pairs=[(1,2)] if name in ('gaiji','text') else [(0,1)]
                if name=='execl':pairs=[(0,1),(2,3)]
                event['strings']=[]
                for a,b in pairs:
                    if args[b]!=0x2000+DS:raise ValueError('OP entry filename/text segment differs')
                    raw=bytes(uc.mem_read(args[b]*16+args[a],160));event['strings'].append(raw[:raw.index(0)+1].hex())
            def external(a,z,v):uc.mem_write(a,v.to_bytes(z,'little'));self.external.append((a,z,v))
            reply=s['reply']
            if name=='input':
                if self.inputs>=len(s['inputs']):raise ValueError('OP entry input fixture exhausted')
                value=s['inputs'][self.inputs];self.inputs+=1;event['input']=value;external(self.data+menu.INPUT,2,value)
                if self.inputs==s.get('corrupt_poll'):external(self.data+menu.INOPT,1,2);external(self.data+menu.QUIT,1,1)
            if name.startswith('select-'):
                reply=s['selection_reply'];event['reply']=reply
                if name=='select-story':
                    offptr,segptr=struct.unpack('<HH',uc.mem_read(self.data+menu.RESIDENT,4));external(segptr*16+offptr+0xc,1,s['selected_char'])
            if name=='init':reply=s['init_reply']
            if name=='determine':external(self.data+menu.ACTIVE,1,s['mode_active'])
            if name=='read':
                length,offptr,segptr=args
                if length!=8 or segptr!=0x4000 or s['read']>8:raise ValueError('OP entry cfg read fixture differs')
                block=bytes(s['cfg'][:s['read']]);uc.mem_write(segptr*16+offptr,block);event['bytes']=block.hex()
            if name=='write':
                length,offptr,segptr=args
                if length not in (4,8) or segptr!=0x4000:raise ValueError('OP entry cfg write span differs')
                block=bytes(uc.mem_read(segptr*16+offptr,length));self.files.append(dict(args=args,bytes=block.hex(),caller=list(ret)))
                # Byte3 in ordinary save is uninitialized local storage; retain
                # it in raw file observations, without a scalar value claim.
                event['defined_bytes']=block[:3].hex() if length==4 else block.hex()
            self.events.append(event);self.set('AX',reply);self.set('EFLAGS',(self.get('EFLAGS')&~1)|s['cf'])
            self.set('SP',sp+width+cleanup);self.set('CS',ret[0]+0x2000);self.set('IP',ret[1])
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            dg=address-self.data
            allowed=(size==1 and (dg in [menu.SEL,menu.QUIT,menu.INMAIN,menu.MAININIT,menu.OPTINIT,menu.MAINLOCK,menu.OPTLOCK,menu.INOPT,menu.ACTIVE,menu.DISABLED] or 0x99<=dg<0xa0)) or (size==2 and dg in (menu.PUT,menu.INPUT,menu.RESIDENT,menu.RESIDENT+2,0x312,0x314)) or (size==4 and dg==0x312)
            offptr,segptr=struct.unpack('<HH',uc.mem_read(self.data+menu.RESIDENT,4));base=segptr*16+offptr
            allowed=allowed or (size==1 and (address-base in [0xb,0xc,0xd,0xe,0xf,0x15,0x16,0x17,0x28,0x33,0x34,0x35,0x36,0x37,0x38,0x39] or 0x18<=address-base<0x28 or 0x29<=address-base<0x32)) or (size==4 and address==base+0x10)
            if not allowed or self.position not in self.meta['bounds']:raise ValueError('OP entry complete native store span differs')
            self.writes.append((address,size,value&((1<<(size*8))-1)))
        def intr(*args):raise ValueError('OP entry unexpected interrupt')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
    def run(self,name,args=(),budget=100000):
        self.stop=False;self.errors.clear();self.entered=False
        row=next(r for r in self.meta['bodies'] if r['name']==name);width=4 if row['far'] else 2
        self.set('CS',row['segment']+0x2000);self.set('SP',0xffd0)
        words=[0xff00]+([CS+0x2000] if width==4 else [])+list(args)
        self.uc.mem_write(self.stack+0xffd0,struct.pack('<'+'H'*len(words),*words))
        self.top=dict(sp=0xffd0,ret=(CS,0xff00),width=width,cleanup=row['cleanup'],name=name,saved={r:self.get(r) for r in ('BP','SI','DI','DS')})
        self.uc.emu_start(0x20000+row['segment']*16+row['offset'],0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('OP entry terminal/budget differs')


def scenario(**kw):
    s=menu.scenario();s.update(offset=0,seed=1,char=1,selected_char=1,mode=0,fast=0,demo=0,selection_reply=0,zoom=0,init_reply=0,
                              seen=[0]*7,inputs=[0x20,0x1000],cfg=[1,1,2,0,0,0,0x60,0],read=8)
    s.update(kw);return s


def observe(mz,name,s,args=()):
    p=EntryProbe(mz,s);before=bytes(p.uc.mem_read(0,0x100000));spec=EntrySpec(before,p.data,p.resident,s)
    spec.native_call(name,args,True);p.run(name,args)
    if p.events!=spec.events or p.writes!=spec.writes or p.external!=spec.external or p.native!=spec.native:
        for label,a,b in [('events',p.events,spec.events),('writes',p.writes,spec.writes),('external',p.external,spec.external),('native',p.native,spec.native)]:
            if a!=b:
                if isinstance(a,list):
                    i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)));detail=str((i,a[i:i+1],b[i:i+1],len(a),len(b)))
                else:detail=str((a,b))
                raise ValueError('OP entry independent scalar '+label+' differs: '+name+' '+detail)
    actual=bytes(p.uc.mem_read(0,0x100000))
    if actual[:p.stack]!=spec.memory[:p.stack] or actual[p.stack+65536:]!=spec.memory[p.stack+65536:]:raise ValueError('OP entry whole physical preservation differs')
    if bool(p.get('EFLAGS')&0x200)!=s['if'] or bool(p.get('EFLAGS')&0x400)!=spec.df:raise ValueError('OP entry IF/DF differs')
    result=p.get('AX')&255 if name in ('story','vs','score') else None
    if result is not None and result!=spec.result:raise ValueError('OP entry boolean return differs')
    digest=lambda x:sha(json.dumps(x,separators=(',',':')).encode())
    return dict(function=name,args=list(args),scenario=s,events=p.events,native_entries=dict(p.native),stores=len(p.writes),stores_sha256=digest(p.writes),
                external_inputs=p.external,files=p.files,result=result,visited=[list(a) for a in sorted(p.visited)],memory_before_sha256=sha(before),memory_after_sha256=sha(spec.memory))


def matrix(mz):
    rows=[]
    for irq,df in itertools.product((False,True),repeat=2):
        flags={'if':irq,'df':df}
        for char,seed,rank in itertools.product(range(1,19),(0,1,0x7fffffff,0xffffffff),(0,3,255)):
            rows.append(observe(mz,'story',scenario(char=char,selected_char=char,seed=seed,rank=rank,offset=0x31,reply=0xffff,cf=1,**flags)))
        for reply in (1,2,0xff,0x100):rows.append(observe(mz,'story',scenario(selection_reply=reply,**flags)))
        for sel in (0,1,2,3,0xffff):rows.append(observe(mz,'vs_choice',scenario(**flags),[0xf3a5,sel]))
        for mode,reply in itertools.product((0,1,127,128,129,130,255),(0,2)):
            for inputs in ([0x20],[1,1,0,0x2000],[2,2,0,0x20],[0x1000,0,3,0,0x20]):
                rows.append(observe(mz,'vs',scenario(mode=mode,selection_reply=reply,inputs=inputs,**flags)))
        for demo in (0,1,2,3,4,254,255):rows.append(observe(mz,'demo',scenario(demo=demo,**flags)))
        for inputs in ([0x20],[0,0,0x20],[0]*521+[0x20]):rows.append(observe(mz,'wait',scenario(inputs=inputs,seed=0xffffffff,**flags)))
        rows.append(observe(mz,'score',scenario(**flags)))
        for zoom,init in itertools.product((0,1,0xffff),(0,0xffff)):
            rows.append(observe(mz,'entry',scenario(zoom=zoom,init_reply=init,maininit=0,**flags)))
        for mode,fast,active in itertools.product((0,128,129,130),(0,1),(0,0xfe)):
            rows.append(observe(mz,'entry',scenario(mode=mode,fast=fast,mode_active=active,maininit=0,selection_reply=2,
                        inputs=[0x20,0x1000],**flags)))
        for sel in range(6):
            inputs=[0x20,0x20,0x20,0,0x1000,0,0x1000]
            rows.append(observe(mz,'entry',scenario(sel=sel,maininit=0,selection_reply=2,inputs=inputs,**flags)))
        rows.append(observe(mz,'entry',scenario(maininit=0,inputs=[0x20,0],corrupt_poll=2,**flags)))
        for bgm,active in itertools.product((0,1,2,255),(0,2,255)):
            rows.append(observe(mz,'cfg_load',scenario(cfg=[bgm,255,255,0,0,0,0x60,0],mode_active=active,**flags)))
        for name in ('cfg_save','cfg_exit'):rows.append(observe(mz,name,scenario(bgm=255,key=254,rank=253,**flags)))
        for n in (0,3,5,7):rows.append(observe(mz,'cfg_load',scenario(read=n,mode_active=0xfe,**flags)))
        for name,count,ptr in (('main',6,0x5dd),('option',4,0x657)):
            for sel,inp in itertools.product(range(count),(0,1,2,3,4,8,12,0x20,0x1000,0x2000,0x302f)):
                rows.append(observe(mz,name,scenario(sel=sel,input=inp,put=ptr,bgm=sel%3,rank=sel%4,key=sel%3,inputs=[0x20,0x1000],**flags)))
        rows.append(observe(mz,'option',scenario(sel=0,rank=3,input=8,put=0x657,**flags)))
        rows.append(observe(mz,'option',scenario(sel=1,bgm=0,input=8,put=0x657,**flags)))
        for name,ptr in (('main',0x5dd),('option',0x657)):
            for initialized in (0,1):
                rows.append(observe(mz,name,scenario(put=ptr,maininit=initialized,optinit=initialized,input=0,inmain=0,**flags)))
        for sel,field in itertools.product((0,1,2,3,4,5,6,0xffff),(0,1,2,3,255)):
            for name in ('main_choice','option_choice'):
                rows.append(observe(mz,name,scenario(rank=field,bgm=field,key=field,**flags),[0xf3a5,sel]))
        for ptr,sel,direction in itertools.product((0x5dd,0x657),(0,3,5,127,128,255),(1,0xffff)):
            rows.append(observe(mz,'move',scenario(sel=sel,put=ptr,**flags),[direction,5 if ptr==0x5dd else 3]))
    return rows


def reentry_failure(mz):
    p=EntryProbe(mz,scenario());p.run('story');first=dict(p.native);p.native.clear()
    try:p.run('story',budget=10000)
    except ValueError as e:
        if 'budget' not in str(e):raise
        return dict(first_terminal=True,second_terminal=False,reason=str(e),first_native=first,second_native=dict(p.native),
                    seen=bytes(p.uc.mem_read(p.data+0x99,7)).hex(),visited=[list(a) for a in sorted(p.visited)])
    raise ValueError('OP entry known dirty seen reentry no longer exhausts budget')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('OP entry parent compiler proof differs')
    parent=json.loads(raw);inputs=dict(parent['inputs']);inputs[PROOF]=sha(raw)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP entry parent input differs: '+p)
    for p in ('scripts/review_th03_op_entry.py','tests/test_op_entry_review.py','scripts/review_th03_op_menu.py','scripts/replay_th03_op_score.py',
              'scripts/review_th03_decoded_code.py','scripts/inventory_rec98_th03.py','scripts/review_th03_mainl_cutscene.py'):inputs[p]=sha((ROOT/p).read_bytes())
    artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-op');stored=read_verified_artifact(ROOT,artifact)
    frozen=frozen_files(REVISION);target=parse_mz((ROOT/menu.DECODED).read_bytes());observations=[]
    paths=[menu.DECODED]+[str(Path(PROOF).parent/f'round{r["number"]}'/'source/bin/th03/op.exe') for r in parent['rounds']]
    for index,path in enumerate(paths):
        raw=(ROOT/path).read_bytes();inputs[path]=sha(raw);mz=parse_mz(raw)
        if not mz.valid:raise ValueError('OP entry invalid decoded MZ')
        meta=analyze(mz.program_image);o=dict(path=path,bodies=meta['bodies'],tables=meta['tables'])
        if index:
            round=parent['rounds'][index-1];tree=Path(path).parents[2];o['source_lineage']={}
            if inputs[path]!=round['products']['bin/th03/op.exe']:raise ValueError('OP entry parent product differs')
            for p in PROVIDERS:
                cp=str(tree/p);raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw);expected=frozen[p]
                if p=='th03/op_01.cpp':
                    text=expected.decode();a=text.index('// Must be non-`const` for data ordering reasons.');b=text.index('void main(void)',a)
                    expected=(text[:a]+'#include "src/op/menu/menu_state.inl"\n\n'+text[b:]).encode()
                if raw!=expected:raise ValueError('OP entry frozen/declared maintained provider differs: '+p)
                o['source_lineage'][p]=dict(frozen_sha256=sha(frozen[p]),cached_sha256=sha(raw),maintained_menu_overlay=p=='th03/op_01.cpp')
            cp=str(tree/'obj/th03/op_01.obj');raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw);obj=describe_omf(raw)
            if not obj['valid'] or obj['dependency_timestamp_normalized_sha256']!=round['all_objects']['obj/th03/op_01.obj']:raise ValueError('OP entry OMF differs')
            o['object']=dict(path=cp,normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'])
            cp=str(tree/'obj/th03/op.map');raw=(ROOT/cp).read_bytes();inputs[cp]=sha(raw)
            carrier=next(c for c in code_rows(raw.decode(),len(mz.program_image)) if c['module']=='th03/op_01.cpp' and c['size'])
            if (carrier['segment'],carrier['offset'],carrier['size'])!=(CS,8,3094):raise ValueError('OP entry original carrier differs')
            o['comparisons']={}
            for name,seg,a,z,c,f in RANGES:
                comp=extent_observation(target,mz,dict(segment=seg,offset=a,start=seg*16+a,size=z));o['comparisons'][name]=comp
                if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('OP entry complete raw/ordered inequality')
            if mz.program_image[DS*16+0x90:DS*16+0x278]!=target.program_image[DS*16+0x90:DS*16+0x278]:raise ValueError('OP entry native labels/statics/table bytes differ')
        o['cpu']=matrix(mz);o['reentry']=reentry_failure(mz);visited={tuple(a) for r in o['cpu'] for a in r['visited']}|{tuple(a) for a in o['reentry']['visited']}
        o['coverage']=dict(instructions=len(meta['bounds']),visited=len(meta['bounds']&visited),unvisited=[list(a) for a in sorted(meta['bounds']-visited)])
        if o['coverage']['unvisited']:raise ValueError('OP entry native coverage incomplete: '+str(o['coverage']['unvisited']))
        if index and normalized_contracts(o['cpu'])!=normalized_contracts(observations[0]['cpu']):raise ValueError('OP entry target/cold contracts differ')
        if index and o['reentry']!=observations[0]['reentry']:raise ValueError('OP entry reentry failure contracts differ')
        observations.append(o);print('Reviewed',path,len(o['cpu']),'cases',o['coverage'],flush=True)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP entry input changed: '+p)
    final=frozen_files(REVISION)
    if any(final[p]!=frozen[p] for p in PROVIDERS) or read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('OP entry provider/canonical target changed')
    report=dict(kind='th03-op-complete-entry-carrier-native-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,observations=observations,
                tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),new_decoded_bytes=1485,previous_carrier_decoded_bytes=1609,
                diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,new_build=False,
                notes='Complete3094-byte original entry carrier includes271 previously reviewed configuration and1338 maintained menu bytes, new1485 complete story/VS/demo/wait/score/startup bodies. Native menu callbacks, IRAND42 and compiler SCOPY28 execute; foreign screens/file/sound/animation/device/init/exec replies explicitly modeled. Ordinary CFG save byte3 is opaque native stack data retained in full file traces, with no scalar value claim. Actual DOS child execution, heap/devices/real timing/packing/fullproduct/exact remain open. Dirty static opponent_seen on reentry after returning execl exhausts budget; no inherited all2^32-seed termination claim.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n');print('PASS complete OP entry native diagnostics; exact open')


if __name__=='__main__':main()
