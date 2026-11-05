# Complete original NEC PC-98 BIOS disk controller boss — after412

Original Japanese Borland `CL.LIB` member **bion_dsk** (index 468) is now
reconstructed as naturally assembled 8086 in `src/mainl/crt/bion_dsk.asm`.
The original single far `__necpc_bios_disk` public entry has **171 full
CODE bytes** implementing actual `INT 1Bh` BIOS disk I/O and its original
far request-structure interface. The source preserves disk format and
operation dispatch (including 50h/70h/80h drive modes and 8Dh/0Dh
special handling), the original far buffer passed via ES:BP, the
native carry/error convention, and the post-call firmware parameter
block copy from physical 0:05D0h or the computed 0:0564h+offset.

The original **eight initialized DATA bytes** encode the genuine command
filter `06 05 10 01 0A 09 0C 02`. They remain readable named DATA,
not an executable byte array. The complete `_TEXT`/`_DATA`/`_BSS`
171/8/0 sizes, BSS-first `08ff03ff02` GROUP, public, zero imports,
and sole **literal ordered original OMF FIXUPP** at CODE+99 to DATA+0
(including frame, addend, target and width) are exactly source-matched.
The active source carrier and installed vendor CL.LIB program are
independently checked identical for this member; raw Borland member
serialization is not asserted byte equal to TASM's distinct record format.

The after412 native builder validates the unchanged 587-source after411
receipt and executes two actual fresh TASM/TLIB/TLINK rounds retaining
complete raw OBJ/LIB/EXE/MAP output and phase logs. Both Japanese decoded
MAINL.EXE and MAP are entirely byte-for-byte equal to the originals
(67,372-byte EXE, 677 ordered MZ relocations). The working CRT increases
to **588/893 source members**, **166,084 original-equal CODE bytes** and
**305** untouched contextual original vendor members. No full cold replay
or Factory packed-file accepted-source credit is claimed.

Focused verification:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after412_work.py nec-bios-disk-controller-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after412_work -v
```
