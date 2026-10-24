"""Independent shared sound/file/timing contracts for explicit OP/MAINL layouts.

DOS and PMD/MMD replies are bounded register/memory interfaces. Counter updates
are an explicit finite input stream, not a claim about physical IRQ delivery or
elapsed frames. File errors, unchecked array indices and suffix overflow remain.
"""
import hashlib,json,struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import Uc,UcError,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR
from unicorn.x86_const import *
from lib.decoded_mainl_sound_layout import CS,DS,PRODUCERS,GLOBALS
from lib.op_sound_layout import CS as OP_CS, DS as OP_DS, ENTRIES as OP_ENTRIES, RUNTIME_FIELDS as OP_FIELDS

REG={n:globals()['UC_X86_REG_'+n.upper()] for n in ('ax','bx','cx','dx','si','di','bp','sp','cs','ds','es','ss','ip')}
GPRS={n:globals()['UC_X86_REG_E'+n.upper()] for n in ('ax','bx','cx','dx','si','di','bp')}
ENTRIES={suffix.removeprefix('sound-').replace('linked-tail-delay','frame_delay'):(CS*16+off+a,size,args,pop)
 for _,_,_,_,_,_,off,_,functions in PRODUCERS for suffix,_,a,size,args,pop in functions}
F={name.removeprefix('_snd_').removeprefix('_'):off for name,off in GLOBALS.items()}
F['counter']=GLOBALS['_vsync_Count1']
def need(v,m):
    if not v:raise ValueError('MAINL sound contract: '+str(m))
def compare(a,b,byte=False):
    mask=255 if byte else 65535;sign=128 if byte else 32768;v=(a-b)&mask
    return int(a<b)|(4 if (v&255).bit_count()%2==0 else 0)|((a^b^v)&16)|(64 if not v else 0)|(128 if v&sign else 0)|(0x800 if (a^b)&(a^v)&sign else 0)
def cstring(memory,a):
    end=memory.find(b'\0',a,a+256);need(end>=a,'finite filename interface');return bytes(memory[a:end+1])

