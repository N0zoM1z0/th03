# Complete console, interrupt, CPU and stack members — after529

Fourteen original Japanese CL.LIB members now have complete maintained
source programs in the working CRT carrier:

| Slot / member | CODE bytes | DATA bytes | BSS bytes | Ordered fields |
| --- | ---: | ---: | ---: | ---: |
| 564 / `screen` | 126 | 0 | 0 | 1 |
| 515 / `ccomputn` | 119 | 0 | 0 | 16 |
| 504 / `pc98mous` | 114 | 0 | 4 | 5 |
| 562 / `movetext` | 111 | 0 | 0 | 4 |
| 555 / `crtinit` | 106 | 22 | 0 | 16 |
| 551 / `conioini` | 42 | 0 | 0 | 4 |
| 523 / `cibmcrsr` | 92 | 0 | 0 | 5 |
| 567 / `validate` | 65 | 0 | 0 | 2 |
| 162 / `cputype` | 92 | 2 | 0 | 5 |
| 15 / `ctrlbrk` | 83 | 0 | 4 | 8 |
| 355 / `hard` | 58 | 0 | 0 | 3 |
| 4 / `alloca` | 50 | 0 | 0 | 0 |
| 7 / `chainint` | 25 | 0 | 0 | 0 |
| 376 / `stack` | 36 | 0 | 0 | 2 |

Total: **1,119 CODE-segment bytes, 24 initialized DATA bytes, 8 BSS bytes,
and 71 ordered logical relocation fields**. CODE contains **1,101 executable
instruction bytes and an 18-byte inline stack diagnostic string**. Startup
tables occupy another 18 bytes: **16 initialized INITDATA bytes and two
uninitialized bytes**, accounted separately from CODE and DATA.

## Recovered behavior and storage

`screen` retains the byte-sized row/column arithmetic, overlap-dependent
forward/backward row traversal, near Pascal line helper and twelve-byte
callee cleanup. `movetext` preserves the original validation, disabled-video
flag and conversion from one-based word coordinates to zero-based bytes.
`validate` keeps the original signed bounds comparisons and eight-byte near
Pascal cleanup. The NEC/IBM dispatcher retains near register/stack interfaces,
including the two-byte character argument cleanup; the IBM cursor helper
preserves mode/height-dependent scanline choices and its BIOS delegation.

`pc98mous` retains the INT 33h register block, callback registration and
FAR callback thunk. The thunk loads DGROUP, clears direction and passes four
word registers. Register-block access switches DS; callback storage writes
therefore require the original **explicit ES overrides**. Its callback is
four uninitialized BSS bytes. `ctrlbrk` keeps its independent four-byte
callback, complete saved interrupt register frame, IRET, zero-result exit
path and vector 23h installation. Its initial DS relocation uses the original
DATA segment with DGROUP frame, not a substitute GROUP target.

`conioini` preserves the original INT 1Ah detection, existing-type guard and
priority-15 FAR startup record. `crtinit` owns the full 20-byte video state,
`__directvideo=1` word and priority-16 FAR startup record. Original DATA
initialization contains a 19-byte LIDATA initializer; the materialization
check expands it and compares every actual byte, independently of record
boundaries. All original segment order, sizes, alignment/combination,
publics, GROUP records and import order remain checked.

`cputype` preserves FLAGS-based 8086/286 detection and the AC-bit test for
386/486, with USE16 segments and the original 32-bit register operations.
It saves full ESP before temporarily aligning SP. Its priority-16 **near**
startup record has an initialized offset and an **uninitialized unused
segment word**. The verifier checks that absence explicitly; it does not
invent zeros. `alloca` retains original word rounding, stack/frame transfer
and wrap/failure behavior. `chainint` retains the original compiler interrupt
frame offsets, CLI and FAR tail return. `stack` emits a typed DOS '$'-terminated
message in CODE and preserves its near exit jump.

## Retained baseline and the huge-pointer diagnostic

