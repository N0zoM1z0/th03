"""Fresh-image consumers preserve raw defaults, strings and pointer tables.

Callbacks stop at the selected entry: their procedure behavior is accepted in
separate reviews. DOS character output/resize/termination are bounded services.
Option-selection cases supply mutable argument-count/vector inputs after load;
they do not execute the tokenizer. These cases add no graphics hardware,
physical stack lifetime or DOS claim.
"""
import hashlib
import itertools
import json
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INTR
from unicorn.x86_const import *
from lib.zun_driver_data_layout import OPTION_TARGETS, SERVICE_TARGETS, need

MESSAGES = (
    (0xC80, 'メモリ縮小に失敗しました。\r\n'),
    (0xC9D, 'すでに常駐しています。\r\n'),
    (0xCB6, '環境領域解放失敗\r\n'),
    (0xCC9, 'マスクデータ領域解放失敗\r\n'),
    (0xCE4, 'ベタデータ領域解放失敗\r\n'),
    (0xCFD, 'コード領域解放失敗\r\n'),
    (0xD12, '解放しました。\r\n'),
    (0xD23, '常駐していません。\r\n'),
    (0xF47, 'メモリが足りません。\r\n'),
    (0xF5E, '常駐しました。(int %02Xh)\r\n'),
    (0xF7A, 'ZUNSP.COM    Version 1.00 Copyright(C) 1997 ZUN           \r\n\r\n'),
    (0xFB9, 'Usage: ZUNSP    -z (常駐)\r\n                -r (解放)\r\n'),
    (0x10F4, '対になる " が見つかりません。\r\n'),
    (0x1114, '引数が足りません。\r\n\r\n'),
    (0x112B, '数値では無い値が指定されています。\r\n\r\n'),
    (0x1152, 'オプションが無効です。\r\n\r\n'),
)
OPTIONS = (b'/Z', b'/R', b'/V', b'MASKTEST', b'PRESSY', b'COPYUL', b'CLSU', b'SPRITE')
DEFAULTS = (0,) * 11 + (15, 1, 0x28FC, 0xFFFF, 0xFFF0)
REGS = dict(ax=UC_X86_REG_AX, bx=UC_X86_REG_BX, cx=UC_X86_REG_CX, dx=UC_X86_REG_DX,
            si=UC_X86_REG_SI, di=UC_X86_REG_DI, bp=UC_X86_REG_BP, sp=UC_X86_REG_SP,
            cs=UC_X86_REG_CS, ds=UC_X86_REG_DS, es=UC_X86_REG_ES, ss=UC_X86_REG_SS)
FULL_REGS = (UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX,
             UC_X86_REG_ESI,UC_X86_REG_EDI,UC_X86_REG_EBP,UC_X86_REG_ESP)


def word(value):
    return (value & 65535).to_bytes(2, 'little')


def specification(image):
    """Semantic initial values, independently of the declaration mapper."""
    expected = {}
    def add(at, raw):
        need(not set(range(at, at+len(raw))) & expected.keys(), 'nonoverlapping semantic fields')
        expected.update({at+i:v for i,v in enumerate(raw)})
    add(0x102, b'SPRITE16\0\x04')
    add(0x8DC, b'0123456789ABCDEF')
    for at, text in MESSAGES:
        add(at, text.encode('shift_jis') + b'\0')
    add(0xD38, bytes(512))
    add(0xF38, bytes(10) + b'\x42' + bytes(4))
    for at, name in zip(OPTION_TARGETS[::2], OPTIONS):
        add(at, name + b'\0')
    add(0x101C, b''.join(map(word, OPTION_TARGETS)) + bytes(2))
    add(0x103E, b''.join(map(word, SERVICE_TARGETS)))
    add(0x1050, b''.join(map(word, DEFAULTS)))
    add(0x1070, bytes(2 + 128 + 2))
    add(0x1170, b'ON\0OFF\0')
    owned = set(range(0x102, 0x10C)) | set(range(0x8DC, 0x8EC))
    owned |= set(range(0xC80, 0x116D)) | set(range(0x1170, 0x1177))
    need(expected.keys() == owned and len(expected) == 1294, 'complete independently interpreted DATA scope')
    need(all(image[a-256] == v for a,v in expected.items()), 'semantic initial DATA values')
    return expected


