# Complete MAINL CDG blitter candidate review

The two complete handwritten CDG drawing TUs contribute 496 decoded bytes:
three complete functions (493 bytes / 200 instructions) and three observed
EVEN bytes. Both cached products match every original raw byte and the two
original ordered relocation sites. Source/control-flow/far-Pascal and
self-modifying operand review is complete for these candidate CODE extents.
No maintained source, physical graphics or exact acceptance follows.

```sh
python3 scripts/review_th03_mainl_cdg_put.py --output .analysis/NEW_CDG_PUT_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_cdg_put_review.py -v
```

Receipt: `.analysis/sol-mainl-cdg-put-review-20261006.json`. It inherits guarded
canonical/decoded/cached lineage and separately pins eleven consulted frozen
providers in both source trees. Assembly differs only by LF-to-CRLF conversion;
headers/macros match byte-for-byte. Both complete TUs/includes, CDG slot and
lookup-table declarations, plane/row constants and relevant GRCG macros were
read. Ghidra headless-usage fails before DB attestation; no DB observations
are used. This is old cached compiler association, without a current cold build.

| Entry in decoded 0C7E | Function | Bytes / instructions | Return |
| --- | --- | ---: | --- |
| 01F4 | CDG with alpha | 179 / 70 | far RET 6 |
| 02A8 | Horizontal flip with alpha | 201 / 80 | far RET 6 |
| 0F32 | CDG without alpha | 113 / 50 | far RET 6 |

The containing MAP contributions are 382 bytes for `th03/cdg_put.asm` and
114 for `th03/cdg_p_na.asm`. NOP bytes 02A7/0371/0FA3 correspond to observed
EVEN positions and are accounted separately. Branches stay within complete
instruction boundaries. The only foreign call is far GRCG color setup at
`0000:0C36`, with four bytes of Pascal arguments. Every return cleans six
argument bytes; SI/DI/BP/DS are preserved. Hflip uses FS for source segments
and leaves it clobbered; ES and other volatile registers are not asserted saved.

## Actual code writes and flat-memory scope

All blitter instructions, REP/LOOP operations, XLAT lookups, segment transitions,
plane reads/stores and far returns execute. A single color-setup interface
models only its argument/return contract; actual OUT 7C,0 is recorded. The
supplied lookup table is a mathematical 256-byte bit reversal fixture, not a
replayed real startup initialization or imported target array. Artificial
alpha/color buffers and deterministic flat memory supply the operand bytes.
No CDG file or game asset is loaded or committed.

Alpha copies affect the addressed flat B window; real GRCG RMW broadcast,
tiles, mask clearing and banked page pixels are not simulated or proved.
The scalar specification reproduces these *flat operand* effects, including
native copy/OR stores and hflip byte reversal. It compares all 393216 bytes
at A0000..FFFFF, every ordered store and the unchanged 65536-byte DGROUP
window, rather than only a rendered rectangle or selected pixels.

Each call patches actual words inside MOV immediates in its own CODE:
alpha writes five words (source segment, starting offset, two widths and
stride); hflip writes six (two last-X offsets, two byte widths and two strides);
noalpha writes one width. Patch destinations are complete immediate operands,
and the complete ordered code-store list and computed values are checked.
The source's short jumps occur after the initial patching. Every valid case
then re-enters the same emulator with different geometry; complete resulting
stores agree, checking that translated-code state does not retain old operands.
Shared patched operands provide no independent proof of interrupt-safe or
reentrant use.

## Preserved coordinate and metadata behavior

Slot addressing uses `1D0E + ((slot << 4) mod 65536)`, with final word wrap,
without a 32-slot check. Fixtures include 0/31/32/FFFF; slot32 aliases the next
data region and FFFF selects 1CFE. The probe supplies constructed metadata at
those addresses without claiming a real loader validates or populates them.
Input pixel width/height are deliberately inconsistent with the precomputed
fields: the core routines use dword width and bottom-left offset, rather than
those pixel fields.

Left uses signed SAR 3, then adds the bottom offset with word wrap. Top produces
segment `(A800 + top*5) mod 65536`. Rows stop according to the sign of the
updated destination offset, with a do-first-row structure. There is no screen
clipping or universal height counter. Source offsets advance with word wrap
and remain continuous across color planes. Native dword stores at offsetFFFF
cross the segment's 64K offset boundary as one flat access; the next word
offset update wraps. Hflip uses separate byte stores with per-byte offset wrap.
The explicit left=-1/bottom0 fixture checks this distinction.

Plane traversal uses unsigned comparisons against C000/C800, adding 0800
between B/R/G and an additional 2000 for E. With top=-1 it draws five color
planes at A7FB/AFFB/B7FB/BFFB/E7FB and consumes a fifth source plane. The
constructed source window supplies those bytes; valid CDG resource size and
normal gameplay reachability remain separate. Left contributes to the signed
row termination as well: with width3/bottom160/left=-1, forward routines visit
two rows while hflip visits three. The probe retains this difference rather
than forcing equivalent rectangle geometry.

Alpha and noalpha explicitly CLD and return with DF clear. Hflip uses scalar
inc/dec addressing and retains incoming DF. Both DF states are checked.
Coordinates beyond the screen, negative coordinates and unchecked slot values
are retained as constructed caller contracts without repairing target behavior.

With dword width0, noalpha's REP copies zero words and returns without pixel
stores. Alpha reaches its color LOOP with CX0 and wraps toFFFF; a 2000-instruction
budget stops after 391 dword stores without return, after GRCG-off. Hflip enters
its alpha byte LOOP with CX0, writes at wrapped last-X FFFF and remains
nonterminal after 327 stores; it has not reached GRCG-off. No successful draw,
parameter guard or physical device outcome is fabricated for these cases.

## Verification and acceptance boundary

Per image: fourteen geometry/slot/DF cases per function, each invoked twice,
plus one zero-width call per function: 87 invocations in 45 records. Across
target/two caches: 261 invocations, 255 terminal returns and six bounded
nonterminal observations. Complete observations agree. Seven synthetic
controls reject malformed cleanup/truncation/EVEN bytes, invalid immediate
patch ownership, branch operands/neighbors, unknown calls, callback/outside
data writes, interface/terminal aliases, stale terminal state and wrong far
cleanup.

Three decoded function boundary rows add no maintained source or stored-file
offset. Raw byte/relocation matches do not close cold source/localized
dependencies, full DGROUP/BSS/lookup-table and resource ownership, GRCG/page
devices, canonical DIET packaging or the complete Oracle set. The broader
TH03 intake remains open.
