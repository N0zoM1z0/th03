#!/usr/bin/env python3
"""Preview or remove regenerable Python/test caches; never traverse .analysis."""

import argparse
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
CACHE_NAMES = ('.pytest_cache', '.mypy_cache', '.ruff_cache')


def cache_paths():
    for name in CACHE_NAMES:
        path = ROOT / name
        if path.is_dir() and not path.is_symlink():
            yield path
    for name in ('scripts', 'tests'):
        base = ROOT / name
        if not base.is_dir() or base.is_symlink():
            continue
        for parent, directories, _ in os.walk(base, followlinks=False):
            if '__pycache__' in directories:
                directories.remove('__pycache__')
                path = Path(parent) / '__pycache__'
                if not path.is_symlink():
                    yield path


def clean_caches(dry_run):
    size = 0
    for path in cache_paths():
        size += sum(p.lstat().st_blocks * 512 for p in path.rglob('*'))
        print(('would remove ' if dry_run else 'remove ') + str(path.relative_to(ROOT)))
        if not dry_run:
            shutil.rmtree(path)
    return size


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--caches-only', action='store_true', help='explicitly select cache cleanup')
    parser.add_argument('--apply', action='store_true', help='delete the listed caches')
    args = parser.parse_args()
    if args.apply and not args.caches_only:
        parser.error('use --caches-only --apply to remove caches')
    size = clean_caches(not args.apply)
    print(f"{'removed' if args.apply else 'would remove'} approximately {size / 1024**2:.1f} MiB")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
