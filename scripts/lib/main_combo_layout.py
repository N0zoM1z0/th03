"""Bind early combo scoring and late helpers to the complete existing owner.

Explicit default CODE identity avoids adding a new empty segment to MAIN_04.
The far scoring entry retains its ABI when the near helper uses the same CS.
"""

from collections import Counter
import re

from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics
from replay_th03_main_exact_units import normalized_code_extents, physical_objects


OBJECTS = {"p_combo", "p_cmbhl"}
CODE_NAMES = {"P_COMBO_TEXT", "E_ENEMY_TEXT", "ENEMY_PUT", "E_EXPL_TEXT"}


def need(value, message):
    if not value:
        raise ValueError("combo producer layout: " + message)


def verify(work, config, target, candidate):
    unit, = [u for u in config["units"] if u["id"] == "th03-main-combo"]
    producers = physical_objects(unit)
    need({p["object"] for p in producers} == OBJECTS, "both declared source producers required")
    extents = normalized_code_extents(unit, config["segment"])
    need([(e["map_segment"], e["size"]) for e in extents]
         == [("P_COMBO_TEXT", 491), ("E_ENEMY_TEXT", 40), ("ENEMY_PUT", 103), ("E_EXPL_TEXT", 344)],
         "four complete CODE parts required")
    functions = [f for f in config["functions"] if f["object"] == "p_combo"]
    need(len(functions) == 5, "five reviewed functions required")
    map_text = (work / "obj/th03/main.map").read_text().replace(chr(92), "/")
    parts_by_object = {name: [] for name in OBJECTS}
    relocations = 0
    for extent in extents:
        part, = extent["map_parts"]
        parts_by_object[part["object"]].append((extent, part))
        lo = extent["segment"] * 16 + extent["start"]
        hi = lo + extent["size"]
        need(candidate.program_image[lo:hi] == target.program_image[lo:hi], "complete linked CODE differs")
        vectors = [[(r.segment, r.offset) for r in image.relocations if lo <= r.linear < hi]
                   for image in (target, candidate)]
        need(vectors[0] == vectors[1], "literal relocation pairs differ")
        relocations += len(vectors[0])
    need(relocations == 9, "nine literal relocation pairs required")
    public_count = 0
    for producer in producers:
        name = producer["object"]
        raw = (work / producer["object_path"]).read_bytes()
        description = describe_omf(raw)
        need(description["valid"] and description["translator_comments"] == ["TC86 Borland C++ 4.02"],
             "valid native TC4 object required: " + name)
        segments = segment_definitions(raw)
        need({s["name"] for s in segments if s["class"] == "CODE"} == CODE_NAMES,
             "default CODE identity or empty segment set differs: " + name)
        definitions = [r for r in parse_omf(raw) if r.name == "SEGDEF"]
        need(all(definitions[s["index"] - 1].data[0] == 0x28 for s in segments if s["class"] == "CODE"),
             "BYTE/PUBLIC/USE16 CODE required")
        allocations = {p["map_segment"]: p["size"] for e, p in parts_by_object[name]}
        positive = [s for s in segments if s["size"]]
        need(all(s["class"] == "CODE" for s in positive)
             and {s["name"]: s["size"] for s in positive} == allocations,
             "complete CODE or private DATA/BSS differs: " + name)
        for extent, part in parts_by_object[name]:
            segment, = [s for s in positive if s["name"] == part["map_segment"]]
            need([r["size"] for r in code_bytes(raw, segment["index"])[1]] == [part["size"]],
                 "single native record required for each CODE part")
            pattern = (rf"(?m)^\s*{extent['segment']:04X}:{part['start']:04X}\s+{part['size']:04X}"
                       rf"\s+C=CODE\s+S={re.escape(part['map_segment'])}\s+G=MAIN_04"
                       rf"\s+M={re.escape(part['map_module'])}\s+ACBP=28\s*$")
            need(len(re.findall(pattern, map_text)) == 1, "literal MAP allocation differs")
            owned = sorted((f for f in functions if part["start"] <= f["offset"] < part["start"] + part["size"]),
                           key=lambda f: f["offset"])
            cursor = part["start"]
            for function in owned:
                need(function["segment"] == extent["segment"] and function["offset"] == cursor,
                     "function coverage gap or overlap")
                cursor += function["size"]
                need(len(re.findall(rf"(?m)^\s*{extent['segment']:04X}:{function['offset']:04X}"
                                    rf"\s+(?:idle\s+)?{re.escape(function['map_public'])}\s*$", map_text)) == 2,
                     "both literal MAP public tables required")
            need(cursor == part["start"] + part["size"], "complete function coverage required")
            actual = Counter((part["start"] + offset, symbol.split("$")[0].lstrip("@_").lower())
                             for offset, symbol in code_publics(raw, segment["index"]))
            expected = Counter((f["offset"], f["name"][:32].lower()) for f in owned)
            need(actual == expected, "complete OMF public ownership differs")
            public_count += len(owned)
    need(public_count == 5, "complete public ownership required")
    return dict(objects=sorted(OBJECTS), functions=5, code_bytes=978, code_record_sizes=[491, 40, 103, 344],
                literal_map_parts=4, literal_public_table_entries=10, ordered_relocations=9,
                private_data_bytes=0, default_code_segment="P_COMBO_TEXT", new_source_exact_credit=0)
