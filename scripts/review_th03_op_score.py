#!/usr/bin/env python3
"""Review complete OP score CODE carriers, public loader and native IRAND."""
import argparse
from collections import Counter
from datetime import datetime,timezone
from importlib.metadata import version
import json
from pathlib import Path
import re
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from inventory_rec98_th03 import frozen_files
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact,load_target_manifest,read_verified_artifact
from review_th03_decoded_code import code_rows,extent_observation
from review_th03_mainl_cutscene import Probe,REVISION,sha

ROOT=Path(__file__).resolve().parents[1]
PROOF='.analysis/sol-op-configuration-review-20261006.json'
COLD='.analysis/th03-main-exact/sol-main-restored-aggregate-20261006/receipt.json'
PROOF_SHA='ecb383f145486d9b978408c09e40b540c37f2aff6c335a3952cd28fec2ce3fe1'
CS,DS,HI,SIZE,SEED,FNPTR=0x990,0xd7f,0x2394,206,0x312,0xa02
RANGES=[('encode',CS,0x1868,165,2,'th03/op_02.cpp'),('decode',CS,0x190d,60,0,'th03/scoredat.cpp'),
        ('recreate',CS,0x1949,127,0,'th03/scoredat.cpp'),('sum',CS,0x19c8,42,0,'th03/scoredat.cpp'),
        ('load',CS,0x19f2,107,2,'th03/op_sel.cpp'),('irand',0,0x1d12,42,'far','th03_op.asm')]
MODEL={0x8d8:('exist',4),0x898:('create',4),0x888:('close',0),0x9a8:('open',4),
       0x9e4:('seek',6),0x8f4:('read',6),0x7c8:('append',4),0xa26:('write',6)}
CALLS={0x1873:(0,0x1d12),0x187b:(0,0x1d12),0x1883:(0,0x1d12),0x18dd:(0,0x7c8),0x18f1:(0,0x9e4),0x18fd:(0,0xa26),0x1902:(0,0x888),
       0x19b8:(CS,0x1868),0x19bb:(CS,0x190d),0x19fa:(0,0x8d8),0x1a08:(0,0x898),0x1a0d:(0,0x888),0x1a19:(0,0x9a8),
       0x1a2d:(0,0x9e4),0x1a39:(0,0x8f4),0x1a3e:(0,0x888),0x1a43:(CS,0x190d),0x1a46:(CS,0x19c8),0x1a4d:(CS,0x1949)}
PROVIDERS=['th03/op_02.cpp','th03/scoredat.cpp','th03/formats/scoredat.cpp','th03/formats/scoredat.hpp','th03/formats/scorecry.hpp',
           'th03/formats/score_es.cpp','th03/formats/score_ld.cpp','th03/op_sel.cpp','th03/op/m_select.cpp','th03/op/m_select.hpp',
           'th03/common.h','th03/score.hpp','th02/score.h','th03/playchar.hpp','th03/sprites/regi.h','th01/rank.h',
           'platform.h','x86real.h','libs/master.lib/master.hpp','libs/master.lib/random.asm','libs/master.lib/rand[data].asm',
           'libs/master.lib/macros.inc','libs/master.lib/func.inc','th03_op.asm']


