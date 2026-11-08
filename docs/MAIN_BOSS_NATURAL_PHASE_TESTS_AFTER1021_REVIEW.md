# TH03 MAIN: natural BOSS phase and renderer comparisons after1021

This pass recovered clearer source expressions in three complete BOSS
owners: Mima's hit/renderer dispatch, Chiyuri's attack clocks and state
thresholds, and Kotohime's ring/radial phase tests. The changes preserve the
original Turbo C++ 4.02 output in independent complete-object comparisons.

## Mima renderer

The damaged-sprite path always returns, so it now directly precedes the
Particle renderer as an else-if continuation. The four renderer-mode
comparisons use named enum values on the left:

    if(boss_hit) {
        // draw the damaged sprite
        return;
    } else if(MIMA_RMODE_PARTICLE == boss_render_mode) {
        // shared Particle / Trail render body
    } else if(MIMA_RMODE_EXPAND == boss_render_mode) {
        // expanding sprite
    } else if(MIMA_RMODE_FLASH == boss_render_mode) {
        // flash sprite
    } else if(MIMA_RMODE_TRAIL == boss_render_mode) {
        boss_render_frame = 0;
        goto render_mode_2;
    }

The original render_mode_2 label and Trail-to-Particle jump remain intact.
The complete ba_mima object is exact at af1021b: 1,922 CODE bytes,
277 ordered OMF FIXUPPs and nine PUBLICs.

Two larger-looking simplifications were rejected. Moving sprite_offset
into the Particle and Flash branch scopes changed complete CODE.
Flattening the nested Particle animation thresholds into a separate
else-if or two sequential tests also changed CODE. Keep the original
function-scope temporary and nested threshold structure.

## Chiyuri attack clocks and mode dispatch

The Cardinal controller now uses a direct byte truth test for its reverse
flag, named forward/reverse endpoint constants, and the already recovered
named first-frame constant. Its compound byte-angle steps and three
quarter-turn bullet rotations retain their original order.

Other attack/update clocks now use consistent natural comparisons:

- The ring cadence is expressed as remainder-first inequality.
- Cardinal and ring pattern-end tests use the named threshold on the left.
- The Select timer uses the named threshold on the left.
- The Trail fire-frame early return uses the named frame on the left.
- Horizontal/vertical fan-axis selection uses named frame values on the
  left, retaining the explicit mutually exclusive else-if.
- The palette-cycle state comparison uses its named state on the left.

The complete ba_chiyu object is exact at af1021a: 2,654 CODE bytes,
381 ordered OMF FIXUPPs and 11 PUBLICs.

One attempted comparison rewrite was not equivalent at the compiler level:
changing boss_pattern_i > boss_pattern_count to
boss_pattern_count < boss_pattern_i changed complete CODE. The original
operand order remains.

## Kotohime ring and radial phases

The shared ring emitter now tests its integer RNG selector directly:

    if(randomize_angle) {
        bullet_template.angle = randring_far_next16();
    }

All three ring/radial start-frame checks put the named phase constant first.
The expansion-limit and release-after comparisons in the random ring,
aimed ring and radial burst use constant-first less-than comparisons.
The Pellet Arc finish test likewise puts its named frame threshold first.

These changes retain the original AL-mediated phase-byte updates, byte
postincrements, signed angle arithmetic and nested radial projectile loops.
The complete ba_koto object is exact at af1019d: 1,840 CODE bytes,
262 ordered OMF FIXUPPs and 11 PUBLICs.

## Complete-object and integration evidence

| Owner / scope | CODE | Ordered OMF FIXUPPs | PUBLICs | Stage |
| --- | ---: | ---: | ---: | --- |
| Mima | 1,922 | 277 | 9 | af1021b |
| Chiyuri | 2,654 | 381 | 11 | af1021a |
| Kotohime | 1,840 | 262 | 11 | af1019d |
| Three BOSSes together | 6,416 | 920 | 31 | af1021c |
| Twelve-owner MAIN integration | 18,792 | 2,546 | 91 | af1021d |

Each affected scope was rebuilt in two independent original TC4 4.02 rounds
and linked through the complete normal Japanese MAIN response. The latest
twelve-owner integration reproduces the 124,642-byte loaded MAIN image and
all 1,553 ordered MZ relocations. The other 87 original game objects and
Borland CRT were reused; no full cold replay was run. All twelve source
hashes in af1021d match the current maintained files.

## Reproduction

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1021a --units ba_chiyu

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1019d --units ba_koto

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1021b --units ba_mima

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1021c \
      --units ba_mima,ba_koto,ba_chiyu

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1021d \
      --units ba_mima,ba_reimu,ba_yumem,ba_ellen,ba_kana,ba_koto,ba_maris,ba_rikak,ba_chiyu,hitbox,hitcirc,e_expl

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af1021d

Protected reports:

- af1021a: .analysis/work/exatt-layout-af1021a/report.json,
  SHA-256 2b9cd91524f458397fd628b52afacd756fed2747a94e9eb80c3a05300a110f41
- af1019d: .analysis/work/exatt-layout-af1019d/report.json,
  SHA-256 bdead77076b04735cc9afba6ac73270c9a321ad7e97557a69cf55751929c1272
- af1021b: .analysis/work/exatt-layout-af1021b/report.json,
  SHA-256 4c0d0961e91bee8e81c2125b9ce5c9bea18198a46bfecdbb3515924883b3e16c
- af1021c: .analysis/work/exatt-layout-af1021c/report.json,
  SHA-256 ac347d1526354f25768fb0b7fffc27e37e98e8c63b517ef8c27e9eaee91632cd
- af1021d: .analysis/work/exatt-layout-af1021d/report.json,
  SHA-256 52b8eb9698a45d15c5ed662cbac979b3554233a489301bafeed160a05649fa4a
