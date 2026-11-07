# Yumemi major BOSS pattern state machine: natural C++ modes (after628)

The complete Yumemi BOSS original Turbo C++ translation unit contains
ten functions / **2,358 CODE bytes**, including the long attack-mode
dispatcher, ring, aimed/random, crossed-ring, chase, rain and intro
renderers. It is a large gameplay controller, not a leaf-only edit.

The rotating ring pattern previously authored two separate branches
solely to assign the signed starting angle step through the AL
register. Its current source uses the natural C++ conditional
expression:

    _AL = ((randring_far_next16_and(1) == 0) ? 3 : -3);
    yumemi_angle_delta = _AL;

Real TC4.02 optimizes this to the identical original register
instructions; the separate source-rooted `af628a` probe passed complete
original CODE/OMF field equality. A tempting `boss_frame << 7`
replacement for the renderer's two sequential left shifts failed native
comparison (`af628b`), and is **not** included.

The large `gba_boss_update_yumemi` dispatch now names each of the
18 possible attack-mode values according to the actual patterns used
by Yumemi. This does not infer a new random distribution: the shared
scheduler still selects the same 2..17 modes. The intro, pattern
selection, descending and explosion values are explicitly identified.
The ring pattern's initialize, warning, fire and finishing phases are
also named as genuine compile-time C++ enum constants, not extra state
or new data. These names make the existing byte-for-byte-verified
control flow and timing independently readable.

The successful `af628e` test introduced the dispatch values; final
`af628f` also names the ring phases. Both tests compiled the *actual*
current source under the corrected v2 native path (with attested
OMF COMENT dependencies), in two original TC4/TLINK rounds:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af628f --units ba_yumem
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af628f

Both rounds preserve all **2,358 CODE bytes, 343 literal ordered native
FIXUPP fields and ten PUBLICs**, plus the original segment definitions,
full normal MAIN link and path-normalized MAP. All 1,553 ordered
Japanese target relocations, the complete program image and the
separately serialized 130,882-byte original MAIN.EXE match.

Retained proof:
`.analysis/work/exatt-layout-af628f/report.json`, SHA-256
`80ddcd9238444e32b4deaac61984d23d381b70f943986a85976c4c8d14c28f47`.
Both actual source and native OBJ/EXE/MAP compiler/linker rounds are
preserved. This is verified maintainable C++ source recovery for
previously owned bytes, not additional packed Factory credit, original
historic vendor OMF packet identity or runtime/device validation.
