"""Current natural player producers; historical unit recipes remain unchanged.

The complete player core, round-result functions, and active shots form three
ordinary TC4 translation units. Literal records, publics, MAP allocation and
all linked bytes/relocations are checked without normalizing native output.
"""
import re

from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions, code_bytes, omf_index
from probe_th03_main_boss_marisa_cpp import code_publics

RETIRED = {"player_m.obj", "p_hyper.obj", "state.obj", "main_010.obj", "shotroot.obj", "p_shot.obj"}
PRODUCERS = [{'object': 'core',
  'source': 'src/main/player/core.cpp',
  'start': 16372,
  'size': 3135,
  'segment': 'MAIN_010_TEXT',
  'records': [1024, 1022, 1024, 65],
  'publics': [[0, '@PLAYER_POS_UPDATE_AND_CLAMP$QR7SPPOINT'],
              [74, '@PLAYER_MOVE$QUI'],
              [284, 'HYPER_STANDBY'],
              [309, 'HYPER_REIMU'],
              [371, 'HYPER_MIMA'],
              [437, 'HYPER_MARISA'],
              [504, 'HYPER_ELLEN'],
              [551, 'HYPER_KOTOHIME'],
              [613, 'HYPER_CHIYURI'],
              [675, 'HYPER_YUMEMI'],
              [737, 'HYPER_KANA'],
              [799, 'HYPER_RIKAKO'],
              [879, '@PLAYER_STATE_UPDATE$QUIP14PLAYER_STUFF_T'],
              [1985, '@PLAYER_RENDER$QP14PLAYER_STUFF_T'],
              [2116, '@PLAYER_OVERLAY_RENDER$QP14PLAYER_STUFF_T'],
              [2325, '@PLAYER_KNOCKBACK_UPDATE$QP14PLAYER_STUFF_T'],
              [2476, 'PLAYER_BOMB'],
              [2595, '@PLAYER_HITTEST$QI'],
              [2817, '@PLAYERS_HIT_DAMAGE_UPDATE$QR14PLAYER_STUFF_T'],
              [2935, '@story_skill_decrement$qv'],
              [2962, '@stage_prepare_shot_sprites$qv']]},
 {'object': 'results',
  'source': 'src/main/round/results.cpp',
  'start': 19507,
  'size': 1060,
  'segment': 'P_SHOT_TEXT',
  'records': [1018, 42],
  'publics': [[0, '@round_objects_and_counters_reset$qv'],
              [72, '@ROUND_RESULT_NUMBER_PUT$QIII'],
              [223, '@round_match_result_render$qv']]},
 {'object': 'shots',
  'source': 'src/main/player/shots.cpp',
  'start': 20567,
  'size': 449,
  'segment': 'P_SHOT_TEXT',
  'records': [449],
  'publics': [[0, '@player_shots_add$qv'], [264, '@shots_update$qv'], [307, '@shots_render$qv']]}]


def need(value, message):
    if not value:
        raise ValueError("player composition: " + message)


def replaced_contribution(line):
    """Only the six old or three new complete positive MAP contributions."""
    row = re.fullmatch(r"\s*096E:([0-9A-Fa-f]{4})\s+([0-9A-Fa-f]+)\s+C=CODE\s+S=(\S+)\s+G=MAIN_01\s+M=(\S+)\s+ACBP=28\s*", line.replace(chr(92), "/"))
    if not row:
        return False
    key = (int(row[1], 16), int(row[2], 16), row[3], row[4])
    old = {
        (0x3FF4, 284, "PLAYER_M_TEXT", "th03/player_m.cpp"),
        (0x4110, 595, "MAIN_010_TEXT", "th03/p_hyper.cpp"),
        (0x4363, 1716, "MAIN_010_TEXT", "src/main/player/state.cpp"),
        (0x4A17, 367, "MAIN_010_TEXT", "th03/main_010.cpp"),
        (0x4B86, 1497, "P_SHOT_TEXT", "src/main/player/shotroot.cpp"),
        (0x515F, 185, "P_SHOT_TEXT", "th03/p_shot.cpp"),
    }
    current = {(p["start"], p["size"], p["segment"], p["source"]) for p in PRODUCERS}
    return key in old | current


