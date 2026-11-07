# TH03 MAIN after709: five actually rebuilt original sources, 58 distinct source-proof owners

This is a fresh, independent two-round original **Turbo C++ 4.02
compiler and full normal MAIN TLINK** integration of only the
five complete original physical translation units whose maintained
product C++ changed this session. It is **not** a 58-object
recompile and does not repeat the full project cold replay.
The other 94 original project objects and original startup/CRT
libraries were reused unchanged.

## Actual modified, freshly rebuilt original native object scope

| Original physical source owner | CODE bytes | Ordered literal native FIXUPPs | PUBLIC offsets |
| --- | ---: | ---: | ---: |
| `ba_kana` — nine-function Kana major BOSS | 1,874 | 274 | 9 |
| `ba_sring` + `ba_srest` — shared BOSS ring and seven controller helpers | 949 | 106 | 8 |
| `core` — large player core with all ten Hyper handlers | 3,135 | 260 | 21 |
| `lose` — four loss/particle/winner state/render functions | 664 | 61 | 4 |
| **Five physically rebuilt original TUs** | **6,622** | **701** | **42** |

The modified product files are **exactly six**:

    src/main/boss/kana.cpp
    src/main/boss/shared.cpp
    src/main/player/hyper.inl
    src/main/player/lose_update.inl
    src/main/player/losedraw.inl
    src/main/player/defeat.inl

The maintained shared BOSS source compiles into two different
physical original TUs. The core and loss functions reside in
real maintained `.inl` implementation files, rather than in
their short top-level `.cpp` include aggregators.

## Real C++ progress and tested negative controls

- **Kana major BOSS:** sixteen-shot attack emission and its
  full sixteen-sprite arrival renderer use natural prefix
  `++i`, as do its RNG parity, BOSS-hit/character-state
  and intro blink Boolean checks. Direct typed field writes
  replacing the original four-way AL rotation selector
  changed TC4 CODE and were rejected (`af704d`).
- **Loss and winner rendering:** natural unsigned `%32`
  winner-bounce period, natural unsigned `%2` alternating
  palette pulse and `if(!lose_anim_time)` completion
  gate; the three loss-particle rings use the original
  DI loop register with natural `++_DI`. A typed
  `%4` replacement for the mutable 8-bit shake
  mask changed original CODE and was rejected (`af706h`).
- **Complete player core/Hyper dispatcher:** Ellen Hyper
  reads the low byte of `round_frame` via natural
  `static_cast<unsigned char>(round_frame)` rather
  than a manual near-pointer reinterpretation, retaining
  the original `&3` instruction. Nine-character
  cardinal/diagonal Hyper motion steps and Rikako's
  strict `>0xFA0` threshold now have compiler-time
  names. Natural `%4` and `>=0xFA1` alternatives
  failed native exactness and were rejected (`af707e`).
- **Shared BOSS ring and controller:** both 16+8-sprite
  explosion ring loops use natural `++i`, and the
  explosion completion checks `if(!boss_mode)`.
  Prefix BOSS angle/pattern-byte increments and
  `if(pid_current)` rather than the original PID==1
  changed actual native CODE; all were restored (`af708f`).

## Correct source provenance and physical linking

The actual full MAIN source-backed parent uses
`probe/af593p/rN/core.obj` for the original `core`
physical object, while `lose` uses the original
`obj/th03/lose.obj` and its actual
`src/main/player/lose.cpp` MAP module. The native
scoped compiler and independent reviewer now force the
current maintained `hyper.inl`, `lose_update.inl`,
`lose_particle.inl`, `losedraw.inl` and `defeat.inl`
through per-round original DOS source overlays.
Each staged `.inl` file has a live SHA identity check,
a verbatim byte snapshot and a mandatory matching emitted
Borland OMF COMENT source dependency. The current packed
BOSS template header is independently checked for the
shared/Kana BOSS sources. The other unchanged implementation
includes in `core` are reused; their live source was not
claimed to have been modified in this session.

All previously accepted original compiler object/target and
native writer evidence remains unmodified. The v1 stale
`TH03WORK/src` false-positive source-copy problem cannot
validate these current altered `.inl` paths.

## Fresh two-round source-native compiler/full MAIN link

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af709a --units ba_kana,ba_sring,ba_srest,core,lose
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af709a

Both independently compiled original TC4/TLINK rounds reproduce
**all 6,622 original CODE bytes, 701 literal ordered native
FIXUPP fields and 42 PUBLIC offsets**, complete original OMF
segment and BSS metadata, both full normal MAIN EXEs and
path-normalized complete MAPs. The Japanese loaded game image
matches all **124,642 bytes with 1,553 literal ordered MZ
relocations**. Independent standard DOS MZ serialization
reproduces every byte of the original **130,882-byte
Japanese MAIN.EXE** in both rounds.

Full retained original-source and native writer evidence:
`.analysis/work/exatt-layout-af709a/report.json`,
SHA-256 `e47cac88a3ce162a4dab2fb8e238ee89a9ff19a15b7d66e6565a684d6fee628d`.
All ten new native OBJ files, per-round actual source/header
overlays, native compiler/linker logs, complete linker
responses, full EXEs/MAPs and independent Japanese MZ files
are preserved outside Git.

## Accurate cumulative accounting, not new Factory credits

The earlier after703 source-proof union covered **56 distinct
original full physical TUs**, 62,608 already source-owned CODE
bytes, 6,982 ordered native fixups and 342 PUBLICs. This
session added **two new distinct full physical source owners**,
`core` and `lose`, for another 3,799 CODE bytes,
321 original fixups and 25 PUBLICs, and freshly revalidated
three previously owned but edited BOSS physical objects.
The **union across separate current and frozen proofs**
therefore now covers **58 distinct complete original TUs**,
**66,407 previously source-owned CODE bytes**,
**7,303 ordered native fixups** and **367 PUBLICs**.

These 58 cumulative figures are **not** a fresh 58-object
compile and are **not new canonical Factory packed-game
accepted bytes**. Historic raw vendor OMF packet byte
identity, pristine packed-game provenance, complete
canonical Factory whole-product acceptance and actual
PC-98 hardware/runtime behavior remain separate unproven
claims. The current session only freshly recompiled the
five original objects listed above.
