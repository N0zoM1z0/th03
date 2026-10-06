# OP main and option menu review

Reference revision: `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
Targets are Japanese YUMEZIKU, `candidate-local-attested`; independent pristine
dump attestation remains unknown. Target facts, compiler results, native reply
fixtures and inference remain separate.

The frozen `th03/op_01.cpp` candidate supplies five contiguous complete
functions at decoded `0990:05DD..0B17`: main drawing122, option drawing330,
selection movement63, main update291 and option update532 bytes. The1338-byte
extent includes two zero producer bytes and20 bytes of original switch tables.
All438 native instruction positions are exercised. Tables are checked as data,
including each destination's instruction boundary; they are never disassembled
as code or replaced by authored padding.

`src/op/menu/menu_state.inl` preserves the natural strings, initialized and
uninitialized menu state, near Pascal drawing callback, byte selection and
`-a2` pragma in the original private OP entry carrier. The manifest hashes the
original bounded span; the remainder of the carrier provides the enums,
`choice_tram_y()`, declarations and reference context. This include is source
present, without maintained ownership of that context, other screen callers,
startup, configuration, library/header/DATA/BSS or whole product. Its label
bytes are compared diagnostically; no additional DATA unit is credited.

## Target and compiler observations

Receipt: `.analysis/sol-op-menu-review-20261006.json`; SHA-256
`59dbc2a77717c8fc72f4702514db6cdd777cdec9ccc36b17548d6615be70baa6`; 113 guarded inputs.

Three images (original DIET restoration and two previous OP-only cold images)
each pass4160 cases,4544 top-level terminal calls,15800 native entries and
14528 ordered native stores. The complete1338-byte raw slices and original ordered
relocation observations agree at unchanged addresses. Fourteen frozen provider
files, original OP entry OMF producer and3094-byte MAP carrier are bound. The
selected canonical packed OP Ghidra database was re-attested before review;
its automatic functions provide no authored or independent Oracle credit.

Receipt: `.analysis/th03-op-menu/sol-op-menu-source-20261006/receipt.json`; SHA-256
`088915e25bf97951160b090e9d4a2d5ea5c139731aa903031b0fdc1a944c5344`; 117 guarded inputs.

Two new frozen archives independently compile the maintained menu include,
previous1309 score/title source bytes and explicitly declared carrier overlays.
Each OP passes4160 menu cases plus96 title cases. Previous543 score/helper
bytes are checked raw and in original relocation order; the previous1168-call
score proof is retained without claiming a new run. Twenty products and350
game object hashes agree between rounds; all416 normalized OMF outputs are
recorded. These are compiler scaffolds, with the whole OP image still unequal
at six raw bytes and in original relocation order. Canonical storage is packed;
there is no invented stored-file offset or exact promotion.

## Independent native contract fixtures

The scalar model compares ordered native stores, renderer/API events, native
entry counts, external fixture writes and all physical memory outside the
64KiB stack. Native callbacks execute their real renderer bodies. Each caller,
near/far frame, Pascal cleanup, saved BP/SI/DI/DS and stack segment is checked,
including the Music Room `NOP; PUSH CS; CALL near` far-return convention.
Callback pointers must select one of the two native drawing entries.

The256 combinations of up/down/left/right/shot/cancel/OK/unknown input are
exercised for every normal menu selection. Additional cases cover held-input
sequences, release gates, initialization, IF/DF, signed selection overflow,
invalid option fields, disabled sound, raw driver replies, arbitrary Pascal
attributes, both drawing functions and callback direction/range extremes.
Eight controls include table operand mutations, invalid callback, native store
changes and exhausted instruction budget. Assertions compare semantics rather
than merely reproducing the source text.

Observed caller behavior includes:

- A menu initializes its input gate tofalse, then unlocks on a zero input word.
  A held nonzero input is consumed once and locked until release. The original
  entry's pre-loop reset/first call remains unreviewed caller context here.
- Up and down execute in that order; right and left execute in that order.
  Simultaneous music directions can stop, determine, play, then stop again.
  Enabled music toggles also perform an extra option redraw before the common
  redraw. Disabled sound still reaches the common redraw.
- Right increments option bytes modulo256 before the upper-bound comparison;
  left sets the maximum only when initially zero, otherwise decrements.
  Invalid option field values are retained as native diagnostic inputs.
- Story, VS and Music Room return through the common fade/wait/CDG callback
  sequence and early return, bypassing the later cancel test. VS writes both
  character fields to1. Score returns to the remaining cancel/input checks.
- Option confirmation exits only on selection3. Cancel always exits; a
  simultaneous confirmation/cancel can perform the exit stores twice.
  Returning sets main selection4 and clears option state.

Text rendering, animations, other screen functions and sound driver behavior
use explicit finite reply fixtures. Sound determination injects a chosen active
byte; screen callbacks inject a chosen input word. Their writes are recorded
separately from native stores. No fixture establishes actual DOS execution,
character selection, music resources, heap lifetime, device behavior, interrupt
liveness, startup held-key behavior or complete original caller closure.

## Acceptance and remaining work

One new source-present owner1338 bytes brings OP to2647 maintained decoded
bytes in two C++ TUs and three bounded includes. OP reviewed decoded coverage
is3255 bytes in14 units. OP exact remains0. MAIN, MAINL and ZUN acceptance is
unchanged. The entry carrier still has1485 unreviewed bytes beyond the earlier
271 configuration bytes and this menu extent: story/VS/demo/wait/score/startup
callers. Character selection, Music Room, root/header/DATA/BSS/resources and
the complete505-file intake remain open.

Full verification: `.analysis/sol-op-menu-complete-ci-20261006.log`, SHA-256
`c630c05aaeeace535ee5d202121b3d6fbb216a082f34062262813808e88c139d`, passes462 tests and all available private headless gates. The initial CI
progress-snapshot failure is preserved in the evidence ledger; the generated
snapshot was refreshed before the complete passing rerun.
