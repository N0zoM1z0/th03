"""Ten whole formatter/print procedures; digit DATA and enclosing gaps are context."""
import hashlib
import re

from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.zun_driver_layout import review,resolve_native
from stage_th03_zun_driver import bodies,dos_text
from verify_th03_zun_driver_hybrid import SCATTERED_PROCS

NAMES=('format_print','print_string','print_stack_string','format_into','pad_zeroes','pad_spaces','pad_field',
       'append_string','format_unsigned','reverse_string')
RANGES=tuple((n,a,b-a) for n,a,b in SCATTERED_PROCS if n.removeprefix('sprite16_') in NAMES)
SOURCE='src/zun/driver_format.inl'
FIXUPS=((0x64D,0x6B0,True),(0x735,0xC40,True),(0x813,0xC40,True),(0x8B5,0x8DC,False))
DEAD=((0x7A0,3,0x86D),(0x7C0,3,0x86D),(0x7E0,3,0x86D),(0x800,2,0x86D))


def need(value,message):
    if not value:raise ValueError('ZUN formatter layout: '+message)


def control_flow(image):
    instructions={}
    for _,a,size in (*RANGES,('sprite16_string_length',0xC40,18)):
        rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image[a-256:a-256+size],a))
        need(sum(i.size for i in rows)==size,'complete instruction boundaries')
        instructions.update({i.address:i for i in rows})
    reached=set();todo=[a for _,a,_ in RANGES]
    while todo:
        address=todo.pop()
        if address in reached:continue
        need(address in instructions,'direct control-flow edge inside complete scopes')
        i=instructions[address];reached.add(address)
        if i.mnemonic.startswith('ret'):continue
        if i.mnemonic.startswith('j') or i.mnemonic=='call':
            need(i.op_str.startswith('0x'),'direct branch/call only');todo.append(int(i.op_str,16))
        if i.mnemonic!='jmp':todo.append(address+i.size)
    dead=tuple((a,i.size,int(i.op_str,16)) for a,i in instructions.items() if a not in reached and i.mnemonic=='jmp')
    need(dead==DEAD and sum(instructions[a].size for a in instructions if a not in reached)==11,'four unreachable unconditional jumps / eleven bytes')
    owned={p for _,a,s in RANGES for p in range(a,a+s)}
    reachable={p for a in reached for p in range(a,a+instructions[a].size)}&owned
    need(len(owned)==677 and len(reachable)==666,'complete owner/reachable partition')
    return instructions,reachable,dict(instruction_bytes=677,reachable_owner_bytes=666,unreachable_owner_bytes=11,
        unreachable_jumps=[dict(address=a,size=s,target=t) for a,s,t in dead],indirect_control_flow=False)


def verify(work,target,candidate,payload_offset,files,maintained):
    obj=(work/'driver/driver.obj').read_bytes();physical=review(obj,(work/'driver/driver.map').read_bytes())
    image,fixups,blocks=resolve_native(obj)
    need(image==candidate==target and len(image)==4224,'complete natural native COM equality')
    need(len(RANGES)==10 and sum(s for _,_,s in RANGES)==677,'ten whole formatter procedures')
    source_bodies=bodies(maintained[SOURCE].decode());owners=[]
    need(set(source_bodies)=={'sprite16_'+n for n in (*NAMES,'is_decimal_digit','is_ascii_lower','ascii_upper')},'complete containing format include')
    for name,start,size in RANGES:
        body=dos_text(source_bodies[name]);slots=[n for n,raw in files.items() if n.startswith('driver/procs/') and raw==body]
        need(len(slots)==1,'unique actual procedure include');slot=slots[0]
        need((work/slot).read_bytes()==body and len(re.findall(rb'(?m)^include '+re.escape(slot.removeprefix('driver/').encode())+rb'\r?$',files['driver/driver.asm']))==1,'one consumed physical source slot')
        native=[f for f in fixups if start<=f['address']<start+size]
        need(all(f['address']+f['width']<=start+size for f in native),'whole native fields')
        digest=hashlib.sha256(target[start-256:start-256+size]).hexdigest()
        owners.append(dict(unit_id='th03-zun-decoded-driver-'+name.removeprefix('sprite16_').replace('_','-'),source=SOURCE,
            procedure=name,object='driver/driver.obj',include=slot,start=start,size=size,origin='library',coordinate_space='decoded-payload-com',
            payload_option='-4',payload_file_offset=start-256,decoded_file_offset=payload_offset+start-256,canonical_file_offset=None,
            format='COM',argument_bytes=2 if name=='sprite16_print_stack_string' else 0,callee_pop_bytes=2 if name=='sprite16_print_stack_string' else 0,
            private_data_bytes=0,private_bss_bytes=0,abi='near register interface; formatter arguments in SS four-byte slots; padding helpers share BP frame; forward string operations',
            ordered_relocations=[],ordered_native_fixups=native,target_sha256=digest,candidate_sha256=digest))
    selected=[f for o in owners for f in o['ordered_native_fixups']]
    need([(f['address'],f['target_address'],f['self_relative']) for f in selected]==list(FIXUPS)
        and [f['width'] for f in selected]==[2,2,2,4],'three relative WORD and one absolute DWORD ordered native fixups')
    need(image[0x8DC-256:0x8EC-256]==b'0123456789ABCDEF','external CS digit table identity')
    _,_,cfg=control_flow(image)
    return dict(owners=owners,functions=10,code_bytes=677,private_data_bytes=0,private_bss_bytes=0,ordered_native_fixups=selected,
        control_flow=cfg,digit_table_dependency_bytes=16,native_layout=physical,native_records=blocks,
        enclosing_driver_accepted=False,reserved_spans_owned=False,original_assembler_identified=False)
