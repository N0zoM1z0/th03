"""Complete file APIs, DOS helpers and PF INT21 hook with native CS storage."""
import hashlib
import json
import re
import struct
import tomllib

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM, X86_REG_AH, X86_REG_CS
from build_th03_mainl_file_work import STATE, DRIVER, REPORT, wrapper, response
from build_th03_mainl_resources_work import native_records, public_records
from lib.omf import parse_omf, describe_omf
from lib.pc98 import parse_mz
from lib.op_asset_native import extent
from lib.op_shared_native import address
from lib.mainl_staff_source import statements
from lib.decoded_mainl_root_helpers_layout import native as root_native, OBJECT, WRAPPER, CODE_BASE, DATA_BASE, DS
from probe_th03_main_boss_marisa_cpp import code_publics

FILE_UNIT, DOS_UNIT, HOOK_UNIT, DATA_UNIT = ('th03-mainl-decoded-file-library', 'th03-mainl-decoded-file-dos-helpers',
    'th03-mainl-decoded-pfint21', 'th03-mainl-decoded-file-initialized-data')
UNITS = {FILE_UNIT, DOS_UNIT, HOOK_UNIT, DATA_UNIT}
SELECTED_SOURCE = STATE[0][1]
BSS_BASE = 0x13F6
FILE = (('FILE_APPEND', 0x786, 84, 4), ('FILE_FLUSH', 0x7DA, 107, 0), ('FILE_CLOSE', 0x846, 15, 0),
        ('FILE_CREATE', 0x856, 64, 4), ('FILE_EXIST', 0x896, 28, 4), ('FILE_READ', 0x8B2, 180, 6),
        ('FILE_ROPEN', 0x966, 59, 4), ('FILE_SEEK', 0x9A2, 52, 6), ('FILE_TELL', 0x9D6, 14, 0),
        ('FILE_SIZE', 0x9E4, 14, 0), ('FILE_WRITE', 0x9F2, 166, 6))
DOS = (('DOS_AXDX', 0x6AE, 23, 6), ('DOS_FILESIZE', 0x6C6, 55, 2))
FILE_SOURCES = ['src/mainl/archive_io/file_' + n + '.asm' for n in ('append', 'close', 'create', 'exist', 'read', 'ropen', 'seek', 'size', 'write')]
DOS_SOURCES = ['src/mainl/archive_io/dos_axdx.asm', 'src/mainl/archive_io/dos_filesize.asm']
HOOK_SOURCE = 'src/mainl/archive_io/pfint21.asm'
SENTINEL = (0x29AE, 0x29AF)
HOOK_CODE = ((0x2856, 188), (0x2912, 56), (0x294A, 56), (0x29B2, 198), (0x2A7A, 51))
FILE_BSS = (('file_Pointer', 0x1406, 4), ('file_Buffer', 0x140A, 4), ('file_BufferPos', 0x140E, 4),
            ('file_BufPtr', 0x1412, 2), ('file_InReadBuf', 0x1414, 2), ('file_Eof', 0x1416, 2), ('file_ErrorStat', 0x1418, 2))


