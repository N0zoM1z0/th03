"""Four complete OP helper bodies; legacy sound trailers remain unowned."""
import hashlib
import json
import re
import tomllib

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.omf import describe_omf, parse_omf
from lib.op_asset_native import extent
from lib.op_shared_native import address
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

CS, DS = 0xBEB, 0xD7F
TRAILER = b'#pragma codestring "\\x90"\n'
# unit, source, wrapper, intermediate include, object, MAP name, OMF public,
# native base, function bytes, excluded trailer bytes, CODE alignment
LEAVES = (
    ('th03-op-decoded-configuration-snd_mode', 'src/op/snd/determine_mode.c',
     'th02/snd_mode.c', 'th02/snd/detmode.c', 'obj/th02/snd_mode.obj',
     '_snd_determine_mode', '_snd_determine_mode', 0x4A, 29, 1, 0x48),
    ('th03-op-decoded-snd-pmd-resident', 'src/op/snd/pmd_resident.c',
     'th02/snd_pmdr.c', 'th02/snd/pmd_res.c', 'obj/th02/snd_pmdr.obj',
     '_snd_pmd_resident', '_snd_pmd_resident', 0x68, 57, 1, 0x28),
    ('th03-op-decoded-polar', 'src/op/math/polar.cpp',
     'th03/polar.cpp', 'th03/math/polar.cpp', 'obj/th03/polar.obj',
     'polar(int,int,int)', '@polar$qiii', 0x155, 26, 0, 0x28),
    ('th03-op-decoded-hflip-lut', 'src/shared/formats/hfliplut.asm',
     'th03/hfliplut.asm', None, 'obj/th03/hfliplut.obj',
     '_hflip_lut_generate', '_hflip_lut_generate', 0xCB8, 30, 0, 0x48),
)
UNITS = {r[0] for r in LEAVES}
FORWARDING = {r[4]: (r[2], r[3], r[1]) for r in LEAVES if r[3]}
EXTERNALS = (
    ('_snd_active', '_snd_midi_active', '_snd_fm_possible'),
    ('_snd_interrupt_if_midi', '_snd_midi_possible', '_snd_midi_active', '_snd_fm_possible'),
    (), ('_hflip_lut',),
)
FIELDS = (((24, 1), (20, 2), (13, 3)), ((17, 2), (12, 4), (7, 3), (2, 1)), (), ((4, 1),))
PROBE = '.analysis/work/sound-bodies.json'
DRIVER = 'scripts/probe_th03_op_sound_bodies.py'


def need(value, message):
    if not value:
        raise ValueError('OP leaf native: ' + str(message))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def resolve(raw, index, count, table):
    row = LEAVES[index]
    asm = index == 3
    description = describe_omf(raw)
    records = parse_omf(raw)
    need(description['valid'] and description['translator_comments'] ==
         (['Turbo Assembler  Version 5.0'] if asm else ['TC86 Borland C++ 4.02']), 'complete native producer integrity')
    geometry = [(1, 'SHARED', 'CODE', count)] + ([] if asm else [(2, '_DATA', 'DATA', 0), (3, '_BSS', 'BSS', 0)])
    need(segment_definitions(raw) == [dict(index=i, name=n, **{'class': c}, overlay='', size=s)
         for i, n, c, s in geometry] and
         [r.data[0] for r in records if r.name == 'SEGDEF'] == [row[-1]] + ([] if asm else [0x48, 0x48]) and
         [r.data for r in records if r.name == 'GRPDEF'] == ([] if asm else [bytes((8, 255, 2, 255, 3))]),
         'whole native segment alignment, group and storage geometry')
    need(code_publics(raw, 1) == [(0, row[6])] and
         (asm or not code_publics(raw, 2) and not code_publics(raw, 3)), 'sole complete helper public')
    code, blocks = code_bytes(raw, 1)
    need([(b['offset'], b['size']) for b in blocks] == [(0, count)] and
         [r.data[0] for r in records if r.name == 'LEDATA'] == [1], 'complete dense native CODE')
    names = EXTERNALS[index]
    need([r.data for r in records if r.name == 'EXTDEF'] ==
         ([b''.join(bytes((len(n),)) + n.encode() + b'\0' for n in names)] if names else []),
         'complete ordered native external inventory')
    method = 0x56 if asm else 0x16
    expected = b''.join(bytes((0xC4, site, method)) + (b'' if asm else b'\1') + bytes((ext,))
                        for site, ext in FIELDS[index])
    need([r.data for r in records if r.name == 'FIXUPP'] == ([expected] if expected else []),
         'complete literal ordered native field stream')
    image, fields = bytearray(code[:row[8]]), []
    for site, ext in FIELDS[index]:
        need(site + 2 <= len(image) and code[site:site + 2] == b'\0\0', 'whole zero-addend offset WORD field')
        seg, off = address(table, names[ext - 1])
        need(seg == DS, 'actual OP DGROUP storage address')
        image[site:site + 2] = off.to_bytes(2, 'little')
        fields.append(dict(site=site, locat=0xC4, method=method, frame=None if asm else 1,
                           target=ext, name=names[ext - 1], addend=0, width=2))
    return bytes(image), fields, description