class Prediction:
    def __init__(self,memory,regs,data,sp,p,fields=None):
        self.f=F if fields is None else fields;self.memory=bytearray(memory);self.regs=dict(regs);self.data=data;self.sp=sp;self.p=p;self.events=[];self.flags=p['flags'];self.driver_count=0;self.counter_updates=0
    def byte(self,name):return self.memory[self.data+self.f[name]]
    def put(self,name,size,value):self.store(self.data+self.f[name],size,value)
    def store(self,a,size,value):
        value&=(1<<(size*8))-1;self.events.append(dict(kind='store',address=a,size=size,value=value));self.memory[a:a+size]=value.to_bytes(size,'little')
    def cmp(self,a,b,byte=False):self.flags=(self.flags&0x600)|compare(a,b,byte)|2
    def interrupt(self,vector,kind):
        p=self.p;request=dict(self.regs);post=dict(request);transfers=[];self.driver_count+=int(vector in (0x60,0x61))
        if kind=='open':post['ax']=p['open_result'];carry=p['open_failure']
        elif kind=='read':
            post['ax']=p['read_result'] if p['read_failure'] else p['read_count'];carry=p['read_failure']
            if not carry:
                a=request['ds']*16+request['dx'];raw=bytes((i*29+0x31)&255 for i in range(p['read_count']))
                transfers.append((a,raw.hex()));self.memory[a:a+len(raw)]=raw
        elif kind=='close':post['ax']=p['close_result'];carry=p['close_failure']
        else:
            i=self.driver_count
            post.update(ax=p['measures'][i-1] if kind=='measure' else p['driver_ax'],cx=(p['seed']^0xA316^i)&65535,es=(p['seed']^0x98AB^i)&65535)
            if kind=='buffer':post.update(ds=p['buffer_segment'],dx=p['buffer_offset'])
            else:post.update(bx=(p['seed']^0xB247^i)&65535,dx=(p['seed']^0xD469^i)&65535)
            carry=bool(i&1)
        flags=(p['flags']&0x600)|((p['seed']+self.driver_count*0x149+len(self.events))&0x8D4)|int(carry)|2
        e=dict(kind='interrupt',vector=vector,service=kind,request=request,post=dict(post),flags=flags,transfers=transfers)
        if kind=='open':e['filename_hex']=cstring(self.memory,request['ds']*16+request['dx']).hex()
        self.events.append(e);self.regs=post;self.flags=flags
    def frame_delay(self,frames):
        self.put('counter',2,0)
        for i,value in enumerate(self.p['ticks']):
            self.events.append(dict(kind='tick',value=value));a=self.data+self.f['counter'];self.memory[a:a+2]=value.to_bytes(2,'little');self.regs['ax']=value;self.counter_updates+=1
            self.cmp(value,frames)
            if value>=frames:
                need(i==len(self.p['ticks'])-1,'counter stream ends at first unsigned limit');return
        raise ValueError('MAINL sound contract: finite counter stream must terminate')
    def run(self,kind):
        p=self.p;r=self.regs;bp,si=r['bp'],r['si']
        if kind!='update':r['bp']=self.sp-2
        if kind=='play':
            r['dx']=p['argument'];self.cmp(self.byte('fm_possible'),0,True)
            if self.byte('fm_possible'):
                current=self.byte('se_playing');self.cmp(current,255,True)
                if current==255:self.put('se_playing',1,p['argument'])
                else:
                    a=self.data+self.f['se_priorities'];priority=self.memory[a+current];new=self.memory[self.data+((self.f['se_priorities']+p['argument'])&65535)]
                    r['ax']=priority;r['bx']=p['argument'];self.cmp(priority,new,True)
                    if priority<=new:self.put('se_playing',1,p['argument']);self.put('se_frame',1,0)
        elif kind=='update':
            self.cmp(self.byte('fm_possible'),0,True)
            if self.byte('fm_possible'):
                current=self.byte('se_playing');self.cmp(current,255,True)
                if current!=255:
                    frame=self.byte('se_frame');self.cmp(frame,0,True)
                    if not frame:
                        r['ax']=0xC00|current;self.interrupt(0x60,'se');r=self.regs
                    self.put('se_frame',1,frame+1);r['bx']=current;r['ax']=self.memory[self.data+self.f['se_priority_frames']+current]
                    self.cmp(r['ax'],self.byte('se_frame'),True)
                    if r['ax']<self.byte('se_frame'):self.put('se_frame',1,0);self.put('se_playing',1,255)
        elif kind=='kaja':
            self.cmp(self.byte('active'),0,True)
            if self.byte('active'):
                r['ax']=p['argument'];self.cmp(self.byte('midi_active'),1,True);self.interrupt(0x61 if self.byte('midi_active')==1 else 0x60,'kaja');r=self.regs
        elif kind=='frame_delay':self.frame_delay(p['frames'])
        elif kind=='measure':
            self.cmp(self.byte('active'),0,True)
            if not self.byte('active'):self.frame_delay(p['frames'])
            else:
                for i,value in enumerate(p['measures']):
                    r['ax']=0x500|(r['ax']&255);self.cmp(self.byte('midi_active'),1,True);mmd=self.byte('midi_active')==1
                    if mmd:r['dx']=192
                    self.interrupt(0x61 if mmd else 0x60,'measure');r=self.regs;self.cmp(r['ax'],p['measure'])
                    if r['ax']>=p['measure']:
                        need(i==len(p['measures'])-1,'measure stream ends at first unsigned limit');break
                else:raise ValueError('MAINL sound contract: finite measure stream must terminate')
        else:
            need(kind=='load','known root');r['cx']=13;r['es']=p['filename_segment']
            for i in range(13):
                r['bx']=(p['filename_offset']+i)&65535;value=self.memory[p['filename_segment']*16+r['bx']];r['ax']=r['ax']&0xFF00|value
                self.store(self.data+self.f['load_fn']+i,1,value)
            r['cx']=0;r['si']=13;r['ax']=p['function'];mmd=p['function']==0x600 and self.byte('midi_active')!=0
            if mmd:
                r['bx']=1
                while self.memory[self.data+((self.f['load_fn']+r['bx'])&65535)]:
                    r['bx']=(r['bx']+1)&65535;need(r['bx']<128,'bounded suffix fixture')
                for i,b in enumerate(b'md\0'):self.store(self.data+((self.f['load_fn']+r['bx']+i)&65535),1,b)
            r['dx']=self.f['load_fn'];r['ax']=0x3D00;self.interrupt(0x21,'open');r=self.regs;r['bx']=r['ax'];r['ax']=p['function']
            self.interrupt(0x61 if mmd else 0x60,'buffer');r=self.regs;r['ax']=0x3F00;r['cx']=0x5000;self.interrupt(0x21,'read');r=self.regs
            r['ds']=self.data//16;r['ax']=0x3E00|(r['ax']&255);self.interrupt(0x21,'close');r=self.regs;r['si']=si
        self.regs['bp']=bp;self.regs['cs']=0x8000

