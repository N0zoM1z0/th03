"""Typed C near-pointer table, with explicit native/context OMF differences."""
import json

from build_th03_mainl_resources_work import need, sha
from build_th03_mainl_display_work import literal_fields, payload
from lib.omf import describe_omf, parse_omf
from lib.pc98 import parse_mz
from lib.op_shared_native import address
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

UNIT = 'th03-mainl-decoded-picture-file-pointers'
SOURCE = 'src/mainl/root/picture_files.c'
OBJECT = 'obj/th03/rootpre.obj'
SOURCE_MAP = {UNIT: (SOURCE, OBJECT)}
NAMES = [f'a{i:02}sl_cd2' for i in range(0, 18, 2)]
OLD_ROWS = [
    '0000:0272 0000 C=CODE   S=_TEXT          G=(none)  M=rootpre.asm ACBP=48',
    '0E3F:0090 0012 C=DATA   S=_DATA          G=DGROUP  M=rootpre.asm ACBP=48']
NEW_ROWS = [
    '0000:0271 0000 C=CODE   S=_TEXT          G=(none)  M=rootpre.c  ACBP=28',
    '0E3F:0090 0012 C=DATA   S=_DATA          G=DGROUP  M=rootpre.c  ACBP=48',
    '0E3F:133C 0000 C=BSS    S=_BSS           G=DGROUP  M=rootpre.c  ACBP=48']


