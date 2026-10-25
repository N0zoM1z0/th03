"""Actual OP init/CFG/input/exit bodies get independent source-level predictions.

Library/device replies remain explicit. The CRT copy body executes as context;
it adds no source ownership here. No private stack bytes are ignored by these
primitive specifications.
"""
from lib.op_startup_state import State,address,logical,ARITH,need
from lib.op_cfg_runtime import reply

ENTRIES={'init':(0xC421,105,8),'planes':(0xBED1,41,4),'cfg_load':(0x9908,120,2),
    'cfg_exit':(0x99C3,84,2),'mode':(0xBEFA,29,4),'copy':(0x337E,28,12),
    'exit_dos':(0xBEB8,25,4),'exit':(0xBFC2,67,4),'input':(0xC986,36,4),'delay':(0xC19E,21,6)}
LIBRARIES={0x10FE:('graph400',0),0x21F4:('text_clear',0),0x2AC6:('resident_create',0),
    0x2B3C:('resident_free',0),0x688:('puts',4),0x952E:('getch',0),
    0xEF6:('gaiji_backup',0),0xF36:('gaiji_load',4),0xF1A:('gaiji_restore',0),
    0x245A:('assign',2),0x19F6:('graph_start',0),0x114C:('graph_clear',0),0x22CA:('vsync_start',0),
    0x1A22:('key_beep_off',0),0x2232:('systemline_hide',0),0x2226:('cursor_hide',0),0x708:('egc_start',0),
    0x2DB8:('js_start',0),0x2B60:('pfstart',4),0x2C1C:('pfend',0),0x2378:('vsync_end',0),
    0x2676:('mem_unassign',0),0x1A1C:('js_end',0),0x1A2E:('key_beep_on',0),
    0x2238:('systemline_show',0),0x222C:('cursor_show',0),0x9A8:('open',4),0x8F4:('read',6),
    0x888:('close',0),0x7C8:('append',4),0x9E4:('seek',6),0xA26:('write',6)}
NEAR_LIBRARIES={0xADE2:'animate',0xB008:'fade',0xB38D:'cdg1',0xB3EF:'cdg3',0xB3C3:'cdg2'}
SAMPLES={0xC1B4:'sense',0x2DF4:'js'}


