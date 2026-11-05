# Original DOS absolute disk read/write boss — after404

The Japanese Borland `CL.LIB` member `absread` (original index 339) is now
source-reconstructed as natural 8086 in `src/mainl/crt/absread.asm`. The
complete **292 CODE bytes** implement a private far-return disk-format
probe at CODE+0 and two public original CRT far APIs: `_absread` at
CODE+86, `_abswrite` at CODE+189. Each selects the extended 10-byte DOS
disk transfer descriptor or original short-register form based on the
cached geometry, invokes the *real* DOS `INT 25h` or `INT 26h`, consumes
the original pushed flags from the DOS call, and propagates the original
`_errno`/return convention. The probe actually calls `_getfat` and the
original near `N_LXMUL@` 32-bit multiplication helper.

The original has separate **2 initialized DATA bytes** (a cached drive
word `0xFFFF`) and **2 uninitialized BSS bytes** (cached mode). Its group
is BSS-first `08ff03ff02`; these two different storage kinds are not
merged or hardcoded into CODE. The initial assembler trial over-generated
a redundant `push cs` before the internal helper call because the helper
is `proc far`. The correct explicit `push cs` plus `call near ptr` restores
the original instruction encoding without patched bytes. Native output
now matches all original CODE/DATA, group, public offsets and ordered imports,
and **all eight original logical OMF FIXUPP fields** (including real
DATA/BSS group frames, _getfat far import, CODE-framed near multiply call,
and two `_errno` targets). Original Borland and TASM order those literal
FIXUPP records differently, so original member-program serialization is
not falsely claimed byte-equal.

The incremental after404 builder validates the complete unchanged after403
parent evidence including its explicitly hashed `stdio_layout.inc` dependency,
then runs two fresh native TASM/TLIB/TLINK producer rounds with complete
source/driver-bound OBJ/LIB/EXE/MAP and writer logs retained. Both whole
decoded Japanese MAINL EXE/MAP are byte-for-byte original-equal
(67,372-byte EXE, 677 ordered DOS MZ relocations). Working-source CRT:
**561/893 members**, **163,850 original-equal CODE bytes**, **332** untouched
original contextual vendor programs. No full cold replay or Factory
packed-original source acceptance was claimed.

Focused checks:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after404_work.py absolute-dos-disk-io-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after404_work -v
```
