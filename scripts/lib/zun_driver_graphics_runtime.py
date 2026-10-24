"""CPU graphics contracts with a bounded two-page memory interface.

All twelve real procedures execute. Port width/order/IF/DF and page selection
are observed. The memory fixture exposes ordinary words in four video banks;
it does not emulate EGC latches, raster operations or physical pixel rendering.
"""
import hashlib
import json
import struct
from unicorn import Uc,UcError,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INSN,UC_HOOK_INTR
from unicorn.x86_const import *
from lib.zun_driver_graphics_layout import RANGES,control_flow

ENTRIES={n.removeprefix('sprite16_'):(a,s) for n,a,s in RANGES}
REG={n:globals()['UC_X86_REG_'+n.upper()] for n in ('ax','bx','cx','dx','si','di','bp','sp','cs','ds','es','ss','ip')}
GPRS={n:globals()['UC_X86_REG_E'+n.upper()] for n in ('ax','bx','cx','dx','si','di','bp')}
BANKS=(0xA8000,0xB0000,0xB8000,0xE0000)
FIELDS=dict(zip(('shift','has_shift','clipped','skip','words','x','y','source','width','height','mono','color','overlap','rop','mask','plane'),range(0x1050,0x1070,2)))
BEGIN=((0x6A,1,7),(0x6A,1,5),(0x6A,1,6),(0x7C,1,0x80),(0x4A0,2,0xFFF0),(0x4A2,2,0xFF),(0x4A4,2,0x28F0),(0x4A8,2,0xFFFF),(0x4AC,2,0),(0x4AE,2,15))
END=((0x4A0,2,0xFFF0),(0x4A2,2,0xFF),(0x4A8,2,0xFFFF),(0x6A,1,7),(0x6A,1,4),(0x6A,1,6),(0x7C,1,0))

def need(value,message):
    if not value:raise ValueError('ZUN graphics contract: '+str(message))
def signed(v):return v-65536 if v&0x8000 else v
def parity(v):return 4 if (v&255).bit_count()%2==0 else 0
def cmp16(a,b):
    r=(a-b)&65535
    return int(a<b)|parity(r)|((a^b^r)&16)|(64 if not r else 0)|(r>>8&128)|(((a^b)&(a^r)&0x8000)>>4)
def add16(a,b):
    r=(a+b)&65535
    return int(a+b>65535)|parity(r)|((a^b^r)&16)|(64 if not r else 0)|(r>>8&128)|((~(a^b)&(a^r)&0x8000)>>4)

