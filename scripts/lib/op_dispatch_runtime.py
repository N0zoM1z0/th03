"""Execute demo/score dispatch, real cfg save, sound routing and game cleanup.

The independent contract retains BYTE demo wrap, adjacent table reads and the
failed-execl path. Files, sound replies, graphics libraries and exec are bounded
interfaces; successful process replacement and physical hardware are not proved.
"""
from dataclasses import replace
import hashlib
import json
import struct

from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import Uc,UcError,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
from unicorn.x86_const import *
from lib.op_dispatch_layout import SEGMENT,OFFSET,DATA_SEGMENT,FUNCTIONS
from lib.op_cfg_runtime import RESIDENT,ACTIVE,MIDI,reply
from lib.op_exit_runtime import SERVICES as EXIT_SERVICES,specification as exit_events

REG={n:globals()['UC_X86_REG_'+n.upper()] for n in ('ax','bx','cx','dx','si','di','bp','sp','cs','ds','es','ss','ip')}
GPRS={n:globals()['UC_X86_REG_E'+n.upper()] for n in ('ax','bx','cx','dx','si','di','bp')}
ENTRIES={name:(SEGMENT*16+OFFSET+off,size) for _,name,off,size in FUNCTIONS}
HELPERS=((0x9980,67),(0xBFC2,67),(0xC403,30))
SERVICES={**{k:(v,0) for k,v in EXIT_SERVICES.items()},0x536:('palette_black_out',2),
 0xF1A:('gaiji_restore',0),0x269A:('super_free',0),0x9119:('execl',0),
 0x7C8:('append',4),0x9E4:('seek',6),0xA26:('write',6),0x888:('close',0)}
PAIRINGS=(3,1,5,13,7,11,9,5)
SEEDS=(600,1000,3200,500)


def need(value,message):
    if not value:raise ValueError('OP dispatch contract: '+str(message))


def add_flags(left,right):
    value=(left+right)&65535
    return ((left+right>65535)| (4 if (value&255).bit_count()%2==0 else 0)
        |((left^right^value)&16)|(64 if value==0 else 0)|(value>>8&128)
        |((~(left^right)&(left^value)&0x8000)>>4))


