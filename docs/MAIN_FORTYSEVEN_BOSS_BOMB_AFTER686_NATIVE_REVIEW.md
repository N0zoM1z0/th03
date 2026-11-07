# TH03 MAIN: 47 complete BOSS, Bomb and gameplay source-native owners after686

This is a **fresh** original Turbo C++ 4.02 compiler and complete
MAIN TLINK two-round integration of the currently modified C++
sources. It extends the after677 43-owner game-source scope with
four complete original character-Bomb objects and incorporates
new substantial C++ recovery in five character BOSS producers.
No original binary objects or frozen compiler ancestor were
patched or replaced to manufacture equality.

## Original physical object scope

| Original source families | Complete TUs | Exact CODE bytes | Ordered literal native FIXUPPs | PUBLIC offsets |
| --- | ---: | ---: | ---: | ---: |
| Nine complete major character BOSS controllers | 9 | 17,451 | 2,434 | 85 |
| Shared BOSS ring and seven-function controller | 2 | 949 | 106 | 8 |
| Ten complete Extra Attack/shared-flight producers | 10 | 8,781 | 563 | 52 |
| Bullet, Fireball, Explosion and four Enemy producers | 7 | 8,195 | 582 | 50 |
| CPU plus Yumemi charged-shot/Gauge | 2 | 2,722 | 197 | 14 |
| Ellen charged-shot/Bomb and Chiyuri/Kotohime charged-shot | 4 | 4,254 | 460 | 31 |
| Kana, Rikako, Mima and Reimu charged-shot/Gauge | 4 | 5,357 | 542 | 40 |
| Marisa full GRCG charged-shot/Gauge | 1 | 1,509 | 152 | 9 |
| Player effects and warning/Gauge | 2 | 2,188 | 158 | 12 |
| Background Chain 1 and Chain 2 | 2 | 1,245 | 86 | 9 |
| New Chiyuri/Kana/Kotohime/Rikako Bomb controllers | 4 | 2,090 | 207 | 4 |
| **Total** | **47** | **54,741** | **5,487** | **314** |

The final 47 includes every selected physical TU with complete
original CODE/fixup/segment ownership, not isolated function
lengths; the other **52** original project objects are
unchanged. Both independent rounds use the real 99-project-object
normal MAIN linker response. This is a **scoped object rebuild,
not a full game cold replay**.

## New actually maintained C++ recovery

- **Ellen major BOSS**: both original even-frame firing
  masks become exact native `boss_frame%2`, a signed
  `-2` replaces opaque final Extra Attack byte 0xFE,
  and burst/renderer loop increments read naturally.
  A combined `if(--i<0)` rewrite of render strip stepping
  was native-unequal and rejected (after678).
- **Rikako major BOSS**: two-stage `(boss_frame*2)*16`
  radius, unsigned `boss_frame%2` and
  `round_or_result_frame%2`, two unsigned `i%4`
  sprite selectors and natural 8-bit frame `*4`
  angle. Flat `frame*32` and unary angle negation
  changed native CODE and were rejected (after679).
- **Chiyuri major BOSS**: all four horizontal/vertical
  upward/downward fan loops now express native original
  `(i*0x70/count)*16` subpixel positions and
  `i*64/count` angles. The **division before scaling**
  is preserved. Palette update and both ring/main
  renderers use natural `phase*16`, `radius*16` and
  `render_frame*4` arithmetic (after680).
- **Kotohime major BOSS**: four complete circular/radial/
  renderer angle expressions now use natural
  `i*256/count` and `i*128/count` before original
  signed integer division; the old near-register
  other-phase updates remain where native-unequal
  shortening has been documented (after685).
- **Marisa major BOSS**: the original four-frame
  render flicker comparison now uses unsigned
  `round_or_result_frame%4<2`, retaining the
  exact original masked x86 instructions (after685).
- **Chiyuri Bomb**: the complete three-phase one-function
  state machine uses native `frame*4`, two-stage
  `(frame-64)*2*16` and terminal `frame*8`
  for color and four radial explosion axes. A typed
  unsigned `%4` shake replacement changed native
  CODE and was rejected (after683).
