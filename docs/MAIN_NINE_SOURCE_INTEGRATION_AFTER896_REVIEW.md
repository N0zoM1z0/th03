# TH03 MAIN after896 — nine genuinely rebuilt original physical sources in one exact native link

This is a **single simultaneous two-round original Turbo C++ 4.02 compiler
and complete normal MAIN TLINK experiment** for every original physical
object modified during this session. The nine original project TUs map
to seven edited maintained files (`enemy.cpp` physically owns four
historical objects; the `results` object includes `results.inl` and
`objects_reset.inl`). Every changed source is bound to its actual
original compiler-emitted OMF dependency; no old native test receipt
was summed or repinned to create a simulated nine-object result.

| Real original physical TU | Complete rebuilt original C++ scope | CODE bytes | Literal ordered native OMF FIXUPPs | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| `eforna` | Enemy formations, load/randomize, first-free allocation and original movement/clip | 729 | 58 | 8 |
| `efornb` | **Full ENEDAT scripted enemy virtual machine** and near velocity/angle helpers | 1,064 | 37 | 4 |
| `eupda` | Original enemy sprite/explosion helper and state update functions | 372 | 24 | 3 |
| `eupdb` | **Full 40-enemy hit/chain scoring, rendering and frame update** | 1,160 | 103 | 4 |
| `e_fireb` | **Full 24-fireball transfer/fall/collision/chain/render engine**, original one-byte DATA and BSS | 1,555 | 115 | 10 |
| `ba_reimu` | Complete **Reimu major BOSS**: three orbit-attack loops, intro/main sprite loops, full scheduler | 2,020 | 270 | 9 |
| `ba_ellen` | Complete **Ellen major BOSS**: 8-shot spread, two RNG radial bursts, nested 4×8 intro, full scheduler | 1,675 | 213 | 9 |
| `b_rika` | Original **Rikako Bomb**: natural 96-pixel explosion row, original palette/quake clocks | 546 | 56 | 1 |
| `results` | Original reset leaf, three-digit formatter and **complete signed 32-bit result/scoreboard** with two source includes | 1,060 | 89 | 3 |
| **Nine actual original physical objects compiled together in each round** | | **10,181** | **965** | **51** |

## Real original native compiler, full normal linker and Japanese program proof

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af896a --units eforna,efornb,eupda,eupdb,e_fireb,ba_reimu,ba_ellen,b_rika,results
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af896a
```

**Two genuinely independent original TC4 4.02 rounds** compiled all
nine complete original physical project TUs **simultaneously**, with
current maintained C++ text and its original compiler-emitted source/
header OMF COMENT dependencies, all original segment/DGROUP geometry,
original DATA/BSS ownership, 16-bit far/near register and calling ABI,
**all 10,181 original CODE bytes, 965 literal ordered native OMF FIXUPP
fields, and 51 PUBLIC offsets** identical to the pinned historical
project objects. Both rounds then used the complete normal historical
MAIN TLINK response in its original order, matching the entire
normal original MAIN EXE and normalized MAP, **124,642 Japanese loaded
program bytes and all 1,553 ordered MZ relocations**. The independent
reviewed standard DOS MZ serializer reproduced **all 130,882 original
Japanese MAIN.EXE bytes**; this does not independently establish the
original Borland linker’s raw MZ-header byte serialization.

**90 unchanged original game project objects and the Borland CRT reused**
from the original source-native parent. There was **no whole-project
cold replay**, target/object byte patch, NOP padding, altered linker
response order, invented code array, direct original binary read as a
substitute source, or weakening of current-source dependency checks.
Both actual native compiler/TLINK writer rounds, original source
snapshots, OBJ/EXE/MAP, independent MZ, complete response, and writer
logs are retained in the protected ignored receipt DAG:
`.analysis/work/exatt-layout-af896a/report.json`, SHA-256
`a06ec583d9f6f2bec02e961d602677b6112779d7f2af03f9221bcb06ae261050`.

## Real codegen negative controls and honest current-source snapshots

The accepted maintained C++ contains real **natural 40-enemy update,
ENEDAT interpreter, 24-fireball collision/transfer, five Reimu orbit,
Ellen 4×8 sprite, Rikako Bomb and shot/Enemy reset loops**, while
retaining compiler-sensitive first-free allocators, original near-call
carriers, byte frame postfix, signed division, original uninitialized
formation RNG `prev`/fireball collision `chain_slot`, and original
byte-animation masks. Every rejected form was actually compiled: the
Enemy and Fireball first-free allocators changed native CODE after
rewriting to `while`; signed height `>>5`, mutable byte prefix,
Ellen `byte += enum` and `%4`/`&3` bit-clock substitutions were also
rejected. In Ellen, **`byte = byte + named enum` was independently proven
native exact**, rather than treating old enum codegen failures as a
universal prohibition. Rikako’s distinct byte shake mask and results’
original 32-bit `>65535UL` boundary were retained by actual native
compiler comparison, not just by semantic guessing.

**Current source binding was rechecked now**, not inferred from older
handoff prose. The independent `af889a`, `af883a`, `af877a`, `af871a`,
`af865a`, `af859a`, and `af853a` still pass read-only source-bound
review for their separate other currently unchanged physical owners.
Earlier genuine `af847a` (Reimu/Enemy source), `af843g` (Enemy source),
`af842a`/`af840a` (older Kana source), and `af835a` (older Marisa BOSS
source) **now fail current maintained-source hash binding**. They remain
authentic **historical** two-round writer receipts, not current-checkout
source proofs. Do not fabricate an all-object replay by summing these
independent experiments or repin/alter their original inputs.

All nine physical original objects had prior historical native source
coverage. **10,181 is a fresh current source/compiler scope, not 10,181
new distinct game CODE bytes or canonical packed Factory acceptance**.
Historical raw vendor OMF packet identity, full original source text
ownership, the separate BIOS `input_s` one-NOP parent link gap and
canonical packed-file Factory acceptance remain open.