class Primitive(State):
    def __init__(self,*args):
        super().__init__(*args)
        self.file=bytearray(self.o['file'])
        self.sample_count=0

    def adopt(self,child):
        self.events.extend(child.events)
        self.r,self.high,self.flags,self.mask=child.r,child.high,child.flags,child.mask
        self.file=child.file
        self.calls=child.calls

    def service(self,name,continuation,cleanup=0,args=(),far=True):
        if far:
            self.frame(continuation,0)
        else:
            self.push(continuation)
        size=(4 if far else 2)+len(args)*2
        at=address(self.ss,self.r['sp'])
        self.calls+=1
        mask=self.mask|0x600
        self.events.append(('service',name,self.full(),bytes(self.memory[at:at+size]).hex(),self.flags&mask,mask,
                            cleanup,far,self.calls))
        if name=='read':
            amount,offset,segment=args
            raw=self.o['cfg'][:min(amount,self.o['read_bytes'])]
            if raw:
                dest=address(segment,offset)
                self.events.append(('file-bytes',dest,raw.hex()))
                self.memory[dest:dest+len(raw)]=raw
        elif name=='write':
            amount,offset,segment=args
            raw=bytes(self.memory[address(segment,offset):address(segment,offset)+amount])
            self.events.append(('file-write',raw.hex()))
            self.file[:amount]=raw
        if name=='cdg2' and continuation==0xBD0 and self.o['raw_dispatch'] is not None:
            value=self.o['raw_dispatch']
            self.events.append(('surface-write',address(self.ds,0x118C),value))
            self.memory[address(self.ds,0x118C)]=value
        status=self.o['assign'] if name=='assign' else self.o['status']
        self.r,self.flags=reply(self.r,self.calls,self.o['seed'],self.flags,status)
        self.mask=ARITH
        if far:
            self.returned(cleanup)
        else:
            self.r['sp']+=2+cleanup

    def call(self,kind,continuation,far=True,bridge=False):
        if bridge:
            self.push(self.r['cs'])
            self.push(continuation)
        elif far:
            segment=0 if kind=='copy' else 0xBEB
            self.frame(continuation,segment)
        else:
            self.push(continuation)
        self.entry(kind,ENTRIES[kind][2])
        child=Primitive(self.memory,self.r,self.high,self.flags,dict(self.o,file=bytes(self.file)))
        child.calls=self.calls
        child.mask=self.mask
        child.invoke(kind)
        self.adopt(child)
        self.done(kind)

    def output(self,port,value):
        self.r['dx']=port
        self.al(value)
        self.events.append(('out',port,1,value&255,self.flags&0x200))

    def invoke(self,kind):
        if kind=='mode':
            self.r['ax']=(self.r['ax']&255)|0x900
            self.calls+=1
            mask=self.mask|0x600
            self.events.append(('driver',self.full(),self.flags&mask,mask,self.calls))
            self.r,self.flags=reply(self.r,self.calls,self.o['seed'],self.flags,self.o['status'])
            self.al(self.o['driver'])
            self.mask=ARITH
            self.r['bx']=0
            self.logic(0)
            value=self.r['ax']&255
            self.op(value,255,True,bits=8)
            if value!=255:
                carry=self.flags&1
                self.r['bx']=self.op(self.r['bx'],1)
                self.flags=(self.flags&~1)|carry
                self.field(0x1A0A,1,1)
            else:
                self.r['bx']=(self.r['bx']&0xFF00)|self.dg(0x1A0B,1)
            self.field(0x5DC,self.r['bx']&255,1)
            self.r['ax']=self.r['bx']
            self.returned()
            return
        self.enter(10 if kind=='cfg_load' else 8 if kind=='cfg_exit' else 0)
        if kind=='planes':
            for index,value in enumerate((0xA8000000,0xB0000000,0xB8000000,0xE0000000)):
                self.field(0x19FA+index*4,value,4)
        elif kind=='init':
            self.push(22000)
            self.service('assign',0x57C,2,(22000,))
            self.logic(self.r['ax'])
            if self.r['ax']:
                self.r['ax']=1
            else:
                self.call('planes',0x58A,bridge=True)
                self.service('graph_start',0x58F)
                self.output(0xA6,1)
                self.service('graph_clear',0x59A)
                self.output(0xA6,0)
                self.service('graph_clear',0x5A5)
                self.output(0xA6,0)
                self.output(0xA4,0)
                for name,ret in (('vsync_start',0x5B4),('key_beep_off',0x5B9),('systemline_hide',0x5BE),
                                 ('cursor_hide',0x5C3),('egc_start',0x5C8),('js_start',0x5CD)):
                    self.service(name,ret)
                value=self.word(self.ss,self.r['bp']+6,4)
                self.push(value,4)
                self.service('pfstart',0x5D6,4,(value&65535,value>>16))
                self.r['ax']=0
                self.logic(0)
        elif kind in ('exit','exit_dos'):
            if kind=='exit_dos':
                self.call('exit',0x10,bridge=True)
                for name,ret in (('key_beep_on',0x15),('systemline_show',0x1A),('cursor_show',0x1F)):
                    self.service(name,ret)
            else:
                self.service('pfend',0x11A)
                self.output(0xA6,1)
                self.service('graph_clear',0x125)
                self.output(0xA6,0)
                self.service('graph_clear',0x130)
                self.output(0xA6,0)
                self.output(0xA4,0)
                for name,ret in (('vsync_end',0x13F),('mem_unassign',0x144),('text_clear',0x149),('js_end',0x14E),('egc_start',0x153)):
                    self.service(name,ret)
        elif kind=='copy':
            self.push(self.r['si'])
            self.push(self.r['di'])
            self.push(self.ds)
            self.r['si']=self.word(self.ss,self.r['bp']+6)
            self.r['ds']=self.word(self.ss,self.r['bp']+8)
            self.r['di']=self.word(self.ss,self.r['bp']+10)
            self.r['es']=self.word(self.ss,self.r['bp']+12)
            self.flags&=~0x400
            original=self.r['cx']
            self.r['cx']=original>>1
            self.flags=(self.flags&0x600)|2|logical(self.r['cx'])|(original&1)
            self.mask=0x8C5
            for _ in range(self.r['cx']):
                value=self.word(self.r['ds'],self.r['si'])
                self.store(address(self.r['es'],self.r['di']),2,value)
                self.r['si']=(self.r['si']+2)&65535
                self.r['di']=(self.r['di']+2)&65535
            self.r['cx']=0
            self.r['cx']=self.op(0,self.flags&1)
            if self.r['cx']:
                value=self.word(self.r['ds'],self.r['si'],1)
                self.store(address(self.r['es'],self.r['di']),1,value)
                self.r['si']=(self.r['si']+1)&65535
                self.r['di']=(self.r['di']+1)&65535
                self.r['cx']=0
            self.pop('ds')
            self.pop('di')
            self.pop('si')
        elif kind=='cfg_load':
            self.push(self.ds)
            self.push(0x166)
            self.service('open',0x15,4,(0x166,self.ds))
            self.push(self.ss)
            self.r['ax']=(self.r['bp']-8)&65535
            self.push(self.r['ax'])
            self.push(8)
            self.service('read',0x21,6,(8,self.r['ax'],self.ss))
            self.service('close',0x26)
            self.r['ax']=self.word(self.ss,self.r['bp']-3)
            self.store(address(self.ss,self.r['bp']-10),2,self.r['ax'])
            self.field(0x2466,self.r['ax'])
            self.field(0x2464,0)
            self.les()
            self.al(self.word(self.ss,self.r['bp']-8,1))
            self.store(address(self.r['es'],self.r['bx']+0x15),1,self.r['ax']&255)
            self.call('mode',0x45)
            self.field(0x90,0,1)
            active=self.dg(0x5DC,1)
            self.op(active,0,True,bits=8)
            if not active:
                self.les()
                self.store(address(self.r['es'],self.r['bx']+0x15),1,0)
                self.field(0x90,1,1)
            else:
                self.op(self.word(self.ss,self.r['bp']-8,1),0,True,bits=8)
                if not self.word(self.ss,self.r['bp']-8,1):
                    self.field(0x5DC,0,1)
            self.les()
            for local,offset in ((-7,0x16),(-6,0xB)):
                self.al(self.word(self.ss,self.r['bp']+local,1))
                self.store(address(self.r['es'],self.r['bx']+offset),1,self.r['ax']&255)
        elif kind=='cfg_exit':
            self.r['ax']=(self.r['bp']-8)&65535
            self.push(self.ss)
            self.push(self.r['ax'])
            self.push(self.ds)
            self.push(0x91)
            self.r['cx']=8
            self.call('copy',0xD8)
            self.push(self.ds)
            self.push(0x166)
            self.service('append',0xE1,4,(0x166,self.ds))
            self.push(0,4)
            self.push(0)
            self.service('seek',0xEB,6,(0,0,0))
            self.les()
            for local,offset in ((-8,0x15),(-7,0x16),(-6,0xB)):
                self.al(self.word(self.r['es'],self.r['bx']+offset,1))
                self.store(address(self.ss,self.r['bp']+local),1,self.r['ax']&255)
            self.push(self.ss)
            self.r['ax']=(self.r['bp']-8)&65535
            self.push(self.r['ax'])
            self.push(8)
            self.service('write',0x110,6,(8,self.r['ax'],self.ss))
            self.service('close',0x115)
        elif kind=='input':
            self.push(self.r['cs'])
            self.push(0xADE)
            self.sample('sense')
            present=self.dg(0x2CC)
            self.op(present,0,True)
            if present:
                self.frame(0xAEA,0)
                self.sample('js')
                self.r['ax']=self.dg(0x11B4)
                value=self.dg(0x1AA6)|self.r['ax']
                self.field(0x1AA6,value)
                self.logic(value)
            self.r['ax']=self.dg(0x1AA2)
            value=self.dg(0x1AA6)|self.r['ax']
            self.field(0x1AA6,value)
            self.logic(value)
        else:
            need(kind=='delay','known actual primitive')
            self.field(0x11E8,0)
            for value in (0,1):
                self.events.append(('tick',value))
                self.memory[address(self.ds,0x11E8):address(self.ds,0x11E8)+2]=value.to_bytes(2,'little')
                self.r['ax']=value
                self.op(value,self.word(self.ss,self.r['bp']+6),True)
        if kind in ('cfg_load','cfg_exit'):
            self.r['sp']=self.r['bp']
        self.pop('bp')
        if kind in ('cfg_load','cfg_exit'):
            self.r['sp']+=2
        else:
            self.returned(8 if kind=='copy' else 2 if kind=='delay' else 0)

    def sample(self,kind):
        mask=self.mask|0x600
        self.calls+=1
        self.events.append(('sample',kind,self.full(),self.flags&mask,mask,self.calls))
        sample=self.o['sample']
        values=((0x1AA6,sample[0]),(0x1AA2,sample[1]),(0x1AA4,sample[2]),(0x11B4,0)) if kind=='sense' else ((0x11B4,sample[3]),)
        for off,value in values:
            dest=address(self.ds,off)
            self.events.append(('sample-write',dest,value))
            self.memory[dest:dest+2]=value.to_bytes(2,'little')
        self.r,self.flags=reply(self.r,self.calls,self.o['seed'],self.flags,self.o['status'])
        self.mask=ARITH
        self.returned()
