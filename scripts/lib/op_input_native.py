"""Complete OP keyboard function; legacy reference trailer remains unowned."""
import hashlib
import json
import re

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

CS, DS, BASE, SIZE = 0xBEB, 0xD7F, 0x304, 417
SOURCE = 'src/op/hardware/input_sense.cpp'
WRAPPER, INCLUDE, OBJECT = 'th03/input_s.cpp', 'th03/hardware/input_s.cpp', 'obj/th03/input_s.obj'
UNIT = 'th03-op-decoded-input-sense'
PUBLIC = '@input_reset_sense_key_held$qv'
EXTERNALS = ('_js_stat', '_input_mp_p1', '_input_mp_p2', '_input_sp')
GROUPS = (0x531, 0x533, 0x532, 0x52F, 0x52E, 0x52C, 0x52A, 0x52D, 0x530)
PROBE = '.analysis/work/input-nostring.json'
DIRECT = '.analysis/work/input-nostring.obj'
ASSEMBLED = '.analysis/work/input-assembly.obj'


def need(value, message):
    if not value:
        raise ValueError('OP input native: ' + str(message))


def address(table, name):
    rows = re.findall(rf'(?m)^\s*([0-9A-F]{{4}}):([0-9A-F]{{4}})\s+(?:idle\s+)?{re.escape(name)}\s*$', table)
    need(len(rows) == 2 and rows[0] == rows[1], 'both OP MAP public tables: ' + name)
    return tuple(int(v, 16) for v in rows[0])


def resolve(raw, table, containing_size):
    native = describe_omf(raw)
    need(native['valid'], 'whole native OMF integrity')
    records = parse_omf(raw)
    # TCC -S declares the empty DGROUP members in the reverse order from
    # direct OMF. Both are actual emitter records; neither has local storage.
    group = bytes((8, 255, 3, 255, 2)) if native['translator_comments'] == ['Turbo Assembler  Version 5.0'] else bytes((8, 255, 2, 255, 3))
    need(segment_definitions(raw) == [dict(index=i, name=n, **{'class': c}, overlay='', size=s)
         for i, n, c, s in ((1, 'SHARED', 'CODE', containing_size), (2, '_DATA', 'DATA', 0), (3, '_BSS', 'BSS', 0))] and
         [r.data[0] for r in records if r.name == 'SEGDEF'] == [0x48] * 3 and
         [r.data for r in records if r.name == 'GRPDEF'] == [group],
         'complete WORD-aligned native layout and sole DGROUP')
    need(code_publics(raw, 1) == [(0, PUBLIC)] and not code_publics(raw, 2) and not code_publics(raw, 3),
         'one complete function public and no private storage')
    code, blocks = code_bytes(raw, 1)
    need([(b['offset'], b['size']) for b in blocks] == [(0, containing_size)] and
         [r.data[0] for r in records if r.name == 'LEDATA'] == [1], 'complete native CODE record')
    ext, = [r.data for r in records if r.name == 'EXTDEF']
    need(ext == b''.join(bytes((len(n),)) + n.encode() + b'\0' for n in EXTERNALS), 'four literal native external identities')
    fixup, = [r.data for r in records if r.name == 'FIXUPP']
    image, fields, at = bytearray(code[:SIZE]), [], 0
    while at < len(fixup):
        loc, low, method, frame, index = fixup[at:at + 5]
        at += 5
        site = (loc & 3) * 256 + low
        need(loc & 0xFC == 0xC4 and method == 0x16 and frame == 1 and 1 <= index <= 4 and site + 2 <= SIZE,
             'ordinary native DGROUP WORD field wholly inside function')
        addend = int.from_bytes(code[site:site + 2], 'little')
        need(addend == 0, 'zero-addend external input word')
        name = EXTERNALS[index - 1]
        seg, off = address(table, name)
        need(seg == DS, 'actual OP DGROUP input storage')
        image[site:site + 2] = off.to_bytes(2, 'little')
        fields.append(dict(site=site, locat=loc, method=method, frame=frame, target=index, name=name, addend=addend))
    need(len(fields) == 42 and len({f['site'] for f in fields}) == 42, 'all42 distinct native input fields')
    return bytes(image), fields, native


