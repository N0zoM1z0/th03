# Reconstruction workflow

1. Inspect Git and `docs/RE_HANDOFF.md`; run `python3 scripts/preflight.py`.
2. Select a bounded source/ownership question. Before using database observations,
   run `python3 scripts/ghidra.py ARTIFACT check`.
3. Recover natural source and compile/link with the pinned native tools.
   Preserve 16-bit widths, near/far/Pascal ABI, layout and link order.
4. Compare complete raw bytes and ordered relocations; verify affected behavior
   and cold reproducibility before promoting exactness.
5. Record useful findings in the ledgers/current handoff, run focused checks,
   `python3 scripts/ci.py` and `git diff --check`, then commit.

Use `.venv/bin/python` for checks. Clear DISPLAY/WAYLAND_DISPLAY and serialize
Borland/Wine writers. Keep heavy work on one CPU at nice10. Ghidra heap limits
can be passed through `_JAVA_OPTIONS="-Xmx768m -XX:ActiveProcessorCount=1"`.

Keep one useful working tree. Delete obsolete experiments, duplicate builds,
logs and caches after use. Old validation outputs are not retention requirements;
future exact claims require fresh verification. Do not change target bytes,
pad code or invent ABI declarations to obtain equality.
