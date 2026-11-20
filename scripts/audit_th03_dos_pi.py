#!/usr/bin/env python3
"""Check TH03 DOS links with moved CODE and DGROUP contributions."""

from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import defaultdict
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from typing import NamedTuple

import build_th03_package_current as package
from build_th03_runtime_linked_current import STAGE as BASELINE
from lib.omf import parse_omf
from lib.pc98 import MZImage, parse_mz

# Layout comparison and displacement screening adapted from the TH04 DOS PI audit.
ROOT, DRIVE = package.ROOT, package.DRIVE
LAYOUTS = {"even": (16, 32, 48), "alt": (32, 16, 64), "odd": (3, 7, 11)}
MAP_ROW = re.compile(
    r"\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4,8})\s+"
    r"C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)\s+ACBP=([0-9A-F]{2})"
)
ALIGNMENTS = {1: "byte", 2: "word", 3: "para", 4: "page", 5: "dword"}


class Contribution(NamedTuple):
    frame: int
    offset: int
    size: int
    kind: str
    name: str
    group: str
    module: str
    acbp: int

    @property
    def start(self) -> int:
        return self.frame * 16 + self.offset

    @property
    def owner(self) -> tuple[str, str, str, str]:
        return self.kind, self.name, self.group.lower(), self.module


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def map_rows(path: Path) -> list[Contribution]:
    rows = []
    for line in path.read_text(encoding="cp437").splitlines():
        match = MAP_ROW.fullmatch(line.rstrip())
        if match:
            frame, offset, size, kind, name, group, module, acbp = match.groups()
            rows.append(Contribution(int(frame, 16), int(offset, 16), int(size, 16),
                                     kind, name, group, module, int(acbp, 16)))
    if not rows:
        raise ValueError(f"no detailed TLINK contributions in {path}")
    return rows


def map_symbols(path: Path) -> dict[str, tuple[int, int]]:
    result = {}
    pattern = r"^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?(\S.*?)\s*$"
    for frame, offset, name in re.findall(pattern, path.read_text(encoding="cp437"), re.M):
        if " C=" in name:
            continue
        address = int(frame, 16), int(offset, 16)
        if name in result and result[name] != address:
            raise ValueError(f"ambiguous MAP symbol {name}")
        result[name] = address
    return result



def run(argv: list[str], cwd: Path) -> None:
    env = dict(os.environ, DISPLAY="", WAYLAND_DISPLAY="", WINEDEBUG="-all", MSDOS_PATH=r"C:\TC4\BIN")
    result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, timeout=120)
    log = result.stdout + result.stderr
    if result.returncode or re.search(rb"(?m)^(?:Error|Fatal):", log):
        raise ValueError(f"native tool failed ({result.returncode}): {log.decode(errors='replace')}")


def omf_module(data: bytes) -> str:
    name = parse_omf(data)[0].data
    return name[1:1 + name[0]].decode("cp437").lower()


def pad_objects(rows: list[Contribution], modules: list[str], work: Path,
                padding: dict[str, int], tasm: Path) -> dict[int, str]:
    """Insert padding after an existing definition, keeping segment discovery order."""
    definitions = defaultdict(list)
    for row in rows:
        if row.kind == "CODE" or (row.kind in {"DATA", "BSS"} and row.group.upper() == "DGROUP"):
            definitions[row.kind, row.name].append(row)
    contents = defaultdict(list)
    for (kind, name), definitions_in_map in definitions.items():
        if not any(row.size for row in definitions_in_map):
            continue
        known = [(modules.index(row.module.lower()), row.acbp)
                 for row in definitions_in_map if row.module.lower() in modules]
        if not known:
            continue
        index, acbp = min(known)
        if (acbp >> 2) & 7 != 2 or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            continue
        alignment = ALIGNMENTS[acbp >> 5]
        fill = {"CODE": "90h", "DATA": "0", "BSS": "?"}[kind]
        contents[index].extend([
            f"{name} segment {alignment} public '{kind}' use16",
            f"    db {padding[kind]} dup({fill})",
            f"{name} ends",
        ])
    if not contents:
        raise ValueError("no eligible CODE or DGROUP segments for padding")
    objects = {}
    for index, lines in sorted(contents.items()):
        stem = f"pi{index:05d}"
        source, obj = stem + ".asm", stem + ".obj"
        (work / source).write_text("\n".join([".386", *lines, "end", ""]), encoding="ascii")
        run(package.native() + [str(tasm), "/m", "/mx", "/kh32768", f"{source},{obj}"], work)
        parse_omf((work / obj).read_bytes())
        objects[index] = obj
    return objects


