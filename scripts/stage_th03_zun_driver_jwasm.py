"""Syntax-only adapter for the existing maintained sprite16 translation unit.

Instruction/procedure includes, state, tables, reserved regions and link response
remain byte-identical to the TASM stage. No machine bytes are emitted here.
"""

import stage_th03_zun_driver as base


def adapt(files):
    result = dict(files)
    header = b".386\r\n.model use16 tiny"
    base.need(result["driver.asm"].count(header) == 1, "16-bit model header drift")
    # MASM selects the default segment word size when processing MODEL; select
    # tiny/16-bit before enabling 386 instructions. The explicit USE16 stays.
    result["driver.asm"] = result["driver.asm"].replace(header, b".model tiny\r\n.386")
    base.need(result["driver.asm"].count(b"include procs\\") == 55, "procedure include closure")
    result["driver.asm"] = result["driver.asm"].replace(b"include procs\\", b"include procs/")
    base.need(result["hardware.inc"].count(b":rest") == 1, "variadic macro parameter drift")
    result["hardware.inc"] = result["hardware.inc"].replace(b":rest", b":vararg")
    base.need({n for n in result if result[n] != files[n]} == {"driver.asm", "hardware.inc"},
              "unexpected semantic source change")
    return result


def payload(root):
    inputs = {n: base.read(root / n) for n in (base.LAYOUT, base.DATA, base.HARDWARE, *base.MODULES)}
    return adapt(base.prepare(inputs)), inputs
