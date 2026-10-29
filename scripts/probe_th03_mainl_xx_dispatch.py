#!/usr/bin/env python3
"""Compile the recovered xx dispatch bank; mini-link only, with no exact credit."""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import tomllib
import build_th03_mainl_work as build
from build_th03_mainl_exception_work import compiler_context
from build_th03_mainl_resources_work import cold_context,need,sha
from lib.decoded_mainl_display_native import externs

ROOT=Path(__file__).resolve().parents[1]
DRIVER='scripts/probe_th03_mainl_xx_dispatch.py'
REPORT='.analysis/work/mainl-xx-dispatch-build.json'
SOURCE='src/mainl/crt/xx_dispatch.inl'
WRAPPER=(b'#include "xx_abi.h"\n'
    b'int near dtorCleanup(XXDtorTable far *,long,xx_registration_ptr,unsigned);\n'
    b'#include "xxbank.inl"\n')
HEADER='src/mainl/crt/xx_abi.h'
FLAGS=['-ml','-3-','-2-','-1-','-x','-O2-pg','-Os','-Z-','-xc','-Vs','-zC_TEXT','-IC:\\TC4\\INCLUDE','-S']
LINK=b'/x /m /c xxdisp.obj xxctx.obj,xxmini.exe,xxmini.map,,\r\n'


def sdk_inventory(root):
    c=tomllib.loads((root/'config/toolchain.toml').read_text())
    installed=root/c['paths']['tc40j_install']/'INCLUDE';active=root/c['paths']['wine_prefix']/'drive_c/TC4/INCLUDE'
    result={p.relative_to(installed).as_posix():sha(p.read_bytes()) for p in installed.rglob('*') if p.is_file()}
    observed={p.relative_to(active).as_posix():sha(p.read_bytes()) for p in active.rglob('*') if p.is_file()}
    need(result==observed and len(result)==64,'all64 available active SDK headers equal pinned installation')
    return result


def trap_context(imports):
    # Diagnostic providers are traps. The single ABI probe must reach none of
    # them; no implementation or behavior of an unresolved helper is modeled.
    lines=["_TEXT segment byte public 'CODE'",'assume cs:_TEXT']
    near_names=('@typeIDcaught','@dtorCleanup','@exceptionHandled','@initCatchArg','@callDestructor','@callMemberFunc')
    for name in imports:
        is_near=name.split('$')[0] in near_names
        lines += ['public '+name,name+' proc '+('near' if is_near else 'far'),'int 3','ret' if is_near else 'retf',name+' endp']
    return ('\n'.join(lines)+"\n_TEXT ends\n_STACK segment para stack 'STACK'\ndw 128 dup (?)\n_STACK ends\nend\n").encode()


