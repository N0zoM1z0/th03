#!/usr/bin/env python3
"""Read-only native receipt review for current TH03 MAIN Extra Attack/BOSS overlays.

Checks the complete genuine TC4/TLINK outputs, input source snapshots and
current maintained source identities. No compiler, linker or cold replay runs.
The frozen after596 historical receipt is a parent, not overwritten evidence.
"""
import argparse
import json
from pathlib import Path
import re

from probe_th03_main_exatt_layout import (ROOT, WORK, ENTITY, SOURCES, ORIGINAL_STAGES, MAP_ROWS, wrapper_source, rooted_source, rooted_wrapper, check_native_dependencies, SOURCE_HEADER_NEEDLE, BOSS_TEMPLATE, BOSS_TEMPLATE_NEEDLE, BINDING_MODE, BOSS_SHARED_UNITS, MAP_ORIGINAL, sha,
                                          need, scope, parent)
from lib.pc98 import parse_mz
from lib.main_mz_compact import compact_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from build_th03_mainl_display_work import payload, literal_fields


def file_pin(meta, root):
    path = ROOT / meta['path']
    need(path.is_file() and not path.is_symlink() and
         path.resolve().is_relative_to(root.resolve()),
         'preserved native evidence root: '+str(path))
    raw = path.read_bytes()
    need(len(raw)==meta['bytes'] and sha(raw)==meta['sha256'],
         'preserved native output hash/length: '+str(path))
    return raw


def expected_response(stage, n, units):
    rsp=parent.response(n)
    for u in units:
        old=(f'probe\\{parent.STAGE}\\r{n}\\{u}.obj' if u in parent.ORDER
             else f'probe\\af567c\\r{n}-{u}.obj' if u.startswith('ba_') and u not in BOSS_SHARED_UNITS
             else f'probe\\{ORIGINAL_STAGES[u]}\\r{n}\\{u}.obj' if u in ORIGINAL_STAGES
             else f'obj\\th03\\{u}.obj').encode()
        new=f'probe\\{stage}\\r{n}\\{u}.obj'.encode()
        need(rsp.count(old)==1, 'actual one physical original response slot '+u)
        rsp=rsp.replace(old,new)
    for ext in ('exe','map'):
        old=f'probe\\{parent.STAGE}\\r{n}.{ext}'.encode()
        new=f'probe\\{stage}\\r{n}.{ext}'.encode()
        need(rsp.count(old)==1,'actual native MAIN link path '+ext)
        rsp=rsp.replace(old,new)
    return rsp


def normalize_map(raw, stage, n, units):
    for u in units:
        old=f'M=probe/{stage}/r{n}/{u}.cpp'.encode()
        new=(f'M=probe/{parent.STAGE}/r{n}/{u}.cpp' if u in parent.ORDER
             else f'M=probe/{ORIGINAL_STAGES[u]}/r{n}/{u}.cpp' if u in ORIGINAL_STAGES
             else f'M={MAP_ORIGINAL[u]}' if u in MAP_ORIGINAL
             else f'M=th03/{u}.cpp').encode()
        need(raw.count(old)==MAP_ROWS.get(u,4), 'all native MAP module rows '+u)
        raw=raw.replace(old,new)
    return raw


