# Mima orbit/spread/bomb cadence from original-native C++ modulo (after633)

Three separate Mima BOSS attack routines now express their firing
frequency as natural unsigned C++ remainders, instead of bit-mask
tests that hide the intended tick interval.

- `mima_pattern_orbit`: `boss_frame % 2 == 0` fires on even
  ticks and advances the signed orbit angle (separate `af633a`
  control).
- `mima_pattern_spread`: the same 2-frame cadence gates bullet
  pairs, short-range pellet groups, animation toggles and incremental
  angle writes. The original per-hit and duration decisions remain
  independent of cadence.
- `mima_pattern_bomb_random`: `boss_frame % 4 == 0` emits
  periodic random pellets and bullets; the separate even-tick sound
  still occurs every two frames. Both conditions lower to the exact
  original mask/test instructions.

The current source uses original `boss_frame` unsigned 16-bit
semantics, so the power-of-two modulo is naturally optimized by
Turbo C++ 4.02 to the original instruction bytes. Source/OMF input
attestation, not an ignored overlay copy, binds the compiler to
the actual edited C++:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af633b --units ba_mima
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af633b

Both fresh original Turbo C++/TLINK rounds reproduce the entire
original **1,922 CODE bytes, 277 literal ordered FIXUPP fields and
nine PUBLIC offsets**, all OMF segments, complete normal MAIN EXE
and path-normalized MAP. The Japanese loaded program, its 1,553
literal MZ relocations and the separately serialized exact
130,882-byte original Japanese MAIN.EXE remain equal.

Retained native report:
`.analysis/work/exatt-layout-af633b/report.json` —
SHA-256 `25a6afe669304d8eb3643f03a49565f6f2085227cb46df2443785e47060c6d57`.
The earlier `af633a` native source control covers the orbit
helper alone. Other original game objects were reused, with no
full cold replay, source masking, object patching or canonical
packed-file credit upgrade.

This is a natural C++ source/ABI improvement within already
tracked original CODE, not proof of historical vendor OMF packets,
whole-product Factory acceptance or device behavior.