def analyze(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[];bounds=set();returns={};entries={};calls={}
    for name,segment,start,size,cleanup,owner in RANGES:
        body=image[segment*16+start:segment*16+start+size];ins=list(decoder.disasm(body,start));local={i.address for i in ins}
        expected=('retf','') if cleanup=='far' else ('ret',str(cleanup) if cleanup else '')
        if len(body)!=size or not ins or sum(i.size for i in ins)!=size or (ins[-1].mnemonic,ins[-1].op_str)!=expected:raise ValueError('OP score complete body/cleanup differs')
        entries[(segment,start)]=name;bounds.update((segment,i.address) for i in ins);edges=[]
        for i in ins:
            if i.mnemonic in ('ret','retf'):
                if (i.mnemonic,i.op_str)!=expected:raise ValueError('OP score interior return differs')
                returns[(segment,i.address)]=cleanup
            if i.mnemonic in ('in','out','int'):raise ValueError('OP score unexpected device/interrupt')
            if not(i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall','ljmp')):continue
            if not i.operands or any(o.type!=X86_OP_IMM for o in i.operands):raise ValueError('OP score indirect/operand edge')
            dest=tuple(o.imm for o in i.operands) if i.mnemonic=='lcall' else (segment,i.operands[0].imm)
            if i.mnemonic in ('call','lcall'):
                if CALLS.get(i.address)!=dest or i.mnemonic!=('call' if dest[0]==CS else 'lcall'):raise ValueError('OP score unknown native/model call')
                calls[(segment,i.address+i.size)]=dict(site=i.address,destination=dest)
            elif i.mnemonic=='ljmp' or dest[1] not in local:raise ValueError('OP score branch enters operand/neighbor')
            edges.append(dict(site=i.address,kind=i.mnemonic,destination=list(dest)))
        rows.append(dict(name=name,segment=segment,offset=start,size=size,cleanup=cleanup,owner=owner,sha256=sha(body),instructions=len(ins),edges=edges))
    return dict(bodies=rows,bounds=bounds,returns=returns,entries=entries,calls=calls)


def rotate(byte):return (byte>>3)|((byte&7)<<5)
def sealed(data):
    data=bytearray(data);data[:2]=(sum(data[2:])&65535).to_bytes(2,'little');return bytes(data)
def encrypt(data):
    """Mathematical backward byte feedback, with two plaintext key bytes."""
    plain=bytes(data);out=bytearray(plain);feedback=plain[205]
    for i in range(203,-1,-1):out[i]=(plain[i]-plain[204]-feedback)&255;feedback=rotate(out[i])^plain[205]
    return bytes(out)
def decrypt(data):
    encoded=bytes(data);out=bytearray(encoded)
    for i in range(203):out[i]=(encoded[i]+encoded[204]+(rotate(encoded[i+1])^encoded[205]))&255
    out[203]=(encoded[203]+encoded[204]+encoded[205])&255
    return bytes(out)
def sample(pattern=0):
    return sealed(bytes((i*(pattern*2+17)+pattern*43+7)&255 for i in range(SIZE)))
def next_random(seed):
    seed=(seed*22695477+1)&0xffffffff;return seed,(seed>>16)&32767


class ScoreSpec:
    """Stateful scalar format, file-argument and complete store specification."""
    def __init__(self,data,seed,scenario,base,filename):
        self.data=bytearray(data);self.seed=seed;self.s=scenario;self.base=base;self.filename=filename
        self.events=[];self.writes=[];self.native=Counter();self.read_write=False
    def put(self,offset,value,width=1):
        self.data[offset:offset+width]=value.to_bytes(width,'little');self.writes.append([self.base+HI+offset,width,value])
    def event(self,name,args,**extra):self.events.append(dict(name=name,args=args,**extra))
    def random(self):
        self.native['irand']+=1;self.seed,word=next_random(self.seed)
        self.writes.extend([[self.base+SEED,2,self.seed&65535],[self.base+SEED+2,2,self.seed>>16]])
        return word
    def encode(self,rank):
        self.native['encode']+=1
        for offset in (204,205,83):self.put(offset,self.random()&255)
        self.put(0,sum(self.data[2:])&65535,2);out=encrypt(self.data)
        for offset in range(203,-1,-1):self.put(offset,out[offset])
        self.event('append',self.filename);self.event('seek',[0,(rank*SIZE)&65535,0])
        self.event('write',[SIZE,HI,0x2000+DS],bytes=bytes(self.data).hex());self.event('close',[])
    def decode(self):
        self.native['decode']+=1;decoded=decrypt(self.data)
        for i in range(204):self.put(i,decoded[i])
    def invalid(self):
        self.native['sum']+=1;return int(int.from_bytes(self.data[:2],'little')!=(sum(self.data[2:])&65535))
    def recreate(self):
        self.native['recreate']+=1
        for place in range(10):
            for j in range(8):self.put(2+place*8+j,42)
            for j in range(10):self.put(84+place*10+j,32)
            self.put(184+place,0);self.put(194+place,33)
        self.put(88,33)
        for place in range(1,10):self.put(84+place*10+3,42-place)
        self.put(82,18)
        for rank in range(4):self.encode(rank);self.decode()
    def load(self,rank):
        self.native['load']+=1;self.event('exist',self.filename)
        if not self.s.get('exists',1):
            self.event('create',self.filename);self.event('close',[]);self.recreate();return 1
        self.event('open',self.filename);self.event('seek',[0,(rank*SIZE)&65535,0])
        supplied=bytes.fromhex(self.s.get('read_hex',''))
        if len(supplied)>SIZE:raise ValueError('OP score scalar read exceeds request')
        self.data[:len(supplied)]=supplied;self.read_write=True
        self.event('read',[SIZE,HI,0x2000+DS],bytes=supplied.hex());self.event('close',[])
        self.decode()
        if self.invalid():self.recreate();return 1
        return 0


class ScoreProbe(Probe):
    def __init__(self,mz,data,seed,scenario):
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc,self.reg=Uc(UC_ARCH_X86,UC_MODE_16),reg;self.uc.mem_map(0,0x100000)
        image=bytearray(mz.program_image)
        for r in mz.relocations:
            at=r.segment*16+r.offset;struct.pack_into('<H',image,at,(struct.unpack_from('<H',image,at)[0]+0x2000)&65535)
        self.uc.mem_write(0x20000,bytes(image));self.code=(0x2000+CS)*16;self.data=(0x2000+DS)*16;self.stack=0x40000
        self.meta=analyze(mz.program_image);self.s=scenario;self.frames=[];self.top=None;self.errors=[];self.stop=False;self.visited=set()
        self.events=[];self.writes=[];self.native=Counter()
        if len(data)!=SIZE:raise ValueError('OP score fixture size differs')
        self.uc.mem_write(self.data+HI,bytes(data));self.uc.mem_write(self.data+SEED,seed.to_bytes(4,'little'))
        self.filename=[int.from_bytes(self.uc.mem_read(self.data+FNPTR,2),'little'),0x2000+DS]
        for r,v in dict(DS=0x2000+DS,SS=0x4000,ES=0x3333,BP=0x7777,SI=0x1357,DI=0x2468,BX=0xbeef).items():self.set(r,v)
        self.set('EFLAGS',2|(0x200 if scenario.get('if',True) else 0)|(0x400 if scenario.get('df') else 0))
        def guard(fn,default=None):
            def invoke(*args):
                try:return fn(*args)
                except Exception as e:self.errors.append(str(e));self.uc.emu_stop();return default
            return invoke
        def code(uc,address,size,user):
            seg=self.get('CS')-0x2000;offset=address-self.get('CS')*16
            if self.get('SS')!=0x4000:raise ValueError('OP score stack segment alias')
            if address==self.code+0xff00:
                f=self.top
                if self.get('CS')!=0x2000+CS or self.get('SP')!=f['sp']+f['frame_bytes']+f['cleanup'] or self.frames or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('OP score terminal return frame differs')
                self.stop=True;uc.emu_stop();return
            if self.frames and (seg,offset)==self.frames[-1]['return_site']:
                f=self.frames.pop()
                if self.get('SP')!=f['sp']+f['frame_bytes']+f['cleanup'] or any(self.get(r)!=v for r,v in f['saved'].items()):raise ValueError('OP score native helper restoration differs')
            if seg==0 and offset in MODEL:
                name,count=MODEL[offset];sp=self.get('SP');ip,cs=struct.unpack('<HH',uc.mem_read(self.stack+sp,4))
                call=self.meta['calls'].get((cs-0x2000,ip))
                if not call or call['destination']!=(0,offset):raise ValueError('OP score interface caller differs')
                args=list(struct.unpack('<'+'H'*(count//2),uc.mem_read(self.stack+sp+4,count))) if count else []
                event=dict(name=name,args=args)
                if name in ('exist','create','open','append') and args!=self.filename:raise ValueError('OP score filename argument differs')
                if name in ('read','write'):
                    if args!=[SIZE,HI,0x2000+DS]:raise ValueError('OP score file complete buffer span differs')
                    if name=='read':
                        block=bytes.fromhex(scenario.get('read_hex',''))
                        if len(block)>SIZE:raise ValueError('OP score read model exceeds request')
                        if block:uc.mem_write(self.data+HI,block)
                        event['bytes']=block.hex()
                    else:event['bytes']=bytes(uc.mem_read(self.data+HI,SIZE)).hex()
                if name=='seek' and (len(args)!=3 or args[0] or args[2]):raise ValueError('OP score seek width/origin differs')
                self.events.append(event);self.set('AX',scenario.get('exists',1) if name=='exist' else scenario.get('reply',0xffff))
                self.set('EFLAGS',(self.get('EFLAGS')&~1)|int(scenario.get('cf',False)))
                self.set('SP',sp+4+count);self.set('CS',cs);self.set('IP',ip);return
            if (seg,offset) not in self.meta['bounds']:raise ValueError('OP score CODE segment alias/unknown boundary')
            self.visited.add((seg,offset))
            if (seg,offset) in self.meta['entries']:
                name=self.meta['entries'][(seg,offset)];self.native[name]+=1
                if self.visited_entry:
                    sp=self.get('SP');far=name=='irand';z=4 if far else 2;ip=int.from_bytes(uc.mem_read(self.stack+sp,2),'little')
                    return_seg=int.from_bytes(uc.mem_read(self.stack+sp+2,2),'little')-0x2000 if far else seg
                    caller=(return_seg,ip);call=self.meta['calls'].get(caller)
                    if not call or call['destination']!=(seg,offset):raise ValueError('OP score native helper caller differs')
                    cleanup=next(r[4] for r in RANGES if r[0]==name);cleanup=0 if far else cleanup
                    self.frames.append(dict(return_site=caller,sp=sp,frame_bytes=z,cleanup=cleanup,saved={r:self.get(r) for r in ('BP','SI','DI','DS')}))
                else:self.visited_entry=True
            if (seg,offset) in self.meta['returns']:
                f=self.frames[-1] if self.frames else self.top;sp=self.get('SP')
                ip=int.from_bytes(uc.mem_read(self.stack+sp,2),'little')
                return_seg=int.from_bytes(uc.mem_read(self.stack+sp+2,2),'little')-0x2000 if f['frame_bytes']==4 else seg
                if sp!=f['sp'] or (return_seg,ip)!=f['return_site']:raise ValueError('OP score native return frame differs')
        def write(uc,access,address,size,value,user):
            if self.stack<=address and address+size<=self.stack+65536:return
            if not any(a<=address and address+size<=a+z for a,z in ((self.data+HI,SIZE),(self.data+SEED,4))):raise ValueError('OP score store exceeds complete declared span')
            self.writes.append([address,size,value&((1<<(size*8))-1)])
        def intr(*args):raise ValueError('OP score unexpected interrupt')
        def port(*args):raise ValueError('OP score unexpected port')
        self.uc.hook_add(UC_HOOK_CODE,guard(code));self.uc.hook_add(UC_HOOK_MEM_WRITE,guard(write));self.uc.hook_add(UC_HOOK_INTR,guard(intr))
        self.uc.hook_add(UC_HOOK_INSN,guard(port),None,1,0,reg.UC_X86_INS_OUT);self.uc.hook_add(UC_HOOK_INSN,guard(port,0),None,1,0,reg.UC_X86_INS_IN)

    def run(self,name,args=(),budget=200000):
        self.stop=False;self.errors.clear();self.visited_entry=False
        row=next(r for r in self.meta['bodies'] if r['name']==name);far=row['cleanup']=='far';z=4 if far else 2
        self.set('CS',0x2000+row['segment']);self.set('SP',0xffd0)
        frame=[0xff00,0x2000+CS] if far else [0xff00]
        self.uc.mem_write(self.stack+0xffd0,struct.pack('<'+'H'*(len(frame)+len(args)),*frame,*args))
        self.top=dict(return_site=(CS,0xff00),sp=0xffd0,frame_bytes=z,cleanup=0 if far else row['cleanup'],saved={r:self.get(r) for r in ('BP','SI','DI','DS')})
        self.uc.emu_start((0x2000+row['segment'])*16+row['offset'],0x100000,count=budget)
        if self.errors:raise ValueError(self.errors[0])
        if not self.stop:raise ValueError('OP score terminal/budget differs')


def matrix(mz):
    rows=[]
    def observe(name,data,seed,s,args=()):
        p=ScoreProbe(mz,data,seed,s);before=bytes(p.uc.mem_read(0,0x100000));spec=ScoreSpec(data,seed,s,p.data,p.filename);result=None
        if name=='load':result=spec.load(args[0])
        elif name=='encode':spec.encode(args[0])
        elif name=='decode':spec.decode()
        elif name=='sum':result=spec.invalid()
        elif name=='recreate':spec.recreate()
        elif name=='irand':result=spec.random()
        else:raise ValueError('OP score unknown matrix call')
        wanted=bytearray(before);wanted[p.data+HI:p.data+HI+SIZE]=spec.data;wanted[p.data+SEED:p.data+SEED+4]=spec.seed.to_bytes(4,'little')
        p.run(name,args);actual=bytes(p.uc.mem_read(0,0x100000))
        if p.events!=spec.events or p.writes!=spec.writes or p.native!=spec.native:raise ValueError('OP score scalar ordered events/stores/native differ: '+str((name,s,args,p.events,spec.events)))
        if actual[:p.stack]!=wanted[:p.stack] or actual[p.stack+65536:]!=wanted[p.stack+65536:]:raise ValueError('OP score whole physical memory outside stack differs')
        if result is not None and p.get('AX')!=result:raise ValueError('OP score boolean/random return differs')
        if bool(p.get('EFLAGS')&0x200)!=s.get('if',True) or bool(p.get('EFLAGS')&0x400)!=bool(s.get('df')):raise ValueError('OP score IF/DF differs')
        rows.append(dict(function=name,scenario=s,args=args,result=result,seed_before=seed,seed_after=spec.seed,native_entries=dict(spec.native),events=spec.events,
                         stores=len(spec.writes),stores_sha256=sha(json.dumps(spec.writes,separators=(',',':')).encode()),hi_before_sha256=sha(data),hi_after_sha256=sha(spec.data),
                         visited=[list(a) for a in sorted(p.visited)],memory_before_sha256=sha(before),memory_after_sha256=sha(wanted)))
    for irq in (False,True):
        for df in (False,True):
            s=dict(df=df,reply=0xffff,cf=True,**{'if':irq})
            for seed in (0,1,0xffff,0x10000,0x7fffffff,0x80000000,0xffffffff,0x12345678):
                observe('irand',sample(),seed,s)
            for pattern in range(4):
                data=sample(pattern)
                for key1,key2 in ((0,0),(0,255),(255,0),(255,255),(23,197),(128,127)):
                    raw=bytearray(data);raw[204:]=bytes([key1,key2]);raw=sealed(raw)
                    observe('decode',encrypt(raw),1,s);observe('sum',raw,1,s)
                    bad=bytearray(raw);bad[17]^=1;observe('sum',bad,1,s)
                for seed in (0,1,0x80000000,0xffffffff):
                    for rank in (0,1,3,4,318,319,32767,32768,65535):observe('encode',data,seed,s,[rank])
                observe('recreate',data,0x12345678,s)
            raw=bytearray(sample());raw[82]=99;raw=sealed(raw);valid=encrypt(raw);bad=bytearray(valid);bad[0]^=1
            for rank in (0,3,4,318,319,32767,32768,65535):
                for exists,initial,read in ((0,sample(),b''),(1,valid,valid),(1,valid,b''),(65535,valid,valid),(1,valid,bytes(bad)),
                                           (1,sample(),valid[:1]),(1,sample(),valid[:100]),(1,valid,valid[:205])):
                    observe('load',initial,0x80000000,dict(s,exists=exists,read_hex=read.hex()),[rank])
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('OP score prior proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw)}
    for p in ['scripts/review_th03_op_score.py','tests/test_op_score_review.py','scripts/inventory_rec98_th03.py','scripts/review_th03_mainl_cutscene.py']:
        inputs[p]=sha((ROOT/p).read_bytes())
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP score input changed: '+p)
    frozen=frozen_files(REVISION);artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-op');stored=read_verified_artifact(ROOT,artifact);observations=[]
    target=parse_mz((ROOT/proof['observations'][0]['path']).read_bytes())
    for index,previous in enumerate(proof['observations']):
        path=previous['path'];mz=parse_mz((ROOT/path).read_bytes());meta=analyze(mz.program_image);o=dict(path=path,bodies=meta['bodies'])
        if not mz.valid:raise ValueError('OP score invalid MZ')
        if index:
            tree=Path(path).parents[2];o['source_lineage']={};o['objects']={}
            for p in PROVIDERS:
                cp=str(tree/p);data=(ROOT/cp).read_bytes();inputs[cp]=sha(data);wanted=frozen[p]
                if p.endswith(('.asm','.inc')):data=data.replace(b'\r\n',b'\n');wanted=wanted.replace(b'\r\n',b'\n')
                if data!=wanted:raise ValueError('OP score frozen source provider differs: '+p)
                o['source_lineage'][p]=dict(frozen_sha256=sha(frozen[p]),cached_sha256=inputs[cp])
            mp=str(tree/'obj/th03/op.map');text=(ROOT/mp).read_text();carriers=code_rows(text,len(mz.program_image));o['comparisons']={}
            cold=json.loads((ROOT/COLD).read_bytes())
            for module,object_name in [('th03/op_02.cpp','obj/th03/op_02.obj'),('th03/scoredat.cpp','obj/th03/scoredat.obj'),('th03/op_sel.cpp','obj/th03/op_sel.obj')]:
                cp=str(tree/object_name);data=(ROOT/cp).read_bytes();inputs[cp]=sha(data);obj=describe_omf(data)
                if not obj['valid'] or obj['dependency_timestamp_normalized_sha256']!=cold['rounds'][index-1]['all_objects'][object_name]:raise ValueError('OP score cold normalized OMF differs')
                o['objects'][module]=dict(path=cp,normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'])
            publics={'encode':'scoredat_encode_and_save(rank_t)','decode':'scoredat_decode()','recreate':'scoredat_recreate()','sum':'scoredat_sum_invalid()','load':'scoredat_load_and_decode(rank_t)','irand':'IRAND'}
            for name,seg,a,z,c,owner in RANGES:
                coords={(int(s,16),int(off,16)) for s,off in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(publics[name])+r'\s*$',text,re.MULTILINE)}
                if coords!={(seg,a)}:raise ValueError('OP score public MAP entry differs')
                carrier=next(c for c in carriers if c['module']==owner and c['segment']==seg and c['size'])
                if not carrier['offset']<=a or a+z>carrier['offset']+carrier['size']:raise ValueError('OP score extent exceeds carrier')
                comp=extent_observation(target,mz,dict(segment=seg,offset=a,start=seg*16+a,size=z));o['comparisons'][name]=comp
                if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('OP score raw/originalordered relocation differs')
            o['initialized_data']={}
            for name,a,wanted in [('seed',SEED,b'\x01\0\0\0'),('filename-pointer',FNPTR,struct.pack('<H',0xa04)),('filename',0xa04,b'YUME.NEM\0')]:
                z=len(wanted);comp=extent_observation(target,mz,dict(segment=DS,offset=a,start=DS*16+a,size=z))
                if target.program_image[DS*16+a:DS*16+a+z]!=wanted or not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('OP score bounded initialized data differs')
                o['initialized_data'][name]=comp
        o['cpu']=matrix(mz);visited={tuple(a) for r in o['cpu'] for a in r['visited']};o['coverage']=dict(instructions=len(meta['bounds']),visited=len(meta['bounds']&visited),unvisited=[list(a) for a in sorted(meta['bounds']-visited)])
        normalize=lambda rows:[{k:v for k,v in r.items() if k not in ('memory_before_sha256','memory_after_sha256')} for r in rows]
        if index and (o['bodies']!=observations[0]['bodies'] or normalize(o['cpu'])!=normalize(observations[0]['cpu'])):raise ValueError('OP score target/cold native contracts differ')
        observations.append(o);print('Reviewed',path,len(o['cpu']),'calls',o['coverage'],flush=True)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP score input changed: '+p)
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('OP score stored target changed')
    final=frozen_files(REVISION)
    if any(final[p]!=frozen[p] for p in PROVIDERS):raise ValueError('OP score frozen source changed')
    result=dict(kind='th03-op-score-complete-carrier-and-loader-review',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,observations=observations,
                tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),new_decoded_bytes=543,diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,new_build=False,
                notes='Two complete direct CPP CODE carriers394, complete public scoreloader107 and independently reviewed native IRAND42. Original raw/ordered relocation equality is bounded decoded observation only. Mathematical format/LCG spec, real native calls/frames/stores and full memory outside stack; file/library reply models do not establish DOS persistence, allocation/dependency/canonicalstorage or completeproduct/runtime/source/exact Oracle acceptance.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS OP score candidate diagnostics; source/exact open')


if __name__=='__main__':main()
