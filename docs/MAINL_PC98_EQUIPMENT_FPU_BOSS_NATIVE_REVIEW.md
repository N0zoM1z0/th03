# Original PC-98 equipment detection and x87 probe — after415

The original Japanese Borland `CL.LIB` member `pc98eqip` (index 498) is
reconstructed as ordinary 16-bit ASM in `src/mainl/crt/pc98eqip.asm`.
The complete **213 original CODE bytes** implement the real far `_pc98equip`
equipment detection routine: physical zero-segment BIOS option flags at
0480h, 0481h, 0458h, 0501h, 054Ch and 054Dh; actual 8087 control/status
word initialization and tests; and the source-level floating-point
positive-infinity comparison used to distinguish coprocessor capabilities.
The four-byte IEEE positive-infinity constant `07F800000h` is **meaningful
inline x87 CODE-resident data** at CODE+132, not a patched target-byte
instruction array. Immediately afterward CODE+136 has `or al,dl` to merge
the coprocessor result back into the hardware capability mask; without this
instruction the original first 136 bytes assembled correctly but the
remaining CODE was two bytes short. The real source fixes the control flow,
not the binary output post hoc.

The entire original `_TEXT`/`_DATA`/`_BSS` = 213/0/0, original BSS-first
`08ff03ff02` GROUP, public `_pc98equip`, zero external imports and both
**literal ordered original Borland OMF FIXUPPs** at CODE+97 and +106
(CS-inline floating-constant destination CODE+132) are exactly reproduced
in TASM. Original full Borland-vs-TASM member record-program serialization
beyond the attestable fields is not asserted byte-equal.

The incremental after415 builder inherits the validated 590-source after414
receipt without a full cold replay, then runs two independent actual
TASM/TLIB/TLINK producer rounds retaining complete source-/driver-bound
OBJ/LIB/EXE/MAP vectors and writer logs. Both whole Japanese decoded
MAINL EXE/MAP are byte-for-byte original-equal (67,372-byte EXE and 677
ordered DOS MZ relocations). Working-source CRT: **591/893** members,
**166,683 original-equal CODE bytes**, with **302** unchanged contextual
vendor members. This does not grant a canonical packed-file source unit or
Factory accepted-source credit.

Focused reproduction:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after415_work.py pc98-equipment-fpu-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after415_work -v
```
