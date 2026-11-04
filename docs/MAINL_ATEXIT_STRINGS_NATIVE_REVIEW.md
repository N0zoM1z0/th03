# Japanese MAINL original atexit / far strcpy / strcat source reconstruction

Three original selected 893-member Borland CRT slots were recovered as native
8086 source, including their complete public ownership:

| Original CRT index | Member | CODE | DATA | BSS | Relocation sites |
| ---: | --- | ---: | ---: | ---: | ---: |
| 5 | `atexit` | 49 | 2 | 128 | 5 |
| 293 | `strcpy` | 41 | 0 | 0 | 0 |
| 290 | `strcat` | 63 | 0 | 0 | 0 |

`src/mainl/crt/atexit.asm` implements the 32-element static table of far
shutdown callbacks and its two-byte count, matching all CODE/DATA bytes and
uninitialized BSS length. The exported ABI includes not only `_atexit`
(CODE+0), but **`__atexitcnt` (DATA+0)** and **`__atexittbl` (BSS+0)**.
The first scoped link *failed* with undefined references to these last two
symbols because a prior code-only inspection omitted DATA/BSS PUBDEFs. This
was resolved by recovering the genuine exports, **not** by changing binary
objects or relaxing the linker. The new local source scope enforces PUBLIC
symbol identity in all three segments, in addition to full original bytes.

`strcpy.asm` uses original far pointer ABI, `SCASB`-based length scan and
`REP MOVSB` to include the NUL terminator. `strcat.asm` searches both strings
and copies an odd leading byte followed by word-aligned `REP MOVSW` and an
optional final byte, preserving the original DS/ES switching. TASM's initial
`xchg di,si` spelling encoded an equivalent but different ModRM from the
original; the actual source uses `xchg si,di` to reproduce the **exact 63 CODE
bytes**. Both source objects preserve the native `_DATA,_BSS` group order,
which differs from the original `atexit` `_BSS,_DATA` group order. No original
CODE or DATA arrays, object patching or artificial size fillers are used.

## Additional original `ctime` DATA ownership correction

Inspecting the failed `atexit` link exposed a more general verification gap:
CODE/DATA byte equality alone does not establish all exported symbols. The
previous recovered `ctime` source already reproduced its complete CODE, DATA,
BSS, and linked executable, but omitted the selected original member's five
**DATA PUBDEFs**. They are now exported at their precise original offsets:
`_SWeekday` +0, `_LWeekday` +28, `_SMonth` +56, `_LMonth` +104, `_AmPm` +152.
The source-based `ctime` carrier was rebuilt in its affected incremental
modes and rechecked against the whole original Japanese EXE/MAP. This is an
ABI/ownership correction, not additional original CODE progress.

## Source-bound native evidence

`scripts/build_th03_mainl_after66_work.py
strerror-bsearch-strdup-abort-atexit-strcpy-strcat` produces two independent
normal TASM/TLIB/TLINK rounds on the original retained CRT context. All
**73 source-compiled members** occupy original slots; **820** original vendor
program records are unchanged. The complete original **67,372-byte Japanese
decoded MAINL EXE** and its original **MAP** remain byte-identical, including
all 677 ordered MZ relocations. Working source produces **30,764 original-
equal CODE bytes**, plus the recovered `atexit` initialized DATA and BSS. All
five `atexit` original fixup sites/targets, both far string CODE extents and
all code/data/bss publics are checked with the actual selected vendor member.

Review via `review_th03_mainl_after66_work.py` for the combined mode and
`tests.test_mainl_after66_work` plus `tests.test_mainl_after62_work`. The
raw OBJ/LIB/EXE/MAP two-round output vectors and local writer logs are
retained under `.analysis/work/after66-*` with source-bound build/review
receipts. **No full cold replay** occurred; this remains a *working-source*
claim, not new accepted ledger credit. Literal original OMF record identity
is still open for several members, even when the complete linked product
is equal.
