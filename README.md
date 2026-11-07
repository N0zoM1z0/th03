# 東方夢時空 ～ Phantasmagoria of Dim.Dream

<p align="center">
  <img src="resources/title-screen.png" width="640" alt="Original Japanese TH03 title screen">
</p>
<p align="center">
  <img src="resources/progress.svg" alt="TH03 reviewed reconstruction scopes">
</p>

This repository reconstructs the original Japanese PC-98 **Touhou 3:
Phantasmagoria of Dim.Dream**. Work covers OP.EXE, MAIN.EXE, MAINL.EXE (the ending)
and ZUN.COM. Reconstruction and whole-product source acceptance remain open.

[Generated progress](docs/PROGRESS.md) distinguishes canonical packed-unit acceptance from reviewed decoded source and historical source-native build evidence. The historical after587 MAINL native link reproduced the decoded Japanese ending EXE and MAP, but its **live source-bound decoded publication remains pending** after later source changes invalidated an old input guard. That historic result does not grant current or canonical packed-file acceptance. See the [current handoff](docs/RE_HANDOFF.md) for the precise scope and outstanding work.
[The handoff](docs/RE_HANDOFF.md) records the latest verified checkpoint,
remaining work, local state and findings for the next agent. Source-present,
bounded exact source scopes and target-equal complete builds are separate claims;
there is no whole-game completion percentage.

## Navigation

| Area | Entry point |
| --- | --- |
| Product source | [MAIN](src/main/), [OP](src/op/), [MAINL](src/mainl/), [ZUN](src/zun/), [proved shared code](src/shared/) |
| Start/resume work | [AGENTS.md](AGENTS.md), [handoff](docs/RE_HANDOFF.md), [workflow](docs/RE_WORKFLOW.md) |
| Source/build/evidence organization | [Architecture](docs/ARCHITECTURE.md), [script index](scripts/README.md) |
| Acceptance and findings | [Units](config/units.csv), [evidence](config/evidence.csv), [knowledge](config/knowledge.csv), [Oracle gates](config/oracles.toml) |
| Pinned inputs/tools | [Japanese targets](config/targets.toml), [DIET identities](config/th03_diet.toml), [native tools](config/toolchain.toml), [Ghidra/JDK](config/analysis_toolchain.toml) |

## Validate an existing checkout

Use the existing `.venv`, installed tools and game-local Wine prefix.

```sh
.venv/bin/python scripts/preflight.py
.venv/bin/python scripts/status.py
git diff --check
```

Choose one CPU allowed by `os.sched_getaffinity(0)`; do not assume a fixed host
CPU number. Serialize Borland/Wine writers. The [workflow](docs/RE_WORKFLOW.md) lists
affected cold/review/publication commands. Check the changed native scope and
reuse an unchanged cold pair. Full `scripts/ci.py` is available for broad
infrastructure changes; it is not a routine per-unit requirement. Re-attest a
Ghidra database before using its observations.

## Fresh installation

Supply your own legal Japanese copy. Targets, disk images, private tools and
assets stay outside Git. Pinned hashes have **candidate-local-attested** provenance;
independent pristine-dump confirmation remains unknown.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --no-cache-dir -r requirements-ci.txt
mkdir -p _reference
git clone https://github.com/nmlgc/ReC98.git _reference/ReC98
git -C _reference/ReC98 checkout --detach b6ba5b0a529edbb31efdf8c0e939263804f8ee47
.venv/bin/python scripts/import_targets.py /path/to/your/legal-copy.rar \
  --include-all-games-smoke --retain-runtime-image
