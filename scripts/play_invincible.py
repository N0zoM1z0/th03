#!/usr/bin/env python3
"""Build a private human-only no-hit DOS variant and open a persistent window."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import time

import build_th03_package_current as package
import play_th03_dos as play
import probe_th03_main_exatt_layout as overlay
from lib.pc98 import parse_mz

ROOT = play.ROOT
DEFAULT = ROOT / '.analysis/runtime/candidates/th03-invincible-play'
STAGE = 'af1411g'
ANCHOR = b'                player_hittest(4);\n'
ADDITION = b'                if(!player->is_cpu) { player->is_hit = false; }\n'


def build():
    """Overlay one current physical TU; retain every other current link input."""
    base = package.DRIVE / 'TH03WORK/probe' / STAGE
    paths = [overlay.SOURCES['core'], overlay.ENTITY, overlay.BOSS_TEMPLATE,
             overlay.BACKGROUND_PHASE, *overlay.owner_inline_paths('core', STAGE)]
    sources = {path: (ROOT / path).read_bytes() for path in paths}
    update = 'src/main/player/update.inl'
    play.need(sources[update].count(ANCHOR) == 1, 'one post-collision source anchor')
    inputs = {p: play.sha(raw) for p, raw in sources.items()}
    for n in (1, 2):
        path = package.DRIVE / f'TH03PKG/af1409l/r{n}/main.lnk'
        inputs[str(path.relative_to(ROOT))] = play.sha(path.read_bytes())
    if base.exists():
        report = json.loads((base / 'variant.json').read_text())
        play.need(report['variant'] == 'human-no-hit' and report['source_sha256'] == inputs,
                  'retained no-hit source/link context changed')
        for n in (1, 2):
            play.need(package.pin(base / f'r{n}/main.exe') == report['rounds'][n-1]['native'] and
                      package.pin(base / f'r{n}/core.obj') == report['rounds'][n-1]['object'],
                      'retained native no-hit output changed')
        return base / 'r1/main.exe', report
    report = dict(variant='human-no-hit', source_sha256=inputs,
                  effect='clear human is_hit after collision, before damage/knockback/death', rounds=[])
    env = os.environ | dict(DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
                            MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        base.mkdir()
        for n in (1, 2):
            rd = base / f'r{n}'
            rd.mkdir()
            for path, original in sources.items():
                raw = original.replace(ANCHOR, ANCHOR + ADDITION) if path == update else original
                raw = (overlay.rooted_source('core', STAGE, n, raw) if path == overlay.SOURCES['core']
                       else overlay.rooted_inline_source(path, STAGE, n, raw))
                dest = rd / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(raw.replace(b'\n', b'\r\n'))
            (rd / 'core.cpp').write_bytes(overlay.rooted_wrapper(
                'core', STAGE, n, overlay.wrapper_source('core')).replace(b'\n', b'\r\n'))
            response_path = package.DRIVE / f'TH03PKG/af1409l/r{n}/main.lnk'
            response = response_path.read_bytes()
            inputs[str(response_path.relative_to(ROOT))] = play.sha(response)
            old = f'probe\\af1191e\\r{n}\\core.obj'.encode()
            play.need(response.count(old) == 1, 'one current core link slot')
            response = response.replace(old, f'probe\\{STAGE}\\r{n}\\core.obj'.encode())
            for suffix in ('exe', 'map'):
                old = f'C:\\TH03PKG\\af1409l\\r{n}\\main.{suffix}'.encode()
                play.need(response.count(old) == 1, 'one native output slot')
                response = response.replace(old, package.windows(rd / ('main.' + suffix)).encode())
            (rd / 'main.lnk').write_bytes(response)
            commands = [package.dos() + ['tcc', '-c', f'-Iprobe/{STAGE}/r{n}', '-I.',
                        '-O', '-b-', '-3', '-Z', '-d', '-DGAME=3', '-ml', "-DBINARY='M'",
                        f'-nprobe/{STAGE}/r{n}/', f'probe/{STAGE}/r{n}/core.cpp'],
                        package.dos() + ['tlink', '@' + package.windows(rd / 'main.lnk')]]
            for label, argv in zip(('compile', 'link'), commands):
                result = subprocess.run(argv, cwd=package.DRIVE / 'TH03WORK', env=env,
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
                (rd / (label + '.log')).write_bytes(result.stdout)
                play.need(result.returncode == 0, label + ' failed; see ' + str(rd))
            native = (rd / 'main.exe').read_bytes()
            parsed = parse_mz(native)
            play.need(parsed.valid and len(parsed.relocations) == 1553, 'complete native variant MZ')
            # Use the ordinary TLINK MZ directly; no executable-byte patches.
            report['rounds'].append(dict(native=package.pin(rd / 'main.exe'),
                                         object=package.pin(rd / 'core.obj')))
            print('Built human no-hit MAIN round', n, flush=True)
    play.need((base / 'r1/main.exe').read_bytes() == (base / 'r2/main.exe').read_bytes(),
              'native no-hit outputs repeat')
    report['main'] = str((base / 'r1/main.exe').relative_to(ROOT))
    (base / 'variant.json').write_text(json.dumps(report, indent=2) + '\n')
    return base / 'r1/main.exe', report


def live(prepared):
    try:
        pid = int((prepared / 'dosbox.pid').read_text())
        argv = Path(f'/proc/{pid}/cmdline').read_bytes()
        return pid if b'dosbox-x' in argv and os.fsencode(prepared / 'execution.hdi') in argv else None
    except (OSError, ValueError):
        return None


def prepare(prepared):
    prepared.mkdir(parents=True)
    main, variant = build()
    original, image, products = play.prepare(argparse.Namespace(original=False, package_stage='af1410p'), prepared)
    raw = main.read_bytes()
    staged = prepared / 'main.exe'
    staged.write_bytes(raw)
    play.media(image, 'mcopy', '-o', str(staged), '::/YUMEZIKU/MAIN.EXE')
    play.need(play.media(image, 'mtype', '::/YUMEZIKU/MAIN.EXE') == raw, 'complete no-hit MAIN readback')
    products['MAIN.EXE'] = dict(path=str(main), bytes=len(raw), sha256=play.sha(raw))
    font = (ROOT / '.analysis/runtime/fonts/FREECG98.BMP').read_bytes()
    play.need(play.sha(font) == play.FONT_SHA256, 'pinned font')
    (prepared / 'FREECG98.BMP').write_bytes(font)
    (prepared / 'captures').mkdir()
    (prepared / 'dosbox-x.conf').write_text(play.PROFILE.replace(
        '[dosbox]\n', '[dosbox]\ncaptures=' + str(prepared / 'captures') + '\n'))
    record = dict(variant=variant, products=products, original_hdi_sha256=play.sha(original.read_bytes()))
    (prepared / 'play.json').write_text(json.dumps(record, indent=2) + '\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prepared-dir', type=Path, default=DEFAULT)
    p.add_argument('--prepare-only', action='store_true')
    p.add_argument('--stop', action='store_true')
    args = p.parse_args()
    prepared = args.prepared_dir.resolve()
    play.need(prepared.is_relative_to(ROOT / '.analysis/runtime/candidates'), 'private playable image')
    pid = live(prepared)
    if args.stop:
        if pid:
            os.kill(pid, signal.SIGTERM)
        print('Stopped' if pid else 'Not running')
        return
    if pid:
        print('Already running:', pid)
        return
    os.sched_setaffinity(0, {max(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    if not prepared.exists():
        prepare(prepared)
    record = json.loads((prepared / 'play.json').read_text())
    for path, expected in record['variant']['source_sha256'].items():
        play.need(play.sha((ROOT / path).read_bytes()) == expected, 'variant source changed: ' + path)
    for name, row in record['products'].items():
        play.need(play.sha(play.media(prepared / 'execution.hdi', 'mtype', '::/YUMEZIKU/' + name)) == row['sha256'],
                  'installed playable product: ' + name)
    if args.prepare_only:
        print(prepared)
        return
    play.need(bool(os.environ.get('DISPLAY')), 'interactive display required')
    emulator = Path('/usr/bin/dosbox-x')
    play.need(play.sha(emulator.read_bytes()) in play.EMULATORS, 'pinned emulator')
    argv = [str(emulator), '-defaultconf', '-defaultmapper', '-conf', str(prepared / 'dosbox-x.conf'),
            '-fastlaunch', '-nomenu', '-c', 'imgmount 2 "' + str(prepared / 'execution.hdi') + '" -t hdd -fs none',
            '-c', 'boot -l c']
    env = {k: v for k, v in os.environ.items() if not k.startswith('TH04_')}
    env.update(SDL_VIDEODRIVER='x11', WAYLAND_DISPLAY='', SDL_AUDIODRIVER='pulseaudio',
               XDG_CACHE_HOME=str(prepared / 'cache'), XDG_CONFIG_HOME=str(prepared / 'config'),
               XDG_DATA_HOME=str(prepared / 'data'))
    with (prepared / 'play.log').open('ab') as log:
        process = subprocess.Popen(argv, cwd=prepared, env=env, stdin=subprocess.DEVNULL,
                                   stdout=log, stderr=log, start_new_session=True)
    time.sleep(3)
    play.need(process.poll() is None, 'DOSBox exited; inspect play.log')
    (prepared / 'dosbox.pid').write_text(str(process.pid) + '\n')
    print('Human no-hit DOSBox running:', process.pid, prepared)


if __name__ == '__main__':
    main()
