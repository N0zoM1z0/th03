"""Source-only MAINL cold aggregate. No compiler, linker, target or object reads.
Rebuilds the ownership overlays from the frozen source archive and live maintained
sources. Writes only a new ignored source staging directory. Native execution is separate.
"""
from pathlib import Path
import argparse, datetime, hashlib, importlib, io, json, os, re, subprocess, sys, tarfile, tomllib
ROOT=Path.cwd(); sys.path.insert(0,str(ROOT/'scripts'))
REV='b6ba5b0a529edbb31efdf8c0e939263804f8ee47'
CONTEXT=ROOT/'config/mainl_cold_context'
STAMP=int(datetime.datetime(2026,10,21,tzinfo=datetime.timezone.utc).timestamp())*10**9
SOURCE_SUFFIXES={'.asm','.cpp','.c','.h','.hpp','.inc','.inl','.asp','.lua'}
def sha(raw): return hashlib.sha256(raw).hexdigest()
def lf(raw): return raw.replace(b'\r\n',b'\n')
def crlf(raw): return lf(raw).replace(b'\n',b'\r\n')
def read(p): return (ROOT/p).read_bytes()
def compose_all(context=None):
    context=Path(context) if context is not None else CONTEXT
    archive=subprocess.check_output(['git','archive','--format=tar',REV],cwd=ROOT/'_reference/ReC98')
    with tarfile.open(fileobj=io.BytesIO(archive)) as t:
        original={m.name:t.extractfile(m).read() for m in t.getmembers() if m.isfile() and Path(m.name).suffix.lower() in SOURCE_SUFFIXES}
    files={n:crlf(b) for n,b in original.items()}; provenance={n:'frozen source archive '+REV for n in files}; stages=[]
    def add(payload,stage):
        for n,b in payload.items(): files[n]=crlf(b);provenance[n]=stage
        stages.append(dict(name=stage,outputs=sorted(payload)))
    def owned(names,stage): add({n:read(n) for n in names},stage)
    # Each root stage receives the immediately preceding generated root, never an
    # old carrier root. Heap is intentionally new to this combined build.
    from stage_th03_mainl_heap import stage_root,SOURCE_PATH
    root=stage_root(lf(original['th03_mainl.asm']),read(SOURCE_PATH))
    add({'th03_mainl.asm':root,SOURCE_PATH:read(SOURCE_PATH)},'maintained heap')
    from lib.mainl_staff_source import generate,FRAGMENTS
    add(generate(files['th03_mainl.asm'],read('src/mainl/formats/cdg_effects.cpp'),{n:read(v[1]) for n,v in FRAGMENTS.items()}),'maintained graphics and staff split')
    from lib.mainl_root_source import compose as root_compose,SOURCE
    add(root_compose(files['th03_mainl.asm'],original['th03/formats/cdg_free_all.asm'],read(SOURCE)),'maintained root')
    from lib.mainl_pi_source import compose as pi_compose,SOURCE
    add(pi_compose(files['th03_mainl.asm'],original['libs/master.lib/graph_pi_load_pack.asm'],read(SOURCE)),'maintained PI decoder')
    for family in ['resources','archive_io','display_hardware','root_tail']:
        module=importlib.import_module('lib.mainl_'+family+'_source')
        paths=getattr(module,'PROVIDER_PATHS',{n:'libs/master.lib/'+n+'.asm' for n in module.NAMES})
        providers={n:original[p] for n,p in paths.items()}
        if family=='root_tail': providers.update({n:b'\t\tdb 0\n' for n in module.ROOT_ANCHORS})
        maintained={n:read('src/mainl/'+family+'/'+n+'.asm') for n in providers}
        add(module.compose(files['th03_mainl.asm'],providers,maintained),'maintained '+family)
    recipe=json.loads(read('config/th03_mainl_linked_game_source.json'))
    from lib.mainl_linked_game_source import compose as linked_compose
    providers={p['name']:original[p['provider_relative']] for p in recipe['providers']}
    wrappers={p['name']:original[p['wrapper_relative']] for p in recipe['providers']}
    maintained={p['name']:read(p['source']['path']) for p in recipe['providers']}
    add(linked_compose(files['th03_mainl.asm'],providers,wrappers,maintained,read(recipe['staff_source']['path']),recipe),'maintained linked game')
    from lib.mainl_vsync_alignment_source import compose as align_compose,SOURCE,CDG_SOURCE
    add(align_compose(files['th03_mainl.asm'],original['libs/master.lib/vs[data].asm'],read(SOURCE),original['th03/formats/cdg[data].asm'],read(CDG_SOURCE)),'maintained historical VSync and ordinary DATA alignment')
    from stage_th03_mainl_cutscene import read_inputs,SLOT,WRAPPER
    add({**read_inputs(ROOT),SLOT:WRAPPER},'maintained cutscene')
    from stage_th03_mainl_regist import read_inputs,SLOTS
    add({**read_inputs(ROOT),**{n:('#include "'+p+'"\n').encode() for n,p in SLOTS.items()}},'maintained registration')
    ownership={p['object']:dict(source=p['source']['path'],wrapper=p['wrapper_relative'],recipe='config/th03_mainl_linked_game_source.json') for p in recipe['providers']}
    ownership.update({('obj/th03/'+Path(n).stem+'.obj'):dict(source=p,wrapper=n,recipe='scripts/stage_th03_mainl_regist.py') for n,p in SLOTS.items()})
    ownership['obj/th03/cutscene.obj']=dict(source='src/mainl/cutscene.cpp',wrapper='th03/cutscene.cpp',recipe='scripts/stage_th03_mainl_cutscene.py')
    for family in ['pi','input','math','cdg_draw','cdg_load','text','snd_load']:
        cfgpath='config/th03_shared_'+family+'_candidate.toml';cfg=tomllib.loads(read(cfgpath).decode())
        for row in cfg.get('carriers',[cfg]):
            if row.get('artifacts') and not any('mainl' in a for a in row['artifacts']): continue
            if 'source' not in row: continue
            source=row['source'];wrapper=row['wrapper']; names=[source,*cfg.get('support_files',[])]
            if family=='text':names.append(cfg['glyph_include'])
            owned(names,'maintained shared '+family)
            line=('include '+source+'\n') if wrapper.endswith('.asm') else ('#include "'+source+'"\n')
            add({wrapper:line.encode()},'maintained shared '+family+' wrapper')
            obj=row.get('original_object',row['object']);ownership[obj]=dict(source=source,wrapper=wrapper,recipe=cfgpath,output=row['object'])
    ownership['obj/th03/mainl.obj']=dict(source='th03_mainl.asm',wrapper='th03_mainl.asm',recipe='chained maintained composers')
    for n in ['gfxpre','gfxdis']:
        ownership['obj/th03/'+n+'.obj']=dict(source='src/mainl/formats/cdg_effects.cpp',wrapper=n+'.cpp',recipe='scripts/lib/mainl_graphics_source.py')
    # Shared recipes may rely on compatibility headers installed by a predecessor.
    # Close those explicit repository includes rather than retain cached carriers.
    changed=True
    while changed:
        changed=False
        for n,b in list(files.items()):
            if not n.startswith(('src/','compat/')): continue
            for target in re.findall(rb'^\s*#include \"((?:src|compat)/[^\"]+)\"',b,re.M):
                dep=target.decode()
                if dep not in files:
                    owned([dep],'transitive maintained compatibility dependency');changed=True
    # The original scanner's codestring is reference context, not an invented
    # alignment fix or source-owned extra byte.
    assert b'#pragma codestring \"\\x90\"' in files['src/mainl/linked_game/input_sense.cpp']
    # This generated sprite include is declared source context, not a cached OBJ.
    asset='th03/sprites/flake.asp';add({asset:(context/'flake.asp').read_bytes()},'declared generated sprite source context')
    response=crlf((context/'mainl.@l').read_bytes())
    oldobjs=re.findall(r'obj\\[^\s,]+\.obj',response.decode())
    assert len(oldobjs)==35 and len(ownership)==35
    tup=original['Tupfile.lua'].decode();first={}
    pattern=r'th0([123]):branch\(MODEL_LARGE, \{ cflags = "-DBINARY=\x27([^\x27]+)\x27" \}\):link\("([^"\n]+)", \{'
    for match in re.finditer(pattern,tup):
        end=tup.index('\n})',match.end())
        for name in re.findall(r'"([^"\n]+\.(?:c|cpp|asm))"',tup[match.end():end]):first.setdefault(name,(int(match[1]),match[2],match[3]))
    graph=[]
    for ordinal,old in enumerate(oldobjs):
        key=old.replace('\\','/');row=ownership[key].copy();wrapper=row['wrapper'];out=row.get('output',key)
        prior='th03/vector.cpp' if key.endswith('/vector.obj') else wrapper
        game,binary,first_binary=(3,'L','mainl') if wrapper in ['gfxpre.cpp','gfxdis.cpp'] else first[prior]
        kind='tasm' if wrapper.endswith('.asm') else 'tcc'
        flags=['/m','/mx','/kh32768','/t','/dGAME='+str(game)] if kind=='tasm' else ['-c','-I.','-O','-b-','-3','-Z','-d','-DGAME='+str(game),'-ml',"-DBINARY='"+binary+"'",'-n'+str(Path(out).parent)+'/']
        graph.append(dict(ordinal=ordinal,original_object=key,output=out,kind=kind,game=game,binary=binary,first_binary=first_binary,flags=flags,**{k:v for k,v in row.items() if k!='output'}))
        if out!=key: response=response.replace(old.encode(),out.replace('/','\\').encode())
    add({'obj/th03/mainl.@l':response},'original response order; explicit vector source producer substitution')
    return files,provenance,stages,graph,sha(archive)