def direct_offsets(before: bytes, after: bytes,
                   pairs: list[tuple[Contribution, Contribution]]) -> dict:
    """Screen direct CS/DS displacements for review after moving their MAP owners."""
    from capstone import Cs, CS_ARCH_X86, CS_MODE_16
    from capstone.x86_const import X86_OP_MEM, X86_REG_CS, X86_REG_DS, X86_REG_INVALID

    dgroup = next((old.frame, new.frame) for old, new in pairs if old.group.upper() == "DGROUP")
    starts = [old.start for old, _ in pairs]
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    decoder.skipdata = True
    candidates = []
    screened = moved = 0
    for old, new in pairs:
        if old.kind != "CODE":
            continue
        for instruction in decoder.disasm(before[old.start:old.start + old.size], old.offset):
            if not instruction.id or instruction.disp_size != 2:
                continue
            for operand in instruction.operands:
                if operand.type != X86_OP_MEM or operand.mem.base or operand.mem.index:
                    continue
                segment = operand.mem.segment
                if segment not in (X86_REG_CS, X86_REG_DS, X86_REG_INVALID):
                    continue
                cs = segment == X86_REG_CS
                old_base, new_base = (old.frame, new.frame) if cs else dgroup
                offset = operand.mem.disp & 0xFFFF
                target = old_base * 16 + offset
                index = bisect_right(starts, target) - 1
                if index < 0:
                    continue
                old_target, new_target = pairs[index]
                if target >= old_target.start + old_target.size:
                    continue
                if cs and old_target.kind != "CODE":
                    continue
                if not cs and old_target.group.upper() != "DGROUP":
                    continue
                expected = (new_target.start + target - old_target.start - new_base * 16) & 0xFFFF
                at = new.start + instruction.address - old.offset + instruction.disp_offset
                actual = int.from_bytes(after[at:at + 2], "little")
                screened += 1
                if actual != expected:
                    candidates.append({
                        "address": f"{old.frame:04X}:{instruction.address:04X}",
                        "module": old.module, "operand": f"{instruction.mnemonic} {instruction.op_str}",
                        "target_module": old_target.module, "baseline": offset,
                        "shifted": actual, "expected": expected,
                    })
                elif actual != offset:
                    moved += 1
    return {"screened": screened, "moved": moved, "candidates": candidates}


