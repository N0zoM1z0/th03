#!/usr/bin/env python3
"""Fast syntax and whitespace checks; Python 3.11+ and Git are sufficient."""
import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def git(*args, **kwargs):
    return subprocess.check_output(['git', *args], cwd=ROOT, **kwargs)


def previous_revision():
    parents = git('rev-list', '--parents', '-n', '1', 'HEAD').split()
    if len(parents) > 1:
        return parents[1].decode()
    return git('hash-object', '-t', 'tree', '--stdin', input=b'').decode().strip()


def changed_files(base):
    return {os.fsdecode(name) for name in
            git('diff', '--name-only', '-z', base, '--').split(b'\0') if name}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', help='check changes since this revision (PR/push base)')
    args = parser.parse_args(argv)
    try:
        base = args.base or 'HEAD'
        if not base.strip('0'):
            base = previous_revision()  # First push of a branch has an all-zero before SHA.
        names = changed_files(base)
        names.update(os.fsdecode(name) for name in
                     git('ls-files', '--others', '--exclude-standard', '-z').split(b'\0') if name)
        if not names and args.base is None:
            base = previous_revision()  # Also check the last commit in a clean checkout.
            names = changed_files(base)
        checked = 0
        for name in sorted(names):
            path = ROOT / name
            if not path.is_file() or path.is_symlink():
                continue
            if path.suffix == '.py':
                ast.parse(path.read_bytes(), filename=name)
            elif path.suffix == '.json':
                json.loads(path.read_bytes())
            elif path.suffix == '.toml':
                tomllib.loads(path.read_text(encoding='utf-8'))
            elif path.suffix == '.sh':
                subprocess.run(['bash', '-n', str(path)], check=True)
            else:
                continue
            checked += 1
        subprocess.run(['git', 'diff', '--check', base, '--'], cwd=ROOT, check=True)
        print(f'Basic checks passed: {checked} syntax files; Git whitespace checked.')
        return 0
    except (OSError, SyntaxError, UnicodeError, ValueError, subprocess.CalledProcessError) as error:
        print(f'Basic checks failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
