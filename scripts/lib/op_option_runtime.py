"""Independent menu policy and ABI with real renderer/sound/box instructions.

Only SDK text/graphics, finite counter updates and driver replies are bounded
interfaces. Main/story/VS/Music Room behavior receives no credit here.
"""
import hashlib,json,struct
from dataclasses import replace
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import Uc,UcError,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR
from unicorn import x86_const as x
from lib.op_option_layout import ENTRIES
from lib.op_render_layout import ENTRIES as RENDERERS
from lib.op_render_runtime import Prediction as RenderPrediction
from lib.op_cfg_runtime import RESIDENT,ACTIVE,FM,MIDI,DISABLED,reply,MODE_START,MODE_SIZE
from lib.shared_sound_runtime import Prediction as SoundPrediction,compare
from lib.op_sound_layout import RUNTIME_FIELDS
from lib.op_dispatch_runtime import add_flags
REG={n:getattr(x,'UC_X86_REG_'+n.upper()) for n in ('ax','bx','cx','dx','si','di','bp','sp','cs','ds','es','ss','ip','fs','gs')}
GPRS={n:getattr(x,'UC_X86_REG_E'+n.upper()) for n in ('ax','bx','cx','dx','si','di','bp','sp')}
MOVE,OPTION=ENTRIES['move'][0],ENTRIES['option'][0]
KAJA,BOX,DELAY=0xC403,0xB0AF,0xC19E
SEL,INIT,LOCK,INOPT,PUT,INPUT=0x161,0x165,0x118B,0x118C,0x118E,0x1AA6
LIBRARIES={0x21F4:('clear',0,True),0xB10A:('unput',2,False),0x28D8:('super',6,True),0xFCC:('gaiji',10,True),0x2254:('text',10,True)}
HELPERS=tuple((s,ins) for kind,(s,_,ins) in RENDERERS.items() if kind!='vs')+((KAJA,30),(BOX,44),(DELAY,21),(MODE_START,MODE_SIZE))

def need(v,m):
    if not v:raise ValueError('OP option contract: '+str(m))
def signed(v):return v-256 if v&128 else v
def logic(v,bits=16):return (4 if (v&255).bit_count()%2==0 else 0)|(64 if not v else 0)|(128 if v&(1<<(bits-1)) else 0)
def add8(a,b):
    v=(a+b)&255
    return int(a+b>255)|(4 if v.bit_count()%2==0 else 0)|((a^b^v)&16)|(64 if not v else 0)|(v&128)|(0x800 if (~(a^b)&(a^v)&128) else 0)

