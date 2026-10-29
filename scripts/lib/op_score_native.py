"""Native ownership of the complete OP score codecs and their storage."""
import hashlib
import re
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import describe_omf, parse_omf
from lib.op_select_native import CS, DS, resolved_code
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

ENCODE = 'src/op/formats/score_encode.cpp'
CODEC = 'src/op/formats/score_data.cpp'
HEADER = 'src/op/formats/scorecrypt.hpp'
DATA_UNIT = 'th03-op-decoded-score-storage'
DATA, BSS = 0xA02, 0x2394
SOURCES = {ENCODE, CODEC}
PRODUCERS = (
    ('op_02', ENCODE, 'OP_02_TEXT', 0x1868, 165, 11, 206, 'th03-op-decoded-score-encode', (
        (0, '@SCOREDAT_ENCODE_AND_SAVE$Q6RANK_T', 165, 2, 'scoredat_encode_and_save(rank_t)'),)),
    ('scoredat', CODEC, 'SCOREDAT_TEXT', 0x190D, 229, 0, 0, 'th03-op-decoded-score-score-data', (
        (0, '@scoredat_decode$qv', 60, 0, 'scoredat_decode()'),
        (60, '@scoredat_recreate$qv', 127, 0, 'scoredat_recreate()'),
        (187, '@scoredat_sum_invalid$qv', 42, 0, 'scoredat_sum_invalid()'))),
)


def need(value, message):
    if not value:
        raise ValueError('OP score native: ' + str(message))


def address(table, name):
    if name == '@SCOREDAT_ENCODE_AND_SAVE$Q6RANK_T':
        name = 'scoredat_encode_and_save(rank_t)'
    rows = re.findall(rf'(?m)^\s*([0-9A-F]{{4}}):([0-9A-F]{{4}})\s+(?:idle\s+)?{re.escape(name)}\s*$', table)
    need(len(rows) == 2 and rows[0] == rows[1], 'both MAP public tables: ' + name)
    return tuple(int(v, 16) for v in rows[0])


def storage(raw, table, target, candidate):
    data, blocks = code_bytes(raw, 2)
    need([(b['offset'], b['size']) for b in blocks] == [(0, 11)] and
         data == struct.pack('<H', 2) + b'YUME.NEM\0', 'complete natural near pointer and filename pool')
    need(code_publics(raw, 2) == [(0, '_SCOREDAT_FN_PTR')] and code_publics(raw, 3) == [(0, '_hi')],
         'initialized DATA and BSS public boundaries')
    need(address(table, '_SCOREDAT_FN_PTR') == (DS, DATA) and address(table, '_hi') == (DS, BSS),
         'both storage MAP public tables')
    # The sole initialized field is an ordinary16-bit DGROUP near pointer.
    # Preserve the filename terminator; do not turn the pointer into a far one.
    block, fixups = None, []
    for record in parse_omf(raw):
        if record.name == 'LEDATA':
            block = record.data[0]
            need(block != 3, 'BSS has no file-backed initializer')
        elif record.name == 'FIXUPP' and block == 2:
            fixups.append(record.data)
    need(fixups == [bytes((0xC4, 0, 20, 2, 2))], 'single native DATA WORD field to own DGROUP DATA')
    linked = struct.pack('<H', DATA + 2) + data[2:]
    start = DS * 16 + DATA
    need(linked == target.program_image[start:start + 11] == candidate.program_image[start:start + 11],
         'complete semantic/native/target/candidate DATA')
    for image in (target, candidate):
        need(not any(start - 1 <= r.linear < start + 11 for r in image.relocations), 'near DATA has no MZ relocation')
    digest = hashlib.sha256(linked).hexdigest()
    return dict(unit_id=DATA_UNIT, name='OP score filename pointer and literal', source=ENCODE,
        object='obj/th03/op_02.obj', segment=DS, offset=DATA, start=start, size=11,
        coordinate_space='decoded-load', canonical_file_offset=None, target_sha256=digest, candidate_sha256=digest,
        ordered_relocations=[], procedure_count=0, procedures=[], code_bytes=0, initialized_data_bytes=11,
        private_data_bytes=11, private_bss_bytes=0, forwarding_chain=['th03/op_02.cpp', ENCODE],
        abi='16-bit DGROUP near filename pointer; NUL-terminated filename')


