# ZUN -3 maintained logo root producer

One fresh maintained-source compile and context link now reproduce the reviewed
logo root. This is source presence for ten existing root procedures, not ownership
of the complete payload or formal exact acceptance.

## Maintained source and actual build

`src/zun/zunsoft.cpp` is localized from frozen `th01/zunsoft.cpp` at revision
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`. Only the five include operands change
to explicit `compat/rec98/` forwarding. All declarations, procedure order, inline
assembly, control flow and integer widths remain unchanged. Four forwarders
already existed; the EGC forwarder is new. `scripts/stage_th03_zunsoft.py`
reproduces the seven-file source overlay deterministically and retains the
original `th01/zunsoft.cpp` translation-unit slot as a single include of its
maintained owner. It never compiles, links or supplies executable bytes.

The maintained source SHA-256 is
`5581a849a98d328e99c61abca772a3277f08cafd3e537ed1ed3a9b80728d8057`;
the reviewed frozen source SHA-256 is
`a2fd32b9213f89dbf582c36d48390f216666ca533f60cf2b3daa42d3d9984d98`.
The fresh build retains `-O -b- -3 -Z -d -DGAME=1 -mt` with the source
`#pragma option -2 -d-`. `GAME=1` is intentional: the frozen build selects the
TH01 tiny-model logo producer for TH03 option -3. Plain char remains signed.
Link order remains C0T, root, masters, emu, maths, ct. These vendor startup and
library inputs are explicit unowned context, not reconstructed producers.

The actual compile/link invocation completed on 2026-10-21 at 22:33:23 UTC
(Factory repository command `5525a4593a9f4518809e5072555cf8b0`). It produced a
4,133-byte OMF object, SHA-256
`845de18164def1d384eadc59be287a22ca47b99a6d4d989c0dfa407c094a08a5`,
and a 10,096-byte COM, SHA-256
`beeb86dc055c585a32f4500c9eabb2e6cb1e0537bcdbc5f3763ebefa4308e297`.
The latter equals the attested decoded target -3 payload with zero byte
differences. Equality of retained library contributions does not transfer their
ownership to this root.

## Bounded ownership and runtime

All ten existing `th03-zun-decoded-logo-*` unit coordinates remain unchanged:
inner CODE starts at `0367`, total size `0513` (1,299 bytes). The ten procedures
are graph_clear_both, zunsoft_init, zunsoft_exit, zunsoft_vector2, objects_setup,
circles_render_and_update, stars_render_and_update, wait, logo_render_and_update
and main. Root DATA is `21CE/000F`; root BSS is `2870/0125`. Initialized DATA
contains the filename and four colors; it is not additional CODE credit.
The genuine BSS wave_padding declaration is retained, not invented CODE padding.

Fifteen checks establish all 25 OMF publics and MAP correspondence, tiny model
segment/group ownership, private DATA coverage, CODE/DATA/BSS contribution sizes,
complete root bytes, decoded procedure boundaries, call destinations, near RETs
and the vector's Pascal RET8. No fake aliases or body padding are used. The
vector retains signed-word coordinates, signed-long products and arithmetic
right shift. Tone/pattern/wave byte promotions retain signed semantics.

The parent then ran the bounded model at 22:36:28–22:37:09 UTC (Factory command
`a54ed743a8ee46bdb55335e09d4c15ea`), with clean exit and all fifteen checks true.
Receipt: `.analysis/zunsoft-native-20261021-v02/parent-runtime-verification.json`.
This is one target and one fresh candidate, each with 1,300 modeled calls:
three complete root flows, 1,280 vectors, one circle-boundary case and sixteen
logo-stage cases. Combined count is 2,600, not the historical three-image 3,900.
Graphics/BFNT/memory/keyboard interfaces remain modeled; two real compiler
arithmetic helpers execute. CRT startup, actual assets, hardware input/display,
VSync timing and device restoration remain outside this model.

## Replay and progress

Run the source tests and the read-only retained proof replay:

```sh
python3 -m unittest discover -s tests -p test_zunsoft_stage.py -v
.venv/bin/python3 scripts/replay_th03_zunsoft_root.py
```

The proof is `config/zunsoft_root/proof.json`. Fast replay rechecks source
bindings, native completion, structural/raw results and the retained runtime
receipt; it does not invoke native tools or rerun the runtime matrix.

Exactly ten existing logo unit rows migrate from unknown/boundary-reviewed to
authored/source-present with owner `src/zun/zunsoft.cpp`. No new rows or packed
file offsets are introduced; the canonical file-offset column stays empty.
Combined with the three previously maintained wrapper extents, ZUN source
presence becomes 13 of 18 tracked units and 1,533 scoped CODE bytes. This is
neither a function denominator for the whole game nor a whole-payload percentage.
No DATA/BSS bytes are added to the CODE total. Formal exact count remains zero.
The initializer and sprite16 historical diagnostic annotations are unchanged.

The previous two-round cache paths cited by the historical review are absent in
this live repo. This fresh proof neither recreates nor relies on those receipts.
The original v01 verifier's ownership/binding defects were corrected in the
separate v02 verifier and preserved rather than overwritten. There was no native
retry: one compile and one link only, no independent second cold producer.

Still open: repeated cold builds, original library/runtime/data/asset ownership,
real hardware or independent emulator behavior, complete -3 ownership, launcher
integration, canonical stored DIET packaging and full acceptance Oracles.
