# TH03 MAIN after845: Reimu whole major BOSS signed/unsigned frame recovery

The complete original physical `ba_reimu` source is one **2,020-CODE-byte
major BOSS** with cloud, multiple spreads, three-phase orbit-burst,
mirrored volleys, full collision/update, normal 6-orb sprite renderer
and eight-sprite entrance renderer. Current maintained C++ source was
compiled as a whole through original Turbo C++ 4.02, not as a sidecar.

The **unsigned 16-bit** `boss_frame` now directly expresses two original
attack clocks as natural C++ remainder: `%2 == 0` accelerates the orbit
cloud, and `%16 != 0` gates the mirrored four-way spread. Full original
circle radius, byte-angle frame-step and the mirrored second volley angle
now have explicit physical names; the launch of paired bullets and
original RNG call sequence remain unchanged. Both 16-bit/byte-sized
renderers use the same named original **four-frame cel division** and
initial 0xC80 entrance radius, but deliberately retain the two subsequent
**byte-valued `anim & 3`** masks for original TC4 lowering.

Real original compiler trials:

- `af845a`: both signedly relevant unsigned *word* clocks `%2/%16`
  pass exact CODE and complete native MAIN/TLINK in both rounds.
- `af845b`: replacing **all four 8-bit renderer `anim & 3` uses**
  with `anim % 4` fails whole-original CODE: **2,044** initialized
  candidate bytes vs **2,020** original. This is a real negative
  control. The original byte masks were restored.
- `af845c`: named physical orbit step/diameter, mirrored barrage
  angle/period, renderer frame divisor and entrance radius, all full
  original CODE exact in both real compiler/link rounds.
- Final `af845d`: the same code plus corrected comments on the critical
  word/byte distinction and the postfix cloud-speed mutation; two
  genuine original TC4/normal MAIN TLINK rounds pass.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af845d --units ba_reimu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af845d
```

The final current-source bound independent rounds match **all 2,020
original initialized CODE bytes, 270 literal ordered OMF FIXUPP fields,
9 PUBLIC offsets**, original segment ABI and source dependencies, full
normal MAIN EXE/MAP, complete 124,642-byte Japanese loaded program and
**all 1,553 ordered original MZ relocations**. Independent standard MZ
serialization produces every byte of the 130,882-byte original Japanese
MAIN.EXE. The 98 other original project objects and CRT were reused;
**no full cold replay, code padding, altered original target or OBJ patch**.

Protected report and two genuine writer rounds:
`.analysis/work/exatt-layout-af845d/report.json`, SHA-256
`6d4d9acd0b5881f96131d1d2ff92f6f42653ec892ba2b89fbdd53a4f8d5c527a`.
These were previously historically covered original CODE bytes. This
improves source-native C++ semantics/codegen certainty, **not new
independent byte coverage, original vendor packet identity or canonical
Factory packed-file acceptance**.
