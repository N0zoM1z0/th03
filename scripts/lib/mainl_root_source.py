"""Consume symbolic MAINL root procedures; never edit objects or target bytes."""
from lib.mainl_staff_source import statements

SOURCE = "src/mainl/root/root.asm"
BEGIN = b"include th03/formats/cdg_free_all.asm"
END = b"sub_9F8D\tendp"


def body(root_asm):
    raw = root_asm.replace(b"\r\n", b"\n")
    if raw.count(BEGIN) != 1 or raw.count(END) != 1:
        raise ValueError("root ownership boundary is not unique")
    start = raw.index(BEGIN)
    end = raw.index(END, start) + len(END)
    return raw[start:end]


def compose(root_asm, free_all, maintained):
    """Expand only the owned handwritten include, checking every statement.

    The caller supplies the already composed snow/staff carrier. CUTSCENE_TEXT,
    all provider declarations, DATA and later cutscene procdesc stay contextual.
    Comments and horizontal whitespace may change; opcode/operand tokens,
    labels, quoted data, local variable definitions and line boundaries may not.
    """
    raw = root_asm.replace(b"\r\n", b"\n")
    original = body(raw)
    expected = original.replace(BEGIN, free_all.replace(b"\r\n", b"\n").rstrip(b"\n"), 1)
    maintained = maintained.replace(b"\r\n", b"\n")
    if statements(expected) != statements(maintained):
        raise ValueError("maintained root full source tokens differ")
    marker = ("include " + SOURCE).encode()
    if marker in raw:
        raise ValueError("root include already consumed")
    raw = raw.replace(original, marker, 1)
    return {"th03_mainl.asm": raw.replace(b"\n", b"\r\n"),
            SOURCE: maintained.replace(b"\n", b"\r\n")}
