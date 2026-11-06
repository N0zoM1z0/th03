"""Complete two remaining project procedures and the typed name-pointer table.

Reuse the unchanged source-bound native pair. No compiler replay, synthetic
alignment, emulator specification or whole-product ownership claim is needed.
"""
import json
import re

from capstone import Cs, CS_ARCH_X86, CS_MODE_16, CS_GRP_JUMP
from capstone.x86 import X86_INS_LOOP, X86_OP_IMM

from lib.omf import describe_omf, parse_omf
from lib.decoded_mainl_registration_layout import (
    verify as registration, native_image, SOURCE as REG_SOURCE, OBJECT as REG_OBJECT,
)
from lib.decoded_mainl_registration_inventory import BINDINGS
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from build_th03_mainl_resources_work import need, sha

PREFIX = 'th03-mainl-decoded-'
LUT_SOURCE = 'src/shared/formats/hfliplut.asm'
LUT_OBJECT = 'obj/th03/hfliplut.obj'
UNITS = (PREFIX + 'hflip-lut-generate', PREFIX + 'registration-music',
         PREFIX + 'registration-name-pointers')


def address(mapping, name):
    matches = re.findall(r'(?m)^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?' +
                         re.escape(name) + r'\s*$', mapping)
    need(len(matches) == 2 and matches[0] == matches[1], 'both native symbol tables: ' + name)
    return tuple(int(n, 16) for n in matches[0])


def extent(target, candidate, segment, offset, body, relocations):
    start = segment * 16 + offset
    for mz in (target, candidate):
        need(mz.program_image[start:start + len(body)] == body, 'entire resolved native extent')
        need([(r.segment, r.offset) for r in mz.relocations if start <= r.linear < start + len(body)] ==
             relocations, 'complete literal ordered MZ vector')


def procedure(body, offset, return_kind, expected_calls):
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    rows = list(decoder.disasm(body, offset))
    need(rows and sum(i.size for i in rows) == len(body) and
         rows[-1].mnemonic == return_kind and not rows[-1].op_str and
         sum(i.mnemonic in ('ret', 'retf') for i in rows) == 1,
         'one complete no-argument procedure and original near/far return')
    boundaries = {i.address for i in rows}
    edges, calls = [], []
    for ins in rows:
        if ins.group(CS_GRP_JUMP) or ins.id == X86_INS_LOOP:
            need(len(ins.operands) == 1 and ins.operands[0].type == X86_OP_IMM and
                 ins.operands[0].imm in boundaries, 'local branch closes at a real instruction')
            edges.append(dict(site=ins.address, target=ins.operands[0].imm, kind=ins.mnemonic))
        if ins.mnemonic in ('call', 'lcall'):
            need(ins.mnemonic == 'lcall' and len(ins.operands) == 2 and
                 all(o.type == X86_OP_IMM for o in ins.operands), 'ordinary direct far call')
            calls.append(tuple(o.imm for o in ins.operands))
    need(calls == expected_calls, 'complete ordered native callees')
    return dict(instruction_count=len(rows), branches=edges, calls=calls,
                return_kind=return_kind, argument_bytes=0, callee_pop_bytes=0)


def owner(unit, name, source, obj, segment, offset, body, relocations, code, abi):
    return dict(unit_id=unit, name=name, source=source, object=obj, origin='authored',
        segment=segment, offset=offset, start=segment * 16 + offset, size=len(body),
        coordinate_space='decoded-load', canonical_file_offset=None,
        target_sha256=sha(body), candidate_sha256=sha(body), ordered_relocations=relocations,
        code_bytes=len(body) if code else 0, initialized_data_bytes=0 if code else len(body),
        procedure_count=int(code), private_data_bytes=0, private_bss_bytes=0, abi=abi)


