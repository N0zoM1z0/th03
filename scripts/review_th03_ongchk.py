#!/usr/bin/env python3
"""Review the complete binary-only ONGCHK intake; no authored or exact credit."""
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
from capstone.x86_const import X86_OP_IMM
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact
from lib.zun import parse_launcher

ROOT = Path(__file__).resolve().parents[1]
REVISION = "b6ba5b0a529edbb31efdf8c0e939263804f8ee47"
SOURCE = "libs/kaja/ongchk.com"
# Contiguous analysis regions, including shared tails; not twelve authored functions.
RANGES = [("startup", 0x100, 39, "int"), ("controller", 0x127, 121, "ret"),
          ("detector_3", 0x1a0, 167, "jmp"), ("detector_2", 0x247, 123, "jmp"),
          ("shared_success", 0x2c2, 27, "ret"), ("shared_failure", 0x2dd, 7, "ret"),
          ("ram_controller", 0x2e4, 23, "ret"), ("ram_write", 0x2fb, 173, "ret"),
          ("ram_read", 0x3a8, 128, "ret"), ("dummy_read", 0x428, 33, "ret"),
          ("compare", 0x449, 12, "ret"), ("register_write", 0x455, 39, "ret")]
CALL_ENTRIES = {0x127, 0x1a0, 0x247, 0x2e4, 0x2fb, 0x3a8, 0x428, 0x449, 0x455}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decode(data):
    if len(data) != 926:
        raise ValueError("complete ONGCHK size differs")
    cs = Cs(CS_ARCH_X86, CS_MODE_16)
    cs.detail = True
    boundaries, rows = set(), []
    for name, start, size, terminal in RANGES:
        body = data[start - 0x100:start - 0x100 + size]
        instructions = list(cs.disasm(body, start))
        if sum(i.size for i in instructions) != size or instructions[-1].mnemonic != terminal:
            raise ValueError("incomplete ONGCHK region/terminal boundary")
        if name == "startup" and instructions[-1].op_str != "0x21":
            raise ValueError("ONGCHK termination interrupt differs")
        boundaries.update(i.address for i in instructions)
        edges = []
        for i in instructions:
            if i.mnemonic.startswith(("j", "loop")) or i.mnemonic == "call":
                if not i.operands or i.operands[0].type != X86_OP_IMM:
                    raise ValueError("unexpected indirect ONGCHK edge")
                edges.append(dict(instruction=i.address, kind=i.mnemonic, target=i.operands[0].imm))
        rows.append(dict(name=name, start=start, size=size, terminal=terminal,
                         instruction_count=len(instructions), body_sha256=sha(body), edges=edges))
    for row in rows:
        for edge in row["edges"]:
            if edge["target"] not in boundaries:
                raise ValueError("ONGCHK branch enters data or instruction operand")
            if edge["kind"] == "call" and edge["target"] not in CALL_ENTRIES:
                raise ValueError("ONGCHK call enters an unreviewed entry/shared tail")
    return rows


