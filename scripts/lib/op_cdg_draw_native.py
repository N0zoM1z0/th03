"""Complete OP native CDG blitters, self-modifying words and natural EVEN layout."""
import hashlib
import re

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import describe_omf, parse_omf
from lib.decoded_mainl_cdg_draw_layout import native_image as shape, PATCHES, WRITERS
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

CS, DS = 0xBEB, 0xD7F
PRODUCERS = (
    ('cdg_put', 'src/shared/formats/cdg_put.asm', 3, 0x170, 382, 'th03-op-decoded-cdg-draw',
     (('alpha', 'CDG_PUT_8', 0, 179), ('hflip', 'CDG_PUT_HFLIP_8', 180, 201))),
    ('cdg_p_na', 'src/shared/formats/cdg_noalpha.asm', 1, 0xC46, 114, 'th03-op-decoded-cdg-draw-noalpha',
     (('noalpha', 'CDG_PUT_NOALPHA_8', 0, 113),)),
)
UNITS = {p[5] for p in PRODUCERS}


def need(value, message):
    if not value:
        raise ValueError('OP CDG draw native: ' + str(message))


def address(table, name):
    rows = re.findall(rf'(?m)^\s*([0-9A-F]{{4}}):([0-9A-F]{{4}})\s+(?:idle\s+)?{re.escape(name)}\s*$', table)
    need(len(rows) == 2 and rows[0] == rows[1], 'both OP MAP public tables: ' + name)
    return tuple(int(v, 16) for v in rows[0])


