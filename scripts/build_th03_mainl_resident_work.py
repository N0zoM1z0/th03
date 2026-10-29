#!/usr/bin/env python3
"""Build six real bounded MAINL resident/math/text/joystick modules twice."""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import tomllib
import build_th03_mainl_work as build
from build_th03_mainl_resources_work import cold_context, need, sha

ROOT=Path(__file__).resolve().parents[1]
DRIVER='scripts/build_th03_mainl_resident_work.py'
REPORT='.analysis/work/mainl-resident-build.json'
BASE='src/mainl/root_tail/'
NEW=[BASE+n for n in ('resident_mcb.inc','respal_exist.inl','respal_create.inl','js_end.inl','resident_signature.inl','joystick_initialized.inl','joystick_uninitialized.inl')]
STATE=['src/mainl/display_hardware/palette_initialized.inl','src/mainl/display_hardware/palette_uninitialized.inl']
# local contributions correspond to complete original bodies, never target bytes.
PARTS={
 'context':[(BASE+'dos_keyclear.asm',0x6FE,6),(BASE+'iatan2.asm',0x175E,108)],
 'resident':[(BASE+'respal_exist.inl',0x276E,60),(BASE+'respal_set_palettes.asm',0x2820,48)],
 'create':[(BASE+'respal_create.inl',0x27AA,118)],
 'sound':[(BASE+'soundio.asm',0x1EF6,42),(BASE+'text_clear.asm',0x1F20,18),(BASE+'text_fillca.asm',0x1F32,56)],
 'joystick':[(BASE+'js_start.asm',0x2AAE,42),(BASE+'js_sense.asm',0x2AD8,61)],
 'end':[(BASE+'js_end.inl',0x17CA,6)],
}
DATA_EXT={'ResPalSeg':'word','PaletteTone':'word','Palettes':'byte','ResPalID':'byte','TextVramSeg':'word'}


def wrappers():
    result={}
    for name,parts in PARTS.items():
        raw=b'.386\r\n.model use16 large _TEXT\r\n'
        if name=='context':raw+=b'.stack 32\r\n'
        raw+=b'include ReC98.inc\r\n_DATA segment word public \'DATA\' use16\r\n'
        if name=='context':
            for n in (STATE[0],'libs/master.lib/tx[data].asm','libs/master.lib/atan8[data].asm'):
                raw+=('include '+n+'\r\n').encode()
        elif name=='resident':raw+=('include '+BASE+'resident_signature.inl\r\n').encode()
        elif name=='joystick':raw+=('include '+BASE+'joystick_initialized.inl\r\n').encode()
        for symbol,t in DATA_EXT.items():
            if name=='context' and symbol!='ResPalID':continue
            if name=='resident' and symbol=='ResPalID':continue
            raw+=('extrn '+symbol+':'+t+'\r\n').encode()
        raw+=b'_DATA ends\r\n'
        if name=='create':raw+=b'extrn RESPAL_EXIST:far\r\n'
        if name=='end':raw+=b'extrn DOS_KEYCLEAR:far\r\n'
        raw+=b'_TEXT segment word public \'CODE\' use16\r\nassume cs:_TEXT,ds:DGROUP\r\n'
        if name=='joystick':raw+=b'extrn SOUND_I:near,SOUND_O:near\r\n'
        if name=='sound':raw+=b'public SOUND_I,SOUND_O\r\n'
        for n,_,_ in parts:raw+=('include '+n+'\r\n').encode()
        raw+=b'_TEXT ends\r\n'
        if name in ('context','joystick'):
            src=STATE[1] if name=='context' else BASE+'joystick_uninitialized.inl'
            raw+=('_BSS segment word public \'BSS\' use16\r\ninclude '+src+'\r\n_BSS ends\r\nDGROUP group _DATA,_BSS\r\n').encode()
        else:raw+=b'DGROUP group _DATA\r\n'
        raw+=b'end\r\n';result[name]=raw
    return result