def verify(root, work, target, candidate, files):
    table = (work / 'obj/th03/op.map').read_text()
    owners, objects = [], []
    for stem, source, segment, base, size, data_size, bss_size, unit, procedures in PRODUCERS:
        obj, wrapper = f'obj/th03/{stem}.obj', f'th03/{stem}.cpp'
        raw = (work / obj).read_bytes()
        native = describe_omf(raw)
        need(native['valid'] and native['module_name'] == wrapper and
             native['translator_comments'] == ['TC86 Borland C++ 4.02'], 'actual complete TC4 producer')
        need(segment_definitions(raw) == [dict(index=i, name=n, **{'class': c}, overlay='', size=s)
             for i, n, c, s in ((1, segment, 'CODE', size), (2, '_DATA', 'DATA', data_size), (3, '_BSS', 'BSS', bss_size))],
             'complete natural segment layout')
        need([r.data for r in parse_omf(raw) if r.name == 'GRPDEF'] ==
             [bytes((8, 255, 1)), bytes((9, 255, 2, 255, 3))], 'group1 CODE and group2 DGROUP')
        need(tuple(code_publics(raw, 1)) == tuple((off, symbol) for off, symbol, *_ in procedures),
             'all complete native CODE public boundaries')
        need(files[wrapper] == ('#include "' + source + '"\n').encode() and
             files[source] == (root / source).read_bytes() and files[HEADER] == (root / HEADER).read_bytes(),
             'literal maintained TU source chain')
        deps = [re.sub('/+', '/', n.replace(chr(92), '/')) for n in native['dependency_paths']]
        sdk = [n for n in deps if n.startswith('C:/TC4/INCLUDE/')]
        need(sdk == (['C:/TC4/INCLUDE/' + n for n in ('stddef.h', '_defs.h', '_null.h')] if stem == 'scoredat' else []),
             'actual consumed SDK headers; bound by current toolchain audit')
        need(all(n in files and (work / n).read_bytes() == files[n] for n in deps if n not in sdk) and
             all(n in deps for n in (wrapper, source, HEADER)), 'complete native source/header binding')
        for seg, offset, length, cls, segname in (
            (CS, base, size, 'CODE', segment),
            (DS, DATA if stem == 'op_02' else 0xA0E, data_size, 'DATA', '_DATA'),
            (DS, BSS if stem == 'op_02' else 0x2462, bss_size, 'BSS', '_BSS')):
            group, acbp = ('GROUP_01', '28') if cls == 'CODE' else ('DGROUP', '48')
            need(len(re.findall(rf'(?m)^\s*{seg:04X}:{offset:04X}\s+{length:04X}\s+C={cls}\s+S={segname}\s+G={group}\s+M=th03/{stem}\.cpp\s+ACBP={acbp}\s*$', table)) == 1,
                 'complete native MAP contribution: ' + stem + '/' + cls)
        code, fields, relocs = resolved_code(raw, base, DATA, BSS, table, lookup=address)
        start = CS * 16 + base
        need(code == target.program_image[start:start + size] == candidate.program_image[start:start + size],
             'complete independently resolved native/target/candidate CODE')
        for image in (target, candidate):
            need([[r.segment, r.offset] for r in image.relocations if start <= r.linear < start + size] == relocs,
                 'complete literal ordered MZ vector')
            need(not any(r.linear < start < r.linear + 2 or r.linear < start + size < r.linear + 2
                         for r in image.relocations), 'no straddling relocation')
        need([off for off, *_ in procedures] == [sum(p[2] for p in procedures[:i]) for i in range(len(procedures))]
             and sum(p[2] for p in procedures) == size, 'complete contiguous procedure partition')
        decoded = []
        for off, symbol, length, cleanup, mapname in procedures:
            need(address(table, mapname) == (CS, base + off), 'native procedure MAP address')
            instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(code[off:off + length], base + off))
            need(sum(i.size for i in instructions) == length and instructions[-1].mnemonic == 'ret' and
                 (int(instructions[-1].op_str, 0) if instructions[-1].op_str else 0) == cleanup,
                 'complete near procedure/argument cleanup: ' + symbol)
            decoded.append(dict(name=mapname, offset=off, size=length, callee_pop_bytes=cleanup,
                                instruction_count=len(instructions)))
        digest = hashlib.sha256(code).hexdigest()
        owners.append(dict(unit_id=unit, name='OP score encode/save' if stem == 'op_02' else 'OP score decode/recreate/checksum',
            source=source, object=obj, segment=CS, offset=base, start=start, size=size,
            coordinate_space='decoded-load', canonical_file_offset=None, target_sha256=digest, candidate_sha256=digest,
            ordered_relocations=relocs, procedure_count=len(procedures), procedures=decoded,
            code_bytes=size, initialized_data_bytes=0, private_data_bytes=0, private_bss_bytes=0,
            forwarding_chain=[wrapper, source], abi='near C; encode/save near Pascal pop2; BYTE bool checksum result'))
        objects.append(dict(object=obj, complete_CODE_bytes=size, native_fields=fields, ordered_relocations=relocs,
                            containing_DATA_bytes=data_size, containing_BSS_bytes=bss_size, sdk_dependencies=sdk))
        if stem == 'op_02':
            owners.append(storage(raw, table, target, candidate))
        else:
            need(not code_publics(raw, 2) and not code_publics(raw, 3), 'codec has no storage publics')
    need(not any(r.name == 'LEDATA' and r.data[0] == 3 for p in PRODUCERS
                 for r in parse_omf((work / f'obj/th03/{p[0]}.obj').read_bytes())), 'uninitialized BSS stays non-file-backed')
    return dict(owners=owners, code_bytes=394, procedures=4, initialized_data_bytes=11,
                native_objects=objects, BSS_extent=[DS, BSS, 206], BSS_public='_hi', BSS_file_backed=False,
                BSS_raw_byte_credit=0, loader_CODE_bytes_previously_accepted=107,
                runtime_matrix_required=False, whole_product_accepted=False)


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
