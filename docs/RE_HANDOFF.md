# TH03 handoff

Prepared2026-10-26. Baseline checkpoint **`6b6026e4`**,main ahead eight.
Existing MAINL registration ownership is staged,not committed:14 procedures,
2720 instruction bytes/988 instructions. Required68 music CODE and40 pointer
DATA remain uncredited context. No source changes/native rebuild/new runtime.
Full CI pending at writing;final result reported separately.

Read `AGENTS.md`, [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md)
and the local [th03-re skill](../.agents/skills/th03-re/SKILL.md) before resuming.
Detailed findings live in maintained source, `config/knowledge.csv`,
`config/evidence.csv`, tests and current review reports.

## Accepted state

| Product | Accepted source scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 459 functions / 78,737 CODE bytes / 106 extents | Open |
| OP | 34 extents / 36 procedures / 4,099 CODE + 487 DATA bytes | Open |
| MAINL | 81 extents / 86 procedures / 12,439 CODE + 224 DATA bytes | Open |
| ZUN | 77 extents / 89 procedures or entries / 6,179 CODE bytes | Open |

OP includes22 separately proved inline compiler bytes. ZUN accepts8,635
CODE+DATA bytes:authored2,179, original ASM1,390, library5,066. Whole-game
source/function denominators and a completion percentage remain unknown.

OP/MAINL/ZUN current source-only cold pairs repeat all outputs and match complete
decoded and canonical DIET `-B` stored targets. Unowned reference/vendor context
is still present; this does not prove whole-product source ownership. MAIN
repeats100 outputs/98 project objects (97 compiled sources plus one fresh vendor
extraction); all1553 literal relocations match. Its header and one CODE alignment
byte still differ.

Publications: `config/{op_work,mainl_work,zun_work}/scoped_acceptance.json`.
Generated accounting: [PROGRESS.md](PROGRESS.md), `resources/progress.svg`.
Inherited post-cleanup CI: **2,413 tests,284 optional archive skips,all checks
passed**;10m01s/about572 MiB peak RSS/no swap,CPU16/nice10.

## MAINL complete registration ownership

All188 native fields and70 literal EXTDEF/MAP identities independently resolve
CODE2788 +DATA40. Only2720 instruction bytes/14 complete near procedures and54
ordered relocations are credited. Music68 CODE, pointer40 DATA, preceding
scoredat229 and external storage remain uncredited. Prior67 owner observations
and all retained reports are unchanged. Current PI operands match;historical
six-mismatch notes are superseded without touching compiled inputs.

Full current938-output source/SDK/recipe bindings pass on the existing cold pair.
Use `review_th03_mainl_registration_work.py --current-cold`;never restart an
ancestor default chain to refresh unchanged supporting traces. Current status
checks177 ledger rows;frozen145/150 fixtures retain historical eligibility.
See [MAINL_REGISTRATION_REVIEW.md](MAINL_REGISTRATION_REVIEW.md).

## MAINL complete cutscene ownership

All236 native fields,58 literal EXTDEF/MAP identities,13 publics and56 ordered
MZ relocations independently resolve the full3195-byte producer. Only3122
instruction bytes are credited;72 inline table bytes and the emitted zero stay
required context. Current PI operands match;this supersedes the historical
source comment without modifying the compiled source. Prior54 owners unchanged.

The comment-only rebuild completed both938-output rounds;its following full
ancestor runtime chain was interrupted at Staff single and is not a pass.
Exact original cold/scoped report bytes were recovered against their published
SHA256 hashes after reverting the comment-only source change. All unchanged
current-cold guards,17 scoped proofs and shared input pass again. Fresh and
interrupted evidence is preserved. No report was repinned or partial run marked
complete. See [MAINL_CUTSCENE_REVIEW.md](MAINL_CUTSCENE_REVIEW.md).
Use the bounded new cutscene review with `--current-cold`;do not restart the
ancestor chain merely to refresh unchanged supporting traces.

