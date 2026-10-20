"""Strict source-only encoding stage. Never assembles or edits target bytes."""
import hashlib
from pathlib import Path

def stage_bytes(source):
    if b"\r" in source:
        raise ValueError("Maintained source must use LF only; CR is ambiguous")
    text = source.decode("utf-8", errors="strict")
    if "\ufffd" in text or text.startswith("\ufeff"):
        raise ValueError("Replacement character or BOM is forbidden")
    if not text.endswith("\n"):
        raise ValueError("Maintained source must end in LF")
    sjis = text.encode("shift_jis", errors="strict")
    if sjis.decode("shift_jis", errors="strict") != text:
        raise ValueError("Non-bijective Shift-JIS mapping is forbidden")
    return sjis.replace(b"\n", b"\r\n")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("destination", type=Path)
    a = p.parse_args()
    data = stage_bytes(a.source.read_bytes())
    with a.destination.open("xb") as f:
        f.write(data)
    print(hashlib.sha256(data).hexdigest())
