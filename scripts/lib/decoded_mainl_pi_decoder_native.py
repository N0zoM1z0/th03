"""Whole current MAINL master.lib PI decoder, including its shared error exit."""
import hashlib
import re

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.omf import parse_omf
from lib.op_asset_native import extent
from lib.op_shared_native import address
from lib.decoded_mainl_root_helpers_layout import native as root_native, CODE_BASE, DATA_BASE, DS, OBJECT, WRAPPER
from lib.mainl_staff_source import statements

SOURCE = 'src/mainl/formats/pi_decode.asm'
PROVIDER = 'libs/master.lib/graph_pi_load_pack.asm'
UNIT = 'th03-mainl-decoded-pi-decoder-load'
START, SIZE = 0x1038, 1524
PARTS = (('shared error exit', 0x1038, 11, 'retf', '12'),
         ('graph_pi_load_pack', 0x1044, 1211, 'retf', '12'),
         ('_read_color', 0x1500, 238, 'ret', ''),
         ('byte_load', 0x15EE, 44, 'ret', ''),
         ('_buffer_load', 0x161A, 18, 'ret', ''))
EVENS = (0x1043, 0x14FF)
FIELDS = ((0x103C, 0xC9, 0x55, 1, 0), (0x1120, 0xC9, 0x55, 1, 0),
          (0x1179, 0xCA, 0x55, 1, 0), (0x1125, 0xC5, 0x54, 2, 0x744),
          (0x117E, 0xC6, 0x54, 2, 0x744), (0x14EC, 0xC9, 0x55, 1, 0))
BRIDGES = {0x1052: 0xAAE, 0x105E: 0x1EC0, 0x112B: 0x210A, 0x1184: 0x210A, 0x14F2: 0x1EAA}
LIBRARY_ORIGINS = (
    ('th03-mainl-decoded-root-tail-keyclear', 'src/mainl/root_tail/dos_keyclear.asm', 'dos_keyclear.asm', 6),
    ('th03-mainl-decoded-root-tail-grcg', 'src/mainl/root_tail/grcg_setcolor.asm', 'grcg_setcolor.asm', 41),
    ('th03-mainl-decoded-root-tail-grcg-off', 'src/mainl/root_tail/grcg_setcolor.asm', 'grcg_setcolor.asm', 5),
    ('th03-mainl-decoded-root-tail-rand', 'src/mainl/root_tail/random.asm', 'random.asm', 42),
    ('th03-mainl-decoded-root-tail-string-compare', 'src/mainl/root_tail/pf_str_ieq.asm', 'pf_str_ieq.asm', 56),
    ('th03-mainl-decoded-pi-decoder-free', 'src/mainl/resources/graph_pi_free.asm', 'graph_pi_free.asm', 76),
)


def need(value, message):
    if not value:
        raise ValueError('MAINL PI decoder native: ' + str(message))


def review_library_origins(root, files, owners):
    reviews = []
    for unit, source, provider, size in LIBRARY_ORIGINS:
        owner, = [o for o in owners if o['unit_id'] == unit]
        need(owner['source'] == source and owner['size'] == size and
             files[source].replace(b'\r\n', b'\n') == (root / source).read_bytes().replace(b'\r\n', b'\n') and
             statements(files[source]) == statements(files['libs/master.lib/' + provider]),
             'complete unmodified master.lib source lineage for previous owner: ' + unit)
        owner['origin'] = 'library'
        reviews.append(dict(unit_id=unit, source=source, provider='libs/master.lib/' + provider,
                            bytes=size, native_owner_fields_unchanged=True))
    return reviews