class Prediction:
    def __init__(self,memory,pages,page,registers,flags,base):
        self.memory=bytearray(memory);self.pages=[[bytearray(b) for b in p] for p in pages];self.page=page
        self.regs=dict(registers);self.flags=flags&0x600;self.flag_mask=0x8C5;self.flag_value=0x44;self.base=base
        self.events=[];self.display=None
    def word(self,seg,off):
        a=seg*16+(off&65535);return int.from_bytes(self.memory[a:a+2],'little')
    def store(self,address,value):
        value&=65535;self.events.append(('store',address,2,value));self.memory[address:address+2]=value.to_bytes(2,'little')
    def field(self,name,value=None):
        at=self.base+FIELDS[name]
        if value is None:return int.from_bytes(self.memory[at:at+2],'little')
        self.store(at,value)
    def flush(self):
        for i,a in enumerate(BANKS):self.pages[self.page][i][:]=self.memory[a:a+0x8000]
    def out(self,port,size,value):
        self.events.append(('out',port,size,value,self.flags))
        if port==0xA4:self.display=value
        if port==0xA6 and value!=self.page:
            need(value in (0,1),'two-page selection');self.flush();self.page=value
            for i,a in enumerate(BANKS):self.memory[a:a+0x8000]=self.pages[value][i]
    def egc(self,begin):
        self.flags&=~0x200
        for p,s,v in BEGIN if begin else END:self.out(p,s,v)
        self.flags|=0x200;self.flag_mask,self.flag_value=0x8C5,0x44
    def copy(self,source,si,dest,di,words):
        for _ in range(words):
            self.store(dest*16+di,self.word(source,si));si=(si+2)&65535;di=(di+2)&65535
        return si,di
    def rows(self):
        r=self.regs;si,di=r['si'],r['di'];h=self.field('height') or 65536;words=self.field('words');skip=self.field('skip')
        need(words*h<=200000,'bounded word-copy domain')
        if words:
            for _ in range(h):si,di=self.copy(r['ds'],si,r['es'],di,words);si=(si+skip)&65535;di=(di+skip)&65535
        last=((r['di']+(h-1)*(words*2+skip))&65535);after=(last+words*2)&65535
        r.update(ax=skip,bx=0,cx=0,dx=words);self.flag_mask,self.flag_value=0x8D5,0x44|int(after+skip>65535)
    def blit(self):
        r=self.regs;source=self.field('source');x,y=self.field('x'),self.field('y');width=self.field('width')
        di=(y*80+((x>>3)&0xFFFE))&65535;shift=x&15
        self.field('shift',shift);self.out(0x4AC,2,shift<<4);self.field('has_shift',0);self.field('has_shift',int(shift!=0))
        self.out(0x4AE,2,((width<<4)-1)&65535);words=(width+bool(shift))&65535
        self.field('words',words);self.field('skip',80-words*2)
        r.update(si=source,di=di,es=0xA800)
        if self.field('mono'):
            for p,v in ((0x4A2,0xFF),(0x4A8,self.field('mask')),(0x4A2,0x40FF),(0x4A4,0xCAC),(0x4A6,self.field('color'))):self.out(p,2,v)
            r['ds']=self.word(self.base//16,0xF3E)
        else:
            if self.field('overlap'):
                for p,v in ((0x4A0,0xFFF0),(0x4A2,0xFF),(0x4A4,0xCC0),(0x4A8,self.field('mask'))):self.out(p,2,v)
                r['ds']=self.word(self.base//16,0xF3C);self.rows()
            else:
                self.out(0x4A2,2,0xFF);self.out(0x4A8,2,self.field('mask'))
            self.out(0x4A4,2,self.field('rop'));r.update(ds=0xA800,si=(r['si']+0x3E80)&65535)
        self.out(0x4A0,2,self.field('plane'));self.rows()
    def clip(self):
        saved=dict(self.regs);r=self.regs
        for k,v in (('x',r['dx']),('y',r['bx']),('source',r['di']),('width',r['ax']&255),('height',r['cx']),('clipped',0)):self.field(k,v)
        y,h=r['bx'],r['cx'];draw=True
        if signed(y)<0:
            total=(y+h)&65535
            if signed(total)<=0:self.flag_mask,self.flag_value=0x8D5,cmp16(total,0);draw=False
            else:self.field('clipped',-y);self.field('source',r['di']+(-y)*80);self.field('y',0)
        elif y>=200:self.flag_mask,self.flag_value=0x8D5,cmp16(y,200);draw=False
        elif signed((y+h)&65535)>200:self.field('clipped',(y+h-200)&65535)
        if draw:self.field('height',h-self.field('clipped'));self.blit()
        self.regs=saved
    def accumulate(self,source,dest):
        last=0
        for off in range(0,16000,2):
            last=self.word(source,off+16000);self.store(dest*16+off,self.word(dest,off)|last)
        return last
    def compress(self):
        self.egc(True)
        for row in range(200):self.copy(0xA800,row*160,0xA800,row*80,40)
        self.egc(False)
    def upper(self):
        self.egc(True);self.copy(0xA800,0,0xA800,16000,8000);self.egc(False)
        self.regs.update(ax=0xA800,ds=0xA800,es=0xA800,si=16000,di=32000,cx=0)
    def lower(self):
        self.egc(True)
        for off in range(16000,32000,2):
            self.out(0xA6,1,0);word=self.word(0xA800,off);self.out(0xA6,1,1);self.store(0xA8000+off,word)
        self.egc(False)
    def run(self,kind):
        saved=dict(self.regs)
        if kind=='draw_clipped':self.clip()
        elif kind=='blit_egc':self.blit()
        elif kind=='copy_rows':self.rows()
        elif kind in ('egc_begin','egc_end'):self.egc(kind=='egc_begin')
        elif kind=='accumulate_plane':
            plane=self.regs['ax'];last=self.accumulate(plane,self.regs['es']);self.regs.update(ds=plane,ax=last,bx=16000,cx=0)
            self.flag_mask,self.flag_value=0x8D5,add16(15998,2)
        elif kind=='compress_rows':self.compress()
        elif kind=='copy_upper_to_lower':self.upper()
        elif kind=='copy_lower_page':self.lower()
        elif kind=='clear_upper':
            self.egc(True);self.out(0x4A4,2,0)
            for off in range(0,16000,2):self.store(0xA8000+off,0)
            self.egc(False)
        elif kind=='prepare_vram':
            self.out(0x6A,1,1);self.out(0xA6,1,0);self.compress();self.upper();self.lower();self.out(0xA4,1,0);self.out(0xA6,1,0)
            self.regs=saved
        else:
            self.egc(False);self.out(0xA6,1,0);solid=self.word(self.base//16,0xF3E);mask=self.word(self.base//16,0xF3C)
            for off in range(0,16000,2):self.store(solid*16+off,0)
            for bank in BANKS:self.accumulate(bank//16,solid)
            for off in range(0,16000,2):self.store(mask*16+off,~self.word(solid,off))
            self.flag_mask,self.flag_value=0x8C5,0x44
        self.flush()

class Machine:
    def __init__(self,image,load):
        need(len(image)==4224,'whole driver image');self.load,self.base=load,load*16
        self.instructions,self.reachable,self.cfg=control_flow(image)
        self.uc=Uc(UC_ARCH_X86,UC_MODE_16);self.uc.mem_map(0,1<<20)
        self.initial=bytearray(b'\xA5'*(1<<20));self.initial[self.base+256:self.base+256+len(image)]=image
        self.page_templates=[[bytes((i*(17+bank*2)+i//257+page*53)&255 for i in range(0x8000)) for bank in range(4)] for page in range(2)]
        self.covered=set();self.maximum_stack=0
        self.hooks=[self.uc.hook_add(UC_HOOK_CODE,self.code),self.uc.hook_add(UC_HOOK_MEM_WRITE,self.write),
            self.uc.hook_add(UC_HOOK_INSN,self.out,None,1,0,UC_X86_INS_OUT),self.uc.hook_add(UC_HOOK_INTR,lambda uc,n,_:self.fail('unexpected interrupt '+str(n)))]
    def close(self):
        for h in self.hooks:self.uc.hook_del(h)
        self.hooks=[];self.uc=None
    def r(self,n):return self.uc.reg_read(REG[n])&65535
    def fail(self,e):self.error=str(e);self.uc.emu_stop()
    def event(self,e):
        need(self.index<len(self.expected.events) and e==self.expected.events[self.index],f'ordered graphics event {self.index}: {e}');self.index+=1
    def flush(self):
        for i,a in enumerate(BANKS):self.pages[self.page][i][:]=self.uc.mem_read(a,0x8000)
    def code(self,uc,address,size,_):
        try:
            if address==self.base+0xFFFF:self.returned=True;uc.emu_stop();return
            ip=address-self.base;need(ip in self.instructions and self.instructions[ip].size==size,'execution in complete graphics instructions')
            self.covered.update(set(range(ip,ip+size))&self.reachable);self.maximum_stack=max(self.maximum_stack,self.stack-self.r('sp'))
        except Exception as e:self.fail(e)
    def write(self,uc,access,address,size,value,_):
        try:
            if self.stack_base+self.stack-64<=address and address+size<=self.stack_base+self.stack:return
            self.event(('store',address,size,value))
        except Exception as e:self.fail(e)
    def out(self,uc,port,size,value,_):
        try:
            self.event(('out',port,size,value,uc.reg_read(UC_X86_REG_EFLAGS)&0x600))
            if port==0xA6 and value!=self.page:
                need(value in (0,1),'bounded page controller');self.flush();self.page=value
                for i,a in enumerate(BANKS):uc.mem_write(a,bytes(self.pages[value][i]))
        except Exception as e:self.fail(e)
    def run(self,kind,*,x=8,y=2,width=2,height=3,source=0x200,words=3,skip=4,mono=0,overlap=1,
            color=0xB,mask=0x5AA5,rop=0x28FC,plane=0xFFF0,page=0,flags=0x202,pattern=0,stack=0xF800,split_stack=False):
        need(kind in ENTRIES and page in (0,1) and 0<=width<=255 and 0<=words<=40,'bounded graphics inputs')
        need(kind in ('egc_begin','egc_end','copy_lower_page','accumulate_plane') or not flags&0x400,'forward graphics precondition')
        self.uc.mem_write(0,bytes(self.initial));self.page=page;self.stack=stack;ss=0x8000 if split_stack else self.load;self.stack_base=ss*16
        table=bytes(i^(pattern&255) for i in range(256));self.pages=[[bytearray(b.translate(table)) for b in p] for p in self.page_templates]
        for i,a in enumerate(BANKS):self.uc.mem_write(a,bytes(self.pages[page][i]))
        # Caller-owned solid/mask buffers and foreign row source/destination.
        for base in (0x40000,0x50000,0x60000,0x70000):self.uc.mem_write(base,bytes((i*29+(base>>12)+pattern)&255 for i in range(0x10000)))
        values=dict(shift=0xA5A5,has_shift=0xA5A5,clipped=0xA5A5,skip=skip,words=words,x=x,y=y,source=source,width=width,height=height,
            mono=mono,color=color,overlap=overlap,rop=rop,mask=mask,plane=plane)
        for name,value in values.items():self.uc.mem_write(self.base+FIELDS[name],struct.pack('<H',value&65535))
        self.uc.mem_write(self.base+0xF3C,struct.pack('<HH',0x6000,0x5000))
        self.uc.mem_write(self.stack_base+stack-64,b'\xCC'*64);self.uc.mem_write(self.stack_base+stack,b'\xFF\xFF\x53\xA9')
        regs=dict(ax=0xB500|width,bx=y&65535,cx=height&65535,dx=x&65535,si=0x3E00,di=source&65535,bp=0xA675^pattern,
            cs=self.load,ds=self.load if kind=='blit_egc' else 0x4000,es=0x7000,ss=ss)
        if kind=='accumulate_plane':regs['ax']=0xA800
        if kind=='copy_rows':regs['di']=0x2000
        initial=bytes(self.uc.mem_read(0,1<<20));self.expected=Prediction(initial,self.pages,page,regs,flags,self.base);self.expected.run(kind)
        high={n:(0xA5A5^pattern)<<16 for n in GPRS}
        for n in GPRS:self.uc.reg_write(GPRS[n],high[n]|regs[n])
        for n in ('cs','ds','es','ss'):self.uc.reg_write(REG[n],regs[n])
        self.uc.reg_write(UC_X86_REG_ESP,stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        self.index,self.error,self.returned=0,None,False
        try:self.uc.emu_start(self.base+ENTRIES[kind][0],self.base+0x10000,count=10000000)
        except UcError as e:raise ValueError('ZUN graphics contract: guest fault') from e
        need(self.error is None,self.error or 'guest error');need(self.returned and self.uc.reg_read(UC_X86_REG_ESP)==stack+2,'near return frame')
        r=self.expected.regs;actual={n:self.r(n) for n in r}
        need(actual==r,'independent WORD/segment result: '+str([(n,hex(actual[n]),hex(v)) for n,v in r.items() if actual[n]!=v]))
        need(all(self.uc.reg_read(GPRS[n])==high[n]|r[n] for n in GPRS),'unchanged DWORD high halves')
        f=self.uc.reg_read(UC_X86_REG_EFLAGS)
        need(f&self.expected.flag_mask==self.expected.flag_value&self.expected.flag_mask,'defined final flags')
        need(f&0x600==self.expected.flags,'actual IF/DF, including unconditional STI')
        need(self.index==len(self.expected.events) and self.page==self.expected.page,'complete event/page sequence')
        self.flush();need(self.pages==self.expected.pages,'both complete video pages under word-memory fixture')
        memory=bytes(self.uc.mem_read(0,1<<20));lo,hi=self.stack_base+stack-64,self.stack_base+stack
        self.expected.memory[lo:hi]=memory[lo:hi];need(memory==self.expected.memory,'whole physical memory outside bounded stack')
        return dict(registers=actual,flags_mask=self.expected.flag_mask,result_flags=f&self.expected.flag_mask,if_df=f&0x600,access_page=self.page,
            event_count=len(self.expected.events),events_sha256=hashlib.sha256(json.dumps(self.expected.events).encode()).hexdigest(),
            page_sha256=[[hashlib.sha256(b).hexdigest() for b in p] for p in self.pages])

def cases():
    for kind in ('egc_begin','egc_end','copy_lower_page','accumulate_plane'):
        for flags in (2,0x202,0x402,0xED7):yield kind,dict(flags=flags,page=int(bool(flags&0x400)))
    for kind in ('prepare_vram','build_mask','compress_rows','copy_upper_to_lower','clear_upper'):
        for page in (0,1):yield kind,dict(page=page,flags=2 if page else 0x202)
    for mono,overlap in ((0,0),(0,1),(1,0),(0x8000,0xFFFF)):
        for x in (0,1,15,16,0xFFFF):
            for y in (-3,-1,0,198,199,200,0x7FFF,0x8000):
                yield 'draw_clipped',dict(x=x,y=y,width=2,height=3,mono=mono,overlap=overlap)
        yield 'blit_egc',dict(mono=mono,overlap=overlap,page=1)
    for x in range(16):yield 'draw_clipped',dict(x=x,width=0 if x==0 else 1,y=-1,height=202)
    for kind in ('copy_rows',):
        for height in (1,2,3):
            for words in (0,1,2,40):
                for skip in (0,2,80-words*2,0xFFFE):yield kind,dict(height=height,words=words,skip=skip)
        yield kind,dict(height=0,words=0,skip=80)
    yield 'draw_clipped',dict(x=0,y=199,width=0,height=0x8000)

def verify(target,candidate):
    observations=[]
    for image in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(image,load)
            try:
                trace=hashlib.sha256()
                for count,(kind,options) in enumerate(cases(),1):
                    row=m.run(kind,pattern=0 if count&1 else 0x5A5A,stack=0xF800 if count&1 else 0xE800,split_stack=bool(count&1),**options)
                    trace.update(json.dumps(row,sort_keys=True).encode())
                need(m.covered==m.reachable,'all 810 reachable owner bytes execute')
                loads.append(dict(load_segment=load,cases=count,covered_owner_bytes=len(m.covered),unreachable_owner_bytes=4,
                    maximum_observed_stack_depth=m.maximum_stack,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent target/candidate graphics observations')
    return dict(images=2,functions=12,code_bytes=814,executed_owner_bytes=810,unreachable_owner_bytes=4,
        cases_per_image=sum(o['cases'] for o in observations[0]),observations=observations[0],video_pages=2,video_banks=4,
        scope='real graphics instructions; port/IF/DF and two-page word-memory interface; no physical EGC latch/ROP/pixel claims')

def negative_controls(image):
    controls=(
        ('width-is-AL-not-AH',0x370,b'\xE4',b'\xC0','draw_clipped',{}),
        ('x-field-store',0x373,b'\x5A',b'\x5C','draw_clipped',{}),
        ('signed-top-rejection',0x39B,b'\x7F',b'\x77','draw_clipped',dict(y=-3,height=1)),
        ('top-source-stride',0x3AD,b'\x04',b'\x03','draw_clipped',dict(y=-1)),
        ('bottom-row-199-is-visible',0x3C5,b'\xC8',b'\xC7','draw_clipped',dict(y=199,height=1)),
        ('EGC-bit-length-times-sixteen',0x44D,b'\x04',b'\x03','blit_egc',{}),
        ('nonzero-shift-adds-word',0x43B,b'\x95',b'\x94','blit_egc',{}),
        ('row-skip-uses-double-width',0x45E,b'\xE0',b'\xE8','blit_egc',{}),
        ('mono-solid-buffer',0x498,b'\x3E',b'\x3C','blit_egc',dict(mono=1)),
        ('mono-shift-mode',0x48B,b'\x0C',b'\x08','blit_egc',dict(mono=1)),
        ('overlap-zero-test',0x4A1,b'\0',b'\x01','blit_egc',{}),
        ('color-lower-half-offset',0x4E9,b'\x80',b'\x82','blit_egc',dict(overlap=0)),
        ('active-plane-port',0x4EC,b'\xA0',b'\xA2','blit_egc',{}),
        ('row-height-field',0x4FD,b'\x62',b'\x60','copy_rows',{}),
        ('row-word-count-field',0x502,b'\x58',b'\x56','copy_rows',{}),
        ('row-count-decrements',0x510,b'\x4B',b'\x43','copy_rows',{}),
        ('near-row-return',0x515,b'\xC3',b'\xCB','copy_rows',{}),
        ('display-page-reset-port',0x537,b'\xA4',b'\xA6','prepare_vram',{}),
        ('mask-inverts-bits',0x588,b'\xD0',b'\xD8','build_mask',{}),
        ('accumulation-is-OR',0x59C,b'\x09',b'\x31','accumulate_plane',{}),
        ('lower-copy-destination-page-one',0x5B2,b'\x01',b'\0','copy_lower_page',{}),
        ('compress-skips-one-source-row',0x5ED,b'\x50',b'\x52','compress_rows',{}),
        ('upper-to-lower-destination',0x605,b'\x80',b'\x82','copy_upper_to_lower',{}),
        ('clear-all-eight-thousand-words',0x627,b'\x40',b'\x3F','clear_upper',{}),
        ('begin-unconditionally-enables-IF',0xC0C,b'\xFB',b'\xFA','egc_begin',dict(flags=2)),
        ('end-unconditionally-enables-IF',0xC38,b'\xFB',b'\x90','egc_end',dict(flags=2)),
    )
    rejected=[]
    for name,at,old,new,kind,options in controls:
        raw=bytearray(image);need(raw[at-256:at-256+len(old)]==old,'literal mutation anchor '+name)
        raw[at-256:at-256+len(new)]=new;m=None
        try:
            try:m=Machine(bytes(raw),0x3000);m.run(kind,**options)
            except ValueError:rejected.append(name)
            else:raise ValueError('ZUN graphics mutation survived: '+name)
        finally:
            if m:m.close()
    return dict(count=len(rejected),rejected=rejected)
