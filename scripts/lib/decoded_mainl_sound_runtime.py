"""MAINL sound/timing state domains and mutations over the shared execution core."""
import hashlib,json
from dataclasses import replace
from lib.shared_sound_runtime import Machine,ENTRIES,F,need

def cases():
    for current in range(256):
        for new in range(33):yield 'play',dict(playing=current,argument=new,frame=0xA5)
    for current in range(33):
        for frame in range(256):yield 'update',dict(playing=current,frame=frame)
    for current in range(33,256):
        for frame in (0,1,254,255):yield 'update',dict(playing=current,frame=frame)
    for v in range(256):
        yield 'kaja',dict(active=v,midi=v)
        yield 'kaja',dict(active=1,midi=v)
        yield 'measure',dict(active=1,midi=v,measure=0x8000,measures=(0x7FFF,0x8000))
        yield 'measure',dict(active=v,midi=1,measure=0,measures=(0xFFFF,))
        yield 'load',dict(midi=v,function=0x600)
        yield 'load',dict(midi=v,function=0xB00)
        yield 'play',dict(fm=v,playing=2,argument=1,frame=7)
        yield 'update',dict(fm=v,playing=2,frame=0)
    for argument in (0,32,33,127,128,255,256,257,0x7FFF,0x8000,0xFFFE,0xFFFF,0xFFF6,0xFFF7,0xFFEA,0x13DA,0x13DB):
        for current in (0,1,31,32,33,127,128,254,255):yield 'play',dict(argument=argument,playing=current,frame=11)
    for a in (0,0x7F,0x80,0xFF):
        for b in (0,0x7F,0x80,0xFF):yield 'play',dict(playing=0,argument=1,priority_patch=((0,a),(1,b)),frame=7)
    for duration in range(256):
        for frame in sorted({duration,(duration+1)&255,255,0}):yield 'update',dict(playing=0,frame=frame,duration_patch=((0,duration),))
    for frames in (0,1,2,0x7FFF,0x8000,0xFFFE,0xFFFF):
        ticks=(0,) if not frames else (0,frames-1,frames)
        for flags in (2,0x202,0x402,0xED7):
            yield 'frame_delay',dict(frames=frames,ticks=ticks,flags=flags)
            yield 'measure',dict(active=0,frames=frames,ticks=ticks,flags=flags,measure=0xFFFF)
        values=(0,) if not frames else (0,frames-1,frames)
        for midi in (0,1,2,0x80,0xFF):yield 'measure',dict(measure=frames,measures=values,midi=midi)
    for length in range(13):
        name=b'X'*length+b'\0'+b'Q'*(12-length)
        for offset in (0x20,0xFFF8,0xFFFF):
            for midi in (0,2):yield 'load',dict(filename=name,filename_offset=offset,midi=midi)
    for end in (13,16,32):yield 'load',dict(filename=b'X'*13,suffix_end=end,midi=2)
    for errors in range(8):
        for function in (0x600,0xB00,0xFFFF):
            for midi in (0,1,2):yield 'load',dict(function=function,midi=midi,open_result=5,open_failure=bool(errors&1),read_failure=bool(errors&2),close_failure=bool(errors&4))
    for count in (0,1,12,13,32,0x5000):
        for failure in (False,True):yield 'load',dict(read_count=count,read_failure=failure)
    for segment in (0x5000,0x6000):
        for offset in (0,0x30,0xFFE0):yield 'load',dict(buffer_segment=segment,buffer_offset=offset,read_count=32)
    for command in (0,1,0x100,0x600,0x8000,0xFFFF):
        for midi in (0,1,2):
            for active in (0,1):yield 'kaja',dict(argument=command,midi=midi,active=active)
    for flags in (2,0x202,0x402,0xED7):
        for kind,p in (
            ('load',dict(midi=2,open_failure=True,read_failure=True)),('load',dict(midi=1,function=0xB00,read_count=0x5000)),
            ('play',dict(fm=0,argument=0x8000)),('play',dict(playing=255,frame=255,argument=0xFFFF)),
            ('play',dict(playing=0,argument=1,priority_patch=((0,128),(1,255)),frame=7)),
            ('update',dict(fm=0,playing=1,frame=255)),('update',dict(playing=0,frame=0,duration_patch=((0,0),))),('update',dict(playing=31,frame=255)),
            ('kaja',dict(active=0,midi=1,argument=0xFFFF)),('kaja',dict(active=0x80,midi=2,argument=0x600)),('kaja',dict(active=1,midi=1,argument=0xFFFF)),
            ('measure',dict(midi=1,measure=0xFFFF,measures=(0x7FFF,0xFFFE,0xFFFF)))):
            yield kind,dict(p,flags=flags)

