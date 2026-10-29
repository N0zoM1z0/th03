#!/usr/bin/env python3
"""Build the complete buffered stream/write bank and compose twenty-five CRT providers."""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import tomllib
import build_th03_mainl_work as build
from build_th03_mainl_resources_work import cold_context,need,sha
from lib.borland_library import library_members,compare_members

ROOT=Path(__file__).resolve().parents[1]
DRIVER='scripts/build_th03_mainl_stdio_work.py'
REPORT='.analysis/work/mainl-stdio-build.json'
SOURCES={n:'src/mainl/crt/'+n+'.asm' for n in ('fflush','flushall','fseek','setvbuf','write','writea','xfflush','setupio','lseek','isatty')}
LAYOUT_HEADER='src/mainl/crt/stdio_layout.inc'


def reused_pairs(root,work,files):
    from build_th03_mainl_path_work import reused_pairs as earlier_pairs
    from lib.decoded_mainl_path_native import selected as path_pair, SOURCES as PATH_SOURCES
    outputs,meta=earlier_pairs(root,work,files);v,r,digest=path_pair(root,work,files)
    for name,path in PATH_SOURCES.items():
        outputs[name]=v[name];meta[name]=dict(source_sha256=r['source_sha256'][path],build_report_sha256=digest,object_sha256=sha(v[name]))
    return outputs,meta


def library_response(members):
    commands=[]
    for member in members:
        folder=r'probe\stdioctx' if member.name in (*SOURCES,'farheap','exec','loadprog','doscmd','dosenv','fullpath','getdcwd','_pathops','dosgdriv') else 'owned' if member.name in build.CRT else 'vendor'
        commands.append('+'+folder+'\\'+member.name+'.obj')
    return build.response(r'probe\stdiolib.lib /E',commands)


def link_response(files):
    raw=files['obj/th03/mainl.@l']
    for old,new in ((b'bin\\th03\\mainl.exe',b'probe\\stdioctx.exe'),(b'obj\\th03\\mainl.map',b'probe\\stdioctx.map'),(b' crt.lib',b' probe\\stdiolib.lib')):
        need(raw.count(old)==1,'one selected output/library input');raw=raw.replace(old,new)
    return raw


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    cold,files,_=cold_context(ROOT);work=build.WORK;source={n:(ROOT/p).read_bytes() for n,p in SOURCES.items()}
    reused,reused_meta=reused_pairs(ROOT,work,files);current=(work/'crt.lib').read_bytes();members=library_members(current)
    config=tomllib.loads((ROOT/'config/toolchain.toml').read_text());prefix=ROOT/config['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    dos=['/usr/bin/wine-stable',str(ROOT/config['paths']['msdos_player']),'-e','-x']
    report=dict(complete=False,source_acceptance=False,whole_product_cold_rebuilt=False,retained_project_objects=36,
        source_sha256={p:sha(source[n]) for n,p in SOURCES.items()},driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        layout_header_sha256=sha((ROOT/LAYOUT_HEADER).read_bytes()),cold_report_sha256=sha(cold),current_library_sha256=sha(current),reused_sources=reused_meta,rounds=[],native_phases=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def execute(argv,cwd,label):
        p=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
        (build.OUT/('stdio-'+label+'.log')).write_bytes(p.stdout)
        report['native_phases'].append(dict(label=label,command=argv,returncode=p.returncode,log_sha256=sha(p.stdout)));save()
        need(p.returncode==0,label+':'+p.stdout.decode(errors='replace')[-1500:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        scratch=work/'probe/stdioctx';need(not scratch.exists(),'fresh standalone source cwd')
        temporary=[work/'probe'/n for n in ('stdiolib.rsp','stdioctx.lnk','stdiolib.lib','stdiolib.bak','stdioctx.exe','stdioctx.map')]
        need(all(not p.exists() for p in temporary),'fresh selected library/link paths');scratch.mkdir(parents=True)
        try:
            header=(ROOT/LAYOUT_HEADER).read_bytes();p=scratch/'stdio_layout.inc';p.write_bytes(header);os.utime(p,(946684800,946684800));(build.OUT/'stdio-layout.inc').write_bytes(header)
            for name,b in source.items():
                p=scratch/(name+'.asm');p.write_bytes(b);os.utime(p,(946684800,946684800));(build.OUT/('stdio-source-'+name+'.asm')).write_bytes(b)
            for name,b in reused.items():(scratch/(name+'.obj')).write_bytes(b)
            libinput,link=library_response(members),link_response(files)
            (work/'probe/stdiolib.rsp').write_bytes(libinput);(work/'probe/stdioctx.lnk').write_bytes(link)
            (build.OUT/'stdio-library.rsp').write_bytes(libinput);(build.OUT/'stdio-link.lnk').write_bytes(link)
            for number in (1,2):
                for p in temporary:
                    if p.suffix.lower() in ('.lib','.bak','.exe','.map'):p.unlink(missing_ok=True)
                outputs={};fresh={}
                for name in SOURCES:
                    p=scratch/(name+'.obj');p.unlink(missing_ok=True)
                    execute(tasm+['/m','/mx','/kh32768','/t',name+'.asm',name+'.obj'],scratch,f'round{number}-{name}')
                    b=p.read_bytes();fresh[name]=b;out=f'.analysis/work/stdio-round{number}-{name}.obj';(ROOT/out).write_bytes(b);outputs[name]=dict(path=out,bytes=len(b),sha256=sha(b))
                execute(dos+['tlib',r'@probe\stdiolib.rsp'],work,f'round{number}-library')
                library=(work/'probe/stdiolib.lib').read_bytes();review=compare_members(members,library_members(library),dict(reused,**fresh))
                execute(dos+['tlink',r'@probe\stdioctx.lnk'],work,f'round{number}-link')
                for kind,b in [('lib',library),('exe',(work/'probe/stdioctx.exe').read_bytes()),('map',(work/'probe/stdioctx.map').read_bytes())]:
                    out=f'.analysis/work/stdio-round{number}.{kind}';(ROOT/out).write_bytes(b);outputs[kind]=dict(path=out,bytes=len(b),sha256=sha(b))
                need((work/'probe/stdioctx.exe').read_bytes()==(work/'bin/th03/mainl.target.exe').read_bytes(),'complete pinned Japanese decoded equality')
                need((work/'probe/stdioctx.map').read_bytes()==(work/'obj/th03/mainl.map').read_bytes(),'complete retained MAP equality')
                report['rounds'].append(dict(round=number,outputs=outputs,library=review));save();print('Buffered stream bank round',number,'whole EXE/MAP PASS',flush=True)
            need({k:v['sha256'] for k,v in report['rounds'][0]['outputs'].items()}=={k:v['sha256'] for k,v in report['rounds'][1]['outputs'].items()},'complete raw ten-OBJ/LIB/EXE/MAP repeat')
        finally:
            for p in temporary:p.unlink(missing_ok=True)
            for p in scratch.iterdir():p.unlink()
            scratch.rmdir()
    cold_context(ROOT);report['complete']=True;save()


if __name__=='__main__':main()
