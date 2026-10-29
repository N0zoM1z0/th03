"""OP's complete CDG loader and text renderer, resolved from its own native MAP."""
import hashlib
import re
import tomllib

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import describe_omf, parse_omf
from lib.decoded_mainl_cdg_layout import native_image as cdg_fields, PROCEDURES as CDG_PROCEDURES
from lib.decoded_mainl_text_layout import FIELDS as TEXT_FIELDS, DEPENDENCIES as TEXT_DEPS
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

CS, DS = 0xBEB, 0xD7F
CDG_SOURCE, TEXT_SOURCE = 'src/shared/formats/cdg_load.cpp', 'src/shared/graphics/text.cpp'
SOURCES = {CDG_SOURCE, TEXT_SOURCE}
CDG_UNIT, TEXT_UNIT = 'th03-op-decoded-cdg-loading', 'th03-op-decoded-graph-putsa-fx'
UNITS = {CDG_UNIT, TEXT_UNIT}
GLYPH = 'src/shared/graphics/text_glyph.inl'
TEXT_PUBLIC = '@GRAPH_PUTSA_FX$QIIINXUC'
TEXT_MAP = 'graph_putsa_fx(int,int,int,const unsigned char far*)'


def need(value, message):
    if not value:
        raise ValueError('OP shared native: ' + str(message))


def address(table, name):
    rows = re.findall(rf'(?m)^\s*([0-9A-F]{{4}}):([0-9A-F]{{4}})\s+(?:idle\s+)?{re.escape(name)}\s*$', table)
    need(len(rows) == 2 and rows[0] == rows[1], 'both OP MAP public tables: ' + name)
    return tuple(int(v, 16) for v in rows[0])


def sdk_inventory(root, names):
    config = tomllib.loads((root / 'config/toolchain.toml').read_text())
    surface, = [s for s in config['surfaces'] if s['id'] == 'tc40j-include']
    consumed = root / config['paths']['wine_prefix'] / 'drive_c/TC4/INCLUDE'
    installed = root / surface['path']
    out = {}
    for name in names:
        a, b = (consumed / name.upper()).read_bytes(), (installed / name.upper()).read_bytes()
        need(a == b, 'actual SDK header matches pinned installation: ' + name)
        out['C:/TC4/INCLUDE/' + name] = hashlib.sha256(a).hexdigest()
    return out


def text_fields(raw):
    records = parse_omf(raw)
    need(tuple(describe_omf(raw)['dependency_paths']) == TEXT_DEPS, 'complete text dependency identity')
    names = ('__ctype', '__mbctype', '__mbcjmstojis', 'GRCG_SETCOLOR', 'GRCG_OFF')
    ext, = [r.data for r in records if r.name == 'EXTDEF']
    need(ext == b''.join(bytes((len(n),)) + n.encode() + b'\0' for n in names), 'all text external identities')
    code, _ = code_bytes(raw, 1)
    fixup, = [r.data for r in records if r.name == 'FIXUPP']
    fields, at = [], 0
    while at < len(fixup):
        loc, low, method = fixup[at:at + 3]
        at += 3
        need(method in (0x16, 0x56), 'literal text field method')
        frame = fixup[at] if method == 0x16 else None
        at += int(frame is not None)
        index = fixup[at]
        at += 1
        site = (loc & 3) * 256 + low
        width = 4 if method == 0x56 else 2
        addend = int.from_bytes(code[site:site + width], 'little')
        fields.append(dict(offset=site, locat=loc, fixdat=method, frame=frame, target=index,
                           name=names[index - 1], addend=addend, width=width, normal_tlink_relaxed_call=False))
    need(tuple((f['offset'], f['locat'], f['fixdat'], f['frame'], f['target'], f['addend']) for f in fields) == TEXT_FIELDS,
         'all six ordered native text fields')
    return fields


def resolve(raw, fields, base, table):
    code, _ = code_bytes(raw, 1)
    image, relocations = bytearray(code), []
    for f in fields:
        site, width, method, addend = f['offset'], f['width'], f['fixdat'], f['addend']
        seg, offset = address(table, f['name'])
        if method == 0x16:
            need(seg == DS and width == 2 and f['frame'] == 1, 'ordinary external near DGROUP field')
            image[site:site + 2] = (offset + addend).to_bytes(2, 'little')
        elif method == 0x56:
            need(seg == 0 and addend == 0 and width == 4 and code[site - 1] == 0x9A, 'ordinary external far service CALL')
            image[site:site + 4] = (offset | seg << 16).to_bytes(4, 'little')
            relocations.append([CS, base + site + 2])
        else:
            need(method == 0x54 and width == 4 and seg == CS and offset == base + addend and
                 f['name'] == 'CDG_FREE' and code[site - 1] == 0x9A, 'normal same-CS native far CALL relaxation')
            # Comparison buffer only: normal TLINK keeps the far return stack
            # with NOP / PUSH CS / CALL near. Native objects remain untouched.
            displacement = (offset - (base + site + 4)) & 65535
            image[site - 1:site + 4] = bytes((0x90, 0x0E, 0xE8)) + displacement.to_bytes(2, 'little')
    return bytes(image), relocations


