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

[Generated progress](docs/PROGRESS.md) distinguishes canonical packed-unit ledger counts from reviewed decoded source acceptance. The selected native link reproduces the original decoded MAINL EXE; its MAP layout and reviewed differences are checked separately. This does not grant canonical packed-unit acceptance. See the handoff for current source ownership.
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

The [current handoff](docs/RE_HANDOFF.md) starts at the validated **after554**
MAINL link, retaining the after548 shared runtime. MAINL has **220 reviewed
extents / 290 procedures / 37,968 source bytes**. The compiler library has
**893/893 source-bound slots / 209,272 CODE-extent bytes**, including unlinked
members; those totals are not authored-game credit or a whole-game denominator.
Formal MAINL canonical Factory acceptance remains **0/250**.

The unfinished after555 research was archived outside the product tree; it was
never built or accepted. Read its [research note](docs/AFTER555_UNBUILT_RESEARCH.md)
before restoring any draft. Historical recipes and evidence remain frozen.

```sh
git status -sb
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_text_banks_work.py
.venv/bin/python scripts/clean_generated.py --caches-only # optional preview
```

The [storage handoff](docs/STORAGE_HANDOFF_CURRENT.md) separates the historical
applied after520 deletion audit from current after554 evidence. The old deletion
guard **rejects this checkout**; its 258-stage / 5,760-file count describes the
old prefix, not today's complete DAG. Native output pruning requires a fresh
source-DAG/hash audit. Cache-only cleanup leaves `.analysis` intact. The latest
handoff maintenance also repacks Git with `--no-prune` and verifies that every
Git object and every private work artifact remains present and unchanged.

Preserve targets, Wine/Borland tools, Ghidra/JDK, both complete raw native rounds,
writer logs, source provenance and reference archives. Never blanket-apply
`clean_generated.py --apply`, prune unreferenced receipts or infer disposability
from age. Avoid unchanged full cold/runtime replay. Commit substantive work as
`gpt-web: xxx`; push only when requested.

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
