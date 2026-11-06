"""Maintained semantic CP932 DATA, with the historical extra zero left unowned."""
import json

from build_th03_mainl_resources_work import need, sha
from build_th03_mainl_display_work import literal_fields
from lib.omf import describe_omf, parse_omf
from lib.pc98 import parse_mz
from lib.op_shared_native import address
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_picture_files_native import selected as selected_parent

PREFIX_UNIT = 'th03-mainl-decoded-registration-initialized-bank'
ENDING_UNIT = 'th03-mainl-decoded-ending-text-bank'
SOURCE_MAP = {
    PREFIX_UNIT: ('src/mainl/data/registration.asm', 'obj/th03/regpre.obj'),
    ENDING_UNIT: ('src/mainl/data/ending_text.asm', 'obj/th03/regtail.obj')}
INCLUDE = 'src/mainl/hiscore/regi_codes.inc'
OLD_ROWS = [
    '0000:2D32 0000 C=CODE   S=_TEXT          G=(none)  M=regpre.asm ACBP=48',
    '0E3F:092E 0130 C=DATA   S=_DATA          G=DGROUP  M=regpre.asm ACBP=48']
NEW_ROWS = [OLD_ROWS[0],
    '0E3F:092E 012F C=DATA   S=_DATA          G=DGROUP  M=regpre.asm ACBP=48']


