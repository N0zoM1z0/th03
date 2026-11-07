# TH03 MAIN static HUD: first complete source-native original object after723

The originally linked physical `hud_stat` module is a **seven-function,
539-byte complete original CODE owner**, not part of the `intro` particle
animation object. Original functions implement the full TRAM wipe, both
players' half-hearts, bombs, rounds won, single-player story lives, gauge
levels and final per-player HUD dispatcher. Original Japanese object metadata
contains **one 539-byte HUD_STAT_TEXT CODE segment, zero-sized DATA/BSS,
18 literal ordered native OMF FIXUPP fields and 7 PUBLIC offsets**.

The maintained `src/main/hud/static.cpp` was made a real independent original
TC4 source producer by extending the current scoped source compiler with the
**actual** original `obj/th03/hud_stat.obj` linker slot, three original MAP
rows, current-maintained source OMF COMENT dependency and original segment
name. This is not new padding or an assembly-byte copy.

## Original OMF provenance recovered, not guessed

- The first attempted source compile `af723a` produced **all 539 exact
  original CODE bytes** and all 18 relocation *sites*, but our attempted
  `#pragma option -zCHUD_STAT_TEXT -zPmain_01` was an **incorrect** OMF
  group definition. The compiler attached PUBLICs to group index 1 instead
  of original group index 0, and seven fixup frames referenced group index
  2 rather than original segment index 1. `af723a` is therefore a failed
  native trial **despite perfect CODE bytes**.
- The corrected source uses **only** `#pragma option -zCHUD_STAT_TEXT`.
  The actual original linker's `MAIN_01` placement is retained without
  falsely declaring an original per-object OMF group. Both rounds of
  corrected `af723b` now matched every CODE, segment, literal fixup and
  PUBLIC field and the original whole normal MAIN/MAP.
- After resolving OMF ownership, three signed `while` loop counters and
  the two-player dispatcher `for` counter were recovered as natural
  `++i`. The half-heart stride remains `i += 2` and sprite call/position
  order remains unchanged. Both **modified-source** rounds of `af723c`
  stayed fully native-exact, independent of the earlier OMF-only control.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af723c --units hud_stat
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af723c

Both genuine original TC4 4.02 / TLINK rounds matched all **539 CODE bytes,
18 literal ordered FIXUPP fields, 7 PUBLICs**, exact segment metadata,
full normal MAIN EXE/MAP, original 124,642-byte Japanese loaded program,
all 1,553 original ordered MZ relocations and complete 130,882-byte Japanese
file after independent standard MZ serialization. Only the single affected
`hud_stat` object was recompiled; 98 other project objects and original
CRT were reused. No full cold replay or object/target byte patching.

Independent current-source receipt:
`.analysis/work/exatt-layout-af723c/report.json`, SHA-256
`7b4d3244e111dfe25890d51c1e121671fb4827cf55a8b66f2b03f513845c94ba`.
Both independent native writer rounds preserve original COMENT source
bindings, compiler logs, OBJ/EXE/MAP, response files and source snapshots.
This is **new current-scoped direct physical-source proof**, not canonical
Factory packed-file accepted code, old vendor raw OMF packet identity or
whole-product source ownership. The negative OMF group trial is retained
and not counted as success.
