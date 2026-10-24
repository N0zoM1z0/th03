"""Lifecycle contracts composing actual maintained parser/print/graphics calls.

DOS allocation/free/resize/termination are explicit bounded replies. Existing
independent library specifications check real nested instructions at call/return
boundaries; no maintained helper is replaced by a stub. Physical DOS lifetime
and EGC raster effects remain outside the contracts.
"""
import hashlib,json,struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import UcError,UC_HOOK_INTR
from unicorn.x86_const import *
from lib.zun_driver_graphics_runtime import Machine as GraphicsMachine,Prediction as GraphicsPrediction,REG,GPRS,BANKS,FIELDS
from lib.zun_driver_command_runtime import Prediction as CommandPrediction,COUNT,CURSOR,VECTOR
from lib.zun_driver_command_runtime import MESSAGES as COMMAND_MESSAGES
from lib.zun_driver_scalar_runtime import specification as scalar_spec,number
from lib.zun_driver_scalar_layout import RANGES as SCALAR_RANGES
from lib.zun_driver_format_runtime import Prediction as FormatPrediction
from lib.zun_driver_command_runtime import arithmetic
from lib.zun_driver_lifecycle_layout import RANGES,control_flow
from verify_th03_zun_driver_hybrid import RESIDENT_PROCS,COMMAND_PROCS,SCATTERED_PROCS

ENTRIES={n.removeprefix('sprite16_'):(a,s) for n,a,s in RANGES}
ALL_PROCS=(*RESIDENT_PROCS,*COMMAND_PROCS,*SCATTERED_PROCS,*((n,a,a+s) for n,a,s in SCALAR_RANGES))
NAMES={a:n.removeprefix('sprite16_') for n,a,_ in ALL_PROCS}
MESSAGES=dict(banner=0xF7A,usage=0xFB9,resize=0xC80,memory=0xF47,installed=0xF5E,present=0xC9D,
 environment=0xCB6,mask=0xCC9,solid=0xCE4,code=0xCFD,removed=0xD12,absent=0xD23)
GRAPHICS={'prepare_vram','build_mask','clear_upper','draw_clipped','egc_begin','egc_end'}
def need(v,m):
    if not v:raise ValueError('ZUN lifecycle contract: '+str(m))
def text(memory,address):
    end=memory.find(b'\0',address,address+2048);need(end>=address,'bounded NUL string');return bytes(memory[address:end])
def word(memory,address):return int.from_bytes(memory[address:address+2],'little')
def parsed(raw):
    r=raw+b'\0'+b'\xA5'*9;v,c,_=number(r,0xA5);return v,c

