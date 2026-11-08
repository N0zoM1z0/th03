# TH03 MAIN Yumemi arrival renderer: natural C++ after1048

This pass continues the complete ten-function Yumemi BOSS owner and targets
the 404-byte four-phase `yumemi_render_arrival()` raster controller plus its
83-byte `gba_boss_render_yumemi()` caller.

## Four-phase entrance raster

The four arrival phase gates now use constant-first comparisons:

```cpp
if(YUMEMI_ARRIVAL_PHASE1_END > boss_frame) { ... }
else if(YUMEMI_ARRIVAL_PHASE2_END > boss_frame) { ... }
else if(YUMEMI_ARRIVAL_PHASE3_END > boss_frame) { ... }
else if(YUMEMI_ARRIVAL_PHASE4_END > boss_frame) { ... }
```

The two named positional shift constants are now honest scale constants:
`YUMEMI_ARRIVAL_POS_LOW_SCALE = 8` and
`YUMEMI_ARRIVAL_POS_HIGH_SCALE = 16`. The original separate signed stages
are expressed as ordinary multiplication, e.g.:

```cpp
((boss_frame * YUMEMI_ARRIVAL_POS_LOW_SCALE) *
    YUMEMI_ARRIVAL_POS_HIGH_SCALE)
((phase * YUMEMI_ARRIVAL_POS_LOW_SCALE) *
    YUMEMI_ARRIVAL_POS_HIGH_SCALE)
```

The first stage remains the `* 8` operation and the second remains `* 16`;
folding them into a single `* 128` changes TC4 CODE. The four original
increasing/decreasing raster loops, inclusive endpoint inequalities,
8-pixel signed steps, per-phase clipping bounds, draw order and the special
extra sprite in phase three remain untouched.

The `top`, `pid_other` and byte `phase` locals are now register-qualified;
`gba_boss_render_yumemi()` also uses a register-qualified `pid_other`. The
arrival top coordinate is base-first, phase differences omit redundant
parentheses, and the caller's INTRO/EXPLODE mode comparisons are
constant-first. The explicit `asm { xor dx, dx }` remains: it produces the
original `33 D2` instruction, whereas natural zeroing or `_DX ^= _DX`
produces the wrong `31 D2` encoding.

## Negative controls

- Folding the two signed scaling stages into `frame * 128` changes CODE.
- Reversing the first increasing raster condition to `right >= left` changes
  CODE; the original `left <= right` spelling remains.
- Reversing the first decreasing raster condition to `right <= left` changes
  CODE; the original `left >= right` spelling remains.
- Reversing `pid_current != gba_boss_launched_by` to the visually symmetric
  `gba_boss_launched_by != pid_current` preserves the apparent condition but
  changes ordered native fields; the original operand order remains.
- The hardware overlap-register XOR is deliberately not replaced by a C++
  zero assignment.

## Complete original-owner verification

Stage `af1048r` rebuilt the entire 2,358-byte `ba_yumem` physical object in
two independent original Turbo C++ 4.02 rounds. All 343 ordered native
fields and ten PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations. The other 98
original game objects and CRT were reused; no full cold replay was run.

Protected report: `.analysis/work/exatt-layout-af1048r/report.json`

SHA-256: `b1bf017e4567c8c9eb8b0889fd7b95c13d80de84504dfc106faebc65387d8a96`

This is current-source natural-C++ recovery within the already owned Yumemi
physical object, not additional unique CODE ownership, raw vendor OMF packet
identity or canonical packed-game acceptance.
