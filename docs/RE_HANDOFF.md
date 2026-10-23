# TH03 current work

Commit format: `gpt-6.1-sol: xxx`. Local headless tools; no Factory MCP.

Use `src/` and the pinned Japanese targets in `.analysis/targets/`. MAIN's one
working tree is `.analysis/toolchain/wineprefix/drive_c/TH03WORK`.

- Exact scope is 87 units / 413 functions / 66,843 bytes. These are reviewed
  CODE extents; the whole-game source denominator remains unknown.
- Chiyuri 978 bytes/four functions and Ellen 1,129 bytes/six functions now pass
  all 11 required unit Oracles from two independent cold source materializations.
  Their 23/14 ordered sites and every raw byte match. Ellen's real 51-byte slot
  initializer starts its producer; native records are 978 and 1024/105. No OMF
  rewriting or fake instruction bytes. Historical filenames remain unknown.
- The root ASM, score far-Pascal alias, link recipe and both bitmap-derived ASP
  inputs are now reproducible. `scripts/lib/main_work_stage.py` starts with the
  pinned reference root, applies finite source transitions, and stages 563 files.
  `config/th03_main_link.rsp` owns the explicit link order. The score alias binds
  the existing `score_bonus_digits_put` entry and its real RETF 8 ABI.
- Each cold round starts without game objects and compiles all 90 game OBJs in
  91 serial native phases. All 92 raw OBJ/EXE/MAP outputs repeat across two fresh
  source trees. Only vendor C0L.OBJ and libraries are reused; they are unowned.
- HUD's four native bodies total 1,478 bytes with twenty ordered sites. Lose
  update/particles/banners total 487 bytes and remain source-present. Their
  renderer candidate is 175 versus 177 bytes; the original stays in the carrier.
- Entry/state/shot raw bytes match. Shot's ordered relocation partition and the
  state/stage cross-unit interleave remain open. Loaded-image differences still
  occur at B4F/EC2D/1DB05; the MZ header/global relocation order also remain open.

Full native replay, with current reports overwritten rather than archived:

```sh
.venv/bin/python scripts/replay_th03_main_native.py
```

This performs two complete cold rebuilds, bounded entry/lose runtime checks and
`scripts/review_th03_main_native_units.py`. The review validates actual target,
OMF/MAP/function coverage, active tool/include/library identity, the raw cold
vector and the complete required Oracle set for the two regrouped owners.
A full MAIN product is still not exact. Entry 293 / lose 1,166 runtime cases and
the eight initializer runs remain bounded checks with explicit foreign stubs.

Next audit the two lose/defeat source-present owners under the fresh cold graph,
then recover the remaining renderer shape and resolve shot/global order and
three outside bytes. Keep targets, installed tools and one working tree; discard
obsolete experiments, logs and caches.

Latest CI: PASS, 1,681 tests / 300 optional archive skips; one CPU, peak RSS
285,668 KiB. Current cold pair repeats all 92 raw outputs.

See [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and
[ledger progress](PROGRESS.md).
