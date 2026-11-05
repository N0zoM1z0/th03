# Original NEC PC-98 BIOS serial-controller boss — after409

Original Japanese Borland `CL.LIB` member **bion_com** (index 467) is
reconstructed in natural 8086 ASM at `src/mainl/crt/bion_com.asm`. The
complete **227 CODE bytes** implement the original near/far register and
buffer operations of the far `__necpc_bios_serialcom` entry. The real
PC-98 BIOS serial service dispatch calls `int 19h`, `int 0D4h` or
`int 0D5h` depending on its controller choice. Other branches configure
the NEC A000h firmware status and D080h/D000h serial-controller vector
(at interrupt-vector offsets 0350h/0354h),
read defaults and set the original baud/parity/handshake registers, and
write the result back into the supplied caller's far structure. The
original compiler's two harmless boundary `nop` instructions remain
natural ASM instructions, not executable target-byte array padding.

The complete original `_TEXT`/`_DATA`/`_BSS` layout (227/0/0), the exact
large-model export, zero imported symbols, zero original logical and
literal FIXUPPs, and BSS-first GROUP record `08ff03ff02` all agree with
native TASM. The live MAINL baseline and installed Japanese CL.LIB member
were independently verified to be the same program for this unit. Whole
raw original Borland member-record serialization still differs from TASM,
which is not claimed exact by this source-bound milestone.

The after409 native builder reuses and validates the unchanged 577-member
after408 source-bound receipt, then performs two independent actual
TASM/TLIB/TLINK rounds with all original native OBJ/LIB/EXE/MAP vectors
and logs retained. Both linked full decoded Japanese MAINL EXE and MAP
are byte-for-byte original-equal (67,372-byte EXE and 677 ordered MZ
relocations). Working-source CRT: **578/893** original-member slots,
**165,377 original-equal CODE bytes**, and **315** contextual vendor
members. No full cold replay, packed-original source credit or Factory
accepted-source decision is implied.

Focused reproducibility:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after409_work.py nec-bios-serial-controller-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after409_work -v
```