class Prediction:
    def __init__(self,memory,regs,p,load):
        self.memory=bytearray(memory);self.r={n:v for n,v in regs.items() if n!='sp'};self.original=dict(self.r);self.p=p;self.load=load
        self.cs=load+0x990;self.ds=load+0xD7F;self.data=self.ds*16;self.res=p['resseg']*16+p['resoff']
        self.flags=p['flags'];self.mask=0x8D5;self.events=[];self.calls=0
    def byte(self,off):return self.memory[self.data+off]
    def word(self,off):return int.from_bytes(self.memory[self.data+off:self.data+off+2],'little')
    def resident(self,off):return self.memory[self.res+off]
    def store_at(self,at,size,value):
        value&=(1<<(8*size))-1;self.events.append(dict(kind='store',address=at,size=size,value=value));self.memory[at:at+size]=value.to_bytes(size,'little')
    def store(self,off,value,size=1):self.store_at(self.data+off,size,value)
    def put(self,off,value):self.store_at(self.res+off,1,value)
    def cmp(self,a,b,byte=False):self.flags=(self.flags&0x600)|compare(a,b,byte)|2;self.mask=0x8D5
    def logical(self,v,bits=16):self.flags=(self.flags&0x600)|logic(v,bits)|2;self.mask=0x8C5
    def al(self,v):self.r['ax']=(self.r['ax']&0xFF00)|v
    def selection_ax(self):self.r['ax']=signed(self.byte(SEL))&65535
    def les(self):self.r.update(bx=self.p['resoff'],es=self.p['resseg'])
    def entry(self,address,sp,args=()):
        self.events.append(dict(kind='entry',address=address,sp=sp,args=args,request=dict(self.r),mask=self.mask,flags=self.flags))
    def service(self,name,sp,args=(),far=True):
        before=dict(self.r,cs=self.load if far else self.cs);self.calls+=1
        after,flags=reply(before,self.calls,self.p['seed'],self.flags,self.p['status'])
        self.events.append(dict(kind='library',name=name,sp=sp,args=args,far=far,request=before,mask=self.mask,flags=self.flags,post=after,post_flags=flags))
        self.r=dict(after,cs=self.cs);self.flags=flags;self.mask=0x8D5
    def render(self,kind,selection,attribute,sp):
        start=RENDERERS[kind][0];self.entry(start,sp,(attribute,selection))
        p=dict(selection=selection,attribute=attribute,stack=sp,seed=self.p['seed'],status=self.p['status'],flags=self.flags,
            rank=self.resident(0xB),bgm=self.resident(0x15),key=self.resident(0x16),resseg=self.p['resseg'],resoff=self.p['resoff'])
        e=RenderPrediction(self.r,p,self.ds,self.load).run(kind)
        for event in e.events:
            self.events.append(dict(kind='library',name=event['service'],sp=sp-20,args=event['arguments'],far=True,request=event['request'],mask=event['flags_mask'],flags=event['flags_value'],post=event['post'],post_flags=event['post_flags'],string_hex=event['string_hex']))
        self.r=dict(e.regs,cs=self.cs);self.flags,self.mask=e.flags,e.mask
    def move(self,maximum,direction,sp):
        original=dict(self.r);self.entry(MOVE,sp,(direction,maximum));self.r['bp']=sp-2
        callback={0x5DD:'main',0x657:'option'}[self.word(PUT)]
        self.selection_ax();self.render(callback,self.r['ax'],1,sp-8)
        direction&=255;maximum&=255;self.al(direction);old=self.byte(SEL)
        self.store(SEL,old+direction);self.flags=(self.flags&0x600)|add8(old,direction)|2;self.mask=0x8D5
        self.cmp(self.byte(SEL),0,True)
        if signed(self.byte(SEL))<0:self.al(maximum);self.store(SEL,maximum)
        self.al(self.byte(SEL));self.cmp(self.byte(SEL),maximum,True)
        if signed(self.byte(SEL))>signed(maximum):self.store(SEL,0)
        self.selection_ax();self.render(callback,self.r['ax'],0xE1,sp-8);self.r['bp']=original['bp']
    def kaja(self,arg,sp):
        self.r['cs']=self.load+0xBEB;self.entry(KAJA,sp,(arg,))
        e=SoundPrediction(self.memory,self.r,self.data,sp,dict(flags=self.flags,argument=arg,seed=self.p['seed'],driver_ax=self.p['driver_ax']),dict(RUNTIME_FIELDS,active=ACTIVE,midi_active=MIDI))
        e.run('kaja')
        for event in e.events:event.update(request_mask=0x8D5,request_flags=compare(self.byte(MIDI),1,True))
        self.events.extend(e.events);self.r=dict(e.regs,cs=self.cs);self.flags,self.mask=e.flags,0x8D5
    def mode(self,sp):
        self.r['cs']=self.load+0xBEB;self.entry(MODE_START,sp);self.r['ax']=(self.r['ax']&255)|0x900
        e=SoundPrediction(self.memory,self.r,self.data,sp,dict(flags=self.flags,seed=self.p['seed'],driver_ax=self.p['driver_ax']),RUNTIME_FIELDS)
        e.interrupt(0x60,'kaja')
        for event in e.events:event.update(request_mask=self.mask,request_flags=self.flags)
        self.events.extend(e.events);self.r=e.regs;self.flags=e.flags
        self.r['bx']=0;self.logical(0);self.cmp(self.r['ax']&255,255,True)
        if self.r['ax']&255!=255:
            carry=self.flags&1;self.r['bx']=1;self.flags=(self.flags&0x600)|add_flags(0,1)&~1|carry|2
            self.store(FM,1)
        else:self.r['bx']=self.byte(MIDI)
        self.store(ACTIVE,self.r['bx']);self.r['ax']=self.r['bx'];self.r['cs']=self.cs;self.mask=0x8D5
    def delay(self,sp):
        self.r['cs']=self.load+0xBEB;self.entry(DELAY,sp,(1,));self.store(RUNTIME_FIELDS['counter'],0,2)
        for value in (0,1):
            self.events.append(dict(kind='tick',value=value));self.memory[self.data+RUNTIME_FIELDS['counter']:self.data+RUNTIME_FIELDS['counter']+2]=value.to_bytes(2,'little');self.r['ax']=value;self.cmp(value,1)
        self.r['cs']=self.cs
    def box(self,sp):
        old=dict(self.r);self.entry(BOX,sp);self.r['bp']=sp-2;self.r['si']=288;self.cmp(288,392)
        for column in range(288,392,8):
            self.service('unput',sp-8,(column,),False)
            self.service('super',sp-14,(2,256,column))
            self.delay(sp-10);self.r['si']=column+8;self.cmp(column+8,392)
        self.r['bp'],self.r['si']=old['bp'],old['si']
    def option(self,sp):
        old=dict(self.r);self.r['bp']=sp-2;self.cmp(self.byte(INIT),0,True)
        if not self.byte(INIT):
            self.service('clear',sp-8);self.box(sp-6);self.store(LOCK,0);self.r['si']=0;self.logical(0)
            for choice in range(4):
                self.cmp(choice,4);self.selection_ax();self.cmp(self.r['ax'],choice);attribute=0xE1 if self.r['ax']==choice else 1
                self.r['ax']=attribute;self.render('option',choice,attribute,sp-10);self.r['si']=choice+1
            self.cmp(4,4);self.store(PUT,0x657,2);self.store(INIT,1);self.store(LOCK,0)
        self.cmp(self.word(INPUT),0)
        if not self.word(INPUT):self.store(LOCK,1)
        self.cmp(self.byte(LOCK),0,True)
        if self.byte(LOCK):
            for bit,direction in ((1,0xFFFF),(2,1)):
                self.logical(self.word(INPUT)&bit,8)
                if self.word(INPUT)&bit:self.move(3,direction,sp-10)
            for bit,increment in ((8,True),(4,False)):
                self.logical(self.word(INPUT)&bit,8)
                if not self.word(INPUT)&bit:continue
                self.selection_ax();selection=self.r['ax'];self.logical(selection)
                if selection:self.cmp(selection,1)
                if selection not in (0,1):self.cmp(selection,2)
                if selection in (0,2):
                    self.les();off,limit=(0xB,3) if selection==0 else (0x16,2);value=self.resident(off)
                    if increment:
                        self.put(off,value+1);self.cmp(self.resident(off),limit,True)
                        if self.resident(off)>limit:self.put(off,0)
                    else:
                        self.cmp(value,0,True)
                        if not value:self.put(off,limit)
                        else:
                            self.les();self.put(off,value-1);carry=self.flags&1;self.flags=(self.flags&0x600)|(compare(value,1,True)&~1)|carry|2
                elif selection==1:
                    self.cmp(self.byte(DISABLED),0,True)
                    if not self.byte(DISABLED):
                        self.les();self.cmp(self.resident(0x15),0,True)
                        if not self.resident(0x15):
                            self.put(0x15,1);self.kaja(0x100,sp-10);self.mode(sp-8);self.kaja(0,sp-10)
                        else:
                            self.les();self.put(0x15,0);self.kaja(0x100,sp-10);self.store(ACTIVE,0)
                        self.selection_ax();self.render('option',self.r['ax'],0xE1,sp-10)
                self.selection_ax();self.render('option',self.r['ax'],0xE1,sp-10)
            self.logical((self.word(INPUT)>>8)&0x20,8)
            confirm=bool(self.word(INPUT)&0x2000)
            if not confirm:self.logical(self.word(INPUT)&0x20,8);confirm=bool(self.word(INPUT)&0x20)
            if confirm:
                self.selection_ax();self.cmp(self.r['ax'],3)
                if self.r['ax']==3:self.store(INIT,0);self.store(SEL,4);self.store(INOPT,0)
            self.logical((self.word(INPUT)>>8)&0x10,8)
            if self.word(INPUT)&0x1000:self.store(INIT,0);self.store(SEL,4);self.store(INOPT,0)
            self.cmp(self.word(INPUT),0)
            if self.word(INPUT):self.store(LOCK,0)
        self.r['bp'],self.r['si']=old['bp'],old['si']
    def run(self,kind,sp):
        if kind=='move':self.move(self.p['maximum'],self.p['direction'],sp)
        else:self.option(sp)
        self.r['sp']=sp+(6 if kind=='move' else 2);return self

