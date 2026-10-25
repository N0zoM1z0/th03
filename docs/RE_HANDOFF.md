# TH03 handoff

Reconstruction checkpoint: 2026-10-25, after `07404db`. MAINL's complete ending
entry now has native ownership and full-state contracts with actual accepted
callees. Five missing consumed SDK headers were added and all fresh producers
now reject undeclared SDK dependencies. Two source-only cold builds and the full
MAINL proof chain were rerun; all previous 40 owners retain their observations.
Read `AGENTS.md`,
[architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and the local
[th03-re skill](../.agents/skills/th03-re/SKILL.md) before continuing.

## Verified state

| Product | Accepted source scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 445 functions / 75,317 CODE bytes / 98 extents | Open |
| OP | 31 functions / 3,620 CODE bytes | Open |
| MAINL | 41 functions / 3,182 CODE bytes | Open |
| ZUN | 77 extents / 89 procedures or entries / 6,179 CODE bytes | Open |

OP includes 22 compiler switch/separator bytes with separate raw/table proof.
ZUN accepts 8,635 CODE+DATA bytes: authored 2,179, original ASM 1,390 and
library 5,066. Keep these origins separate. No whole-game denominator or
completion percentage is known. Use [generated progress](PROGRESS.md),
`config/units.csv`, `config/evidence.csv` and `config/knowledge.csv` for details.

The current OP, MAINL and ZUN cold pairs repeat every raw output and match their
complete decoded **and** canonical DIET `-B` stored targets. This complete-file
observation includes unowned reference/vendor context; source acceptance is
limited to the scopes above. Publications are
`config/{op_work,mainl_work,zun_work}/scoped_acceptance.json`.
MAIN's 101 raw outputs / 99 native objects repeat; its whole file remains unequal.

Last reconstruction CI: **2,209 tests, 284 optional archive skips, all checks passed**;
6m53s, about 536 MiB peak RSS, no swap. Heavy work was pinned to CPU 16 at nice10.

## Resume work

1. Inspect Git and run `.venv/bin/python scripts/preflight.py`.
2. Continue MAINL resources/ending, then remaining OP/ZUN ownership and the
   overall four-product source/link graph. Whole-product completion is unproved.
3. Re-attest the chosen Ghidra database before using it:
   `.venv/bin/python scripts/ghidra.py th03-mainl check`.
4. Select a complete bounded source/ownership scope. Preserve natural native
   production, full raw bytes, literal ordered relocations, ABI/layout and
   independent affected-behavior contracts. Finish with focused checks, full CI,
   whitespace checks and an English `gpt-6.1-sol: ...` commit; push checkpoints.

### MAINL resource scopes

All scopes below are current in `config/mainl_work/scoped_acceptance.json`.
Use the matching `review_th03_mainl_*_work.py --current-cold` to revalidate the
unchanged complete cold pair and rerun one stage. Current source graphs retain
original GAME3/O first use for shared producers and GAME3/L for ending producers.
Shared CS/DS are `0C7E/0E3F`; PI buffers/headers are DS:`1F0E/1F26`, CDG slots
DS:`1D0E`. PiHeader is72 bytes; each CDG slot is16 bytes.

- **PI release:** root `GRAPH_PI_FREE` at `0000:0FEC`,76 CODE bytes. Its5,558
  cases/image cover all segment BYTE lanes, zero/repeated segments, failed-free
  clearing, effective offset wrap and live header/caller-frame aliases;20
  instruction mutations fail. HMEM_FREE at root22B2 remains a bounded unowned
  reply preserving BX/CX/DX/SI/DI/BP/DS/ES/SS, high halves and IF/DF.
- **PI callers:** five complete functions,555 CODE bytes from four TC4 producers;
  25 ordered native fixups/seven MZ fields. The5,932 cases/image execute all555
  owner bytes, actual release76 and35 of36 CRT memcpy bytes;46 owner/three
  contextual mutations fail. The odd-tail MOVSB is not reached by the48-byte
  copy and no library ownership follows. WORD row addition truncates before
  paragraph normalization; quarter always draws200 rows of width320.
- **CDG loaders:** five complete functions,593 CODE bytes in
  `src/shared/formats/cdg_load.cpp`;35 ordered native fields/24 MZ relocations.
  Four far fields relax naturally in TLINK; one backward bridge is native TC4.
  The7,328 cases/image execute real nested free/all helpers;66 mutations fail.
  Maximum entries include255 CDG frees,510 heap frees/allocations and511 reads.
  Counts are unchecked BYTEs, not capped to32 slots. The noalpha wrapper writes
  1 then0; slot0EB8 aliases its flag through header bottom_left atDS:0894, and
  slot0E30 permits self-aliasing file metadata. File/heap bodies remain unowned.
- **CDG drawing:** alpha179/hflip201/noalpha113,493 CODE bytes from two maintained
  TASM5 producers;19 native fields/two MZ relocations/12 real SMC WORDs. The8,298
  complete entries/image execute every owner byte and real41-byte GRCG setup;
  58 owner/one helper mutations fail. Three outer EVEN bytes stay excluded.
  Hflip preserves DF and leaves FS at the color segment; alpha/noalpha clear DF
  and restore DS. Actual setup OUTs have IF clear; caller GRCG-off restores IF.

Every physical/flat-memory byte and all DWORD/segment/defined flags/native frames
are checked without ignored stack windows. Unicorn may omit far-CALL write
hooks; both real return words are checked at callee entry. Graphics/decoder/heap
replies and external LUT data remain explicit interfaces; physical pixels,
GRCG latches/planar RMW/timing, LUT generation and IRQ reentrancy are unproved.

The readonly-height FFFF interlace loop has a closed native CFG and invariant
covering32,768 even WORD counter states;144 checked live prefixes/image stay
separate from terminal calls. Immutable height, returning packed interfaces and
disjoint DGROUP/stack are assumptions. CDG width0 is finite: LOOP runs65,536
inner iterations, while REP0 writes nothing. Actual alpha/hflip reach RETF after
262,144 DWORD/327,680 BYTE stores respectively in the zero-width fixtures.
Native WORD recurrences give row delta-80, at most411 rows/plane and26 color
planes under mapped disjoint-memory/stable-SMC assumptions. Budget expiry is
never nontermination evidence.

### MAINL ending entry

Complete `_mainl_ending` owns **280 CODE bytes** at `095F:2382`, with34 ordered
native fields,14 ordered MZ relocations and the compiler-owned near cdecl frame.
`src/mainl/staff/data.cpp` is copied literally to `staffdat.cpp` and compiled
GAME3/L. Full producer inventory is19 procedures/3,695 CODE bytes,224 initialized
DATA bytes and no BSS; the other18 procedures and DATA remain unaccepted.
Current command: `review_th03_mainl_ending_work.py --current-cold`.

- **9,528 complete entries per image** at two loads execute all280 ending bytes
  and227 actual accepted helper bytes: CDG free63, PI free76, frame delay21 and
  game exit67. Full DWORD/segment registers, defined flags/IF/DF, ordered native
  frames/stores/ports and all flat memory pass. Peak stack24; no ignored window.
  Thirty-five owner and four actual helper instruction mutations fail.
- All resident character/credit BYTE values, decimal digit addition overflow,
  far offset wrap and script-pointer self-aliasing, live resident redirection
  after staff/registration replies, zero/repeated segments and persistent reentry
  pass. Character0 gives `(-1)/2 == 0`; character255 gives signed BYTE127.
  The bonus gate reloads resident state after registration: credits exactly3
  and original character BYTE below15. A failed returning execl reaches the
  actual cdecl cleanup/near RET. Script/staff/registration/exec bodies and
  physical IRQ/graphics remain explicit unowned interfaces.
- The complete nine-header SDK inventory now includes PROCESS/STDLIB and
  MBCTYPE/CTYPE/MBSTRING, consumed by root/staff/text/cutscene objects. Every
  fresh project/CRT object is checked against that declaration in both builds
  and the independent publication audit. Product source and complete decoded/
  stored files are unchanged; full prerequisites and the OP/MAINL joint witness
  were regenerated against the new recipe/cold report.

Next candidates: remaining staff/snow/graphics and cutscene ownership, then
remaining OP/ZUN and the overall source/link graph. Whole-product completion
remains open.
Use `review_th03_mainl_sound_work.images()` to revalidate the complete current
cold pair and obtain `work,target,candidate,cold,raw,graph,files`.

### Other open reconstruction work

- **OP:** all five main/option menu functions own 1,338 CODE bytes, including
  22 inline bytes. Fourteen entry-TU functions cover its first 2,831 bytes;
  root `_main`263, initialized DATA487/BSS6, Music Room and resource scopes remain.
  The ordinary Music Room far call uses `samecodeseg`; TC4's symbolic far field
  lets TLINK generate NOP/PUSH CS/near CALL naturally. Do not restore hand-written
  call assembly. `lib/op_nested_context.py` shares the actual physical UC and
  native frames across story/VS/score/attract. Static seen slots survive failed
  exec and menu reentry. Eight full legacy scope observations must remain equal
  to immutable checkpoint `d118c46`; fresh phase logs need not be byte-identical.
- **MAINL:** sound mode/PMD/volume/reset still contain explicit trailing NOPs.
  Unpadded bodies are recovered, but their natural enclosing layout is unproved.
  Generated WORD/BYTE segment controls are diagnostics, not source acceptance.
  Five root helpers own 150 bytes; three adjacent NOPs stay excluded.
- **ZUN:** all five payloads have native source producers. ONGCHK owns 892 CODE
  +34 initialized DATA bytes; its 42 BSS bytes are not file-backed. Driver -4's
  55 procedures, header/tables and natural CODE layout pass separate gates;
  **3+9 reserved DATA bytes** and runtime/vendor context remain open. Do not add
  an empty segment to force the trailing storage. ONGCHK replays every native
  loop iteration; its optimized audit reproduces the original full traces.
- **MAIN layout:** 124,642 load-image bytes differ only at `EC2D` and `1DB05`
  (target `90`, candidate `00`). Header sizes are target 6,240 / candidate 7,680.
  The first 1,072 of 1,553 ordered relocations match; 242 positions differ.
  Next mismatch is record1072 at `DC42`, state / MAIN_010_TEXT. The first shot
  procedure's twelve far calls split 7/5 around state records. A simple combined
  TU preserves bytes but reaches only record1073; grouping remains unresolved.
  `EC2D` follows input_sense RETF before snd_se_reset; `1DB05` is DGROUP:`05A5`,
  between vsync_OldMask and BYTE_MASK. Normal TASM/MASM51/QUIRKS controls emit
  zero; the OP Music Room fix does not explain these bytes.
- **MAIN producers:** keep combo's explicit P_COMBO_TEXT / MAIN_04 identities,
  far-Pascal ABI and samecodeseg call relaxation. The loss renderer's near
  member ABI and 128-byte player layout are proved; original class/file
  organization remains an inference. See `config/main_work/` and
  `probe_th03_main_producers.py` for current bounded observations.

## Local state to retain

- Fixed Japanese targets and legally supplied runtime data in ignored private
  paths; provenance remains **candidate-local-attested**.
- `.analysis/toolchain/wineprefix`, installed TC4/TASM/JWasm, `.tools/ghidra`,
  `.tools/jdk`, `.venv`, `_reference/ReC98`, and `ghidra-project/`.
- One current working tree per product: `drive_c/TH03WORK`, `TH03OP`, `TH03ML`,
  `TH03ZUN`; full paths are in the build scripts. Current manifests/reviews live
  in `.analysis/work/*-build.json` and `main-unit-review.json`.
- **Required archive:**
  `.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar`.
  Despite the old directory name, current OP/MAINL staging consumes it directly.
  It is a build input, not an obsolete verification run.
- Ghidra/JDK identity checks cover their **entire installed trees**, including
  bundled documentation/archives. Removing those files invalidates attestation.
  Download caches outside the installed trees are disposable.
- Keep `scripts/lib/zun.py` unchanged: MAIN's promoted serial schedule pins it.
  OP's builder is also a shared utility input to MAINL/ZUN. Avoid gratuitous
  edits; real recipe/source changes require fresh bound cold pairs and reviews.

## Checks and cleanup

Use [the workflow](RE_WORKFLOW.md) for cold rebuild/review/publication order and
[the script index](../scripts/README.md) to find current entry points.

```sh
taskset -c 16 nice -n 10 env DISPLAY= WAYLAND_DISPLAY= \
  _JAVA_OPTIONS='-Xmx768m -XX:ActiveProcessorCount=1' \
  .venv/bin/python scripts/ci.py
git diff --check
```

CPU 16 is available on this machine; choose one allowed CPU on another host.
Serialize Borland/Wine writers and preserve the prefix. Use `.venv/bin/python`;
system Python's Unicorn installation is unsuitable here.

Old logs, temporary probes, duplicate receipts and Python caches are disposable;
references alone do not require retaining them. Preserve actual current build
and proof inputs. `clean_generated.py` previews its guarded cleanup unless
`--apply` is supplied. After a full CI,
`clean_generated.py --caches-only --apply` removes standard caches/build output
while leaving all `.analysis` state alone. Read-only status checks can use
`PYTHONDONTWRITEBYTECODE=1`.
