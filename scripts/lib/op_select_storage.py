"""Natural selection prefix, complete initialized DATA and native BSS layout."""
import hashlib
import json
import re
import struct
import tomllib

from build_th03_op_selection_work import STATE, WRAPPER, OBJECT, DRIVER, REPORT, wrapper, native_records
from lib.omf import describe_omf, parse_omf
from lib.op_asset_native import extent
from lib.op_select_native import resolved_code, TAIL
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

UNIT = 'th03-op-decoded-select-data'
CS, DS, BASE, DATA, BSS = 0x990, 0xD7F, 0x1A8D, 0xA0E, 0x2462
SOURCE = 'src/op/menu/character_selection.inl'
BSS_DECLARATIONS = (
    ('curve_cycle', 0, 1, 1), ('resident', 2, 4, 2), ('sel', 6, 2, 1),
    ('sel_confirmed', 8, 2, 1), ('page_shown', 10, 1, 1), ('input_mode', 12, 4, 2),
    ('fadeout_frame_third', 16, 2, 2), ('curve_unused', 18, 2, 2),
    ('curve_trail_count', 20, 2, 2), ('playchars_available', 22, 1, 1),
)
BSS_REFERENCES = [0, 2, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22]


def need(value, message):
    if not value:
        raise ValueError('OP Select storage: ' + str(message))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def initializer(source, name):
    matches = re.findall(r'\b' + name + r'(?:\[[^\]]*\])+\s*=\s*\{(.*?)\};', source, re.S)
    need(len(matches) == 1, 'single complete natural initializer: ' + name)
    return matches[0]


def semantic_data(files, state):
    """Evaluate actual declarations/macros, including C aggregate zero members."""
    source, functions = state.decode(), files[SOURCE].decode()
    header = files['th03/shiftjis/fns.hpp'].decode('cp932')
    macro, = re.findall(r'#define PLAYCHAR_PIC_FN_DEF \{(.*?)\n\}', header, re.S)
    names = re.findall(r'"([^"\\]*)"', macro)
    need(len(names) == 9 and 'PLAYCHAR_PIC_FN[PLAYCHAR_COUNT] = PLAYCHAR_PIC_FN_DEF;' in source,
         'all nine source filename pointer initializers')
    stats = initializer(source, 'PLAYCHAR_STATS')
    rows = re.findall(r'\{\s*(\d+),\s*(\d+),\s*(\d+)\s*\}', stats)
    need(len(rows) == 9, 'all nine three-BYTE stats rows')
    data = bytearray(9 * 4)
    data.extend(int(v) for row in rows for v in row)
    gaiji = files['th03/gaiji/gaiji.h'].decode()
    codes = {name: int(value, 0) for name, value in re.findall(r'(gc_P\d_(?:TOP|BOTTOM)_\d)\s*=\s*(0x[\da-fA-F]+)', gaiji)}
    need(re.search(r'#define\s+gc_GAIJI_W\s+2\b', gaiji), 'actual two-glyph cursor width')
    for name in ('g_CURSOR_TOP', 'g_CURSOR_BOTTOM'):
        pairs = re.findall(r'\{\s*(gc_\w+),\s*(gc_\w+)\s*\}', initializer(source, name))
        need(len(pairs) == 2, 'both two-glyph cursor rows')
        for a, b in pairs:
            data.extend((codes[a], codes[b], 0))  # Third C aggregate member is implicitly zero.
    need(re.search(r'input_locked\[PLAYER_COUNT\]\s*=\s*\{\s*false,\s*false\s*\};', source), 'two explicitly false BYTE flags')
    data.extend((0, 0))
    need(len(data) == 77, 'all initialized arrays/flags precede the pool at77')
    functions = re.sub(r'//[^\n]*|/\*.*?\*/', '', functions, flags=re.S)
    extra = list(dict.fromkeys(re.findall(r'"([^"\\]*)"', functions)))
    need(len(extra) == 7, 'complete seven additional first-use filename literals')
    pointers, literals = [], []
    for index, text in enumerate(names + extra):
        at = len(data)
        raw = text.encode() + b'\0'
        data.extend(raw)
        literals.append(dict(text=text, offset=at, size=len(raw)))
        if index < 9:
            struct.pack_into('<HH', data, index * 4, at, 0)
            pointers.append(at)
    # This vendor header has mixed legacy comment encodings; macro tokens are
    # ASCII. A one-byte decoding preserves every byte while reading those tokens.
    gfx = files['libs/master.lib/pc98_gfx.hpp'].decode('latin1')
    colors = {n: int(v, 0) for n, v in re.findall(r'^#define\s+(TX_\w+)\s+(0x[\da-fA-F]+)\s*$', gfx, re.M)}
    used = re.findall(r'\bTX_\w+\b', initializer(functions, 'TRAM_COLORS_UNUSED'))
    need(len(data) == 224 and len(used) == 3, 'native final three-BYTE unused text-color declaration')
    data.extend(colors[n] for n in used)
    need(len(data) == 227, 'complete semantic DATA without fabricated fill')
    return bytes(data), pointers, literals


