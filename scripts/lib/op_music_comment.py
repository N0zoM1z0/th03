"""Native byte, OMF and relocation checks for Music Room copy/comment helpers."""
import hashlib
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.op_music_polygon import layout as polygon_layout
from lib.op_music_state_layout import CS, DS, START as CARRIER, OBJECT, native_image
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_bytes

RANGES = ((CARRIER + 216, 30), (CARRIER + 891, 877))
PLANE = 0x19FA


def need(value, message):
    if not value:
        raise ValueError('OP Music comments native check: ' + str(message))


def layout(root, work, target, candidate):
    raw = (work / OBJECT).read_bytes()
    native_image(raw)
    polygon_layout(root, work, target, candidate)  # Whole containing MAP and context geometry.
    code, _ = code_bytes(raw, 1)
    image = bytearray(code)
    names, fields, relocs, block = [], [], [], None
    externals = {1: ('_VRAM_PLANE', DS, PLANE), 2: ('_VRAM_PLANE_B', DS, PLANE), 3: ('HMEM_ALLOCBYTE', 0, 0x24CA),
        4: ('HMEM_FREE', 0, 0x25CE), 8: ('FILE_ROPEN', 0, 0x9A8), 9: ('FILE_READ', 0, 0x8F4),
        10: ('FILE_SEEK', 0, 0x9E4), 11: ('FILE_CLOSE', 0, 0x888),
        12: ('@FRAME_DELAY_2$QI', 0xBEB, 0xCD6), 15: ('@GRAPH_PUTSA_FX$QIIINXUC', 0xBEB, 0x82B),
        22: ('GRCG_SETCOLOR', 0, 0xEC6), 23: ('GRCG_OFF', 0, 0xEF0)}
    def owned(site):
        return any(start - CARRIER <= site < start - CARRIER + size for start, size in RANGES)
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
                if not owned(site):
                    continue
                need(owned(site + width - 1), 'whole scoped field')
                addend = int.from_bytes(code[site:site + width], 'little')
                fields.append([site, width, loc, method, frame, index, addend])
                if method == 20:
                    need(frame == 1 and width == 2 and index in (2, 3), 'DGROUP local field')
                    value = {2: 0x5F2, 3: 0x1F70}[index] + addend
                else:
                    name, segment, offset = externals[index]
                    need(names[index - 1] == name, 'exact external identity')
                    if method == 22:
                        need(frame == 1 and width == 2 and index in (1, 2), 'VRAM far-pointer storage field')
                        value = offset + addend
                    else:
                        need(width == 4 and code[site - 1] == 0x9A, 'ordinary far CALL')
                        value = (segment << 16) + offset + addend
                        relocs.append([CS, 0xC1E + site + 2])
                image[site:site + width] = value.to_bytes(width, 'little')
    instructions, digest = [], hashlib.sha256()
    for start, size in RANGES:
        body = bytes(image[start - CARRIER:start - CARRIER + size])
        need(body == target.program_image[start:start + size] == candidate.program_image[start:start + size], 'complete native/target/candidate bytes')
        rows = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(body, start))
        need(sum(i.size for i in rows) == size, 'whole instruction partition')
        instructions.extend(rows)
        digest.update(body)
    for mz in (target, candidate):
        need([[r.segment, r.offset] for r in mz.relocations if owned(r.linear - CARRIER)] == relocs, 'literal ordered MZ relocations')
        need(not any(owned(r.linear - CARRIER) != owned(r.linear + 1 - CARRIER) for r in mz.relocations), 'no straddling relocation')
    need((len(fields), len(relocs), len(instructions)) == (63, 14, 315), 'complete native field/instruction counts')
    return dict(code_bytes=907, procedures=7, native_fields=fields, ordered_relocations=relocs,
        instruction_count=len(instructions), raw_sha256=digest.hexdigest(), ranges=[list(r) for r in RANGES],
        source='src/op/music/animation_and_menu.inl;src/op/music/nopoly_blit.inl', object=OBJECT,
        source_ownership_promoted=False, whole_product_accepted=False)