def main(destruction=False):
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    cold_context(ROOT);compiler=compiler_context(ROOT);headers=sdk_inventory(ROOT)
    config=tomllib.loads((ROOT/'config/toolchain.toml').read_text());prefix=ROOT/config['paths']['wine_prefix'];work=build.WORK
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/config['paths']['msdos_player']),'-e','-x'];tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t']
    stem='xx-destruction' if destruction else 'xx-dispatch'
    sources={'xxbank.inl':SOURCE,'xx_abi.h':HEADER}
    wrapper=WRAPPER
    if destruction:
        sources['xxdtor.inl']='src/mainl/crt/xx_destroy.inl'
        wrapper=WRAPPER.replace(b'int near dtorCleanup',b'static int near dtorCleanup')+b'#include "xxdtor.inl"\n'
    report_path='.analysis/work/mainl-'+stem+'-build.json'
    report=dict(complete=False,source_acceptance=False,accepted_source_bytes=0,whole_product_linked=False,whole_product_cold_rebuilt=False,miniature_only=True,
        compiler=compiler,compiler_flags=FLAGS,source_sha256={n:sha((ROOT/n).read_bytes()) for n in sources.values()},driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        available_SDK_header_sha256=headers,wrapper_sha256=sha(wrapper),cold_report_sha256=sha((build.OUT/'mainl-build.json').read_bytes()),rounds=[],native_phases=[])
    save=lambda:(ROOT/report_path).write_text(json.dumps(report,indent=2)+'\n')
    def run(cmd,scratch,label):
        p=subprocess.run(cmd,cwd=scratch,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
        out=build.OUT/(stem+'-'+label+'.log');out.write_bytes(p.stdout)
        report['native_phases'].append(dict(label=label,command=cmd,returncode=p.returncode,log_sha256=sha(p.stdout)));save()
        need(p.returncode==0,label+': '+p.stdout.decode(errors='replace')[-1500:])
        if label.endswith('compile'):need(p.stdout.startswith(compiler['banner'].encode()+b'\r\n'),'actual scoped BCC banner')
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);scratch=work/'probe/xxdisp';need(not scratch.exists(),'fresh isolated dispatch candidate cwd');scratch.mkdir()
        try:
            for short,path in sources.items():
                raw=(ROOT/path).read_bytes();p=scratch/short;p.write_bytes(raw);os.utime(p,(946684800,946684800));(build.OUT/(stem+'-source-'+short)).write_bytes(raw)
            (scratch/'xxdisp.cpp').write_bytes(wrapper);os.utime(scratch/'xxdisp.cpp',(946684800,946684800));(build.OUT/(stem+'-wrapper.cpp')).write_bytes(wrapper)
            (scratch/'xxmini.lnk').write_bytes(LINK);(build.OUT/(stem+'-mini.lnk')).write_bytes(LINK)
            for number in (1,2):
                for suffix in ('asm','obj'):(scratch/('xxdisp.'+suffix)).unlink(missing_ok=True)
                for name in ('xxctx.asm','xxctx.obj','xxmini.exe','xxmini.map'):(scratch/name).unlink(missing_ok=True)
                run(dos+[r'C:\BC45\BCC.EXE',*FLAGS,'xxdisp.cpp'],scratch,f'round{number}-compile')
                os.utime(scratch/'xxdisp.asm',(946684800,946684800))
                run(tasm+(['/l'] if destruction else [])+['xxdisp.asm','xxdisp.obj'],scratch,f'round{number}-assemble')
                imports=externs((scratch/'xxdisp.obj').read_bytes());context=trap_context(imports)
                if destruction:
                    need(not any(n.startswith('@dtorCleanup$') for n in imports),'cleanup resolves inside the original xx TU')
                else:
                    need(len(imports)==7 and {n.split('$')[0] for n in imports}=={'@typeIDcaught','@dtorCleanup','@exceptionHandled','@initCatchArg','___call_unexpected','__Global_unwind','___JumpToCatch__'},'only the seven explicitly unresolved private/runtime interfaces')
                (scratch/'xxctx.asm').write_bytes(context);os.utime(scratch/'xxctx.asm',(946684800,946684800));(build.OUT/(stem+'-context.asm')).write_bytes(context)
                run(tasm+['xxctx.asm','xxctx.obj'],scratch,f'round{number}-context')
                run(dos+['tlink','@xxmini.lnk'],scratch,f'round{number}-mini-link')
                outputs={}
                names=[('asm','xxdisp.asm'),('obj','xxdisp.obj'),('context','xxctx.obj'),('exe','xxmini.exe'),('map','xxmini.map')]
                if destruction:names.append(('listing','xxdisp.lst'))
                for key,filename in names:
                    actual=next((p for p in scratch.iterdir() if p.name.lower()==filename),scratch/filename)
                    raw=actual.read_bytes();path=f'.analysis/work/{stem}-round{number}-'+filename;(ROOT/path).write_bytes(raw);outputs[key]=dict(path=path,bytes=len(raw),sha256=sha(raw))
                report['rounds'].append(dict(round=number,outputs=outputs,unresolved_imports=imports,context_sha256=sha(context)));save();print('Dispatch bank actual compiler/assembler/mini-link round',number,flush=True)
            # TASM's diagnostic listing includes wall-clock page headers. Bind
            # each complete listing, but compare the five native build outputs
            # without changing or normalizing any output bytes.
            need({k:m['sha256'] for k,m in report['rounds'][0]['outputs'].items() if k!='listing'}=={k:m['sha256'] for k,m in report['rounds'][1]['outputs'].items() if k!='listing'},'whole raw generated ASM/two-OBJ/mini-EXE/MAP repetition')
        finally:
            for p in scratch.iterdir():p.unlink()
            scratch.rmdir()
    cold_context(ROOT);need(compiler_context(ROOT)==compiler and sdk_inventory(ROOT)==headers,'unchanged compiler/runtime/all available SDK headers')
    report['complete']=True;save()


if __name__=='__main__':
    import sys
    main(destruction='--with-destruction' in sys.argv[1:])
