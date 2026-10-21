# MAINL graphics and resource source proof

## Owned scope

The 23 maintained symbolic includes in `src/mainl/resources/` own 14 existing
MAINL decoded units, totaling 3,475 bytes. This adds no units to the denominator.
The source checkpoint was `ad0e8d4`; it did not change source counts. Native and
runtime evidence below support promotion to source-present, not formal exactness.

| Existing unit suffix | Segment:offset | Bytes |
| --- | --- | ---: |
| draw-gaiji | 0000:0F58 | 148 |
| draw-pack | 0000:162C | 212 |
| draw-scroll | 0000:1700 | 88 |
| draw-show | 0000:1758 | 6 |
| draw-noclip | 0000:2C68 | 202 |
| draw-table | 0000:1AAA | 1,024 |
| bfnt-library | 0000:0272 | 512 |
| super-library | 0000:237E | 1,008 |
| dos-close | 0000:0A98 | 22 |
| gdc-outpw | 0000:0C66 | 11 |
| pi-decoder-free | 0000:0FEC | 76 |
| stack-memory | 0000:1EAA | 76 |
| palette-bfnt | 0000:04C6 | 64 |
| buffer-dos-open | 0000:0AAE | 26 |

## Symbolic source and dependencies

The composer changes exactly one original include position per provider in the
already maintained MPI02 root. Full statement expansion matches the original
providers. Original `EVEN`, macros, aliases, memory-model frames, carry/DF quirks,
and BFNT/super self-modified instruction slots are retained. Mutation controls
reject changed instructions, branches, table entries, dispatch offsets, removed
alignment and appended bytes. No target-byte arrays or object rewriting are used.

RotTbl is 256 typed DD entries, not 1,024 instruction bytes. For input v and plane
b=0..3 its little-endian byte is `(v >> b & 1) | ((v >> (b+4) & 1) << 1)`.
All entries are exhaustively checked against that independent semantic formula;
the native 1,024-byte output is separately compared to the target.

Imported DATA/BSS, clipping state, font/VRAM state, palette/header/pattern arrays,
mask tables and allocator context remain explicit dependencies. Existing heap
source credit is not counted again. Source localization does not imply ownership
of every contextual provider used by the models.

## Two real consumed-source assemblies and links

MRS01 and MRS02 each freshly assemble the root through TASM and link through the
original TLINK response order. Each phase has a 90-second native budget and
15-second owned cleanup budget, one CPU, nice 10 or greater, with the existing
shared lock/claim/poison controls. All four phases finished exit 0, no timeout,
no surviving owned process, no poison and a released lock.

MRS02 copies 1,822 declared first-build inputs at their observed mtimes and omits
root OBJ, EXE and MAP outputs. Its independently produced raw root OBJ, EXE and
MAP exactly equal MRS01. Complete EXE and MAP also equal MPI02. This is a hybrid
root rebuild with retained contextual objects, not a whole-program cold build.

All 14 scopes /3,475 bytes equal the decoded target. Each scope has zero loader
relocation sites in both images. Previously proved 13,495 scoped bytes survive
by complete EXE identity, for 16,970 scoped target-equal bytes in total.

EXE SHA256: `6d159b90fffe0d0ac00d587429204fa616228abc7244ee4c4e184449a2fdde63`.
MAP SHA256: `ec8f9b4d397f7194253fdc45b2c4fd1ad4d30b794bdd7f601b387227c3340363`.

## Runtime models

Ten independently bounded, one-CPU phases reran the existing models on decoded
target and freshly linked MRS01. All succeeded and cross-image observations match:

- Draw: 7,196 terminal cases and 16 nonterminal prefixes per image.
- BFNT/super: 949 terminal cases and 10 prefixes per image.
- Stack memory: 488 terminal cases per image.
- Palette: 2,498 terminal cases and 8 prefixes per image.
- Buffered DOS I/O: 1,754 terminal cases per image.

These cover explicit DOS, GDC, BIOS, font, GRCG and self-modifying dispatch models,
not physical-device execution. Models may include contextual callers; that is not
additional source credit. Nonterminal prefixes prove bounded behavior, not return.
The existing PI_FREE evidence is retained by complete target/candidate EXE identity
from `.analysis/mainl-pi-fresh-models-20261021-v01.json`, not rerun.

Each original comparison contract is preserved. Draw/super/smem/palette omit only
top-level before/after full-memory hashes when comparing different images, while
each case checks the independent scalar memory model. Buffer instead omits only
`data_before_sha256` / `data_after_sha256`; its per-case checks still compare entire
64 KiB data, buffer and output regions. No generic normalization is introduced.

The compact comparison receipt is
`.analysis/mainl-resources-source-20261021-v01/model-comparison.json`.
Fast replay retains actual model dependencies, complete receipts, consumed sources,
native phase/cleanup records, raw outputs and observed input mtimes. It invokes
neither native tools nor the runtime matrices. Unrelated progress presentation
changes are not live model dependencies; a real model mutation is rejected.

## Acceptance limits

Eligible source progress becomes 65/145 MAINL units /20,671 bytes. MAINL exact stays
zero. The complete decoded image still differs at DATA 0E3F:0849 (target 90h,
candidate 00h). All 677 relocation members match, with 461 global order-index
differences. Canonical packed mapping and a whole-program cold aggregate remain
unproved. Historical receipts remain unchanged.

Reproduce the bounded check with `python3 scripts/replay_th03_mainl_resources_link.py`.
