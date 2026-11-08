# TH03 MAIN Mima update and Random Bomb source recovery

Two more parts of the Mima controller now use natural constant-first and
postfix forms without changing the complete original physical owner.

The far update controller increments its unsigned-word frame with postfix
syntax and checks INTRO completion constant-first:

```cpp
boss_frame++;

case MIMA_MODE_INTRO:
    if(MIMA_BOSS_INTRO_END == boss_frame) {
        boss_frame = 0;
        boss_mode = MIMA_MODE_SELECT;
        break;
    } else {
        return;
    }
```

The completion reset, SELECT transition, switch break and non-completion
return are unchanged.

The 262-byte `mima_pattern_bomb_random()` leaf now places the named phase
constants first in all four frame comparisons:

```cpp
if(MIMA_RANDOM_BOMB_WARN == boss_frame) {
    boss_render_mode = MIMA_RMODE_TRAIL;
} else if(MIMA_RANDOM_BOMB_FIRE_BEGIN > boss_frame) {
    return;
}

if(MIMA_RANDOM_BOMB_BULLET_WAIT_END < boss_frame) {
    // barrage, ring, sound and finish transition
    if(MIMA_RANDOM_BOMB_RING_FRAME == boss_frame) {
        // ring emission
    }
    if(MIMA_RANDOM_BOMB_END <= boss_frame) {
        // SELECT transition
    }
}
```

The warning-mode setup and early return remain before origin-coordinate
calculation. The three marker-bomb frames still emit and return before the
live barrage; the RNG, pellet, ring, sound and finish order is unchanged.
The unsigned 16-bit frame and four-frame low-bit cadence remain intact.

The complete owner was rebuilt after the combined source changes in two
independent original Turbo C++ 4.02 rounds at `af1035o`: all 1,922 CODE bytes,
277 ordered native fields and nine PUBLIC offsets match. Both normal Japanese
MAIN links reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1035o/report.json`

SHA-256: `3f2979bec421837a2668fcd4d25d4837fa446cf87614be7730182780099196ae`

## Rejected alternatives

- Moving the EXPLODE switch case into a pre-switch early return changed the
  complete owner; keep the case in the switch.
- Declaring `pid_other` inside the active-player block with an initializer
  changed CODE; keep the declaration and assignment at their current points.
- Rewriting the Random Bomb active body as a positive `frame >= FIRE_BEGIN`
  scope with an `else return` changed CODE; keep the warning/early-return
  structure and the separate positive barrage wait guard.
- Constant-first rewrites of the Trail leaf's byte-phase comparisons changed
  CODE; this finding is specific to Trail and does not generalize to Random
  Bomb's unsigned-word frame comparisons.