The existing `src/mainl/crt/h_padd.asm` already has complete maintained source
and is bound to retained cold project objects. It is unchanged and receives
**no new member or CODE credit** in this stage. The incremental receipt set
counts explicit replacements against an earlier 28-source carrier, so its
remaining context list includes some existing baseline source owners. That
list must not be treated as a list of missing source functions.

The initial fifteen-member experiment also reassembled `h_padd` with the
pinned compatible emitter and original CL.LIB PUBLIC chronology. It matched
all CODE and the complete EXE, but reversed one same-address PADD@/F_PADD@
pair in the retained MAP. This exposed the distinction between the compiler's
original library and the earlier source carrier's export enumeration.
The experiment is **not** accepted as additional reconstruction progress.
Its incomplete receipt, raw native scratch, writer logs, original source/
recipe/profile snapshots and SHA-256 inventory remain retained under
`.analysis/work/probe/platform-fifteen-alias-diagnostic/` and the original
`TH03ML/probe/after529` workdir. No binary or MAP patch was made.

For the actual fourteen-member stage, every original program/profile comes
from the pinned compiler CL.LIB. Its hash is verified through the retained
cold receipt and reported separately by the independent reviewer. The
inherited maintained carrier remains the link baseline. The successful
producer uses fresh `TH03ML/probe/af529b` scratch and **af529b-** raw output/log
paths explicitly bound in the new receipt.

## Twelve disclosed near-call frame differences

Eleven members have literal ordered FIXUPP equality. Only `screen`,
`ccomputn` and `movetext` differ: at the following twelve external near-call
fields the original uses `(frame_method=5, frame=null)` TARGET while TASM
uses `(frame_method=0, frame=1)` CODE.

| Member | Ordered field sites | Actual target scope |
| --- | --- | --- |
| screen | 86 | `__MOVELINE` |
| ccomputn | 111, 98, 76, 64, 49, 37, 22, 10 | original NEC/IBM character and VRAM helpers |
| movetext | 105, 58, 25 | `__MOVETEXT`, `__VALIDATEXY`, `__VALIDATEXY` |

The exact target name is pinned per site. Segment, offset, field type/width,
relative flag, target, addend and ordered position all agree. Both raw
transcripts remain recorded in every round and are independently enumerated
by the reviewer. Logical comparison recognizes only these guarded frame
pairs; no object bytes are changed. Original Borland OBJ identity and full
literal FIXUPP equality are **not** claimed.

## Scoped native evidence

The [producer](../scripts/build_th03_mainl_after529_work.py) validates the
unchanged after528 carrier, including its 23 TU hashes, two include hashes
and sixteen explicitly recorded loader-frame differences. The older source
DAG and both complete output rounds remain intact. Only the fourteen affected
members are assembled, with headless serialized Borland writers on one CPU
at nice10.

Two native TLIB/TLINK rounds reproduce the full original decoded Japanese
**67,372-byte MAINL EXE, original MAP and all 677 ordered MZ relocations**.
Both entire OBJ/LIB/EXE/MAP vectors agree between rounds. All 797 inherited
source members, 82 retained context members and original 893-member order
are preserved. The [independent reviewer](../scripts/review_th03_mainl_after529_work.py)
checks actual source-path mappings, tool/recipe/parent hashes, writer logs,
initialized coverage, uninitialized extents, ordered fields and both full
native vectors. No full CI, cold replay or new runtime/test matrix was used.
All artifacts and diagnostic branches remain retained.

Incremental working-source CRT: **811/893 complete members, 205,748 original-equal
CODE-segment bytes**. Formal Factory canonical packed-file acceptance stays
**0/250**; whole-game completion is unknown. Targets remain
`candidate-local-attested`.

Receipt: `.analysis/work/mainl-after529-platform-startup-stack-fourteen-build.json`

SHA-256: `8a08bde43984b4031b9260915985866764e9212bdc30848edc84a5c64896073b`.