def verify(root, work, target, candidate, graph, files):
    raw = (work / OBJECT).read_bytes()
    _, description = root_native(raw)  # Actual whole containing producer geometry.
    records = parse_omf(raw)
    need([r.data for r in records if r.name == 'GRPDEF'] ==
         [bytes((20, 255, 9, 255, 2)), bytes((21, 255, 7, 255, 6, 255, 5, 255, 4, 255, 3))],
         'root group1 is DGROUP over actual BSS/DATA; group2 is independent game CODE')
    row, = [r for r in graph if r['output'] == OBJECT]
    need((row['source'], row['wrapper'], row['kind'], row['game'], row['binary'], row['first_binary']) ==
         (WRAPPER, WRAPPER, 'tasm', 3, 'L', 'mainl'), 'actual maintained GAME3/L TASM containing producer')
    need(files[WRAPPER].count(('include ' + SOURCE).encode()) == 1 and
         SOURCE in description['dependency_paths'] and
         files[SOURCE].replace(b'\r\n', b'\n') == (root / SOURCE).read_bytes().replace(b'\r\n', b'\n'),
         'literal maintained decoder include and declared line-ending transport')
    need(statements(files[PROVIDER]) == statements(files[SOURCE]), 'complete symbolic original master.lib source lineage')
    need(all(n in files and (work / n).read_bytes() == files[n] for n in description['dependency_paths']),
         'complete actual root macro/header/provider closure')
    begin, end = START - CODE_BASE, START - CODE_BASE + SIZE
    data, block = {}, None
    for r in records:
        if r.name == 'LEDATA':
            block = r.data[0], int.from_bytes(r.data[1:3], 'little')
            if block[0] != 1:
                continue
            for i, byte in enumerate(r.data[3:]):
                site = block[1] + i
                if begin <= site < end:
                    need(site not in data, 'nonoverlapping scoped native LEDATA')
                    data[site] = byte
    need(set(data) == set(range(begin, end)), 'complete1524-byte native coverage without implicit fill')
    code = bytes(data[i] for i in range(begin, end))
    image, fields, relocs = bytearray(code), [], []
    for r in records:
        if r.name == 'LEDATA':
            block = r.data[0], int.from_bytes(r.data[1:3], 'little')
        elif r.name == 'FIXUPP':
            at = 0
            while at < len(r.data):
                loc, low, method = r.data[at:at + 3]
                at += 3
                need(loc & 128 and method & ~3 in (4, 20, 84) and method & 3 < 3, 'literal unthreaded root field grammar')
                frame = None
                if method & ~3 in (4, 20):
                    frame = r.data[at]
                    at += 1
                index = r.data[at]
                at += 1
                width = {1: 2, 2: 2, 3: 4}[loc >> 2 & 15]
                site = block[1] + (loc & 3) * 256 + low
                if block[0] != 1 or not begin <= site < end:
                    need(block[0] != 1 or not any(site < b < site + width for b in (begin, end)), 'no straddling native field')
                    continue
                offset = site - begin
                addend = int.from_bytes(code[offset:offset + width], 'little')
                need(width == 2 and loc & 0x40 and frame is None and method in (0x54, 0x55), 'native absolute WORD/segment field')
                fields.append((CODE_BASE + site, loc, method, index, addend))
                if method == 0x55:
                    need(loc >> 2 & 15 == 2 and index == 1 and addend == 0, 'genuine group1 segment base')
                    value = DS
                    relocs.append([0, CODE_BASE + site])
                else:
                    need(loc >> 2 & 15 == 1 and index == 2 and addend == 0x744, 'own DATA mem_AllocID near WORD')
                    value = DATA_BASE + addend
                image[offset:offset + 2] = value.to_bytes(2, 'little')
    need(tuple(fields) == FIELDS, 'all six fields in literal emitted order')
    table = (work / 'obj/th03/mainl.map').read_text()
    need(address(table, 'GRAPH_PI_LOAD_PACK') == (0, 0x1044) and address(table, 'mem_AllocID') == (DS, DATA_BASE + 0x744),
         'actual loader and external allocator-tag storage in both MAP tables')
    extent((target, candidate), image, 0, START, relocs)
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    ins = list(decoder.disasm(image, START))
    need(sum(i.size for i in ins) == SIZE, 'complete instruction and ordinary alignment partition')
    bounds = {i.address for i in ins}
    for i in ins:
        if i.mnemonic.startswith(('j', 'loop')):
            need(i.operands[0].type == X86_OP_IMM and i.operands[0].imm in bounds, 'every branch enters an owned complete instruction')
        elif i.mnemonic == 'call':
            need(i.operands[0].type == X86_OP_IMM, 'direct genuine near call')
            if i.address in BRIDGES:
                need(i.operands[0].imm == BRIDGES[i.address] and image[i.address - START - 1] == 0x0E,
                     'native same-CS PUSH CS/CALL bridge')
            else:
                need(i.operands[0].imm in (0x1500, 0x15EE, 0x161A), 'all actual private decoder call entries')
    decoded = []
    for name, start, size, mnemonic, operand in PARTS:
        body = [i for i in ins if start <= i.address < start + size]
        need(sum(i.size for i in body) == size and body[-1].mnemonic == mnemonic and
             (int(body[-1].op_str, 0) if body[-1].op_str else 0) == (int(operand) if operand else 0),
             'complete procedure/shared-exit extent and original cleanup: ' + name)
        decoded.append(dict(name=name, offset=start - START, size=size, instruction_count=len(body),
                            callee_pop_bytes=12 if mnemonic == 'retf' else 0))
    need(sum(p[2] for p in PARTS) + len(EVENS) == SIZE and
         all(next(i for i in ins if i.address == a).mnemonic == 'nop' for a in EVENS),
         'four functions, shared error exit and two genuine outer EVEN bytes')
    digest = hashlib.sha256(image).hexdigest()
    owner = dict(unit_id=UNIT, name='Complete master.lib packed PI decoder', source=SOURCE, object=OBJECT,
        origin='library', segment=0, offset=START, start=START, size=SIZE, coordinate_space='decoded-load', canonical_file_offset=None,
        target_sha256=digest, candidate_sha256=digest, ordered_relocations=relocs, procedure_count=4,
        procedures=decoded[1:], shared_exit=decoded[0], code_bytes=SIZE, initialized_data_bytes=0,
        private_data_bytes=0, private_bss_bytes=0, abi='far Pascal pop12 loader; three private near helpers; shared error borrows loader BP/SI/DI frame')
    return dict(owners=[owner], library_CODE_bytes=SIZE, procedures=4, native_fields=[list(f) for f in fields],
        ordered_relocations=relocs, ordinary_outer_EVEN_bytes=list(EVENS), shared_error_is_procedure=False,
        same_CS_call_bridges=[dict(call=a, target=b) for a, b in BRIDGES.items()],
        source_origin='master.lib SuCa assembly', source_original_directives_preserved=True,
        external_macro_DATA_BSS_or_allocator_accepted=False, runtime_matrix_required=False, whole_product_accepted=False)


if __name__ == '__main__':
    import json
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    # Includes the complete current source/tool/library/cold-output guard,
    # while preserving all unchanged prior runtime observations.
    result = audit(Path(__file__).resolve().parents[2])
    print(json.dumps(result['scope']['pi_decoder_native'], indent=2))
