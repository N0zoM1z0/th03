"""Independent contracts for 16 actual library-origin driver scalar services.

Every called helper is owned and executes. There are no DOS, hardware, graphics
or parser-dispatch stubs. The enclosing driver's DATA is an explicit interface;
its reserved spans and the rest of its procedures gain no ownership here.
"""

import hashlib
import json
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR
from unicorn.x86_const import *
from lib.zun_driver_scalar_layout import RANGES


ENTRIES = {n.removeprefix("sprite16_"): (a, size) for n, a, size in RANGES}
FIELDS = dict(zip(("set_mono_enabled", "set_mono_color", "set_overlap", "set_access_plane", "set_rop", "set_mask"),
                  (0x1064, 0x1066, 0x1068, 0x106E, 0x106A, 0x106C)))
REG = {n: globals()["UC_X86_REG_" + n.upper()] for n in
       ("ax", "bx", "cx", "dx", "si", "di", "bp", "sp", "cs", "ds", "es", "ss", "ip")}


def need(value, message):
    if not value: raise ValueError("ZUN driver scalar contract: " + message)


def upper(value): return value - 32 if 97 <= value <= 122 else value
def parity(value): return 4 if (value & 255).bit_count() % 2 == 0 else 0


def cmp8(a, b):
    result = (a - b) & 255
    return (int(a < b) | parity(result) | (16 if (a ^ b ^ result) & 16 else 0)
            | (64 if result == 0 else 0) | (result & 128) | (0x800 if (a ^ b) & (a ^ result) & 128 else 0))


def decimal(text):
    sign = -1 if text.startswith(b"-") else 1
    digits = text[1:] if text[:1] in (b"-", b"+") else text
    value = 0
    for byte in digits:
        if not 48 <= byte <= 57: return value, 1
        value = (value * 10 + byte - 48) & 65535
    return (value * sign) & 65535, 0


def hexadecimal(text):
    value = 0
    for byte in text:
        digit = ((byte - 32 if byte >= 91 else byte) - 48) & 255
        if digit >= 10:
            digit = (digit - 7) & 255
            if digit >= 16: return value, 1
        value = (value * 16 + digit) & 65535
    return value, 0


def binary(text):
    value = 0
    for byte in text:
        if byte not in (48, 49): return value, 1
        value = (value * 2 + byte - 48) & 65535
    return value, 0


def switch(text):
    folded = bytes(upper(b) for b in text)
    return (1, 0) if folded == b"ON" else (0, 0) if folded == b"OFF" else (0, 1)


def number(raw, before):
    """Return value/CF and any temporary suffix index, including index -1."""
    text = raw.split(b"\0", 1)[0]
    if raw[0] == 39:
        if raw[2:4] == b"'\0": return raw[1], 0, None
        if raw[3:5] == b"'\0": return raw[1] * 256 + raw[2], 0, None
        return 0, 1, None
    if raw[0] == 36: return *hexadecimal(text[1:]), None
    last = upper(text[-1] if text else before)
    if last in (ord("H"), ord("B")):
        value, carry = (hexadecimal if last == ord("H") else binary)(text[:-1] if text else b"")
        return value, carry, len(text) - 1
    value, carry = decimal(text)
    if carry: value, carry = switch(text)
    return value, carry, None


