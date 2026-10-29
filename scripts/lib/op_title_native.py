"""Complete current TC4 title producer, including its native column restore."""
import hashlib
import re

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

CS, DS, BASE, SIZE, DATA = 0x990, 0xD7F, 0x14E2, 902, 0x9E2
OBJECT, WRAPPER, INCLUDE = 'obj/th03/op_main.obj', 'th03/op_main.cpp', 'th03/op/m_main.cpp'
SOURCE, COLUMN = 'src/op/menu/title_animation.inl', 'src/op/menu/column_restore.inl'
SOURCES = {SOURCE, COLUMN}
TITLE_UNIT, COLUMN_UNIT = 'th03-op-decoded-title-animation', 'th03-op-decoded-title-column'
PROCEDURES = (
    (0, '@op_animate$qv', 550, 0, 'op_animate()'),
    (550, '@op_fadein_animate$qv', 167, 0, 'op_fadein_animate()'),
    (717, '@box_main_to_submenu_animate$qv', 44, 0, 'box_main_to_submenu_animate()'),
    (761, '@box_submenu_to_main_animate$qv', 47, 0, 'box_submenu_to_main_animate()'),
    (808, '@BOX_COLUMN16_UNPUT$QUI', 94, 2, 'box_column16_unput(unsigned int)'),
)
ALIASES = {
    '@FRAME_DELAY$QI': 'frame_delay(int)', '@PI_LOAD$QINXC': 'pi_load(int,const char far*)',
    '@PI_PALETTE_APPLY$QI': 'pi_palette_apply(int)', '@PI_PUT_8$QIII': 'pi_put_8(int,int,int)',
    '@select_cdg_load_part1_of_4$qv': 'select_cdg_load_part1_of_4()',
    '@select_cdg_load_part3_of_4$qv': 'select_cdg_load_part3_of_4()',
}


def need(value, message):
    if not value:
        raise ValueError('OP title native: ' + str(message))


def address(table, name):
    name = ALIASES.get(name, name)
    rows = re.findall(rf'(?m)^\s*([0-9A-F]{{4}}):([0-9A-F]{{4}})\s+(?:idle\s+)?{re.escape(name)}\s*$', table)
    need(len(rows) == 2 and rows[0] == rows[1], 'both MAP public tables: ' + name)
    return tuple(int(v, 16) for v in rows[0])


def resolve(raw, table):
    code, blocks = code_bytes(raw, 1)
    need([(b['offset'], b['size']) for b in blocks] == [(0, SIZE)], 'complete natural CODE record')
    image, names, fields, relocations, block = bytearray(code), [], [], [], None
    for record in parse_omf(raw):
        if record.name == 'EXTDEF':
            at = 0
            while at < len(record.data):
                length = record.data[at]
                names.append(record.data[at + 1:at + 1 + length].decode())
                at += length + 1
                need(record.data[at] == 0, 'untyped external identity')
                at += 1
        elif record.name == 'LEDATA':
            block = record.data[0], int.from_bytes(record.data[1:3], 'little')
        elif record.name == 'FIXUPP':
            need(block == (1, 0), 'only CODE has native fixups')
            at = 0
            while at < len(record.data):
                loc, low, method = record.data[at:at + 3]
                at += 3
                need(method in (20, 22, 86), 'literal supported native field')
                frame = None
                if method in (20, 22):
                    frame = record.data[at]
                    at += 1
                index = record.data[at]
                at += 1
                site, kind = (loc & 3) * 256 + low, loc >> 2 & 15
                width = 4 if kind == 3 else 2
                need(loc & 0x80 and kind in (1, 3) and site + width <= SIZE, 'complete native field')
                addend = int.from_bytes(code[site:site + width], 'little')
                name = None
                if method == 20:
                    need(frame == 1 and index == 2 and kind == 1 and loc & 0x40 and addend < 31,
                         'own string-pool field in sole native DGROUP')
                    value = DATA + addend
                else:
                    need(1 <= index <= len(names), 'external index')
                    name = names[index - 1]
                    seg, offset = address(table, name)
                    if method == 22:
                        need(frame == 1 and kind == 1 and loc & 0x40 and seg == DS, 'external DGROUP field')
                        value = offset + addend
                    elif kind == 1:
                        need(not loc & 0x40 and addend == 0 and seg == CS and code[site - 1] == 0xE8,
                             'genuine external self-relative near CALL')
                        value = (offset - (BASE + site + 2)) & 65535
                    else:
                        need(loc & 0x40 and addend == 0 and seg != CS and code[site - 1] == 0x9A,
                             'ordinary unrelaxed far CALL')
                        value = (seg << 16) | offset
                        relocations.append([CS, BASE + site + 2])
                image[site:site + width] = value.to_bytes(width, 'little')
                fields.append(dict(site=site, width=width, locat=loc, method=method, frame=frame,
                                   target=index, name=name, addend=addend))
    return bytes(image), fields, relocations