def need(value, message):
    if not value:
        raise ValueError('MAINL file native: ' + str(message))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def selected_pair(root, work, files):
    report_raw = (root / REPORT).read_bytes()
    report = json.loads(report_raw)
    need(report['complete'] and not report['source_acceptance'] and not report['whole_product_cold_rebuilt'] and
         report['context_project_objects'] == 35 and report['driver_sha256'] == sha((root / DRIVER).read_bytes()) and
         report['cold_report_sha256'] == sha((root / '.analysis/work/mainl-build.json').read_bytes()) and
         report['source_sha256'] == {n: sha((root / n).read_bytes()) for _, n in STATE}, 'complete maintained state/recipe/cold context binding')
    generated, link = wrapper(files), response(files)
    need(report['wrapper_sha256'] == sha(generated) and report['response_sha256'] == sha(link) and
         (root / '.analysis/work/file-root.asm').read_bytes() == generated and
         (root / '.analysis/work/file-root.lnk').read_bytes() == link, 'actual include and unchanged link position')
    config = tomllib.loads((root / 'config/toolchain.toml').read_text())
    prefix = root / config['paths']['wine_prefix']
    commands = [ ['/usr/bin/wine-stable', str(prefix / 'drive_c/TASM50/bin/TASM32.EXE'), '/m', '/mx', '/kh32768', '/t',
                  '/dGAME=3', WRAPPER, r'probe\fileroot.obj'],
                 ['/usr/bin/wine-stable', str(root / config['paths']['msdos_player']), '-e', '-x', 'tlink', r'@probe\fileroot.lnk'] ]
    need([(p['label'], p['command'], p['returncode']) for p in report['native_phases']] ==
         [(f'round{n}-{name}', commands[i], 0) for n in (1, 2) for i, name in enumerate(('assemble', 'link'))], 'two actual selected assembly/link rounds')
    need([r['round'] for r in report['rounds']] == [1, 2], 'two complete selected output vectors')
    rounds = []
    for row in report['rounds']:
        outputs = {}
        need(set(row['outputs']) == {'obj', 'exe', 'map'}, 'whole selected vector')
        for kind, info in row['outputs'].items():
            raw = (root / info['path']).read_bytes()
            need(info['bytes'] == len(raw) and info['sha256'] == sha(raw), 'current selected raw output')
            outputs[kind] = raw
        need(outputs['exe'] == (work / 'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map'] == (work / 'obj/th03/mainl.map').read_bytes(), 'whole pinned target and retained MAP equality')
        rounds.append(outputs)
    need(rounds[0] == rounds[1], 'complete raw selected OBJ/EXE/MAP repeat equality')
    raw, baseline = rounds[0]['obj'], (work / OBJECT).read_bytes()
    need(native_records(raw) == native_records(baseline) and public_records(raw) == public_records(baseline),
         'literal native payload/fixup order and complete public identity')
    description = describe_omf(raw)
    replacements = dict(STATE)
    need(description['valid'] and description['module_name'] == WRAPPER and
         description['translator_comments'] == ['Turbo Assembler  Version 5.0'] and
         description['dependency_paths'] == [replacements.get(n, n) for n in describe_omf(baseline)['dependency_paths']],
         'actual three maintained state includes and complete native dependency closure')
    # Semantic declarations may change whitespace, never storage, names or types.
    keywords = {b'public', b'label', b'word', b'dword', b'dw', b'dd', b'db', b'if', b'ge', b'endif'}
    compact = lambda raw: tuple(b''.join(t.upper() if t.lower() in keywords else t for t in row) for row in statements(raw))
    for old, new in STATE:
        need(compact(files[old]) == compact((root / new).read_bytes()), 'complete original state declarations: ' + new)
    return raw, parse_mz(rounds[0]['exe']), report, sha(report_raw)


def byte_map(raw, segment):
    result = {}
    for record in parse_omf(raw):
        if record.name == 'LEDATA' and record.data[0] == segment:
            start = int.from_bytes(record.data[1:3], 'little')
            for i, value in enumerate(record.data[3:]):
                need(start + i not in result, 'nonoverlapping native initializer records')
                result[start + i] = value
    return result


