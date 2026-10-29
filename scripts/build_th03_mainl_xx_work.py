#!/usr/bin/env python3
"""Compile xx under its real module name and link the retained MAINL project."""
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tomllib
import build_th03_mainl_work as build
import probe_th03_mainl_xx_dispatch as miniature
from probe_th03_mainl_xx_rtti import NAMES,UNIT,wrapper
from build_th03_mainl_exception_work import compiler_context
from build_th03_mainl_resources_work import cold_context,need,sha
from lib.borland_library import library_members,compare_members,object_program_records
from lib.decoded_mainl_acceptance import proof_inputs

ROOT=Path(__file__).resolve().parents[1]
DRIVER='scripts/build_th03_mainl_xx_work.py'
REPORT='.analysis/work/mainl-xx-product-build.json'
ACCEPTED_SHA='de7276df0d534f40e8bb1ab84f2d054688fd1960bf8cdf92d4a8108d7b34a551'
BASE_BUILD='.analysis/work/mainl-exception-native-build.json'
BASE_REVIEW='.analysis/work/mainl-exception-native-review.json'
MINI_BUILD='.analysis/work/mainl-xx-rtti-build.json'
MINI_REVIEW='.analysis/work/mainl-xx-rtti-review.json'
SOURCES=dict(NAMES,**{'xx_abi.h':miniature.HEADER,'xx.cpp':UNIT})
SUPPORT=['scripts/probe_th03_mainl_xx_dispatch.py','scripts/probe_th03_mainl_xx_rtti.py',
    'scripts/review_th03_mainl_xx_rtti.py','scripts/lib/decoded_mainl_xx_rtti_probe.py',
    'scripts/lib/decoded_mainl_xx_throw_probe.py']


def retained_pair(root,path,stem):
    raw=(root/path).read_bytes();report=json.loads(raw);vectors=[]
    need(report['complete'] and report['compiler']==compiler_context(root),
        'retained complete native pair with current scoped compiler')
    need(report['source_sha256']=={p:sha((root/p).read_bytes()) for p in report['source_sha256']},
        'unchanged retained source graph')
    need(report['driver_sha256']==sha((root/('scripts/build_th03_mainl_exception_work.py' if stem=='exception-native' else miniature.DRIVER)).read_bytes()),'unchanged retained native driver')
    for key in ('profile_driver_sha256','probe_support_sha256'):
        if key in report:need(report[key]=={p:sha((root/p).read_bytes()) for p in report[key]},'current retained '+key)
    for row in report['rounds']:
        vector={}
        for kind,meta in row['outputs'].items():
            data=(root/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),'retained complete raw output')
            vector[kind]=data
        vectors.append(vector)
    need(len(vectors)==2 and {k:v for k,v in vectors[0].items() if k!='listing'}=={k:v for k,v in vectors[1].items() if k!='listing'},'unchanged full retained native pair,no ancestor runtime replay')
    for phase in report['native_phases']:
        need(sha((root/('.analysis/work/'+stem+'-'+phase['label']+'.log')).read_bytes())==phase['log_sha256'],'actual retained native phase log')
    return report,vectors[0],sha(raw)


def baseline(root):
    cold,files,_=cold_context(root)
    publication_raw=(root/'config/mainl_work/scoped_acceptance.json').read_bytes();publication=json.loads(publication_raw)
    need(sha(publication_raw)==ACCEPTED_SHA and publication['proof_inputs']==proof_inputs(root) and len(publication['audit']['scope']['owners'])==211,'unchanged accepted211-owner publication and verifier inputs')
    old,vector,digest=retained_pair(root,BASE_BUILD,'exception-native')
    review_raw=(root/BASE_REVIEW).read_bytes();review=json.loads(review_raw)
    need(review['selected_build_report_sha256']==digest and review['whole_EXE_MAP_equal'] and review['full_raw_vector_repeated'] and review['source_CRT_providers_in_selected_library']==28,'current reviewed normal28-provider pair')
    need(vector['exe']==(build.WORK/'bin/th03/mainl.target.exe').read_bytes() and vector['map']==(build.WORK/'obj/th03/mainl.map').read_bytes(),'actual baseline EXE/MAP remain target equal')
    mini,mv,mdigest=retained_pair(root,MINI_BUILD,'xx-rtti')
    mr_raw=(root/MINI_REVIEW).read_bytes();mr=json.loads(mr_raw)
    need(mr['complete'] and mr['selected_build_report_sha256']==mdigest and mr['review_driver_sha256']==sha((root/'scripts/review_th03_mainl_xx_rtti.py').read_bytes()) and mr['whole_xx_source_graph_present'] and not mr['source_acceptance'],'current whole source graph miniature review')
    members=library_members(vector['lib']);need(len(members)==893 and sum(m.name=='xx' for m in members)==1,'normal893-member library with original xx position')
    return dict(accepted_publication_sha256=ACCEPTED_SHA,cold_report_sha256=sha(cold),
        library_build_report_sha256=digest,library_review_sha256=sha(review_raw),
        library_sha256=sha(vector['lib']),miniature_build_report_sha256=mdigest,
        miniature_review_sha256=sha(mr_raw)),files,vector['lib'],members,mv