def selected(root, work, graph):
    # Delay historical builders until acceptance.proof_inputs exists.
    import build_th03_mainl_text_banks_work as b
    _, prior, prior_hash = selected_parent(root, work, graph)
    config, config_hash = b.inputs()
    record, digest = b.base.load(b.REPORT)
    sources = {n: (root / n).read_bytes() for n in config['inputs']}
    need(config['inputs'] == [SOURCE_MAP[PREFIX_UNIT][0], SOURCE_MAP[ENDING_UNIT][0], INCLUDE] and
         prior_hash == config['parent_report_sha256'], 'exact maintained bank inputs and actual source parent')
    need(record['complete'] and record['source_acceptance'] is False and
         record['whole_product_accepted'] is False and record['canonical_credit_changed'] is False and
         record['cold_rebuilt'] is False and record['game_objects_recompiled'] == 2 and
         record['cold_game_objects_retained'] == 32 and record['source_root_recompiled'] is False and
         record['source_picture_recompiled'] is False and record['library_rebuilt'] is False and
         record['packing_rebuilt'] is False and record['driver_sha256'] == sha((root / b.DRIVER).read_bytes()) and
         record['config_sha256'] == config_hash and record['source_sha256'] == {n: sha(v) for n, v in sources.items()} and
         record['assembler_sha256'] == sha(b.TASM.read_bytes()) ==
         'ba50fe547863b96242d98cff54cdf95ab268a8682395afad172eedbfc46c5b26' and
         record['parent_report_sha256'] == prior_hash and
         record['cold_report_sha256'] == sha((root / '.analysis/work/mainl-build.json').read_bytes()) and
         record['cold_producers'] == [g for g in graph if g['output'] in {v[1] for v in SOURCE_MAP.values()}] and
         record['original_objects_sha256'] == {v[1]: sha((work / v[1]).read_bytes()) for v in SOURCE_MAP.values()},
         'actual source-bound native stage and pinned emitter')
    transported = {}
    for name, raw in sources.items():
        expected = raw.decode('utf-8').encode('cp932').replace(b'\n', b'\r\n')
        need((b.SCRATCH / name).read_bytes() == expected and
             expected.decode('cp932').replace('\r\n', '\n') == raw.decode('utf-8'), 'literal reversible text transport ' + name)
        transported[name] = sha(expected)
    need(record['transported_sha256'] == transported and
         all((b.SCRATCH / u['module']).read_bytes() == (b.SCRATCH / u['source']).read_bytes() for u in config['units']) and
         (b.SCRATCH / 'driver.py').read_bytes() == (root / b.DRIVER).read_bytes() and
         (b.SCRATCH / 'config.json').read_bytes() == (root / b.CONFIG).read_bytes(), 'actual consumed assembly and recipe snapshots')
    phases = record['phases']
    need([p['label'] for p in phases] == [f'round{i}-{k}' for i in (1, 2)
         for k in ('registration-assemble', 'ending-assemble', 'link')] and
         all(p['returncode'] == 0 and sha((root / p['log_path']).read_bytes()) == p['log_sha256'] for p in phases),
         'all six real native assembler/linker logs')
    dos = ['/usr/bin/wine-stable', str(root / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    vectors = []
    for number, row in enumerate(record['rounds'], 1):
        need(row['round'] == number and set(row['outputs']) == {'registration', 'ending', 'exe', 'map'}, 'complete raw native vector')
        vector = {k: b.base.checked(v) for k, v in row['outputs'].items()}
        old = prior['rounds'][number - 1]
        reused = dict(startup=old['reused_startup'], library=old['reused_library'], root=old['reused_root'], pictures=old['outputs']['obj'])
        need(row['reused'] == reused and all((b.SCRATCH / filename).read_bytes() == b.base.checked(reused[key])
             for key, filename in [('startup', 'c0l.obj'), ('library', f'r{number}.lib'),
                                   ('root', 'rootdata.obj'), ('pictures', 'rootpre.obj')]), 'actual inherited source root/pictures/C0/library')
        rsp = b.parent.parent.runtime.link_response('mainl', work, number).replace(b'af548h', b'af554b')
        for name in ('rootdata', 'rootpre', 'regpre', 'regtail'):
            key = ('obj\\th03\\' + name + '.obj').encode()
            need(rsp.count(key) == 1, 'one explicit source object replacement')
            rsp = rsp.replace(key, ('probe\\af554b\\' + name + '.obj').encode())
        need((b.SCRATCH / f'r{number}.lnk').read_bytes() == rsp and row['response_sha256'] == sha(rsp), 'literal original-order link response')
        for phase, unit in zip(phases[(number-1)*3:(number-1)*3+2], config['units']):
            need(phase['argv'] == b.assembler(dos, unit['module']) and phase['cwd'] == str(b.SCRATCH.relative_to(root)), 'direct pinned native assembler command')
            description = describe_omf(vector[unit['name']])
            dependencies = [unit['module']] + ([INCLUDE] if unit['name'] == 'registration' else [])
            need(description['valid'] and description['module_name'] == unit['module'] and
                 description['dependency_paths'] == dependencies, 'complete actual local source dependencies')
        phase = phases[number*3-1]
        need(phase['argv'] == dos + ['tlink', f'@probe\\af554b\\r{number}.lnk'] and
             phase['cwd'] == str(work.relative_to(root)), 'normal native linker command')
        before, old_rows = b.parent.map_partition(b.base.checked(old['outputs']['map']), 'regpre.asm')
        after, new_rows = b.parent.map_partition(vector['map'], 'regpre.asm')
        need(before == after and old_rows == row['original_MAP_rows'] == OLD_ROWS and
             new_rows == row['native_MAP_rows'] == NEW_ROWS and vector['exe'] == b.base.checked(old['outputs']['exe']),
             'whole original EXE and only one literal MAP DATA-extent change')
        vectors.append(vector)
    need(len(vectors) == 2 and vectors[0] == vectors[1], 'both complete raw two-OBJ/EXE/MAP vectors repeat')
    return vectors[0], record, digest


def verify(root, work, target, candidate, graph, files):
    import build_th03_mainl_text_banks_work as b
    vector, record, digest = selected(root, work, graph)
    mapping = vector['map'].decode()
    linked = parse_mz(vector['exe'])
    need(all(m.valid and m.raw == target.raw and len(m.raw) == 67372 and
             [(r.segment, r.offset) for r in m.relocations] == [(r.segment, r.offset) for r in target.relocations] and
             len(m.relocations) == 677 for m in (target, candidate, linked)), 'complete original EXE and literal global MZ vector')
    owners, banks = [], {}
    specs = [(PREFIX_UNIT, 'registration', 0x92E, 303, 35), (ENDING_UNIT, 'ending', 0xB3E, 360, 82)]
    for unit, name, offset, size, public_count in specs:
        source, obj = SOURCE_MAP[unit]
        raw, original = vector[name], (work / obj).read_bytes()
        records, old_records = parse_omf(raw), parse_omf(original)
        initialized = b.base.b.initialized_payload(raw)
        old_initialized = b.base.b.initialized_payload(original)
        need([(s['name'], s['class'], s['size']) for s in segment_definitions(raw)] ==
             [('_TEXT', 'CODE', 0), ('_DATA', 'DATA', size)] and
             [r.data[0] for r in records if r.name == 'SEGDEF'] == [0x48, 0x48] and
             [r.data for r in records if r.name == 'GRPDEF'] == [b'\x06\xff\x02'] and
             set(initialized) == {(2, i) for i in range(size)} and
             initialized == {k: v for k, v in old_initialized.items() if k[1] < size},
             'complete one-write native DATA, original word alignment and DGROUP')
        fields = literal_fields(raw)
        expected = [] if name == 'ending' else [dict(segment=2, site=site, location_type=1, width=2,
            segment_relative=True, frame_method=1, frame=1, target_method=0, target=2, addend=addend)
            for site, addend in [(72, 214), (74, 223)]]
        need(fields == literal_fields(original) == expected, 'all full literal ordered native near-pointer fields')
        pubs = code_publics(raw, 2)
        native_packets = [r.data for r in records if r.name == 'PUBDEF']
        old_packets = [r.data for r in old_records if r.name == 'PUBDEF']
        need(pubs == code_publics(original, 2) and len(pubs) == public_count and
             len(native_packets) == len(old_packets) == public_count and sorted(native_packets) == sorted(old_packets) and
             not code_publics(raw, 1) and all(address(mapping, symbol) == (0xE3F, offset+site) for site, symbol in pubs),
             'every original public alias, exact address and complete PUBLIC packet set')
        body = bytearray(initialized[2, i] for i in range(size))
        for field in fields:
            body[field['site']:field['site']+2] = (offset + field['addend']).to_bytes(2, 'little')
        start = 0xE3F * 16 + offset
        need(all(m.program_image[start:start+size] == body and not [r for r in m.relocations if start <= r.linear < start+size]
                 for m in (target, candidate, linked)), 'complete resolved DATA and empty ordered MZ scope')
        strings = []
        sites = sorted({site for site, _ in pubs if site >= (84 if name == 'registration' else 0)})
        for site, end in zip(sites, sites[1:]+[size]):
            text = bytes(body[site:end])
            need(text[-1:] == b'\0' and b'\0' not in text[:-1], 'one complete nul-terminated string per public extent')
            strings.append(dict(offset=site, bytes=end-site, text=text[:-1].decode('cp932'),
                symbols=[symbol for at, symbol in pubs if at == site]))
        need(len(strings) == (20 if name == 'registration' else 41), 'complete semantic string inventory')
        if name == 'registration':
            names = ['REIMU   ', 'MIMA    ', 'MARISA  ', 'ELEN    ', 'KOTOHIME', 'KANA    ', 'RIKAKO  ', 'CHIYURI ', 'YUMEMI  ']
            glyphs = bytes(14 if c == ' ' else ord(c)-ord('A')+(3 if c >= 'N' else 0) for text in names for c in text)
            need(body[:72] == glyphs and body[76:84] == bytes(8) and native_packets == old_packets and
                 strings[-1]['text'] == 'over.m' and len(old_initialized) == 304 and old_initialized[2, 303] == 0,
                 'nine eight-glyph sprite names, four initialized hold words, and excluded historical final zero')
            a = [(r.name, r.data) for r in records if r.name != 'COMENT']
            z = [(r.name, r.data) for r in old_records if r.name != 'COMENT']
            changes = [(i, x, y) for i, (x, y) in enumerate(zip(a, z)) if x != y]
            need(len(a) == len(z) and len(changes) == 2 and
                 [(x[0], y[0]) for _, x, y in changes] == [('SEGDEF', 'SEGDEF'), ('LEDATA', 'LEDATA')] and
                 changes[0][1][1] == b'\x48\x2f\x01\x04\x05\x01' and changes[0][2][1] == b'\x48\x30\x01\x04\x05\x01' and
                 changes[1][2][1] == changes[1][1][1] + b'\0', 'only exact original non-comment changes: size303 and omitted last zero')
        else:
            need([(r.name, r.data) for r in records if r.name not in ('COMENT', 'PUBDEF')] ==
                 [(r.name, r.data) for r in old_records if r.name not in ('COMENT', 'PUBDEF')] and
                 native_packets != old_packets, 'all other original non-comment records equal; PUBLIC order difference explicit')
        owner = dict(unit_id=unit, name='registration initialized state/text bank' if name == 'registration' else 'ending/verdict/staff text bank',
            source=source, object=obj, origin='authored', segment=0xE3F, offset=offset, start=start, size=size,
            coordinate_space='decoded-load', canonical_file_offset=None, target_sha256=sha(body), candidate_sha256=sha(body),
            ordered_relocations=[], code_bytes=0, initialized_data_bytes=size, procedure_count=0,
            private_data_bytes=0, private_bss_bytes=0, maintained_native_object=record['rounds'][0]['outputs'][name]['path'],
            abi='CP932 nul-terminated strings and exact native PUBLIC aliases; registration adds72 byte glyphs, two near pointers and four zero words')
        owners.append(owner)
        banks[name] = dict(initialized_bytes=size, strings=strings, ordered_native_fields=fields,
            PUBLIC_entries=public_count, PUBLIC_packets=public_count, original_PUBLIC_order_equal=native_packets == old_packets,
            original_PUBLIC_packet_set_equal=True, original_game_standalone_object_available=False)
    gap = 0xE3F * 16 + 0xA5D
    need('0E3F:0A5E 00E0 C=DATA   S=_DATA          G=DGROUP  M=staffdat.cpp ACBP=48' in mapping and
         address(mapping, '_mainl_ending_script') == (0xE3F, 0xA5E) and
         linked.program_image[gap:gap+1] == b'\0' and gap+1 == 0xE3F*16+0xA5E and
         not any(o['start'] <= gap < o['start']+o['size'] for o in owners), 'real following WORD-aligned contribution; one unowned native linker gap')
    return json.loads(json.dumps(dict(owners=owners, banks=banks, source_sha256=record['source_sha256'],
        selected_build_report_sha256=digest, source_CODE_bytes=0, source_initialized_DATA_bytes=663,
        linker_gap_start=gap, linker_gap_bytes=1, linker_gap_credited=False,
        encoding_transport='UTF-8 to CP932, LF to CRLF; reversible text only',
        entire_raw_EXE_equal=True, MAP_only_registration_extent_304_to_303=True,
        entire_raw_pair_repeated=True, fresh_outputs_per_round=4, source_cold_rebuilt=False,
        ancestor_runtime_replayed=False, physical_file_success_claimed=False, whole_product_accepted=False)))
