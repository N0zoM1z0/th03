# 東方夢時空 ～ Phantasmagoria of Dim.Dream

This is the `port/modern-64` branch. The first native C++17 title/menu slice
builds for Linux x64 and Windows x64; [portable status and commands](docs/PORTABLE.md)
describe its checks and remaining gameplay integration. The DOS reconstruction
is retained on `main` and remains the behavioral baseline.

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

[Generated progress](docs/PROGRESS.md) shows the source inventory, decoded
acceptance and currently verified native physical owners. All chart bars count
tracked extents; MAIN's function ledger is separate. MAINL has a retained
decoded publication backed by its Staff/root native refresh. MAIN has many
independently verified owners, but these are **not** one all-source build or
canonical packed-game acceptance.

For current stages, remaining blockers and the next agent's starting point,
use [the handoff](docs/RE_HANDOFF.md). Source presence, physical-source
exactness and whole-product acceptance remain different claims; there is no
honest whole-game completion percentage.

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
blockers and the next reconstruction targets. Basic checks need only Python
3.11+ and Git:

    git status -sb
    python3 scripts/ci.py

Run `.venv/bin/python scripts/preflight.py` before target-dependent native
work or after changing targets/tools. Ordinary documentation and CI edits do
not need that private-tool check.

For MAIN source edits, rebuild the affected original physical translation
units and compare the complete native scope in two original TC4/TASM rounds
and two normal MAIN links. Other products use their own affected native scopes.
Use [generated progress](docs/PROGRESS.md) for current source-bound stages.
Full cold replay and broad test suites are not routine per-edit requirements.

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
```

The native compiler bootstrap above is for a fresh, empty TH03 toolchain;
it refuses to overlay an existing prefix. Attach the checkout to Factory's
shared Ghidra/JDK/Wine runtime as described in
[shared tools](docs/SHARED_TOOLS.md), then run `.venv/bin/python scripts/preflight.py`.
The legacy `bootstrap_analysis_toolchain.sh` installs separate Ghidra/JDK
copies and is superseded by that shared-runtime procedure.

Host dependencies include Python 3, a C compiler, the shared Wine runtime,
archive utilities and mtools. Bootstrap verifies downloaded packages;
manifests identify the exact installed versions. Use `.venv/bin/python`
consistently for Capstone/Unicorn. The bounded ZUN emitter is installed through
`scripts/bootstrap_jwasm.py`.

## Maintenance and handing off

Use [the current handoff](docs/RE_HANDOFF.md) for blockers and next work,
[generated progress](docs/PROGRESS.md) for tracked scopes, and
[the workflow](docs/RE_WORKFLOW.md) for affected native rebuilds and complete
comparisons. Whole-game source reconstruction remains unfinished.

Keep necessary inputs, current source/ledgers/build tools and concise useful
knowledge. Historical trial output, archives and cleanup reports need no
permanent retention. See the [short storage guidance](docs/STORAGE_HANDOFF_CURRENT.md).

## Credits

- [Our TH04 reconstruction repository](https://github.com/N0zoM1z0/th04)
  provides the reference workflow, directory organization, headless tool setup
  and cold-build exact Oracle approach.
- [ReC98 by Nmlgc and contributors](https://github.com/nmlgc/ReC98)
  provides foundational PC-98 Touhou reverse engineering and the pinned scaffold.

TH03's maintained ownership and exactness are checked against its own Japanese
targets. Referenced work retains its authorship and licensing.
