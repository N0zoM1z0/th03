# Original NEC PC-98 BIOS equipment/memory/time Boss — after408

The previously contextual Japanese Borland `CL.LIB` member **bion_equ**
(index 469) is now reconstructed as readable, naturally assembled 16-bit
source in `src/mainl/crt/bion_equ.asm`. Its three original far public
entries are `__necpc_bios_equiplist` at CODE+0, `__necpc_bios_memsize` at
+207 and `__necpc_bios_timeofday` at +231. All **262 CODE bytes** are
source-equal to the target, including a real x87 `fninit`/`fnstcw`/`fnstsw`
detection sequence, BIOS equipment bit counting, DOS interrupt vector
33h inspection with a literal resident-driver signature, the actual
`int 33h` mouse check, NEC A000h/D000h memory status probes, and the
original `int 1Ch` time-of-day entry. This is not a PC emulator replacement
or a synthetic array of original executable bytes.

All **41 initialized DATA bytes** are the original named null-terminated
DOS driver signature, used by the pre-DOS-3 resident-vector comparison.
The original `_TEXT`/`_DATA`/`_BSS` 262/41/0 segmentation, BSS-first
GROUP `08ff03ff02`, all public offsets, zero external imports, and the
single **literal ordered original FIXUPP** for CODE+107 -> DATA+0 are
reproduced, including frame/target/addend. Active MAINL and installed
CL.LIB vendor programs were independently checked to be identical for
this member; unlike the earlier `setblock` case, there is no context
identity ambiguity here. Original complete Borland OMF member-record
serialization beyond the protected fields is still not claimed equal.

The after408 source-bound native builder validates the active after407
576-member carrier and executes two new actual TASM/TLIB/TLINK rounds,
retaining full OBJ/LIB/EXE/MAP outputs and writer logs for both. Both
whole original decoded Japanese MAINL EXE/MAP are byte-for-byte equal
(67,372-byte MZ EXE and 677 ordered relocations). Working CRT now has
**577/893** source-linked members and **165,150 original-equal CODE bytes**,
leaving **316** contextual vendor members. No full cold replay was run;
this milestone grants no accepted packed-file unit or Factory source credit.

Focused checks:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_after408_work.py nec-bios-equipment-boss
PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_after408_work -v
```
