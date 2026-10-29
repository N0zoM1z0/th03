"""Complete SUPER procedures and the naturally generated CS pixel table."""
import hashlib
import json
import re
import tomllib

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_REG_CS
from build_th03_mainl_resources_work import SOURCE as TABLE_SOURCE, OLD, DRIVER, REPORT, wrapper, response, native_records, public_records
from lib.omf import describe_omf, parse_omf
from lib.op_asset_native import extent
from lib.op_shared_native import address
from lib.mainl_staff_source import statements
from lib.decoded_mainl_root_helpers_layout import native as root_native, OBJECT, WRAPPER, CODE_BASE, DATA_BASE, DS
from probe_th03_main_boss_marisa_cpp import code_publics

SUPER_UNIT, TABLE_UNIT = 'th03-mainl-decoded-super-library', 'th03-mainl-decoded-draw-table'
SUPER_START, SUPER_SIZE, TABLE_START, TABLE_SIZE, BSS_BASE = 0x237E, 1008, 0x1AAA, 1024, 0x13F6
SOURCES = ['src/mainl/resources/' + n + '.asm' for n in
           ('super_free', 'super_entry_pat', 'super_entry_at', 'super_entry_bfnt', 'super_cancel_pat', 'super_put')]
# Six far public procedures, four near drawing helpers and one tail dispatcher.
PROCEDURES = (('SUPER_FREE', 0x237E, 48, 'retf', 0), ('SUPER_ENTRY_PAT', 0x23C2, 171, 'retf', 8),
    ('SUPER_ENTRY_AT', 0x246E, 116, 'retf', 6), ('SUPER_ENTRY_BFNT', 0x24E2, 137, 'retf', 4),
    ('SUPER_CANCEL_PAT', 0x256C, 79, 'retf', 2), ('SUPER_PUT', 0x25BC, 240, 'retf', 6),
    ('SUPERPUT_DISP1', 0x26AC, 35, 'ret', 0), ('SUPERPUT_DISP2', 0x26D0, 45, 'ret', 0),
    ('SUPERPUT_DISP3', 0x26FE, 54, 'ret', 0), ('SUPERPUT_DISP4', 0x2734, 49, 'ret', 0),
    ('SUPERPUT_DISP', 0x2766, 8, 'jmp', 0))
EVENS = (0x246D, 0x256B, 0x25BB, 0x26CF, 0x26FD, 0x2765)
SHARED_ERROR = (0x23AE, 20)
SMC = {0x2769: ('mov', 2), 0x276C: ('jmp', 2),
       **{a: ('add', 1) for a in (0x26C7, 0x26F5, 0x272C, 0x275D)},
       **{a: ('mov', 1) for a in (0x26C9, 0x26F7, 0x272E, 0x275F)}}


def need(value, message):
    if not value:
        raise ValueError('MAINL resources native: ' + str(message))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def dense(raw, start, size):
    data = {}
    begin, end = start - CODE_BASE, start - CODE_BASE + size
    for r in parse_omf(raw):
        if r.name == 'LEDATA' and r.data[0] == 1:
            base = int.from_bytes(r.data[1:3], 'little')
            for i, value in enumerate(r.data[3:]):
                if begin <= base + i < end:
                    need(base + i not in data, 'nonoverlapping native bytes')
                    data[base + i] = value
    need(set(data) == set(range(begin, end)), 'complete scoped LEDATA without fabricated fill')
    return bytes(data[i] for i in range(begin, end))


def resolve(raw, start, size):
    code = dense(raw, start, size)
    image, fields, block = bytearray(code), [], None
    begin, end = start - CODE_BASE, start - CODE_BASE + size
    for r in parse_omf(raw):
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
                need(width == 2 and loc & 0x40 and loc >> 2 & 15 == 1 and
                     (method, frame, index) in ((0x54, None, 1), (0x54, None, 2), (0x14, 1, 2), (0x14, 1, 9), (4, 2, 9)),
                     'ordinary own-CS offset or DGROUP member WORD field')
                addend = int.from_bytes(code[offset:offset + 2], 'little')
                value = {1: CODE_BASE, 2: DATA_BASE, 9: BSS_BASE}[index] + addend
                image[offset:offset + 2] = value.to_bytes(2, 'little')
                fields.append(dict(site=CODE_BASE + site, locat=loc, method=method, frame=frame, target=index,
                                   addend=addend, value=value, width=width))
    return bytes(image), fields


