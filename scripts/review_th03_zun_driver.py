#!/usr/bin/env python3
"""Review the complete frozen sprite16 candidate against derived TH03 bytes.

Source-labelled ranges are diagnostics. This script grants no source/exact
acceptance, performs no compiler replay, and never uses packed database code.
"""
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
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact
from lib.zun import parse_launcher

ROOT = Path(__file__).resolve().parents[1]
REVISION = "b6ba5b0a529edbb31efdf8c0e939263804f8ee47"
SOURCE = "libs/sprite16/sprite16.asm"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def procedure_ranges(text, trailing_data_start):
    matches = list(re.finditer(r"^(sub_([0-9A-F]+))\s+proc\s+(near|far)\s*$", text, re.M))
    if not matches:
        raise ValueError("no source procedures")
    rows = []
    previous_end = 0x100
    for index, match in enumerate(matches):
        endp = re.search(r"^" + re.escape(match[1]) + r"\s+endp\s*$", text[match.end():], re.M)
        if endp is None:
            raise ValueError("source procedure lacks ENDP")
        endp_end = match.end() + endp.end()
        next_start = matches[index + 1].start() if index + 1 < len(matches) else text.index(
            "aGbgvgkpkpmvOFs", endp_end)
        if endp_end > next_start:
            raise ValueError("overlapping source procedures")
        gap_text = text[endp_end:next_start]
        zeros = sum(int(n[:-1], 16) if n.lower().endswith("h") else int(n)
                    for n in re.findall(r"db\s+(\w+)\s+dup\(0\)", gap_text, re.I))
        nops = len(re.findall(r"^\s*nop\s*$", gap_text, re.M))
        digits = 16 if "0123456789ABCDEF" in gap_text else 0
        start = int(match[2], 16)
        next_address = int(matches[index + 1][2], 16) if index + 1 < len(matches) else trailing_data_start
        end = next_address - zeros - nops - digits
        if start < previous_end or end <= start:
            raise ValueError("invalid source-labelled procedure range")
        previous_end = next_address
        rows.append(dict(name=match[1], candidate_distance=match[3], start=start,
                         size=end - start, gap_zero_bytes=zeros, gap_nops=nops,
                         gap_digit_bytes=digits))
    return rows


def decode_procedures(data, ranges):
    disassembler = Cs(CS_ARCH_X86, CS_MODE_16)
    disassembler.detail = True
    rows, entries, boundaries = [], {r["start"] for r in ranges}, set()
    for row in ranges:
        start, size = row["start"], row["size"]
        if start < 0x100 or size <= 0 or start + size - 0x100 > len(data):
            raise ValueError("procedure exceeds driver bytes")
        body = data[start - 0x100:start - 0x100 + size]
        instructions = list(disassembler.disasm(body, start))
        if sum(i.size for i in instructions) != size:
            raise ValueError("procedure does not completely decode")
        if instructions[-1].mnemonic not in {"ret", "iret"}:
            raise ValueError("procedure does not end at a reviewed return")
        if (row["candidate_distance"] == "far") != (instructions[-1].mnemonic == "iret"):
            raise ValueError("unexpected interrupt versus near-return boundary")
        boundaries.update(i.address for i in instructions)
        edges = []
        for instruction in instructions:
            if instruction.mnemonic.startswith(("j", "loop")) or instruction.mnemonic == "call":
                target = (instruction.operands[0].imm if instruction.operands and
                          instruction.operands[0].type == X86_OP_IMM else None)
                edges.append(dict(instruction=instruction.address, kind=instruction.mnemonic,
                                  target=target, operands=instruction.op_str))
        rows.append(dict(row, body_sha256=sha(body), instruction_count=len(instructions),
                         return_kind=instructions[-1].mnemonic,
                         return_operands=instructions[-1].op_str, edges=edges))
    for row in rows:
        for edge in row["edges"]:
            if edge["target"] is not None and edge["target"] not in boundaries:
                raise ValueError("direct control flow enters noninstruction bytes")
            if edge["kind"] == "call" and edge["target"] is not None and edge["target"] not in entries:
                raise ValueError("direct call enters an unreviewed procedure interior")
    return rows


