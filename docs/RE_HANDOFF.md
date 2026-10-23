# TH03 current work

Commit format: `gpt-6.1-sol: xxx`. Local headless tools; no Factory MCP.

Use `src/` and the pinned Japanese targets in `.analysis/targets/`. MAIN's one
working tree is `.analysis/toolchain/wineprefix/drive_c/TH03WORK`.

- Exact scope:95 CODE extents /440 functions /74,398 bytes. The whole-game
  source denominator is unknown; the complete MAIN product is not exact.
- Two independent589-file source materializations compile all95 source OBJs in
  96 serial native phases. All97 raw OBJ/EXE/MAP outputs repeat. All249 maintained
  inputs match staging. Only vendor C0L.OBJ/libraries are reused/unowned.
- Main flow is one3,050-byte entry.obj producer: main146, loop862, real demo
  callbacks57/5, stage900, initializer855, compiler tables/alignment48 and
  round-finish106/71. Public starts0/146/1008/1065/1070/2009/2873/2979;
  CODE records1021/1018/1011 naturally match all56 literal ordered sites.
  Target stage19/round-finish6/initializer8 interleave is now reproduced.
  Loop -G keeps its distinct score exits; stage -G- restores the default
  profile. Shared declarations avoid duplicate legacy headers. Bounded .inl
  bodies keep four reviewed owners in one .cpp; there is no private DATA/BSS.
  The first394 global records now match after native library and SHARED ordering;
  different positions fall1,225->947. Grouping/filenames remain inferred;
  flow grouping adds no authored credit.
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
- Stage palette adds four exact far functions /130 bytes in maintained ASM:
  21/26/41/40 instruction bytes plus two separately reviewed natural EVEN bytes.
  TASM5 emits one positive130-byte HITCIRC_TEXT producer at096E:0C98, with no
  storage allocation. All11 gates pass;1556 target/candidate cases execute all128
  instruction bytes, covering all byte PIDs, all valid-PID channel values, dirty
  word carriers, complete non-stack memory, ordered stores/show and far cleanup.
  Eight mutations fail. DF0 is required; palette output remains a bounded stub.
- Character setup adds twelve exact C++ functions /3888 bytes: resource
  helpers85/34/97 and nine408-byte setters. One native HITCIRC_TEXT producer at
  096E:0D6C emits records1017/1023/1017/831 and all277 literal sites. No private
  DATA/BSS; the12-byte filename template and all state remain in the root.
  Real near entries take far filenames where specified; ABI distance is parsed
  from the entry qualifier. All11 gates pass. The1020-case independent model
  executes all3888 bytes, checking all characters/PIDs and palette parities,
  signed resource wrap/division, far mutable filenames, SEG-before-OFFSET
  stores, ordered services, complete non-stack memory and Pascal cleanup.
  Sixteen controls fail; foreign file/palette/random/boss services remain stubs.
- Existing RNG fill18, near getters44 and collision reset20 retain their
  accepted source ownership in one82-byte TASM producer at096E:0D1A. Four
  publics0/18/36/62,80 instruction bytes and two EVEN bytes match, without
  DATA/BSS allocation or extra credit. The runtime model checks every byte ring
  index, including index255 reading the already-incremented index as its word
  high byte, and1656 dword collision stores. MAIN_04 getters remain in root.
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

The unit auditor checks ten native owners /37 functions /9,662 bytes and all95
configured extents. Shared coverage rejects gaps/overlap/wrong frames; controls
preserve local vectors yet reject wrong cross-owner entry/loop and stage/finish
orders. Current runtime/unit checks require no archived entry verification.

Unresolved:

- All3,168 PLAYFLD bytes match raw bytes; the first3050 also match joint order.
  Palette show plus boss ring/movement match through record115; the primitive
  IRAND site and277 character sites now extend the prefix through393. Record394
  is next: target185A6/1853B/18516 within chiyuri_bomb. Remaining order differs
  at947 positions. Keep the real segment-first-declaration order when moving
  objects. Root HITCIRC now has958 bytes fromB37C onward; moving the entire root
  earlier is known to change PLAYER_M placement.
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

Latest CI: PASS,1,720 tests /300 optional archive skips. One CPU at nice10;
CI peak RSS343,608 KiB, native build/review peak RSS546,976 KiB.
Keep targets, installed tools, current reports and one working tree; discard
old experiments, duplicate builds, logs and caches.

See [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and
[ledger progress](PROGRESS.md).
