"""Five complete native PI procedures, four TC4 producers and literal fixups."""
import hashlib
import re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

CS, DS = 0xC7E, 0xE3F
DATA = {'_pi_headers': 0x1F26, '_pi_buffers': 0x1F0E, '_Palettes': 0x141E}
CALLS = {'_memcpy': 0x4B7D, 'PALETTE_SHOW': 0x17D0, 'GRAPH_PACK_PUT_8': 0x1632,
         'GRAPH_PI_FREE': 0xFEC, 'GRAPH_PI_LOAD_PACK': 0x1044}
# leaf, source, first binary, offset, size, procedures(kind,symbol,MAP name,off,size,args)
PRODUCERS = (
    ('pi_put', 'src/shared/formats/pi_put.cpp', 'op', 0x52A, 173,
     (('palette', '@PI_PALETTE_APPLY$QI', 'pi_palette_apply(int)', 0, 37, 2),
      ('put', '@PI_PUT_8$QIII', 'pi_put_8(int,int,int)', 37, 136, 6))),
    ('pi_put_i', 'src/mainl/formats/pi_put_interlace.cpp', 'mainl', 0x5D7, 135,
     (('interlace', '@PI_PUT_INTERLACE_8$QIII', 'pi_put_interlace_8(int,int,int)', 0, 135, 6),)),
    ('pi_load', 'src/shared/formats/pi_load.cpp', 'op', 0xCCB, 70,
     (('load', '@PI_LOAD$QINXC', 'pi_load(int,const char far*)', 0, 70, 6),)),
    ('pi_put_q', 'src/mainl/formats/pi_put_quarter.cpp', 'mainl', 0xD11, 177,
     (('quarter', '@PI_PUT_QUARTER_8$QIIII', 'pi_put_quarter_8(int,int,int,int)', 0, 177, 8),)))
ENTRIES = {k: (CS * 16 + offset + at, size, args)
           for _, _, _, offset, _, procedures in PRODUCERS for k, _, _, at, size, args in procedures}
EXTERNALS = {
    'pi_put': ('_memcpy', 'PALETTE_SHOW', '_Palettes', 'GRAPH_PACK_PUT_8', '_pi_headers', '_pi_buffers'),
    'pi_put_i': ('GRAPH_PACK_PUT_8', '_pi_headers', '_pi_buffers'),
    'pi_load': ('GRAPH_PI_LOAD_PACK', 'GRAPH_PI_FREE', '_pi_headers', '_pi_buffers'),
    'pi_put_q': ('GRAPH_PACK_PUT_8', '_pi_buffers')}
# offset, LOCAT, FIXDAT, explicit frame, external index, raw addend: native order.
FIELDS = {
    'pi_put': ((160,196,22,1,5,22),(115,196,22,1,5,20),(93,204,86,None,4,0),(90,196,22,1,5,20),
               (60,196,22,1,6,0),(56,196,22,1,6,2),(29,204,86,None,2,0),(21,204,86,None,1,0),
               (18,196,22,1,3,0),(13,196,22,1,5,24)),
    'pi_put_i': ((122,196,22,1,2,22),(78,196,22,1,2,20),(56,204,86,None,1,0),
                 (53,196,22,1,2,20),(23,196,22,1,3,0),(19,196,22,1,3,2)),
    'pi_load': ((58,204,86,None,1,0),(53,196,22,1,4,0),(43,196,22,1,3,0),
                (29,204,86,None,2,0),(26,196,22,1,4,0),(14,196,22,1,3,0)),
    'pi_put_q': ((113,204,86,None,1,0),(24,196,22,1,2,0),(20,196,22,1,2,2))}


def need(value, message):
    if not value:
        raise ValueError('MAINL PI layout: ' + message)


def native_image(raw, leaf):
    code, _ = code_bytes(raw, 1)
    image, fields, names = bytearray(code), [], []
    block = None
    for record in parse_omf(raw):
        if record.name == 'EXTDEF':
            at = 0
            while at < len(record.data):
                n = record.data[at]
                names.append(record.data[at + 1:at + n + 1].decode())
                at += n + 2
        if record.name == 'LEDATA':
            block = (record.data[0], int.from_bytes(record.data[1:3], 'little'))
        if record.name != 'FIXUPP':
            continue
        need(block[0] == 1, 'all native fields are in CODE')
        at = 0
        while at < len(record.data):
            loc, low, method = record.data[at:at + 3]
            at += 3
            frame = record.data[at] if method == 0x16 else None
            at += int(frame is not None)
            index = record.data[at]
            at += 1
            site = block[1] + (loc & 3) * 256 + low
            far = method == 0x56
            width = 4 if far else 2
            need((loc, method, frame) == ((0xCC, 0x56, None) if far else (0xC4, 0x16, 1))
                 and site + width <= len(code), 'literal width/frame/external method')
            addend = int.from_bytes(code[site:site + width], 'little')
            fields.append((site, loc, method, frame, index, addend))
            name = names[index - 1]
            need(name in (CALLS if far else DATA), 'reviewed external identity')
            value = CALLS[name] if far else DATA[name] + addend
            need(not far or addend == 0, 'root far-call offset and zero segment addend')
            image[site:site + width] = value.to_bytes(width, 'little')
    need(tuple(names) == EXTERNALS[leaf] and tuple(fields) == FIELDS[leaf], 'complete literal ordered native field/name vector')
    return bytes(image), [dict(offset=s, locat=l, fixdat=m, frame=f, external=i, name=names[i-1], addend=a,
                                width=4 if m == 0x56 else 2) for s,l,m,f,i,a in fields]


