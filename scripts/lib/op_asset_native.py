"""Complete OP PI procedures and PFOPEN in its actual split tail producer."""
import hashlib
import re

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.omf import describe_omf, parse_omf
from lib.op_shared_native import address, sdk_inventory
from lib.decoded_mainl_pi_layout import native_image as pi_shape
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

CS, DS = 0xBEB, 0xD7F
PI = (
    ('pi_put', 'src/shared/formats/pi_put.cpp', 0x4A6, 173, (
        ('th03-op-decoded-pi-palette', '@PI_PALETTE_APPLY$QI', 'pi_palette_apply(int)', 0, 37, 2),
        ('th03-op-decoded-pi-put', '@PI_PUT_8$QIII', 'pi_put_8(int,int,int)', 37, 136, 6))),
    ('pi_load', 'src/shared/formats/pi_load.cpp', 0xA90, 70, (
        ('th03-op-decoded-pi-load', '@PI_LOAD$QINXC', 'pi_load(int,const char far*)', 0, 70, 6),)),
)
PF_SOURCE, PF_PROVIDER = 'src/shared/formats/pfopen.asm', 'th03/formats/pfopen.asm'
PF_WRAPPER, PF_OBJECT = 'th03_optail.asm', 'obj/th03/optail.obj'
PF_BASE, PF_START, PF_SIZE = 0x2B5A, 0x2EF2, 281
PF_UNIT = 'th03-op-decoded-pfopen'
UNITS = {p[0] for *_, procedures in PI for p in procedures} | {PF_UNIT}


def need(value, message):
    if not value:
        raise ValueError('OP asset native: ' + str(message))


def extent(executables, image, segment, offset, relocations):
    start, size = segment * 16 + offset, len(image)
    for executable in executables:
        need(image == executable.program_image[start:start + size], 'complete independently resolved native/target/candidate bytes')
        need([[r.segment, r.offset] for r in executable.relocations if start <= r.linear < start + size] == relocations,
             'complete literal ordered MZ vector')
        need(not any(r.linear < start < r.linear + 2 or r.linear < start + size < r.linear + 2
                     for r in executable.relocations), 'no straddling relocation')


def owner(unit, source, obj, segment, offset, body, relocations, name, cleanup, chain):
    ins = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(body, offset))
    need(sum(i.size for i in ins) == len(body) and (ins[-1].mnemonic, ins[-1].op_str) == ('retf', str(cleanup)),
         'complete far Pascal procedure and cleanup: ' + name)
    digest = hashlib.sha256(body).hexdigest()
    return dict(unit_id=unit, name=name, source=source, object=obj, segment=segment, offset=offset,
        start=segment * 16 + offset, size=len(body), coordinate_space='decoded-load', canonical_file_offset=None,
        target_sha256=digest, candidate_sha256=digest, ordered_relocations=relocations, procedure_count=1,
        procedures=[dict(name=name, offset=0, size=len(body), callee_pop_bytes=cleanup, instruction_count=len(ins))],
        code_bytes=len(body), initialized_data_bytes=0, private_data_bytes=0, private_bss_bytes=0,
        forwarding_chain=chain, abi=f'far Pascal pop{cleanup}; original unchecked widths and native register traffic')


