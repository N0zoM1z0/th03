# TH03 MAIN: Kotohime radial loop recovery and HitCircle enum layout

This pass recovered a more natural source layout in Kotohime's nested
radial-burst generator and HitCircle's compile-time geometry/capacity
constants. Both complete physical owners retain the original TC4 4.02
output; the final changes also pass a four-owner and twelve-owner
simultaneous MAIN integration.

## HitCircle: compile-time layout and capacity

The dimensions, VRAM stride and animation-frame constants now form one
named enum:

    enum hitcircle_layout_t {
        HITCIRCLE_W = 48,
        HITCIRCLE_H = 48,
        HITCIRCLE_VRAM_W = (HITCIRCLE_W / BYTE_DOTS),
        HITCIRCLE_VRAM_W_PER_CEL_TERM = (HITCIRCLE_VRAM_W / 3),
        HITCIRCLE_CELS = 4,
        HITCIRCLE_FRAMES_PER_CEL = 4,
        HITCIRCLE_FRAMES = (HITCIRCLE_FRAMES_PER_CEL * HITCIRCLE_CELS),
    };

The enemy/player slot counts and total array extent now form a second
named enum. The player-count quirk comment sits directly above that group.
This replaces a set of independent static const declarations with
compile-time enum values while keeping the existing relationships explicit.

Each change was tested independently before being combined. The full
445-byte hitcirc CODE, all 30 ordered OMF FIXUPPs and four PUBLICs match
in two original TC4 rounds. The original BX/AX cel sequence remains
untouched: BX still receives age - 1, self-divides by the named
four-frame constant, multiplies by the named VRAM-width term, and returns
the original three BX additions.

The enemy ring wrap guard now uses the named capacity on the left:

    if(HITCIRCLE_ENEMY_COUNT <= last_id) {
        last_id = 0;
    }

The byte last_id++ remains postfix. Its prefix form changed the original
CODE in the earlier negative trial.

An alternative cel return using
SO_HITCIRCLE + BX + (BX * HITCIRCLE_VRAM_W_PER_CEL_TERM) changed
complete CODE. The explicit three-add return remains.

Final complete hitcirc proof: af1024b, 445 CODE bytes, 30 ordered OMF
FIXUPPs and four PUBLICs. Both original compiler rounds and normal MAIN
links match. The report is bound to the current maintained source.

## Kotohime: radial burst scratch lifetime and loop form

The full kotohime_pattern_radial_burst() nested projectile traversal now
declares its scratch values once in the release branch, before the outer
loop:

    int x;
    int y;
    unsigned char center_angle;
    int bullet_i;
    int center_i;

    for(center_i = 0; kotohime_orbit_count > center_i; center_i++) {
        // calculate center_angle, x and y
        // emit kotohime_burst_count projectiles
        for(bullet_i = 0; kotohime_burst_count > bullet_i; bullet_i++) {
            // preserve signed angle/speed division and bullets_add order
        }
    }

This keeps the two natural nested loops, but gives the five scratch
variables one explicit block lifetime instead of recreating the coordinate
temporaries per outer iteration and declaring both indices in their
headers. Both loop indices use postfix increment. The constant-first
count comparisons also preserve complete CODE.

Experiments were separated:
- Hoisting x, y and center_angle before the outer loop passed.
- Hoisting bullet_i passed.
- Hoisting center_i passed.
- Changing both built-in loop increments to postfix passed.
- Putting each count on the left of > passed.
- Replacing either < count bound with != count changed complete CODE
  and was restored.

The original signed 16-bit multiply-before-divide order, byte-angle
truncation, polar calls, inner bullet angle/speed calculations, and
bullets_add() order remain unchanged.

Final complete ba_koto proof: af1024c, 1,840 CODE bytes, 262 ordered OMF
FIXUPPs and 11 PUBLICs. Both original compiler rounds and normal MAIN
links match. The report is bound to the current maintained source.

## Combined verification

The four changed/current owners Mima, Kotohime, Chiyuri and HitCircle were
rebuilt simultaneously at af1024d:

| Scope | CODE | Ordered OMF FIXUPPs | PUBLICs |
| --- | ---: | ---: | ---: |
| Four complete owners | 6,861 bytes | 950 | 35 |

The twelve-owner integration af1024e then rebuilt all nine major BOSS
owners together with complete Hitbox, HitCircle and explosion-chain owners
in two independent original TC4 4.02 rounds:

| Scope | Exact original result |
| --- | ---: |
| Complete physical owners | 12 |
| CODE | 18,792 bytes |
| Ordered OMF FIXUPPs | 2,546 |
| PUBLICs | 91 |
| Japanese MAIN loaded image | 124,642 bytes |
| Ordered MZ relocations | 1,553 |

Both complete normal MAIN links match. The other 87 original game objects
and Borland CRT were reused; no full cold replay was run. All twelve source
hashes in af1024e match the current maintained files.

## Reproduction

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1024b --units hitcirc

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1024c --units ba_koto

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1024d \
      --units ba_mima,ba_koto,ba_chiyu,hitcirc

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1024e \
      --units ba_mima,ba_reimu,ba_yumem,ba_ellen,ba_kana,ba_koto,ba_maris,ba_rikak,ba_chiyu,hitbox,hitcirc,e_expl

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af1024e

Protected reports:

- af1024b: .analysis/work/exatt-layout-af1024b/report.json,
  SHA-256 62b731c48a1910f261b2b16e00baf2186fc6557b8002de3029c3c3ce0ad8d750
- af1024c: .analysis/work/exatt-layout-af1024c/report.json,
  SHA-256 6f0ea0a0ca95731e8ebdf90a6b4c6c7f601288ee4d902faad3713a363fadde82
- af1024d: .analysis/work/exatt-layout-af1024d/report.json,
  SHA-256 85a09bd39ea4f01f7f0a730951e223d50ae9b65e79b1917faec62f2b96532b64
- af1024e: .analysis/work/exatt-layout-af1024e/report.json,
  SHA-256 a37060b2d80d066ab2058774a606f522ecf6f43d726e0bc2983fdbda2416cc7c
