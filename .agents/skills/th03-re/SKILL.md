---
name: th03-re
description: Recover one bounded TH03 PC-98 source unit and verify exact native output.
---

Read AGENTS.md, the concise handoff and relevant architecture/workflow sections.
Use preflight before target-dependent work or after target/runtime changes; attest a database
before using its observations. Treat upstream code and Ghidra boundaries as
hypotheses. Recover natural source with the pinned Japanese target, preserving
storage boundaries, ownership, 16-bit widths, ABI and native build order.

Prioritize complete raw bytes, literal ordered relocations, native layout and
affected-scope reproducibility. Runtime probes are optional tools for concrete
uncertainties, not mandatory failure/null-pointer/input-domain matrices. Do not
build large independent emulator specifications merely to accept equal native
code. Do not repeat unchanged cold builds or ancestor runtime reviews.

Use direct headless tools, one CPU at nice10 and serialized Borland writers.
Record useful source findings, update the handoff, run affected checks and
whitespace verification. CI checks syntax/whitespace only; choose relevant
tests explicitly rather than running a broad suite for every unit or commit.
