# Mima BOSS and collision: original nested gates and renderer dispatch

Mima's nine-function BOSS owner now exposes the two separate requirements for
its pellet subpattern: the frame must still precede `mima_pellet_until`, and
the unsigned-word timer must be divisible by six. The main two-frame bullet
and sound cadence, two original pellet calls, and the post-volley signed
byte-angle update remain in their original order. Mima's initial pattern,
random-bomb entry and intro-exit comparisons are now phrased with the frame
on the left. The renderer also uses a positive check for `MIMA_RMODE_TRAIL`:
only that mode resets the render frame and jumps to the existing particle
renderer label. The label and all sprite/VRAM effects are retained, not
duplicated into another rendering branch.

In `hitbox_hittest()`, live-shot and player-ownership tests now appear as two
separate early-continue guards. The original `alive != true` test is retained
because a plain Boolean negation previously changed TC4 instructions. Bomb
damage is explicitly nested under the player's active-bomb check, with the
independent two-frame unsigned-word cadence and original byte postincrement.
The 13-record HitCircle update now positively guards live ages and expires
only ages strictly greater than the original 16-frame lifetime. Its signed
index and near pointer continue advancing on every slot, including dormant
ones. The existing near-call carrier and original renderer register masks
are unchanged.

Original TC4/TLINK native results:

- `af1317k`: complete Mima BOSS, **1,922 CODE bytes, 277 ordered native fields,
  nine PUBLICs**, two independent original compiler and normal-link rounds
- `af1317l`: complete Hitbox and HitCircle objects, **711 CODE bytes, 63
  ordered native fields, five PUBLICs**, two rounds
- `af1317j`: joint recompile of all three physical objects, **2,633 CODE
  bytes, 340 ordered fields, 14 PUBLICs**, with both normal Japanese MAIN
  executable images, full original MAP and ordered MZ relocations identical

The negative `af1317h` tried moving the random-bomb `frame < 0x20` gate ahead
of the `frame == 0x10` warning update. Although the early-frame behavior
seemed equivalent, TC4 reversed the order of its first two comparisons and
changed the original near branch into a longer conditional jump. The object
shrank from 1,922 to 1,920 bytes. That change was rejected; the warning
state update retains its original explicit `if` / `else if` placement. No
object padding or target-byte injection was used.

Recheck the live physical scopes without cold replay:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1317k af1317l
```

These prove the selected original source-bound native owners, not whole-game
source ownership or Factory packed-file Oracle acceptance.
