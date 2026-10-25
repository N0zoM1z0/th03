"""Semantic 32-slot directory DATA, native OMF iterated records and outer layout."""
import hashlib
import re
import struct

from lib.omf import describe_omf,parse_omf
from lib.zun import parse_launcher

SOURCE = 'src/zun/directory.asm'
PARAMETERS = ('ONGCHK_BYTES','INIT_BYTES','ZUNSOFT_BYTES','DRIVER_BYTES','RES_YUME_BYTES','STUB_BYTES','CALL_BYTES')
PUBLICS = dict(directory_count=0x100,directory_names=0x102,directory_entries=0x202,directory_end=0x244)


def need(value,message):
    if not value:
        raise ValueError('ZUN directory layout: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def iterated(raw):
    """Bounded 16-bit OMF LIDATA expansion; never used to alter product outputs."""
    def block(at,depth):
        need(depth <= 8 and at+4 <= len(raw),'bounded complete iterated block')
        repeat,children = struct.unpack_from('<HH',raw,at)
        at += 4
        need(repeat > 0,'positive native repetition count')
        if children:
            parts = []
            need(children <= 324,'bounded nested count')
            for _ in range(children):
                part,at = block(at,depth+1)
                parts.append(part)
            data = b''.join(parts)
        else:
            need(at < len(raw),'leaf length')
            size = raw[at]
            at += 1
            need(size > 0 and at+size <= len(raw),'complete nonempty literal leaf')
            data = raw[at:at+size]
            at += size
        need(len(data)*repeat <= 324,'directory-sized expansion')
        return data*repeat,at
    parts,at = [],0
    while at < len(raw):
        data,at = block(at,0)
        parts.append(data)
    result = b''.join(parts)
    need(len(result) <= 324,'complete bounded iterated record')
    return result


def native(obj,linked,map_raw):
    records = parse_omf(obj)
    meta = describe_omf(obj)
    need(meta['valid'] and meta['translator_comments'] == ['Turbo Assembler  Version 5.0']
         and meta['dependency_paths'] == ['meta.asm'],'actual native producer identity')
    allowed = {'THEADR','COMENT','LNAMES','SEGDEF','GRPDEF','PUBDEF','LEDATA','LIDATA','MODEND'}
    need(all(r.name in allowed for r in records),'no fixups, externals or wide storage dialect')
    need(b''.join(r.data for r in records if r.name == 'LNAMES') == b'\0\x05_TEXT\x04CODE\x05_DATA\x04DATA\x06DGROUP',
         'native tiny names')
    need([r.data for r in records if r.name == 'SEGDEF'] == [b'\x48\x44\x02\x02\x03\x01',b'\x48\0\0\x04\x05\x01'],
         'WORD public USE16 0244h CODE contribution and empty DATA')
    need([r.data for r in records if r.name == 'GRPDEF'] == [b'\x06\xFF\x02\xFF\x01']
         and [r.data for r in records if r.name == 'MODEND'] == [b'\xC1\x10\x01\x01\0\x01'],
         'tiny group order and 0100 entry')
    publics = {}
    for r in records:
        if r.name != 'PUBDEF':
            continue
        need(r.data[:2] == b'\x01\x01','group-relative CODE public')
        at = 2
        while at < len(r.data):
            size = r.data[at];at += 1
            need(size > 0 and at+size+3 <= len(r.data),'complete public')
            name = r.data[at:at+size].decode('ascii');at += size
            value = struct.unpack_from('<H',r.data,at)[0];at += 2
            need(r.data[at] == 0 and name not in publics,'untyped unique public');at += 1
            publics[name] = value
    need(publics == PUBLICS,'all field/extent public addresses')
    result,blocks = bytearray(),[]
    for r in records:
        if r.name not in ('LEDATA','LIDATA'):
            continue
        need(len(r.data) >= 4 and r.data[0] == 1,'local CODE data record')
        start = struct.unpack_from('<H',r.data,1)[0]
        data = r.data[3:] if r.name == 'LEDATA' else iterated(r.data[3:])
        need(start == 256+len(result),'complete ordered nonoverlapping native records')
        result.extend(data)
        blocks.append(dict(kind=r.name,start=start,size=len(data),encoded_bytes=len(r.data)-3))
    need([(b['kind'],b['start'],b['size']) for b in blocks]
         == [('LEDATA',0x100,42),('LIDATA',0x12A,216),('LEDATA',0x202,12),('LIDATA',0x20E,54)],
         'literal fields plus native unused-name and unused-entry repetitions')
    need(bytes(result) == linked and len(linked) == 324,'complete native expansion equals raw linked COM')
    text = map_raw.decode('ascii')
    allocation = re.findall(r'(?m)^\s*([0-9A-F]+)H\s+([0-9A-F]+)H\s+([0-9A-F]+)H\s+(_TEXT|_DATA)\s+(CODE|DATA)\s*$',text)
    need([(int(a,16),int(b,16),int(c,16),n,cls) for a,b,c,n,cls in allocation]
         == [(0,0x243,0x244,'_TEXT','CODE'),(0x244,0x244,0,'_DATA','DATA')],'complete native MAP allocation')
    detail = re.findall(r'(?m)^\s*0000:([0-9A-F]+)\s+([0-9A-F]+) C=(CODE|DATA)\s+S=(_TEXT|_DATA)\s+G=DGROUP\s+M=meta.asm\s+ACBP=48\s*$',text)
    need([(int(a,16),int(b,16),c,n) for a,b,c,n in detail]
         == [(0,0x244,'CODE','_TEXT'),(0x244,0,'DATA','_DATA')],'MAP group/module/alignment')
    rows = re.findall(r'(?m)^\s*0000:([0-9A-F]+)\s+(?:idle\s+)?(directory_\w+)\s*$',text)
    need(len(rows) == 8 and all(sum(n == name and int(a,16) == value for a,n in rows) == 2
                                for name,value in PUBLICS.items()),'both complete MAP public tables')
    return dict(publics=publics,native_records=blocks,ordered_native_fixups=[],com_relocations=[],
                initialized_bytes=324,uninitialized_ORG_prefix_bytes=256,private_bss_bytes=0)


def specification(image):
    directory = parse_launcher(image,223)
    need([p['name'] for p in directory['payloads']] == ['-1','-2','-3','-4','-5'],'five semantic option names')
    lengths = (926,1390,10096,4224,5618)
    starts,at = [],0x326
    for size in lengths:
        starts.append(at);at += size
    starts.append(at)
    expected = struct.pack('<H',5)+b''.join(f'-{i}'.encode().ljust(8,b' ') for i in range(1,6))+b' '*(27*8)
    expected += struct.pack('<33H',*starts,*([0]*27))
    need(image[223:547] == expected and at == len(image)+256-8,'all 324 semantic DATA bytes and final helper boundary')
    return dict(count=5,capacity=32,names_bytes=256,entry_words=33,ordered_payload_boundaries=starts,
                unused_name_bytes=216,unused_entry_words=27,data_bytes=324)


def verify(work,target,candidate,files,maintained,cold):
    need(target == candidate and len(target) == 22812,'whole decoded source composition equality')
    need(files['wrapper/meta.asm'] == maintained[SOURCE] == (work/'wrapper/meta.asm').read_bytes(),'whole consumed maintained TU')
    need(files['wrapper/meta.rsp'] == b'-c -s -t -3 meta.obj,meta.com,meta.map,\r\n'
         == (work/'wrapper/meta.rsp').read_bytes(),'normal single-object link input')
    linked = (work/'wrapper/meta.com').read_bytes()
    need(linked == target[223:547],'actual complete composed directory contribution')
    physical = native((work/'wrapper/meta.obj').read_bytes(),linked,(work/'wrapper/meta.map').read_bytes())
    semantic = specification(target)
    expected = dict(zip(PARAMETERS,(926,1390,10096,4224,5618,223,3)))
    for rnd in (1,2):
        need(cold['rounds'][rnd-1]['directory_definitions'] == expected,'each cold round actual linked-length inputs')
        phase, = [p for p in cold['native_phases'] if p['label'] == f'round{rnd}:directory-assemble']
        need([a for a in phase['argv'] if a.startswith('/d')] == [f'/d{k}={v}' for k,v in expected.items()]
             and phase['argv'][-1] == 'meta.asm,meta.obj' and phase['returncode'] == 0,
             'actual seven native command-line definitions')
    digest = sha(linked)
    owner = dict(unit_id='th03-zun-directory',source=SOURCE,object='wrapper/meta.obj',include='wrapper/meta.asm',
        start=0x1DF,size=324,origin='authored',code_bytes=0,data_bytes=324,procedures=0,
        coordinate_space='decoded-launcher-com',payload_option=None,decoded_file_offset=223,canonical_file_offset=None,
        format='COM',ordered_relocations=[],ordered_native_fixups=[],argument_bytes=0,callee_pop_bytes=0,
        private_data_bytes=324,private_bss_bytes=0,abi='five records in fixed 32-slot directory; near CS offsets from actual linked input lengths',
        target_sha256=digest,candidate_sha256=digest)
    return dict(owners=[owner],code_bytes=0,data_bytes=324,functions=0,native_layout=physical,semantic=semantic,
        native_definitions=expected,outer_publics={n:a+0xDF for n,a in PUBLICS.items()},
        original_generation_tool_identified=False,payloads_owned=False,enclosing_product_accepted=False)
