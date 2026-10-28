"""Complete natural Music Room initialized DATA and non-file-backed BSS layout."""
import hashlib
import re
import struct

from lib.omf import parse_omf
from lib.op_music_state_layout import DS, DATA, BSS, SOURCE, WRAPPER, OBJECT, native_image
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

UNIT = 'th03-op-decoded-music-data'
SIZE = 1008
DATA_PUBLICS = ((0, '_MUSIC_CHOICES'), (84, '_MUSIC_FILES'),
                (160, '_polygons_initialized'), (161, '_track_playing'))
BSS_PUBLICS = ((200, '_music_sel'), (201, '_music_page_accessed'),
               (202, '_nopoly_B'), (204, '_cmt_bg'), (220, '_cmt'))
BSS_DECLARATIONS = (
    ('points', 0, 40, 'screen_point_t[10]'),
    ('center', 40, 64, 'polygon_point_t[16]'),
    ('velocity', 104, 64, 'polygon_point_t[16]'),
    ('angle', 168, 16, 'unsigned char[16]'),
    ('angle_speed', 184, 16, 'unsigned char[16]'),
    ('music_sel', 200, 1, 'uint8_t'),
    ('music_page_accessed', 201, 1, 'page_t'),
    ('nopoly_B', 202, 2, 'segment-only pointer'),
    ('cmt_bg', 204, 16, 'four far pointers'),
    ('cmt', 220, 840, '20 records of42 bytes'),
)
BSS_REFERENCES = (0, 40, 42, 104, 106, 168, 184, 200, 201, 202,
                  204, 206, 208, 210, 212, 214, 216, 218, 220, 260)


def need(value, message):
    if not value:
        raise ValueError('OP Music storage: ' + str(message))


def semantic_data(work):
    """Evaluate the actual CP932 literal declarations, not a target-byte dump."""
    header = (work / 'th03/shiftjis/music.hpp').read_bytes().decode('cp932')
    bgm = (work / 'th03/shiftjis/bgm.hpp').read_bytes().decode('cp932')
    fns = (work / 'th03/shiftjis/fns.hpp').read_bytes().decode('cp932')
    macros = dict(re.findall(r'^#define\s+(TH03_\w+|BGM_MENU_MAIN_FN)\s+"([^"\\]*)"\s*$', bgm + fns, re.M))
    def strings(name):
        body, = re.findall(r'\b' + name + r'\[\]\s*=\s*\{(.*?)\};', header, re.S)
        result = []
        for line in body.splitlines():
            line = line.split('//')[0].strip().rstrip(',')
            if not line:
                continue
            literal = re.fullmatch(r'"([^"\\]*)"(?:\s+(TH03_\w+))?', line)
            need(literal is not None or line in macros, 'reviewed literal initializer: ' + name)
            result.append(literal[1] + (macros[literal[2]] if literal[2] else '') if literal else macros[line])
        return result
    choices, files = strings('MUSIC_CHOICES'), strings('MUSIC_FILES')
    need(len(choices) == 21 and len(files) == 19, 'complete21/19 far-pointer arrays')
    need(all(len(s.encode('cp932')) == 32 for s in choices), 'all21 display rows contain32 CP932 bytes')
    need(choices[19] == ' ' * 11 + '\u3000' * 2 + ' ' * 17 and 'Ｑｕｉｔ' in choices[20], 'blank19 and Quit20')
    source = (work / SOURCE).read_bytes()
    need(b'bool polygons_initialized = false;' in source and b'uint8_t track_playing = 0;' in source,
         'two explicit BYTE zero initializers')
    image = bytearray((len(choices) + len(files)) * 4 + 2)
    pointers, literals = [], []
    for i, text in enumerate(choices + files):
        offset = len(image)
        raw = text.encode('cp932') + b'\0'
        image.extend(raw)
        struct.pack_into('<HH', image, i * 4, offset, 0)
        pointers.append(offset)
        literals.append(dict(kind='choice' if i < 21 else 'filename', index=i if i < 21 else i - 21,
                             offset=offset, size=len(raw), text=text))
    for text in ('MUSIC.TXT', 'op3.pi'):
        raw = text.encode('ascii') + b'\0'
        literals.append(dict(kind='loader filename', offset=len(image), size=len(raw), text=text))
        image.extend(raw)
    need(len(image) == SIZE, 'complete natural DATA image; no unnamed holes')
    return bytes(image), pointers, literals


