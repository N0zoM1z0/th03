"""Check the complete physical partition of the maintained enemy producer.

Bytes and literal relocations are checked by the MAIN reviewer. This gate binds
all four native objects to their real CODE allocations and nineteen entrypoints;
empty DATA/BSS declarations cannot hide a new private allocation.
"""

from collections import Counter, defaultdict
import re

from lib.omf import describe_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics
from replay_th03_main_exact_units import normalized_code_extents, physical_objects


OBJECTS = {"eforna", "efornb", "eupda", "eupdb"}
RETIRED = {"e_ena.obj", "e_enb.obj"}


def need(value, message):
    if not value:
        raise ValueError("enemy producer layout: " + message)


def verify(work, config):
    unit, = [u for u in config["units"] if u["id"] == "th03-main-enemies"]
    producers = physical_objects(unit)
    need({p["object"] for p in producers} == OBJECTS, "four declared producers required")
    extents = normalized_code_extents(unit, config["segment"])
    functions = [f for f in config["functions"] if f["object"] == unit["object"]]
    need(len(functions) == 19, "nineteen reviewed functions required")
    map_text = (work / "obj/th03/main.map").read_text()
    allocations = defaultdict(dict)
    parts_by_object = defaultdict(list)
    for extent in extents:
        for part in extent["map_parts"]:
            pattern = (
                rf"(?m)^\s*{extent['segment']:04X}:{part['start']:04X}\s+{part['size']:04X}"
                rf"\s+C=CODE\s+S={re.escape(part['map_segment'])}"
                rf"\s+G={re.escape(part['map_group'])}\s+M={re.escape(part['map_module'])}"
                rf"\s+ACBP={part['map_acbp']}\s*$"
            )
            need(len(re.findall(pattern, map_text)) == 1,
                 "literal MAP contribution differs: " + part["object"])
            need(part["map_segment"] not in allocations[part["object"]],
                 "duplicate native segment allocation")
            allocations[part["object"]][part["map_segment"]] = part["size"]
            parts_by_object[part["object"]].append((extent, part))
    public_count = 0
    for producer in producers:
        name = producer["object"]
        raw = (work / producer["object_path"]).read_bytes()
        description = describe_omf(raw)
        need(description["valid"] and description["record_counts"].get("THEADR") == 1
             and description["record_counts"].get("MODEND") == 1
             and producer["translator_comment"] in description["translator_comments"],
             "invalid or foreign OMF: " + name)
        segments = segment_definitions(raw)
        positive = [s for s in segments if s["size"]]
        need(all(s["class"] == "CODE" for s in positive), "private DATA/BSS: " + name)
        need({s["name"]: s["size"] for s in positive} == dict(allocations[name])
             and len(positive) == len(allocations[name]), "complete CODE allocation differs: " + name)
        for extent, part in parts_by_object[name]:
            segment, = [s for s in positive if s["name"] == part["map_segment"]]
            publics = code_publics(raw, segment["index"])
            actual = Counter((part["start"] + offset,
                              symbol.split("$")[0].lstrip("@_").lower())
                             for offset, symbol in publics)
            owned = [f for f in functions if f.get("segment", config["segment"]) == extent["segment"]
                     and part["start"] <= f["offset"] < part["start"] + part["size"]]
            # TC4's observed 32-character public names and Pascal case are resolved
            # only for public-name metadata. Program bytes are never normalized.
            expected = Counter((f["offset"], f["name"][:32].lower()) for f in owned)
            need(actual == expected, "complete OMF public ownership differs: " + name)
            for function in owned:
                need(function["offset"] + function["size"] <= part["start"] + part["size"],
                     "function crosses producer boundary")
                pattern = (rf"(?m)^\s*{extent['segment']:04X}:{function['offset']:04X}"
                           rf"\s+(?:idle\s+)?{re.escape(function['map_public'])}\s*$")
                need(len(re.findall(pattern, map_text)) == 2,
                     "both literal MAP public tables required: " + function["name"])
            public_count += len(publics)
    need(public_count == len(functions), "complete public set required")
    return dict(objects=sorted(OBJECTS), functions=public_count, code_bytes=sum(
        sum(parts.values()) for parts in allocations.values()), private_data_bytes=0,
        literal_map_parts=sum(len(v) for v in parts_by_object.values()),
        literal_public_table_entries=public_count * 2)
