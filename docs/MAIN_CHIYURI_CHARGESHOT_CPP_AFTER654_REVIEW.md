# Chiyuri complete charged-shot and Gauge original-native source (after654)

The complete nine-function physical cs_chiyu translation unit owns 1,011
original CODE bytes: shot reset, eight staggered projectile creation,
reverse-order update, per-shot sprite rendering, collision, and Gauge
attack. This is not a small extracted fragment.

Three actual changed-source native Turbo C++ tests independently pass:
- af654b: sprite flicker uses explicitly unsigned % 2 instead of bitwise
  parity, preserving exact original code.
- af654c: the Gauge attack odd-frame bullet gate uses the same typed
  unsigned remainder, still preserving all original bullet order.
- af654d: the staggered initial ages are naturally i * 4 + 2 rather
  than an authored left shift; TC4 generates the original instructions.

The full physical projectile stride is 6 bytes, center at offset +02,
with eight slots per player and sixteen across both players. These size
and offset assertions are checked by the original 16-bit compiler.
The Gauge timing record also has a checked four-byte size. Update,
hitbox and render traverse slots 7..0 in original descending order.

IMPORTANT original behavior: chargeshots_reset_chiyuri loops 16 times but
does NOT advance its pointer, therefore repeatedly clearing only the
first physical slot. This is preserved deliberately, not corrected
as an apparent bug. The asymmetric hitbox clipping conditions, age
transitions and original sound effects are also unchanged.

Fresh two-round original TC4.02/TLINK proof:
    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af654e --units cs_chiyu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af654e

Both native object rounds reproduce ALL 1,011 CODE bytes, 96 literal
ordered FIXUPP fields, 9 PUBLIC offsets, complete OMF segment definitions,
full normal MAIN executable and normalized MAP, 1,553 literal ordered
Japanese original relocations and the independent 130,882-byte Japanese
MAIN.EXE MZ serialization.

Retained original-source and native evidence:
.analysis/work/exatt-layout-af654e/report.json
SHA-256 bc151f38fa88fd0fb0b08086d2eae76814570d8087c773b39be1f8c7c1946eb8.
Actual OMF COMENT dependencies attest the compiler-consumed current source.
The original other 98 objects plus C0/CRT were reused, not cold replayed.

These are already tracked game CODE bytes, not new canonical packed-game
Factory credit, raw historic vendor OMF packet identity, or physical
PC-98 gameplay proof.
