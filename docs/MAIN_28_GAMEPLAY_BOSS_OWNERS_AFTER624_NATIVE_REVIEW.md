# MAIN twenty-eight native gameplay/BOSS C++ units (after624)

This proof recompiled the **real current modified source** of 28 complete
Turbo C++ translation units together, not 28 isolated functions or an
unchanged historical compiler snapshot. The stage expands the genuine
after622 26-object BOSS/Extra Attack/Bullet/Enemy/Fireball/Explosion link
with both physical shared-BOSS producers:

| Source family | Native original TUs | CODE bytes | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: | ---: |
| Nine character BOSS controllers | 9 | 17,451 | 2,434 | 85 |
| Ten Extra Attack / shared flight producers | 10 | 8,781 | 563 | 52 |
| Bullet, Fireball, Explosion, four Enemy producers | 7 | 8,195 | 582 | 50 |
| Shared boss ring and seven-function controller | 2 | 949 | 106 | 8 |
| **Combined** | **28** | **35,376** | **3,685** | **195** |

The shared-BOSS source contains a full 348-byte ring and a 601-byte core
with BOSS movement, launch, lifetime, target selection, pattern scheduler
and hit termination. Common motion, despawn, wait and reward constants
are now named natural C++ enum expressions. In the major character BOSS
renderers, signed AX register expressions compile the actual original
SAR instruction. The Extra Attack source includes a byte-packed shared
32-byte per-character entity; the Explosion source includes normal C++
saturating-chain and collision/bonus handling.

Native execution:
`scripts/probe_th03_main_exatt_layout.py --stage af624a` with the 28
original units, followed by
`scripts/review_th03_main_source_overlay.py --stage af624a`.
**Two independent original Turbo C++ 4.02/TLINK rounds** compiled all
28 physical project objects from explicitly rooted per-round source
wrappers. Their emitted OMF COMENT source-dependency paths were
independently checked against the staged current C++ and shared header.
The other 71 original project objects and existing C0/CRT libraries
were reused unchanged; no full cold replay was performed.

The final read-only reviewer proves complete original source-produced CODE
and the Fireball's single initialized DATA byte, every ordered native
fixup field, 195 PUBLIC offsets and segment/BSS metadata, both normal
full 99-object MAIN EXEs and complete normalized MAPs, the original
124,642-byte loaded Japanese program and **1,553 ordered MZ
relocations**. The separately reviewed standard DOS MZ serializer
reproduces all 130,882 Japanese MAIN.EXE bytes.

The retained complete receipt, including all 56 raw object outputs,
two EXEs and MAPs, two independently serialized Japanese MZ files,
per-round response files, source snapshots and 58 native
compiler/linker phase logs, is:

`.analysis/work/exatt-layout-af624a/report.json`

SHA-256:
`7e3fe02ce754fb898dd0264a84352ca1c2766af245441d5327a3fce26335971b`.

A native negative experiment tried replacing the BOSS 32-byte register
and REP MOVSW copy with a natural struct assignment; Turbo C++ emitted a
far F_SCOPY routine instead. Keeping the original inline SI/DI/CX/ES
contract is required. Earlier v1 source-overlay controls remain historical
and cannot be used as changed-source proofs.

This new checkpoint is **not** 35,376 newly recovered packed-file bytes.
It verifies updated original-source output and native linker composition;
it does not establish original vendor OMF packet byte identity,
independent pristine packed-file provenance, physical PC-98 runtime
compatibility or canonical Factory whole-game acceptance.