class Machine:
    def __init__(self,mz,load,profile="mainl"):
        need(mz.valid and profile in ('mainl','op'),'valid MZ/profile');self.profile=profile;self.entries=ENTRIES if profile=='mainl' else OP_ENTRIES;self.fields=F if profile=='mainl' else OP_FIELDS
        self.base=load*16;self.cs=load+(CS if profile=='mainl' else OP_CS);self.ds=load+(DS if profile=='mainl' else OP_DS);self.data=self.ds*16
        self.uc=Uc(UC_ARCH_X86,UC_MODE_16);self.uc.mem_map(0,1<<20);self.initial=bytearray(b'\xA5'*(1<<20));body=mz.relocated_program_image(load);self.initial[self.base:self.base+len(body)]=body
        self.instructions={};self.owned=set()
        for start,size,*_ in self.entries.values():
            rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[start:start+size],start));need(sum(i.size for i in rows)==size,'complete instruction boundaries')
            self.instructions.update({i.address:i.size for i in rows});self.owned.update(range(start,start+size))
        self.covered=set();self.maximum_stack=0;self.hooks=[self.uc.hook_add(UC_HOOK_CODE,self.code),self.uc.hook_add(UC_HOOK_MEM_WRITE,self.write),self.uc.hook_add(UC_HOOK_INTR,self.interrupt)]
    def close(self):
        for h in self.hooks:self.uc.hook_del(h)
        self.hooks=[];self.uc=None
    def r(self,n):return self.uc.reg_read(REG[n])&65535
    def registers(self):return {n:self.r(n) for n in (*GPRS,'cs','ds','es','ss')}
    def fail(self,e):self.error=str(e);self.uc.emu_stop()
    def event(self,actual):
        need(self.index<len(self.expected.events) and actual==self.expected.events[self.index],f'ordered event {self.index}: {actual}; expected {self.expected.events[self.index:self.index+1]}');self.index+=1
    def code(self,uc,address,size,_):
        try:
            if address==0x80040:self.returned=True;uc.emu_stop();return
            rva=address-self.base;need(self.instructions.get(rva)==size,'execution outside whole maintained instructions: '+hex(rva));self.covered.update(range(rva,rva+size));self.maximum_stack=max(self.maximum_stack,self.stack-self.r('sp'))
            if rva==self.entries['frame_delay'][0]+9:
                need(self.index<len(self.expected.events),'counter fixture event');e=self.expected.events[self.index];need(e['kind']=='tick','ordered counter read');self.event(e)
                uc.mem_write(self.data+self.fields['counter'],e['value'].to_bytes(2,'little'))
        except Exception as e:self.fail(e)
    def write(self,uc,access,address,size,value,_):
        try:
            if 0x70000+self.stack-32<=address and address+size<=0x70000+self.stack:
                self.maximum_stack=max(self.maximum_stack,0x70000+self.stack-address);return
            self.event(dict(kind='store',address=address,size=size,value=value))
        except Exception as e:self.fail(e)
    def interrupt(self,uc,vector,_):
        try:
            need(self.index<len(self.expected.events),'bounded interrupt schedule');e=self.expected.events[self.index]
            need(e['kind']=='interrupt' and e['vector']==vector and self.registers()==e['request'],'independent interrupt request '+str((vector,self.registers(),e)))
            need(uc.reg_read(UC_X86_REG_EFLAGS)&0x600==self.flags&0x600,'interface inherits IF/DF')
            if e['service']=='open':need(cstring(bytes(uc.mem_read(0,1<<20)),self.r('ds')*16+self.r('dx')).hex()==e['filename_hex'],'actual unchecked filename/suffix')
            self.event(e)
            for a,raw in e['transfers']:uc.mem_write(a,bytes.fromhex(raw))
            for n,v in e['post'].items():
                if v!=e['request'][n]:uc.reg_write(REG[n],v)
            uc.reg_write(UC_X86_REG_EFLAGS,e['flags'])
        except Exception as e:self.fail(e)
    def run(self,kind,*,fm=1,active=1,midi=0,playing=255,frame=0,argument=1,frames=2,ticks=(0,1,2),measure=2,measures=(0,1,2),
            filename=b'SONG.M\0TRASH!',filename_offset=0x20,filename_segment=0x5000,function=0x600,suffix_end=16,
            open_result=7,open_failure=False,read_count=13,read_failure=False,read_result=6,close_result=0xBEEF,close_failure=False,
            buffer_segment=0x6000,buffer_offset=0x800,driver_ax=0xFA97,priority_patch=(),duration_patch=(),seed=0x1357,flags=0x202,stack=0xF800):
        need(kind in self.entries and all(0<=v<=255 for v in (fm,active,midi,playing,frame)),'bounded root and BYTE states')
        need(all(0<=v<=65535 for v in (argument,frames,measure,filename_offset,function,open_result,read_result,close_result,buffer_offset,driver_ax)),'WORD interface fields')
        need(len(filename)==13 and filename_segment in (0x5000,0x6000) and buffer_segment in (0x5000,0x6000),'disjoint far filename/buffer fixtures')
        need(13<=suffix_end<=32 and 0<=read_count<=0x5000 and buffer_offset+read_count<=65536 and 64<=stack<=0xFFF0,'bounded transfer/stack/suffix fixture')
        need(1<=len(ticks)<=4 and 1<=len(measures)<=4 and all(0<=v<=65535 for v in (*ticks,*measures)),'finite WORD counter/driver streams')
        self.uc.mem_write(0,bytes(self.initial));self.stack,self.flags=stack,flags
        for name,value in (('fm_possible',fm),('active',active),('midi_active',midi),('se_playing',playing),('se_frame',frame)):
            if name in self.fields:self.uc.mem_write(self.data+self.fields[name],bytes((value,)))
        self.uc.mem_write(self.data+self.fields['load_fn'],b'X'*(suffix_end+4));self.uc.mem_write(self.data+self.fields['load_fn']+suffix_end,b'\0')
        for i,b in enumerate(filename):self.uc.mem_write(filename_segment*16+((filename_offset+i)&65535),bytes((b,)))
        for name,patch in (('se_priorities',priority_patch),('se_priority_frames',duration_patch)):
            need(all(0<=i<33 and 0<=v<=255 for i,v in patch),'mutable 33-entry sound tables')
            for i,v in patch:self.uc.mem_write(self.data+self.fields[name]+i,bytes((v,)))
        self.uc.mem_write(0x70000+stack-32,b'\xD3'*32)
        args=(filename_offset,filename_segment,function) if kind=='load' else (frames,measure) if kind=='measure' else (frames,) if kind=='frame_delay' else () if kind=='update' else (argument,)
        self.uc.mem_write(0x70000+stack,struct.pack('<'+'H'*(2+len(args)),0x40,0x8000,*args))
        regs={n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)};regs.update(cs=self.cs,ds=self.ds,es=seed,ss=0x7000)
        self.high={n:(seed^0xA5A5)<<16 for n in GPRS}
        for n in GPRS:self.uc.reg_write(GPRS[n],self.high[n]|regs[n])
        for n in ('cs','ds','es','ss'):self.uc.reg_write(REG[n],regs[n])
        self.uc.reg_write(REG['sp'],stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        p=dict(locals());p.pop('self');p['seed']=seed;p['flags']=flags
        self.expected=Prediction(bytes(self.uc.mem_read(0,1<<20)),regs,self.data,stack,p,self.fields);self.expected.run(kind)
        self.index,self.error,self.returned=0,None,False
        try:self.uc.emu_start(self.base+self.entries[kind][0],0x100000,count=50000)
        except UcError as e:raise ValueError('MAINL sound contract: guest fault') from e
        need(self.error is None,self.error or 'guest error');need(self.returned and self.r('sp')==stack+4+self.entries[kind][3],'actual far caller/callee cleanup')
        need(self.registers()==self.expected.regs,'independent final WORD registers: '+str([(n,self.r(n),v) for n,v in self.expected.regs.items() if self.r(n)!=v]))
        need(all(self.uc.reg_read(GPRS[n])==self.high[n]|self.expected.regs[n] for n in GPRS),'preserved DWORD high halves')
        actual_flags=self.uc.reg_read(UC_X86_REG_EFLAGS);need(actual_flags&0x8D5==self.expected.flags&0x8D5 and actual_flags&0x600==flags&0x600,'defined final flags and IF/DF')
        need(self.index==len(self.expected.events),'complete sound/file/counter protocol')
        actual=bytes(self.uc.mem_read(0,1<<20));lo,hi=0x70000+stack-32,0x70000+stack;self.expected.memory[lo:hi]=actual[lo:hi];need(actual==self.expected.memory,'whole physical memory outside 32 stack bytes')
        return dict(registers=self.registers(),flags=actual_flags&0xED5,driver_calls=self.expected.driver_count,counter_updates=self.expected.counter_updates,
            event_count=len(self.expected.events),trace_sha256=hashlib.sha256(json.dumps(self.expected.events,sort_keys=True).encode()).hexdigest(),
            playing=self.expected.byte('se_playing') if 'se_playing' in self.fields else None,frame=self.expected.byte('se_frame') if 'se_frame' in self.fields else None)