def compare_layout(original: MZImage, shifted: MZImage, old_rows: list[Contribution],
                   new_rows: list[Contribution], synthetic: set[str]) -> tuple[dict, dict]:
    if not original.valid or not shifted.valid:
        raise ValueError("invalid MZ")
    new_by_owner = defaultdict(list)
    for row in new_rows:
        if row.size and row.module.lower() not in synthetic:
            new_by_owner[row.owner].append(row)
    moved = defaultdict(int)
    target_frames = defaultdict(set)
    pairs = []
    for old in old_rows:
        if old.size == 0:
            continue
        if not new_by_owner[old.owner]:
            raise ValueError(f"lost MAP contribution {old.owner}")
        new = new_by_owner[old.owner].pop(0)
        if old.size != new.size:
            raise ValueError(f"size changed for {old.owner}")
        pairs.append((old, new))
        target_frames[old.frame].add(new.frame)
        if old.offset != new.offset:
            moved[old.kind] += 1
    if any(new_by_owner.values()):
        raise ValueError("unexpected extra MAP contributions")
    if any(moved[kind] == 0 for kind in ("CODE", "DATA", "BSS")):
        raise ValueError(f"CODE, DATA, and BSS must all move within their frames: {dict(moved)}")
    # A public segment can have a paragraph frame of its own even when TLINK
    # reports its detailed contributions relative to a wider group.
    sections = []
    for rows in (old_rows, new_rows):
        section_starts = {}
        for row in sorted(rows, key=lambda row: row.start):
            section_starts.setdefault((row.kind, row.name), row.start)
        sections.append(section_starts)
    for section, old_start in sections[0].items():
        if section in sections[1]:
            target_frames[old_start >> 4].add(sections[1][section] >> 4)
    pairs.sort(key=lambda pair: pair[0].start)
    old_starts = [old.start for old, _ in pairs]
    expected = []
    old_image, new_image = original.program_image, shifted.program_image
    unmapped_frames = set()
    far_transfers = 0
    for relocation in original.relocations:
        site = relocation.linear
        index = bisect_right(old_starts, site) - 1
        if index < 0:
            raise ValueError(f"unowned baseline relocation at {site:#x}")
        old, new = pairs[index]
        if site + 2 > old.start + old.size:
            raise ValueError(f"unowned baseline relocation at {site:#x}")
        new_site = new.start + site - old.start
        expected.append(new_site)
        old_frame = int.from_bytes(old_image[site:site + 2], "little")
        new_frame = int.from_bytes(new_image[new_site:new_site + 2], "little")
        if new_frame not in target_frames[old_frame]:
            unmapped_frames.add((old_frame, new_frame))
        # Immediate far CALL/JMP has its offset directly before the MZ segment
        # relocation. Compare the full destination when it resolves to code.
        if old.kind != "CODE" or site - 3 < old.start or old_image[site - 3] not in (0x9A, 0xEA):
            continue
        old_destination = old_frame * 16 + int.from_bytes(old_image[site - 2:site], "little")
        destination_index = bisect_right(old_starts, old_destination) - 1
        if destination_index < 0:
            continue
        old_target, new_target = pairs[destination_index]
        if old_target.kind != "CODE" or old_destination >= old_target.start + old_target.size:
            continue
        new_destination = new_frame * 16 + int.from_bytes(new_image[new_site - 2:new_site], "little")
        if (old_image[site - 3] != new_image[new_site - 3]
                or new_destination != new_target.start + old_destination - old_target.start):
            raise ValueError(f"far transfer at load offset {site - 3:#x} lost its code target")
        far_transfers += 1
    actual = [entry.linear for entry in shifted.relocations]
    ordered_sites = sorted(actual)
    if any(site + 2 > len(new_image) for site in actual) or any(
        right < left + 2 for left, right in zip(ordered_sites, ordered_sites[1:])
    ):
        raise ValueError("invalid shifted MZ relocation sites")
    if sorted(expected) != ordered_sites:
        raise ValueError("MZ relocations no longer cover the same bytes within their owners")
    if expected != actual:
        raise ValueError("ordered MZ relocation sites changed within their owners")
    if unmapped_frames:
        values = ", ".join(f"{old:04X}->{new:04X}" for old, new in sorted(unmapped_frames))
        raise ValueError(f"MZ relocation frame pairs lack MAP ownership: {values}")
    direct = direct_offsets(old_image, new_image, pairs)
    layout = {"moved_offsets_by_class": dict(moved),
              "checked_contributions": len(pairs), "relocations": len(actual),
              "ordered_owner_sites_identical": expected == actual,
              "relocated_far_transfers": far_transfers,
              "direct_offsets_screened": direct["screened"], "direct_offsets_moved": direct["moved"],
              "direct_offsets_for_review": len(direct["candidates"])}
    return layout, direct

def consumed_input(name: str, cwd: Path) -> Path:
    if name[:3].lower() == "c:\\":
        cwd, name = DRIVE, name[3:]
    path = cwd / name.replace("\\", "/")
    return path if path.is_file() else path.parent / path.name.upper()


def replace_once(raw, old, new):
    if raw.count(old) != 1:
        raise ValueError(f"expected one native replacement: {old!r}")
    return raw.replace(old, new)


