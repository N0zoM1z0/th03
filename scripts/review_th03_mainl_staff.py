#!/usr/bin/env python3
"""Complete decoded STAFF_TEXT review with explicit foreign-interface models."""
import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import re
import struct
import subprocess
import tomllib

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation

ROOT = Path(__file__).resolve().parents[1]
REVISION = "b6ba5b0a529edbb31efdf8c0e939263804f8ee47"
CS, DS = 0x95f, 0xe3f
RANGES = [("staff_music", 0x233e, 68, ""), ("ending_dispatch", 0x2382, 280, ""),
          ("flake_put", 0x249a, 76, "6")]
SOURCES = ["th03_mainl.asm", "th03/staff.cpp", "th03/end/staff.cpp",
           "th03/sprites/flake.h", "planar.h", "pc98.h", "platform.h",
           "th03/score.hpp", "th03/common.h", "th02/score.h", "th03/resident.hpp",
           "th01/math/subpixel.hpp", "platform/x86real/flags.hpp", "x86real.h",
           "libs/master.lib/graph_pi_free.asm", "th03/snd/delaymea.cpp"]
# segment, offset: name, argument bytes, callee cleanup, return kind
IMPORTS = {(0xc7e, 0x6e2): ("SND_KAJA_INTERRUPT", 2, 2, "far"),
           (0xc7e, 0xa0): ("snd_load", 6, 0, "far"),
           (0, 0x536): ("PALETTE_BLACK_IN", 2, 2, "far"),
           (0xc7e, 0xc1c): ("SND_DELAY_UNTIL_MEASURE", 4, 4, "far"),
           (0, 0x57a): ("PALETTE_BLACK_OUT", 2, 2, "far"),
           (0xc7e, 0x950): ("CDG_FREE", 2, 2, "far"),
           (0, 0xfec): ("GRAPH_PI_FREE", 8, 8, "far"),
           (0, 0x17d0): ("PALETTE_SHOW", 0, 0, "far"),
           (0xc7e, 0x372): ("frame_delay", 2, 2, "far"),
           (0, 0xe72): ("GRAPH_CLEAR", 0, 0, "far"),
           (0, 0x1758): ("GRAPH_SHOW", 0, 0, "far"),
           (CS, 0xb3e): ("cutscene_script_load", 4, 4, "near"),
           (CS, 0x167e): ("cutscene_animate", 0, 0, "near"),
           (CS, 0xb84): ("cutscene_script_free", 0, 0, "near"),
           (CS, 0x2e1d): ("staff_animation_unreviewed", 0, 0, "near"),
           (CS, 0x21e2): ("regist_menu", 0, 0, "near"),
           (0, 0x1f20): ("TEXT_CLEAR", 0, 0, "far"),
           (0, 0xc96): ("GAIJI_RESTORE", 0, 0, "far"),
           (0xc7e, 0x1b0): ("game_exit", 0, 0, "far"),
           (0, 0x8e37): ("execl", 12, 0, "far")}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decode(image):
    cs = Cs(CS_ARCH_X86, CS_MODE_16)
    cs.detail = True
    rows, boundaries = [], set()
    for name, start, size, cleanup in RANGES:
        body = image[CS * 16 + start:CS * 16 + start + size]
        instructions = list(cs.disasm(body, start))
        if (sum(i.size for i in instructions) != size or not instructions or
                instructions[-1].mnemonic != "ret"):
            raise ValueError("incomplete STAFF body/near-return boundary")
        if instructions[-1].op_str != cleanup:
            raise ValueError("STAFF cdecl/Pascal return cleanup differs")
        boundaries.update(i.address for i in instructions)
        edges = []
        for i in instructions:
            if i.mnemonic.startswith(("j", "loop")) or i.mnemonic in ("call", "lcall"):
                if not i.operands or any(o.type != X86_OP_IMM for o in i.operands):
                    raise ValueError("unexpected indirect STAFF edge")
                if i.mnemonic == "lcall":
                    destination = tuple(o.imm for o in i.operands)
                else:
                    destination = (CS, i.operands[0].imm)
                edges.append(dict(instruction=i.address, kind=i.mnemonic, destination=destination))
        rows.append(dict(name=name, offset=start, size=size, body_sha256=sha(body),
                         instruction_count=len(instructions), return_cleanup=cleanup, edges=edges))
    for row in rows:
        for edge in row["edges"]:
            destination = edge["destination"]
            if edge["kind"] in ("call", "lcall"):
                if destination not in IMPORTS:
                    raise ValueError("STAFF call lacks an explicit reviewed interface")
                if IMPORTS[destination][3] != ("far" if edge["kind"] == "lcall" else "near"):
                    raise ValueError("STAFF import near/far ABI differs")
            elif (destination[1] not in boundaries or
                  not row["offset"] <= destination[1] < row["offset"] + row["size"]):
                raise ValueError("STAFF branch enters data or instruction operand")
    return rows


