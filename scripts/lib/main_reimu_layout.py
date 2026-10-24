"""Bind the live flight/Reimu grouping to its two existing semantic owners.

The standalone scoped-replay TUs remain available. MAIN uses one 825-byte native
record followed by the 331-byte update/render record. No function credit is added.
"""

import re

from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics


PRODUCERS = (("ex_rfly", 0x11C7, 825), ("ex_reup", 0x1500, 331))
OWNERS = {"th03-main-exatt-shared-main06", "th03-main-exatt-reimu"}


def need(value, message):
    if not value:
        raise ValueError("flight/Reimu producer layout: " + message)


def verify(work, config, target, candidate):
    units = [u for u in config["units"] if u["id"] in OWNERS]
    need({u["id"] for u in units} == OWNERS, "both semantic owners required")
    extents = sorted((u["code_extents"][0] for u in units), key=lambda e: e["start"])
    need([(e["segment"], e["start"], e["size"]) for e in extents]
         == [(0x18FE, 0x11C7, 215), (0x18FE, 0x129E, 941)], "complete owner partition differs")
    functions = sorted((f for f in config["functions"] if f["object"] in {u["object"] for u in units}),
                       key=lambda f: f["offset"])
    cursor = 0x11C7
    for function in functions:
        need(function["segment"] == 0x18FE and function["offset"] == cursor,
             "function coverage has a gap or overlap")
        cursor += function["size"]
    need(len(functions) == 10 and cursor == 0x164B, "ten complete functions required")
    map_text = (work / "obj/th03/main.map").read_text().replace(chr(92), "/")
    public_count = 0
    for name, start, size in PRODUCERS:
        raw = (work / f"obj/th03/{name}.obj").read_bytes()
        description = describe_omf(raw)
        need(description["valid"] and description["translator_comments"] == ["TC86 Borland C++ 4.02"],
             "invalid or foreign native object: " + name)
        positive = [s for s in segment_definitions(raw) if s["size"]]
        need([(s["name"], s["class"], s["size"]) for s in positive]
             == [("MAIN_06_TEXT", "CODE", size)], "complete CODE or private DATA/BSS differs: " + name)
        segment = positive[0]["index"]
        definition = [r for r in parse_omf(raw) if r.name == "SEGDEF"][segment - 1]
        need(definition.data[0] == 0x28, "BYTE/PUBLIC/USE16 required: " + name)
        _, records = code_bytes(raw, segment)
        need([r["size"] for r in records] == [size], "one complete native CODE record required: " + name)
        pattern = (rf"(?m)^\s*18FE:{start:04X}\s+{size:04X}\s+C=CODE\s+S=MAIN_06_TEXT"
                   rf"\s+G=MAIN_06\s+M=th03/{name}\.cpp\s+ACBP=28\s*$")
        need(len(re.findall(pattern, map_text)) == 1, "literal MAP contribution differs: " + name)
        owned = [f for f in functions if start <= f["offset"] < start + size]
        expected = []
        for function in owned:
            need(function["offset"] + function["size"] <= start + size,
                 "function crosses producer boundary")
            symbol = ("@reimu_exatt_render_one$qv" if function["name"] == "reimu_exatt_render_one"
                      else "_exatt_fly_update" if function["name"] == "exatt_fly_update"
                      else function["name"].upper())
            expected.append((function["offset"] - start, symbol))
            map_symbol = "reimu_exatt_render_one()" if function["name"] == "reimu_exatt_render_one" else symbol
            need(len(re.findall(rf"(?m)^\s*18FE:{function['offset']:04X}\s+(?:idle\s+)?{re.escape(map_symbol)}\s*$",
                                map_text)) == 2, "both literal MAP public tables required")
        need(code_publics(raw, segment) == expected, "complete OMF public ownership differs: " + name)
        public_count += len(expected)
    lo, hi = 0x1A1A7, 0x1A62B
    need(candidate.program_image[lo:hi] == target.program_image[lo:hi], "complete linked CODE bytes differ")
    vectors = [[(r.segment, r.offset) for r in image.relocations if lo <= r.linear < hi]
               for image in (target, candidate)]
    need(vectors[0] == vectors[1] and len(vectors[0]) == 18, "eighteen literal relocation pairs required")
    return dict(objects=[p[0] for p in PRODUCERS], semantic_owners=sorted(OWNERS),
                functions=public_count, code_bytes=1156, code_record_sizes=[825, 331],
                literal_map_parts=2, literal_public_table_entries=20,
                ordered_relocations=18, private_data_bytes=0, new_source_exact_credit=0)
