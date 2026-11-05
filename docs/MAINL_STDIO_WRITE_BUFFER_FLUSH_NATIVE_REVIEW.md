# Original Japanese CRT native write, setvbuf and fflush complete source

Three previously authored yet uncounted 16-bit Borland runtime members are
independently reassembled as **full original-source providers**, not copied
vendor objects or a short wrapper-only subset:

| Original library member | CODE / DATA | Original public and implementation |
| --- | --- | --- |
| `write` (331) | 358 / 0 bytes | `___write` — translated/buffered write, append seek and short-write accounting |
| `setvbuf` (285) | 289 / 4 bytes | `_setvbuf` — verify FILE token/flags, flush old buffer, preserve position and set buffering policy/ownership |
| `fflush` (219) | 209 / 0 bytes | `_fflush` — flush all or selected FILE, preserve input/output level and pending buffer semantics |

The exact source implementations reside in `src/mainl/crt/{write,setvbuf,fflush}.asm`,
including their source-bound shared `stdio_layout.inc`. The original Japanese
CL.LIB member interface, CODE/DATA/BSS segment geometry, every public and
external import, and **all 24 relocation sites, target names, frames and
literal FIXUPP order** agree with independent original native OMF analysis.
The separately extracted `vendor/write.obj` differs in an `_IOERROR`
near-call frame at CODE+23; the authoritative CL.LIB member, not that
alternative standalone OBJ, is the builder's original.

`scripts/build_th03_mainl_after348_work.py stdio-write-buffer-flush` checks
the full inherited source/receipt-bound **390-member** Japanese carrier,
hashes both named `.asm` and `stdio_layout.inc` and reassembles these three
source files using original native TASM, TLIB and TLINK in **two independent
rounds**. The 893-slot CRT carrier remains complete; **393** members are now
native-source-backed, **500** remain unchanged original contextual members,
and original-equal CRT CODE reaches **127,006 bytes** (+856), plus the four
bytes of original initialized setvbuf DATA. Both original Japanese MAINL
**67,372-byte EXE and MAP** and the **677 original ordered DOS MZ
relocations** match exactly. The entire raw OBJ/LIB/EXE/MAP vectors, source
and include hashes, parent receipts and compiler/linker logs are retained
under `.analysis/work/after348-*` and reviewed by the scoped reviewer and
`tests.test_mainl_after348_work`.

These are validated working-source reconstructions; **full original Borland
OMF member record streams are not identical** to TASM metadata, nor is
Factory accepted decoded/packed unit scope increased. No cold replay ran.
