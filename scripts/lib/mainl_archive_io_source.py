"""Compose complete symbolic archive/file providers in the current MAINL root."""
from pathlib import Path
from lib.mainl_staff_source import statements

NAMES = ('file_append', 'file_close', 'file_create', 'file_exist', 'file_read', 'file_ropen', 'file_seek', 'file_size', 'file_write', 'dos_axdx', 'dos_filesize', 'pfint21', 'pfopen', 'pfclose', 'pfgetc', 'pfread', 'pfrewind', 'pfseek', 'bcloser', 'bfill', 'bgetc', 'bopenr', 'bread', 'bseek', 'bseek_')

PROVIDER_PATHS = {'file_append': 'libs/master.lib/file_append.asm', 'file_close': 'libs/master.lib/file_close.asm', 'file_create': 'libs/master.lib/file_create.asm', 'file_exist': 'libs/master.lib/file_exist.asm', 'file_read': 'libs/master.lib/file_read.asm', 'file_ropen': 'libs/master.lib/file_ropen.asm', 'file_seek': 'libs/master.lib/file_seek.asm', 'file_size': 'libs/master.lib/file_size.asm', 'file_write': 'libs/master.lib/file_write.asm', 'dos_axdx': 'libs/master.lib/dos_axdx.asm', 'dos_filesize': 'libs/master.lib/dos_filesize.asm', 'pfint21': 'libs/master.lib/pfint21.asm', 'pfopen': 'th03/formats/pfopen.asm', 'pfclose': 'libs/master.lib/pfclose.asm', 'pfgetc': 'libs/master.lib/pfgetc.asm', 'pfread': 'libs/master.lib/pfread.asm', 'pfrewind': 'libs/master.lib/pfrewind.asm', 'pfseek': 'libs/master.lib/pfseek.asm', 'bcloser': 'libs/master.lib/bcloser.asm', 'bfill': 'libs/master.lib/bfill.asm', 'bgetc': 'libs/master.lib/bgetc.asm', 'bopenr': 'libs/master.lib/bopenr.asm', 'bread': 'libs/master.lib/bread.asm', 'bseek': 'libs/master.lib/bseek.asm', 'bseek_': 'libs/master.lib/bseek_.asm'}

def compose(root_asm, providers, maintained):
    """Require all 25 providers, preserving every token and include position."""
    if set(providers) != set(NAMES) or set(maintained) != set(NAMES):
        raise ValueError("complete archive/file provider set required")
    root = root_asm.replace(b"\r\n", b"\n")
    generated = {}
    for name in NAMES:
        old = ("include " + PROVIDER_PATHS[name]).encode()
        path = "src/mainl/archive_io/" + name + ".asm"
        new = ("include " + path).encode()
        if root.count(old) != 1 or new in root:
            raise ValueError("archive/file include boundary missing, duplicated or already consumed: " + name)
        body = maintained[name].replace(b"\r\n", b"\n")
        if statements(body) != statements(providers[name]):
            raise ValueError("complete archive/file source statements differ: " + name)
        root = root.replace(old, new, 1)
        generated[path] = body.replace(b"\n", b"\r\n")
    generated["th03_mainl.asm"] = root.replace(b"\n", b"\r\n")
    return generated

def stage(destination, generated):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    for name, raw in generated.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as out:
            out.write(raw)