def build_pi_main(output, baseline):
    """Compile the isolated PI player core twice against the normal input pair."""
    import probe_th03_main_exatt_layout as overlay

    stage = output.name
    work = overlay.WORK / "probe" / stage
    source_path = overlay.SOURCES["core"]
    original_path = "src/main/player/stuff.inl"
    pi_path = "src/main/player/hittest_columns_pi.inl"
    closure = [source_path, overlay.ENTITY, overlay.BOSS_TEMPLATE, overlay.BACKGROUND_PHASE,
               *overlay.owner_inline_paths("core", stage), pi_path]
    sources = {path: (ROOT / path).read_bytes() for path in closure}
    original = sources[original_path]
    begin = b"\tinitial_mask_ready:\n"
    end = b"\trow_scan:\n"
    if original.count(begin) != 1 or original.count(end) != 1:
        raise ValueError("expected the original bounded column setup")
    prefix, tail = original.split(begin)
    _, suffix = tail.split(end)
    rounds = []
    for number in (1, 2):
        source_dir = work / f"r{number}"
        source_dir.mkdir(parents=True)
        dos_path = f"probe/{stage}/r{number}"
        for path, raw in sources.items():
            if path == source_path:
                raw = overlay.rooted_source("core", stage, number, raw)
            elif path == original_path:
                raw = prefix + sources[pi_path] + end + suffix
            else:
                raw = overlay.rooted_inline_source(path, stage, number, raw)
            destination = source_dir / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(raw.replace(b"\n", b"\r\n"))
        wrapper = overlay.rooted_wrapper("core", stage, number, overlay.wrapper_source("core"))
        (source_dir / "core.cpp").write_bytes(wrapper.replace(b"\n", b"\r\n"))
        run(package.dos() + ["tcc", "-c", "-I" + dos_path, "-I.", "-O", "-b-", "-3", "-Z", "-d",
                             "-DGAME=3", "-ml", "-DBINARY='M'", "-n" + dos_path + "/", dos_path + "/core.cpp"],
            overlay.WORK)
        obj = (source_dir / "core.obj").read_bytes()
        overlay.check_native_dependencies(obj, "core", stage, number, False, False)
        retained = (overlay.WORK / "probe" / "af1191e" / f"r{number}" / "core.obj").read_bytes()
        old_segments = [row for row in overlay.segment_definitions(retained) if row["class"] != "CODE"]
        new_segments = [row for row in overlay.segment_definitions(obj) if row["class"] != "CODE"]
        data = lambda raw: {k: v for k, v in overlay.payload(raw).items()
                            if k[0] in {row["index"] for row in old_segments}}
        if old_segments != new_segments or data(obj) != data(retained):
            raise ValueError("PI core changed storage outside CODE")
        native = output / f"r{number}"
        native.mkdir()
        base_round = baseline / f"r{number}"
        response = replace_once((base_round / "main.lnk").read_bytes(),
                                f"probe\\af1191e\\r{number}\\core.obj".encode(),
                                dos_path.replace("/", "\\").encode() + b"\\core.obj")
        for extension in ("exe", "map"):
            name = f"main.{extension}"
            response = replace_once(response, package.windows(base_round / name).encode(),
                                    package.windows(native / name).encode())
        rsp = native / "main.lnk"
        rsp.write_bytes(response)
        run(package.dos() + ["tlink", "@" + package.windows(rsp)], overlay.WORK)
        image = parse_mz((native / "main.exe").read_bytes())
        original_image = parse_mz((base_round / "main.exe").read_bytes())
        if not image.valid or len(image.relocations) != len(original_image.relocations):
            raise ValueError("invalid PI MAIN image or relocation count")
        rounds.append((obj, image))
    overlay.scope(rounds[1][0], rounds[0][0], "PI player core")
    if rounds[0][1].raw != rounds[1][1].raw:
        raise ValueError("independent PI MAIN links differ")
    (output / "pi-core.json").write_text(json.dumps({
        "sources": {path: sha(raw) for path, raw in sources.items()},
        "rounds": [package.pin(output / f"r{number}" / "main.exe") for number in (1, 2)],
    }, indent=2) + "\n")
    print("PI MAIN: two independent TC4 objects and complete MZ links agree", flush=True)
    return output / "r1"


