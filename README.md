# 東方夢時空 ～ Phantasmagoria of Dim.Dream

Agent workflow: follow the highest-priority requirements in [AGENTS.md](AGENTS.md). Use affected exact checks and searchable Markdown knowledge; ordinary notes do not require full CI or replay.

<p align="center">
  <img src="resources/title-screen.png" width="640" alt="Original Japanese TH03 title screen">
</p>
<p align="center">
  <img src="resources/progress.svg" alt="TH03 reviewed reconstruction scopes">
</p>

This repository reconstructs the original Japanese PC-98 **Touhou 3:
Phantasmagoria of Dim.Dream**. Work covers OP.EXE, MAIN.EXE, MAINL.EXE (the ending)
and ZUN.COM. Reconstruction and whole-product source acceptance remain open.

[Generated progress](docs/PROGRESS.md) shows source inventory, decoded acceptance and independently verified current native owners. All chart bars count tracked unit extents; MAIN's function ledger is separate. MAINL's **current decoded publication is restored** through the `af1055m` Staff/root native refresh and revalidated retained ancestry. Two original compiler rounds reproduce the complete decoded EXE/MAP and ordered relocations; whole-product source ownership remains open. See the [current handoff](docs/RE_HANDOFF.md) for the precise scope and outstanding work.
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

Use the current [handoff](docs/RE_HANDOFF.md) for source-bound proof stages,
blockers and the next reconstruction targets. Start with:

    git status -sb
    .venv/bin/python scripts/preflight.py
    git diff --check

For source edits, rebuild only the affected original physical translation
units and compare the complete native scope in two original TC4 rounds and
two normal MAIN links. Do not use historical composite stages as current
proofs; the active handoff lists the current source-bound stages. Full cold
replay and full CI are not routine per-edit requirements.

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

Use the [active handoff](docs/RE_HANDOFF.md) for current source-bound
proofs, exactness limits, blockers and next work. Follow [AGENTS.md](AGENTS.md)
for the workflow and [RE_WORKFLOW.md](docs/RE_WORKFLOW.md) for scoped native
verification. The active handoff is intentionally shorter than the historical
chronology; detailed earlier experiments remain in
[the after927 archive](docs/RE_HANDOFF_ARCHIVE_AFTER927.md) and the
experiment-specific review notes.

The latest source-bound MAIN integration is recorded in the active handoff.
It covers selected complete BOSS/collision owners and reuses unchanged
original game objects; it is not whole-game source acceptance or canonical
Factory packed-file acceptance. Use the generated
[progress report](docs/PROGRESS.md) and current preflight for product status.

For storage, use the [current retention policy](docs/STORAGE_HANDOFF_CURRENT.md)
and [after1024 applied cleanup audit](docs/STORAGE_HANDOFF_AFTER1024.md).
That cleanup removed only regenerable Python bytecode and repacked Git
without pruning any objects. It did not delete native proof stages. Preserve
the source-bound receipt DAG, both original compiler rounds, OBJ/LIB/EXE/MAP,
writer logs, Japanese targets and installed toolchain. Never prune proof
trees by age or by a generic generated-file preview; no full cold replay is
needed for an ordinary scoped source change.

## Credits

- [Our TH04 reconstruction repository](https://github.com/N0zoM1z0/th04)
  provides the reference workflow, directory organization, headless tool setup
  and cold-build exact Oracle approach.
- [ReC98 by Nmlgc and contributors](https://github.com/nmlgc/ReC98)
  provides foundational PC-98 Touhou reverse engineering and the pinned scaffold.

TH03's maintained ownership and exactness are checked against its own Japanese
targets. Referenced work retains its authorship and licensing.
