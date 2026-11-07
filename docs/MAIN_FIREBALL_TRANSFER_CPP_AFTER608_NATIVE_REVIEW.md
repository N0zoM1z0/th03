# Fireball falling/transfer state machine: natural C++ control flow after608

The full real `src/main/enemy/fireball.cpp` is an original physical producer
that includes fireball creation, collision, hit/explosion, rendering and the
large `fireballs_update` state machine. This refresh removes two manual
jump labels from that state machine without changing the original effects:

- In `FF_FALL`, the out-of-bounds Y test directly assigns `EFF_FREE` and
  `continue`s instead of jumping backwards to `free_and_continue`.
  The earlier X/bomb-flag free path still has its own identical release
  and frame-loop continue. The code does **not** add an unoriginal
  defensive check or suppress the original update.
- In `FF_TRANSFER`, a single C++ conditional now expresses the actual
  playfield-specific crossing: P1 reaches its destination when the
  translated X position is at/above the target, while the other player
  reaches it when at/below the target. The former `switch_to_fall`
  label and transfer-branch `goto` are gone; the same six state writes
  and `continue` implement the transition from horizontal transfer to
  vertical falling.

These changes were not accepted merely because they look equivalent.
Real 16-bit Turbo C++ 4.02 compiled the full physical object twice and
the actual original TLINK relinked the complete MAIN into an exact
source-native program and map. Source-only compiler experiments
`af607f` (FALL) and `af608a` (TRANSFER) passed independently. The
post-formatting `af608c` version is the current source-bound proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af608c --units e_fireb
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af608c

For both rounds, the source-compiled object's **1,555 original CODE bytes,
1 initialized DATA byte, 1 BSS byte, 115 ordered native FIXUPP fields,
10 PUBLIC offsets, and complete segment definitions** are original-equal.
Both normal full TLINK EXE files and normalized complete MAPs agree with the
frozen source-native after596 baseline; the Japanese MAIN loaded image and
all 1,553 ordered relocations match. The separate standard DOS MZ
serialization reproduces the 130,882-byte original Japanese file.

Retained evidence:
`.analysis/work/exatt-layout-af608c/report.json` SHA-256
`942b8b3bc4a061ff48c6b2bb85948631e7e64153374a5551de5153f2ec163a39`.
The `af608b` seven-owner control also verified the updated Fireball,
Enemy, Explosion and Bullet sources simultaneously in two native rounds
(8,195 CODE bytes, 582 ordered fixup fields and one Fireball initialized
DATA byte). All native input overlays, logs, objects, EXEs, maps and
source-bound receipt hashes are retained; no cold replay or target object
patch was used.

No claim of historical raw vendor OMF packet byte identity, new packed
Factory credit, or untested PC-98 runtime behavior is made. All 1,555 CODE
bytes were already tracked as an original source scope; the improvement
is the actual C++ expression and native build reproducibility.
