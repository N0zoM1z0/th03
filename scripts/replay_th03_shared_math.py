#!/usr/bin/env python3
"""Cold compile symbolic vector and LUT ASM with separately recorded producers."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib
from lib.omf import describe_omf, normalize_dependency_timestamps, parse_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from replay_th03_main_exact_units import execute
from replay_th03_shared_cdg_load import apply_previous
from replay_th03_shared_cdg_draw import producer_records
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import sha
from review_th03_shared_math import ROOT, PROFILES, PARENT, PARENT_SHA, analyze, matrix, coverage, semantic

MANIFEST='config/th03_shared_math_candidate.toml'
PROOF='.analysis/sol-shared-math-review-20261006.json'
PROOF_SHA='8f0734efcc7a53706066af5e5fce18daca97a3f7cee96b30adf72665269ca938'


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run-id',required=True);args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',args.run_id):raise ValueError('invalid run id')
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('math diagnostic proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw)}
    if not proof['diagnostic_checks_pass'] or proof['exact_acceptance']:raise ValueError('math diagnostic scope differs')
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('math prerequisite differs: '+p)
    output=ROOT/'.analysis/th03-shared-math'/args.run_id;output.mkdir(parents=True,exist_ok=False)
    cfg=tomllib.loads((ROOT/MANIFEST).read_text());manifests={};source_files={*[c['source'] for c in cfg['carriers']],*cfg['support_files']}
    for name in ('score','title','entry','menu','music','select'):
        path=f'config/th03_op_{name}_candidate.toml';c=manifests[name]=tomllib.loads((ROOT/path).read_text());inputs[path]=sha((ROOT/path).read_bytes());source_files.update(c.get('support_files',[]))
        if 'source' in c:source_files.add(c['source'])
        for u in c.get('units',[]):source_files.add(u['source'])
    shared={}
    for name in ('cdg_load','cdg_draw','text'):
        path=f'config/th03_shared_{name}_candidate.toml';c=shared[name]=tomllib.loads((ROOT/path).read_text());inputs[path]=sha((ROOT/path).read_bytes());source_files.update(c.get('support_files',[]))
        if 'source' in c:source_files.add(c['source'])
        if 'glyph_include' in c:source_files.add(c['glyph_include'])
        source_files.update(ca['source'] for ca in c.get('carriers',[]))
    source_files=sorted(source_files)
    for p in [MANIFEST,'scripts/replay_th03_shared_math.py','tests/test_shared_math_review.py','.analysis/sol-shared-math-controls-20261006.log',*source_files]:inputs[p]=sha((ROOT/p).read_bytes())
    snapshot=output/'repository-inputs'
    for p,h in inputs.items():
        if p.startswith('.analysis/'):continue
        dest=snapshot/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,dest)
        if sha(dest.read_bytes())!=h:raise ValueError('math source snapshot changed')
    previous=json.loads((ROOT/PARENT).read_bytes())
    if sha((ROOT/PARENT).read_bytes())!=PARENT_SHA:raise ValueError('math previous cold proof differs')
    artifacts={a:find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-'+a) for a in PROFILES}
    stored={a:read_verified_artifact(ROOT,x) for a,x in artifacts.items()};targets={a:parse_mz((ROOT/proof['observations'][a][0]['path']).read_bytes()) for a in PROFILES}
    subprocess.run([sys.executable,'scripts/attest_toolchain.py'],cwd=ROOT,check=True)
    tool=tomllib.loads((ROOT/'config/toolchain.toml').read_text());attestation=sha((ROOT/'.analysis/toolchain/attestation.json').read_bytes())
    env=os.environ.copy();env.update(DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(ROOT/tool['paths']['wine_prefix']),MSDOS_PATH=r'C:\TC4\BIN')
    archive=output/'reference.tar';subprocess.run(['git','archive','--format=tar',f'--output={archive}',cfg['reference_revision']],cwd=ROOT/'_reference/ReC98',check=True);archive_sha=sha(archive.read_bytes());rounds=[]
    for number in (1,2):
        logs=output/f'round{number}';work=logs/'source';work.mkdir(parents=True);subprocess.run(['tar','-xf',str(archive),'-C',str(work)],check=True)
        if list(work.rglob('*.obj')) or list((work/'bin').glob('th0[1-5]/*.exe')):raise ValueError('math archive is not cold')
        for p in source_files:
            dest=work/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(snapshot/p,dest)
            if Path(p).suffix in ('.asm','.inc'):dest.write_bytes(dest.read_bytes().replace(b'\r\n',b'\n').replace(b'\n',b'\r\n'))
        apply_previous(work,manifests)
        for name in ('cdg_load','text'):
            c=shared[name]
            if sha((work/c['wrapper']).read_bytes())!=c['original_wrapper_sha256']:raise ValueError('math preceding CPP wrapper differs')
            (work/c['wrapper']).write_text(f'#include "{c["source"]}"\n')
        for c in shared['cdg_draw']['carriers']:
            if sha((work/c['wrapper']).read_bytes())!=c['original_wrapper_sha256']:raise ValueError('math preceding drawing wrapper differs')
            (work/c['wrapper']).write_bytes(('include '+c['source']+'\r\n').encode())
        for c in cfg['carriers']:
            original_wrapper=(work/c['original_wrapper']).read_bytes()
            if c['original_wrapper'].endswith('.asm'):original_wrapper=original_wrapper.replace(b'\r\n',b'\n')
            if sha(original_wrapper)!=c['original_wrapper_sha256']:raise ValueError('math original frozen wrapper differs')
            (work/c['wrapper']).write_bytes(('include '+c['source']+'\r\n').encode())
        tup=work/'Tupfile.lua';original=tup.read_bytes()
        if sha(original)!=cfg['original_tup_sha256']:raise ValueError('math original frozen link graph differs')
        text=original.decode();marker='th03:branch(MODEL_LARGE, { cflags = "-DBINARY=\'L\'" }):link("mainl", {'
        start=text.index(marker);end=text.index('\n})',start)+3;block=text[start:end]
        if block.count('"th03/vector.cpp"')!=1:raise ValueError('math original vector link position differs')
        modified=text[:start]+block.replace('"th03/vector.cpp"','"th03/vector_far.asm"')+text[end:];tup.write_text(modified)
        if modified.replace('"th03/vector_far.asm"','"th03/vector.cpp"')!=text:raise ValueError('math changed another link graph entry')
        command=['wine','cmd','/d','/c',r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%' r'&&set PROCESSOR_ARCHITECTURE=AMD64&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat']
        build=execute(command,work,env,logs/'cold-build.log')
        objects={p.relative_to(work).as_posix():sha(normalize_dependency_timestamps(p.read_bytes())) for p in sorted((work/'obj').rglob('*.obj'))};game={p:h for p,h in objects.items() if any(p.startswith(f'obj/th0{n}/') for n in range(1,6))};products={}
        for item in load_target_manifest(ROOT/'config/targets.toml')['artifacts']:
            p=Path('bin')/item['game']/Path(item['private_path']).name;products[p.as_posix()]=sha((work/p).read_bytes())
        if products!=previous['rounds'][0]['products'] or len(products)!=20 or len(game)!=351 or len(objects)!=417:raise ValueError('math complete product/object vector differs')
        owned={c['object'] for c in cfg['carriers']}
        if {p:h for p,h in game.items() if p not in owned}!={p:h for p,h in previous['rounds'][0]['game_objects'].items() if p not in owned}:raise ValueError('math changed another original game object')
        nongame={p:dict(previous=previous['rounds'][0]['all_objects'][p],current=h) for p,h in objects.items() if p not in game and h!=previous['rounds'][0]['all_objects'][p]};producers={}
        for c in cfg['carriers']:
            raw=(work/c['object']).read_bytes();obj=describe_omf(raw);old=ROOT/Path(proof['observations']['mainl'][number]['path']).parents[2]/c['original_object'];inputs[str(old.relative_to(ROOT))]=sha(old.read_bytes())
            if not obj['valid'] or obj['translator_comments']!=['Turbo Assembler  Version 5.0']:raise ValueError('math maintained TASM producer differs')
            same=producer_records(raw)==producer_records(old.read_bytes())
            if c['size']==30 and not same or c['size']==160 and same:raise ValueError('math declared original producer association differs')
            segs=[r.data.hex() for r in parse_omf(raw) if r.name=='SEGDEF'];expected=['28a000020301'] if c['size']==160 else ['481e00020301']
            if segs!=expected:raise ValueError('math maintained physical segment layout differs: '+str(segs))
            # Record exact SEGDEF bytes; raw decoded extent/public/layout gates
            # separately constrain their physical output rather than normalize
            # a compiler-to-assembler producer change into equality.
            producers[c['object']]=dict(normalized_sha256=obj['dependency_timestamp_normalized_sha256'],module_name=obj['module_name'],translator_comments=obj['translator_comments'],records=producer_records(raw),segments=segs,original_nondependency_records_equal=same,original_records=producer_records(old.read_bytes()))
        observations={}
        for art,p in PROFILES.items():
            candidate=parse_mz((work/f'bin/th03/{art}.exe').read_bytes());meta=analyze(candidate.program_image,p);mp=work/f'obj/th03/{art}.map';map_text=mp.read_text();maprows=code_rows(map_text,len(candidate.program_image));comparisons={}
            for c in cfg['carriers']:
                if art not in c['artifacts']:continue
                row=next(r for r in maprows if r['module']==c['wrapper'] and r['size'])
                if (row['segment'],row['offset'],row['size'])!=(c[art+'_segment'],c[art+'_offset'],c['size']):raise ValueError('math complete source MAP ownership differs')
                comp=extent_observation(targets[art],candidate,row)
                if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('math complete original raw/ordered carrier differs')
                comparisons[c['wrapper']]=comp
            publics={'_hflip_lut_generate':p['lut']}
            if 'vector' in p:publics.update(VECTOR2=p['vector'],VECTOR2_BETWEEN_PLUS=p['between'])
            for public,start in publics.items():
                coords={(int(seg,16),int(at,16)) for seg,at in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+public+r'\s*$',map_text,re.M)}
                if coords!={(p['cs'],start)}:raise ValueError('math original public binding differs')
            cpu=matrix(candidate,p,focused=True);target_cpu=matrix(targets[art],p,focused=True)
            if semantic(cpu)!=semantic(target_cpu):raise ValueError('math maintained scalar contracts differ')
            changes=[dict(decoded_linear=i,target=x,candidate=y) for i,(x,y) in enumerate(zip(targets[art].program_image,candidate.program_image)) if x!=y]
            if len(candidate.program_image)!=len(targets[art].program_image) or len(changes)!=(6 if art=='op' else 21):raise ValueError('math known whole decoded inequality differs')
            observations[art]=dict(comparisons=comparisons,cpu=cpu,coverage=coverage(meta,cpu),map_sha256=sha(mp.read_bytes()),whole_decoded=dict(equal=False,changes=changes,original_ordered_relocations_equal=targets[art].relocations==candidate.relocations))
        rounds.append(dict(number=number,build=build,all_objects=objects,game_objects=game,products=products,nongame_object_changes=nongame,producers=producers,link_graph=dict(original_sha256=sha(original),modified_sha256=sha(tup.read_bytes()),only_mainl_vector_carrier_replaced=True,original_vector_object_retained=True),observations=observations))
        print('PASS maintained shared math cold round',number,flush=True)
    if rounds[0]['products']!=rounds[1]['products'] or rounds[0]['game_objects']!=rounds[1]['game_objects']:raise ValueError('math cold determinism differs')
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('math source input changed: '+p)
    if sha(archive.read_bytes())!=archive_sha or any(sha((snapshot/p).read_bytes())!=inputs[p] for p in source_files):raise ValueError('math frozen archive/source snapshot changed')
    if any(read_verified_artifact(ROOT,a)!=stored[art] for art,a in artifacts.items()):raise ValueError('math canonical target changed')
    report=dict(kind='th03-shared-math-maintained-cold-probes',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,reference_archive_sha256=archive_sha,toolchain_receipt_sha256=attestation,rounds=rounds,diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,notes='Natural symbolic vectorASM160 forMAINL plus sharedLUTASM30. No referenceCXX opcodearrays/codestring adopted. ExistingMAIN naturalASM source remains a candidate precedent withoutinheritedacceptance; MAIN accepted aggregate unchanged. OriginalCPPvector.obj retainedforotherproducts; onlyMAINL inputat sameorderedposition replacedbynewvector_far.obj. Both20product351gameobject vectors deterministic/all417OMFrecorded; all20products equalprecedingtext,349otheroriginalgameobjects unchanged. LUToriginalnondependencyrecords equal; vectorTC86->TASM producer differs explicitly, notnormalizedaway. Complete original raw/ordered carrierbytes/public/MAP match; sourcecases coverallreachablepositions withfullphysical-state/orderedstores/nativeframes/wordalias/reentry/IFDF andrealDIVstops. Tables/DGROUP/globaldeclarations/interruptframes/devices/canonicalpacking/fullproduct/exact remainopen.')
    (output/'receipt.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS source-present shared math cold probes; exact open')


if __name__=='__main__':main()
