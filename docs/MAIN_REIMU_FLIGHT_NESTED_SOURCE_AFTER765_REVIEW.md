# TH03 MAIN Reimu Extra Attack shared flight and update: original-native after765

The historical original Reimu Extra Attack is **two distinct physical
Turbo C++ translation units** whose maintained C++ implementation
functions live in three separately included `.inl` bodies:

- `ex_rfly` (complete original **825 CODE bytes**, 51 ordered OMF
  FIXUPPs, **8 PUBLICs**) includes `src/main/player/exatt_flight.inl`
  (shared flight/update helpers) and
  `src/main/player/exatt_reimu_prefix.inl` (Reimu creation, special
  Extra Attack, sprite state render and collision stripes).
- `ex_reup` (complete original **331 CODE bytes**, 22 ordered OMF
  FIXUPPs, **2 PUBLICs**) owns the actual separate
  `src/main/player/exatt_reimu_update.inl` entity update and renderer.
  Its update-only compiler wrapper excludes the prefix implementation.

These are not independent artificial function snippets. Both original
physical units were genuine TC4-compiled and full-MAIN-linked in every
accepted round, with the original 32-byte entity storage and bitwidths.

## Newly closed actual source-provenance loophole

Previous source-native receipts for these two original objects included
the maintained `exatt_flight_reimu.cpp`/`exatt_reimu.cpp` root wrapper,
but did **not** force the current **three actual `.inl` implementations**.
The Turbo C++ include lookup could therefore silently fall back to an
older WORK/src implementation despite a newly edited product source.
The scoped source compiler and independent read-only reviewer now
**version the dependency contract**: historical stages before after765
retain their genuine older scope; from after765 onward `ex_rfly`
requires both flight and prefix `.inl` source snapshots and `ex_reup`
requires the update `.inl`, all with real compiler-emitted OMF COMENT
records naming the staged implementation paths. The original update-only
wrapper's uncompiled prefix is **not** falsely counted as an additional
update-object dependency.

Three new targeted regression tests in
`tests/test_main_source_overlay_inline_contract.py` assert the actual
legacy/current source set, the required stage-local roots, and the
correct physically separate update-only include. Historical native
writer receipts were never rewritten or repinned.

## Natural original-native C++ recovery

The flight owner now names original byte lifecycle states:
active 1, flying 2, and appearing 3. Its original signed boundary tests
and `goto moving/arrived` control flow remain preserved, with the
original near `exatt_fly_update()` result, unsigned PID truth test,
original player transfer and 16-bit velocity initializer unchanged.
The prefix's two original eight-entity slot allocators and their
pointer postincrements now use naturally signed local `++i`, with
original field access and RNG draw sequence intact. The 8-slot update
and render owner also uses natural `++i`, free-state Boolean checks,
explicit flying/active state names, and natural `if(exatt_fly_update())`
while retaining original collision, sprite and random angle ordering.

Actual negative codegen experiments **were not accepted**:

- `af765c` combined two seemingly equivalent unary-negation forms
  `p->velocity_{x,y} = -p->velocity_{x,y}` for the original mutable
  16-bit `*= -1` reflection; actual `ex_reup` CODE changed.
- `af765e` isolated just the horizontal `x` replacement and failed.
- `af765f` isolated just the vertical `y` replacement and failed.
  Both original compound signed mutations were restored; no gameplay
  behavior was fixed or approximated to obtain native equality.

The unchanged-source expanded-input baseline `af765a` passed, then
changed source `af765b` passed, and the final current maintained source
with explicit negative-control notes was genuinely recompiled and linked
in two independent original TC4 4.02 rounds at `af765g`:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af765g --units ex_rfly,ex_reup
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af765g

Both rounds reproduce **1,156 complete original CODE bytes, 73 literal
ordered original OMF FIXUPP fields, 10 PUBLICs**, all segment/ABI
contracts and actual maintained implementation source dependencies.
The full normal 99-project-object MAIN EXE/MAP, Japanese 124,642-byte
loaded game and all 1,553 MZ relocations match, with independently
serialized original Japanese 130,882-byte MAIN.EXE. The remaining
97 original project objects and Borland CRT were reused, not rebuilt.

Primary current-source proof:
`.analysis/work/exatt-layout-af765g/report.json`, SHA-256
`d4b3deed7f1f1a41add74a0628771a6dceca549db3a9b173e0f77ab13ae2e933`.
Actual negative writer evidence and two full original compiler/linker
rounds are retained in protected ignored work. This is stronger real
current-source codegen/ABI provenance, **not** additional canonical
Factory packed-file acceptance, raw original vendor OMF identity or
whole-game source ownership.
