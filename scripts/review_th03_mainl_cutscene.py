#!/usr/bin/env python3
"""Whole TH03 cutscene candidate analysis; selected CPU contracts, no acceptance."""
import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import struct
import subprocess
import tomllib

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation

ROOT = Path(__file__).resolve().parents[1]
REVISION = "b6ba5b0a529edbb31efdf8c0e939263804f8ee47"
CS, DS = 0x95f, 0xe3f
RANGES = [("script_load", 0xb3e, 70, "4"), ("script_free", 0xb84, 31, ""),
          ("egc_start_copy", 0xba3, 52, ""), ("pic_copy_to_other", 0xbd7, 117, "4"),
          ("pic_put_both_masked", 0xc4c, 303, "8"), ("box_allocate_snap", 0xd7b, 209, ""),
          ("box_free", 0xe4c, 31, ""), ("box_put", 0xe6b, 175, ""),
          ("number_first", 0xf1a, 201, "4"), ("number_second", 0xfe3, 41, "4"),
          ("cursor_advance", 0x100c, 81, ""), ("script_op", 0x105d, 1496, "2"),
          ("animate", 0x167e, 315, "")]
SOURCES = ["th03/cutscene.cpp", "th03/cutscene/cutscene.cpp", "th03/cutscene/cutscene.hpp",
           "th03/formats/script.hpp", "game/cutscene.hpp", "th01/hardware/egcstart.cpp",
           "th01/hardware/egc_impl.hpp", "th03/formats/pi.hpp", "th02/formats/pi.h",
           "th03/pi_put.cpp", "th02/formats/pi_put.cpp", "libs/master.lib/graph_gaiji_putc.asm",
           "libs/master.lib/func.hpp", "platform.h", "pc98.h", "planar.h"]
# Every foreign call in the complete root; ownership/implementation remains separate.
FOREIGN = {(0, x) for x in (0x724, 0x73a, 0x846, 0x8b2, 0x966, 0x9e4, 0x21ae, 0x22b2,
                           0x2c6e, 0x3641, 0x536, 0x57a, 0x208a, 0x20ca, 0x17d0,
                           0x1700, 0xf58, 0xe72, 0xeac, 0xfec, 0xb9e, 0xc36, 0xc60)}
FOREIGN |= {(0xc7e, x) for x in (0x372, 0xee5, 0xc9a, 0xc1c, 0xc4d, 0x6e2, 0xccb,
                                0xd11, 0xa0, 0x65e, 0x66a, 0x6a6, 0xdc2, 0x9b7,
                                0x529, 0x52a, 0x54e, 0x54f)}
