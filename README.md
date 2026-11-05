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

[Generated progress](docs/PROGRESS.md) distinguishes canonical packed-unit ledger counts from separately reviewed decoded source acceptance. The independent working-source CRT can reproduce the decoded MAINL EXE/MAP without granting any new formally accepted ledger units; see the handoff for the current source-module count.
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

CPU 16 is available on the current machine; select one allowed CPU on another
host. Serialize Borland/Wine writers. The [workflow](docs/RE_WORKFLOW.md) lists
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

The live handoff is [docs/RE_HANDOFF.md](docs/RE_HANDOFF.md) (verified
`after423`, **617/893** source-built original CRT members). Historical
member reviews are indexed in
[MAINL recovery history](docs/MAINL_WORKING_CRT_RECOVERY_INDEX.md).
Do not infer formal MAINL acceptance from this working-source CRT;
`docs/PROGRESS.md` is regenerated from the separate ledgers.

This checkout has **161 active MAINL native receipt stages**. Do not delete
their raw logs, build receipts, or two OBJ/LIB/EXE/MAP output rounds.
`clean_generated.py`'s general `.analysis` preview is **not** a native
proof-dependency oracle; never blanket-apply it here.

```sh
python3 scripts/cleanup_mainl_after388_handoff.py  # guarded dry-run only
# After reviewing the exact source/receipt hash and scope:
# python3 scripts/cleanup_mainl_after388_handoff.py --apply
.venv/bin/python scripts/clean_generated.py --caches-only --apply
```

The historical after388 cleanup script deliberately rejects this newer source checkpoint;
re-audit the new live DAG before adapting it. Read
[current protected-storage rules](docs/STORAGE_HANDOFF_CURRENT.md) and
[working-file rules](docs/RE_WORKFLOW.md#working-files) first. Keep original
Japanese targets, `.analysis/toolchain` (Wine/Borland), Ghidra/JDK identity
trees, runtime images, accepted ledgers, `.venv` and all live proof inputs.
The old-named `reference.tar` is still a consumed reference input.

Commit format: `gpt-web: xxx`. Run affected checks and `git diff --check`,
then save substantial progress locally. Push only when requested.

## Credits

- [Our TH04 reconstruction repository](https://github.com/N0zoM1z0/th04)
  provides the reference workflow, directory organization, headless tool setup
  and cold-build exact Oracle approach.
- [ReC98 by Nmlgc and contributors](https://github.com/nmlgc/ReC98)
  provides foundational PC-98 Touhou reverse engineering and the pinned scaffold.

TH03's maintained ownership and exactness are checked against its own Japanese
targets. Referenced work retains its authorship and licensing.
