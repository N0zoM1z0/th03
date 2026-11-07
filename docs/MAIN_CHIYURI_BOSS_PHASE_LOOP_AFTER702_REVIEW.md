# Chiyuri complete BOSS: native four-fan and ring loops / big update phases (after702)

This is a fresh original-compiler proof for the complete
eleven-function 2,654-CODE-byte Chiyuri major BOSS physical
source: the main frame/mode/collision dispatcher, four-pass
horizontal/vertical fan emitter, cardinal/ring/trail
attack families and actual animated sprite renderers.

## Original-codegen-equal natural C++ updates

All **four distinct** fan emission loops use natural
`++i` instead of `i++`. Both ascending and
descending horizontal and vertical speed passes
retain the original exact per-bullet angular and
signed subpixel geometry. The 16-sprite ring
renderer also uses the natural `++i` part of
its angle-advancing loop. The full physical BOSS
object remained original-native exact (af702c).

Inside the long `gba_boss_update_chiyuri`, both
palette-phase nonzero checks now use ordinary
`if(boss_move_phase)`, and the render-state
countdown uses ordinary `if(boss_render_mode)`.
These preserve exactly the original short-circuit
and original 8-bit field behavior under real
original Turbo C++ 4.02 (af702b).

Two deliberately challenged equal-looking rewrites
**changed original native CODE** and were rejected:
- The mutable 8-bit render frame update
  `boss_render_frame &= 3` cannot be replaced
  with `boss_render_frame %= 4` (af702a).
- The palette byte countdown `boss_move_phase--`
  cannot be changed into `--boss_move_phase`
  (af702d) without different compiler instructions.

Both original forms remain in the final product
source. No code padding, binary original-byte copies,
extra DATA/BSS, unconditional branches or
runtime defensive fixes were introduced.

## Actual original native proof

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af702e --units ba_chiyu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af702e

Both independent source/packed-BOSS-header-OMF-COMENT-attested
original Turbo C++ 4.02 and whole normal MAIN
TLINK rounds reproduce **all 2,654 original CODE
bytes, 381 literal ordered FIXUPP fields,
eleven PUBLIC offsets**, complete original
OMF segment and native 16-bit calling ABI,
complete normal MAIN EXE and normalized
MAP, Japanese loaded program, 1,553
ordered MZ relocations and independently
serialized original 130,882-byte Japanese MAIN.EXE.

Preserved real modified-source and writer proof:
`.analysis/work/exatt-layout-af702e/report.json`,
SHA-256 `5c2d7f5f23623c1909f1df8036381936c363153b219644446a64a8085a1bd198`.
Only this one changed physical original BOSS TU
was rebuilt twice, leaving all 98 other
original project objects and CRT libraries
reused unchanged. No whole cold replay.

All CODE bytes were already source-owned;
this is original-native C++ progress rather
than new canonical packed-game Factory
accepted CODE, historical raw vendor OMF
packet-byte identity or PC-98 runtime proof.