def runtime_hazards(data):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INTR
    from unicorn.x86_const import (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES,
                                  UC_X86_REG_SS, UC_X86_REG_SP, UC_X86_REG_AX,
                                  UC_X86_REG_SI, UC_X86_REG_EFLAGS)
    def machine():
        uc = Uc(UC_ARCH_X86, UC_MODE_16)
        uc.mem_map(0, 0x100000)
        uc.mem_write(0x20100, data)
        for register in (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS):
            uc.reg_write(register, 0x2000)
        uc.reg_write(UC_X86_REG_SP, 0xff00)
        uc.reg_write(UC_X86_REG_EFLAGS, 2)
        return uc
    uc = machine()
    uc.mem_write(0x30100, data)
    uc.mem_write(0x42 * 4, struct.pack("<HH", 0x22a, 0x3000))
    uc.mem_write(0x30f38, struct.pack("<HH", 0x4567, 0xabcd))
    stop = {}
    def interrupt(uc, number, user):
        stop.update(number=number, ax=uc.reg_read(UC_X86_REG_AX))
        uc.emu_stop()
    uc.hook_add(UC_HOOK_INTR, interrupt)
    uc.emu_start(0x202ad, 0x30000, count=1000)
    vector = list(struct.unpack("<HH", uc.mem_read(0x42 * 4, 4)))
    if stop != dict(number=0x21, ax=0x4900) or vector != [0, 0x4567]:
        raise ValueError("reviewed uninstall prefix differs")
    numeric = []
    for count in (1, 0):
        uc = machine()
        uc.mem_write(0x2ff00, struct.pack("<H", 0xffff))
        uc.mem_write(0x21070, struct.pack("<HH", count, 0x1200))
        uc.mem_write(0x210f2, struct.pack("<H", 0x1072))
        uc.mem_write(0x21200, b"123\0")
        uc.reg_write(UC_X86_REG_SI, 0x1200)
        stopped = []
        def code(uc, address, size, user):
            if address == 0x2ffff:
                stopped.append(True)
                uc.emu_stop()
        uc.hook_add(UC_HOOK_CODE, code)
        uc.emu_start(0x20a24, 0x30000, count=1000)
        value = uc.reg_read(UC_X86_REG_AX)
        if not stopped or value != (0 if count else 123):
            raise ValueError("reviewed optional-number prefix differs")
        numeric.append(dict(initial_count=count, previous_si=0x1200, string="123",
                            returned_ax=value, final_count=struct.unpack("<H", uc.mem_read(0x21070, 2))[0]))
    return dict(uninstall=dict(old_vector=[0xabcd, 0x4567], written_vector=vector,
                               stop=stop, scope="Stop at first DOS free; no kernel/free/hardware execution"),
                optional_numeric=numeric, scope="Constructed state; complete target instructions, no game-runtime claim")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    frozen = {}
    def read(path):
        data = (ROOT / path).read_bytes()
        frozen[path] = data
        return data
    config = tomllib.loads(read("config/th03_zun_launcher.toml").decode())
    if config["reference_revision"] != REVISION:
        raise ValueError("reference revision differs")
    diet = tomllib.loads(read("config/th03_diet.toml").decode())
    for path in ("config/targets.toml", "scripts/review_th03_zun_driver.py", "scripts/lib/zun.py",
                 "scripts/lib/targets.py"):
        read(path)
    stored = read_verified_artifact(ROOT, find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-zun"))
    decoded = read(config["decoded_path"])
    expected = next(a for a in diet["artifacts"] if a["id"] == "th03-zun")
    if sha(decoded) != expected["decoded_sha256"]:
        raise ValueError("decoded identity differs")
    restoration = json.loads(read(config["diet_receipt"]))
    lineage = next(o for o in restoration["observations"] if o["artifact"] == "th03-zun")
    if (sha(frozen[config["diet_receipt"]]) != config["diet_receipt_sha256"] or
            lineage["stored"]["sha256"] != sha(stored) or lineage["decoded"]["sha256"] != sha(decoded) or
            not restoration["restoration_checks_pass"]):
        raise ValueError("restoration lineage differs")
    source = subprocess.check_output(["git", "show", f"{REVISION}:{SOURCE}"], cwd=ROOT / "_reference/ReC98")
    text = source.decode("shift_jis", errors="surrogateescape")
    proc_ranges = procedure_ranges(text, 0xc80)
    if len(proc_ranges) != 55:
        raise ValueError("complete source procedure catalogue differs")
    payload = parse_launcher(decoded, 223)["payloads"][3]
    target = decoded[payload["decoded_file_offset"]:payload["decoded_file_offset"] + payload["size"]]
    source_md5 = re.search(r"Input\s+MD5\s*:\s*([0-9A-Fa-f]{32})", text)[1].lower()
    if hashlib.md5(target).hexdigest() != source_md5:
        raise ValueError("decoded driver does not bind to original source input MD5")
    target_rows = decode_procedures(target, proc_ranges)
    startup = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(target[:2], 0x100))
    if (len(startup) != 1 or startup[0].mnemonic != "jmp" or
            startup[0].op_str != "0x10c" or target[2:12] != b"SPRITE16\0\x04"):
        raise ValueError("startup/signature boundary differs")
    procedure_offsets = {address - 0x100 for row in proc_ranges
                         for address in range(row["start"], row["start"] + row["size"])}
    pin = next(p for p in config["payloads"] if p["option"] == "-4")
    rounds = []
    for path in pin["cold_paths"]:
        candidate = read(path)
        if sha(candidate) != pin["sha256"] or len(candidate) != len(target):
            raise ValueError("candidate payload identity differs")
        rows = decode_procedures(candidate, proc_ranges)
        for target_row, row in zip(target_rows, rows):
            if target_row["edges"] != row["edges"] or target_row["return_kind"] != row["return_kind"]:
                raise ValueError("candidate control-flow shape differs")
            row["target_body_raw_equal"] = target_row["body_sha256"] == row["body_sha256"]
        rounds.append(dict(path=path, procedures=rows, runtime_hazards=runtime_hazards(candidate)))
        rounds[-1]["raw_differing_bytes"] = sum(a != b for a, b in zip(target, candidate))
        if (sum(r["target_body_raw_equal"] for r in rows) != 52 or
                rounds[-1]["raw_differing_bytes"] != 10):
            raise ValueError("complete raw comparison differs")
        if any(a != b for offset, (a, b) in enumerate(zip(target, candidate))
               if offset not in procedure_offsets):
            raise ValueError("candidate differs outside complete procedure bodies")
        rounds[-1]["outside_procedures_raw_equal"] = True
    if rounds[0]["procedures"] != rounds[1]["procedures"]:
        raise ValueError("cached rounds differ")
    target_runtime = runtime_hazards(target)
    if any(r["runtime_hazards"] != target_runtime for r in rounds):
        raise ValueError("runtime hazard vector differs")
    service_table = list(struct.unpack_from("<9H", target, 0x103e - 0x100))
    if service_table != [0x520, 0x540, 0x364, 0x340, 0x346, 0x34c, 0x352, 0x358, 0x35e]:
        raise ValueError("resident service table differs")
    for path, data in frozen.items():
        if (ROOT / path).read_bytes() != data:
            raise ValueError("input changed during static/cached review")
    if read_verified_artifact(ROOT, find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-zun")) != stored:
        raise ValueError("canonical target changed")
    if subprocess.check_output(["git", "show", f"{REVISION}:{SOURCE}"], cwd=ROOT / "_reference/ReC98") != source:
        raise ValueError("frozen reference source changed")
    result = dict(kind="th03-zun-driver-complete-candidate-review", observed_utc=datetime.now(timezone.utc).isoformat(),
                  reference_revision=REVISION, source=SOURCE, source_sha256=sha(source),
                  source_input_md5=source_md5, stored_sha256=sha(stored), decoded_sha256=sha(decoded),
                  driver_sha256=sha(target), driver_size=len(target), target_procedures=target_rows,
                  byte_accounting=dict(procedure_bodies=len(procedure_offsets), startup_instruction=2,
                                       signature_and_version=10, source_labelled_gaps=88,
                                       trailing_data=0x1180 - 0xc80),
                  tools=dict(capstone_distribution=version("capstone"),
                             unicorn_distribution=version("unicorn")),
                  service_table=service_table, target_runtime_hazards=target_runtime, rounds=rounds,
                  inputs={p: sha(d) for p, d in frozen.items()}, diagnostic_checks_pass=True,
                  fresh_build=False, source_acceptance=False, exact_acceptance=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS 55 candidate procedure diagnostics; 52 raw bodies agree; full driver raw failure and no acceptance: {args.output}")


if __name__ == "__main__":
    main()