def resolve(raw, start, size, linked, holes=()):
    payload = byte_map(raw, 1)
    missing = {i for i in range(start, start + size) if i - CODE_BASE not in payload}
    need(missing == set(holes), 'complete native coverage except the explicit uninitialized sentinel WORD')
    # Only the source-declared DW ? uses real repeated TLINK output. Never
    # invent missing native CODE or initialize the source to target bytes.
    code = bytes(payload[i - CODE_BASE] if i - CODE_BASE in payload else linked.program_image[i] for i in range(start, start + size))
    image, fields, relocs, block = bytearray(code), [], [], None
    for record in parse_omf(raw):
        if record.name == 'LEDATA':
            block = record.data[0], int.from_bytes(record.data[1:3], 'little')
        elif record.name == 'FIXUPP':
            at = 0
            while at < len(record.data):
                loc, low, method = record.data[at:at + 3]
                at += 3
                need(loc & 128 and method & ~3 in (4, 20, 84) and method & 3 < 3, 'literal unthreaded root field grammar')
                frame = None
                if method & ~3 in (4, 20):
                    frame = record.data[at]
                    at += 1
                index = record.data[at]
                at += 1
                width = {1: 2, 2: 2, 3: 4}[loc >> 2 & 15]
                site = CODE_BASE + block[1] + (loc & 3) * 256 + low
                if block[0] != 1 or not start <= site < start + size:
                    need(block[0] != 1 or not any(site < b < site + width for b in (start, start + size)), 'no straddling native field')
                    continue
                need(width == 2 and loc & 0x40 and not set(range(site, site + width)) & set(holes), 'whole emitted native WORD field')
                offset = site - start
                addend = int.from_bytes(code[offset:offset + 2], 'little')
                if (method, frame, index) == (0x55, None, 1):
                    need(loc >> 2 & 15 == 2 and addend == 0, 'actual group1 segment base')
                    value = DS
                    relocs.append([0, site])
                else:
                    need(loc >> 2 & 15 == 1 and (method, frame, index) in
                         ((0x54, None, 1), (0x54, None, 2), (4, 2, 9), (0x14, 1, 9)), 'actual own CODE/DATA/DGROUP BSS offset WORD')
                    value = {1: CODE_BASE, 2: DATA_BASE, 9: BSS_BASE}[index] + addend
                image[offset:offset + 2] = value.to_bytes(2, 'little')
                fields.append(dict(site=site, locat=loc, method=method, frame=frame, target=index, addend=addend, value=value))
    return bytes(image), fields, relocs


