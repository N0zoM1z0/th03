# Shared Factory registration

Repository ID: `th03`; adapter: `th03-pc98-v1`; toolchain identity:
`toolchain:th03-borland16`. Cross-game smoke targets are excluded from progress.

| Provider | Target |
| --- | --- |
| `th03-ghidra` | `target:th03-main` |
| `th03-op-ghidra` | `target:th03-op` |
| `th03-mainl-ghidra` | `target:th03-mainl` |
| `th03-zun-ghidra` | `target:th03-zun` |

All use `attested-ghidra-command-v1` with `scripts/factory_ghidra.py` and a
private implementation-file aggregate. The Factory checks disk identity and
MZ structure independently; the wrapper checks full nonce-bound Ghidra bytes,
mapping, relocations and entry in the same process as the semantic query.

The public Factory MCP URL and tool metadata remain unchanged. Hot deployment
uses a separately validated stateless instance and a proxy switch, while
existing MCP and worker processes remain alive. Paths, binding hashes, port
and endpoint configuration belong only to ignored operator state.

Native TH03 receipt replay is unavailable until a Factory driver is implemented
and the worker is migrated. The checked-in local
`scripts/replay_th03_main_exact_units.py` can run through Factory's repository
shell; its exact owner ledgers remain imported claims, separate from Truth
Kernel acceptance.

TH03's allowlisted TH04 reference is discoverable at `/references/th04` inside
the repository shell. For example, `cat /references/th04/src/shared/math/vector.cpp`
reads real maintained source without requiring the host path. Writes are denied.
