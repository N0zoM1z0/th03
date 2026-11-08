# TH03 MAIN: natural for-loop and ordered guards in explosion-chain collision

The complete far-__cdecl explosions_hittest() now uses one ordinary
C++ for header to advance the signed 16-bit EFE index and near pointer:

    for(i = 0; i < EFE_COUNT; i++, expl_p++) {

This replaces the earlier while body, where each of six early-continue
paths and the successful collision path repeated both increments. The
iterator now advances once after every rejected entry or completed hit.
The original order is index first, pointer second.

The state, player and animation filters also share one ordered short-circuit
guard. It preserves the original evaluation order and the byte-valued
frame & 3 test:

    if(
        (expl_p->flag < EFF_EXPLOSION_IGNORING_ENEMIES) ||
        ((explosion_hittest_against == EHA_ENEMY) && (
            (expl_p->flag == EFF_EXPLOSION_IGNORING_ENEMIES) ||
            (expl_p->flag >= (
                EFF_EXPLOSION_HITTING_ENEMIES +
                (expl_p->explosion_max_enemy_hits_half * 2)
            ))
        )) ||
        (expl_p->pid != hitbox.pid) ||
        (expl_p->frame & (EXPLOSION_HIT_PERIOD - 1))
    ) {
        continue;
    }

The two geometry guards remain separate because the original routine
expands the radius to a diameter between their tests. Collision mutation,
enemy flag postfix, chain saturation, signed bonus arithmetic, score,
Gauge, charged-fireball and BOSS side-effect order are unchanged.

## Original TC4 experiments

- af994f moved all six skip paths and the success-path increments into
  the natural for header.
- af995a combined the two ordered explosion-state filters.
- af995b combined the player-id and byte-frame filters.
- af996b confirmed prefix pointer increment; af996c confirmed postfix
  index increment; af996d confirmed the ordinary i++, expl_p++ header.
- af997d combined all four state/player/frame prefilters into one
  short-circuit guard. af997e is the final maintained-source receipt.
- The pointer-bounded loop forms (< end and != end) and a loop-local
  for(int i = 0; ...) changed complete CODE.
- A switch(against2), explicit bonus = bonus + round_speed,
  extent.v *= 2 and bonus = bonus + bonus each changed complete CODE.
  The original score branch, compound arithmetic and extent shift remain.
- The byte animation %4 replacement, strict <255 saturation and
  prefix explosion-flag mutation remain known negative compiler results
  from the earlier af902/af846 experiments.

## Complete original-object verification

The final af997e stage rebuilt the complete e_expl physical owner in
two independent original Turbo C++ 4.02 rounds, followed by two complete
normal MAIN links:

| Scope | Exact original result |
| --- | ---: |
| CODE | 630 bytes |
| Ordered OMF FIXUPPs | 49 |
| PUBLICs | 1 |
| Japanese MAIN loaded image | 124,642 bytes |
| Ordered MZ relocations | 1,553 |

The other 98 original game objects and Borland CRT were reused. The
complete physical object, its ordered native fields and both normal MAIN
images/relocations match. This is a new current-source proof for an
already historically source-covered object, not additional distinct CODE
ownership or canonical packed-file acceptance.

Reproduction:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af997e --units e_expl

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af997e

Protected report:
.analysis/work/exatt-layout-af997e/report.json, SHA-256
f33b52becbfbd8f817265fd118158fb8568e5477f8975fd7a7bb1d938e9f13f0
