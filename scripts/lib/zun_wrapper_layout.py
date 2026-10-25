"""Three whole TASM/TLINK wrapper producers, in outer decoded COM coordinates."""
import hashlib
import re
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import describe_omf, parse_omf
from lib.zun import parse_launcher

SOURCES = ('src/zun/launcher.asm','src/zun/transfer_call.asm','src/zun/transfer_helper.asm')
ALIASES = ('stub','call','helper')
UNITS = ('th03-zun-launcher','th03-zun-transfer-call','th03-zun-transfer-helper')
FIXUPS = ((0x11A,0x1DF),(0x135,0x1DF),(0x138,0x1E1),(0x167,0x2E1),(0x16B,0x1DF),
          (0x16E,0x1E1),(0x172,0x102),(0x184,0x102),(0x18D,0x104))


def need(value,message):
    if not value:
        raise ValueError('ZUN wrapper layout: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def native(obj, linked, map_raw, alias):
    records = parse_omf(obj)
    meta = describe_omf(obj)
    need(meta['valid'] and meta['translator_comments'] == ['Turbo Assembler  Version 5.0']
         and meta['dependency_paths'] == [alias+'.asm'], 'complete native producer identity')
    names = b''.join(r.data for r in records if r.name == 'LNAMES')
    need(names == b'\0\x05_TEXT\x04CODE\x05_DATA\x04DATA\x06DGROUP', 'native segment/group names')
    size = 256+len(linked)
    segments = [r.data for r in records if r.name == 'SEGDEF']
    need(segments == [b'\x48'+struct.pack('<H',size)+b'\x02\x03\x01',b'\x48\0\0\x04\x05\x01'],
         'WORD/PUBLIC/USE16 CODE and empty DATA, complete ORG span')
    need([r.data for r in records if r.name == 'GRPDEF'] == [b'\x06\xFF\x02\xFF\x01']
         and [r.data for r in records if r.name == 'MODEND'] == [b'\xC1\x10\x01\x01\0\x01'],
         'literal tiny group order and native 0100 entry')
    allowed = {'THEADR','COMENT','LNAMES','SEGDEF','GRPDEF','LEDATA','FIXUPP','MODEND'}
    need(all(r.name in allowed for r in records), 'no external, public, iterated or wide-record fallback')
    data = [r.data for r in records if r.name == 'LEDATA']
    need(len(data) == 1 and data[0][:3] == b'\x01\0\x01' and data[0][3:] == linked,
         'whole initialized OMF contribution equals normal linked COM, without normalization')
    fixes = []
    for r in records:
        if r.name != 'FIXUPP':
            continue
        need(len(r.data)%5 == 0, 'literal unthreaded native fixup records')
        for i in range(0,len(r.data),5):
            loc,site,fd,frame,target = r.data[i:i+5]
            need((loc,fd,frame,target) == (0xC4,0x14,1,1) and site+2 <= len(linked),
                 'absolute WORD, group frame and local CODE segment target')
            fixes.append(dict(address=256+site,width=2,self_relative=False,
                frame_group=1,target_segment=1,target_address=struct.unpack_from('<H',linked,site)[0]))
    text = map_raw.decode('ascii')
    allocation = re.findall(r'(?m)^\s*([0-9A-F]+)H\s+([0-9A-F]+)H\s+([0-9A-F]+)H\s+(_TEXT|_DATA)\s+(CODE|DATA)\s*$',text)
    end = (size+1)&~1
    need([(int(a,16),int(b,16),int(c,16),n,cls) for a,b,c,n,cls in allocation]
         == [(0,size-1,size,'_TEXT','CODE'),(end,end,0,'_DATA','DATA')], 'complete MAP extents')
    detail = re.findall(r'(?m)^\s*0000:([0-9A-F]+)\s+([0-9A-F]+) C=(CODE|DATA)\s+S=(_TEXT|_DATA)\s+G=DGROUP\s+M=(\w+\.asm)\s+ACBP=48\s*$',text)
    need([(int(a,16),int(b,16),c,n,m) for a,b,c,n,m in detail]
         == [(0,size,'CODE','_TEXT',alias+'.asm'),(end,0,'DATA','_DATA',alias+'.asm')], 'MAP module/group/alignment ownership')
    return dict(ordered_native_fixups=fixes,code_segment_bytes=size,initialized_bytes=len(linked),
        uninitialized_ORG_prefix_bytes=256,private_bss_bytes=0,com_relocations=[],map_data_start=end)


def instructions(image):
    """Decode only source-owned instructions; the 21 DATA bytes are excluded."""
    d = parse_launcher(image,223)
    spans = ((0x100,2),(0x117,200),(0x323,3),(d['helper_offset']+256,8))
    result = {}
    decoder = Cs(CS_ARCH_X86,CS_MODE_16)
    for at,size in spans:
        part = list(decoder.disasm(image[at-256:at-256+size],at))
        need(sum(i.size for i in part) == size, 'complete instruction partition')
        result.update({i.address:i for i in part})
    need(sum(i.size for i in result.values()) == 213, '213 CODE bytes, separate 21-byte DATA')
    return result


def verify(work,target,candidate,files,maintained):
    need(target == candidate and len(target) == 22812, 'whole decoded launcher equality')
    directory = parse_launcher(target,223)
    starts = (0x100,0x323,directory['helper_offset']+256)
    sizes = (223,3,8)
    owners,profiles = [],[]
    for source,alias,uid,start,size,code in zip(SOURCES,ALIASES,UNITS,starts,sizes,(202,3,8)):
        slot = 'wrapper/'+alias+'.asm'
        need(files[slot] == maintained[source] == (work/slot).read_bytes(), 'complete actual maintained TU '+source)
        rsp = f'-c -s -t -3 {alias}.obj,{alias}.com,{alias}.map,\r\n'.encode()
        need(files['wrapper/'+alias+'.rsp'] == rsp == (work/('wrapper/'+alias+'.rsp')).read_bytes(),
             'one normal native object in actual link response')
        linked = (work/('wrapper/'+alias+'.com')).read_bytes()
        need(len(linked) == size and linked == target[start-256:start-256+size], 'whole relocated composition contribution')
        p = native((work/('wrapper/'+alias+'.obj')).read_bytes(),linked,(work/('wrapper/'+alias+'.map')).read_bytes(),alias)
        expected = list(FIXUPS) if alias == 'stub' else []
        need([(f['address'],f['target_address']) for f in p['ordered_native_fixups']] == expected,
             'nine literal native WORD fields; transfer TUs have no fixups')
        digest = sha(linked)
        owners.append(dict(unit_id=uid,source=source,object='wrapper/'+alias+'.obj',include=slot,
            start=start,size=size,origin='authored',code_bytes=code,data_bytes=size-code,procedures=1,
            coordinate_space='decoded-launcher-com',payload_option=None,decoded_file_offset=start-256,
            canonical_file_offset=None,format='COM',ordered_relocations=[],ordered_native_fixups=p['ordered_native_fixups'],
            argument_bytes=0,callee_pop_bytes=0,private_data_bytes=size-code,private_bss_bytes=0,
            abi='COM PSP entry; DS=ES=CS, SS caller stack; direct transfer entries require DF=0, SI at a canonical payload, DI=0100, CX within that payload; helper discards return and enters 0100; successful lookup leaves remaining count on stack',
            target_sha256=digest,candidate_sha256=digest))
        profiles.append(dict(alias=alias,**p))
    # The composer owns the intervening directory, not any of these three TUs.
    need(target[2:23] == b'\0\0No COM-Soft !!!\r\n\n$', 'complete semantic launcher DATA')
    need((0x326+struct.unpack_from('<h',target,0x324-256)[0])&65535 == starts[2],
         'actual near CALL reaches helper over all five current payloads')
    need(sum(p['size'] for p in directory['payloads']) == 22254, 'current payload-length definition')
    need(b'PAYLOAD_BYTES' in maintained[SOURCES[1]], 'payload-length source expression')
    ins = instructions(target)
    need(ins[0x1DC].mnemonic == 'jmp' and ins[0x1DC].op_str == '0x323', 'external-directory jump target')
    return dict(owners=owners,code_bytes=213,data_bytes=21,functions=3,native_profiles=profiles,
        ordered_native_fixups=profiles[0]['ordered_native_fixups'],
        directory_bytes_excluded=324,payloads_owned=False,enclosing_product_accepted=False,
        source_only=True,stored_offsets_invented=False)
