"""Native byte, OMF, MAP and relocation checks for the Music Room polygons."""
import hashlib
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.op_music_state_layout import CS, DS, START as CARRIER, OBJECT, native_image, verify as carrier_layout
from probe_th03_main_boss_marisa_cpp import code_bytes
from lib.omf import parse_omf

START, SIZE = CARRIER + 246, 645
RANDOM, RENDER = 0x1D12, 0xC6A


def need(value, message):
    if not value:
        raise ValueError('OP Music polygon native check: ' + str(message))


def layout(root, work, target, candidate):
    """Resolve native fields, never patching an object or executable."""
    raw = (work / OBJECT).read_bytes()
    carrier_layout(root, work, target, candidate)  # Entire producer MAP/public geometry.
    native_image(raw)  # Complete natural carrier records, segments and publics.
    code, _ = code_bytes(raw, 1)
    image = bytearray(code[246:891])
    names, fields, relocations, block = [], [], [], None
    externals = {5: ('_SinTable8', DS, 0x316), 6: ('_CosTable8', DS, 0x396),
                 7: ('IRAND', 0, RANDOM), 19: ('@polar$qiii', 0xBEB, 0x155),
                 24: ('GRCG_POLYGON_C', 0, RENDER)}
    for record in parse_omf(raw):
        if record.name == 'EXTDEF':
            at = 0
            while at < len(record.data):
                length = record.data[at]
                at += 1
                names.append(record.data[at:at + length].decode())
                at += length
                need(record.data[at] == 0, 'untyped external')
                at += 1
        elif record.name == 'LEDATA':
            block = record.data[0], int.from_bytes(record.data[1:3], 'little')
        elif record.name == 'FIXUPP' and block[0] == 1:
            at = 0
            while at < len(record.data):
                loc, low, method = record.data[at:at + 3]
                at += 3
                frame = None
                need(method in (20, 22, 86), 'native field form')
                if method in (20, 22):
                    frame = record.data[at]
                    at += 1
                index = record.data[at]
                at += 1
                site = block[1] + (loc & 3) * 256 + low
                width = 4 if (loc >> 2 & 15) == 3 else 2
                if not 246 <= site < 891:
                    continue
                need(site + width <= 891, 'complete scoped field')
                addend = int.from_bytes(code[site:site + width], 'little')
                fields.append([site, width, loc, method, frame, index, addend])
                if method == 20:
                    need(frame == 1 and width == 2 and index in (2, 3), 'DGROUP field')
                    value = {2: 0x5F2, 3: 0x1F70}[index] + addend
                else:
                    name, segment, offset = externals[index]
                    need(names[index - 1] == name, 'external identity')
                    if method == 22:
                        need(frame == 1 and width == 2 and index in (5, 6), 'trigonometry DATA field')
                        value = offset + addend
                    else:
                        need(width == 4 and code[site - 1] == 0x9A and index in (7, 19, 24), 'ordinary far CALL')
                        value = (segment << 16) + offset + addend
                        relocations.append([CS, 0xC1E + site + 2])
                image[site - 246:site - 246 + width] = value.to_bytes(width, 'little')
    need(len(fields) == 54 and len(relocations) == 14, 'complete native field/relocation counts')
    need(bytes(image) == target.program_image[START:START + SIZE] == candidate.program_image[START:START + SIZE],
         'complete independently resolved native/target/candidate bytes')
    for mz in (target, candidate):
        need([[r.segment, r.offset] for r in mz.relocations if START <= r.linear < START + SIZE] == relocations,
             'literal ordered MZ relocation vector')
        need(not any(r.linear < START < r.linear + 2 or r.linear < START + SIZE < r.linear + 2 for r in mz.relocations),
             'no straddling relocation')
    instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(image, START))
    need(sum(i.size for i in instructions) == SIZE, 'whole instruction partition')
    return dict(code_bytes=SIZE, procedures=2, native_fields=fields, ordered_relocations=relocations,
                instruction_count=len(instructions), raw_sha256=hashlib.sha256(image).hexdigest(),
                source='src/op/music/animation_and_menu.inl', object=OBJECT,
                source_ownership_promoted=False, whole_product_accepted=False)
