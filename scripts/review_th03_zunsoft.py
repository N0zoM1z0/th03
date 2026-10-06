#!/usr/bin/env python3
"""Complete logo root review with modeled library calls; no exact acceptance."""
import argparse
from collections import Counter
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
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact
from lib.zun import parse_launcher

ROOT = Path(__file__).resolve().parents[1]
REVISION = "b6ba5b0a529edbb31efdf8c0e939263804f8ee47"
SOURCES = ["th01/zunsoft.cpp", "th01/math/polar.hpp", "th01/hardware/grcg.hpp",
           "libs/master.lib/master.hpp", "libs/master.lib/pc98_gfx.hpp", "libs/master.lib/func.hpp",
           "platform/x86real/pc98/egc.hpp", "platform/x86real/pc98/page.hpp", "platform.h"]
RANGES = [("graph_clear_both", 0x367, 29), ("zunsoft_init", 0x384, 76),
          ("zunsoft_exit", 0x3d0, 20), ("zunsoft_vector2", 0x3e4, 85),
          ("objects_setup", 0x439, 201), ("circles_render_and_update", 0x502, 180),
          ("stars_render_and_update", 0x5b6, 205), ("wait", 0x683, 21),
          ("logo_render_and_update", 0x698, 309), ("main", 0x7cd, 173)]
IMPORTS = {0x928: ("GRAPH_CLEAR", 0), 0x1344: ("MEM_ASSIGN_ALL", 0),
           0x958: ("GRAPH_START", 0), 0xab6: ("KEY_BEEP_OFF", 0),
           0x8b8: ("TEXT_SYSTEMLINE_HIDE", 0), 0x8ac: ("TEXT_CURSOR_HIDE", 0),
           0x155e: ("EGC_START", 0), 0x87a: ("TEXT_CLEAR", 0),
           0x139c: ("GRC_SETCLIP", 8), 0x94c: ("GRAPH_HIDE", 0),
           0xd16: ("SUPER_ENTRY_BFNT", 2), 0x978: ("PALETTE_SHOW", 0),
           0x952: ("GRAPH_SHOW", 0), 0xf68: ("SUPER_FREE", 0),
           0x136a: ("MEM_UNASSIGN", 0), 0x16b2: ("IRAND", 0),
           0x14b4: ("GRCG_SETCOLOR", 4), 0x1588: ("GRCG_CIRCLEFILL", 6),
           0x14e4: ("GRCG_PSET", 4), 0xe9c: ("SUPER_PUT_8", 6),
           0x1008: ("SUPER_WAVE_PUT", 12), 0x161a: ("GRCG_BYTEBOXFILL_X", 8),
           0xace: ("KEY_SENSE", 2)}
MATH = [(0x17d8, 0x17f8), (0x188c, 0x18a3)]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decode(data):
    if len(data) != 10096:
        raise ValueError("complete logo payload size differs")
    cs = Cs(CS_ARCH_X86, CS_MODE_16)
    cs.detail = True
    boundaries, rows = set(), []
    entries = {s for _, s, _ in RANGES} | set(IMPORTS) | {s for s, _ in MATH}
    for name, start, size in RANGES:
        body = data[start - 0x100:start - 0x100 + size]
        instructions = list(cs.disasm(body, start))
        if sum(i.size for i in instructions) != size or instructions[-1].mnemonic != "ret":
            raise ValueError("incomplete logo root/return boundary")
        if instructions[-1].op_str != ("8" if name == "zunsoft_vector2" else ""):
            raise ValueError("logo near cdecl/Pascal cleanup differs")
        boundaries.update(i.address for i in instructions)
        edges = []
        for i in instructions:
            if i.mnemonic.startswith(("j", "loop")) or i.mnemonic == "call":
                if not i.operands or i.operands[0].type != X86_OP_IMM:
                    raise ValueError("unexpected indirect logo root edge")
                edges.append(dict(instruction=i.address, kind=i.mnemonic, target=i.operands[0].imm))
        rows.append(dict(name=name, start=start, size=size, body_sha256=sha(body),
                         instruction_count=len(instructions), return_operands=instructions[-1].op_str, edges=edges))
    for row in rows:
        for edge in row["edges"]:
            if edge["kind"] == "call":
                if edge["target"] not in entries:
                    raise ValueError("logo root call lacks bounded entry/explicit import")
            elif edge["target"] not in boundaries:
                raise ValueError("logo root branch enters data or instruction operand")
    return rows


