#!/usr/bin/env python3
"""Review res_yume root and its direct library contracts using guarded bytes.

Whole cached payload equality does not grant startup/runtime-library ownership,
fresh maintained-source acceptance or exactness.
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
from lib.omf import describe_omf
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact
from lib.zun import parse_launcher

ROOT = Path(__file__).resolve().parents[1]
REVISION = "b6ba5b0a529edbb31efdf8c0e939263804f8ee47"
SOURCES = ["th03/res_yume.cpp", "th02/res_init.cpp", "th02/formats/cfg_init.c",
           "th03/resident.hpp", "th03/formats/cfg.hpp", "th02/formats/cfg.hpp",
           "th03/playchar.hpp", "th03/score.hpp", "th02/score.h", "th03/common.h",
           "th01/rank.h", "libs/master.lib/master.hpp", "libs/master.lib/func.hpp",
           "platform.h", "th02/snd/snd.h",
           "libs/master.lib/func.inc", "libs/master.lib/resdata.asm",
           "libs/master.lib/graph_clear.asm", "libs/master.lib/grp[data].asm",
           *[f"libs/master.lib/{name}.asm" for name in
             ["dos_free", "dos_axdx", "dos_create", "dos_puts2", "dos_close", "dos_write", "dos_seek"]]]
RANGES = [("cfg_init", 0x367, 97), ("main", 0x3c8, 225),
          ("GRAPH_CLEAR", 0x4aa, 35), ("RESDATA_EXIST", 0x4ce, 72),
          ("RESDATA_CREATE", 0x516, 117), ("DOS_FREE", 0x58c, 16),
          ("DOS_AXDX", 0x59c, 21), ("DOS_CREATE", 0x5b2, 20),
          ("DOS_PUTS2", 0x5c6, 39), ("DOS_CLOSE", 0x5ee, 21),
          ("DOS_WRITE", 0x604, 26), ("DOS_SEEK", 0x61e, 28), ("N_SCOPY@", 0x7ca, 28)]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decode(data):
    if len(data) != 5618:
        raise ValueError("complete resident payload size differs")
    cs = Cs(CS_ARCH_X86, CS_MODE_16)
    cs.detail = True
    entries, boundaries, rows = {start for _, start, _ in RANGES}, set(), []
    for name, start, size in RANGES:
        body = data[start - 0x100:start - 0x100 + size]
        instructions = list(cs.disasm(body, start))
        if sum(i.size for i in instructions) != size or instructions[-1].mnemonic != "ret":
            raise ValueError("incomplete resident procedure/return boundary")
        boundaries.update(i.address for i in instructions)
        edges = []
        for i in instructions:
            if i.mnemonic.startswith(("j", "loop")) or i.mnemonic == "call":
                if not i.operands or i.operands[0].type != X86_OP_IMM:
                    raise ValueError("unexpected indirect resident edge")
                edges.append(dict(instruction=i.address, kind=i.mnemonic, target=i.operands[0].imm))
        rows.append(dict(name=name, start=start, size=size, body_sha256=sha(body),
                         return_operands=instructions[-1].op_str, instruction_count=len(instructions), edges=edges))
    for row in rows:
        for edge in row["edges"]:
            if edge["target"] not in boundaries:
                raise ValueError("resident branch enters data or instruction operand")
            if edge["kind"] == "call" and edge["target"] not in entries:
                raise ValueError("resident call enters a procedure interior")
    return rows


def root_case(data, arguments=(), resident=False, allocations=(0x800,), existing_file=None,
              open_handle=5, create_error=False, write_error=False, seek_error=False,
              close_error=False, free_error=False, mcb_prefix=False, resident_id=b"YUMEConfig",
              resident_paragraphs=0x10):
    """Invoke the complete main, bypassing unreviewed CRT startup/argv/exit."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INTR, UC_HOOK_INSN
    from unicorn import x86_const as reg
    uc = Uc(UC_ARCH_X86, UC_MODE_16)
    uc.mem_map(0, 0x100000)
    uc.mem_write(0x20100, data)
    for name in ("CS", "DS", "ES", "SS"):
        uc.reg_write(getattr(reg, "UC_X86_REG_" + name), 0x2000)
    uc.reg_write(reg.UC_X86_REG_SP, 0xff00)
    uc.reg_write(reg.UC_X86_REG_EFLAGS, 0x402)  # search clears inherited DF
    uc.reg_write(reg.UC_X86_REG_SI, 0xabba)
    uc.reg_write(reg.UC_X86_REG_DI, 0xcdda)
    uc.reg_write(reg.UC_X86_REG_BP, 0x1234)
    argv = ["res_yume", *arguments]
    pointers = []
    for i, argument in enumerate(argv):
        pointer = 0x1900 + i * 0x80
        raw = argument.encode("ascii")
        if len(raw) > 126 or i > 3:
            raise ValueError("constructed argv exceeds fixture bounds")
        uc.mem_write(0x20000 + pointer, raw + b"\0")
        pointers.append(pointer)
    uc.mem_write(0x21800, struct.pack("<" + "H" * len(pointers), *pointers))
    uc.mem_write(0x2ff00, struct.pack("<HHH", 0xffff, len(argv), 0x1800))
    uc.mem_write(0x7000, struct.pack("<H", 0x1000))
    resident_segment = 0x1014 if mcb_prefix else 0x1001
    if mcb_prefix:
        uc.mem_write(0x10000, b"M" + struct.pack("<HH", 0, 0x12))
    uc.mem_write((resident_segment - 1) * 16,
                 b"Z" + struct.pack("<HH", 0xffff if resident else 0, resident_paragraphs))
    uc.mem_write(resident_segment * 16, resident_id + b"\xa5" * (256 - len(resident_id)))
    uc.mem_write(0x70, b"\xb6" * 0x110)
    uc.mem_write(0xa8000, b"\xa5" * 32000)
    events, stdout, ports, errors, stopped = [], [], [], [], []
    allocation_queue = list(allocations)
    allocated = []
    file_data = None if existing_file is None else bytearray(existing_file)
    position, strategy = 0, 0
    def flags(failed, ax=None):
        value = uc.reg_read(reg.UC_X86_REG_EFLAGS)
        uc.reg_write(reg.UC_X86_REG_EFLAGS, (value | 1) if failed else (value & ~1))
        if ax is not None:
            uc.reg_write(reg.UC_X86_REG_AX, ax)
    def interrupt(uc, number, user):
        nonlocal file_data, position, strategy
        try:
            if number != 0x21:
                raise ValueError("unexpected modeled resident interrupt")
            ax, bx, cx, dx, ds, es = [uc.reg_read(getattr(reg, "UC_X86_REG_" + n))
                                      for n in ("AX", "BX", "CX", "DX", "DS", "ES")]
            ah = ax >> 8
            if ah == 2:
                stdout.append(dx & 255)
            elif ah == 0x52:
                uc.reg_write(reg.UC_X86_REG_ES, 0x700)
                uc.reg_write(reg.UC_X86_REG_BX, 2)
                events.append(dict(kind="mcb-head"))
            elif ax == 0x5800:
                flags(False, strategy)
                events.append(dict(kind="get-strategy", strategy=strategy))
            elif ax == 0x5801:
                strategy = bx
                flags(False)
                events.append(dict(kind="set-strategy", strategy=strategy))
            elif ah == 0x48:
                if not allocation_queue:
                    raise ValueError("constructed allocation queue exhausted")
                segment = allocation_queue.pop(0)
                flags(segment is None, 8 if segment is None else segment)
                if segment is not None:
                    uc.mem_write(segment * 16, b"\xa5" * (bx * 16))
                    allocated.append(segment)
                events.append(dict(kind="allocate", paragraphs=bx, segment=segment, modeled_failure=segment is None))
            elif ah == 0x49:
                flags(free_error, 7 if free_error else ax)
                events.append(dict(kind="free-request", segment=es, modeled_failure=free_error))
            elif ah in (0x3d, 0x3c):
                filename = bytes(uc.mem_read(ds * 16 + dx, 128)).split(b"\0", 1)[0]
                if filename != b"yume.cfg":
                    raise ValueError("modeled config filename differs")
                if ah == 0x3d:
                    flags(file_data is None, 2 if file_data is None else open_handle)
                    events.append(dict(kind="open", handle=None if file_data is None else open_handle))
                else:
                    flags(create_error, 5 if create_error else 6)
                    if not create_error:
                        file_data, position = bytearray(), 0
                    events.append(dict(kind="create", attributes=cx, modeled_failure=create_error))
            elif ah == 0x42:
                offset = cx * 65536 + dx
                if not seek_error:
                    position = offset
                flags(seek_error, 1 if seek_error else position & 65535)
                if not seek_error:
                    uc.reg_write(reg.UC_X86_REG_DX, position >> 16)
                events.append(dict(kind="seek", handle=bx, offset=offset, mode=ax & 255, modeled_failure=seek_error))
            elif ah == 0x40:
                raw = bytes(uc.mem_read(ds * 16 + dx, cx))
                failed = write_error or file_data is None
                events.append(dict(kind="write", handle=bx, offset=position, bytes=raw.hex(), modeled_failure=failed))
                if not failed:
                    if len(file_data) < position + cx:
                        file_data.extend(b"\0" * (position + cx - len(file_data)))
                    file_data[position:position + cx] = raw
                    position += cx
                flags(failed, 5 if failed else cx)
            elif ah == 0x3e:
                events.append(dict(kind="close", handle=bx, modeled_failure=close_error))
                flags(close_error, 6 if close_error else ax)
            else:
                raise ValueError("unexpected resident DOS model function")
        except Exception as error:
            errors.append(str(error))
            uc.emu_stop()
    def code(uc, address, size, user):
        if address == 0x2ffff:
            stopped.append(True)
            uc.emu_stop()
    def output(uc, port, size, value, user):
        ports.append(dict(port=port, size=size, value=value))
    uc.hook_add(UC_HOOK_INTR, interrupt)
    uc.hook_add(UC_HOOK_CODE, code)
    uc.hook_add(UC_HOOK_INSN, output, None, 1, 0, reg.UC_X86_INS_OUT)
    uc.emu_start(0x203c8, 0x30000, count=100000)
    if errors or not stopped:
        raise ValueError(errors[0] if errors else "resident main missed bounded return")
    preserved = {name: uc.reg_read(getattr(reg, "UC_X86_REG_" + name)) for name in ("SI", "DI", "BP", "DS", "SP")}
    if preserved != dict(SI=0xabba, DI=0xcdda, BP=0x1234, DS=0x2000, SP=0xff02):
        raise ValueError("resident main cdecl frame/register differs")
    if bytes(uc.mem_read(0xa8000, 32000)) != b"\0" * 32000 or ports != [
            dict(port=0x7c, size=1, value=0x80), *[dict(port=0x7e, size=1, value=0)] * 4,
            dict(port=0x7c, size=1, value=0)]:
        raise ValueError("bounded graph memory/port vector differs")
    images = {hex(segment): bytes(uc.mem_read(segment * 16, 256)).hex() for segment in allocated}
    return dict(arguments=list(arguments), resident_initially=resident, allocations=list(allocations),
                existing_file=None if existing_file is None else existing_file.hex(), open_handle=open_handle,
                modeled_errors=dict(create=create_error, write=write_error, seek=seek_error,
                                    close=close_error, free=free_error), returned_ax=uc.reg_read(reg.UC_X86_REG_AX),
                mcb_prefix=mcb_prefix, resident_id=resident_id.hex(), resident_paragraphs=resident_paragraphs,
                preserved=preserved, debug=uc.mem_read(0x2131e, 1)[0], events=events, ports=ports,
                stdout_sha256=sha(bytes(stdout)), file_result=None if file_data is None else bytes(file_data).hex(),
                allocated_images=images, strategy_restored=strategy == 0,
                existing_resident_sha256=sha(bytes(uc.mem_read(resident_segment * 16, 256))),
                low_memory_70_180=bytes(uc.mem_read(0x70, 0x110)).hex())