## MAIN narrow game-graphics ownership

Four existing complete RET/RETF entries add207 instruction bytes/96 instructions
in three spans:27/87/93. Full216-byte gf_ctx provider remains checked; nine
unowned context bytes include B398's five-byte prefix and four post-transfer
bytes. Its known branch toB37F shares the first implementation without recounting.
These bytes are not claimed padding or unreachable. Executed NOPs stay code.

Positive target/caller evidence is game-specific288px playfield/HUD geometry,
dual-player strip copying, near/far adapter and gauge-only four-row fill.
Original filename/language/historical derivation remain unknown. No new source
implementation, mask DATA, callbacks or executed-body runtime claim.

The fixed graphics adapter reuses existing provider/context partition policy;
player helper, generic accounting and RET rules are unchanged. Existing two-cold
builds/native review pass all11 gates, repeat100 outputs/98 objects and retain
106 extents/78,737 bytes/all1553 literal relocations. Whole executable repeats;
EC2D and header remain open. See `MAIN_GRAPHICS_FILL_REVIEW.md` and
`config/main_work/graphics_fill_acceptance.json`. Existing focused42 tests pass.
Final full CI pending at note writing; no post-CI source edits are intended.

## MAIN remaining player-family ownership

Four complete native owners add existing render/overlay/knock/bomb610,
stage-shot sprites173,round reset/results1060 and shots_add264:9 functions,
2,107 bytes/748 instructions. No new implementation. Explicit complete
core3135/results1060/shots449 partitions preserve all prior owners,including
the distinct185-byte shots update/render suffix. Native records/publics/MAP,
raw bytes and literal ordered relocations remain checked; no external DATA/BSS
or callback ownership. Near-this loss member RET2 is not a far callback.

Existing full two-cold replay passes all11 exact requirements,repeats100 outputs/
98 objects,and retains103 extents/78,530 bytes plus all1,553 literal MZ entries.
See `MAIN_PLAYER_FAMILY_REVIEW.md` and
`config/main_work/player_family_acceptance.json`. No new runtime harness or
executed-body claim. Full CI pending at writing; final receipt reported separately.
Historical snapshots below remain dated prior observations,not live counters.

## MAIN player-state ownership recovery

Already reconstructed `player_state_update` owns only loadDA43..DE95:
1,106 bytes/375 instructions,near Pascal/RET4. Not a new implementation.
Complete3,135-byte core partition preserves previous owners and leaves610
adjacent player bytes plus173 sprite bytes unaccepted. Shared root BSS4B9C
is an existing1+2+2 reserve view,not new storage.

Full existing two-cold replay passes all11 exact requirements,repeats100
outputs/98 objects,and retains99 extents/76,423 bytes/all1,553 literal relocations.
Native records/publics/MAP/zero private DATA/BSS remain checked. Round-loop
runtime stubs this callee;no executed-body claim or new harness. See
`MAIN_PLAYER_STATE_UPDATE_REVIEW.md` and
`config/main_work/player_state_update_acceptance.json`. Full CI pending at
writing;final receipt reported separately. No push or new commit yet.

## MAIN original VSync vendor dependency

The actual TH04 dependency mechanism transfers: native TLIB extracts unchanged
`VS.ASM` from the pinned original `MASTERS.LIB`, then ordinary TLINK places its
DATA8/BSS8 between the root's real head/tail contributions. This restores90 at
load1DB05; no source NOP, object patch or original-assembler substitution is used.
VS remains prebuilt vendor context, not recovered authored source.

Two full614-input cold trees compile97 source objects and freshly extract one
vendor object in99 native phases, repeating100 raw outputs. All other124641 load
bytes, all1359 public names/addresses/idle flags and all1553 literal relocations
remain unchanged. Prior98 owned extents/75317 bytes retain their checks. Only
EC2D (target90/candidate00) and MZ header6240/7680 remain open. See
`config/main_work/vsync_vendor_observation.json`; the older player observation
remains historical and is not rewritten. Full existing CI is pending.

