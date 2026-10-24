"""Twelve whole graphics procedures, excluding alignment bytes and shared DATA."""
import hashlib
import re
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.zun_driver_layout import review,resolve_native
from stage_th03_zun_driver import bodies,dos_text
from verify_th03_zun_driver_hybrid import SCATTERED_PROCS

NAMES=('draw_clipped','blit_egc','copy_rows','prepare_vram','build_mask','accumulate_plane','copy_lower_page',
       'compress_rows','copy_upper_to_lower','clear_upper','egc_begin','egc_end')
RANGES=tuple((n,a,b-a) for n,a,b in SCATTERED_PROCS if n.removeprefix('sprite16_') in NAMES)
SOURCE='src/zun/driver_graphics.inl'
FIXUPS=((0x373,0x105A),(0x377,0x105C),(0x37B,0x105E),(0x37E,0x1060),(0x382,0x1062),(0x386,0x1054),
 (0x38C,0x105C),(0x392,0x105C),(0x396,0x1062),(0x3A6,0x105C),(0x3A9,0x1054),(0x3B7,0x105E),(0x3BB,0x105C),
 (0x3C3,0x105C),(0x3CF,0x105C),(0x3D3,0x1062),(0x3E0,0x105C),(0x3E4,0x1062),(0x3EA,0x1054),(0x3EF,0x1054),(0x3F3,0x1062),
 (0x404,0x105E),(0x407,0x105A),(0x413,0x105C),(0x41B,0x105A),(0x421,0x1050),(0x427,0x1050),(0x42F,0x1052),
 (0x437,0x1050),(0x43E,0x1052),(0x449,0x1060),(0x451,0x1060),(0x455,0x1052),(0x458,0x1058),(0x45B,0x1058),
 (0x466,0x1056),(0x46B,0x1064),(0x47C,0x106C),(0x492,0x1066),(0x498,0xF3E),(0x49F,0x1068),(0x4BE,0x106C),
 (0x4C4,0xF3C),(0x4D7,0x106C),(0x4DF,0x106A),(0x4F0,0x106E),(0x4FD,0x1062),(0x502,0x1058),(0x506,0x1056),
 (0x544,0xC10),(0x54D,0xF3E),(0x55B,0xF3E),(0x578,0xF3E),(0x57D,0xF3C),(0x5A8,0xBD0),(0x5CA,0xC10),
 (0x5D4,0xBD0),(0x5F1,0xC10),(0x5F8,0xBD0),(0x60D,0xC10),(0x613,0xBD0),(0x62C,0xC10))
RELATIVE={0x544,0x5A8,0x5CA,0x5D4,0x5F1,0x5F8,0x60D,0x613,0x62C}

def need(value,message):
    if not value:raise ValueError('ZUN graphics layout: '+message)

def control_flow(image):
    ins={}
    for _,a,s in RANGES:
        rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image[a-256:a-256+s],a))
        need(sum(i.size for i in rows)==s,'whole procedure instruction boundaries');ins.update({i.address:i for i in rows})
    todo=[a for _,a,_ in RANGES];seen=set()
    while todo:
        a=todo.pop()
        if a in seen:continue
        need(a in ins,'direct edge inside owned graphics instructions');i=ins[a];seen.add(a)
        if i.mnemonic.startswith('ret'):continue
        if i.mnemonic.startswith('j') or i.mnemonic in ('call','loop'):
            need(i.op_str.startswith('0x'),'direct branch/call');todo.append(int(i.op_str,16))
        if i.mnemonic!='jmp':todo.append(a+i.size)
    dead=[(a,i.size,i.mnemonic,i.op_str) for a,i in ins.items() if a not in seen]
    need(dead==[(0x39F,2,'jmp','0x3ee'),(0x3CB,2,'jmp','0x3ee')],'two unreachable two-byte clipping jumps')
    reached={p for a in seen for p in range(a,a+ins[a].size)}
    need(len(reached)==810,'810 reachable bytes, four dead bytes')
    return ins,reached,dict(code_bytes=814,reachable_owner_bytes=810,unreachable_owner_bytes=4,unreachable_jumps=[dict(address=a,size=s,target=0x3EE) for a,s,_,_ in dead])

def verify(work,target,candidate,payload_offset,files,maintained):
    obj=(work/'driver/driver.obj').read_bytes();physical=review(obj,(work/'driver/driver.map').read_bytes());image,fixups,blocks=resolve_native(obj)
    need(image==candidate==target and len(image)==4224,'complete natural native driver equality')
    source=bodies(maintained[SOURCE].decode());need(set(source)=={'sprite16_'+n for n in NAMES},'all twelve complete source procedures')
    owners=[]
    for name,a,size in RANGES:
        body=dos_text(source[name]);slots=[n for n,raw in files.items() if n.startswith('driver/procs/') and raw==body]
        need(len(slots)==1,'one native include slot');slot=slots[0]
        need((work/slot).read_bytes()==body and len(re.findall(rb'(?m)^include '+re.escape(slot.removeprefix('driver/').encode())+rb'\r?$',files['driver/driver.asm']))==1,'actual consumed source')
        fields=[f for f in fixups if a<=f['address']<a+size];need(all(f['address']+f['width']<=a+size for f in fields),'whole native fields')
        digest=hashlib.sha256(image[a-256:a-256+size]).hexdigest()
        owners.append(dict(unit_id='th03-zun-decoded-driver-'+name.removeprefix('sprite16_').replace('_','-'),source=SOURCE,procedure=name,
            object='driver/driver.obj',include=slot,start=a,size=size,origin='library',coordinate_space='decoded-payload-com',payload_option='-4',
            payload_file_offset=a-256,decoded_file_offset=payload_offset+a-256,canonical_file_offset=None,format='COM',argument_bytes=0,
            callee_pop_bytes=0,private_data_bytes=0,private_bss_bytes=0,abi='near register interface; shared CS state; forward string preconditions; EGC helpers force IF on',
            ordered_relocations=[],ordered_native_fixups=fields,target_sha256=digest,candidate_sha256=digest))
    selected=[f for o in owners for f in o['ordered_native_fixups']]
    need([(f['address'],f['target_address']) for f in selected]==list(FIXUPS)
        and all(f['width']==2 and f['self_relative']==(f['address'] in RELATIVE) for f in selected),'62 ordered WORD fixups, nine relative')
    _,_,cfg=control_flow(image)
    return dict(owners=owners,functions=12,code_bytes=814,private_data_bytes=0,private_bss_bytes=0,ordered_native_fixups=selected,control_flow=cfg,
        native_layout=physical,native_records=blocks,enclosing_driver_accepted=False,reserved_spans_owned=False,original_assembler_identified=False)
