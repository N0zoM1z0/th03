"""Read real relocated STAFF initializers through already accepted native consumers.

Existing full-state contracts remain intact. Additional semantic assertions bind
outputs to the sprite, mask and symbol meanings, rather than copying input bytes
into expectations. Eight zero-strength mask bytes have static ownership only:
the native zero-strength branch never reads them.
"""
import hashlib
import itertools
import json
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_16, CS_AC_READ
from capstone.x86_const import X86_OP_MEM
from unicorn import UC_HOOK_CODE
from lib.decoded_mainl_root_helpers_runtime import GPRS, REG
from lib.decoded_mainl_staff_data_layout import START,SIZE,DS,POINTERS,semantic_image,sprite_words,mask_words,need
from lib.decoded_mainl_staff_draw_runtime import Machine as Draw
from lib.decoded_mainl_dissolve_runtime import Machine as Dissolve
from lib.decoded_mainl_staff_verdict_runtime import Machine as Verdict, DATA as VERDICT
from lib.decoded_mainl_ending_runtime import Machine as Ending
from lib.decoded_mainl_pi_free_runtime import address


def prepare(machine,image,load,mutation=None):
    start=DS*16+START
    data=bytearray(image.relocated_program_image(load)[start:start+SIZE])
    need(bytes(data)==semantic_image(load),'live independently relocated initializer')
    if mutation is not None:
        off,bit=mutation
        data[off]^=1<<bit
    at=address(machine.ds,START)
    initial=bytearray(machine.initial)
    initial[at:at+SIZE]=data
    machine.initial=bytes(initial)
    return data


