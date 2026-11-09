# TH03 MAIN — Chiyuri BOSS frame clocks, ring cadence and render state (af1119b)

The complete original `ba_chiyu` physical Turbo C++ 4.02 owner includes its
four attack families, entire launch/collision controller, sixteen-sprite
ring/intro rendering, main sprite mode dispatch, monochrome rendering and
native template. This is an entire BOSS, not an isolated leaf. The global
unsigned-word frame counter now uses natural prefix increment. The eight-frame
trail warning and four-frame shared render clock use unsigned-word remainders
rather than equivalent bitmasks. The distinct byte render-frame mask remains:
replacing *that* mask with `%4` is not an equivalent native compiler operation.

The sixteen-sprite orbit renderer uses natural prefix progression of its signed
index with its separate byte-angle assignment. Main sprite rendering now
expresses the palette-mode check as a separate `if` after the original normal
rendering branch returns; the mono color threshold chain remains intact.

`af1119a` verified the word clocks and sprite progression, and final `af1119b`
verified the main renderer branch. Both stages passed two independently
compiled original TC4/full normal MAIN TLINK rounds, matching 2,654 original
CODE bytes, 381 ordered native fields, 11 PUBLICs, the full Japanese MAIN
loaded image and all 1,553 MZ relocations. Final current source evidence is
`.analysis/work/exatt-layout-af1119b/report.json`.

The independent `af1119c` candidate also flattened an `else if` in the
cardinal attack. Although its frame guards cannot both be true, the real
compiler emitted different CODE; the original branch relation was restored.
No canonical Factory packed-product credit is implied by these local proofs.
