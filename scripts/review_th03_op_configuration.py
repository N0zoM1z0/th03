#!/usr/bin/env python3
"""Review OP configuration and lifecycle candidates at original decoded entries."""
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
from review_th03_mainl_graphics import COLD, COLD_SHA
from review_th03_mainl_linked_tail import object_code
from review_th03_mainl_heap import cached_provider

ROOT = Path(__file__).resolve().parents[1]
DECODED = '.analysis/th03-diet/sol-diet-restoration-20261006-b/op.exe'
DECODED_SHA = 'efd858aef69a240af3a27c747a5beae150f55f0b41b8afdd1eda1760a759ecc0'
DIET = '.analysis/th03-diet/sol-diet-restoration-20261006-b/receipt.json'
DIET_SHA = 'ca533176a0ce89ccc7a782ff397965a781d4a60fdcf750e1b5fcbc3ead85d71d'
GROUP, SHARED, DGROUP = 0x990, 0xbeb, 0xd7f
# name, segment, original entry, cold entry, complete bytes, RETF/RET cleanup, carrier
RANGES = [('cfg_load', GROUP, 8, 8, 120, 'near', 'th03/op_01.cpp'),
          ('cfg_save', GROUP, 0x80, 0x80, 67, 'near', 'th03/op_01.cpp'),
          ('cfg_save_exit', GROUP, 0xc3, 0xc3, 84, 'near', 'th03/op_01.cpp'),
          ('exit_dos', SHARED, 8, 8, 25, 0, 'th02/exit_dos.cpp'),
          ('planes', SHARED, 0x21, 0x21, 41, 0, 'th01/vplanset.cpp'),
          ('snd_mode', SHARED, 0x4a, 0x4a, 29, 0, 'th02/snd_mode.c'),
          ('init', SHARED, 0x571, 0x570, 105, 0, 'th03/initop.cpp'),
          ('scopy', 0, 0x337e, 0x337e, 28, 8, 'f_scopy')]
MODEL = {(0,0x9a8): ('open',4), (0,0x8f4): ('read',6), (0,0x888): ('close',0),
         (0,0x7c8): ('append',4), (0,0x9e4): ('seek',6), (0,0xa26): ('write',6),
         (SHARED,0x112): ('game_exit',0), (0,0x1a2e): ('beep_on',0),
         (0,0x2238): ('systemline_show',0), (0,0x222c): ('cursor_show',0),
         (0,0x245a): ('assign',2), (0,0x19f6): ('graph_start',0),
         (0,0x114c): ('graph_clear',0), (0,0x22ca): ('vsync_start',0),
         (0,0x1a22): ('beep_off',0), (0,0x2232): ('systemline_hide',0),
         (0,0x2226): ('cursor_hide',0), (0,0x708): ('egc_start',0),
         (0,0x2db8): ('js_start',0), (0,0x2b60): ('pfstart',4)}
RESIDENT, ACTIVE, DISABLED, FM, MIDI, PLANES = 0x2464, 0x5dc, 0x90, 0x1a0a, 0x1a0b, 0x19fa
FORWARDERS = {'th01/vplanset.cpp':'src/main/hardware/vram_planes.cpp'}
PROVIDERS = ['th03/op_01.cpp','th03/core/initop.cpp','th03/initop.cpp','th02/exit_dos.cpp',
             'th01/vplanset.cpp','th01/hardware/vplanset.cpp','th01/hardware/vplanset.h',
             'th02/snd_mode.c','th02/snd/detmode.c','th02/snd/snd.h','th03/snd/snd.h',
             'th03/formats/cfg_impl.hpp','th03/formats/cfg.hpp','th02/formats/cfg.hpp',
             'th03/core/initexit.h','th02/core/initexit.h','th03/resident.hpp','platform.h',
             'x86real.h','Tupfile.lua','libs/master.lib/master.hpp','libs/master.lib/pc98_gfx.hpp']


