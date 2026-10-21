"""Maintained tiny-init recipe; a reviewed parent supervisor owns native execution.

No compiler subprocess is created here. build_round is the concrete fixed recipe
used by the cold-pair adapter, not a generic command runner. The supervisor must
provide the reviewed Run native/step/event operations and consumed(). A CLI never
launches native tools. This recipe does not wire the default wrapper build graph.
"""
from pathlib import Path
import hashlib
import os
import stat
from stage_th03_zun_init import stage_bytes
from verify_th03_zun_init_standalone import parse_object, verify_outputs
SOURCE = 'src/zun/init.asm'
SOURCE_SHA = '078525c35dfa4b499feb661980733964e16fa5654e8403ee55b0de221e828dc2'
STAGED_SHA = '6f35dcba455a9d9ab9bb9545e55141da7ca25186749df6749d8ac4c3c43a1e55'
RESPONSE = b'-c -s -t -3 init.obj,init.com,init.map,\r\n'
OUTPUTS = ('init.obj', 'init.com', 'init.map')

def require(ok, message):
    if not ok: raise ValueError(message)

def plain(path, directory=False):
    path = Path(path)
    require(path.is_absolute(), 'absolute owned path required')
    for part in (path, *path.parents):
        require(not part.is_symlink(), 'symlink in owned path')
    mode = path.lstat().st_mode
    require(stat.S_ISDIR(mode) if directory else stat.S_ISREG(mode), 'wrong owned path kind')
    return path

def identity(path):
    path = plain(path); before = path.stat(); raw = path.read_bytes(); after = path.stat()
    key = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mode, s.st_mtime_ns, s.st_ctime_ns)
    require(key(before) == key(after), 'input changed during read')
    return dict(path=str(path), mode=stat.S_IMODE(after.st_mode), size=len(raw),
                sha256=hashlib.sha256(raw).hexdigest())

def write_new(path, raw):
    plain(path.parent, directory=True)
    with path.open('xb') as out:
        out.write(raw); out.flush(); os.fsync(out.fileno())

def stage(source_path, work, source_mtime_ns):
    """Create a new, empty round. A failed/colliding directory is never reused."""
    source_path = plain(source_path)
    require(type(source_mtime_ns) is int and source_path.stat().st_mtime_ns == source_mtime_ns, 'declared maintained-source mtime changed')
    raw = source_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA, 'maintained source identity')
    staged = stage_bytes(raw)
    require(hashlib.sha256(staged).hexdigest() == STAGED_SHA, 'strict encoding identity')
    plain(work.parent, directory=True)
    work.mkdir()  # Exclusive, including an existing empty directory or symlink.
    (work / 'src/zun').mkdir(parents=True)
    write_new(work / SOURCE, staged)
    os.utime(work / SOURCE, ns=(source_mtime_ns, source_mtime_ns), follow_symlinks=False)
    require((work / SOURCE).stat().st_mtime_ns == source_mtime_ns, 'staged source mtime differs')
    write_new(work / 'link.rsp', RESPONSE)
    return [identity(work / name) for name in (SOURCE, 'link.rsp')]

def commands(wine, msdos):
    require(Path(wine).is_absolute() and Path(msdos).is_absolute(), 'pinned absolute tools required')
    return (
        [wine, r'C:\TASM50\BIN\TASM32.EXE', '/m', '/mx', '/kh32768', '/t',
         r'src\zun\init.asm,init.obj'],
        [wine, msdos, '-e', '-x', 'tlink', '@link.rsp'])

def build_round(run):
    """Exactly one fresh assembly and one tiny link under the reviewed supervisor.

run.work has been exclusively created by stage(), never a retained workdir.
The adapter binds the source, recipe/import closure, tool installation, history,
registry baseline, manifest and generated files before entering this function.
"""
    require(run.m['source'] == SOURCE and run.native_count == 0, 'fresh maintained round required')
    assemble, link = commands(run.m['wine'], str(run.root / run.m['msdos_player']))
    run.consumed('before-assemble')
    run.native('assemble', assemble, list(OUTPUTS), ['init.obj'])
    run.consumed('before-link')
    run.step('fresh OMF', lambda: parse_object(plain(run.work / 'init.obj').read_bytes()), 30)
    obj = run.step('fresh object identity', lambda: identity(run.work / 'init.obj'), 5)
    run.inputs.append(obj); run.event('assembled-object.json', obj)
    run.native('link', link, ['init.com', 'init.map'], ['init.com', 'init.map'])
    for name in ('init.com', 'init.map'):
        run.inputs.append(run.step('linked output identity', lambda n=name: identity(run.work / n), 5))
    run.event('linked-output-inputs.json', run.inputs)
    def verify():
        target = plain(run.root / run.m['decoded_target']).read_bytes()[0x5c4:0xb32]
        return verify_outputs(*(plain(run.work / n).read_bytes() for n in OUTPUTS), target)
    result = run.step('nine boundaries and raw OMF MAP equality', verify, 30)
    require(run.native_count == 2, 'exactly two native phases required')
    run.event('validation.json', result)
    return result

if __name__ == '__main__':
    raise SystemExit('Use the reviewed parent cold-pair adapter. This recipe does not launch native tools directly.')