class Machine:
    def __init__(self,mz,load):
        need(mz.valid,'valid MZ');self.load=load;self.base=load*16;self.cs=load+0x990;self.ds=load+0xD7F;self.data=self.ds*16
        self.uc=Uc(UC_ARCH_X86,UC_MODE_16);self.uc.mem_map(0,1<<20);self.initial=bytearray(b'\xA5'*(1<<20));body=mz.relocated_program_image(load);self.initial[self.base:self.base+len(body)]=body
        self.instructions={};self.owned={v for s,n in ENTRIES.values() for v in range(s,s+n)};self.nested=set()
        for start,size in (*ENTRIES.values(),*HELPERS):
            rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[start:start+size],start));need(sum(i.size for i in rows)==size,'complete owner/helper instruction boundaries')
            self.instructions.update({i.address:i.size for i in rows})
            if start not in (MOVE,OPTION):self.nested.update(range(start,start+size))
        self.covered=set();self.nested_covered=set();self.maximum_stack=0
        self.hooks=[self.uc.hook_add(UC_HOOK_CODE,self.code),self.uc.hook_add(UC_HOOK_MEM_WRITE,self.write),self.uc.hook_add(UC_HOOK_INTR,self.interrupt)]
    def close(self):
        for h in self.hooks:self.uc.hook_del(h)
        self.hooks=[];self.uc=None
    def r(self,n):return self.uc.reg_read(REG[n])&65535
    def registers(self):return {n:self.r(n) for n in (*GPRS,'cs','ds','es','ss','fs','gs')}
    def fail(self,e):self.error=str(e);self.uc.emu_stop()
    def peek(self,kind):
        need(self.index<len(self.expected.events),'complete finite event plan');e=self.expected.events[self.index];need(e['kind']==kind,f'event {self.index}: expected {e["kind"]}, got {kind}');return e
    def check_regs(self,regs,mask,flags):
        got=self.registers();need(all(got[n]==v for n,v in regs.items()),'independent full WORD/segment request: '+str((got,regs)))
        need(all(self.uc.reg_read(GPRS[n])==self.high[n]|regs[n] for n in GPRS if n!='sp'),'full request DWORD registers')
        f=self.uc.reg_read(x.UC_X86_REG_EFLAGS);need(f&mask==flags&mask and f&0x600==self.flags&0x600,'defined request flags / IF / DF')
    def frame(self,e,far):
        sp=self.r('sp');need(sp==e['sp'],'exact near/far physical stack frame')
        ip=int.from_bytes(self.uc.mem_read(0x70000+sp,2),'little');cs=int.from_bytes(self.uc.mem_read(0x70000+sp+2,2),'little') if far else self.cs
        need(cs*16+ip-self.base in self.instructions or ip==0xFFFF and cs==self.cs,'frame returns to reviewed instruction boundary')
        size=len(e['args'])*2;actual=tuple(struct.unpack('<'+'H'*len(e['args']),bytes(self.uc.mem_read(0x70000+sp+(4 if far else 2),size)))) if size else ()
        need(actual==e['args'],'complete physical argument WORDs including BYTE padding');return sp,ip,cs
    def code(self,uc,address,size,_):
        try:
            if address==self.cs*16+0xFFFF:self.returned=True;uc.emu_stop();return
            rva=address-self.base;self.maximum_stack=max(self.maximum_stack,self.stack-self.r('sp'))
            if self.index<len(self.expected.events):
                e=self.expected.events[self.index]
                if e['kind']=='entry' and rva==e['address']:
                    self.check_regs(e['request'],e['mask'],e['flags']);self.frame(e,rva in (KAJA,MODE_START,DELAY));self.index+=1
            if rva==DELAY+9:
                e=self.peek('tick');self.index+=1;uc.mem_write(self.data+RUNTIME_FIELDS['counter'],e['value'].to_bytes(2,'little'))
            if rva in LIBRARIES:
                name,_,far=LIBRARIES[rva];e=self.peek('library');need(e['name']==name and e['far']==far,'independent service order')
                self.check_regs(e['request'],e['mask'],e['flags']);sp,ip,cs=self.frame(e,far)
                if 'string_hex' in e:
                    _,off,seg,_,_=e['args'];raw=bytes.fromhex(e['string_hex']);need(bytes(uc.mem_read(seg*16+off,len(raw)))==raw,'actual complete string including NUL')
                self.index+=1
                for n in ('ax','bx','cx','dx','es'):uc.reg_write(REG[n],e['post'][n])
                uc.reg_write(x.UC_X86_REG_EFLAGS,e['post_flags']);uc.reg_write(REG['sp'],sp+(4 if far else 2)+len(e['args'])*2);uc.reg_write(REG['cs'],cs);uc.reg_write(REG['ip'],ip);return
            need(self.instructions.get(rva)==size,'only complete owner/real-helper instructions: '+hex(rva));region=set(range(rva,rva+size));self.covered.update(region&self.owned);self.nested_covered.update(region&self.nested)
        except Exception as error:self.fail(error)
    def write(self,uc,access,address,size,value,_):
        try:
            if 0x70000+self.stack-64<=address and address+size<=0x70000+self.stack:
                self.maximum_stack=max(self.maximum_stack,0x70000+self.stack-address);return
            e=self.peek('store');need(e==dict(kind='store',address=address,size=size,value=value),'exact ordered WORD/BYTE store');self.index+=1
        except Exception as error:self.fail(error)
    def interrupt(self,uc,vector,_):
        try:
            e=self.peek('interrupt');need(e['vector']==vector,'real driver vector');self.check_regs(e['request'],e['request_mask'],e['request_flags']);self.index+=1
            for n,v in e['post'].items():uc.reg_write(REG[n],v)
            uc.reg_write(x.UC_X86_REG_EFLAGS,e['flags'])
        except Exception as error:self.fail(error)
    def run(self,kind,*,selection=0,maximum=3,direction=1,callback='option',input=0,initialized=1,allowed=1,in_option=1,rank=0,bgm=0,key=0,disabled=0,active=1,midi=0,fm=0,driver_ax=0,status=0xFFFF,seed=0x1357,flags=0x202,stack=0xF800,resseg=0x6000,resoff=0x31):
        p=dict(locals());p.pop('self');need(kind in ENTRIES and callback in ('main','option'),'bounded caller/callback')
        need(all(0<=p[n]<=255 for n in ('selection','initialized','allowed','in_option','rank','bgm','key','disabled','active','midi','fm')),'BYTE state')
        need(all(0<=p[n]<=65535 for n in ('maximum','direction','input','driver_ax','status','seed')) and 80<=stack<=0xFFF0 and resseg in (0x5000,0x6000) and 0<=resoff<=0xFF80,'WORD arguments and disjoint stack/resident')
        self.uc.mem_write(0,bytes(self.initial));self.stack,self.flags=stack,flags
        self.uc.mem_write(0x70000+stack-64,b'\xD3'*64);self.uc.mem_write(0x70000+stack,struct.pack('<3H',0xFFFF,direction,maximum) if kind=='move' else b'\xFF\xFF\x5A\xA5')
        self.uc.mem_write(self.data+RESIDENT,struct.pack('<HH',resoff,resseg));res=resseg*16+resoff;self.uc.mem_write(res,b'\xA5'*0x60)
        for off,value in ((SEL,selection),(INIT,initialized),(LOCK,allowed),(INOPT,in_option),(DISABLED,disabled),(ACTIVE,active),(MIDI,midi),(FM,fm)):self.uc.mem_write(self.data+off,bytes((value,)))
        self.uc.mem_write(self.data+PUT,struct.pack('<H',0x5DD if callback=='main' else 0x657));self.uc.mem_write(self.data+INPUT,struct.pack('<H',input))
        for off,value in ((0xB,rank),(0x15,bgm),(0x16,key)):self.uc.mem_write(res+off,bytes((value,)))
        initial={n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)};initial['sp']=stack;initial.update(cs=self.cs,ds=self.ds,es=seed,ss=0x7000,fs=seed^0xA55A,gs=seed^0x5AA5)
        self.high={n:(seed^0x5AA5)<<16 for n in GPRS}
        for n in GPRS:self.uc.reg_write(GPRS[n],self.high[n]|initial[n])
        for n in ('cs','ds','es','ss','fs','gs'):self.uc.reg_write(REG[n],initial[n])
        self.uc.reg_write(x.UC_X86_REG_EFLAGS,flags);self.expected=Prediction(self.uc.mem_read(0,1<<20),initial,p,self.load).run(kind,stack)
        self.index,self.error,self.returned=0,None,False
        try:self.uc.emu_start(self.base+ENTRIES[kind][0],1<<20,count=100000)
        except UcError as e:raise ValueError('OP option guest fault') from e
        need(self.error is None,self.error or 'guest error');need(self.returned and self.index==len(self.expected.events),'complete returning event plan')
        self.check_regs(self.expected.r,self.expected.mask,self.expected.flags)
        need(all(self.uc.reg_read(GPRS[n])==self.high[n]|self.expected.r[n] for n in GPRS),'all DWORD registers including ESP')
        memory=bytes(self.uc.mem_read(0,1<<20));expected=self.expected.memory;lo,hi=0x70000+stack-64,0x70000+stack;expected[lo:hi]=memory[lo:hi]
        need(memory==expected,'every physical memory byte outside 64 stack bytes, including live arguments')
        return dict(registers=self.registers(),full_registers={n:self.uc.reg_read(r) for n,r in GPRS.items()},flags=self.uc.reg_read(x.UC_X86_REG_EFLAGS)&(self.expected.mask|0x600),flags_mask=self.expected.mask,event_count=self.index,event_sha256=hashlib.sha256(json.dumps(self.expected.events,sort_keys=True).encode()).hexdigest(),state=list(memory[self.data+SEL:self.data+INIT+1]),options=list(memory[res+0xB:res+0x17]))

