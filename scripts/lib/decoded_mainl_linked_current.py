"""Additional disjoint MAINL ownership from the complete current linked build."""
import csv
import re

from build_th03_mainl_linked_current import review, SOURCES
from build_th03_mainl_function_bodies import review as function_review, FUNCTIONS
from build_th03_mainl_sound_current import review as sound_review, SOUND
from build_th03_mainl_display_work import payload, literal_fields
from lib.decoded_mainl_xx_native import native_bodies
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from build_th03_mainl_resources_work import need, sha

STAGE = 'af1369m'
PREFIX = 'th03-mainl-decoded-'
# Complete original bank boundaries. Inline compiler tables retain DATA credit.
XX = {
    'crt-xx-front': (0x580D, 49, 49),
    'crt-xx-type-equal': (0x583E, 157, 157),
    'crt-xx-types': (0x58DB, 1121, 1121),
    'crt-xx-calls': (0x5D3C, 1495, 1327),
    'crt-xx-throw': (0x6313, 2524, 2446),
    'crt-xx-catch': (0x6CEF, 1476, 1434),
    'crt-xx-dispatch': (0x72B3, 1565, 1533),
    'crt-xx-destruction': (0x78D0, 2500, 2422),
    'crt-xx-rtti': (0x8294, 1735, 1599),
}
EXTRA = {
    'math-vector': ('obj/th03/vector_far.obj', 1, 0x110, 0x110, 69, True),
    'math-between': ('obj/th03/vector_far.obj', 1, 0x110, 0x156, 90, True),
    'linked-tail-producer-0155': ('obj/th03/vector_far.obj', 1, 0x110, 0x155, 1, False),
    'linked-tail-producer-02a7': ('obj/th03/cdg_put.obj', 3, 0x1F4, 0x2A7, 1, False),
    'linked-tail-producer-0371': ('obj/th03/cdg_put.obj', 3, 0x1F4, 0x371, 1, False),
    'linked-tail-producer-0fa3': ('obj/th03/cdg_p_na.obj', 1, 0xF32, 0xFA3, 1, False),
    'root-tail-grcg-setcolor-align': ('obj/th03/mainl.obj', 1, 0x272, 0xC5F, 1, False),
    'root-tail-grcg-off-align': ('obj/th03/mainl.obj', 1, 0x272, 0xC65, 1, False),
    'root-tail-root-zero-font': ('obj/th03/mainl.obj', 1, 0x272, 0xC71, 1, False),
    'root-tail-compare-align': ('obj/th03/mainl.obj', 1, 0x272, 0x2C2F, 1, False),
}
SOUND_TAILS = {'linked-tail-producer-0049': 'snd_mode', 'linked-tail-producer-0083': 'snd_pmdr',
               'linked-tail-producer-009f': 'snd_dlyv', 'linked-tail-producer-0669': 'snd_se_r'}
UNITS = {PREFIX + name for name in (*XX, *EXTRA, *FUNCTIONS, *SOUND_TAILS, 'crt-xx-data')}


def xx_procedures(raw, assembly, sources):
    # Reuse the reviewed original function boundaries, without regenerating
    # obsolete miniatures or replaying unrelated emulator models.
    from review_th03_mainl_xx_rtti import (
        FRONT_BODIES, TAIL_BODIES, TYPE_BODIES, THROW_BODIES, CATCH_BODIES,
        CALL_BODIES, DISPATCH_BODIES, DESTROY_BODIES,
    )
    original = [*FRONT_BODIES, ('sameTypeID', 0x583E, 157, 'far'), *TYPE_BODIES,
                *THROW_BODIES, *CATCH_BODIES, *DESTROY_BODIES, *TAIL_BODIES]
    original += [(n, o, size, 'near') for n, o, size, _ in CALL_BODIES]
    original += [(n, 0x72B3 + o, size, 'near' if kind == 'ret' else 'far')
                 for n, o, size, kind in DISPATCH_BODIES]
    original.sort(key=lambda b: b[1])
    definitions = [dict(name=n, offset=o, size=s, return_kind=k) for n, o, s, k in original]
    symbols = [dict(name=n.decode(), return_kind=k.decode()) for n, k in re.findall(
        rb'^\s*(\S+)\s+proc\s+(near|far)\s*$', assembly, re.M)]
    procedures = native_bodies(raw, assembly, sources, definitions, symbols)
    need([(r['start'] + 0x580D, r['size'], r['return_kind']) for r in procedures] ==
         [(o, s, k) for _, o, s, k in original], 'all 50 original xx source/LINNUM function extents')
    return procedures