# Only these interfaces are substituted in the selected runtime scopes.
MODELS = {(0, 0x966): ("FILE_ROPEN", 4, 4), (0, 0x9e4): ("FILE_SIZE", 0, 0),
          (0, 0x21ae): ("HMEM_ALLOCBYTE", 2, 2), (0, 0x22b2): ("HMEM_FREE", 2, 2),
          (0, 0x8b2): ("FILE_READ", 6, 6), (0, 0x846): ("FILE_CLOSE", 0, 0),
          (0, 0x3641): ("tolower", 2, 0)}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decode(image):
    cs = Cs(CS_ARCH_X86, CS_MODE_16)
    cs.detail = True
    rows, boundaries = [], set()
    entries = {s for _, s, _, _ in RANGES}
    for name, start, size, cleanup in RANGES:
        body = image[CS * 16 + start:CS * 16 + start + size]
        instructions = list(cs.disasm(body, start))
        if (sum(i.size for i in instructions) != size or not instructions or
                instructions[-1].mnemonic != "ret" or instructions[-1].op_str != cleanup):
            raise ValueError("incomplete cutscene body/near cleanup boundary")
        boundaries.update(i.address for i in instructions)
        edges = []
        for i in instructions:
            if i.mnemonic.startswith(("j", "loop")) or i.mnemonic in ("call", "lcall"):
                if i.address in (0x108c, 0x112a):
                    if i.mnemonic != "jmp" or len(i.operands) != 1 or i.operands[0].type != X86_OP_MEM:
                        raise ValueError("cutscene switch indirect dispatch differs")
                    expected = "word ptr cs:[bx + 0x20]" if i.address == 0x108c else "word ptr cs:[bx + 0x1636]"
                    if i.op_str != expected:
                        raise ValueError("cutscene switch address expression differs")
                    edges.append(dict(instruction=i.address, kind="switch", table=0x165e if i.address == 0x108c else 0x1636))
                    continue
                if not i.operands or any(o.type != X86_OP_IMM for o in i.operands):
                    raise ValueError("unexpected indirect cutscene edge")
                destination = tuple(o.imm for o in i.operands) if i.mnemonic == "lcall" else (CS, i.operands[0].imm)
                edges.append(dict(instruction=i.address, kind=i.mnemonic, destination=destination))
        rows.append(dict(name=name, offset=start, size=size, body_sha256=sha(body),
                         instruction_count=len(instructions), cleanup=cleanup, edges=edges))
    for row in rows:
        for edge in row["edges"]:
            if edge["kind"] == "switch":
                continue
            segment, offset = edge["destination"]
            if edge["kind"] == "lcall":
                if (segment, offset) not in FOREIGN:
                    raise ValueError("cutscene far call has unreviewed interface coordinates")
            elif edge["kind"] == "call":
                if segment != CS or offset not in entries:
                    raise ValueError("cutscene near call enters a body interior")
            elif offset not in boundaries or not row["offset"] <= offset < row["offset"] + row["size"]:
                raise ValueError("cutscene branch enters data/operand/another body")
    weights = list(struct.unpack_from("<4H", image, CS * 16 + 0x1636))
    keys = list(struct.unpack_from("<16H", image, CS * 16 + 0x163e))
    destinations = list(struct.unpack_from("<16H", image, CS * 16 + 0x165e))
    if keys != list(b"$=@bcefgkmnpstvw") or len(set(destinations)) != 16:
        raise ValueError("complete cutscene opcode key/destination catalogue differs")
    if any(d not in boundaries or not 0x105d <= d < 0x1635 for d in weights + destinations):
        raise ValueError("cutscene table enters data or instruction operand")
    if image[CS * 16 + 0x1635] != 0:
        raise ValueError("observed compiler table-alignment byte differs")
    return dict(functions=rows, tables=dict(weight_destinations=weights, opcode_keys=keys,
                opcode_destinations=destinations, data_start=0x1636, data_size=72,
                alignment_start=0x1635, alignment_size=1))