def cases():
    # Each BYTE lane is exhaustive independently; this is not the Cartesian
    # product of every unchecked caller state. High parameter bytes are live.
    for callback,maximum in (('option',3),('main',5)):
        for selection in range(256):
            for direction in (0x5A01,0xA5FF):yield 'move',dict(callback=callback,maximum=0xA500|maximum,direction=direction,selection=selection)
        for direction in range(256):
            for selection in (0,127,128,255):yield 'move',dict(callback=callback,maximum=maximum,direction=0x5A00|direction,selection=selection)
        for maximum in range(256):
            for selection in (0,127):yield 'move',dict(callback=callback,maximum=0xA500|maximum,direction=0x5AFF,selection=selection)
    yield 'move',dict(selection=1,direction=0,bgm=2)
    for selection in (0,1,2,3,4,127,128,255):
        for arrows in range(16):
            for buttons in (0,0x20,0x2000,0x1000,0x3020,0x8000):yield 'option',dict(selection=selection,input=arrows|buttons)
    for selection,field in ((0,'rank'),(1,'bgm'),(2,'key')):
        for value in range(256):
            for arrows in (4,8,12):yield 'option',dict(selection=selection,input=arrows,**{field:value})
    for active in (0,1,255):
        for midi in (0,1,2,255):
            for disabled in (0,255):
                for bgm in (0,1,255):
                    for driver_ax in (0,0x12FF,0xFFFF):
                        for arrows in (4,8,12):yield 'option',dict(selection=1,input=arrows,active=active,midi=midi,disabled=disabled,bgm=bgm,driver_ax=driver_ax)
    for initialized in (0,1,255):
        for allowed in (0,1,255):
            for selection in (0,1,2,3,128,255):
                for input in (0,3,12,0x20,0x1000,0x302F):yield 'option',dict(initialized=initialized,allowed=allowed,selection=selection,input=input)
    # Orthogonal register, flag, resident and stack ABI profiles.
    for seed in (0,1,0x1357,0xECA8,0x8000,0xFFFF):
        for flags in (2,0x202,0x402,0xED7):
            for stack in (0x80,0xFFF0):
                for kind,p in (('move',dict(selection=255,maximum=0xA503,direction=0x5A01)),('option',dict(initialized=0)),('option',dict(selection=1,input=12,driver_ax=0x12FF,midi=2))):
                    yield kind,dict(p,seed=seed,flags=flags,stack=stack,resseg=0x5000,resoff=0xFF80)