## MAIN player source composition (preceding checkpoint)

The current native graph uses `src/main/player/core.cpp` (3135 CODE bytes),
`src/main/round/results.cpp` (1060), and `src/main/player/shots.cpp` (449).
Complete existing bodies live in bounded `.inl` files; standalone historical
wrappers and historical evidence rows remain distinct. No authored counters
increase and no original-filename provenance is claimed.

Two full614-input source restagings compile96 objects in97 native phases and
repeat all98 raw outputs. The complete124642-byte previous load image and all
98 owned extents/75317 bytes remain unchanged. All1553 literal ordered MZ
entries match target (previously242 differing positions). Core records are
1024/1022/1024/65, result records1018/42, and shots449. The semantic split at
complete function boundaries places result11 relocations before the genuine
Mima13 and active-shot5 afterward; no output sorting or patches are used.

Packed shared types are MAIN-owned; no global compatibility headers changed.
The real DWORD `round_frame` is read through its low BYTE in Hyper, and the
existing one-byte `pid.current` field is explicitly BYTE in inline assembly.
The old two-TU result was limited evidence, not a reason to exclude this larger
natural composition. See `config/main_work/player_composition_observation.json`.

At that checkpoint load offsetsEC2D/1DB05 (target90/candidate00) and MZ
header6240/7680 differed; the vendor composition above now closes1DB05. Ordinary pinned DIET `-B` then
`-ra` leaves the candidate completely unchanged; that route does not explain
the header. The additional documented DIET `-B -G`/`-ra` route likewise restores the
candidate unchanged. Neither tested storage route explains the header.

## Resumed Music Room state/track review

`scripts/review_th03_op_music_state_work.py --current-cold` passes for
`th03-op-decoded-music-state-and-tracks`: four complete near procedures,
216 CODE bytes at0990:0C1E,12 literal ordered native fields and4 ordered MZ
relocations. Native OMF/MAP, complete raw bytes, exact consumed SDK
`mem.h`/`_defs.h`/`_null.h`, the two maintained-owner entries and literal
three-include producer bind the entire unchanged cold source/tool/recipe/
32-output graph. Fresh composed prior scope observations equal `bcdf24a`.
The frozen historical replay command and cohort remain unchanged.

Target and candidate each pass1,788 cases across loads1000/3000, including
all216 executable bytes. Each load has894 returns:562 track,289 list,
33 snapshot and10 free;264,000 actual DWORD copy callbacks,peak stack28,
no ignored stack bytes. All38 instruction controls reject. Fixed formerly
nondiscriminating page-field and bold-FX fixtures (page128/color0), and made
constructor/unexpected callback errors fatal rather than rejection credit.
Eight regression tests pass,including list callback reloads and rejection of
unrelated owner additions or altered prior observations.

Preserve BYTE arguments in WORD slots,all21 list entries,raw page wrap,live page
and pointer reloads after text callbacks (including nested lists),and all8,000
explicit DWORD snapshot iterations. DF does not change copy direction;source
WORD offsets wrap,source/destination overlap is live,and allocator AX0 is not
checked. Actual consecutive snapshot/free leaves the saved segment unchanged.

The original unaccepted draft and probe logs remain preserved under
`.analysis/work/op-music-state-draft/`;the current bound report is
`.analysis/work/op-music-state-build.json`. The original draft files are not
current proof. Containing Music producer CODE2,244/DATA1,008/BSS1,060 do not
receive wider ownership from this216-byte scope.

Next bounded work remains Music Room animation/menu,OP BSS initialization,
remaining MAINL score-data/context,ZUN ownership and the four-product
source/link graph. MAINL is the ending. Ending-to-roll aggregate composition
remains separate from individual function ownership.

## Proof boundaries to preserve