def verify(work, target, candidate, graph, files):
    root = Path(__file__).resolve().parents[2]
    text = (work / 'obj/th03/mainl.map').read_text()
    owners, native = [], []
    for leaf, source, first, offset, size, procedures in PRODUCERS:
        obj, wrapper = 'obj/th03/' + leaf + '.obj', 'th03/' + leaf + '.cpp'
        raw = (work / obj).read_bytes()
        description = describe_omf(raw)
        need(description['valid'] and description['translator_comments'] == ['TC86 Borland C++ 4.02'], 'native TC4 identity')
        need(segment_definitions(raw) == [dict(index=1,name='SHARED',**{'class':'CODE'},overlay='',size=size),
             dict(index=2,name='_DATA',**{'class':'DATA'},overlay='',size=0),dict(index=3,name='_BSS',**{'class':'BSS'},overlay='',size=0)],
             'complete CODE and zero private DATA/BSS')
        need([r.data[0] for r in parse_omf(raw) if r.name == 'SEGDEF'] == [0x28,0x48,0x48]
             and [b['size'] for b in code_bytes(raw,1)[1]] == [size]
             and code_publics(raw,1) == [(a,n) for _,n,_,a,_,_ in procedures], 'native BYTE alignment / one record / all publics')
        row, = [r for r in graph if r['output'] == obj]
        need((row['wrapper'],row['source'],row['game'],row['binary'],row['first_binary'])
             == (wrapper,source,3,'O' if first == 'op' else 'L',first), 'actual first-use producer slot')
        need(source in description['dependency_paths'] and wrapper in description['dependency_paths']
             and files[source] == (work/source).read_bytes()
             and files[source].replace(b'\r\n',b'\n') == (root/source).read_bytes().replace(b'\r\n',b'\n'), 'current source consumption / transport')
        need(len(re.findall(rf'(?m)^\s*0C7E:{offset:04X}\s+{size:04X}\s+C=CODE\s+S=SHARED\s+G=\(none\)\s+M={re.escape(wrapper)}\s+ACBP=28\s*$',text)) == 1,
             'literal complete MAP allocation')
        image, fields = native_image(raw, leaf)
        start = CS*16 + offset
        need(image == target.program_image[start:start+size] == candidate.program_image[start:start+size], 'complete independently resolved native bytes')
        native.append(dict(object=obj, fields=fields, code_bytes=size, private_data_bytes=0, private_bss_bytes=0))
        for kind, symbol, mapname, at, count, args in procedures:
            body = image[at:at+count]
            need(len(re.findall(rf'(?m)^\s*0C7E:{offset+at:04X}\s+{re.escape(mapname)}\s*$',text)) == 2, 'both owner MAP publics')
            ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(body, offset+at))
            need(sum(i.size for i in ins) == count and (ins[-1].mnemonic,ins[-1].op_str) == ('retf',str(args)), 'complete far Pascal procedure')
            expected = [(CS,offset+f['offset']+2) for f in fields if f['width'] == 4 and at <= f['offset'] < at+count]
            for mz in (target,candidate):
                observed = [(r.segment,r.offset) for r in mz.relocations if start+at <= r.linear < start+at+count]
                need(observed == expected, 'literal ordered complete MZ relocation vector')
            h = hashlib.sha256(body).hexdigest()
            owners.append(dict(unit_id='th03-mainl-decoded-pi-'+kind,name=symbol,source=source,object=obj,
                start=start+at,size=count,segment=CS,offset=offset+at,coordinate_space='decoded-load',canonical_file_offset=None,
                target_sha256=h,candidate_sha256=h,ordered_relocations=[list(r) for r in expected],argument_bytes=args,callee_pop_bytes=args,
                private_data_bytes=0,private_bss_bytes=0,abi='far Pascal; unchecked WORD slot/coordinates; native frames and truncated far normalization'))
    for name, offset in DATA.items():
        need(len(re.findall(rf'(?m)^\s*0E3F:{offset:04X}\s+{name}\s*$',text)) == 2, 'both external DATA MAP publics')
    for name, offset in CALLS.items():
        need(len(re.findall(rf'(?m)^\s*0000:{offset:04X}\s+{name}\s*$',text)) == 2, 'both root dependency MAP publics')
    return dict(owners=owners, functions=5, code_bytes=555, native_objects=native,
                ordered_native_fields=sum(len(n['fields']) for n in native), mz_relocation_count=7,
                private_data_bytes=0,private_bss_bytes=0,library_context_accepted=False,whole_product_accepted=False)
