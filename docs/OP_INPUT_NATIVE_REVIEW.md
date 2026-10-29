# OP input scanner native source review

2026-10-29: the complete function at0BEB:0304 now has source ownership:
417 CODE bytes/115 instructions/42 native DGROUP WORD fields/no scoped MZ
relocations. It returns far without arguments or callee cleanup. The explicit
legacy byte at04A5 is outside this function and remains unowned.

## Function proof independent of the trailer

The actual TC4 producer consumes `th03/input_s.cpp`, then the literal include
`th03/hardware/input_s.cpp`, then maintained `src/op/hardware/input_sense.cpp`.
Every consumed source/header is checked against the unchanged current source
graph and staged file. The actual module has WORD-aligned CODE418, empty DATA
and BSS, and one native function public. Both MAP public tables and every
containing allocation are checked.

The actual emitted stream has42 distinct offset fields. Each is an
ordinary near DGROUP WORD reference to `js_stat`, `input_mp_p1`, `input_mp_p2`
or `input_sp`, with a zero native addend. Every field is resolved from the OP
MAP, in its emitted order. Complete417-byte function equality is checked against
the Japanese target and current candidate, with an empty literal MZ vector.

Two independent native emitter routes also prove all417 bytes without the
trailing pragma: a direct TC4 compile and an unmodified TC4 `-S` output assembled
by TASM. Both produce a complete417-byte CODE record ending at the same RETF.
They retain their own emitted fixup order. Their empty DGROUP member orders
differ (DATA/BSS versus BSS/DATA), which is explicitly checked; neither emits
local storage. No object, source instruction or executable is patched.

These emitter observations are not a new two-round cold pair. The current
unchanged cold pair already repeats the containing native producer; its complete
input/output bindings are revalidated. Only the complete function is accepted,
with the legacy pragma declaration excluded from source ownership. No source
change or whole-TU/whole-product source acceptance is implied.

## Original input behavior

The function clears the four input WORDs, initializes BL to2 and ES to0, and
reads BIOS key groups7,9,8,5,4,2,0,3,6 in that order. It accumulates the two
samples with OR, preserving the original SP/P1/P2 key mappings and independent
tests. Between the samples it executes the original1024-iteration delay loop
on port5F. The zero-distance initial jump, register behavior and final RETF are
preserved. Every direct branch enters a complete instruction within the
function. There is no hidden library call or stack-frame prologue.

Native code equality proves this bounded source/ABI scope. It does not prove
physical keyboard typematic behavior or the delay port's physical duration.
No exhaustive key/flag matrix or second emulator implementation was added.

## Trailer and linked-layout experiments remain diagnostic

The legacy `#pragma codestring "\x90"` produces the current extra byte. Removing
it leaves the complete function and its native fields unchanged. The compiler's
actual ASM output ends without an EVEN directive or an extra instruction, and
TASM also emits417 bytes.

Three selected-object context links were observed, retaining all unrelated
native objects. Default linking without the trailer differs at4861 loaded
bytes. The documented TLINK packing switch `-P` gives the same result. An
explicit diagnostic annotation of the following PI module's segment from BYTE
to WORD alignment restores all other loaded bytes, leaving only04A5 as candidate
00 versus target90. That control still fails literal relocation-order equality.
It is not maintained product source, a native recipe change or an accepted fix.

This separates correct function code from the unresolved source/layout of the
following byte. Whole-file equality with the legacy codestring does not prove
its legitimate provenance. The byte must not be replaced with another arbitrary
padding mechanism. Further work must explain the actual layout/producer rule.

Evidence is `.analysis/work/input-native-review.json` and
`.analysis/work/input-layout-diagnostic.json`. The original direct probe remains
`.analysis/work/input-nostring.json`; its original non-acceptance statement is
preserved. The later complete function proof adds ownership without rewriting
that earlier observation. Product sources and native products were unchanged.

## Checks

```sh
PYTHONPATH=scripts .venv/bin/python -m lib.op_input_native
.venv/bin/python -m unittest tests.test_op_input_native tests.test_op_work_acceptance
.venv/bin/python scripts/publish_th03_op_work_scopes.py
```

Use one CPU, nice10 and empty displays. Focused controls reject identical
corrupted BIOS reads and an invented segment relocation on a near DATA field.
No full native cold replay or unrelated runtime chain is needed.
