"""Consume the complete symbolic PI decoder; do not edit executable bytes."""
from pathlib import Path
from lib.mainl_staff_source import statements

SOURCE = "src/mainl/formats/pi_decode.asm"
PROVIDER = b"include libs/master.lib/graph_pi_load_pack.asm"

def compose(root_asm, provider, maintained):
    """Change only one provider include in the existing maintained root carrier."""
    raw = root_asm.replace(b"\r\n", b"\n")
    marker = ("include " + SOURCE).encode()
    if raw.count(PROVIDER) != 1 or marker in raw:
        raise ValueError("PI include boundary is missing, duplicated or already consumed")
    maintained = maintained.replace(b"\r\n", b"\n")
    if statements(provider) != statements(maintained):
        raise ValueError("maintained PI complete symbolic statements differ")
    return {"th03_mainl.asm": raw.replace(PROVIDER, marker, 1).replace(b"\n", b"\r\n"),
            SOURCE: maintained.replace(b"\n", b"\r\n")}

def stage(destination, generated):
    """Refuse an existing destination before writing any generated source."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    for name, raw in generated.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as out:
            out.write(raw)