class Probe:
    """Relocate private MZ bytes, execute STAFF only, model every foreign call."""
    def __init__(self, mz, packed=1, credits=3, fail_interfaces=False):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INTR, UC_HOOK_INSN, UC_HOOK_MEM_WRITE
        from unicorn import x86_const as reg
        self.reg, self.uc = reg, Uc(UC_ARCH_X86, UC_MODE_16)
        self.load = 0x2000
        self.events, self.ports, self.writes, self.errors = [], [], [], []
        self.stopped, self.fail_interfaces = False, fail_interfaces
        uc = self.uc
        uc.mem_map(0, 0x100000)
        image = bytearray(mz.program_image)
        for relocation in mz.relocations:
            at = relocation.segment * 16 + relocation.offset
            struct.pack_into("<H", image, at, (struct.unpack_from("<H", image, at)[0] + self.load) & 0xffff)
        uc.mem_write(self.load * 16, bytes(image))
        self.data = (self.load + DS) * 16
        self.code = (self.load + CS) * 16
        self.stack = 0x40000
        for name, value in (("CS", self.load + CS), ("DS", self.load + DS), ("ES", 0x3333),
                            ("SS", 0x4000), ("BP", 0x7777), ("SI", 0x1357), ("DI", 0x2468),
                            ("EFLAGS", 0x202)):
            self.set_register(name, value)
        uc.mem_write(self.data + 0x21ea, struct.pack("<HH", 0, 0x5000))
        uc.mem_write(0x5000c, bytes([packed]))
        uc.mem_write(0x50036, bytes([credits]))
        self.filename_pointer = struct.unpack("<HH", uc.mem_read(self.data + 0xa5e, 4))
        self.initial_filename = self.cstring(*self.filename_pointer)
        imports_at = {(self.load + segment) * 16 + offset: key
                      for key in IMPORTS for segment, offset in [key]}
        def guard(callback, default=None):
            def run(*args):
                try:
                    return callback(*args)
                except Exception as error:
                    self.errors.append(str(error))
                    uc.emu_stop()
                    return default
            return run
        def code(uc, address, size, user):
            if address == self.code + 0xff00:
                self.stopped = True
                uc.emu_stop()
                return
            segment = self.register("CS") - self.load
            # Unicorn's code-hook IP reports a translated PC at some boundaries;
            # use the supplied physical address and pinned segment coordinates.
            offset = address - self.code
            key = imports_at.get(address)
            if key in IMPORTS:
                if segment != key[0]:
                    raise ValueError("STAFF import entered through a segment alias")
                name, count, cleanup, kind = IMPORTS[key]
                sp = self.register("SP")
                return_size = 4 if kind == "far" else 2
                words = struct.unpack("<" + "H" * ((return_size + count) // 2),
                                      uc.mem_read(self.stack + sp, return_size + count))
                arguments = list(words[return_size // 2:])  # stack order, not source order
                event = dict(name=name, stack_words=arguments)
                if name == "cutscene_script_load":
                    event["filename"] = self.cstring(*arguments).decode("ascii")
                if name == "execl":
                    event["path"] = self.cstring(*arguments[:2]).decode("ascii")
                    event["arg0"] = self.cstring(*arguments[2:4]).decode("ascii")
                    if arguments[4:] != [0, 0]:
                        raise ValueError("execl lacks the far NULL terminator")
                if name in ("cutscene_script_load", "snd_load", "execl"):
                    returned = 1 if name == "cutscene_script_load" else 0xffff
                    self.set_register("AX", returned if self.fail_interfaces or name == "execl" else 0)
                    event["returned_ax"] = self.register("AX")
                    if name == "execl":
                        event["modeled_exec_failure"] = True  # successful exec would not return
                self.events.append(event)
                self.set_register("SP", sp + return_size + cleanup)
                self.set_register("CS", words[1] if kind == "far" else self.load + CS)
                self.set_register("IP", words[0])
            elif segment != CS or not any(start <= offset < start + length for _, start, length, _ in RANGES):
                raise ValueError(f"CPU escaped the reviewed STAFF bodies/imports: {segment:04x}:{offset:04x} at {address:05x}")
        def interrupt(uc, number, user):
            raise ValueError("unexpected STAFF kernel interrupt")
        def output(uc, port, width, value, user):
            if port not in (0xa4, 0xa6) or width != 1:
                raise ValueError("unexpected STAFF port/width")
            self.ports.append([port, value])
        def input_port(uc, port, width, user):
            raise ValueError("unexpected STAFF input port")
        def write(uc, access, address, size, value, user):
            if address >= 0xa0000:
                if not 0xa8000 <= address < 0xb8010 or size != 2:
                    raise ValueError("STAFF write escaped modeled blue VRAM")
                self.writes.append([address - 0xa8000, size, value])
        uc.hook_add(UC_HOOK_CODE, guard(code))
        uc.hook_add(UC_HOOK_INTR, guard(interrupt))
        uc.hook_add(UC_HOOK_INSN, guard(output), None, 1, 0, reg.UC_X86_INS_OUT)
        uc.hook_add(UC_HOOK_INSN, guard(input_port, 0), None, 1, 0, reg.UC_X86_INS_IN)
        uc.hook_add(UC_HOOK_MEM_WRITE, guard(write))

    def register(self, name):
        return self.uc.reg_read(getattr(self.reg, "UC_X86_REG_" + name))

    def set_register(self, name, value):
        self.uc.reg_write(getattr(self.reg, "UC_X86_REG_" + name), value)

    def cstring(self, offset, segment):
        data = bytes(self.uc.mem_read(segment * 16 + offset, 64))
        if b"\0" not in data:
            raise ValueError("unterminated modeled filename")
        return data.split(b"\0", 1)[0]

    def run(self, entry, stack_words=()):
        self.set_register("SP", 0xfff0)
        self.uc.mem_write(self.stack + 0xfff0, struct.pack("<" + "H" * (1 + len(stack_words)), 0xff00, *stack_words))
        self.uc.emu_start(self.code + entry, 0x100000, count=10000)
        if self.errors or not self.stopped:
            raise ValueError(self.errors[0] if self.errors else "STAFF did not reach its reviewed return")
        if (self.register("SP") != 0xfff2 + 2 * len(stack_words) or self.register("BP") != 0x7777 or
                self.register("SI") != 0x1357 or self.register("DI") != 0x2468):
            raise ValueError("STAFF stack/callee-saved register contract differs")


def ending_case(mz, packed, credits, fail_interfaces=False):
    p = Probe(mz, packed, credits, fail_interfaces)
    p.run(0x2382)
    value = max(0, (packed - 1) // 2)
    expected = bytearray(p.initial_filename)
    if value >= 10:
        expected[1] = (expected[1] + value // 10) & 255
    expected[2] = (expected[2] + value % 10) & 255
    filename = p.cstring(*p.filename_pointer)
    extra = credits == 3 and packed < 15
    loads = [e["filename"] for e in p.events if e["name"] == "cutscene_script_load"]
    if (filename != expected or loads != [expected.decode("ascii")] + (["@99ED.TXT"] if extra else []) or
            p.uc.mem_read(0x50033, 1)[0] != 99 or p.uc.mem_read(0x5000c, 1)[0] != packed or
            p.uc.mem_read(0x50036, 1)[0] != credits or p.ports != [[0xa6, 0], [0xa4, 0]] +
            ([[0xa6, 1], [0xa6, 0], [0xa4, 0]] if extra else [])):
        raise ValueError("ending filename/stage/credit/port contract differs")
    names = [e["name"] for e in p.events]
    expected_names = (["CDG_FREE"] * 3 + ["GRAPH_PI_FREE", "PALETTE_SHOW", "frame_delay", "GRAPH_CLEAR", "GRAPH_SHOW",
                      "cutscene_script_load", "cutscene_animate", "cutscene_script_free", "staff_animation_unreviewed", "regist_menu"] +
                      (["GRAPH_CLEAR"] * 2 + ["cutscene_script_load", "cutscene_animate", "cutscene_script_free"] if extra else []) +
                      ["TEXT_CLEAR", "GAIJI_RESTORE", "game_exit", "execl"])
    if names != expected_names or p.events[-1].get("path") != "op" or p.events[-1].get("arg0") != "op":
        raise ValueError("ending import order/exec contract differs")
    if next(e for e in p.events if e["name"] == "frame_delay")["stack_words"] != [96]:
        raise ValueError("ending initial delay differs")
    return dict(packed=packed, credits=credits, modeled_interface_failure=fail_interfaces,
                filename=filename.decode("ascii"), extra_ending=extra,
                stage=p.uc.mem_read(0x50033, 1)[0], ports=p.ports, events=p.events,
                final_sp=p.register("SP"), final_ax=p.register("AX"))


def flake_case(mz, left, top, cel):
    p = Probe(mz)
    source = (0xa62 + ((cel & 65535) << 4)) & 65535
    pattern = [0x8001, 0x1248, 0xffff, 0, 0xaaaa, 0x5555, 0x80, 0xff00]
    p.uc.mem_write(p.data + source, struct.pack("<8H", *pattern))
    expected = bytearray(b"\x5a\xa5" * 32769)
    p.uc.mem_write(0xa8000, bytes(expected))
    p.run(0x249a, (cel & 65535, top & 65535, left & 65535))
    at, rotate = ((left >> 3) + top * 80) & 65535, left & 7
    writes = []
    for value in pattern:
        dots = ((value >> rotate) | (value << (16 - rotate))) & 65535
        value = struct.unpack_from("<H", expected, at)[0] | dots
        struct.pack_into("<H", expected, at, value)
        writes.append([at, 2, value])
        at = (at + 80) & 65535
    actual = bytes(p.uc.mem_read(0xa8000, len(expected)))
    if actual != expected or p.writes != writes or p.ports or p.events or p.register("ES") != 0xa800:
        raise ValueError("flake rotation/OR/stride/wrap/segment contract differs")
    return dict(left=left, top=top, cel=cel, constructed_sprite_offset=source,
                writes=p.writes, blue_vram_sha256=sha(actual), final_sp=p.register("SP"), final_es=p.register("ES"))


def runtime_matrix(mz):
    endings = [ending_case(mz, packed, credits) for packed in range(256) for credits in (2, 3)]
    failures = [ending_case(mz, packed, 3, True) for packed in (0, 14, 15, 255)]
    flakes = [flake_case(mz, 80 + bit, top, cel) for bit in range(8) for top in (-1, 0, 399, 400) for cel in range(4)]
    flakes += [flake_case(mz, *args) for args in [(-1, 0, -1), (-16, 0, 4), (640, 400, 0), (639, 399, 3)]]
    p = Probe(mz, fail_interfaces=True)
    p.run(0x233e)
    expected = [("SND_KAJA_INTERRUPT", [0x100]), ("snd_load", [0xa56, 0x2e3f, 0x600]),
                ("SND_KAJA_INTERRUPT", [0]), ("PALETTE_BLACK_IN", [1]),
                ("SND_DELAY_UNTIL_MEASURE", [64, 3]), ("PALETTE_BLACK_OUT", [1]),
                ("SND_KAJA_INTERRUPT", [0x100])]
    if [(e["name"], e["stack_words"]) for e in p.events] != expected or p.ports:
        raise ValueError("staff music/interface contract differs")
    return dict(ending_cases=endings, failed_interface_cases=failures, flake_cases=flakes,
                music_case=dict(events=p.events, final_sp=p.register("SP")))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    frozen = {}
    def read(path):
        frozen[path] = (ROOT / path).read_bytes()
        return frozen[path]
    config = tomllib.loads(read("config/th03_decoded_code_review.toml").decode())
    diet = tomllib.loads(read("config/th03_diet.toml").decode())
    for path in ("config/targets.toml", "scripts/review_th03_mainl_staff.py", "scripts/review_th03_decoded_code.py",
                 "scripts/lib/pc98.py", "scripts/lib/omf.py", "scripts/lib/targets.py"):
        read(path)
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-mainl")
    stored = read_verified_artifact(ROOT, artifact)
    entry = next(a for a in config["artifacts"] if a["id"] == "th03-mainl")
    decoded = read(entry["decoded_path"])
    restoration = json.loads(read(config["diet_receipt"]))
    replay = json.loads(read(config["replay_receipt"]))
    pin = next(a for a in diet["artifacts"] if a["id"] == "th03-mainl")
    lineage = next(o for o in restoration["observations"] if o["artifact"] == "th03-mainl")
    if (sha(decoded) != pin["decoded_sha256"] or sha(frozen[config["diet_receipt"]]) != config["diet_receipt_sha256"] or
            sha(frozen[config["replay_receipt"]]) != config["replay_receipt_sha256"] or
            lineage["stored"]["sha256"] != sha(stored) or lineage["decoded"]["sha256"] != sha(decoded) or
            not restoration["restoration_checks_pass"] or not restoration["canonical_targets_unchanged"] or
            not replay["pass"] or not replay["all_products_equal"] or
            restoration["reference_revision"] != REVISION or diet["reference_revision"] != REVISION or
            replay["reference_revision"] != config["reference_revision"] or config["reference_revision"] != REVISION):
        raise ValueError("MAINL STAFF stored/decoded/cached scaffold lineage differs")
    if [r["round"] for r in entry["rounds"]] != [1, 2]:
        raise ValueError("STAFF review requires both ordered cached rounds")
    sources = {p: subprocess.check_output(["git", "show", f"{REVISION}:{p}"], cwd=ROOT / "_reference/ReC98") for p in SOURCES}
    target = parse_mz(decoded)
    if not target.valid:
        raise ValueError("invalid MAINL decoded image")
    rows, observations = decode(target.program_image), runtime_matrix(target)
    rounds, objects = [], []
    for item in entry["rounds"]:
        receipt_round = next(r for r in replay["rounds"] if r["round"] == item["round"])
        if receipt_round["products"]["bin/th03/mainl.exe"] != item["candidate_sha256"]:
            raise ValueError("MAINL candidate is not a recorded cold product")
        binary, map_data = read(item["candidate_path"]), read(item["map_path"])
        if sha(binary) != item["candidate_sha256"] or sha(map_data) != item["map_sha256"]:
            raise ValueError("MAINL cached image/MAP identity differs")
        candidate = parse_mz(binary)
        if not candidate.valid:
            raise ValueError("invalid MAINL candidate MZ")
        tree = str(Path(item["candidate_path"]).parents[2])
        association = []
        for path, raw in sources.items():
            cached_path = str(Path(tree) / path)
            cached = read(cached_path)
            transform = "LF to CRLF only" if path.endswith(".asm") else "byte identity"
            expected = raw.replace(b"\n", b"\r\n") if path.endswith(".asm") else raw
            if cached != expected:
                raise ValueError(f"MAINL cached provider differs: {path}")
            association.append(dict(source=path, sha256=sha(raw), cached_path=cached_path,
                                    cached_sha256=sha(cached), transform=transform))
        contributions = [r for r in code_rows(map_data.decode("ascii"), len(candidate.program_image)) if r["name"] == "STAFF_TEXT"]
        if [(r["module"], r["segment"], r["offset"], r["size"]) for r in contributions] != [
                ("th03_mainl.asm", CS, 0x233e, 348), ("th03/staff.cpp", CS, 0x249a, 76)]:
            raise ValueError("MAINL complete STAFF CODE contributions differ")
        declaration_rows = []
        for line in map_data.decode("ascii").splitlines():
            match = re.fullmatch(r" ([0-9A-F]{4}):([0-9A-F]{4}) ([0-9A-F]+) C=(DATA|BSS)\s+S=(\S+)\s+G=\S+\s+M=th03/staff.cpp\s+ACBP=([0-9A-F]+)", line)
            if match:
                declaration_rows.append(dict(segment=int(match[1], 16), offset=int(match[2], 16),
                                             size=int(match[3], 16), kind=match[4], name=match[5], acbp=match[6]))
        if [(r["kind"], r["size"]) for r in declaration_rows] != [("DATA", 0), ("BSS", 0)]:
            raise ValueError("STAFF C++ declaration-only DATA/BSS contribution differs")
        extents = [extent_observation(target, candidate, r) for r in contributions]
        if any(not e["raw_slice_equal"] for e in extents) or not extents[1]["ordered_relocations_equal"]:
            raise ValueError("complete STAFF cached raw/body relocations differ")
        candidate_rows, cases = decode(candidate.program_image), runtime_matrix(candidate)
        if candidate_rows != rows or cases != observations:
            raise ValueError("MAINL STAFF CPU/source-coordinate observations differ")
        obj_path = str(Path(tree) / "obj/th03/staff.obj")
        obj = describe_omf(read(obj_path))
        if (not obj["valid"] or obj["module_name"] != "th03/staff.cpp" or
                obj["translator_comments"] != ["TC86 Borland C++ 4.02"]):
            raise ValueError("invalid cached STAFF C++ object")
        objects.append(obj)
        rounds.append(dict(round=item["round"], path=item["candidate_path"], source_associations=association,
                           extents=extents, code_regions=candidate_rows, runtime=cases,
                           staff_object_path=obj_path, staff_object=obj, declaration_rows=declaration_rows))
    if objects[0]["dependency_timestamp_normalized_sha256"] != objects[1]["dependency_timestamp_normalized_sha256"]:
        raise ValueError("cached STAFF OMF differs after dependency timestamp normalization")
    for path, raw in frozen.items():
        if (ROOT / path).read_bytes() != raw:
            raise ValueError("MAINL STAFF review input changed")
    if read_verified_artifact(ROOT, artifact) != stored:
        raise ValueError("canonical MAINL changed")
    for path, raw in sources.items():
        if subprocess.check_output(["git", "show", f"{REVISION}:{path}"], cwd=ROOT / "_reference/ReC98") != raw:
            raise ValueError("frozen STAFF source changed")
    result = dict(kind="th03-mainl-complete-staff-code-review", observed_utc=datetime.now(timezone.utc).isoformat(),
                  reference_revision=REVISION, stored_sha256=sha(stored), decoded_sha256=sha(decoded),
                  code_regions=rows, target_runtime=observations, rounds=rounds, code_bytes=424,
                  initialized_data_acceptance=False, bss_acceptance=False,
                  runtime_scope="STAFF instructions only; foreign calls, exec, devices, sprite data and resident/stack inputs are constructed models",
                  tools=dict(capstone_distribution=version("capstone"), unicorn_distribution=version("unicorn")),
                  inputs={p: sha(d) for p, d in frozen.items()}, sources={p: sha(d) for p, d in sources.items()},
                  diagnostic_checks_pass=True, fresh_build=False, authored_source=False,
                  source_acceptance=False, exact_acceptance=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    count = sum(len(observations[k]) for k in ("ending_cases", "failed_interface_cases", "flake_cases")) + 1
    print(f"PASS three complete STAFF bodies/424 bytes and {count * 3} CPU/model calls; generated relocation order remains open: {args.output}")


if __name__ == "__main__":
    main()
