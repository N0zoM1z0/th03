"""Bounded directory validation for the reviewed five-payload COM launcher."""

import hashlib
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_16

PSP_SIZE = 0x100
MAX_PROCS = 32
DIRECTORY_SIZE = 2 + MAX_PROCS * 8 + (MAX_PROCS + 1) * 2 + 3


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compose_launcher(stub: bytes, call: bytes, helper: bytes, names: list[str], payloads: list[bytes]) -> bytes:
    if not 1 <= len(names) <= MAX_PROCS or len(names) != len(payloads):
        raise ValueError("invalid composition count")
    if len(call) != 3 or len(helper) != 8:
        raise ValueError("compiled transfer extents differ")
    directory_names = b"".join(name.encode("ascii").ljust(8, b" ") for name in names)
    if len(directory_names) != len(names) * 8:
        raise ValueError("overlong composition name")
    directory_names += b" " * ((MAX_PROCS - len(names)) * 8)
    entry = len(stub) + DIRECTORY_SIZE + PSP_SIZE
    entries = [entry]
    for payload in payloads:
        entry += len(payload)
        entries.append(entry)
    if entry + len(helper) > 0x10000:
        raise ValueError("composition exceeds COM address space")
    entries += [0] * (MAX_PROCS + 1 - len(entries))
    directory = struct.pack("<H", len(names)) + directory_names + struct.pack("<33H", *entries)
    data = stub + directory + call + b"".join(payloads) + helper
    parse_launcher(data, len(stub))
    return data


def parse_launcher(data: bytes, stub_size: int) -> dict:
    if stub_size <= 0 or len(data) > 0xff00 or len(data) < stub_size + DIRECTORY_SIZE + 8:
        raise ValueError("invalid launcher size")
    count = struct.unpack_from("<H", data, stub_size)[0]
    if not 1 <= count <= MAX_PROCS:
        raise ValueError("unsupported launcher procedure count")
    names_start = stub_size + 2
    names = bytes(data[names_start:names_start + MAX_PROCS * 8])
    used_names = [names[i * 8:(i + 1) * 8] for i in range(count)]
    if any(not name.strip() or any(c < 32 or c >= 127 for c in name) for name in used_names):
        raise ValueError("invalid procedure name")
    if len(set(used_names)) != count:
        raise ValueError("duplicate procedure name")
    if names[count * 8:] != b" " * ((MAX_PROCS - count) * 8):
        raise ValueError("nonspace unused name slots")
    table_start = names_start + MAX_PROCS * 8
    entries = struct.unpack_from("<33H", data, table_start)
    payload_start = stub_size + DIRECTORY_SIZE
    helper_start = len(data) - 8
    used_entries = entries[:count + 1]
    if (used_entries[0] != payload_start + PSP_SIZE or
            used_entries[-1] != helper_start + PSP_SIZE or
            any(a >= b for a, b in zip(used_entries, used_entries[1:])) or
            any(entries[count + 1:])):
        raise ValueError("invalid procedure partition or unused entry slots")
    call_start = table_start + 66
    if data[call_start] != 0xe8:
        raise ValueError("moveup_indirect is not a near CALL")
    displacement = struct.unpack_from("<h", data, call_start + 1)[0]
    if (call_start + 3 + displacement) & 0xffff != helper_start:
        raise ValueError("near CALL does not reach the trailing helper")
    helper = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(data[helper_start:], PSP_SIZE + helper_start))
    if (sum(i.size for i in helper) != 8 or
            [(i.mnemonic, i.op_str) for i in helper] != [
                ("rep movsb", "byte ptr es:[di], byte ptr [si]"), ("pop", "ax"),
                ("mov", "ax, 0x100"), ("push", "ax"), ("ret", "")]):
        raise ValueError("unexpected moveup helper")
    payloads = []
    for index, name in enumerate(used_names):
        start, end = (used_entries[index] - PSP_SIZE, used_entries[index + 1] - PSP_SIZE)
        payloads.append(dict(name=name.decode().rstrip(), decoded_file_offset=start,
                             runtime_start=used_entries[index], size=end - start,
                             sha256=digest(data[start:end])))
    return dict(count=count, stub_size=stub_size, directory_size=DIRECTORY_SIZE,
                stub_sha256=digest(data[:stub_size]),
                directory_sha256=digest(data[stub_size:payload_start]),
                helper_offset=helper_start, helper_sha256=digest(data[helper_start:]),
                payloads=payloads)


