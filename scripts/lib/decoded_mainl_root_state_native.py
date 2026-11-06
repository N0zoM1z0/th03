"""Complete natural root TU, 28 initialized far pointers and true reserved BSS."""
import json
from pathlib import Path

from build_th03_mainl_resources_work import need, sha
from lib.omf import describe_omf, parse_omf
from lib.pc98 import parse_mz
from lib.decoded_mainl_root_orchestration_layout import native, ROOTDATA
from lib.op_shared_native import address
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

UNIT = 'th03-mainl-decoded-root-initialized-pointers'
SOURCE = 'src/mainl/root/recovered/complete.cpp'
OBJECT = 'obj/th03/rootdata.obj'
SOURCE_MAP = {UNIT: (SOURCE, OBJECT)}


def selected(root, work, graph, files):
    # The preserved runtime builders import acceptance's proof_inputs. Load
    # them only after that module has finished defining its public API.
    import build_th03_mainl_root_state_work as b
    config, config_hash = b.inputs()
    parent, preservation = b.parent_inputs(config)
    record, digest = b.base.load(b.REPORT)
    original = (work / OBJECT).read_bytes()
    producer, = [g for g in graph if g['output'] == OBJECT]
    sources = {n: (root / n).read_bytes() for n in config['inputs']}
    need(record['complete'] and record['whole_product_accepted'] is False and
         record['source_acceptance'] is False and record['canonical_credit_changed'] is False and
         record['cold_rebuilt'] is False and record['game_objects_recompiled'] == 1 and
         record['retained_project_objects'] == 35 and record['library_rebuilt'] is False and
         record['packing_rebuilt'] is False and record['config_sha256'] == config_hash and
         record['driver_sha256'] == sha((root / b.DRIVER).read_bytes()) and
         record['source_sha256'] == {n: sha(raw) for n, raw in sources.items()} and
         record['cold_report_sha256'] == sha((root / '.analysis/work/mainl-build.json').read_bytes()) and
         record['original_object_sha256'] == sha(original) and record['cold_producer'] == producer and
         record['parent_report_sha256'] == preservation['parent_report_sha256'] and
         record['parent_review'] == preservation, 'actual source-only root stage and unchanged preserved parent')
    for name, raw in sources.items():
        need((b.SCRATCH / name).read_bytes() == raw, 'actual consumed root input ' + name)
    need((b.SCRATCH / 'rootdata.cpp').read_bytes() == sources[SOURCE] and
         (b.SCRATCH / 'driver.py').read_bytes() == (root / b.DRIVER).read_bytes() and
         (b.SCRATCH / 'config.json').read_bytes() == (root / b.CONFIG).read_bytes(), 'literal TU transport and actual recipe snapshots')
    phases = record['phases']
    need([p['label'] for p in phases] == [f'round{i}-{kind}' for i in (1, 2) for kind in ('compile', 'link')] and
         all(p['returncode'] == 0 and sha((root / p['log_path']).read_bytes()) == p['log_sha256'] for p in phases),
         'all four real compiler/linker writer logs')
    dos = ['/usr/bin/wine-stable', str(root / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    cold = json.loads((root / '.analysis/work/mainl-build.json').read_bytes())
    vectors = []
    for number, row in enumerate(record['rounds'], 1):
        need(row['round'] == number and set(row['outputs']) == {'obj', 'exe', 'map'}, 'whole selected raw output vector')
        vector = {k: b.base.checked(v) for k, v in row['outputs'].items()}
        old = parent['rounds'][number - 1]['outputs']
        need(row['reused_startup'] == old['startup'] and row['reused_library'] == old['lib'] and
             (b.SCRATCH / 'c0l.obj').read_bytes() == b.base.checked(old['startup']) and
             (b.SCRATCH / f'r{number}.lib').read_bytes() == b.base.checked(old['lib']), 'actual source C0 and unchanged library pair')
        response = b.runtime.link_response('mainl', work, number).replace(b'af548h', b'af552h')
        key = rb'obj\th03\rootdata.obj'
        need(response.count(key) == 1, 'one selected root object replacement')
        response = response.replace(key, rb'probe\af552h\rootdata.obj')
        need((b.SCRATCH / f'r{number}.lnk').read_bytes() == response and row['response_sha256'] == sha(response) and
             phases[(number - 1) * 2]['argv'] == b.compiler(dos) and
             phases[(number - 1) * 2]['cwd'] == str(b.SCRATCH.relative_to(root)) and
             phases[(number - 1) * 2 + 1]['argv'] == dos + ['tlink', f'@probe\\af552h\\r{number}.lnk'] and
             phases[(number - 1) * 2 + 1]['cwd'] == str(work.relative_to(root)), 'normal compiler/linker commands and explicit original context')
        need(b.program(vector['obj']) == b.program(original) and
             [r.data for r in parse_omf(vector['obj']) if r.name == 'THEADR'] ==
             [r.data for r in parse_omf(original) if r.name == 'THEADR'] and
             vector['exe'] == b.base.checked(old['mainl_exe']) and vector['map'] == b.base.checked(old['mainl_map']),
             'all original non-comment OMF records, entire target EXE and current MAP')
        description = describe_omf(vector['obj'])
        need(description['valid'] and description['module_name'] == 'rootdata.cpp', 'complete original module identity')
        b.cold.verify_vendor_dependencies(description, cold['vendor_header_sha256'])
        for dependency in description['dependency_paths']:
            name = dependency.replace('\\', '/')
            while '//' in name:
                name = name.replace('//', '/')
            if name.startswith('C:/TC4/INCLUDE/'):
                continue  # Actual vendor inputs were bound above and by the current full cold audit.
            if name == 'rootdata.cpp':
                continue
            if name in sources:
                need((b.SCRATCH / name).read_bytes() == sources[name], 'consumed recovered include')
            else:
                path = (b.SCRATCH / name).resolve()
                relative = str(path.relative_to(work))
                need(relative in files and path.read_bytes() == files[relative], 'actual unchanged staged header ' + relative)
        vectors.append(vector)
    need(len(vectors) == 2 and vectors[0] == vectors[1], 'both whole raw OBJ/EXE/MAP vectors repeat')
    return vectors[0], record, digest


def verify(root, work, target, candidate, graph, files):
    vector, record, digest = selected(root, work, graph, files)
    raw = vector['obj']
    need([(s['name'], s['class'], s['size']) for s in segment_definitions(raw)] ==
         [('ROOTPRE_TEXT', 'CODE', 2458), ('_DATA', 'DATA', 112), ('_BSS', 'BSS', 186)], 'complete original segment partition')
    images, fields = native(raw, ROOTDATA, 3, 0xA2, 0x133C)
    data_fields = [f for f in fields if f['segment_index'] == 2]
    need(len(fields) == 278 and len(data_fields) == 28 and
         [f['offset'] for f in data_fields] == list(range(108, -1, -4)) and
         all((f['locat'], f['fixdat'], f['frame'], f['addend'], f['width']) ==
             (0xCC, 0x16, 2, 0, 4) for f in data_fields), 'all full ordered far-pointer fields; no invented addends')
    names = (['_mainl_script_' + str(i) for i in range(9)] + ['_mainl_story_template'] +
             [f'_mainl_{kind}_{i}' for i in range(9) for kind in ('title', 'name')])
    need([f['name'] for f in reversed(data_fields)] == names and
         code_publics(raw, 2) == [(0, '_WIN_MESSAGE_FN'), (36, '_mainl_story_script'), (40, '_mainl_char_info')],
         'actual nine-file table, mutable story pointer and eighteen title/name pointers')
    mapping = vector['map'].decode()
    for f in data_fields:
        name, segment, offset, _ = ROOTDATA['bindings'][f['target'] - 1]
        need(name == f['name'] and address(mapping, name) == (segment, offset) and segment == 0xE3F and
             images[2][f['offset']:f['offset'] + 4] == offset.to_bytes(2, 'little') + segment.to_bytes(2, 'little'),
             'each independently resolved original far-pointer value')
    linked = parse_mz(vector['exe'])
    start, size = 0xE3F * 16 + 0xA2, 112
    relocations = [(0xE3F, 0xA2 + f['offset'] + 2) for f in data_fields]
    for mz in (target, candidate, linked):
        need(mz.valid and mz.program_image[start:start + size] == images[2] and
             [(r.segment, r.offset) for r in mz.relocations if start <= r.linear < start + size] == relocations,
             'complete original/native DATA bytes and literal ordered DATA MZ vector')
    writes = []
    for rec in parse_omf(raw):
        need(rec.name != 'LIDATA', 'ordinary complete compiler LEDATA')
        if rec.name == 'LEDATA':
            seg, offset = rec.data[0], int.from_bytes(rec.data[1:3], 'little')
            writes.extend((seg, offset + i) for i in range(len(rec.data) - 3))
    need(len(writes) == len(set(writes)) == 2570 and
         set(writes) == {(1, i) for i in range(2458)} | {(2, i) for i in range(112)}, 'every initialized byte written once; no BSS initializer')
    bss = [(0, '_win_text', 183), (183, '_playchar', 2), (185, '_do_not_show_stage_number', 1)]
    need(code_publics(raw, 3) == [(off, name) for off, name, _ in bss] and
         all(address(mapping, name) == (0xE3F, 0x133C + off) for off, name, _ in bss), 'exact typed BSS symbols and sizes')
    bss_start = 0xE3F * 16 + 0x133C
    minimum_allocation = ((len(linked.program_image) + 15) // 16 + int.from_bytes(vector['exe'][10:12], 'little')) * 16
    need(len(target.program_image) == len(linked.program_image) == bss_start and
         bss_start + 186 <= minimum_allocation, 'BSS begins beyond the file-backed image and fits the real MZ reservation')
    consumers = [f for f in fields if f['segment_index'] == 1 and f['fixdat'] == 0x14 and f['target'] in (2, 3)]
    need({f['target'] for f in consumers} == {2, 3} and
         all(0 <= f['addend'] < (112 if f['target'] == 2 else 186) for f in consumers), 'actual fixed DATA/BSS reference bases')
    owner = dict(unit_id=UNIT, name='root initialized far-pointer bank', source=SOURCE, object=OBJECT,
        origin='authored', segment=0xE3F, offset=0xA2, start=start, size=112, coordinate_space='decoded-load',
        canonical_file_offset=None, target_sha256=sha(images[2]), candidate_sha256=sha(images[2]),
        ordered_relocations=[list(r) for r in relocations], code_bytes=0, initialized_data_bytes=112,
        procedure_count=0, private_data_bytes=0, private_bss_bytes=0, associated_reserved_BSS_bytes=186,
        maintained_native_object=record['rounds'][0]['outputs']['obj']['path'],
        abi='28 four-byte large-model far pointers in original DGROUP; mutable story pointer; external strings excluded')
    result = dict(owners=[owner], selected_build_report_sha256=digest,
        source_sha256=record['source_sha256'], source_CODE_bytes=0, source_initialized_DATA_bytes=112,
        original_root_CODE_bytes=2458, original_reserved_BSS_bytes=186, BSS_file_byte_credit=0,
        BSS_begin=bss_start, BSS_end=bss_start + 186, BSS_symbols=bss,
        all_original_noncomment_OMF_records_equal=True, ordered_native_fields=fields,
        pointer_fields=data_fields, native_DATA_BSS_consumers=consumers, DATA_MZ_relocations=[list(r) for r in relocations],
        entire_raw_EXE_MAP_equal=True, entire_raw_pair_repeated=True, fresh_outputs_per_round=3,
        source_cold_rebuilt=False, ancestor_runtime_replayed=False, physical_device_or_file_success_claimed=False,
        whole_product_accepted=False)
    return json.loads(json.dumps(result))