def prepare(destination,context=None):
    files,provenance,stages,graph,archive_sha=compose_all(context)
    if destination.exists():raise ValueError('fresh destination required')
    assert all(Path(n).suffix.lower() not in {'.obj','.exe','.map','.lib','.dll','.com'} for n in files)
    destination.mkdir();source=destination/'sources';source.mkdir()
    rows={}
    for n,b in sorted(files.items()):
        p=source/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);os.utime(p,ns=(STAMP,STAMP));rows[n]=dict(sha256=sha(b),bytes=len(b),mtime_ns=STAMP,provenance=provenance[n])
    phases=[dict(name='compile_%02d_%s'%(r['ordinal'],Path(r['output']).stem),**r) for r in graph]+[dict(name='link',kind='tlink',flags=['@obj/th03/mainl.@l'],output='bin/th03/mainl.exe')]
    groups=[dict(group=i//5+1,phases=phases[i:i+5],native_seconds=90,cleanup_seconds=15,work_budget_seconds=900,factory_timeout_seconds=1000) for i in range(0,len(phases),5)]
    report=dict(schema='mainl-cold-source-proposal-v1',reference_revision=REV,archive_sha256=archive_sha,source_mtime_ns=STAMP,source_inventory=rows,stages=stages,object_graph=graph,groups=groups,project_objects=35,retained_project_objects=0,native_phases_per_round=36,rounds=2,native_execution_performed=False,exact_acceptance=False,historical_cold_proof_applies_to_current_sources=False,post_alignment_full_cold_build_pending=True,context=['Frozen reference headers, declarations, macros, root DATA/BSS and original scanner codestring remain explicitly contextual.','Generated th03/sprites/flake.asp is a declared 1281-byte CRLF input (1239 bytes with LF); this proposal does not claim regenerating it from BMP.','TC4 startup c0l.obj, EMU.LIB, MATHL.LIB and CL.LIB remain declared toolchain inputs; the proved private CRT substitution is separate and is not applied by this source-only project stage.'],verification=['Verify all 35 declared objects plus EXE/MAP absent in each fresh carrier before compiling.','Use the exact same source snapshot and timestamps for both rounds.','Compare all 35 object files plus EXE/MAP raw; do not normalize dependency timestamps.','Report DATA 0E3F:0849 and relocation ordering honestly; no packed/canonical acceptance follows from decoded equality.'])
    (destination/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['schema','project_objects','retained_project_objects','native_phases_per_round','native_execution_performed']}));print('sources',len(rows),'groups',len(groups),'manifest',sha((destination/'manifest.json').read_bytes()))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--context-directory',type=Path);a=p.parse_args();d=Path(a.output)
    if len(d.parts)!=3 or d.parts[0]!='.analysis' or not d.parts[1].startswith('mainl-cold-aggregate-proposal-'):raise ValueError('output must be inside a dedicated ignored proposal')
    prepare(d,a.context_directory)
