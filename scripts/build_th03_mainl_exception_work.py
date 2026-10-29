#!/usr/bin/env python3
"""Build natural allocation/exception C++ with the scoped optimizing compiler."""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import tomllib
import build_th03_mainl_work as build
from build_th03_mainl_resources_work import cold_context,need,sha
from lib.borland_library import library_members,compare_members
from lib.omf import describe_omf

ROOT=Path(__file__).resolve().parents[1]
DRIVER='scripts/build_th03_mainl_exception_work.py'
REPORT='.analysis/work/mainl-exception-native-build.json'
SOURCES={n:'src/mainl/crt/'+n+'.cpp' for n in ('new','xalloc','xmsg')}
FLAGS=['-c','-ml','-3-','-2-','-1-','-x','-O1','-xc','-Vs','-zC_TEXT','-IC:\\TC4\\INCLUDE']

TOOLCHAIN='config/mainl_work/exception_toolchain.toml'


def compiler_context(root):
    raw=(root/TOOLCHAIN).read_bytes();c=tomllib.loads(raw.decode());surfaces=[]
    need(c['provenance']=='candidate-local-attested','claim-scoped compiler provenance')
    for entry in c['surfaces']:
        a=(root/entry['installed']).read_bytes();b=(root/entry['active']).read_bytes()
        need(a==b and len(a)==entry['bytes'] and sha(a)==entry['sha256'],'scoped optimizing compiler/runtime identity: '+entry['name'])
        surfaces.append(dict(entry))
    active=(root/c['surfaces'][0]['active']).parent
    need({p.name for p in active.iterdir()}=={'BCC.EXE','RTM.EXE','DPMI16BI.OVL'},'isolated compiler/runtime directory without ambient config')
    return dict(manifest_sha256=sha(raw),surfaces=surfaces,banner=c['banner'],translator=c['translator'])


def reused_pairs(root,work,files):
    from build_th03_mainl_stdio_work import reused_pairs as earlier_pairs
    from lib.decoded_mainl_stdio_native import selected as stdio_pair, SOURCES as STDIO_SOURCES
    outputs,meta=earlier_pairs(root,work,files);v,r,digest=stdio_pair(root,work,files)
    for name,path in STDIO_SOURCES.items():
        outputs[name]=v[name];meta[name]=dict(source_sha256=r['source_sha256'][path],build_report_sha256=digest,object_sha256=sha(v[name]))
    return outputs,meta


def library_response(members):
    commands=[]
    for member in members:
        folder=r'probe\excnat' if member.name in (*SOURCES,'farheap','exec','loadprog','doscmd','dosenv','fullpath','getdcwd','_pathops','dosgdriv','fflush','flushall','fseek','setvbuf','write','writea','xfflush','setupio','lseek','isatty') else 'owned' if member.name in build.CRT else 'vendor'
        commands.append('+'+folder+'\\'+member.name+'.obj')
    return build.response(r'probe\excnlib.lib /E',commands)


