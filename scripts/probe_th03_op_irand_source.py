#!/usr/bin/env python3
"""Two native TASM/TLINK rounds for OP's maintained 42-byte IRAND include.

Reuses unchanged current OP link inputs; never performs a whole cold build.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tomllib

from build_th03_mainl_display_work import literal_fields, payload
from lib.mainl_owner_migrations import public_offsets
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from build_th03_op_work import ROOT, WORK, source_graph


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_obj(original, actual, source_dep):
    for name, parser in (('initialized bytes', payload),
                         ('ordered fixups', literal_fields),
                         ('PUBLICs', public_offsets),
                         ('segments', segment_definitions)):
        need(parser(original) == parser(actual), 'OP assembler owner differs: '+name)
    meta = describe_omf(actual)
    need(meta['valid'] and source_dep in meta['dependency_paths'],
         'actual TASM object lacks maintained IRAND include dependency')
    return dict(initialized_bytes=len(payload(actual)),
                ordered_fixups=len(literal_fields(actual)),
                publics=len(public_offsets(actual)),
                segments=len(segment_definitions(actual)))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage', required=True)
    args = ap.parse_args()
    need(re.fullmatch(r'af[0-9]+[a-z][0-9]*', args.stage), 'DOS-safe stage ID')
    files = source_graph()
    source = 'src/op/libs/random.asm'
    need((ROOT/source).is_file() and not (ROOT/source).is_symlink(),
         'maintained IRAND source')
    maintained = (ROOT/source).read_bytes()
    anchor = b'include libs/master.lib/random.asm'
    original_link_source = files['th03_op.asm']
    need(original_link_source.count(anchor) == 1, 'one physical OP IRAND include')
    # Keep the old complete cold OP source graph unchanged. Replace just the
    # IRAND include in this isolated source/native probe, so the previous
    # accepted scopes retain their exact published input bindings.
    need(original_link_source == (WORK/'th03_op.asm').read_bytes(),
         'current OP assembler parent changed')
    link_source = original_link_source.replace(anchor, b'include '+source.encode())
    original_obj = (WORK/'obj/th03/op.obj').read_bytes()
    original_exe = (WORK/'bin/th03/op.exe').read_bytes()
    original_map = (WORK/'obj/th03/op.map').read_bytes()
    target = (WORK/'bin/th03/op.target.exe').read_bytes()
    config = tomllib.loads((ROOT/'config/th03_diet.toml').read_text())
    expected_sha = next(x['decoded_sha256'] for x in config['artifacts'] if x['id']=='th03-op')
    need(sha(target)==expected_sha, 'decoded OP target identity')
    orig_image, target_image = parse_mz(original_exe), parse_mz(target)
    irand_start, irand_size = 0x1d12, 42
    need(orig_image.program_image[irand_start:irand_start+irand_size] ==
         target_image.program_image[irand_start:irand_start+irand_size],
         'unchanged native IRAND target bytes')
    work_stage = WORK/'probe'/args.stage
    log_stage = ROOT/'.analysis/work'/('op-irand-source-'+args.stage)
    need(not work_stage.exists() and not log_stage.exists(), 'fresh scoped stage')

    prefix = ROOT/'.analysis/toolchain/wineprefix'
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
               WINEPREFIX=str(prefix), MSDOS_PATH=r'C:\TC4\BIN')
    cpu = str(min(os.sched_getaffinity(0)))
    native = ['taskset', '-c', cpu, 'nice', '-n', '10', '/usr/bin/wine-stable']
    asm_tool = str(prefix/'drive_c/TASM50/bin/TASM32.EXE')
    dos = str(ROOT/'_reference/ReC98/bin/msdos.exe')
    output = {'stage': args.stage, 'source': source, 'source_sha256': sha(maintained),
              'target_decoded_sha256': sha(target), 'rounds': [],
              'native_OP_IRAND_raw_exact': False,
              'whole_current_OP_link_equal': False,
              'whole_original_OP_decoded_image_equal': False}

    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        work_stage.mkdir(parents=True)
        log_stage.mkdir(parents=True)

        def run(argv, label):
            result = subprocess.run(native+argv, cwd=WORK, env=env,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, timeout=120)
            (log_stage/(label+'.log')).write_bytes(result.stdout)
            need(result.returncode==0, label+' failed; inspect native log')

        for n in (1, 2):
            rel = 'probe/'+args.stage+'/r'+str(n)
            rd = WORK/rel
            (rd/'src/op/libs').mkdir(parents=True)
            maintained_dep = rel+'/'+source
            (rd/source).write_bytes(maintained.replace(b'\n', b'\r\n'))
            body = link_source.replace(b'include '+source.encode(),
                                       b'include '+maintained_dep.encode())
            (rd/'th03_op.asm').write_bytes(body)
            run([asm_tool, '/m', '/mx', '/kh32768', '/t', '/dGAME=3',
                 rel.replace('/', '\\')+'\\th03_op.asm',
                 rel.replace('/', '\\')+'\\op.obj'], f'r{n}-TASM')
            asm_obj = (rd/'op.obj').read_bytes()
            counts = check_obj(original_obj, asm_obj, maintained_dep)
            parent_response = (WORK/'obj/th03/op.@l').read_bytes()
            old = b'obj\\th03\\op.obj'
            need(parent_response.count(old)==1, 'single physical OP assembler link slot')
            response = parent_response.replace(old, (rel+'/op.obj').replace('/', '\\').encode())
            response = response.replace(b'bin\\th03\\op.exe',
                                        (rel+'/op.exe').replace('/', '\\').encode())
            response = response.replace(b'obj\\th03\\op.map',
                                        (rel+'/op.map').replace('/', '\\').encode())
            (rd/'op.@l').write_bytes(response)
            run([dos, '-e', '-x', 'tlink', '@'+(rel+'/op.@l').replace('/', '\\')],
                f'r{n}-TLINK')
            linked = (rd/'op.exe').read_bytes()
            need(linked==original_exe, 'whole normal OP image differs')
            candidate = parse_mz(linked)
            need(candidate.relocations==orig_image.relocations,
                 'literal ordered OP relocations differ')
            linked_map = (rd/'op.map').read_bytes()
            old_name = ('M='+rel.replace('/', '\\')+'\\th03_op.asm').encode()
            need(linked_map.count(old_name)==3, 'three physical OP assembler MAP rows')
            need(linked_map.replace(old_name, b'M=th03_op.asm')==original_map,
                 'complete native OP MAP geometry differs')
            need((rd/source).read_bytes()==maintained.replace(b'\n', b'\r\n'),
                 'staged maintained source changed')
            output['rounds'].append(dict(number=n, object=counts,
                                         object_sha256=sha(asm_obj),
                                         image_sha256=sha(linked),
                                         map_sha256=sha(linked_map)))
            print('round',n,'native OP IRAND42, full assembler object and normal OP link equal',flush=True)
        need((ROOT/source).read_bytes()==maintained, 'live native source changed')
    output['native_OP_IRAND_raw_exact'] = True
    output['whole_current_OP_link_equal'] = True
    output['whole_original_OP_decoded_image_equal'] = (original_exe==target)
    report = log_stage/'report.json'
    report.write_text(json.dumps(output, indent=2)+'\n')
    print('PROOF',report.relative_to(ROOT),'SHA256',sha(report.read_bytes()))


if __name__=='__main__':
    main()