def runtime_matrix(data):
    specifications = [dict(), dict(arguments=("/D",)), dict(arguments=("/R",)),
                      dict(arguments=("/R",), resident=True), dict(resident=True),
                      dict(arguments=("/X",)), dict(arguments=("/R", "ignored")),
                      dict(allocations=(None,)), dict(allocations=(0x3000, 0x800)),
                      dict(allocations=(0x3000, None)), dict(existing_file=b"abcdeTAILMORE"),
                      dict(existing_file=b"abcdeTAILMORE", open_handle=0),
                      dict(create_error=True), dict(write_error=True),
                      dict(existing_file=b"abcdeTAILMORE", seek_error=True),
                      dict(close_error=True), dict(arguments=("/R",), resident=True, free_error=True),
                      dict(arguments=("/R",), resident=True, mcb_prefix=True),
                      dict(resident=True, resident_id=b"YUMEConfiX"),
                      dict(resident=True, resident_paragraphs=15)]
    cases = [root_case(data, **specification) for specification in specifications]
    expected_returns = [0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if [c["returned_ax"] for c in cases] != expected_returns or not all(c["strategy_restored"] for c in cases):
        raise ValueError("resident main bounded return/strategy vector differs")
    expected_new = "0100010000000800"
    if cases[0]["file_result"] != expected_new or cases[1]["file_result"] != expected_new[:-2] + "01":
        raise ValueError("new config bytes differ")
    if cases[10]["file_result"] != b"abcde\0\x08\0LMORE".hex() or cases[11]["file_result"] != expected_new:
        raise ValueError("existing/zero-handle config behavior differs")
    if cases[12]["file_result"] is not None or cases[13]["file_result"] != "":
        raise ValueError("ignored create/write error vector differs")
    if cases[14]["file_result"] != b"\0\x08\0deTAILMORE".hex():
        raise ValueError("ignored seek error vector differs")
    for index in (0, 1, 6, 8):
        image = bytes.fromhex(cases[index]["allocated_images"]["0x800"])
        if image != b"YUMEConfig\xa5" + b"\0" * 245:
            raise ValueError("resident ID/untouched terminator/zero loop differs")
    failed = bytes.fromhex(cases[9]["low_memory_70_180"])
    if (cases[9]["file_result"] != "0100010000080000" or failed[1:3] != b"\xff\xff" or
            failed[0x10:0x1a] != b"YUMEConfig" or failed[0x1b:] != b"\0" * 245):
        raise ValueError("unchecked fallback allocation hazard differs")
    if ([e["segment"] for e in cases[17]["events"] if e["kind"] == "free-request"] != [0x1014] or
            any(cases[i]["file_result"] != expected_new for i in (18, 19))):
        raise ValueError("MCB chain/ID/paragraph comparison differs")
    return cases


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
    for path in ("config/targets.toml", "scripts/review_th03_zun_resident.py", "scripts/lib/zun.py",
                 "scripts/lib/targets.py", "scripts/lib/omf.py"):
        read(path)
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-zun")
    stored = read_verified_artifact(ROOT, artifact)
    decoded = read(config["decoded_path"])
    restoration = json.loads(read(config["diet_receipt"]))
    lineage = next(o for o in restoration["observations"] if o["artifact"] == "th03-zun")
    expected = next(a for a in diet["artifacts"] if a["id"] == "th03-zun")
    cold = json.loads(read(config["cold_receipt"]))
    if (config["reference_revision"] != REVISION or sha(decoded) != expected["decoded_sha256"] or
            sha(frozen[config["diet_receipt"]]) != config["diet_receipt_sha256"] or
            lineage["stored"]["sha256"] != sha(stored) or lineage["decoded"]["sha256"] != sha(decoded) or
            not restoration["restoration_checks_pass"] or
            sha(frozen[config["cold_receipt"]]) != config["cold_receipt_sha256"] or
            cold["reference_revision"] != REVISION or not cold["pass"] or not cold["all_products_equal"]):
        raise ValueError("resident restoration/cached build lineage differs")
    sources = {path: subprocess.check_output(["git", "show", f"{REVISION}:{path}"], cwd=ROOT / "_reference/ReC98")
               for path in SOURCES}
    payload = parse_launcher(decoded, 223)["payloads"][4]
    target = decoded[payload["decoded_file_offset"]:payload["decoded_file_offset"] + payload["size"]]
    target_rows, target_cases = decode(target), runtime_matrix(target)
    pin = next(p for p in config["payloads"] if p["option"] == "-5")
    rounds = []
    for path in pin["cold_paths"]:
        candidate = read(path)
        if sha(candidate) != pin["sha256"] or candidate != target:
            raise ValueError("complete cached resident payload raw differs")
        source_root = Path(path).parents[2]
        associations = []
        for source_path, original in sources.items():
            cached_path = str(source_root / source_path)
            cached = read(cached_path)
            if cached != original and cached != original.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"):
                raise ValueError(f"cached compiler source differs beyond CRLF transform: {source_path}")
            associations.append(dict(source=source_path, cached_path=cached_path, exact_bytes=cached == original,
                                     transformation="none" if cached == original else "CRLF only"))
        map_path = str(source_root / "obj/th03/res_yume.map")
        map_bytes = read(map_path)
        text = map_bytes.decode("ascii")
        if (not re.search(r"0000:0367 0142 C=CODE\s+S=_TEXT\s+G=DGROUP\s+M=th03/res_yume.cpp", text) or
                not re.search(r"0000:131E 0133 C=DATA\s+S=_DATA\s+G=DGROUP\s+M=th03/res_yume.cpp", text)):
            raise ValueError("resident root MAP contributions differ")
        object_path = str(source_root / "obj/th03/res_yume.obj")
        omf = describe_omf(read(object_path))
        rows, cases = decode(candidate), runtime_matrix(candidate)
        if rows != target_rows or cases != target_cases:
            raise ValueError("resident cached diagnostics differ")
        rounds.append(dict(path=path, complete_raw_equal=True, source_associations=associations,
                           map_path=map_path, object_path=object_path, omf=omf, procedures=rows, runtime_cases=cases))
    if rounds[0]["omf"]["dependency_timestamp_normalized_sha256"] != rounds[1]["omf"]["dependency_timestamp_normalized_sha256"]:
        raise ValueError("cached resident normalized OMF differs")
    for path, data in frozen.items():
        if (ROOT / path).read_bytes() != data:
            raise ValueError("resident diagnostic input changed")
    for path, original in sources.items():
        if subprocess.check_output(["git", "show", f"{REVISION}:{path}"], cwd=ROOT / "_reference/ReC98") != original:
            raise ValueError("frozen resident source changed")
    if read_verified_artifact(ROOT, artifact) != stored:
        raise ValueError("canonical ZUN changed")
    result = dict(kind="th03-zun-resident-root-candidate-review", observed_utc=datetime.now(timezone.utc).isoformat(),
                  reference_revision=REVISION, sources={p: sha(d) for p, d in sources.items()},
                  stored_sha256=sha(stored), decoded_sha256=sha(decoded), payload=payload,
                  target_procedures=target_rows, target_runtime_cases=target_cases, rounds=rounds,
                  runtime_scope="Bypass CRT startup/argv/exit; modeled MCB/allocation/files, flat graph RAM and recorded OUT only",
                  tools=dict(capstone_distribution=version("capstone"), unicorn_distribution=version("unicorn")),
                  inputs={p: sha(d) for p, d in frozen.items()}, diagnostic_checks_pass=True,
                  fresh_build=False, source_acceptance=False, exact_acceptance=False,
                  complete_runtime_library_review=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS whole cached -5 raw equality; root/direct-helper review and 60 CPU/model cases; no acceptance: {args.output}")


if __name__ == "__main__":
    main()
