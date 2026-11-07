# TH03 MAIN after788: original eight-object simultaneous current-source TC4 integration

This stage combines the four **genuinely modified complete physical owners**
from after783–after786 (two major BOSSes, the main frame scheduler and Kana
Bomb) with four **additional complete original collision/shot/score owners**
that were historically source-built in after591/595, but had *not* been
included in the currently maintained strict overlay source-provenance driver:

| Real original physical TC4 source | Current-source scope/ABI | Original CODE | Ordered native FIXUPPs | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| `ba_reimu` | Reimu entire major BOSS: signed orbit timing/angle loops | 2,020 | 270 | 9 |
| `b_kana` | Kana Bomb timed reflection/explosion and byte fade | 526 | 53 | 1 |
| `entry` | Full MAIN entry, 200+-line frame scheduler and stage/score; **4 bound implementation `.inl` sources** | 3,050 | 433 | 8 |
| `ba_mima` | Mima entire major BOSS, native C++ unsigned `%2`/`%4` clocks | 1,922 | 277 | 9 |
| `hitbox` | Entire shot-pair/explosion/Chargeshot/collision damage; original segment-local `NOP; PUSH CS; CALL near` preserved | 266 | 33 | 1 |
| `hitcirc` | Enemy/player hit-circle spawn, update, sprite and clipping rendering | 445 | 30 | 4 |
| `shots` | Entire physical shot creation, flight/culling and fast dual-sprite renderer; **2 bound `.inl` sources** | 449 | 17 | 3 |
| `results` | Entire reset, match-scoreboard, digit and bonus renderer; **2 bound `.inl` sources** | 1,060 | 89 | 3 |
| **Eight actually compiled original physical TUs in one simultaneous native run** | | **9,738** | **1,202** | **38** |

## Current maintained C++ and original physical linker slots

The bounded original-source native overlay driver now knows the original
physical `hitbox` / `hitcirc` object slots retained from `af591c`, and
`shots` / `results` slots retained from `af595h`. Each is compiled through
its existing original source wrapper (not a new fake ABI or byte patch),
with the current original source force-rooted into two independently
compiled DOS-safe stage directories. The two `shots` and two `results`
`.inl` bodies are likewise individually rooted, SHA-256 pinned and checked
against **actual native compiler-emitted OMF COMENT file dependencies**;
without this, historical Wine `TH03WORK/src` copies could silently mask
live changes. Original `hitbox` special near-segment explosion-call encoding
and HitCircle sprite16 hardware-register calls are preserved; prior genuine
natural-C++ non-exact attempts are not reclassified as success. Two new
regression tests guard both historical linker identities and the full new
four-`.inl` current-source dependency set (nine total targeted tests).

The first isolated new strict-rooting experiments were `af788a` for
`hitbox,hitcirc` (711 CODE bytes, 63 FIXUPPs, 5 PUBLICs), and `af788b`
for `shots,results` (1,509 CODE bytes, 106 FIXUPPs, 6 PUBLICs). Each
passed two original compiler/normal TLINK rounds and source-bound review.
The later combined `af788c` is **not** a synthetic union of isolated
proofs: it compiles *all eight physical source units together* in each
of two original native writer rounds, then **normal-links the whole MAIN**
with the 91 other original project objects and original CRT unchanged.

## Fresh original native integration and independent review

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af788c --units ba_reimu,b_kana,entry,ba_mima,hitbox,hitcirc,shots,results
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af788a af788b af788c
.venv/bin/python -m unittest discover -s tests -p test_main_source_overlay_inline_contract.py -q
```

Both genuine independent original Turbo C++ 4.02/TLINK rounds matched **all
9,738 original initialized CODE bytes, 1,202 literal ordered OMF FIXUPP
fields, 38 original PUBLIC names and offsets**, segment source/storage ABI,
all originally allocated MAP module rows, and the complete normal MAIN EXE.
The full **124,642-byte Japanese loaded program** and **1,553 literal
ordered original MZ relocations** matched, while the independent standard
MZ serializer reproduced all original **130,882 bytes of MAIN.EXE**.
No whole-project cold replay was used. The real per-file original native
OBJ copies, TC4 writer logs, source/header/`.inl` snapshots, linker
responses, MZ, EXE and MAP outputs are preserved under protected ignored
`TH03WORK/probe/af788c` and `.analysis/work/exatt-layout-af788c/`.

Independent reviewer: `.analysis/work/exatt-layout-af788c/report.json`,
SHA-256 `3b031cc241ac6ac6a4f8047d9de291489f6ac0f8c0f817829e8a75041ed0974b`.
The original legacy collision and result source extents were historically
proven and thus are **not new distinct CODE ownership**. Their *current
source file and separate inline dependencies* now have a stronger fresh
source-binding proof. Raw original vendor OMF packet identity, full original
source ownership, canonical packed-file Factory approval and the separate
BIOS `input_s` one-NOP historical linker gap are **not** resolved by this
stage; do not claim additional canonical exact bytes.
