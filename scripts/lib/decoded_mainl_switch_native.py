"""Own generated switch data and prove the compiler's one-byte table alignment.

The -a1 control explains code generation; it is never accepted or linked into a
product. Acceptance compares the complete unmodified -a2 bytes and literal
ordered native/MZ fields, without masking or transforming any target byte.
"""
import argparse
import json
import re
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86 import X86_OP_IMM
from build_th03_mainl_display_work import payload, literal_fields
from build_th03_mainl_resources_work import need, sha
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics
from lib.omf import parse_omf
from lib.decoded_mainl_cutscene_layout import (
    verify as cutscene, native_image, SOURCE, OBJECT, START, CS,
)
from lib.decoded_mainl_root_orchestration_layout import verify as orchestration, native, ROOTDATA
from review_th03_mainl_cutscene import RANGES
from review_th03_mainl_root import analyze

CONFIG = 'config/mainl_work/switch_tables_after551.json'
REPORT = '.analysis/work/mainl-switch-tables-after551-review.json'


def checked(root, meta):
    raw = (root / meta['path']).read_bytes()
    need(sha(raw) == meta['sha256'], 'actual retained switch probe: ' + meta['path'])
    return raw


def compiler_control(root, work, graph, config):
    raw = checked(root, config['probe_report'])
    checked(root, config['probe_driver'])
    record = json.loads(raw)
    source = (root / SOURCE).read_bytes()
    original = (work / OBJECT).read_bytes()
    producer, = [g for g in graph if g['output'] == OBJECT]
    need(record['source'] == SOURCE and record['source_sha256'] == sha(source) and
         config['source_sha256'] == sha(source) and record['cold_object_sha256'] == sha(original) and
         record['producer'] == producer and source.count(b'#pragma option -a2') == 1,
         'complete unchanged original source and actual GAME3/L producer')
    need([p['variant'] for p in record['phases']] == ['a2', 'a1', 's2'], 'bounded actual compiler schedule')
    for name, meta in record['files'].items():
        blob = (root / name).read_bytes()
        need(meta == dict(bytes=len(blob), sha256=sha(blob)), 'whole retained source/native control artifact')
    prefix = config['probe_work']
    for phase in record['phases']:
        variant = phase['variant']
        directory = work / prefix / variant
        expected_source = source if variant != 'a1' else source.replace(b'#pragma option -a2', b'#pragma option -a1')
        need((directory / 'source.inl').read_bytes() == expected_source and
             (directory / 'cutscene.cpp').read_text() == f'#include "{prefix}/{variant}/source.inl"\n',
             'literal source clone; only one alignment pragma changes in control')
        flags = [f for f in producer['flags'] if f not in ('-c', '-nobj/th03/')]
        windows = (prefix + '/' + variant).replace('/', '\\')
        expected = ['/usr/bin/wine-stable', str(root / '_reference/ReC98/bin/msdos.exe'), '-e', '-x', 'tcc',
                    '-S' if variant == 's2' else '-c', *flags, '-n' + windows + '\\', windows + '\\cutscene.cpp']
        need(phase['argv'] == expected and phase['returncode'] == 0 and
             sha((root / phase['log_path']).read_bytes()) == phase['log_sha256'], 'actual successful native compiler command/log')
    a = (work / prefix / 'a2/cutscene.obj').read_bytes()
    z = (work / prefix / 'a1/cutscene.obj').read_bytes()
    need(payload(a) == payload(original) and literal_fields(a) == literal_fields(original) and
         segment_definitions(a) == segment_definitions(original) and
         code_publics(a, 1) == code_publics(original, 1), 'complete unmodified baseline bytes/ordered fields/public layout')
    # All literal metadata except TU/dependency/debug comments agrees too.
    structural = lambda raw: [(r.name, r.data) for r in parse_omf(raw) if r.name not in ('THEADR', 'COMENT')]
    need(structural(a) == structural(original), 'entire baseline non-comment OMF stream equals actual cold producer')
    pa, pz = payload(a), payload(z)
    gap = 2807
    need(set(pa) == {(1, i) for i in range(3195)} and set(pz) == {(1, i) for i in range(3194)} and
         pa[1, gap] == 0 and segment_definitions(z) ==
         [dict(s, size=3194 if s['index'] == 1 else s['size']) for s in segment_definitions(a)],
         'one-byte compiler size difference; no private DATA/BSS or hidden initialized regions')
    expected_fields = []
    for field in literal_fields(a):
        changed = dict(field)
        if changed['site'] > gap:
            changed['site'] -= 1
        if changed['target_method'] == 0 and changed['target'] == 1 and changed['addend'] > gap:
            changed['addend'] -= 1
        expected_fields.append(changed)
    need(expected_fields == literal_fields(z) and len(expected_fields) == 236 and
         code_publics(z, 1) == [(o - int(o > gap), n) for o, n in code_publics(a, 1)],
         'all control fields/publics follow exactly the one-byte layout change')
    ca, cz = bytes(pa[1, i] for i in range(3195)), bytes(pz[1, i] for i in range(3194))
    field_sites = {site for f in literal_fields(a) for site in range(f['site'], f['site'] + f['width'])}
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    calls = []
    for _, address, size, _ in RANGES:
        begin = address - START
        shifted = begin - int(begin > gap)
        ai = list(decoder.disasm(ca[begin:begin + size], begin))
        zi = list(decoder.disasm(cz[shifted:shifted + size], shifted))
        need(len(ai) == len(zi) and sum(i.size for i in ai) == sum(i.size for i in zi) == size,
             'complete equal instruction partitions in alignment control')
        for before, after in zip(ai, zi):
            need(before.mnemonic == after.mnemonic and before.size == after.size,
                 'control preserves all instruction kinds and widths')
            if before.bytes == after.bytes:
                continue
            if before.mnemonic == 'call':
                need(before.operands[0].type == after.operands[0].type == X86_OP_IMM and
                     after.operands[0].imm == before.operands[0].imm - int(before.operands[0].imm > gap),
                     'shifted near CALL retains actual function target')
                calls.append(dict(original_site=before.address, control_site=after.address,
                                  original_target=before.operands[0].imm, control_target=after.operands[0].imm))
            else:
                need(all(before.address + n in field_sites for n, (x, y) in
                         enumerate(zip(before.bytes, after.bytes)) if x != y), 'only verified native field operands change')
    need(len(calls) == 5 and ca[2808:2880] == cz[2807:2879],
         'same entire 72-byte table bank; five real shifted near calls; zero absent only under -a1')
    assembly = (work / prefix / 's2/cutscene.asm').read_text(errors='strict')
    need(re.search(r'@SCRIPT_OP\$QUC\s+endp\s+@\S+\s+label\s+word\s+dw\s+@', assembly) and
         assembly.count('\tdw\t@12@') == 20, 'unmodified compiler assembly identifies symbolic switch destinations')
    return dict(probe_report_sha256=sha(raw), baseline_CODE_bytes=3195, control_CODE_bytes=3194,
        baseline_full_noncomment_OMF_equal=True, literal_ordered_fields=236,
        original_pragma='-a2', control_pragma='-a1', compiler_emitted_zero_offset=gap,
        compiler_alignment_bytes=1, control_near_calls=calls, control_accepted=False,
        compiler_assembly_used_as_product=False, native_rebuilt_by_review=False)