class Plan:
    def __init__(self,m,kind,parameters):
        self.m,self.p=m,parameters;self.events=[];self.terminal=None;self.final=None;self.para=parameters['paragraphs'];self.allocs=0
        self.kind=kind;self.initial=dict(m.initial_regs);self.used_graphics=False;self.unit(kind)
    def store(self,offset,size,value,base=None):self.events.append(('store',(self.m.base if base is None else base)+offset,size,value&((1<<(size*8))-1)))
    def call(self,name,**args):
        self.used_graphics|=name in GRAPHICS;self.events.append(('call',name,args))
    def dos(self,name,*args):self.events.append(('dos',name,*args))
    def printing(self,name):self.call('print_stack_string',pointer=MESSAGES[name])
    def allocate(self):
        for i,offset in enumerate((0xF3C,0xF3E)):
            failed=self.p['allocation_failure']==i;segment=(0x6000,0x5000)[i]
            self.dos('allocate',i,failed)
            if failed:self.printing('memory');self.exit(0x4C01);return False
            self.store(offset,2,segment);self.para=(self.para+1000)&65535;self.store(0xF43,2,self.para)
        return True
    def exit(self,ax,dx=None):self.dos('terminate',ax,dx);self.terminal=ax
    def scalar(self,args,count=1):
        results=[]
        for i in range(count):
            raw=args[i] if i<len(args) else None
            self.call('require_number',argument=raw)
            if raw is None or parsed(raw)[1]:self.terminal=0x4C01;return None
            results.append(parsed(raw)[0])
        return results
    def unit(self,kind):
        p=self.p
        if kind=='allocate_buffers':
            if self.allocate():self.final='allocation'
        elif kind=='set_interrupt_argument':
            v=self.scalar(p['arguments'])
            if v is not None:self.store(0xF42,1,v[0]);self.final=('number',v[0])
        elif kind in ('mask_test_command','draw_command'):
            self.call('allocate_buffers')
            if not self.allocate():return
            if kind=='mask_test_command':
                for name in ('prepare_vram','build_mask','clear_upper'):self.call(name)
                self.events.append(('mask_copy',));self.final='mask_command'
            else:
                self.call('build_mask');v=self.scalar(p['arguments'],5)
                if v is None:return
                formal=dict(dx=v[0],bx=v[1],di=v[2],ax=v[3],cx=v[4])
                self.call('egc_begin',registers=formal);self.call('draw_clipped',registers=formal);self.call('egc_end');self.final=('draw_command',v)
        elif kind=='install':
            if p['present']:self.printing('present');self.final='signature_match'
            else:
                self.call('allocate_buffers')
                if not self.allocate():return
                self.store(p['vector']*4+2,2,self.m.load,0);self.store(p['vector']*4,2,0x22A,0)
                self.store(0xF38,2,0x9000);self.store(0xF3A,2,0x7654)
                self.call('format_print',argument=p['vector'],pointer=0xF5E);self.exit(0x3100,self.para)
        elif kind=='uninstall':
            if not p['present']:self.printing('absent');self.final='signature_absent';return
            self.store(p['vector']*4+2,2,0xBEEF,0);self.store(p['vector']*4,2,0,0)
            for i,segment in enumerate((0x8800,0x6100,0x5100,0x9000)):
                fail=bool(p['free_failures']>>i&1);self.dos('free',segment,fail)
                if fail:self.printing(('environment','mask','solid','code')[i])
            if not p['free_failures']&8:self.printing('removed')
            self.final='uninstalled'
        elif kind=='interrupt_dispatch':
            service=p['service'];target=self.m.service_target
            self.store(0xF45,2,target);self.call(NAMES[target],irq=True);self.final='iret'
        else:
            self.call('print_stack_string',pointer=0xF7A,df_clear=True);self.store(0xF40,2,int(p['int40_signature']));self.para=0x119;self.store(0xF43,2,self.para)
            self.dos('resize',p['resize_failure'])
            if p['resize_failure']:self.printing('resize');self.exit(0x4C01);return
            tail=p['tail'];end=tail.find(b'\r',0,128);end=127 if end<0 else end;self.store(0x81+end,1,0)
            self.call('tokenize_command')
            shadow=bytearray(self.m.shadow);shadow[self.m.base+0x81+end]=0
            regs=dict(self.initial,si=0x81,flags=p['flags']&~0x400)
            cp=CommandPrediction(shadow,regs,self.m.base,self.m.stack_base,0xF36);cp.run('tokenize_command',False)
            if cp.exit:self.terminal=0x4C01;return
            count=cp.word(COUNT)
            if not count:self.printing('usage');self.exit(0x4C01);return
            pointer=cp.word(VECTOR);head=cp.text(pointer);key=head.upper().replace(b'-',b'/',1) if head[:1]==b'-' else head.upper()
            callback={b'/V':'set_interrupt_argument',b'/Z':'install',b'/R':'uninstall',b'MASKTEST':'mask_test_command',b'SPRITE':'draw_command'}.get(key)
            if not callback:self.call('dispatch_options');self.terminal=0x4C01;return
            self.call('dispatch_options',transparent=True);self.store(CURSOR,2,VECTOR);self.store(CURSOR,2,VECTOR+2);self.store(COUNT,2,count-1)
            if head[:1]==b'-':self.store(pointer,1,47)
            self.call(callback);self.p=dict(p,arguments=tuple(cp.text(cp.word(VECTOR+i*2)) for i in range(1,count)))
            self.unit(callback);self.p=p
            if self.terminal:return
            consumed=1 if callback=='set_interrupt_argument' else 5 if callback=='draw_command' else 0
            need(count==consumed+1,'entry fixture has one option and its complete arguments')
            self.store(CURSOR,2,VECTOR+(consumed+2)*2);self.exit(0x4C00)