def link_response(files):
    raw=files['obj/th03/mainl.@l']
    for old,new in [(b'bin\\th03\\mainl.exe',b'probe\\xxwhole\\xxfull.exe'),
                    (b'obj\\th03\\mainl.map',b'probe\\xxwhole\\xxfull.map'),
                    (b' crt.lib',b' probe\\xxwhole\\xxcrt.lib'),
                    (b'c0l.obj',b'C:\\TC4\\LIB\\C0L.OBJ'),
                    (b'emu.lib',b'C:\\TC4\\LIB\\EMU.LIB'),
                    (b'mathl.lib',b'C:\\TC4\\LIB\\MATHL.LIB')]:
        need(raw.count(old)==1,'one actual whole-product output/library position');raw=raw.replace(old,new)
    return raw


def library_response(members):
    return build.response(r'probe\xxwhole\xxcrt.lib /E',
        ['+probe\\xxwhole\\'+m.name+'.obj' for m in members])


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    before,files,library,members,_=baseline(ROOT);compiler=compiler_context(ROOT)
    headers=miniature.sdk_inventory(ROOT);unit=wrapper(b'')
    config=tomllib.loads((ROOT/'config/toolchain.toml').read_text());prefix=ROOT/config['paths']['wine_prefix'];work=build.WORK
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\BC45;C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    dos=['/usr/bin/wine-stable',str(ROOT/config['paths']['msdos_player']),'-e','-x']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t']
    original_link=files['obj/th03/mainl.@l']
    binary_inputs=re.findall(r'(?i)\b(?:[\w@]+\\)*[\w@]+\.obj',original_link.decode())+['emu.lib','mathl.lib']
    need(len(binary_inputs)==39 and len(set(binary_inputs))==39,'36 retained project objects plus real startup and two libraries')
    preserved={}
    for name in binary_inputs:
        path=work/name.replace('\\','/')
        if not path.exists():
            need(name in ('c0l.obj','emu.lib','mathl.lib'),'only actual SDK startup/libraries use pinned search paths')
            path=prefix/'drive_c/TC4/LIB'/name.upper()
        preserved[path.relative_to(ROOT).as_posix()]=sha(path.read_bytes())
    report=dict(complete=False,source_acceptance=False,accepted_source_bytes=0,
        whole_product_linked=False,whole_product_cold_rebuilt=False,retained_project_objects=36,
        diagnostic_candidate=True,compiler=compiler,compiler_flags=miniature.FLAGS,
        available_SDK_header_sha256=headers,source_sha256={p:sha((ROOT/p).read_bytes()) for p in SOURCES.values()},
        driver_sha256=sha((ROOT/DRIVER).read_bytes()),support_sha256={p:sha((ROOT/p).read_bytes()) for p in SUPPORT},
        baseline=before,retained_binary_inputs_sha256=preserved,wrapper_sha256=sha(unit),native_phases=[],rounds=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def execute(argv,cwd,label):
        result=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (build.OUT/('xx-product-'+label+'.log')).write_bytes(result.stdout)
        report['native_phases'].append(dict(label=label,command=argv,returncode=result.returncode,log_sha256=sha(result.stdout)));save()
        need(result.returncode==0,label+': '+result.stdout.decode(errors='replace')[-1500:])
        if label.endswith('compile'):need(result.stdout.startswith(compiler['banner'].encode()+b'\r\n'),'actual scoped compiler banner')
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        scratch=work/'probe/xxwhole';need(not scratch.exists(),'fresh isolated whole xx native working directory');scratch.mkdir()
        try:
            (scratch/'base.lib').write_bytes(library)
            extract=build.response('base.lib',['*'+m.name for m in members])
            (scratch/'extract.rsp').write_bytes(extract);(build.OUT/'xx-product-extract.rsp').write_bytes(extract)
            execute(dos+['tlib','@extract.rsp'],scratch,'extract-current-library')
            extracted={p.stem.casefold():p for p in scratch.iterdir() if p.suffix.lower()=='.obj'}
            need(set(extracted)=={m.name.casefold() for m in members},'all893 actual native extracted objects')
            for member in members:
                current=extracted[member.name.casefold()];destination=scratch/(member.name+'.obj')
                need(object_program_records(current.read_bytes())==member.program_records,'unchanged extracted native member: '+member.name)
                if current!=destination:current.rename(destination)
            for short,path in SOURCES.items():
                raw=unit if short=='xx.cpp' else (ROOT/path).read_bytes()
                (scratch/short).write_bytes(raw);os.utime(scratch/short,(946684800,946684800))
                (build.OUT/('xx-product-source-'+short)).write_bytes(raw)
            (build.OUT/'xx-product-maintained-xx.cpp').write_bytes((ROOT/UNIT).read_bytes())
            libinput,link=library_response(members),link_response(files)
            (scratch/'library.rsp').write_bytes(libinput);(scratch/'link.lnk').write_bytes(link)
            (build.OUT/'xx-product-library.rsp').write_bytes(libinput);(build.OUT/'xx-product-link.lnk').write_bytes(link)
            for number in (1,2):
                for name in ('xx.obj','xx.asm','xx.lst','xxcrt.lib','xxcrt.bak','xxfull.exe','xxfull.map'):(scratch/name).unlink(missing_ok=True)
                execute(dos+[r'C:\BC45\BCC.EXE',*miniature.FLAGS,'xx.cpp'],scratch,f'round{number}-compile')
                os.utime(scratch/'xx.asm',(946684800,946684800))
                execute(tasm+['/l','xx.asm','xx.obj'],scratch,f'round{number}-assemble')
                execute(dos+['tlib',r'@probe\xxwhole\library.rsp'],work,f'round{number}-library')
                review=compare_members(members,library_members((scratch/'xxcrt.lib').read_bytes()),{'xx':(scratch/'xx.obj').read_bytes()})
                execute(dos+['tlink',r'@probe\xxwhole\link.lnk'],work,f'round{number}-link')
                outputs={}
                for kind,name in [('asm','xx.asm'),('obj','xx.obj'),('listing','xx.lst'),('lib','xxcrt.lib'),('exe','xxfull.exe'),('map','xxfull.map')]:
                    actual=next(p for p in scratch.iterdir() if p.name.lower()==name)
                    data=actual.read_bytes();out=f'.analysis/work/xx-product-round{number}-'+name;(ROOT/out).write_bytes(data)
                    outputs[kind]=dict(path=out,bytes=len(data),sha256=sha(data))
                report['rounds'].append(dict(round=number,outputs=outputs,library=review));save()
                print('Whole MAINL xx source compile/assemble/normal-library/link round',number,flush=True)
            need({k:v['sha256'] for k,v in report['rounds'][0]['outputs'].items() if k!='listing'}=={k:v['sha256'] for k,v in report['rounds'][1]['outputs'].items() if k!='listing'},'whole raw ASM/OBJ/LIB/EXE/MAP repeat;unmodified listings retained separately')
        finally:shutil.rmtree(scratch)
    after,_,_,_,_=baseline(ROOT)
    need(after==before and preserved=={p:sha((ROOT/p).read_bytes()) for p in preserved} and compiler_context(ROOT)==compiler and miniature.sdk_inventory(ROOT)==headers,'baseline,all39 retained binary inputs,compiler and SDK unchanged')
    report.update(complete=True,whole_product_linked=True);save()


if __name__=='__main__':main()