- **Rikako Bomb**: natural palette `frame*4`,
  late fade `frame*8` and preserved RNG-seeded
  `TO_SP(288)`/ `TO_SP(96)` horizontal explosion
  ranges (after683).
- **Kana Bomb**: two mirrored polar explosion paths now
  multiply X/Y by 16 in normal C++ and use
  `frame*8` for final palette phase. The original
  `frame&3` shake test is retained after a negative
  native `%4` control (after684).
- **Kotohime Bomb**: original three-particle row's
  288-pixel bound and 96-pixel step use natural
  `TO_SP`, plus standard loop preincrement and
  `frame*8` palette fade. Its original read of an
  **uninitialized local color** is deliberately not
  rewritten into new defined behavior (after684).

## New physical external-storage ownership

The four original character-Bomb physical objects
`b_chiyu`, `b_kana`, `b_koto`, `b_rika` are now
explicitly supported by the source-native v2 compiler
and its independent reviewer, with original object
slots and original MAP names. The latter three have
**external private data owned by the original frozen
carrier**, not additional BSS in their CODE-only producer.
The scoped compiler sets `TH03_BOMB_EXTERNAL_STORAGE`
per corresponding **actual** character source.
The frozen unchanged-source control `af681b`
proved all four objects before edits, avoiding the
previous Ellen-only wrapper bug.

The original Borland compiler-generated **OMF COMENT
source/header dependencies** prove the compiler read the
current modified staged C++ and maintained packed BOSS/
Extra Attack headers. The independent reviewer compares
both full original source/native OBJ rounds and all
actual source input snapshots. Shared background
`phase.inl` is likewise bound to the current source.

## Full MAIN two-round native integration

The affected current gameplay graph was newly compiled
as **47 full original physical translation units in two
independent Turbo C++ 4.02 rounds**, with the other 52
original project objects and original startup/CRT
libraries reused unchanged. Original full normal
TLINK links all 99 project objects.

Both compiled object vectors reproduce every byte of
the original CODE and initialized DATA payloads,
**5,487 literal ordered native FIXUPP fields**,
**314 PUBLIC offsets** and original complete segment
and BSS definitions. Both normal full MAIN EXEs and
complete path-normalized MAPs match the retained
after596 original source-native baseline.

Both Japanese loaded program images match the
original **124,642 bytes** and **1,553 ordered MZ
relocations**. A separate standard DOS MZ serialization
reproduces the original **130,882-byte Japanese MAIN.EXE**
in both rounds without confusing modern TLINK header
provenance with original historical source identity.

Scoped command (stage must be fresh if re-run):

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af686a --units b_chiyu,b_kana,b_koto,b_rika,chain1,chain2,cs_mari,effects,warning,cs_kana,cs_rika,cs_mima,cs_reimu,cs_ellen,b_ellen,cs_chiyu,cs_koto,p_cpu,cs_yume,ba_chiyu,ba_kana,ba_koto,ba_ellen,ba_rikak,ba_yumem,ba_mima,ba_reimu,ba_maris,ba_sring,ba_srest,ex_yume,ex_mima,ex_rika,ex_rfly,ex_reup,ex_ellen,ex_koto,ex_chyu,ex_maris,ex_kana,e_fireb,e_expl,bullet,eforna,efornb,eupda,eupdb
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af686a

Retained actual compiler/linker/OMF/native evidence:
`.analysis/work/exatt-layout-af686a/report.json`,
SHA-256 `8595e718ead526989a2b1307a5df7c04d11e0fd32368fd1cb131cb5ebba3013e`.
Both rounds' **94 freshly produced real OBJ files**,
compiler/linker logs, current C++ source/header overlays,
complete EXEs/MAPs, original linker response files and
independent Japanese standard-MZ serialization are
preserved under ignored evidence storage.

**Honest acceptance boundary:** All 54,741 original
CODE bytes in this joint proof were already source-owned
and must NOT be counted as newly accepted Factory
canonical packed-file bytes. Historic original raw vendor
OMF packet identity, complete pristine packed-game
provenance, Factory whole-product source acceptance
and physical PC-98 runtime remain separately unproven.
