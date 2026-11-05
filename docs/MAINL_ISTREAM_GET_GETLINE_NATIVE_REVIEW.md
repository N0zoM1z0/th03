# Complete original C++ istream::get and getline, native Japanese EXE/MAP

The original Japanese Borland CL.LIB members **779** (`istgstr`) and **776**
(`istgline`) have been reconstructed as complete 8086 source:
`src/mainl/crt/istgstr.asm` and `src/mainl/crt/istgline.asm`. These are not
one-call wrappers. Both functions implement the full streambuf read/get area,
virtual far underflow/refill, delimiter handling, EOF/fail and original stream
state updates with the original `ios::setstate` and `istream::ipfx` imports.
The two have distinct delimiter and terminator behavior, not artificially
shared output bytes.

| Original member | Complete CODE | Public far C++ function |
| --- | ---: | --- |
| `istgstr` (779) | 327 | `@istream@get$qncic` |
| `istgline` (776) | 325 | `@istream@getline$qncic` |

Both own `_TEXTA` CODE segments and zero-length `_DATA`/`_BSS`, with original
DGROUP ordering `08ff02ff03`. Each complete member has one original far
public and two original imported far calls. The source keeps the actual
virtual `streambuf` calls and their register/stack conventions, rather than
substituting ordinary near C library input calls.

The original BCC emits its OMF FIXUPP fields in **reverse site order**:
`[301,19]` for `istgstr` and `[299,19]` for `istgline`. A straightforward
forward source matched all original **652 CODE bytes** and all logical OMF
fields but reversed these two record pairs. The final source places the
second genuine `ios::setstate` call at its original CODE offset first, via
`ORG`, then emits the original earlier `ipfx` body from CODE+0. That preserves
all 8086 instruction semantics and bytes, and restores the **four literal
original FIXUPP fields, frame, targets, sites and order** without binary
arrays or patched object records. The native OMF program metadata still
differs from the original complete Borland record serialization; full OBJ
record identity is not claimed.

`scripts/build_th03_mainl_after357_work.py istream-get-getline-boss`
revalidates the **408-member** source-bound Japanese MAINL carrier and
compiles only these two new original members, rebuilding the 893-slot CRT
library and full link in **two independent TASM/TLIB/TLINK rounds**. Both
exactly reproduce the original decoded **67,372-byte MAINL EXE and MAP**,
including the complete 677 ordered DOS MZ relocations. The carrier now
contains **410 complete source-backed members**, **483 unchanged original
contextual programs**, and **132,428 source-compiled original-equal CRT CODE
bytes**, an increase of **652 bytes**. Original OMF evidence, raw two-round
OBJ/LIB/EXE/MAP producer artifacts, logs and hashes are retained under
`.analysis/work/after357-*`, with scoped review and raw original OBJ checks
in `scripts/review_th03_mainl_after357_work.py` and
`tests/test_mainl_after357_work.py`.

This is working CRT source progress; no full cold replay, new Factory formal
accepted extent or canonical packed-image unit credit is claimed.
