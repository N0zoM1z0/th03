---
name: th03-re
description: Recover one bounded TH03 PC-98 unit using attested targets, headless tools and separate evidence/acceptance ledgers.
---

Read AGENTS.md and docs/RE_HANDOFF.md, ARCHITECTURE.md and RE_WORKFLOW.md.
Run preflight and selected database attestation before target analysis.
Review storage/decompression boundaries, segment ownership and 16-bit ABI.
Treat upstream code and Ghidra boundaries as hypotheses. Recover natural
source, record evidence classes and source presence, and promote exactness
only after all configured cold/raw/layout/ledger gates pass.
Use headless tools only; serialize Borland builds. Update the concise handoff
and finish with CI and whitespace verification.
