#!/usr/bin/env python3
"""Rebuild MAINL root with maintained palette/vsync/gaiji state; reuse unchanged context."""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import tomllib

import build_th03_mainl_work as build
from build_th03_mainl_resources_work import cold_context, need, sha, native_records, public_records
from lib.omf import describe_omf, parse_omf

ROOT = Path(__file__).resolve().parents[1]
WRAPPER, OBJECT = 'th03_mainl.asm', 'obj/th03/mainl.obj'
DRIVER, REPORT = 'scripts/build_th03_mainl_display_work.py', '.analysis/work/mainl-display-build.json'
STATE = (
    ('libs/master.lib/pal[data].asm','src/mainl/display_hardware/palette_initialized.inl'),
    ('libs/master.lib/pal[bss].asm','src/mainl/display_hardware/palette_uninitialized.inl'),
    ('src/mainl/display_hardware/vsync_data.asm','src/mainl/display_hardware/vsync_initialized.inl'),
    ('libs/master.lib/vs[bss].asm','src/mainl/display_hardware/vsync_counters.inl'),
    ('libs/master.lib/vsync[bss].asm','src/mainl/display_hardware/vsync_delay.inl'),
    ('libs/master.lib/gaiji_backup[data].asm','src/mainl/display_hardware/gaiji_backup_state.inl'),
    ('libs/master.lib/gaiji_entry_bfnt[data].asm','src/mainl/display_hardware/gaiji_dimensions.inl'),
    ('src/mainl/display_hardware/palette_show.asm','src/mainl/display_hardware/palette_show.inl'),
)
NATURAL = {n:'src/mainl/display_hardware/'+n+'.inl' for n in
           ('palette_black_in','palette_black_out','vsync','gaiji_backup','gaiji_entry_bfnt','palette_show')}
CONTEXT = [
 ('memory/heap.inl',0x210A,628),('resources/smem_release.asm',0x1EAA,16),('resources/smem_wget.asm',0x1EBA,60),
 ('display_hardware/graph_extmode.asm',0xF02,86),('display_hardware/dos_setvect.asm',0x704,32),('resources/dos_close.asm',0xA98,22),
 ('resources/dos_ropen.asm',0xAAE,26),('resources/bfnt_header_read.asm',0x3D6,60),('resources/bfnt_extend_header_skip.asm',0x3B4,34),
 ('display_hardware/gaiji_read.asm',0xD48,108),('display_hardware/gaiji_write.asm',0xDB4,112),
 ('display_hardware/palette_show.inl',0x17D0,266),('display_hardware/vsync_wait.asm',0x2064,38),
 ('display_hardware/palette_entry_rgb.asm',0x1A68,66),('display_hardware/palette_white_in.asm',0x208A,64),('display_hardware/palette_white_out.asm',0x20CA,64),
]
SUBJECTS = {'vsync':(0x1F6A,250,['DOS_SETVECT'],['GRAPH_EXTMODE']),
            'palette_black_in':(0x536,68,['VSYNC_WAIT','PALETTE_SHOW'],[]),
            'palette_black_out':(0x57A,62,['VSYNC_WAIT','PALETTE_SHOW'],[]),
            'gaiji_backup':(0xC72,64,['HMEM_ALLOC','HMEM_FREE'],['GAIJI_READ_ALL','GAIJI_WRITE_ALL']),
            'gaiji_entry_bfnt':(0xCB2,150,['FONTFILE_OPEN','SMEM_WGET','BFNT_HEADER_READ','BFNT_EXTEND_HEADER_SKIP','SMEM_RELEASE'],['GAIJI_WRITE_ALL'])}
CONTEXT_STATE = ['src/mainl/memory/heap_initialized.inl','src/mainl/memory/heap_uninitialized.inl']
DATA_EXTERN = {'vsync_Proc':'dword','vsync_Delay':'word','vsync_OldMask':'byte','vsync_Count1':'word','vsync_Count2':'word',
               'vsync_OldVect':'dword','vsync_delay_count':'word','PaletteTone':'word'}



