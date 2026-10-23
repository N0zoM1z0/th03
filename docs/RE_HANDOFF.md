# TH03 current work

Commit format: `gpt-6.1-sol: xxx`. Local headless tools; no Factory MCP.

Use `src/` and the pinned Japanese targets in `.analysis/targets/`. MAIN's one
working tree is `.analysis/toolchain/wineprefix/drive_c/TH03WORK`.

- Exact scope:93 CODE extents /424 functions /70,380 bytes. The whole-game
  source denominator is unknown; the complete MAIN product is not exact.
- Two independent577-file source materializations compile all92 source OBJs in
  93 serial native phases. All94 raw OBJ/EXE/MAP outputs repeat. All240 maintained
  inputs match staging. Only vendor C0L.OBJ/libraries are reused/unowned.
- Main flow is one3,050-byte entry.obj producer: main146, loop862, real demo
  callbacks57/5, stage900, initializer855, compiler tables/alignment48 and
  round-finish106/71. Public starts0/146/1008/1065/1070/2009/2873/2979;
  CODE records1021/1018/1011 naturally match all56 literal ordered sites.
  Target stage19/round-finish6/initializer8 interleave is now reproduced.
  Loop -G keeps its distinct score exits; stage -G- restores the default
  profile. Shared declarations avoid duplicate legacy headers. Bounded .inl
  bodies keep four reviewed owners in one .cpp; there is no private DATA/BSS.
  The first99 global records now match after native library and SHARED ordering;
  different positions fall1,281->1,242. Grouping/filenames remain inferred;
  authored counts do not rise.
- All11 owner gates pass for those four owners. Entry1,172, loop240, demo214,
  initializer240 and round-finish768 target/candidate cases retain their ABI,
  ordered calls/stores and complete non-stack memory contracts. Seven/eight/
  six/six/five mutations fail respectively. Entry far RETF, loop near AL0/1/2,
  unsigned wrap/caps and score-transfer/resident fields are preserved.
  Stage setup900 and compiler data48 are outside those runtime models.
- Chiyuri978/four functions and Ellen1,129/six functions pass all11 gates.
  Ellen's51-byte slot initializer begins its producer; records978 and1024/105
  match23/14 literal ordered sites. No OMF rewriting.
- Lose update/particles/banners pass487 bytes/three functions, six/four ordered
  sites, Pascal RET2/RET4 and cdecl RET. Their1,166 cases cover all487 bytes;
  four controls reject semantic changes. Renderer remains175 versus177.
- The unowned master.lib prefix has2269 CODE bytes endingB4F. Following context
  is word-aligned atB50; TLINK supplies matching00. All2270 bytes/order match.
  Near cutline/far APIs and external DATA/BSS widths remain genuine. A second
  unowned object holds8307 library CODE bytes atB50..2BC3; word-aligned root
  context begins2BC4. TLINK supplies00 without the old explicit db0. All8308
  body/gap bytes and six ordered relocations match; root CODE is now748 bytes.
  DATA/BSS remain allocated in the root; sound helpers retain near calls.
- All17 native SHARED objects retain physical order and follow the zero-size
  layout declarations in bo_shim. The resident loader follows them. All positive
  MAP contributions and program bytes remain unchanged;30 SHARED and3 loader
  records extend the matching global prefix66->99. SHARED raw equality remains
  false atEC2D, with no extra source/byte credit.
- Root ASM, score aliases, link recipe and two bitmap-derived ASP inputs are
  regenerated. Source names remain inferred; old proof archives are unnecessary.
- Foreign services are explicit bounded stubs; VSYNC delivery in the loop is
  modeled. Demo callbacks have no foreign stubs. These models do not establish
  actual DOS, graphics, sound or physical-device behavior.

Fresh replay, overwriting current reports:

```sh
.venv/bin/python scripts/replay_th03_main_native.py
```

The unit auditor checks eight native owners /21 functions /5,644 bytes and all93
configured extents. Shared coverage rejects gaps/overlap/wrong frames; controls
preserve local vectors yet reject wrong cross-owner entry/loop and stage/finish
orders. Current runtime/unit checks require no archived entry verification.

Unresolved:

- All3,168 PLAYFLD bytes come from maintained source and match raw bytes. The
  first3,050 bytes now also match joint order. Global record99 is the next gap;
  remaining whole-object/record order differs at1,242 positions. Target record99
  is stage_palette_show atA3A3 in the unowned HITCIRC prefix. It precedes16
  boss_explosion_ring records and boss_move_sine atF381, then retained HITCIRC
  records beginning in randring_fill atA401 and atA841/A835.
  Preserve physical segments and real source boundaries while investigating.
- Renderer pointer/reference/register/argsused and adjacent-function controls
  still emit175 bytes; target177 saves SI+DI and uses DI as its counter.
- State/P_SHOT bytes match, but shot26-site order and stage7/state6/stage5
  interleave remain open. A simple combined multi-section TU keeps raw bytes
  but fails those literal orders. Do not repeat that assumption.
- Loaded-image differences remain at EC2D/1DB05. DATA1DB05 follows
  vsync_OldMask; ordinary TASM/QUIRKS/MASM51 still align it with00. Header and
  global order remain open, alongside the full source/product graph.

`scripts/probe_th03_main_producers.py` replays bounded native renderer/alignment
controls and removes temporary products while preserving working outputs.

Latest CI: PASS,1,711 tests /300 optional archive skips. One CPU at nice10;
CI peak RSS451,448 KiB, native replay peak RSS450,488 KiB.
Keep targets, installed tools, current reports and one working tree; discard
old experiments, duplicate builds, logs and caches.

See [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and
[ledger progress](PROGRESS.md).
