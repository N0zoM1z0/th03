# TH03 MAIN Mima: explicit trail-byte narrowing and natural hit truth test

Two small but compiler-sensitive parts of the complete Mima BOSS now use
more explicit C++ without changing the original physical object.

The trail controller computes its six-frame-dependent remainder from the
unsigned 16-bit BOSS clock, then narrows it to the original byte before
comparing the two phases:

    unsigned char remainder =
        static_cast<unsigned char>(boss_frame % mima_trail_interval);

The explicit cast documents the real width transition. It does not widen
the phase local or change the signed promotion in the later
mima_trail_interval / 2 comparison.

The main renderer's damaged-sprite branch now uses the natural byte truth
test:

    if(boss_hit) {

This is native-exact with the prior explicit nonzero comparison. The hit
branch still draws the damaged sprite and returns before all normal render
modes.

## Experiments and compiler boundaries

- af1000e moved the trail-mode check ahead of the particle label and jumped
  forward into the shared body. The complete BOSS CODE changed.
- af1000f removed the register qualifier from split_distance; complete CODE
  changed.
- af1001a moved pid_other's assignment into its declaration initializer;
  complete CODE changed.
- af1001b made the trail remainder's byte narrowing explicit with
  static_cast<unsigned char>; the complete BOSS object matched.
- af1001c changed boss_hit != 0 to if(boss_hit) on top of that cast; the
  complete BOSS object still matched.
- af1001d explicitly cast mima_trail_interval / 2 to unsigned char in both
  phase comparisons; complete CODE changed. Keep the original promoted
  interval expression.

## Complete original-object verification

The final af1001c stage rebuilt the complete ba_mima physical owner in two
independent original Turbo C++ 4.02 rounds, followed by two complete normal
MAIN links:

| Scope | Exact original result |
| --- | ---: |
| CODE | 1,922 bytes |
| Ordered OMF FIXUPPs | 277 |
| PUBLICs | 9 |
| Japanese MAIN loaded image | 124,642 bytes |
| Ordered MZ relocations | 1,553 |

The other 98 original game objects and Borland CRT were reused. Both
complete physical objects and both normal MAIN images/relocations match.

Reproduction:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1001c --units ba_mima

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af1001c

Protected report:
.analysis/work/exatt-layout-af1001c/report.json, SHA-256
4b7eaaa3c29f789db710be4ee69912f271644e60a766ae812bc25662c4073137
