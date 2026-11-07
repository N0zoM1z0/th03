# Yumemi full GRCG triangle Bomb: physical 8.3 name and exact natural C++ (after687)

The complete original `bomb_yumemi.cpp` owns a **698-CODE-byte**
large single-function Bomber effect in `P_COMBO_TEXT`, including
two staggered GRCG triangles, 200-line-domain polar math,
GRCG/EGC clip setup, warning, sprite display and two palette
fade and shake phases. Real TC4 names the compiled producer
**`bomb~cxk`**, an eight-character 8.3 shortname. The original
99-project-object TLINK response instead records
`obj/th03/bomb_yumemi.obj`, and the original complete MAP
identifies the CODE/DATA/BSS module as
`src/main/player/bomb~cxk.cpp`.

The source-native v2 compiler and independent reviewer now
bind these *three distinct original physical identities*,
instead of mistakenly assuming the long source name is also
the compiler output file or original MAP name. The initial
failed stage `af687a` emitted `bomb~cxk.obj`, not
`bomb_yumemi.obj`; stage `af687b` then verified the
authentic current source/OMF dependency, 698 original CODE
bytes and entire linked MAIN image before any source edits.

The full GRCG/Bomb logic now uses native-original natural
C++ `frame * 4` and `frame * 8` palette shifts
(`af687c`), normal `++i` loops for both three-vertex
triangle groups (`af687d`), and
`static_cast<unsigned int>(frame) % 8 == 0` for
the warning/axis trigger (`af687e`). These changes
preserve the source's signed 16-bit polar Y **division
by two**, rather than wrongly using arithmetic shift
for negative odd Y values. The real early 32, 64 and
144 tick windows are compiler-time C++ phase names.
No new DATA/BSS or hidden target bytes were introduced.

A separate natural-looking unsigned `color % 4 < 2`
shake replacement changed the original native machine
code (`af687f`) and was rejected. The original
`color & 3` shake selection and all original short-circuit
control are retained.

Final real source/OMF-COMENT-attested original Turbo C++
4.02 compiler/TLINK pair:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af687g --units bomb~cxk
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af687g

Both rounds reproduce **all 698 original CODE bytes,
53 literal ordered OMF FIXUPP fields and one PUBLIC
offset**, complete original segments, complete normal
MAIN EXE and normalized MAP, original Japanese loaded
program, all 1,553 ordered MZ relocations and independent
full 130,882-byte original Japanese MAIN.EXE serialization.

Retained source and writer evidence:
`.analysis/work/exatt-layout-af687g/report.json`;
SHA-256 `1136eb46a313c86cd845b1a3463a60b73511e700973e74285caf9a183e592d74`.
Only this one original physical source object was compiled
in two rounds; 98 original project objects and startup/
CRT libraries were reused. No complete cold replay was run.

This recovers original-native C++ within already tracked
source-owned CODE, not additional Factory packed-file
accepted bytes or historical vendor raw OMF packet identity.
