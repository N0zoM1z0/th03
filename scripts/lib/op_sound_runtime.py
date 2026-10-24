"""OP-specific load/delay domains over the independent shared sound core."""
import hashlib,json
from dataclasses import replace
from lib.shared_sound_runtime import Machine as CoreMachine,need
from lib.decoded_mainl_sound_runtime import cases as mainl_cases

class Machine(CoreMachine):
    def __init__(self,mz,load):super().__init__(mz,load,'op')
def cases():
    for kind,params in mainl_cases():
        if kind in ('load','frame_delay'):yield kind,params
def verify(target,candidate):
    observations=[]
    for mz in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(mz,load)
            try:
                trace=hashlib.sha256();counts={'load':0,'frame_delay':0}
                for count,(kind,options) in enumerate(cases(),1):
                    row=m.run(kind,seed=0x1357 if count&1 else 0xECA8,stack=0x80 if count&1 else 0xFFF0,**options)
                    counts[kind]+=1;trace.update(json.dumps(row,sort_keys=True).encode())
                need(m.covered==m.owned,'all 133 OP load/delay bytes execute')
                loads.append(dict(load_segment=load,cases=count,cases_by_function=counts,covered_owner_bytes=len(m.covered),maximum_observed_stack_depth=m.maximum_stack,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent OP target/candidate load/delay observations')
    return dict(images=2,functions=2,code_bytes=133,executed_owner_bytes=133,cases_per_image=sum(o['cases'] for o in observations[0]),
        filename_copy_bytes=13,file_read_request_bytes=0x5000,exhaustive_MIDI_bytes=256,observations=observations[0],
        scope='actual OP load/delay bodies; bounded DOS/PMD/MMD and finite WORD-counter replies; no physical I/O or elapsed-time claim')
def negative_controls(target):
    controls=(
        ('load-thirteen-byte-copy',6,b'\x0D',b'\x0C','load',{}),
        ('load-far-filename',12,b'\x06',b'\x08','load',{}),
        ('MIDI-only-song-function',30,b'\x06',b'\x0B','load',dict(midi=1)),
        ('suffix-skips-first-byte',42,b'\x43',b'\x90','load',dict(midi=1)),
        ('literal-md-suffix',54,b'\x6D',b'\x6E','load',dict(midi=1)),
        ('nonzero-MIDI-route',90,b'\xCD\x61',b'\xCD\x60','load',dict(midi=2)),
        ('failed-open-handle',74,b'\xD8',b'\xC3','load',dict(open_failure=True,open_result=5)),
        ('read-request-5000h',101,b'\x50',b'\x40','load',{}),
        ('DS-before-close',104,b'\x1F',b'\x90','load',{}),
        ('read-AL-in-close-request',105,b'\xB4',b'\xB0','load',{}),
        ('load-cdecl-return',111,b'\xCB',b'\xCA','load',{}),
        ('counter-WORD-reset',3,b'\xC7',b'\xC6','frame_delay',{}),
        ('counter-unsigned-bound',15,b'\x72',b'\x7C','frame_delay',dict(frames=0x8000,ticks=(0x7FFF,0x8000))),
        ('delay-Pascal-pop',19,b'\x02',b'\x04','frame_delay',{}))
    rejected=[]
    for name,offset,old,new,kind,p in controls:
        start=0xBF52 if kind=='load' else 0xC19E;at=start+offset;raw=bytearray(target.program_image)
        need(raw[at:at+len(old)]==old,'OP literal mutation anchor '+name);raw[at:at+len(new)]=new;m=None
        try:
            try:m=Machine(replace(target,program_image=bytes(raw)),0x3000);m.run(kind,**p)
            except ValueError:rejected.append(name)
            else:raise ValueError('OP sound mutation survived: '+name)
        finally:
            if m:m.close()
    return dict(count=len(rejected),rejected=rejected)
