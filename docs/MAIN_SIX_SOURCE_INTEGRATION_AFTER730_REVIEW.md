# TH03 MAIN after730: six complete current physical sources compiled together

This is the fresh two-round original Turbo C++ 4.02/TLINK source integration
of **six actual original physical translation units**, consisting of five
modified maintained source owners and the newly directly proved unmodified
CFG resident-loader source. Only these six original objects were rebuilt;
the other **93 original project objects and original CRT** were reused from
the unchanged after596 source-native MAIN parent. There was no full cold
replay or new historical byte patching.

| Physical original TU | Actually compiled source recovery | Original CODE bytes | Ordered native OMF FIXUPPs | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| `core` | Complete player movement/Hyper/hit/damage/charge controller with **10 nested current `.inl` bodies source-bound**; long CPU targeting and charged/BOSS shot state machine | 3,135 | 260 | 21 |
| `ba_rikak` | Major Rikako BOSS: three attack families, full update, orbit/intro renderer, exact bounded-index `i & 3` sprite cycle | 1,677 | 215 | 8 |
| `snd_se` | PMD sound-effect priority and frame expiration, direct array lookup and original byte increment | 120 | 18 | 2 |
| `ba_reimu` | Major Reimu BOSS: cloud/orbit/ring/mirror attacks, full update, two renderer paths, natural unsigned frame masks | 2,020 | 270 | 9 |
| `polar` | Signed 32-bit Q8 polar math, natural `center + scaled` expression | 26 | 0 | 1 |
| `cfg_lres` | Original real-mode resident configuration loader; newly directly proved original physical C++ source, unchanged body | 49 | 6 | 1 |
| **Six original physical source producers together** | | **7,027** | **769** | **42** |

## Actual modified current-source native integration

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af730a --units core,ba_rikak,snd_se,ba_reimu,polar,cfg_lres
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af730a

Both independent native compiler/TLINK rounds reproduced every original
initialized CODE byte, all complete segment/zero-DATA/BSS declarations,
**all 769 literal ordered original OMF FIXUPP fields and 42 PUBLIC offsets**,
source-bound original physical linker slots, the complete normal MAIN.EXE
and path-normalized MAP. The original Japanese **124,642-byte loaded program**
and **all 1,553 ordered MZ relocation words** matched. Independently
serialized standard MZ matched all **130,882 Japanese MAIN.EXE bytes** in both
rounds. The latter is an independent container serialization, not a claim
that TLINK itself historically emitted those exact compact header bytes.

Full retained native writer proof:
`.analysis/work/exatt-layout-af730a/report.json`, SHA-256
`bb1c0ad0f3884d975b0585cbbb1d340513ad44c9ca31be529d7b2b0103715b8f`.
Its ignored but **protected** evidence includes complete original and native
OBJ, source/HDR/.inl snapshots, both real compile/link writer logs, linker
response files, EXE/MAP, normalized Japanese EXE and independent reviewer
input checks. No source snapshots or old native receipts were overwritten.

## Legacy source-provenance regression actually discovered and fixed

The after725 driver *rightly* tightened `core` source verification from just
`hyper.inl` to all **five core.cpp direct includes plus five nested
state.inl includes**. But a new reviewer using that unversioned list on the
historical `af709a` receipt wrongly failed the previously valid
**hyper-only** source-bound proof. We reproduced this failure. The driver
and independent reviewer now select **the original stage-specific binding
contract**: before the after725 upgrade, core source binds `hyper.inl`
only; from after725 onward, it requires all **ten current implementation
sources and their actual compiler-emitted Borland OMF dependency records**.
This never grants a historical receipt more source inputs than it actually
compiled and never weakens the post-upgrade nested binding requirements.

The three independent read-only checks below now all pass without modifying
original evidence. Four focused unit tests in
`tests/test_main_source_overlay_inline_contract.py` verify the historic
single-include guard, required ten post-upgrade includes, and nested
source path rewriting:

    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af709a
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af725d
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af730a

## Source-exactness and progress boundaries

The five changed original producers are **not five newly discovered game
bytes**: `core`, both BOSSes and sound/math helpers were already represented
in old original assets or source candidates. The changed native exact
source is now directly compiler-bound in the scoped workflow. The preceding
**seven-object after724 proof remains separately preserved**: it rebuilt
Marisa/Mima/Ellen BOSSes, full Bullet/intro, and original initmain/static
HUD. Do not combine those two receipt totals as a disjoint byte set or
relabel either as a fresh 13-object run. The historical after709 58-owner
union was not recomputed and no Factory **canonical packed-file unit credit**
changed. Historical vendor OMF raw-packet identity, independent pristine
target provenance, 99-object complete source ownership and MAINL's pending
current decoded source-publication gate remain open.

Negative codegen controls are preserved and never promoted:
`af725c` (compound damage assignment), `af726b` (global BOSS spin prefix),
`af726e` (signed angle unary minus), `af727c` (global sound frame prefix),
`af728c` (Reimu cloud speed prefix) and `af729c` (extra long polar register
local). The original hardware ABI and original-bug semantics were retained.