def verify(root, stage=STAGE):
    proof = review(stage)
    work = root / proof['work']
    target = parse_mz((work / 'bin/th03/mainl.exe').read_bytes())
    table = (work / 'obj/th03/mainl.map').read_text()
    with (root / 'config/units.csv').open() as stream:
        units = {u['id']: u for u in csv.DictReader(stream)}
    raw = (work / 'xx/xx.obj').read_bytes()
    native_sources = {n: (work / 'xx' / n).read_bytes() for n in SOURCES if n.endswith('.inl')}
    procedures = xx_procedures(raw, (work / 'xx/xx.asm').read_bytes(), native_sources)
    owners = []

    def owner(name, obj, segment, offset, size, code, count):
        u = units[PREFIX + name]
        need((u['artifact'], u['segment'].lower(), int(u['offset'], 0), int(u['size'], 0)) ==
             ('th03-mainl', f'decoded:{segment:04x}', offset, size), 'complete original ledger extent')
        start = segment * 16 + offset
        body = target.program_image[start:start + size]
        pairs = [[r.segment, r.offset] for r in target.relocations if start <= r.linear < start + size]
        need(len(body) == size and not any(r.linear < start < r.linear + 2 or
             r.linear < start + size < r.linear + 2 for r in target.relocations), 'complete owned bytes and ordered fields')
        owners.append(dict(unit_id=u['id'], source=u['source'], object=obj, origin=u['origin'],
            segment=segment, offset=offset, start=start, size=size,
            coordinate_space='decoded-load', canonical_file_offset=None,
            target_sha256=sha(body), candidate_sha256=sha(body), ordered_relocations=pairs,
            code_bytes=code, initialized_data_bytes=size-code, procedure_count=count))

    need('0000:580D' in table and '0E3F:1172' in table, 'original complete xx CODE/DATA positions')
    need(sum(size for _, size, _ in XX.values()) == 12622 and
         sum(code for _, _, code in XX.values()) == 12088, 'complete disjoint xx banks and inline tables')
    for name, (offset, size, code) in XX.items():
        selected = [r for r in procedures if offset <= 0x580D+r['start'] < offset+size]
        expected = units[PREFIX+name]['source']
        need(selected and all(SOURCES[r['source']] == expected and
             0x580D+r['start']+r['size'] <= offset+size for r in selected),
             'entire bank bound to its maintained original source definitions')
        owner(name, 'xx/xx.obj', 0, offset, size, code, len(selected))
    data = bytes(payload(raw)[2, i] for i in range(18))
    need(target.program_image[0xE3F0+0x1172:0xE3F0+0x1184] == data,
         'all initialized xx DATA and separate unchanged ten-byte BSS')
    owner('crt-xx-data', 'xx/xx.obj', 0xE3F, 0x1172, 18, 0, 0)
    for name, (obj, native_segment, base, offset, size, function) in EXTRA.items():
        segment = 0 if obj.endswith('mainl.obj') else 0xC7E
        raw = (work / obj).read_bytes()
        description = describe_omf(raw)
        source = units[PREFIX+name]['source']
        need(source in [p.replace('\\', '/') for p in description['dependency_paths']] and
             (work / source).read_bytes().replace(b'\r\n', b'\n') ==
             (root / source).read_bytes().replace(b'\r\n', b'\n'), 'actual current ASM source consumption')
        body = target.program_image[segment*16+offset:segment*16+offset+size]
        if not function:
            image = payload(raw)
            need(body == bytes([image[native_segment, offset-base]]) and
                 body == (b'\0' if name.endswith('zero-font') else b'\x90') and
                 not any(f['segment'] == native_segment and
                         f['site'] < offset-base+1 and f['site']+f['width'] > offset-base
                         for f in literal_fields(raw)), 'actual emitted natural alignment/empty-string byte')
        owner(name, obj, segment, offset, size, size if function else 0, int(function))
    functions = function_review()
    need(functions['parent'] == proof, 'natural function scopes use this complete target-equal link')
    for name, (obj, offset, size) in FUNCTIONS.items():
        raw = (root / functions['work'] / obj).read_bytes()
        need(units[PREFIX+name]['source'] in
             [p.replace('\\', '/') for p in describe_omf(raw)['dependency_paths']],
             'function owner binds its actually consumed maintained source')
        owner(name, obj, 0xC7E, offset, size, size, 1)
    sound = sound_review()
    need(sound['parent'] == proof, 'natural sound providers compose with this current complete project')
    for name, stem in SOUND_TAILS.items():
        source, _, offset, size, _ = SOUND[stem]
        need(units[PREFIX+name]['source'] == f'src/mainl/sound/{source}.asm',
             'alignment ownership binds the actual complete maintained ASM producer')
        raw = (root / sound['work'] / (stem + '.obj')).read_bytes()
        need(payload(raw)[1, size] == target.program_image[0xC7E0+offset+size] == 0x90 and
             not any(f['site'] < size+1 and f['site']+f['width'] > size for f in literal_fields(raw)),
             'complete emitted EVEN byte without an instruction or relocation straddling ownership')
        owner(name, stem + '.obj', 0xC7E, offset+size, 1, 0, 0)
    return dict(build=proof, owners=owners, xx_procedures=procedures, natural_function_bodies=functions,
                natural_sound=sound,
                complete_current_combined_link=True, original_cold_rebuilt=False,
                whole_product_source_accepted=False)
