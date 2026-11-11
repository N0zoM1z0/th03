#!/usr/bin/env python3
"""Export and launch the private no-hit DOS variant with Windows DOSBox-X."""
import argparse
import json
import os
from pathlib import Path
import subprocess

import play_invincible as variant
import play_th03_dos as play

OUTPUT = Path('/mnt/d/Entertainment/Game/Touhou/th03-reconstruct')
EMULATOR = Path('/mnt/d/Entertainment/Game/Touhou/东方旧作整合/dosbox-x')
EXE_SHA = '8f6ecd007b0784d55d07e28c2d41be69ae2afe0d9bd720cffb3c236f44449521'
FONT_SHA = '41535bd7242c07d69ec5427584d31f068ca4eb996ca95246caed4e3573a494e6'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir', type=Path, default=OUTPUT)
    p.add_argument('--prepare-only', action='store_true')
    args = p.parse_args()
    output = args.output_dir.resolve()
    play.need(str(output).startswith('/mnt/'), 'Windows output directory')
    play.need(not variant.live(variant.DEFAULT), 'close Linux playback before exporting its disk')
    if not variant.DEFAULT.exists():
        os.sched_setaffinity(0, {max(os.sched_getaffinity(0))})
        if os.nice(0) < 10:
            os.nice(10 - os.nice(0))
        variant.prepare(variant.DEFAULT)
    main_exe, proof = variant.build()
    record = json.loads((variant.DEFAULT / 'play.json').read_text())
    play.need(record['products']['MAIN.EXE']['sha256'] == play.sha(main_exe.read_bytes()), 'current no-hit MAIN')
    if not output.exists():
        exe = (EMULATOR / 'dosbox-x.exe').read_bytes()
        font = (EMULATOR / 'font_jp.bmp').read_bytes()
        play.need(play.sha(exe) == EXE_SHA and play.sha(font) == FONT_SHA, 'attested Windows emulator/font')
        # This collection stores literal backslash-r/backslash-n in its configs.
        config = (EMULATOR / 'th03_jp.conf').read_bytes().replace(b'\\r\\n', b'\r\n')
        play.need(config.count(b'imgmount c jp.hdi') == 1 and b'cycles=15000' in config and
                  b'core=dynamic' in config, 'collection TH03 Japanese profile')
        config = config.replace(b'imgmount c jp.hdi', b'imgmount c play.hdi')
        config = (b'[sdl]\r\nfullscreen=false\r\noutput=surface\r\n'
                  b'[render]\r\nscaler=normal2x forced\r\n' + config + b'\r\n')
        raw = (variant.DEFAULT / 'execution.hdi').read_bytes()
        output.mkdir(parents=True)
        (output / 'play.hdi').write_bytes(raw)
        for name, data in [('dosbox-x.exe', exe), ('FREECG98.BMP', font), ('th03-nohit.conf', config)]:
            (output / name).write_bytes(data)
        launcher = ('@echo off\r\ncd /d "%~dp0"\r\n'
                    'start "" "%~dp0dosbox-x.exe" -conf "%~dp0th03-nohit.conf"\r\n')
        (output / 'start-th03.bat').write_text(launcher, encoding='ascii', newline='')
        (output / 'README.txt').write_text(
            'TH03 reconstructed DOS game - human no-hit test build\n\n'
            'Double-click start-th03.bat. Use English keyboard input.\n'
            'Arrow keys: move/menu; Z: fire/charge; X: bomb; Escape: pause.\n'
            'Press a direction at the title to show the menu.\n'
            'Forced 2x pixel scaling is enabled. F11+F toggles fullscreen.\n'
            'Human players take no collision damage or death animation. CPU opponents remain vulnerable.\n'
            'Saves are inside this folder\'s play.hdi. Do not run two copies at once.\n'
            'This is a modified test build, separate from the exact reconstruction.\n', encoding='ascii')
        manifest = dict(variant='human-no-hit', products=record['products'],
                        dosbox_x_sha256=EXE_SHA, font_sha256=FONT_SHA,
                        config_sha256=play.sha(config), initial_hdi_sha256=play.sha(raw))
        (output / 'package.json').write_text(json.dumps(manifest, indent=2) + '\n')
    manifest = json.loads((output / 'package.json').read_text())
    play.need(manifest['variant'] == 'human-no-hit' and manifest['products'] == record['products'],
              'existing Windows package has different products; preserve its saves')
    for name, key in [('dosbox-x.exe', 'dosbox_x_sha256'), ('FREECG98.BMP', 'font_sha256'),
                      ('th03-nohit.conf', 'config_sha256')]:
        play.need(play.sha((output / name).read_bytes()) == manifest[key], 'Windows package identity: ' + name)
    windows = subprocess.check_output(['wslpath', '-w', str(output)], text=True).strip()
    quoted = "'" + windows.replace("'", "''") + "'"
    # Windows DOSBox holds its writable HDI exclusively. Detect the owned
    # process before attempting another disk read or opening another writer.
    probe = (f'$exe=Join-Path {quoted} "dosbox-x.exe"; '
             'Get-Process -Name "dosbox-x" -ErrorAction SilentlyContinue | '
             'Where-Object {$_.Path -eq $exe} | Select-Object Id,MainWindowTitle | ConvertTo-Json -Compress')
    running = subprocess.check_output(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', probe], text=True).strip()
    if running:
        print('Already running:', running)
        return
    for name, row in manifest['products'].items():
        play.need(play.sha(play.media(output / 'play.hdi', 'mtype', '::/YUMEZIKU/' + name)) == row['sha256'],
                  'complete Windows disk product readback: ' + name)
    if args.prepare_only:
        print(output)
        return
    command = (f'$dir={quoted}; $exe=Join-Path $dir "dosbox-x.exe"; '
               '$live=Get-Process -Name "dosbox-x" -ErrorAction SilentlyContinue | Where-Object {$_.Path -eq $exe}; '
               'if($live){$live | Select-Object Id,MainWindowTitle | ConvertTo-Json -Compress; exit 0}; '
               '$p=Start-Process -FilePath $exe -ArgumentList @("-conf","th03-nohit.conf") '
               '-WorkingDirectory $dir -PassThru; Start-Sleep -Seconds 4; $p.Refresh(); '
               'if($p.HasExited){throw "Windows DOSBox-X exited"}; '
               '$p | Select-Object Id,MainWindowTitle,MainWindowHandle | ConvertTo-Json -Compress')
    subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', command], check=True)


if __name__ == '__main__':
    main()