def runtime_case(data, *, tail="", boards=(), fallback=None, override=255,
                 rom_version=None, ram="pass", instruction_budget=300000):
    """Real instructions, constructed ROM/PSP/DOS and deterministic port behavior."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INTR, UC_HOOK_INSN
    from unicorn.x86_const import (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES,
                                  UC_X86_REG_SS, UC_X86_REG_SP, UC_X86_REG_AX,
                                  UC_X86_REG_IP, UC_X86_REG_EFLAGS,
                                  UC_X86_INS_IN, UC_X86_INS_OUT)
    if len(data) != 926 or len(tail.encode("ascii")) > 126:
        raise ValueError("invalid ONGCHK runtime input size")
    if ram not in ("pass", "mismatch", "write-timeout", "read-ready-stall", "read-busy-stall",
                   "read-data-busy-stall", "register-busy-stall"):
        raise ValueError("unknown constructed RAM mode")
    board_map = dict(boards)
    if any(base & 255 != 0x88 or kind not in (2, 3) for base, kind in boards):
        raise ValueError("invalid constructed port profile")
    uc = Uc(UC_ARCH_X86, UC_MODE_16)
    uc.mem_map(0, 0x100000)
    base = 0x20000
    uc.mem_write(base + 0x100, data)
    uc.mem_write(base + 0x49c, bytes([override]))
    command = tail.encode("ascii")
    uc.mem_write(base + 0x80, bytes([len(command)]) + command + b"\r")
    if rom_version is not None:
        uc.mem_write(0xfd802, struct.pack("<HH", 0x2a27, rom_version))
    for register in (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS):
        uc.reg_write(register, 0x2000)
    uc.reg_write(UC_X86_REG_SP, 0xfffc)  # wrapper retains the selected-option count
    uc.reg_write(UC_X86_REG_EFLAGS, 0x602)  # start DF/IF set; startup must clear DF
    state = dict(steps=0, detectors=[], phase="detect", read_index=0, registers={},
                 written=bytearray(), trace=[], stop=None, errors=[])

    def guarded(callback, default=None):
        def run(*args):
            try:
                return callback(*args)
            except Exception as error:
                state["errors"].append(str(error))
                uc.emu_stop()
                return default
        return run

    def code(uc, address, size, user):
        if state["steps"] == instruction_budget:
            state["stop"] = dict(kind="instruction-budget", ip=address - base)
            uc.emu_stop()
            return
        state["steps"] += 1
        inner = address - base
        if inner in (0x1a0, 0x247):
            state["detectors"].append(3 if inner == 0x1a0 else 2)
        elif inner == 0x2fb:
            state["phase"] = "write"
        elif inner == 0x3a8:
            state["phase"] = "read"

    def interrupt(uc, number, user):
        ax = uc.reg_read(UC_X86_REG_AX)
        if number != 0x21 or ax >> 8 != 0x4c:
            raise ValueError("unexpected ONGCHK DOS interrupt")
        state["stop"] = dict(kind="modeled-dos-exit", code=ax & 255)
        uc.emu_stop()

    def output(uc, port, size, value, user):
        if size != 1:
            raise ValueError("unexpected ONGCHK port width")
        state["trace"].append(["out", port, value])
        ports = struct.unpack("<4H", uc.mem_read(base + 0x49e, 8))
        if state["phase"] != "detect":
            if port == ports[2]:
                state["registers"][port] = value
            elif port == ports[3]:
                register = state["registers"].get(ports[2])
                if state["phase"] == "write" and register == 8:
                    state["written"].append(value)
                elif register == 0:
                    state["ram_mode_register"] = value
            else:
                raise ValueError("RAM path wrote an unexpected port")
        elif port & 255 == 0x88:
            state["registers"][port] = value
        elif port not in (0x5f, 0xa460, 0xa66e, 0x6e) and port & 255 != 0x8a:
            raise ValueError("detector wrote an unexpected port")

    def input_port(uc, port, size, user):
        if size != 1:
            raise ValueError("unexpected ONGCHK port width")
        ports = struct.unpack("<4H", uc.mem_read(base + 0x49e, 8))
        if state["phase"] != "detect":
            if port == ports[2]:
                ip = uc.reg_read(UC_X86_REG_IP)
                if ram == "write-timeout" and state["phase"] == "write":
                    value = 0
                elif ram == "read-ready-stall" and state["phase"] == "read" and ip in (0x406, 0x407):
                    value = 0
                elif (state["phase"] == "read" and
                      ((ram == "read-busy-stall" and ip == 0x3fe) or
                       (ram == "read-data-busy-stall" and ip in (0x40c, 0x40d)) or
                       ram == "register-busy-stall")):
                    value = 0x80
                else:
                    value = 8
            elif port == ports[3] and state["phase"] == "read":
                index = state["read_index"] - 2  # real dummy-read routine runs twice
                value = state["written"][index] if 0 <= index < len(state["written"]) else 0
                if ram == "mismatch" and index == 31:
                    value ^= 1
                state["read_index"] += 1
            else:
                raise ValueError("RAM path read an unexpected port")
        elif port == 0xa460:
            value = 7 if any(kind == 3 for kind in board_map.values()) else 255
        elif port == 0xa66e:
            value = 255
        elif port & 255 == 0x8a:
            pair = port - 2
            value = (0xaa if pair == fallback and state["registers"].get(pair) == 0x0b
                     else 1 if pair in board_map else 255)
        elif port & 255 in (0x8c, 0x8e):
            pair = port - (4 if port & 255 == 0x8c else 6)
            value = 255 if board_map.get(pair) == 3 else 0
        else:
            raise ValueError("detector read an unexpected port")
        state["trace"].append(["in", port, value])
        return value

    uc.hook_add(UC_HOOK_CODE, guarded(code))
    uc.hook_add(UC_HOOK_INTR, guarded(interrupt))
    uc.hook_add(UC_HOOK_INSN, guarded(input_port, 0), None, 1, 0, UC_X86_INS_IN)
    uc.hook_add(UC_HOOK_INSN, guarded(output), None, 1, 0, UC_X86_INS_OUT)
    uc.emu_start(base + 0x100, 0x30000, count=instruction_budget + 2)
    if state["errors"]:
        raise ValueError(state["errors"][0])
    if not state["stop"]:
        raise ValueError("ONGCHK failed to reach an explicit bounded stop")
    trace = state["trace"]
    return dict(tail=tail, tail_length=len(command), boards=list(boards), fallback=fallback,
                override=override, rom_version=rom_version, ram_model=ram,
                stop=state["stop"], steps=state["steps"], detector_order=state["detectors"],
                priority=uc.mem_read(base + 0x4a7, 1)[0], result=uc.mem_read(base + 0x49d, 1)[0],
                ports=list(struct.unpack("<4H", uc.mem_read(base + 0x49e, 8))),
                final_sp=uc.reg_read(UC_X86_REG_SP), final_es=uc.reg_read(UC_X86_REG_ES),
                final_flags=uc.reg_read(UC_X86_REG_EFLAGS), phase=state["phase"],
                ram_bytes_written=len(state["written"]), ram_write_sha256=sha(state["written"]),
                ram_data_reads=state["read_index"],
                buffer_sha256=sha(bytes(uc.mem_read(base + 0x4a8, 32))),
                port_trace_count=len(trace),
                port_trace_sha256=sha(json.dumps(trace, separators=(",", ":")).encode()),
                detector_pairs=[p for kind, p, value in trace if kind == "out" and p & 255 == 0x88],
                output_6e=[v for kind, p, v in trace if kind == "out" and p == 0x6e])


def runtime_matrix(data):
    cases = []
    def case(expected, **kwargs):
        result = runtime_case(data, **kwargs)
        if (result["stop"] != dict(kind="modeled-dos-exit", code=expected) or
                result["result"] != expected or result["final_sp"] != 0xfffc or
                result["final_flags"] & 0x400 or
                result["final_flags"] & 1 != (1 if expected == 0 else 0)):
            # Fallback JMPs use shared RET tails, bypassing the controller's CLC.
            raise ValueError("ONGCHK terminal result/stack/flags differs")
        cases.append(result)
        return result
    case(0)
    for pair in (0x88, 0x188, 0x288, 0x388):
        result = case(1, fallback=pair)
        if result["ports"] != [pair, pair + 2, pair + 4, pair + 6] or result["ram_bytes_written"]:
            raise ValueError("fallback port layout/RAM gate differs")
    for kind, pair in ((2, 0x88), (2, 0x388), (3, 0x188), (3, 0x288)):
        for ram, expected in (("pass", kind + 2), ("mismatch", kind), ("write-timeout", kind)):
            result = case(expected, boards=((pair, kind),), ram=ram)
            if result["ports"] != [pair, pair + 2, pair + 4, pair + 6]:
                raise ValueError("detector port layout differs")
            if ram == "write-timeout":
                if result["ram_bytes_written"] != 1 or result["ram_data_reads"] != 0:
                    raise ValueError("bounded write timeout differs")
            elif (result["ram_bytes_written"] != 32 or result["ram_data_reads"] != 34 or
                  result["ram_write_sha256"] != sha(data[0x37c:0x39c]) or
                  ((result["buffer_sha256"] == result["ram_write_sha256"]) != (ram == "pass"))):
                raise ValueError("complete RAM transfer/compare differs")
    both = ((0x188, 3), (0x88, 2))
    for tail, expected, priority, order in [
            ("", 5, 0, [3]), ("8", 5, 0, [3]), ("x" * 56, 4, 1, [2]),
            ("8" + " " * 31, 4, 1, [2]), (" " * 3 + "8" + "x" * 28, 4, 1, [2]),
            ("x" * 32, 5, 0, [3])]:
        result = case(expected, tail=tail, boards=both)
        if result["priority"] != priority or result["detector_order"] != order:
            raise ValueError("PSP length-byte priority contract differs")
    result = case(5, tail="x" * 56, boards=((0x188, 3),))
    if result["detector_order"] != [2, 3]:
        raise ValueError("priority detector fallback order differs")
    for kind in (2, 3):
        case(kind + 2, boards=((0x588, kind),), override=5)
    case(1, fallback=0x588, override=5)
    case(0, fallback=0x188, override=5)
    for rom in (5, 6):
        result = case(4 if rom == 5 else 5, boards=both, rom_version=rom)
        if result["output_6e"] != ([] if rom == 5 else [1]):
            raise ValueError("ROM-version detector/control-port gate differs")
    stalls = []
    for mode, polling_ips in (("read-ready-stall", {0x407, 0x408, 0x40a}),
                             ("read-busy-stall", {0x3fe, 0x3ff, 0x401}),
                             ("read-data-busy-stall", {0x40d, 0x40e, 0x410}),
                             ("register-busy-stall", {0x461, 0x462, 0x464})):
        result = runtime_case(data, boards=((0x188, 3),), ram=mode, instruction_budget=100000)
        if (result["stop"]["kind"] != "instruction-budget" or result["phase"] != "read" or
                result["ram_bytes_written"] != 32 or result["result"] != 3 or
                result["stop"]["ip"] not in polling_ips):
            raise ValueError("read stall did not retain nonterminal polling path")
        stalls.append(result)
    return cases, stalls


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
    for path in ("config/targets.toml", "scripts/review_th03_ongchk.py", "scripts/lib/zun.py", "scripts/lib/targets.py"):
        read(path)
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-zun")
    stored = read_verified_artifact(ROOT, artifact)
    decoded = read(config["decoded_path"])
    restoration = json.loads(read(config["diet_receipt"]))
    expected = next(a for a in diet["artifacts"] if a["id"] == "th03-zun")
    lineage = next(o for o in restoration["observations"] if o["artifact"] == "th03-zun")
    if (config["reference_revision"] != REVISION or sha(decoded) != expected["decoded_sha256"] or
            sha(frozen[config["diet_receipt"]]) != config["diet_receipt_sha256"] or
            lineage["stored"]["sha256"] != sha(stored) or lineage["decoded"]["sha256"] != sha(decoded) or
            not restoration["restoration_checks_pass"]):
        raise ValueError("ONGCHK decoded restoration lineage differs")
    upstream = subprocess.check_output(["git", "show", f"{REVISION}:{SOURCE}"], cwd=ROOT / "_reference/ReC98")
    pin = next(p for p in config["payloads"] if p["option"] == "-1")
    payload = parse_launcher(decoded, 223)["payloads"][0]
    target = decoded[payload["decoded_file_offset"]:payload["decoded_file_offset"] + payload["size"]]
    if pin["reference_path"] != SOURCE or target != upstream or sha(target) != pin["sha256"]:
        raise ValueError("complete ONGCHK frozen binary equality differs")
    rows = decode(target)
    cases, stalls = runtime_matrix(target)
    for path, data in frozen.items():
        if (ROOT / path).read_bytes() != data:
            raise ValueError("ONGCHK diagnostic input changed")
    if read_verified_artifact(ROOT, artifact) != stored:
        raise ValueError("canonical ZUN changed")
    if subprocess.check_output(["git", "show", f"{REVISION}:{SOURCE}"], cwd=ROOT / "_reference/ReC98") != upstream:
        raise ValueError("frozen ONGCHK input changed")
    result = dict(kind="th03-ongchk-complete-binary-intake-review", observed_utc=datetime.now(timezone.utc).isoformat(),
                  reference_revision=REVISION, upstream_binary=SOURCE, upstream_sha256=sha(upstream),
                  stored_sha256=sha(stored), decoded_sha256=sha(decoded), payload=payload,
                  complete_upstream_raw_equal=True, code_regions=rows, runtime_cases=cases, polling_stalls=stalls,
                  byte_accounting=dict(code=892, initialized_data=34, stored_total=926,
                                       external_mutable_workspace_start=0x49e, external_mutable_workspace_size=42),
                  runtime_scope="Constructed DOS exit/PSP/ROM/port/RAM model; no actual device or kernel observation",
                  tools=dict(capstone_distribution=version("capstone"), unicorn_distribution=version("unicorn")),
                  inputs={p: sha(d) for p, d in frozen.items()}, diagnostic_checks_pass=True,
                  compiler_observation=False, fresh_build=False, authored_source=False,
                  source_acceptance=False, exact_acceptance=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS complete 926-byte binary intake, 12 shared-tail regions, {len(cases)} terminal/{len(stalls)} bounded polling cases; no acceptance: {args.output}")


if __name__ == "__main__":
    main()
