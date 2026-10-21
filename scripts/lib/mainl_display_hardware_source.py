"""Compose complete symbolic display/hardware providers in the current MAINL root."""
from pathlib import Path
from lib.mainl_staff_source import statements

NAMES = ('palette_black_in', 'palette_black_out', 'palette_show', 'palette_entry_rgb', 'vsync_wait', 'palette_white_in', 'palette_white_out', 'vsync', 'dos_setvect', 'graph_extmode', 'egc', 'grcg_boxfill', 'grcg_byteboxfill_x', 'gaiji_backup', 'gaiji_entry_bfnt', 'gaiji_read', 'gaiji_write', 'graph_400line', 'graph_clear', 'graph_copy_page')

PROVIDER_PATHS = {'palette_black_in': 'libs/master.lib/palette_black_in.asm', 'palette_black_out': 'libs/master.lib/palette_black_out.asm', 'palette_show': 'libs/master.lib/palette_show.asm', 'palette_entry_rgb': 'libs/master.lib/palette_entry_rgb.asm', 'vsync_wait': 'libs/master.lib/vsync_wait.asm', 'palette_white_in': 'libs/master.lib/palette_white_in.asm', 'palette_white_out': 'libs/master.lib/palette_white_out.asm', 'vsync': 'libs/master.lib/vsync.asm', 'dos_setvect': 'libs/master.lib/dos_setvect.asm', 'graph_extmode': 'libs/master.lib/graph_extmode.asm', 'egc': 'libs/master.lib/egc.asm', 'grcg_boxfill': 'libs/master.lib/grcg_boxfill.asm', 'grcg_byteboxfill_x': 'libs/master.lib/grcg_byteboxfill_x.asm', 'gaiji_backup': 'libs/master.lib/gaiji_backup.asm', 'gaiji_entry_bfnt': 'libs/master.lib/gaiji_entry_bfnt.asm', 'gaiji_read': 'libs/master.lib/gaiji_read.asm', 'gaiji_write': 'libs/master.lib/gaiji_write.asm', 'graph_400line': 'libs/master.lib/graph_400line.asm', 'graph_clear': 'libs/master.lib/graph_clear.asm', 'graph_copy_page': 'libs/master.lib/graph_copy_page.asm'}

def compose(root_asm, providers, maintained):
    """Require all 20 providers, preserving every token and include position."""
    if set(providers) != set(NAMES) or set(maintained) != set(NAMES):
        raise ValueError("complete display/hardware provider set required")
    root = root_asm.replace(b"\r\n", b"\n")
    generated = {}
    for name in NAMES:
        old = ("include " + PROVIDER_PATHS[name]).encode()
        path = "src/mainl/display_hardware/" + name + ".asm"
        new = ("include " + path).encode()
        if root.count(old) != 1 or new in root:
            raise ValueError("display/hardware include boundary missing, duplicated or already consumed: " + name)
        body = maintained[name].replace(b"\r\n", b"\n")
        if statements(body) != statements(providers[name]):
            raise ValueError("complete display/hardware source statements differ: " + name)
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
