# TH03 current work

Commit format: `gpt-6.1-sol: xxx`. Use local headless tools; no Factory MCP.

The owner requested removal of historical validation outputs and documents.
`.analysis` was reduced from about 17 GiB to 1.3 GiB. Old receipts, archives,
experiments and generated acceptance publications are gone. Historical ledger
rows remain as records, not locally replayable proof. Regenerate verification
from source before claiming a new exact result.

## Continue here

- Current MAIN work tree: `.analysis/toolchain/wineprefix/drive_c/TH03WORK`.
  It contains source, link inputs and the last mixed MAIN executable/MAP.
- Product source is under `src/`; Japanese targets are under `.analysis/targets/`.
- MAIN's recorded reviewed scope is 87 extents / 413 functions / 66,843 bytes.
  This is not a whole-game percentage. The whole authored denominator is unknown.
- Entry146, state1716 and shot1497 source candidates still need exact acceptance.
  Their 18 far-call differences are the immediate next work.
- Fresh native control: `#pragma samecodeseg` preserves the far ABI and makes
  TLINK relax a cross-segment call in the same code group. `/P` alone did not.
  Small source/result pairs are in `.analysis/work/`; old native capsules are gone.
- The lose renderer remains175 versus177 target bytes; no padding or dummy ABI.

Read [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and
[exact gates](ORACLES.md). Inspect Git, run preflight, then work from current
source and target bytes. Keep only useful current outputs; do not grow archives.
