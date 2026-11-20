#!/usr/bin/env python3
"""Exercise the TH03 MAINL ending or score registration on isolated DOS disks."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess

from audit_th03_dos_pi import DRIVE
from capture_th03_pi_demos import install
from play_th03_dos import ROOT, media, need, run, sha


def seed_disk(args, output):
    build = DRIVE / "TH03PI" / args.stage
    links = json.loads((build / "layout.json").read_bytes())
    original, disk, hashes = install(build / args.layout, output, links, args.layout)
    fixture = output / "piseed.com"
    stage, score_only = (2, 1) if args.score else (9, 0)
    subprocess.run(["nasm", "-f", "bin", f"-DSTAGE={stage}", f"-DSCORE_ONLY={score_only}",
                    str(ROOT / "scripts/runtime/th03_pi_resident.asm"), "-o", str(fixture)], check=True)
    media(disk, "mcopy", "-o", str(fixture), "::/YUMEZIKU/PISEED.COM")
    batch = media(disk, "mtype", "::/YUMEZIKU/GAME.BAT")
    updated, count = re.subn(rb"(?im)^op[ \t]*\r?$", b"piseed\r", batch)
    need(count == 6, "original GAME.BAT startup branches")
    path = output / "GAME.BAT"
    path.write_bytes(updated)
    media(disk, "mcopy", "-o", str(path), "::/YUMEZIKU/GAME.BAT")
    need(media(disk, "mtype", "::/YUMEZIKU/GAME.BAT") == updated, "fixture batch installed in private disk")
    hashes["zun"] = sha(media(disk, "mtype", "::/YUMEZIKU/ZUN.COM"))
    products = {(name.upper() + (".COM" if name == "zun" else ".EXE")): {"sha256": digest}
                for name, digest in hashes.items()}
    return original, disk, products


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--layout", choices=("control", "even", "alt", "odd"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--score", action="store_true", help="start directly at score registration")
    parser.add_argument("--seconds", type=float, required=True)
    parser.add_argument("--event", action="append", default=[])
    parser.add_argument("--frame", action="append", default=[])
    args = parser.parse_args()
    need(re.fullmatch(r"af[0-9]+[a-z]", args.stage), "retained PI stage")
    args.original = False
    args.emulator = Path("/usr/bin/dosbox-x")
    args.font_bmp = ROOT / ".analysis/runtime/fonts/FREECG98.BMP"
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(0 - os.nice(0) + 10)
    run(args, seed_disk)


if __name__ == "__main__":
    main()