def verify(root, work, target, candidate, files):
    source = (root / SOURCE).read_bytes()
    trailer = b'#pragma codestring "\\x90"\n'
    need(source.endswith(trailer) and source.count(b'#pragma codestring') == 1 and b'__emit__' not in source,
         'explicit single legacy trailer outside owned function')
    need(files[SOURCE] == source and files[WRAPPER] == ('#include "' + INCLUDE + '"\n').encode() and
         files[INCLUDE] == ('#include "' + SOURCE + '"\n').encode(), 'literal maintained source forwarding chain')
    raw = (work / OBJECT).read_bytes()
    table = (work / 'obj/th03/op.map').read_text()
    image, fields, native = resolve(raw, table, SIZE + 1)
    need(native['module_name'] == WRAPPER and native['translator_comments'] == ['TC86 Borland C++ 4.02'],
         'actual current native TC4 producer')
    deps = [n.replace(chr(92), '/') for n in native['dependency_paths']]
    need(all(n in files and (work / n).read_bytes() == files[n] for n in deps) and
         all(n in deps for n in (WRAPPER, INCLUDE, SOURCE)), 'actual complete source/header consumption')
    need(len(re.findall(r'(?m)^\s*0BEB:0304\s+01A2\s+C=CODE\s+S=SHARED\s+G=\(none\)\s+M=th03/input_s\.cpp\s+ACBP=48\s*$', table)) == 1,
         'actual containing418-byte MAP contribution; trailer excluded')
    for base, cls, name in ((0x5F2, 'DATA', '_DATA'), (0x1F70, 'BSS', '_BSS')):
        need(len(re.findall(rf'(?m)^\s*0D7F:{base:04X}\s+0000\s+C={cls}\s+S={name}\s+G=DGROUP\s+M=th03/input_s\.cpp\s+ACBP=48\s*$', table)) == 1,
             'empty native storage contribution')
    need(address(table, 'input_reset_sense_key_held()') == (CS, BASE), 'actual native entry in both MAP tables')
    # Prove the entire function also emits without the legacy codestring, by
    # two real emitter routes. Keep each route's emitted field order intact.
    proof_raw = (root / PROBE).read_bytes()
    proof = json.loads(proof_raw)
    need(proof['source_sha256'] == hashlib.sha256(source).hexdigest() and
         proof['source_without_codestring_sha256'] == hashlib.sha256(source[:-len(trailer)]).hexdigest() and
         proof['original_object_sha256'] == hashlib.sha256(raw).hexdigest() and
         proof['native_compiler_returncode'] == 0 and proof['fresh_compiles'] == 1 and
         not proof['reproducibility_pair_claimed'] and not proof['source_acceptance'], 'honest source-bound diagnostic receipt')
    natural = []
    for path, translator in ((DIRECT, 'TC86 Borland C++ 4.02'), (ASSEMBLED, 'Turbo Assembler  Version 5.0')):
        probe_raw = (root / path).read_bytes()
        body, probe_fields, description = resolve(probe_raw, table, SIZE)
        need(description['translator_comments'] == [translator] and body == image, 'complete natural417-byte independent emitter equality')
        if path == DIRECT:
            need(hashlib.sha256(probe_raw).hexdigest() == proof['probe_object_sha256'] and probe_fields == fields,
                 'recorded direct native object and unchanged complete field stream')
        natural.append(dict(object=path, sha256=hashlib.sha256(probe_raw).hexdigest(), CODE_bytes=SIZE,
                            translator=translator, native_fields=probe_fields, contains_codestring_bytes=False))
    start = CS * 16 + BASE
    need(image == target.program_image[start:start + SIZE] == candidate.program_image[start:start + SIZE],
         'complete independently resolved function/target/candidate bytes')
    for executable in (target, candidate):
        need(not [r for r in executable.relocations if start <= r.linear < start + SIZE], 'complete empty ordered function MZ vector')
        need(not any(r.linear < start < r.linear + 2 or r.linear < start + SIZE < r.linear + 2
                     for r in executable.relocations), 'no straddling function relocation')
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    ins = list(decoder.disasm(image, BASE))
    need(len(ins) == 115 and sum(i.size for i in ins) == SIZE and (ins[-1].mnemonic, ins[-1].op_str) == ('retf', ''),
         'complete115-instruction far C function without callee cleanup')
    bounds = {i.address for i in ins}
    need(not any(i.mnemonic in ('call', 'lcall', 'int', 'iret', 'enter', 'leave', 'push', 'pop') for i in ins),
         'no hidden service call or stack-frame producer')
    for i in ins:
        if i.mnemonic.startswith(('j', 'loop')):
            need(len(i.operands) == 1 and i.operands[0].type == X86_OP_IMM and i.operands[0].imm in bounds,
                 'every scanner branch enters its own complete instruction')
    reads = [int(i.op_str.rsplit('0x', 1)[1].rstrip(']'), 16) for i in ins
             if i.mnemonic == 'mov' and i.op_str.startswith('ah, byte ptr es:')]
    need(tuple(reads) == GROUPS and [(i.mnemonic, i.op_str) for i in ins if i.mnemonic in ('in', 'out')] == [('out', '0x5f, al')],
         'all nine BIOS groups in source order and the original delay port')
    digest = hashlib.sha256(image).hexdigest()
    lines = source.splitlines()
    source_lines = [next(i + 1 for i, line in enumerate(lines) if line.startswith(b'void input_reset_sense_key_held')), len(lines) - 1]
    owner = dict(unit_id=UNIT, name='input_reset_sense_key_held()', source=SOURCE, object=OBJECT,
        segment=CS, offset=BASE, start=start, size=SIZE, coordinate_space='decoded-load', canonical_file_offset=None,
        target_sha256=digest, candidate_sha256=digest, ordered_relocations=[], procedure_count=1,
        procedures=[dict(name='input_reset_sense_key_held()', offset=0, size=SIZE, callee_pop_bytes=0, instruction_count=115)],
        code_bytes=SIZE, initialized_data_bytes=0, private_data_bytes=0, private_bss_bytes=0,
        forwarding_chain=[WRAPPER, INCLUDE, SOURCE], source_function_lines=source_lines,
        abi='far C no arguments/no cleanup; original register and BIOS/port behavior')
    return dict(owners=[owner], code_bytes=SIZE, procedures=1, native_fields=fields, containing_CODE_bytes=SIZE + 1,
        natural_emitters=natural, probe_receipt_sha256=hashlib.sha256(proof_raw).hexdigest(),
        BIOS_groups=list(GROUPS), legacy_codestring_accepted=False, excluded_tail_extent=[CS, BASE + SIZE, 1],
        trailer_layout_or_provenance_resolved=False, runtime_matrix_required=False, whole_product_accepted=False)


if __name__ == '__main__':
    from pathlib import Path
    import build_th03_op_work as build
    from review_th03_op_cfg_work import images
    from lib.op_startup_cold import verify as cold_graph
    root = Path(__file__).resolve().parents[2]
    work, target, candidate, cold, cold_raw = images(root)
    cold_graph(root, work, target, candidate, cold)
    print(json.dumps(dict(cold_report_sha256=hashlib.sha256(cold_raw).hexdigest(),
                         scope=verify(root, work, target, candidate, build.source_graph())), indent=2))