def verify(target,candidate):
    observations=[]
    for mz in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(mz,load);trace=hashlib.sha256();counts={'move':0,'option':0};maximum_events=0
            try:
                for kind,p in cases():
                    try:row=m.run(kind,**p)
                    except ValueError as e:raise ValueError(f'{kind} {p}: {e}') from e
                    trace.update(json.dumps(row,sort_keys=True).encode());counts[kind]+=1;maximum_events=max(maximum_events,row['event_count'])
                need(m.covered==m.owned,'every one of 595 owner instruction bytes executes')
                need(m.nested_covered==m.nested,'unexecuted helper instruction bytes: '+str(sorted(m.nested-m.nested_covered)))
                loads.append(dict(load_segment=load,cases=sum(counts.values()),cases_by_function=counts,executed_owner_bytes=len(m.covered),executed_nested_bytes=len(m.nested_covered),maximum_stack_depth=m.maximum_stack,maximum_events=maximum_events,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent target/candidate observations')
    return dict(images=2,functions=2,code_bytes=595,executed_owner_bytes=595,cases_per_image=sum(o['cases'] for o in observations[0]),observations=observations[0],exhaustive_BYTE_lanes=['selection','maximum','direction','rank','bgm','key'],ignored_private_stack_bytes=64,real_nested_helpers=True,main_caller_accepted=False,whole_product_accepted=False)

def negative_controls(target):
    rows=[
      ('move-callback-black',0xA0AA,1,dict(kind='move')),
      ('move-signed-negative',0xA0BB,14,dict(kind='move',selection=128,direction=0)),
      ('move-max-second-check',0xA0C9,8,dict(kind='move',selection=127,maximum=128,direction=0)),
      ('move-callback-white',0xA0D6,1,dict(kind='move')),
      ('move-pascal-pop',0xA0DE,2,dict(kind='move')),
      ('option-init-branch',0xA20C,1,dict(initialized=0)),
      ('option-clear-lock',0xA21A,1,dict(initialized=0,input=8)),
      ('option-init-choices',0xA237,1,dict(initialized=0)),
      ('option-callback-pointer',0xA23E,1,dict(initialized=0,input=3)),
      ('option-up-mask',0xA263,1,dict(input=1)),
      ('option-down-mask',0xA271,2,dict(input=2)),
      ('option-right-mask',0xA27F,8,dict(input=8)),
      ('option-rank-limit',0xA2A4,1,dict(input=8,rank=2)),
      ('option-rank-reset',0xA2AB,1,dict(input=8,rank=3)),
      ('option-sound-disabled',0xA2B4,1,dict(input=8,selection=1,disabled=255)),
      ('option-enable-bgm',0xA2C4,1,dict(input=8,selection=1)),
      ('option-stop-argument',0xA2C6,1,dict(input=8,selection=1)),
      ('option-play-argument',0xA2D3,1,dict(input=8,selection=1)),
      ('option-sound-active-clear',0xA2F0,1,dict(input=8,selection=1,bgm=1)),
      ('option-key-limit',0xA30A,1,dict(input=8,selection=2,key=1)),
      ('option-left-mask',0xA321,4,dict(input=4)),
      ('option-rank-left-wrap',0xA34A,1,dict(input=4)),
      ('option-key-left-wrap',0xA3B6,1,dict(input=4,selection=2)),
      ('option-confirm-high-mask',0xA3D0,32,dict(input=0x2000,selection=3)),
      ('option-confirm-low-mask',0xA3D7,32,dict(input=0x20,selection=3)),
      ('option-quit-selection',0xA3E0,1,dict(input=0x20,selection=3)),
      ('option-return-main-selection',0xA3EC,1,dict(input=0x20,selection=3)),
      ('option-cancel-mask',0xA3F6,16,dict(input=0x1000)),
      ('option-cancel-state',0xA407,1,dict(input=0x1000)),
      ('option-lock-reset',0xA413,1,dict(input=0x8000)),
      ('real-mode-vector',MODE_START+3,1,dict(input=8,selection=1)),
      ('real-kaja-midi-policy',KAJA+17,1,dict(input=8,selection=1,midi=1)),
      ('real-box-step',BOX+34,8,dict(initialized=0)),
      ('real-delay-limit',DELAY+15,5,dict(initialized=0)),
      ('real-option-renderer',RENDERERS['option'][0]+10,2,dict(input=8)),
    ];rejected=[]
    for name,at,mask,p in rows:
        raw=bytearray(target.program_image);raw[at]^=mask;m=Machine(replace(target,program_image=bytes(raw)),0x3000)
        try:
            try:m.run(p.pop('kind','option'),**p)
            except ValueError:rejected.append(name)
            else:raise ValueError('OP option instruction mutation survived: '+name)
        finally:m.close()
    return dict(count=len(rows),rejected=rejected,actual_instruction_mutations=len(rows),data_mutations=0)
