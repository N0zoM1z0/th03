# TH03 current work

Commit format: `gpt-6.1-sol: xxx`. Local headless tools; no Factory MCP.

Continue from `src/` and the pinned Japanese targets in `.analysis/targets/`.
The current MAIN tree is `.analysis/toolchain/wineprefix/drive_c/TH03WORK`.

- Exact ledger scope is 85 units / 403 functions / 64,736 bytes. Chiyuri/Ellen
  boundaries changed and remain source-present pending fresh canonical cold
  acceptance. Whole-game source completion remains unknown.
- All 87 tracked extents / 66,843 bytes retain complete raw equality and scoped
  ordered relocations. This does not establish the complete product's order.
- Ellen's real 51-byte slot initializer now begins its native C++ producer:
  Chiyuri 978 bytes/four functions; Ellen 1,129 bytes/six functions. TC4 emits
  records 978 and 1024/105, matching 23/14 ordered sites without OMF rewriting.
  The old reframe helper is deleted. Original function addresses are unchanged.
- The slot initializer passes eight target/candidate runs at two load segments,
  checking all 51 code bytes, 24 ordered pointer writes, histories and far ABI.
- All 90 game OBJs are now rebuilt from maintained source plus the current root
  carrier. Only vendor C0L.OBJ is retained; vendor libraries remain unowned.
  Two successive builds repeat all 90 raw OBJs and the entire EXE. Input mtimes
  are fixed; native object contents are never adjusted after compilation.
- HUD's four native bodies total 1,478 bytes with twenty ordered sites. Lose
  update/particles/banners total 487 bytes and remain source-present. Renderer
  candidate is 175 versus 177 bytes; the 177-byte original stays in the carrier.
- Entry/state/shot raw bytes match. Shot's ordered relocations and cross-unit
  order remain open. Three loaded-image bytes differ at B4F/EC2D/1DB05;
  the MZ header/global relocation order also remain open.

Rebuild all game objects and check the current mixed tree:

```sh
.venv/bin/python scripts/build_th03_main_work.py --build --rebuild-context --runtime
```

This runs 91 serial native phases, stages full C++ TU copies, and uses no cached
game OBJs. The root ASM and link recipe are still materialized working inputs.
Next reconstruct their canonical staging recipe, then perform independent cold
rounds from fresh source. Recompiling this existing tree alone is insufficient
for new exact acceptance. Entry 293 / lose 1,166 bounded runtime cases also pass.

Overwrite current reports in `.analysis/work/`; delete obsolete experiments,
logs and caches. Keep targets, installed tools and one useful working tree.
Checks: CI PASS, 1,676 tests / 300 optional archive skips; one CPU, peak RSS
288,988 KiB. Latest full native rebuild peak RSS was 271,596 KiB.

See [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and
[ledger progress](PROGRESS.md).
