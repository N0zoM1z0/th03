#!/usr/bin/env python3
"""Replay consumed root source and two actual hybrid builds, not packed exact."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from lib import mainl_root_source as composer
from lib.mainl_graphics_link import relocs, diffs, parse_mz
from review_th03_mainl_root import analyze, matrix, RANGES
ROOT = Path(__file__).resolve().parents[1]
RECIPE = 'config/th03_mainl_root_link.json'
RECIPE_SHA = '96ecf82a15f63fb58bc3cb7bf61e6a145e056de57b4096cebb3d18469251e279'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def need(ok, message):
    if not ok: raise ValueError(message)
def validate_partition(unit):
    need(unit == dict(unit_id='th03-mainl-decoded-root', segment=0x95f, offset=0x186, bytes=2488, source_paths=['src/mainl/root/root.asm']), 'root existing-unit partition differs')
def replay(root=ROOT):
    raw = (root / RECIPE).read_bytes()
    need(sha(raw) == RECIPE_SHA, 'recipe identity differs')
    recipe = json.loads(raw)
    for path, expected in recipe['proof_inputs_sha256'].items():
        need(sha((root / path).read_bytes()) == expected, 'retained input differs: ' + path)
    validate_partition(recipe['unit'])
    source_recipe = json.loads((root / 'config/th03_mainl_root_source.json').read_text())
    values = {}
    for key in ['previous_generated_root', 'free_all_provider', 'source', 'composer']:
        row = source_recipe[key]; values[key] = (root / row['path']).read_bytes()
        need(sha(values[key]) == row['sha256'], 'source recipe identity differs: ' + key)
    generated = composer.compose(values['previous_generated_root'], values['free_all_provider'], values['source'])
    products = []
    for build in recipe['builds']:
        work = root / build['work']; output = root / build['output']
        manifest = json.loads((root / build['proposal'] / 'manifest.json').read_text())
        for row in manifest['inputs']:
            need(sha((root / row['path']).read_bytes()) == row['sha256'], 'guarded native input differs: ' + row['path'])
        for name in ['obj/th03/mainl.obj', 'bin/th03/mainl.exe', 'obj/th03/mainl.map']:
            need(name not in manifest['repeat_inputs'], 'native output copied as input: ' + name)
        if build.get('repeat'):
            mtimes = json.loads((output / 'source-mtimes.json').read_text())
            for name, row in manifest['repeat_inputs'].items():
                first, second = root / row['path'], work / name
                need(first.read_bytes() == second.read_bytes(), 'repeat source input differs: ' + name)
                need(first.stat().st_mtime_ns == second.stat().st_mtime_ns == row['mtime_ns'] == mtimes[name], 'declared repeat input mtime differs: ' + name)
        done = json.loads((output / 'completion.json').read_text())
        need(done['complete'] and done['native_invocations'] == 2 and done['owned_lock_released'] and not done['errors'], 'fresh root/link incomplete')
        for path, content in generated.items(): need((work / path).read_bytes() == content, 'consumed root source differs: ' + path)
        for phase in ['root', 'link']:
            start = json.loads((output / (phase + '-started.json')).read_text())
            end = json.loads((output / (phase + '-finished.json')).read_text())
            transition = json.loads((output / (phase + '-registry-transition.json')).read_text())
            need(start['argv'] == manifest['native_argv'][phase] and start['wait_seconds'] == 90 and start['cleanup_seconds'] == 15, 'native command/budget differs')
            need(end['exit_code'] == 0 and not end['timeout'] and not end['cleanup_uncertain'] and not end['poison'] and not end['survivors'] and not end['errors'] and transition['ok'], 'native cleanup/result differs')
        products.append({p: (work / p).read_bytes() for p in ['obj/th03/mainl.obj', 'bin/th03/mainl.exe', 'obj/th03/mainl.map']})
    need(len(products) == 2 and products[0] == products[1], 'repeat raw OBJ/EXE/MAP differs')
    target = parse_mz((root / recipe['decoded_target']).read_bytes())
    candidate_raw = products[0]['bin/th03/mainl.exe']
    need(candidate_raw == (root / recipe['previous_exe']).read_bytes(), 'retained complete EXE identity differs')
    prior = json.loads((root / recipe['prior_model_proof']).read_text())
    need(prior['input_sha256']['exe'] == sha(candidate_raw) and prior['diagnostic_checks_pass'] and prior['runtime_equal'] and prior['staff_runtime_equal'], 'prior complete-image model proof differs')
    candidate = parse_mz(candidate_raw)
    need(target.valid and candidate.valid, 'invalid MZ')
    start, end = 0x95f * 16 + 0x186, 0x95f * 16 + 0xb3e
    need(target.program_image[start:end] == candidate.program_image[start:end], 'root raw bytes differ')
    ta, ca = relocs(target), relocs(candidate)
    scoped = lambda rows: [r for r in rows if start <= r[0] * 16 + r[1] < end]
    tr, cr = scoped(ta), scoped(ca)
    need(len(tr) == len(cr) == 114 and Counter(tr) == Counter(cr), 'root relocation membership differs')
    need(analyze(target.program_image) == analyze(candidate.program_image), 'root instruction/ABI analysis differs')
    a, b = matrix(target), matrix(candidate)
    need(a == b, 'root runtime observations differ')
    return dict(kind='mainl-root-consumed-source-replay', recipe_sha256=sha(raw),
        source_owned_bytes_eligible=2488, existing_source_units=[recipe['unit']],
        native_fragment_consumption_proven=True, fresh_root_link_builds=2,
        raw_repeat_obj_exe_map_equal=True, root_relocation_membership_equal=True,
        root_ordered_relocations_equal=tr==cr, root_ordered_difference_count=sum(x!=y for x,y in zip(tr,cr)),
        target_decoded_difference_count=len(diffs(target.program_image,candidate.program_image)),
        global_relocation_membership_equal=Counter(ta)==Counter(ca),
        global_ordered_difference_count=sum(x!=y for x,y in zip(ta,ca)),
        runtime_observations_equal=True, root_model_records_per_image=len(a), root_model_calls_per_image=456,
        root_models_rerun=True, prior_staff_models_rerun=False,
        prior_scoped_bytes_preserved_by_complete_exe_identity=9483, total_scoped_target_equal_bytes=11971,
        native_invocations_in_this_replay=0, opt_in_only=True, cold_aggregate=False, exact_acceptance=False)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args();result=replay();text=json.dumps(result,indent=2)+'\n'
    if a.output:
        with a.output.open('x') as f:f.write(text)
    else: print(text,end='')
if __name__ == '__main__': main()