def verify(root, work, target, candidate, graph, files):
    raw, linked, report, report_sha = selected_pair(root, work, files)
    _, description = root_native(raw)
    need([r.data for r in parse_omf(raw) if r.name == 'GRPDEF'] ==
         [bytes((20, 255, 9, 255, 2)), bytes((21, 255, 7, 255, 6, 255, 5, 255, 4, 255, 3))], 'native DGROUP member/frame identities')
    row, = [r for r in graph if r['output'] == OBJECT]
    need((row['source'], row['kind'], row['game'], row['binary']) == (WRAPPER, 'tasm', 3, 'L'), 'actual GAME3/L root producer')
    for source in FILE_SOURCES + DOS_SOURCES + [HOOK_SOURCE]:
        need(files[WRAPPER].count(('include ' + source).encode()) == 1 and source in description['dependency_paths'] and
             files[source] == (work / source).read_bytes() and
             files[source].replace(b'\r\n', b'\n') == (root / source).read_bytes().replace(b'\r\n', b'\n') and
             statements(files[source]) == statements(files['libs/master.lib/' + source.rsplit('/', 1)[1]]), 'actual complete library source: ' + source)
    table = (work / 'obj/th03/mainl.map').read_text()
    for cls, base, size, name in (('CODE', CODE_BASE, 10944, '_TEXT'), ('DATA', DATA_BASE, 2036, '_DATA'), ('BSS', BSS_BASE, 5108, '_BSS')):
        seg, group = (0, '(none)') if cls == 'CODE' else (DS, 'DGROUP')
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{base:04X}\s+{size:04X}\s+C={cls}\s+S={name}\s+G={re.escape(group)}\s+M=th03_mainl\.asm\s+ACBP=48\s*$', table)) == 1, 'whole containing native layout')
    owners, native = [], []
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    for unit, source, start, size, procedures, evens, field_count in (
        (FILE_UNIT, FILE_SOURCES[0], 0x786, 786, FILE, (0x845, 0x855, 0x9A1), 88),
        (DOS_UNIT, DOS_SOURCES[0], 0x6AE, 80, DOS, (0x6C5, 0x6FD), 0)):
        image, fields, relocations = resolve(raw, start, size, linked)
        need(len(fields) == field_count and not relocations, 'complete file/DOS native field stream')
        extent((target, candidate), image, 0, start, [])
        decoded = []
        for name, off, count, cleanup in procedures:
            body = list(decoder.disasm(image[off - start:off - start + count], off))
            need(sum(i.size for i in body) == count and body[-1].mnemonic == 'retf' and
                 (int(body[-1].op_str, 0) if body[-1].op_str else 0) == cleanup and
                 (off - CODE_BASE, name) in code_publics(raw, 1) and address(table, name) == (0, off), 'complete public far Pascal procedure/cleanup: ' + name)
            decoded.append(dict(name=name, offset=off - start, size=count, callee_pop_bytes=cleanup, instruction_count=len(body)))
        need(sum(p['size'] for p in decoded) + len(evens) == size and
             all(image[a - start] == 0x90 for a in evens), 'complete procedure/ordinary EVEN partition')
        owners.append(owner(unit, source, 0, start, image, size, 0, decoded, [], report))
        native.append(dict(unit_id=unit, fields=fields, ordered_relocations=[], ordinary_outer_EVEN_bytes=list(evens)))
    image, fields, relocations = resolve(raw, 0x2850, 605, linked, SENTINEL)
    need(len(fields) == 52 and relocations == [[0, 0x295D]], 'all52 hook fields and sole group1 MZ segment entry')
    extent((target, candidate), image, 0, 0x2850, relocations)
    need(re.search(rb'\bdefault\s+dw\s+\?,\s*_Thru', files[HOOK_SOURCE]) and
         linked.program_image[0x29AE:0x29B0] == b'\0\0', 'source-declared uninitialized sentinel; real repeat-linked zero file storage')
    code = [i for off, count in HOOK_CODE for i in decoder.disasm(image[off - 0x2850:off - 0x2850 + count], off)]
    need(sum(i.size for i in code) == 549, 'all hook instruction fragments exclude tables/state')
    bounds = {i.address for i in code}
    for i in code:
        if i.mnemonic.startswith(('j', 'loop')) and i.operands[0].type == X86_OP_IMM:
            need(i.operands[0].imm in bounds, 'hook static branches enter owned instructions')
    writer, = [i for i in code if i.mnemonic == 'mov' and i.operands[0].type == X86_OP_MEM and
               i.operands[0].mem.segment == X86_REG_CS and i.operands[0].mem.disp == 0x29AE]
    need(writer.operands[0].size == 1 and writer.operands[1].reg == X86_REG_AH, 'sentinel low BYTE is written from live AH before dispatch')
    dispatch = [struct.unpack_from('<HH', image, off - 0x2850) for off in range(0x2982, 0x29B2, 4)]
    need([a for a, _ in dispatch] == [0x3D, 0x3E, 0x3F, 0x42, 0x46, 0x40, 0x45, 0x4C, 0x57, 0x5C, 0x44, 0] and
         all(dest in bounds for _, dest in dispatch) and dispatch[-1][1] == 0x2A82 and
         struct.unpack_from('<H', image, 0x2A78 - 0x2850)[0] == sum(1 << bit for bit in (0, 1, 2, 3, 6, 7, 10, 12)),
         'all12 dispatch records and semantic IOCTL bit mask')
    need(image[:6] == b'\0' * 5 + b'\x90' and code[-1].mnemonic == 'iret', 'five real CS state bytes,ordinary EVEN and native interrupt return')
    for name, off, cleanup in (('PFSTART', 0x2856, 4), ('PFEND', 0x2912, 0)):
        need(address(table, name) == (0, off) and (off - CODE_BASE, name) in code_publics(raw, 1), 'both hook API native/MAP publics')
        count = 188 if cleanup else 56
        last = next(i for i in code if i.address + i.size == off + count)
        need(last.mnemonic == 'retf' and (int(last.op_str, 0) if last.op_str else 0) == cleanup, 'native hook API cleanup')
    procedures = [dict(name='PFSTART', offset=6, size=188, callee_pop_bytes=4), dict(name='PFEND', offset=194, size=56, callee_pop_bytes=0),
                  dict(name='pfint21', offset=250, size=355, code_bytes=305, embedded_data_bytes=50, entry_kind='interrupt', return_kind='iret')]
    owners.append(owner(HOOK_UNIT, HOOK_SOURCE, 0, 0x2850, image, 550, 55, procedures, relocations, report))
    native.append(dict(unit_id=HOOK_UNIT, fields=fields, ordered_relocations=relocations, instruction_bytes=549,
        ordinary_outer_EVEN_bytes=[0x2855], initialized_CS_state_bytes=5, embedded_table_bytes=50,
        dispatch_records=[dict(ah=a, target=b) for a, b in dispatch], source_uninitialized_file_slot=[0x29AE, 2],
        native_LEDATAs_cover_uninitialized_slot=False, slot_bytes_from_two_real_link_rounds=True, source_initializer_added=False))
    data = byte_map(raw, 2)
    initialized = bytes(data[i] for i in range(0x554 - DATA_BASE, 0x558 - DATA_BASE))
    need(initialized == struct.pack('<Hh', 0, -1), 'two natural initialized file state WORDs')
    extent((target, candidate), initialized, DS, 0x554, [])
    for name, off in (('file_BufferSize', 0x554), ('file_Handle', 0x556)):
        need(address(table, name) == address(table, '_' + name) == (DS, off), 'both initialized-state aliases in both MAP tables')
    for name, off, size in FILE_BSS:
        need(address(table, name) == address(table, '_' + name) == (DS, off), 'both BSS aliases in both MAP tables')
    need(sum(n for _, _, n in FILE_BSS) == 20 and not byte_map(raw, 9), 'twenty uninitialized file bytes and no BSS initializer records')
    owners.append(owner(DATA_UNIT, SELECTED_SOURCE, DS, 0x554, initialized, 0, 4, [], [], report))
    return dict(owners=owners, source_CODE_bytes=1416, source_initialized_DATA_bytes=59, procedures=16,
        native_scopes=native, source_paths=FILE_SOURCES + DOS_SOURCES + [HOOK_SOURCE] + [n for _, n in STATE],
        file_BSS_bytes=20, hook_BSS_bytes=134, BSS_file_byte_credit=0, selected_build_report_sha256=report_sha,
        selected_assembly_link_rounds=2, context_project_objects_reused=35, original_cold_rebuilt=False,
        physical_DOS_or_vector_execution_claimed=False, runtime_matrix_required=False, whole_product_accepted=False)


def owner(unit, source, segment, offset, image, code, data, procedures, relocations, report):
    digest = sha(image)
    return dict(unit_id=unit, name=unit.removeprefix('th03-mainl-decoded-'), source=source, object=OBJECT, origin='library',
        segment=segment, offset=offset, start=segment * 16 + offset, size=len(image), coordinate_space='decoded-load',
        canonical_file_offset=None, target_sha256=digest, candidate_sha256=digest, ordered_relocations=relocations,
        code_bytes=code, initialized_data_bytes=data, procedure_count=len(procedures), procedures=procedures,
        private_data_bytes=0, private_bss_bytes=0, maintained_native_object=report['rounds'][0]['outputs']['obj']['path'],
        abi='original16-bit far Pascal file APIs/native interrupt frame; original unchecked state and carry behavior')


if __name__ == '__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['file_native'], indent=2))
