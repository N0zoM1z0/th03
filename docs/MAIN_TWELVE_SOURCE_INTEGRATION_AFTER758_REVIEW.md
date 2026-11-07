# TH03 MAIN after758: twelve current physical sources rebuilt together, original-native

This is the **latest genuinely executed, simultaneous two-round original
Turbo C++ 4.02 / full normal MAIN TLINK source-attested proof** for the
currently maintained source of twelve complete original physical game
translation units, including **three major BOSSes**, the complete
Fireball, Ellen/Kotohime Extra Attacks, explosion-chain collision,
Combo HUD/BOSS-panic, Ellen Chargeshot and both Extra Attack/Gauge leaf
owners. All are real original physical objects, not fabricated function
slices. The **remaining 87 original project objects and Borland CRT**
were reused unchanged from the source-native after596 normal MAIN parent,
not recompiled or replaced by a full cold replay.

| Original physical source | Actually compiled maintained C++ scope | Initialized CODE bytes | Ordered native FIXUPPs | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| `ba_chiyu` | **Large Chiyuri BOSS**, four attack families, whole controller, palette and ring/intro render, native exact signed shifts | 2,654 | 381 | 11 |
| `e_fireb` | **Full Fireball** spawning/transfer/explosions, hit/chain and renderer; original one initialized DATA byte and BSS byte retained | 1,555 | 115 | 10 |
| `ba_maris` | **Large Marisa BOSS**, ring/columns/spread controller and native C++ split renderer | 1,431 | 199 | 9 |
| `ex_ellen` | **Full Ellen Extra Attack**, twelve slots and seven-point history/trail, collision and renderer | 1,129 | 79 | 6 |
| `e_expl` | **Entire explosion/chain hit-test**, named original charge/bonus tiers and natural hit counter | 630 | 49 | 1 |
| `ba_mima` | **Large Mima BOSS**, spread/random/trail/orbit/update and native SI/DI split renderer, explicit correct target-ID reevaluation | 1,922 | 277 | 9 |
| `ex_koto` | **Full Kotohime Extra Attack**, eight-function lifecycle, 4/10-projectile emitters, original-byte modulo and renderer | 1,054 | 100 | 8 |
| `p_combo` | Original **Combo score/HUD** two-function source partition, natural blinking mask and 16-bit score ABI | 491 | 17 | 2 |
| `p_cmbhl` | Original separate **BOSS/Panic/Fireball combo** three-function physical partition | 487 | 40 | 3 |
| `cs_ellen` | **Ellen Chargeshot**, ten functions: homing/Hyper/Gauge plus sprite leaf now using natural C++ SI/DI register locals instead of manual `_SI/_DI/_AX` writes | 1,530 | 169 | 10 |
| `p_exatt` | **Extra Attack callback leaf**: direct natural two 16-bit Subpixel `.v` locals and original Pascal function pointer calls | 41 | 2 | 1 |
| `p_gauge` | **Gauge saturation leaf**: original 16-bit increment/overcap ABI, no false codegen simplification | 55 | 1 | 1 |
| **12 original physical source owners, genuinely compiled together** | | **12,979** | **1,429** | **71** |

## Fresh actual original compiler, OMF and full native link

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af758a --units ba_chiyu,e_fireb,ba_maris,ex_ellen,e_expl,ba_mima,ex_koto,p_combo,p_cmbhl,cs_ellen,p_exatt,p_gauge
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af758a

Each of **two separately performed original Turbo C++ 4.02/TLINK rounds**
reproduced every original initialized **12,979 CODE byte**, original
Fireball initialized DATA and BSS ownership, **all 1,429 ordered literal
OMF FIXUPP fields and 71 PUBLIC offsets**, original OMF segments and
native compiler-emitted source dependency COMENT fields. The complete
normal source-native MAIN EXE and normalized MAP match. The original
Japanese **124,642-byte loaded program** and all **1,553 ordered MZ
relocation words** match. An independent standard DOS MZ serializer
produced a byte-for-byte match to the **130,882-byte original Japanese
MAIN.EXE**; this **does not** mean the historical TLINK direct MZ header
was identical to the serializer's file container.

The independent current-source review receipt:
`.analysis/work/exatt-layout-af758a/report.json`, SHA-256
`c3cdb9cc0d715b8e91ed1e1e053796d191e017abb0dec7fddeeb9bf5a895bc56`.
Its protected ignored evidence includes both real writer rounds,
physical original and new OMF OBJ, native compiler consumed source and
headers, compiler/log/COMENT source checks, full original linker
response/EXE/MAP, compact Japanese MZ and original Japanese targets.
No original target bytes, compiler objects or outputs were hand-patched;
no historical evidence stage was overwritten or repinned.

## Genuine natural C++ recovery and negative experiments

The newly source-recovered **Ellen Chargeshot sprite renderer** is the
most significant natural C++ improvement here: two ordered typed
`register` locals cause original TC4 to allocate SI/DI and emit original
AX shift/masked sprite code, replacing explicit `_SI`, `_DI` and `_AX`
source assignments without any target instruction injection. Reversing
the declaration order was actually compiled and **failed** whole-object
CODE equality (`af752d`). The original BOSS/Extra Attack/Combo/Gauge
source trials independently confirmed further 16-bit compiler quirks:

- Mima opponent-ID local reuse after the shared helper changed original
  code (`af749c`), so the historical recomputation remains.
- Kotohime Extra Attack byte `%4` cannot be replaced with `&3`
  (`af750a`), and its mutable `p->angle++` cannot be prefix (`af750c`).
  Correct eight-function lifecycle and index recovery passed `af750d`.
- Combining original signed **32-bit Combo score widening and addition**
  in one initialization changed CODE (`af751c`). Two stage-local
  expressions remain, while natural HUD frame mask passed `af751d`.
- Gauge `p.gauge_avail += charge` cannot be replaced with an explicit
  assignment (`af753b`); original memory update remains. Extra Attack
  argument wrappers now use direct `.v` word field loads (`af753d`).

All negative trials preserve real source and compiler outputs, and none
is counted as accepted native-source or canonical Factory byte credit.
Separate previously retained after748 five-source, after751 seven,
after752 nine, and after753 ten-source **original source-bound two-round
receipts** also pass independent review of this checkout and are archived
for provenance; do not add their byte totals to after758 as new distinct
physical ownership.

## Keyboard scanner remains an explicit **nonaccepted** adjacent case

The separate original 417-byte `input_s` keyboard scanner **is not in
these twelve successful original linked TUs**. Real natural C++ input
scanner compiled byte-exact at the original OBJECT, but the frozen
MAIN parent used an experimental **418-byte** object with one extra
0x90 trailing NOP, creating a **one-byte full linked MAIN difference**.
`PYTHONPATH=scripts .venv/bin/python scripts/review_th03_input_s_link_gap_after744.py`
correctly returns `normal_MAIN_exact=false`. It was not padded,
patched, silently accepted or included in the after758 original-link
success. See `docs/MAIN_INPUT_S_LINK_GAP_AFTER744_REVIEW.md`.

The source-native compiler/full link proofs are **not** proof of
historical raw vendor OMF packet identity, independent pristine targets,
whole-product 99-object source ownership or Factory canonical packed-game
accepted units. Earlier source-backed byte counts include overlapping
original game CODE; after758 is a simultaneous *affected-scope* proof,
not a fresh fully cold-replayed or independently deduplicated 99-TU
accepted product.
