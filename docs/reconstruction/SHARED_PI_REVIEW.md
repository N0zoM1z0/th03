# Complete shared and ending PI wrapper review

Frozen revision: `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
Japanese YUMEZIKU targets remain `candidate-local-attested`; independent
pristine-dump attestation is unknown. OP/MAINL packed Ghidra databases were
re-attested before target observations. DIET restorations are diagnostic
namespaces, with no canonical-target replacement or invented stored offsets.

Four complete CPP carriers own five functions/555 bytes in MAINL. OP links
the shared palette/ordinary put/load subset, three functions/243 bytes.

| Carrier | OP decoded binding | MAINL decoded binding | Bytes |
| --- | --- | --- | ---: |
| `th03/pi_put.cpp` | `0BEB:04A6` | `0C7E:052A` | 173 |
| `th03/pi_load.cpp` | `0BEB:0A90` | `0C7E:0CCB` | 70 |
| `th03/pi_put_i.cpp` | absent | `0C7E:05D7` | 135 |
| `th03/pi_put_q.cpp` | absent | `0C7E:0D11` | 177 |

Independent DATA bindings are OP DS `0D7F`, headers `1CC0`, buffers `1CA8`,
palette `11B8`; and MAINL DS `0E3F`, headers `1F26`, buffers `1F0E`, palette
`141E`. The header stride is 72 bytes, buffer stride four bytes. The unchecked
slot calculations wrap at 16 bits. Header declarations and DATA/BSS ownership
remain separate from these observed CODE operands.

The five bodies have 197 instruction positions in MAINL; OP has 91.
Native library context adds graph free76/33 positions and memcpy36/20
positions. OP uses `0000:12DC` and `0000:4E5F`; MAINL uses `0000:0FEC` and
`0000:4B7D`. Context is never new wrapper ownership. Their complete callers,
branches, instruction boundaries and far returns are audited independently.
Graph free's three NOPs before PUSH CS/CALL execute when their corresponding
free branch is taken. The memcpy odd-byte branch is exercised through separate
direct calls; coverage is not inferred from the palette's fixed even length.

Twenty frozen providers establish wrapper/implementation/header/helper/root
and link lineage. Both preceding sound-loader cold trees retain them, except
the already recorded MAINL vector filename change. The diagnostic reverses
only that known filename replacement to compare the complete frozen Tupfile.
Historical MAINL cached PI shifts and caller-operand failures remain separate;
the original `0C7E:0529` neighbor is outside these carriers and gets no ownership.
The old cached receipt is not rebased or interpreted as a current producer.

Diagnostic receipt: `.analysis/sol-shared-pi-review-20261006.json`, SHA256
`51324b64b0df4d7b2e865b956b63bf02f347bae0f4af9179d4a85e62325b427b`, 658 guards.
Each artifact's target and two preceding sound-loader cold images passes:

- OP: 331 invocations, 327 far returns, four explicit draw-budget prefixes,
  all 144 wrapper/context positions, 2,074 ordered stores and 944 callbacks.
- MAINL: 499 invocations, 491 far returns, eight explicit draw-budget prefixes,
  all 250 wrapper/context positions, 2,074 stores and 14,976 callbacks.

All complete carrier bytes and original ordered relocations agree. The fresh
MAPs use the independently observed target bindings, with no former PI shift
or source credit for the neighboring byte.

## Native contracts and declared interfaces

`review_th03_shared_pi.py` executes the complete wrappers and original native
graph free/memcpy. Its scalar reads actual physical header and buffer bytes.
It compares ordered stores, full callback argument lists and physical 1 MiB
memory outside the 64 KiB caller-stack region. Stack locals and prologue writes
are excluded from memory equality; native return CS/SP, saved BP/SI/DI/DS/FS,
actual callback far frames and cleanup are checked separately. Budget prefixes
prove their observed requests and non-stack effects, without completed-return
or complete stack/local-state claims.

Palette show, packed drawing, heap free and image loading remain declared
callbacks. They preserve the registers required by their caller contracts,
return the declared AX/CF, and perform only explicit fixture writes. Callback
memory changes are separate from native stores and reflected in the scalar's
live physical memory. There is no synthetic replacement of native memcpy or
graph free, and no claim that the modeled graphics/loader/heap bodies execute.
Earlier native PACK/heap/decoder reviews are not silently inherited.

Observed behavior retained in the source and scalar:

- Palette apply uses native 48-byte memcpy, copying 24 forward words. Native
  CLD clears incoming DF. Overlap can propagate earlier word stores; the scalar
  reads each word from live memory, rather than copying a saved byte slice.
- Ordinary put uses the initial buffer far pointer, then reads live width and
  height around each callback. Width is halved unsigned for row advancement.
  A callback changing dimensions affects subsequent stride and termination.
- Interlace advances the source by a full width and the ushort counter by two.
  At height `FFFFh`, the even counter can wrap without reaching the height;
  its budget prefix is not reported as a returned call.
- Quarter put selects only quarters 1/2/3 for displacements 160/64000/64160.
  Other word values use the initial pointer. It normalizes before the first
  call and always emits 200 rows of width 320, independent of header dimensions.
- Far-pointer arithmetic first truncates the offset addition, then adds its
  upper 12 offset bits to the segment and keeps the low nibble. Carry lost in
  the 16-bit offset addition is not reconstructed as a linear advance.
- Top increments with word wrap and uses a signed comparison against 400.
  It subtracts 400 once when the wrapped signed value is at least 400.
- Load passes the existing header and buffer to native graph free before the
  load callback. Comment and machine pointers are read at header+2 and +18;
  the machine pointer is loaded after the first heap callback. Free clears the
  six-byte records in their actual word-store order, even on a modeled failure.
- Graph free does not clear `pi_buffers[slot]`. Repeated calls can free the
  retained buffer segment again. A declared loader callback can replace the
  pointer, and later calls use that live replacement. The loader's AX status
  propagates unchanged, including values with the high bit set.

Cases include odd/zero/max widths, zero/odd/max heights, all quarter branches,
invalid/wrapped slots, signed top/left boundaries, offset/segment wrap,
header/palette overlap, changed dimensions at the first and second callbacks,
changed machine pointers during free, retained/replaced buffers, all four
incoming IF/DF pairs, native odd/zero memcpy and overlapping direct copies.
Three load calls on one engine retain header and buffer effects between calls;
caller frames/registers are refreshed. Fourteen controls reject DATA/call/
cleanup/operand-entry/native copy-direction mutations and extra physical bytes,
and verify the observed overlap/counter/free/status/coverage hazards.

Device timing, VRAM clipping/ports, actual heap failure semantics, PI decoder,
files/assets, interrupt frames, CRT-wide behavior and real PC-98 execution
remain open. These fixtures and complete CODE observations do not constitute
the full Oracle set or exact acceptance.

## Maintained ownership

Shared ordinary drawing/palette and loading belong to
`src/shared/formats/pi_put.cpp` and `pi_load.cpp`. Ending-specific functions
belong to `src/mainl/formats/pi_put_interlace.cpp` and `pi_put_quarter.cpp`.
The complete frozen natural implementations are localized with explicit
compatibility imports. The new `compat/rec98/th03/formats/pi.hpp` is a pure
include forwarder; header layout/macros remain unreviewed dependencies.
Existing MAIN PI loader source/manifest and accepted aggregate are unchanged.
No opcode arrays, codestring padding, fake ABI or source from target bytes are
introduced. Source presence remains distinct from complete-file/exact credit.

Both final source cold rounds pass. Receipt:
`.analysis/th03-shared-pi/sol-shared-pi-source-20261006/receipt.json`, SHA256
`464ba04649e071f3f5a2a59f7c2fcbd703ac80f00c8fc615f82e5a960d7a026b`, 668 guards.
Each source image per round passes OP283 calls/279 returns/four prefixes or
MAINL451 calls/443 returns/eight prefixes, with all144/250 native positions.
There are1,786 ordered stores per artifact; callbacks are752 OP/14,784 MAINL.
Complete original raw/ordered carrier bytes, public/MAP coordinates, TC86
nondependency OMF records and declared SEGDEFs match. All four carriers retain
empty DATA/BSS contributions; their CODE lengths are173/70/135/177. They compile
with GAME3/large model, O for shared carriers and L for ending-specific ones.
No additional link-graph change is introduced beyond the preceding math change.

Both20-product/351-game-object vectors are deterministic; all417 OMF hashes
are recorded. All20products equal the preceding sound-loader proof and347
othergameobjects are unchanged. Nine nongame Research timestamp differences
per round remain separate; no417-object determinism claim. Whole OP six-byte/
MAINL21-byte and original relocation-order inequalities remain. Historical
MAINL shifted-carrier failures and unowned neighbor0529 remain separate.

OP now has29 reviewed decoded units/11,977 bytes and22 source-present
extents/11,610 bytes. MAINL retains145 rows,22 source-present extents/2,559
bytes in five shared CPP, two ending CPP and four ASM TUs. Five existing
MAINL rows gain source presence without new interval credit. Existing MAIN
accepted source/manifest remains unchanged; OP/MAINL exact acceptance stays0.

Current coverage receipt:
`.analysis/sol-current-decoded-coverage-after-shared-pi-20261006.json`, SHA256
`6cb884e6889f7743dad6ceb5d6b8df38b8bcdca6705d329aa1d7747c91ae9efb`,683guards.
OP100carriers/55,262bytes have11,977reviewed/43,285gaps; MAINL108carriers/
58,340bytes retain28,381reviewed/29,959gaps. Both have zero overlap.

This replay produced no failed preparation directories. Five unreferenced
successful preflight logs (10,051bytes) are removed after checking their
successful terminal status, ledger/proof references and protected paths.
All1,992 retained private input states are unchanged. Current diagnostics/
source/coverage, failed transcripts and complete cold receipt trees remain.
Cleanup receipt `.analysis/sol-pi-redundant-preflight-cleanup-20261006.json`,
SHA256 `f31cf94e9594617a2e535c45251f49cabcc31424fbe35f3e3724b18aa343d4a3`,three guards.
Historical missing/stale inputs are preserved without repair or rebasing.

Full CI passes581tests and all available private headless gates:
`.analysis/sol-shared-pi-complete-ci-20261006.log`, SHA256
`ff7fd223e52d6fa5b4721afea9e440f16e13b12d3ca6eb399860273ad1c65b7f`. Tracking:238units/2310evidence/288knowledge/120MAIN authored-function
rows. The505-file review/migration goal remains open; this bounded migration
adds no exact claim.
