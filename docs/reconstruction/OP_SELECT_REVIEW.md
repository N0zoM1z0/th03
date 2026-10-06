# OP character-selection carrier

The original decoded OP selection carrier is `0990:19F2..25B7`,3013bytes,
19complete near functions. Its first107bytes are the previously maintained
score loader. The remaining2906bytes/18functions are reviewed as one owner;
score/random/polar context is never credited again. These are decoded
observations from the pinned Japanese candidate-local-attested target, with
no invented stored-file offset or independent pristine provenance.

The frozen candidate is ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th03/op_sel.cpp` forwarding to
`th03/op/m_select.cpp`. The preceding Music Room cold trees include the
maintained107-byte loader, encoder and score-data wrappers. The review checks
that precise overlay instead of describing the entire cached source as frozen.

| Complete CODE scope | Offset | Bytes | Functions |
| --- | --- | --- | --- |
| Previous score loader |19F2|107|1|
| Unlock and three CDG loaders |1A5D|199|4|
| Initialize and free |1B24|207|2|
| Pictures, stats, names, extras |1BF3|461|5|
| Curve and animation |1DC0|486|2|
| Cursor and player update |1FA6|482|2|
| Versus, CPU and story menus |2188|1071|3|

The compiler MAP also observes DATA `0D7F:0A0E`,227bytes, and BSS
`0D7F:2462`,23bytes. Original DATA includes nine far filename pointers,
27stat bytes, two pairs of three-byte cursor strings, the persistent input
locks and filenames. Target/cold DATA bytes and original ordered relocation
rows are compared. BSS is a compiler contribution; the replay initializes
its state explicitly and does not invent file-backed target BSS acceptance.

Replay the diagnostic with:

```sh
env DISPLAY= WAYLAND_DISPLAY= python3 scripts/ghidra.py th03-op check
python3 scripts/review_th03_op_select.py --output .analysis/NEW_OP_SELECT.json
python3 -m unittest discover -s tests -p test_op_select_review.py
```

`SelectSpec` independently describes 16-bit scalar state, file formats,
curves and complete menus. `SelectProbe` executes original instructions for
all19functions, four other score functions394bytes, IRAND42 and POLAR26:
3475native bytes total,569bytes of previously reviewed context. The existing
independent `ScoreSpec` supplies the scalar score algorithm; native score
functions execute through real load/decode/check/recreate/encode callers.
Every instruction boundary, branch target, direct caller, near/far return,
Pascal cleanup, C caller cleanup, stack segment and saved BP/SI/DI/DS is checked.

All three public menus execute through normal confirmation/fadeout/free exits
and cancellation. Four IF/DF profiles additionally cover unlock/recreate,
all resource loaders, stat rows, signed/byte wrap, input release/held states,
confirm collisions and low16 curve products. Ordered native stores, callbacks,
port writes, explicit external clock/input/file writes and the entire physical
1MiB outside the64KiB stack are compared. Plot callbacks retain every point
in the ordered-event digest; notes retain nonpoint callbacks. Gaiji color is
byte-wide; its unspecified upper argument byte is excluded from scalar color
semantics, with full original caller instructions still compared unchanged.

The input callback is an actual stored four-byte far pointer despite the
candidate typedef name. Three indirect sites at2240/237D/24E8 must read246E;
the dynamic pointer must name exactly one of AD6/AFA/B04/B26 in segment0BEB.
No unknown edge is inferred from a callback result. Unicorn1.0.2rc4 read hooks
change original RETF behavior, as independently recorded in the Music Room
control. This probe installs no memory-read hook and executes original returns.

Observed behavior retained in the natural source:

- A later failed score load returns seven characters even after an earlier
  cleared rank selected nine. Missing or invalid data invokes real recreation.
- Initialization preserves the input locks, curve cycle and confirmation
  fields. Its counter reaches30 and remains there; the first subsequent wait
  can reduce the trail count from8 to7 without an intervening counter reset.
- Up, down, Shot and Bomb are independent tests in that order. Shot and Bomb
  both execute when both bits are set, even after Shot has marked confirmation.
- Other-player confirmation enables palette collision adjustment and resets
  the fade counter. Shot increments the colliding palette byte; Bomb decrements.
- Curve angle addition wraps to8bits, multiplication wraps to signed16, division
  by256 truncates toward zero, and the quotient wraps to8bits. Trail reduction
  is adaptive. No fixed4096-point or CPU-cycle claim is imported.
- Cancel is checked after updates. Normal fadeout writes the tone before its
  frame>32 exit; frame33 produces tone2. CPU mode advances after P1 frame13
  without performing that iteration's flip. Free releases slots0..21.

Clock changes occur only at four attested polling sites using explicit counter
sequences. File data and input words are fixture writes; graphics, BFNT, CDG,
sound and palette callbacks preserve flat memory. No actual banking, assets,
ROM, DOS, sound, IRQ/ISR timing or hardware liveness is accepted. The complete
Oracle set, header/library/CRT ownership, canonical packing and whole OP build
remain open. The curves351 and versus407 functions have identical raw bytes but different
original relocation order. These two failures are recorded without sorting
or normalization. Prior whole OP six raw-byte and original relocation-order failures
are retained even when the reviewed Select extent matches.

The original relocation order is retained literally. In curves351 the target
order is1E7F,1F98,1F32,1EB9; the compiler order is1F98,1F32,1EB9,1E7F.
Versus407 has fourteen rows with a different starting position. This does not
identify a producer or packing cause; canonical storage/producer investigation
remains open. Identical relocation multisets grant no ordered equality.

A separate frozen-source compiler probe, `scripts/probe_th03_op_select_layout.py`,
removes only `padding_1` and `padding_2`. The original OMF BSS SEGDEF is23bytes;
without the declarations it is21bytes, with different producer records. These
are explicit candidate allocations, not natural compiler alignment. The
maintained owner therefore uses `src/op/menu/character_selection.inl`; its
2906bytes/18functions compile under a private, unowned DATA/BSS prefix and the
previous107-byte loader. The prefix is routed through19explicit compatibility
forwarders, four newly added. Neither candidate padding declaration is placed
in product source or granted ABI/layout ownership.

Diagnostic receipt: `.analysis/sol-op-select-review-20261006.json`, SHA256
`7e8d58a346b49abfefe74b976aa86efc5728a509a858dc5096fbd50def39c722`,325guarded inputs.
Original and both preceding Music Room cold OP images each440cases/all1239
positions pass, with839925native entries,69761ordered stores and429541foreign/
port events per image. The two perfunction ordered relocation failures remain.
Thirteen focused controls pass, including a floor-division mutation that fails
on negative wrapped curve products.

Frozen-layout receipt: `.analysis/th03-op-select-layout/sol-select-alignment-20261006-d/receipt.json`,
SHA256 `e8b71faf1ba9fb6ce004444697c7f3caa71904fc213469ef618a0f39a34ed09c`. The earlier preparation
compiler invocation escaped the character macro incorrectly; the corrected
frozen-source probe supplies the compiler observation above. No result is
inferred from that failed invocation.

The bounded owner is now source-present. Replay with
`python3 scripts/replay_th03_op_select.py --run-id NEW_OP_SELECT`. Two fresh
frozen trees each build20products/350gameobjects, recording all416normalized
OMF outputs. Both product vectors equal the preceding Music Room proof and
each other. Each new OP reruns112selectedcases/all1239positions, with449246
native entries,19392stores and230779orderedforeign/portevents. Previous
entry/menu/title/Music/score raw and ordered results are retained without
repeating their unchanged old matrices.

Source receipt: `.analysis/th03-op-select/sol-op-select-source-20261006/receipt.json`,
SHA256 `885ecb011fd829c9da2d1272f2f571415f49e0ec71303ec9ec9e4b8d5c06b0b2`,333guarded inputs. Complete3013-byte carrier
and2906-byte remaining-owner raw slices match; both aggregate original ordered
relocation lists fail, together with the curves/versus perfunction failures.
DATA227raw/originalorder matches remain diagnostic. Whole OP still differs in
six raw bytes and its original relocation order. No producer or canonical
packing cause is inferred. OP now has13source-present extents/9523bytes in
three CPP TUs and six bounded inls;9890decoded bytes reviewed,exact0.

After both writers completed, guarded cleanup retired7128files/71733816bytes
of unreferenced failed/superseded layout preparations and temporary outputs.
The full-CPP draft was discarded; its unproved padding declarations were never
admitted to product source. Current frozen-layout/source/target/toolchain/DB
proofs survive, all1843retained input states match across deletion, and the
meaningful first compiler macro-escaping failure is kept verbatim. Cleanup
receipt `.analysis/sol-op-select-temporary-cleanup-20261006.json`, SHA256
`5712b574d06d817102fcd9b3c579053c6ddce4a37f089fe59e85968f4baa88de`; the separate retained-state audit records the hash/missing map
atcleanup time. See `ANALYSIS_CLEANUP.md`.

Final verification:508tests/all available private headless gates pass in
`.analysis/sol-op-select-complete-ci-20261006.log`, SHA256
`820559d9aafa23df8bdb24ba926bfa80abef31a546b0d78be267079d8d945e34`. `git diff --check` passes.
MAIN/MAINL/ZUN acceptance is unchanged. The505-file intake remains open; this
is complete bounded Select CODE review/source presence, not a whole OP build
or a complete header/DATA/BSS/CRT/runtime/canonical-packing Oracle result.
