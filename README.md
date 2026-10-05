# TH03 reconstruction

Japanese PC-98 TH03 reconstruction, bootstrapped from TH04's evidence and
toolchain workflow. The current phase is infrastructure: targets, executable
compiler probes and four headless Ghidra projects are available. Maintained
game source and exact units start empty.

```sh
python3 scripts/preflight.py
python3 scripts/status.py
python3 scripts/ghidra.py th03-main check
python3 scripts/ci.py
```

Source ownership is `src/main`, `src/op`, `src/mainl`, `src/zun` and
`src/shared`. Configuration and CSV ledgers are tracked; `.tools`, `.analysis`,
`_reference`, `ghidra-project` and original game files are private and ignored.
The matching game archive is stored outside Git at `../game_exe/`.

Read [the handoff](docs/RE_HANDOFF.md), [workflow](docs/RE_WORKFLOW.md),
[toolchain instructions](docs/TOOLCHAIN.md), [Ghidra instructions](docs/GHIDRA.md)
and [source layout](docs/SOURCE_LAYOUT.md).

The shared Touhou Reconstruction Factory selects repository `th03` and native
providers `th03-ghidra`, `th03-op-ghidra`, `th03-mainl-ghidra`,
`th03-zun-ghidra`. No separate TH03 public MCP service is required.

The original Japanese disk remains `candidate-local-attested`, not an
independently certified pristine release. ReC98 is a pinned calibration and
source hypothesis, never proof of target exactness.
