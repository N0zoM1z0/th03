# TH03 current work

Commit format: `gpt-6.1-sol: xxx`. Local headless tools; no Factory MCP.

Use `src/` and the pinned Japanese targets in `.analysis/targets/`. MAIN's one
working tree is `.analysis/toolchain/wineprefix/drive_c/TH03WORK`.

- Exact scope:93 CODE extents /424 functions /70,380 bytes. The whole-game
  source denominator is unknown; the complete MAIN product is not exact.
- Two independent577-file source materializations compile all93 source OBJs in
  94 serial native phases. All95 raw OBJ/EXE/MAP outputs repeat. All240 maintained
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
- Native C++ round_loop862 bytes passes all11 owner gates and16 literal
  ordered sites. TC4 -G keeps the two distinct score/return exits naturally;
  default generation tail-shares them into857 bytes. Reuses real score_commit
  and near/far/Pascal/BX-register interfaces, with no new DATA/BSS. Its240
  cases cover all862 bytes at two loads/resident offsets: all exits, repeated
  frames, callback/port order, counters/caps/wrap and complete non-stack memory.
  Eight semantic/ABI/memory mutations fail. VSYNC delivery is a modeled IRQ.
- Entry and loop now share the real1,008-byte entry.obj CODE record with
  publics0/146 and23 descending literal sites. The .cpp includes bounded .inl
  owners and a guarded resident view; function bodies and all owned bytes stay
  unchanged. Entry.obj follows CRT: the first27 global sites now match and
  differing positions drop1,337->1,314. Shared-producer coverage rejects gaps,
  overlap and wrong frames. A cross-owner swap preserves both local vectors
  yet fails the joint order check. Source grouping/filename remain inferred.
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
- Foreign services in the entry/lose/round/initializer/loop models are explicit stubs.
  The demo callback model has no foreign stubs. Keep bounded models distinct
  from actual DOS, graphics, sound and whole-game runtime behavior.

Fresh replay, overwriting current reports:

```sh
.venv/bin/python scripts/replay_th03_main_native.py
```

The current unit auditor checks eight native owners /21 functions /5,644 bytes
and replays all93 configured extents. The obsolete archive-dependent entry
review was removed; entry checks now live in the current runtime/unit review.

Unresolved:

- All3,168 PLAYFLD bytes come from maintained source and match raw bytes.
  The entry/loop cross-owner order is now resolved; the remaining global
  object/record order still differs at1,314 positions.
  Target global record27 starts stage_round at load9E92; the candidate next
  emits boss-shared atF348. Next test stage_round after the entry producer.
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

Latest CI: PASS,1,707 tests /300 optional archive skips. One CPU at nice10;
CI peak RSS418,044 KiB, native replay peak RSS478,592 KiB.
Keep targets, installed tools, current reports and one working tree; discard
old experiments, duplicate builds, logs and caches.

See [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and
[ledger progress](PROGRESS.md).