DISPLAY= WAYLAND_DISPLAY= bash scripts/bootstrap_toolchain.sh
DISPLAY= WAYLAND_DISPLAY= bash scripts/bootstrap_analysis_toolchain.sh
.venv/bin/python scripts/preflight.py
```

Host dependencies include Python 3, a C compiler, Wine, archive utilities and
mtools. Bootstrap verifies downloaded packages; manifests identify the exact
installed versions. Use `.venv/bin/python` consistently for Capstone/Unicorn.
The bounded ZUN emitter is installed through `scripts/bootstrap_jwasm.py`.

## Maintenance and handing off

The [current, concise handoff](docs/RE_HANDOFF.md) begins with the
**latest after921 six-original-physical-object native integration**:
both complete **shared BOSS ring/lifecycle owners**, the entire CPU
combat AI, full Kana Extra Attack, full original HitCircle leaf, and
the complete nine-function Marisa Chargeshot/Gauge. Five maintained C++
files produce six historical original project objects. **All six were
genuinely compiled together** in two independent original TC4 4.02
and complete normal MAIN TLINK rounds, matching **4,643 original CODE
bytes, 396 literal ordered native OMF FIXUPPs and 30 PUBLICs**,
full original normal MAIN EXE/MAP, all 124,642 Japanese loaded program
bytes and all 1,553 ordered MZ relocations. **93 other unchanged
original game objects and CRT reused**, no cold replay. See
[after921 six-original-object native integration](docs/MAIN_SIX_SOURCE_INTEGRATION_AFTER921_REVIEW.md).
The preceding **after915 five-original-physical-object integration**:
complete **Kotohime major BOSS**, full Reimu Chargeshot/Gauge,
complete Yumemi and Kotohime Extra Attack controllers, and the
original far-Pascal **PC-98 volatile VSYNC frame-delay leaf**. All five
changed original physical project objects were **genuinely recompiled
together** in two independent original TC4 4.02 and complete normal
MAIN TLINK rounds, matching **6,059 original CODE bytes, 589 literal
ordered native OMF FIXUPPs and 35 PUBLICs**, normal MAIN EXE/MAP,
all **124,642 Japanese loaded bytes and 1,553 ordered MZ relocations**.
**94 other original game objects and CRT were reused**, no full cold
replay. See
[after915 five-original-object native integration](docs/MAIN_FIVE_SOURCE_INTEGRATION_AFTER915_REVIEW.md).
The preceding **after909 five-original-physical-object integration**:
complete **Rikako major BOSS**, full Ellen Chargeshot/Gauge,
all **nine character resource and callback selectors**, all nine
original keyboard/joystick/CPU input-mode functions, and the complete
PC-98 PMD sound-effect hardware leaf. The five edited current original
project objects were **genuinely compiled together** in both independent
original TC4 4.02 and complete normal MAIN TLINK rounds, matching
**7,582 original CODE bytes, 1,595 literal ordered native OMF FIXUPPs
and 41 PUBLICs**, complete normal MAIN EXE/MAP, all **124,642 Japanese
loaded bytes and 1,553 ordered MZ relocations**. **94 other game
objects and original Borland CRT were reused**, no cold replay. See
[after909 five-object integration](docs/MAIN_FIVE_SOURCE_INTEGRATION_AFTER909_REVIEW.md).
The preceding **after903 seven-original-physical-object integration**:
complete **Yumemi and Mima major BOSSes**, the full **Bullet engine**
with original 9,500-byte BSS, both physical Combo HUD/BOSS-Panic
owners, the original **Hitbox leaf**, and the full explosion-chain
collision engine. **Seven changed original project objects were
genuinely recompiled together** in two independent real TC4 4.02/
normal full MAIN TLINK rounds, matching **8,839 original CODE bytes,
955 literal ordered native OMF FIXUPPs, and 46 PUBLICs**, full normal
MAIN EXE/MAP, all 124,642 Japanese loaded bytes and all 1,553
original ordered MZ relocations. **92 unchanged original project
objects and original CRT reused**, no full cold replay. See
[after903 seven-object native integration](docs/MAIN_SEVEN_SOURCE_INTEGRATION_AFTER903_REVIEW.md).
The preceding **after896 nine-original-physical-object integration**:
all four original Enemy engine and ENEDAT script interpreter objects,
the full Fireball engine, **complete Reimu and Ellen major BOSSes**,
Rikako Bomb and the original round-reset/result scoreboard source.
**Nine edited original project objects were genuinely recompiled
together** in two independent original TC4 4.02/complete normal MAIN
TLINK rounds, matching **10,181 original CODE bytes, 965 literal
ordered native OMF FIXUPPs and 51 PUBLICs**, entire normal MAIN
EXE/MAP, all 124,642 Japanese loaded program bytes and all 1,553
ordered MZ relocations. **90 other original project objects and CRT
reused**, no full cold replay. See
[after896 nine-original-object native integration](docs/MAIN_NINE_SOURCE_INTEGRATION_AFTER896_REVIEW.md).
The preceding **after889 five-original-physical-object integration**:
full **Kana major BOSS**, complete Marisa Extra Attack, complete
Ellen Bomb, all seven static-HUD functions and the original DOS
`execl` leaf. **Two genuine independent original TC4 4.02 + complete
normal TLINK rounds simultaneously compiled all five changed project
objects**, matching **4,191 original CODE bytes, 454 literal ordered
native OMF FIXUPPs, 25 PUBLICs**, entire normal MAIN EXE/MAP, all
124,642 Japanese loaded bytes and 1,553 ordered MZ relocations.
**94 other game objects and Borland CRT were reused**, no full cold
replay. See
[after889 five-original-object native integration](docs/MAIN_FIVE_SOURCE_INTEGRATION_AFTER889_REVIEW.md).
The preceding **after883 four-original-physical-object integration**:
complete Chain 1 and Chain 2 background controllers with their shared
current `phase.inl`, the complete **Marisa major BOSS**, and the small
resident CFG loader leaf. **Four modified original physical objects
were genuinely compiled together** in each of two independent original
TC4 4.02/complete normal MAIN TLINK rounds, matching **2,725 CODE
bytes, 291 literal ordered native OMF FIXUPPs, 19 PUBLICs**, full
normal MAIN EXE/MAP, all 124,642 Japanese loaded program bytes and
1,553 ordered MZ relocations. **95 other original game objects and CRT
were reused**, no cold replay. See
[after883 four-original-object native integration](docs/MAIN_FOUR_SOURCE_INTEGRATION_AFTER883_REVIEW.md).
The preceding **after877 five-original-physical-source integration**:
complete Chiyuri **major BOSS**, Ellen and Rikako Extra Attacks,
complete Chiyuri Chargeshot/Gauge, and the original PC-98 shutdown
leaf. Two independent real original TC4 4.02 and complete normal
TLINK rounds **simultaneously recompile the five modified source owners**
and match **5,563 CODE bytes, 610 literal ordered native OMF FIXUPPs,
32 PUBLICs**, normal MAIN EXE/MAP, all 124,642 Japanese loaded bytes
and 1,553 original MZ relocations. **94 other game objects and CRT
reused**, no cold replay. See
[after877 five-source native integration](docs/MAIN_FIVE_SOURCE_INTEGRATION_AFTER877_REVIEW.md).
The previous **after871 five-original-physical-source integration**:
Kotohime's complete **major BOSS**, Chiyuri's full paired Extra Attack,
Marisa's complete Chargeshot/Gauge, the original 30-byte PMD/MIDI sound
service leaf and the complete Kotohime Bomb. **Two independent genuine
original TC4 4.02 and complete normal TLINK rounds simultaneously
recompiled these five changed physical owners** and matched **4,885
original CODE bytes, 521 literal ordered native OMF FIXUPPs, 26 PUBLICs**,
entire normal MAIN EXE/MAP, all 124,642 Japanese loaded bytes and all
1,553 original ordered MZ relocations. The **94 other original game
objects and CRT were reused**, no full cold replay. See
[after871 five-source native integration](docs/MAIN_FIVE_SOURCE_INTEGRATION_AFTER871_REVIEW.md).
The preceding **after865 five-original-physical-source integration**:
complete Yumemi and Kotohime **Extra Attacks**, full Rikako **major
BOSS**, Rikako Chargeshot/Gauge and the original shared volatile VSYNC
wait leaf. Two genuine independent TC4 4.02 and complete normal TLINK
rounds **simultaneously recompiled these five changed original physical
sources** and matched **5,728 original CODE bytes, 541 literal ordered
native OMF FIXUPPs, 33 PUBLICs**, entire normal MAIN EXE/MAP,
124,642 Japanese loaded bytes and all 1,553 original MZ relocations.
The **94 other original project objects and CRT were reused**; no full
cold replay. See
[after865 five-source native integration](docs/MAIN_FIVE_SOURCE_INTEGRATION_AFTER865_REVIEW.md).
The preceding **after859 five-original-physical-object native integration**:
complete Ellen Chargeshot/Gauge, the full Mima **major BOSS**,
Yumemi Chargeshot/target/Gauge, five-function player effects and the
small Extra Attack callback leaf. **Five real modified original TUs
were compiled together** in each of two independent original TC4
4.02/complete normal TLINK rounds, matching **5,766 CODE bytes,
614 literal ordered native OMF FIXUPPs, 35 PUBLICs**, entire normal
MAIN EXE/MAP, 124,642 Japanese loaded bytes and all 1,553 ordered
MZ relocations. **94 other original game objects and CRT reused**,
no full cold replay. See
[after859 current five-source native integration](docs/MAIN_FIVE_SOURCE_INTEGRATION_AFTER859_REVIEW.md).
The preceding **after853 six-original-physical-object native integration**:
full Yumemi major BOSS, both Combo HUD/BOSS helper owners, full
Warning/Gauge controller, native Gauge saturation leaf and complete
Mima Extra Attack. Five changed maintained C++ source files compiled
as six historical original physical TUs in **two genuine independent
TC4 4.02 + complete normal MAIN TLINK rounds**, matching **5,678 CODE
bytes, 570 literal ordered OMF FIXUPP fields, 27 PUBLICs**, normal
MAIN EXE/MAP, 124,642 Japanese loaded bytes and all 1,553 original
MZ relocations; **93 other game objects and CRT reused**, without full
cold replay. See
[after853 six-source native integration](docs/MAIN_SIX_SOURCE_INTEGRATION_AFTER853_REVIEW.md).
The previous **after847 seven-original-physical-object integration**: full
1,049-line Enemy source (four historical physical TUs), complete Fireball,
full Reimu major BOSS and original explosion-chain collision. Both
original TC4 4.02/complete normal TLINK rounds compile all **seven
changed physical objects simultaneously**, matching **7,530 original
CODE bytes, 656 ordered OMF FIXUPPs, 39 PUBLICs**, complete original
MAIN EXE/MAP, all 124,642 loaded Japanese bytes and 1,553 ordered
MZ relocations. The **92 other original project objects and CRT are
reused**, without full cold replay. See
[after847 source-native integration](docs/MAIN_SEVEN_SOURCE_INTEGRATION_AFTER847_REVIEW.md).
The previous **after842 six-original-physical-object integration**: full Kana
major BOSS, both shared BOSS ring/controller carriers, complete CPU AI,
all input modes and Kana's complete four-trail Chargeshot/Gauge. Five
modified C++ source files were genuinely recompiled as six historical
original TUs in each of two original TC4 4.02/complete normal TLINK
rounds. All **5,558 original CODE bytes, 619 literal ordered native
FIXUPPs, 39 PUBLICs**, full original MAIN EXE/MAP, all 124,642 Japanese
loaded bytes and 1,553 ordered MZ relocations match; **93 other original
game objects and CRT reused**, no whole cold replay. See
[after842 six-object native integration](docs/MAIN_SIX_SOURCE_INTEGRATION_AFTER842_REVIEW.md).
The preceding **after840 five-object source-native integration**: full Kana
BOSS, shared BOSS ring/lifecycle carrier, complete CPU AI collision/retry
and all original input modes. Four modified maintained C++ source files
produce five historical original physical objects. Two genuine independent
original TC4/TLINK rounds compile these five together and match **4,267
original CODE bytes, 502 ordered OMF FIXUPPs, 30 PUBLICs**, complete
normal MAIN EXE/MAP, all 124,642 Japanese loaded bytes and 1,553 ordered
relocations. **94 other project objects and CRT reused**, no cold replay.
See [after840 five-object native integration](docs/MAIN_FIVE_SOURCE_INTEGRATION_AFTER840_REVIEW.md).
The earlier, still source-current **after835 five-object integration**: complete
Marisa and Ellen major BOSSes, the large Bullet/GRCG engine, signed-Q8
`polar` and the original PMD sound-effect leaf. Both real original TC4
4.02/full normal TLINK rounds **simultaneously** compile only these five
changed sources and match **5,937 CODE bytes, 626 ordered FIXUPPs,
41 PUBLICs**, normal MAIN EXE/MAP, 124,642 Japanese loaded bytes and
all 1,553 MZ relocations. The remaining **94 original project objects
and CRT are reused**, without cold replay. See
[after835 five-source native integration](docs/MAIN_FIVE_SOURCE_INTEGRATION_AFTER835_REVIEW.md).
The earlier now historical-source **after829 four-object integration**: three
complete major BOSSes (Yumemi, Rikako and Chiyuri) plus full Reimu
Chargeshot/Gauge. Two real original TC4/TLINK rounds recompile **these
four genuinely modified original physical sources together** and match
**8,137 CODE bytes, 1,077 ordered native FIXUPPs, 39 PUBLICs**, the full
normal MAIN EXE/MAP, 124,642 Japanese loaded bytes and all 1,553
original MZ relocations; 95 other original game objects and CRT reused.
No full cold replay. See
[after829 four-source integration](docs/MAIN_FOUR_SOURCE_INTEGRATION_AFTER829_REVIEW.md).
Earlier historical-source **after827 original-source three-object integration**: complete Yumemi
and Rikako major BOSSes plus the full Reimu Chargeshot/Gauge, all modified
this session. Two real original TC4/TLINK rounds simultaneously rebuild
these three original physical sources and match **5,483 CODE bytes,
696 literal ordered native FIXUPPs, 28 PUBLICs**, full MAIN EXE/MAP,
124,642 Japanese loaded bytes and all 1,553 MZ relocations. 96 other
original objects and CRT reused, no full cold replay. See
[after827 current three-source review](docs/MAIN_THREE_SOURCE_INTEGRATION_AFTER827_REVIEW.md).
The earlier nine-source after823 proof remains genuine **historical**
compiler evidence, but its Reimu source snapshot no longer matches the
present checkout; after829/827 likewise use an older Yumemi snapshot.
No separate receipts can be represented as a simultaneous all-object build.
The earlier
**historical after823 nine-original-physical-owner simultaneous
native proof**: complete Reimu, Mima and Kotohime major BOSSes, main entry/frame
scheduler, Kana Bomb, hitbox damage, HitCircle sprites, full shot and
scoreboard/bonus pipelines. All nine *did compile together* with original
TC4 4.02 and normal MAIN TLINK in two independent historical rounds. All **11,578 CODE bytes, 1,464 ordered OMF FIXUPPs, 49 PUBLICs**,
the entire Japanese MAIN program/MAP and all 1,553 relocations match;
independent MZ serialization reproduces every byte of the original
130,882-byte MAIN.EXE. 90 unchanged original objects and CRT reused,
not cold-rebuilt. Its then-current `.inl` implementations were source-bound;
no byte patches or new canonical Factory packed-game credit. See
[after823 nine-source integration](docs/MAIN_NINE_SOURCE_INTEGRATION_AFTER823_REVIEW.md).
This also includes the new exact natural C++ HitCircle update and render
loops, not present in the older after792 source snapshot. The after792
receipt remains historical evidence, not a current checkout source review.
The earlier [after788 eight-source integration](docs/MAIN_EIGHT_SOURCE_INTEGRATION_AFTER788_REVIEW.md)
passed at its time but its `results` source hash is **historical** after
the after789 source edits; `af823a` itself became historical after
Reimu BOSS edits and `af829a`/`af827a` after the newer Yumemi edit.
Review **after853** for current Yumemi/Combo/Warning/Gauge/Mima Extra,
**after847** for current Reimu/Enemy/Fireball, and **after842/835**
for other current unchanged physical sources.
The earlier **after787 four-physical-source proof**: full
Reimu and Mima major BOSSes, complete main/frame/stage/score `entry`
(including all four live implementation `.inl` files) and complete Kana
Bomb. Both genuine original TC4/TLINK rounds match **7,518 original CODE
bytes, 1,033 ordered OMF FIXUPPs, 27 PUBLICs**, the full normal MAIN
EXE/MAP, loaded Japanese program and all MZ relocations; original
130,882-byte MZ equality is independently serialized. 95 other original
project objects and CRT were reused; no full cold replay. See
[after787 source integration](docs/MAIN_FOUR_SOURCE_INTEGRATION_AFTER787_REVIEW.md).
These original source owners were already covered and are **not** extra
distinct bytes or canonical packed-file acceptance. The earlier
**after782** **six-genuinely-modified-original-physical-source simultaneous**
native proof: full Yumemi Chargeshot/target and **major Yumemi BOSS**,
Rikako's homing Extra Attack, Mima's complete 30-projectile Chargeshot,
Chiyuri's paired GRCG beam Extra Attack and Kana's eight-slot Extra
Attack. This includes a genuine recovery of the original handwritten
**BX/memory/conditional jump** in Chiyuri's big beam entity update
as a normal C++ `if(!exatt_entity_p->state) goto ...` which original
Turbo C++ 4.02 compiles into **the exact original BX instructions**.
Both real TC4/TLINK rounds prove 7,684 original CODE bytes, 771
literal ordered OMF FIXUPP fields and 44 PUBLICs with **93 other
original game objects and CRT reused**, no full cold replay or
binary-code padding. The after775/766 original native rounds remain
historical compiler evidence, but their source hashes **do not** match
this checkout after accumulated edits; the new after859/853/847/842/835
scopes have separately verified current-source read-only receipts.
Overlapping CODE must not be double-counted as accepted ownership.
The original BIOS `input_s` object remains source-native exact at
417 CODE bytes but is **full-MAIN blocked** by the old parent link's
extra trailing NOP; no fake link acceptance is claimed.
It retains after596 MAIN and historical after587 MAINL as *different*
source-native ancestors, not current
whole-game acceptance. The [after709 chronological archive](docs/RE_HANDOFF_ARCHIVE_AFTER709.md)
and [earlier after596 archive](docs/RE_HANDOFF_ARCHIVE_AFTER596.md)
preserve the detailed experiments, negative trials and limitations.

MAIN's frozen after596 source-native parent and the **historical**
after782 six-object native overlay reproduced the complete 124,642-byte
Japanese loaded program and all 1,553 ordered MZ relocations at their
original source checkpoints. `af782a` no longer passes this checkout's
source-hash binding after subsequent C++ changes. `af859a` is also now a *historical*
source snapshot after the later Ellen Chargeshot edit; use `af921a`
for the latest genuine compiler proof of current changed sources.
A **separate standard DOS MZ serializer** then reproduces the entire
original 130,882-byte Japanese MAIN.EXE; this does not prove that the
historic compiler/linker used the same header format. The historical after587 MAINL
source-native link reproduced the entire 67,372-byte decoded Japanese
MAINL EXE and all 677 ordered relocations. Neither establishes
canonical packed-file Factory acceptance or complete historical source
ownership. MAINL's historical after587 decoded publication reviewed 220
extents / 37,968 bytes, but the live decoded source gate is **pending**
after later MAIN source edits invalidated an older broad source-snapshot
guard. Its formal packed-unit credit remains 0/250; see the handoff
for the unchanged historical linker evidence and recertification blocker.

To verify this checkout without replaying unchanged source or toolchains:

    git status -sb
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af921a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af915a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af909a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af903a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af896a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af889a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af883a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af880h
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af881i
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af882e
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af877a
    .venv/bin/python -m unittest discover -s tests -p test_main_source_overlay_inline_contract.py -q
    # Diagnostic reports expected input_s one-byte full-link FAILURE, not acceptance:
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_input_s_link_gap_after744.py
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_yumemi_cpu_after596_work.py
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_score_input_pi_after587_work.py
    .venv/bin/python scripts/progress.py --check
    .venv/bin/python scripts/validate_tracking.py
    git diff --check

Earlier `af758a`, `af753a`, `af741b`, `af730a`, `af736a`, `af724a`,
`af721a`, `af715a` and `af709a` remain protected **historical source
snapshots**, but their current maintained input hashes intentionally
differ from later BOSS, player, or enemy changes. The live read-only
reviewer rejects source drift. Preserve their original compiler/whole-link
evidence. `af766a` likewise has a historical source snapshot now;
use `af921a` for this session's six changed original physical owners,
plus separate source-current `af915a`, `af909a`, `af903a`, `af896a`,
`af889a`, `af883a`, `af880h`, `af881i`, `af882e`, `af877a` for their
unchanged physical source scopes. Earlier `af871a` is historical after
Kotohime BOSS/CPU edits; `af865a` after Rikako BOSS, `af859a` after
Ellen Chargeshot, `af853a` after Mima/Yumemi/Combo, `af847a`/`af843g`
after Enemy/Reimu, `af842a`/`af840a` after Kana and `af835a` after
Marisa/Bullet.

The [storage handoff](docs/STORAGE_HANDOFF_CURRENT.md) distinguishes
the historical applied after520 deletion audit (258 stages / 5,760
protected native files) from current retained evidence, and records
subsequent **audited disposable-only maintenance**. Do not apply the
old cleanup script to a newer source graph or delete full old
compiler stages by age. Cache-only cleanup is separate from original
evidence retention; preserve Japanese targets, installed Wine/Borland
tools, source root, native OBJ/EXE/MAP, both rounds, scripts/receipts
and writer logs. Prefer changed-scope validation, not full cold replay.

Historical details: [after554 handoff archive](docs/RE_HANDOFF_ARCHIVE_AFTER554.md),
[after520 storage record](docs/STORAGE_HANDOFF_AFTER520.md) and
[CRT recovery index](docs/MAINL_WORKING_CRT_RECOVERY_INDEX.md).

## Credits

- [Our TH04 reconstruction repository](https://github.com/N0zoM1z0/th04)
  provides the reference workflow, directory organization, headless tool setup
  and cold-build exact Oracle approach.
- [ReC98 by Nmlgc and contributors](https://github.com/nmlgc/ReC98)
  provides foundational PC-98 Touhou reverse engineering and the pinned scaffold.

TH03's maintained ownership and exactness are checked against its own Japanese
targets. Referenced work retains its authorship and licensing.
