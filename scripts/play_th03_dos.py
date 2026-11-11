#!/usr/bin/env python3
"""Boot the rebuilt DOS game in a disposable HDI and exercise real SDL input.

Run under xvfb-run. All media, captures, saves and emulator state stay in the
new output directory. This does not patch the game or grant source-exact credit.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time
import tomllib

ROOT = Path(__file__).resolve().parents[1]
EMULATORS = {
    '30a5fdf8fa95abaf7bae1a9e624ccfc9e26e5357a19cc567bf3a2ac659699258': 'Ubuntu DOSBox-X 2024.03.01',
    '6e1a6e706d8b62aefa3204e30be5b77125fb4413d6891b5d10bd2701a6616ba1': 'TH04 read-only demo-observer build, observer disabled',
}
FONT_SHA256 = '91d75314ac4f940ab13b3c33fb260ef1713865d025a94f09f6814a72e47dfa87'
PROFILE = '''[sdl]
fullscreen=false
output=surface
videodriver=x11
autolock=false
waitonerror=false
priority=normal,normal
showmenu=false
[dosbox]
machine=pc98
memsize=16
fastbioslogo=true
startbanner=false
synchronize time=false
working directory option=noprompt
quit warning=false
[pc98]
pc-98 fm board=board86c
pc-98 sound bios=false
pc-98 load sound bios rom file=false
pc-98 enable 256-color=false
pc-98 enable 16-color=true
pc-98 enable grcg=true
pc-98 enable egc=true
pc-98 start gdc at 5mhz=false
pc-98 timer always cycles=true
pc-98 timer master frequency=5
pc-98 force ibm keyboard layout=false
pc-98 force JIS keyboard layout=false
pc-98 try font rom=false
[cpu]
core=normal
cputype=pentium
fpu=true
cycles=fixed 24000
turbo=false
[mixer]
nosound=false
[midi]
mpu401=none
mididevice=none
[dos]
keyboardlayout=none
'''


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(value, message):
    if not value:
        raise ValueError(message)


def timed(spec):
    name, second = spec.rsplit('@', 1)
    need(bool(re.fullmatch(r'[A-Za-z0-9_+:.-]+', name)), 'invalid event/checkpoint name')
    return float(second), name


def media(image, operation, *args):
    # This pinned PC-98 FAT12 volume uses FE in its BPB and F8 in the FAT.
    return subprocess.check_output([operation, '-i', str(image) + '@@38912', *args],
                                   env=os.environ | {'MTOOLS_SKIP_CHECK': '1'}, stderr=subprocess.PIPE)


def prepare(args, output):
    targets = tomllib.loads((ROOT / 'config/targets.toml').read_text())
    original = ROOT / '.analysis/runtime/images/zun.hdi'
    need(sha(original.read_bytes()) == targets['source']['hdi_sha256'], 'pinned original HDI identity')
    image = output / 'execution.hdi'
    image.write_bytes(original.read_bytes())
    package = ROOT / '.analysis/toolchain/wineprefix/drive_c/TH03PKG' / args.package_stage
    proof = None if args.original else json.loads((package / 'runtime-package.json').read_bytes())
    if proof is not None:
        need(proof['complete'] and proof['stage'] == args.package_stage, 'complete current packing receipt')
    def put(name, data):
        staged = output / 'stage.bin'
        staged.write_bytes(data)
        media(image, 'mcopy', '-o', str(staged), '::/' + name)
        need(media(image, 'mtype', '::/' + name) == data, 'complete installed readback: ' + name)
    products = {}
    for target in targets['artifacts']:
        if target.get('game') != 'th03':
            continue
        name = target['dos_path'].split('/')[-1]
        source = ROOT / target['private_path'] if args.original else package / 'r1/packed' / name.lower()
        raw = source.read_bytes()
        need(len(raw) == target['size'] and sha(raw) == target['sha256'], 'complete pinned Japanese product: ' + name)
        if proof is not None:
            need(proof['rounds'][0]['outputs']['packed/' + name.lower()] == dict(bytes=len(raw), sha256=sha(raw)),
                 'actual current packed producer: ' + name)
        need(media(image, 'mtype', '::/' + target['dos_path']) == raw, 'original-data product identity')
        put(target['dos_path'], raw)
        products[name] = dict(path=str(source), bytes=len(raw), sha256=sha(raw))
    put('AUTOEXEC.BAT', b'@ECHO OFF\r\nPATH A:\\DOS;A:\\\r\nSET TEMP=A:\\DOS\r\nSET DOSDIR=A:\\DOS\r\n'
        b'CD \\YUMEZIKU\r\nECHO START > A:\\TH03RUN.TXT\r\nCALL GAME.BAT\r\nECHO EXIT >> A:\\TH03RUN.TXT\r\n\x1a')
    (output / 'stage.bin').unlink()
    return original, image, products


def run(args):
    output = args.output.resolve()
    need(output.is_relative_to(ROOT / '.analysis/runtime') and not output.exists(), 'use a fresh private runtime directory')
    need(bool(os.environ.get('DISPLAY')), 'run through xvfb-run with a private display')
    emulator = args.emulator.resolve()
    digest = sha(emulator.read_bytes())
    need(digest in EMULATORS, 'uncalibrated emulator binary')
    font = args.font_bmp.read_bytes()
    need(sha(font) == FONT_SHA256, 'pinned FREECG98 bitmap font')
    timeline = sorted([(second, 'input', name) for second, name in map(timed, args.event)] +
                      [(second, 'frame', name) for second, name in map(timed, args.frame)])
    need(all(0 <= second < args.seconds for second, _, _ in timeline), 'events/checkpoints must precede stop')
    need(len({name for _, kind, name in timeline if kind == 'frame'}) == len(args.frame), 'unique frame names')
    output.mkdir(parents=True)
    original, image, products = prepare(args, output)
    (output / 'FREECG98.BMP').write_bytes(font)
    (output / 'captures').mkdir()
    config = output / 'dosbox-x.conf'
    config.write_text(PROFILE.replace('[dosbox]\n', '[dosbox]\ncaptures=' + str(output / 'captures') + '\n'))
    argv = [str(emulator), '-defaultconf', '-defaultmapper', '-conf', str(config), '-fastlaunch', '-nogui', '-nomenu',
            '-exit', '-c', 'imgmount 2 "' + str(image) + '" -t hdd -fs none', '-c', 'boot -l c']
    env = {k: v for k, v in os.environ.items() if not k.startswith('TH04_')}
    env.update(SDL_VIDEODRIVER='x11', SDL_AUDIODRIVER='dummy', WAYLAND_DISPLAY='',
               XDG_CACHE_HOME=str(output / 'cache'), XDG_CONFIG_HOME=str(output / 'config'), XDG_DATA_HOME=str(output / 'data'))
    record = dict(emulator=str(emulator), emulator_sha256=digest, emulator_profile=EMULATORS[digest],
                  config_sha256=sha(config.read_bytes()), font_sha256=sha(font), products=products,
                  role='original' if args.original else 'rebuilt', cpu_affinity=sorted(os.sched_getaffinity(0)),
                  nice=os.nice(0), argv=argv, events=[], frames={}, starting_hdi_sha256=sha(image.read_bytes()))
    for name in ('YUME.CFG', 'YUME.NEM'):
        (output / ('before-' + name)).write_bytes(media(image, 'mtype', '::/YUMEZIKU/' + name))
    window = None
    def control(action, key):
        need(window is not None, 'emulator window missing')
        subprocess.run(['xdotool', 'windowfocus', '--sync', window], check=True, env=env, capture_output=True)
        command = ['xdotool', action]
        if action == 'key':
            command += ['--delay', '300']
        subprocess.run([*command, key], check=True, env=env, capture_output=True)
    with (output / 'boot.log').open('wb') as log:
        process = subprocess.Popen(argv, cwd=output, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        started = time.monotonic()
        pending = list(timeline)
        try:
            while process.poll() is None and time.monotonic() - started < args.seconds:
                if window is None:
                    found = subprocess.run(['xdotool', 'search', '--onlyvisible', '--pid', str(process.pid), '--name', 'DOSBox-X'],
                                           env=env, capture_output=True, text=True).stdout.split()
                    if found:
                        need(len(found) == 1, 'one emulator window'); window = found[0]
                while pending and time.monotonic() - started >= pending[0][0]:
                    second, kind, name = pending.pop(0)
                    if kind == 'frame':
                        path = output / (name + '.png')
                        need(window is not None, 'frame window missing')
                        subprocess.run(['import', '-window', window, str(path)], env=env, check=True, capture_output=True)
                        record['frames'][path.name] = sha(path.read_bytes())
                    else:
                        action, key = ('keydown', name[5:]) if name.startswith('down:') else (
                            ('keyup', name[3:]) if name.startswith('up:') else ('key', name))
                        control(action, key)
                    record['events'].append(dict(requested=second, observed=time.monotonic()-started, kind=kind, name=name))
                time.sleep(.03)
            need(not pending, 'emulator exited before all requested events/checkpoints')
            control('key', 'ctrl+F9')
            process.wait(timeout=10)
        finally:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try: process.wait(timeout=5)
                except subprocess.TimeoutExpired: os.killpg(process.pid, signal.SIGKILL); process.wait()
    record['exit_code'] = process.returncode
    need(process.returncode == 0, 'emulator did not close normally')
    record['executed_hdi_sha256'] = sha(image.read_bytes())
    record['dos_markers'] = media(image, 'mtype', '::/TH03RUN.TXT').decode('ascii').strip()
    for name in ('YUME.CFG', 'YUME.NEM'):
        (output / ('after-' + name)).write_bytes(media(image, 'mtype', '::/YUMEZIKU/' + name))
    for name, row in products.items():
        need(sha(media(image, 'mtype', '::/YUMEZIKU/' + name)) == row['sha256'], 'executed product changed: ' + name)
    expected = tomllib.loads((ROOT / 'config/targets.toml').read_text())['source']['hdi_sha256']
    need(sha(original.read_bytes()) == expected, 'original media changed')
    record['original_hdi_unchanged'] = True
    (output / 'run.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(dict(output=str(output), frames=record['frames'], dos_markers=record['dos_markers']), indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--seconds', type=float, default=60)
    p.add_argument('--event', action='append', default=[], help='KEY@SECOND, down:KEY@SECOND or up:KEY@SECOND')
    p.add_argument('--frame', action='append', default=[], help='NAME@SECOND; save an actual window PNG')
    p.add_argument('--package-stage', default='af1410p')
    p.add_argument('--original', action='store_true')
    p.add_argument('--emulator', type=Path, default=Path('/usr/bin/dosbox-x'))
    p.add_argument('--font-bmp', type=Path, default=ROOT / '.analysis/runtime/fonts/FREECG98.BMP')
    args = p.parse_args()
    need(0 < args.seconds <= 1800 and re.fullmatch(r'af[0-9]+[a-z]', args.package_stage), 'bounded duration and DOS-safe package stage')
    cpu = max(os.sched_getaffinity(0))
    os.sched_setaffinity(0, {cpu})
    if os.nice(0) < 10: os.nice(10 - os.nice(0))
    run(args)


if __name__ == '__main__':
    main()
