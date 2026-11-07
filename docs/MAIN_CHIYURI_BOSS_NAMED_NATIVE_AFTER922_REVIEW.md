# TH03 MAIN after922 — full Chiyuri major BOSS native named arithmetic and controller

The complete 11-function original physical `ba_chiyu` Turbo C++ 4.02
translation unit was actually compiled: BOSS state/template, cardinal
four-way pattern, ring/trail attacks, **all four substantial horizontal
and vertical fan bullet generators**, full BOSS scheduler, collision,
main/mono GRCG render and the full 16-sprite intro ring. Its historical
shared BOSS/DGROUP storage and AL/AX register carriers remain external;
no new source-owned state is invented.

## Original-machine-code-exact natural C++ changes

- Both original *unsigned 16-bit* cardinal/ring frame interval
  predicates now naturally use constant-first `1 != (frame % period)`.
- The four cardinal projectile headings now use native-exact C++
  `angle = angle + CHIYURI_CARDINAL_QUARTER_TURN`, with exactly three
  +0x40 rotations **after** preceding `bullets_add()` calls.
- The bidirectional moving cardinal angle uses natural
  `angle = angle +/- CHIYURI_CARDINAL_STEP` with a source-named +8/-8
  byte step, preserving historical wraparound and reversal endpoints.
- All four original fan speed-memory updates now use natural named
  `bullet_template.speed.v = bullet_template.speed.v +/-
  CHIYURI_FAN_SPEED_STEP` rather than literal `+=2/-=2`. This is
  machine-code-exact, despite an older genuine failed trial of a
  *different* `speed += enum` source spelling.
- The original 16-sprite ring byte angle also accepts natural
  `angle = angle + CHIYURI_RING_SPRITE_ANGLE_STEP`; original signed
  polar calculations and draw-then-increment order are unchanged.
- The original 16-bit global BOSS tick can use natural `++boss_frame`.
  The 8-bit render frame, movement phase and palette phase retain their
  compiler-sensitive original mask/postfix operations.
- The complete 64×48 collision tiles, 32-pixel hit radius, 128×64
  main sprite, 48×40 damaged sprite and 32×24 animation sprite now
  use named source-only dimensions and exact sprite offsets.

## Actual original Turbo C++ 4.02 trials

- `af922a`: reversed both unsigned word-frame cardinal/ring remainder
  comparisons, both original TC4/full normal MAIN TLINK rounds exact.
- `af922b`: placing a new enum *after* its first use caused genuine TC4
  `Undefined symbol`; this historical compiler does not permit that
  source-order dependency. `af922c` moved the enum before use and
  all three explicit named quarter-turn assignments became byte-exact.
- `af922d/e`: explicitly assigned both live byte cardinal angles +/-8,
  then named their step. Both variants were original byte-exact.
- `af922f`: explicit named 16-sprite byte ring angle +0x10 was
  original-exact (distinct from earlier failing `angle += enum`).
- `af922g`: named the true collision/render geometry, still exact.
- `af922h`: four separate fan +/-2 memory-speed assignments with
  source-named enum remained **entire-original CODE exact**.
- `af922i`: replacing the original mutable byte-memory render mask
  `boss_render_frame &= 3` with `%4` generated **2,660** CODE bytes,
  not original **2,654** (first discrepancy segment 4 offset 1388).
  Restored the original byte mask.
- `af922j`: the *different* 16-bit global `boss_frame++` could become
  natural `++boss_frame`, native original-exact in both rounds.
- `af922k`: byte `boss_move_phase--` to prefix generated different CODE
  at original segment 4 offset 1388; restored the original postfix.
- Final `af922l`: all current source and compiler-sensitive comments
  compiled in two independent genuine original TC4 4.02 and complete
  normal MAIN TLINK rounds, entire original BOSS exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af922l --units ba_chiyu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af922l
```

Both original compiler and normal complete linker rounds reproduce
**all 2,654 CODE bytes, 381 literal ordered original OMF FIXUPP fields
and 11 PUBLIC offsets**, original real source/segments/16-bit ABI,
complete normal MAIN EXE/normalized MAP, **124,642 Japanese loaded
program bytes and all 1,553 ordered MZ relocations**. Independent
checked standard DOS MZ serialization reconstructs all 130,882 bytes
of the pinned Japanese MAIN.EXE; historical vendor header serialization
identity is not separately proved. **98 other original game project
objects and CRT reused**, not cold built, patched, byte-padded or
replaced by synthetic code arrays.

Protected real original source-bound two-round writer receipt:
`.analysis/work/exatt-layout-af922l/report.json` SHA-256
`c2f56b71b18d285bae5aac2e66f416f5546cfe699ab60e449c9d175a2c235336`.
The original object was historically source-covered. This advances
natural current C++ and compiler certainty, **not distinct new original
CODE credit, raw vendor packet-identical OMF or canonical Factory
packed-game accepted credit**.
