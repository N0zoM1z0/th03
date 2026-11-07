# TH03 MAIN after792: nine live original physical C++ sources compiled and linked together

After789 recovered the large result scoreboard using native C++ `%8`
and documented all signed-long score multipliers, and after791 recovered
Kotohime's **complete major BOSS** signed orbit/burst geometry and native
`%4` sprite-flicker clock, this stage strictly recompiles **all nine**
affected/verified original physical TC4 source owners *in the same complete
MAIN link*, not just a sum of isolated objects:

| Original physical object | Scope | Original CODE | Ordered OMF FIXUPPs | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| `ba_reimu` | Full major BOSS, signed orbit angles | 2,020 | 270 | 9 |
| `b_kana` | Full Kana Bomb byte-timed phase machine | 526 | 53 | 1 |
| `entry` | Main entry, full 200+-line frame scheduler, stage/score (four live `.inl` sources) | 3,050 | 433 | 8 |
| `ba_mima` | Full major BOSS, genuine unsigned `%2/%4` clocks | 1,922 | 277 | 9 |
| `hitbox` | Full shot/bomb/boss collision damage | 266 | 33 | 1 |
| `hitcirc` | HitCircle enemy/player spawn/update, sprites and clipping | 445 | 30 | 4 |
| `shots` | Entire shot creation, flight and rendering (two live `.inl` sources) | 449 | 17 | 3 |
| `results` | Full naturally recovered match/scoreboard/bonus renderer (two live `.inl` sources) | 1,060 | 89 | 3 |
| `ba_koto` | Full Kotohime major BOSS, signed-angle/radial/intro and `%4` render | 1,840 | 262 | 11 |
| **Nine simultaneously recompiled original owners** | | **11,578** | **1,464** | **49** |

## One-byte native control failure resolved instead of hidden

The first nine-owner trial **`af792a`** correctly rejected a pending
natural-C++ experiment in `src/main/collision/hitcircle.cpp`:
`_DX &= 1` lowered as `83 E2 01`, a **three-byte `AND DX,imm8`**, while
the genuine original TU uses `81 E2 01 00`, a **four-byte `AND DX,imm16`**
from the original `asm { and dx, 1 }` after `_DX = round_or_result_frame`.
These are semantically equivalent for 16-bit DX but **not** binary exact.
The original inline assembler was restored, with the real native negative
control documented at the actual call site. No padding/NOP or target byte
substitution was applied. Other preserved register/segmented ABI idioms in
the complete BOSS, Bomb and collision originals likewise remain intentional.

## Genuine original TC4 4.02 and TLINK, not full cold replay

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af792b --units ba_reimu,b_kana,entry,ba_mima,hitbox,hitcirc,shots,results,ba_koto
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af792b
.venv/bin/python -m unittest discover -s tests -p test_main_source_overlay_inline_contract.py -q
```

The **two genuine independent original TC4 compile/full normal MAIN TLINK
rounds** reproduce all 11,578 original CODE bytes, 1,464 ordered literal
OMF FIXUPP fields, 49 PUBLIC offsets, original physical segments and
source/header/implementation COMENT dependencies and complete normal MAIN
EXE and MAP. The full **124,642-byte Japanese loaded program** and **1,553
ordered original MZ relocations** match; the independently checked standard
DOS MZ serializer reproduces all original **130,882 Japanese MAIN.EXE
bytes**. The other **90 original project objects and original CRT were
reused**, unchanged; no full source/object cold replay occurred.

The source-bound two-round report is
`.analysis/work/exatt-layout-af792b/report.json`, SHA-256
`979077bc49e34d180be1e1c1eb67bbe447c7d2efc3af3b3a6ade88682e84c615`.
The actual native source snapshots, `.inl` dependencies, object bytes,
compiler outputs, linker responses, EXE and MAP are retained under
protected ignored `.analysis/work/exatt-layout-af792b` and native Wine
stage directory `probe/af792b`. The earlier `af788c` is a **historical
source snapshot** and no longer a live-checkout review target because
`results` source changed after its evidence was recorded. Preserve it;
use `af792b` for this exact current checkout instead.

The nine owners were covered in older historical experiments; these
11,578 bytes are a **single current-source native overlap**, **not**
11,578 new distinct target bytes. Raw historical vendor OMF metadata,
whole-game rebuilt ownership and canonical Factory packed-game acceptance
remain **unproven**, as does the separate original BIOS `input_s` linker
one-NOP gap. No canonical packed-unit score is incremented by this pass.