def verify(root, work, target, candidate, files):
    raw = (work / OBJECT).read_bytes()
    native = describe_omf(raw)
    need(native['valid'] and native['module_name'] == WRAPPER and
         native['translator_comments'] == ['TC86 Borland C++ 4.02'], 'actual complete TC4 producer')
    need(segment_definitions(raw) == [dict(index=i, name=n, **{'class': c}, overlay='', size=s)
         for i, n, c, s in ((1, 'OP_MAIN_TEXT', 'CODE', SIZE), (2, '_DATA', 'DATA', 31), (3, '_BSS', 'BSS', 0))],
         'complete natural segment layout')
    need([r.data for r in parse_omf(raw) if r.name == 'GRPDEF'] == [bytes((8, 255, 2, 255, 3))],
         'native group1 is DGROUP over DATA/BSS; CODE has no OMF group')
    need(tuple(code_publics(raw, 1)) == tuple((off, symbol) for off, symbol, *_ in PROCEDURES) and
         not code_publics(raw, 2) and not code_publics(raw, 3), 'all native public boundaries')
    need(files[WRAPPER] == ('#include "' + INCLUDE + '"\n').encode() and
         files[INCLUDE] == ('#include "' + SOURCE + '"\n\n#include "' + COLUMN + '"\n').encode(),
         'literal two-include maintained source chain')
    deps = [n.replace(chr(92), '/') for n in native['dependency_paths']]
    need(all(n in files and (work / n).read_bytes() == files[n] for n in deps) and
         all(n in deps for n in (WRAPPER, INCLUDE, SOURCE, COLUMN)), 'actual complete native source/header binding')
    need(all(files[n] == (root / n).read_bytes() for n in SOURCES), 'current maintained source')
    table = (work / 'obj/th03/op.map').read_text()
    for seg, base, size, cls, name, acbp in (
        (CS, BASE, SIZE, 'CODE', 'OP_MAIN_TEXT', '28'),
        (DS, DATA, 31, 'DATA', '_DATA', '48'), (DS, 0x2394, 0, 'BSS', '_BSS', '48')):
        group = 'GROUP_01' if cls == 'CODE' else 'DGROUP'
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{base:04X}\s+{size:04X}\s+C={cls}\s+S={name}\s+G={group}\s+M=th03/op_main\.cpp\s+ACBP={acbp}\s*$', table)) == 1,
             'complete native MAP contribution: ' + cls)
    code, fields, relocs = resolve(raw, table)
    start = CS * 16 + BASE
    need(code == target.program_image[start:start + SIZE] == candidate.program_image[start:start + SIZE],
         'complete independently resolved native/target/candidate bytes')
    for executable in (target, candidate):
        need([[r.segment, r.offset] for r in executable.relocations if start <= r.linear < start + SIZE] == relocs,
             'complete literal ordered MZ vector')
        need(not any(r.linear < start < r.linear + 2 or r.linear < start + SIZE < r.linear + 2
                     for r in executable.relocations), 'no straddling relocation')
    decoded = []
    need([off for off, *_ in PROCEDURES] == [sum(p[2] for p in PROCEDURES[:i]) for i in range(5)] and
         sum(p[2] for p in PROCEDURES) == SIZE, 'complete contiguous procedure partition')
    for off, symbol, length, cleanup, mapname in PROCEDURES:
        need(address(table, mapname) == (CS, BASE + off), 'native public MAP address')
        instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(code[off:off + length], BASE + off))
        need(sum(i.size for i in instructions) == length and instructions[-1].mnemonic == 'ret' and
             (int(instructions[-1].op_str, 0) if instructions[-1].op_str else 0) == cleanup,
             'complete near procedure/argument cleanup: ' + symbol)
        decoded.append(dict(name=mapname, offset=off, size=length, callee_pop_bytes=cleanup,
                            instruction_count=len(instructions)))
    owners = []
    for unit, source, begin, length, procedures in (
        (TITLE_UNIT, SOURCE, 0, 808, decoded[:4]), (COLUMN_UNIT, COLUMN, 808, 94, decoded[4:])):
        digest = hashlib.sha256(code[begin:begin + length]).hexdigest()
        owners.append(dict(unit_id=unit, name='Title/menu animations' if begin == 0 else procedures[0]['name'],
            source=source, object=OBJECT, segment=CS, offset=BASE + begin, start=start + begin, size=length,
            coordinate_space='decoded-load', canonical_file_offset=None, target_sha256=digest, candidate_sha256=digest,
            ordered_relocations=[r for r in relocs if BASE + begin <= r[1] < BASE + begin + length],
            procedure_count=len(procedures), procedures=procedures, code_bytes=length, initialized_data_bytes=0,
            private_data_bytes=0, private_bss_bytes=0, forwarding_chain=[WRAPPER, INCLUDE, source],
            abi='near C; column near Pascal pop2 with compiler-owned BP/SI/DI saves'))
    return dict(owners=owners, code_bytes=SIZE, procedures=5, native_fields=fields, ordered_relocations=relocs,
                containing_DATA_bytes=31, containing_DATA_accepted=False, BSS_bytes=0,
                column_raw_equal=True, runtime_matrix_required=False, whole_product_accepted=False)


if __name__ == '__main__':
    import json
    from pathlib import Path
    import build_th03_op_work as build
    from review_th03_op_cfg_work import images
    from lib.op_startup_cold import verify as cold_graph
    root = Path(__file__).resolve().parents[2]
    work, target, candidate, cold, cold_raw = images(root)
    cold_graph(root, work, target, candidate, cold)
    print(json.dumps(dict(cold_report_sha256=hashlib.sha256(cold_raw).hexdigest(),
                         scope=verify(root, work, target, candidate, build.source_graph())), indent=2))