def pi_verify(root, work, target, candidate, files, table):
    owners, objects = [], []
    for stem, source, base, size, procedures in PI:
        obj, wrapper = f'obj/th03/{stem}.obj', f'th03/{stem}.cpp'
        raw = (work / obj).read_bytes()
        description = describe_omf(raw)
        need(description['valid'] and description['module_name'] == wrapper and
             description['translator_comments'] == ['TC86 Borland C++ 4.02'], 'actual complete OP TC4 PI producer')
        need(segment_definitions(raw) == [dict(index=i, name=n, **{'class': c}, overlay='', size=s)
             for i, n, c, s in ((1, 'SHARED', 'CODE', size), (2, '_DATA', 'DATA', 0), (3, '_BSS', 'BSS', 0))] and
             [r.data[0] for r in parse_omf(raw) if r.name == 'SEGDEF'] == [0x28, 0x48, 0x48] and
             [r.data for r in parse_omf(raw) if r.name == 'GRPDEF'] == [bytes((8, 255, 2, 255, 3))],
             'whole PI producer BYTE CODE alignment and empty DATA/BSS')
        code, blocks = code_bytes(raw, 1)
        need([(b['offset'], b['size']) for b in blocks] == [(0, size)] and
             code_publics(raw, 1) == [(off, symbol) for _, symbol, _, off, _, _ in procedures] and
             not code_publics(raw, 2) and not code_publics(raw, 3), 'complete PI record and public inventory')
        need(files[wrapper] == ('#include "' + source + '"\n').encode() and files[source] == (root / source).read_bytes(),
             'literal maintained PI include chain')
        deps = [re.sub('/+', '/', n.replace(chr(92), '/')) for n in description['dependency_paths']]
        sdk = [n for n in deps if n.startswith('C:/TC4/INCLUDE/')]
        need(sdk == (['C:/TC4/INCLUDE/' + n for n in ('mem.h', '_defs.h', '_null.h')] if stem == 'pi_put' else []),
             'complete consumed PI SDK header declaration')
        need(all(n in files and (work / n).read_bytes() == files[n] for n in deps if not n.startswith('C:/TC4/INCLUDE/')) and
             all(n in deps for n in (wrapper, source)), 'complete actual PI source/header consumption')
        for seg, off, count, cls, name, group, alignment in (
            (CS, base, size, 'CODE', 'SHARED', '(none)', '28'),
            (DS, 0x5F2, 0, 'DATA', '_DATA', 'DGROUP', '48'), (DS, 0x1F70, 0, 'BSS', '_BSS', 'DGROUP', '48')):
            need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+{count:04X}\s+C={cls}\s+S={name}\s+G={re.escape(group)}\s+M=th03/{stem}\.cpp\s+ACBP={alignment}\s*$', table)) == 1,
                 'whole native PI MAP contribution')
        _, fields = pi_shape(raw, stem)  # Shared native grammar only; MAINL addresses are discarded.
        image, relocs = bytearray(code), []
        for f in fields:
            site, width = f['offset'], f['width']
            seg, off = address(table, f['name'])
            if width == 4:
                need(seg == 0 and f['addend'] == 0 and code[site - 1] == 0x9A, 'ordinary external far PI service call')
                value = off | seg << 16
                relocs.append([CS, base + site + 2])
            else:
                need(seg == DS, 'actual OP PI DGROUP reference')
                value = off + f['addend']
            image[site:site + width] = value.to_bytes(width, 'little')
        extent((target, candidate), image, CS, base, relocs)
        need([p[3] for p in procedures] == [sum(p[4] for p in procedures[:i]) for i in range(len(procedures))] and
             sum(p[4] for p in procedures) == size, 'complete contiguous PI function partition')
        for unit, _, name, off, count, cleanup in procedures:
            need(address(table, name) == (CS, base + off), 'actual OP PI procedure address')
            selected = [r for r in relocs if base + off <= r[1] < base + off + count]
            owners.append(owner(unit, source, obj, CS, base + off, image[off:off + count], selected, name, cleanup, [wrapper, source]))
        objects.append(dict(object=obj, native_fields=fields, ordered_relocations=relocs, complete_CODE_bytes=size, consumed_paths=deps))
    return owners, objects


