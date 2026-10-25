"""Read-only validation of the entire existing OP native cold graph."""
import hashlib
import tomllib
from lib.omf import describe_omf
from lib.toolchain import attest_surface


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(value,message):
    if not value:raise ValueError('OP complete cold graph: '+str(message))


def verify(root,work,target,candidate,report):
    import build_th03_op_work as build
    need(root.resolve()==build.ROOT and work==build.WORK,'live source/build roots')
    need(report['complete'] and report['raw_repeat_equal'] and report['retained_project_objects']==0,'source-only cold pair')
    need(report['recipe_sha256']==build.recipe_inventory(),'complete current recipe')
    files=build.source_graph()
    need(report['source_sha256']=={n:sha(raw) for n,raw in sorted(files.items())},'entire current source inventory')
    need(all((work/n).read_bytes()==raw for n,raw in files.items()),'every staged source/header')
    producers=build.producers(files)
    need(len(producers)==30 and len(report['rounds'])==2 and [r['round'] for r in report['rounds']]==[1,2],'all producers and two cold rounds')
    outputs=report['rounds'][0]['outputs']
    need(outputs==report['rounds'][1]['outputs'] and set(outputs)=={p['output'] for p in producers}|{'bin/th03/op.exe','obj/th03/op.map'},'all32 raw outputs in both rounds')
    for name,row in outputs.items():
        raw=(work/name).read_bytes()
        need(row==dict(bytes=len(raw),sha256=sha(raw)),'complete current output: '+name)
        if name.endswith('.obj'):need(describe_omf(raw)['valid'],'all native OMF: '+name)
    labels=[f'round{r}:'+name for r in (1,2) for name in [p['output'] for p in producers]+['link']]+['diet:selfcheck','diet:restore-target']
    need([p['label'] for p in report['native_phases']]==labels and
        all(p['returncode']==(1 if p['label']=='diet:restore-target' else 0) for p in report['native_phases']),
        'complete serial native schedule')
    config=tomllib.loads((root/'config/toolchain.toml').read_text())
    surfaces=[attest_surface(root,s) for s in config['surfaces'] if not s.get('bootstrap_only')]
    need(surfaces==report['toolchain_surfaces'] and all(s['pass'] or not s['required'] for s in surfaces),'all current pinned tool surfaces')
    decoded=(work/'bin/th03/op.target.exe').read_bytes()
    linked=(work/'bin/th03/op.exe').read_bytes()
    need(decoded==linked and target.valid and candidate.valid and build.compare_mz(linked,decoded)==report['comparison'],'whole decoded file and independent MZ comparison')
    # cfg.images independently checks the pinned Japanese decoded/stored
    # identities and consumed CFG SDK headers before reaching this function.
    stored=(work/'bin/th03/op.packed.exe').read_bytes()
    packing=report['packing']
    need(packing['options']==['-B'] and packing['stored_equal'] and packing['raw_repeat_equal'] and
        packing['same_tool_roundtrip'] and len(packing['rounds'])==2,'complete two-round DIET packing proof')
    need(all(p['packed_sha256']==sha(stored) and p['packed_bytes']==len(stored) and p['stored_equal'] and p['decoded_roundtrip_equal']
        for p in packing['rounds']),'both complete stored/decoded roundtrips')
    return dict(source_files=len(files),native_objects_per_round=30,outputs_per_round=32,rounds=2,
        recipe_sha256=report['recipe_sha256'],decoded_sha256=sha(decoded),stored_sha256=sha(stored),
        entire_current_source_staging_outputs_tools_and_packing_validated=True,native_pair_rebuilt=False)