def dispatch_observation(data: bytes, directory: dict, command: str, fcb_name: str) -> dict:
    """Execute only the COM wrapper; stop before any embedded payload executes."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INTR
    from unicorn.x86_const import (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES,
                                  UC_X86_REG_SS, UC_X86_REG_SP, UC_X86_REG_AX,
                                  UC_X86_REG_DX, UC_X86_REG_EFLAGS)
    segment = 0x2000
    base = segment * 16
    machine = Uc(UC_ARCH_X86, UC_MODE_16)
    machine.mem_map(0, 0x100000)
    machine.mem_write(base + PSP_SIZE, data)
    raw_command = command.encode("ascii")
    if len(raw_command) > 126 or len(fcb_name) > 8:
        raise ValueError("invalid bounded dispatch input")
    machine.mem_write(base + 0x80, bytes([len(raw_command)]) + raw_command + b"\r")
    machine.mem_write(base + 0x5d, fcb_name.encode("ascii").ljust(8, b" "))
    second_fcb = b"0123456789ABCDEF"
    machine.mem_write(base + 0x6c, second_fcb)
    for register in (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS):
        machine.reg_write(register, segment)
    machine.reg_write(UC_X86_REG_SP, 0xfffe)
    machine.reg_write(UC_X86_REG_EFLAGS, 0x402)  # DF starts set; the real CLD must clear it.
    output = bytearray()
    state = dict(steps=0, outcome=None)

    def code(uc, address, size, user):
        state["steps"] += 1
        if state.get("transferring") and address != base + PSP_SIZE:
            raise ValueError("wrapper transfer missed the payload entry")
        if address == base + PSP_SIZE and state["steps"] > 1:
            state["outcome"] = "payload-entry"
            uc.emu_stop()
        if address == base + PSP_SIZE + directory["helper_offset"] + 7:
            state["transferring"] = True

    def interrupt(uc, number, user):
        ax = uc.reg_read(UC_X86_REG_AX)
        ah = ax >> 8
        if number != 0x21:
            raise ValueError("unexpected wrapper interrupt")
        if ah == 2:
            output.append(uc.reg_read(UC_X86_REG_DX) & 0xff)
        elif ah == 9:
            address = base + uc.reg_read(UC_X86_REG_DX)
            for index in range(256):
                byte = uc.mem_read(address + index, 1)[0]
                if byte == ord("$"):
                    break
                output.append(byte)
            else:
                raise ValueError("unterminated DOS output string")
        elif ah == 0x4c:
            state["outcome"] = "dos-exit"
            uc.emu_stop()
        else:
            raise ValueError("unexpected wrapper DOS service")

    # This installed Unicorn uses ctypes callbacks: exceptions must not escape
    # the FFI boundary, where they could be printed and ignored while execution
    # continues into an unreviewed payload.
    def guarded(callback):
        def invoke(uc, *arguments):
            try:
                callback(uc, *arguments)
            except Exception as error:
                state["hook_error"] = str(error)
                uc.emu_stop()
        return invoke

    machine.hook_add(UC_HOOK_CODE, guarded(code))
    machine.hook_add(UC_HOOK_INTR, guarded(interrupt))
    machine.emu_start(base + PSP_SIZE, base + 0x10000, count=100000)
    if "hook_error" in state:
        raise ValueError(state["hook_error"])
    if state["outcome"] is None:
        raise ValueError("wrapper did not reach a bounded stop")
    sp = machine.reg_read(UC_X86_REG_SP)
    tail_size = machine.mem_read(base + 0x80, 1)[0]
    result = dict(command=command, fcb_name=fcb_name, **state,
                  stdout=output.decode("ascii"), sp=sp,
                  ax=machine.reg_read(UC_X86_REG_AX),
                  flags=machine.reg_read(UC_X86_REG_EFLAGS),
                  tail=bytes(machine.mem_read(base + 0x81, tail_size)).decode("ascii"),
                  tail_terminator=machine.mem_read(base + 0x81 + tail_size, 1)[0],
                  first_fcb_hex=bytes(machine.mem_read(base + 0x5c, 16)).hex())
    if result["outcome"] == "payload-entry":
        payload = next(p for p in directory["payloads"] if p["name"] == fcb_name)
        copied = bytes(machine.mem_read(base + PSP_SIZE, payload["size"]))
        if digest(copied) != payload["sha256"]:
            raise ValueError("dispatched payload copy differs from its complete input")
        if result["first_fcb_hex"] != second_fcb.hex() or result["tail_terminator"] != 13:
            raise ValueError("wrapper FCB/command-tail fixup differs")
        result.update(payload=payload["name"], copied_size=payload["size"],
                      copied_sha256=digest(copied),
                      remaining_count=struct.unpack("<H", machine.mem_read(base + sp, 2))[0])
    return result
