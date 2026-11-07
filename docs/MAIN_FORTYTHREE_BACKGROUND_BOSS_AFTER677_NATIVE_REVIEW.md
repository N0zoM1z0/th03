# TH03 MAIN: 43 original BOSS/background/charged-shot native source owners (after677)

This is a fresh **two-round original Turbo C++ 4.02 compiler and
complete full MAIN TLINK integration** of the latest maintained
C++ sources. This is not reuse of the after670 41-object proof
or a full cold replay of 99 project objects.

## Current original physical source scope

| Original source family | Complete TUs | Original CODE | Literal ordered FIXUPPs | PUBLICs |
| --- | ---: | ---: | ---: | ---: |
| Nine complete major character BOSS controllers | 9 | 17,451 | 2,434 | 85 |
| Shared BOSS ring and seven-function core | 2 | 949 | 106 | 8 |
| Ten complete Extra Attack/shared-flight producers | 10 | 8,781 | 563 | 52 |
| Bullet, Fireball, Explosion and four Enemy owners | 7 | 8,195 | 582 | 50 |
| CPU and Yumemi charged-shot/Gauge | 2 | 2,722 | 197 | 14 |
| Ellen charged-shot/Bomb, Chiyuri/Kotohime charged-shot | 4 | 4,254 | 460 | 31 |
| Kana/Rikako/Mima/Reimu charged-shot/Gauge | 4 | 5,357 | 542 | 40 |
| Marisa GRCG charged-shot/Gauge | 1 | 1,509 | 152 | 9 |
| Player explosion effects and warning/Gauge | 2 | 2,188 | 158 | 12 |
| **New background Chain 1** | **1** | **695** | **43** | **6** |
| **New background Chain 2** | **1** | **550** | **43** | **3** |
| **Total** | **43** | **52,651** | **5,280** | **310** |

## Current maintained source changes in this exact native link

- Chain 1 six-function player background: original 48-particle
  initializer's sprite RNG parity is expressed as natural
  `static_cast<unsigned int>(irand())%2`, with original
  byte-for-byte codegen; its near wrapping/pixel helpers
  and two huge drawing state machines remain hardware/ABI-bound.
- Both shared background Chain periodic controllers now use
  original-native unsigned C++ `%4096` frame cycle, `%8`
  phase increment and `%4` phase decrement clocks. Their
  `(frame&127)<64` direction phase and intentionally
  indeterminate local `changed` behavior stay original:
  modulo-128 changed real TC4 CODE and was rejected.
- Chain 2 three-function player background: native
  `irand()%TO_SP(640)` and `%TO_SP(400)` spawn coordinates,
  meaningful physical 50-particle pool/40 special sprite
  partition. Collapsed ternary sprite selection and
  `round_frame>=145UL` rendered native-different
  code, so their original branches remain.
- Kana full nine-function BOSS: large entry-ring radius uses
  `(boss_frame*2)*16`; four-cel sprite animation uses
  natural `((boss_frame/4)%4)*32*0x28` in the **actual
  two-stage 16-bit operation order**. Flattening the scale
  to a single `*1280` was native-unequal.
- Yumemi full nine-function BOSS: all four arrival sprite
  scale paths use natural two-stage `(frame*8)*16`
  C++, replacing paired shifts. A collapsed `*128`
  emitted original-unequal machine instructions and
  was rejected.
- Reimu full nine-function BOSS: entry radius uses
  natural `boss_frame*32` in its single-stage case;
  both rendering leaves express four-cel and alternate
  frame selection as explicitly unsigned `anim%4`
  and `anim%2`. The large orbit's separately
  verified two-stage calculation remains unflattened.

Each changed source was compiled through a forced per-round
current-source wrapper. The original Borland OMF COMENT
dependencies confirm the actual modified C++ source, current
packed BOSS/Extra Attack headers where consumed and, critically,
the **current shared background phase.inl file in both Chain
physical compilation units**. Independent read-only review
checks all staged source and header identities. Neither
original targets nor frozen native ancestors were patched.

The original `chain1.obj` and `chain2.obj` reside in the
real original linker response under `obj/`, **not**
`obj/th03/`. This real physical ownership and DOS
backslash linker response were corrected in the scoped
compiler and reviewer before accepting new source.
The original complete MAP module identities are
`src/main/background/chain1.cpp` and chain2.cpp.

## Two genuine 16-bit native compiler/TLINK rounds

The scoped builder freshly recompiled only the **43**
affected/relevant complete physical source objects in
each of two independent original TC4 rounds. The other
**56** original project objects, C0 startup and CRT
libraries were reused unchanged; **no full cold replay**.

Both new object vectors reproduce every original CODE
and initialized DATA payload byte, **all 5,280 literal
ordered native fixup fields**, **310 original PUBLIC offsets**,
and complete original OMF segment/initialized/BSS definitions.
Both complete normal linked MAIN EXEs and path-normalized
complete MAPs agree with the retained source-native parent.

Both Japanese loaded program images match the original
124,642 bytes, with every one of the 1,553 ordered MZ
relocations intact. Independent standard MZ serialization
reproduces the complete 130,882-byte original Japanese
MAIN.EXE in both rounds. The newly generated normal
TLINK header is not called the original historical header.

Command to reproduce this **scoped** work (fresh stage required):

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af677a --units chain1,chain2,cs_mari,effects,warning,cs_kana,cs_rika,cs_mima,cs_reimu,cs_ellen,b_ellen,cs_chiyu,cs_koto,p_cpu,cs_yume,ba_chiyu,ba_kana,ba_koto,ba_ellen,ba_rikak,ba_yumem,ba_mima,ba_reimu,ba_maris,ba_sring,ba_srest,ex_yume,ex_mima,ex_rika,ex_rfly,ex_reup,ex_ellen,ex_koto,ex_chyu,ex_maris,ex_kana,e_fireb,e_expl,bullet,eforna,efornb,eupda,eupdb
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af677a

Retained report:
`.analysis/work/exatt-layout-af677a/report.json`,
SHA-256 `f67c9055d248af5e278c08f460e2a0bcdde3a203ce18a9037bf575694278e5df`.
Preserved ignored native evidence includes all 86
fresh original OBJ files, both full EXEs/MAPs, original
TLINK responses, independent MZ serializations, current
compiler-consumed source/header overlays and all native
compiler/linker writer logs in both rounds.

**Honest boundary:** The 52,651 CODE bytes in this proof
were already source-owned original target bytes. This
is original compiler-exact natural C++ and physical
source ownership progress, **not** 52,651 new canonical
Factory packed-game accepted bytes. Raw historical
vendor OMF packet-byte identity, pristine packed-game
provenance, full canonical Factory acceptance and
actual PC-98 runtime behavior remain separate unproven
requirements.