class Machine:
    def __init__(self, image, load):
        self.image, self.load, self.base = image, load, load*16
        self.uc = Uc(UC_ARCH_X86, UC_MODE_16)
        self.uc.mem_map(0, 1 << 20)
        self.hooks = [self.uc.hook_add(UC_HOOK_CODE, self.code),
                      self.uc.hook_add(UC_HOOK_INTR, self.interrupt)]
        self.traces = []
        self.cases = 0

    def close(self):
        for hook in self.hooks:
            self.uc.hook_del(hook)
        self.hooks.clear()

    def r(self, name):
        return self.uc.reg_read(REGS[name])

    def write(self, offset, raw):
        self.uc.mem_write(self.base+offset, raw)

    def read(self, offset, size):
        return bytes(self.uc.mem_read(self.base+offset, size))

    def code(self, uc, address, size, _):
        ip = address-self.base
        if ip == self.stop:
            self.stopped = True
            uc.emu_stop()
        else:
            self.minimum_sp = min(self.minimum_sp, self.r('sp'))
            need(0x100 <= ip < 0xC80, 'actual bounded CODE consumer')

    def interrupt(self, uc, number, _):
        need(number == 0x21, 'bounded DOS interface only')
        ah = self.r('ax') >> 8
        if ah == 2:
            self.output.append(self.r('dx') & 255)
        elif ah == 0x4A:
            need(self.r('bx') == 0x119 and self.r('es') == self.load and self.r('sp') == 0xF38,
                 'startup resize paragraphs, PSP and actual 512-byte stack top')
            self.resized = True
            flags = self.uc.reg_read(UC_X86_REG_EFLAGS)
            self.uc.reg_write(UC_X86_REG_EFLAGS, (flags & ~1) | int(self.resize_failure))
        elif ah == 0x4C:
            self.terminal = self.r('ax')
            uc.emu_stop()
        else:
            raise ValueError('unmodelled DOS service ' + hex(ah))

    def reset(self, *, stop=0xFFFE, resize_failure=False, **regs):
        self.uc.mem_write(0, bytes(1 << 20))
        self.write(0x100, self.image)
        # Only PSP/caller storage is supplied; all 1,294 DATA bytes stay raw.
        self.write(0x80, b'\0\r')
        for reg in FULL_REGS:
            self.uc.reg_write(reg,0)
        for n, v in dict(cs=self.load, ds=self.load, es=self.load, ss=self.load,
                         ax=0x7123, bx=0x2345, cx=0x3456, dx=0x4567,
                         si=0x5678, di=0x6789, bp=0xFA40, sp=0xFA00).items():
            self.uc.reg_write(REGS[n], v)
        for n,v in regs.items():
            self.uc.reg_write(REGS[n], v)
        self.uc.reg_write(UC_X86_REG_EFLAGS, 0x202)
        self.write(self.r('sp'), word(0xFFFE))
        self.stop, self.resize_failure = stop, resize_failure
        self.output, self.terminal, self.resized, self.stopped = bytearray(), None, False, False
        self.minimum_sp = self.r('sp')

    def run(self, entry):
        try:
            self.uc.emu_start(self.base+entry, 0, count=100000)
        except UcError as error:
            raise ValueError('DATA consumer execution failed') from error
        need(self.stopped or self.terminal is not None, 'bounded consumer completed')
        self.cases += 1
        self.traces.append(dict(entry=entry, stop=self.stop, output=self.output.hex(), terminal=self.terminal,
            registers={n:self.r(n) for n in REGS}, flags=self.uc.reg_read(UC_X86_REG_EFLAGS),
            minimum_sp=self.minimum_sp, memory=hashlib.sha256(bytes(self.uc.mem_read(0,1<<20))).hexdigest()))

    def contracts(self, *, check_initial=True):
        if check_initial:
            specification(self.image)
        self.reset(stop=0x10C)
        for reg in FULL_REGS:
            self.uc.reg_write(reg,0xA5790000 | self.uc.reg_read(reg))
        full_before = bytes(self.uc.mem_read(0,1<<20))
        full_regs = {reg:self.uc.reg_read(reg) for reg in FULL_REGS}
        before = {n:self.r(n) for n in REGS}
        self.run(0x100)
        need(before == {n:self.r(n) for n in REGS} and self.uc.reg_read(UC_X86_REG_EFLAGS) == 0x202,
             'entry JMP preserves all WORD registers and flags')
        need(full_before == bytes(self.uc.mem_read(0,1<<20)), 'entry JMP preserves all memory')
        for reg in FULL_REGS:
            need(self.uc.reg_read(reg) == full_regs[reg], 'entry JMP preserves DWORD high halves')
        for at, text in MESSAGES:
            self.reset()
            self.write(0xFA02, word(at))
            self.run(0x676)
            need(self.output == text.encode('shift_jis') and self.r('sp') == 0xFA04,
                 'raw SS NUL message output and RET 2')
        for fail in (False, True):
            self.reset(resize_failure=fail)
            self.uc.reg_write(UC_X86_REG_EFLAGS, 0x602)
            self.run(0x100)
            wanted = MESSAGES[10][1] + MESSAGES[0 if fail else 11][1]
            need(self.resized and self.terminal == 0x4C01 and self.output == wanted.encode('shift_jis'),
                 'fresh header to terminal startup output')
            need(self.minimum_sp >= 0xD38 and self.read(0x1050,32) == b''.join(map(word,DEFAULTS)),
                 'startup stays in 512-byte stack and preserves graphics defaults')
        for lower in (0,1):
            for value in (*range(16), 0xABCD, 0xFFFFFFFF):
                self.reset(bx=0x2000)
                self.uc.reg_write(UC_X86_REG_EDX, value)
                self.uc.reg_write(UC_X86_REG_ECX, 16)
                self.write(0xFA28,word(lower))
                self.run(0x89F)
                expected = format(value, 'x' if lower else 'X').encode()+b'\0'
                need(self.read(0x2000,len(expected)) == expected, 'raw digit alphabet output')
        for text, expected, carry in ((b'ON',1,0),(b'OFF',0,0),(b'',0,1),(b'ONLY',0,1)):
            variants = itertools.product(*[(bytes((c,)),bytes((c|32,))) for c in text]) if text else [()]
            for parts in variants:
                self.reset(si=0x2000)
                self.write(0x2000,b''.join(parts)+b'\0')
                self.run(0xBA2)
                need(self.r('ax') == expected and self.uc.reg_read(UC_X86_REG_EFLAGS)&1 == carry,
                     'raw folded ON/OFF strings')
        for i, name in enumerate(OPTIONS):
            for tail in (name, name.lower(), b'-'+name[1:] if name.startswith(b'/') else name.lower()):
                target = OPTION_TARGETS[i*2+1]
                self.reset(stop=target)
                # Mutable parser outputs are caller inputs for this table scope.
                self.write(0x1070,word(1)+word(0x2000))
                self.write(0x2000,tail+b'\0')
                self.run(0xA36)
                need(self.read(0x1070,2) == bytes(2) and self.read(0x10F2,2) == word(0x1074)
                     and self.r('sp') == 0xF9EC and self.r('es') == self.load,
                     'raw option-table selection and saved callback frame')
        self.reset()
        self.write(0x1070,word(1)+word(0x2000))
        self.write(0x2000,b'unknown\0')
        self.run(0xA36)
        need(self.terminal == 0x4C01 and self.output == MESSAGES[-1][1].encode('shift_jis'),
             'raw option-table sentinel and invalid-option message')
        for i,target in enumerate(SERVICE_TARGETS):
            self.reset(stop=target,ax=i<<8)
            self.write(0xFA00,word(0xFFFE)+word(self.load)+word(0x602))
            self.run(0x22A)
            need(self.read(0xF45,2) == word(target) and self.uc.reg_read(UC_X86_REG_EFLAGS)&0x200
                 and self.r('sp') == 0xF9FE, 'raw interrupt-table target, shared state and STI')
        for i,offset in enumerate((0x1064,0x1066,0x1068,0x106E,0x106A,0x106C)):
            for value in (0,1,0x8000,0xFFFF):
                self.reset(dx=value)
                initial = bytearray(self.read(0x1050,32))
                initial[offset-0x1050:offset-0x1050+2] = word(value)
                self.run(0x340+i*6)
                need(self.read(0x1050,32) == initial, 'packed setter changes only its default WORD')
        return dict(load_segment=self.load, cases=self.cases, initial_data_bytes=1294,
            header_executed_bytes=2, raw_data_preserved_on_load=True, callback_bodies_executed=False,
            trace_sha256=hashlib.sha256(json.dumps(self.traces,sort_keys=True).encode()).hexdigest())