class Machine:
    def __init__(self,mz,load):
        need(mz.valid,'valid decoded MZ')
        self.base=load*16;self.cs=load+SEGMENT;self.ds=load+DATA_SEGMENT;self.data=self.ds*16
        self.uc=Uc(UC_ARCH_X86,UC_MODE_16);self.uc.mem_map(0,1<<20)
        self.initial=bytearray(b'\xA5'*(1<<20));body=mz.relocated_program_image(load);self.initial[self.base:self.base+len(body)]=body
        self.instructions={};self.owned={p for start,size in ENTRIES.values() for p in range(start,start+size)}
        self.nested={p for start,size in HELPERS for p in range(start,start+size)}
        for start,size in (*ENTRIES.values(),*HELPERS):
            rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[start:start+size],start))
            need(sum(r.size for r in rows)==size,'complete root/helper instruction boundaries')
            self.instructions.update({r.address:r.size for r in rows})
        self.covered=set();self.nested_covered=set();self.maximum_stack=0
        self.hooks=[self.uc.hook_add(UC_HOOK_CODE,self.code),self.uc.hook_add(UC_HOOK_MEM_WRITE,self.write),
            self.uc.hook_add(UC_HOOK_INTR,self.interrupt),self.uc.hook_add(UC_HOOK_INSN,self.out,None,1,0,UC_X86_INS_OUT)]
    def close(self):
        for h in self.hooks:self.uc.hook_del(h)
        self.hooks=[];self.uc=None
    def r(self,n):return self.uc.reg_read(REG[n])&65535
    def fail(self,error):self.error=str(error);self.uc.emu_stop()
    def event(self,event):
        need(self.index<len(self.events) and event==self.events[self.index],f'ordered event #{self.index}: {event}')
        self.index+=1
    def response(self):
        self.calls+=1
        values,flags=reply({n:self.r(n) for n in REG},self.calls,self.seed,self.uc.reg_read(UC_X86_REG_EFLAGS),self.status)
        for n in ('ax','bx','cx','dx','es'):self.uc.reg_write(REG[n],values[n])
        self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
    def code(self,uc,address,size,_):
        try:
            if address==self.cs*16+0xFFFF:self.returned=True;uc.emu_stop();return
            self.maximum_stack=max(self.maximum_stack,self.stack-self.r('sp'))
            rva=address-self.base
            if rva in SERVICES:
                kind,args=SERVICES[rva];sp=0x70000+self.r('sp');ip,cs=struct.unpack('<HH',bytes(uc.mem_read(sp,4)))
                need(cs*16+ip-self.base in self.instructions,'real far service frame returns to root/helper')
                payload=None
                if kind=='palette_black_out':payload=struct.unpack('<H',bytes(uc.mem_read(sp+4,2)))[0]
                elif kind=='append':
                    off,seg=struct.unpack('<HH',bytes(uc.mem_read(sp+4,4)));need((off,seg)==(0x166,self.ds),'real cfg filename pointer')
                    payload=bytes(uc.mem_read(seg*16+off,9)).hex()
                elif kind=='seek':
                    origin,offset=struct.unpack('<HI',bytes(uc.mem_read(sp+4,6)));payload=(offset,origin)
                elif kind=='write':
                    count,off,seg=struct.unpack('<HHH',bytes(uc.mem_read(sp+4,6)))
                    payload=(seg,off,count,bytes(uc.mem_read(seg*16+off,count)).hex())
                    self.file[:count]=bytes.fromhex(payload[3])
                elif kind=='execl':
                    payload=tuple(struct.unpack('<6H',bytes(uc.mem_read(sp+4,12))))
                    need(bytes(uc.mem_read(self.data+0x16F,6))==b'mainl\0','actual lowercase MAINL exec filename')
                self.event(('service',kind,payload));self.response()
                uc.reg_write(REG['sp'],self.r('sp')+4+args);uc.reg_write(REG['cs'],cs);uc.reg_write(REG['ip'],ip);return
            need(self.instructions.get(rva)==size,'execution outside complete root/helper instructions')
            self.covered.update(set(range(rva,rva+size))&self.owned)
            self.nested_covered.update(set(range(rva,rva+size))&self.nested)
        except Exception as error:self.fail(error)
    def write(self,uc,access,address,size,value,_):
        try:
            if 0x70000+self.stack-80<=address and address+size<=0x70000+self.stack:
                self.maximum_stack=max(self.maximum_stack,0x70000+self.stack-address);return
            self.event(('store',address,size,value))
        except Exception as error:self.fail(error)
    def out(self,uc,port,size,value,_):
        try:self.event(('out',port,value));need(size==1,'BYTE video port writes')
        except Exception as error:self.fail(error)
    def interrupt(self,uc,number,_):
        try:self.event(('interrupt',number,self.r('ax')));self.response()
        except Exception as error:self.fail(error)
    def run(self,kind,*,demo=0,resoff=0x31,resseg=0x6000,active=1,midi=0,resident_seed=0xA5,
            options=(0x81,0x52,0xA3),trash=0xD3,seed=0x1357,status=0xFFFF,flags=0x202,stack=0xF800):
        need(kind in ENTRIES and all(0<=v<=255 for v in (demo,active,midi,resident_seed,trash,*options)),'bounded BYTE input')
        need(resseg in (0x5000,0x6000) and 0<=resoff<=0xFF80 and 80<=stack<=0xFFF0,'mapped disjoint far resident and bounded stack')
        self.uc.mem_write(0,bytes(self.initial));self.stack,self.seed,self.status=stack,seed,status
        self.uc.mem_write(0x70000+stack-80,bytes((trash,))*80);self.uc.mem_write(0x70000+stack,b'\xFF\xFF\x5A\xA5')
        self.uc.mem_write(self.data+RESIDENT,struct.pack('<HH',resoff,resseg));self.uc.mem_write(self.data+ACTIVE,bytes((active,)))
        self.uc.mem_write(self.data+MIDI,bytes((midi,)));base=resseg*16+resoff
        self.uc.mem_write(base,bytes((resident_seed,))*0x60);self.uc.mem_write(base+0x39,bytes((demo,)))
        for off,value in zip((0x15,0x16,0xB),options):self.uc.mem_write(base+off,bytes((value,)))
        self.memory=bytearray(self.uc.mem_read(0,1<<20));self.events=[]
        def store(off,size,value):
            self.events.append(('store',base+off,size,value));self.memory[base+off:base+off+size]=value.to_bytes(size,'little')
        if kind=='start_demo':
            store(0xE,1,1);store(0xF,1,1);num=(demo+1)&255;store(0x39,1,num)
            if num>4:num=1;store(0x39,1,1)
            for off,val in ((0x17,0),(0x33,0),(0x28,0x7F),(0x35,0)):store(off,1,val)
            pair=PAIRINGS[(num-1)*2:num*2] if num else (0x8F,0)
            for off,val in zip((0xC,0xD),pair):store(off,1,val)
            random=SEEDS[num-1] if num else 0x05090B07;store(0x10,4,random)
        else:
            random=None
            for off,val in ((0x33,0xFF),(0x35,1),(0x28,0)):store(off,1,val)
        for i in range(16):store(0x18+i,1,0)
        if kind=='start_demo':self.events.append(('service','palette_black_out',1))
        self.expected_file=bytes((*options,trash,0x57,0,0x50,0xA7));self.file=bytearray(b'\x02\x01\x03\x48\x57\0\x50\xA7')
        self.events += [('service','append',b'YUME.CFG\0'.hex()),('service','seek',(0,0)),
            ('service','write',(0x7000,stack-16,4,self.expected_file[:4].hex())),('service','close',None),('service','gaiji_restore',None)]
        if active:self.events.append(('interrupt',0x61 if midi==1 else 0x60,0x100))
        if kind=='score_menu':self.events.append(('service','super_free',None))
        self.events += [row if row[0]=='out' else ('service',row[0],None) for row in exit_events('exit')]
        self.events.append(('service','execl',(0x16F,self.ds,0x16F,self.ds,0,0)))
        initial={n:((seed+i*0x231)&65535) for i,n in enumerate(GPRS)}
        high={n:((seed^0x5AA5)<<16) for n in GPRS}
        for n in GPRS:self.uc.reg_write(GPRS[n],high[n]|initial[n])
        initial.update(es=seed,cs=self.cs,ds=self.ds,ss=0x7000)
        for n in ('es','cs','ds','ss'):self.uc.reg_write(REG[n],initial[n])
        self.uc.reg_write(REG['sp'],stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        self.calls,self.index,self.error,self.returned=0,0,None,False
        try:self.uc.emu_start(self.base+ENTRIES[kind][0],0x100000,count=2000)
        except UcError as error:raise ValueError('OP dispatch contract: guest fault') from error
        need(self.error is None,self.error or 'guest error')
        need(self.returned and self.r('sp')==stack+2,'near return/no arguments; cdecl execl cleanup')
        count=sum(row[0] in ('service','interrupt') for row in self.events)
        expected,_=reply(initial,count,seed,flags,status)
        if kind=='score_menu':expected['ax']&=0xFF00 # Native bool return writes only AL.
        actual={n:self.r(n) for n in expected};need(actual==expected,'independent final register contract')
        full={n:self.uc.reg_read(GPRS[n]) for n in GPRS}
        for n in GPRS:
            upper=(random&0xFFFF0000) if n=='ax' and random is not None else high[n]
            need(full[n]==upper|expected[n],'full 32-bit register: '+n)
        actual_flags=self.uc.reg_read(UC_X86_REG_EFLAGS)
        need(actual_flags&0x8D5==add_flags(stack-16,12),'final cdecl stack arithmetic flags')
        need(actual_flags&0x600==flags&0x600,'inherited IF/DF')
        need(self.index==len(self.events) and self.file==self.expected_file,'complete dispatch/file/port transaction')
        memory=bytes(self.uc.mem_read(0,1<<20));lo,hi=0x70000+stack-80,0x70000+stack
        self.memory[lo:hi]=memory[lo:hi];need(memory==self.memory,'whole memory outside bounded stack')
        return dict(registers=actual,full_registers=full,file_hex=self.file.hex(),events=self.events,flags=actual_flags&0xED5)


def cases():
    for value in range(256):
        yield 'start_demo',dict(demo=value)
        yield 'start_demo',dict(demo=value,active=value,midi=value,options=(value,value^0x55,value^0xAA))
        yield 'score_menu',dict(active=value,midi=value,options=(value,value^0x55,value^0xAA))
        yield 'score_menu',dict(active=1,midi=value,trash=value)
    for kind in ENTRIES:
        for segment in (0x5000,0x6000):
            for off in (0,0x31,0xFF80):
                for status in (0,0x7FFF,0x8000,0xFFFF):
                    yield kind,dict(resseg=segment,resoff=off,status=status,resident_seed=status&255)


def verify(target,candidate):
    observations=[]
    for mz in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(mz,load)
            try:
                trace=hashlib.sha256()
                for count,(kind,options) in enumerate(cases(),1):
                    row=m.run(kind,seed=0x1357 if count&1 else 0xECA8,flags=(2,0x202,0x402,0xED7)[count%4],stack=0x80 if count&1 else 0xFFF0,**options)
                    trace.update(json.dumps(row,sort_keys=True).encode())
                need(m.covered==m.owned and m.nested_covered==m.nested,'all root and nested helper instruction bytes execute')
                loads.append(dict(load_segment=load,cases=count,covered_owner_bytes=len(m.covered),executed_nested_bytes=len(m.nested_covered),
                    maximum_observed_stack_depth=m.maximum_stack,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent target/candidate dispatch observations')
    return dict(images=2,functions=2,code_bytes=296,cases_per_image=sum(o['cases'] for o in observations[0]),
        exhaustive_demo_bytes=256,exhaustive_sound_flag_bytes=256,executed_owner_bytes=296,observations=observations[0],
        scope='real cfg save, sound routing and game cleanup; failed execl, bounded external libraries/files/driver; no successful exec or physical hardware claim')


def negative_controls(target):
    controls=(
        ('both-players-are-CPU',0x9D58,b'\x01',b'\0','start_demo',{}),
        ('demo-four-is-valid',0x9D66,b'\x04',b'\x03','start_demo',dict(demo=3)),
        ('demo-bound-is-unsigned',0x9D67,b'\x76',b'\x7E','start_demo',dict(demo=127)),
        ('wrapped-byte-remains-zero',0x9D60,b'\x47',b'\x4F','start_demo',dict(demo=255)),
        ('stage-is-deterministic',0x9D7B,b'\0',b'\x01','start_demo',{}),
        ('demo-mode-byte',0x9D80,b'\x7F',b'\x7E','start_demo',{}),
        ('pairing-origin',0x9D92,b'\xC2',b'\xC4','start_demo',{}),
        ('seed-index-is-DWORD',0x9DBE,b'\x02',b'\x01','start_demo',{}),
        ('all-sixteen-score-digits',0x9DE1,b'\x10',b'\x0F','start_demo',{}),
        ('fade-one-frame',0x9DE5,b'\x01',b'\x02','start_demo',{}),
        ('ordinary-cfg-save',0x9DEC,b'\x92\xFB',b'\xD5\xFB','start_demo',{}),
        ('gaiji-restored-before-exit',0x9DEF,b'\x1A\x0F',b'\x4C\x11','start_demo',{}),
        ('stop-command-low-byte',0x9DF4,b'\0',b'\x01','start_demo',{}),
        ('far-null-terminator',0x9E00,b'\x66',b'\x90','start_demo',{}),
        ('duplicate-exec-argv0',0x9E09,b'\x6F',b'\x70','start_demo',{}),
        ('near-demo-return',0x9E15,b'\xC3',b'\xCB','start_demo',{}),
        ('score-stage-none',0x9E8B,b'\xFF',b'\0','score_menu',{}),
        ('score-window-free',0x9EBC,b'\x9A\x26',b'\x9B\x26','score_menu',{}),
        ('cdecl-twelve-byte-cleanup',0x9ED7,b'\x0C',b'\x08','score_menu',{}),
        ('false-is-AL-zero',0x9ED9,b'\0',b'\x01','score_menu',{}),
        ('nested-save-four-bytes',0x99B6,b'\x04',b'\x08','score_menu',{}),
        ('real-sound-MIDI-byte-one',0xC414,b'\x01',b'\0','score_menu',dict(midi=1)),
        ('real-cleanup-page-order',0xBFCE,b'\x01',b'\0','score_menu',{}),
    )
    rejected=[]
    for name,at,old,new,kind,options in controls:
        raw=bytearray(target.program_image);need(raw[at:at+len(old)]==old,'literal mutation anchor '+name)
        raw[at:at+len(new)]=new
        m=None
        try:
            try:
                m=Machine(replace(target,program_image=bytes(raw)),0x3000);m.run(kind,**options)
            except ValueError:rejected.append(name)
            else:raise ValueError('OP dispatch mutation survived: '+name)
        finally:
            if m:m.close()
    return dict(count=len(rejected),rejected=rejected)
