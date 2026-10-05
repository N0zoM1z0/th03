"""Bounded directory validation for the reviewed five-payload COM launcher."""

import hashlib
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_16

PSP_SIZE = 0x100
MAX_PROCS = 32
DIRECTORY_SIZE = 2 + MAX_PROCS * 8 + (MAX_PROCS + 1) * 2 + 3


def digest(data):
    return hashlib.sha256(data).hexdigest()


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
