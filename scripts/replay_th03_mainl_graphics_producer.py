#!/usr/bin/env python3
"""Read-only MAINL graphics producer proof; not a linker or exactness promotion."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
from lib.omf import parse_omf

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "src/mainl/formats/cdg_effects.cpp"
RECIPE = "config/th03_mainl_graphics_producer.json"
RECIPE_SHA = "805154cfcb4121e3404c9b6b8a51a61532b9c998602e8d93e835cb40e7ead43a"
PROOF = ".analysis/mainl-graphics-encoding-probe-20261021-v03"
OUTPUT = ".analysis/mainl-graphics-encoding-output-20261021-v03"
OBJECT = ".analysis/toolchain/wineprefix/drive_c/MGE03/probe.obj"
TARGET = ".analysis/th03-diet/sol-diet-restoration-20261006-b/mainl.exe"
OBJECT_SHA = "dbfe67ef668954fab6fadad72b776c8d8a6ed9861817d5d7ec2e42c155abd47b"
TARGET_SHA = "92600c8858bb407516cac6a9d77538ebdf0c33522c4f6bd9194d569eb927134a"
EXTERNALS = ["_cdg_slots", "_mainl_dissolve_alpha_enabled",
             "_mainl_dissolve_alpha_requested", "_mainl_dissolve_pattern",
             "CDG_PUT_NOALPHA_8", "CDG_PUT_8"]
BODIES = [("unput", 0, 0x24e6, 123, "CDG_UNPUT_FOR_UPWARDS_MOTION_E_8"),
          ("clear", 123, 0x2561, 21, "_mainl_clear_blue"),
          ("dissolve", 144, 0x2731, 211, "CDG_PUT_DISSOLVE_E_8")]
# Relocation-field contracts, not target addresses. Original file bytes remain intact.
FIELDS = [(0x134, 2, 4, 0), (0xee, 4, 6, 0), (0xde, 4, 5, 0),
          (0xcf, 2, 3, 0), (0xc8, 2, 2, 0), (0xab, 2, 1, 4),
          (0x9e, 2, 1, 2), (0x1b, 2, 1, 4), (0x0e, 2, 1, 2)]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def require(condition, message):
    if not condition:
        raise ValueError(message)

def parse_fields(raw):
    """Accept only this compiler's explicit external offset16/pointer32 forms."""
    fields = []
    pos = 0
    while pos < len(raw):
        require(pos + 4 <= len(raw), "truncated fixup")
        first, low, method = raw[pos:pos+3]
        kind = (first >> 2) & 15
        require(first & 0xc0 == 0xc0 and kind in (1, 3), "unexpected fixup location")
        offset = ((first & 3) << 8) | low
        width = 2 if kind == 1 else 4
        if method == 0x16:
            require(pos + 5 <= len(raw) and raw[pos+3] == 1, "non-DGROUP frame")
            external = raw[pos+4]
            pos += 5
        else:
            require(method == 0x56 and width == 4, "unexpected fixup method")
            external = raw[pos+3]
            pos += 4
        require(1 <= external <= len(EXTERNALS), "unknown external")
        fields.append((offset, width, external))
    return fields

def inspect_object(raw):
    records = parse_omf(raw)
    segments = [r.data for r in records if r.name == "SEGDEF"]
    require(segments == [bytes.fromhex("286301020301"),
                         bytes.fromhex("480000040501"),
                         bytes.fromhex("480000060701")], "CODE355 byte alignment / empty DATA BSS changed")
    data = [r.data for r in records if r.name == "LEDATA"]
    require(len(data) == 1 and data[0][:3] == b"\x01\x00\x00" and len(data[0]) == 358, "single complete CODE contribution")
    code = data[0][3:]
    ext = [r.data for r in records if r.name == "EXTDEF"]
    require(len(ext) == 1, "external record count")
    names = []
    pos = 0
    while pos < len(ext[0]):
        size = ext[0][pos]
        require(pos + size + 2 <= len(ext[0]) and ext[0][pos+size+1] == 0, "external type")
        names.append(ext[0][pos+1:pos+size+1].decode("ascii"))
        pos += size + 2
    require(names == EXTERNALS, "symbolic external contracts changed")
    pubs = [r.data for r in records if r.name == "PUBDEF"]
    require(len(pubs) == 3, "three complete public bodies")
    for pub, (_, offset, _, _, name) in zip(pubs, BODIES):
        expected = b"\x00\x01" + bytes([len(name)]) + name.encode() + struct.pack("<H", offset) + b"\x00"
        require(pub == expected, "public entry or near ABI name changed")
    fix = [r.data for r in records if r.name == "FIXUPP"]
    require(len(fix) == 1, "fixup record count")
    actual = parse_fields(fix[0])
    require(actual == [x[:3] for x in FIELDS], "ordered symbolic fixup fields changed")
    occupied = set()
    for offset, width, external, addend in FIELDS:
        require(int.from_bytes(code[offset:offset+width], "little") == addend, "symbolic field addend changed")
        span = set(range(offset, offset+width))
        require(not span & occupied, "overlapping fixups")
        occupied |= span
    require(code[119:123] == bytes.fromhex("c9c20600") and code[-4:] == bytes.fromhex("c9c20800"), "Pascal RET6/RET8 changed")
    return code, occupied

