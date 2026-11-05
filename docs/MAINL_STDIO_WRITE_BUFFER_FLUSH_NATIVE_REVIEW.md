# Original `write`, `setvbuf`, `fflush`: three complete 16-bit CRT members

This increment validates and adopts three **existing natural-source
implementations**, never assuming that their earlier revisions, notes or
standalone vendor OBJs were correct. We independently recompiled
`src/mainl/crt/{write,setvbuf,fflush}.asm` with native TASM, compared every
materialized CODE/DATA byte, all PUBDEF and EXTDEF identities, DGROUP
layout and the original complete ordered FIXUPP inventories against **the
pinned Japanese CL.LIB members**, then rebuilt a real original 893-member
library and the complete MAINL executable in two separate native rounds.

| Original CL.LIB slot | CODE | Initialized DATA | Complete native operation |
| --- | ---: | ---: | --- |
| `write` (331) | 358 | 0 | `___write`: CRLF translation with 128-byte scratch, append seek, partial/short write, EOF and error paths |
| `setvbuf` (285) | 289 | 4 | `_setvbuf`: preserve stream position, flush/free existing buffer, install shared or owned buffer, manage stdin/stdout flags |
| `fflush` (219) | 209 | 0 | `_fflush`: reset input/get position, commit buffered output with short-write/error semantics, and all-stream flush |

The three 8086 far functions use the original `stdio_layout.inc` FILE flags,
member offsets and mode masks. The 4-byte DATA state in `setvbuf` is the two
original initialized 16-bit standard-stream configuration words. The new
producer and reviewer both bind the **content SHA256 of the included
`stdio_layout.inc`**, not just the top-level `.asm` source hashes. All
**856 CODE bytes, four initialized DATA bytes, 24 original FIXUPP fields and
their literal order** are correct. Each member's full Borland OMF program
serialization remains different in other records; this is not described as
an original byte-identical individual OBJ.

## Rechecked actual CL.LIB versus alternate standalone `vendor/write.obj`

The separate original-style `vendor/write.obj` is not the exact CL.LIB
member. Both have identical CODE, PUBLIC/EXTERNAL interfaces, group and
relocation targets, but the near `__IOERROR` call at CODE+23 is **CODE
frame0** in the pinned CL.LIB and **TARGET frame5** in the standalone
vendor program. The driver explicitly verifies this one-field mismatch
rather than weakening original-library comparisons. For `setvbuf` and
`fflush`, the standalone vendor logical fixups have the same full fields as
the pinned library (their record order may still differ).

`scripts/build_th03_mainl_after348_work.py stdio-write-buffer-flush`
consumes the SHA-bound **390-source** parent, builds **three entire changed
CRT objects**, and reconstructs all 893 original member slots using
TASM/TLIB/TLINK in **two independent native rounds**. Both reproduce the
original Japanese decoded **67,372-byte MAINL EXE and MAP** byte-for-byte,
including all **677 original ordered MZ relocations**. The working CRT now
contains **393 complete source members**, **500 unchanged original
contextual programs** and **127,006 original-equal CRT CODE bytes**, a gain
of **856**. Raw dual-round OBJ/LIB/EXE/MAP files, assembler/linker logs,
full source hashes and parent receipt bindings remain in
`.analysis/work/after348-*`. The scoped reviewer and direct regression are
`scripts/review_th03_mainl_after348_work.py` and
`tests/test_mainl_after348_work.py`.

No cold replay, invented code arrays, target-object patches, formal Factory
accepted source-ownership credit or whole-game exactness is claimed.
