# TH03 MAIN after703: seven actually rebuilt original owners, 56-owner source-proof union

This is a fresh original Turbo C++ 4.02 and whole normal MAIN TLINK
**two-round native integration of ONLY the seven original physical
translation units whose product C++ changed this session**. It is not
a replay of the already proved 51-object graph. The historical normal
MAIN linker response reused the other **92 original project objects**
and startup/CRT libraries without recompiling or patching any
original binary.

## Seven genuinely rebuilt current-source originals

| Original physical source owner | Complete CODE bytes | Ordered literal FIXUPP fields | PUBLIC offsets |
| --- | ---: | ---: | ---: |
| `ch_setup` — nine character callbacks/resource loader | 3,888 | 1,135 | 12 |
| `p_combo` — Combo raw scoring and large HUD update | 491 | 17 | 2 |
| `p_cmbhl` — Combo fireball/BOSS/panic helper functions | 487 | 40 | 3 |
| `p_exatt` — Extra Attack character callback leaf | 41 | 2 | 1 |
| `p_gauge` — saturating Gauge increment leaf | 55 | 1 | 1 |
| `ba_koto` — complete Kotohime BOSS/attack/render source | 1,840 | 262 | 11 |
| `ba_chiyu` — complete Chiyuri BOSS/attack/render source | 2,654 | 381 | 11 |
| **Actually rebuilt in after703** | **9,456** | **1,838** | **41** |

The six product source files that actually changed are exactly:

    src/main/player/character_setup.cpp
    src/main/player/combo.cpp
    src/main/player/exatt.cpp
    src/main/player/gauge.cpp
    src/main/boss/kotohime.cpp
    src/main/boss/chiyuri.cpp

The maintained `combo.cpp` compiles into two *different* original
physical objects and both are independently freshly verified.

### Real source recovery and negative experiments

- Character callbacks/resource loader: all nine character MRS
  odd-numbered resource IDs have natural compiler-time C++ names;
  the shared twelve-byte filename copy uses `++i`, the nine player
  selectors use `if(!pid)`, and decimal ones-place assignment is
  explicit. An unsigned modulo-2 rewrite of the original
  palette-bit test was native-unequal and rejected (`af695c`).
- Full Combo scoring/HUD and chained-fireball/BOSS/panic helpers:
  native-exact player/pointer preincrements, zero-state checks,
  explicit decimal remainder and natural four-frame blink modulo;
  physically meaningful 12/5120/30000/3 thresholds. The original
  timer postdecrement, bitwise `&` predicate and temporary hit
  maximum copy are retained after actual native-unequal alternatives,
  as is the original near/far fireball call boundary (`af698c`).
- Small Gauge and Extra Attack leaves: natural split early returns
  for the 16-bit Gauge saturation helper and `if(!pid)` character
  callback dispatch. Combining the original Gauge addition with a
  comparison, or deleting Extra Attack's Subpixel argument copies,
  was native-unequal and rejected (`af700c`).
- Kotohime complete major BOSS: natural byte-state tests and standard
  prefix loop iteration in complete random/aimed/radial attack and
  sprite renderers. Replacing the original AL-mediated ring phase +2
  with a typed direct byte field write was native-unequal
  (`af701e`).
- Chiyuri complete major BOSS: natural nonzero phase/render checks,
  natural prefix iteration in the four separate fan volley loops and
  the full ring renderer. Replacing the original mutable
  `boss_render_frame &= 3` with `%= 4`, or converting its byte
  countdown to prefix decrement, changed actual native code and
  were rejected (`af702e`).

The genuine compiler emitted Borland **OMF COMENT source/packed-header
dependencies** attesting the actual modified current C++ inputs.
Independent read-only review checks complete CODE/initialized DATA,
ordered literal FIXUPPs, PUBLIC offsets, OMF segment/BSS definitions
and entire linked MAIN/MAP per physical original compiler unit.
The original character setup's linker slot is
`probe/af592p/rN/ch_setup.obj`, **not** a fabricated generic
`obj/th03/ch_setup.obj` source-link input. The original Combo split
has six MAP module ownership rows per physical TU; Gauge and Extra
Attack each have only three. These real physical facts were
established in independent unchanged-source controls before
accepting the current edits.

## Two actual fresh native compiler/full-link rounds

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af703a --units ch_setup,p_combo,p_cmbhl,p_exatt,p_gauge,ba_koto,ba_chiyu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af703a

Both genuine original native compiler/TLINK rounds match **all
9,456 CODE bytes, 1,838 literal ordered native fixup fields,
41 PUBLIC offsets**, and complete initialized/segment metadata.
Both normal complete MAIN EXEs and path-normalized whole MAPs equal
the retained source-native original. Both original Japanese loaded
program images match all **124,642 bytes and 1,553 ordered MZ
relocations**. Independent standard DOS MZ serialization reproduces
the entire **130,882-byte original Japanese MAIN.EXE**.

Retained complete current-source and original native writer proof:
`.analysis/work/exatt-layout-af703a/report.json`,
SHA-256 `a27177371b79be97c1f69ab7a8ec290b6113f5d8e92f22d6720588d576e4a197`.
This ignored proof retains fourteen new complete raw OBJ outputs,
two compiler/TLINK log sets, source/header overlays, linker response
files, full EXEs/MAPs and two original-equal independent MZ outputs.

## Honest cumulative scope, not a new 56-object compile

The previous original-current-source union, after693, covered **51
distinct full original TUs**: 57,646 existing source-owned CODE bytes,
5,787 ordered literal native fields and 323 PUBLIC offsets. This
session added **five previously unselected original physical owners**
(`ch_setup,p_combo,p_cmbhl,p_exatt,p_gauge`) and reverified the two
already-owned but newly edited Kotohime/Chiyuri BOSS objects.
The unchanged earlier 49 source owners retain their complete original
source/native receipts.

The union therefore covers **56 distinct complete original TUs,
62,608 original CODE bytes, 6,982 ordered literal native fields and
342 PUBLIC offsets**, across original source-backed receipts.
**Only seven physical TUs were freshly recompiled in after703**.
Do not misreport the union as a fresh 56-object compiler run and do
not double-count previously tracked target bytes as newly accepted
canonical Factory packed-game credit. Historic raw vendor OMF packet
byte identity, pristine packed-game provenance, complete canonical
Factory acceptance and real PC-98 runtime remain separate unproven
requirements.
