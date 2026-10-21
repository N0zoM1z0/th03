"""Compose maintained symbolic snow/staff includes without altering their tokens."""
import re
from lib.mainl_graphics_source import generate as graphics_generate, replace_once

FRAGMENTS = {"snow": ("MAINL_SNOW_TEXT", "src/mainl/staff/snow.asm", 443),
             "staff": ("MAINL_STAFF_TEXT", "src/mainl/staff/staff.asm", 2541)}


def statements(raw):
    """Keep every lexical token, case, quoted byte and statement boundary.

    Only comments and horizontal whitespace are ignored. This is a source
    equivalence check, never executable/OMF normalization.
    """
    text = raw.replace(b"\r\n", b"\n")
    tokens = re.findall(rb"'[^'\n]*'|\"[^\"\n]*\"|;[^\n]*|\n|[^\s;]+", text)
    rows, row = [], []
    for token in tokens:
        if token.startswith(b";"):
            continue
        if token == b"\n":
            if row:
                rows.append(tuple(row))
                row = []
        else:
            row.append(token)
    if row:
        rows.append(tuple(row))
    return tuple(rows)


def fragment_body(raw, segment):
    begin = (segment + " segment byte public 'CODE' use16\n").encode()
    end = (segment + " ends").encode()
    if raw.count(begin) != 1 or raw.count(end) != 1:
        raise ValueError("fragment segment boundary is not unique")
    a = raw.index(begin) + len(begin)
    b = raw.index(end, a)
    return raw[a:b]


def generate(root_asm, graphics, fragments):
    if set(fragments) != set(FRAGMENTS):
        raise ValueError("complete snow/staff fragment set required")
    generated = graphics_generate(root_asm, graphics)
    root = generated["th03_mainl.asm"].replace(b"\r\n", b"\n")
    for name, (segment, path, size) in FRAGMENTS.items():
        body = fragment_body(root, segment)
        maintained = fragments[name].replace(b"\r\n", b"\n")
        if statements(body) != statements(maintained):
            raise ValueError("maintained " + name + " full source tokens differ")
        root = replace_once(root, body, ("include " + path + "\n").encode())
        generated[path] = maintained.replace(b"\n", b"\r\n")
    generated["th03_mainl.asm"] = root.replace(b"\n", b"\r\n")
    return generated
