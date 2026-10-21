"""Compose complete symbolic resource providers in the current MAINL root."""
from pathlib import Path
from lib.mainl_staff_source import statements

NAMES = ('graph_gaiji_putc', 'graph_pack_put_8', 'graph_scrollup', 'graph_show', 'graph_pack_put_8_noclip', 'rottbl', 'bfnt_entry_pat', 'bfnt_extend_header_skip', 'bfnt_header_read', 'bfnt_header_analysis', 'super_free', 'super_entry_pat', 'super_entry_at', 'super_entry_bfnt', 'super_cancel_pat', 'super_put', 'dos_close', 'gdc_outpw', 'graph_pi_free', 'smem_release', 'smem_wget', 'bfnt_palette_set', 'dos_ropen')

def compose(root_asm, providers, maintained):
    """Require all 23 providers, preserving every token and include position."""
    if set(providers) != set(NAMES) or set(maintained) != set(NAMES):
        raise ValueError("complete resource provider set required")
    root = root_asm.replace(b"\r\n", b"\n")
    generated = {}
    for name in NAMES:
        old = ("include libs/master.lib/" + name + ".asm").encode()
        path = "src/mainl/resources/" + name + ".asm"
        new = ("include " + path).encode()
        if root.count(old) != 1 or new in root:
            raise ValueError("resource include boundary missing, duplicated or already consumed: " + name)
        body = maintained[name].replace(b"\r\n", b"\n")
        if statements(body) != statements(providers[name]):
            raise ValueError("complete resource source statements differ: " + name)
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