- OP entry owns all15 procedures/3,094 CODE and487 initialized DATA bytes.
  BSS6 starts exactly at decoded image end0E97A and is not file-backed.
  DATA consumers cover472 bytes with3,769 semantic bit controls. Type strings15
  remain static only in these fixtures;static-only does not mean unreachable.
  Unchecked story indices221/223/225/227 read unnamed spaces and reach a closed
  retry loop;229 reads their NUL and returns. Demo255 also aliases prior data.
- OP startup is far cdecl/noargs/RETF;init filename cleanup is caller4. Actual
  owned children share one UC. Root frames/new primitive stack bytes are checked;
  inherited windows remain main96,option64,wait/VS80. Held descendants retain
  full SP through intermediate frames. Short CFG/raw-dispatch prefixes are
  separate from returns. Keep natural `samecodeseg` relaxation. Prior complete
  observations remain bound to d118c46,dbf8a52 and9402601.
- MAINL staff TU owns19 procedures/3,695 CODE plus224 DATA. Whole roll returns
  execute257 input/199 fade iterations,32 frees and7,616,000 clear WORD callbacks,
  peak stack78,no ignored stack. No-input prefixes are separate. Native faults,
  raw BYTE/WORD aliases,live particle80/81 fields and SMC remain intentional.
  See the staff/resource verifiers and knowledge ledger for exact conditions.
- MAINL sound retains explicit trailing NOP/layout questions. ZUN reserved
  DATA3+9 bytes and vendor context remain open. Do not manufacture padding or
  empty segments. MAIN still differs at EC2D (target90/candidate00),
  headers6,240/7,680 bytes. Its complete ordered relocation vector now matches.

## Retained local state and commands

Keep fixed Japanese targets/assets (`candidate-local-attested`),the local Wine
prefix,TC4/TASM/JWasm,`.tools/ghidra`,`.tools/jdk`,`.venv`,
`_reference/ReC98` and `ghidra-project/`. Ghidra/JDK attest their entire trees,
including documentation/archives;do not trim them. Use Factory MCP repository
shell execution of these headless tools; no GUI tools. The user authorized the
Factory route on 2026-10-26. Preserve all target and acceptance checks.
One working build per product under Wine `drive_c/`:
`TH03WORK`, `TH03OP`, `TH03ML`, `TH03ZUN`.

Required actual source input:
`.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar`.
Keep `scripts/lib/zun.py` unchanged;MAIN pins it. OP's builder is a shared
MAINL/ZUN utility;real edits require fresh bound pairs. Current reports are
`.analysis/work/*-build.json` and `main-unit-review.json`.

```sh
th03_cpu=16  # choose an allowed CPU on another host
th03_run() {
  taskset -c "$th03_cpu" nice -n 10 env DISPLAY= WAYLAND_DISPLAY= \
    _JAVA_OPTIONS='-Xmx768m -XX:ActiveProcessorCount=1' .venv/bin/python "$@"
}
th03_run scripts/preflight.py
th03_run scripts/ghidra.py th03-op check
th03_run scripts/ci.py
git diff --check
```

Current full review chains: `review_th03_op_music_state_work.py`,
`review_th03_mainl_staff_roll_work.py`, `review_th03_zun_ongchk_work.py`.
`--current-cold` revalidates the entire unchanged native graph and reruns the
selected stage;it cannot repair stale prerequisites. Do not rebuild unchanged
products. Serialize Borland/Wine writers and preserve the prefix.

Old logs,experiments,caches,receipts and installer downloads are disposable;
references alone do not require retaining obsolete runs. Preserve actual current
inputs/builds/proofs and the explicitly retained Music Room draft. Use guarded
cleanup previews;`--caches-only --apply` leaves `.analysis` untouched.

Cleanup removed approximately1.9 MiB of obsolete logs/experiments/caches. The
Music Room draft,all guarded current proofs,required source archive and the four
working builds were retained. No accepted ledger or publication was changed.