class Helper:
    def __init__(self,m,name,formal):
        self.name=name;self.sp=m.r('sp');self.return_ip=word(m.shadow,m.stack_base+self.sp);self.delta=2
        self.regs=m.registers();self.full={n:m.uc.reg_read(GPRS[n]) for n in GPRS};self.flags=m.uc.reg_read(UC_X86_REG_EFLAGS)
        self.memory=bytearray(m.uc.mem_read(0,1<<20));self.pages=None;self.events=None;self.writes=[];self.output=b'';self.exit=False
        self.mask,self.value=0x8C5,0x44;self.if_df=self.flags&0x600
        if formal.get('df_clear'):need(not self.flags&0x400,'entry CLD before banner')
        if formal.get('irq'):need(self.flags&0x200,'STI before real interrupt service')
        for n,v in formal.get('registers',{}).items():need(self.regs[n]==v,'root passes parsed graphics register '+n)
        if name in GRAPHICS:
            p=GraphicsPrediction(self.memory,m.pages,m.page,self.regs,self.flags,m.base);p.run(name)
            self.memory,self.regs,self.events,self.pages,self.page=p.memory,p.regs,p.events,p.pages,p.page
            self.mask,self.value,self.if_df=p.flag_mask,p.flag_value,p.flags
        elif name.startswith('set_'):
            p=scalar_spec(name,dict(self.regs,flags=self.flags),b'\0'*16,b'\0',0,m.base,self.regs['ds']*16,0)
            self.regs={n:v for n,v in p['registers'].items() if n!='flags'};self.writes=p['writes'];self.mask,self.value=p['flags_mask'],p['flags_value']
            for a,s,v in self.writes:self.memory[a:a+s]=v.to_bytes(s,'little')
        elif name in ('require_number','tokenize_command','dispatch_options'):
            if name=='require_number':
                remaining=word(self.memory,m.base+COUNT);arg=None if not remaining else text(self.memory,m.base+word(self.memory,m.base+word(self.memory,m.base+CURSOR)))
                need(arg==formal['argument'],'numeric argument source/cursor')
            p=CommandPrediction(self.memory,dict(self.regs,flags=self.flags),m.base,m.stack_base,self.sp);p.run(name,False)
            need(not p.callbacks,'transparent option callbacks execute through lifecycle plan')
            self.memory=p.memory;self.regs={n:v for n,v in p.regs.items() if n!='flags'};self.writes=p.writes
            self.mask,self.value,self.output,self.exit,self.delta=p.flags_mask,p.flags_value,bytes(p.output),p.exit,p.sp_delta
        elif name=='format_print':
            need(self.regs['dx']==formal['pointer'] and self.regs['bx']==(self.sp+2)&65535,'installed formatter register/stack interface')
            value=int.from_bytes(self.memory[m.stack_base+self.regs['bx']:m.stack_base+self.regs['bx']+4],'little');need(value==formal['argument'],'MOVZX DWORD interrupt argument')
            fmt=text(self.memory,self.regs['ds']*16+self.regs['dx']);p=FormatPrediction(self.memory);raw=p.format(fmt,(value,),m.stack_base+self.sp-210)
            need(len(raw)<=208,'bounded installed message');self.memory=p.memory;self.output=raw.split(b'\0',1)[0]
            self.full['cx']&=65535;self.full['dx']=p.last_number&0xFFFF0000|self.regs['dx']
        else:
            need(name=='print_stack_string','known maintained helper')
            pointer=word(self.memory,m.stack_base+self.sp+2);need(pointer==formal['pointer'],'SS diagnostic pointer')
            self.output=text(self.memory,m.stack_base+pointer);self.delta=4
        for n in GPRS:self.full[n]=self.full[n]&0xFFFF0000|self.regs[n]
        self.index,self.printed=0,0
    def finish(self,m,terminal=False):
        need(m.r('sp')==(self.sp+self.delta)&65535,'actual helper near/error frame')
        need(m.registers()==self.regs,'independent helper WORD/segment result: '+self.name)
        need(all(m.uc.reg_read(GPRS[n])==self.full[n] for n in GPRS),'independent helper DWORD effects: '+self.name)
        flags=m.uc.reg_read(UC_X86_REG_EFLAGS);need(flags&self.mask==self.value&self.mask and flags&0x600==self.if_df,'helper flag/IF/DF contract: '+self.name)
        need(self.printed==len(self.output) and self.index==len(self.events if self.events is not None else self.writes),'complete helper events/output')
        actual=bytes(m.uc.mem_read(0,1<<20));m.ignore_stack(self.memory,actual);need(actual==self.memory,'whole helper memory: '+self.name)
        if self.pages is not None:m.flush();need(m.pages==self.pages and m.page==self.page,'helper two-page backing')
        m.shadow=self.memory