def verify(target,candidate):
    observations = []
    for image in (target,candidate):
        rows = []
        for load in (0x1000,0x3000):
            machine = Machine(image,load)
            try:
                rows.append(machine.contracts())
            finally:
                machine.close()
        observations.append(rows)
    need(observations[0] == observations[1], 'independent fresh-image observations agree')
    return dict(images=2, data_bytes=1294, code_bytes=2, functions=0,
        cases_per_image=sum(r['cases'] for r in observations[0]), observations=observations[0],
        default_state_replaced=False, callbacks_are_selection_boundaries=True,
        physical_DOS_or_graphics_emulated=False)


def negative_controls(image):
    # Every interpreted DATA byte must fail the independent initial-state contract.
    rejected = 0
    for address,value in specification(image).items():
        changed = bytearray(image)
        changed[address-256] = value ^ 1
        try:
            specification(changed)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('DATA mutation escaped at ' + hex(address))
    runtime_rejected = []
    for address in (0x101,0xC80,0x8E6,0x101E,0x1044,0xF7A,0x1170):
        changed = bytearray(image)
        changed[address-256] ^= 1
        machine = Machine(bytes(changed),0x1000)
        try:
            machine.contracts(check_initial=False)
        except (ValueError,UcError):
            runtime_rejected.append(address)
        else:
            raise ValueError('actual consumer mutation escaped at ' + hex(address))
        finally:
            machine.close()
    return dict(data_byte_mutations_rejected=rejected, runtime_mutation_addresses=runtime_rejected,
                header_instruction_mutations=1, consumed_data_mutations=6,
                reserved_bytes_mutated=False, data_mutations_are_instruction_execution=False)