def verify(root, work, target, candidate, files):
    table = (work / 'obj/th03/op.map').read_text()
    sdk = sdk_inventory(root, ('mbctype.h', 'ctype.h', '_defs.h', 'mbstring.h', '_null.h'))
    owners, objects = [], []
    for stem, source, base, size, unit in (
        ('cdg_load', CDG_SOURCE, 0x5DA, 593, CDG_UNIT), ('grppsafx', TEXT_SOURCE, 0x82B, 613, TEXT_UNIT)):
        obj, wrapper = f'obj/th03/{stem}.obj', f'th03/{stem}.cpp'
        raw = (work / obj).read_bytes()
        native = describe_omf(raw)
        need(native['valid'] and native['module_name'] == wrapper and
             native['translator_comments'] == ['TC86 Borland C++ 4.02'], 'actual complete OP TC4 producer')
        need(segment_definitions(raw) == [dict(index=i, name=n, **{'class': c}, overlay='', size=s)
             for i, n, c, s in ((1, 'SHARED', 'CODE', size), (2, '_DATA', 'DATA', 0), (3, '_BSS', 'BSS', 0))],
             'complete natural CODE and zero private storage')
        records = parse_omf(raw)
        need([r.data[0] for r in records if r.name == 'SEGDEF'] == [0x28, 0x48, 0x48] and
             [r.data for r in records if r.name == 'GRPDEF'] == [bytes((8, 255, 2, 255, 3))],
             'native alignment and sole DGROUP over DATA/BSS')
        need([(b['offset'], b['size']) for b in code_bytes(raw, 1)[1]] == [(0, size)] and
             [r.data[0] for r in records if r.name == 'LEDATA'] == [1], 'one complete CODE record; no other initializer')
        need(files[wrapper] == ('#include "' + source + '"\n').encode() and
             files[source] == (root / source).read_bytes(), 'literal maintained TU source chain')
        deps = [re.sub('/+', '/', n.replace(chr(92), '/')) for n in native['dependency_paths']]
        need(all((n in sdk if n.startswith('C:/TC4/INCLUDE/') else
                  n in files and (work / n).read_bytes() == files[n]) for n in deps) and
             all(n in deps for n in (wrapper, source)), 'complete OP native source/header dependencies')
        if stem == 'grppsafx':
            need(GLYPH in deps and files[GLYPH] == (root / GLYPH).read_bytes(), 'actual bounded glyph include')
            procedures = (('text', 0, 613, 10, TEXT_MAP),)
            publics = [(0, TEXT_PUBLIC)]
            fields = text_fields(raw)
        else:
            procedures = CDG_PROCEDURES
            publics = [(off, name) for _, off, _, _, name in procedures]
            _, fields = cdg_fields(raw)  # Literal native shape only; all addresses resolved from OP below.
        need(code_publics(raw, 1) == publics and not code_publics(raw, 2) and not code_publics(raw, 3),
             'all complete native public boundaries')
        for seg, offset, length, cls, name, group, alignment in (
            (CS, base, size, 'CODE', 'SHARED', '(none)', '28'),
            (DS, 0x5F2, 0, 'DATA', '_DATA', 'DGROUP', '48'), (DS, 0x1F70, 0, 'BSS', '_BSS', 'DGROUP', '48')):
            need(len(re.findall(rf'(?m)^\s*{seg:04X}:{offset:04X}\s+{length:04X}\s+C={cls}\s+S={name}\s+G={re.escape(group)}\s+M=th03/{stem}\.cpp\s+ACBP={alignment}\s*$', table)) == 1,
                 'complete actual OP MAP contribution: ' + stem + '/' + cls)
        image, relocs = resolve(raw, fields, base, table)
        start = CS * 16 + base
        need(image == target.program_image[start:start + size] == candidate.program_image[start:start + size],
             'complete independently resolved OP native/target/candidate bytes')
        for executable in (target, candidate):
            need([[r.segment, r.offset] for r in executable.relocations if start <= r.linear < start + size] == relocs,
                 'complete literal ordered OP MZ vector')
            need(not any(r.linear < start < r.linear + 2 or r.linear < start + size < r.linear + 2
                         for r in executable.relocations), 'no straddling relocation')
        need([off for _, off, *_ in procedures] == [sum(p[2] for p in procedures[:i]) for i in range(len(procedures))]
             and sum(p[2] for p in procedures) == size, 'complete contiguous procedure partition')
        decoded = []
        for name, off, length, cleanup, mapname in procedures:
            need(address(table, mapname) == (CS, base + off), 'actual OP procedure address')
            ins = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(image[off:off + length], base + off))
            need(sum(i.size for i in ins) == length and ins[-1].mnemonic == 'retf' and int(ins[-1].op_str, 0) == cleanup,
                 'complete far Pascal procedure and cleanup: ' + name)
            decoded.append(dict(name=mapname, offset=off, size=length, callee_pop_bytes=cleanup, instruction_count=len(ins)))
        digest = hashlib.sha256(image).hexdigest()
        owners.append(dict(unit_id=unit, name='CDG load/free carrier' if stem == 'cdg_load' else TEXT_MAP,
            source=source, object=obj, segment=CS, offset=base, start=start, size=size,
            coordinate_space='decoded-load', canonical_file_offset=None, target_sha256=digest, candidate_sha256=digest,
            ordered_relocations=relocs, procedure_count=len(procedures), procedures=decoded,
            code_bytes=size, initialized_data_bytes=0, private_data_bytes=0, private_bss_bytes=0,
            forwarding_chain=[wrapper, source], abi='far Pascal; CDG pop8/8/6/6/2; text pop10, far cdecl converter'))
        objects.append(dict(object=obj, complete_CODE_bytes=size, native_fields=fields, ordered_relocations=relocs,
            normal_tlink_relaxed_calls=sum(f['normal_tlink_relaxed_call'] for f in fields), consumed_paths=deps))
    return dict(owners=owners, code_bytes=1206, procedures=6, native_objects=objects, sdk_sha256=sdk,
                private_data_bytes=0, private_bss_bytes=0, physical_font_or_device_accepted=False,
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