def wrapper(files):
    raw = files[WRAPPER]
    for index,(old, new) in enumerate(STATE):
        if index == 2:
            continue  # Legacy DATA090 alignment stays contextual; real state7 is compiled in the independent TU.
        marker = ('include ' + old).encode()
        need(raw.count(marker) == 1, 'one state provider at original source position')
        raw = raw.replace(marker, ('include ' + new).encode())
    return raw


def response(files):
    raw = files['obj/th03/mainl.@l']
    for a, b in ((b'obj\\th03\\mainl.obj', b'probe\\dpyroot.obj'),
                 (b'bin\\th03\\mainl.exe', b'probe\\dpyroot.exe'),
                 (b'obj\\th03\\mainl.map', b'probe\\dpyroot.map')):
        need(raw.count(a) == 1, 'one affected root at original link position')
        raw = raw.replace(a, b)
    return raw


def mini_wrappers():
    prefix = b'.386\r\n.model use16 large _TEXT\r\n'
    context = prefix+b'.stack 32\r\ninclude ReC98.inc\r\n_TEXT segment word public \'CODE\' use16\r\nassume cs:_TEXT,ds:DGROUP\r\n'
    context += b''.join(('include src/mainl/'+n+'\r\n').encode() for n,_,_ in CONTEXT)+b'_TEXT ends\r\n'
    context += b'_DATA segment word public \'DATA\' use16\r\n'
    context += b''.join(('include '+n+'\r\n').encode() for n in (STATE[0][1],STATE[2][1],
                 'src/mainl/memory/heap_initialized.inl','libs/master.lib/tx[data].asm','libs/master.lib/bfnt_id[data].asm','libs/master.lib/dos_ropen[data].asm'))
    context += b'_DATA ends\r\n_BSS segment word public \'BSS\' use16\r\n'
    context += b''.join(('include '+n+'\r\n').encode() for n in (STATE[1][1],STATE[3][1],STATE[4][1],'src/mainl/memory/heap_uninitialized.inl'))
    context += b'_BSS ends\r\nDGROUP group _DATA,_BSS\r\nend\r\n'
    result = {'context':context}
    for name,(_,_,outside,inside) in SUBJECTS.items():
        raw = prefix+b'include ReC98.inc\r\n_DATA segment word public \'DATA\' use16\r\n'
        raw += b''.join(('extrn '+n+':'+t+'\r\n').encode() for n,t in DATA_EXTERN.items())
        if name == 'gaiji_backup':raw += ('include '+STATE[5][1]+'\r\n').encode()
        if name == 'gaiji_entry_bfnt':raw += ('include '+STATE[6][1]+'\r\n').encode()
        raw += b'_DATA ends\r\n'+('extrn '+','.join(n+':far' for n in outside)+'\r\n').encode()
        raw += b'_TEXT segment word public \'CODE\' use16\r\nassume cs:_TEXT,ds:DGROUP\r\n'
        if inside:raw += ('extrn '+','.join(n+':far' for n in inside)+'\r\n').encode()
        raw += ('include '+NATURAL[name]+'\r\n_TEXT ends\r\nend\r\n').encode()
        result[name] = raw
    return result


def mini_response():
    return ('-c -s '+' '.join('probe\\dpy-'+n+'.obj' for n in mini_wrappers())+',probe\\dpymini.exe,probe\\dpymini.map\r\n').encode()


def literal_fields(raw):
    result,block = [],None
    for record in parse_omf(raw):
        if record.name == 'LEDATA':
            block = (record.data[0],int.from_bytes(record.data[1:3],'little'),record.data[3:])
        elif record.name == 'FIXUPP':
            data,at = record.data,0
            def index():
                nonlocal at
                value = data[at];at += 1
                if value & 128:
                    value = ((value&127)<<8)|data[at];at += 1
                return value
            while at < len(data):
                loc,low,method = data[at:at+3];at += 3
                need(loc&128 and method&0x8c == 4 and (method>>4)&7 in (0,1,5) and method&3 in (0,1,2),'explicit unthreaded native fields')
                frame_method = (method>>4)&7
                frame = index() if frame_method in (0,1) else None
                target = index();offset = ((loc&3)<<8)|low;kind = (loc>>2)&15
                width = {1:2,2:2,3:4}[kind]
                need(block is not None and offset+width <= len(block[2]),'complete native field in initializer block')
                result.append(dict(segment=block[0],site=block[1]+offset,location_type=kind,width=width,
                    segment_relative=bool(loc&64),frame_method=frame_method,frame=frame,target_method=method&3,target=target,
                    addend=int.from_bytes(block[2][offset:offset+width],'little')))
    return result


