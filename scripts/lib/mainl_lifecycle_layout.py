"""Review complete MAINL lifecycle native objects and external plane storage."""

import hashlib
import re

from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics


OWNERS = (
    ("th03-mainl-decoded-linked-tail-planes", "planes", "vram_planes_set", "vram_planes_set()", "th01/vplanset.cpp", "obj/th01/vplanset.obj", 2, 41),
    ("th03-mainl-decoded-lifecycle-exit", "exit", "game_exit", "game_exit()", "th03/exit.cpp", "obj/th03/exit.obj", 0x1B0, 67),
    ("th03-mainl-decoded-lifecycle-init", "init", "GAME_INIT_MAIN", "game_init_main(const unsigned char far*)", "th03/initmain.cpp", "obj/th03/initmain.obj", 0x700, 62),
    ("th03-mainl-decoded-lifecycle-exit-to-main", "exit_to_main", "game_exit_from_mainl_to_main", "game_exit_from_mainl_to_main()", "th03/exitmain.cpp", "obj/th03/exitmain.obj", 0x98F, 40),
)


def need(value, message):
    if not value:
        raise ValueError("MAINL lifecycle layout: " + message)


def verify(work, target, candidate):
    text = (work / "obj/th03/mainl.map").read_text().replace(chr(92), "/")
    owners = []
    for unit, stem, symbol, map_public, wrapper, obj, offset, size in OWNERS:
        source = "src/mainl/linked_game/" + stem + ".cpp"
        raw = (work / obj).read_bytes()
        description = describe_omf(raw)
        need(description["valid"] and description["translator_comments"] == ["TC86 Borland C++ 4.02"], "native TC4 object")
        deps = [n.replace(chr(92), "/") for n in description["dependency_paths"]]
        need(wrapper in deps and source in deps, "actual maintained source dependency")
        need(segment_definitions(raw) == [
            dict(index=1, name="SHARED", **{"class": "CODE"}, overlay="", size=size),
            dict(index=2, name="_DATA", **{"class": "DATA"}, overlay="", size=0),
            dict(index=3, name="_BSS", **{"class": "BSS"}, overlay="", size=0)], "complete CODE and no private DATA/BSS")
        need([r.data[0] for r in parse_omf(raw) if r.name == "SEGDEF"] == [0x28, 0x48, 0x48],
             "BYTE CODE / WORD DATA/BSS, PUBLIC and USE16")
        need([r["size"] for r in code_bytes(raw, 1)[1]] == [size], "single complete native CODE record")
        public = "@" + symbol + ("$QNXUC" if stem == "init" else "$qv")
        need(code_publics(raw, 1) == [(0, public)], "complete OMF public ownership")
        need(len(re.findall(rf"(?m)^\s*0C7E:{offset:04X}\s+{size:04X}\s+C=CODE\s+S=SHARED"
                            rf"\s+G=\(none\)\s+M={re.escape(wrapper)}\s+ACBP=28\s*$", text)) == 1,
             "literal MAP allocation")
        need(len(re.findall(rf"(?m)^\s*0C7E:{offset:04X}\s+{re.escape(map_public)}\s*$", text)) == 2,
             "both literal MAP public tables")
        start, end = 0xC7E0 + offset, 0xC7E0 + offset + size
        a, b = target.program_image[start:end], candidate.program_image[start:end]
        need(len(a) == len(b) == size and a == b, "complete raw owner extent")
        pairs = []
        for image in (target, candidate):
            need(not any(r.linear < end and r.linear + 2 > start and not start <= r.linear <= end - 2
                         for r in image.relocations), "straddling relocation")
            pairs.append([[r.segment, r.offset] for r in image.relocations if start <= r.linear < end])
        need(pairs[0] == pairs[1], "literal ordered relocation pairs")
        owners.append(dict(unit_id=unit, source=source, object=obj, start=start, size=size,
                           coordinate_space="decoded-load", canonical_file_offset=None,
                           target_sha256=hashlib.sha256(a).hexdigest(), candidate_sha256=hashlib.sha256(b).hexdigest(),
                           ordered_relocations=pairs[0], argument_bytes=4 if stem == "init" else 0,
                           callee_pop_bytes=4 if stem == "init" else 0, private_data_bytes=0))
    for suffix, offset in (("B", 0x1C60), ("R", 0x1C64), ("G", 0x1C68), ("E", 0x1C6C)):
        need(len(re.findall(rf"(?m)^\s*0E3F:{offset:04X}\s+_VRAM_PLANE_{suffix}\s*$", text)) == 2,
             "external plane storage in both MAP public tables")
    need(sum(len(o["ordered_relocations"]) for o in owners) == 19, "all nineteen literal pairs")
    return owners
