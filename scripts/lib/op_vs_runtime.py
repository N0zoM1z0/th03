"""VS caller contracts with real owned helpers and a bounded selection boundary.

Character-selection procedures and graphics/device/file/exec services are
explicit external interfaces. Their implementations receive no credit here.
The real renderer, box transition, input interface, counter wait, cfg save,
KAJA and cleanup instructions execute. No physical timing or pixels are inferred.
"""
import hashlib
import json
import struct
from lib.op_nested_context import configure
from types import SimpleNamespace

from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import UcError
from unicorn.x86_const import UC_X86_REG_EFLAGS
from lib.op_dispatch_runtime import Machine as Base,REG,GPRS,add_flags
from lib.op_vs_layout import START,SIZE,BOX,BOX_SIZE
from lib.op_cfg_runtime import Prediction as CfgPrediction,RESIDENT,ACTIVE,MIDI,reply
from lib.op_render_runtime import Prediction as RenderPrediction
from lib.shared_input_runtime import Prediction as InputPrediction,service_reply,cmp16
from lib.shared_input_layout import PROFILES
from lib.shared_sound_runtime import Prediction as SoundPrediction
from lib.op_sound_layout import ENTRIES as SOUND_ENTRIES,RUNTIME_FIELDS as SOUND_FIELDS
from lib.op_exit_runtime import specification as exit_events,SERVICES as EXIT_SERVICES

P = PROFILES['op']
INPUT = P['code_segment']*16+P['start']
DELAY = SOUND_ENTRIES['frame_delay'][0]
RENDER,CFG,KAJA,EXIT = 0x9B9D,0x9980,0xC403,0xBFC2
HELPERS = ((RENDER,66),(INPUT,36),(DELAY,21),(CFG,67),(KAJA,30),(EXIT,67),(BOX,BOX_SIZE))
INPUT_SERVICES = {P['code_segment']*16+P['sense']:'sense',P['js']:'js'}
ROOT_LIBRARIES = {0x21F4:('text_clear',0,4),0xB10A:('unput',2,2),0x28D8:('super',6,4),
                  0xF1A:('gaiji_restore',0,4),0x9119:('execl',12,4)}
FILE_SERVICES = {0x7C8:('append',4),0x9E4:('seek',6),0xA26:('write',6),0x888:('close',0)}
SELECTION = {0xBA88:'players',0xBC1F:'cpu'}


def need(value,message):
    if not value:
        raise ValueError('OP VS contract: '+str(message))


def word(memory,at):
    return int.from_bytes(memory[at:at+2],'little')


