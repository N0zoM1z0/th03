"""Detach remaining reference context around native cleanup/transition TUs.

The graphics ASM retains reference provenance. These are byte/layout gates;
the independent native auditor owns complete source/behavior acceptance.
"""

import hashlib
import re

from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

BODY_SHA256 = "f82838cb9be5935ce476f4d1e860c3af099bcbe556bf8f98386703b7be19f1b4"
PROCS = (("sub_B37C", "near"), ("sub_B398", "near"), ("sub_B39E", "far"),
         ("sub_B3A2", "near"), ("sub_B3F6", "near"), ("@GameExecl$qnxc", "far"),
         ("sub_B4A3", "near"), ("sub_B4A8", "near"), ("sub_B60A", "near"))
ALIASES = (("_round_playfield_clear", "near"), ("_hud_gauge_highlight_fill", "near"),
           ("_hud_gauge_highlights_restore", "near"), ("_hud_gauge_bar_fill", "near"),
           ("MAIN_EXEC", "far"), ("_stage_background_update_none", "near"),
           ("_stage_demo_finish", "near"), ("_bomb_bg_fill", "far"))
STORAGE = (("fp_1FBC0", "word"), ("byte_1FBC2", "byte"), ("byte_1FBC3", "byte"),
           *((f"word_1F{x:03X}", "word") for x in range(0xBC4, 0xBD4, 2)),
           ("trapezoid_hmask", "word"))


def need(value, message):
    if not value:
        raise ValueError("HITCIRC source grouping: " + message)


def detach(text):
    first = text.index("public _round_playfield_clear\n")
    last = text.index("sub_B60A\tendp", first) + len("sub_B60A\tendp")
    body = text[first:last]
    need(hashlib.sha256(body.encode("latin1")).hexdigest() == BODY_SHA256,
         "pinned remaining body differs")
    need(tuple(re.findall(r"^(\S+)\s+proc\s+(near|far)", body, re.M)) == PROCS,
         "nine original procedures required")
    declarations = dict(PROCS + ALIASES)
    del declarations["@GameExecl$qnxc"]
    text = text[:first] + "\n".join(f"extrn {n}:{t}" for n, t in declarations.items()) + text[last:]
    for old in ("public sub_B39E\n", "public _bomb_bg_fill\n_bomb_bg_fill = sub_B39E\n"):
        need(text.count(old) == 1, "original alias declaration differs")
        text = text.replace(old, "")
    for name, kind in STORAGE:
        directive = {"byte": "db", "word": "dw"}[kind]
        # trapezoid_hmask is defined by the existing master DATA include.
        if name != "trapezoid_hmask":
            need(len(re.findall(r"(?m)^" + name + r"\s+" + directive + r"\s+\?\s*$", text)) == 1,
                 "existing storage width differs: " + name)
    for old, new in (("sub_B4A3", "_stage_background_update_none"),
                     ("sub_B4A8", "_stage_demo_finish"),
                     ("sub_B60A", "_stage_demo_uncover")):
        text = re.sub(r"\b" + old + r"\b", new, text)
    bridge = ("public _playfield_transition_vertices,_transition_hmask\n"
              "_playfield_transition_vertices = word_1FBC4\n"
              "_transition_hmask = trapezoid_hmask\n")
    # All instructions now belong to native TUs. A trailing WORD-aligned empty
    # contribution would round up their odd end when hitcirc.obj links earlier.
    # The real segment still starts on WORD alignment through the order scaffold.
    marker = "HITCIRC_TEXT\tsegment\tword public 'CODE' use16"
    need(text.count(marker) == 1, "original empty segment declaration differs")
    text = text.replace(marker, marker.replace("word", "byte"))
    return bridge + "public " + ",".join(n for n, _ in STORAGE) + "\n" + text


