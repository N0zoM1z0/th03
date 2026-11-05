# Original far MBCS tokenizer state machine — after454

Japanese Borland CL.LIB member `FMBSTOK` (index **689**) is now
maintained in [natural 8086 source](../src/mainl/crt/FMBSTOK.asm).
The full 230-CODE-byte `__fmbstok` routine consumes an optional
incoming far string or the saved static far tokenizer cursor. It
skips delimiter prefixes via `__fmbsspnp`, rejects invalid terminal
lead-byte characters using the genuine `__mbctype` classification,
searches for the next delimiter through `__fmbspbrk`, handles the
original double-byte delimiter boundary and NUL-terminates the
extracted token. It preserves the real saved offset/segment pointer
and the original 16-bit far-pointer arithmetic without defensive
rewriting. Its DATA contains a genuine four-byte persistent far
cursor, not unexplained zero padding.

The entire **230 original CODE + 4 initialized DATA bytes**, public,
three ordered imports and **12 logical original OMF FIXUPPs** agree
at site, kind, frame, target and addend. This includes CODE+54
-> `__fmbsspnp` and +127 -> `__fmbspbrk`, two `__mbctype` lookups
and all real saved-state DATA references. An initial native build
caught a genuine error hidden by CODE/FIXUPP equality: **TASM emitted
GRPDEF `08ff03ff02` instead of the original `08ff02ff03`**.
Changing the natural group declaration to `_BSS,_DATA` restored
its exact original GRPDEF; no special-case acceptance or OMF patch
was used. The literal ordered Borland/TASM FIXUPP chronology still
differs and complete raw OBJ-program identity is not claimed.

After454 validates the unchanged after453 661-source parent, then
runs two fresh TASM/TLIB/TLINK native rounds with raw OBJ/LIB/EXE/MAP
pairs, logs and source hashes retained. Both complete decoded
Japanese MAINL EXE and MAP match their targets exactly (67,372-byte
EXE, 677 ordered MZ relocations). The working CRT now has
**662/893** original source-linked members, **177,902 original-equal
CODE bytes**, and 231 remaining contextual vendor members.
This is not Factory source acceptance or a full cold replay.

Focused reviewer: scripts/review_th03_mainl_after454_work.py,
mode far-multibyte-strtok-state-machine.
Tests: tests.test_mainl_after454_work.
