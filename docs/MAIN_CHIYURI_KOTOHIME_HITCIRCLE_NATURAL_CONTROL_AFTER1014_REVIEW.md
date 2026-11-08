# TH03 MAIN: natural Chiyuri cardinal, Kotohime intro and HitCircle guards

This round revisited three complete physical owners rather than treating
older expression notes as final answers. It recovered natural byte updates
in Chiyuri's cardinal attack, a clearer Intro transition in Kotohime's full
BOSS dispatcher, and simpler age guards in the HitCircle update/render path.

## Chiyuri cardinal attack

The cardinal controller now uses ordinary compound assignments for its
byte-angle state:

    if(chiyuri_cardinal_reverse == 0) {
        chiyuri_cardinal_angle += CHIYURI_CARDINAL_STEP;
        // original upper reversal endpoint and reset
    } else {
        chiyuri_cardinal_angle -= CHIYURI_CARDINAL_STEP;
        // original lower reversal endpoint and reset
    }

The three following 90-degree bullet rotations likewise use:

    bullet_template.angle += CHIYURI_CARDINAL_QUARTER_TURN;

Each rotation remains after the preceding bullets_add() call. The source
also uses the natural remainder-first predicate
(boss_frame % chiyuri_cardinal_interval) != 1; it retains the unsigned
16-bit frame arithmetic and early return. The reverse flag's explicit
zero comparison is also exact.

This resolves an ambiguity in older compiler notes: literal += 8 and
named explicit assignments had each been proven separately, but the named
compound += CHIYURI_CARDINAL_STEP / -= CHIYURI_CARDINAL_STEP spellings
had not. Fresh complete-object trials now show both named compound
assignments and the three named quarter-turn compound assignments preserve
the original CODE.

Two alternatives were rejected:
- Swapping the reverse/forward branch order and testing
  chiyuri_cardinal_reverse != 0 changed complete CODE.
- Moving pid_other's declaration and initializer into the frame-one block
  also changed complete CODE; the original function-scope local remains.

The final complete ba_chiyu source is bound to af1013h.

## Kotohime Intro dispatcher

The Intro switch arm now describes the successful transition directly:

    case KOTOHIME_MODE_INTRO:
        if(boss_frame == KOTOHIME_INTRO_FINISH_FRAME) {
            boss_frame = 0;
            boss_mode = KOTOHIME_MODE_SELECT;
            break;
        } else {
            return;
        }

This is equivalent to the former mismatch-first early return, but makes
the one transition frame explicit. The complete
gba_boss_update_kotohime() owner remains byte-exact in two independent
original compiler rounds. The complete ba_koto source is bound to af1013c.

## HitCircle update and render

All three active-age tests now use the byte's natural truth value:

    if(p->age) {
        // update or draw the active hit circle
    }

The enemy render loop uses an early continue for inactive records:

    for(i = 0; i < HITCIRCLE_ENEMY_COUNT; (++i, ++p)) {
        if(!p->age) {
            continue;
        }
        sprite16_clip_set_for_pid(p->pid);
        sprite16_offset_t so = p->cel();
        sprite16_put(p->topleft.x, p->topleft.y, so);
    }

The original postfix age increment, near-pointer/index update order,
per-record cel call, player-circle palette and final GRCG reset remain
unchanged. The full 445-byte hitcirc object is exact in two independent
original TC4 rounds; its final source is bound to af1014d.

## Complete-object and integrated verification

| Complete owner | CODE | Ordered OMF FIXUPPs | PUBLICs | Source-bound stage |
| --- | ---: | ---: | ---: | --- |
| Chiyuri ba_chiyu | 2,654 | 381 | 11 | af1013h |
| Kotohime ba_koto | 1,840 | 262 | 11 | af1013c |
| HitCircle hitcirc | 445 | 30 | 4 | af1014d |
| Kotohime + Chiyuri together | 4,494 | 643 | 22 | af1014a |

The simultaneous af1014e integration rebuilt all nine major BOSS owners
together with Hitbox, HitCircle and the explosion-chain owner in both
independent original Turbo C++ 4.02 rounds:

| Scope | Exact original result |
| --- | ---: |
| Complete physical owners | 12 |
| CODE | 18,792 bytes |
| Ordered OMF FIXUPPs | 2,546 |
| PUBLICs | 91 |
| Japanese MAIN loaded image | 124,642 bytes |
| Ordered MZ relocations | 1,553 |

Both complete normal MAIN links match. The other 87 original game objects
and Borland CRT were reused; no full cold replay was run. All twelve
integrated source hashes match the current maintained files.

## Reproduction

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1013h --units ba_chiyu

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1013c --units ba_koto

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1014d --units hitcirc

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1014a --units ba_koto,ba_chiyu

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1014e \
      --units ba_mima,ba_reimu,ba_yumem,ba_ellen,ba_kana,ba_koto,ba_maris,ba_rikak,ba_chiyu,hitbox,hitcirc,e_expl

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af1014e

Protected reports:

- af1013h: .analysis/work/exatt-layout-af1013h/report.json,
  SHA-256 23b2d265f55e5fd0506c0090beeb0ffde54830e36ad8672c47afbf1c8398214e
- af1013c: .analysis/work/exatt-layout-af1013c/report.json,
  SHA-256 2e17b4f8bf1a2b4f7464fe5fce0758031732e3c929c1c784f667204b56a21e15
- af1014d: .analysis/work/exatt-layout-af1014d/report.json,
  SHA-256 a5b2b4f8ecfc27d398fbd5f9c19fa0be7f96fb53d3753239c84ad1d32439de1e
- af1014a: .analysis/work/exatt-layout-af1014a/report.json,
  SHA-256 e679446c6bd88d6eebe9bb28dc57a6e8b0003ec696b23e363991809b2c534300
- af1014e: .analysis/work/exatt-layout-af1014e/report.json,
  SHA-256 9bde7e2cdb79408067660e7722c3beac1e21db5fd0f4fb25d46b3ed903fd2cbe
