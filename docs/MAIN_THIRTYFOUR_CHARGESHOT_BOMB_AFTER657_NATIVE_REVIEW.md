# TH03 MAIN: 34 original native gameplay/BOSS/charged-shot objects after657

This is a fresh original Turbo C++ 4.02/TLINK **two-round** full MAIN
link proof, after substantial maintained C++ work in four physical
charged-shot/Bomb source producers and two complete BOSS objects.
It is NOT a cold replay, nor a reread of the earlier after650
30-object receipt.

## Complete current source-native ownership scope

| Source family | Original physical TUs | Exact CODE bytes | Ordered OMF FIXUPPs | PUBLICs |
| --- | ---: | ---: | ---: | ---: |
| Nine complete major character BOSSes | 9 | 17,451 | 2,434 | 85 |
| Shared BOSS ring and seven-function controller | 2 | 949 | 106 | 8 |
| Ten Extra Attack/shared-flight producers | 10 | 8,781 | 563 | 52 |
| Bullet, Fireball, Explosion and four Enemy owners | 7 | 8,195 | 582 | 50 |
| CPU targeting/evading and Yumemi charged-shot/Gauge | 2 | 2,722 | 197 | 14 |
| Ellen charged-shot / Gauge | 1 | 1,530 | 169 | 10 |
| Ellen bomb update/render/palette | 1 | 1,023 | 116 | 3 |
| Chiyuri charged-shot / Gauge | 1 | 1,011 | 96 | 9 |
| Kotohime charged-shot / Gauge | 1 | 690 | 79 | 9 |
| **Total** | **34** | **42,352** | **4,342** | **240** |

Newly source-recovered details in the four physical additions:

- Ellen charged-shot: natural predecrement in the complete
  homing/clip/collision updater, no temporary AX preprocessor macro
  in signed 16-bit private rendering, checked 12-byte projectile
  physical record (+04 center, +08 velocity), and source-readable
  two-stage homing / full Gauge attack. The original cross-loop goto
  is preserved because natural break code changed native bytes.
- Ellen bomb: corrected an actually observed source/ABI mismatch:
  compiling its 132-byte private particle state in the CODE module
  changed 18 original code address/addend bytes. Real original
  b_ellen has **zero private BSS**; the original particle storage
  is external, with 8-byte slot stride, 128-byte two-player pool
  and the separately bound count/pointer. Natural unsigned %2
  palette pulse reproduces original native code; unmatching
  modulo-4 shaking and structured respawn code are rejected.
- Chiyuri charged-shot: truly original-equal unsigned modulo-2
  Gauge and sprite cadence, and natural i*4+2 staggered ages.
  The 6-byte physical projectile ABI, eight slots per player
  and reverse storage traversal are checked. The original
  broken reset loop that repeatedly clears the same first
  slot sixteen times remains original behavior.
- Kotohime charged-shot: original-byte-equal natural boolean
  active/inactive checks, checked 8-byte physical record
  (+02 center, +06 vertical velocity), original Gauge phase.
  Native evidence showed that replacing its BX-bound collision
  pointer macro with a normal register pointer selects SI and
  changes original code; the BX form remains.
- Mima/Rikako big BOSS: direct natural opponent PID computation
  after the shared target-helper call and a direct byte-field
  pellet-speed +8 replace explicit AL load/add/store. A
  seemingly equivalent AX -=8 register rewrite was rejected.

Incremental preserved accepted stages: af652g, af653g, af654e,
af655e and af656d. Original-unequal negative stages, native
writer logs and source overlays remain retained; no old receipt
was rewritten or used to mask current source provenance.

## Genuine native 34-object two-round integration

The current scoped builder **actually compiled all 34 complete
selected physical translation units twice**, leaving the other
65 original project objects and startup/CRT libraries unchanged
in the historical original 99-object normal MAIN TLINK response.
It bound the compiler to per-round copies of the current modified
source, and where consumed to the correctly packed 32-byte BOSS
and Extra Attack headers. Actual emitted Borland OMF COMENT
dependencies verify those source paths, avoiding the historical
v1 stale-TH03WORK false-positive problem.

All native original CODE and initialized DATA payloads, all
4,342 literal ordered FIXUPP fields, 240 PUBLIC offsets and
whole OMF segment/BSS metadata are original-equal in both
compiler rounds. Both full normal MAIN EXEs and complete
path-normalized MAPs equal the retained source-native original.

The loaded Japanese MAIN program contains the identical
124,642 byte original image and all 1,553 literal ordered
MZ relocations. The independently serialized standard MZ
produces the exact original 130,882-byte Japanese MAIN.EXE.
This does not conflate a newly emitted TLINK header with the
original historical header.

Reproduce the same bounded native rebuild, without cold replay:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af657a --units cs_ellen,b_ellen,cs_chiyu,cs_koto,p_cpu,cs_yume,ba_chiyu,ba_kana,ba_koto,ba_ellen,ba_rikak,ba_yumem,ba_mima,ba_reimu,ba_maris,ba_sring,ba_srest,ex_yume,ex_mima,ex_rika,ex_rfly,ex_reup,ex_ellen,ex_koto,ex_chyu,ex_maris,ex_kana,e_fireb,e_expl,bullet,eforna,efornb,eupda,eupdb
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af657a

Native evidence root:
.analysis/work/exatt-layout-af657a/report.json
SHA-256 108f93b705111f69cd9832e3d8837644af20df230a9c70e0809ead655cb487ab.

Both actual compiler/linker rounds, 68 native object files,
both full EXE/MAP files, both independent MZ serializations,
linker response files, writer logs and all source/header
overlays are retained outside Git.

**Limits:** All 42,352 CODE bytes were already tracked as
original source-owned target bytes; this is source-quality,
ABI and compiler-native integration progress, NOT 42,352
new canonical Factory packed-game byte credits. Raw historic
vendor OMF packet byte identity, pristine packed-game origin,
formal canonical Factory acceptance and physical PC-98
runtime behavior remain separate unproven questions.
