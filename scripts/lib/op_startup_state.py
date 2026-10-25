"""Independent flat 16-bit state and real near/far frames for OP composition."""
import struct
from lib.op_option_runtime import REG,GPRS

ARITH=0x8D5


def need(value,message):
    if not value:
        raise ValueError('OP startup contract: '+str(message))


def address(segment,offset):
    return segment*16+(offset&65535)


def logical(value,bits=16):
    return (4 if (value&255).bit_count()%2==0 else 0)|(64 if not value else 0)|(128 if value&(1<<(bits-1)) else 0)


class State:
    def __init__(self,memory,registers,high,flags,options):
        self.memory=memory
        self.r=dict(registers)
        self.high=dict(high)
        self.flags,self.mask=flags,ARITH
        self.o=options
        self.events=[]
        self.ds,self.ss=registers['ds'],registers['ss']
        self.calls=0

    def full(self):
        return {name:self.high[name]|value if name in self.high else value for name,value in self.r.items()}

    def word(self,segment,offset,size=2):
        at=address(segment,offset)
        return int.from_bytes(self.memory[at:at+size],'little')

    def dg(self,offset,size=2):
        return self.word(self.ds,offset,size)

    def store(self,at,size,value):
        value&=(1<<(size*8))-1
        self.events.append(('store',at,size,value))
        self.memory[at:at+size]=value.to_bytes(size,'little')

    def field(self,offset,value,size=2):
        self.store(address(self.ds,offset),size,value)

    def push(self,value,size=2):
        self.r['sp']-=size
        self.store(address(self.ss,self.r['sp']),size,value)

    def pop(self,name):
        self.r[name]=self.word(self.ss,self.r['sp'])
        self.r['sp']+=2

    def enter(self,locals=0):
        self.push(self.r['bp'])
        self.r['bp']=self.r['sp']
        self.r['sp']-=locals

    def frame(self,continuation,segment):
        self.r['sp']-=4
        at=address(self.ss,self.r['sp'])
        self.memory[at:at+4]=struct.pack('<HH',continuation,self.r['cs'])
        self.events.append(('far-frame',at,continuation,self.r['cs']))
        self.r['cs']=self.o['load']+segment

    def returned(self,cleanup=0):
        self.r['cs']=self.word(self.ss,self.r['sp']+2)
        self.r['sp']+=4+cleanup

    def op(self,left,right,subtract=False,bits=16):
        mask=(1<<bits)-1
        result=(left-right if subtract else left+right)&mask
        carry=left<right if subtract else left+right>mask
        overflow=((left^right)&(left^result) if subtract else ~(left^right)&(left^result))&(1<<(bits-1))
        self.flags=(self.flags&0x600)|2|logical(result,bits)|int(carry)|(16 if (left^right^result)&16 else 0)|(0x800 if overflow else 0)
        self.mask=ARITH
        return result

    def logic(self,value,bits=16):
        self.flags=(self.flags&0x600)|2|logical(value,bits)
        self.mask=0x8C5

    def al(self,value):
        self.r['ax']=(self.r['ax']&0xFF00)|(value&255)

    def entry(self,name,size):
        at=address(self.ss,self.r['sp'])
        mask=self.mask|0x600
        self.events.append(('entry',name,self.full(),bytes(self.memory[at:at+size]).hex(),self.flags&mask,mask))

    def done(self,name):
        mask=self.mask|0x600
        self.events.append(('owned-return',name,self.full(),self.flags&mask,mask))

    def les(self):
        value=self.dg(0x2464,4)
        self.r['bx'],self.r['es']=value&65535,value>>16