def selected(root, work, graph):
    # Historical runtime builders import acceptance.proof_inputs at startup.
    import build_th03_mainl_picture_files_work as b
    config, config_hash = b.inputs()
    parent_config, parent_config_hash = b.parent.inputs()
    _, preservation = b.parent.parent_inputs(parent_config)
    parent, parent_hash = b.base.load(b.parent.REPORT)
    record, digest = b.base.load(b.REPORT)
    source = (root / SOURCE).read_bytes()
    producer, = [g for g in graph if g['output'] == OBJECT]
    need(parent['complete'] and parent_hash == config['parent_report_sha256'] and
         parent['config_sha256'] == parent_config_hash and
         parent['driver_sha256'] == sha((root / b.parent.DRIVER).read_bytes()) and
         parent['source_sha256'] == {n: sha((root / n).read_bytes()) for n in parent_config['inputs']},
         'unchanged actual source root parent')
    need(record['complete'] and record['source_acceptance'] is False and
         record['whole_product_accepted'] is False and record['canonical_credit_changed'] is False and
         record['cold_rebuilt'] is False and record['game_objects_recompiled'] == 1 and
         record['source_root_recompiled'] is False and record['source_root_reused'] is True and
         record['cold_game_objects_retained'] == 34 and record['library_rebuilt'] is False and
         record['packing_rebuilt'] is False and record['config_sha256'] == config_hash and
         record['driver_sha256'] == sha((root / b.DRIVER).read_bytes()) and
         record['source_sha256'] == sha(source) and record['parent_report_sha256'] == parent_hash and
         record['parent_preservation'] == preservation and record['cold_producer'] == producer and
         record['cold_report_sha256'] == sha((root / '.analysis/work/mainl-build.json').read_bytes()) and
         record['original_object_sha256'] == sha((work / OBJECT).read_bytes()), 'actual bounded native producer')
    for name, expected in [('rootpre.c', source), ('driver.py', (root / b.DRIVER).read_bytes()),
                           ('config.json', (root / b.CONFIG).read_bytes())]:
        need((b.SCRATCH / name).read_bytes() == expected, 'literal consumed source/recipe ' + name)
    phases = record['phases']
    need([p['label'] for p in phases] == [f'round{i}-{k}' for i in (1, 2) for k in ('compile', 'link')] and
         all(p['returncode'] == 0 and sha((root / p['log_path']).read_bytes()) == p['log_sha256'] for p in phases),
         'all four real compiler/linker writer logs')
    dos = ['/usr/bin/wine-stable', str(root / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    vectors = []
    for number, row in enumerate(record['rounds'], 1):
        need(row['round'] == number and set(row['outputs']) == {'obj', 'exe', 'map'}, 'complete raw output vector')
        vector = {k: b.base.checked(v) for k, v in row['outputs'].items()}
        old = parent['rounds'][number - 1]
        for key, old_key, filename in [('reused_startup', 'reused_startup', 'c0l.obj'),
                ('reused_library', 'reused_library', f'r{number}.lib'), ('reused_root', None, 'rootdata.obj')]:
            expected = old[old_key] if old_key else old['outputs']['obj']
            need(row[key] == expected and (b.SCRATCH / filename).read_bytes() == b.base.checked(expected),
                 'actual inherited source C0/library/root ' + filename)
        response = b.parent.runtime.link_response('mainl', work, number).replace(b'af548h', b'af553h')
        for module in ('rootdata', 'rootpre'):
            key = ('obj\\th03\\' + module + '.obj').encode()
            need(response.count(key) == 1, 'one explicit source object replacement')
            response = response.replace(key, ('probe\\af553h\\' + module + '.obj').encode())
        compile_phase, link_phase = phases[(number - 1) * 2:number * 2]
        need((b.SCRATCH / f'r{number}.lnk').read_bytes() == response and row['response_sha256'] == sha(response) and
             compile_phase['argv'] == b.compiler(dos) and compile_phase['cwd'] == str(b.SCRATCH.relative_to(root)) and
             link_phase['argv'] == dos + ['tlink', f'@probe\\af553h\\r{number}.lnk'] and
             link_phase['cwd'] == str(work.relative_to(root)), 'actual normal compiler/linker commands and response')
        before, old_rows = b.map_partition(b.base.checked(old['outputs']['map']), 'rootpre.asm')
        after, new_rows = b.map_partition(vector['map'], 'rootpre.c')
        need(before == after and old_rows == row['original_MAP_rows'] == OLD_ROWS and
             new_rows == row['native_MAP_rows'] == NEW_ROWS and
             vector['exe'] == b.base.checked(old['outputs']['exe']),
             'whole original EXE and every MAP byte outside three explicit contributor changes')
        description = describe_omf(vector['obj'])
        need(description['valid'] and description['module_name'] == 'rootpre.c' and
             description['dependency_paths'] == ['rootpre.c'], 'only actual literal C TU is consumed')
        vectors.append(vector)
    need(len(vectors) == 2 and vectors[0] == vectors[1], 'both complete raw OBJ/EXE/MAP vectors repeat')
    return vectors[0], record, digest


def verify(root, work, target, candidate, graph, files):
    vector, record, digest = selected(root, work, graph)
    raw = vector['obj']
    need([(s['name'], s['class'], s['size']) for s in segment_definitions(raw)] ==
         [('_TEXT', 'CODE', 0), ('_DATA', 'DATA', 18), ('_BSS', 'BSS', 0)] and
         code_publics(raw, 2) == [(0, '_PIC_FN')] and not code_publics(raw, 1) and not code_publics(raw, 3),
         'complete near-pointer DATA contribution; no CODE or reserved BSS credit')
    records = parse_omf(raw)
    need([r.data for r in records if r.name == 'EXTDEF'] ==
         [b''.join(bytes([len(n)]) + n.encode() + b'\0' for n in NAMES)] and
         [r.data for r in records if r.name == 'GRPDEF'] == [b'\x08\xff\x02\xff\x03'] and
         not any(r.name == 'LIDATA' for r in records) and
         payload(raw) == {(2, n): 0 for n in range(18)}, 'real symbolic near offsets, DGROUP and one-write initialized bytes')
    fields = literal_fields(raw)
    expected = [dict(segment=2, site=2*i, location_type=1, width=2, segment_relative=True,
                     frame_method=1, frame=1, target_method=2, target=i+1, addend=0) for i in range(8, -1, -1)]
    original_fields = literal_fields((work / OBJECT).read_bytes())
    old_expected = [dict(segment=2, site=2*i, location_type=1, width=2, segment_relative=True,
                         frame_method=5, frame=None, target_method=2, target=i+1, addend=0) for i in range(9)]
    need(fields == expected and original_fields == old_expected and fields != original_fields,
         'literal full native field stream; context ASM frame/order difference remains explicit')
    mapping = vector['map'].decode()
    need(address(mapping, '_PIC_FN') == (0xE3F, 0x90), 'original public near-table address')
    data, strings = bytearray(), []
    linked = parse_mz(vector['exe'])
    for i, name in enumerate(NAMES):
        segment, offset = address(mapping, name)
        text = f'{i*2:02}sl.cd2'.encode() + b'\0'
        need(segment == 0xE3F and linked.program_image[segment*16+offset:segment*16+offset+len(text)] == text,
             'existing independent filename string binding ' + name)
        data.extend(offset.to_bytes(2, 'little'))
        strings.append(dict(name=name, segment=segment, offset=offset, filename=text[:-1].decode()))
    start = 0xE3F * 16 + 0x90
    relocs = [(r.segment, r.offset) for r in target.relocations]
    for mz in (target, candidate, linked):
        need(mz.valid and mz.raw == target.raw and len(mz.raw) == 67372 and
             mz.program_image[start:start+18] == data and
             [(r.segment, r.offset) for r in mz.relocations] == relocs and len(relocs) == 677 and
             not [r for r in mz.relocations if start <= r.linear < start+18],
             'whole original EXE, literal global MZ order and empty near-table relocation scope')
    owner = dict(unit_id=UNIT, name='picture filename near-pointer table', source=SOURCE, object=OBJECT,
        origin='authored', segment=0xE3F, offset=0x90, start=start, size=18, coordinate_space='decoded-load',
        canonical_file_offset=None, target_sha256=sha(data), candidate_sha256=sha(data), ordered_relocations=[],
        code_bytes=0, initialized_data_bytes=18, procedure_count=0, private_data_bytes=0, private_bss_bytes=0,
        maintained_native_object=record['rounds'][0]['outputs']['obj']['path'],
        abi='nine two-byte near char pointers in DGROUP; existing assembler string symbols excluded')
    return json.loads(json.dumps(dict(owners=[owner], selected_build_report_sha256=digest,
        source_sha256=record['source_sha256'], source_CODE_bytes=0, source_initialized_DATA_bytes=18,
        ordered_native_fields=fields, contextual_ASM_fields=original_fields, contextual_OMF_identity=False,
        original_game_standalone_object_available=False, pointer_bindings=strings, DATA_MZ_relocations=[],
        entire_raw_EXE_equal=True, MAP_only_explicit_contributor_rows_differ=True,
        original_MAP_rows=OLD_ROWS, native_MAP_rows=NEW_ROWS, entire_raw_pair_repeated=True,
        fresh_outputs_per_round=3, source_cold_rebuilt=False, ancestor_runtime_replayed=False,
        physical_file_success_claimed=False, whole_product_accepted=False)))