def selected_pair(root, work, files):
    raw_report = (root / REPORT).read_bytes()
    report = json.loads(raw_report)
    need(report['complete'] and not report['source_acceptance'] and not report['whole_product_cold_rebuilt'] and
         report['context_project_objects'] == 35 and report['driver_sha256'] == sha((root / DRIVER).read_bytes()) and
         report['cold_report_sha256'] == sha((root / '.analysis/work/mainl-build.json').read_bytes()) and
         report['source_sha256'] == sha((root / TABLE_SOURCE).read_bytes()), 'complete source-bound selected native recipe')
    generated, link = wrapper(files), response(files)
    need((root / '.analysis/work/resources-root.asm').read_bytes() == generated and report['wrapper_sha256'] == sha(generated) and
         (root / '.analysis/work/resources-root.lnk').read_bytes() == link and report['response_sha256'] == sha(link),
         'actual generated include and unchanged link position/context')
    cfg = tomllib.loads((root / 'config/toolchain.toml').read_text())
    prefix = root / cfg['paths']['wine_prefix']
    commands = [ ['/usr/bin/wine-stable', str(prefix / 'drive_c/TASM50/bin/TASM32.EXE'), '/m', '/mx', '/kh32768', '/t',
                  '/dGAME=3', WRAPPER, r'probe\resroot.obj'],
                 ['/usr/bin/wine-stable', str(root / cfg['paths']['msdos_player']), '-e', '-x', 'tlink', r'@probe\resroot.lnk'] ]
    need([(p['label'], p['command'], p['returncode']) for p in report['native_phases']] ==
         [(f'round{n}-{name}', commands[i], 0) for n in (1, 2) for i, name in enumerate(('assemble', 'link'))],
         'two actual selected assembly/link rounds')
    need([r['round'] for r in report['rounds']] == [1, 2], 'two complete selected output vectors')
    rounds = []
    for row in report['rounds']:
        outputs = {}
        need(set(row['outputs']) == {'obj', 'exe', 'map'}, 'complete selected vector')
        for kind, meta in row['outputs'].items():
            raw = (root / meta['path']).read_bytes()
            need((len(raw), sha(raw)) == (meta['bytes'], meta['sha256']), 'current selected raw output identity')
            outputs[kind] = raw
        need(outputs['exe'] == (work / 'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map'] == (work / 'obj/th03/mainl.map').read_bytes(), 'whole pinned target and retained MAP equality')
        rounds.append(outputs)
    need(rounds[0] == rounds[1], 'complete raw selected OBJ/EXE/MAP repeat equality')
    raw, baseline = rounds[0]['obj'], (work / OBJECT).read_bytes()
    need(native_records(raw) == native_records(baseline) and public_records(raw) == public_records(baseline),
         'literal native records/fixup order and all public records with multiplicity')
    description = describe_omf(raw)
    old_description = describe_omf(baseline)
    need(description['valid'] and description['module_name'] == WRAPPER and
         description['translator_comments'] == ['Turbo Assembler  Version 5.0'] and
         description['dependency_paths'] == [TABLE_SOURCE if n == OLD else n for n in old_description['dependency_paths']],
         'actual generated table consumption and unchanged full root dependency closure')
    return raw, report, sha(raw_report)


