# TH03 MAIN: natural nested and repeated fan for-loops in Kotohime and Chiyuri

The complete Kotohime radial burst and Chiyuri fan attack now use ordinary
C++ for-headers instead of manually initialized while loops. These are
large projectile-generation paths: their signed 16-bit division, geometry,
bullet field updates, speed ramps and spawn order remain in the original
sequence.

## Kotohime: ring emitter and nested radial burst

kotohime_ring_emit() now owns its index in the loop header:

    for(int i = 0; i < kotohime_orbit_count; ++i) {
        int x;
        int y;
        unsigned char angle;
        // optional RNG, signed full-turn division, polar geometry, bullets_add
    }

The complete kotohime_pattern_radial_burst() now uses two nested loops:

    for(int center_i = 0; center_i < kotohime_orbit_count; ++center_i) {
        int x;
        int y;
        unsigned char center_angle;
        // original center angle, polar geometry and center coordinates

        for(int bullet_i = 0; bullet_i < kotohime_burst_count; ++bullet_i) {
            // original half-turn angle and speed divisions
            bullets_add();
        }
    }

The geometry temporaries now live in the outer loop body, where they are
used. Both angle calculations still perform signed 16-bit multiplication
and division before byte truncation. The center RNG/phase setup, per-center
polar calls, per-projectile angle and speed calculations, and bullet spawn
order are unchanged.

Independent complete-owner trials established that both nested loops can
use local int indices without register, and that the geometry locals can be
scoped to the outer iteration. The optional-angle ring emitter also uses a
local int loop index and iteration-local geometry variables.

## Chiyuri: four fan passes and axis dispatch

chiyuri_pattern_fans() now uses four natural for-headers: ascending and
descending horizontal passes, then ascending and descending vertical
passes. One ordinary function-local int i is initialized in each header.
The original speed assignments remain in the loop bodies, after the same
bullet calls; the signed count, division-before-scale coordinate expression,
angle calculation and dual horizontal spawn order are unchanged.

The horizontal branch returns after its two passes, so the vertical-axis
filter is now an else if:

    if(boss_frame == CHIYURI_FAN_HORIZONTAL_FRAME) {
        // horizontal warnings and two ascending/descending passes
        return;
    } else if(boss_frame != CHIYURI_FAN_VERTICAL_FRAME) {
        return;
    }

TC4 4.02 rejects repeating for(int i = ...) declarations for all four
passes in this one function (af1006b: “Multiple declaration for 'i'”).
A single function-local int i with natural for(i = 0; ...) headers
compiles to the original complete object. This is a compiler limitation,
not a reason to retain the manual while-loop increments.

## Complete original-object proofs

Each final maintained source was rebuilt in two independent original
Turbo C++ 4.02 rounds and linked through the complete normal MAIN response:

| Owner | CODE | Ordered OMF FIXUPPs | PUBLICs | Final source stage |
| --- | ---: | ---: | ---: | --- |
| Kotohime ba_koto | 1,840 | 262 | 11 | af1006g |
| Chiyuri ba_chiyu | 2,654 | 381 | 11 | af1006h |

Both rounds reproduce each complete physical object's original CODE and
ordered native fields, plus the full 124,642-byte Japanese MAIN loaded image
and all 1,553 ordered MZ relocations.

The simultaneous af1007a integration rebuilt all nine major BOSS owners
together with complete Hitbox, HitCircle and explosion-chain owners in both
independent compiler rounds:

| Scope | Exact original result |
| --- | ---: |
| Complete physical owners | 12 |
| CODE | 18,792 bytes |
| Ordered OMF FIXUPPs | 2,546 |
| PUBLICs | 91 |
| Japanese MAIN loaded image | 124,642 bytes |
| Ordered MZ relocations | 1,553 |

Both complete normal MAIN links match. The other 87 original game objects
and Borland CRT were reused; no full cold replay was run.

## Reproduction

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1006g --units ba_koto

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1006h --units ba_chiyu

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1007a \
      --units ba_mima,ba_reimu,ba_yumem,ba_ellen,ba_kana,ba_koto,ba_maris,ba_rikak,ba_chiyu,hitbox,hitcirc,e_expl

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af1007a

Protected reports:

- .analysis/work/exatt-layout-af1006g/report.json,
  SHA-256 000d8a1b91179226d194eede2b4109847797e653e4a3cd11a2dce12751163b97
- .analysis/work/exatt-layout-af1006h/report.json,
  SHA-256 bb1dae5e061eb186ffdf57e92d4fc0a5d8d2015331628c931f57b85ee61df554
- .analysis/work/exatt-layout-af1007a/report.json,
  SHA-256 fffad35d10b614090bc408d14cfba5794ebd452a312788299a49a09feafd3b50