def pf_verify(root, work, target, candidate, files, table):
    raw = (work / PF_OBJECT).read_bytes()
    description = describe_omf(raw)
    records = parse_omf(raw)
    need(description['valid'] and description['module_name'] == PF_WRAPPER and
         description['translator_comments'] == ['Turbo Assembler  Version 5.0'], 'actual split tail TASM producer')
    need(segment_definitions(raw) == [dict(index=i, name=n, **{'class': c}, overlay='', size=s)
         for i, n, c, s in ((1, '_TEXT', 'CODE', 1258), (2, '_DATA', 'DATA', 0), (3, '_BSS', 'BSS', 0))] and
         [r.data[0] for r in records if r.name == 'SEGDEF'] == [0x48] * 3 and
         [r.data for r in records if r.name == 'GRPDEF'] == [bytes((8, 255, 3, 255, 2))], 'whole actual tail segment geometry')
    need((PF_START - PF_BASE, 'PFOPEN') in code_publics(raw, 1) and
         not any(PF_START - PF_BASE < off < PF_START - PF_BASE + PF_SIZE for off, _ in code_publics(raw, 1)),
         'whole PFOPEN public boundary')
    need(address(table, 'PFOPEN') == (0, PF_START), 'both actual OP PFOPEN MAP publics')
    for seg, off, count, cls, name, group in (
        (0, PF_BASE, 1258, 'CODE', '_TEXT', '(none)'),
        (DS, 0x5F2, 0, 'DATA', '_DATA', 'DGROUP'), (DS, 0x1F70, 0, 'BSS', '_BSS', 'DGROUP')):
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+{count:04X}\s+C={cls}\s+S={name}\s+G={re.escape(group)}\s+M=th03_optail\.asm\s+ACBP=48\s*$', table)) == 1,
             'whole containing tail MAP allocation')
    need(files[PF_PROVIDER] == (root / PF_SOURCE).read_bytes() == (work / PF_PROVIDER).read_bytes() and
         files[PF_WRAPPER].count(('include ' + PF_PROVIDER).encode()) == 1,
         'actual byte-for-byte maintained source copy and containing include')
    deps = [n.replace(chr(92), '/') for n in description['dependency_paths']]
    need(PF_PROVIDER in deps and PF_WRAPPER in deps and
         all(n in files and (work / n).read_bytes() == files[n] for n in deps), 'all actual tail source/include dependencies')
    begin, end = PF_START - PF_BASE, PF_START - PF_BASE + PF_SIZE
    # Only the owned procedure must have dense LEDATA. Do not manufacture the
    # containing module's unrelated assembler gaps as zero bytes.
    data, names, block = {}, [], None
    for record in records:
        if record.name == 'LEDATA' and record.data[0] == 1:
            at = int.from_bytes(record.data[1:3], 'little')
            for i, byte in enumerate(record.data[3:]):
                if begin <= at + i < end:
                    need(at + i not in data, 'nonoverlapping PFOPEN native bytes')
                    data[at + i] = byte
        elif record.name == 'EXTDEF':
            at = 0
            while at < len(record.data):
                size = record.data[at]
                names.append(record.data[at + 1:at + 1 + size].decode())
                at += size + 1
                need(record.data[at] == 0, 'untyped tail external')
                at += 1
    need(set(data) == set(range(begin, end)), 'complete PFOPEN LEDATA coverage without implicit fill')
    code = bytes(data[i] for i in range(begin, end))
    image, fields = bytearray(code), []
    for record in records:
        if record.name == 'LEDATA':
            block = record.data[0], int.from_bytes(record.data[1:3], 'little')
        elif record.name == 'FIXUPP':
            at = 0
            while at < len(record.data):
                loc, low, method = record.data[at:at + 3]
                at += 3
                need(loc & 0x80 and method & ~3 in (4, 20, 84) and method & 3 < 3, 'literal unthreaded tail field grammar')
                frame = None
                if method & ~3 in (4, 20):
                    frame = record.data[at]
                    at += 1
                index = record.data[at]
                at += 1
                site = block[1] + (loc & 3) * 256 + low
                width = {1: 2, 2: 2, 3: 4}.get(loc >> 2 & 15)
                need(width is not None, 'native tail field width')
                if block[0] != 1 or not begin <= site < end:
                    need(block[0] != 1 or not any(site < boundary < site + width for boundary in (begin, end)), 'no straddling native field')
                    continue
                site -= begin
                need(width == 2 and loc & 0xFC in (0x84, 0xC4) and frame == 1 and method in (6, 22) and
                     1 <= index <= len(names), 'scoped native external offset WORD field')
                name = names[index - 1]
                addend = int.from_bytes(code[site:site + 2], 'little')
                need(addend == 0, 'zero-addend PFOPEN field')
                seg, off = address(table, name)
                if method == 22:
                    need(loc & 0x40 and seg == DS and name in ('mem_AllocID', 'pfint21_entries', 'pferrno'), 'actual OP PFOPEN DGROUP field')
                    value = off
                elif loc & 0x40:
                    need(seg == 0 and name in ('PFGETX0', 'PFGETX1', 'PFGETC1'), 'same-CS near decoder pointer')
                    value = off
                else:
                    need(seg == 0 and name in ('HMEM_ALLOCBYTE', 'BOPENR', 'BSEEK_', 'BCLOSER', 'HMEM_FREE') and
                         code[site - 2:site] == bytes((0x0E, 0xE8)), 'real emitted PUSH CS/near CALL bridge')
                    value = (off - (PF_START + site + 2)) & 65535
                image[site:site + 2] = value.to_bytes(2, 'little')
                fields.append(dict(site=site, locat=loc, method=method, frame=frame, target=index, name=name, addend=addend))
    need(len(fields) == 12 and len({f['site'] for f in fields}) == 12, 'complete twelve-field native PFOPEN stream')
    extent((target, candidate), image, 0, PF_START, [])
    result = owner(PF_UNIT, PF_SOURCE, PF_OBJECT, 0, PF_START, image, [], 'PFOPEN', 8, [PF_WRAPPER, PF_PROVIDER, PF_SOURCE])
    result['source_transport'] = 'exact byte copy into ' + PF_PROVIDER
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    ins = list(decoder.disasm(image, PF_START))
    bounds = {i.address for i in ins}
    for i in ins:
        if i.mnemonic.startswith(('j', 'loop')):
            need(len(i.operands) == 1 and i.operands[0].type == X86_OP_IMM and i.operands[0].imm in bounds,
                 'every PFOPEN branch enters its own complete instruction')
    compare, = [i for i in ins if i.mnemonic == 'call' and i.address == PF_START + 79]
    need(compare.operands[0].imm == 0x300C and files[PF_WRAPPER].count(b'include libs/master.lib/pf_str_ieq.asm') == 1,
         'actual private near string comparator after excluded alignment byte')
    return result, dict(object=PF_OBJECT, native_fields=fields, complete_containing_CODE_bytes=1258,
        owned_CODE_bytes=PF_SIZE, consumed_paths=deps, containing_producer_accepted=False,
        private_compare_entry=0x300C, following_alignment_accepted=False)


def verify(root, work, target, candidate, files):
    table = (work / 'obj/th03/op.map').read_text()
    owners, objects = pi_verify(root, work, target, candidate, files, table)
    pf, pf_native = pf_verify(root, work, target, candidate, files, table)
    owners.append(pf)
    objects.append(pf_native)
    return dict(owners=owners, code_bytes=524, procedures=4, native_objects=objects,
        sdk_sha256=sdk_inventory(root, ('mem.h', '_defs.h', '_null.h')), private_data_bytes=0, private_bss_bytes=0,
        external_library_or_storage_accepted=False, runtime_matrix_required=False, whole_product_accepted=False)


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
