# TH03 handoff

Prepared 2026-10-26. Last committed reconstruction checkpoint: **`bcdf24a`**,
pushed on `main`; current HEAD before this resumed work is `a432dd8`.
The user resumed TH03 and authorized Factory MCP as the execution route.
The bounded Music Room state/track scope below now passes its full current
review and repository-local publication gates. Final CI is required before a
checkpoint; consult the latest session gate result.
No native source or builder changed; no commit or push has been made.

Read `AGENTS.md`, [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md)
and the local [th03-re skill](../.agents/skills/th03-re/SKILL.md) before resuming.
Detailed findings live in maintained source, `config/knowledge.csv`,
`config/evidence.csv`, tests and current review reports.

## Accepted state

| Product | Accepted source scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 445 functions / 75,317 CODE bytes / 98 extents | Open |
| OP | 34 extents / 36 procedures / 4,099 CODE + 487 DATA bytes | Open |
| MAINL | 54 extents / 59 procedures / 6,597 CODE + 224 DATA bytes | Open |
| ZUN | 77 extents / 89 procedures or entries / 6,179 CODE bytes | Open |

OP includes22 separately proved inline compiler bytes. ZUN accepts8,635
CODE+DATA bytes:authored2,179, original ASM1,390, library5,066. Whole-game
source/function denominators and a completion percentage remain unknown.

OP/MAINL/ZUN current source-only cold pairs repeat all outputs and match complete
decoded and canonical DIET `-B` stored targets. Unowned reference/vendor context
is still present; this does not prove whole-product source ownership. MAIN
repeats101 outputs/99 objects but its whole file/header/relocation order differs.

Publications: `config/{op_work,mainl_work,zun_work}/scoped_acceptance.json`.
Generated accounting: [PROGRESS.md](PROGRESS.md), `resources/progress.svg`.
Inherited post-cleanup CI: **2,413 tests,284 optional archive skips,all checks
passed**;10m01s/about572 MiB peak RSS/no swap,CPU16/nice10.

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
remaining MAINL cutscene/registration,ZUN ownership and the four-product
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
  empty segments. MAIN still differs at EC2D and1DB05 (target90/candidate00),
  headers6,240/7,680 bytes,and ordered relocation record1072 onward.

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