def verify(root, work, target, candidate):
    native = (work / OBJECT).read_bytes()
    native_image(native)  # Whole producer records, segments and all CODE publics.
    data, blocks = code_bytes(native, 2)
    semantic, pointers, literals = semantic_data(work)
    need([(b['offset'], b['size']) for b in blocks] == [(0, SIZE)] and data == semantic,
         'complete semantic/native initialized DATA')
    need(tuple(code_publics(native, 2)) == DATA_PUBLICS and tuple(code_publics(native, 3)) == BSS_PUBLICS,
         'all initialized/BSS public boundaries')
    image, fields, bss_fields, block = bytearray(data), [], [], None
    for record in parse_omf(native):
        if record.name == 'LEDATA':
            block = record.data[0], int.from_bytes(record.data[1:3], 'little'), record.data[3:]
            need(block[0] != 3, 'BSS has no file-backed initializer')
        elif record.name == 'FIXUPP':
            at = 0
            while at < len(record.data):
                loc, low, method = record.data[at:at + 3]
                at += 3
                need(method in (20, 22, 86), 'native field form')
                frame = None
                if method in (20, 22):
                    frame = record.data[at]
                    at += 1
                index = record.data[at]
                at += 1
                site = (loc & 3) * 256 + low
                if block[0] == 1 and method == 20 and index == 3:
                    bss_fields.append(int.from_bytes(block[2][site:site + 2], 'little'))
                if block[0] != 2:
                    continue
                site += block[1]
                need(loc == 0xCC and method == 20 and frame == 1 and index == 2 and site % 4 == 0 and site < 160,
                     'ordinary DGROUP far pointer to own DATA')
                addend = int.from_bytes(data[site:site + 4], 'little')
                fields.append([site, 4, loc, method, frame, index, addend])
                image[site:site + 4] = struct.pack('<HH', DATA + addend, DS)
    need(fields == [[i * 4, 4, 0xCC, 20, 1, 2, pointers[i]] for i in range(39, -1, -1)],
         'all40 literal native far fields in emitted order')
    need(tuple(sorted(set(bss_fields))) == BSS_REFERENCES, 'all native CODE BSS field addends')
    start, end = DS * 16 + DATA, DS * 16 + DATA + SIZE
    need(bytes(image) == target.program_image[start:end] == candidate.program_image[start:end],
         'complete semantic/native/target/candidate DATA')
    relocations = [[DS, DATA + f[0] + 2] for f in fields]
    for executable in (target, candidate):
        need([[r.segment, r.offset] for r in executable.relocations if start <= r.linear < end] == relocations,
             'complete literal ordered DATA relocation vector')
        need(not any(r.linear < start < r.linear + 2 or r.linear < end < r.linear + 2 for r in executable.relocations),
             'no straddling DATA relocation')
        for load in (0x1000, 0x3000):
            loaded = bytearray(image)
            for f in fields:
                struct.pack_into('<H', loaded, f[0] + 2, DS + load)
            need(executable.relocated_program_image(load)[start:end] == bytes(loaded), 'complete relocated DATA at both loads')
    table = (work / 'obj/th03/op.map').read_text()
    for base, publics in ((DATA, DATA_PUBLICS), (BSS, BSS_PUBLICS)):
        for offset, name in publics:
            need(len(re.findall(rf'(?m)^\s*{DS:04X}:{base + offset:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$', table)) == 2,
                 'both storage MAP public tables: ' + name)
    need(len(re.findall(rf'(?m)^\s*{DS:04X}:{DATA:04X}\s+03F0\s+C=DATA\s+S=_DATA\s+G=DGROUP\s+M=th03/op_music\.cpp\s+ACBP=48\s*$', table)) == 1,
         'complete DATA MAP contribution')
    need(len(re.findall(rf'(?m)^\s*{DS:04X}:{BSS:04X}\s+0424\s+C=BSS\s+S=_BSS\s+G=DGROUP\s+M=th03/op_music\.cpp\s+ACBP=48\s*$', table)) == 1,
         'complete non-file-backed BSS MAP contribution')
    need([offset for _, offset, _, _ in BSS_DECLARATIONS] ==
         [sum(size for _, _, size, _ in BSS_DECLARATIONS[:i]) for i in range(len(BSS_DECLARATIONS))] and
         sum(size for _, _, size, _ in BSS_DECLARATIONS) == 1060, 'entire BSS declaration layout without holes')
    digest = hashlib.sha256(image).hexdigest()
    owner = dict(unit_id=UNIT, name='Music Room initialized DATA', source=SOURCE, object=OBJECT,
        segment=DS, offset=DATA, start=start, size=SIZE, coordinate_space='decoded-load', canonical_file_offset=None,
        target_sha256=digest, candidate_sha256=digest, ordered_relocations=relocations,
        procedure_count=0, procedures=[], code_bytes=0, initialized_data_bytes=SIZE, private_data_bytes=SIZE,
        private_bss_bytes=0, abi='40 ordinary32-bit far DATA pointers; two BYTE initializers; CP932 literal pool')
    return dict(owners=[owner], initialized_data_bytes=SIZE, code_bytes=0, procedures=0,
        ordered_native_fields=fields, ordered_relocations=relocations, literals=literals, initialized_holes=0,
        bss_layout_reviewed=True, bss_file_backed=False, bss_bytes=1060, BSS_extent=[DS, BSS, 1060],
        bss_declarations=[dict(name=n, offset=o, size=s, type=t) for n, o, s, t in BSS_DECLARATIONS],
        bss_publics=[list(p) for p in BSS_PUBLICS], native_CODE_BSS_addends=list(BSS_REFERENCES),
        BSS_raw_byte_credit=0, whole_product_accepted=False)


if __name__ == '__main__':
    import json
    from pathlib import Path
    from review_th03_op_cfg_work import images
    from review_th03_op_music_menu_work import examine
    repository = Path(__file__).resolve().parents[2]
    examine(repository)  # Current complete native source/tool/output graph.
    work, target, candidate, *_ = images(repository)
    print(json.dumps(verify(repository, work, target, candidate), indent=2))