def verify(work, target, candidate):
    map_text = (work / "obj/th03/main.map").read_text().replace(chr(92), "/")
    observations = []
    cursor = 0x3FF4
    for producer in PRODUCERS:
        need(producer["start"] == cursor, "complete producer coverage has a gap")
        cursor += producer["size"]
        raw = (work / ("obj/th03/" + producer["object"] + ".obj")).read_bytes()
        description = describe_omf(raw)
        need(description["valid"] and description["translator_comments"] == ["TC86 Borland C++ 4.02"],
             "valid native TC4 object required")
        segments = [s for s in segment_definitions(raw) if s["size"]]
        need([(s["name"], s["class"], s["size"]) for s in segments]
             == [(producer["segment"], "CODE", producer["size"])], "CODE or private DATA/BSS differs")
        segment = segments[0]
        definition = [r for r in parse_omf(raw) if r.name == "SEGDEF"][segment["index"] - 1]
        need(definition.data[0] == 0x28, "ordinary BYTE/PUBLIC/USE16 code required")
        need([list(p) for p in code_publics(raw, segment["index"])] == producer["publics"],
             "complete native public set differs")
        need([r["size"] for r in code_bytes(raw, segment["index"])[1]] == producer["records"],
             "native record partition differs")
        pattern = (rf"(?m)^\s*096E:{producer['start']:04X}\s+{producer['size']:04X}\s+C=CODE"
                   rf"\s+S={producer['segment']}\s+G=MAIN_01\s+M={re.escape(producer['source'])}\s+ACBP=28\s*$")
        need(len(re.findall(pattern, map_text)) == 1, "literal MAP contribution differs")
        for offset, symbol in producer["publics"]:
            address = producer["start"] + offset
            need(len(re.findall(rf"(?m)^[ \t]*096E:{address:04X}[ \t]+(?![0-9A-F]+[ \t]+C=)(?:idle[ \t]+)?\S.*$", map_text)) == 2,
                 "both MAP public tables required: " + symbol)
        lo, hi = 0x96E0 + producer["start"], 0x96E0 + cursor
        need(candidate.program_image[lo:hi] == target.program_image[lo:hi], "complete linked body differs")
        vectors = [[(r.segment, r.offset) for r in image.relocations if lo <= r.linear < hi]
                   for image in (target, candidate)]
        need(vectors[0] == vectors[1], "literal scoped relocation order differs")
        records = []
        for index, record in enumerate(parse_omf(raw)):
            if record.name not in {"LEDATA", "FIXUPP"}:
                continue
            row = dict(index=index, file_offset=record.offset, kind=record.name,
                       data_hex=record.data.hex(), checksum=record.checksum)
            if record.name == "LEDATA":
                seg, pos = omf_index(record.data)
                row.update(segment=seg, offset=int.from_bytes(record.data[pos:pos+2], "little"),
                           size=len(record.data) - pos - 2)
            records.append(row)
        observations.append(dict(producer, ordered_relocations=vectors[1], physical_records=records))
    need(cursor == 0x5218, "complete player tail boundary differs")
    need(len(target.program_image) == len(candidate.program_image) == 124642, "whole payload size differs")
    differences = [i for i, (a, b) in enumerate(zip(target.program_image, candidate.program_image)) if a != b]
    need(differences == [0xEC2D], "whole payload changed outside the remaining input alignment byte")
    need(len(target.relocations) == len(candidate.relocations) == 1553
         and target.relocations == candidate.relocations, "complete literal MZ relocation vector differs")
    return dict(producers=observations, code_bytes=4644, functions=27, private_data_bytes=0,
                full_ordered_relocations=1553, full_order_equal=True, new_source_exact_credit=0,
                whole_product_exact=False, remaining_payload_differences=differences)
