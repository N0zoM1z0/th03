# TH03 current work

Commit format: `gpt-6.1-sol: xxx`. Local headless tools; no Factory MCP.

Use `src/` and the pinned Japanese targets in `.analysis/targets/`. MAIN's one
working tree is `.analysis/toolchain/wineprefix/drive_c/TH03WORK`.

- Exact scope is 91 units / 422 functions / 69,372 bytes. These are reviewed
  CODE extents; the whole-game source denominator remains unknown.
- Chiyuri 978 bytes/four functions and Ellen 1,129 bytes/six functions now pass
  all 11 required unit Oracles from two independent cold source materializations.
  Their 23/14 ordered sites and every raw byte match. Ellen's real 51-byte slot
  initializer starts its producer; native records are 978 and 1024/105. No OMF
  rewriting or fake instruction bytes. Historical filenames remain unknown.
- The root ASM, score far-Pascal alias, link recipe and both bitmap-derived ASP
  inputs are now reproducible. `scripts/lib/main_work_stage.py` starts with the
  pinned reference root, applies finite source transitions, and stages 572 files.
  `config/th03_main_link.rsp` owns the explicit link order. The score alias binds
  the existing `score_bonus_digits_put` entry and its real RETF 8 ABI.
- Each cold round starts without game objects and compiles all 92 game OBJs in
  93 serial native phases. All 94 raw OBJ/EXE/MAP outputs repeat across two fresh
  source trees. Only vendor C0L.OBJ and libraries are reused; they are unowned.
- HUD's four native bodies total 1,478 bytes with twenty ordered sites. Lose
  update/particles/banners now pass all 11 unit Oracles: 487 bytes/three functions,
  six/four ordered sites, near Pascal RET2/RET4 and cdecl RET. Their renderer
  candidate is still 175 versus 177 bytes; the original stays in the carrier.
- `src/main/core/roundfin.cpp` now owns next-round106 and score-commit71 bytes.
  Native TC4 emits the target's six descending ordered sites; TASM emitted them
  ascending despite equal raw bytes. Both complete functions pass all 11 Oracles.
  Valid-PID score writes, round wrap and call/port order pass 768 independent
  target/candidate cases and five semantic/cleanup mutations. Callees are stubs.
- `src/main/round/stage_round.cpp` owns the real adjacent demo callbacks57/5,
  stage setup900 and initializer855 instruction bytes, plus48 compiler-local
  table/alignment bytes:1,865 bytes total at load9AD6..A21F. Native TC4 records
  are1021/844; all27 literal ordered relocations now match naturally. The previous
  two-function producer's actual1019/784 records had moved site9EEE ahead of
  stage sites. No dummy callback, padding, normalization or OMF rewriting.
- The six data ranges partition the whole owner with the four functions. Each
  switch-table word names a decoded entry inside its owning function; natural
  zero bytes, native public starts0/57/62/1001 and near RET cleanup are reviewed.
- Demo callbacks pass214 target/candidate cases covering all62 bytes at two
  loads, unsigned frame limits, separate duplicate exit writes and the next-call
  transition at7000. Six semantic/stack controls are rejected; no foreign stubs.
- Initializer runtime covers all855 code bytes in240 target/candidate cases and
  rejects6 mutations. Negative story difficulty indices are not lower-clamped;
  uint8 speed/boss/gauge operations wrap before caps.128 random results, strided
  clears and both player records are checked; foreign services remain stubs.
  The900-byte stage setup and48 table bytes are outside this runtime model.
- The current scoped audit checks all 236 maintained source inputs against the
  actual cold staged contents, including headers and the replayed score alias.
  A source-drift negative control rejects old builds after a maintained edit.
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
vector and the complete required Oracle set for six native owners.
A full MAIN product is still not exact. Entry 293 / lose 1,166 runtime cases and
the eight initializer runs remain bounded checks with explicit foreign stubs.
Round-finish adds 768 scenarios covering all 177 bytes, including resident far
offsets 0/0x200 at two loads; port events do not establish physical device behavior.

Next recover the remaining renderer shape and resolve shot/global order and
three outside bytes. Keep targets, installed tools and one working tree; discard
obsolete experiments, logs and caches.

Latest CI: PASS, 1,697 tests / 300 optional archive skips; one CPU, peak RSS
405,264 KiB. Current cold pair repeats all 94 raw outputs; native replay peak
480,164 KiB.

See [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and
[ledger progress](PROGRESS.md).