def analyze(image, original=True):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    parts=[];bounds=set();entries={};returns={};calls={};ports={}
    for name,seg,orig,cold,z,cleanup,owner in RANGES:
        a=orig if original else cold;body=image[seg*16+a:seg*16+a+z]
        ins=list(decoder.disasm(body,a));local={i.address for i in ins}
        expected=('ret','') if cleanup=='near' else ('retf',str(cleanup) if cleanup else '')
        if len(body)!=z or not ins or sum(i.size for i in ins)!=z or (ins[-1].mnemonic,ins[-1].op_str)!=expected:
            raise ValueError('OP complete function/return boundary differs: '+name)
        parts.append((name,seg,a,z,cleanup,owner,ins,local));bounds.update((seg,i.address) for i in ins);entries[(seg,a)]=name
    rows=[]
    for name,seg,a,z,cleanup,owner,ins,local in parts:
        edges=[]
        for j,i in enumerate(ins):
            if i.mnemonic in ('ret','retf'):
                expected=('ret','') if cleanup=='near' else ('retf',str(cleanup) if cleanup else '')
                if (i.mnemonic,i.op_str)!=expected:
                    raise ValueError('OP interior return cleanup differs')
                returns[(seg,i.address)]=cleanup
            if i.mnemonic in ('int','in','out'):
                if i.mnemonic=='int' and name=='snd_mode' and i.address==0x4c and i.op_str=='0x60':continue
                wanted={0x594:(0xa6,1),0x59f:(0xa6,0),0x5aa:(0xa6,0),0x5ae:(0xa4,0)}
                site=i.address+(0 if original else 1)
                if name!='init' or i.mnemonic!='out' or site not in wanted or i.op_str!='dx, al':raise ValueError('OP unexpected device instruction')
                ports[(seg,i.address)]=wanted[site];continue
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('OP indirect/operand branch')
            if i.mnemonic=='lcall':dest=tuple(o.imm for o in i.operands)
            else:dest=(seg,i.operands[0].imm)
            if i.mnemonic in ('call','lcall'):
                if i.mnemonic=='call' and (dest not in entries and dest not in MODEL or not j or ins[j-1].bytes!=b'\x0e'):
                    raise ValueError('OP near call lacks native far frame')
                if dest not in entries and dest not in MODEL:raise ValueError('OP unknown call interface')
                if dest in entries and entries[dest] not in ('planes','snd_mode','scopy'):raise ValueError('OP unexpected native helper')
                calls[(seg,i.address+i.size)]=dict(site=i.address,destination=dest)
            elif dest!=(seg,dest[1]) or dest[1] not in local or i.mnemonic=='ljmp':raise ValueError('OP branch enters operand/neighbor')
            edges.append(dict(site=i.address,kind=i.mnemonic,destination=list(dest)))
        rows.append(dict(name=name,segment=seg,offset=a,size=z,cleanup=cleanup,carrier=owner,
                         instructions=len(ins),sha256=sha(image[seg*16+a:seg*16+a+z]),edges=edges))
    if image[SHARED*16+0x67]!=0x90:raise ValueError('OP sound producer differs')
    return dict(bodies=rows,bounds=bounds,entries=entries,returns=returns,calls=calls,ports=ports)