def verify(root, work, target, candidate, graph, files):
    # This already binds the whole regdata TU, all seventy imports, all188
    # unsorted literal fields, complete native CODE/DATA and actual MAP entries.
    reg = registration(work, target, candidate, graph, files)
    raw = (work / REG_OBJECT).read_bytes()
    images, fields = native_image(raw)
    mapping = (work / 'obj/th03/mainl.map').read_text()
    music_fields = [f for f in fields if f['segment_index'] == 1 and f['offset'] >= 2720]
    data_fields = [f for f in fields if f['segment_index'] == 2]
    names = ['SND_KAJA_INTERRUPT', '_snd_load', 'SND_KAJA_INTERRUPT', 'PALETTE_BLACK_IN',
             'SND_DELAY_UNTIL_MEASURE', 'PALETTE_BLACK_OUT', 'SND_KAJA_INTERRUPT']
    need([f['name'] for f in reversed(music_fields) if f['width'] == 4] == names and
         [f['offset'] for f in music_fields] == [2782, 2774, 2767, 2756, 2749, 2739, 2736, 2727],
         'all eight literal music fields retain actual compiler order')
    need(address(mapping, '_mainl_reg_music') == (0x95F, 0x233E), 'original near music entry')
    calls = [address(mapping, n) for n in names]
    music = images[1][2720:]
    need(len(music) == 68, 'complete music suffix through RET')
    music_body = procedure(music, 0x233E, 'ret', calls)
    music_mz = [(0x95F, 0x189E + f['offset'] + 2) for f in music_fields if f['width'] == 4]
    extent(target, candidate, 0x95F, 0x233E, music, music_mz)
    # The real large-model table contains ten far pointers, not its strings.
    pointer_names = ['none', 'reimu', 'mima', 'marisa', 'ellen', 'kotohime', 'kana',
                     'rikako', 'chiyuri', 'yumemi']
    need([f['name'] for f in reversed(data_fields)] == ['_mainl_name_' + n for n in pointer_names] and
         [f['offset'] for f in data_fields] == list(range(36, -1, -4)) and
         all((f['locat'], f['fixdat'], f['frame'], f['addend'], f['width']) ==
             (0xCC, 0x16, 2, 0, 4) for f in data_fields), 'literal typed far-pointer producer fields')
    pointer_bindings = []
    for f in data_fields:
        name, _, segment, offset = BINDINGS[f['target']]
        need(address(mapping, name) == (segment, offset) and segment == 0xE3F and
             images[2][f['offset']:f['offset'] + 4] ==
             offset.to_bytes(2, 'little') + segment.to_bytes(2, 'little'), 'each actual external name pointer')
        pointer_bindings.append(dict(site=f['offset'], name=name, segment=segment, offset=offset))
    data_mz = [(0xE3F, 0x906 + f['offset'] + 2) for f in data_fields]
    extent(target, candidate, 0xE3F, 0x906, images[2], data_mz)
    need(address(mapping, '_REGIST_PLAYCHARS') == (0xE3F, 0x906) and
         any(f['segment_index'] == 1 and f['offset'] == 1402 and f['name'] == '_REGIST_PLAYCHARS'
             for f in fields), 'actual registration menu consumes this table')

    lut_raw = (work / LUT_OBJECT).read_bytes()
    description = describe_omf(lut_raw)
    need(description['valid'] and description['module_name'] == r'th03\hfliplut.asm' and
         description['translator_comments'] == ['Turbo Assembler  Version 5.0'] and
         description['record_counts'] == dict(COMENT=6, EXTDEF=1, FIXUPP=1, LEDATA=1,
             LNAMES=2, MODEND=1, PUBDEF=1, SEGDEF=1, THEADR=1), 'complete original assembler module')
    producer, = [g for g in graph if g['output'] == LUT_OBJECT]
    need((producer['source'], producer['wrapper'], producer['kind'], producer['game'],
          producer['binary'], producer['first_binary']) ==
         (LUT_SOURCE, 'th03/hfliplut.asm', 'tasm', 3, 'O', 'op') and
         files[LUT_SOURCE].replace(b'\r\n', b'\n') == (root / LUT_SOURCE).read_bytes() and
         ('include ' + LUT_SOURCE).encode() in files['th03/hfliplut.asm'], 'actual unchanged first-use source producer')
    records = lambda kind: [r.data for r in parse_omf(lut_raw) if r.name == kind]
    need(segment_definitions(lut_raw) ==
         [dict(index=1, name='SHARED', **{'class': 'CODE'}, overlay='', size=30)] and
         [r.data[0] for r in parse_omf(lut_raw) if r.name == 'SEGDEF'] == [0x48],
         'complete WORD/PUBLIC USE16 CODE; no private DATA/BSS')
    need(records('EXTDEF') == [bytes([10]) + b'_hflip_lut' + bytes([0])] and
         records('PUBDEF') == [bytes([0, 1, 19]) + b'_hflip_lut_generate' + bytes([0, 0, 0])] and
         records('MODEND') == [bytes([0])] and not records('GRPDEF'),
         'complete ordered original external and public')
    need(records('FIXUPP') == [bytes([0xC4, 4, 0x56, 1])], 'entire unthreaded literal LUT offset record')
    lut_fields = [dict(segment=1, site=4, location_type=1, width=2, segment_relative=True,
        frame_method=5, frame=None, target_method=2, target=1, addend=0)]
    blocks = records('LEDATA')
    need(len(blocks) == 1 and blocks[0][:3] == b'\1\0\0' and len(blocks[0]) == 33 and
         blocks[0][7:9] == bytes([0, 0]), 'every instruction byte emitted once; original field addend')
    lut = bytearray(blocks[0][3:])
    need(address(mapping, '_hflip_lut') == (0xE3F, 0x20D6) and
         address(mapping, '_hflip_lut_generate') == (0xC7E, 0xFA4), 'real output state and far entry')
    lut[4:6] = (0x20D6).to_bytes(2, 'little')
    lut = bytes(lut)
    lut_body = procedure(lut, 0xFA4, 'retf', [])
    extent(target, candidate, 0xC7E, 0xFA4, lut, [])
    need(len(lut_body['branches']) == 3, 'original entry jump and both nested loop edges')
    owners = [
        owner(UNITS[0], '_hflip_lut_generate', LUT_SOURCE, LUT_OBJECT, 0xC7E, 0xFA4, lut, [], True,
              'far noargs; DI preserved; AX/CX/DX clobbered; writes existing 256-byte LUT; DS unchanged'),
        owner(UNITS[1], '_mainl_reg_music', REG_SOURCE, REG_OBJECT, 0x95F, 0x233E, music, music_mz, True,
              'near noargs; BP frame preserved; original Pascal sound/palette and far C snd_load calls'),
        owner(UNITS[2], '_REGIST_PLAYCHARS', REG_SOURCE, REG_OBJECT, 0xE3F, 0x906, images[2], data_mz, False,
              'ten existing large-model four-byte const Shift-JIS pointers; strings and BSS excluded'),
    ]
    result = dict(owners=owners, procedures=2, source_CODE_bytes=98, source_initialized_DATA_bytes=40,
        instruction_count=music_body['instruction_count'] + lut_body['instruction_count'],
        music=music_body, lut=lut_body, music_literal_fields=music_fields,
        pointer_literal_fields=data_fields, pointer_bindings=pointer_bindings, lut_literal_fields=lut_fields,
        regdata_entire_producer_fields=len(fields), regdata_entire_object_sha256=reg['native_object_sha256'],
        lut_entire_object_sha256=sha(lut_raw), vector_alignment_accepted=False,
        LUT_storage_newly_credited=False, original_cold_rebuilt=False, ancestor_runtime_replayed=False,
        physical_hardware_execution_claimed=False, whole_product_accepted=False)
    return json.loads(json.dumps(result))


if __name__ == '__main__':
    import argparse
    from pathlib import Path
    from review_th03_mainl_sound_work import images as cold_images

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold', action='store_true', required=True)
    parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    work, target, candidate, cold, cold_raw, graph, files = cold_images(root)
    scope = verify(root, work, target, candidate, graph, files)
    report = dict(schema='th03-mainl-completion-after550-current-native-v1', complete=True,
        cold_report_sha256=sha(cold_raw), outputs_per_existing_round=len(cold['rounds'][0]['outputs']),
        verifier_sha256=sha(Path(__file__).read_bytes()), provenance='candidate-local-attested',
        source_sha256={n: sha((root / n).read_bytes()) for n in (REG_SOURCE, LUT_SOURCE)},
        scope=scope, original_cold_rebuilt=False, ancestor_runtime_replayed=False)
    (root / '.analysis/work/mainl-completion-after550-review.json').write_text(json.dumps(report, indent=2) + '\n')
    print('MAINL completion: two complete procedures /98 CODE /37 instructions +40 typed DATA; '
          '19 selected literal fields /17 ordered MZ relocations; unchanged native pair reused')
