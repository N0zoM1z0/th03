#!/usr/bin/env python3
"""Review natural OP Music Room far-call relaxation on the current cold pair."""
from pathlib import Path
import argparse,fcntl,hashlib,json,os,subprocess,sys,tempfile,tomllib
from lib.op_music_call import SOURCE,PRAGMA,layout,runtime,negative_controls,native_field
from lib.op_current_source import LIVE_SOURCES,HISTORICAL_REVISION
from lib.omf import describe_omf
from lib.toolchain import attest_surface
from review_th03_op_cfg_work import images,sdk_inventory
from build_th03_op_work import compare_mz

ROOT=Path(__file__).resolve().parents[1];REPORT=ROOT/'.analysis/work/op-music-call-build.json'
INPUTS=('scripts/review_th03_op_music_call_work.py','scripts/lib/op_music_call.py','scripts/lib/op_current_source.py',
        'scripts/build_th03_op_work.py','scripts/review_th03_op_cfg_work.py','scripts/lib/op_cfg_layout.py',
        'scripts/lib/omf.py','scripts/lib/pc98.py','scripts/lib/toolchain.py','src/op/entry.cpp',SOURCE,
        'config/toolchain.toml','config/targets.toml','config/th03_diet.toml')
def need(v,m):
    if not v:raise ValueError('OP Music Room review: '+m)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs():return {n:sha((ROOT/n).read_bytes()) for n in INPUTS}
def case_file(root,name):
    matches=[p for p in root.iterdir() if p.name.lower()==name.lower()]
    need(len(matches)==1,'single native output: '+name);return matches[0]
def surfaces(config):
    rows=[attest_surface(ROOT,s) for s in config['surfaces'] if not s.get('bootstrap_only')]
    need(all(s['pass'] or not s['required'] for s in rows),'pinned installed tool surfaces');return rows

def control(work):
    config=tomllib.loads((ROOT/'config/toolchain.toml').read_text());prefix=ROOT/config['paths']['wine_prefix']
    before=surfaces(config);sdk_before=sdk_inventory(ROOT);phases=[]
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(prefix),
        MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/config['paths']['msdos_player']),'-e','-x']
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        with tempfile.TemporaryDirectory(prefix='',dir=prefix/'drive_c') as temp:
            scratch=Path(temp);need(len(scratch.name)==8,'DOS 8.3 scratch basename')
            win=lambda name:'C:\\'+scratch.name+'\\'+name
            source=(ROOT/SOURCE).read_bytes();need(source.count(PRAGMA.encode())==1,'one source declaration')
            for name,raw in (('th03/op_01.cpp',(work/'th03/op_01.cpp').read_bytes()),
                             ('src/op/entry.cpp',(ROOT/'src/op/entry.cpp').read_bytes()),
                             (SOURCE,source.replace(PRAGMA.encode(),b''))):
                p=scratch/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
            def execute(args,cwd,label):
                r=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
                phases.append(dict(label=label,returncode=r.returncode,output_sha256=sha(r.stdout)))
                need(r.returncode==0,label+': '+r.stdout.decode(errors='replace')[-800:])
            execute(dos+['tcc','-c','-I.','-I'+str('C:\\'+work.name),'-O','-b-','-3','-Z','-d',
                         '-DGAME=3','-ml',"-DBINARY='O'",'-oPLAIN.OBJ','th03/op_01.cpp'],scratch,'ordinary-far-control:compile')
            obj=case_file(scratch,'PLAIN.OBJ').read_bytes();need(describe_omf(obj)['valid'],'native control object')
            field=native_field(obj);need(field==[2221,4,0xCC,0x56,None,14],'ordinary far CALL control field')
            response=(work/'obj/th03/op.@l').read_text();needle='obj\\th03\\op_01.obj'
            need(response.count(needle)==1,'one real containing object response slot')
            response=response.replace(needle,win('PLAIN.OBJ')).replace('bin\\th03\\op.exe',win('PLAIN.EXE')).replace('obj\\th03\\op.map',win('PLAIN.MAP'))
            (scratch/'PLAIN.RSP').write_text(response)
            execute(dos+['tlink','@'+win('PLAIN.RSP')],work,'ordinary-far-control:link')
            result=compare_mz(case_file(scratch,'PLAIN.EXE').read_bytes(),(work/'bin/th03/op.target.exe').read_bytes())
            differences=result.pop('differing_program_sites')
    need(before==surfaces(config) and sdk_before==sdk_inventory(ROOT),'tools/SDK unchanged by control')
    need(len(differences)==5 and result['candidate_relocations']==608 and result['target_relocations']==607
         and not result['file_equal'] and not result['header_equal'] and not result['ordered_relocations_equal'],
         'unannotated native far CALL must fail target equality')
    return dict(native_field=field,comparison=result,differing_program_sites=differences,native_phases=phases,
        changed_source_files=[SOURCE],private_control_only=True,scratch_removed=True,
        maintained_source_or_current_build_modified=False,source_acceptance=False)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.parse_args()
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    work,target,candidate,cold,raw=images(ROOT)
    r=dict(schema='th03-op-music-call-current-review-v1',complete=False,implementation_sha256=inputs(),
        provenance='candidate-local-attested',source_acceptance=False,whole_product_accepted=False,
        canonical_unit_credit_changed=False,authored_byte_credit_changed=False,native_pair_built_now=False,
        cold_report_sha256=sha(raw),source_inventory_sha256=sha(json.dumps(cold['source_sha256'],sort_keys=True).encode()),
        immutable_historical_source_revision=HISTORICAL_REVISION,explicit_live_sources=list(LIVE_SOURCES))
    REPORT.parent.mkdir(exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    r['layout']=layout(ROOT,work,target,candidate);r['runtime']=runtime(target,candidate)
    r['negative_controls']=negative_controls(target);r['native_control']=control(work)
    need(images(ROOT)[4]==raw and inputs()==r['implementation_sha256'],'current native pair/source/model remained bound')
    r['complete']=True;save()
    print('OP Music Room: ordinary source far call, native same-CS fixup and TLINK relaxation pass; no enclosing-source or whole-product credit',flush=True)
    return 0
if __name__=='__main__':raise SystemExit(main())