def verify(root, work, target, candidate, files):
    state = (root / STATE).read_bytes()
    need(not re.search(rb'\bpadding_\d\b|codestring|__emit__', state) and
         state.count(b'#pragma option -a2') == state.count(b'#pragma option -a-') == 1 and
         state.index(b'#pragma option -a2') < state.index(b'static unsigned char curve_cycle;') <
         state.index(b'static unsigned char playchars_available;') < state.index(b'#pragma option -a-'),
         'natural WORD state alignment restored to BYTE before all function definitions')
    report_raw = (root / REPORT).read_bytes()
    report = json.loads(report_raw)
    need(report['complete'] and not report['source_acceptance'] and not report['whole_product_cold_rebuilt'] and
         report['context_objects'] == 29 and report['driver_sha256'] == sha((root / DRIVER).read_bytes()) and
         report['cold_report_sha256'] == sha((root / '.analysis/work/op-build.json').read_bytes()) and
         report['source_sha256'] == {STATE: sha(state), SOURCE: sha((root / SOURCE).read_bytes())},
         'complete current maintained selected-source/driver/cold-context binding')
    generated = wrapper()
    need(report['wrapper_sha256'] == sha(generated) and
         (root / '.analysis/work/selection-tail.cpp').read_bytes() == generated,
         'actual maintained prefix and bounded function-slice includes')
    response = files['obj/th03/op.@l']
    for old, new in ((b'obj\\th03\\seltail.obj', b'probe\\selstate.obj'),
                     (b'bin\\th03\\op.exe', b'probe\\selstate.exe'),
                     (b'obj\\th03\\op.map', b'probe\\selstate.map')):
        need(response.count(old) == 1, 'one selected native producer substituted at unchanged link position')
        response = response.replace(old, new)
    need(report['response_sha256'] == sha(response) and
         (root / '.analysis/work/selection-tail.lnk').read_bytes() == response, 'complete actual link response')
    config = tomllib.loads((root / 'config/toolchain.toml').read_text())
    dos = ['/usr/bin/wine-stable', str(root / config['paths']['msdos_player']), '-e', '-x']
    commands = [dos + ['tcc', '-c', '-I.', '-O', '-b-', '-3', '-Z', '-d', '-DGAME=3', '-ml',
                "-DBINARY='O'", '-oprobe/selstate.obj', WRAPPER], dos + ['tlink', r'@probe\selstate.lnk']]
    need([(p['label'], p['command'], p['returncode']) for p in report['native_phases']] ==
         [(f'round{n}-{name}', commands[i], 0) for n in (1, 2) for i, name in enumerate(('compile', 'link'))],
         'two actual selected native compile/link rounds')
    need(len(report['rounds']) == 2 and [r['round'] for r in report['rounds']] == [1, 2], 'both independent selected outputs')
    rounds = []
    for row in report['rounds']:
        need(set(row['outputs']) == {'obj', 'exe', 'map'}, 'complete selected output vector')
        outputs = {}
        for kind, meta in row['outputs'].items():
            raw = (root / meta['path']).read_bytes()
            need(meta['sha256'] == sha(raw) and meta['bytes'] == len(raw), 'every current selected raw output')
            outputs[kind] = raw
        need(outputs['exe'] == (work / 'bin/th03/op.target.exe').read_bytes() and
             outputs['map'] == (work / 'obj/th03/op.map').read_bytes(), 'whole independently linked target and complete original native MAP')
        rounds.append(outputs)
    need(rounds[0] == rounds[1], 'complete raw OBJ/EXE/MAP selected repeat equality')
    raw, baseline = rounds[0]['obj'], (work / OBJECT).read_bytes()
    native = describe_omf(raw)
    need(native['valid'] and native['module_name'] == WRAPPER and native['translator_comments'] == ['TC86 Borland C++ 4.02'] and
         native_records(raw) == native_records(baseline), 'all native records including dense CODE/DATA,segments,groups,publics,external and fixup order')
    deps = native['dependency_paths']
    need(deps[:2] == [WRAPPER, STATE] and deps == [WRAPPER, STATE] + describe_omf(baseline)['dependency_paths'][1:] and
         all(n in (WRAPPER, STATE) or n in files and (work / n).read_bytes() == files[n] for n in deps),
         'complete actual maintained native dependency closure')
    need(code_publics(raw, 1) == [(off, name) for off, name, *_ in TAIL] and
         code_publics(raw, 2) == [] and code_publics(raw, 3) == [(2, '_resident'), (12, '_input_mode')],
         'all seventeen complete functions and initialized/BSS publics')
    table = (work / 'obj/th03/op.map').read_text()
    code, fields, code_relocs = resolved_code(raw, BASE, DATA, BSS, table)
    extent((target, candidate), code, CS, BASE, code_relocs)
    semantic, pointers, literals = semantic_data(files, state)
    data, blocks = code_bytes(raw, 2)
    need(data == semantic and [(b['offset'], b['size']) for b in blocks] == [(0, 227)], 'complete source-derived native DATA')
    image, data_fields, block = bytearray(data), [], None
    for record in parse_omf(raw):
        if record.name == 'LEDATA':
            block = record.data[0]
            need(block != 3, 'BSS contains no file-backed initializer')
        elif record.name == 'FIXUPP' and block == 2:
            at = 0
            while at < len(record.data):
                loc, site, method, frame, index = record.data[at:at + 5]
                at += 5
                need(loc == 0xCC and method == 20 and frame == index == 2 and site % 4 == 0 and site < 36,
                     'ordinary own-DATA far-pointer field')
                addend = int.from_bytes(data[site:site + 4], 'little')
                data_fields.append([site, loc, method, frame, index, addend])
                struct.pack_into('<HH', image, site, DATA + addend, DS)
    need(data_fields == [[i * 4, 0xCC, 20, 2, 2, pointers[i]] for i in range(8, -1, -1)],
         'all nine literal ordered far filename pointer fields')
    relocs = [[DS, DATA + f[0] + 2] for f in data_fields]
    extent((target, candidate), image, DS, DATA, relocs)
    need(sorted({f['addend'] for f in fields if f['method'] == 20 and f['target'] == 3}) == BSS_REFERENCES,
         'complete native CODE BSS field addends')
    offset, gaps = 0, []
    for name, at, size, alignment in BSS_DECLARATIONS:
        aligned = (offset + alignment - 1) // alignment * alignment
        need(aligned == at, 'natural16-bit declaration alignment: ' + name)
        gaps.extend(range(offset, aligned))
        offset = aligned + size
    need(offset == 23 and gaps == [1, 11], 'entire natural BSS with two implicit compiler holes')
    for start, size, cls, name in ((DATA, 227, 'DATA', '_DATA'), (BSS, 23, 'BSS', '_BSS')):
        need(len(re.findall(rf'(?m)^\s*{DS:04X}:{start:04X}\s+{size:04X}\s+C={cls}\s+S={name}\s+G=DGROUP\s+M=th03/seltail\.cpp\s+ACBP=48\s*$', table)) == 1,
             'whole native storage MAP allocation')
    digest = sha(image)
    owner = dict(unit_id=UNIT, name='Character selection initialized DATA', source=STATE, object=OBJECT,
        segment=DS, offset=DATA, start=DS * 16 + DATA, size=227, coordinate_space='decoded-load', canonical_file_offset=None,
        target_sha256=digest, candidate_sha256=digest, ordered_relocations=relocs, procedure_count=0, procedures=[],
        code_bytes=0, initialized_data_bytes=227, private_data_bytes=227, private_bss_bytes=0,
        forwarding_chain=[WRAPPER, STATE], supporting_source=SOURCE,
        maintained_native_object=report['rounds'][0]['outputs']['obj']['path'],
        abi='nine far filename pointers;27 stats BYTEs;two2x3 cursor arrays;two BYTE flags;literal pool;three text colors')
    return dict(owners=[owner], initialized_data_bytes=227, procedures=0, native_DATA_fields=data_fields,
        ordered_relocations=relocs, literals=literals, native_CODE_bytes=2858, native_CODE_fields=len(fields),
        native_CODE_relocations=code_relocs, bss_bytes=23, BSS_raw_byte_credit=0, BSS_alignment_gaps=gaps,
        BSS_declarations=[dict(name=n, offset=o, size=s, alignment=a) for n, o, s, a in BSS_DECLARATIONS],
        native_CODE_BSS_addends=BSS_REFERENCES, consumed_paths=deps, selected_build_report_sha256=sha(report_raw),
        context_objects_reused=29, selected_compile_link_rounds=2, source_only_cold_rebuild_claimed=False,
        legacy_dummy_padding_accepted=False, following_alignment_accepted=False, runtime_matrix_required=False,
        whole_product_accepted=False)


if __name__ == '__main__':
    from pathlib import Path
    import build_th03_op_work as build
    from review_th03_op_cfg_work import images
    from lib.op_startup_cold import verify as cold_graph
    root = Path(__file__).resolve().parents[2]
    work, target, candidate, cold, _ = images(root)
    cold_graph(root, work, target, candidate, cold)
    print(json.dumps(verify(root, work, target, candidate, build.source_graph()), indent=2))