def verify(root, work, target, candidate, graph, files):
    baseline = (work / OBJECT).read_bytes()
    root_native(baseline)
    raw, report, report_sha = selected_pair(root, work, files)
    root_native(raw)
    need([r.data for r in parse_omf(raw) if r.name == 'GRPDEF'] ==
         [bytes((20, 255, 9, 255, 2)), bytes((21, 255, 7, 255, 6, 255, 5, 255, 4, 255, 3))],
         'actual DGROUP includes DATA/BSS; explicit SEG_DATA frame uses that group')
    row, = [r for r in graph if r['output'] == OBJECT]
    need((row['source'], row['wrapper'], row['kind'], row['game'], row['binary']) == (WRAPPER, WRAPPER, 'tasm', 3, 'L'),
         'actual current containing root producer')
    for source in SOURCES:
        need(files[WRAPPER].count(('include ' + source).encode()) == 1 and
             files[source] == (work / source).read_bytes() and
             files[source].replace(b'\r\n', b'\n') == (root / source).read_bytes().replace(b'\r\n', b'\n') and
             statements(files[source]) == statements(files['libs/master.lib/' + source.rsplit('/', 1)[1]]),
             'complete consumed symbolic library source: ' + source)
    table = (work / 'obj/th03/mainl.map').read_text()
    for cls, base, size, name in (('CODE', CODE_BASE, 10944, '_TEXT'), ('DATA', DATA_BASE, 2036, '_DATA'), ('BSS', BSS_BASE, 5108, '_BSS')):
        seg, group = (0, '(none)') if cls == 'CODE' else (DS, 'DGROUP')
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{base:04X}\s+{size:04X}\s+C={cls}\s+S={name}\s+G={re.escape(group)}\s+M=th03_mainl\.asm\s+ACBP=48\s*$', table)) == 1,
             'complete native root MAP contribution and member offset: ' + cls)
    for name, off in (('super_buffer', 0x87A), ('super_patnum', 0x87C), ('super_charfree', 0x87E),
                      ('super_patdata', BSS_BASE + 106), ('super_patsize', BSS_BASE + 1130)):
        need(address(table, name) == (DS, off), 'actual external storage in both MAP tables')
    image, fields = resolve(raw, SUPER_START, SUPER_SIZE)
    need(len(fields) == 50, 'complete fifty-field native SUPER stream')
    extent((target, candidate), image, 0, SUPER_START, [])
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    ins = list(decoder.disasm(image, SUPER_START))
    need(sum(i.size for i in ins) == SUPER_SIZE, 'complete SUPER instruction and alignment partition')
    bounds = {i.address for i in ins}
    for i in ins:
        if i.mnemonic.startswith(('j', 'loop')):
            need(i.operands[0].type == X86_OP_IMM and i.operands[0].imm in bounds, 'all static branches enter complete owned instructions')
    procedures = []
    for index, (name, start, size, mnemonic, pop) in enumerate(PROCEDURES):
        body = [i for i in ins if start <= i.address < start + size]
        need(sum(i.size for i in body) == size and body[-1].mnemonic == mnemonic and
             (mnemonic == 'jmp' or (int(body[-1].op_str, 0) if body[-1].op_str else 0) == pop), 'complete native procedure and cleanup: ' + name)
        if index < 6:
            need((start - CODE_BASE, name) in code_publics(raw, 1) and address(table, name) == (0, start), 'whole native and both MAP public entries')
        procedures.append(dict(name=name, offset=start - SUPER_START, size=size, callee_pop_bytes=pop,
                               instruction_count=len(body), tail_dispatch=mnemonic == 'jmp'))
    need(sum(p['size'] for p in procedures) + SHARED_ERROR[1] + len(EVENS) == SUPER_SIZE and
         all(next(i for i in ins if i.address == a).mnemonic == 'nop' for a in EVENS), 'complete eleven procedures/shared exits/ordinary outer EVEN partition')
    smc = []
    for field in [f for f in fields if f['target'] == 1]:
        writer = next(i for i in ins if i.address <= field['site'] < i.address + i.size)
        dest = field['value']
        need(dest in SMC and writer.mnemonic == 'mov' and writer.operands[0].type == X86_OP_MEM and
             writer.operands[0].mem.segment == X86_REG_CS and writer.operands[0].mem.disp == dest,
             'own-CS native field is an actual operand writer')
        consumer = next(i for i in ins if i.address <= dest < i.address + i.size)
        need((consumer.mnemonic, consumer.imm_size) == SMC[dest] and consumer.address + consumer.imm_offset == dest and
             writer.operands[0].size == consumer.imm_size, 'each write replaces a complete real immediate/displacement operand')
        if dest == 0x276C:
            need(writer.operands[1].type == X86_OP_IMM and (0x276E + writer.operands[1].imm) & 65535 in (0x26AC, 0x26D0, 0x26FE, 0x2734),
                 'all four relative dispatch writers enter real near helpers')
        smc.append(dict(writer=writer.address, field=field['site'], destination=dest, width=consumer.imm_size, consumer=consumer.address))
    need(len(smc) == 13 and {r['destination'] for r in smc} == set(SMC), 'all thirteen writers and ten operand slots')
    source = (root / TABLE_SOURCE).read_text()
    need('REPT 256' in source and 'REPT 4' in source and 'DD rotation_entry' in source and
         not re.search(r'(?im)^\s*(?:DB|DW|ORG)\b|^\s*DD\s+[0-9]', source), 'natural semantic table generator without literal target bytes/fill')
    expected = bytes(((value >> plane) & 1) | (((value >> (plane + 4)) & 1) << 1) for value in range(256) for plane in range(4))
    data, table_fields = resolve(raw, TABLE_START, TABLE_SIZE)
    need(data == expected and not table_fields and address(table, 'RotTbl') == (0, TABLE_START) and
         (TABLE_START - CODE_BASE, 'RotTbl') in code_publics(raw, 1), 'all256 semantic DWORD entries and actual CS table public')
    extent((target, candidate), data, 0, TABLE_START, [])
    owners = []
    for unit, name, src, start, body, code_bytes, data_bytes, procs in (
        (SUPER_UNIT, 'Complete SUPER sprite library', SOURCES[0], SUPER_START, image, SUPER_SIZE, 0, procedures),
        (TABLE_UNIT, 'Generated packed-pixel plane rotation table', TABLE_SOURCE, TABLE_START, data, 0, TABLE_SIZE, [])):
        digest = sha(body)
        owners.append(dict(unit_id=unit, name=name, source=src, object=OBJECT, origin='library', segment=0, offset=start, start=start,
            size=len(body), coordinate_space='decoded-load', canonical_file_offset=None, target_sha256=digest, candidate_sha256=digest,
            ordered_relocations=[], procedure_count=len(procs), procedures=procs, code_bytes=code_bytes, initialized_data_bytes=data_bytes,
            private_data_bytes=0, private_bss_bytes=0, maintained_native_object=report['rounds'][0]['outputs']['obj']['path'],
            abi='six far Pascal APIs,five private near entries,shared borrowed error frame' if procs else '256 DWORDs in CS; four plane BYTEs per packed-pixel BYTE'))
    return dict(owners=owners, library_CODE_bytes=SUPER_SIZE, library_initialized_DATA_bytes=TABLE_SIZE, procedures=11,
        source_paths=SOURCES + [TABLE_SOURCE], native_fields=fields, ordered_relocations=[], SMC_writers=smc,
        ordinary_outer_EVEN_bytes=list(EVENS), borrowed_error_extent=list(SHARED_ERROR), borrowed_errors_are_procedures=False,
        table_entries=256, table_entry_bytes=4, table_stored_in_CODE_segment=True, table_is_instruction_bytes=False,
        selected_build_report_sha256=report_sha, selected_assembly_link_rounds=2, context_project_objects_reused=35,
        original_native_public_records_equal=True,
        PUBDEF_emission_order_changed=[r.data for r in parse_omf(raw) if r.name == 'PUBDEF'] != [r.data for r in parse_omf(baseline) if r.name == 'PUBDEF'],
        native_FIXUPP_order_unchanged=True,
        original_cold_rebuilt=False, external_DATA_BSS_or_device_accepted=False, runtime_matrix_required=False, whole_product_accepted=False)


if __name__ == '__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['resources_native'], indent=2))
