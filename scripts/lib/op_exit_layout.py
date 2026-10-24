"""Complete native ownership/layout audit of OP's exit and plane producers."""

import hashlib
import re

from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics


OWNERS = (
    ("th03-op-decoded-configuration-exit_dos", "game_exit_to_dos", "src/op/core/exit_dos.cpp", "th02/exit_dos.cpp", "obj/th02/exit_dos.obj", 8, 25),
    ("th03-op-decoded-configuration-planes", "vram_planes_set", "src/op/hardware/vram_planes_set.cpp", "th01/vplanset.cpp", "obj/th01/vplanset.obj", 33, 41),
    ("th03-op-decoded-game-exit", "game_exit", "src/op/core/exit.cpp", "th03/exit.cpp", "obj/th03/exit.obj", 274, 67),
)


def need(value, message):
    if not value:
        raise ValueError("OP exit layout: " + message)


def verify(work, target, candidate):
    text = (work / "obj/th03/op.map").read_text().replace(chr(92), "/")
    owners = []
    for unit, name, source, wrapper, obj, offset, size in OWNERS:
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
        need([r["size"] for r in code_bytes(raw, 1)[1]] == [size], "complete single native CODE record")
        need(code_publics(raw, 1) == [(0, "@" + name + "$qv")], "complete OMF public ownership")
        pattern = (rf"(?m)^\s*0BEB:{offset:04X}\s+{size:04X}\s+C=CODE\s+S=SHARED"
                   rf"\s+G=\(none\)\s+M={re.escape(wrapper)}\s+ACBP=28\s*$")
        need(len(re.findall(pattern, text)) == 1, "literal MAP owner")
        need(len(re.findall(rf"(?m)^\s*0BEB:{offset:04X}\s+{name}\(\)\s*$", text)) == 2,
             "both MAP public tables")
        start, end = 0xBEB0 + offset, 0xBEB0 + offset + size
        a, b = target.program_image[start:end], candidate.program_image[start:end]
        need(len(a) == len(b) == size and a == b, "full raw owner extent")
        pairs = []
        for image in (target, candidate):
            need(not any(r.linear < end and r.linear + 2 > start and not start <= r.linear <= end - 2
                         for r in image.relocations), "relocation straddles owner")
            pairs.append([[r.segment, r.offset] for r in image.relocations if start <= r.linear < end])
        need(pairs[0] == pairs[1], "literal ordered relocation pairs")
        owners.append(dict(unit_id=unit, name=name, source=source, object=obj, start=start, size=size,
                           coordinate_space="decoded-load", canonical_file_offset=None,
                           target_sha256=hashlib.sha256(a).hexdigest(), candidate_sha256=hashlib.sha256(b).hexdigest(),
                           ordered_relocations=pairs[0], abi="far cdecl, no arguments; BP/BX/SI/DI/DS/SS preserved",
                           private_data_bytes=0))
    need(sum(len(o["ordered_relocations"]) for o in owners) == 11, "all eleven literal pairs")
    return owners