class Machine(GraphicsMachine):
    def __init__(self,image,load):
        super().__init__(image,load);self.uc.hook_del(self.hooks.pop())
        self.hooks.append(self.uc.hook_add(UC_HOOK_INTR,self.interrupt))
        self.instructions={i.address:i for _,a,z in ALL_PROCS for i in Cs(CS_ARCH_X86,CS_MODE_16).disasm(image[a-256:z-256],a)}
        _,self.reachable,self.cfg=control_flow(image);self.covered=set();self.calls=0
        self.buffer_templates={base:bytes((i*29+(base>>12))&255 for i in range(65536)) for base in (0x50000,0x60000)}
    def registers(self):return {n:self.r(n) for n in (*GPRS,'cs','ds','es','ss')}
    def ignore_stack(self,expected,actual):
        for lo,hi in self.stack_windows:expected[lo:hi]=actual[lo:hi]
    def event(self,event):
        need(self.index<len(self.plan.events) and event==self.plan.events[self.index],f'root event {self.index}: {event}; expected {self.plan.events[self.index:self.index+1]}');self.index+=1
    def checkpoint(self):
        actual=bytes(self.uc.mem_read(0,1<<20));self.ignore_stack(self.shadow,actual);need(actual==self.shadow,'root memory before/after maintained call')
    def code(self,uc,address,size,_):
        try:
            ip=address-self.base
            if self.active and ip==self.active.return_ip:
                self.active.finish(self);self.active=None
            if address==self.base+0xFFFF or address==0x98040:self.returned=True;uc.emu_stop();return
            need(ip in self.instructions and self.instructions[ip].size==size,'real complete maintained instructions')
            self.covered.update(set(range(ip,ip+size))&self.reachable)
            reference=0xF38 if self.kind=='entry' and self.r('sp')<0x2000 else self.stack
            self.maximum_stack=max(self.maximum_stack,reference-self.r('sp'))
            if self.starting:self.starting=False;return
            if self.active:return
            if ip in NAMES:
                ret=word(bytes(uc.mem_read(self.stack_base+self.r('sp'),2)),0)
                root_return=any(a<=ret<a+s for _,a,s in RANGES)
                resident=ip in {a for _,a,_ in RANGES}
                if not (root_return or resident):return
                need(self.index<len(self.plan.events) and self.plan.events[self.index][0]=='call','unexpected maintained root call '+NAMES[ip])
                _,name,formal=self.plan.events[self.index];need(NAMES[ip]==name,'ordered maintained call '+name+' / '+NAMES[ip]);self.index+=1;self.calls+=1
                self.checkpoint()
                if resident or formal.get('transparent'):return
                self.active=Helper(self,name,formal)
        except Exception as e:self.fail(e)
    def write(self,uc,access,address,size,value,_):
        try:
            if any(lo<=address and address+size<=hi for lo,hi in self.stack_windows):return
            if self.active:
                h=self.active;event=('store',address,size,value)
                expected=h.events[h.index] if h.events is not None and h.index<len(h.events) else h.writes[h.index] if h.index<len(h.writes) else None
                need(event==expected if h.events is not None else (address,size,value)==expected,'ordered maintained helper store '+h.name);h.index+=1
            elif self.index<len(self.plan.events) and self.plan.events[self.index]==('mask_copy',):
                off=self.mask_copy_index*2;need((address,size,value)==(0xA8000+off,2,word(self.shadow,0x60000+off)),'root mask copy');self.mask_copy_index+=1
                self.shadow[address:address+2]=value.to_bytes(2,'little')
                if self.mask_copy_index==8000:self.index+=1
            else:self.event(('store',address,size,value));self.shadow[address:address+size]=value.to_bytes(size,'little')
        except Exception as e:self.fail(e)
    def out(self,uc,port,size,value,_):
        try:
            h=self.active;need(h is not None and h.events is not None,'ports only inside actual graphics helpers')
            need(h.index<len(h.events) and h.events[h.index]==('out',port,size,value,uc.reg_read(UC_X86_REG_EFLAGS)&0x600),'ordered maintained graphics port');h.index+=1
            if port==0xA6 and value!=self.page:
                self.flush();self.page=value
                for i,a in enumerate(BANKS):uc.mem_write(a,bytes(self.pages[value][i]))
        except Exception as e:self.fail(e)
    def interrupt(self,uc,n,_):
        try:
            need(n==0x21,'bounded DOS only; optional INT40 is terminal-unreachable');ah=self.r('ax')>>8
            if ah==2:
                h=self.active;need(h and h.printed<len(h.output) and self.r('dx')&255==h.output[h.printed],'DOS character order')
                h.printed+=1;self.console.append(self.r('dx')&255);uc.reg_write(REG['ax'],self.r('ax')&0xFF00|self.r('dx')&255)
                uc.reg_write(UC_X86_REG_EFLAGS,(uc.reg_read(UC_X86_REG_EFLAGS)&0x600)|0x8D7|2);return
            if ah==0x4C and self.active:
                need(self.active.exit and self.plan.terminal==0x4C01,'specified parser error exit');self.active.finish(self,True);self.active=None
            elif ah in (0x4C,0x31):
                self.event(('dos','terminate',self.r('ax'),self.r('dx') if ah==0x31 else None))
            else:
                event=self.plan.events[self.index];need(event[0]=='dos','ordered DOS request')
                if ah==0x48:
                    _,_,i,failed=event;need(event[1]=='allocate' and self.r('bx')==1000,'decimal-1000 paragraph allocation');reply=8 if failed else (0x6000,0x5000)[i]
                elif ah==0x49:
                    _,_,seg,failed=event;need(event[1]=='free' and self.r('es')==seg,'DOS free ordering/segment');reply=7 if failed else 0
                else:
                    need(ah==0x4A and event[1]=='resize' and self.r('es')==self.load and self.r('bx')==0x119 and self.r('sp')==0xF38,'entry resize size/segment/stack')
                    failed=event[2];reply=9 if failed else 0
                self.index+=1;uc.reg_write(REG['ax'],reply);uc.reg_write(UC_X86_REG_EFLAGS,(uc.reg_read(UC_X86_REG_EFLAGS)&0x600)|0x8D6|int(failed));return
            need(self.index==len(self.plan.events),'terminal DOS after complete root protocol');self.exited=True;uc.emu_stop()
        except Exception as e:self.fail(e)
    def run(self,kind,*,arguments=(b'66',),tail=b'/V 66\r',allocation_failure=-1,free_failures=0,present=False,prefix=0,vector=0x42,
            paragraphs=0x119,int40_signature=False,resize_failure=False,service=3,flags=0x202,pattern=0,stack=0xF800,split_stack=False):
        need(kind in ENTRIES and 0<=vector<=255 and 0<=service<=9,'bounded lifecycle inputs')
        need(kind not in ('install','uninstall','mask_test_command','draw_command') or not flags&0x400,'forward lifecycle precondition')
        need(kind!='interrupt_dispatch' or service>=3 or not flags&0x400,'forward interrupt graphics precondition')
        self.uc.mem_write(0,bytes(self.initial));self.kind,self.stack=kind,stack;ss=0x8000 if split_stack else self.load;self.stack_base=ss*16
        self.stack_windows=[(self.stack_base+stack-512,self.stack_base+stack),(self.stack_base+0xD38,self.stack_base+0xF38)]
        self.page=0;self.pages=[[bytearray(b) for b in p] for p in self.page_templates]
        for i,a in enumerate(BANKS):self.uc.mem_write(a,bytes(self.pages[0][i]))
        for base,raw in self.buffer_templates.items():self.uc.mem_write(base,raw)
        for i,offset in enumerate((*MESSAGES.values(),*COMMAND_MESSAGES.values())):
            if ss!=self.load:self.uc.mem_write(self.stack_base+offset,('S%02d'%i).encode()+b'\0')
        for k,v in dict(x=8,y=2,width=2,height=3,source=512,words=3,skip=74,mono=0,overlap=1,mask=0x5AA5,color=0xB,rop=0x28FC,plane=0xFFF0).items():self.uc.mem_write(self.base+FIELDS[k],struct.pack('<H',v))
        self.uc.mem_write(self.base+0xF3C,struct.pack('<HH',0x6000,0x5000));self.uc.mem_write(self.base+0xF42,bytes((vector,)));self.uc.mem_write(self.base+0xF43,struct.pack('<H',paragraphs))
        self.uc.mem_write(0x100,struct.pack('<HH',0x170,0x8800));self.uc.mem_write(0x88172,b'OK' if int40_signature else b'NO')
        sig=bytearray(self.initial[self.base+0x102:self.base+0x10C]);need(0<=prefix<10,'signature mismatch prefix')
        if not present:sig[prefix]^=0x55
        self.uc.mem_write(0x90102,bytes(sig));self.uc.mem_write(vector*4,struct.pack('<HH',0x7654,0x9000))
        self.uc.mem_write(0x9002C,struct.pack('<H',0x8800));self.uc.mem_write(0x90F38,struct.pack('<HHHH',0xBEEF,0x7654,0x6100,0x5100))
        need(len(tail)<=127,'bounded PSP tail');self.uc.mem_write(self.base+0x81,tail+b' '*(127-len(tail)))
        pointers=[]
        for i,arg in enumerate(arguments):
            off=0x3000+i*128;need(len(arg)<120,'bounded numeric text');self.uc.mem_write(self.base+off,arg+b'\0'+b'\xA5'*9);pointers.append(off)
        self.uc.mem_write(self.base+COUNT,struct.pack('<H',len(arguments)));self.uc.mem_write(self.base+CURSOR,struct.pack('<H',VECTOR));self.uc.mem_write(self.base+VECTOR,b''.join(struct.pack('<H',v) for v in pointers+[0xDEAD]))
        self.uc.mem_write(self.stack_base+stack,b'\xFF\xFF\x53\xA9\x65\x87')
        regs=dict(ax=0xB53A^pattern,bx=2,cx=3,dx=8,si=0x2001,di=512,bp=0xA675^pattern,cs=self.load,ds=self.load,es=self.load,ss=ss)
        if kind=='interrupt_dispatch':
            regs['ax']=service<<8|2
            if service==9:self.uc.mem_write(self.base+0x1050,struct.pack('<H',0x35E))
            self.service_target=word(bytes(self.uc.mem_read(self.base+0x103E+service*2,2)),0)
            self.uc.mem_write(self.stack_base+stack,struct.pack('<HHH',0x40,0x9800,flags))
        self.initial_regs=regs;self.shadow=bytearray(self.uc.mem_read(0,1<<20))
        params=dict(arguments=arguments,tail=tail,allocation_failure=allocation_failure,free_failures=free_failures,present=present,prefix=prefix,vector=vector,
            paragraphs=paragraphs,int40_signature=int40_signature,resize_failure=resize_failure,service=service,flags=flags)
        self.plan=Plan(self,kind,params)
        self.high={n:(0xA5A5^pattern)<<16 for n in GPRS}
        for n in GPRS:self.uc.reg_write(GPRS[n],self.high[n]|regs[n])
        for n in ('cs','ds','es','ss'):self.uc.reg_write(REG[n],regs[n])
        self.uc.reg_write(UC_X86_REG_ESP,stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags&~0x300 if kind=='interrupt_dispatch' else flags)
        self.index,self.active,self.error,self.returned,self.exited,self.starting,self.mask_copy_index=0,None,None,False,False,True,0;self.console=bytearray();self.calls=0
        try:self.uc.emu_start(self.base+ENTRIES[kind][0],0x100000,count=10000000)
        except UcError as e:raise ValueError('ZUN lifecycle contract: guest fault') from e
        need(self.error is None,self.error or 'guest error');need(self.index==len(self.plan.events),'complete lifecycle protocol')
        need(self.exited==(self.plan.terminal is not None) and (self.exited or self.returned),'terminal DOS / real return')
        self.checkpoint();self.check_final(flags,params)
        return dict(registers=self.registers(),flags=self.uc.reg_read(UC_X86_REG_EFLAGS)&0xED7,terminal=self.plan.terminal,
            root_events=len(self.plan.events),root_trace_sha256=hashlib.sha256(json.dumps(self.plan.events,default=lambda v:v.hex()).encode()).hexdigest(),output_sha256=hashlib.sha256(self.console).hexdigest(),maintained_calls=self.calls)
    def check_final(self,flags,p):
        r=dict(self.initial_regs);f=self.plan.final;mask,value=0x8C5,0x44
        expected_if_df=flags&0x600
        if self.kind=='entry':expected_if_df&=~0x400
        if self.kind!='interrupt_dispatch' and self.plan.used_graphics:expected_if_df|=0x200
        need(self.uc.reg_read(UC_X86_REG_EFLAGS)&0x600==expected_if_df,'root IF/DF and entry CLD/graphics STI')
        if self.exited:
            need(self.r('ax')==self.plan.terminal,'DOS terminal AX')
            if self.plan.terminal==0x3100:need(self.r('dx')==self.plan.para and self.uc.reg_read(UC_X86_REG_EAX)==0x3100,'TSR paragraphs and MOVZX width')
            return
        if f=='iret':
            r['cs']=0x9800;need(self.uc.reg_read(UC_X86_REG_ESP)==self.stack+6,'IRET six-byte frame')
            need(self.uc.reg_read(UC_X86_REG_EFLAGS)&0xED7==flags&0xED7,'IRET restores stacked flags, overriding STI')
        else:
            need(self.uc.reg_read(UC_X86_REG_ESP)==self.stack+2,'near return frame')
            if f=='allocation':r.update(ax=0x5000,bx=1000);mask,value=0x8D5,arithmetic((self.plan.para-1000)&65535,1000)
            elif isinstance(f,tuple) and f[0]=='number':r['ax']=f[1];mask,value=1,0
            elif f in ('signature_match','signature_absent','uninstalled'):
                n=10 if p['present'] else p['prefix']+1;r.update(ax=0,bx=p['vector']*4,cx=10-n,si=0x102+n,di=0x102+n)
                if f!='signature_match':r['es']=0x9000
                if f=='uninstalled':r.update(ax=7 if p['free_failures']&8 else 0,dx=0xBEEF)
            elif f=='mask_command':r.update(ax=0xA800,bx=1000,cx=0,si=16000,di=16000)
            elif isinstance(f,tuple) and f[0]=='draw_command':
                v=f[1];r.update(dx=v[0],bx=v[1],di=v[2],ax=v[3],cx=v[4])
            need(self.uc.reg_read(UC_X86_REG_EFLAGS)&mask==value&mask,'root final defined flags')
        actual=self.registers();need(actual==r,'root final WORD registers: '+str([(n,hex(actual[n]),hex(v)) for n,v in r.items() if actual[n]!=v]))
        need(all(self.uc.reg_read(GPRS[n])==self.high[n]|r[n] for n in GPRS),'root preserved DWORD high halves')

