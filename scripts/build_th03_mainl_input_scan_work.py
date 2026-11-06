#!/usr/bin/env python3
"""Recover the complete input function; leave its adjacent byte unowned."""
import fcntl
import json
import os
import subprocess
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_16, CS_GRP_JUMP
from capstone.x86 import X86_INS_LOOP, X86_OP_IMM
import build_th03_runtime_after548_work as runtime
import review_th03_runtime_after548_work as prior_review
from review_th03_mainl_sound_work import images
from build_th03_mainl_resources_work import need, sha

ROOT = runtime.ROOT
base = runtime.base
DRIVER = 'scripts/build_th03_mainl_input_scan_work.py'
CONFIG = 'config/mainl_work/input_scan_candidate.json'
PREFIX = '.analysis/work/mainl-input-scan-'
REPORT = PREFIX + 'build.json'
SCRATCH = base.b.WORK / 'probe/af549h'


def inputs():
    config, digest = base.load(CONFIG)
    _, attestation = runtime.parent.inputs()
    need(config['schema'] == 'th03-mainl-input-scan-candidate-v1' and
         config['source'] == 'src/mainl/hardware/input_scan.asm' and
         config['cold_object'] == 'obj/th03/input_s.obj' and
         config['symbol'] == '@input_reset_sense_key_held$qv' and
         config['decoded_start'] == 0xCB68 and config['instruction_bytes'] == 417 and
         config['literal_fields'] == 42 and config['unowned_following_byte'] == 0x90 and
         config['whole_product_acceptance'] is False and config['source_acceptance_publication_changed'] is False and
         config['compatible_profile'] == 'config/th03_zun_driver_jwasm.toml' and
         config['compatible_flags'] == ['-nologo', '-Cp', '-omf'], 'bounded complete input function candidate')
    return config, dict(config_sha256=digest, compatible_attestation=attestation)


def load_image(raw):
    header = int.from_bytes(raw[8:10], 'little') * 16
    need(raw[:2] == b'MZ' and header < len(raw), 'complete native MZ image')
    return raw[header:]


def scope(cold_object, native_object, target, candidate, config):
    a, z = base.b.segment_definitions(cold_object), base.b.segment_definitions(native_object)
    expected = [dict(s, size=417 if s['index'] == 1 else s['size']) for s in a]
    need(z == expected and len(z) == 3 and z[0]['name'] == 'SHARED' and
         all(s['size'] == 0 for s in z[1:]), 'original segment geometry; no private DATA/BSS or adjacent byte')
    records = lambda raw, kind: [r for r in base.b.parse_omf(raw) if r.name == kind]
    need([r.data[0] for r in records(cold_object, 'SEGDEF')] ==
         [r.data[0] for r in records(native_object, 'SEGDEF')], 'original segment alignment/combination/width flags')
    for kind in ('GRPDEF', 'ALIAS', 'MODEND'):
        need([r.data for r in records(cold_object, kind)] == [r.data for r in records(native_object, kind)], 'original ' + kind)
    old, new = base.b.initialized_payload(cold_object), base.b.initialized_payload(native_object)
    need(old.get((1, 417)) == 0x90 and new == {(1, i): old[1, i] for i in range(417)} and
         len(new) == 417, 'all original instruction bytes; trailing context byte remains absent')
    need(base.b.externs(cold_object) == base.b.externs(native_object) ==
         ['_js_stat', '_input_mp_p1', '_input_mp_p2', '_input_sp'], 'ordered original word-state imports')
    af, zf = base.b.literal_fields(cold_object), base.b.literal_fields(native_object)
    need(af == zf and len(af) == 42, 'all complete literal fields retained in native producer order')
    ap, zp = runtime.parent.ordered_publics(cold_object), runtime.parent.ordered_publics(native_object)
    need(ap == zp and len(zp) == 1 and zp[0]['name'] == config['symbol'] and zp[0]['offset'] == 0,
         'one original far API and complete PUBLIC attributes')
    sites = []
    for record in base.b.parse_omf(native_object):
        need(record.name != 'LIDATA', 'instruction-only candidate emits LEDATA')
        if record.name == 'LEDATA':
            segment, pos = runtime.parent.omf_index(record.data)
            offset = int.from_bytes(record.data[pos:pos + 2], 'little')
            sites.extend((segment, i) for i in range(offset, offset + len(record.data) - pos - 2))
    need(len(sites) == len(set(sites)) == 417 and set(sites) == set(new), 'each instruction byte written once')
    start, size = config['decoded_start'], config['instruction_bytes']
    ta, ca = load_image(target), load_image(candidate)
    body = ta[start:start + size]
    need(body == ca[start:start + size] and ta[start + size] == config['unowned_following_byte'],
         'complete actual target instruction extent at unchanged native address')
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    instructions = list(decoder.disasm(body, 0))
    need(sum(i.size for i in instructions) == 417 and instructions[-1].address == 416 and
         instructions[-1].mnemonic == 'retf', 'entire instruction extent ends at real RETF')
    boundaries = {i.address for i in instructions}
    branches = []
    for ins in instructions:
        if ins.group(CS_GRP_JUMP) or ins.id == X86_INS_LOOP:
            need(len(ins.operands) == 1 and ins.operands[0].type == X86_OP_IMM and
                 ins.operands[0].imm in boundaries, 'every direct edge closes inside complete function')
            branches.append(dict(site=ins.address, target=ins.operands[0].imm, mnemonic=ins.mnemonic))
    differences = [i for i in range(max(len(target), len(candidate)))
                   if target[i:i + 1] != candidate[i:i + 1]]
    need(differences and target != candidate, 'whole product remains explicitly unaccepted')
    return dict(instruction_scope_exact=True, whole_product_exact=False, public_entries=zp,
        original_fields=af, native_fields=zf, instruction_bytes=417, instruction_count=len(instructions),
        branches=branches, body_sha256=sha(body), every_instruction_byte_written_once=True,
        trailing_context=dict(decoded_start=start + size, bytes=1, target_byte=0x90, owned=False),
        candidate_image_bytes=len(candidate), original_image_bytes=len(target),
        full_EXE_difference_count=len(differences), full_EXE_difference_offsets=differences)


