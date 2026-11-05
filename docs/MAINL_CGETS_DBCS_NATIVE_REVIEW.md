# Original Japanese `cgets` DBCS console reader: 347-byte source-bound member

The original Borland CL.LIB member **521**, `cgets`, is recovered in its
entirety as `src/mainl/crt/cgets.asm`. The source contains a **35-byte
nonexported near echo/backspace helper** plus the full **312-byte far `_cgets`
function** exported at original CODE+35. It preserves the original buffer
length handling, echo, CR termination, backspace and multi-byte Japanese
character paths. It performs the same original direct accesses to
`__wkanji`, `___conio_type` and indexed `__mbctype+1` (DGROUP-framed), and
uses the original far functions `_getch`, `_putch` and `__mbsbtype`.

The entire original `_TEXT` segment is **347 CODE bytes** with no missing
materialized bytes, and original empty `_DATA` / `_BSS`, original group
`08ff02ff03`, one far public and six imports. The complete **11 native
OMF FIXUPP fields** match site, location, width, target, addend, *and frame*.
The original ordered FIXUPP record sequence is not identical to TASM's,
so full Borland OBJ serialization identity is not claimed.

`scripts/build_th03_mainl_after336_work.py cgets-dbcs-console` extends the
360-source + 2,522-byte regexp matching source-bound carrier to the full
**362 source-backed** CRT members, with **531** unchanged original contextual
members and **118,024 original-equal CRT CODE bytes** (increase **347**).
Two serialized native TASM/TLIB/TLINK rounds exactly reproduce the complete
original Japanese decoded MAINL **67,372-byte EXE / MAP**, including all
**677 ordered MZ relocations**. The original member code and imports, both
native OBJ/LIB/EXE/MAP producer rounds, writer logs, checksums, source hashes
and parent receipt chain are available under `.analysis/work/after336-*` and
through `scripts/review_th03_mainl_after336_work.py` plus
`tests/test_mainl_after336_work.py`.

No whole cold replay, synthetic byte arrays, packed-file ownership or new
Factory acceptance is claimed for this working-source member.