def verify(root, work, target, candidate, files):
    table = (work / 'obj/th03/op.map').read_text()
    proof_raw = (root / PROBE).read_bytes()
    proof = json.loads(proof_raw)
    config = tomllib.loads((root / 'config/toolchain.toml').read_text())
    need(proof['complete'] and proof['driver_sha256'] == sha((root / DRIVER).read_bytes()) and
         proof['cold_report_sha256'] == sha((root / '.analysis/work/op-build.json').read_bytes()) and
         len(proof['objects']) == 2 and proof['rounds'] == 2 and
         proof['source_acceptance'] is False and not proof['whole_product_rebuilt'],
         'source-bound scoped compiler diagnostic')
    owners, objects = [], []
    for index, row in enumerate(LEAVES):
        unit, source, wrapper, middle, obj, mapname, public, base, size, tail, alignment = row
        raw = (work / obj).read_bytes()
        image, fields, description = resolve(raw, index, size + tail, table)
        need(description['module_name'].replace(chr(92), '/') == wrapper, 'actual helper producer identity')
        chain = [wrapper, middle, source] if middle else [wrapper, source]
        need(files[source] == (root / source).read_bytes(), 'maintained helper source')
        for parent, child in zip(chain, chain[1:]):
            include = '#include "' + child + '"\n' if middle else 'include ' + child + '\r\n'
            need(files[parent] == include.encode(), 'literal maintained helper include chain')
        deps = [n.replace(chr(92), '/') for n in description['dependency_paths']]
        need(all(n in files and (work / n).read_bytes() == files[n] for n in deps) and all(n in deps for n in chain),
             'complete actual source/header dependency closure')
        need(address(table, mapname) == (CS, base), 'actual helper MAP public')
        for seg, off, count, cls, name, group, attr in (
            [(CS, base, size + tail, 'CODE', 'SHARED', '(none)', alignment)] +
            ([] if middle is None else [(DS, 0x5F2, 0, 'DATA', '_DATA', 'DGROUP', 0x48),
                                       (DS, 0x1F70, 0, 'BSS', '_BSS', 'DGROUP', 0x48)])):
            module = re.escape(wrapper.replace('/', '\\') if middle is None else wrapper)
            need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+{count:04X}\s+C={cls}\s+S={name}\s+G={re.escape(group)}\s+M={module}\s+ACBP={attr:02X}\s*$', table)) == 1,
                 'whole containing native MAP contribution')
        natural = None
        if tail:
            source_raw = files[source]
            need(source_raw.endswith(TRAILER) and source_raw.count(TRAILER) == 1, 'sole excluded legacy codestring')
            p = proof['objects'][index]
            need(p['source'] == source and p['source_sha256'] == sha(source_raw) and
                 p['current_object_sha256'] == sha(raw) and
                 p['stripped_source_sha256'] == sha(source_raw[:-len(TRAILER)]) and
                 (root / p['stripped_source']).read_bytes() == source_raw[:-len(TRAILER)], 'actual pragma-free native input')
            bodies = []
            for compiled in p['outputs']:
                need(compiled['command'] == ['/usr/bin/wine-stable', str(root / config['paths']['msdos_player']),
                     '-e', '-x', 'tcc', '-c', '-I.', '-O', '-b-', '-3', '-Z', '-d', '-DGAME=2', '-ml',
                     "-DBINARY='O'", '-nprobe/', p['native_source']], 'actual native C/GAME2/O compiler command')
                probe_raw = (root / compiled['path']).read_bytes()
                body, probe_fields, desc = resolve(probe_raw, index, size, table)
                need(compiled['returncode'] == 0 and compiled['sha256'] == sha(probe_raw) and body == image and
                     probe_fields == fields, 'complete repeated natural body and native field equality')
                probe_deps = desc['dependency_paths']
                need(probe_deps == [p['native_source']] + description['dependency_paths'][3:],
                     'actual stripped input consumes identical complete header closure')
                bodies.append(probe_raw)
            need(len(bodies) == 2 and bodies[0] == bodies[1], 'two complete raw-equal pragma-free native objects')
            natural = dict(outputs=p['outputs'], CODE_bytes=size, source_without_codestring_sha256=p['stripped_source_sha256'])
        extent((target, candidate), image, CS, base, [])
        decoder = Cs(CS_ARCH_X86, CS_MODE_16)
        decoder.detail = True
        ins = list(decoder.disasm(image, base))
        need(sum(i.size for i in ins) == size and (ins[-1].mnemonic, ins[-1].op_str) == ('retf', ''),
             'complete far helper with caller cleanup')
        bounds = {i.address for i in ins}
        for i in ins:
            if i.mnemonic.startswith(('j', 'loop')):
                need(len(i.operands) == 1 and i.operands[0].type == X86_OP_IMM and i.operands[0].imm in bounds,
                     'all helper branches enter complete owned instructions')
        digest = sha(image)
        owners.append(dict(unit_id=unit, name=mapname, source=source, object=obj, segment=CS, offset=base,
            start=CS * 16 + base, size=size, coordinate_space='decoded-load', canonical_file_offset=None,
            target_sha256=digest, candidate_sha256=digest, ordered_relocations=[], procedure_count=1,
            procedures=[dict(name=mapname, offset=0, size=size, callee_pop_bytes=0, instruction_count=len(ins))],
            code_bytes=size, initialized_data_bytes=0, private_data_bytes=0, private_bss_bytes=0,
            forwarding_chain=chain, abi='far C; polar has three signed16 stack arguments; original register traffic'))
        objects.append(dict(object=obj, native_fields=fields, consumed_paths=deps,
            complete_containing_CODE_bytes=size + tail, owned_CODE_bytes=size, natural_body=natural))
    return dict(owners=owners, code_bytes=142, procedures=4, native_objects=objects,
        sound_probe_sha256=sha(proof_raw), excluded_tail_extents=[[CS, 0x67, 1], [CS, 0xA1, 1]],
        legacy_codestrings_accepted=False, external_storage_accepted=False, runtime_matrix_required=False,
        whole_product_accepted=False)


if __name__ == '__main__':
    from pathlib import Path
    import build_th03_op_work as build
    from review_th03_op_cfg_work import images
    from lib.op_startup_cold import verify as cold_graph
    root = Path(__file__).resolve().parents[2]
    work, target, candidate, cold, cold_raw = images(root)
    cold_graph(root, work, target, candidate, cold)
    print(json.dumps(dict(cold_report_sha256=sha(cold_raw),
                         scope=verify(root, work, target, candidate, build.source_graph())), indent=2))