def response(number):
    raw = runtime.link_response('mainl', base.b.WORK, number).replace(b'af548h', b'af549h')
    key = b'obj\\th03\\input_s.obj'
    need(raw.count(key) == 1, 'one actual input object binding')
    return raw.replace(key, b'probe\\af549h\\input_s.obj')


def main():
    config, attestation = inputs()
    previous = prior_review.review()
    parent, parent_hash = base.load(runtime.REPORT)
    _, _, _, cold, cold_raw, graph, _ = images(ROOT)
    producers = [g for g in graph if g.get('output') == config['cold_object']]
    need(len(producers) == 1 and producers[0]['source'] == 'src/mainl/linked_game/input_sense.cpp',
         'actual cold input producer and maintained original statements')
    source = (ROOT / config['source']).read_bytes()
    original = (base.b.WORK / config['cold_object']).read_bytes()
    record = dict(complete=False, whole_product_accepted=False, canonical_unit_credit_changed=False,
        source_acceptance_publication_changed=False, cold_rebuilt=False, game_objects_recompiled=0,
        driver_sha256=sha((ROOT / DRIVER).read_bytes()), source_sha256=sha(source),
        config_sha256=attestation['config_sha256'], attestation=attestation, previous=previous,
        parent_build_sha256=parent_hash, cold_report_sha256=sha(cold_raw), cold_object_sha256=sha(original),
        cold_producer=producers[0],
        phases=[], rounds=[])
    save = lambda: (ROOT / REPORT).write_text(json.dumps(record, indent=2) + '\n')
    prefix = ROOT / '.analysis/toolchain/wineprefix'
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', WINEPREFIX=str(prefix),
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    jwasm = str(ROOT / attestation['compatible_attestation']['native_tools']['jwasm']['path'])
    dos = ['/usr/bin/wine-stable', str(ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']

    def run(argv, cwd, label):
        p = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        path = PREFIX + label + '.log'
        (ROOT / path).write_bytes(p.stdout)
        record['phases'].append(dict(label=label, argv=argv, returncode=p.returncode,
                                     log_path=path, log_sha256=sha(p.stdout)))
        save()
        need(p.returncode == 0, label + ': ' + p.stdout.decode(errors='replace')[-1200:])

    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        need(not SCRATCH.exists(), 'fresh retained candidate directory')
        SCRATCH.mkdir()
        for path, raw in [('input_s.asm', source), ('config.json', (ROOT / CONFIG).read_bytes()),
                          ('driver.py', (ROOT / DRIVER).read_bytes())]:
            (SCRATCH / path).write_bytes(raw)
        os.utime(SCRATCH / 'input_s.asm', (946684800, 946684800))
        vectors = []
        for number in (1, 2):
            parent_outputs = parent['rounds'][number - 1]['outputs']
            (SCRATCH / 'c0l.obj').write_bytes(base.checked(parent_outputs['startup']))
            (SCRATCH / f'r{number}.lib').write_bytes(base.checked(parent_outputs['lib']))
            run([jwasm, *config['compatible_flags'], '-Foinput_s.obj', 'input_s.asm'], SCRATCH, f'round{number}-assemble')
            rsp = response(number)
            (SCRATCH / f'r{number}.lnk').write_bytes(rsp)
            run(dos + ['tlink', f'@probe\\af549h\\r{number}.lnk'], base.b.WORK, f'round{number}-link')
            vector = dict(obj=(SCRATCH / 'input_s.obj').read_bytes(), exe=(SCRATCH / f'r{number}.exe').read_bytes(),
                          map=(SCRATCH / f'r{number}.map').read_bytes())
            target = base.checked(parent_outputs['mainl_exe'])
            result = scope(original, vector['obj'], target, vector['exe'], config)
            outputs = {}
            for kind, raw in vector.items():
                path = PREFIX + f'round{number}-' + kind + '.bin'
                (ROOT / path).write_bytes(raw)
                outputs[kind] = dict(path=path, bytes=len(raw), sha256=sha(raw))
            record['rounds'].append(dict(round=number, outputs=outputs, scope=result,
                response_sha256=sha(rsp), reused_startup=parent_outputs['startup'], reused_library=parent_outputs['lib']))
            save()
            vectors.append(vector)
            print('Input scan round', number, 'complete 417-byte function / 42 ordered fields exact; whole product unaccepted', flush=True)
        need(vectors[0] == vectors[1] and source == (ROOT / config['source']).read_bytes(), 'actual raw pair and source repeat')
    record['complete'] = True
    save()


if __name__ == '__main__':
    main()