def review(stage):
    need(re.fullmatch(r'af[0-9]+[a-z][0-9]*',stage) is not None,
         'known DOS-safe stage name')
    saved=ROOT/'.analysis/work'/('exatt-layout-'+stage)
    report_path=saved/'report.json'
    need(report_path.is_file() and not report_path.is_symlink(),
         'complete recorded proof '+stage)
    report=json.loads(report_path.read_text())
    units=report['units']
    need(report['schema']=='th03-main-source-rooted-overlay-v2' and
         report.get('compiler_source_binding')==BINDING_MODE and
         report['stage']==stage and len(units)==len(set(units)) and
         all(u in SOURCES for u in units) and
         len(report['rounds'])==2 and
         report['whole_original_image_and_relocations_equal'] is True and
         report['canonical_Factory_credit'] is False and
         report['parent_report']==parent.REPORT and
         report['parent_report_sha256']==sha((ROOT/parent.REPORT).read_bytes()),
         'current source-bound 2-round native overlay provenance')
    # The selected *current* C++ source variants must be exactly those compiled.
    sources={u:(ROOT/SOURCES[u]).read_bytes() for u in units}
    entity=(ROOT/ENTITY).read_bytes()
    boss_template=(ROOT/BOSS_TEMPLATE).read_bytes()
    # Explicit OMF dependency validation is mandatory. Old v1 receipts
    # verified a copied source snapshot, NOT which copy TC4 actually read.
    need(report['wrapper_sha256']=={u:sha(wrapper_source(u)) for u in units},
         'exact natural original producer wrapper input identities')
    needs_header = any(SOURCE_HEADER_NEEDLE in sources[u] for u in units)
    needs_boss_template = any(BOSS_TEMPLATE_NEEDLE in sources[u] for u in units)
    need(all(b'\r' not in s for s in (*sources.values(),entity)) and
         report['source_sha256']=={u:sha(v) for u,v in sources.items()} and
         (not needs_header or report['entity_header_sha256']==sha(entity)) and
         (not needs_boss_template or
          report.get('boss_template_header_sha256')==sha(boss_template)),
         'native compiler inputs remain bound to maintained live source')
    previous=json.loads((ROOT/parent.REPORT).read_text())
    need(previous['complete'] and len(previous['rounds'])==2,
         'frozen original full MAIN source-native parent')
    target=read_verified_artifact(ROOT,find_artifact(
        load_target_manifest(ROOT/'config/targets.toml'),'th03-main'))
    mz_target=parse_mz(target)
    need(len(target)==130882 and len(mz_target.relocations)==1553,
         'immutable candidate-local-attested Japanese MAIN')
    originals={u:(WORK/'obj/th03'/(u+'.obj')).read_bytes() for u in units}
    allround=[]
    for n,row in enumerate(report['rounds'],start=1):
        need(row['number']==n and set(row['scopes'])==set(units),
             'source-scope row and original round order')
        expected=expected_response(stage,n,units)
        scratch=WORK/'probe'/stage
        need((scratch/f'r{n}.@l').read_bytes()==expected and
             row['response_sha256']==sha(expected),
             'actual original 99-object TLINK response')
        rd=scratch/f'r{n}'
        saved_header = (rd/ENTITY).read_bytes()
        need(sha(saved_header.replace(b'\r\n',b'\n'))==report['entity_header_sha256'] and
             (not needs_header or saved_header==entity.replace(b'\n',b'\r\n')),
             'retained header snapshot and consumed-input identity round '+str(n))
        if needs_boss_template:
            native_header=(rd/BOSS_TEMPLATE).read_bytes()
            need(native_header==boss_template.replace(b'\n',b'\r\n'),
                 'compiled BOSS physical template header matches maintained bytes')
        output=row['outputs']
        need(set(output)=={u+'_obj' for u in units}|{'exe','map','compact_mz'},
             'complete OBJ/EXE/MAP/vector native outputs')
        items={k:file_pin(v,saved) for k,v in output.items()}
        for u in units:
            need((rd/SOURCES[u]).read_bytes()==
                 rooted_source(u,stage,n,sources[u]).replace(b'\n',b'\r\n'),
                 'compiler-forced maintained source overlay '+u)
            wrapper=rooted_wrapper(u,stage,n,wrapper_source(u)).replace(b'\n',b'\r\n')
            need((rd/(u+'.cpp')).read_bytes()==wrapper,
                 'compiler-forced original source wrapper '+u)
            actual=items[u+'_obj']
            need((rd/(u+'.obj')).read_bytes()==actual,
                 'actual native built OBJ '+u)
            check_native_dependencies(actual,u,stage,n,
                SOURCE_HEADER_NEEDLE in sources[u],
                BOSS_TEMPLATE_NEEDLE in sources[u])
            need(scope(actual,originals[u],u)==row['scopes'][u],
                 'complete CODE, native fields, PUBLICs and segment layout '+u)
        phases=row['phases']
        labels=[f'round{n}-{u}-TC4' for u in units]+[f'round{n}-TLINK']
        need([x['label'] for x in phases]==labels and
             all(x['exit_code']==0 and file_pin(x['log'],saved) is not None
                 for x in phases),
             'all actual original compiler and linker writer-log identities')
        prev=previous['rounds'][n-1]['outputs']
        exe=items['exe']
        need(exe==parent.read_pin(prev['exe']) and
             normalize_map(items['map'],stage,n,units)==parent.read_pin(prev['map']),
             'full original source-native EXE and all MAP module/segment rows')
        parsed=parse_mz(exe)
        need(parsed.program_image==mz_target.program_image and
             parsed.relocations==mz_target.relocations and
             compact_mz(exe)==items['compact_mz']==target,
             'full Japanese MAIN source image, ordered MZ relocations and MZ file')
        allround.append(items)
    need(allround[0]['exe']==allround[1]['exe'] and
         allround[0]['compact_mz']==allround[1]['compact_mz'] and
         all(payload(allround[0][u+'_obj'])==payload(allround[1][u+'_obj']) and
             literal_fields(allround[0][u+'_obj'])==literal_fields(allround[1][u+'_obj'])
             for u in units),
         'two native round independent complete original vectors repeat')
    totals={key:sum(v[key] for v in report['rounds'][0]['scopes'].values())
            for key in ('CODE_bytes','ordered_native_fields','PUBLICs')}
    return {'stage':stage,'report_sha256':sha(report_path.read_bytes()),
            'native_rounds':len(allround),'complete_original_units':len(units),
            'original_scope':totals,'full_Japanese_MAIN_equal':True}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stage',nargs='+',required=True)
    args=ap.parse_args()
    for stage in args.stage:
        print(json.dumps(review(stage),sort_keys=True),flush=True)

if __name__=='__main__':
    main()
