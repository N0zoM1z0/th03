"""Physical ownership of nine complete maintained driver command procedures."""
import hashlib
import re

from lib.zun_driver_layout import review, resolve_native
from stage_th03_zun_driver import bodies, dos_text
from verify_th03_zun_driver_hybrid import COMMAND_PROCS

RANGES=tuple((name,start,end-start) for name,start,end in COMMAND_PROCS[:9])
SOURCE='src/zun/driver_command.inl'
# Literal native operand sites and target offsets, in producer order. Internal
# same-contribution near calls have assembler-resolved fields, not OMF fixups.
FIXUPS=((0x928,0x1070),(0x92D,0x1072),(0x952,0x1070),(0x95A,0x10F4),(0x95D,0x676),
        (0x974,0x1070),(0x9CF,0x1070),(0x9D5,0x1114),(0x9D8,0x676),(0x9E1,0x1070),
        (0x9E5,0x10F2),(0x9E9,0x10F2),(0x9F1,0x1070),(0x9FB,0x1070),(0x9FF,0x10F2),
        (0xA03,0x10F2),(0xA12,0xA90),(0xA17,0x112B),(0xA1A,0x676),(0xA31,0xA90),
        (0xA38,0x10F2),(0xA3A,0x1072),(0xA3E,0x10F2),(0xA42,0x10F2),(0xA49,0x1070),
        (0xA52,0x1070),(0xA5F,0x101C),(0xA67,0x1152),(0xA6A,0x676),(0xA74,0xC52))
RELATIVE={0x95D,0x9D8,0xA12,0xA1A,0xA31,0xA6A,0xA74}


def need(value,message):
    if not value:raise ValueError('ZUN command layout: '+message)


def verify(work,target,candidate,payload_offset,files,maintained):
    obj=(work/'driver/driver.obj').read_bytes()
    physical=review(obj,(work/'driver/driver.map').read_bytes())
    image,fixups,blocks=resolve_native(obj)
    need(image==candidate==target and len(image)==4224,'natural complete native COM equality')
    need(len(RANGES)==9 and sum(size for _,_,size in RANGES)==361,'complete command contribution')
    source_bodies=bodies(maintained[SOURCE].decode());owners=[]
    need(set(source_bodies)=={n for n,_,_ in RANGES},'whole bounded command include ownership')
    for name,start,size in RANGES:
        body=dos_text(source_bodies[name]);slots=[n for n,raw in files.items() if n.startswith('driver/procs/') and raw==body]
        need(len(slots)==1,'unique actual command procedure slot');slot=slots[0]
        need((work/slot).read_bytes()==body,'consumed command include bytes')
        need(len(re.findall(rb'(?m)^include '+re.escape(slot.removeprefix('driver/').encode())+rb'\r?$',files['driver/driver.asm']))==1,'one physical command include')
        native=[f for f in fixups if start<=f['address']<start+size]
        need(all(f['address']+f['width']<=start+size for f in native),'complete owned fixup fields')
        raw=target[start-256:start-256+size];digest=hashlib.sha256(raw).hexdigest()
        owners.append(dict(unit_id='th03-zun-decoded-driver-'+name.removeprefix('sprite16_').replace('_','-'),
            source=SOURCE,procedure=name,object='driver/driver.obj',include=slot,start=start,size=size,origin='library',
            coordinate_space='decoded-payload-com',payload_option='-4',payload_file_offset=start-256,
            decoded_file_offset=payload_offset+start-256,canonical_file_offset=None,format='COM',argument_bytes=0,
            callee_pop_bytes=0,private_data_bytes=0,private_bss_bytes=0,
            abi='near register interface; DS=driver group; dispatch ES=DS; diagnostic strings use SS; optional terminal DOS exit',
            ordered_relocations=[],ordered_native_fixups=native,target_sha256=digest,candidate_sha256=digest))
    selected=[f for o in owners for f in o['ordered_native_fixups']]
    need([(f['address'],f['target_address']) for f in selected]==list(FIXUPS)
         and all(f['width']==2 and f['self_relative']==(f['address'] in RELATIVE) for f in selected),'thirty literal ordered command fixups')
    need(physical['layout_profile']=='native-paragraph-contributions' and physical['linker_zero_bytes']==71,'natural enclosing driver layout')
    return dict(owners=owners,functions=9,code_bytes=361,private_data_bytes=0,private_bss_bytes=0,
                native_layout=physical,native_records=blocks,ordered_native_fixups=selected,
                enclosing_driver_accepted=False,reserved_spans_owned=False,original_assembler_identified=False)
