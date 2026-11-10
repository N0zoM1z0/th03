# Storage: keep what reconstruction needs

Keep original Japanese programs, pinned tools/SDKs, Ghidra projects and the
isolated mutable Wine state. Factory supplies shared executables and system
modules; do not duplicate their installations.

Keep maintained source, exact-match ledgers and scripts that can recompile
and compare the complete affected native output, including ordered relocations
and layout. Current entry points still reuse a native baseline and source
snapshots; keep those actual working inputs until they can be regenerated.
A chain of historical receipts is not itself a retention requirement.

Keep concise knowledge: current blockers, verified compiler/ABI findings and
failed approaches worth avoiding. Historical archives, duplicate evidence,
old trial output and successive cleanup reports can be deleted. Remove their
obsolete documentation references too. No new audit, manifest or archive is
needed just to perform cleanup.

The `input_s` linker discrepancy is a specific exception: retain the original
417-byte object, the 418-byte frozen parent and the `af1305a` experiment while
resolving the one-byte gap. See the [current handoff](RE_HANDOFF.md).

`clean_generated.py --caches-only --apply` removes Python/test caches only.
It leaves native build output and `.analysis` alone. Remove obsolete native
work according to the current build/compare inputs, not document reachability.