def specification(kind, registers, raw, second, before, base, data_base, pointer):
    text = raw.split(b"\0", 1)[0]
    result, flags_mask, flags_value, writes = dict(registers), 0, 0, []
    if kind in FIELDS:
        writes = [(base + FIELDS[kind], 2, registers["dx"])]
        flags_mask, flags_value = 0xED7, registers["flags"] & 0xED7
    elif kind in ("is_decimal_digit", "is_ascii_lower", "ascii_upper"):
        value = registers["dx"] & 255 if kind == "is_decimal_digit" else registers["ax"] & 255
        first, end = (48, 58) if kind == "is_decimal_digit" else (97, 123)
        flags_value = cmp8(value, first if value < first else end)
        if value < first: flags_value &= ~1
        flags_mask = 0x8D5
        if kind == "ascii_upper" and 97 <= value <= 122:
            folded = upper(value)
            result["ax"] = (registers["ax"] & 0xFF00) | folded
            flags_mask = 0x8C5  # AND leaves AF undefined.
            flags_value = parity(folded) | (64 if folded == 0 else 0) | (folded & 128)
    elif kind == "string_equal_folded":
        other = second.split(b"\0", 1)[0]
        for index in range(max(len(text), len(other)) + 1):
            a = upper(text[index]) if index < len(text) else 0
            b = upper(other[index]) if index < len(other) else 0
            if a != b or not a: break
        flags_mask, flags_value = 0x8D5, cmp8(a, b)
    elif kind == "string_length":
        result["ax"] = len(text)
        flags_mask, flags_value = 0x8C5, 0x44
    else:
        suffix = None
        if kind == "parse_number": value, carry, suffix = number(raw, before)
        else:
            value, carry = {"parse_decimal": decimal, "parse_hex": hexadecimal,
                            "parse_binary": binary, "parse_switch": switch}[kind](text)
        result["ax"] = value
        flags_mask, flags_value = 1, carry
        if suffix is not None:
            original = before if suffix == -1 else text[suffix]
            at = data_base + pointer + suffix
            writes = [(at, 1, 0), (at, 1, original)]
    return dict(registers=result, flags_mask=flags_mask, flags_value=flags_value, writes=writes)


class Machine:
    def __init__(self, image, load):
        need(len(image) == 4224 and image[0x1070:0x1077] == b"ON\0OFF\0", "bounded external ON/OFF storage")
        self.load, self.base = load, load * 16
        self.uc = Uc(UC_ARCH_X86, UC_MODE_16); self.uc.mem_map(0, 1 << 20)
        self.initial = bytearray(b"\xA5" * (1 << 20))
        self.initial[self.base + 256:self.base + 256 + len(image)] = image
        self.instructions = {}
        for start, size in ENTRIES.values():
            rows = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(image[start - 256:start - 256 + size], start))
            need(sum(i.size for i in rows) == size and rows[-1].mnemonic == "ret", "complete near procedure boundaries")
            self.instructions.update({i.address: i.size for i in rows})
        self.covered, self.maximum_stack = set(), 0
        self.hooks = [self.uc.hook_add(UC_HOOK_CODE, self.code), self.uc.hook_add(UC_HOOK_MEM_WRITE, self.write),
                      self.uc.hook_add(UC_HOOK_INTR, lambda uc, number, _: self.fail("unexpected interrupt " + str(number)))]

    def close(self):
        for hook in self.hooks: self.uc.hook_del(hook)
        self.hooks = []; self.uc = None

    def r(self, name): return self.uc.reg_read(REG[name])
    def fail(self, error): self.error = str(error); self.uc.emu_stop()

    def code(self, uc, address, size, _):
        try:
            if address == self.base + 0xFFFF:
                self.stopped = True; uc.emu_stop(); return
            ip = address - self.base
            need(self.instructions.get(ip) == size, "execution outside owned instructions")
            self.covered.update(range(ip, ip + size))
        except Exception as error: self.fail(error)

    def write(self, uc, access, address, size, value, _):
        try:
            if self.stack_base + self.stack - 64 <= address and address + size <= self.stack_base + self.stack:
                self.maximum_stack = max(self.maximum_stack, self.stack_base + self.stack - address)
                return
            need(self.write_index < len(self.expected["writes"])
                 and (address, size, value) == self.expected["writes"][self.write_index], "independent ordered field/suffix writes")
            self.write_index += 1
        except Exception as error: self.fail(error)

    def run(self, kind, *, text=b"123", other=b"123", value=0xBEEF, before=0xA5,
            flags=0x202, stack=0xF800, pattern=0, in_cs=False, split_stack=False, alias=False):
        need(kind in ENTRIES and len(text) <= 1024 and len(other) <= 1024, "bounded scalar inputs")
        forward = kind in ("parse_hex", "parse_binary", "string_length") or (kind == "parse_number" and not text.startswith(b"'"))
        need(not forward or not flags & 0x400, "forward LODSB precondition")
        self.stack = stack
        ds = self.load if in_cs else 0x5000
        es = ds if alias else 0x6000
        ss = 0x7000 if split_stack else self.load
        self.stack_base, data_base = ss * 16, ds * 16
        pointer, other_pointer = 0x2001, 0x2001 if alias else 0x2401
        self.uc.mem_write(0, bytes(self.initial))
        self.uc.mem_write(data_base + pointer - 1, bytes((before,)) + text + b"\0" + b"\xA5" * 8)
        if kind == "string_equal_folded": self.uc.mem_write(es * 16 + other_pointer, other + b"\0" + b"\xA5" * 8)
        raw = bytes(self.uc.mem_read(data_base + pointer, max(len(text), len(other)) + 9))
        second = bytes(self.uc.mem_read(es * 16 + other_pointer, len(other) + 9))
        self.uc.mem_write(self.stack_base + stack, b"\xFF\xFF\x53\xA9")
        initial = bytes(self.uc.mem_read(0, 1 << 20))
        registers = dict(ax=0xB53A ^ pattern, bx=0x37C1 ^ pattern, cx=0x1298 ^ pattern,
            dx=pointer, si=pointer, di=other_pointer, bp=0xA675 ^ pattern,
            cs=self.load, ds=ds, es=es, ss=ss, flags=flags)
        if kind in FIELDS: registers["dx"] = value
        elif kind == "is_decimal_digit": registers["dx"] = (registers["dx"] & 0xFF00) | value
        elif kind in ("is_ascii_lower", "ascii_upper"): registers["ax"] = (registers["ax"] & 0xFF00) | value
        self.expected = specification(kind, registers, raw, second, before, self.base, data_base, pointer)
        for name, val in registers.items():
            if name != "flags": self.uc.reg_write(REG[name], val)
        self.uc.reg_write(REG["sp"], stack); self.uc.reg_write(UC_X86_REG_EFLAGS, flags)
        self.write_index, self.error, self.stopped = 0, None, False
        try: self.uc.emu_start(self.base + ENTRIES[kind][0], self.base + 0x10000, count=50000)
        except UcError as error: raise ValueError("ZUN driver scalar contract: guest execution failed") from error
        need(self.error is None, self.error or "guest error")
        need(self.stopped and self.r("sp") == stack + 2, "near register ABI and unchanged caller cleanup")
        need(all(self.r(n) == v for n, v in self.expected["registers"].items() if n != "flags"), "independent return and register preservation")
        actual_flags = self.uc.reg_read(UC_X86_REG_EFLAGS)
        need(actual_flags & self.expected["flags_mask"] == self.expected["flags_value"], "independent return flags")
        need(actual_flags & 0x600 == flags & 0x600, "inherited IF/DF")
        need(self.write_index == len(self.expected["writes"]), "complete temporary suffix/field writes")
        expected = bytearray(initial)
        for at, size, val in self.expected["writes"]: expected[at:at + size] = val.to_bytes(size, "little")
        actual = bytes(self.uc.mem_read(0, 1 << 20))
        lo, hi = self.stack_base + stack - 64, self.stack_base + stack
        expected[lo:hi] = actual[lo:hi]
        need(actual == expected, "whole physical memory outside bounded stack")
        return dict(ax=self.r("ax"), flags_mask=self.expected["flags_mask"],
                    result_flags=actual_flags & self.expected["flags_mask"], ordered_writes=self.expected["writes"])


