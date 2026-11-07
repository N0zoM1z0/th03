# TH03 MAIN after791/821: entire Kotohime BOSS native flicker and radial C++ geometry

The **entire original physical `ba_koto`** owner contains the Kotohime
BOSS template, ring emitter, random/aimed/pellet/radial attack families,
full update/collision controller and animated multi-sprite renderer.
Its sprite-ring renderer previously used
`(boss_frame & (KOTOHIME_RENDER_FLICKER_PERIOD - 1))` to pick the two
alternate palette frames out of each four-frame animation period.
Since `boss_frame` is a 16-bit unsigned native timer, the maintained
C++ can naturally express
`(boss_frame % KOTOHIME_RENDER_FLICKER_PERIOD) < KOTOHIME_RENDER_ALT_FRAMES`.
Original Turbo C++ 4.02 generates the **identical original machine code**.

## Real native negative controls, not hand-waved equivalence

- Stage `af791a` attempted to eliminate the two ring-pattern handwritten
  `_AL` byte increment sequences with ordinary `boss_move_phase += 2`.
  It compiled but produced **fewer CODE bytes** than the original and
  failed original full-object equality. The compiler reused the AL value
  from an earlier increment rather than emitting the original extra
  memory load.
- Stage `af791b` tried a volatile C++ near reference; this also compiled
  but produced different CODE. Both variants were **rejected**; the
  original `_AL = boss_move_phase; _AL += 2; boss_move_phase = _AL`
  remains where the genuine compiler cannot reproduce its load sequence
  naturally with these alternatives.
- Stage `af791c` kept both original AL updates while proving the natural
  `%4` sprite-ring flicker condition against the whole original object.
- The **final `af791e`** additionally names the 256-unit full-circle and
  128-unit half-circle angular spans, 0x40 center offset, 0x30/0x10
  burst speed scale/base and 0xC8 intro radius in the **entire BOSS attack
  and rendering controllers**, retaining original signed integer division
  before byte-angle truncation. Full physical source again passes two real
  native rounds; this stage supersedes `af791c` for current source.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af791e --units ba_koto
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af791e
```

Both independent original Turbo C++ 4.02 and complete normal MAIN TLINK
rounds reproduce **all 1,840 original initialized CODE bytes, 262
literal ordered OMF FIXUPP fields, 11 PUBLIC offsets**, full original
MAIN EXE/MAP and **all 124,642 loaded Japanese program bytes with 1,553
ordered relocations**. The independent DOS-MZ serializer reproduces
the 130,882-byte Japanese original MAIN.EXE. The other 98 original
project objects and CRT were reused; no full cold replay. Protected
current-source native report `.analysis/work/exatt-layout-af791e/report.json`,
SHA-256 `13fe72001ab53f62e11f8aab62267e292aaa61e60b78b6faebc65a013c18aa98`.
This is an improved natural C++ source recovery for an already historically
covered BOSS owner, not new distinct CODE-byte credit or canonical
packed-game Factory whole-product acceptance.

## After821: signed orbit geometry in the whole current BOSS source

The maintained full `ba_koto` owner now also names the physical **256-unit
full rotation** used by the random/aimed ring emitters and sprite renderer,
the **128-unit radial half arc**, the `0x40` center-angle offset, and the
`0x30` scale plus `0x10` base of the per-projectile speed sweep. These
are **signed 16-bit integer quotient computations before truncation to a
byte-valued angle**; they must not be collapsed into byte arithmetic,
or moved outside their nested `center_i` / `bullet_i` loops. The intro
closing radius is named at 200 pixels. All existing bullet emission, RNG
consumption, update/collision, and sprite-render order remain unchanged.

The `af821a` fresh original compiler experiment independently confirmed
that simply replacing both `_AL` byte-phase updates with `+= 2` drops the
original AL memory reload. `af821b`/`af821c` tested volatile near reference
variants and also did not restore whole-original CODE; `af821f` separately
challenged the radial `_AL += 0xFC` with natural `boss_move_phase -= 4` and
failed native CODE equality. All these forms were **rejected**, not accepted
by assumption or by running only a simulated behavioral test.

`af821d` proved natural unsigned `%4` for the complete BOSS, followed by
**`af821e`**, which genuinely compiled the whole 538-line BOSS twice with
the additional signed-orbit geometry. Both original TC4 4.02 / complete
normal TLINK rounds reproduce **1,840 original CODE bytes, 262 ordered
OMF FIXUPP fields, 11 PUBLIC offsets**, complete Japanese MAIN loaded
program, and all 1,553 ordered relocation words. The independent
serializer also reproduces all 130,882 bytes of the pinned original MZ.
`af821e`'s live source binding is independently reviewable:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af821e
```

Protected report `.analysis/work/exatt-layout-af821e/report.json`
SHA-256 `59504cb34ba013695ac57d25ea66a2640703827b4b2609fe7364892b7782f614`.
98 unrelated original game objects and CRT were reused. No cold replay,
relocation patching, target-byte padding, new distinct byte ownership, or
canonical packed-file Factory acceptance is claimed. The original AL
carriers remain explicit until an actually exact natural alternative is
found. Earlier `af791c` is historic source-snapshot evidence, not a
claim that today's additional geometry-named source matches its hash.
