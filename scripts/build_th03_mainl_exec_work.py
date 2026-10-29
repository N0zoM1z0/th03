#!/usr/bin/env python3
"""Rebuild the complete DOS overlay executor, replace its normal library member, link twice."""
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
SOURCE='src/mainl/crt/exec.asm'
DRIVER='scripts/build_th03_mainl_exec_work.py'
REPORT='.analysis/work/mainl-exec-build.json'


def library_response(members):
    commands=[]
    for member in members:
        folder=r'probe\cexec' if member.name in ('exec','farheap') else 'owned' if member.name in build.CRT else 'vendor'
        commands.append('+'+folder+'\\'+member.name+'.obj')
    return build.response(r'probe\cexlib.lib /E',commands)


def link_response(files):
    raw=files['obj/th03/mainl.@l']
    for old,new in ((b'bin\\th03\\mainl.exe',b'probe\\cexec.exe'),(b'obj\\th03\\mainl.map',b'probe\\cexec.map'),(b' crt.lib',b' probe\\cexlib.lib')):
        need(raw.count(old)==1,'one selected output/library input');raw=raw.replace(old,new)
    return raw


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    cold,files,_=cold_context(ROOT);work=build.WORK;source=(ROOT/SOURCE).read_bytes()
    current=(work/'crt.lib').read_bytes();members=library_members(current);need(len(members)==893,'complete normal library')
    from lib.decoded_mainl_farheap_native import selected as farheap_pair
    reused,prior,prior_sha=farheap_pair(ROOT,work,files)
    reused_object=reused['obj']
    config=tomllib.loads((ROOT/'config/toolchain.toml').read_text());prefix=ROOT/config['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    dos=['/usr/bin/wine-stable',str(ROOT/config['paths']['msdos_player']),'-e','-x']
    report=dict(complete=False,source_acceptance=False,whole_product_cold_rebuilt=False,retained_project_objects=36,
        source_sha256=sha(source),driver_sha256=sha((ROOT/DRIVER).read_bytes()),cold_report_sha256=sha(cold),
        current_library_sha256=sha(current),reused_farheap=dict(source_sha256=prior['source_sha256'],build_report_sha256=prior_sha,object_sha256=sha(reused_object)),rounds=[],native_phases=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def execute(argv,cwd,label):
        p=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
        (build.OUT/('exec-'+label+'.log')).write_bytes(p.stdout)
        report['native_phases'].append(dict(label=label,command=argv,returncode=p.returncode,log_sha256=sha(p.stdout)));save()
        need(p.returncode==0,label+':'+p.stdout.decode(errors='replace')[-1500:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        scratch=work/'probe/cexec';need(not scratch.exists(),'fresh standalone source cwd')
        temporary=[work/'probe'/n for n in ('cexlib.rsp','cexec.lnk','cexlib.lib','cexlib.bak','cexec.exe','cexec.map')]
        need(all(not p.exists() for p in temporary),'fresh selected library/link paths')
        scratch.mkdir(parents=True)
        try:
            (scratch/'exec.asm').write_bytes(source);os.utime(scratch/'exec.asm',(946684800,946684800))
            (scratch/'farheap.obj').write_bytes(reused_object)
            (build.OUT/'exec-source.asm').write_bytes(source)
            libinput,link=library_response(members),link_response(files)
            (work/'probe/cexlib.rsp').write_bytes(libinput);(work/'probe/cexec.lnk').write_bytes(link)
            (build.OUT/'exec-library.rsp').write_bytes(libinput);(build.OUT/'exec-link.lnk').write_bytes(link)
            for number in (1,2):
                (scratch/'exec.obj').unlink(missing_ok=True)
                for p in temporary:
                    if p.suffix.lower() in ('.lib','.bak','.exe','.map'):p.unlink(missing_ok=True)
                execute(tasm+['/m','/mx','/kh32768','/t','exec.asm','exec.obj'],scratch,f'round{number}-assemble')
                obj=(scratch/'exec.obj').read_bytes();(build.OUT/f'exec-round{number}.obj').write_bytes(obj)
                execute(dos+['tlib',r'@probe\cexlib.rsp'],work,f'round{number}-library')
                library=(work/'probe/cexlib.lib').read_bytes();review=compare_members(members,library_members(library),{'exec':obj,'farheap':reused_object})
                execute(dos+['tlink',r'@probe\cexec.lnk'],work,f'round{number}-link')
                outputs={}
                for kind,b in [('obj',obj),('lib',library),('exe',(work/'probe/cexec.exe').read_bytes()),('map',(work/'probe/cexec.map').read_bytes())]:
                    path=f'.analysis/work/exec-round{number}.{kind}';(ROOT/path).write_bytes(b);outputs[kind]=dict(path=path,bytes=len(b),sha256=sha(b))
                need((work/'probe/cexec.exe').read_bytes()==(work/'bin/th03/mainl.target.exe').read_bytes(),'complete pinned Japanese decoded equality')
                need((work/'probe/cexec.map').read_bytes()==(work/'obj/th03/mainl.map').read_bytes(),'complete retained MAP equality')
                report['rounds'].append(dict(round=number,outputs=outputs,library=review));save();print('exec round',number,'whole EXE/MAP PASS',flush=True)
            need({k:v['sha256'] for k,v in report['rounds'][0]['outputs'].items()}=={k:v['sha256'] for k,v in report['rounds'][1]['outputs'].items()},'complete raw OBJ/LIB/EXE/MAP repeat')
        finally:
            for p in temporary:p.unlink(missing_ok=True)
            for p in scratch.iterdir():p.unlink()
            scratch.rmdir()
    cold_context(ROOT);report['complete']=True;save()


if __name__=='__main__':main()
