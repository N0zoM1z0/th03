# Shared DOS exec and OP source-runtime adoption after537

`src/shared/crt/dos_exec.asm` restores the real compiler-library `exec` member
and is now consumed by **both MAINL and OP**. This corrects an original-input
mistake in the historical after338 comparison; it adds no function/member or
CODE-extent credit.

## Correct original evidence and the source change

The installed Japanese compiler CL.LIB SHA-256 is
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
Its member 345 has a 933-byte CODE extent. The first **255 bytes are initialized
zeros**, represented by the original 13-byte recursive LIDATA record
`010000ff000100010000000100`. They are named work storage: a 143-byte copy
stack, PSP word, 80-byte pathname, two FCB bytes, MZ header and overlay load
parameters. The source initializes those fields individually. They are not
padding or an instruction byte array.

The two-byte saved-environment word at CODE+356–357 remains genuinely
uninitialized. The 97-byte copied continuation starts at +255; the public
574-byte near `__exec` body starts at +359. The complete CODE extent therefore
has **931 initialized bytes and two true holes**. The original instructions,
unchecked DOS/COM/MZ behavior, cleanup, copied stack/transfer and error paths
are preserved. No runtime probe is needed to test a changed algorithm: the
671 instruction bytes remain the same.

Original data-import fields at CODE+371,+397,+482,+560 use **TARGET frame5**.
The old source assigned those imports to its own empty DATA segment, emitting
DGROUP frame1. Declaring the imported runtime words outside that segment
restores the original frames without changing instructions or operands.
All **21 full literal relocation fields now match in original order**, with
no normalization. SEGDEF, GROUP, imports, PUBLIC and MODEND record payloads
also agree. OMF data-record packing differs; complete program-record identity
is not claimed.

The historical after338 receipt actually used the earlier 28-source carrier
library SHA `64b0a5cce0523b38123eb475d7db4e2b91e546b045f80aea37ff56e978dec406`
as its member oracle. That already contained the uninitialized work area and
DGROUP-frame reconstruction. Its raw repeat and native MAINL link remain valid
historical observations, but its claims about the real original work area and
complete original program identity were incorrect. Those receipts, sources
and raw outputs remain unchanged; the old review now points to this correction.
The latest live exec owner is the new shared TU, not the frozen historical TU.

## Two actual products and complete original material coverage

Two fresh TASM/TLIB rounds replace only `exec` in the source-bound 893-slot
library; **892 other member programs and all slot positions remain unchanged**.
Each round reuses after535's source-generated large-model C0, the unchanged
MAINL game objects and OP's current source-bound thirty-object cold vector.
OP's live 330-source staging graph, both original round inventories, all raw
objects, recipe/tools, decoded and stored target identities are revalidated.
No game object, old CRT member or native cold graph is rebuilt.

| Output | Both rounds |
| --- | --- |
| MAINL decoded EXE | **67,372 bytes, original raw equality, 677 ordered relocations** |
| MAINL native MAP | **80,967 bytes, exact equality to reviewed after536 MAP** |
| OP decoded EXE | **63,866 bytes, original raw equality, 607 ordered relocations** |
| OP canonical packed file | **36,041 bytes, original raw equality** |
| OP native MAP | **68,078 bytes; precisely reviewed zero-length rows below** |
| DIET OP pack/restore | Two real `-B`/`-ra` rounds; original packed bytes and decoded roundtrip |

The entire seven-file exec-OBJ/LIB/two-EXE/two-MAP/packed-OP vector repeats
byte-for-byte. C0 and library inputs are explicit local paths; the link does
not silently fall back to the prebuilt installed C0L or CL.LIB.

The actual selected member material is compared directly against the **real
original CL.LIB**, including every initialized byte, uninitialized position,
segment attribute, complete extent and actual MAP contribution:

| Selected runtime material | MAINL: 75 members | OP: 76 members |
| --- | ---: | ---: |
| CODE extent / initialized / uninitialized | 29,961 / 29,953 / 8 | 29,964 / 29,956 / 8 |
| DATA extent / initialized / uninitialized | 1,645 / 1,639 / 6 | 1,647 / 1,641 / 6 |
| INITDATA extent / initialized / uninitialized | 30 / 26 / 4 | 30 / 26 / 4 |
| EXITDATA, initialized | 6 | 6 |
| BSS, uninitialized | 150 | 150 |

These are shared compiler-runtime contributions, **not new authored-game
credit**. The 893-slot whole-library count includes unlinked members and is
not a game-completion denominator. The separately reused C0 has its previously
reviewed 625-byte CODE extent, 144 DATA and 128 reserved STACK bytes.

OP's complete MAP differs from its historical cold MAP only by the zero-sized
`fbrk` BSS row at existing `0D7F:2502` and omission of the zero-sized `setblock`
BSS row at existing `0D7F:2510`. Every material row and every other byte remain
equal. This reflects the inherited source GROUP/empty-segment shapes; it does
not allocate or move any storage. The comparator checks exactly those literal
rows and does not broadly normalize or rewrite either artifact. MAINL retains
after536's explicitly reviewed PUBLIC tie/zero-BSS layout.

## Retained proof and exactness limits

Producer: `scripts/build_th03_runtime_after537_work.py`.
Independent reviewer: `scripts/review_th03_runtime_after537_work.py`.
Scope: `config/th03_runtime_after537.json`.
Root: `.analysis/work/runtime-after537-build.json`.
SHA-256: `ee5fcbe49af194eab79fe96234fcf23a627e91a114b6d3e2032891b1cdbeab2c`.

All seven raw outputs per round and thirteen native writer logs remain under
`runtime-after537-*`; actual sources, recipe/config, extracted inputs and
responses remain under `TH03ML/probe/af537d` and `TH03OP/probe/af537d`.
The unchanged C0, parent libraries and thirty OP game objects remain in their
original evidence locations. The historical OP cold builder retained one raw
vector with equal two-round inventories; this stage does not invent two
independently stored historical cold vectors.

Earlier `af537a` established the cross-product link and exposed the work-area
coverage difference; `af537b` restored initialization; `af537c` checked the
original frames. All probe sources, objects, outputs and logs remain. The
independent final review launches no native writer or ancestor runtime model.
Preflight, affected native review, progress/tracking and whitespace checks pass.
No full CI, native cold replay, emulator matrix or output cleanup was run.

Other literal OMF differences remain. The retained diagnostic inventory
`.analysis/work/runtime-after537-selected-literal-field-audit.json` classifies
OP's 76 selected members: 56 have equal literal field streams, 16 have field
order differences, and four have per-site attribute differences (`fbrk`,
`write`, `execl`, `loadprog`; ten near-call frame differences total). This is
an investigation queue, not source-exact progress. C0's 58-field ordering gap
also remains. Whole-product source acceptance and canonical Factory unit credit
are unchanged; MAINL is still **0/250** and the whole-game denominator is unknown.
