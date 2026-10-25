# TH03 handoff

Reconstruction checkpoint: 2026-10-25, after `0674ce2`. Five complete MAINL PI
callers now have native ownership and full-state contracts. The consumed SDK
inventory includes `mem.h`; two fresh source-only cold rounds and the complete
dependent review chain were rerun.
Read `AGENTS.md`,
[architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and the local
[th03-re skill](../.agents/skills/th03-re/SKILL.md) before continuing.

## Verified state

| Product | Accepted source scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 445 functions / 75,317 CODE bytes / 98 extents | Open |
| OP | 31 functions / 3,620 CODE bytes | Open |
| MAINL | 32 functions / 1,816 CODE bytes | Open |
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

Last reconstruction CI: **2,156 tests, 284 optional archive skips, all checks passed**;
6m54s, about 528 MiB peak RSS, no swap. Heavy work was pinned to CPU 16 at nice10.

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

### MAINL resources

Five complete PI callers now own **555 CODE bytes**: palette37, put136,
interlace135, load70 and quarter177. The four real TC4 producers preserve
GAME3/O first use for shared `pi_put.cpp`/`pi_load.cpp` and GAME3/L for interlace
and quarter. Complete native OMF/MAP/publics, 25 literal ordered fixups and seven
MZ relocations pass. Private DATA/BSS are zero. Current command:
`review_th03_mainl_pi_work.py --current-cold`; publication remains
`config/mainl_work/scoped_acceptance.json`.

Independent target/candidate contracts run **5,932 cases per image** at two
loads. They execute all 555 bytes, the actual previously accepted 76-byte root
PI release and 35 bytes of the 36-byte CRT memcpy. Its odd-tail MOVSB is not
reached by the fixed 48-byte copy; library context adds no source ownership.
All DWORD/segment state, defined flags, ordered stores and every physical memory
byte, including private stack/caller data, pass. Both real far return words are
checked at callee entry because Unicorn may omit their write hooks. Peak stack
depth is 26 bytes; no stack window is ignored. Forty-six owner and three
contextual instruction mutations fail.

- Slot BYTE lanes, overlapping forward palette copies, signed top wrapping,
  live width/height changes and persistent load reentry are covered. Row offset
  addition truncates to WORD **before** paragraph normalization; quarter always
  draws 200 rows of width320. Its selectors are full WORD values.
- The readonly-height `FFFF` interlace loop is now proved closed: init0,
  add2 and unsigned JA at `0C7E:0656` retain all 32,768 even counter states.
  The native CFG has only this exit guard. Returning packed interfaces,
  immutable height and disjoint DGROUP/private stack are explicit assumptions.
  Each image has 144 independently checked live prefixes, separate from
  ordinary terminating calls (including callbacks that change the height).
  Instruction-budget expiry is never evidence.
- PI load executes actual root `GRAPH_PI_FREE` at `0000:0FEC`; header fields are
  cleared even after a failed free. HMEM_FREE at root `22B2` remains a bounded
  interface preserving BX/CX/ES and IF/DF, with AX/arithmetic-flag replies.
  Decoder/graphics/heap internal effects and physical hardware remain unowned.
- MAINL CS/DS are `0C7E/0E3F`; PI buffers are DS:`1F0E`, headers `1F26`, palette
  destination `141E`. PiHeader is72 bytes. Compatibility forwarding and the
  complete consumed SDK/source graph remain bound by the native cold pair.

Next: the five complete CDG functions in `src/shared/formats/cdg_load.cpp` total
**593 bytes**: single138, single-noalpha134, all230, all-noalpha28 and free63,
at `0C7E:073E..098F`. Actual wrapper is `th03/cdg_load.cpp`, GAME3/O first use,
with zero private DATA/BSS. CDG slots are DS:`1D0E`, flag `0894`; CDG is16 bytes.
Single truncates `bitplane_size * 5` to WORD before widening and the signed-WORD
image-index multiply. Color allocation/read lengths also wrap to WORD.
All-noalpha calls the real all-loader and finally sets the flag to zero rather
than restoring its entering value. Execute actual owned free/all helpers.
Keep buffer fixtures disjoint from DGROUP/stack and retain unchecked slots and
segment-zero allocations explicitly. Use `review_th03_mainl_sound_work.images()`
to revalidate the full current graph and obtain
`work,target,candidate,cold,raw,graph,files`.

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