class Probe:
    """Execute root and two compiler arithmetic helpers, substitute other imports."""
    def __init__(self, data, early_key=False, hardware=False, asset_error=False):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INTR, UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.reg, self.uc = reg, Uc(UC_ARCH_X86, UC_MODE_16)
        uc = self.uc
        uc.mem_map(0, 0x100000)
        uc.mem_write(0x20100, data)
        for name in ("CS", "DS", "ES", "SS"):
            uc.reg_write(getattr(reg, "UC_X86_REG_" + name), 0x2000)
        uc.reg_write(reg.UC_X86_REG_EFLAGS, 2)
        uc.mem_write(0x45c, bytes([0x40 if hardware else 0]))
        uc.mem_write(0x54d, b"\xff")
        self.events, self.ports, self.errors, self.stopped = [], [], [], False
        self.random_index, self.input_index = 0, 0
        self.early_key, self.asset_error = early_key, asset_error
        def guarded_code(uc, address, size, user):
            try:
                if address == 0x2ffff:
                    self.stopped = True
                    uc.emu_stop()
                    return
                offset = address - 0x20000
                if offset in IMPORTS:
                    name, cleanup = IMPORTS[offset]
                    sp = self.read_register("SP")
                    words = struct.unpack("<" + "H" * (cleanup // 2 + 1), uc.mem_read(0x20000 + sp, cleanup + 2))
                    arguments = list(reversed(words[1:]))
                    event = dict(name=name, arguments=arguments, frame=self.word(0x2950))
                    if name == "IRAND":
                        value = [0, 32767, 16384, 640, 400, 31, 32][self.random_index % 7]
                        self.random_index += 1
                        self.write_register("AX", value)
                        event["returned_ax"] = value
                    elif name == "KEY_SENSE":
                        value = 1 if self.early_key and arguments == [3] else 0
                        self.write_register("AX", value)
                        event["returned_ax"] = value
                    elif name == "SUPER_ENTRY_BFNT":
                        self.write_register("AX", 0xfff3 if self.asset_error else 0)
                        event["returned_ax"] = self.read_register("AX")
                    if name == "PALETTE_SHOW":
                        event["tone"] = self.word(0x2248)
                    self.events.append(event)
                    self.write_register("SP", sp + 2 + cleanup)
                    self.write_register("IP", words[0])
                elif not (0x367 <= offset < 0x87a or any(a <= offset < b for a, b in MATH)):
                    raise ValueError("logo execution escaped root/compiler arithmetic/import boundary")
            except Exception as error:
                self.errors.append(str(error))
                uc.emu_stop()
        def output(uc, port, size, value, user):
            self.ports.append(dict(port=port, size=size, value=value))
        def input_(uc, port, size, user):
            if port != 0xa0 or size != 1:
                self.errors.append("unmodeled logo input port")
                uc.emu_stop()
                return 0
            value = [0x20, 0, 0, 0x20][self.input_index % 4]
            self.input_index += 1
            return value
        def interrupt(uc, number, user):
            self.errors.append("unmodeled logo interrupt")
            uc.emu_stop()
        uc.hook_add(UC_HOOK_CODE, guarded_code)
        uc.hook_add(UC_HOOK_INTR, interrupt)
        uc.hook_add(UC_HOOK_INSN, output, None, 1, 0, reg.UC_X86_INS_OUT)
        uc.hook_add(UC_HOOK_INSN, input_, None, 1, 0, reg.UC_X86_INS_IN)

    def read_register(self, name):
        return self.uc.reg_read(getattr(self.reg, "UC_X86_REG_" + name))

    def write_register(self, name, value):
        self.uc.reg_write(getattr(self.reg, "UC_X86_REG_" + name), value)

    def word(self, address):
        return struct.unpack("<H", self.uc.mem_read(0x20000 + address, 2))[0]

    def call(self, entry, stack_words=(), budget=4000000):
        self.stopped = False
        self.uc.mem_write(0x2ff00, struct.pack("<" + "H" * (len(stack_words) + 1), 0xffff, *stack_words))
        self.write_register("SP", 0xff00)
        self.uc.emu_start(0x20000 + entry, 0x30000, count=budget)
        if self.errors or not self.stopped:
            raise ValueError(self.errors[0] if self.errors else "logo root missed bounded return")

    def observation(self):
        return dict(root_bss=bytes(self.uc.mem_read(0x22870, 293)).hex(),
                    frame=self.word(0x2950), tone=self.uc.mem_read(0x22872, 1)[0],
                    hardware_byte_54d=self.uc.mem_read(0x54d, 1)[0],
                    library_counts=dict(sorted(Counter(e["name"] for e in self.events).items())),
                    event_sha256=sha(json.dumps(self.events, sort_keys=True).encode()),
                    port_counts=dict(sorted(Counter(hex(p["port"]) for p in self.ports).items())),
                    port_sha256=sha(json.dumps(self.ports, sort_keys=True).encode()),
                    vsync_reads=self.input_index,
                    palette=[dict(frame=e["frame"], tone=e["tone"]) for e in self.events if e["name"] == "PALETTE_SHOW"])


def runtime_matrix(data):
    flows = []
    for early, hardware, asset_error in [(False, False, False), (True, True, False), (False, True, True)]:
        p = Probe(data, early, hardware, asset_error)
        for name, value in [("SI", 0xabba), ("DI", 0xcdda), ("BP", 0x1234)]:
            p.write_register(name, value)
        p.call(0x7cd)
        if {n: p.read_register(n) for n in ("SI", "DI", "BP", "SP", "DS")} != dict(SI=0xabba, DI=0xcdda, BP=0x1234, SP=0xff02, DS=0x2000):
            raise ValueError("logo main near frame/register return differs")
        observation = p.observation()
        expected_frames = 1 if early else 231
        if (observation["frame"] != (0 if early else 231) or observation["tone"] != (2 if early else 0) or
                observation["vsync_reads"] != expected_frames * 8 or
                observation["library_counts"]["KEY_SENSE"] != expected_frames * 8 or
                observation["library_counts"]["SUPER_FREE"] != 1):
            raise ValueError("logo fade/keyboard/wait/exit vector differs")
        flows.append(dict(early_key=early, hardware=hardware, modeled_asset_error=asset_error, **observation))
    # Complete vector function executes real 16-bit long-multiply/shift helpers.
    p, vectors = Probe(data), []
    for length in (-32768, -37, 0, 37, 32767):
        for angle in range(256):
            p.call(0x3e4, [length & 65535, angle, 0x1802, 0x1800], budget=200)
            vectors.append(dict(length=length, angle=angle,
                                xy=list(struct.unpack("<hh", p.uc.mem_read(0x21800, 4)))))
            if p.read_register("SP") != 0xff0a:
                raise ValueError("vector near Pascal cleanup differs")
    positive = next(v["xy"] for v in vectors if v["length"] == 37 and v["angle"] == 32)
    negative = next(v["xy"] for v in vectors if v["length"] == 37 and v["angle"] == 160)
    if positive != [26, 26] or negative != [-27, -27]:
        raise ValueError("negative arithmetic-shift rounding differs")
    p = Probe(data)
    p.uc.mem_write(0x22878, struct.pack("<8h", 40, 40, 41, 41, 599, 359, 600, 360))
    p.uc.mem_write(0x22952, struct.pack("<8h", -8, -8, 8, 8, -8, -8, 8, 8))
    p.call(0x502)
    circles = dict(position=list(struct.unpack("<8h", p.uc.mem_read(0x22878, 16))),
                   speeds=list(struct.unpack("<8h", p.uc.mem_read(0x22952, 16))), events=p.events)
    if circles["position"] != [32, 32, 33, 33, 607, 367, 608, 368] or circles["speeds"] != [8, -8, 8, -8, 8, -8, 8, -8]:
        raise ValueError("circle inclusive/exclusive bounce boundary differs")
    phases = []
    for frame in (49, 50, 55, 60, 65, 89, 90, 109, 110, 129, 130, 155, 160, 165, 169, 170):
        p = Probe(data)
        p.uc.mem_write(0x22950, struct.pack("<h", frame))
        p.uc.mem_write(0x22873, bytes([6, 23, 250, 80, 0]))
        p.call(0x698)
        phases.append(dict(frame=frame, state=bytes(p.uc.mem_read(0x22873, 4)).hex(), events=p.events))
    if (phases[0]["events"] or phases[-1]["events"] or
            [len(p["events"]) for p in phases[1:-1]] != [2] * 14 or
            phases[6]["state"] != "0616fe54" or phases[8]["state"] != "0818fe4c"):
        raise ValueError("logo phase boundary/byte wrap vector differs")
    return dict(main_flows=flows, vector_cases=vectors, circle_boundaries=circles, logo_phase_cases=phases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    frozen = {}
    def read(path):
        frozen[path] = (ROOT / path).read_bytes()
        return frozen[path]
    config = tomllib.loads(read("config/th03_zun_launcher.toml").decode())
    diet = tomllib.loads(read("config/th03_diet.toml").decode())
    for path in ("config/targets.toml", "scripts/review_th03_zunsoft.py", "scripts/lib/zun.py", "scripts/lib/targets.py", "scripts/lib/omf.py"):
        read(path)
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-zun")
    stored = read_verified_artifact(ROOT, artifact)
    decoded = read(config["decoded_path"])
    restoration = json.loads(read(config["diet_receipt"]))
    lineage = next(o for o in restoration["observations"] if o["artifact"] == "th03-zun")
    cold = json.loads(read(config["cold_receipt"]))
    expected = next(a for a in diet["artifacts"] if a["id"] == "th03-zun")
    if (config["reference_revision"] != REVISION or sha(decoded) != expected["decoded_sha256"] or
            sha(frozen[config["diet_receipt"]]) != config["diet_receipt_sha256"] or
            lineage["stored"]["sha256"] != sha(stored) or lineage["decoded"]["sha256"] != sha(decoded) or
            not restoration["restoration_checks_pass"] or
            sha(frozen[config["cold_receipt"]]) != config["cold_receipt_sha256"] or
            not cold["pass"] or cold["reference_revision"] != REVISION or not cold["all_products_equal"]):
        raise ValueError("logo restoration/cached receipt lineage differs")
    sources = {p: subprocess.check_output(["git", "show", f"{REVISION}:{p}"], cwd=ROOT / "_reference/ReC98") for p in SOURCES}
    payload = parse_launcher(decoded, 223)["payloads"][2]
    target = decoded[payload["decoded_file_offset"]:payload["decoded_file_offset"] + payload["size"]]
    target_rows, target_cases = decode(target), runtime_matrix(target)
    pin = next(p for p in config["payloads"] if p["option"] == "-3")
    rounds = []
    for path in pin["cold_paths"]:
        candidate = read(path)
        if sha(candidate) != pin["sha256"] or candidate != target:
            raise ValueError("complete cached logo raw equality differs")
        source_root = Path(path).parents[2]
        associations = []
        for p, original in sources.items():
            cached_path = str(source_root / p)
            cached = read(cached_path)
            if cached != original:
                raise ValueError("cached logo source/provider bytes differ")
            associations.append(dict(source=p, cached_path=cached_path, exact_bytes=True))
        map_path = str(source_root / "obj/th01/zunsoft.map")
        map_text = read(map_path).decode("ascii")
        for address, size, cls in [(0x367, 0x513, "CODE"), (0x21ce, 15, "DATA"), (0x2870, 293, "BSS")]:
            pattern = rf"0000:{address:04X} {size:04X} C={cls}\s+S=\S+\s+G=DGROUP\s+M=th01/zunsoft.cpp"
            if not re.search(pattern, map_text):
                raise ValueError("logo root MAP contribution differs")
        object_path = str(source_root / "obj/th01/zunsoft.obj")
        omf = describe_omf(read(object_path))
        if decode(candidate) != target_rows or runtime_matrix(candidate) != target_cases:
            raise ValueError("cached logo root observations differ")
        rounds.append(dict(path=path, complete_raw_equal=True, source_associations=associations,
                           map_path=map_path, object_path=object_path, omf=omf, runtime_checked=True))
    if rounds[0]["omf"]["dependency_timestamp_normalized_sha256"] != rounds[1]["omf"]["dependency_timestamp_normalized_sha256"]:
        raise ValueError("logo cached normalized OMF differs")
    for path, data in frozen.items():
        if (ROOT / path).read_bytes() != data:
            raise ValueError("logo diagnostic input changed")
    for path, data in sources.items():
        if subprocess.check_output(["git", "show", f"{REVISION}:{path}"], cwd=ROOT / "_reference/ReC98") != data:
            raise ValueError("frozen logo source changed")
    if read_verified_artifact(ROOT, artifact) != stored:
        raise ValueError("canonical ZUN changed")
    result = dict(kind="th03-zunsoft-complete-root-candidate-review", observed_utc=datetime.now(timezone.utc).isoformat(),
                  reference_revision=REVISION, sources={p: sha(d) for p, d in sources.items()}, payload=payload,
                  stored_sha256=sha(stored), decoded_sha256=sha(decoded), target_procedures=target_rows,
                  runtime_cases=target_cases, rounds=rounds, inputs={p: sha(d) for p, d in frozen.items()},
                  tools=dict(capstone_distribution=version("capstone"), unicorn_distribution=version("unicorn")),
                  diagnostic_checks_pass=True, fresh_build=False, source_acceptance=False, exact_acceptance=False,
                  complete_runtime_library_review=False,
                  runtime_scope="Root plus two real compiler arithmetic helpers; other libraries/keys/ports modeled; no BFNT assets or PC-98 device execution")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS complete logo root 1299 bytes/10 procedures and cached 10096-byte equality; no acceptance: {args.output}")


if __name__ == "__main__":
    main()
