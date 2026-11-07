# Kana full BOSS: staged-ring C++ updates and original native mode/timing (after638)

The maintained Kana BOSS source consists of the full original
1,874-CODE-byte, nine-function physical Turbo C++ object: four
substantial attacks, the large character update dispatcher and
multiple renderers. The original staged ring emits volleys at
different phases, including a separate 16-iteration symmetric
pellet expansion. Three new natural C++ expressions have been
proven independently to preserve the native code:

- In `kana_pattern_staged_ring()`, the original AL load/add/store
  for the rotating pellet angle now uses `bullet_template.angle += 6`.
  The adjacent AL speed increment similarly becomes
  `bullet_template.speed.v += 3`. Both update the same original
  byte fields in the same loop; actual original TC4.02 emitted
  identical instructions in independent tests `af638c` and
  `af638d`.
- In `kana_pattern_rotating_ring()`, the original `boss_frame & 3`
  interval check becomes `boss_frame % 4`, verified by `af638a`.
  The compile-time modulo lowers to the same native 16-bit mask.

The rotating direction setup remains the real four-branch
`-3/-1/+1/+3` AL assignment: an attempted one-line
`(randring_far_next16_and(3) * 2) - 3` would change original
machine code (`af638b`) despite yielding the same values.
Kana's cloud-ring `SUB AL,10h` remains authored inline assembly
because C++ lowering selects original-unequal ADD AL,F0.

The full scheduler's 18 real mode IDs and four attack phase maps
(acceleration ring, staged ring, cloud ring and rotating ring)
now have typed C++ names. The final hand audit corrected a
**semantic trap** in the first compiler-equal enum experiment:
same-valued constants representing a **PID subtraction, animation
mode, 0x40 angle or 0x10 loop count** are not frame boundaries and
must not be given the phase names. These now retain their original
distinct numeric meanings. Phase enums only label actual
`boss_frame` timing conditions. This matters for recovery quality
even though both variants compile to identical CODE.

Final original-source/OMF-dependency-bound dual native build:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af638f --units ba_kana
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af638f

Both genuine Turbo C++ 4.02/TLINK rounds match the complete
**1,874 original CODE bytes, 274 literal ordered native FIXUPP
fields, nine PUBLIC offsets**, all original object segments,
the full normal 99-object MAIN executable and path-normalized
MAP. The original Japanese loaded program and all **1,553 ordered
MZ relocations** remain identical; the separate standard MZ
serialization yields the complete 130,882-byte Japanese MAIN.EXE.

Native source-bound proof:
`.analysis/work/exatt-layout-af638f/report.json`,
SHA-256 `166f5cf8000ec8927757506c5bb1ed3463840274dc539cd860d06d4ebaf40535`.
Both compiler/linker source, OBJ, EXE/MAP vectors and real writer
logs are retained. Only the affected Kana source was rebuilt; no
full project cold replay or object-byte patching was performed.

These CODE bytes were already tracked. Neither the physical
original Borland OMF packet identities nor the provenance of the
full packed game/PC-98 hardware runtime are claimed by this proof.