def verify(root, work, target, candidate, files):
    table = (work / 'obj/th03/op.map').read_text().replace(chr(92), '/')
    owners, objects = [], []
    for stem, source, index, base, size, unit, procedures in PRODUCERS:
        obj, wrapper = f'obj/th03/{stem}.obj', f'th03/{stem}.asm'
        raw = (work / obj).read_bytes()
        native = describe_omf(raw)
        need(native['valid'] and native['module_name'].replace(chr(92), '/') == wrapper and
             native['translator_comments'] == ['Turbo Assembler  Version 5.0'], 'actual complete OP TASM producer')
        segments = [('CDG_PUT_TEXT', 'CODE', 0), ('_DATA', 'DATA', 0), ('SHARED', 'CODE', 382)] if index == 3 else [('SHARED', 'CODE', 114)]
        need(segment_definitions(raw) == [dict(index=i + 1, name=n, **{'class': c}, overlay='', size=s)
             for i, (n, c, s) in enumerate(segments)], 'complete natural segment layout')
        records = parse_omf(raw)
        need([r.data[0] for r in records if r.name == 'SEGDEF'] == [0x48] * len(segments) and
             [r.data for r in records if r.name == 'GRPDEF'] == ([bytes((8, 255, 2))] if index == 3 else []),
             'WORD/PUBLIC/USE16 alignment and native groups')
        need([(b['offset'], b['size']) for b in code_bytes(raw, index)[1]] == [(0, size)] and
             [r.data[0] for r in records if r.name == 'LEDATA'] == [index], 'one complete CODE record; no other initializer')
        need(code_publics(raw, index) == [(off, name) for _, name, off, _ in procedures] and
             all(not code_publics(raw, i + 1) for i in range(len(segments)) if i + 1 != index),
             'complete public inventory')
        need(files[wrapper].replace(b'\r\n', b'\n') == ('include ' + source + '\n').encode() and files[source] == (root / source).read_bytes(),
             'literal maintained ASM source chain')
        deps = [n.replace(chr(92), '/') for n in native['dependency_paths']]
        need(all(n in files and (work / n).read_bytes() == files[n] for n in deps) and
             all(n in deps for n in (wrapper, source)), 'every actual native source/include dependency')
        need(len(re.findall(rb'(?im)^\s*even\s*$', files[source])) == (4 if index == 3 else 2),
             'ordinary source EVEN directives, including loop alignment')
        need(len(re.findall(rf'(?m)^\s*{CS:04X}:{base:04X}\s+{size:04X}\s+C=CODE\s+S=SHARED\s+G=\(none\)\s+M={re.escape(wrapper)}\s+ACBP=48\s*$', table)) == 1,
             'complete actual OP native CODE allocation')
        if index == 3:
            need(len(re.findall(r'(?m)^\s*0CB9:000C\s+0000\s+C=CODE\s+S=CDG_PUT_TEXT\s+G=\(none\)\s+M=th03/cdg_put\.asm\s+ACBP=48\s*$', table)) == 1 and
                 len(re.findall(r'(?m)^\s*0D7F:05F2\s+0000\s+C=DATA\s+S=_DATA\s+G=DGROUP\s+M=th03/cdg_put\.asm\s+ACBP=48\s*$', table)) == 1,
                 'empty native compatibility CODE/DATA contributions')
        # Reuse only the shared native grammar/field metadata. Discard its
        # MAINL comparison image and resolve OP's raw object from its own MAP.
        _, fields = shape(raw, stem, index, base)
        code, _ = code_bytes(raw, index)
        image, relocs = bytearray(code), []
        for f in fields:
            site, width = f['offset'], f['width']
            if f['fixdat'] == 0x54:
                need(f['target'] == index and width == 2 and f['name'] == 'SHARED', 'own CS WORD field')
                value = base + f['addend']
            else:
                seg, off = address(table, f['name'])
                need(f['addend'] == 0, 'ordinary external field with zero addend')
                if width == 4:
                    need(f['name'] == 'GRCG_SETCOLOR' and seg == 0 and code[site - 1] == 0x9A,
                         'ordinary external far GRCG call')
                    value = off | seg << 16
                    relocs.append([CS, base + site + 2])
                else:
                    need(seg == DS and f['name'] in ('_cdg_slots', '_hflip_lut'), 'external near DGROUP reference')
                    value = off
            image[site:site + width] = value.to_bytes(width, 'little')
        start = CS * 16 + base
        need(bytes(image) == target.program_image[start:start + size] == candidate.program_image[start:start + size],
             'complete independently resolved OP native/target/candidate bytes')
        for executable in (target, candidate):
            need([[r.segment, r.offset] for r in executable.relocations if start <= r.linear < start + size] == relocs,
                 'complete literal ordered OP MZ vector')
            need(not any(r.linear < start < r.linear + 2 or r.linear < start + size < r.linear + 2
                         for r in executable.relocations), 'no straddling relocation')
        decoded, occupied = [], set()
        for kind, name, off, length in procedures:
            need(address(table, name) == (CS, base + off), 'actual OP procedure address')
            ins = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(image[off:off + length], base + off))
            need(sum(i.size for i in ins) == length and (ins[-1].mnemonic, ins[-1].op_str) == ('retf', '6'),
                 'complete far Pascal procedure')
            by = {i.address: i for i in ins}
            smc = []
            for writer, patch in zip(WRITERS[kind], PATCHES[kind]):
                instruction = by[base + off + writer]
                need(instruction.mnemonic == 'mov' and instruction.op_str.startswith('word ptr cs:') and
                     f'0x{base + off + patch:x}' in instruction.op_str, 'native SMC store targets its own operand WORD')
                consumer, = [i for i in ins if i.address + 1 == base + off + patch and i.size == 3]
                need(consumer.mnemonic == 'mov', 'entire MOV immediate is the self-modifying destination')
                smc.append(dict(writer=writer, operand=patch))
            decoded.append(dict(name=name, offset=off, size=length, callee_pop_bytes=6, instruction_count=len(ins), self_modifying_words=smc))
            occupied.update(range(off, off + length))
        outer_even = sorted(set(range(size)) - occupied)
        need(outer_even == ([179, 381] if index == 3 else [113]) and
             all(image[i] == 0x90 for i in outer_even), 'separate natural inter-procedure/trailing EVEN bytes')
        digest = hashlib.sha256(image).hexdigest()
        owners.append(dict(unit_id=unit, name='CDG alpha/hflip native producer' if index == 3 else 'CDG noalpha native producer',
            source=source, object=obj, segment=CS, offset=base, start=start, size=size,
            coordinate_space='decoded-load', canonical_file_offset=None, target_sha256=digest, candidate_sha256=digest,
            ordered_relocations=relocs, procedure_count=len(procedures), procedures=decoded, code_bytes=size,
            initialized_data_bytes=0, private_data_bytes=0, private_bss_bytes=0,
            forwarding_chain=[wrapper, source], abi='far Pascal pop6; original CS operand writes and segment registers',
            procedure_body_bytes=sum(p[3] for p in procedures), outer_EVEN_offsets=outer_even))
        objects.append(dict(object=obj, native_fields=fields, ordered_relocations=relocs, complete_CODE_bytes=size,
                            consumed_paths=deps, outer_EVEN_offsets=outer_even))
    return dict(owners=owners, code_bytes=496, procedures=3, procedure_body_bytes=493, outer_EVEN_bytes=3,
                self_modifying_WORDs=12, native_objects=objects, private_data_bytes=0, private_bss_bytes=0,
                lookup_or_hardware_accepted=False, runtime_matrix_required=False, whole_product_accepted=False)


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
