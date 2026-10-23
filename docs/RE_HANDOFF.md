# TH03 current work

Commit format: `gpt-6.1-sol: xxx`. Local headless tools; no Factory MCP.

Use `src/` and the pinned Japanese targets in `.analysis/targets/`. MAIN's one
working tree is `.analysis/toolchain/wineprefix/drive_c/TH03WORK`.

- Exact scope:92 CODE extents /423 functions /69,518 bytes. The whole-game
  source denominator is unknown; the complete MAIN product is not exact.
- Two independent573-file source materializations compile all93 source OBJs in
  94 serial native phases. All95 raw OBJ/EXE/MAP outputs repeat. All236 maintained
  inputs match actual staging. Only vendor C0L.OBJ/libraries are reused/unowned.
- The generated unowned master.lib prefix owns2269 CODE bytes endingB4F;
  following context is word-aligned atB50. TLINK supplies the matching00 gap.
  All2270 context bytes/order match without source padding or output edits.
  `main_master_prefix.py` retains near cutline and far API declarations and
  external DATA/BSS widths. Authored counters do not change.
- Root ASM, score aliases, explicit link recipe and two bitmap-derived ASP
  inputs are regenerated. Source names/historical compiler filenames remain
  inferred. Installed tools stay pinned; old proof archives are unnecessary.
- Native C++ `main`146 bytes passes all11 owner Oracles: seven literal ordered
  sites, public `_main`, far-cdecl RETF, SI/BP preservation and external storage.
  Its1,172 cases cover two loads/resident offsets, all terminal return bytes,
  continuations, OP/ending and story wrap. Independent complete non-stack memory
  and ordered stores reject seven mutations. CRT/MZ startup is separate/unowned.
- Chiyuri978/four functions and Ellen1,129/six functions pass all11 owner gates.
  Ellen's real51-byte slot initializer begins its native producer; CODE records
  are978 and1024/105, with23/14 literal ordered sites. No OMF rewriting.
- Lose update/particles/banners pass487 bytes/three functions and six/four ordered
  sites, Pascal RET2/RET4 and cdecl RET. Their1,166 runtime cases cover all487
  bytes; four controls reject semantic changes. Renderer remains175 versus177.
- Round-finish owns106/71 bytes with six descending ordered sites. All177 bytes
  pass11 gates,768 runtime cases and five controls. Resident score slots and
  round-byte wrap are checked; port events do not prove physical device behavior.
- Stage/round owns real demo callbacks57/5, stage900 and initializer855 code
  bytes plus48 compiler data bytes:1,865 bytes at load9AD6..A21F. Native records
  1021/844 now match all27 ordered sites naturally. Public starts0/57/62/1001,
  complete coverage, near RET and all compiler-table destinations are reviewed.
  Demo214 cases cover all62 bytes; initializer240 cases cover all855 bytes,
  including negative difficulty indices and uint8 wrap/caps. Six controls each.
  Stage setup900 and table48 bytes are outside those runtime models.
- Foreign services in the entry/lose/round/initializer models are explicit stubs.
  The demo callback model has no foreign stubs. Keep bounded models distinct
  from actual DOS, graphics, sound and whole-game runtime behavior.

Fresh replay, overwriting current reports:

```sh
.venv/bin/python scripts/replay_th03_main_native.py
```

The current unit auditor checks seven native owners /20 functions /4,782 bytes
and replays all92 configured extents. The obsolete archive-dependent entry
review was removed; entry checks now live in the current runtime/unit review.

Unresolved:

- Renderer pointer/reference/register/argsused and adjacent-function controls
  still emit175 bytes; target177 saves SI+DI and uses DI as its counter.
- State/shot bytes match, but shot26-site order and the stage7/state6/stage5
  cross-unit interleave remain open. A simple combined multi-section TU keeps
  raw bytes but fails those literal orders. Do not repeat that assumption.
- Whole loaded-image differences remain at EC2D/1DB05. The DATA byte follows
  vsync_OldMask; ordinary TASM/QUIRKS/MASM51 still align it with00. Header and global
  relocation order remain open, alongside the full source/product graph.

Replay the bounded native controls with
`scripts/probe_th03_main_producers.py`. It records source/context hashes,
removes temporary native products and preserves working OBJ/EXE/MAP bytes.

Latest CI: PASS,1,699 tests /300 optional archive skips. One CPU at nice10;
CI peak RSS407,628 KiB, native replay peak RSS483,176 KiB.
Keep targets, installed tools, current reports and one working tree; discard
old experiments, duplicate builds, logs and caches.

See [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and
[ledger progress](PROGRESS.md).
