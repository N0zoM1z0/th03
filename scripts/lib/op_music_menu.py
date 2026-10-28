"""Native byte, OMF, MAP, far ABI and relocation checks for the Music Room menu."""
import hashlib
import re
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.op_music_comment import layout as dependencies_layout
from lib.op_music_state_layout import CS, DS, START as CARRIER, OBJECT
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_bytes

START, SIZE = CARRIER + 1768, 476
KEY = 0x1AA6


def need(value, message):
    if not value:
        raise ValueError('OP Music menu native check: ' + str(message))


def layout(root, work, target, candidate):
    dependencies_layout(root, work, target, candidate)
    raw = (work / OBJECT).read_bytes()
    code, _ = code_bytes(raw, 1)
    body = bytearray(code[1768:2244])
    declarations = {
        13: ('_input_sp', DS, KEY), 14: ('@INPUT_MODE_INTERFACE$QV', 0xBEB, 0xAD6),
        16: ('SND_KAJA_INTERRUPT', 0xBEB, 0x553), 17: ('_snd_load', 0xBEB, 0xA2),
        18: ('CDG_FREE', 0xBEB, 0x7EC), 20: ('GRAPH_CLEAR', 0, 0x114C),
        21: ('GRAPH_COPY_PAGE', 0, 0x1186), 25: ('PALETTE_SHOW', 0, 0x1AA4),
        26: ('_PaletteTone', DS, 0x2D4), 27: ('GRAPH_PI_FREE', 0, 0x12DC),
        28: ('SUPER_FREE', 0, 0x269A), 29: ('TEXT_CLEAR', 0, 0x21F4),
        30: ('_pi_headers', DS, 0x1CC0), 31: ('_pi_buffers', DS, 0x1CA8),
        32: ('@PI_LOAD$QINXC', 0xBEB, 0xA90), 33: ('@PI_PALETTE_APPLY$QI', 0xBEB, 0x4A6),
        34: ('@PI_PUT_8$QIII', 0xBEB, 0x4CB)}
    names, fields, relocs, block = [], [], [], None
    for rec in parse_omf(raw):
        if rec.name == 'EXTDEF':
            at = 0
            while at < len(rec.data):
                length = rec.data[at]
                at += 1
                names.append(rec.data[at:at + length].decode())
                at += length
                need(rec.data[at] == 0, 'untyped external')
                at += 1
        elif rec.name == 'LEDATA':
            block = rec.data[0], int.from_bytes(rec.data[1:3], 'little')
        elif rec.name == 'FIXUPP' and block[0] == 1:
            at = 0
            while at < len(rec.data):
                loc, low, method = rec.data[at:at + 3]
                at += 3
                frame = None
                need(method in (20, 22, 86), 'native field form')
                if method in (20, 22):
                    frame = rec.data[at]
                    at += 1
                index = rec.data[at]
                at += 1
                site = block[1] + (loc & 3) * 256 + low
                width = 4 if loc >> 2 & 15 == 3 else 2
                if not 1768 <= site < 2244:
                    continue
                need(site + width <= 2244, 'whole native field')
                addend = int.from_bytes(code[site:site + width], 'little')
                fields.append([site, width, loc, method, frame, index, addend])
                if method == 20:
                    need(frame == 1 and width == 2 and index in (2, 3), 'DGROUP local')
                    value = {2: 0x5F2, 3: 0x1F70}[index] + addend
                else:
                    name, segment, offset = declarations[index]
                    need(names[index - 1] == name, 'exact native external identity')
                    if method == 22:
                        need(frame == 1 and width == 2 and index in (13, 26, 30, 31), 'DGROUP external storage')
                        value = offset + addend
                    else:
                        need(width == 4 and code[site - 1] == 0x9A, 'ordinary far CALL')
                        value = (segment << 16) + offset + addend
                        relocs.append([CS, 0xC1E + site + 2])
                body[site - 1768:site - 1768 + width] = value.to_bytes(width, 'little')
    need(len(fields) == 57 and len(relocs) == 18, 'complete field/relocation vectors')
    need(bytes(body) == target.program_image[START:START + SIZE] == candidate.program_image[START:START + SIZE], 'complete native/target/candidate menu bytes')
    for mz in (target, candidate):
        need([[r.segment, r.offset] for r in mz.relocations if START <= r.linear < START + SIZE] == relocs, 'literal ordered MZ vector')
        need(not any(r.linear < START < r.linear + 2 or r.linear < START + SIZE < r.linear + 2 for r in mz.relocations), 'no straddling relocation')
    table = (work / 'obj/th03/op.map').read_text()
    need(len(re.findall(r'(?m)^\s*0990:1306\s+(?:idle\s+)?musicroom_menu\(\)\s*$', table)) == 2, 'both complete menu MAP publics')
    rows = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(body, START))
    need(sum(i.size for i in rows) == SIZE and rows[-1].mnemonic == 'retf', 'whole far procedure')
    return dict(procedures=1, code_bytes=SIZE, instruction_count=len(rows), native_fields=fields,
        ordered_relocations=relocs, raw_sha256=hashlib.sha256(body).hexdigest(),
        source='src/op/music/animation_and_menu.inl', object=OBJECT,
        source_ownership_promoted=False, whole_product_accepted=False)