def relink(product: str, output: Path, stage: Path, tasm: Path) -> dict:
    cwd = DRIVE / package.PRODUCTS[product][0]
    original = (stage / f"{product}.lnk").read_bytes()
    objects_text, files_text = original.decode("ascii").split(",", 1)
    objects = re.findall(r"[^\s+]+", objects_text)
    if objects[:3] != ["-c", "-s", "-E"]:
        raise ValueError(f"unexpected TLINK flags for {product}")
    objects = objects[3:]
    files = [field.strip() for field in files_text.split(",")]
    if len(files) != 3 or not files[2].lower().endswith("\\linked.lib"):
        raise ValueError(f"unexpected TLINK resources for {product}")
    object_paths = [consumed_input(name, cwd) for name in objects]
    object_bytes = [path.read_bytes() for path in object_paths]
    modules = [omf_module(data) for data in object_bytes]
    library = consumed_input(files[2], cwd)
    library_hash = sha(library.read_bytes())
    baseline_image = (stage / f"{product}.exe").read_bytes()
    baseline_map = (stage / f"{product}.map").read_bytes()
    rows = map_rows(stage / f"{product}.map")
    details = {}

    for layout in ("control", *LAYOUTS):
        work = output / layout
        work.mkdir(exist_ok=True)
        private = work / product
        private.mkdir()
        exe = work / f"{product}.exe"
        mapping = work / f"{product}.map"
        rsp = private / "link.rsp"
        selected, synthetic = objects, set()
        if layout != "control":
            padding = dict(zip(("CODE", "DATA", "BSS"), LAYOUTS[layout], strict=True))
            pads = pad_objects(rows, modules, private, padding, tasm)
            selected = []
            for index, name in enumerate(objects):
                selected.append(name)
                if index in pads:
                    selected.append(package.windows(private / pads[index]))
            synthetic = {Path(name).with_suffix(".asm").name for name in pads.values()}
        # Keep existing +/line continuations and casing in the unperturbed control.
        if layout == "control":
            command = original
            for name, destination in zip(files[:2], (exe, mapping), strict=True):
                command = command.replace(name.encode(), package.windows(destination).encode())
        else:
            command = (" ".join(["-c", "-s", "-E", *selected]) + ", " +
                       ", ".join([package.windows(exe), package.windows(mapping), files[2]]) + "\r\n").encode()
        rsp.write_bytes(command)
        run(package.dos() + ["tlink", "@" + package.windows(rsp)], cwd)
        if layout == "control":
            if exe.read_bytes() != baseline_image or mapping.read_bytes() != baseline_map:
                raise ValueError(f"{product}: unshifted complete EXE/MAP differs")
            continue
        linked = exe.read_bytes()
        layout_result, direct = compare_layout(parse_mz(baseline_image), parse_mz(linked),
                                                rows, map_rows(mapping), synthetic)
        details[layout] = {**layout_result, "exe_sha256": sha(linked), "map_sha256": sha(mapping.read_bytes()),
                           "direct_candidates": direct["candidates"]}
        print(product, layout, layout_result, flush=True)

    if any(path.read_bytes() != data for path, data in zip(object_paths, object_bytes, strict=True)):
        raise ValueError(f"{product}: retained object changed")
    if sha(library.read_bytes()) != library_hash:
        raise ValueError(f"{product}: retained library changed")
    return {"baseline_sha256": sha(baseline_image), "baseline_map_sha256": sha(baseline_map),
            "object_sha256": dict(zip(objects, map(sha, object_bytes), strict=True)),
            "library_sha256": library_hash, "layouts": details}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True, help="unused DOS-safe af<number><letter> stage")
    parser.add_argument("--only", nargs="+", choices=package.PRODUCTS, default=list(package.PRODUCTS))
    parser.add_argument("--original-collision", action="store_true", help="retain the original collision scan for diagnosis")
    args = parser.parse_args()
    if not re.fullmatch(r"af[0-9]{1,5}[a-z]", args.stage):
        parser.error("expected a DOS-safe stage")
    output = DRIVE / "TH03PI" / args.stage
    base = DRIVE / "TH03PKG" / BASELINE
    stage = base / "r1"
    receipt = json.loads((base / "runtime-linked.json").read_bytes())
    for product in args.only:
        for suffix in ("exe", "map"):
            name = f"{product}.{suffix}"
            if package.pin(stage / name) != receipt["rounds"][0]["outputs"][name]:
                raise ValueError(f"retained baseline differs from {BASELINE}: {name}")
    tools = json.loads((ROOT / package.STARTUP_CONFIG).read_text())["native_tools"]
    for declaration in tools.values():
        if package.pin(ROOT / declaration["path"])["sha256"] != declaration["sha256"]:
            raise ValueError(f"tool hash differs: {declaration['path']}")
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    with (ROOT / ".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        output.mkdir(parents=True)
        main_stage = stage
        if "main" in args.only and not args.original_collision:
            main_stage = build_pi_main(output, base)
        result = {}
        for product in dict.fromkeys(args.only):
            source = main_stage if product == "main" else stage
            result[product] = relink(product, output, source, ROOT / tools["tasm"]["path"])
        (output / "layout.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
