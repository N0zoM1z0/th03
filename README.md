# TH03 reconstruction

PC-98 Japanese TH03 source reconstruction using the pinned Borland toolchain.
The whole game is unfinished; reviewed byte counts are not a completion percentage.

Start with [the current handoff](docs/RE_HANDOFF.md), [architecture](docs/ARCHITECTURE.md)
and [workflow](docs/RE_WORKFLOW.md).

```sh
.venv/bin/python scripts/preflight.py
.venv/bin/python scripts/ci.py
git diff --check
```

Keep source, targets, installed tools and one working tree. Old verification,
downloads, experiments and caches can be deleted; regenerate checks when needed.
