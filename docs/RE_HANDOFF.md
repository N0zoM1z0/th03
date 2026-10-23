# TH03 current work

Commit format: `gpt-6.1-sol: xxx`. Use local headless tools; no Factory MCP.

The owner requested removal of historical validation outputs and documents.
`.analysis` was reduced from about 17 GiB to 1.3 GiB. Old receipts, archives,
experiments and generated acceptance publications are gone. Historical ledger
rows remain as records, not locally replayable proof. Regenerate verification
from source before claiming a new exact result.

Latest CI: 1,675 tests, 300 optional archive skips; PASS. One CPU, peak RSS
278,704 KiB. Preflight and whitespace checks also pass.

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
- Lose update270/particle98 and defeat banners119 now link from maintained C++
  with full raw and scoped relocation equality. Two units/three functions are
  source-present candidates; exact counts remain 87 / 413 / 66,843 bytes.
  Their 1,166 paired runtime cases execute all487 bytes; four semantic mutations
  fail. Foreign math/audio/graphics are bounded stubs; renderer/devices are open.
- HUD intro is now one native TC4 unit, `src/main/hud/intro.cpp`: four complete
  bodies688/104/51/635, all1,478 bytes and twenty ordered MZ sites match target.
  The helper instruction-byte directives, generated-ASM splice and OMF reversal
  are gone. Native TC4 emits records1024/454 and preserves SI/DI itself.
- Rebuild/check the current mixed tree with
  `.venv/bin/python scripts/build_th03_main_work.py --build --runtime`.
  Nine native phases rebuild eight objects and reuse83 explicit context objects.
  Repeated EXE/six C++ OBJs are identical; native outputs stay unmodified through
  link. This is not a cold aggregate.
  Reports/logs are overwritten in `.analysis/work/`, not archived.
- Both loaded images are124,642 bytes. Three outside bytes still differ at
  B4F/EC2D/1DB05, along with the MZ header/global relocation order.
- A two-segment state+shot compiler TU retains P_SHOT LEDATA1023/474; it does
  not explain the target first7/next5 relocation partition. First declaration
  controls function segment ownership. Guard the anonymous pid union once;
  its byte fields are fixed, its whole-union packing is context dependent.
- Original relocation order interleaves seven stage sites before six state tail
  sites. The current report exposes both full cross-unit vectors; projected
  equality alone misses this. Uniform1023-byte records do not explain MAIN_01.
- Next remove Ellen's remaining legacy OMF reframe, rebuild the context from
  source for a fresh cold aggregate, and resolve the shot relocation producer.
  Exact acceptance remains at the recorded87 extents; no new promotion yet.
- `losedraw.cpp` remains175 versus177 target bytes and is not linked. The original
  177-byte renderer stays in the working carrier; no padding or dummy ABI.

Read [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and
[exact gates](ORACLES.md). Inspect Git, run preflight, then work from current
source and target bytes. Keep only useful current outputs; do not grow archives.