def payload(raw):
    result = {}
    for r in parse_omf(raw):
        if r.name == 'LEDATA':
            seg,off = r.data[0],int.from_bytes(r.data[1:3],'little')
            for n,value in enumerate(r.data[3:]):
                need((seg,off+n) not in result,'nonoverlapping complete native initializer bytes')
                result[seg,off+n] = value
    return result


def equivalent_root(raw,baseline):
    # Removing ORG changes TASM's LEDATA/FIXUPP packet boundaries. Preserve every
    # emitted byte and the complete literal field stream at absolute object sites.
    metadata = lambda b:[(r.name,r.data) for r in parse_omf(b) if r.name not in ('COMENT','PUBDEF','LEDATA','FIXUPP')]
    return metadata(raw) == metadata(baseline) and payload(raw) == payload(baseline) and literal_fields(raw) == literal_fields(baseline) and public_records(raw) == public_records(baseline)


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    cold_raw, files, _ = cold_context(ROOT)
    sources = {n: (ROOT/n).read_bytes() for n in dict.fromkeys([n for _,n in STATE]+list(NATURAL.values())+CONTEXT_STATE)}
    generated, link = wrapper(files), response(files)
    config = tomllib.loads((ROOT / 'config/toolchain.toml').read_text())
    prefix, work = ROOT / config['paths']['wine_prefix'], build.WORK
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', WINEPREFIX=str(prefix),
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    dos = ['/usr/bin/wine-stable', str(ROOT / config['paths']['msdos_player']), '-e', '-x']
    tasm = ['/usr/bin/wine-stable', str(prefix / 'drive_c/TASM50/bin/TASM32.EXE')]
    report = dict(complete=False, source_acceptance=False, whole_product_cold_rebuilt=False, context_project_objects=35,
        driver_sha256=sha((ROOT / DRIVER).read_bytes()), cold_report_sha256=sha(cold_raw),
        source_sha256={n: sha(b) for n, b in sources.items()}, wrapper_sha256=sha(generated), response_sha256=sha(link),
        rounds=[], mini_rounds=[], native_phases=[])
    save = lambda: (ROOT / REPORT).write_text(json.dumps(report, indent=2) + '\n')
    def execute(argv, label):
        result = subprocess.run(argv, cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        (build.OUT / ('display-' + label + '.log')).write_bytes(result.stdout)
        report['native_phases'].append(dict(label=label, command=argv, returncode=result.returncode, log_sha256=sha(result.stdout)))
        save()
        need(result.returncode == 0, label + ': ' + result.stdout.decode(errors='replace')[-1000:])
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        original, stamp = (work / WRAPPER).read_bytes(), (work / WRAPPER).stat()
        mini = {f'probe/dpy-{n}.asm':b for n,b in mini_wrappers().items()}
        mini['probe/dpymini.lnk'] = mini_response()
        temporary = [work / n for n in (*sources, 'probe/dpyroot.obj', 'probe/dpyroot.exe', 'probe/dpyroot.map', 'probe/dpyroot.lnk')]
        temporary += [work/n for n in mini]+[work/f'probe/dpy-{n}.obj' for n in mini_wrappers()]+[work/'probe/dpymini.exe',work/'probe/dpymini.map']
        need(all(not p.exists() for p in temporary), 'fresh selected temporary paths')
        try:
            (work / 'probe').mkdir(exist_ok=True)
            for name, content in [*sources.items(), *mini.items(), (WRAPPER, generated), ('probe/dpyroot.lnk', link)]:
                (work / name).write_bytes(content)
                os.utime(work / name, (946684800, 946684800))
            (build.OUT / 'display-root.asm').write_bytes(generated)
            (build.OUT / 'display-root.lnk').write_bytes(link)
            for n,b in mini_wrappers().items():(build.OUT/f'display-mini-{n}.asm').write_bytes(b)
            (build.OUT/'display-mini.lnk').write_bytes(mini_response())
            for number in (1, 2):
                for ext in ('obj', 'exe', 'map'):
                    (work / f'probe/dpyroot.{ext}').unlink(missing_ok=True)
                execute(tasm + ['/m', '/mx', '/kh32768', '/t', '/dGAME=3', WRAPPER, r'probe\dpyroot.obj'], f'round{number}-assemble')
                raw, baseline = (work / 'probe/dpyroot.obj').read_bytes(), (work / OBJECT).read_bytes()
                (build.OUT/'display-current-root.obj').write_bytes(raw)
                need(describe_omf(raw)['valid'] and equivalent_root(raw,baseline), 'complete native payload/fixup order/public identity')
                execute(dos + ['tlink', r'@probe\dpyroot.lnk'], f'round{number}-link')
                outputs = {}
                for ext in ('obj', 'exe', 'map'):
                    raw = (work / f'probe/dpyroot.{ext}').read_bytes()
                    path = f'.analysis/work/display-round{number}.{ext}'
                    (ROOT / path).write_bytes(raw)
                    outputs[ext] = dict(path=path, bytes=len(raw), sha256=sha(raw))
                need((work / 'probe/dpyroot.exe').read_bytes() == (work / 'bin/th03/mainl.target.exe').read_bytes() and
                     (work / 'probe/dpyroot.map').read_bytes() == (work / 'obj/th03/mainl.map').read_bytes(), 'whole pinned target and retained MAP')
                report['rounds'].append(dict(round=number, outputs=outputs))
                mini_outputs = {}
                for name in mini_wrappers():
                    output = rf'probe\dpy-{name}.obj'
                    (work/output.replace('\\','/')).unlink(missing_ok=True)
                    execute(tasm+['/m','/mx','/kh32768','/t','/dGAME=3',rf'probe\dpy-{name}.asm',output],f'round{number}-mini-{name}')
                    raw = (work/output.replace('\\','/')).read_bytes()
                    path = f'.analysis/work/display-mini-round{number}-{name}.obj'
                    (ROOT/path).write_bytes(raw);mini_outputs[name] = dict(path=path,bytes=len(raw),sha256=sha(raw))
                for ext in ('exe','map'):(work/f'probe/dpymini.{ext}').unlink(missing_ok=True)
                execute(dos+['tlink',r'@probe\dpymini.lnk'],f'round{number}-mini-link')
                for ext in ('exe','map'):
                    raw = (work/f'probe/dpymini.{ext}').read_bytes();path = f'.analysis/work/display-mini-round{number}.{ext}'
                    (ROOT/path).write_bytes(raw);mini_outputs[ext] = dict(path=path,bytes=len(raw),sha256=sha(raw))
                report['mini_rounds'].append(dict(round=number,outputs=mini_outputs))

                save()
                print(f'display round{number}: maintained state/native root/whole target and MAP PASS', flush=True)
            need({k: v['sha256'] for k, v in report['rounds'][0]['outputs'].items()} ==
                 {k: v['sha256'] for k, v in report['rounds'][1]['outputs'].items()}, 'complete raw selected repeat equality')
            need({k:v['sha256'] for k,v in report['mini_rounds'][0]['outputs'].items()} ==
                 {k:v['sha256'] for k,v in report['mini_rounds'][1]['outputs'].items()},'whole native display mini repetition')
        finally:
            (work / WRAPPER).write_bytes(original)
            os.utime(work / WRAPPER, ns=(stamp.st_atime_ns, stamp.st_mtime_ns))
            for p in temporary:
                p.unlink(missing_ok=True)
    cold_context(ROOT)
    report['complete'] = True
    save()


if __name__ == '__main__':
    main()
