# TH03 current work

Commit format: `gpt-6-astra-medium: xxx ~`. Local headless tools; no Factory MCP.

Continue exact reconstruction from `src/` and the pinned Japanese targets in
`.analysis/targets/`. The current mixed MAIN tree is
`.analysis/toolchain/wineprefix/drive_c/TH03WORK`.

- Recorded exact scope is currently 85 units / 403 functions / 64,736 bytes.
  Chiyuri/Ellen ownership was changed in the uncommitted work, so both units
  await fresh cold acceptance. The whole-game denominator remains unknown.
- The current mixed build matches all 87 tracked extents / 66,843 bytes and
  their scoped ordered relocations. These checks do not establish a cold build.
- Ellen's real 51-byte slot initializer now belongs to its native C++ producer:
  Chiyuri 978 bytes, Ellen 1,129 bytes. The old OMF reframe was removed; the
  resulting mixed EXE is unchanged. Finish the pending probe dimensions
  and fresh cold verification before accepting these boundaries.
- HUD intro's four native bodies total 1,478 bytes with twenty ordered sites.
  Lose update/particles/banners total 487 bytes and remain source-present;
  the 177-byte renderer still uses the original carrier (candidate is 175).
- Entry/state/shot raw bytes match. Shot's ordered relocations and cross-unit
  order remain open. Three loaded-image bytes differ at B4F/EC2D/1DB05;
  the MZ header/global relocation order also remain open.

Rebuild the mixed tree with:

```sh
.venv/bin/python scripts/build_th03_main_work.py --build --runtime
```

It rebuilds ten objects in eleven native phases and reuses 81 context objects,
including the vendor startup. A fresh cold rebuild of the remaining game
context is still required. Preserve the uncommitted reconstruction work.

Keep one current build and overwrite reports in `.analysis/work/`. Delete old
validation, experiments, caches and downloaded installers when no longer used.
They need not be retained because an old document or ledger mentions them.
Installed Wine/Borland/Ghidra/JDK and canonical inputs remain available.

Checks: CI PASS, 1,674 tests / 300 optional archive skips; one CPU, peak RSS
276,916 KiB. Preflight and whitespace checks pass.

See [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and
[ledger progress](PROGRESS.md).