def cases():
    for v in range(256):
        yield 'set_interrupt_argument',dict(arguments=(str(v).encode(),))
        yield 'install',dict(vector=v,present=bool(v&1))
        yield 'uninstall',dict(vector=v,present=True,free_failures=v&15)
    for prefix in range(10):
        yield 'install',dict(prefix=prefix)
        yield 'uninstall',dict(prefix=prefix)
    for para in (0,1,0x7FFF,0x8000,0xFFFF):
        for failure in (-1,0,1):
            for flags in (2,0xED7):yield 'allocate_buffers',dict(paragraphs=para,allocation_failure=failure,flags=flags)
    for arg in (b'',b'255',b'256',b'511',b'32767',b'32768',b'65535',b'65536',b'-1',b'FFh',b'$8000',b"'OK'",b'bad'):
        yield 'set_interrupt_argument',dict(arguments=(arg,))
    yield 'set_interrupt_argument',dict(arguments=())
    for service in range(10):
        for flags in ((2,0x202,0x2D7) if service<3 else (2,0x202,0x402,0xED7)):
            yield 'interrupt_dispatch',dict(service=service,flags=flags)
    for failure in (-1,0,1):
        yield 'mask_test_command',dict(allocation_failure=failure)
        yield 'draw_command',dict(allocation_failure=failure,arguments=(b'8',b'2',b'512',b'2',b'3'))
    for index in range(5):
        args=[b'8',b'2',b'512',b'2',b'3'];args[index]=b'bad';yield 'draw_command',dict(arguments=tuple(args))
        yield 'draw_command',dict(arguments=tuple(args[:index]))
    for args in ((b'65535',b'200',b'0',b'65535',b'0'),(b'0',b'-1',b'512',b'2',b'202')):
        yield 'draw_command',dict(arguments=args)
    tails=(b'\r',b'/V 66\r',b'-v 511\r',b'/V bad\r',b'/V\r',b'/R\r',b'/Z\r',b'MASKTEST\r',b'SPRITE 8 2 512 2 3\r',b'/WHAT\r',b'"open\r',b' '*127)
    for tail in tails:
        for signature,present in ((False,False),(True,True)):
            yield 'entry',dict(tail=tail,int40_signature=signature,present=present)
    for flags in (2,0xED7):yield 'entry',dict(resize_failure=True,flags=flags)