class Machine(Base):
    def __init__(self,mz,load):
        super().__init__(mz,load)
        self.load = load
        self.instructions = {}
        self.owned = set(range(START,START+SIZE))
        self.nested = set()
        for start,size in ((START,SIZE),*HELPERS):
            rows = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[start:start+size],start))
            need(sum(i.size for i in rows) == size,'complete root/helper instruction boundaries')
            self.instructions.update({i.address:i.size for i in rows})
            if start != START:
                self.nested.update(range(start,start+size))

    def registers(self):
        return {n:self.r(n) for n in (*GPRS,'cs','ds','es','ss')}

    def outside_stack(self,expected):
        actual = bytes(self.uc.mem_read(0,1<<20))
        lo,hi = 0x70000+self.stack-80,0x70000+self.stack
        expected[lo:hi] = actual[lo:hi]
        need(actual == expected,'whole memory outside 80 private stack bytes, including caller words')

    def root_event(self,event):
        need(self.root_index < len(self.plan) and self.plan[self.root_index] == event,
             f'root event {self.root_index}: {event}; expected {self.plan[self.root_index:self.root_index+1]}')
        self.root_index += 1

    def event(self,event):
        if self.active is None:
            self.root_event(event)
            if event[0] == 'store':
                self.shadow[event[1]:event[1]+event[2]] = event[3].to_bytes(event[2],'little')
        else:
            h = self.active
            need(h.index < len(h.events) and h.events[h.index] == event,
                 f'{h.name} event {h.index}: {event}; expected {h.events[h.index:h.index+1]}')
            h.index += 1

    def begin(self,name):
        expected = self.plan[self.root_index]
        need(expected[0] == name,'real helper called in root order')
        self.root_event(expected)
        self.outside_stack(self.shadow)
        regs,sp = self.registers(),self.r('sp')
        flags = self.uc.reg_read(UC_X86_REG_EFLAGS)
        h = SimpleNamespace(name=name,sp=sp,index=0,if_df=flags&0x600,
            return_rva=self.cs*16+word(self.shadow,0x70000+sp)-self.base)
        h.full = {n:self.uc.reg_read(GPRS[n]) for n in GPRS}
        if name == 'input':
            need(self.poll < len(self.samples),'finite device sample stream')
            h.sample = self.samples[self.poll];self.poll += 1
            e = InputPrediction(self.shadow,regs,'op',self.data,self.seed,flags,[h.sample],self.present,0)
            e.run('input_mode_interface')
            h.events = [('store',*v[1:]) if v[0] == 'write' else ('device',*v[1:]) for v in e.events]
            h.regs,h.mask,h.flags,h.memory = e.regs,e.flags_mask,e.flags_value,e.memory
            h.delta,h.service_index = 4,0
        elif name == 'delay':
            need(word(self.shadow,0x70000+sp+4) == 1,'real far Pascal delay argument one')
            e = SoundPrediction(self.shadow,regs,self.data,sp,dict(flags=flags,ticks=(0,1)),SOUND_FIELDS)
            e.frame_delay(1)
            h.events = [('store',v['address'],v['size'],v['value']) if v['kind'] == 'store' else ('tick',v['value']) for v in e.events]
            h.regs,h.mask,h.flags,h.memory,h.delta = e.regs,0x8D5,e.flags,e.memory,6
            self.delay_calls += 1
        elif name == 'render':
            attr,selection = struct.unpack('<HH',bytes(self.uc.mem_read(0x70000+sp+2,4)))
            need((selection,attr) == expected[1:],'near Pascal renderer arguments')
            e = RenderPrediction(regs,dict(selection=selection,attribute=attr,stack=sp,seed=self.seed,
                status=self.status,flags=flags),self.ds,self.load).run('vs')
            h.events = [('gaiji',v) for v in e.events]
            h.regs,h.mask,h.flags,h.memory,h.delta = e.regs,e.mask,e.flags,bytearray(self.shadow),6
            self.renderer_calls += 1
        elif name == 'cfg':
            e = CfgPrediction(self.shadow,regs,self.data,sp,'cfg_save',bytes(self.file),0,
                self.resoff,self.resseg,0,0,self.seed,flags,self.status)
            e.run()
            h.events = [('file',*v[1:]) for v in e.events]
            h.regs,h.mask,h.flags,h.memory,h.delta,h.file = e.regs,0x8D5,e.flags_value,e.memory,2,e.file
        elif name == 'kaja':
            need(word(self.shadow,0x70000+sp+4) == 0x100,'actual song-stop argument')
            fields = dict(SOUND_FIELDS,active=ACTIVE,midi_active=MIDI)
            e = SoundPrediction(self.shadow,regs,self.data,sp,dict(flags=flags,argument=0x100,
                seed=self.seed,driver_ax=self.status),fields)
            e.run('kaja')
            h.events = [('interrupt',v) for v in e.events]
            h.regs,h.mask,h.flags,h.memory,h.delta = e.regs,0x8D5,e.flags,e.memory,6
        else:
            need(name == 'exit','known maintained helper')
            h.events = [('out',*v[1:]) if v[0] == 'out' else ('cleanup',v[0],None) for v in exit_events('exit')]
            h.regs,h.flags = reply(regs,8,self.seed,flags,self.status)
            h.mask,h.memory,h.delta,h.calls = 0x8D5,bytearray(self.shadow),4,0
        h.regs['cs'] = self.cs
        h.full = {n:(h.full[n]&0xFFFF0000)|h.regs[n] for n in GPRS}
        self.active = h

    def finish(self):
        h = self.active
        need(self.r('sp') == h.sp+h.delta and self.registers() == h.regs,'complete '+h.name+' return ABI')
        need(all(self.uc.reg_read(GPRS[n]) == h.full[n] for n in GPRS),'complete '+h.name+' DWORD effects')
        flags = self.uc.reg_read(UC_X86_REG_EFLAGS)
        need(flags&h.mask == h.flags&h.mask and flags&0x600 == h.if_df,'defined '+h.name+' flags / IF / DF')
        need(h.index == len(h.events),'complete '+h.name+' events')
        self.outside_stack(h.memory)
        if h.name == 'cfg':
            need(self.file == h.file,'actual four-byte cfg transaction, including the incoming stack byte')
        self.helper_trace.update(json.dumps((h.name,h.events),sort_keys=True).encode())
        self.shadow,self.active = h.memory,None
        self.helper_calls += 1

    def frame(self,args,far=True):
        sp = self.r('sp');frame = 4 if far else 2
        ip = word(bytes(self.uc.mem_read(0x70000+sp,2)),0)
        cs = word(bytes(self.uc.mem_read(0x70000+sp+2,2)),0) if far else self.cs
        need(cs*16+ip-self.base in self.instructions,'real service frame returns to maintained code')
        payload = tuple(struct.unpack('<'+'H'*(args//2),bytes(self.uc.mem_read(0x70000+sp+frame,args))))
        return sp,ip,cs,payload

    def leave_service(self,sp,ip,cs,args,far=True):
        self.uc.reg_write(REG['sp'],sp+(4 if far else 2)+args)
        self.uc.reg_write(REG['cs'],cs);self.uc.reg_write(REG['ip'],ip)

    def respond(self,index,status=None):
        regs,flags = reply(self.registers(),index,self.seed,self.uc.reg_read(UC_X86_REG_EFLAGS),
                         self.status if status is None else status)
        for n in ('ax','bx','cx','dx','es'):
            self.uc.reg_write(REG[n],regs[n])
        self.uc.reg_write(UC_X86_REG_EFLAGS,flags)

    def code(self,uc,address,size,_):
        try:
            rva = address-self.base
            if self.active and rva == self.active.return_rva:
                self.finish()
            if self.box_return is not None and rva == self.box_return:
                need(self.r('si') == 0 and self.r('bp') == self.stack-2 and self.r('di') == self.initial_regs['di'],
                     'real box transition restores caller SI/BP/DI')
                f = uc.reg_read(UC_X86_REG_EFLAGS)
                need(f&0x8D5 == cmp16(392,392),'box transition final column comparison')
                self.box_return = None
            if address == getattr(self,'boundary_return',self.cs*16+0xFFFF):
                self.returned = True;uc.emu_stop();return
            entries = {INPUT:'input',DELAY:'delay',RENDER:'render',CFG:'cfg',KAJA:'kaja',EXIT:'exit'}
            if rva in entries:
                need(self.active is None,'bounded helper nesting')
                self.begin(entries[rva])
            if rva == BOX:
                self.root_event(('box',))
                self.box_return = self.cs*16+word(bytes(uc.mem_read(0x70000+self.r('sp'),2)),0)-self.base
            if rva == DELAY+9:
                h = self.active;need(h and h.name == 'delay','counter read inside actual delay')
                e = h.events[h.index];need(e[0] == 'tick','finite ordered counter update')
                self.event(e);uc.mem_write(self.data+SOUND_FIELDS['counter'],e[1].to_bytes(2,'little'))
                self.counter_updates += 1
            if rva in INPUT_SERVICES:
                h = self.active;need(h and h.name == 'input','device sampling inside actual input interface')
                sp,ip,cs,args = self.frame(0)
                kind = INPUT_SERVICES[rva]
                post = dict(single=h.sample[0],player1=h.sample[1],player2=h.sample[2],joystick=0) if kind == 'sense' else dict(joystick=h.sample[3])
                self.event(('device',kind,post,None))
                for field,value in post.items():uc.mem_write(self.data+P[field],struct.pack('<H',value))
                h.service_index += 1
                regs,flags = service_reply(self.registers(),h.service_index,self.seed,uc.reg_read(UC_X86_REG_EFLAGS))
                for n in ('ax','cx','dx','es'):uc.reg_write(REG[n],regs[n])
                uc.reg_write(UC_X86_REG_EFLAGS,flags);self.leave_service(sp,ip,cs,0);return
            if rva == 0xFCC:
                h = self.active;need(h and h.name == 'render','gaiji call inside real VS renderer')
                e = h.events[h.index][1]
                sp,ip,cs,args = self.frame(10)
                need(args == e['arguments'] and self.registers() == e['request'],'complete renderer request ABI')
                f = uc.reg_read(UC_X86_REG_EFLAGS);need(f&e['flags_mask'] == e['flags_value'],'renderer request flags')
                _,off,seg,_,_ = args;raw = bytes.fromhex(e['string_hex'])
                need(bytes(uc.mem_read(seg*16+off,len(raw))) == raw,'complete actual gaiji string including NUL')
                self.event(('gaiji',e))
                for n in ('ax','bx','cx','dx','es'):uc.reg_write(REG[n],e['post'][n])
                uc.reg_write(UC_X86_REG_EFLAGS,e['post_flags']);self.leave_service(sp,ip,cs,10);return
            if self.active and self.active.name == 'cfg' and rva in FILE_SERVICES:
                name,n = FILE_SERVICES[rva];sp,ip,cs,args = self.frame(n)
                payload = None
                if name == 'append':
                    off,seg = args;need((off,seg) == (0x166,self.ds),'cfg filename pointer')
                    payload = bytes(uc.mem_read(seg*16+off,9)).hex()
                elif name == 'seek':payload = (args[1]|args[2]<<16,args[0])
                elif name == 'write':
                    count,off,seg = args;raw = bytes(uc.mem_read(seg*16+off,count))
                    payload = (seg,off,count,raw.hex());self.file[:count] = raw
                self.event(('file',name,payload));self.respond(self.active.index)
                self.leave_service(sp,ip,cs,n);return
            if self.active and self.active.name == 'exit' and rva in EXIT_SERVICES:
                sp,ip,cs,args = self.frame(0);h = self.active
                self.event(('cleanup',EXIT_SERVICES[rva],None));h.calls += 1
                self.respond(h.calls);self.leave_service(sp,ip,cs,0);return
            if rva in SELECTION:
                need(self.active is None,'selection is an unowned product boundary')
                kind = SELECTION[rva];self.root_event(('selection',kind))
                sp,ip,cs,args = self.frame(0,False)
                need(self.r('ax')&255 == self.selected_mode and self.r('bx') == self.resoff and self.r('es') == self.resseg,
                     'selection request observes the configured resident mode')
                need(self.r('bp') == self.stack-2 and self.r('si') == self.expected_previous,'selection preserves the caller frame')
                f = uc.reg_read(UC_X86_REG_EFLAGS);need(f&0x8D5 == cmp16(self.selected,1),'selection dispatch comparison')
                for off,raw in self.selection_transfers:
                    uc.mem_write(self.resbase+off,raw);self.shadow[self.resbase+off:self.resbase+off+len(raw)] = raw
                self.root_calls += 1;self.respond(self.root_calls,self.selection_ax)
                self.leave_service(sp,ip,cs,0,False);return
            if rva in ROOT_LIBRARIES:
                need(self.active is None,'root/box library boundary')
                name,n,frame = ROOT_LIBRARIES[rva];sp,ip,cs,args = self.frame(n,frame == 4)
                if name == 'execl':
                    need(args == (0x16F,self.ds,0x16F,self.ds,0,0),'all six far-cdecl exec argument WORDs')
                    need(bytes(uc.mem_read(self.data+0x16F,6)) == b'mainl\0','actual MAINL name bytes')
                    cleanup = 0
                else:cleanup = n
                self.root_event(('library',name,args))
                self.root_calls += 1;self.respond(self.root_calls)
                self.leave_service(sp,ip,cs,cleanup,frame == 4);return
            need(self.instructions.get(rva) == size,'only complete root/real-helper instructions')
            self.covered.update(set(range(rva,rva+size))&self.owned)
            self.nested_covered.update(set(range(rva,rva+size))&self.nested)
            self.maximum_stack = max(self.maximum_stack,self.stack-self.r('sp'))
        except Exception as error:self.fail(error)

    def write(self,uc,access,address,size,value,_):
        try:
            if 0x70000+self.stack-80 <= address and address+size <= 0x70000+self.stack:
                self.maximum_stack = max(self.maximum_stack,0x70000+self.stack-address);return
            self.event(('store',address,size,value))
        except Exception as error:self.fail(error)

    def out(self,uc,port,size,value,_):
        try:
            need(self.active and self.active.name == 'exit' and size == 1,'BYTE cleanup port boundary')
            self.event(('out',port,value))
        except Exception as error:self.fail(error)

    def interrupt(self,uc,vector,_):
        try:
            h = self.active;need(h and h.name == 'kaja','interrupt only inside actual KAJA helper')
            e = h.events[h.index][1]
            need(vector == e['vector'] and self.registers() == e['request'],'complete KAJA driver request')
            self.event(('interrupt',e))
            for n in ('ax','bx','cx','dx','es'):uc.reg_write(REG[n],e['post'][n])
            uc.reg_write(UC_X86_REG_EFLAGS,e['flags'])
        except Exception as error:self.fail(error)

    def run(self,*,mode=0,samples=((0x20,0,0,0),),present=0,selection_ax=1,active=1,midi=0,
            seed=0x1357,status=0xFFFF,flags=0x202,stack=0xF800,resseg=0x6000,resoff=0x31,
            options=(0x81,0x52,0xA3),selection_patch=True,_context=None):
        configure(self,_context)
        if _context is not None:
            stack,flags=_context.stack,_context.flags;resoff,resseg,base=_context.resident(self)
            mode=_context.memory[base+0x28];active,midi=_context.memory[self.data+ACTIVE],_context.memory[self.data+MIDI]
            options=tuple(_context.memory[base+v] for v in (0x15,0x16,0xB))
            present=word(_context.memory,self.data+P['presence'])
        need(all(0 <= v <= 255 for v in (mode,active,midi,*options)) and 0 <= selection_ax <= 65535,
             'BYTE resident options/mode and WORD selection response')
        need(0 <= present <= 65535 and 0 <= seed <= 65535 and 0 <= status <= 65535,'WORD service domains')
        need(80 <= stack <= 0xFFF0 and resseg in (0x5000,0x6000) and 0 <= resoff <= 0xFF80,
             'disjoint resident and bounded private stack')
        if _context is None:
            self.uc.mem_write(0,bytes(self.initial))
            self.stack,self.seed,self.status = stack,seed,status
            self.resseg,self.resoff,self.resbase = resseg,resoff,resseg*16+resoff
            self.uc.mem_write(0x70000+stack-80,b'\xD3'*80)
            self.uc.mem_write(0x70000+stack,b'\xFF\xFF\x5A\xA5')
            self.uc.mem_write(self.data+RESIDENT,struct.pack('<HH',resoff,resseg))
            self.uc.mem_write(self.resbase,b'\xA5'*0x60)
            self.uc.mem_write(self.resbase+0x28,bytes((mode,)))
            for off,value in zip((0x15,0x16,0xB),options):
                self.uc.mem_write(self.resbase+off,bytes((value,)))
            self.uc.mem_write(self.data+ACTIVE,bytes((active,)))
            self.uc.mem_write(self.data+MIDI,bytes((midi,)))
            self.uc.mem_write(self.data+P['presence'],struct.pack('<H',present))
            self.uc.mem_write(self.data+P['single'],b'\xFF\xFF')
        self.stack,self.seed,self.status=stack,seed,status
        self.resseg,self.resoff,self.resbase=resseg,resoff,resseg*16+resoff
        self.file = bytearray(b'\x02\x01\x03\x48\x57\0\x50\xA7' if _context is None else _context.file)
        self.samples = list(samples)
        need(len(self.samples) <= 64 and all(len(s) == 4 and all(0 <= v <= 65535 for v in s) for s in self.samples),
             'finite WORD device samples')
        self.present,self.poll,self.selection_ax = present,0,selection_ax
        self.selection_transfers = [(0xC,b'\x85\xFE'),(0x10,struct.pack('<I',0xA7F01234)),
            (0x15,b'\xD2\x63'),(0xB,b'\xB4')] if selection_patch else []
        self.shadow = bytearray(self.uc.mem_read(0,1<<20))
        self.plan = []
        if mode < 128:
            self.plan += [('library','text_clear',()),('box',)]
            for x in range(288,392,8):
                self.plan += [('library','unput',(x,)),('library','super',(2,256,x)),('delay',)]
            selection,previous = 0,0
            self.plan += [('render',0,0xE1),('render',1,1),('render',2,1)]
            for index,sample in enumerate(self.samples):
                self.plan.append(('input',))
                value = sample[0]|sample[1]|(sample[3] if present else 0)
                if previous == 0:
                    if value&1:
                        self.plan.append(('render',selection,1));selection = (selection-1)%3
                        self.plan.append(('render',selection,0xE1))
                    if value&2:
                        self.plan.append(('render',selection,1));selection = (selection+1)%3
                        self.plan.append(('render',selection,0xE1))
                    if value&0x2020:
                        need(index == len(self.samples)-1,'sample stream stops at the first accepted confirm')
                        break
                previous = value
                self.plan.append(('delay',))
            else:
                raise ValueError('OP VS contract: stream must release held input and eventually confirm; CANCEL is not an exit')
            self.expected_previous = previous
        else:
            selection = mode-128
            self.expected_previous = 0
            need(not self.samples,'post-match entry does not poll or draw')
        self.selected,self.selected_mode = selection,128+selection
        def store(off,size,value):
            self.plan.append(('store',self.resbase+off,size,value))
        for off,value in ((0xE,int(selection == 2)),(0xF,int(selection != 1)),
                          (0x39,0),(0x17,0),(0x33,0),(0x28,self.selected_mode),(0x35,0)):
            store(off,1,value)
        self.plan.append(('selection','players' if selection == 1 else 'cpu'))
        self.cancelled = bool(selection_ax&255)
        if self.cancelled:
            store(0x28,1,0)
        else:
            for i in range(16):store(0x18+i,1,0)
            self.plan += [('cfg',),('library','gaiji_restore',()),('kaja',),('exit',),
                          ('library','execl',(0x16F,self.ds,0x16F,self.ds,0,0))]
        if _context is None:
            self.initial_regs = {n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)}
            self.high = {n:(seed^0x5AA5)<<16 for n in GPRS}
            for n in GPRS:self.uc.reg_write(GPRS[n],self.high[n]|self.initial_regs[n])
            self.initial_regs.update(cs=self.cs,ds=self.ds,es=seed,ss=0x7000)
            for n in ('cs','ds','es','ss'):self.uc.reg_write(REG[n],self.initial_regs[n])
            self.uc.reg_write(REG['sp'],stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        else:self.initial_regs,self.high=_context.initial()
        self.root_index,self.root_calls,self.helper_calls = 0,0,0
        self.renderer_calls,self.delay_calls,self.counter_updates = 0,0,0
        self.active,self.box_return,self.error,self.returned = None,None,None,False
        self.helper_trace = hashlib.sha256()
        try:
            self.uc.emu_start(self.base+START,0x100000,count=200000)
        except UcError as error:
            raise ValueError('OP VS contract: guest fault') from error
        need(self.error is None,self.error or 'guest error')
        need(self.returned and self.r('sp') == stack+2 and self.active is None and self.box_return is None,'near root return')
        need(self.root_index == len(self.plan) and self.poll == (len(self.samples) if mode < 128 else 0),'complete root/device plan')
        expected,_ = reply(self.initial_regs,self.root_calls,seed,flags,self.selection_ax if self.cancelled else status)
        expected['ax'] = (expected['ax']&0xFF00)|int(self.cancelled)
        if self.cancelled:expected.update(bx=resoff,es=resseg)
        need(self.registers() == expected,'independent final WORD/segment registers: '+str((self.registers(),expected)))
        need(all(self.uc.reg_read(GPRS[n]) == self.high[n]|expected[n] for n in GPRS),'returning DWORD high halves')
        f = self.uc.reg_read(UC_X86_REG_EFLAGS)
        mask,value = (0x8C5,((4 if (selection_ax&255).bit_count()%2 == 0 else 0)|
                     (128 if selection_ax&128 else 0))) if self.cancelled else (0x8D5,add_flags(stack-18,12))
        need(f&mask == value&mask and f&0x600 == flags&0x600,'final AL-test or cdecl cleanup flags / inherited IF / DF')
        self.outside_stack(self.shadow)
        if _context is not None:_context.accept(self,expected,self.high,mask,value,self.shadow,file=self.file)
        return dict(selection=selection,polled_samples=self.poll,cancelled=self.cancelled,
            registers=self.registers(),flags=f&(mask|0x600),flags_mask=mask,
            renderer_calls=self.renderer_calls,delay_calls=self.delay_calls,counter_updates=self.counter_updates,
            root_calls=self.root_calls,helper_calls=self.helper_calls,file_hex=self.file.hex(),
            plan_sha256=hashlib.sha256(json.dumps(self.plan).encode()).hexdigest(),helper_trace_sha256=self.helper_trace.hexdigest())


def cases():
    # Both ordinary-entry mode values and every unchecked post-match selection.
    for mode in range(256):
        yield dict(mode=mode,samples=() if mode >= 128 else ((0x20,0,0,0),),selection_ax=0 if mode&1 else 0xA501)
    # Only AL controls the character-selection result; AH is retained by bool returns.
    for value in range(256):
        yield dict(mode=128+value%128,samples=(),selection_ax=0xA500|value,status=(value<<8)|0x53)
    for value in sorted(set(range(256))|{i<<8 for i in range(256)}|{0x7FFF,0xFFFF}):
        stream = [(value,0,0,0)]
        if not value&0x2020:stream += [(0,0,0,0),(0x20,0,0,0)]
        yield dict(samples=stream,selection_ax=0 if value&1 else 1)
    for present in (0,1,0x8000,0xFFFF):
        for lane in range(4):
            for bit in range(16):
                sample = [0,0,0,0];sample[lane] = 1<<bit
                merged = sample[0]|sample[1]|(sample[3] if present else 0)
                stream = [tuple(sample)]
                if not merged&0x2020:stream += [(0,0,0,0),(0x2000,0,0,0)]
                yield dict(present=present,samples=stream,selection_ax=0 if bit&1 else 1)
    for value in range(256):
        yield dict(mode=129,samples=(),selection_ax=0,active=value,midi=1)
        yield dict(mode=130,samples=(),selection_ax=0,active=1,midi=value)
    for values in ((1,0,1,0,1,0,0x20),(2,0,2,0,2,0,0x2000),
                   (1,0x21,1,0,0x20),(0x4000,0x20,0,0x2000),(3,0,0x23),
                   (*([0]*63),0x20)):
        for response in (0,0x100,0xFFFF):
            yield dict(samples=[(v,0,0,0) for v in values],selection_ax=response)
    for segment in (0x5000,0x6000):
        for off in (0,0x31,0xFF80):
            for flags in (2,0x202,0x402,0xED7):
                for response in (0,0x100,0xFFFF):
                    yield dict(resseg=segment,resoff=off,flags=flags,selection_ax=response,
                               status=(0,0x7FFF,0x8000,0xFFFF)[flags%4])
    for response in (0,1,0x100,0x8000,0x80FF,0xFFFF):
        yield dict(selection_ax=response,selection_patch=False,options=(0,0xFF,0x80),status=0)


def verify(target,candidate):
    results = []
    for mz in (target,candidate):
        rows = []
        for load in (0x1000,0x3000):
            m = Machine(mz,load)
            trace,count,maximum_polls,maximum_delays = hashlib.sha256(),0,0,0
            ordinary = direct = 0
            try:
                for count,parameters in enumerate(cases(),1):
                    r = m.run(seed=0x1357 if count&1 else 0xECA8,stack=0x80 if count&1 else 0xFFF0,**parameters)
                    ordinary += parameters.get('mode',0) < 128
                    direct += parameters.get('mode',0) >= 128
                    maximum_polls = max(maximum_polls,r['polled_samples'])
                    maximum_delays = max(maximum_delays,r['delay_calls'])
                    trace.update(json.dumps(r,sort_keys=True).encode())
                need(m.covered == m.owned and m.nested_covered == m.nested,
                     'all 365 root and 331 real helper instruction bytes execute')
                rows.append(dict(load_segment=load,cases=count,ordinary_menu_cases=ordinary,post_match_cases=direct,
                    covered_owner_bytes=len(m.covered),executed_nested_bytes=len(m.nested_covered),
                    maximum_observed_stack_depth=m.maximum_stack,maximum_polls=maximum_polls,
                    maximum_actual_delay_calls=maximum_delays,trace_sha256=trace.hexdigest()))
            finally:m.close()
        results.append(rows)
    need(results[0] == results[1],'independent target/candidate VS observations agree')
    return dict(images=2,functions=1,code_bytes=365,executed_owner_bytes=365,executed_nested_bytes=331,
        cases_per_image=sum(r['cases'] for r in results[0]),observations=results[0],exhaustive_mode_bytes=256,
        exhaustive_selection_result_bytes=256,exhaustive_sound_state_bytes=256,
        character_selection_implementations_executed=False,physical_timing_or_pixels_emulated=False,
        scope='VS caller with real renderer/box/input/delay/cfg/KAJA/cleanup; bounded unowned character-selection replies/transfers and SDK/device/file/failed-exec interfaces')


def negative_controls(target):
    from dataclasses import replace
    controls = (
        ('previous-input-starts-empty',START+5,1,dict(samples=((0x21,0,0,0),))),
        ('mode-threshold-is-unsigned',0x9BEF,14,dict(mode=0x80,samples=())),
        ('new-menu-selection-zero',0x9BFE,1,{}),
        ('held-input-debounce',0x9C22,1,dict(samples=((1,0,0,0),(0x21,0,0,0),(0,0,0,0),(0x20,0,0,0)))),
        ('up-mask',0x9C28,2,dict(samples=((0x22,0,0,0),))),
        ('up-wrap',0x9C3F,1,dict(samples=((0x21,0,0,0),))),
        ('down-mask',0x9C4E,2,dict(samples=((0x22,0,0,0),))),
        ('down-wrap',0x9C65,1,dict(samples=((2,0,0,0),(0,0,0,0),(2,0,0,0),(0,0,0,0),(0x22,0,0,0)))),
        ('shot-mask',0x9C74,0x20,{}),
        ('OK-high-byte-mask',0x9C7B,0x20,dict(samples=((0x2000,0,0,0),))),
        ('previous-input-is-WORD',0x9C7E,1,dict(samples=((0x8000,0,0,0),(0x20,0,0,0),(0,0,0,0),(0x20,0,0,0)))),
        ('poll-delay-one',0x9C83,1,dict(samples=((0,0,0,0),(0x20,0,0,0)))),
        ('CPU-left-equality',0x9C9E,1,dict(mode=130,samples=())),
        ('CPU-right-equality',0x9CB2,1,dict(mode=129,samples=())),
        ('clear-demo-byte',0x9CC7,1,dict(mode=129,samples=())),
        ('mode-add-128',0x9CD6,1,dict(mode=129,samples=())),
        ('selection-kind-branch',0x9CE4,1,dict(mode=129,samples=())),
        ('selection-tests-AL-only',0x9CE9,1,dict(mode=129,samples=(),selection_ax=0x100)),
        ('cancel-clears-mode',0x9CFE,1,dict(mode=129,samples=())),
        ('cancel-returns-true',0x9D00,1,dict(mode=129,samples=())),
        ('score-loop-count-16',0x9D1C,1,dict(mode=129,samples=(),selection_ax=0)),
        ('score-store-BYTE',0x9D15,1,dict(mode=129,samples=(),selection_ax=0)),
        ('stop-song-argument',0x9D28,1,dict(mode=129,samples=(),selection_ax=0)),
        ('exec-argument-cdecl-cleanup',0x9D46,2,dict(mode=129,samples=(),selection_ax=0)),
        ('failed-exec-returns-false',0x9D48,1,dict(mode=129,samples=(),selection_ax=0)),
        ('root-near-return',0x9D4B,8,dict(mode=129,samples=())),
        ('real-box-step-eight',BOX+34,8,{}),
        ('real-renderer-y',RENDER+20,1,{}),
        ('real-input-merges-player-one',INPUT+30,0x80,dict(samples=((0,0x20,0,0),))),
        ('real-delay-unsigned-limit',DELAY+15,5,{}),
        ('real-cfg-writes-four',CFG+54,1,dict(mode=129,samples=(),selection_ax=0)),
    )
    rejected = []
    for name,address,xor,parameters in controls:
        changed = bytearray(target.program_image);changed[address] ^= xor
        m = Machine(replace(target,program_image=bytes(changed)),0x1000)
        try:
            m.run(**parameters)
        except (ValueError,UcError):rejected.append(name)
        else:raise ValueError('actual VS instruction mutation escaped: '+name)
        finally:m.close()
    return dict(count=len(rejected),rejected=rejected,actual_guest_mutations=True,
                character_selection_code_mutated=False,payload_bytes_patched=False)
