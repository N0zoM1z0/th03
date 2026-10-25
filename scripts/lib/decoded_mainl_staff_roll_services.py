"""Source-level sound/input children with real frames for the staff-roll proof.

Device, DOS, palette and sampling replies are explicit bounded interfaces. This
module grants no ownership to the called scanner, driver or library bodies.
"""
from lib.decoded_mainl_snow_runtime import Spec as State
from lib.decoded_mainl_pi_free_runtime import address
from lib.decoded_mainl_pi_runtime import ARITH,signed


def need(value,message):
    if not value:
        raise ValueError('MAINL roll service contract: '+str(message))


def sound_reply(kind,regs,flags,options):
    out=dict(regs)
    writes=[]
    if kind=='buffer':
        out.update(ds=0x5000,dx=0x200)
    elif kind=='open':
        out['ax']=5
    elif kind=='read':
        count=options['song_bytes']
        raw=bytes((i*29+31)&255 for i in range(count))
        writes.append((address(regs['ds'],regs['dx']),raw))
        out['ax']=count
    elif kind=='close':
        out['ax']=0
    else:
        need(kind=='kaja','known sound interrupt reply')
        out['ax']=0xFFFF
    return out,(flags&0x600)|2|0x95,writes


class SoundSpec(State):
    def interrupt(self,kind,number):
        mask=self.mask|0x600
        self.events.append(('sound-interrupt',kind,number,self.full(),self.flags&mask,mask))
        self.r,self.flags,writes=sound_reply(kind,self.r,self.flags,self.o)
        for at,raw in writes:
            self.events.append(('song-bytes',at,raw.hex()))
            self.memory[at:at+len(raw)]=raw
        self.mask=ARITH

    def run(self,kind):
        self.enter()
        if kind=='kaja':
            active=self.dg(0x880,1)
            self.op(active,0,True,bits=8)
            if active:
                self.r['ax']=self.word(self.ss,self.r['bp']+6)
                midi=self.dg(0x1C71,1)
                self.op(midi,1,True,bits=8)
                self.interrupt('kaja',0x61 if midi==1 else 0x60)
        elif kind=='delay':
            self.field(0x144E,0)
            index=0
            while True:
                value=self.o['delay_ticks'][min(index,len(self.o['delay_ticks'])-1)]
                self.memory[address(self.ds,0x144E):address(self.ds,0x144E)+2]=value.to_bytes(2,'little')
                self.events.append(('delay-poll',value))
                index+=1
                self.r['ax']=value
                frames=self.word(self.ss,self.r['bp']+6)
                self.op(value,frames,True)
                if value>=frames:
                    break
        else:
            need(kind=='load','complete owned sound child')
            self.push(self.r['si'])
            self.push(self.ds)
            self.r['cx']=13
            self.r['si']=0
            self.logical(0)
            for i in range(13):
                self.r['bx']=self.word(self.ss,self.r['bp']+6)
                self.r['es']=self.word(self.ss,self.r['bp']+8)
                self.r['bx']=self.op(self.r['bx'],self.r['si'])
                value=self.memory[address(self.r['es'],self.r['bx'])]
                self.r['ax']=(self.r['ax']&0xFF00)|value
                self.field(0x1C74+self.r['si'],value,1)
                carry=self.flags&1
                self.r['si']=self.op(self.r['si'],1)
                self.flags=(self.flags&~1)|carry
                self.r['cx']=(self.r['cx']-1)&65535
            function=self.word(self.ss,self.r['bp']+10)
            self.r['ax']=function
            self.op(function,0x600,True)
            if function==0x600:
                midi=self.dg(0x1C71,1)
                self.op(midi,0,True,bits=8)
                if midi:
                    self.r['bx']=0
                    self.logical(0)
                    while True:
                        carry=self.flags&1
                        self.r['bx']=self.op(self.r['bx'],1)
                        self.flags=(self.flags&~1)|carry
                        byte=self.dg((0x1C74+self.r['bx'])&65535,1)
                        self.op(byte,0,True,bits=8)
                        if not byte:
                            break
                    for delta,value in enumerate(b'md\0'):
                        self.field((0x1C74+self.r['bx']+delta)&65535,value,1)
            self.r.update(dx=0x1C74,ax=0x3D00)
            self.interrupt('open',0x21)
            self.r['bx']=self.r['ax']
            self.r['ax']=self.word(self.ss,self.r['bp']+10)
            self.op(self.r['ax'],0x600,True)
            midi=0
            if self.r['ax']==0x600:
                midi=self.dg(0x1C71,1)
                self.op(midi,0,True,bits=8)
            self.interrupt('buffer',0x61 if midi else 0x60)
            self.r.update(ax=0x3F00,cx=0x5000)
            self.interrupt('read',0x21)
            self.pop('ds')
            self.r['ax']=(self.r['ax']&255)|0x3E00
            self.interrupt('close',0x21)
            self.pop('si')
        self.pop('bp')
        self.returned(0 if kind=='load' else 2)


INPUT=dict(presence=0x570,joystick=0x141A,player1=0x1D08,player2=0x1D0A,single=0x1D0C)


def sample_reply(kind,regs,flags,options):
    out=dict(regs)
    seed=options['sample_seed']
    for j,name in enumerate(('ax','cx','dx','es')):
        out[name]=(seed^(0x1234+j*0x231))&65535
    return out,(flags&0x600)|2|0x95


class InputSpec(State):
    def service(self,kind,continuation,bridge=False):
        if bridge:
            self.push(self.r['cs'])
            self.push(continuation)
        else:
            self.frame(continuation)
        mask=self.mask|0x600
        self.events.append(('sample',kind,self.full(),self.flags&mask,mask))
        values=dict(zip(('single','player1','player2','joystick'),self.o['sample'])) if kind=='sense' else dict(joystick=self.o['sample'][3])
        if kind=='sense':
            values['joystick']=0
        for name,value in values.items():
            at=address(self.ds,INPUT[name])
            self.events.append(('sample-write',at,value))
            self.memory[at:at+2]=value.to_bytes(2,'little')
        self.r,self.flags=sample_reply(kind,self.r,self.flags,self.o)
        self.mask=ARITH
        self.returned(0)

    def run(self):
        self.enter()
        self.service('sense',0xDCA,bridge=True)
        present=self.dg(INPUT['presence'])
        self.op(present,0,True)
        if present:
            self.service('js',0xDD6)
            self.r['ax']=self.dg(INPUT['joystick'])
            value=self.dg(INPUT['single'])|self.r['ax']
            self.field(INPUT['single'],value)
            self.logical(value)
        self.r['ax']=self.dg(INPUT['player1'])
        value=self.dg(INPUT['single'])|self.r['ax']
        self.field(INPUT['single'],value)
        self.logical(value)
        self.pop('bp')
        self.returned(0)
