# TH03 current work

Commit format: `gpt-6-astra-medium: xxx ~`. Use local headless tools; no Factory MCP.

The owner requested removal of historical validation outputs and documents.
`.analysis` was reduced from about 17 GiB to 1.3 GiB. Old receipts, archives,
experiments and generated acceptance publications are gone. Historical ledger
rows remain as records, not locally replayable proof. Regenerate verification
from source before claiming a new exact result.

Latest CI: 1,677 tests, 300 optional archive skips; PASS. One CPU, peak RSS
273,848 KiB. Preflight and whitespace checks also pass.

## Continue here

- Current MAIN work tree: `.analysis/toolchain/wineprefix/drive_c/TH03WORK`.
  It contains source, link inputs and the last mixed MAIN executable/MAP.
- Product source is under `src/`; Japanese targets are under `.analysis/targets/`.
- MAIN's recorded reviewed scope is 87 extents / 413 functions / 66,843 bytes.
  This is not a whole-game percentage. The whole authored denominator is unknown.
- Entry146, state1716 and shot1497 now have complete raw target equality.
  `samecodeseg` preserves far/Pascal ABI and fixes all18 old call mismatches.
  Entry/state ordered relocations match; shot's26 sites still have wrong order.
  All87 recorded scopes still match raw bytes and literal relocation order.
- Rebuild/check the current mixed tree with
  `.venv/bin/python scripts/build_th03_main_work.py --build --runtime`.
  Six native phases rebuild five objects and reuse84 explicit context objects.
  Repeated EXE/three candidate OBJs are identical; this is not a cold aggregate.
  Reports/logs are overwritten in `.analysis/work/`, not archived.
- Both loaded images are124,642 bytes. Three outside bytes still differ at
  B4F/EC2D/1DB05, along with the MZ header/global relocation order.
- A two-segment state+shot compiler TU retains P_SHOT LEDATA1023/474; it does
  not explain the target first7/next5 relocation partition. First declaration
  controls function segment ownership. Guard the anonymous pid union once;
  its byte fields are fixed, its whole-union packing is context dependent.
- Next resolve the shot relocation producer and create a fresh cold aggregate.
  Exact acceptance remains at the recorded87 extents; no new promotion yet.
- The lose renderer remains175 versus177 target bytes; no padding or dummy ABI.

Read [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and
[exact gates](ORACLES.md). Inspect Git, run preflight, then work from current
source and target bytes. Keep only useful current outputs; do not grow archives.