def verify(target,candidate):
    observations=[]
    for image in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(image,load)
            try:
                trace=hashlib.sha256()
                for count,(kind,options) in enumerate(cases(),1):
                    r=m.run(kind,pattern=0 if count&1 else 0x5A5A,stack=0xF800 if count&1 else 0xE800,split_stack=bool(count&1),**options)
                    trace.update(json.dumps(r,sort_keys=True).encode())
                need(m.covered==m.reachable,'all 549 DOS-reachable lifecycle bytes execute')
                loads.append(dict(load_segment=load,cases=count,covered_owner_bytes=len(m.covered),terminal_unreachable_owner_bytes=15,
                    maximum_observed_stack_depth=m.maximum_stack,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'target/candidate lifecycle observations')
    return dict(images=2,functions=8,code_bytes=564,executed_owner_bytes=549,terminal_unreachable_owner_bytes=15,
        cases_per_image=sum(o['cases'] for o in observations[0]),observations=observations[0],exhaustive_vector_bytes=256,
        scope='real maintained nested helpers; bounded DOS services, terminal 4C/31; two-page word interface excludes physical EGC and DOS lifetime')

def negative_controls(image):
    controls=(
        ('entry-clears-DF',0x10C,b'\xFC',b'\xFD','entry',dict(flags=0xED7)),
        ('INT40-returned-offset',0x11C,b'\0',b'\x04','entry',dict(int40_signature=True)),
        ('INT40-signature-word-order',0x128,b'\xC4',b'\xC0','entry',dict(int40_signature=True)),
        ('resident-extra-paragraph',0x143,b'\x40',b'\x48','entry',{}),
        ('startup-stack-boundary',0x148,b'\x38',b'\x36','entry',{}),
        ('command-tail-CR-scan',0x165,b'\x0D',b'\x0B','entry',{}),
        ('decimal-1000-paragraphs',0x19D,b'\xE8',b'\xE9','allocate_buffers',{}),
        ('allocation-carry-branch',0x1A3,b'\x73',b'\x72','allocate_buffers',{}),
        ('first-buffer-is-mask',0x1B1,b'\x3C',b'\x3E','allocate_buffers',{}),
        ('resident-size-increment',0x1B7,b'\xE8',b'\xE9','allocate_buffers',{}),
        ('interrupt-field-is-BYTE',0x1DA,b'\xA2',b'\xA3','set_interrupt_argument',{}),
        ('mask-adapter-source-buffer',0x1EE,b'\x3C',b'\x3E','mask_test_command',{}),
        ('mask-adapter-copies-WORDs',0x1FD,b'\xA5',b'\xA4','mask_test_command',{}),
        ('SPRITE-x-register',0x20B,b'\xD0',b'\xD8','draw_command',dict(arguments=(b'16',b'2',b'512',b'2',b'3'))),
        ('service-selector-is-AH',0x22C,b'\xDC',b'\xD8','interrupt_dispatch',{}),
        ('service-call-enables-IF',0x23C,b'\xFB',b'\xFA','interrupt_dispatch',dict(flags=2)),
        ('interrupt-returns-with-IRET',0x242,b'\xCF',b'\xCB','interrupt_dispatch',dict(flags=2)),
        ('resident-signature-offset',0x256,b'\x02',b'\x04','install',dict(present=True)),
        ('exchange-saves-old-segment',0x27A,b'\x87',b'\x89','install',{}),
        ('interrupt-is-zero-extended-DWORD',0x28A,b'\xB6',b'\xBE','install',dict(vector=0x80)),
        ('TSR-retains-paragraph-count',0x29D,b'\x43',b'\x3C','install',{}),
        ('uninstall-zeroes-old-offset',0x2D6,b'\xC0',b'\xDB','uninstall',dict(present=True)),
        ('environment-segment-offset',0x2EE,b'\x2C',b'\x2E','uninstall',dict(present=True)),
        ('mask-freed-before-solid',0x301,b'\x3C',b'\x3E','uninstall',dict(present=True)),
        ('last-free-carry-selects-message',0x327,b'\x73',b'\x72','uninstall',dict(present=True)),
    )
    rejected=[]
    for name,at,old,new,kind,opts in controls:
        raw=bytearray(image);need(raw[at-256:at-256+len(old)]==old,'literal mutation anchor '+name);raw[at-256:at-256+len(new)]=new;m=None
        try:
            try:m=Machine(bytes(raw),0x3000);m.run(kind,**opts)
            except ValueError:rejected.append(name)
            else:raise ValueError('ZUN lifecycle mutation survived: '+name)
        finally:
            if m:m.close()
    return dict(count=len(rejected),rejected=rejected)