class Probe:
    """Execute loader, parameter readers and gaiji command; real gaiji ADC prefix."""
    def __init__(self, mz, *, open_ok=True, size=3, allocation=0x6000, read_result=0):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_INTR, UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc, self.reg = Uc(UC_ARCH_X86, UC_MODE_16), reg
        self.events, self.reads, self.ports, self.errors = [], [], [], []
        self.stop = False
        self.open_ok, self.size, self.allocation, self.read_result = open_ok, size, allocation, read_result
        self.uc.mem_map(0, 0x100000)
        image = bytearray(mz.program_image)
        for relocation in mz.relocations:
            at = relocation.segment * 16 + relocation.offset
            struct.pack_into("<H", image, at, (struct.unpack_from("<H", image, at)[0] + 0x2000) & 65535)
        self.uc.mem_write(0x20000, bytes(image))
        self.code, self.data, self.stack = (0x2000 + CS) * 16, (0x2000 + DS) * 16, 0x40000
        for name, value in (("CS", 0x2000 + CS), ("DS", 0x2000 + DS), ("SS", 0x4000),
                            ("ES", 0x3333), ("BP", 0x7777), ("SI", 0x1357), ("DI", 0x2468), ("EFLAGS", 0x202)):
            self.set(name, value)
        self.word(0x21e0, 80)
        self.word(0x21e2, 320)
        self.uc.mem_write(self.data + 0x21e6, b"\x0f")
        self.gaiji_frame = None
        self.model_at = {(0x2000 + segment) * 16 + offset: (segment, offset) for segment, offset in MODELS}
        def guarded(callback, default=None):
            def run(*args):
                try:
                    return callback(*args)
                except Exception as error:
                    self.errors.append(str(error))
                    self.uc.emu_stop()
                    return default
            return run
        def code(uc, address, length, user):
            if address == self.code + 0xff00:
                self.stop = True
                uc.emu_stop()
                return
            if address == 0x20f58:
                if self.get("CS") != 0x2000:
                    raise ValueError("gaiji prefix entered through a segment alias")
                sp = self.get("SP")
                words = list(struct.unpack("<6H", uc.mem_read(self.stack + sp, 12)))
                self.gaiji_frame = (sp, words)
                self.events.append(dict(name="GRAPH_GAIJI_PUTC-prefix", stack_words=words[2:],
                                        carry_in=self.get("EFLAGS") & 1, accessed_page=self.ports[-1][1]))
                return
            if self.gaiji_frame and 0x20f58 < address < 0x20f70:
                return
            if self.gaiji_frame and address == 0x20f70:
                sp, words = self.gaiji_frame
                self.events[-1]["jis_word"] = self.get("BP")
                self.events[-1]["carry_after_and"] = self.get("EFLAGS") & 1
                self.set("DI", struct.unpack("<H", uc.mem_read(self.stack + sp - 4, 2))[0])
                self.set("BP", struct.unpack("<H", uc.mem_read(self.stack + sp - 2, 2))[0])
                self.set("SP", sp + 12)
                self.set("CS", words[1])
                self.set("IP", words[0])
                self.gaiji_frame = None
                return
            if address in self.model_at:
                key = self.model_at[address]
                if self.get("CS") != 0x2000 + key[0]:
                    raise ValueError("cutscene model import segment alias")
                name, count, cleanup = MODELS[key]
                sp = self.get("SP")
                words = list(struct.unpack("<" + "H" * ((4 + count) // 2), uc.mem_read(self.stack + sp, 4 + count)))
                args = words[2:]
                event = dict(name=name, stack_words=args)
                if name == "FILE_ROPEN":
                    self.set("AX", int(self.open_ok))
                elif name == "FILE_SIZE":
                    self.set("AX", self.size & 65535)
                    self.set("DX", self.size >> 16)
                elif name == "HMEM_ALLOCBYTE":
                    self.set("AX", self.allocation)
                elif name in ("FILE_READ", "FILE_CLOSE", "HMEM_FREE"):
                    self.set("AX", self.read_result)
                elif name == "tolower":
                    value = args[0]
                    self.set("AX", value + 32 if 65 <= value <= 90 else value)
                event["returned_ax"] = self.get("AX")
                self.events.append(event)
                self.set("SP", sp + 4 + cleanup)
                self.set("CS", words[1])
                self.set("IP", words[0])
                return
            offset = address - self.code
            if self.get("CS") != 0x2000 + CS or not any(start <= offset < start + size for _, start, size, _ in RANGES):
                raise ValueError("CPU escaped cutscene reviewed code/model interfaces")
        def read(uc, access, address, size, value, user):
            if 0x50000 <= address < 0x60000:
                self.reads.append([address - 0x50000, size])
        def interrupt(uc, number, user):
            raise ValueError("unexpected cutscene kernel interrupt")
        def output(uc, port, width, value, user):
            if port != 0xa6 or width != 1:
                raise ValueError("unexpected selected cutscene port/width")
            self.ports.append([port, value])
        def input_port(uc, port, width, user):
            raise ValueError("unexpected selected cutscene input port")
        self.uc.hook_add(UC_HOOK_CODE, guarded(code))
        self.uc.hook_add(UC_HOOK_MEM_READ, guarded(read))
        self.uc.hook_add(UC_HOOK_INTR, guarded(interrupt))
        self.uc.hook_add(UC_HOOK_INSN, guarded(output), None, 1, 0, reg.UC_X86_INS_OUT)
        self.uc.hook_add(UC_HOOK_INSN, guarded(input_port, 0), None, 1, 0, reg.UC_X86_INS_IN)

    def get(self, name):
        return self.uc.reg_read(getattr(self.reg, "UC_X86_REG_" + name))

    def set(self, name, value):
        self.uc.reg_write(getattr(self.reg, "UC_X86_REG_" + name), value)

    def word(self, offset, value=None):
        if value is not None:
            self.uc.mem_write(self.data + offset, struct.pack("<H", value & 65535))
        return struct.unpack("<H", self.uc.mem_read(self.data + offset, 2))[0]

    def script(self, raw, offset=0):
        self.uc.mem_write(self.data + 0x21d6, struct.pack("<HH", offset, 0x5000))
        for i, byte in enumerate(raw):
            self.uc.mem_write(0x50000 + ((offset + i) & 65535), bytes([byte]))

    def run(self, entry, args=()):
        self.set("SP", 0xfff0)
        self.uc.mem_write(self.stack + 0xfff0, struct.pack("<" + "H" * (1 + len(args)), 0xff00, *args))
        self.uc.emu_start(self.code + entry, 0x100000, count=10000)
        if self.errors or not self.stop:
            raise ValueError(self.errors[0] if self.errors else "cutscene scope did not reach its reviewed return")
        if self.get("SP") != 0xfff2 + 2 * len(args) or [self.get(r) for r in ("BP", "SI", "DI")] != [0x7777, 0x1357, 0x2468]:
            raise ValueError("cutscene stack/callee-saved contract differs")


def parameter_case(mz, text, offset=0, second=False, default=73):
    p = Probe(mz)
    p.script(text.encode("ascii"), offset)
    p.word(0x21e8, default)
    p.run(0xfe3 if second else 0xf1a, (0x100, 0x7000))
    skip = 1 if second and text.startswith(",") else 0
    digits = ""
    if not second or skip:
        for character in text[skip:skip + 3]:
            if not character.isdigit():
                break
            digits += character
    expected = int(digits) if digits else default
    consumed = skip + len(digits)
    actual = struct.unpack("<H", p.uc.mem_read(0x70100, 2))[0]
    if actual != expected or p.word(0x21d6) != (offset + consumed) & 65535 or p.word(0x21d8) != 0x5000:
        raise ValueError("parameter value/word-only far pointer movement differs")
    expected_reads = ([[offset, 1]] if second else [])
    if not second or skip:
        expected_reads += [[(offset + skip + i) & 65535, 1] for i in range(3)]
    if p.reads != expected_reads:
        raise ValueError("parameter three-byte speculative read order differs")
    return dict(text=text, offset=offset, second=second, default=default, value=actual,
                final_offset=p.word(0x21d6), final_segment=p.word(0x21d8), reads=p.reads,
                carry=p.get("EFLAGS") & 1, final_sp=p.get("SP"))


def gaiji_case(mz, number, offset=0):
    p = Probe(mz)
    p.script(("a" + number + "!").encode("ascii"), offset)
    p.run(0x105d, (ord("g"),))
    events = [e for e in p.events if e["name"] == "GRAPH_GAIJI_PUTC-prefix"]
    if len(events) != 2 or [e["accessed_page"] for e in events] != [1, 0]:
        raise ValueError("gaiji dual-page call sequence differs")
    parameter = parameter_case(mz, number + "!", (offset + 1) & 65535, default=0)
    value, carry = parameter["value"], parameter["carry"]
    expected_ids = [(value - 1) & 65535, value]
    if ([e["stack_words"][1] for e in events] != expected_ids or
            [e["carry_in"] for e in events] != [carry, 0] or
            [e["jis_word"] for e in events] != [((expected_ids[0] + 0x5680 + carry) & 0xff7f), ((value + 0x5680) & 0xff7f)] or
            any(e["carry_after_and"] for e in events) or p.get("AX") & 255 != 0 or p.word(0x21e0) != 96):
        raise ValueError("gaiji real ADC prefix/carry/cursor contract differs")
    return dict(number=number, offset=offset, parameter=parameter, events=events,
                final_script_offset=p.word(0x21d6), final_sp=p.get("SP"), final_cursor=[p.word(0x21e0), p.word(0x21e2)])


def runtime_matrix(mz):
    params = [parameter_case(mz, text, offset, second) for text, second in [
        ("x", False), ("0x", False), ("7x", False), ("12x", False), ("999x", False),
        ("1234", False), (",12x", True), (",x", True), ("12x", True)] for offset in (0, 0xfffd, 0xfffe, 0xffff)]
    gaiji = [gaiji_case(mz, number, offset) for number in ("", "0", "1", "9", "12", "123") for offset in (0, 0xfffd)]
    loaders = []
    for opened, size, allocation in [(False, 3, 0x6000), (True, 0, 0x6000), (True, 3, 0x6000),
                                     (True, 0x10003, 0x6000), (True, 3, 0)]:
        p = Probe(mz, open_ok=opened, size=size, allocation=allocation)
        p.script(b"old", 7)
        p.run(0xb3e, (0x300, 0x7000))
        names = [e["name"] for e in p.events]
        expected = ["HMEM_FREE", "FILE_ROPEN"] + (["FILE_SIZE", "HMEM_ALLOCBYTE", "FILE_READ", "FILE_CLOSE"] if opened else [])
        if (names != expected or p.get("AX") != (0 if opened else 1) or p.word(0x21d6) != 0 or
                p.word(0x21d8) != (allocation if opened else 0)):
            raise ValueError("loader unchecked allocation/read/open/free contract differs")
        if opened and p.events[-2]["stack_words"] != [size & 65535, 0, allocation]:
            raise ValueError("loader 16-bit size/null read request differs")
        loaders.append(dict(open_ok=opened, modeled_file_size=size, allocation_segment=allocation,
                            events=p.events, final_pointer=[p.word(0x21d6), p.word(0x21d8)], returned_ax=p.get("AX")))
    return dict(parameter_cases=params, gaiji_cases=gaiji, loader_cases=loaders,
                scope="Selected loader/parameter/gaiji/cursor contracts; box/picture/interpreter/device execution remains open")


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
    for path in ("config/targets.toml", "scripts/review_th03_mainl_cutscene.py", "scripts/review_th03_decoded_code.py",
                 "scripts/lib/pc98.py", "scripts/lib/omf.py", "scripts/lib/targets.py"):
        read(path)
    target_artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-mainl")
    stored = read_verified_artifact(ROOT, target_artifact)
    entry = next(a for a in config["artifacts"] if a["id"] == "th03-mainl")
    decoded = read(entry["decoded_path"])
    restoration, replay = json.loads(read(config["diet_receipt"])), json.loads(read(config["replay_receipt"]))
    pin = next(a for a in diet["artifacts"] if a["id"] == "th03-mainl")
    lineage = next(o for o in restoration["observations"] if o["artifact"] == "th03-mainl")
    if (sha(decoded) != pin["decoded_sha256"] or sha(frozen[config["diet_receipt"]]) != config["diet_receipt_sha256"] or
            sha(frozen[config["replay_receipt"]]) != config["replay_receipt_sha256"] or
            lineage["stored"]["sha256"] != sha(stored) or lineage["decoded"]["sha256"] != sha(decoded) or
            not restoration["restoration_checks_pass"] or not restoration["canonical_targets_unchanged"] or
            not replay["pass"] or not replay["all_products_equal"] or
            any(x["reference_revision"] != REVISION for x in (config, diet, replay, restoration)) or
            [r["round"] for r in entry["rounds"]] != [1, 2]):
        raise ValueError("cutscene stored/decoded/cached lineage differs")
    sources = {p: subprocess.check_output(["git", "show", f"{REVISION}:{p}"], cwd=ROOT / "_reference/ReC98") for p in SOURCES}
    target = parse_mz(decoded)
    if not target.valid:
        raise ValueError("invalid decoded MAINL")
    analysis, runtime = decode(target.program_image), runtime_matrix(target)
    rounds, objects = [], []
    for item in entry["rounds"]:
        if next(r for r in replay["rounds"] if r["round"] == item["round"])["products"]["bin/th03/mainl.exe"] != item["candidate_sha256"]:
            raise ValueError("cutscene candidate absent from cached receipt")
        binary, map_raw = read(item["candidate_path"]), read(item["map_path"])
        if sha(binary) != item["candidate_sha256"] or sha(map_raw) != item["map_sha256"]:
            raise ValueError("cutscene cached binary/MAP changed")
        candidate = parse_mz(binary)
        if not candidate.valid or candidate.program_image[0xf58:0xf70] != target.program_image[0xf58:0xf70]:
            raise ValueError("candidate MZ/real gaiji prefix differs")
        tree = str(Path(item["candidate_path"]).parents[2])
        associations = []
        for path, raw in sources.items():
            cached_path = str(Path(tree) / path)
            cached = read(cached_path)
            expected = raw.replace(b"\n", b"\r\n") if path.endswith(".asm") else raw
            if cached != expected:
                raise ValueError(f"cutscene cached source association differs: {path}")
            associations.append(dict(source=path, sha256=sha(raw), cached_path=cached_path,
                                     transform="LF to CRLF only" if path.endswith(".asm") else "byte identity"))
        rows = [r for r in code_rows(map_raw.decode("ascii"), len(candidate.program_image)) if r["module"] == "th03/cutscene.cpp" and r["size"]]
        if len(rows) != 1 or (rows[0]["segment"], rows[0]["offset"], rows[0]["size"]) != (CS, 0xb3e, 3195):
            raise ValueError("complete cutscene CODE contribution differs")
        extent = extent_observation(target, candidate, rows[0])
        differences = [at for at in range(0xb3e, 0x17b9) if target.program_image[CS * 16 + at] != candidate.program_image[CS * 16 + at]]
        if differences != [0x140a, 0x1414, 0x144b] or not extent["ordered_relocations_equal"]:
            raise ValueError("cutscene raw/ordered-relocation diagnostic vector differs")
        helper_rows = []
        for name, target_start, candidate_start, size, cleanup in [("pi_palette_apply", 0x52a, 0x529, 37, "2"), ("pi_put_8", 0x54f, 0x54e, 136, "6")]:
            left = target.program_image[0xc7e0 + target_start:0xc7e0 + target_start + size]
            right = candidate.program_image[0xc7e0 + candidate_start:0xc7e0 + candidate_start + size]
            instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(left, target_start))
            if left != right or sum(i.size for i in instructions) != size or instructions[-1].mnemonic != "retf" or instructions[-1].op_str != cleanup:
                raise ValueError("complete PI direct-callee body/entry/ABI association differs")
            helper_rows.append(dict(name=name, target_segment=0xc7e, target_offset=target_start,
                                    candidate_offset=candidate_start, size=size, raw_body_equal=True, body_sha256=sha(left), far_cleanup=cleanup))
        candidate_analysis, observations = decode(candidate.program_image), runtime_matrix(candidate)
        if candidate_analysis["tables"] != analysis["tables"] or observations != runtime:
            raise ValueError("cutscene table/selected CPU observations differ")
        obj_path = str(Path(tree) / "obj/th03/cutscene.obj")
        obj = describe_omf(read(obj_path))
        if (not obj["valid"] or obj["module_name"] != "th03/cutscene.cpp" or
                obj["translator_comments"] != ["TC86 Borland C++ 4.02"]):
            raise ValueError("invalid cutscene cached OMF")
        objects.append(obj)
        rounds.append(dict(round=item["round"], source_associations=associations, code=extent,
                           differences=differences, analysis=candidate_analysis, runtime=observations,
                           pi_helper_diagnostics=helper_rows, object_path=obj_path, object=obj))
    if objects[0]["dependency_timestamp_normalized_sha256"] != objects[1]["dependency_timestamp_normalized_sha256"]:
        raise ValueError("cached cutscene OMF differs beyond dependency timestamps")
    prefix = target.program_image[0xf58:0xf70]
    prefix_instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(prefix, 0xf58))
    if (sum(i.size for i in prefix_instructions) != 24 or
            [(i.address, i.mnemonic, i.op_str) for i in prefix_instructions[-2:]] !=
            [(0xf68, "adc", "bp, 0x5680"), (0xf6c, "and", "bp, 0xff7f")]):
        raise ValueError("gaiji real carry-prefix boundary differs")
    for path, raw in frozen.items():
        if (ROOT / path).read_bytes() != raw:
            raise ValueError("cutscene review input changed")
    if read_verified_artifact(ROOT, target_artifact) != stored:
        raise ValueError("canonical MAINL changed")
    for path, raw in sources.items():
        if subprocess.check_output(["git", "show", f"{REVISION}:{path}"], cwd=ROOT / "_reference/ReC98") != raw:
            raise ValueError("frozen cutscene provider changed")
    result = dict(kind="th03-mainl-whole-cutscene-candidate-analysis", observed_utc=datetime.now(timezone.utc).isoformat(),
                  stored_sha256=sha(stored), decoded_sha256=sha(decoded), reference_revision=REVISION,
                  analysis=analysis, selected_runtime=runtime, rounds=rounds,
                  byte_accounting=dict(function_bodies=3122, switch_tables=72, observed_alignment=1, total=3195),
                  gaiji_prefix=dict(start=0xf58, size=24, sha256=sha(prefix), full_function_acceptance=False),
                  runtime_scope=runtime["scope"], whole_runtime_proved=False,
                  tools=dict(capstone_distribution=version("capstone"), unicorn_distribution=version("unicorn")),
                  inputs={p: sha(d) for p, d in frozen.items()}, sources={p: sha(d) for p, d in sources.items()},
                  diagnostic_checks_pass=True, raw_root_equal=False, fresh_build=False,
                  source_acceptance=False, exact_acceptance=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS 3195-byte candidate analysis/13 bodies,195 selected CPU calls including companion parameter probes; three raw call-coordinate differences remain: {args.output}")


if __name__ == "__main__":
    main()
