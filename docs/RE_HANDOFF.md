# TH03 handoff

Prepared 2026-10-26. Accepted reconstruction checkpoint: **`bcdf24a`**, pushed
on `main`. Music Room work after that checkpoint is an unaccepted private draft.
The reconstruction goal was cleared; no reconstruction probe remains running.

Read `AGENTS.md`, [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md)
and the local [th03-re skill](../.agents/skills/th03-re/SKILL.md) before resuming.
Detailed findings live in maintained source, `config/knowledge.csv`,
`config/evidence.csv`, tests and current review reports.

## Accepted state

| Product | Accepted source scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 445 functions / 75,317 CODE bytes / 98 extents | Open |
| OP | 33 extents / 32 procedures / 3,883 CODE + 487 DATA bytes | Open |
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
Post-cleanup CI: **2,413 tests,284 optional archive skips,all checks
passed**;10m01s/about572 MiB peak RSS/no swap,CPU16/nice10.

## Next work: Music Room draft

Preserved locally in **`.analysis/work/op-music-state-draft/`**:

- `README.txt`: exact observations, failed control and remaining gates.
- `op_music_state_layout.py`, `op_music_state_runtime.py`: provisional modules;
  restore both to `scripts/lib/` before running them.
- Native instruction/field dump and four-function/matrix/control probe logs.

No draft source was promoted into the product, ledgers or publications.
The maintained Music Room source already exists in `src/op/music/` as three
bounded includes. Its natural `th03/op_music.cpp` producer contains2,244 CODE,
1,008 DATA and1,060 BSS bytes. The next existing ledger unit is
`th03-op-decoded-music-state-and-tracks`:complete216 CODE bytes/four procedures
at0990:0C1E,with12 ordered native fields and4 ordered MZ relocations.

Draft layout passed. One target/load3000 runtime passed889 cases plus two actual
snapshot/free pairs and executed all216 bytes. This is **not** a complete
acceptance review. The negative-control run stopped at `page-field`:mutating
2039->2038 survives page0 because the adjacent byte is also0. Make that fixture
discriminate behavior,then audit remaining controls,constructor-failure handling,
both images/two loads and complete cold/SDK/source bindings.

Preserve BYTE arguments in WORD slots,all21 list entries,raw page wrap,live page
and pointer reloads after text callbacks,and all8,000 explicit DWORD snapshot
iterations. DF does not change that copy's direction;source WORD offsets wrap,
source/destination overlap is live,and allocator AX0 is not checked. Actual
producer SDK inputs include `mem.h`,outside the current CFG five-header set.

Subsequent scope remains Music Room animation/menu,OP BSS initialization,
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
including documentation/archives;do not trim them. No Factory MCP or GUI tools.
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

Current full review chains: `review_th03_op_entry_data_work.py`,
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
