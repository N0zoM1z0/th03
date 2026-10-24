# Reconstruction workflow

1. Inspect Git and `docs/RE_HANDOFF.md`; run `python3 scripts/preflight.py`.
2. Select a bounded source/ownership question. Before using database observations,
   run `python3 scripts/ghidra.py ARTIFACT check`.
3. Recover natural source and compile/link with the pinned native tools.
   Preserve 16-bit widths, near/far/Pascal ABI, layout and link order.
4. For exact acceptance, check complete raw bytes, literal ordered relocations,
   ownership, ABI/MAP/layout, affected behavior and two independent cold builds.
   Required checks are in `config/oracles.toml`; compiler success alone is insufficient.
   Use `scripts/review_th03_op_cfg_work.py` for the SDK-guarded OP cold pair
   and cfg review. After rebuilding OP or MAINL, run `scripts/review_th03_shared_input_work.py`
   before republishing their source scopes. Its complete input models bind both
   current cold reports; status only replays short ABI cases.
5. Record useful findings in the ledgers/current handoff, run focused checks,
   `python3 scripts/ci.py` and `git diff --check`, then commit.

Use `.venv/bin/python` for checks. Clear DISPLAY/WAYLAND_DISPLAY and serialize
Borland/Wine writers. Keep heavy work on one CPU at nice10. Ghidra heap limits
can be passed through `_JAVA_OPTIONS="-Xmx768m -XX:ActiveProcessorCount=1"`.

Keep one useful working tree. Delete obsolete experiments, duplicate builds,
logs and caches after use. Old validation outputs are not retention requirements;
future exact claims require fresh verification. Do not change target bytes,
pad code or invent ABI declarations to obtain equality.
Installed tools stay pinned; download archives and installation media can be
deleted after installation. Keep current findings in source, ledgers and the
handoff, without requiring old validation directories to remain on disk.