def verify(work, target, candidate):
    metadata = (("gf_ctx", 0x1C9C, 216, "48"), ("execl", 0x1D74, 79, "28"),
                ("tr_ctx", 0x1DC3, 663, "28"))
    map_text = (work / "obj/th03/main.map").read_text().replace(chr(92), "/")
    root_raw = (work / "obj/th03/main.obj").read_bytes()
    need(describe_omf(root_raw)["valid"], "invalid root object")
    root_segment, = [s for s in segment_definitions(root_raw) if s["name"] == "HITCIRC_TEXT"]
    root_definition = [r for r in parse_omf(root_raw) if r.name == "SEGDEF"][root_segment["index"] - 1]
    need(root_segment["size"] == 0 and root_definition.data[0] == 0x28,
         "empty root HITCIRC must remain BYTE/PUBLIC/USE16")
    need(len(re.findall(r"(?m)^\s*096E:2217\s+0000\s+C=CODE\s+S=HITCIRC_TEXT"
                        r"\s+G=MAIN_01\s+M=th03_main\.asm\s+ACBP=28\s*$", map_text)) == 1,
         "empty root HITCIRC literal MAP contribution differs")
    for name, start, size, alignment in metadata:
        raw = (work / f"obj/th03/{name}.obj").read_bytes()
        description = describe_omf(raw)
        need(description["valid"], "invalid native object: " + name)
        segments = [s for s in segment_definitions(raw) if s["size"]]
        need([(s["name"], s["class"], s["size"]) for s in segments]
             == [("HITCIRC_TEXT", "CODE", size)], "CODE or private storage differs: " + name)
        module = f"th03/{name}." + ("asm" if name == "gf_ctx" else "cpp")
        pattern = (rf"(?m)^\s*096E:{start:04X}\s+{size:04X}\s+C=CODE\s+S=HITCIRC_TEXT"
                   rf"\s+G=MAIN_01\s+M={re.escape(module)}\s+ACBP={alignment}\s*$")
        need(len(re.findall(pattern, map_text)) == 1, "literal MAP contribution differs: " + name)
        lo = 0x96E0 + start
        need(candidate.program_image[lo:lo + size] == target.program_image[lo:lo + size],
             "raw context or C++ body differs: " + name)
        if name == "execl":
            need(description["translator_comments"] == ["TC86 Borland C++ 4.02"]
                 and code_publics(raw, segments[0]["index"]) == [(0, "MAIN_EXEC")],
                 "complete C++ producer ownership differs")
            vectors = [[(r.segment, r.offset) for r in image.relocations if lo <= r.linear < lo + size]
                       for image in (target, candidate)]
            need(vectors[0] == vectors[1] and len(vectors[0]) == 9,
                 "nine literal C++ relocations required")
            need(len(re.findall(r"(?m)^\s*096E:1D74\s+(?:idle\s+)?MAIN_EXEC\s*$", map_text)) == 2,
                 "both literal C++ public tables required")
        if name == "tr_ctx":
            need(description["translator_comments"] == ["TC86 Borland C++ 4.02"]
                 and code_publics(raw, segments[0]["index"]) == [
                     (0, "_stage_background_update_none"), (5, "_stage_demo_finish"),
                     (359, "_stage_demo_uncover")], "complete transition producer ownership differs")
            vectors = [[(r.segment, r.offset) for r in image.relocations if lo <= r.linear < lo + size]
                       for image in (target, candidate)]
            need(vectors[0] == vectors[1] and len(vectors[0]) == 16,
                 "sixteen literal transition relocations required")
    # One newly named existing DATA symbol; no general public/MAP relaxation.
    need(len(re.findall(r"(?m)^\s*1D56:064C\s+_hud_gauge_left_masks\s*$", map_text)) == 2,
         "both exact gauge-mask public rows required")
    masks = []
    for width in range(16):
        bits = (0xFFFF << (16 - width)) & 0xFFFF if width else 0xFFFF
        masks.extend((bits >> 8, bits & 255))
    expected_masks = bytes(masks)
    need(candidate.program_image[0x1DBAC:0x1DBCC] == expected_masks
         == target.program_image[0x1DBAC:0x1DBCC],
         "existing 16-WORD little-endian pixel-mask table differs")
    return dict(candidate_object="obj/th03/execl.obj", candidate_bytes=79,
                ordered_relocations=9, transition_candidate_bytes=663,
                transition_ordered_relocations=16, reference_context_bytes=216,
                review_scope="byte-and-native-layout", exact_acceptance=False,
                behavior_acceptance=False, private_data_bytes=0)