def verify(root, work, target, candidate, graph, files):
    config = json.loads((root / CONFIG).read_bytes())
    need(config['schema'] == 'th03-mainl-switch-tables-after551-v1' and
         config['source'] == SOURCE and config['whole_product_accepted'] is False and
         config['canonical_credit_changed'] is False, 'bounded generated-table publication')
    need([(s['unit_id'], s['source'], s['object'], s['segment'], s['offset'], s['size'],
           s['inline_table_bytes'], s['compiler_alignment_bytes']) for s in config['scopes']] == [
        ('th03-mainl-decoded-cutscene-switch-tables', SOURCE, OBJECT, CS, 0x1635, 73, 72, 1),
        ('th03-mainl-decoded-stage-intro-switch-table', 'src/mainl/root/complete_data.cpp',
         'obj/th03/rootdata.obj', CS, 0x6AF, 18, 18, 0)], 'exact disjoint original table allocations')
    control = compiler_control(root, work, graph, config)
    cut = cutscene(work, target, candidate, graph, files)
    orchestration(work, target, candidate, graph, files)
    cut_image, cut_fields = native_image((work / OBJECT).read_bytes())
    root_image, root_fields = native((work / 'obj/th03/rootdata.obj').read_bytes(), ROOTDATA, 3, 0xA2, 0x133C)
    root_analysis = analyze(target.program_image)
    need(root_analysis['table']['offset'] == 0x6AF and
         root_analysis['table']['words'] == [0x5A7, 0x5A7, 0x5AF, 0x5B7, 0x5AF, 0x5B7, 0x5A7, 0x5BF, 0x5C7],
         'all nine original enemy-selection destinations, including aliases')
    need(cut['boundaries']['tables']['opcode_keys'] == list(b'$=@bcefgkmnpstvw'),
         'all sixteen generated script opcode keys in literal native order')
    owners = []
    selected_fields = []
    for spec, image, fields, base in ((config['scopes'][0], cut_image, cut_fields, START),
                                    (config['scopes'][1], root_image[1], root_fields, 3)):
        begin, size = spec['offset'] - base, spec['size']
        body = image[begin:begin + size]
        need(len(body) == size, 'entire original table extent exists')
        selected = [f for f in fields if f.get('segment_index', 1) == 1 and begin <= f['offset'] < begin + size]
        need(len(selected) == (20 if base == START else 9) and
             all(f['fixdat'] == 0x14 and f['frame'] == f['target'] == 1 and f['width'] == 2 for f in selected),
             'all literal own-CODE destination fields; keys/alignment have no relocation')
        start = spec['segment'] * 16 + spec['offset']
        for mz in (target, candidate):
            need(mz.program_image[start:start + size] == body and
                 not [r for r in mz.relocations if start <= r.linear < start + size], 'whole raw table/alignment extent; literal empty MZ vector')
        owners.append(dict(**spec, name=spec['unit_id'].removeprefix('th03-mainl-decoded-'),
            origin='authored', start=start, coordinate_space='decoded-load', canonical_file_offset=None,
            target_sha256=sha(body), candidate_sha256=sha(body), ordered_relocations=[],
            code_bytes=0, initialized_data_bytes=size, code_segment_initialized_data_bytes=size,
            procedure_count=0, instruction_count=0, private_data_bytes=0, private_bss_bytes=0,
            abi='compiler-generated near WORD switch destinations/keys in original CODE group; no callable entry'))
        selected_fields.append(selected)
    return dict(owners=owners, procedures=0, instructions=0, source_CODE_bytes=0,
        code_segment_initialized_DATA_bytes=91, inline_table_bytes=90, compiler_alignment_bytes=1,
        literal_ordered_native_table_fields=selected_fields, scoped_MZ_relocations=[],
        compiler_alignment=control, cutscene_whole_producer_bytes=3195,
        cutscene_entire_instruction_and_table_partition_complete=True,
        original_cold_rebuilt=False, ancestor_runtime_replayed=False, whole_product_accepted=False)


if __name__ == '__main__':
    from review_th03_mainl_sound_work import images
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold', action='store_true', required=True)
    parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    work, target, candidate, cold, cold_raw, graph, files = images(root)
    scope = verify(root, work, target, candidate, graph, files)
    report = dict(schema='th03-mainl-switch-tables-after551-review-v1', complete=True,
        config_sha256=sha((root / CONFIG).read_bytes()), verifier_sha256=sha(Path(__file__).read_bytes()),
        cold_report_sha256=sha(cold_raw), scope=scope, provenance='candidate-local-attested')
    (root / REPORT).write_text(json.dumps(report, indent=2) + '\n')
    print('MAINL switches: 90 inline table bytes +1 compiler alignment; all29 table fields ordered-equal; '
          'complete cutscene3195 partition; unchanged cold pair reused')