def verify(target,candidate):
    observations=[]
    for image in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(image,load)
            try:
                trace=hashlib.sha256();counts={k:0 for k in ENTRIES};max_driver=max_counter=0
                for count,(kind,options) in enumerate(cases(),1):
                    row=m.run(kind,seed=0x1357 if count&1 else 0xECA8,stack=0x80 if count&1 else 0xFFF0,**options);counts[kind]+=1
                    max_driver=max(max_driver,row['driver_calls']);max_counter=max(max_counter,row['counter_updates']);trace.update(json.dumps(row,sort_keys=True).encode())
                need(m.covered==m.owned,'all 332 maintained sound/timing bytes execute')
                loads.append(dict(load_segment=load,cases=count,cases_by_function=counts,covered_owner_bytes=len(m.covered),maximum_observed_stack_depth=m.maximum_stack,
                    maximum_driver_calls=max_driver,maximum_counter_updates=max_counter,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent target/candidate sound observations')
    return dict(images=2,functions=6,code_bytes=332,cases_per_image=sum(o['cases'] for o in observations[0]),executed_owner_bytes=332,
        exhaustive_byte_states=256,legitimate_SE_entries=33,filename_copy_bytes=13,file_read_request_bytes=0x5000,observations=observations[0],
        scope='real six maintained bodies and nested frame delay; bounded DOS/PMD/MMD and finite counter-update replies, no physical IRQ/timing/audio or unbounded lifetime claim')

def negative_controls(target):
    controls=(
        ('load-copies-all-thirteen-bytes',0xC886,b'\x0D',b'\x0C','load',{}),
        ('load-input-far-pointer',0xC88C,b'\x06',b'\x08','load',{}),
        ('MIDI-only-song-function',0xC89E,b'\x06',b'\x0B','load',dict(midi=1)),
        ('suffix-scan-skips-byte-zero',0xC8AA,b'\x43',b'\x90','load',dict(midi=1)),
        ('suffix-characters-are-md',0xC8B6,b'\x6D',b'\x6E','load',dict(midi=1)),
        ('load-MIDI-tests-nonzero',0xC8DA,b'\xCD\x61',b'\xCD\x60','load',dict(midi=2)),
        ('open-error-does-not-change-handle-copy',0xC8CA,b'\xD8',b'\xC3','load',dict(open_failure=True,open_result=5)),
        ('read-request-is-5000h',0xC8E5,b'\x50',b'\x40','load',{}),
        ('DS-restored-before-close',0xC8E8,b'\x1F',b'\x90','load',{}),
        ('close-preserves-read-AL',0xC8E9,b'\xB4',b'\xB0','load',{}),
        ('load-cdecl-arguments-remain',0xC8EF,b'\xCB',b'\xCA','load',{}),
        ('play-loads-WORD-argument',0xCE4F,b'\x06',b'\x08','play',{}),
        ('SE-active-field-is-FM-possible',0xCE52,b'\x70',b'\x71','play',dict(fm=1,midi=0)),
        ('idle-first-SE-keeps-stale-frame',0xCE5C,b'\x75',b'\x74','play',dict(frame=7)),
        ('full-WORD-priority-index',0xCE72,b'\xDA',b'\xD8','play',dict(playing=1,argument=0x100)),
        ('priority-comparison-is-unsigned',0xCE77,b'\x77',b'\x7F','play',dict(playing=0,argument=1,priority_patch=((0,0x80),(1,0x7F)))),
        ('equal-priority-restarts-frame',0xCE80,b'\x08',b'\x09','play',dict(playing=1,argument=1,frame=7)),
        ('play-Pascal-two-byte-pop',0xCE84,b'\x02',b'\x04','play',dict(fm=0)),
        ('SE-driver-is-PMD',0xCEA1,b'\x60',b'\x61','update',dict(playing=1,frame=0)),
        ('SE-driver-command-is-0C',0xCE9C,b'\x0C',b'\x0D','update',dict(playing=1,frame=0)),
        ('frame-increment-is-BYTE',0xCEA2,b'\xFE',b'\xFF','update',dict(playing=1,frame=255)),
        ('duration-comparison-is-unsigned',0xCEB5,b'\x73',b'\x7D','update',dict(playing=0,frame=0x7E,duration_patch=((0,0x80),))),
        ('expired-SE-is-FF',0xCEC0,b'\xFF',b'\xFE','update',dict(playing=0,frame=1,duration_patch=((0,0),))),
        ('inactive-KAJA-keeps-incoming-AX',0xCECA,b'\x74',b'\x75','kaja',dict(active=0,argument=0xFFFF)),
        ('KAJA-MIDI-is-exactly-one',0xCED3,b'\x01',b'\x02','kaja',dict(midi=2)),
        ('counter-reset-is-WORD',0xCB55,b'\xC7',b'\xC6','frame_delay',{}),
        ('counter-bound-is-unsigned',0xCB61,b'\x72',b'\x7C','frame_delay',dict(frames=0x8000,ticks=(0x7FFF,0x8000))),
        ('delay-far-Pascal-pop',0xCB65,b'\x02',b'\x04','frame_delay',{}),
        ('measure-no-BGM-argument-order',0xD408,b'\x06',b'\x08','measure',dict(active=0,frames=2,measure=0xFFFF)),
        ('measure-query-command-is-05',0xD413,b'\x05',b'\x06','measure',{}),
        ('MMD-four-quarter-ticks',0xD420,b'\xC0',b'\xBF','measure',dict(midi=1)),
        ('measure-bound-is-unsigned',0xD427,b'\x72',b'\x7C','measure',dict(measure=0x8000,measures=(0x7FFF,0x8000))),
        ('measure-Pascal-four-byte-pop',0xD42B,b'\x04',b'\x02','measure',{}),
    )
    rejected=[]
    for name,at,old,new,kind,options in controls:
        raw=bytearray(target.program_image);need(raw[at:at+len(old)]==old,'literal mutation anchor '+name);raw[at:at+len(new)]=new;m=None
        try:
            try:m=Machine(replace(target,program_image=bytes(raw)),0x3000);m.run(kind,**options)
            except ValueError:rejected.append(name)
            else:raise ValueError('MAINL sound mutation survived: '+name)
        finally:
            if m:m.close()
    return dict(count=len(rejected),rejected=rejected)