def cases():
    for kind in FIELDS:
        for value in (0, 1, 0x7FFF, 0x8000, 0xFFFF, 0x5555, 0xAAAA, 0x28FC):
            for flags in (2, 0x2D7, 0x402, 0xED7): yield kind, dict(value=value, flags=flags)
    for kind in ("is_decimal_digit", "is_ascii_lower", "ascii_upper"):
        for value in range(256):
            for flags in (2, 0xED7): yield kind, dict(value=value, flags=flags)
    for value in range(256):
        raw = bytes((value,))
        for kind in ("parse_number", "parse_decimal", "parse_hex", "parse_binary", "parse_switch", "string_length"):
            yield kind, dict(text=raw)
        for other in (bytes((upper(value),)), bytes(((value + 1) & 255,)), b"PREFIX" + raw):
            yield "string_equal_folded", dict(text=raw, other=other, flags=0x646)
    texts = (b"", b"+", b"-", b"65535", b"65536", b"-32768", b"-65537", b"4294967296", b"-12x", b"+12 ",
             b"ON", b"oN", b"OFF", b"oFf", b"ONx", b"$", b"$ff", b"$123456", b"0H", b"ffh", b"101B", b"101b",
             b"2B", b"GH", b"'A'", b"'AB'", b"'abc'", b"'A'x", b"''", b"'\0'", b":;<>?@", b"[\\]^_`", b"9" * 128)
    for text in texts:
        for kind in ("parse_number", "parse_decimal", "parse_hex", "parse_binary", "parse_switch"):
            yield kind, dict(text=text)
    for before in (0, ord("H"), ord("h"), ord("B"), ord("b")):
        yield "parse_number", dict(text=b"", before=before)
    for length in (0, 1, 127, 128, 255, 256, 511, 1023): yield "string_length", dict(text=b"x" * length)
    for left, right in ((b"abc", b"ABC"), (b"abc", b"AB"), (b"ab", b"ABC"), (b"\xFF", b"\xFF")):
        yield "string_equal_folded", dict(text=left, other=right, alias=True, flags=0xED7)


