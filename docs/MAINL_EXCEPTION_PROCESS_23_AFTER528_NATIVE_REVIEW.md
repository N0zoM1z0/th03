# Complete exception, diagnostic and process-launch members — after528

Twenty-three original Japanese CL.LIB members now have complete maintained
instruction source. No previous source-linked member was replaced or counted
again.

| Slot / member | CODE bytes | DATA bytes | Ordered OMF fields |
| --- | ---: | ---: | ---: |
| 155 / `xxas` | 143 | 0 | 3 |
| 154 / `xxa` | 93 | 0 | 3 |
| 135 / `unhandl` | 122 | 36 | 9 |
| 0 / `_abort` | 27 | 31 | 3 |
| 41 / `errormsg` | 42 | 0 | 3 |
| 101 / `pureerr` | 68 | 58 | 8 |
| 158 / `assert` | 48 | 0 | 3 |
| 346 / `execl` | 35 | 0 | 2 |
| 347 / `execle` | 73 | 0 | 2 |
| 348 / `execlp` | 38 | 0 | 2 |
| 349 / `execlpe` | 74 | 0 | 2 |
| 350 / `execv` | 36 | 0 | 2 |
| 351 / `execve` | 40 | 0 | 2 |
| 352 / `execvp` | 39 | 0 | 2 |
| 353 / `execvpe` | 41 | 0 | 2 |
| 368 / `spawnl` | 81 | 0 | 4 |
| 369 / `spawnle` | 127 | 0 | 4 |
| 370 / `spawnlp` | 87 | 0 | 4 |
| 371 / `spawnlpe` | 129 | 0 | 4 |
| 372 / `spawnv` | 83 | 0 | 4 |
| 373 / `spawnve` | 91 | 0 | 4 |
| 374 / `spawnvp` | 89 | 0 | 4 |
| 375 / `spawnvpe` | 93 | 0 | 4 |

Total: **1,699 executable CODE bytes, 125 DATA bytes and 80 ordered logical
relocation fields**. The producer pins the actual CL.LIB member indices;
all segment payloads, public offsets, import order, GROUP records and
SEGDEF alignment/combination attributes are checked. Storage is typed
strings and a callback pointer. There are no target instruction arrays,
inserted padding or binary patches.

`xxas` and `xxa` preserve SS:10h's destructor count and SS:14h's exception
list. The registration frame saves **SEG DGROUP** at +0Eh, not the code
segment. Its exception handler has separate symbolic offset and segment
relocations. Original ascending assembly relocation chronology and DGROUP
membership order are reproduced, including the local push-CS/near-call
sequence to FAR accessors and the two-byte Pascal exit cleanup.

`unhandl` retains the FAR callback, DX:AX result and original four-/two-byte
Pascal cleanup. `_abort` retains its CR/LF message and exit code 3.
`pureerr` owns two distinct copies of its original diagnostic string; its
near and far entry points retain RET and RETF respectively. `errormsg`
reads the byte handle from stderr's original FILE layout and sign-extends
it before the low-level write. Assertion arguments and termination calls
are unchanged.

The sixteen process wrappers retain near `__exec`/`__spawn` callbacks to
near `__LoadProg`, four-byte FAR argv entries, original variadic terminator
scans, explicit environment traversal and PATH flags. Spawn mode 0 waits,
mode 2 overlays, and other values set original `EINVAL` (19). Existing
[errno constants](../src/mainl/crt/crt_errno.inc) and
[FILE layout](../src/mainl/crt/stdio_layout.inc) are hash-bound dependencies.
No pointer defenses or additional mode handling were added.

## Literal fields and the sixteen disclosed frame differences

All seven exception/diagnostic members have **literal ordered FIXUPP
equality**. Each process wrapper has exactly one difference, at its near
`__LoadProg` call: original `(frame_method=5, frame=null)` uses TARGET;
TASM emits `(frame_method=0, frame=1)`, its CODE segment. Segment, field
site, location type, width, relative flag, external target, addend and
ordered position all agree. Callback-pointer fields already agree literally.

| Member | Loader field offset | Member | Loader field offset |
| --- | ---: | --- | ---: |
| execl | 26 | spawnl | 61 |
| execle | 62 | spawnle | 105 |
| execlp | 29 | spawnlp | 67 |
| execlpe | 63 | spawnlpe | 107 |
| execv | 27 | spawnv | 63 |
| execve | 31 | spawnve | 71 |
| execvp | 30 | spawnvp | 69 |
| execvpe | 32 | spawnvpe | 73 |

Both full raw field transcripts are retained in each round's
`raw_frame_differences_by_member`. The logical comparison recognizes only
these pinned near-loader sites and validates all other attributes before
comparing them. It changes no object bytes. Original Borland OBJ program
record identity and full literal FIXUPP equality are **not** claimed.

## Scoped native evidence

The [producer](../scripts/build_th03_mainl_after528_work.py) reuses the
unchanged, source-bound after527 carrier, including its two short-DOS
`af527b-` vectors and both include hashes. Its retained chain still checks
the after526 raw FP/near-call differences. Two fresh headless TASM 5.0 /
TLIB / TLINK rounds reproduce the complete original decoded Japanese
**67,372-byte MAINL EXE, original MAP and all 677 ordered MZ relocations**.
Both complete OBJ/LIB/EXE/MAP vectors agree between rounds; all 774 inherited
source members, 96 remaining vendor members and the original 893-member
order are preserved.

The [independent reviewer](../scripts/review_th03_mainl_after528_work.py)
checks source/include/recipe/parent hashes, all actual writer logs, complete
payloads/interfaces, the 16 raw differences and both full native output
vectors. No full cold replay, new runtime model or redundant test matrix
was run. All outputs, logs and scratch remain protected pending a fresh
storage audit.

Current working-source CRT: **797/893 complete members, 204,629 original-equal
CODE-segment bytes**. Formal Factory canonical packed-file acceptance stays
**0/250**; whole-game completion is not established. Pinned targets remain
`candidate-local-attested`.

Receipt: `.analysis/work/mainl-after528-exception-report-process-twenty-three-build.json`

SHA-256: `1c657c3fedcded7918174728314bb84daa5de8c19b6967b0d60763ba7f2787e3`.