def replay(root=ROOT):
    recipe_raw = (root/RECIPE).read_bytes()
    require(sha(recipe_raw) == RECIPE_SHA, "producer recipe identity changed")
    recipe = json.loads(recipe_raw)
    for name, expected in recipe["proof_inputs_sha256"].items():
        require(sha((root/name).read_bytes()) == expected, "retained native proof changed: " + name)
    manifest = json.loads((root/PROOF/"manifest.json").read_text())
    start = json.loads((root/OUTPUT/"started.json").read_text())
    transition = json.loads((root/OUTPUT/"registry-transition.json").read_text())
    require(start["argv"] == manifest["native_argv"] == recipe["native_argv"], "native argument provenance changed")
    require(start["argv"][5:] == recipe["flags"], "documented compiler flags changed")
    require(start["wait_seconds"] == 90 and start["cleanup_seconds"] == 15 and transition["ok"], "native bounds or registry transition changed")
    source = (root/SOURCE).read_bytes()
    require(sha(source) == recipe["source_sha256"], "maintained source hash differs from native recipe")
    consumed = (root/PROOF/"probe.cpp").read_bytes()
    require(source.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n") == consumed, "maintained source not consumed by native producer")
    completion = json.loads((root/OUTPUT/"completion.json").read_text())
    native = json.loads((root/OUTPUT/"finished.json").read_text())
    require(completion["complete"] and completion["compiler_success"] and completion["native_invocations"] == 1 and completion["owned_lock_released"], "native producer incomplete")
    require(native["exit_code"] == 0 and not native["timeout"] and not native["cleanup_uncertain"] and not native["survivors"] and not native["poison"], "native execution or cleanup failed")
    raw = (root/OBJECT).read_bytes()
    require(sha(raw) == OBJECT_SHA, "retained raw object changed")
    code, fields = inspect_object(raw)
    target = (root/TARGET).read_bytes()
    require(sha(target) == TARGET_SHA and target[:2] == b"MZ", "decoded target lineage changed")
    header = struct.unpack_from("<H", target, 8)[0] * 16
    image = target[header:]
    bodies = []
    for name, start, entry, size, symbol in BODIES:
        original = image[0x95f*16+entry:0x95f*16+entry+size]
        candidate = code[start:start+size]
        compared = [i for i in range(size) if start+i not in fields]
        require(all(candidate[i] == original[i] for i in compared), "non-fixup instruction bytes differ: " + name)
        bodies.append(dict(name=name, source_symbol=symbol, bytes=size,
                           non_fixup_equal_bytes=len(compared),
                           entire_raw_equal=candidate == original))
    return dict(kind="mainl-graphics-source-producer", source_sha256=sha(source),
                consumed_source_sha256=sha(consumed), raw_object_sha256=sha(raw),
                bodies=bodies, code_bytes=355, non_fixup_target_equal_bytes=333,
                unresolved_external_field_bytes=22, symbolic_fixup_count=9,
                fixups=[dict(offset=a,width=b,symbol=EXTERNALS[c-1],addend=d) for a,b,c,d in FIELDS],
                source_consumed=True, source_installed_in_default_link=False,
                linked_raw_body_equality=False, ordered_mz_relocations_proved=False,
                exact_acceptance=False, source_progress_counts_changed=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = replay()
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as handle:
            handle.write(rendered)
    else:
        print(rendered, end="")

if __name__ == "__main__":
    main()