def verify(target, candidate):
    observations = []
    for image in (target, candidate):
        loads = []
        for load in (0x1000, 0x3000):
            machine = Machine(image, load)
            try:
                trace = hashlib.sha256()
                for count, (kind, options) in enumerate(cases(), 1):
                    row = machine.run(kind, stack=0xF800 if count & 1 else 0xE800,
                        pattern=0 if count & 1 else 0xFFFF, in_cs=count % 3 == 0, split_stack=count % 2 == 0, **options)
                    # Physical addresses depend on the selected load/segments;
                    # target/candidate compare at the identical physical setup.
                    trace.update(json.dumps(row, sort_keys=True).encode())
                need(len(machine.covered) == 428, "all 428 owned instruction bytes execute")
                loads.append(dict(load_segment=load, cases=count, covered_owner_bytes=len(machine.covered),
                                  maximum_observed_stack_depth=machine.maximum_stack, trace_sha256=trace.hexdigest()))
            finally: machine.close()
        observations.append(loads)
    need(observations[0] == observations[1], "target/candidate independent observations")
    return dict(images=2, functions=16, code_bytes=428, private_data_bytes=0, private_bss_bytes=0,
                cases_per_image=sum(o["cases"] for o in observations[0]), executed_owner_bytes=428,
                observations=observations[0], exhaustive_byte_domains=256,
                scope="library scalar/register services only; enclosing driver, reserved spans and hardware unaccepted")


def negative_controls(target):
    controls = (
        ("setter-CS-override", 0x340, b"\x3E", "set_mono_enabled", {}),
        ("setter-word-width", 0x341, b"\x88", "set_mono_enabled", {}),
        ("decimal-digit-end", 0x690, b"\x39", "is_decimal_digit", dict(value=57)),
        ("lowercase-end", 0x699, b"\x7A", "is_ascii_lower", dict(value=122)),
        ("fold-mask", 0x6A3, b"\xFF", "ascii_upper", dict(value=97)),
        ("quote-byte-order", 0xAB1, b"\x90\x90", "parse_number", dict(text=b"'AB'")),
        ("hex-prefix", 0xABE, b"\x74", "parse_number", dict(text=b"$ff")),
        ("suffix-restore", 0xAE2, b"\x48", "parse_number", dict(text=b"ffh")),
        ("decimal-base", 0xB32, b"\x0B", "parse_decimal", dict(text=b"123")),
        ("decimal-negative", 0xB44, b"\xD0", "parse_decimal", dict(text=b"-123")),
        ("permissive-hex-fold", 0xB59, b"\x21", "parse_hex", dict(text=b"[")),
        ("binary-digit", 0xB8E, b"\x32", "parse_binary", dict(text=b"1")),
        ("switch-on-word", 0xBAA, b"\x73", "parse_switch", dict(text=b"ON")),
        ("folded-comparison", 0xC69, b"\x74", "string_equal_folded", dict(text=b"a", other=b"b")),
    )
    rejected = []
    for name, at, replacement, kind, options in controls:
        raw = bytearray(target); raw[at - 256:at - 256 + len(replacement)] = replacement
        machine = Machine(bytes(raw), 0x3000)
        try:
            try: machine.run(kind, **options)
            except ValueError: rejected.append(name)
            else: raise ValueError("ZUN driver scalar mutation escaped: " + name)
        finally: machine.close()
    return dict(count=len(rejected), rejected=rejected)
