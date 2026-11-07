# TH03 MAIN after887 — complete static HUD native loops and original score-display cap

The entire original `hud_stat` physical Turbo C++ 4.02 source contains
seven real static-HUD routines in the historical `HUD_STAT_TEXT` segment:
both players' full-/half-/empty-heart rows, Bomb glyphs, rounds won,
story-mode lives, Gauge/BOSS next-level digits, text wiping and the
complete two-player static HUD dispatcher. It is recompiled as one
original physical object, not isolated rendering leaves.

The two half-heart/empty-heart loops now use ordinary C++ `for` with
the original **shared signed halfheart index and +2 advance**, preserving
the choice between full and half glyphs and the fill of remaining slots.
The Bomb count, rounds-won and story-lives loops also use native-exact
`for` with the original signed `++i` and player-dependent glyph direction.
The **two-player dispatcher** now uses a natural typed `while`, retaining
all four calls in the original order before advancing its player index.
The three historical player-byte `pid==0` tests accept natural
`if(!pid)` in this actual original compiler owner. All TRAM/palette
and resident storage remain external to this physical source.

## Original TC4 compiler trials, including a real negative

- `af887a`: changed complete two-player dispatcher from `for` to
  natural `while`; original CODE and full normal MAIN exact twice.
- `af887b/c`: both linked halfheart/empty glyph loops changed to
  natural `for`, retaining one shared signed index; original CODE exact.
- `af887d`: Bomb, round-win and story-lives glyph traversals likewise
  became natural `for`, original object/whole link exact twice.
- `af887e`: all three byte player-ID checks use `if(!pid)` naturally;
  real TC4 4.02 still emitted every original instruction.
- `af887f`: challenged the original BOSS-level saturation guard
  `level >= GBA_BOSS_LEVEL_MAX` with mathematically equivalent
  `level > (MAX - 1)`. The candidate had the same 539 initialized
  bytes but **different original CODE at segment 1 offset 465**;
  the original `>=` comparison was restored.
- Final `af887g`: current complete maintained source and codegen
  comments compiled in two independent genuine TC4/normal MAIN rounds,
  with original CODE, ordered fixups and all PUBLICs exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af887g --units hud_stat
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af887g
```

Both independent original compiler/complete normal TLINK rounds match
**all 539 original CODE bytes, 18 literal ordered native OMF FIXUPP
fields and seven PUBLIC offsets**, real source/segment ABI, normal
MAIN EXE and normalized MAP, **124,642 Japanese loaded program bytes
and all 1,553 original MZ relocations**. Independent standard DOS MZ
serialization reproduces the entire **130,882-byte Japanese MAIN.EXE**.
The other **98 original project objects and Borland CRT were reused**,
not cold rebuilt or patched. Preserved genuine native proof:
`.analysis/work/exatt-layout-af887g/report.json`, SHA-256
`da6eebb496b6491209aeaa114cf85421178ae6b21ddf77c336c8f7aef4bc24e4`.

This had historical source coverage; it is improved native C++ fidelity,
**not newly distinct original CODE or canonical Factory accepted credit**.