def response():
    return ('-c -s '+' '.join('probe\\rsm-'+n+'.obj' for n in PARTS)+',probe\\rsmini.exe,probe\\rsmini.map\r\n').encode()


def main():
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if os.nice(0)<10:os.nice(10-os.nice(0))
    cold,files,_=cold_context(ROOT);work=build.WORK
    config=tomllib.loads((ROOT/'config/toolchain.toml').read_text());prefix=ROOT/config['paths']['wine_prefix']
    env=dict(os.environ,DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(prefix),MSDOS_PATH=r'C:\TC4\BIN',TZ='UTC',LANG='C',LC_ALL='C')
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    dos=['/usr/bin/wine-stable',str(ROOT/config['paths']['msdos_player']),'-e','-x']
    source={n:(ROOT/n).read_bytes() for n in NEW+STATE}
    generated={f'probe/rsm-{n}.asm':b for n,b in wrappers().items()};generated['probe/rsmini.lnk']=response()
    report=dict(complete=False,source_acceptance=False,root_rebuilt=False,whole_product_cold_rebuilt=False,driver_sha256=sha((ROOT/DRIVER).read_bytes()),
        cold_report_sha256=sha(cold),source_sha256={n:sha(b) for n,b in source.items()},rounds=[],native_phases=[])
    save=lambda:(ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    def execute(argv,label):
        p=subprocess.run(argv,cwd=work,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
        (build.OUT/('resident-'+label+'.log')).write_bytes(p.stdout)
        report['native_phases'].append(dict(label=label,command=argv,returncode=p.returncode,log_sha256=sha(p.stdout)));save()
        need(p.returncode==0,label+':'+p.stdout.decode(errors='replace')[-1500:])
    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        temporary=[work/n for n in (*source,*generated)]+[work/f'probe/rsm-{n}.obj' for n in PARTS]+[work/f'probe/rsmini.{n}' for n in ('exe','map')]
        need(all(not p.exists() for p in temporary),'fresh bounded native inputs')
        try:
            (work/'probe').mkdir(exist_ok=True)
            for n,b in {**source,**generated}.items():(work/n).write_bytes(b);os.utime(work/n,(946684800,946684800))
            for name,b in wrappers().items():(build.OUT/f'resident-mini-{name}.asm').write_bytes(b)
            (build.OUT/'resident-mini.lnk').write_bytes(response())
            for number in (1,2):
                outputs={}
                for name in PARTS:
                    path=work/f'probe/rsm-{name}.obj';path.unlink(missing_ok=True)
                    execute(tasm+['/m','/mx','/kh32768','/t','/dGAME=3',rf'probe\rsm-{name}.asm',rf'probe\rsm-{name}.obj'],f'round{number}-{name}')
                    out=f'.analysis/work/resident-mini-round{number}-{name}.obj';b=path.read_bytes();(ROOT/out).write_bytes(b);outputs[name]=dict(path=out,bytes=len(b),sha256=sha(b))
                for ext in ('exe','map'):(work/f'probe/rsmini.{ext}').unlink(missing_ok=True)
                execute(dos+['tlink',r'@probe\rsmini.lnk'],f'round{number}-link')
                for ext in ('exe','map'):
                    b=(work/f'probe/rsmini.{ext}').read_bytes();out=f'.analysis/work/resident-mini-round{number}.{ext}';(ROOT/out).write_bytes(b);outputs[ext]=dict(path=out,bytes=len(b),sha256=sha(b))
                report['rounds'].append(dict(round=number,outputs=outputs));save()
                print('resident native round',number,'complete',flush=True)
            need({k:v['sha256'] for k,v in report['rounds'][0]['outputs'].items()}=={k:v['sha256'] for k,v in report['rounds'][1]['outputs'].items()},'complete raw repetition')
        finally:
            for p in temporary:p.unlink(missing_ok=True)
    cold_context(ROOT);report['complete']=True;save()


if __name__=='__main__':main()
