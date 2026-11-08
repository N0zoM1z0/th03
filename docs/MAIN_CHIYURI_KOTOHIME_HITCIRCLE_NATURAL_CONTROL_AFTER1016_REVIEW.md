# TH03 MAIN: Chiyuri cardinal, Kotohime dispatch and HitCircle iteration

This pass made three source-level improvements across two complete BOSS
owners and the complete HitCircle collision/render owner. Each affected
physical object was rebuilt in two original Turbo C++ 4.02 rounds and
linked through the normal MAIN response.

## Chiyuri cardinal controller

The opponent PID temporary now lives only in the frame-one initialization
block, where it is consumed by the four bomb-axis calls:

    if(boss_frame == CHIYURI_CARDINAL_FIRST_FRAME) {
        pid_t pid_other;
        // initialize cardinal direction and place the four bomb axes
    }

The assignment remains a separate pid_other = (1 - pid_current).
Moving only the declaration into the block preserves the complete
2,654-byte BOSS object. Moving the declaration and initializer together
changed CODE; replacing subtraction with logical negation also changed
CODE. The successful scope change was rechecked after adding the named
first-frame constant.

The cardinal first frame is now named
CHIYURI_CARDINAL_FIRST_FRAME = 1 and the attack controller compares
against that constant. This is also original-code exact.

Final complete ba_chiyu proof: af1016c, 2,654 CODE bytes, 381 ordered
OMF FIXUPPs and 11 PUBLICs. Two original compiler rounds and complete
normal MAIN links match.

## Kotohime full update dispatcher

gba_boss_update_kotohime() now uses the active-player path as the
positive branch:

    if(pid_current == gba_boss_launched_by) {
        pid_other = (1 - pid_current);
        // target update, frame increment, mode dispatch and collision
    } else {
        return;
    }

The entire scheduler, attack switch and collision/hitbox tail remain
inside this branch. The Intro switch arm also uses the explicit
finish-frame transition before returning for all other frames.

This is exact for the complete 1,840-byte ba_koto object. A further
attempt to move pid_other from function scope into the active-player
block changed CODE, so its existing function-scope lifetime is retained.

Final complete ba_koto proof: af1015e, 1,840 CODE bytes, 262 ordered
OMF FIXUPPs and 11 PUBLICs. Two original compiler rounds and complete
normal MAIN links match.

## HitCircle update loop

The thirteen-record age update now skips inactive records at the top of
the loop:

    for(i = 0; i < HITCIRCLE_COUNT; (++i, ++p)) {
        if(!p->age) {
            continue;
        }
        p->age++;
        if(HITCIRCLE_FRAMES < p->age) {
            p->age = 0;
        }
    }

This preserves the original byte postfix increment and the index-first,
near-pointer-second for-header update. The enemy render loop already uses
the same early-continue structure; all three active-age tests use natural
byte truth tests.

Final complete hitcirc proof: af1016a, 445 CODE bytes, 30 ordered OMF
FIXUPPs and four PUBLICs. Two original compiler rounds and complete
normal MAIN links match.

The attempt to replace the cel's BX multiply/add sequence with a single
natural scaled accumulation changed complete CODE and was restored. The
original BX/AX division round-trip, named stride multiply and three BX
additions remain.

## Simultaneous integration

The latest af1016d integration rebuilt all nine major BOSS owners plus
complete Hitbox, HitCircle and explosion-chain owners in two independent
original compiler rounds:

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
source hashes in the report match the current maintained files.

## Reproduction

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1016c --units ba_chiyu

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1015e --units ba_koto

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1016a --units hitcirc

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1016d \
      --units ba_mima,ba_reimu,ba_yumem,ba_ellen,ba_kana,ba_koto,ba_maris,ba_rikak,ba_chiyu,hitbox,hitcirc,e_expl

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af1016d

Protected reports:

- af1016c: .analysis/work/exatt-layout-af1016c/report.json,
  SHA-256 ad24fbbdacb1fce89436e5870edc76336f0927b38a6ae508aa029f3546c64ff3
- af1015e: .analysis/work/exatt-layout-af1015e/report.json,
  SHA-256 b5b49782235e27f6f1fe1a807dbfd501561189bdd6f5807d4c5a6d379728b315
- af1016a: .analysis/work/exatt-layout-af1016a/report.json,
  SHA-256 a116f75e4f08561a6f65755086d7bc20b11bbb6aacb058ba77cb7e48cb391ef8
- af1016d: .analysis/work/exatt-layout-af1016d/report.json,
  SHA-256 85b842b589a4bd839e1bdca1adbc3f1dc6fe13010742cf8cad98f490b607b742
