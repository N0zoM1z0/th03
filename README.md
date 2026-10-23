# TH03 reconstruction

PC-98 Japanese TH03 source reconstruction using the pinned Borland toolchain.
The whole game is unfinished; reviewed byte counts are not a completion percentage.

Start with [the current handoff](docs/RE_HANDOFF.md), [source layout](docs/SOURCE_LAYOUT.md)
and [workflow](docs/RE_WORKFLOW.md). Exact acceptance follows [these gates](docs/ORACLES.md).

```sh
.venv/bin/python scripts/preflight.py
.venv/bin/python scripts/ci.py
git diff --check
```

The owner requested a lean workspace: historical validation directories,
acceptance snapshots and history documents have been removed. Keep source,
canonical targets, tools and one working tree; regenerate verification when needed.
