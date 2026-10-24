"""Independent complete KAJA and duplicate delay bodies in their OP layout."""
import hashlib,json
from dataclasses import replace
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.shared_sound_runtime import Machine as CoreMachine,need
from lib.op_helpers_layout import SOUND_ENTRIES,SOUND_FIELDS
from lib.decoded_mainl_sound_runtime import cases as mainl_cases
class Machine(CoreMachine):
    def __init__(self,mz,load):
        super().__init__(mz,load,'op')
        # Replace only the explicit entry/field profile before any guest executes.
        self.entries=SOUND_ENTRIES;self.fields=dict(self.fields,**SOUND_FIELDS);self.instructions={};self.owned=set()
        for start,size,*_ in self.entries.values():
            rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[start:start+size],start));need(sum(i.size for i in rows)==size,'complete OP helper instruction boundaries')
            self.instructions.update({i.address:i.size for i in rows});self.owned.update(range(start,start+size))
def cases():
    for kind,p in mainl_cases():
        if kind in ('kaja','frame_delay'):yield kind,p
def verify(target,candidate):
    observations=[]
    for mz in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(mz,load)
            try:
                trace=hashlib.sha256();counts={k:0 for k in SOUND_ENTRIES}
                for count,(kind,p) in enumerate(cases(),1):
                    row=m.run(kind,seed=0x1357 if count&1 else 0xECA8,stack=0x80 if count&1 else 0xFFF0,**p);counts[kind]+=1;trace.update(json.dumps(row,sort_keys=True).encode())
                need(m.covered==m.owned,'all 51 helper bytes execute')
                loads.append(dict(load_segment=load,cases=count,cases_by_function=counts,covered_owner_bytes=len(m.covered),maximum_observed_stack_depth=m.maximum_stack,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent OP helper target/candidate observations')
    return dict(images=2,functions=2,code_bytes=51,executed_owner_bytes=51,cases_per_image=sum(o['cases'] for o in observations[0]),exhaustive_BYTE_states=256,observations=observations[0],scope='actual KAJA and frame_delay_2; same external vsync_Count1, finite counter and bounded driver replies')
def negative_controls(target):
    controls=(('active-is-BYTE',3,b'\x80',b'\x81','kaja',{}),
        ('inactive-keeps-AX',8,b'\x74',b'\x75','kaja',dict(active=0)),
        ('argument-at-BP-plus-six',12,b'\x06',b'\x08','kaja',{}),
        ('MIDI-exactly-one',17,b'\x01',b'\x02','kaja',dict(midi=2)),
        ('PMD-vector',21,b'\x60',b'\x61','kaja',{}),
        ('MMD-vector',25,b'\x61',b'\x60','kaja',dict(midi=1)),
        ('KAJA-Pascal-pop',28,b'\x02',b'\x04','kaja',{}),
        ('same-Counter1-reset',5,b'\xE8\x11',b'\xEA\x11','frame_delay',{}),
        ('counter-reset-WORD',3,b'\xC7',b'\xC6','frame_delay',{}),
        ('counter-unsigned-bound',15,b'\x72',b'\x7C','frame_delay',dict(frames=0x8000,ticks=(0x7FFF,0x8000))),
        ('delay-Pascal-pop',19,b'\x02',b'\x04','frame_delay',{}))
    rejected=[]
    for name,at,old,new,kind,p in controls:
        at+=SOUND_ENTRIES[kind][0];raw=bytearray(target.program_image);need(raw[at:at+len(old)]==old,'literal OP helper anchor '+name);raw[at:at+len(new)]=new;m=None
        try:
            try:m=Machine(replace(target,program_image=bytes(raw)),0x3000);m.run(kind,**p)
            except ValueError:rejected.append(name)
            else:raise ValueError('OP helper sound mutation survived: '+name)
        finally:
            if m:m.close()
    return dict(count=len(rejected),rejected=rejected)