def link_response(files):
    raw=files['obj/th03/mainl.@l']
    for old,new in ((b'bin\\th03\\mainl.exe',b'probe\\excnat.exe'),(b'obj\\th03\\mainl.map',b'probe\\excnat.map'),(b' crt.lib',b' probe\\excnlib.lib')):
        need(raw.count(old)==1,'one selected output/library input');raw=raw.replace(old,new)
    return raw


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    cold,files,_=cold_context(ROOT);compiler=compiler_context(ROOT);work=build.WORK;source={n:(ROOT/p).read_bytes() for n,p in SOURCES.items()}
    reused,reused_meta=reused_pairs(ROOT,work,files);current=(work/'crt.lib').read_bytes();members=library_members(current)
    config=tomllib.loads((ROOT/'config/toolchain.toml').read_text());prefix=ROOT/config['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/config['paths']['msdos_player']),'-e','-x']
    report=dict(complete=False,source_acceptance=False,accepted_source_bytes=0,compiler_flags=FLAGS,whole_product_cold_rebuilt=False,retained_project_objects=36,
        compiler=compiler,vendor_header_sha256={},source_sha256={p:sha(source[n]) for n,p in SOURCES.items()},driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        cold_report_sha256=sha(cold),current_library_sha256=sha(current),reused_sources=reused_meta,rounds=[],native_phases=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def execute(argv,cwd,label):
        p=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
        (build.OUT/('exception-native-'+label+'.log')).write_bytes(p.stdout)
        report['native_phases'].append(dict(label=label,command=argv,returncode=p.returncode,log_sha256=sha(p.stdout)));save()
        need(p.returncode==0,label+':'+p.stdout.decode(errors='replace')[-1500:])
        if label.endswith(tuple(SOURCES)):
            need(p.stdout.startswith(compiler['banner'].encode()+b'\r\n'),'actual optimizing compiler banner')
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        scratch=work/'probe/excnat';need(not scratch.exists(),'fresh standalone source cwd')
        temporary=[work/'probe'/n for n in ('excnlib.rsp','excnat.lnk','excnlib.lib','excnlib.bak','excnat.exe','excnat.map')]
        need(all(not p.exists() for p in temporary),'fresh selected library/link paths');scratch.mkdir(parents=True)
        try:
            for name,b in source.items():
                p=scratch/(name+'.cpp');p.write_bytes(b);os.utime(p,(946684800,946684800));(build.OUT/('exception-native-source-'+name+'.cpp')).write_bytes(b)
            for name,b in reused.items():(scratch/(name+'.obj')).write_bytes(b)
            libinput,link=library_response(members),link_response(files)
            (work/'probe/excnlib.rsp').write_bytes(libinput);(work/'probe/excnat.lnk').write_bytes(link)
            (build.OUT/'exception-native-library.rsp').write_bytes(libinput);(build.OUT/'exception-native-link.lnk').write_bytes(link)
            for number in (1,2):
                for p in temporary:
                    if p.suffix.lower() in ('.lib','.bak','.exe','.map'):p.unlink(missing_ok=True)
                outputs={};fresh={}
                for name in SOURCES:
                    p=scratch/(name+'.obj');p.unlink(missing_ok=True)
                    execute(dos+[r'C:\BC45\BCC.EXE',*FLAGS,name+'.cpp'],scratch,f'round{number}-{name}')
                    b=p.read_bytes()
                    for dependency in describe_omf(b)['dependency_paths']:
                        dependency=dependency.replace(chr(92),'/')
                        if dependency.upper().startswith('C:/TC4/INCLUDE/'):
                            filename=dependency.rsplit('/',1)[1].upper();active=prefix/'drive_c/TC4/INCLUDE'/filename;installed=ROOT/config['paths']['tc40j_install']/'INCLUDE'/filename
                            raw=active.read_bytes();need(raw==installed.read_bytes(),'actual consumed SDK header identity');digest=sha(raw)
                            need(report['vendor_header_sha256'].get(dependency,digest)==digest,'stable consumed SDK header across rounds');report['vendor_header_sha256'][dependency]=digest
                        else:need(dependency==name+'.cpp','undeclared compiler source dependency')
                    fresh[name]=b;out=f'.analysis/work/exception-native-round{number}-{name}.obj';(ROOT/out).write_bytes(b);outputs[name]=dict(path=out,bytes=len(b),sha256=sha(b))
                execute(dos+['tlib',r'@probe\excnlib.rsp'],work,f'round{number}-library')
                library=(work/'probe/excnlib.lib').read_bytes();review=compare_members(members,library_members(library),dict(reused,**fresh))
                execute(dos+['tlink',r'@probe\excnat.lnk'],work,f'round{number}-link')
                for kind,b in [('lib',library),('exe',(work/'probe/excnat.exe').read_bytes()),('map',(work/'probe/excnat.map').read_bytes())]:
                    out=f'.analysis/work/exception-native-round{number}.{kind}';(ROOT/out).write_bytes(b);outputs[kind]=dict(path=out,bytes=len(b),sha256=sha(b))
                equal_exe=(work/'probe/excnat.exe').read_bytes()==(work/'bin/th03/mainl.target.exe').read_bytes()
                equal_map=(work/'probe/excnat.map').read_bytes()==(work/'obj/th03/mainl.map').read_bytes()
                need(equal_exe and equal_map,'complete pinned Japanese decoded EXE and retained MAP equality');report['whole_EXE_equal']=equal_exe;report['whole_MAP_equal']=equal_map
                report['rounds'].append(dict(round=number,outputs=outputs,library=review));save();print('Natural C++ round',number,'whole EXE/MAP equal:',equal_exe,equal_map,flush=True)
            need({k:v['sha256'] for k,v in report['rounds'][0]['outputs'].items()}=={k:v['sha256'] for k,v in report['rounds'][1]['outputs'].items()},'complete raw three-OBJ/LIB/EXE/MAP repeat')
        finally:
            for p in temporary:p.unlink(missing_ok=True)
            for p in scratch.iterdir():p.unlink()
            scratch.rmdir()
    cold_context(ROOT);need(compiler_context(ROOT)==compiler,'unchanged scoped compiler');report['complete']=True;save()


if __name__=='__main__':main()