class ConfigurationProbe(Probe):
    """Execute complete callers, planes, mode selection and compiler copy helper."""
    def __init__(self,mz,scenario,original=True):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,(struct.unpack_from('<H',image,at)[0]+0x2000)&65535)
        self.uc.mem_write(0x20000,bytes(image));self.data=(0x2000+DGROUP)*16;self.stack=0x40000
        self.s=scenario;self.meta=analyze(mz.program_image,original);self.errors=[];self.stop=False;self.frame=None;self.helpers=[]
        self.events=[];self.ports=[];self.writes=[];self.visited=set();self.native=Counter();self.drivers=[]
        self.uc.mem_write(self.stack,bytes([scenario.get('stack',0xa5)])*65536)
        self.seed=bytes(scenario.get('seed',[0x55,0x66,0x77,0x88,0x99,0,0x60,0xaa]))
        if len(self.seed)!=8:raise ValueError('OP CFG seed size differs')
        self.uc.mem_write(self.stack+0xffc6,self.seed)
        self.uc.mem_write(self.data+RESIDENT,struct.pack('<HH',scenario.get('offset',0),scenario.get('segment',0x6000)))
        self.uc.mem_write(self.data+ACTIVE,bytes([scenario.get('active',0x7e)]));self.uc.mem_write(self.data+DISABLED,b'\x7d')
        self.uc.mem_write(self.data+FM,b'\x7c');self.uc.mem_write(self.data+MIDI,bytes([scenario.get('midi',0)]))
        seg=scenario.get('segment',0x6000);off=scenario.get('offset',0)
        for field,key,default in ((0x15,'bgm',2),(0x16,'key',1),(0xb,'rank',3)):
            self.uc.mem_write(seg*16+((off+field)&65535),bytes([scenario.get(key,default)]))
        self.uc.mem_write(self.data+PLANES,b'\x5a'*16)
        for r,v in dict(DS=0x2000+DGROUP,SS=0x4000,BP=0x7777,SI=0x1357,DI=0x2468,ES=0x3333,AX=0xabcd,BX=0xbeef,CX=0x5678,DX=0x789a).items():self.set(r,v)
        self.set('EFLAGS',2|(0x200 if scenario.get('if',True) else 0)|(0x400 if scenario.get('df') else 0))
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            cs=self.get('CS');logical=address-cs*16;seg=cs-0x2000
            if self.get('SS')!=0x4000:raise ValueError('OP stack segment alias')
            if address==0x20000+GROUP*16+0xff00:
                f=self.frame
                if cs!=0x2000+GROUP or self.get('SP')!=f['sp']+(2 if f['near'] else 4) or any(self.get(r)!=v for r,v in f['saved'].items()) or self.helpers:
                    raise ValueError('OP terminal native return frame differs')
                self.stop=True;uc.emu_stop();return
            if self.helpers and (seg,logical)==self.helpers[-1]['return_site']:
                f=self.helpers.pop()
                if self.get('SP')!=f['sp']+4+f['cleanup'] or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('OP native helper return differs')
            if (seg,logical) in MODEL:
                sp=self.get('SP');ip,retcs=struct.unpack('<HH',uc.mem_read(self.stack+sp,4));caller=(retcs-0x2000,ip)
                call=self.meta['calls'].get(caller);name,count=MODEL[(seg,logical)]
                if not call or tuple(call['destination'])!=(seg,logical):raise ValueError('OP modeled interface caller frame differs')
                args=list(struct.unpack('<'+'H'*(count//2),uc.mem_read(self.stack+sp+4,count))) if count else []
                event=dict(name=name,args=args)
                if name=='read':
                    length,off,pseg=args
                    if length!=8 or pseg!=0x4000 or off!=0xffc6:raise ValueError('OP CFG read pointer/size differs')
                    block=bytes(self.s.get('cfg',self.seed));n=self.s.get('read',8)
                    if len(block)!=8 or not 0<=n<=8:raise ValueError('OP CFG model read bounds differ')
                    uc.mem_write(pseg*16+off,block[:n]);event['bytes']=block[:n].hex()
                if name=='write':
                    length,off,pseg=args
                    if length not in (4,8) or pseg!=0x4000 or off!=0xffc6:raise ValueError('OP CFG write pointer/size differs')
                    event['bytes']=bytes(uc.mem_read(pseg*16+off,length)).hex()
                self.events.append(event);self.set('AX',self.s.get('assign',0) if name=='assign' else self.s.get('reply',0xace1))
                self.set('EFLAGS',(self.get('EFLAGS')&~1)|int(self.s.get('cf',False)))
                self.set('SP',sp+4+count);self.set('CS',retcs);self.set('IP',ip);return
            if (seg,logical) not in self.meta['bounds']:raise ValueError('OP CODE segment alias/unknown instruction boundary')
            self.visited.add((seg,logical))
            if (seg,logical) in self.meta['entries']:
                name=self.meta['entries'][(seg,logical)];self.native[name]+=1
                if name in ('planes','snd_mode','scopy') and name!=self.frame['name']:
                    sp=self.get('SP');ip,retcs=struct.unpack('<HH',uc.mem_read(self.stack+sp,4));caller=(retcs-0x2000,ip);call=self.meta['calls'].get(caller)
                    if not call or tuple(call['destination'])!=(seg,logical):raise ValueError('OP native helper caller differs')
                    cleanup=8 if name=='scopy' else 0
                    self.helpers.append(dict(return_site=caller,sp=sp,cleanup=cleanup,saved={r:self.get(r) for r in ('BP','SI','DI','DS')}))
                    if name=='scopy':
                        words=list(struct.unpack('<4H',uc.mem_read(self.stack+sp+4,8)))
                        if words!=[0x91,0x2000+DGROUP,0xffc6,0x4000] or self.get('CX')!=8:raise ValueError('OP copy helper argument layout differs')
            if (seg,logical) in self.meta['returns']:
                cleanup=self.meta['returns'][(seg,logical)]
                if cleanup=='near':
                    if int.from_bytes(uc.mem_read(self.stack+self.get('SP'),2),'little')!=0xff00:raise ValueError('OP near native return frame differs')
                elif self.helpers:
                    ip,cs=struct.unpack('<HH',uc.mem_read(self.stack+self.get('SP'),4));f=self.helpers[-1]
                    if (cs-0x2000,ip)!=f['return_site'] or self.get('SP')!=f['sp']:raise ValueError('OP helper far native return frame differs')
                else:
                    ip,cs=struct.unpack('<HH',uc.mem_read(self.stack+self.get('SP'),4))
                    if (ip,cs)!=(0xff00,0x2000+GROUP) or self.get('SP')!=self.frame['sp']:raise ValueError('OP far native return frame differs')
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            ptr=struct.unpack('<HH',uc.mem_read(self.data+RESIDENT,4));base=ptr[1]*16
            allowed=[(self.data+RESIDENT,4),(self.data+ACTIVE,1),(self.data+DISABLED,1),(self.data+FM,1),(self.data+PLANES,16)]
            allowed += [(base+((ptr[0]+field)&65535),1) for field in (0xb,0x15,0x16)]
            if not any(a<=address and address+size<=a+z for a,z in allowed):raise ValueError('OP store exceeds complete declared span')
            self.writes.append([address,size,value&((1<<(size*8))-1)])
        def output(uc,port,width,value,user):
            key=(self.get('CS')-0x2000,self.get('IP'));expected=self.meta['ports'].get(key)
            # Unicorn reports linear-low16 IP in shared segments; derive the logical site.
            if expected is None:key=(key[0],(key[1]-(self.get('CS')*16&65535))&65535);expected=self.meta['ports'].get(key)
            if expected!=(port,value) or width!=1:raise ValueError('OP unexpected port/site/value')
            self.ports.append([port,value])
        def intr(uc,number,user):
            ip=self.get('IP');cs=self.get('CS')
            if number!=0x60 or cs!=0x2000+SHARED or self.get('AX')>>8!=9:raise ValueError('OP unexpected interrupt/interface')
            self.drivers.append(dict(number=number,ah=9,reply=self.s.get('driver',0xff)))
            self.set('AX',(self.get('AX')&0xff00)|self.s.get('driver',0xff));self.set('EFLAGS',(self.get('EFLAGS')&~1)|int(self.s.get('cf',False)))
        def inp(*args):raise ValueError('OP unexpected input interface')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(output),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(inp,0),None,1,0,reg.UC_X86_INS_IN)

    def run(self,name,args=(),budget=10000):
        if name in ('snd_mode','scopy'):raise ValueError('OP helper requires complete public caller')
        self.stop=False;self.errors.clear();row=next(r for r in self.meta['bodies'] if r['name']==name);near=row['cleanup']=='near'
        self.set('CS',0x2000+row['segment']);self.set('SP',0xffd0)
        frame=[0xff00] if near else [0xff00,0x2000+GROUP]
        self.uc.mem_write(self.stack+0xffd0,struct.pack('<'+'H'*(len(frame)+len(args)),*frame,*args))
        self.frame=dict(name=name,sp=0xffd0,near=near,saved={r:self.get(r) for r in ('BP','SI','DI','DS')})
        self.uc.emu_start((0x2000+row['segment'])*16+row['offset'],0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('OP terminal/budget differs')


def matrix(mz,original=True):
    rows=[]
    def observe(name,s,args=()):
        p=ConfigurationProbe(mz,s,original);memory=bytearray(p.uc.mem_read(0,0x100000));before=sha(memory);writes=[];events=[];ports=[];native=Counter({name:1});drivers=[]
        def put(a,v,z=1):memory[a:a+z]=v.to_bytes(z,'little');writes.append([a,z,v])
        def event(name,args,**extra):events.append(dict(name=name,args=args,**extra))
        pointer=struct.unpack('<HH',memory[p.data+RESIDENT:p.data+RESIDENT+4])
        if name=='cfg_load':
            cfg=bytearray(p.seed);cfg[:s.get('read',8)]=bytes(s.get('cfg',p.seed))[:s.get('read',8)]
            segment=int.from_bytes(cfg[5:7],'little');base=segment*16
            event('open',[0x166,0x2000+DGROUP]);event('read',[8,0xffc6,0x4000],bytes=bytes(s.get('cfg',p.seed))[:s.get('read',8)].hex());event('close',[])
            put(p.data+RESIDENT+2,segment,2);put(p.data+RESIDENT,0,2);put(base+0x15,cfg[0]);native['snd_mode']+=1
            driver=s.get('driver',0xff);midi=s.get('midi',0);active=midi if driver==255 else 1
            drivers.append(dict(number=96,ah=9,reply=driver))
            if driver!=255:put(p.data+FM,1)
            put(p.data+ACTIVE,active);put(p.data+DISABLED,0)
            if not active:put(base+0x15,0);put(p.data+DISABLED,1)
            elif cfg[0]==0:put(p.data+ACTIVE,0)
            put(base+0x16,cfg[1]);put(base+0xb,cfg[2]);ax=(active&0xff00)|cfg[2]
        elif name in ('cfg_save','cfg_save_exit'):
            event('append',[0x166,0x2000+DGROUP]);event('seek',[0,0,0])
            cfg=bytearray(8) if name=='cfg_save_exit' else bytearray(p.seed)
            for field,at in ((0x15,0),(0x16,1),(0xb,2)):cfg[at]=memory[pointer[1]*16+((pointer[0]+field)&65535)]
            z=8 if name=='cfg_save_exit' else 4;event('write',[z,0xffc6,0x4000],bytes=bytes(cfg[:z]).hex());event('close',[])
            if name=='cfg_save_exit':native['scopy']+=1
            ax=s.get('reply',0xace1)
        elif name=='planes':
            for i,v in enumerate((0xa8000000,0xb0000000,0xb8000000,0xe0000000)):put(p.data+PLANES+i*4,v,4)
            ax=0xabcd
        elif name=='exit_dos':
            for n in ('game_exit','beep_on','systemline_show','cursor_show'):event(n,[])
            ax=s.get('reply',0xace1)
        elif name=='init':
            event('assign',[22000]);ax=int(bool(s.get('assign',0)))
            if not ax:
                native['planes']+=1
                for i,v in enumerate((0xa8000000,0xb0000000,0xb8000000,0xe0000000)):put(p.data+PLANES+i*4,v,4)
                for n in ('graph_start','graph_clear','graph_clear','vsync_start','beep_off','systemline_hide','cursor_hide','egc_start','js_start'):event(n,[])
                event('pfstart',list(args));ports=[[166,1],[166,0],[166,0],[164,0]]
        else:raise ValueError('OP unknown matrix caller')
        p.run(name,args);actual=bytes(p.uc.mem_read(0,0x100000));wanted=bytes(memory)
        if p.events!=events or p.writes!=writes or p.ports!=ports or p.native!=native or p.drivers!=drivers or p.get('AX')!=ax:
            raise ValueError('OP scalar event/store/native/AX differs: '+str((name,s,p.events,events,p.writes,writes,p.get('AX'),ax)))
        if actual[:p.stack]!=wanted[:p.stack] or actual[p.stack+65536:]!=wanted[p.stack+65536:]:raise ValueError('OP whole memory outside stack differs')
        expected_df=False if name=='cfg_save_exit' else bool(s.get('df'))
        if bool(p.get('EFLAGS')&0x400)!=expected_df or bool(p.get('EFLAGS')&0x200)!=s.get('if',True):raise ValueError('OP IF/DF contract differs')
        rows.append(dict(function=name,scenario=s,args=args,ax=ax,events=events,stores=writes,ports=ports,native_entries=dict(native),drivers=drivers,df=expected_df,
                         visited=[list(a) for a in sorted(p.visited)],memory_before_sha256=before,memory_after_sha256=sha(wanted)))
    for irq in (False,True):
        for df in (False,True):
            flags=dict(df=df,**{'if':irq})
            for driver in (0,0xfe,0xff):
                for midi in (0,1,2,255):
                    for bgm,key,rank in ((0,0,0),(1,1,1),(2,2,3),(255,255,255)):
                        for read in (0,1,3,5,6,7,8):
                            for segment in (0,0x5000,0x7000):
                                cfg=[bgm,key,rank,0xab,0xcd,segment&255,segment>>8,0xef]
                                observe('cfg_load',dict(flags,cfg=cfg,read=read,driver=driver,midi=midi))
            for name in ('cfg_save','cfg_save_exit'):
                for offset in (0,0x123,0xfff0):
                    for pattern in (0,0xa5,255):
                        for bgm,key,rank in ((0,0,0),(1,2,3),(255,255,255)):
                            observe(name,dict(flags,offset=offset,seed=[pattern]*8,bgm=bgm,key=key,rank=rank,reply=0xffff,cf=True))
            for assign in (0,1,32767,32768,65535):
                for pointer in ((0,0),(0x123,0x6000),(65535,0xffff)):
                    observe('init',dict(flags,assign=assign,cf=True),pointer)
            for reply in (0,65535):observe('exit_dos',dict(flags,reply=reply,cf=True))
            observe('planes',flags)
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/COLD).read_bytes();diet_raw=(ROOT/DIET).read_bytes();decoded=(ROOT/DECODED).read_bytes()
    if sha(raw)!=COLD_SHA or sha(diet_raw)!=DIET_SHA or sha(decoded)!=DECODED_SHA:raise ValueError('OP pinned cold/restoration/decoded proof differs')
    cold=json.loads(raw);diet=json.loads(diet_raw);frozen=frozen_files(REVISION)
    if not cold['pass'] or not cold['all_products_equal'] or cold['reference_revision']!=REVISION or not diet['restoration_checks_pass']:raise ValueError('OP parent proof status differs')
    inputs={COLD:sha(raw),DIET:sha(diet_raw),DECODED:sha(decoded)}
    for p in ['scripts/review_th03_op_configuration.py','tests/test_op_configuration_review.py','config/targets.toml','scripts/lib/pc98.py','scripts/lib/targets.py','scripts/lib/omf.py','scripts/review_th03_decoded_code.py','scripts/review_th03_mainl_linked_tail.py','scripts/review_th03_mainl_heap.py']:
        inputs[p]=sha((ROOT/p).read_bytes())
    stored=read_verified_artifact(ROOT,find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-op'))
    restoration=next(o for o in diet['observations'] if o['artifact']=='th03-op')
    if restoration['stored']['sha256']!=sha(stored) or restoration['decoded']['sha256']!=sha(decoded):raise ValueError('OP stored/restored lineage differs')
    target=parse_mz(decoded);observations=[]
    for index,path in enumerate([DECODED]+[str(Path(COLD).parent/f'round{i}/source/bin/th03/op.exe') for i in (1,2)]):
        data=(ROOT/path).read_bytes();inputs[path]=sha(data);mz=parse_mz(data)
        if not mz.valid:raise ValueError('OP invalid MZ')
        meta=analyze(mz.program_image,not index);o=dict(path=path,bodies=meta['bodies'])
        if index:
            if sha(data)!=cold['rounds'][index-1]['products']['bin/th03/op.exe']:raise ValueError('OP original cold product differs')
            tree=Path(path).parents[2];o['source_lineage']={};o['objects']={}
            o['archived_source_inputs']={};o['historical_unarchived_input_paths']=[]
            for p,h in cold['source_inputs'].items():
                cp=str(tree/p)
                if not (ROOT/cp).is_file():
                    o['historical_unarchived_input_paths'].append(p);continue
                inputs[cp]=sha((ROOT/cp).read_bytes())
                if inputs[cp]!=h:raise ValueError('OP archived cold input differs: '+p)
                o['archived_source_inputs'][p]=h
            if len(o['archived_source_inputs'])!=127 or len(o['historical_unarchived_input_paths'])!=25:raise ValueError('OP archived input availability changed')
            log=str(tree.parent/'cold-build.log');logdata=(ROOT/log).read_bytes();inputs[log]=sha(logdata)
            if sha(logdata)!=cold['rounds'][index-1]['commands'][0]['log_sha256']:raise ValueError('OP original cold command log differs')
            response=str(tree/'obj/th03/op.@l');response_data=(ROOT/response).read_bytes();inputs[response]=sha(response_data)
            o['compiler_command_log']=log;o['link_response']=response
            if not all(token in response_data for token in (b'op_01.obj',b'initop.obj',b'exit_dos.obj',b'snd_mode.obj',b'vplanset.obj')):raise ValueError('OP selected linker input missing')
            for local in FORWARDERS.values():
                if local not in o['archived_source_inputs']:raise ValueError('OP selected local provider not archived')
            for p in PROVIDERS:
                cp=str(tree/p);cached=(ROOT/cp).read_bytes();inputs[cp]=sha(cached)
                expected=f'#include "{FORWARDERS[p]}"\n'.encode() if p in FORWARDERS else cached_provider(p,frozen[p]) if p=='Tupfile.lua' else frozen[p]
                if p.endswith(('.asm','.inc')):cached=cached.replace(b'\r\n',b'\n');expected=expected.replace(b'\r\n',b'\n')
                if cached!=expected:raise ValueError('OP frozen/forwarded provider differs: '+p)
                o['source_lineage'][p]=dict(frozen_sha256=sha(frozen[p]),cached_sha256=inputs[cp],forwarder=FORWARDERS.get(p))
            mp=str(tree/'obj/th03/op.map');inputs[mp]=sha((ROOT/mp).read_bytes());text=(ROOT/mp).read_text();carriers=code_rows(text,len(mz.program_image))
            for owner in sorted({r[6] for r in RANGES if r[6]!='f_scopy'}|{'th03_op.asm'}):
                object_relative=Path('obj/th03/op.obj') if owner=='th03_op.asm' else Path('obj')/Path(owner).with_suffix('.obj')
                p=str(tree/object_relative);data=(ROOT/p).read_bytes();inputs[p]=sha(data);obj=describe_omf(data)
                if not obj['valid'] or obj['dependency_timestamp_normalized_sha256']!=cold['rounds'][index-1]['all_objects'][str(object_relative)]:raise ValueError('OP original cold OMF differs')
                o['objects'][owner]=dict(path=p,normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'])
                if owner in ('th02/snd_mode.c','th02/exit_dos.cpp','th01/vplanset.cpp','th03/initop.cpp'):
                    emitted=object_code(data);carrier=next(c for c in carriers if c['module']==owner and c['segment']==SHARED and c['size'])
                    if len(emitted)!=carrier['size']:raise ValueError('OP complete OMF/MAP emission size differs')
                    if owner=='th02/snd_mode.c' and emitted[-1]!=0x90:raise ValueError('OP OMF sound producer differs')
                    o['objects'][owner]['emitted_shared_code_sha256']=sha(emitted)
            publics={'cfg_load':'cfg_load()','cfg_save':'cfg_save()','cfg_save_exit':'cfg_save_exit()',
                     'exit_dos':'game_exit_to_dos()','planes':'vram_planes_set()','snd_mode':'_snd_determine_mode',
                     'init':'game_init_op(const unsigned char far*)','scopy':'F_SCOPY@'}
            for name,seg,orig,entry,z,cleanup,owner in RANGES:
                coords={(int(s,16),int(a,16)) for s,a in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(publics[name])+r'\s*$',text,re.MULTILINE)}
                if coords!={(seg,entry)}:raise ValueError('OP cold public MAP entry differs: '+name)
            o['fixed_comparisons']={};o['paired_observations']={}
            for name,seg,orig,entry,z,cleanup,owner in RANGES:
                if owner!='f_scopy':
                    carrier=next(c for c in carriers if c['module']==owner and c['segment']==seg and c['size'])
                    if not carrier['offset']<=entry or entry+z>carrier['offset']+carrier['size']:raise ValueError('OP cold complete function exceeds carrier')
                row=dict(segment=seg,offset=entry,start=seg*16+entry,size=z)
                o['fixed_comparisons'][name]=extent_observation(target,mz,row)
                left=target.program_image[seg*16+orig:seg*16+orig+z];right=mz.program_image[seg*16+entry:seg*16+entry+z]
                o['paired_observations'][name]=dict(original_entry=orig,cold_entry=entry,target_sha256=sha(left),cold_sha256=sha(right),raw_equal=left==right,different_bytes=sum(a!=b for a,b in zip(left,right)))
                if name!='init' and (not o['fixed_comparisons'][name]['raw_slice_equal'] or not o['fixed_comparisons'][name]['ordered_relocations_equal']):raise ValueError('OP unshifted raw/ordered comparison differs')
            if o['fixed_comparisons']['init']['raw_slice_equal'] or o['paired_observations']['init']['different_bytes']!=1:raise ValueError('OP retained shifted init failure differs')
            o['sound_producer']=extent_observation(target,mz,dict(segment=SHARED,offset=0x67,start=SHARED*16+0x67,size=1))
            if not o['sound_producer']['raw_slice_equal'] or not o['sound_producer']['ordered_relocations_equal']:raise ValueError('OP sound producer raw/relocation differs')
            for a,z,wanted in ((0x91,8,b'\0'*8),(0x166,9,b'YUME.CFG\0')):
                if target.program_image[DGROUP*16+a:DGROUP*16+a+z]!=wanted or mz.program_image[DGROUP*16+a:DGROUP*16+a+z]!=wanted:raise ValueError('OP initialized template/filename differs')
        o['cpu']=matrix(mz,not index);visited={tuple(a) for r in o['cpu'] for a in r['visited']};o['coverage']=dict(instructions=len(meta['bounds']),visited=len(meta['bounds']&visited),unvisited=[list(a) for a in sorted(meta['bounds']-visited)])
        normalize=lambda rows:[{k:v for k,v in r.items() if k not in ('visited','memory_before_sha256','memory_after_sha256')} for r in rows]
        if index and normalize(o['cpu'])!=normalize(observations[0]['cpu']):raise ValueError('OP target/cold scalar CPU contracts differ')
        observations.append(o);print('Reviewed',path,len(o['cpu']),'calls',o['coverage'],flush=True)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP input changed: '+p)
    if read_verified_artifact(ROOT,find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-op'))!=stored:raise ValueError('OP canonical target changed')
    final=frozen_files(REVISION)
    if any(final[p]!=frozen[p] for p in PROVIDERS):raise ValueError('OP frozen provider changed')
    result=dict(kind='th03-op-configuration-lifecycle-candidate-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,observations=observations,
                tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),new_decoded_bytes=472,compiler_helper_context_bytes=28,diagnostic_checks_pass=True,
                source_acceptance=False,exact_acceptance=False,new_build=False,
                notes='Original/cold init571/570 remain different, including native near-call displacement; fixed raw/ordered comparison fails. No byte normalization. Native SCOPY28 context only; models retain external file/driver/library replies. Complete OP4867-byte failure not classified here. Canonical storage/source/exact/wholefile/wholeproduct Oracles remain open.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS OP candidate diagnostics; shifted init/source/exact open')


if __name__=='__main__':main()
