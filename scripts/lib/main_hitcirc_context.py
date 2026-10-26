"""Detach remaining reference context around native cleanup/transition TUs.

The graphics provider retains nine unowned context bytes. These are byte/layout gates;
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


# Three complete owners; no padding or shared-tail prefix receives credit.
GRAPHICS_PARTITION = [
    (0x1C9C, 27, "th03-main-playfield-fill"),
    (0x1CB7, 7, None),
    (0x1CBE, 87, "th03-main-gauge-adapter-restore"),
    (0x1D15, 1, None),
    (0x1D16, 93, "th03-main-gauge-bar-fill"),
    (0x1D73, 1, None),
]
GRAPHICS_OWNERS = {owner for _, _, owner in GRAPHICS_PARTITION if owner}
GRAPHICS_PUBLICS = [
    (0, "_round_playfield_clear"), (0, "sub_B37C"),
    (28, "_hud_gauge_highlight_fill"), (28, "sub_B398"),
    (34, "_bomb_bg_fill"), (34, "sub_B39E"),
    (38, "_hud_gauge_highlights_restore"), (38, "sub_B3A2"),
    (122, "_hud_gauge_bar_fill"), (122, "sub_B3F6"),
]


def graphics_ownership(unit, units):
    """Fixed gf_ctx provider/context partition, not a general split-owner policy."""
    need(unit["id"] in GRAPHICS_OWNERS and unit["object"] == "gf_ctx"
         and unit["source"] == "src/main/graphics/round_fill_context.asm"
         and unit["map_module"] == "th03/gf_ctx.asm", "unexpected graphics owner")
    cursor, expected = 0x1C9C, []
    for start, size, owner in GRAPHICS_PARTITION:
        need(start == cursor and size > 0, "graphics partition gap or overlap")
        cursor += size
        if owner:
            expected.append((start, size, owner))
    need(cursor == 0x1D74, "complete graphics provider required")
    actual = []
    for peer in units:
        for extent in peer.get("code_extents", [peer]):
            start = extent["start"]
            if extent.get("segment", peer.get("segment", 0x18FE)) == 0x96E and start < cursor and start + extent["size"] > 0x1C9C:
                actual.append((start, extent["size"], peer["id"]))
    need(sorted(actual) == expected, "graphics owned/context partition differs")
    extent, = unit["code_extents"]
    need((extent["segment"], extent["map_segment"], extent["map_group"], extent["map_acbp"])
         == (0x96E, "HITCIRC_TEXT", "MAIN_01", 48), "graphics owner frame differs")
    return dict(extent=dict(extent, start=0x1C9C, size=216),
                owners=sorted(GRAPHICS_OWNERS), functions=[],
                partition=[dict(start=s, size=n, owner=o) for s, n, o in GRAPHICS_PARTITION])


def graphics_provider(work, target, candidate):
    """Bind the unchanged complete provider and known real entry dependencies."""
    import capstone
    from probe_th03_main_bomb_rikako_cpp import code_bytes

    raw = (work / "obj/th03/gf_ctx.obj").read_bytes()
    description = describe_omf(raw)
    segments = [s for s in segment_definitions(raw) if s["size"]]
    need(description["valid"] and description["translator_comments"] == ["Turbo Assembler  Version 5.0"]
         and [(s["index"], s["name"], s["class"], s["size"]) for s in segments]
         == [(6, "HITCIRC_TEXT", "CODE", 216)], "complete graphics OMF differs")
    records = parse_omf(raw)
    need([r.data.hex() for r in records if r.name == "FIXUPP"] == ["c4cc5601"],
         "literal mask OFFSET16 fixup differs")
    need([r.data for r in records if r.name == "EXTDEF"] == [bytes([21]) + b"_hud_gauge_left_masks" + bytes([0])],
         "sole mask external differs")
    code, chunks = code_bytes(raw, 6)
    need([r["size"] for r in chunks] == [216] and code_publics(raw, 6) == GRAPHICS_PUBLICS,
         "complete graphics LEDATA/publics differ")
    need(code[0xCC:0xCE] == bytes(2), "unlinked mask addend differs")
    map_text = (work / "obj/th03/main.map").read_text().replace(chr(92), "/")
    need(len(re.findall(r"(?m)^\s*096E:1C9C\s+00D8\s+C=CODE\s+S=HITCIRC_TEXT\s+G=MAIN_01\s+M=th03/gf_ctx\.asm\s+ACBP=48\s*$", map_text)) == 1,
         "full graphics MAP contribution differs")
    for offset, name in GRAPHICS_PUBLICS:
        need(len(re.findall(rf"(?m)^\s*096E:{0x1C9C + offset:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$", map_text)) == 2,
             "both graphics public tables required: " + name)
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    decoder.detail = True
    incoming = [(0x9A49, 0xB37C), (0x9A5A, 0xB37C), (0xC839, 0xB3A2),
                (0xC87A, 0xB398), (0xC8BA, 0xB398), (0xC91E, 0xB3F6),
                (0xC953, 0xB3F6), (0xC9A3, 0xB3F6), (0xC9F3, 0xB3F6),
                (0x1840A, 0xB39E), (0x187AF, 0xB39E), (0x18C04, 0xB39E),
                (0x18E11, 0xB39E), (0x148FF, 0xB39E), (0x1522B, 0xB39E),
                (0x17202, 0xB39E), (0xB5D3, 0xB39E), (0xB5DB, 0xB39E)]
    for image in (target, candidate):
        linked = image.program_image[0xB37C:0xB454]
        need(len(linked) == 216 and linked[:0xCC] == code[:0xCC]
             and linked[0xCE:] == code[0xCE:] and linked[0xCC:0xCE] == bytes.fromhex("4c06"),
             "graphics source-object-linked mapping differs")
        need(not [r for r in image.relocations if 0xB37C <= r.linear < 0xB454],
             "graphics MZ relocations must be empty")
        for site, destination in incoming + [(0xB39B, 0xB37F), (0xB39E, 0xB37C)]:
            instruction = next(decoder.disasm(image.program_image[site:site + 7], site - 0x96E0))
            need(instruction.mnemonic in {"call", "lcall", "jmp"}
                 and all(o.type == capstone.x86.X86_OP_IMM for o in instruction.operands),
                 "known graphics transfer differs")
            operands = [o.imm for o in instruction.operands]
            reached = 0x96E0 + operands[0] if len(operands) == 1 else operands[0] * 16 + operands[1]
            need(reached == destination, "known graphics entry dependency differs")
    return dict(provider_bytes=216, owned_instruction_bytes=207, unowned_context_bytes=9,
                ordered_mz_relocations=0, known_incoming_edges=incoming,
                shared_context_edge=[0xB39B, 0xB37F],
                physical_records=[dict(kind=r.name, offset=r.offset, data_hex=r.data.hex(), checksum=r.checksum)
                                  for r in records if r.name in {"LEDATA", "FIXUPP"}],
                table_data_owned=False, context_unreachable_claim=False)
