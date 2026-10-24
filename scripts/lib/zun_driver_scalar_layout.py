"""Native producer review for 16 bounded driver scalar/register services.

The enclosing driver and its unresolved reserved spans remain context. This
grants no ownership to graphics, interrupts, parser dispatch or private DATA.
"""

import hashlib
import re

from lib.zun_driver_layout import review, resolve_native
from stage_th03_zun_driver import bodies, dos_text
from verify_th03_zun_driver_hybrid import COMMAND_PROCS, SCATTERED_PROCS, NAMES


SOURCES = {**{n: "src/zun/driver_services.inl" for n in NAMES},
           **{n: "src/zun/driver_numbers.inl" for n, _, _ in COMMAND_PROCS if n.startswith("sprite16_parse_")},
           **{n: "src/zun/driver_strings.inl" for n, _, _ in COMMAND_PROCS if n.startswith("sprite16_string_")},
           **{n: "src/zun/driver_format.inl" for n in ("sprite16_is_decimal_digit", "sprite16_is_ascii_lower", "sprite16_ascii_upper")}}
RANGES = sorted([(n, a, b - a) for n, a, b in (*COMMAND_PROCS, *SCATTERED_PROCS) if n in SOURCES]
                + [(n, 0x340 + i * 6, 6) for i, n in enumerate(NAMES)], key=lambda r: r[1])
OBJECT = "driver/driver.obj"


def need(value, message):
    if not value: raise ValueError("ZUN driver scalar layout: " + message)


def native_image(raw):
    return resolve_native(raw)


def verify(work, target, candidate, payload_offset, files, maintained):
    physical = review((work / OBJECT).read_bytes(), (work / "driver/driver.map").read_bytes())
    image, fixups, blocks = native_image((work / OBJECT).read_bytes())
    need(len(target) == len(candidate) == 4224 and image == target == candidate, "natural complete native COM equality")
    need(len(RANGES) == 16 and sum(size for _, _, size in RANGES) == 428, "complete bounded scalar/register scope")
    owners = []
    for name, start, size in RANGES:
        source = SOURCES[name]
        body = dos_text(bodies(maintained[source].decode())[name])
        slots = [n for n, raw in files.items() if n.startswith("driver/procs/") and raw == body]
        need(len(slots) == 1, "actual complete maintained procedure include")
        slot = slots[0]
        need((work / slot).read_bytes() == body, "consumed bounded include bytes")
        include = slot.removeprefix("driver/").encode()
        need(len(re.findall(rb"(?m)^include " + re.escape(include) + rb"\r?$", files["driver/driver.asm"])) == 1,
             "one physical producer include")
        raw = target[start - 256:start - 256 + size]
        owned_fixups = [f for f in fixups if start <= f["address"] < start + size]
        need(all(f["address"] + f["width"] <= start + size for f in owned_fixups), "fixup wholly inside source owner")
        owners.append(dict(unit_id="th03-zun-decoded-driver-" + name.removeprefix("sprite16_").replace("_", "-"),
            source=source, procedure=name, object=OBJECT, include=slot, start=start, size=size, origin="library",
            coordinate_space="decoded-payload-com", payload_option="-4", payload_file_offset=start - 256,
            decoded_file_offset=payload_offset + start - 256, canonical_file_offset=None, format="COM",
            argument_bytes=0, callee_pop_bytes=0, private_data_bytes=0, private_bss_bytes=0,
            abi="near register interface; caller stack; numeric CF / folded-compare flags", ordered_relocations=[],
            ordered_native_fixups=owned_fixups, target_sha256=hashlib.sha256(raw).hexdigest(), candidate_sha256=hashlib.sha256(raw).hexdigest()))
    selected = [f for o in owners for f in o["ordered_native_fixups"]]
    absolute = [f for f in selected if not f["self_relative"]]
    relative = [f for f in selected if f["self_relative"]]
    expected = [(0x343 + i * 6, value) for i, value in enumerate((0x1064, 0x1066, 0x1068, 0x106E, 0x106A, 0x106C))]
    expected += [(0xBAA, 0x1170), (0xBB5, 0x1173)]
    need([(f["address"], f["resolved"]) for f in absolute] == expected and all(f["width"] == 2 for f in selected),
         "eight literal ordered native state/string fixups")
    need([(f["address"], f["target_address"]) for f in relative] == [(0xAC9, 0xC40), (0xAD1, 0x69D), (0xB29, 0x689), (0xB7B, 0xC40), (0xBAD, 0xC52), (0xBB8, 0xC52), (0xC59, 0x69D), (0xC61, 0x69D)], "eight literal cross-contribution near-call fixups")
    need(physical["layout_profile"] == "native-paragraph-contributions" and physical["linker_zero_bytes"] == 71, "current natural driver layout")
    return dict(owners=owners, code_bytes=428, functions=16, private_data_bytes=0, private_bss_bytes=0,
                native_layout=physical, native_records=blocks, ordered_native_fixups=fixups,
                enclosing_driver_accepted=False, reserved_spans_owned=False, original_assembler_identified=False)