def fixture(kind,image,load,parameters,mutation=None):
    cls={'flake':Draw,'mask':Dissolve,'verdict':Verdict,'ending':Ending}[kind]
    machine=cls(image,load)
    data=prepare(machine,image,load,mutation)
    read=set()
    start=address(machine.ds,START)
    decoder=Cs(CS_ARCH_X86,CS_MODE_16)
    decoder.detail=True
    operands={}
    for at,size in machine.instructions.items():
        ins=next(decoder.disasm(image.program_image[at:at+size],at))
        if ins.mnemonic=='lea':
            continue
        fields=[]
        for op in ins.operands:
            if op.type==X86_OP_MEM and op.access&CS_AC_READ:
                mem=op.mem
                fields.append((ins.reg_name(mem.segment),ins.reg_name(mem.base),
                               ins.reg_name(mem.index),mem.scale,mem.disp,op.size))
        if fields:
            operands[at]=fields
    def reads(u,at,size,user):
        # Decode explicit memory reads at instructions that the full-state
        # consumer contract executes. A no-op UC memory-read hook changed
        # guest control flow in the local probe; its cause remains unknown.
        for seg,base,index,scale,disp,width in operands.get(at-machine.base,()):
            def value(name):
                return u.reg_read(GPRS.get(name,REG.get(name)))&65535 if name else 0
            off=(value(base)+value(index)*scale+disp)&65535
            segment=value(seg or ('ss' if base in ('bp','sp') else 'ds'))
            physical=address(segment,off)
            read.update(range(max(physical,start)-start,min(physical+width,start+SIZE)-start))
    machine.hooks.append(machine.u.hook_add(UC_HOOK_CODE,reads))
    try:
        if kind=='flake':
            cel,rotation=parameters
            # All source bits must be observable through OR, independently of
            # the existing register/store/full-memory scalar contract.
            left,top=320+rotation,80
            graph=0xA8000+top*80+(left>>3)
            initial=bytearray(machine.initial)
            for row in range(8):
                initial[graph+row*80:graph+row*80+2]=bytes(2)
            machine.initial=bytes(initial)
            result=machine.run('flake',left=left,top=top,index=cel)
            for row,word in enumerate(sprite_words()[cel*8:cel*8+8]):
                expected=((word>>rotation)|(word<<(16-rotation)))&65535 if rotation else word
                need(int.from_bytes(machine.u.mem_read(graph+row*80,2),'little')==expected,
                     'semantic flake cel/row/rotation output')
        elif kind=='mask':
            strength,phase=parameters
            # No image bytes precede the AND; an all-one destination exposes
            # every bit of the selected mask WORD.
            initial=bytearray(machine.initial)
            initial[0xE0000:0xF0002]=b'\xFF'*65538
            machine.initial=bytes(initial)
            patterns=struct.unpack_from('<32H',data,68)
            result=machine.run(left=8,top=phase,strength=strength,width=16,height=1,blit_width=0,patterns=patterns)
            graph=0xE0000+phase*80
            need(int.from_bytes(machine.u.mem_read(graph,2),'little')==((~mask_words()[strength*4+phase])&65535),
                 'semantic strength/phase complement output')
        elif kind=='verdict':
            playchar,rank,digit=parameters
            memory=bytearray(machine.initial)
            score=(digit,)*9
            for off,raw in ((VERDICT['score'],bytes(score)),(VERDICT['playchar'],bytes([playchar])),
                            (VERDICT['rank'],bytes([rank])),(VERDICT['skill'],b'\x00')):
                at=address(machine.ds,off)
                memory[at:at+len(raw)]=raw
            machine.u.mem_write(0,bytes(memory))
            result=machine.run(persistent=True)
            bindings={site:offset for site,_,_,offset in POINTERS}
            expected=[bindings[132+playchar*4],bindings[168+rank*4]]
            expected += [bindings[184+digit*4]]*(8 if digit else 0)
            expected += [bindings[184+digit*4]]*2+[bindings[184]]
            need([r['pointer'] for r in result['rendered'][:-1]]==[[load+DS,off] for off in expected],
                 'semantic renderer far-pointer identities, including both native WORDs')
        else:
            character,credits=parameters
            script=struct.unpack_from('<HH',data,0)
            result=machine.run(character=character,credits=credits,script=script,digits=(48,48))
            playchar=max(0,(character-1)//2)
            expected=bytes(((48+playchar//10)&255,(48+playchar%10)&255))
            need(bytes(machine.u.mem_read(address(machine.ds,0xB3F),2))==expected,
                 'semantic ending script pointer and decimal character updates')
        return dict(kind=kind,parameters=list(parameters),result=result),read
    finally:
        machine.close()


def cases():
    for cel,rotation in itertools.product(range(4),range(8)):
        yield 'flake',(cel,rotation)
    for strength,phase in itertools.product(range(1,8),range(4)):
        yield 'mask',(strength,phase)
    for playchar,rank in itertools.product(range(9),range(4)):
        yield 'verdict',(playchar,rank,9)
    for digit in range(10):
        yield 'verdict',(0,0,digit)
    for character,credits in itertools.product((1,15,21,255),(0,3,255)):
        yield 'ending',(character,credits)


def verify(target,candidate):
    observations=[]
    for image in (target,candidate):
        rows=[]
        for load in (0x1000,0x3000):
            trace=hashlib.sha256()
            read=set()
            counts={kind:0 for kind in ('flake','mask','verdict','ending')}
            for kind,parameters in cases():
                result,used=fixture(kind,image,load,parameters)
                trace.update(json.dumps(result,sort_keys=True).encode())
                read|=used
                counts[kind]+=1
            expected=set(range(SIZE))-set(range(68,76))
            need(read==expected,'all216 reachable initializer bytes read by actual native operands; zero-strength8 remain static')
            rows.append(dict(load_segment=load,complete_calls=counts,initialized_bytes_read=len(read),
                             static_only_bytes=8,trace_sha256=trace.hexdigest()))
        observations.append(rows)
    need(observations[0]==observations[1],'complete independent target/candidate data-consumer observations')
    return dict(images=2,initialized_data_bytes=SIZE,observations=observations[0],cases_per_image=236,
        ignored_stack_bytes=0,guest_iterations_skipped=False,existing_full_state_contracts_preserved=True,
        new_CODE_ownership_bytes=0,pointee_strings_or_renderer_owned=False,physical_pixels_or_timing_proved=False)


def negative_controls(target):
    rejected=[]
    # Mutants are inputs to both UC and the existing scalar state model. Only
    # the additional semantic output assertion rejects them; no raw-byte check,
    # memory mismatch against an unmutated model, or fixture rejection counts.
    for off in range(SIZE):
        if 2<=off<4 or 68<=off<76:
            continue
        if off<2:
            kind,parameters='ending',(21,0)
        elif off<68:
            kind,parameters='flake',((off-4)//16,0)
        elif off<132:
            word=(off-68)//2
            kind,parameters='mask',(word//4,word%4)
        elif off<168:
            kind,parameters='verdict',((off-132)//4,0,0)
        elif off<184:
            kind,parameters='verdict',(0,(off-168)//4,0)
        else:
            kind,parameters='verdict',(0,0,(off-184)//4)
        for bit in range(8):
            try:
                fixture(kind,target,0x1000,parameters,(off,bit))
            except ValueError as error:
                need('semantic ' in str(error),'control must reach independent semantic output assertion: '+str(error))
                rejected.append([off,bit])
            else:
                raise ValueError('MAINL staff DATA semantic control survived: '+str((off,bit)))
    need(len(rejected)==1712,'all214 behavior-observable DATA bytes / eight bit lanes reject')
    return dict(count=len(rejected),data_bit_mutations=rejected,actual_native_consumers=True,
        static_only_mask_bytes=8,script_segment_WORD_behavior_controls=False,CODE_mutations_counted=False)
