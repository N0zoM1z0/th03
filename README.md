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
**latest after829 original-source four-object integration**: three
complete major BOSSes (Yumemi, Rikako and Chiyuri) plus full Reimu
Chargeshot/Gauge. Two real original TC4/TLINK rounds recompile **these
four genuinely modified original physical sources together** and match
**8,137 CODE bytes, 1,077 ordered native FIXUPPs, 39 PUBLICs**, the full
normal MAIN EXE/MAP, 124,642 Japanese loaded bytes and all 1,553
original MZ relocations; 95 other original game objects and CRT reused.
No full cold replay. See
[after829 four-source integration](docs/MAIN_FOUR_SOURCE_INTEGRATION_AFTER829_REVIEW.md).
Earlier **after827 original-source three-object integration**: complete Yumemi
and Rikako major BOSSes plus the full Reimu Chargeshot/Gauge, all modified
this session. Two real original TC4/TLINK rounds simultaneously rebuild
these three original physical sources and match **5,483 CODE bytes,
696 literal ordered native FIXUPPs, 28 PUBLICs**, full MAIN EXE/MAP,
124,642 Japanese loaded bytes and all 1,553 MZ relocations. 96 other
original objects and CRT reused, no full cold replay. See
[after827 current three-source review](docs/MAIN_THREE_SOURCE_INTEGRATION_AFTER827_REVIEW.md).
The distinct earlier nine-source proof remains current for its **nine
other unchanged source owners**; the two experiments must not be
incorrectly represented as one simultaneous 12-object build.
The earlier
**latest after823 nine-current-source-original-physical-owner simultaneous
native proof**: complete Reimu, Mima and Kotohime major BOSSes, main entry/frame
scheduler, Kana Bomb, hitbox damage, HitCircle sprites, full shot and
scoreboard/bonus pipelines. All nine *actually compile together* with
current original TC4 4.02 and full normal MAIN TLINK in two independent
rounds. All **11,578 CODE bytes, 1,464 ordered OMF FIXUPPs, 49 PUBLICs**,
the entire Japanese MAIN program/MAP and all 1,553 relocations match;
independent MZ serialization reproduces every byte of the original
130,882-byte MAIN.EXE. 90 unchanged original objects and CRT reused,
not cold-rebuilt. Full current `.inl` implementations are source-bound;
no byte patches or new canonical Factory packed-game credit. See
[after823 nine-source integration](docs/MAIN_NINE_SOURCE_INTEGRATION_AFTER823_REVIEW.md).
This also includes the new exact natural C++ HitCircle update and render
loops, not present in the older after792 source snapshot. The after792
receipt remains historical evidence, not a current checkout source review.
The earlier [after788 eight-source integration](docs/MAIN_EIGHT_SOURCE_INTEGRATION_AFTER788_REVIEW.md)
passed at its time but its `results` source hash is **historical** after
the after789 source edits: review **after823** for this current checkout.
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
binary-code padding. Previous after775/766 native scopes remain
independently current-source reviewable; historical snapshots whose
hashes drift are not current checkout passes, and overlapping original
CODE totals must not be double-counted as new accepted ownership.
The original BIOS `input_s` object remains source-native exact at
417 CODE bytes but is **full-MAIN blocked** by the old parent link's
extra trailing NOP; no fake link acceptance is claimed.
It retains after596 MAIN and historical after587 MAINL as *different*
source-native ancestors, not current
whole-game acceptance. The [after709 chronological archive](docs/RE_HANDOFF_ARCHIVE_AFTER709.md)
and [earlier after596 archive](docs/RE_HANDOFF_ARCHIVE_AFTER596.md)
preserve the detailed experiments, negative trials and limitations.

MAIN's frozen after596 normal source-native link, and the later
after782 six-object current-source overlay, reproduce the complete
124,642-byte Japanese loaded program and all 1,553 ordered MZ relocations.
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
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af829a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af827a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af823a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af787a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af782a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af775a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af772a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af766a
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af765g
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af764d
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af763d
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af762c
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af761c
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af760c
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af759c
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
evidence; use `af766a` for the latest eight changed physical source owners.

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
